
var OGVDemuxerOggW = (function() {
  var _scriptDir = typeof document !== 'undefined' && document.currentScript ? document.currentScript.src : undefined;
  return (
function(OGVDemuxerOggW) {
  OGVDemuxerOggW = OGVDemuxerOggW || {};


if (typeof zim_fix_wasm_target === 'undefined') {
    IS_IN_ZIM = self.location.href.indexOf("/-/") != -1 || self.location.href.indexOf("/I/") != -1 || self.location.href.indexOf("/A/") != -1;
    ZIM_IMG_NS = (IS_IN_ZIM) ? '../../../I/' : '';
    hasImageNamespacePrefix = function(target) { return target.indexOf("/I/") != -1; }
    hasMetaNamespacePrefix = function(target) { return target.indexOf("/-/") != -1; }
    changeNamespacePrefix = function(target, new_ns) { return target.replace("/-/", new_ns); }
    zim_fix_wasm_target = function(target) {
        console.debug("in-file zim_fix_wasm_target:", target);
        if (!IS_IN_ZIM) {
            console.debug("..not in zim");
            return target;
        }
        if (hasImageNamespacePrefix(target)) {
            // we already have a good path, leave it
        }
        else if (hasMetaNamespacePrefix(target)) {
            // we have a prefix, just replace it
            target = changeNamespacePrefix(target, "I");
        }
        else {
            // we lack the prefix, add it
            target = ZIM_IMG_NS + "assets/ogvjs/" + target;
        }
        console.debug("..target:", target);
        return target;
    }
  }

var a;a||(a=typeof OGVDemuxerOggW !== 'undefined' ? OGVDemuxerOggW : {});var aa=a;a.memoryLimit&&(a.TOTAL_MEMORY=aa.memoryLimit);var f={},g;for(g in a)a.hasOwnProperty(g)&&(f[g]=a[g]);a.arguments=[];a.thisProgram="./this.program";a.quit=function(b,c){throw c;};a.preRun=[];a.postRun=[];var l=!1,n=!1,p=!1,q=!1;l="object"===typeof window;n="function"===typeof importScripts;p="object"===typeof process&&"function"===typeof require&&!l&&!n;q=!l&&!p&&!n;var r="";
if(p){r=__dirname+"/";var t,u;a.read=function(b,c){t||(t=require("fs"));u||(u=require("path"));b=u.normalize(b);b=t.readFileSync(b);return c?b:b.toString()};a.readBinary=function(b){b=a.read(b,!0);b.buffer||(b=new Uint8Array(b));b.buffer||x("Assertion failed: undefined");return b};1<process.argv.length&&(a.thisProgram=process.argv[1].replace(/\\/g,"/"));a.arguments=process.argv.slice(2);process.on("unhandledRejection",x);a.quit=function(b){process.exit(b)};a.inspect=function(){return"[Emscripten Module object]"}}else if(q)"undefined"!=
typeof read&&(a.read=function(b){return read(b)}),a.readBinary=function(b){if("function"===typeof readbuffer)return new Uint8Array(readbuffer(b));b=read(b,"binary");"object"===typeof b||x("Assertion failed: undefined");return b},"undefined"!=typeof scriptArgs?a.arguments=scriptArgs:"undefined"!=typeof arguments&&(a.arguments=arguments),"function"===typeof quit&&(a.quit=function(b){quit(b)});else if(l||n)n?r=self.location.href:document.currentScript&&(r=document.currentScript.src),_scriptDir&&(r=_scriptDir),
0!==r.indexOf("blob:")?r=r.substr(0,r.lastIndexOf("/")+1):r="",a.read=function(b){var c=new XMLHttpRequest;c.open("GET",b,!1);c.send(null);return c.responseText},n&&(a.readBinary=function(b){var c=new XMLHttpRequest;c.open("GET",b,!1);c.responseType="arraybuffer";c.send(null);return new Uint8Array(c.response)}),a.readAsync=function(b,c,d){var e=new XMLHttpRequest;e.open("GET",b,!0);e.responseType="arraybuffer";e.onload=function(){200==e.status||0==e.status&&e.response?c(e.response):d()};e.onerror=
d;e.send(null)},a.setWindowTitle=function(b){document.title=b};var A=a.print||("undefined"!==typeof console?console.log.bind(console):"undefined"!==typeof print?print:null),B=a.printErr||("undefined"!==typeof printErr?printErr:"undefined"!==typeof console&&console.warn.bind(console)||A);for(g in f)f.hasOwnProperty(g)&&(a[g]=f[g]);f=void 0;var ba={"f64-rem":function(b,c){return b%c},"debugger":function(){debugger}};"object"!==typeof WebAssembly&&B("no native wasm support detected");
var C,ca=!1,da="undefined"!==typeof TextDecoder?new TextDecoder("utf8"):void 0;"undefined"!==typeof TextDecoder&&new TextDecoder("utf-16le");function D(b){0<b%65536&&(b+=65536-b%65536);return b}var buffer,E,F,G;function ea(){a.HEAP8=E=new Int8Array(buffer);a.HEAP16=new Int16Array(buffer);a.HEAP32=G=new Int32Array(buffer);a.HEAPU8=F=new Uint8Array(buffer);a.HEAPU16=new Uint16Array(buffer);a.HEAPU32=new Uint32Array(buffer);a.HEAPF32=new Float32Array(buffer);a.HEAPF64=new Float64Array(buffer)}
var H=a.TOTAL_MEMORY||16777216;5242880>H&&B("TOTAL_MEMORY should be larger than TOTAL_STACK, was "+H+"! (TOTAL_STACK=5242880)");a.buffer?buffer=a.buffer:"object"===typeof WebAssembly&&"function"===typeof WebAssembly.Memory?(C=new WebAssembly.Memory({initial:H/65536}),buffer=C.buffer):buffer=new ArrayBuffer(H);ea();G[1700]=5249712;
function I(b){for(;0<b.length;){var c=b.shift();if("function"==typeof c)c();else{var d=c.I;"number"===typeof d?void 0===c.F?a.dynCall_v(d):a.dynCall_vi(d,c.F):d(void 0===c.F?null:c.F)}}}var fa=[],ha=[],ia=[],ja=[],la=!1;function qa(){var b=a.preRun.shift();fa.unshift(b)}var J=0,K=null,L=null;a.preloadedImages={};a.preloadedAudios={};
function ra(){var b=M;return String.prototype.startsWith?b.startsWith("data:application/octet-stream;base64,"):0===b.indexOf("data:application/octet-stream;base64,")}var M="ogv-demuxer-ogg-wasm.wasm";if(!ra()){var sa=M;M=a.locateFile?a.locateFile(sa,r):r+sa;M=zim_fix_wasm_target(M);}function ta(){try{if(a.wasmBinary)return new Uint8Array(a.wasmBinary);if(a.readBinary)return a.readBinary(M);throw"both async and sync fetching of the wasm failed";}catch(b){x(b)}}
function ua(){return a.wasmBinary||!l&&!n||"function"!==typeof fetch?new Promise(function(b){b(ta())}):fetch(M,{credentials:"same-origin"}).then(function(b){if(!b.ok)throw"failed to load wasm binary file at '"+M+"'";return b.arrayBuffer()}).catch(function(){return ta()})}
function va(b){function c(b){a.asm=b.exports;J--;a.monitorRunDependencies&&a.monitorRunDependencies(J);0==J&&(null!==K&&(clearInterval(K),K=null),L&&(b=L,L=null,b()))}function d(b){c(b.instance)}function e(b){return ua().then(function(b){return WebAssembly.instantiate(b,k)}).then(b,function(b){B("failed to asynchronously prepare wasm: "+b);x(b)})}var k={env:b,global:{NaN:NaN,Infinity:Infinity},"global.Math":Math,asm2wasm:ba};J++;a.monitorRunDependencies&&a.monitorRunDependencies(J);if(a.instantiateWasm)try{return a.instantiateWasm(k,
c)}catch(y){return B("Module.instantiateWasm callback failed with error: "+y),!1}(function(){return a.wasmBinary||"function"!==typeof WebAssembly.instantiateStreaming||ra()||"function"!==typeof fetch?e(d):WebAssembly.instantiateStreaming(fetch(M,{credentials:"same-origin"}),k).then(d,function(b){B("wasm streaming compile failed: "+b);B("falling back to ArrayBuffer instantiation");e(d)})})();return{}}
a.asm=function(b,c){c.memory=C;c.table=new WebAssembly.Table({initial:68,maximum:68,element:"anyfunc"});c.__memory_base=1024;c.__table_base=0;return va(c)};var wa=[null,[],[]],N=0;function O(){N+=4;return G[N-4>>2]}var P={};function xa(){return E.length}function ya(b){b=D(b);var c=buffer.byteLength;try{return-1!==C.grow((b-c)/65536)?(buffer=C.buffer,!0):!1}catch(d){return!1}}
var za=a.asm({},{b:x,q:function(){},g:function(b){a.___errno_location&&(G[a.___errno_location()>>2]=b);return b},m:function(b,c){N=c;try{return P.H(),O(),O(),O(),O(),0}catch(d){return x(d),-d.G}},f:function(b,c){N=c;try{var d=O(),e=O(),k=O();for(c=b=0;c<k;c++){for(var y=G[e+8*c>>2],ka=G[e+(8*c+4)>>2],R=0;R<ka;R++){var S=F[y+R],T=wa[d];if(0===S||10===S){var Aa=1===d?A:B;for(var v=T,m=0,w=m+void 0,z=m;v[z]&&!(z>=w);)++z;if(16<z-m&&v.subarray&&da)var ma=da.decode(v.subarray(m,z));else{for(w="";m<z;){var h=
v[m++];if(h&128){var U=v[m++]&63;if(192==(h&224))w+=String.fromCharCode((h&31)<<6|U);else{var na=v[m++]&63;h=224==(h&240)?(h&15)<<12|U<<6|na:(h&7)<<18|U<<12|na<<6|v[m++]&63;if(65536>h)w+=String.fromCharCode(h);else{var oa=h-65536;w+=String.fromCharCode(55296|oa>>10,56320|oa&1023)}}}else w+=String.fromCharCode(h)}ma=w}Aa(ma);T.length=0}else T.push(S)}b+=ka}return b}catch(pa){return x(pa),-pa.G}},l:function(b,c){N=c;try{var d=P.H(),e=O(),k=O();return(void 0).read(d,E,e,k)}catch(y){return x(y),-y.G}},
k:function(b,c){N=c;return 0},j:function(b,c){N=c;try{return P.H(),0}catch(d){return x(d),-d.G}},e:function(){},i:xa,p:function(b,c,d){F.set(F.subarray(c,c+d),b)},o:function(b){if(2147418112<b)return!1;for(var c=Math.max(xa(),16777216);c<b;)536870912>=c?c=D(2*c):c=Math.min(D((3*c+2147483648)/4),2147418112);if(!ya(c))return!1;ea();return!0},d:function(b,c,d,e){a.audioPackets.push({data:a.HEAPU8.buffer.slice?a.HEAPU8.buffer.slice(b,b+c):(new Uint8Array(new Uint8Array(a.HEAPU8.buffer,b,c))).buffer,timestamp:d,
discardPadding:e})},h:function(b,c){function d(b){for(var c="",d=a.HEAPU8;0!=d[b];b++)c+=String.fromCharCode(d[b]);return c}b&&(a.videoCodec=d(b));c&&(a.audioCodec=d(c));b=a._ogv_demuxer_media_duration();a.duration=0<=b?b:NaN;a.loadedMetadata=!0},c:function(b,c,d,e,k){a.videoPackets.push({data:a.HEAPU8.buffer.slice?a.HEAPU8.buffer.slice(b,b+c):(new Uint8Array(new Uint8Array(a.HEAPU8.buffer,b,c))).buffer,timestamp:d,keyframeTimestamp:e,isKeyframe:!!k})},n:function(){x("OOM")},a:6800},buffer);
a.asm=za;a._free=function(){return a.asm.r.apply(null,arguments)};a._malloc=function(){return a.asm.s.apply(null,arguments)};a._ogv_demuxer_destroy=function(){return a.asm.t.apply(null,arguments)};a._ogv_demuxer_flush=function(){return a.asm.u.apply(null,arguments)};a._ogv_demuxer_init=function(){return a.asm.v.apply(null,arguments)};a._ogv_demuxer_keypoint_offset=function(){return a.asm.w.apply(null,arguments)};a._ogv_demuxer_media_duration=function(){return a.asm.x.apply(null,arguments)};
a._ogv_demuxer_media_length=function(){return a.asm.y.apply(null,arguments)};a._ogv_demuxer_process=function(){return a.asm.z.apply(null,arguments)};a._ogv_demuxer_receive_input=function(){return a.asm.A.apply(null,arguments)};a._ogv_demuxer_seek_to_keypoint=function(){return a.asm.B.apply(null,arguments)};a._ogv_demuxer_seekable=function(){return a.asm.C.apply(null,arguments)};a.dynCall_vi=function(){return a.asm.D.apply(null,arguments)};a.asm=za;
a.then=function(b){if(a.calledRun)b(a);else{var c=a.onRuntimeInitialized;a.onRuntimeInitialized=function(){c&&c();b(a)}}return a};function Q(b){this.name="ExitStatus";this.message="Program terminated with exit("+b+")";this.status=b}Q.prototype=Error();Q.prototype.constructor=Q;L=function Ba(){a.calledRun||V();a.calledRun||(L=Ba)};
function V(){function b(){if(!a.calledRun&&(a.calledRun=!0,!ca)){la||(la=!0,I(ha));I(ia);if(a.onRuntimeInitialized)a.onRuntimeInitialized();if(a.postRun)for("function"==typeof a.postRun&&(a.postRun=[a.postRun]);a.postRun.length;){var b=a.postRun.shift();ja.unshift(b)}I(ja)}}if(!(0<J)){if(a.preRun)for("function"==typeof a.preRun&&(a.preRun=[a.preRun]);a.preRun.length;)qa();I(fa);0<J||a.calledRun||(a.setStatus?(a.setStatus("Running..."),setTimeout(function(){setTimeout(function(){a.setStatus("")},1);
b()},1)):b())}}a.run=V;function x(b){if(a.onAbort)a.onAbort(b);void 0!==b?(A(b),B(b),b=JSON.stringify(b)):b="";ca=!0;throw"abort("+b+"). Build with -s ASSERTIONS=1 for more info.";}a.abort=x;if(a.preInit)for("function"==typeof a.preInit&&(a.preInit=[a.preInit]);0<a.preInit.length;)a.preInit.pop()();a.noExitRuntime=!0;V();var W,X,Y;Y="undefined"===typeof performance||"undefined"===typeof performance.now?Date.now:performance.now.bind(performance);
function Z(b){var c=Y();b=b();c=Y()-c;a.cpuTime+=c;return b}a.loadedMetadata=!1;a.videoCodec=null;a.audioCodec=null;a.duration=NaN;a.onseek=null;a.cpuTime=0;a.audioPackets=[];Object.defineProperty(a,"hasAudio",{get:function(){return a.loadedMetadata&&a.audioCodec}});Object.defineProperty(a,"audioReady",{get:function(){return 0<a.audioPackets.length}});Object.defineProperty(a,"audioTimestamp",{get:function(){return 0<a.audioPackets.length?a.audioPackets[0].timestamp:-1}});a.videoPackets=[];
Object.defineProperty(a,"hasVideo",{get:function(){return a.loadedMetadata&&a.videoCodec}});Object.defineProperty(a,"frameReady",{get:function(){return 0<a.videoPackets.length}});Object.defineProperty(a,"frameTimestamp",{get:function(){return 0<a.videoPackets.length?a.videoPackets[0].timestamp:-1}});Object.defineProperty(a,"keyframeTimestamp",{get:function(){return 0<a.videoPackets.length?a.videoPackets[0].keyframeTimestamp:-1}});
Object.defineProperty(a,"nextKeyframeTimestamp",{get:function(){for(var b=0;b<a.videoPackets.length;b++){var c=a.videoPackets[b];if(c.isKeyframe)return c.timestamp}return-1}});Object.defineProperty(a,"processing",{get:function(){return!1}});Object.defineProperty(a,"seekable",{get:function(){return!!a._ogv_demuxer_seekable()}});a.init=function(b){Z(function(){a._ogv_demuxer_init()});b()};
a.receiveInput=function(b,c){Z(function(){var c=b.byteLength;W&&X>=c||(W&&a._free(W),X=c,W=a._malloc(X));var e=W;a.HEAPU8.set(new Uint8Array(b),e);a._ogv_demuxer_receive_input(e,c)});c()};a.process=function(b){var c=Z(function(){return a._ogv_demuxer_process()});b(!!c)};a.dequeueVideoPacket=function(b){if(a.videoPackets.length){var c=a.videoPackets.shift().data;b(c)}else b(null)};a.dequeueAudioPacket=function(b){if(a.audioPackets.length){var c=a.audioPackets.shift();b(c.data,c.discardPadding)}else b(null)};
a.getKeypointOffset=function(b,c){var d=Z(function(){return a._ogv_demuxer_keypoint_offset(1E3*b)});c(d)};a.seekToKeypoint=function(b,c){var d=Z(function(){return a._ogv_demuxer_seek_to_keypoint(1E3*b)});d&&(a.audioPackets.splice(0,a.audioPackets.length),a.videoPackets.splice(0,a.videoPackets.length));c(!!d)};a.flush=function(b){Z(function(){a.audioPackets.splice(0,a.audioPackets.length);a.videoPackets.splice(0,a.videoPackets.length);a._ogv_demuxer_flush()});b()};a.close=function(){};


  return OGVDemuxerOggW
}
);
})();
if (typeof exports === 'object' && typeof module === 'object')
      module.exports = OGVDemuxerOggW;
    else if (typeof define === 'function' && define['amd'])
      define([], function() { return OGVDemuxerOggW; });
    else if (typeof exports === 'object')
      exports["OGVDemuxerOggW"] = OGVDemuxerOggW;
    