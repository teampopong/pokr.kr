define([
    'text!./member.tmpl.html',
    'lib/js/bootstrap-tooltip'
    ], function (
        memberTmpl
    ) {

    return Backbone.View.extend({

        template: _.template(memberTmpl),

        render: function () {
            if (!this.model) {
                this.$el.text('not found');
                return this.$el;
            }

            var html = this.template({
                    q: this.model.get('name'),
                    member: this.model.toJSON()
                });

            this.$el.html(html);
            this.registerTooltip();

            return this.$el;
        },

        search: function (name) {
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

