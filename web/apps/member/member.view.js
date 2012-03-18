define([
    'text!./member.tmpl.html',
    'text!./member.notfound.tmpl.html',
    'lib/js/bootstrap-tooltip'
    ], function (
        memberTmpl,
        notFoundTmpl
    ) {

    return Backbone.View.extend({

        template: _.template(memberTmpl),
        notFoundTemplate: _.template(notFoundTmpl),

        render: function () {
            var template = this.model ? this.template : this.notFoundTemplate,
                html = template({
                    q: this.q,
                    member: this.model && this.model.toJSON() || null
                });

            this.$el.html(html);
            this.registerTooltip();

            return this.$el;
        },

        search: function (name) {
            this.q = name;
            this.model = this.collection.find(function (member) {
                    // TODO: n-gram w/ misspell tolerance
                    return member.get('name') == name;
                });
            this.render().show();
        },

        registerTooltip: function () {
            $('#member-age', this.el).tooltip();
        }
    });
});

