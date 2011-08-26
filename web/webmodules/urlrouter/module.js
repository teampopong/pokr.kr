var map;
module.routeURL = function() {
    // handle #! hashes
    var path = parent.location.hash.replace(/^#!/, "");
    // TODO basepath
    // var path = parent.location.pathname;
    for (var m in map) {
        var re = new RegExp("^" + map[m].urls + "$");
        var args = re.exec(path);
        if (args != null) {
            args.shift();
            WM.debug("routing '"+ path +"' to " + m);
            return WM.loadModule(m).then(function(module){
                module.load.apply(module, args);
            });
        }
    }
    WM.debug("no route for '"+ path +"'");
};

module.onload = function() {
    parent.$("link[rel='webmodules-map']", parent.document).each(function(){
        parent.$.getJSON(this.href).then(function(map1){
            if (!map)
                map = map1;
            // TODO merge multiple maps
            module.routeURL();
            // TODO we might need http://benalman.com/projects/jquery-hashchange-plugin/
            parent.$(parent).bind("hashchange", module.routeURL);
        });
    });
    // TODO hook a onclick's to hash changes or HTML5 history API
};
