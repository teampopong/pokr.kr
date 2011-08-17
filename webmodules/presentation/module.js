var PRESENTATION_FRAME_ID = 'webmodules-presentation-frame';
var presentationFrame;

module.display = function(url) {
    // TODO manage frames
    // TODO remove previous ones
    if (!presentationFrame) {
        presentationFrame = WM.addHTMLElement(
                "div", {
                    attributes: {
                        id: PRESENTATION_FRAME_ID
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

module.loadCSS = function (url) {
	WM.addHTMLElement("link", {
				attributes: {
					rel: "stylesheet",
					type: "text/css",
					href: url
				},
				target: parent.document.getElementById(PRESENTATION_FRAME_ID)
			});
};
