define([
    'text!./main.tmpl.html',
    'userlib/base.view'
    ], function (
        MainTmpl,
        BaseView
    ) {

    return BaseView.extend({
        template: _.template(MainTmpl),
    });
});
