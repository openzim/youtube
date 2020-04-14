#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

""" Kiwix/OpenZIM S3 interface

    helpers for S3 storage, autoconf from URL + Wasabi (wasabisys.com) extras

    Goal is mainly to provide a configured s3.client and s3.resource from an URL
    Users could limit usage to this and use boto3 directly from there.

    A few additional wrappers are in place to simplify common actions.
    Also, non-S3, wasabi-specific features are exposed directly.

    Example usage:

    url = "https://s3.us-west-1.wasabisys.com/?keyId=x&secretAccessKey=y&bucketName=z"
    s3 = KiwixStorage(url)
    if not s3.check_credentials(failsafe=True):
        return # bad auth

    ### typical scraper use case

    online_url = "https://xxx"
    fpath = "/local/path.ext"
    # retrieve origin etag
    etag = req.headers.get("Etag")
    # check if we have that very same version in store
    if s3.has_matching_object(key=url, etag=etag)
        # lastest version in our store, download from there (using progress output)
        s3.download_file(key=url, fpath=fpath, progress=True)
    else:
        # download the origin file using your regular tools
        download_file(url, fpath)
        # upload it our storage
        s3.upload_file(fpath=fpath, key=url)
    # now you have a local file of lastest version and the storage is up to date

    # other use cases

    # create a bucket
    bucket = s3.create_bucket()
    # set auto-delete on bucket
    s3.set_bucket_autodelete_after(nb_days=7)
    # allow public downloads from bucket
    s3.allow_public_downloads_on()
    # upload a file
    s3.upload_file(fpath, "some/path/file.img", meta={"ENCODER_VERSION": "v1"})
    # set autodelete on specific file
    s3.set_object_autodelete_on(key, datetime.datetime.now())
    # download a file
    s3.download_file(key, fpath)
    # get URL for external download
    s3.get_download_url(key)

    Resources:
        https://wasabi.com/wp-content/themes/wasabi/docs/API_Guide
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html

    """

import sys
import uuid
import json
import urllib
import pathlib
import hashlib
import logging
import datetime
import threading

import boto3
import botocore
import requests
from aws_requests_auth.aws_auth import AWSRequestsAuth  # aws-requests-auth==0.4.2

logger = logging.getLogger(__name__)


class TransferHook(object):
    """ Generic transfer hook based on size """

    def __init__(
        self,
        size=-1,
        output=sys.stdout,
        flush=None,
        name="",
        fmt="\r{progress} / {total} ({percentage:.2f}%)",
    ):
        self.size = size
        self.output = output
        if flush is None and getattr(output, "name") in ("<stdout>", "<stderr>"):
            flush = True
        self.flush = bool(flush)
        self.name = name
        self.fmt = fmt
        self.seen_so_far = 0

    def __call__(self, bytes_amount):
        self.seen_so_far += bytes_amount
        if self.size > 0:
            total = self.size
            percentage = (self.seen_so_far / self.size) * 100
        else:
            total = "?"
            percentage = 0
        self.output.write(
            self.fmt.format(
                name=self.name,
                progress=self.seen_so_far,
                total=total,
                percentage=percentage,
            )
        )
        if self.flush:
            self.output.flush()


class FileTransferHook(TransferHook):
    """ Sample progress report hook printing to STDOUT """

    def __init__(
        self,
        filename,
        output=sys.stdout,
        flush=None,
        fmt="\r{name} {progress} / {total} ({percentage:.2f}%)",
    ):
        super().__init__(
            size=float(pathlib.Path(filename).stat().st_size),
            output=output,
            flush=flush,
            fmt=fmt,
        )
        self.name = filename
        self.lock = threading.Lock()

    def __call__(self, bytes_amount):
        with self.lock:
            super().__call__(bytes_amount)


