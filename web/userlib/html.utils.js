define(function () {
    var loadedCss = {};

    return {
        loadCss: function (url) {
            if (loadedCss[url]) return;

            var link = document.createElement("link");
            link.type = "text/css";
            link.rel = "stylesheet";
            link.href = url;
            document.getElementsByTagName("head")[0].appendChild(link);

            loadedCss[url] = true;
        }
    };
});
