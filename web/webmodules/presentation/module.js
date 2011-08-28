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

	if (context) {
		return module.template(url).then(
				function(template) {
					presentationFrame.innerHTML = template(context);
				},
				function(error) {
					// TODO nicely display error
					alert("Error loading " + url);
				}
				);

	} else {
		return $.get(url).then(
				function(html) {
					presentationFrame.innerHTML = html;
				},
				function(error) {
					// TODO nicely display error
					alert("Error loading " + url);
				}
				);
	}
};

module.template = function (url) {
	var defer = $.Deferred();

	if (compiled_templates[url]) {
		var template = compiled_templates[url];
		defer.resolve(template);

	} else {
		$.get(url).then(
				function(html) {
					compiled_templates[url] = template = _.template(html);
					defer.resolve(template);
				},
				function(error) {
					// TODO nicely display error
					alert("Error loading " + url);
				}
				);
	}

	return defer;
}

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
