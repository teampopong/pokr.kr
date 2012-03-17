(function (global) { // prevent global scope

var $app;

define([
    'require',

    // Templates
    'text!./main.tmpl.html',

    // Data
    'json!data/members.json',

    // MVC Components
    'userlib/base.view',
    ], function (
        require,

        // Templates
        mainTmpl,

        // Data
        members,

        // MVC Components
        BaseView
    ) {

    POPONG.Utils.loadCss(require.toUrl('./member.css'));

    return BaseView.extend({

        template: _.template(mainTmpl),

        context: {},

        show: function () {
            BaseView.prototype.show.apply(this, arguments);

            $app = $('#member-search');
            registerEvents();
        },
    });
});

function registerEvents() {
    $('#member-search-form', $app).submit(function () {
        var text = $('input[name="q"]', $app).val();
        alert(text);
        return false;
    });
}

}(window));
