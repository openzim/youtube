
var OGVDecoderVideoVP8W = (function() {
  var _scriptDir = typeof document !== 'undefined' && document.currentScript ? document.currentScript.src : undefined;
  return (
function(OGVDecoderVideoVP8W) {
  OGVDecoderVideoVP8W = OGVDecoderVideoVP8W || {};


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

var a;a||(a=typeof OGVDecoderVideoVP8W !== 'undefined' ? OGVDecoderVideoVP8W : {});var m=a;a.memoryLimit&&(a.TOTAL_MEMORY=m.memoryLimit);var n={},p;for(p in a)a.hasOwnProperty(p)&&(n[p]=a[p]);a.arguments=[];a.thisProgram="./this.program";a.quit=function(b,c){throw c;};a.preRun=[];a.postRun=[];var q=!1,r=!1,t=!1,aa=!1;q="object"===typeof window;r="function"===typeof importScripts;t="object"===typeof process&&"function"===typeof require&&!q&&!r;aa=!q&&!t&&!r;var v="";
if(t){v=__dirname+"/";var w,x;a.read=function(b,c){w||(w=require("fs"));x||(x=require("path"));b=x.normalize(b);b=w.readFileSync(b);return c?b:b.toString()};a.readBinary=function(b){b=a.read(b,!0);b.buffer||(b=new Uint8Array(b));b.buffer||y("Assertion failed: undefined");return b};1<process.argv.length&&(a.thisProgram=process.argv[1].replace(/\\/g,"/"));a.arguments=process.argv.slice(2);process.on("unhandledRejection",y);a.quit=function(b){process.exit(b)};a.inspect=function(){return"[Emscripten Module object]"}}else if(aa)"undefined"!=
typeof read&&(a.read=function(b){return read(b)}),a.readBinary=function(b){if("function"===typeof readbuffer)return new Uint8Array(readbuffer(b));b=read(b,"binary");"object"===typeof b||y("Assertion failed: undefined");return b},"undefined"!=typeof scriptArgs?a.arguments=scriptArgs:"undefined"!=typeof arguments&&(a.arguments=arguments),"function"===typeof quit&&(a.quit=function(b){quit(b)});else if(q||r)r?v=self.location.href:document.currentScript&&(v=document.currentScript.src),_scriptDir&&(v=_scriptDir),
0!==v.indexOf("blob:")?v=v.substr(0,v.lastIndexOf("/")+1):v="",a.read=function(b){var c=new XMLHttpRequest;c.open("GET",b,!1);c.send(null);return c.responseText},r&&(a.readBinary=function(b){var c=new XMLHttpRequest;c.open("GET",b,!1);c.responseType="arraybuffer";c.send(null);return new Uint8Array(c.response)}),a.readAsync=function(b,c,d){var e=new XMLHttpRequest;e.open("GET",b,!0);e.responseType="arraybuffer";e.onload=function(){200==e.status||0==e.status&&e.response?c(e.response):d()};e.onerror=
d;e.send(null)},a.setWindowTitle=function(b){document.title=b};var ba=a.print||("undefined"!==typeof console?console.log.bind(console):"undefined"!==typeof print?print:null),A=a.printErr||("undefined"!==typeof printErr?printErr:"undefined"!==typeof console&&console.warn.bind(console)||ba);for(p in n)n.hasOwnProperty(p)&&(a[p]=n[p]);n=void 0;var ca={"f64-rem":function(b,c){return b%c},"debugger":function(){debugger}},da=0;"object"!==typeof WebAssembly&&A("no native wasm support detected");
var B,ea=!1;"undefined"!==typeof TextDecoder&&new TextDecoder("utf8");"undefined"!==typeof TextDecoder&&new TextDecoder("utf-16le");function C(b){0<b%65536&&(b+=65536-b%65536);return b}var buffer,fa,D,F;function ha(){a.HEAP8=fa=new Int8Array(buffer);a.HEAP16=new Int16Array(buffer);a.HEAP32=F=new Int32Array(buffer);a.HEAPU8=D=new Uint8Array(buffer);a.HEAPU16=new Uint16Array(buffer);a.HEAPU32=new Uint32Array(buffer);a.HEAPF32=new Float32Array(buffer);a.HEAPF64=new Float64Array(buffer)}
var G=a.TOTAL_MEMORY||16777216;5242880>G&&A("TOTAL_MEMORY should be larger than TOTAL_STACK, was "+G+"! (TOTAL_STACK=5242880)");a.buffer?buffer=a.buffer:"object"===typeof WebAssembly&&"function"===typeof WebAssembly.Memory?(B=new WebAssembly.Memory({initial:G/65536}),buffer=B.buffer):buffer=new ArrayBuffer(G);ha();F[2380]=5252432;
function H(b){for(;0<b.length;){var c=b.shift();if("function"==typeof c)c();else{var d=c.N;"number"===typeof d?void 0===c.L?a.dynCall_v(d):a.dynCall_vi(d,c.L):d(void 0===c.L?null:c.L)}}}var ia=[],ja=[],ka=[],la=[],ma=!1;function na(){var b=a.preRun.shift();ia.unshift(b)}var L=0,M=null,N=null;a.preloadedImages={};a.preloadedAudios={};
function oa(){var b=O;return String.prototype.startsWith?b.startsWith("data:application/octet-stream;base64,"):0===b.indexOf("data:application/octet-stream;base64,")}var O="ogv-decoder-video-vp8-wasm.wasm";if(!oa()){var pa=O;O=a.locateFile?a.locateFile(pa,v):v+pa;O=zim_fix_wasm_target(O);}function wa(){try{if(a.wasmBinary)return new Uint8Array(a.wasmBinary);if(a.readBinary)return a.readBinary(O);throw"both async and sync fetching of the wasm failed";}catch(b){y(b)}}
function xa(){return a.wasmBinary||!q&&!r||"function"!==typeof fetch?new Promise(function(b){b(wa())}):fetch(O,{credentials:"same-origin"}).then(function(b){if(!b.ok)throw"failed to load wasm binary file at '"+O+"'";return b.arrayBuffer()}).catch(function(){return wa()})}
function ya(b){function c(b){a.asm=b.exports;L--;a.monitorRunDependencies&&a.monitorRunDependencies(L);0==L&&(null!==M&&(clearInterval(M),M=null),N&&(b=N,N=null,b()))}function d(b){c(b.instance)}function e(b){return xa().then(function(b){return WebAssembly.instantiate(b,f)}).then(b,function(b){A("failed to asynchronously prepare wasm: "+b);y(b)})}var f={env:b,global:{NaN:NaN,Infinity:Infinity},"global.Math":Math,asm2wasm:ca};L++;a.monitorRunDependencies&&a.monitorRunDependencies(L);if(a.instantiateWasm)try{return a.instantiateWasm(f,
c)}catch(g){return A("Module.instantiateWasm callback failed with error: "+g),!1}(function(){return a.wasmBinary||"function"!==typeof WebAssembly.instantiateStreaming||oa()||"function"!==typeof fetch?e(d):WebAssembly.instantiateStreaming(fetch(O,{credentials:"same-origin"}),f).then(d,function(b){A("wasm streaming compile failed: "+b);A("falling back to ArrayBuffer instantiation");e(d)})})();return{}}
a.asm=function(b,c){c.memory=B;c.table=new WebAssembly.Table({initial:94,maximum:94,element:"anyfunc"});c.__memory_base=1024;c.__table_base=0;return ya(c)};function za(){return fa.length}function Aa(b){b=C(b);var c=buffer.byteLength;try{return-1!==B.grow((b-c)/65536)?(buffer=B.buffer,!0):!1}catch(d){return!1}}
var Ja=a.asm({},{e:y,c:function(b){da=b},b:function(){return da},m:function(b,c){var d=P();try{return Ba(b,c)}catch(e){Q(d);if(e!==e+0&&"longjmp"!==e)throw e;R(1,0)}},i:function(b,c,d){var e=P();try{return Ca(b,c,d)}catch(f){Q(e);if(f!==f+0&&"longjmp"!==f)throw f;R(1,0)}},l:function(b,c,d,e){var f=P();try{return Da(b,c,d,e)}catch(g){Q(f);if(g!==g+0&&"longjmp"!==g)throw g;R(1,0)}},n:function(b,c,d,e,f,g){var k=P();try{return Ea(b,c,d,e,f,g)}catch(l){Q(k);if(l!==l+0&&"longjmp"!==l)throw l;R(1,0)}},
h:function(b){var c=P();try{Fa(b)}catch(d){Q(c);if(d!==d+0&&"longjmp"!==d)throw d;R(1,0)}},f:function(b,c){var d=P();try{Ga(b,c)}catch(e){Q(d);if(e!==e+0&&"longjmp"!==e)throw e;R(1,0)}},k:function(b,c,d){var e=P();try{Ha(b,c,d)}catch(f){Q(e);if(f!==f+0&&"longjmp"!==f)throw f;R(1,0)}},g:function(b,c,d,e,f){var g=P();try{Ia(b,c,d,e,f)}catch(k){Q(g);if(k!==k+0&&"longjmp"!==k)throw k;R(1,0)}},j:function(b){a.___errno_location&&(F[a.___errno_location()>>2]=b);return b},s:za,r:function(b,c,d){D.set(D.subarray(c,
c+d),b)},q:function(b){if(2147418112<b)return!1;for(var c=Math.max(za(),16777216);c<b;)536870912>=c?c=C(2*c):c=Math.min(C((3*c+2147483648)/4),2147418112);if(!Aa(c))return!1;ha();return!0},d:function(b,c){R(b,c||1);throw"longjmp";},p:function(b,c,d,e,f,g,k,l,U,E,I,J,V,W,qa,ra){function X(b,c,e,d,f,g,k,l){b=Ma.subarray(b,b+c*e);var h=b.buffer;"function"===typeof h.slice?(b=h.slice(b.byteOffset,b.byteOffset+b.byteLength),b=new Uint8Array(b)):b=new Uint8Array(b);var z,u;for(z=u=0;z<f;z++,u+=c)for(h=0;h<
c;h++)b[u+h]=l;for(;z<f+k;z++,u+=c){for(h=0;h<d;h++)b[u+h]=l;for(h=d+g;h<c;h++)b[u+h]=l}for(;z<e;z++,u+=c)for(h=0;h<c;h++)b[u+h]=l;return b}var Ma=a.HEAPU8,K=a.videoFormat,sa=(V&-2)*U/k,ta=(W&-2)*E/l,ua=I*U/k,va=J*E/l;I===K.cropWidth&&J===K.cropHeight&&(qa=K.displayWidth,ra=K.displayHeight);a.frameBuffer={format:{width:k,height:l,chromaWidth:U,chromaHeight:E,cropLeft:V,cropTop:W,cropWidth:I,cropHeight:J,displayWidth:qa,displayHeight:ra},y:{bytes:X(b,c,l,V,W,I,J,0),stride:c},u:{bytes:X(d,e,E,sa,ta,
ua,va,128),stride:e},v:{bytes:X(f,g,E,sa,ta,ua,va,128),stride:g}}},o:function(){y("OOM")},a:9520},buffer);a.asm=Ja;a._free=function(){return a.asm.t.apply(null,arguments)};a._malloc=function(){return a.asm.u.apply(null,arguments)};a._ogv_video_decoder_async=function(){return a.asm.v.apply(null,arguments)};a._ogv_video_decoder_destroy=function(){return a.asm.w.apply(null,arguments)};a._ogv_video_decoder_init=function(){return a.asm.x.apply(null,arguments)};
a._ogv_video_decoder_process_frame=function(){return a.asm.y.apply(null,arguments)};a._ogv_video_decoder_process_header=function(){return a.asm.z.apply(null,arguments)};
var R=a._setThrew=function(){return a.asm.A.apply(null,arguments)},Q=a.stackRestore=function(){return a.asm.J.apply(null,arguments)},P=a.stackSave=function(){return a.asm.K.apply(null,arguments)},Ba=a.dynCall_ii=function(){return a.asm.B.apply(null,arguments)},Ca=a.dynCall_iii=function(){return a.asm.C.apply(null,arguments)},Da=a.dynCall_iiii=function(){return a.asm.D.apply(null,arguments)},Ea=a.dynCall_iiiij=function(){return a.asm.E.apply(null,arguments)},Fa=a.dynCall_v=function(){return a.asm.F.apply(null,
arguments)},Ga=a.dynCall_vi=function(){return a.asm.G.apply(null,arguments)},Ha=a.dynCall_vii=function(){return a.asm.H.apply(null,arguments)},Ia=a.dynCall_viiii=function(){return a.asm.I.apply(null,arguments)};a.asm=Ja;a.then=function(b){if(a.calledRun)b(a);else{var c=a.onRuntimeInitialized;a.onRuntimeInitialized=function(){c&&c();b(a)}}return a};function S(b){this.name="ExitStatus";this.message="Program terminated with exit("+b+")";this.status=b}S.prototype=Error();S.prototype.constructor=S;
N=function Ka(){a.calledRun||T();a.calledRun||(N=Ka)};
function T(){function b(){if(!a.calledRun&&(a.calledRun=!0,!ea)){ma||(ma=!0,H(ja));H(ka);if(a.onRuntimeInitialized)a.onRuntimeInitialized();if(a.postRun)for("function"==typeof a.postRun&&(a.postRun=[a.postRun]);a.postRun.length;){var b=a.postRun.shift();la.unshift(b)}H(la)}}if(!(0<L)){if(a.preRun)for("function"==typeof a.preRun&&(a.preRun=[a.preRun]);a.preRun.length;)na();H(ia);0<L||a.calledRun||(a.setStatus?(a.setStatus("Running..."),setTimeout(function(){setTimeout(function(){a.setStatus("")},1);
b()},1)):b())}}a.run=T;function y(b){if(a.onAbort)a.onAbort(b);void 0!==b?(ba(b),A(b),b=JSON.stringify(b)):b="";ea=!0;throw"abort("+b+"). Build with -s ASSERTIONS=1 for more info.";}a.abort=y;if(a.preInit)for("function"==typeof a.preInit&&(a.preInit=[a.preInit]);0<a.preInit.length;)a.preInit.pop()();a.noExitRuntime=!0;T();var Y,La,Na;Na="undefined"===typeof performance||"undefined"===typeof performance.now?Date.now:performance.now.bind(performance);
function Z(b){var c=Na();b=b();a.cpuTime+=Na()-c;return b}a.loadedMetadata=!!m.videoFormat;a.videoFormat=m.videoFormat||null;a.frameBuffer=null;a.cpuTime=0;Object.defineProperty(a,"processing",{get:function(){return!1}});a.init=function(b){Z(function(){a._ogv_video_decoder_init()});b()};a.processHeader=function(b,c){var d=Z(function(){var c=b.byteLength;Y&&La>=c||(Y&&a._free(Y),La=c,Y=a._malloc(La));var d=Y;a.HEAPU8.set(new Uint8Array(b),d);return a._ogv_video_decoder_process_header(d,c)});c(d)};
a.M=[];a.processFrame=function(b,c){function d(b){a._free(g);c(b)}var e=a._ogv_video_decoder_async(),f=b.byteLength,g=a._malloc(f);e&&a.M.push(d);var k=Z(function(){a.HEAPU8.set(new Uint8Array(b),g);return a._ogv_video_decoder_process_frame(g,f)});e||d(k)};a.close=function(){};a.sync=function(){a._ogv_video_decoder_async()&&(a.M.push(function(){}),Z(function(){a._ogv_video_decoder_process_frame(0,0)}))};


  return OGVDecoderVideoVP8W
}
);
})();
if (typeof exports === 'object' && typeof module === 'object')
      module.exports = OGVDecoderVideoVP8W;
    else if (typeof define === 'function' && define['amd'])
      define([], function() { return OGVDecoderVideoVP8W; });
    else if (typeof exports === 'object')
      exports["OGVDecoderVideoVP8W"] = OGVDecoderVideoVP8W;
    