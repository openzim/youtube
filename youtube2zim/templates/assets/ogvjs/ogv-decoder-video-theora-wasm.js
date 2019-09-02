
var OGVDecoderVideoTheoraW = (function() {
  var _scriptDir = typeof document !== 'undefined' && document.currentScript ? document.currentScript.src : undefined;
  return (
function(OGVDecoderVideoTheoraW) {
  OGVDecoderVideoTheoraW = OGVDecoderVideoTheoraW || {};


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

var a;a||(a=typeof OGVDecoderVideoTheoraW !== 'undefined' ? OGVDecoderVideoTheoraW : {});var m=a;a.memoryLimit&&(a.TOTAL_MEMORY=m.memoryLimit);var n={},p;for(p in a)a.hasOwnProperty(p)&&(n[p]=a[p]);a.arguments=[];a.thisProgram="./this.program";a.quit=function(b,c){throw c;};a.preRun=[];a.postRun=[];var t=!1,u=!1,v=!1,w=!1;t="object"===typeof window;u="function"===typeof importScripts;v="object"===typeof process&&"function"===typeof require&&!t&&!u;w=!t&&!v&&!u;var y="";
if(v){y=__dirname+"/";var z,A;a.read=function(b,c){z||(z=require("fs"));A||(A=require("path"));b=A.normalize(b);b=z.readFileSync(b);return c?b:b.toString()};a.readBinary=function(b){b=a.read(b,!0);b.buffer||(b=new Uint8Array(b));b.buffer||B("Assertion failed: undefined");return b};1<process.argv.length&&(a.thisProgram=process.argv[1].replace(/\\/g,"/"));a.arguments=process.argv.slice(2);process.on("unhandledRejection",B);a.quit=function(b){process.exit(b)};a.inspect=function(){return"[Emscripten Module object]"}}else if(w)"undefined"!=
typeof read&&(a.read=function(b){return read(b)}),a.readBinary=function(b){if("function"===typeof readbuffer)return new Uint8Array(readbuffer(b));b=read(b,"binary");"object"===typeof b||B("Assertion failed: undefined");return b},"undefined"!=typeof scriptArgs?a.arguments=scriptArgs:"undefined"!=typeof arguments&&(a.arguments=arguments),"function"===typeof quit&&(a.quit=function(b){quit(b)});else if(t||u)u?y=self.location.href:document.currentScript&&(y=document.currentScript.src),_scriptDir&&(y=_scriptDir),
0!==y.indexOf("blob:")?y=y.substr(0,y.lastIndexOf("/")+1):y="",a.read=function(b){var c=new XMLHttpRequest;c.open("GET",b,!1);c.send(null);return c.responseText},u&&(a.readBinary=function(b){var c=new XMLHttpRequest;c.open("GET",b,!1);c.responseType="arraybuffer";c.send(null);return new Uint8Array(c.response)}),a.readAsync=function(b,c,d){var e=new XMLHttpRequest;e.open("GET",b,!0);e.responseType="arraybuffer";e.onload=function(){200==e.status||0==e.status&&e.response?c(e.response):d()};e.onerror=
d;e.send(null)},a.setWindowTitle=function(b){document.title=b};var D=a.print||("undefined"!==typeof console?console.log.bind(console):"undefined"!==typeof print?print:null),E=a.printErr||("undefined"!==typeof printErr?printErr:"undefined"!==typeof console&&console.warn.bind(console)||D);for(p in n)n.hasOwnProperty(p)&&(a[p]=n[p]);n=void 0;var aa={"f64-rem":function(b,c){return b%c},"debugger":function(){debugger}};"object"!==typeof WebAssembly&&E("no native wasm support detected");var F,ba=!1;
"undefined"!==typeof TextDecoder&&new TextDecoder("utf8");"undefined"!==typeof TextDecoder&&new TextDecoder("utf-16le");function I(b){0<b%65536&&(b+=65536-b%65536);return b}var buffer,ca,J,K;function da(){a.HEAP8=ca=new Int8Array(buffer);a.HEAP16=new Int16Array(buffer);a.HEAP32=K=new Int32Array(buffer);a.HEAPU8=J=new Uint8Array(buffer);a.HEAPU16=new Uint16Array(buffer);a.HEAPU32=new Uint32Array(buffer);a.HEAPF32=new Float32Array(buffer);a.HEAPF64=new Float64Array(buffer)}var L=a.TOTAL_MEMORY||16777216;
5242880>L&&E("TOTAL_MEMORY should be larger than TOTAL_STACK, was "+L+"! (TOTAL_STACK=5242880)");a.buffer?buffer=a.buffer:"object"===typeof WebAssembly&&"function"===typeof WebAssembly.Memory?(F=new WebAssembly.Memory({initial:L/65536}),buffer=F.buffer):buffer=new ArrayBuffer(L);da();K[1148]=5247504;function M(b){for(;0<b.length;){var c=b.shift();if("function"==typeof c)c();else{var d=c.A;"number"===typeof d?void 0===c.s?a.dynCall_v(d):a.dynCall_vi(d,c.s):d(void 0===c.s?null:c.s)}}}
var ea=[],fa=[],ha=[],ia=[],ja=!1;function ka(){var b=a.preRun.shift();ea.unshift(b)}var N=0,O=null,P=null;a.preloadedImages={};a.preloadedAudios={};function ra(){var b=Q;return String.prototype.startsWith?b.startsWith("data:application/octet-stream;base64,"):0===b.indexOf("data:application/octet-stream;base64,")}var Q="ogv-decoder-video-theora-wasm.wasm";if(!ra()){var sa=Q;Q=a.locateFile?a.locateFile(sa,y):y+sa;Q=zim_fix_wasm_target(Q);}
function ta(){try{if(a.wasmBinary)return new Uint8Array(a.wasmBinary);if(a.readBinary)return a.readBinary(Q);throw"both async and sync fetching of the wasm failed";}catch(b){B(b)}}function ua(){return a.wasmBinary||!t&&!u||"function"!==typeof fetch?new Promise(function(b){b(ta())}):fetch(Q,{credentials:"same-origin"}).then(function(b){if(!b.ok)throw"failed to load wasm binary file at '"+Q+"'";return b.arrayBuffer()}).catch(function(){return ta()})}
function va(b){function c(b){a.asm=b.exports;N--;a.monitorRunDependencies&&a.monitorRunDependencies(N);0==N&&(null!==O&&(clearInterval(O),O=null),P&&(b=P,P=null,b()))}function d(b){c(b.instance)}function e(b){return ua().then(function(b){return WebAssembly.instantiate(b,h)}).then(b,function(b){E("failed to asynchronously prepare wasm: "+b);B(b)})}var h={env:b,global:{NaN:NaN,Infinity:Infinity},"global.Math":Math,asm2wasm:aa};N++;a.monitorRunDependencies&&a.monitorRunDependencies(N);if(a.instantiateWasm)try{return a.instantiateWasm(h,
c)}catch(k){return E("Module.instantiateWasm callback failed with error: "+k),!1}(function(){return a.wasmBinary||"function"!==typeof WebAssembly.instantiateStreaming||ra()||"function"!==typeof fetch?e(d):WebAssembly.instantiateStreaming(fetch(Q,{credentials:"same-origin"}),h).then(d,function(b){E("wasm streaming compile failed: "+b);E("falling back to ArrayBuffer instantiation");e(d)})})();return{}}
a.asm=function(b,c){c.memory=F;c.table=new WebAssembly.Table({initial:16,maximum:16,element:"anyfunc"});c.__memory_base=1024;c.__table_base=0;return va(c)};function wa(){return ca.length}function xa(b){b=I(b);var c=buffer.byteLength;try{return-1!==F.grow((b-c)/65536)?(buffer=F.buffer,!0):!1}catch(d){return!1}}
var ya=a.asm({},{c:B,b:function(b){a.___errno_location&&(K[a.___errno_location()>>2]=b);return b},i:wa,h:function(b,c,d){J.set(J.subarray(c,c+d),b)},g:function(b){if(2147418112<b)return!1;for(var c=Math.max(wa(),16777216);c<b;)536870912>=c?c=I(2*c):c=Math.min(I((3*c+2147483648)/4),2147418112);if(!xa(c))return!1;da();return!0},f:function(b,c,d,e,h,k,l,q,C,g,x,G,R,S,la,ma){function T(b,c,e,d,h,k,q,l){b=za.subarray(b,b+c*e);var f=b.buffer;"function"===typeof f.slice?(b=f.slice(b.byteOffset,b.byteOffset+
b.byteLength),b=new Uint8Array(b)):b=new Uint8Array(b);var g,r;for(g=r=0;g<h;g++,r+=c)for(f=0;f<c;f++)b[r+f]=l;for(;g<h+q;g++,r+=c){for(f=0;f<d;f++)b[r+f]=l;for(f=d+k;f<c;f++)b[r+f]=l}for(;g<e;g++,r+=c)for(f=0;f<c;f++)b[r+f]=l;return b}var za=a.HEAPU8,H=a.videoFormat,na=(R&-2)*C/l,oa=(S&-2)*g/q,pa=x*C/l,qa=G*g/q;x===H.cropWidth&&G===H.cropHeight&&(la=H.displayWidth,ma=H.displayHeight);a.frameBuffer={format:{width:l,height:q,chromaWidth:C,chromaHeight:g,cropLeft:R,cropTop:S,cropWidth:x,cropHeight:G,
displayWidth:la,displayHeight:ma},y:{bytes:T(b,c,q,R,S,x,G,0),stride:c},u:{bytes:T(d,e,g,na,oa,pa,qa,128),stride:e},v:{bytes:T(h,k,g,na,oa,pa,qa,128),stride:k}}},e:function(b,c,d,e,h,k,l,q,C,g,x){a.videoFormat={width:b,height:c,chromaWidth:d,chromaHeight:e,cropLeft:q,cropTop:C,cropWidth:k,cropHeight:l,displayWidth:g,displayHeight:x,fps:h};a.loadedMetadata=!0},d:function(){B("OOM")},a:4592},buffer);a.asm=ya;a._free=function(){return a.asm.j.apply(null,arguments)};
a._malloc=function(){return a.asm.k.apply(null,arguments)};a._ogv_video_decoder_async=function(){return a.asm.l.apply(null,arguments)};a._ogv_video_decoder_destroy=function(){return a.asm.m.apply(null,arguments)};a._ogv_video_decoder_init=function(){return a.asm.n.apply(null,arguments)};a._ogv_video_decoder_process_frame=function(){return a.asm.o.apply(null,arguments)};a._ogv_video_decoder_process_header=function(){return a.asm.p.apply(null,arguments)};a.asm=ya;
a.then=function(b){if(a.calledRun)b(a);else{var c=a.onRuntimeInitialized;a.onRuntimeInitialized=function(){c&&c();b(a)}}return a};function U(b){this.name="ExitStatus";this.message="Program terminated with exit("+b+")";this.status=b}U.prototype=Error();U.prototype.constructor=U;P=function Aa(){a.calledRun||V();a.calledRun||(P=Aa)};
function V(){function b(){if(!a.calledRun&&(a.calledRun=!0,!ba)){ja||(ja=!0,M(fa));M(ha);if(a.onRuntimeInitialized)a.onRuntimeInitialized();if(a.postRun)for("function"==typeof a.postRun&&(a.postRun=[a.postRun]);a.postRun.length;){var b=a.postRun.shift();ia.unshift(b)}M(ia)}}if(!(0<N)){if(a.preRun)for("function"==typeof a.preRun&&(a.preRun=[a.preRun]);a.preRun.length;)ka();M(ea);0<N||a.calledRun||(a.setStatus?(a.setStatus("Running..."),setTimeout(function(){setTimeout(function(){a.setStatus("")},1);
b()},1)):b())}}a.run=V;function B(b){if(a.onAbort)a.onAbort(b);void 0!==b?(D(b),E(b),b=JSON.stringify(b)):b="";ba=!0;throw"abort("+b+"). Build with -s ASSERTIONS=1 for more info.";}a.abort=B;if(a.preInit)for("function"==typeof a.preInit&&(a.preInit=[a.preInit]);0<a.preInit.length;)a.preInit.pop()();a.noExitRuntime=!0;V();var W,X,Y;Y="undefined"===typeof performance||"undefined"===typeof performance.now?Date.now:performance.now.bind(performance);
function Z(b){var c=Y();b=b();a.cpuTime+=Y()-c;return b}a.loadedMetadata=!!m.videoFormat;a.videoFormat=m.videoFormat||null;a.frameBuffer=null;a.cpuTime=0;Object.defineProperty(a,"processing",{get:function(){return!1}});a.init=function(b){Z(function(){a._ogv_video_decoder_init()});b()};a.processHeader=function(b,c){var d=Z(function(){var c=b.byteLength;W&&X>=c||(W&&a._free(W),X=c,W=a._malloc(X));var d=W;a.HEAPU8.set(new Uint8Array(b),d);return a._ogv_video_decoder_process_header(d,c)});c(d)};a.w=[];
a.processFrame=function(b,c){function d(b){a._free(k);c(b)}var e=a._ogv_video_decoder_async(),h=b.byteLength,k=a._malloc(h);e&&a.w.push(d);var l=Z(function(){a.HEAPU8.set(new Uint8Array(b),k);return a._ogv_video_decoder_process_frame(k,h)});e||d(l)};a.close=function(){};a.sync=function(){a._ogv_video_decoder_async()&&(a.w.push(function(){}),Z(function(){a._ogv_video_decoder_process_frame(0,0)}))};


  return OGVDecoderVideoTheoraW
}
);
})();
if (typeof exports === 'object' && typeof module === 'object')
      module.exports = OGVDecoderVideoTheoraW;
    else if (typeof define === 'function' && define['amd'])
      define([], function() { return OGVDecoderVideoTheoraW; });
    else if (typeof exports === 'object')
      exports["OGVDecoderVideoTheoraW"] = OGVDecoderVideoTheoraW;
    