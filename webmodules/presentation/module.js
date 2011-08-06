var presentationFrame;
module.display = function(url) {
    // TODO manage frames
    // TODO remove previous ones
    if (!presentationFrame) {
        presentationFrame = WM.addHTMLElement(
                "div", {
                    attributes: {
                        id: "webmodules-presentation-frame"
                    }
                });
    }
    return $.get(url).then(
            function(data) {
                presentationFrame.innerHTML = data;
                // TODO hook all links to history API
            },
            function(error) {
                // TODO nicely display error
                alert("Error loading " + url);
            }
            );
};

WM.addHTMLElement("style", {
    attributes: {
        type: "text/css",
        src: module.base + "/style.css"
    }
});
