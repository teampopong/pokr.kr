module = {}

module.loadJSON = function(moduleName, name, url) {
	var defer = $.Deferred();

	$.getJSON(url + '?callback=?', function (data) {
		if (WM[moduleName] == undefined) {
			throw "not existing module";
		}

		WM[moduleName][name] = data

		defer.resolve();
	});

	return defer;
};
