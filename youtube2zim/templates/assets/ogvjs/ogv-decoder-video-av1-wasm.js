
var OGVDecoderVideoAV1W = (function() {
  var _scriptDir = typeof document !== 'undefined' && document.currentScript ? document.currentScript.src : undefined;
  return (
function(OGVDecoderVideoAV1W) {
  OGVDecoderVideoAV1W = OGVDecoderVideoAV1W || {};


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

var a;a||(a=typeof OGVDecoderVideoAV1W !== 'undefined' ? OGVDecoderVideoAV1W : {});var p=a;a.memoryLimit&&(a.TOTAL_MEMORY=p.memoryLimit);var q={},u;for(u in a)a.hasOwnProperty(u)&&(q[u]=a[u]);a.arguments=[];a.thisProgram="./this.program";a.quit=function(b,c){throw c;};a.preRun=[];a.postRun=[];var v=!1,y=!1,z=!1,aa=!1;v="object"===typeof window;y="function"===typeof importScripts;z="object"===typeof process&&"function"===typeof require&&!v&&!y;aa=!v&&!z&&!y;var A="";
if(z){A=__dirname+"/";var B,E;a.read=function(b,c){B||(B=require("fs"));E||(E=require("path"));b=E.normalize(b);b=B.readFileSync(b);return c?b:b.toString()};a.readBinary=function(b){b=a.read(b,!0);b.buffer||(b=new Uint8Array(b));b.buffer||F("Assertion failed: undefined");return b};1<process.argv.length&&(a.thisProgram=process.argv[1].replace(/\\/g,"/"));a.arguments=process.argv.slice(2);process.on("unhandledRejection",F);a.quit=function(b){process.exit(b)};a.inspect=function(){return"[Emscripten Module object]"}}else if(aa)"undefined"!=
typeof read&&(a.read=function(b){return read(b)}),a.readBinary=function(b){if("function"===typeof readbuffer)return new Uint8Array(readbuffer(b));b=read(b,"binary");"object"===typeof b||F("Assertion failed: undefined");return b},"undefined"!=typeof scriptArgs?a.arguments=scriptArgs:"undefined"!=typeof arguments&&(a.arguments=arguments),"function"===typeof quit&&(a.quit=function(b){quit(b)});else if(v||y)y?A=self.location.href:document.currentScript&&(A=document.currentScript.src),_scriptDir&&(A=_scriptDir),
0!==A.indexOf("blob:")?A=A.substr(0,A.lastIndexOf("/")+1):A="",a.read=function(b){var c=new XMLHttpRequest;c.open("GET",b,!1);c.send(null);return c.responseText},y&&(a.readBinary=function(b){var c=new XMLHttpRequest;c.open("GET",b,!1);c.responseType="arraybuffer";c.send(null);return new Uint8Array(c.response)}),a.readAsync=function(b,c,d){var e=new XMLHttpRequest;e.open("GET",b,!0);e.responseType="arraybuffer";e.onload=function(){200==e.status||0==e.status&&e.response?c(e.response):d()};e.onerror=
d;e.send(null)},a.setWindowTitle=function(b){document.title=b};var H=a.print||("undefined"!==typeof console?console.log.bind(console):"undefined"!==typeof print?print:null),I=a.printErr||("undefined"!==typeof printErr?printErr:"undefined"!==typeof console&&console.warn.bind(console)||H);for(u in q)q.hasOwnProperty(u)&&(a[u]=q[u]);q=void 0;var ba={"f64-rem":function(b,c){return b%c},"debugger":function(){debugger}};"object"!==typeof WebAssembly&&I("no native wasm support detected");
var J,ca=!1,da="undefined"!==typeof TextDecoder?new TextDecoder("utf8"):void 0;"undefined"!==typeof TextDecoder&&new TextDecoder("utf-16le");function K(b){0<b%65536&&(b+=65536-b%65536);return b}var buffer,ea,P,Q;function fa(){a.HEAP8=ea=new Int8Array(buffer);a.HEAP16=new Int16Array(buffer);a.HEAP32=Q=new Int32Array(buffer);a.HEAPU8=P=new Uint8Array(buffer);a.HEAPU16=new Uint16Array(buffer);a.HEAPU32=new Uint32Array(buffer);a.HEAPF32=new Float32Array(buffer);a.HEAPF64=new Float64Array(buffer)}
var R=a.TOTAL_MEMORY||16777216;5242880>R&&I("TOTAL_MEMORY should be larger than TOTAL_STACK, was "+R+"! (TOTAL_STACK=5242880)");a.buffer?buffer=a.buffer:"object"===typeof WebAssembly&&"function"===typeof WebAssembly.Memory?(J=new WebAssembly.Memory({initial:R/65536}),buffer=J.buffer):buffer=new ArrayBuffer(R);fa();Q[97380]=5632432;
function S(b){for(;0<b.length;){var c=b.shift();if("function"==typeof c)c();else{var d=c.H;"number"===typeof d?void 0===c.C?a.dynCall_v(d):a.dynCall_vi(d,c.C):d(void 0===c.C?null:c.C)}}}var ha=[],ia=[],ja=[],ka=[],la=!1;function ma(){var b=a.preRun.shift();ha.unshift(b)}var T=0,na=null,U=null;a.preloadedImages={};a.preloadedAudios={};
function oa(){var b=V;return String.prototype.startsWith?b.startsWith("data:application/octet-stream;base64,"):0===b.indexOf("data:application/octet-stream;base64,")}var V="ogv-decoder-video-av1-wasm.wasm";if(!oa()){var pa=V;V=a.locateFile?a.locateFile(pa,A):A+pa;V=zim_fix_wasm_target(V);}function qa(){try{if(a.wasmBinary)return new Uint8Array(a.wasmBinary);if(a.readBinary)return a.readBinary(V);throw"both async and sync fetching of the wasm failed";}catch(b){F(b)}}
function ra(){return a.wasmBinary||!v&&!y||"function"!==typeof fetch?new Promise(function(b){b(qa())}):fetch(V,{credentials:"same-origin"}).then(function(b){if(!b.ok)throw"failed to load wasm binary file at '"+V+"'";return b.arrayBuffer()}).catch(function(){return qa()})}
function sa(b){function c(b){a.asm=b.exports;T--;a.monitorRunDependencies&&a.monitorRunDependencies(T);0==T&&(null!==na&&(clearInterval(na),na=null),U&&(b=U,U=null,b()))}function d(b){c(b.instance)}function e(b){return ra().then(function(b){return WebAssembly.instantiate(b,n)}).then(b,function(b){I("failed to asynchronously prepare wasm: "+b);F(b)})}var n={env:b,global:{NaN:NaN,Infinity:Infinity},"global.Math":Math,asm2wasm:ba};T++;a.monitorRunDependencies&&a.monitorRunDependencies(T);if(a.instantiateWasm)try{return a.instantiateWasm(n,
c)}catch(f){return I("Module.instantiateWasm callback failed with error: "+f),!1}(function(){return a.wasmBinary||"function"!==typeof WebAssembly.instantiateStreaming||oa()||"function"!==typeof fetch?e(d):WebAssembly.instantiateStreaming(fetch(V,{credentials:"same-origin"}),n).then(d,function(b){I("wasm streaming compile failed: "+b);I("falling back to ArrayBuffer instantiation");e(d)})})();return{}}
a.asm=function(b,c){c.memory=J;c.table=new WebAssembly.Table({initial:422,maximum:422,element:"anyfunc"});c.__memory_base=1024;c.__table_base=0;return sa(c)};var va=[null,[],[]],W=0;function X(){W+=4;return Q[W-4>>2]}var wa={};function xa(){return ea.length}function ya(b){b=K(b);var c=buffer.byteLength;try{return-1!==J.grow((b-c)/65536)?(buffer=J.buffer,!0):!1}catch(d){return!1}}
var za=a.asm({},{b:F,k:function(b){a.___errno_location&&(Q[a.___errno_location()>>2]=b);return b},q:function(b,c){W=c;try{return wa.G(),X(),X(),X(),X(),0}catch(d){return F(d),-d.F}},h:function(b,c){W=c;try{var d=X(),e=X(),n=X();for(c=b=0;c<n;c++){for(var f=Q[e+8*c>>2],w=Q[e+(8*c+4)>>2],x=0;x<w;x++){var C=P[f+x],r=va[d];if(0===C||10===C){var G=1===d?H:I;for(var l=r,m=0,g=m+void 0,t=m;l[t]&&!(t>=g);)++t;if(16<t-m&&l.subarray&&da)var L=da.decode(l.subarray(m,t));else{for(g="";m<t;){var h=l[m++];if(h&
128){var M=l[m++]&63;if(192==(h&224))g+=String.fromCharCode((h&31)<<6|M);else{var D=l[m++]&63;h=224==(h&240)?(h&15)<<12|M<<6|D:(h&7)<<18|M<<12|D<<6|l[m++]&63;if(65536>h)g+=String.fromCharCode(h);else{var N=h-65536;g+=String.fromCharCode(55296|N>>10,56320|N&1023)}}}else g+=String.fromCharCode(h)}L=g}G(L);r.length=0}else r.push(C)}b+=w}return b}catch(O){return F(O),-O.F}},p:function(b,c){W=c;return 0},o:function(b,c){W=c;try{return wa.G(),0}catch(d){return F(d),-d.F}},g:function(){a.abort()},n:xa,m:function(b,
c,d){P.set(P.subarray(c,c+d),b)},l:function(b){if(2147418112<b)return!1;for(var c=Math.max(xa(),16777216);c<b;)536870912>=c?c=K(2*c):c=Math.min(K((3*c+2147483648)/4),2147418112);if(!ya(c))return!1;fa();return!0},s:function(b,c,d,e,n,f,w,x,C,r,G,l,m,g,t,L){function h(b,c,d,e,h,n,m,l){b=M.subarray(b,b+c*d);var k=b.buffer;"function"===typeof k.slice?(b=k.slice(b.byteOffset,b.byteOffset+b.byteLength),b=new Uint8Array(b)):b=new Uint8Array(b);var g,f;for(g=f=0;g<h;g++,f+=c)for(k=0;k<c;k++)b[f+k]=l;for(;g<
h+m;g++,f+=c){for(k=0;k<e;k++)b[f+k]=l;for(k=e+n;k<c;k++)b[f+k]=l}for(;g<d;g++,f+=c)for(k=0;k<c;k++)b[f+k]=l;return b}var M=a.HEAPU8,D=a.videoFormat,N=(m&-2)*C/w,O=(g&-2)*r/x,ta=G*C/w,ua=l*r/x;G===D.cropWidth&&l===D.cropHeight&&(t=D.displayWidth,L=D.displayHeight);a.frameBuffer={format:{width:w,height:x,chromaWidth:C,chromaHeight:r,cropLeft:m,cropTop:g,cropWidth:G,cropHeight:l,displayWidth:t,displayHeight:L},y:{bytes:h(b,c,x,m,g,G,l,0),stride:c},u:{bytes:h(d,e,r,N,O,ta,ua,128),stride:e},v:{bytes:h(n,
f,r,N,O,ta,ua,128),stride:f}}},e:function(){return 0},f:function(){return 0},d:function(){return 0},c:function(){return 0},j:function(){return 11},i:function(){},r:function(){F("OOM")},a:389520},buffer);a.asm=za;a._free=function(){return a.asm.t.apply(null,arguments)};a._malloc=function(){return a.asm.u.apply(null,arguments)};a._ogv_video_decoder_async=function(){return a.asm.v.apply(null,arguments)};a._ogv_video_decoder_destroy=function(){return a.asm.w.apply(null,arguments)};
a._ogv_video_decoder_init=function(){return a.asm.x.apply(null,arguments)};a._ogv_video_decoder_process_frame=function(){return a.asm.y.apply(null,arguments)};a._ogv_video_decoder_process_header=function(){return a.asm.z.apply(null,arguments)};a.dynCall_v=function(){return a.asm.A.apply(null,arguments)};a.dynCall_vi=function(){return a.asm.B.apply(null,arguments)};a.asm=za;a.then=function(b){if(a.calledRun)b(a);else{var c=a.onRuntimeInitialized;a.onRuntimeInitialized=function(){c&&c();b(a)}}return a};
function Aa(b){this.name="ExitStatus";this.message="Program terminated with exit("+b+")";this.status=b}Aa.prototype=Error();Aa.prototype.constructor=Aa;U=function Ba(){a.calledRun||Ca();a.calledRun||(U=Ba)};
function Ca(){function b(){if(!a.calledRun&&(a.calledRun=!0,!ca)){la||(la=!0,S(ia));S(ja);if(a.onRuntimeInitialized)a.onRuntimeInitialized();if(a.postRun)for("function"==typeof a.postRun&&(a.postRun=[a.postRun]);a.postRun.length;){var b=a.postRun.shift();ka.unshift(b)}S(ka)}}if(!(0<T)){if(a.preRun)for("function"==typeof a.preRun&&(a.preRun=[a.preRun]);a.preRun.length;)ma();S(ha);0<T||a.calledRun||(a.setStatus?(a.setStatus("Running..."),setTimeout(function(){setTimeout(function(){a.setStatus("")},
1);b()},1)):b())}}a.run=Ca;function F(b){if(a.onAbort)a.onAbort(b);void 0!==b?(H(b),I(b),b=JSON.stringify(b)):b="";ca=!0;throw"abort("+b+"). Build with -s ASSERTIONS=1 for more info.";}a.abort=F;if(a.preInit)for("function"==typeof a.preInit&&(a.preInit=[a.preInit]);0<a.preInit.length;)a.preInit.pop()();a.noExitRuntime=!0;Ca();var Y,Da,Ea;Ea="undefined"===typeof performance||"undefined"===typeof performance.now?Date.now:performance.now.bind(performance);
function Z(b){var c=Ea();b=b();a.cpuTime+=Ea()-c;return b}a.loadedMetadata=!!p.videoFormat;a.videoFormat=p.videoFormat||null;a.frameBuffer=null;a.cpuTime=0;Object.defineProperty(a,"processing",{get:function(){return!1}});a.init=function(b){Z(function(){a._ogv_video_decoder_init()});b()};a.processHeader=function(b,c){var d=Z(function(){var c=b.byteLength;Y&&Da>=c||(Y&&a._free(Y),Da=c,Y=a._malloc(Da));var d=Y;a.HEAPU8.set(new Uint8Array(b),d);return a._ogv_video_decoder_process_header(d,c)});c(d)};
a.D=[];a.processFrame=function(b,c){function d(b){a._free(f);c(b)}var e=a._ogv_video_decoder_async(),n=b.byteLength,f=a._malloc(n);e&&a.D.push(d);var w=Z(function(){a.HEAPU8.set(new Uint8Array(b),f);return a._ogv_video_decoder_process_frame(f,n)});e||d(w)};a.close=function(){};a.sync=function(){a._ogv_video_decoder_async()&&(a.D.push(function(){}),Z(function(){a._ogv_video_decoder_process_frame(0,0)}))};


  return OGVDecoderVideoAV1W
}
);
})();
if (typeof exports === 'object' && typeof module === 'object')
      module.exports = OGVDecoderVideoAV1W;
    else if (typeof define === 'function' && define['amd'])
      define([], function() { return OGVDecoderVideoAV1W; });
    else if (typeof exports === 'object')
      exports["OGVDecoderVideoAV1W"] = OGVDecoderVideoAV1W;
    