define([
    'text!./member.tmpl.html',
    'text!./member.notfound.tmpl.html'
    ], function (
        memberTmpl,
        notFoundTmpl
    ) {

    return Backbone.View.extend({

        template: _.template(memberTmpl),
        notFoundTemplate: _.template(notFoundTmpl),

        initialize: function (options) {
            this.app = options.app;
        },

        hide: function () {
            this.$el.hide();
        },

        render: function () {
            var template = this.model ? this.template : this.notFoundTemplate,
                html = template({
                    q: this.q,
                    member: this.model && this.model.toJSON() || null
                });

            this.$el.html(html);

            return this.$el;
        },

        search: function (name) {
            this.q = name;
            this.model = this.collection.find(function (member) {
                    // TODO: n-gram w/ misspell tolerance
                    return member.get('name') == name;
                });
            this.render().show();
        }
    });
});

