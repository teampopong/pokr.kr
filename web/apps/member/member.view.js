define([
    ], function () {

    return Backbone.View.extend({
        search: function (name) {
            var member = this.collection.find(function (member) {
                // TODO: n-gram w/ misspell tolerance
                return member.get('name') == name;
            });
            this.$el.text(member && member.get('id') || 'not found');
        }
    });
});
