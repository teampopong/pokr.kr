module = {}

module.loadJSON = function(name, url, data) {
	var nameSegments = name.split(/\./);
	var last = nameSegments.pop();
	var p = module;
	for (var i in nameSegments) {
		var s = nameSegments[i];
		if (p[s] == undefined)
			p[s] = {};
		if (typeof p[s] != "object")
			throw Error("variable name '" + name + "' contains a name overwriting existing object: " + s);
		p = p[s];
	}

	if (data) {
		$.getJSON(url, data, function (data) {
			p[last] = data;
		});
	} else {
		$.getJSON(url, function (data) {
			p[last] = data;
		});
	}
};