class HeadStat(object):
    """ easy access to useful object properties """

    def __init__(self, data={}):
        self.data = data

    def __dict__(self):
        return ", ".join(
            [
                f"{k}={getattr(self, k)}"
                for k in ("mtime", "size", "etag", "type", "meta")
            ]
        )

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__()})"

    def __str__(self):
        return str(self.__repr__())

    @property
    def mtime(self):
        return self.data.get("LastModified")

    @property
    def size(self):
        return self.data.get("ContentLength")

    @property
    def etag(self):
        return self.data.get("ETag")

    @property
    def type(self):
        return self.data.get("ContentType")

    @property
    def meta(self):
        return self.data.get("Metadata")


class AuthenticationError(Exception):
    pass


class NotFoundError(Exception):
    pass


class KiwixStorage(object):

    BUCKET_NAME = "bucketname"
    KEY_ID = "keyid"
    SECRET_KEY = "secretaccesskey"
    ENDPOINT_URL = "endpoint_url"

    EXTRA_ARGS_KEY = "ExtraArgs"
    META_KEY = "Metadata"  # insde ExtraArgs or head response
    CALLBACK_KEY = "Callback"

    # JSON polcy template
    PUBLIC_ACCESS_POLICY = """{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowPublicDownloads",
      "Effect": "Allow",
      "Principal": "*",
      "Action": ["s3:GetObject"],
      "Resource": "arn:aws:s3:::{bucket_name}/*"
    }
  ]
}
"""

    def __init__(self, url, **kwargs):
        self._resource = self._bucket = None
        self._params = {}
        self._parse_url(url, **kwargs)

    def _parse_url(self, url, **kwargs):
        try:
            self.url = urllib.parse.urlparse(url)
            env = {
                k.lower(): v for k, v in urllib.parse.parse_qs(self.url.query).items()
            }

            env["endpoint_url"] = f"{self.url.scheme}://{self.url.netloc}"
            for key in (self.KEY_ID, self.SECRET_KEY, self.BUCKET_NAME):
                env[key] = env.get(key, [None])[-1]
        except Exception as exc:
            raise ValueError(f"Incorrect URL: {exc}")
        self._params.update(env)
        self._params.update(kwargs)

    @property
    def params(self):
        """ dict of query parameters from URL """
        return self._params

    @property
    def bucket_name(self):
        """ bucket name set in URL """
        return self.params.get(self.BUCKET_NAME)

    @property
    def is_wasabi(self):
        return self.url.hostname.endswith("wasabisys.com")

    @property
    def wasabi_url(self):
        return f"https://{self.url.netloc}"

    @property
    def client(self):
        """ Configured boto3 client """
        return self.resource.meta.client

    @property
    def aws_auth(self):
        """ requests-compatible AWS authentication plugin """
        return self.get_aws_auth_for(
            access_key_id=self.params.get(self.KEY_ID),
            secret_access_key=self.params.get(self.SECRET_KEY),
            host=self.url.netloc,
        )

    @property
    def resource(self):
        if self._resource is None:
            self._resource = self.get_resource()
        return self._resource

    def get_resource(self):
        """ Configured boto3.resource('s3') """
        try:
            return boto3.resource(
                "s3",
                aws_access_key_id=self.params.get(self.KEY_ID),
                aws_secret_access_key=self.params.get(self.SECRET_KEY),
                endpoint_url=self.params.get(self.ENDPOINT_URL),
            )
        except Exception as exc:
            raise AuthenticationError(str(exc))

    def test_access_list_buckets(self):
        self.client.list_buckets()

    def test_access_bucket(self, bucket_name=None):
        bucket_name = self._bucket_name_param(bucket_name)
        if not bucket_name:
            raise ValueError("Can't test for bucket without a bucket name")
        if self.get_bucket(bucket_name).creation_date is None:
            raise AuthenticationError("Bucket doesn't exist of not reachable")

    def test_access_write(self, key=None, bucket_name=None, check_read=False):
        bucket_name = self._bucket_name_param(bucket_name)
        if not bucket_name:
            raise ValueError("Can't test for write without a bucket name")
        if key is None:
            key = f"{uuid.uuid4().hex}/{uuid.uuid4().hex}"
        self.put_text_object(key, key, bucket_name=bucket_name)

        try:
            if check_read:
                self.test_access_read(key, bucket_name)
        except Exception as exc:
            raise exc
        finally:
            self.client.delete_object(Bucket=self.bucket_name, Key=key)

    def test_access_read(self, key, bucket_name=None):
        bucket_name = self._bucket_name_param(bucket_name)
        if not bucket_name:
            raise ValueError("Can't test for read without a bucket name")
        if self.has_object(key):
            self.get_object_head(key)
        else:
            raise ValueError(f"Can't test read with missing key: {key}")

    def check_credentials(
        self, list_buckets=False, bucket=False, write=None, read=None, failsafe=False
    ):
        """ ensures your credentials allows some common actions

            list_buckets (bool): test for bucket listing access
            bucket (bool): test for access to bucket
            bucket (str): test for access to a different bucket (than URL)
            write (bool): test for write access to bucket
            write (str) test for write access on a specific key
            read (bool) test for read access on written object (only if write)
            read (str): test for read access on specific key """
        if not list_buckets and not bucket and not write and not read:
            raise ValueError("Nothing to test your credentials over.")
        try:
            self.client  # make sure this didn't fail

            if list_buckets:
                self.test_access_list_buckets()

            bucket_name = bucket if isinstance(bucket, str) else None

            if bucket:
                self.test_access_bucket(bucket_name=bucket_name)

            if write:
                self.test_access_write(
                    key=write if isinstance(write, str) else None,
                    bucket_name=bucket_name,
                    check_read=read is True,
                )

            if read and (read is not True or not write):
                self.test_access_read(
                    read=str(read), bucket_name=bucket_name,
                )
        except AuthenticationError as exc:
            if failsafe:
                return False
            raise exc
        return True

    def _bucket_name_param(self, bucket_name=None):
        """ passed bucket_name if defined else self.bucket_name

            Used to easily use provided param if present & default to configured one"""
        if bucket_name is None and not self.bucket_name:
            raise ValueError("No bucket_name supplied (not in params nor url)")
        return self.bucket_name if bucket_name is None else bucket_name

    @property
    def bucket(self):
        if not self.bucket_name:
            return NotFoundError("No bucket specified")

        if self._bucket is None:
            self._bucket = self.get_bucket()
        return self._bucket

    def bucket_exists(self, bucket_name=None):
        """ whether bucket exists on server """
        bucket_name = self._bucket_name_param(bucket_name)
        return bucket_name in [b["Name"] for b in self.client.list_buckets()["Buckets"]]

    def get_bucket(self, bucket_name=None, must_exists=False):
        """ s3.Bucket()a from URL or param """
        bucket_name = self._bucket_name_param(bucket_name)

        if must_exists and not self.bucket_exists(bucket_name):
            raise ValueError(f"Bucket `{bucket_name} does not exists or not reachable")

        return self.resource.Bucket(bucket_name)

    def create_bucket(self, bucket_name, **kwargs):
        bucket_name = self._bucket_name_param(bucket_name)
        if self.bucket_exists(bucket_name):
            raise ValueError(f"Bucket {bucket_name} already exists.")

        return self.client.create_bucket(Bucket=bucket_name, **kwargs)

    def has_object(self, key, bucket_name=None):
        bucket_name = self._bucket_name_param(bucket_name)
        try:
            self.get_object_head(key, bucket_name)
        except botocore.exceptions.ClientError as e:
            error_code = int(e.response["Error"]["Code"])
            if error_code == 403:
                raise AuthenticationError(f"Authorization Error testing key={key}")
            elif error_code == 404:
                return False
        return True

    def has_object_matching_etag(self, key, etag, bucket_name=None):
        bucket_name = self._bucket_name_param(bucket_name)
        try:
            s3_etag = self.get_object_etag(key, bucket_name)
        except botocore.exceptions.ClientError as e:
            error_code = int(e.response["Error"]["Code"])
            if error_code == 403:
                raise AuthenticationError(f"Authorization Error testing key={key}")
            elif error_code == 404:
                return False
        return etag == s3_etag

    def has_object_matching_meta(self, key, tag, value, bucket_name=None):
        bucket_name = self._bucket_name_param(bucket_name)
        try:
            (meta,) = self.get_object_head(key, bucket_name, only=[self.META_KEY])
        except botocore.exceptions.ClientError as e:
            error_code = int(e.response["Error"]["Code"])
            if error_code == 403:
                raise AuthenticationError(f"Authorization Error testing key={key}")
            elif error_code == 404:
                return False

        return meta.get(tag) == value

    def get_object(self, key, bucket_name=None):
        bucket_name = self._bucket_name_param(bucket_name)
        return self.resource.Object(bucket_name=bucket_name, key=key)

    def get_object_head(self, key, bucket_name=None, unserialize_etag=True, only=None):
        bucket_name = self._bucket_name_param(bucket_name)
        response = self.client.head_object(Bucket=bucket_name, Key=key)
        if unserialize_etag and "ETag" in response.keys():
            response["ETag"] = json.loads(response["ETag"])
        if only is not None:
            return [value for key, value in response.items() if key in only]
        return response

    def get_object_stat(self, key, bucket_name=None):
        bucket_name = self._bucket_name_param(bucket_name)
        return HeadStat(self.get_object_head(key, bucket_name))

    def get_object_etag(self, key, bucket_name=None):
        bucket_name = self._bucket_name_param(bucket_name)
        return self.get_object_stat(key, bucket_name).etag

    def put_text_object(self, key, content, bucket_name=None, **kwargs):
        """ records a simple text file """
        bucket_name = self._bucket_name_param(bucket_name)
        self.client.put_object(
            Bucket=bucket_name, Key=key, Body=content.encode("UTF-8"), **kwargs
        )

    def allow_public_downloads_on(self, bucket_name=None):
        """ sets policy on bucket to allow anyone to GET objects (downloads)

            TODO: add this policy instead of overwriting everything """
        if not self.is_wasabi:
            raise NotImplementedError("Only Wasabi at the moment.")

        bucket_name = self._bucket_name_param(bucket_name)
        policy = self.PUBLIC_ACCESS_POLICY.replace("{bucket_name}", bucket_name)
        self.get_bucket(bucket_name).Policy().put(Policy=policy)

    def set_bucket_autodelete_after(self, nb_days, bucket_name=None):
        """ apply compliance setting RetentionDays and DeleteAfterRetention """
        if not self.is_wasabi:
            raise NotImplementedError("Only Wasabi at the moment")

        bucket_name = self._bucket_name_param(bucket_name)
        compliance = "<BucketComplianceConfiguration>\n\t<Status>enabled</Status>\n\t<LockTime>off</LockTime>\n\t<RetentionDays>{nb_days}</RetentionDays>\n\t<DeleteAfterRetention>true</DeleteAfterRetention>\n</BucketComplianceConfiguration>".format(
            nb_days=nb_days
        )
        return self.set_wasabi_compliance(compliance, key=None, bucket_name=bucket_name)

    def set_object_autodelete_on(self, key, on, bucket_name=None):
        """ apply compliance setting RetentionTime

             """
        if not self.is_wasabi:
            raise NotImplementedError("Only Wasabi at the moment")

        if on.tzinfo != datetime.timezone.utc:
            on = on.astimezone(datetime.timezone.utc)
        bucket_name = self._bucket_name_param(bucket_name)
        compliance = "<ObjectComplianceConfiguration>\n\t<ConditionalHold>false</ConditionalHold>\n\t<RetentionTime>{retention_time}</RetentionTime>\n</ObjectComplianceConfiguration>".format(
            retention_time=on.isoformat(timespec="seconds").replace("+00:00", "Z")
        )
        return self.set_wasabi_compliance(compliance, key=key, bucket_name=bucket_name)

    def delete_bucket(self, bucket_name=None, force=False):
        """ delete a bucket

            force (bool) only for Wasabi: delete even if there are objects in bucket """
        bucket_name = self._bucket_name_param(bucket_name)
        if not force:
            return self.client.delete_bucket(Bucket=bucket_name)

        if not self.is_wasabi:
            raise NotImplementedError("Only Wasabi allows force delete")

        url = f"{self.wasabi_url}/{bucket_name}?force_delete=true"
        req = requests.delete(url, auth=self.aws_auth)
        req.raise_for_status()

    def rename_bucket(self, new_bucket_name, bucket_name=None):
        """ change name or a bucket """
        if not self.is_wasabi:
            raise NotImplementedError("Only Wasabi allows bucket rename")

        bucket_name = self._bucket_name_param(bucket_name)
        url = f"{self.wasabi_url}/{bucket_name}"
        req = requests.request(
            "MOVE", url, headers={"Destination": new_bucket_name}, auth=self.aws_auth
        )
        req.raise_for_status()
        return req.text

    def rename_objects(
        self, key, new_key, overwrite=False, as_prefix=False, bucket_name=None
    ):
        """ change key of an object or list of objects

            overwrite (bool) whether to overwrite destination
            as_prefix (bool) rename whole bucket keys starting with `key`
             and replacing this part with `new_key` """
        if not self.is_wasabi:
            raise NotImplementedError("Only Wasabi allows objects rename")

        bucket_name = self._bucket_name_param(bucket_name)
        url = f"{self.wasabi_url}/{bucket_name}/{key}"
        req = requests.request(
            "MOVE",
            url,
            auth=self.aws_auth,
            headers={
                "Destination": new_key,
                "Overwrite": "true" if overwrite else "false",
                "X-Wasabi-Quiet": "true",
                "X-Wasabi-Prefix": "true" if as_prefix else "false",
            },
        )
        req.raise_for_status()
        return req.text

    @staticmethod
    def get_aws_auth_for(
        access_key_id,
        secret_access_key,
        # host="s3.wasabisys.com",  # was "s3.us-west-1.wasabisys.com"
        host="s3.us-west-1.wasabisys.com",  # was "s3.us-west-1.wasabisys.com"
        region="",  # "us-east-1",  # was ""
        service="s3",
    ):
        """ prepares AWS Signature v4 headers for requests

            Sets: Authorization, x-amz-date and x-amz-content-sha256 """
        return AWSRequestsAuth(
            aws_access_key=access_key_id,
            aws_secret_access_key=secret_access_key,
            aws_host=host,
            aws_region=region,
            aws_service=service,
        )

    def set_wasabi_compliance(self, compliance, key=None, bucket_name=None):
        """ apply a compliance to a bucket of object """
        if not self.is_wasabi:
            raise NotImplementedError("Only Wasabi feature")

        url = f"{self.wasabi_url}/{bucket_name}"
        if key is not None:
            url += f"/{key}"
        url += "?compliance"
        req = requests.put(url=url, auth=self.aws_auth, data=compliance)
        req.raise_for_status()
        return req

    def _mix_kwargs(
        self,
        meta=None,
        progress=False,
        progress_size=None,
        progress_fpath=None,
        **kwargs,
    ):
        """ parse and mix shortcut args with boto3 ones

            meta (dict): sets Metadata
            progress (bool): enables default progress report
            progress (callable): custom progress report hook
            progress_size: sets size for auto progress reporter
            progress_fpath: sets fpath for auto progress reporter
            """
        if meta:
            if self.EXTRA_ARGS_KEY not in kwargs:
                kwargs[self.EXTRA_ARGS_KEY] = {}
            if self.META_KEY not in kwargs[self.EXTRA_ARGS_KEY]:
                kwargs[self.EXTRA_ARGS_KEY][self.META_KEY] = {}
            kwargs[self.EXTRA_ARGS_KEY][self.META_KEY].update(meta)

        if progress and self.CALLBACK_KEY not in kwargs:
            if callable(progress):
                kwargs[self.CALLBACK_KEY] = progress
            else:  # auto-size mode
                if progress_fpath:
                    kwargs[self.CALLBACK_KEY] = FileTransferHook(progress_fpath)
                elif progress_size:
                    kwargs[self.CALLBACK_KEY] = TransferHook(size=progress_size)
                else:
                    kwargs[self.CALLBACK_KEY] = TransferHook()
        return kwargs

    def upload_file(
        self, fpath, key, bucket_name=None, meta=None, progress=False, **kwargs
    ):
        """ upload a file to the bucket

            meta (dict): metadata for the object
            progress (bool): enable default progress report
            progress (callable): your own progress report callback """
        bucket = self.get_bucket(bucket_name) if bucket_name else self.bucket
        kwargs = self._mix_kwargs(
            meta=meta, progress=progress, progress_fpath=fpath, **kwargs
        )
        print(kwargs)
        bucket.upload_file(Filename=str(fpath), Key=key, **kwargs)

    def download_file(self, key, fpath, bucket_name=None, progress=False, **kwargs):
        """ download object to fpath using boto3

            progress (bool): enable default progress report
            progress (callable): your own progress report callback """
        bucket_name = self._bucket_name_param(bucket_name)
        size = self.get_object_stat(key, bucket_name).size if progress is True else None
        kwargs = self._mix_kwargs(progress=progress, progress_size=size, **kwargs)
        self.resource.Bucket(bucket_name).download_file(
            Key=key, Filename=str(fpath), **kwargs
        )

    def get_download_url(self, key, bucket_name=None, prefer_torrent=True):
        """ URL of object for external download

            torrent is a shortcut for calling {key}.torrent which is the uploader's
            responsibility to create.
            if testing this torrent file key results in 404, fallback to {key}.

            this is not using GetObjectTorrent as it is limited to 5G on AWS
            and not supported at all on Wasabi. """
        bucket_name = self._bucket_name_param(bucket_name)
        torrent_key = f"{key}.torrent"
        if prefer_torrent and self.has_object(torrent_key, bucket_name):
            return self.get_download_url(torrent_key, bucket_name, prefer_torrent=False)

        return f"https://{self.url.netloc}/{bucket_name}/{key}"

    def validate_file_etag(self, fpath: pathlib.Path, etag: str):
        """ Validates a server ETag matches a local file

            Using recipe from https://teppen.io/2018/10/23/aws_s3_verify_etags/ """

        def factor_of_1MB(filesize, num_parts):
            x = filesize / int(num_parts)
            y = x % 1048576
            return int(x + 1048576 - y)

        def possible_partsizes(filesize, num_parts):
            return (
                lambda partsize: partsize < filesize
                and (float(filesize) / float(partsize)) <= num_parts
            )

        def calc_etag(fpath, partsize):
            md5_digests = []
            with open(fpath, "rb") as f:
                for chunk in iter(lambda: f.read(partsize), b""):
                    md5_digests.append(hashlib.md5(chunk).digest())
            return (
                hashlib.md5(b"".join(md5_digests)).hexdigest()
                + "-"
                + str(len(md5_digests))
            )

        def md5sum(fpath):
            h = hashlib.md5()
            with open(fpath, "rb") as f:
                for chunk in iter(lambda: f.read(2 ** 20 * 8), b""):
                    h.update(chunk)
            return h.hexdigest()

        filesize = fpath.stat().st_size
        num_parts = etag.rsplit("-", 1)[-1]
        if not num_parts.isnumeric():
            num_parts = 1
        num_parts = int(num_parts)

        if num_parts == 1:
            return md5sum(fpath) == etag

        partsizes = [
            8388608,  # aws_cli/boto3
            15728640,  # s3cmd
            factor_of_1MB(filesize, num_parts),  # many clients to upload large files
        ]

        for partsize in filter(possible_partsizes(filesize, num_parts), partsizes):
            if etag == calc_etag(fpath, partsize):
                return True

        return False


def cache_found():
    url = "https://s3.eu-central-1.wasabisys.com/?keyId=D5W1LBOSAV7GT0VL80HO&secretAccessKey=IPCYjVRhAuXeAHsmnsmznIsz2yB1CWO4ECBHM0yQ&bucketName=testbucket-nabin"
    s3 = KiwixStorage(url)
    s3.upload_file("ngrams.csv", "/Users/nabin/Desktop/testing.csv.txt")


if __name__ == '__main__':
    cache_found()
