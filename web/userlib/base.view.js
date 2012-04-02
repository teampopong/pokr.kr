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
            this.rendered = true;
            return this.$el;
        },

        show: function () {
            if (!this.rendered) {
                this.render()
                    .appendTo('#content');
            }

            this.$el.show();
        },

        hide: function () {
            this.$el.hide();
        }
    });
});
