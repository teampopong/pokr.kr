define(function () {
    return Backbone.View.extend({

        tagName: 'div',
        className: 'page',

        context: {},

        render: function () {
            if (this.template) {
                var html = this.template(this.context);
                this.$el.html(html);
            }
            return this.$el;
        },

        show: function () {
            this.render()
                .appendTo('#content')
                .show();
        }
    });
});
