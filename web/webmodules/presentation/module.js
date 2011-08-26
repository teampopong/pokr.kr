var PRESENTATION_FRAME_ID = 'webmodules-presentation-frame';
var presentationFrame;

var compiled_templates = {};

module.display = function(url, context) {
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

	// FIXME: should check if the file got changed.

	// When the template is already compiled once
	if (context && compiled_templates[url]) {
		var defer = $.Deferred();
		var template = compiled_templates[url];
		presentationFrame.innerHTML = template(context);
		defer.resolve();
		return defer;
	}

    return $.get(url).then(
            function(html) {
				// In case using template
				if (context) {
					compiled_templates[url] = template = _.template(html);
					presentationFrame.innerHTML = template(context);

				// In case wants raw html
				} else {
					presentationFrame.innerHTML = html;
					// TODO: it can also be cached.

				}
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
