trigger_webp_polyfill = function () {
    webpHero.detectWebpSupport().then(function (support_webp){
        if (!support_webp) {
            console.log("no WebP support, polyfilling.");
            // un-hide ogvjs-poster so the polyfill can transform it
            $(".ogvjs-poster").css("visibility", "");
            // hide video-js poster (which uses background-image)
            $(".vjs-poster").css("display", "none");

            let webpMachine = new webpHero.WebpMachine();
            webpMachine.polyfillDocument();
        }
    });
}

$(document).ready(function() { trigger_webp_polyfill(); });
