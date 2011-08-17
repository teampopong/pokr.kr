WM = parent.WM;
jQuery = parent.jQuery; $ = parent.$;

function WebModule(moduleName) {
    // prototype for WebModule
    this.name = moduleName;
    this.base = WM.pathForModuleName(moduleName);

    this.display = function(path) {
        // FIXME check if url is relative or not?
        return WM.webmodules.presentation.display(module.base +"/"+ path);
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

String.prototype.summarize = function (maxlength) {
	if (this.length > maxlength) {
		return this.substr(0, maxlength - 1);
	} else {
		return this;
	}
};

String.prototype.startsWith = function (substr) {
	return this.slice(0, substr.length) == substr;
}

String.prototype.contains = function (substr) {
	return str.indexOf(substr) != -1;
}

function Set() {
	var keywords = [];

	function isKeyword(item) {
		for (var i in keywords)
			if (keywords[i] === item)
				return true;
		return false;
	}

	this.add = function (item) {
		if (isKeyword(item)) {
			throw "the name {0} is not allowed".format(item);
		}
		this[item] = true;
	};

	this.toArray = function () {
		var arr = [];
		for (var item in this) {
			if (this.hasOwnProperty(item) && !isKeyword(item)) {
				arr.push(item);
			}
		}
	};

	for (var i in this) {
		if (this.hasOwnProperty(i) && typeof i == 'function') {
			keywords.push(i);
		}
	}
};

function isArray(obj) {
	return typeof(obj) === 'object' && obj.length !== undefined;
};
