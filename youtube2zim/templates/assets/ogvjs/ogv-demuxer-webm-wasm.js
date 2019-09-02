
var OGVDemuxerWebMW = (function() {
  var _scriptDir = typeof document !== 'undefined' && document.currentScript ? document.currentScript.src : undefined;
  return (
function(OGVDemuxerWebMW) {
  OGVDemuxerWebMW = OGVDemuxerWebMW || {};


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

var a;a||(a=typeof OGVDemuxerWebMW !== 'undefined' ? OGVDemuxerWebMW : {});var aa=a;a.memoryLimit&&(a.TOTAL_MEMORY=aa.memoryLimit);var g={},h;for(h in a)a.hasOwnProperty(h)&&(g[h]=a[h]);a.arguments=[];a.thisProgram="./this.program";a.quit=function(b,c){throw c;};a.preRun=[];a.postRun=[];var l=!1,m=!1,n=!1,q=!1;l="object"===typeof window;m="function"===typeof importScripts;n="object"===typeof process&&"function"===typeof require&&!l&&!m;q=!l&&!n&&!m;var r="";
if(n){r=__dirname+"/";var t,u;a.read=function(b,c){t||(t=require("fs"));u||(u=require("path"));b=u.normalize(b);b=t.readFileSync(b);return c?b:b.toString()};a.readBinary=function(b){b=a.read(b,!0);b.buffer||(b=new Uint8Array(b));b.buffer||v("Assertion failed: undefined");return b};1<process.argv.length&&(a.thisProgram=process.argv[1].replace(/\\/g,"/"));a.arguments=process.argv.slice(2);process.on("unhandledRejection",v);a.quit=function(b){process.exit(b)};a.inspect=function(){return"[Emscripten Module object]"}}else if(q)"undefined"!=
typeof read&&(a.read=function(b){return read(b)}),a.readBinary=function(b){if("function"===typeof readbuffer)return new Uint8Array(readbuffer(b));b=read(b,"binary");"object"===typeof b||v("Assertion failed: undefined");return b},"undefined"!=typeof scriptArgs?a.arguments=scriptArgs:"undefined"!=typeof arguments&&(a.arguments=arguments),"function"===typeof quit&&(a.quit=function(b){quit(b)});else if(l||m)m?r=self.location.href:document.currentScript&&(r=document.currentScript.src),_scriptDir&&(r=_scriptDir),
0!==r.indexOf("blob:")?r=r.substr(0,r.lastIndexOf("/")+1):r="",a.read=function(b){var c=new XMLHttpRequest;c.open("GET",b,!1);c.send(null);return c.responseText},m&&(a.readBinary=function(b){var c=new XMLHttpRequest;c.open("GET",b,!1);c.responseType="arraybuffer";c.send(null);return new Uint8Array(c.response)}),a.readAsync=function(b,c,d){var e=new XMLHttpRequest;e.open("GET",b,!0);e.responseType="arraybuffer";e.onload=function(){200==e.status||0==e.status&&e.response?c(e.response):d()};e.onerror=
d;e.send(null)},a.setWindowTitle=function(b){document.title=b};var w=a.print||("undefined"!==typeof console?console.log.bind(console):"undefined"!==typeof print?print:null),x=a.printErr||("undefined"!==typeof printErr?printErr:"undefined"!==typeof console&&console.warn.bind(console)||w);for(h in g)g.hasOwnProperty(h)&&(a[h]=g[h]);g=void 0;var ba={"f64-rem":function(b,c){return b%c},"debugger":function(){debugger}};"object"!==typeof WebAssembly&&x("no native wasm support detected");
var y,z=!1,A="undefined"!==typeof TextDecoder?new TextDecoder("utf8"):void 0;
function B(b,c,d){var e=c+d;for(d=c;b[d]&&!(d>=e);)++d;if(16<d-c&&b.subarray&&A)return A.decode(b.subarray(c,d));for(e="";c<d;){var f=b[c++];if(f&128){var k=b[c++]&63;if(192==(f&224))e+=String.fromCharCode((f&31)<<6|k);else{var p=b[c++]&63;f=224==(f&240)?(f&15)<<12|k<<6|p:(f&7)<<18|k<<12|p<<6|b[c++]&63;65536>f?e+=String.fromCharCode(f):(f-=65536,e+=String.fromCharCode(55296|f>>10,56320|f&1023))}}else e+=String.fromCharCode(f)}return e}function F(b){return b?B(G,b,void 0):""}
"undefined"!==typeof TextDecoder&&new TextDecoder("utf-16le");function H(b){0<b%65536&&(b+=65536-b%65536);return b}var buffer,J,G,K;function L(){a.HEAP8=J=new Int8Array(buffer);a.HEAP16=new Int16Array(buffer);a.HEAP32=K=new Int32Array(buffer);a.HEAPU8=G=new Uint8Array(buffer);a.HEAPU16=new Uint16Array(buffer);a.HEAPU32=new Uint32Array(buffer);a.HEAPF32=new Float32Array(buffer);a.HEAPF64=new Float64Array(buffer)}var M=a.TOTAL_MEMORY||16777216;
5242880>M&&x("TOTAL_MEMORY should be larger than TOTAL_STACK, was "+M+"! (TOTAL_STACK=5242880)");a.buffer?buffer=a.buffer:"object"===typeof WebAssembly&&"function"===typeof WebAssembly.Memory?(y=new WebAssembly.Memory({initial:M/65536}),buffer=y.buffer):buffer=new ArrayBuffer(M);L();K[2760]=5253952;function N(b){for(;0<b.length;){var c=b.shift();if("function"==typeof c)c();else{var d=c.I;"number"===typeof d?void 0===c.F?a.dynCall_v(d):a.dynCall_vi(d,c.F):d(void 0===c.F?null:c.F)}}}
var ca=[],da=[],ea=[],fa=[],ha=!1;function ia(){var b=a.preRun.shift();ca.unshift(b)}var O=0,P=null,Q=null;a.preloadedImages={};a.preloadedAudios={};function ja(){var b=R;return String.prototype.startsWith?b.startsWith("data:application/octet-stream;base64,"):0===b.indexOf("data:application/octet-stream;base64,")}var R="ogv-demuxer-webm-wasm.wasm";if(!ja()){var ka=R;R=a.locateFile?a.locateFile(ka,r):r+ka;R=zim_fix_wasm_target(R);}
function la(){try{if(a.wasmBinary)return new Uint8Array(a.wasmBinary);if(a.readBinary)return a.readBinary(R);throw"both async and sync fetching of the wasm failed";}catch(b){v(b)}}function ma(){return a.wasmBinary||!l&&!m||"function"!==typeof fetch?new Promise(function(b){b(la())}):fetch(R,{credentials:"same-origin"}).then(function(b){if(!b.ok)throw"failed to load wasm binary file at '"+R+"'";return b.arrayBuffer()}).catch(function(){return la()})}
function na(b){function c(b){a.asm=b.exports;O--;a.monitorRunDependencies&&a.monitorRunDependencies(O);0==O&&(null!==P&&(clearInterval(P),P=null),Q&&(b=Q,Q=null,b()))}function d(b){c(b.instance)}function e(b){return ma().then(function(b){return WebAssembly.instantiate(b,f)}).then(b,function(b){x("failed to asynchronously prepare wasm: "+b);v(b)})}var f={env:b,global:{NaN:NaN,Infinity:Infinity},"global.Math":Math,asm2wasm:ba};O++;a.monitorRunDependencies&&a.monitorRunDependencies(O);if(a.instantiateWasm)try{return a.instantiateWasm(f,
c)}catch(k){return x("Module.instantiateWasm callback failed with error: "+k),!1}(function(){return a.wasmBinary||"function"!==typeof WebAssembly.instantiateStreaming||ja()||"function"!==typeof fetch?e(d):WebAssembly.instantiateStreaming(fetch(R,{credentials:"same-origin"}),f).then(d,function(b){x("wasm streaming compile failed: "+b);x("falling back to ArrayBuffer instantiation");e(d)})})();return{}}
a.asm=function(b,c){c.memory=y;c.table=new WebAssembly.Table({initial:20,maximum:20,element:"anyfunc"});c.__memory_base=1024;c.__table_base=0;return na(c)};var oa=[null,[],[]],S=0;function T(){S+=4;return K[S-4>>2]}var pa={};function qa(){return J.length}function ra(b){b=H(b);var c=buffer.byteLength;try{return-1!==y.grow((b-c)/65536)?(buffer=y.buffer,!0):!1}catch(d){return!1}}
var sa=a.asm({},{c:v,b:function(b,c,d,e){v("Assertion failed: "+F(b)+", at: "+[c?F(c):"unknown filename",d,e?F(e):"unknown function"])},e:function(b){a.___errno_location&&(K[a.___errno_location()>>2]=b);return b},l:function(b,c){S=c;try{return pa.H(),T(),T(),T(),T(),0}catch(d){return v(d),-d.G}},d:function(b,c){S=c;try{var d=T(),e=T(),f=T();for(c=b=0;c<f;c++){for(var k=K[e+8*c>>2],p=K[e+(8*c+4)>>2],C=0;C<p;C++){var D=G[k+C],E=oa[d];0===D||10===D?((1===d?w:x)(B(E,0)),E.length=0):E.push(D)}b+=p}return b}catch(I){return v(I),
-I.G}},k:function(b,c){S=c;return 0},j:function(b,c){S=c;try{return pa.H(),0}catch(d){return v(d),-d.G}},i:function(){a.abort()},h:qa,g:function(b,c,d){G.set(G.subarray(c,c+d),b)},r:function(b){if(2147418112<b)return!1;for(var c=Math.max(qa(),16777216);c<b;)536870912>=c?c=H(2*c):c=Math.min(H((3*c+2147483648)/4),2147418112);if(!ra(c))return!1;L();return!0},f:function(b,c,d,e){a.audioPackets.push({data:a.HEAPU8.buffer.slice?a.HEAPU8.buffer.slice(b,b+c):(new Uint8Array(new Uint8Array(a.HEAPU8.buffer,
b,c))).buffer,timestamp:d,discardPadding:e})},q:function(b,c,d,e,f,k,p,C,D,E,I){a.videoFormat={width:b,height:c,chromaWidth:d,chromaHeight:e,cropLeft:C,cropTop:D,cropWidth:k,cropHeight:p,displayWidth:E,displayHeight:I,fps:f}},p:function(b,c){function d(b){for(var c="",d=a.HEAPU8;0!=d[b];b++)c+=String.fromCharCode(d[b]);return c}b&&(a.videoCodec=d(b));c&&(a.audioCodec=d(c));b=a._ogv_demuxer_media_duration();a.duration=0<=b?b:NaN;a.loadedMetadata=!0},m:function(b,c){if(a.onseek)a.onseek(b+4294967296*
c)},o:function(b,c,d,e,f){a.videoPackets.push({data:a.HEAPU8.buffer.slice?a.HEAPU8.buffer.slice(b,b+c):(new Uint8Array(new Uint8Array(a.HEAPU8.buffer,b,c))).buffer,timestamp:d,keyframeTimestamp:e,isKeyframe:!!f})},n:function(){v("OOM")},a:11040},buffer);a.asm=sa;a._free=function(){return a.asm.s.apply(null,arguments)};a._malloc=function(){return a.asm.t.apply(null,arguments)};a._ogv_demuxer_destroy=function(){return a.asm.u.apply(null,arguments)};
a._ogv_demuxer_flush=function(){return a.asm.v.apply(null,arguments)};a._ogv_demuxer_init=function(){return a.asm.w.apply(null,arguments)};a._ogv_demuxer_keypoint_offset=function(){return a.asm.x.apply(null,arguments)};a._ogv_demuxer_media_duration=function(){return a.asm.y.apply(null,arguments)};a._ogv_demuxer_media_length=function(){return a.asm.z.apply(null,arguments)};a._ogv_demuxer_process=function(){return a.asm.A.apply(null,arguments)};
a._ogv_demuxer_receive_input=function(){return a.asm.B.apply(null,arguments)};a._ogv_demuxer_seek_to_keypoint=function(){return a.asm.C.apply(null,arguments)};a._ogv_demuxer_seekable=function(){return a.asm.D.apply(null,arguments)};a.asm=sa;a.then=function(b){if(a.calledRun)b(a);else{var c=a.onRuntimeInitialized;a.onRuntimeInitialized=function(){c&&c();b(a)}}return a};function U(b){this.name="ExitStatus";this.message="Program terminated with exit("+b+")";this.status=b}U.prototype=Error();
U.prototype.constructor=U;Q=function ta(){a.calledRun||V();a.calledRun||(Q=ta)};
function V(){function b(){if(!a.calledRun&&(a.calledRun=!0,!z)){ha||(ha=!0,N(da));N(ea);if(a.onRuntimeInitialized)a.onRuntimeInitialized();if(a.postRun)for("function"==typeof a.postRun&&(a.postRun=[a.postRun]);a.postRun.length;){var b=a.postRun.shift();fa.unshift(b)}N(fa)}}if(!(0<O)){if(a.preRun)for("function"==typeof a.preRun&&(a.preRun=[a.preRun]);a.preRun.length;)ia();N(ca);0<O||a.calledRun||(a.setStatus?(a.setStatus("Running..."),setTimeout(function(){setTimeout(function(){a.setStatus("")},1);
b()},1)):b())}}a.run=V;function v(b){if(a.onAbort)a.onAbort(b);void 0!==b?(w(b),x(b),b=JSON.stringify(b)):b="";z=!0;throw"abort("+b+"). Build with -s ASSERTIONS=1 for more info.";}a.abort=v;if(a.preInit)for("function"==typeof a.preInit&&(a.preInit=[a.preInit]);0<a.preInit.length;)a.preInit.pop()();a.noExitRuntime=!0;V();var W,X,Y;Y="undefined"===typeof performance||"undefined"===typeof performance.now?Date.now:performance.now.bind(performance);
function Z(b){var c=Y();b=b();c=Y()-c;a.cpuTime+=c;return b}a.loadedMetadata=!1;a.videoCodec=null;a.audioCodec=null;a.duration=NaN;a.onseek=null;a.cpuTime=0;a.audioPackets=[];Object.defineProperty(a,"hasAudio",{get:function(){return a.loadedMetadata&&a.audioCodec}});Object.defineProperty(a,"audioReady",{get:function(){return 0<a.audioPackets.length}});Object.defineProperty(a,"audioTimestamp",{get:function(){return 0<a.audioPackets.length?a.audioPackets[0].timestamp:-1}});a.videoPackets=[];
Object.defineProperty(a,"hasVideo",{get:function(){return a.loadedMetadata&&a.videoCodec}});Object.defineProperty(a,"frameReady",{get:function(){return 0<a.videoPackets.length}});Object.defineProperty(a,"frameTimestamp",{get:function(){return 0<a.videoPackets.length?a.videoPackets[0].timestamp:-1}});Object.defineProperty(a,"keyframeTimestamp",{get:function(){return 0<a.videoPackets.length?a.videoPackets[0].keyframeTimestamp:-1}});
Object.defineProperty(a,"nextKeyframeTimestamp",{get:function(){for(var b=0;b<a.videoPackets.length;b++){var c=a.videoPackets[b];if(c.isKeyframe)return c.timestamp}return-1}});Object.defineProperty(a,"processing",{get:function(){return!1}});Object.defineProperty(a,"seekable",{get:function(){return!!a._ogv_demuxer_seekable()}});a.init=function(b){Z(function(){a._ogv_demuxer_init()});b()};
a.receiveInput=function(b,c){Z(function(){var c=b.byteLength;W&&X>=c||(W&&a._free(W),X=c,W=a._malloc(X));var e=W;a.HEAPU8.set(new Uint8Array(b),e);a._ogv_demuxer_receive_input(e,c)});c()};a.process=function(b){var c=Z(function(){return a._ogv_demuxer_process()});b(!!c)};a.dequeueVideoPacket=function(b){if(a.videoPackets.length){var c=a.videoPackets.shift().data;b(c)}else b(null)};a.dequeueAudioPacket=function(b){if(a.audioPackets.length){var c=a.audioPackets.shift();b(c.data,c.discardPadding)}else b(null)};
a.getKeypointOffset=function(b,c){var d=Z(function(){return a._ogv_demuxer_keypoint_offset(1E3*b)});c(d)};a.seekToKeypoint=function(b,c){var d=Z(function(){return a._ogv_demuxer_seek_to_keypoint(1E3*b)});d&&(a.audioPackets.splice(0,a.audioPackets.length),a.videoPackets.splice(0,a.videoPackets.length));c(!!d)};a.flush=function(b){Z(function(){a.audioPackets.splice(0,a.audioPackets.length);a.videoPackets.splice(0,a.videoPackets.length);a._ogv_demuxer_flush()});b()};a.close=function(){};


  return OGVDemuxerWebMW
}
);
})();
if (typeof exports === 'object' && typeof module === 'object')
      module.exports = OGVDemuxerWebMW;
    else if (typeof define === 'function' && define['amd'])
      define([], function() { return OGVDemuxerWebMW; });
    else if (typeof exports === 'object')
      exports["OGVDemuxerWebMW"] = OGVDemuxerWebMW;
    