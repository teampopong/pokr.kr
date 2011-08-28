// WebModules -- a set of scripts and conventions to build a modular web site
// Author: Jaeho Shin <netj@sparcs.org>
// Created: 2011-08-01

function WebModules() {
    var WM = this;
    // TODO track basepath
    var readyListBeforeInit = [];
    this.ready = function(fn) { readyListBeforeInit.push(fn) };
    this.init = function() {
        $(window).load(function() {
            var d = WM.loadModule("webmodules.presentation");
            d = d.pipe(function(){ return WM.loadModule("db"); });
            d = d.pipe(function(){ return WM.loadModule("webmodules.urlrouter"); });
            // TODO dependency btwn modules?
            for (var i in readyListBeforeInit)
                d.done(readyListBeforeInit[i]);
        });
    };
    this.debug = function() {
        /* XXX remove me */
        arguments[arguments.length++] = "(WebModules)";
        console.log.apply(console, arguments);
    };
    this.addHTMLElement = function(name, params) {
        var doc = params.document;
        if (!doc)
            doc = document;
        var e = doc.createElement(name);
        var properties = params.properties;
        if (properties)
            for (var propName in properties)
                e[propName] = properties[propName];
        var attributes = params.attributes;
        if (attributes)
            for (var attrName in attributes)
                e.setAttribute(attrName, attributes[attrName]);
        var content = params.content;
        if (content)
            e.innerHTML = content;
        var target = params.target;
        if (!target)
            target = doc.body;
        target.appendChild(e);
        return e;
    };
    this.pathForModuleName = function(moduleName) {
        return moduleName.replace(/\./, "/");
    };
    this._modules = [];
    this.registerModule = function(moduleName, module) {
        this.debug("loaded "+ moduleName);
        this._modules[moduleName] = module;
        var moduleNameSegments = moduleName.split(/\./);
        var last = moduleNameSegments.pop();
        var p = WM;
        for (var i in moduleNameSegments) {
            var s = moduleNameSegments[i];
            if (p[s] == undefined)
                p[s] = {};
            if (typeof p[s] != "object")
                throw Error("module name '" + moduleName + "' contains a name overwriting existing object: " + s);
            p = p[s];
        }
        p[last] = module;
        // TODO signal module observers
    };
    // module loader using iframe, avoid redundant loading
    this.loadModule = function(moduleName) {
        var defer = $.Deferred();
        // TODO check _modules first
        var module = this._modules[moduleName];
        if (module) {
            defer.resolve(module);
            return defer;
        }
        var sandbox = this.addHTMLElement("iframe", {
            attributes: {
                name: moduleName + "-WebModulesLoaderSandbox",
                style: "display: none;"
            }
        });
        var w = sandbox.contentWindow;
        w.moduleName = moduleName;
        w.moduleBase = WM.pathForModuleName(moduleName);
        // top-half
        WM.addHTMLElement("script", {
            properties: {
                src: "webmodules/core.js",
                onload: function(){
                    // module body
                    WM.addHTMLElement("script", {
                        properties: {
                            src: w.moduleBase + "/module.js",
                            onload: function() {
                                // bottom-half
                                var m = w.module;
                                WM.registerModule(moduleName, m);
                                if (m.onload)
                                    setTimeout(m.onload, 1);
                                // XXX unviable: sandbox.parentNode.removeChild(sandbox);
                                w.document.clear();
                                defer.resolve(m);
                            }
                        },
                        document: w.document
                    });
                }
            },
            document: w.document
        });
        return defer;
    };
    return this;
}
WM = new WebModules();

// load external libraries and trigger WM.init()
(function () {
// load jQuery first if not available
if (window.$ && $.fn.jquery >= "1.6")
	loadUnderscore();
else {
    WM.addHTMLElement("script", {
        properties: {
            src: "http://code.jquery.com/jquery-latest.min.js",
            onload: loadUnderscore
        },
        target: document.head
    });
}

// load Underscore.js
function loadUnderscore() {
	if (window._ && _.VERSION >= "1.1.7")
		WM.init();
	else {
		WM.addHTMLElement("script", {
			properties: {
				src: "http://documentcloud.github.com/underscore/underscore-min.js",
				onload: WM.init
			},
			target: document.head
		});
	}
}
})();

// url router
// TODO load the current url (from full path, and hash too?)
// TODO function to jump to a new URL and subsequently route to some module without reloading page w/ HTML5 history API


// presentations
// TODO function for adding+showing/hiding html fragment from URL (within a new iframe?)


// data sources
// TODO function for accessing (+ loading if needed) cached primitive data, e.g. HTML, JSON, XML, ... w/ XHR
// TODO support higher-level data source modules that provide complex operations on them?  or should these be just ordinary modules without presentation stuff?
