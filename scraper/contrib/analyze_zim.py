#!/usr/bin/env python3
from __future__ import annotations

# usage = python analyze_zim.py /path/to/file1.zim /path/to/file2.zim
import json
import sys

import isodate
from libzim.reader import Archive


def analyze_zim(path: str):
    archive = Archive(path)
    entry = archive.get_entry_by_path("home_playlists.json")
    data = json.loads(bytes(entry.get_item().content))

    videos = {}  # dedupe across playlists
    for playlist in data.get("playlists", []):
        for v in playlist.get("videos", []):
            vid = v.get("id", "")
            if not vid or vid in videos:
                continue
            dur = isodate.parse_duration(v.get("duration", "PT0S")).total_seconds()
            size = None
            for ext in ("webm", "mp4"):
                try:
                    size = (
                        archive.get_entry_by_path(f"videos/{vid}/video.{ext}")
                        .get_item()
                        .size
                    )
                    break
                except KeyError:
                    pass
            if size and dur > 0:
                videos[vid] = (v.get("slug", ""), dur, size)

    return videos


def main():
    min_args = 2
    if len(sys.argv) < min_args:
        print(f"Usage: {sys.argv[0]} <zim_file> [<zim_file> ...]")  # noqa: T201
        sys.exit(1)

    all_ratios = []

    for zim_path in sys.argv[1:]:
        print(f"  {zim_path}")  # noqa: T201

        videos = analyze_zim(zim_path)
        ratios = []

        for slug, dur, size in videos.values():
            mb = size / (1024 * 1024)
            mins = dur / 60
            ratio = mb / mins
            ratios.append(ratio)
            print(  # noqa: T201
                f"  {slug[:50]:<50s}  {mins:6.1f}min  {mb:7.1f}MB  {ratio:5.2f} MB/min"
            )

        if ratios:
            avg = sum(ratios) / len(ratios)
            ratios.sort()
            median = ratios[len(ratios) // 2]
            std = (sum((r - avg) ** 2 for r in ratios) / len(ratios)) ** 0.5
            print(  # noqa: T201
                f"\n  {len(ratios)} videos — avg {avg:.2f} MB/min, "
                f"median {median:.2f}, std {std:.2f}"
            )
            all_ratios.extend(ratios)

    if all_ratios:
        avg = sum(all_ratios) / len(all_ratios)
        std = (sum((r - avg) ** 2 for r in all_ratios) / len(all_ratios)) ** 0.5
        all_ratios.sort()
        median = all_ratios[len(all_ratios) // 2]
        print(  # noqa: T201
            f"  OVERALL ({len(all_ratios)} videos across {len(sys.argv)-1} ZIMs)"
        )
        print(  # noqa: T201
            f"  1 min of YouTube ≈ {avg:.2f} MB in ZIM  "
            f"(±{std:.2f}, median {median:.2f})"
        )


if __name__ == "__main__":
    main()
