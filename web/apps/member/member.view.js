define([
    'text!./member.tmpl.html'
    ], function (
        memberTmpl
    ) {

    return Backbone.View.extend({

        template: _.template(memberTmpl),

        initialize: function (options) {
            this.app = options.app;
        },

        hide: function () {
            this.$el.hide();
        },

        render: function () {
            var html = this.template({
                    member: this.model && this.model.toJSON() || null
                });

            this.$el.html(html);

            return this.$el;
        },

        show: function (model) {
            this.model = model;
            this.render().show();
        }
    });
});

