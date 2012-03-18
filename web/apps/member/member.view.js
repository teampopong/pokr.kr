define([
    'text!./member.tmpl.html',
    ], function (
        memberTmpl
    ) {

    return Backbone.View.extend({

        template: _.template(memberTmpl),

        search: function (name) {
            var member = this.collection.find(function (member) {
                    // TODO: n-gram w/ misspell tolerance
                    return member.get('name') == name;
                });

            if (!member) {
                this.$el.text('not found');
                return;
            }

            var html = this.template({
                    q: name,
                    member: member.toJSON()
                });
            this.$el.html(html);
        }
    });
});

