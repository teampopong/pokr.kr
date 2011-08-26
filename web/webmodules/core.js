WM = parent.WM;
jQuery = parent.jQuery; $ = parent.$; // jQuery
_ = parent._; // Underscore.js

function WebModule(moduleName) {
    // prototype for WebModule
    this.name = moduleName;
    this.base = WM.pathForModuleName(moduleName);

    this.display = function(path, context) {
        // FIXME check if url is relative or not?
        return WM.webmodules.presentation.display(module.base +"/"+ path, context);
    };
    this.loadCSS = function(path) {
        // FIXME check if url is relative or not?
        return WM.webmodules.presentation.loadCSS(module.base +"/"+ path);
    };
	this.loadJSON = function(name, url) {
		return WM.db.loadJSON(moduleName, name, url);
	};
}
module = new WebModule(moduleName);

// Setup general utils
String.prototype.format = function () {
	var formatted = this;
	for (var i = 0; i < arguments.length; i++) {
		var regexp = new RegExp('\\{'+i+'\\}', 'gi');
		formatted = formatted.replace(regexp, arguments[i]);
	}
	return formatted;
};

String.prototype.summarize = function (maxlength, suffix) {
	suffix = suffix || '...';

	if (this.length > maxlength) {
		return this.substr(0, maxlength - 1) + suffix;
	} else {
		return this;
	}
};

String.prototype.startsWith = function (substr) {
	return this.slice(0, substr.length) == substr;
}

String.prototype.contains = function (substr) {
	return this.indexOf(substr) != -1;
}

function isArray(obj) {
	return typeof(obj) === 'object' && obj.length !== undefined;
};

function sortObject(o) {
	var sorted = {},
	key, a = [];

	for (key in o) {
		if (o.hasOwnProperty(key)) {
			a.push(key);
		}
	}

	a.sort();

	for (key = 0; key < a.length; key++) {
		sorted[a[key]] = o[a[key]];
	}
	return sorted;
}
