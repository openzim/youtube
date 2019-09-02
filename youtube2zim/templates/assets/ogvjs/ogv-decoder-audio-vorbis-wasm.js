
var OGVDecoderAudioVorbisW = (function() {
  var _scriptDir = typeof document !== 'undefined' && document.currentScript ? document.currentScript.src : undefined;
  return (
function(OGVDecoderAudioVorbisW) {
  OGVDecoderAudioVorbisW = OGVDecoderAudioVorbisW || {};


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

var a;a||(a=typeof OGVDecoderAudioVorbisW !== 'undefined' ? OGVDecoderAudioVorbisW : {});var g=a;a.memoryLimit&&(a.TOTAL_MEMORY=g.memoryLimit);var h={},k;for(k in a)a.hasOwnProperty(k)&&(h[k]=a[k]);a.arguments=[];a.thisProgram="./this.program";a.quit=function(b,c){throw c;};a.preRun=[];a.postRun=[];var l=!1,m=!1,n=!1,p=!1;l="object"===typeof window;m="function"===typeof importScripts;n="object"===typeof process&&"function"===typeof require&&!l&&!m;p=!l&&!n&&!m;var r="";
if(n){r=__dirname+"/";var t,u;a.read=function(b,c){t||(t=require("fs"));u||(u=require("path"));b=u.normalize(b);b=t.readFileSync(b);return c?b:b.toString()};a.readBinary=function(b){b=a.read(b,!0);b.buffer||(b=new Uint8Array(b));b.buffer||v("Assertion failed: undefined");return b};1<process.argv.length&&(a.thisProgram=process.argv[1].replace(/\\/g,"/"));a.arguments=process.argv.slice(2);process.on("unhandledRejection",v);a.quit=function(b){process.exit(b)};a.inspect=function(){return"[Emscripten Module object]"}}else if(p)"undefined"!=
typeof read&&(a.read=function(b){return read(b)}),a.readBinary=function(b){if("function"===typeof readbuffer)return new Uint8Array(readbuffer(b));b=read(b,"binary");"object"===typeof b||v("Assertion failed: undefined");return b},"undefined"!=typeof scriptArgs?a.arguments=scriptArgs:"undefined"!=typeof arguments&&(a.arguments=arguments),"function"===typeof quit&&(a.quit=function(b){quit(b)});else if(l||m)m?r=self.location.href:document.currentScript&&(r=document.currentScript.src),_scriptDir&&(r=_scriptDir),
0!==r.indexOf("blob:")?r=r.substr(0,r.lastIndexOf("/")+1):r="",a.read=function(b){var c=new XMLHttpRequest;c.open("GET",b,!1);c.send(null);return c.responseText},m&&(a.readBinary=function(b){var c=new XMLHttpRequest;c.open("GET",b,!1);c.responseType="arraybuffer";c.send(null);return new Uint8Array(c.response)}),a.readAsync=function(b,c,d){var e=new XMLHttpRequest;e.open("GET",b,!0);e.responseType="arraybuffer";e.onload=function(){200==e.status||0==e.status&&e.response?c(e.response):d()};e.onerror=
d;e.send(null)},a.setWindowTitle=function(b){document.title=b};var w=a.print||("undefined"!==typeof console?console.log.bind(console):"undefined"!==typeof print?print:null),x=a.printErr||("undefined"!==typeof printErr?printErr:"undefined"!==typeof console&&console.warn.bind(console)||w);for(k in h)h.hasOwnProperty(k)&&(a[k]=h[k]);h=void 0;var aa={"f64-rem":function(b,c){return b%c},"debugger":function(){debugger}};"object"!==typeof WebAssembly&&x("no native wasm support detected");var y,A=!1;
"undefined"!==typeof TextDecoder&&new TextDecoder("utf8");"undefined"!==typeof TextDecoder&&new TextDecoder("utf-16le");function B(b){0<b%65536&&(b+=65536-b%65536);return b}var buffer,C,D,E;function F(){a.HEAP8=C=new Int8Array(buffer);a.HEAP16=new Int16Array(buffer);a.HEAP32=E=new Int32Array(buffer);a.HEAPU8=D=new Uint8Array(buffer);a.HEAPU16=new Uint16Array(buffer);a.HEAPU32=new Uint32Array(buffer);a.HEAPF32=new Float32Array(buffer);a.HEAPF64=new Float64Array(buffer)}var G=a.TOTAL_MEMORY||16777216;
5242880>G&&x("TOTAL_MEMORY should be larger than TOTAL_STACK, was "+G+"! (TOTAL_STACK=5242880)");a.buffer?buffer=a.buffer:"object"===typeof WebAssembly&&"function"===typeof WebAssembly.Memory?(y=new WebAssembly.Memory({initial:G/65536}),buffer=y.buffer):buffer=new ArrayBuffer(G);F();E[15228]=5303824;function H(b){for(;0<b.length;){var c=b.shift();if("function"==typeof c)c();else{var d=c.u;"number"===typeof d?void 0===c.s?a.dynCall_v(d):a.dynCall_vi(d,c.s):d(void 0===c.s?null:c.s)}}}
var I=[],ba=[],ca=[],J=[],L=!1;function da(){var b=a.preRun.shift();I.unshift(b)}var M=0,N=null,O=null;a.preloadedImages={};a.preloadedAudios={};function P(){var b=Q;return String.prototype.startsWith?b.startsWith("data:application/octet-stream;base64,"):0===b.indexOf("data:application/octet-stream;base64,")}var Q="ogv-decoder-audio-vorbis-wasm.wasm";if(!P()){var R=Q;Q=a.locateFile?a.locateFile(R,r):r+R;Q=zim_fix_wasm_target(Q);}
function S(){try{if(a.wasmBinary)return new Uint8Array(a.wasmBinary);if(a.readBinary)return a.readBinary(Q);throw"both async and sync fetching of the wasm failed";}catch(b){v(b)}}function ea(){return a.wasmBinary||!l&&!m||"function"!==typeof fetch?new Promise(function(b){b(S())}):fetch(Q,{credentials:"same-origin"}).then(function(b){if(!b.ok)throw"failed to load wasm binary file at '"+Q+"'";return b.arrayBuffer()}).catch(function(){return S()})}
function fa(b){function c(b){a.asm=b.exports;M--;a.monitorRunDependencies&&a.monitorRunDependencies(M);0==M&&(null!==N&&(clearInterval(N),N=null),O&&(b=O,O=null,b()))}function d(b){c(b.instance)}function e(b){return ea().then(function(b){return WebAssembly.instantiate(b,q)}).then(b,function(b){x("failed to asynchronously prepare wasm: "+b);v(b)})}var q={env:b,global:{NaN:NaN,Infinity:Infinity},"global.Math":Math,asm2wasm:aa};M++;a.monitorRunDependencies&&a.monitorRunDependencies(M);if(a.instantiateWasm)try{return a.instantiateWasm(q,
c)}catch(z){return x("Module.instantiateWasm callback failed with error: "+z),!1}(function(){return a.wasmBinary||"function"!==typeof WebAssembly.instantiateStreaming||P()||"function"!==typeof fetch?e(d):WebAssembly.instantiateStreaming(fetch(Q,{credentials:"same-origin"}),q).then(d,function(b){x("wasm streaming compile failed: "+b);x("falling back to ArrayBuffer instantiation");e(d)})})();return{}}
a.asm=function(b,c){c.memory=y;c.table=new WebAssembly.Table({initial:52,maximum:52,element:"anyfunc"});c.__memory_base=1024;c.__table_base=0;return fa(c)};function T(){return C.length}function ha(b){b=B(b);var c=buffer.byteLength;try{return-1!==y.grow((b-c)/65536)?(buffer=y.buffer,!0):!1}catch(d){return!1}}
var ia=a.asm({},{b:v,c:function(b){a.___errno_location&&(E[a.___errno_location()>>2]=b);return b},j:T,i:function(b,c,d){D.set(D.subarray(c,c+d),b)},h:function(b){if(2147418112<b)return!1;for(var c=Math.max(T(),16777216);c<b;)536870912>=c?c=B(2*c):c=Math.min(B((3*c+2147483648)/4),2147418112);if(!ha(c))return!1;F();return!0},g:function(b){if(!a.noExitRuntime&&(A=!0,a.onExit))a.onExit(b);a.quit(b,new U(b))},f:function(b,c,d){var e=a.HEAPU32,q=a.HEAPF32,z=[];if(0!==b)for(var f,K=0;K<c;K++)f=e[b/4+K],
q.buffer.slice?(f=q.buffer.slice(f,f+4*d),f=new Float32Array(f)):(f=q.subarray(f/4,f/4+d),f=new Float32Array(f)),z.push(f);a.audioBuffer=z},e:function(b,c){a.audioFormat={channels:b,rate:c};a.loadedMetadata=!0},d:function(){v("OOM")},a:60912},buffer);a.asm=ia;a._free=function(){return a.asm.k.apply(null,arguments)};a._malloc=function(){return a.asm.l.apply(null,arguments)};a._ogv_audio_decoder_destroy=function(){return a.asm.m.apply(null,arguments)};
a._ogv_audio_decoder_init=function(){return a.asm.n.apply(null,arguments)};a._ogv_audio_decoder_process_audio=function(){return a.asm.o.apply(null,arguments)};a._ogv_audio_decoder_process_header=function(){return a.asm.p.apply(null,arguments)};a.dynCall_vi=function(){return a.asm.q.apply(null,arguments)};a.asm=ia;a.then=function(b){if(a.calledRun)b(a);else{var c=a.onRuntimeInitialized;a.onRuntimeInitialized=function(){c&&c();b(a)}}return a};
function U(b){this.name="ExitStatus";this.message="Program terminated with exit("+b+")";this.status=b}U.prototype=Error();U.prototype.constructor=U;O=function ja(){a.calledRun||V();a.calledRun||(O=ja)};
function V(){function b(){if(!a.calledRun&&(a.calledRun=!0,!A)){L||(L=!0,H(ba));H(ca);if(a.onRuntimeInitialized)a.onRuntimeInitialized();if(a.postRun)for("function"==typeof a.postRun&&(a.postRun=[a.postRun]);a.postRun.length;){var b=a.postRun.shift();J.unshift(b)}H(J)}}if(!(0<M)){if(a.preRun)for("function"==typeof a.preRun&&(a.preRun=[a.preRun]);a.preRun.length;)da();H(I);0<M||a.calledRun||(a.setStatus?(a.setStatus("Running..."),setTimeout(function(){setTimeout(function(){a.setStatus("")},1);b()},
1)):b())}}a.run=V;function v(b){if(a.onAbort)a.onAbort(b);void 0!==b?(w(b),x(b),b=JSON.stringify(b)):b="";A=!0;throw"abort("+b+"). Build with -s ASSERTIONS=1 for more info.";}a.abort=v;if(a.preInit)for("function"==typeof a.preInit&&(a.preInit=[a.preInit]);0<a.preInit.length;)a.preInit.pop()();a.noExitRuntime=!0;V();var W,X;function ka(b){if(W&&X>=b)return W;W&&a._free(W);X=b;return W=a._malloc(X)}var Y;Y="undefined"===typeof performance||"undefined"===typeof performance.now?Date.now:performance.now.bind(performance);
function Z(b){var c=Y();b=b();a.cpuTime+=Y()-c;return b}a.loadedMetadata=!!g.audioFormat;a.audioFormat=g.audioFormat||null;a.audioBuffer=null;a.cpuTime=0;Object.defineProperty(a,"processing",{get:function(){return!1}});a.init=function(b){Z(function(){a._ogv_audio_decoder_init()});b()};a.processHeader=function(b,c){var d=Z(function(){var c=b.byteLength,d=ka(c);a.HEAPU8.set(new Uint8Array(b),d);return a._ogv_audio_decoder_process_header(d,c)});c(d)};
a.processAudio=function(b,c){var d=Z(function(){var c=b.byteLength,d=ka(c);a.HEAPU8.set(new Uint8Array(b),d);return a._ogv_audio_decoder_process_audio(d,c)});c(d)};a.close=function(){};


  return OGVDecoderAudioVorbisW
}
);
})();
if (typeof exports === 'object' && typeof module === 'object')
      module.exports = OGVDecoderAudioVorbisW;
    else if (typeof define === 'function' && define['amd'])
      define([], function() { return OGVDecoderAudioVorbisW; });
    else if (typeof exports === 'object')
      exports["OGVDecoderAudioVorbisW"] = OGVDecoderAudioVorbisW;
    