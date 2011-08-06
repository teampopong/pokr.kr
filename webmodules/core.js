WM = parent.WM;
jQuery = parent.jQuery; $ = parent.$;

function WebModule(name) {
    // prototype for WebModule
    this.name = name;
    this.base = WM.pathForModuleName(name);

    var presentationFrame;
    this.display = function(path) {
        // FIXME check if url is relative or not?
        return WM.webmodules.presentation.display(module.base +"/"+ path);
    };
}
module = new WebModule(moduleName);
