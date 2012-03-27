define([
    'text!./member.tmpl.html',
    'text!./collage.tmpl.html',
    'text!./member.notfound.tmpl.html',
    'lib/js/bootstrap-tooltip'
    ], function (
        memberTmpl,
        collageTmpl,
        notFoundTmpl
    ) {

    var COLLAGE_SIZE = 30;

    function pickRandItems(list, num) {
        var size = Math.min(list.length, num);
        return _.shuffle(list).slice(0, size);
    }

    return Backbone.View.extend({

        template: _.template(memberTmpl),
        collageTemplate: _.template(collageTmpl),
        notFoundTemplate: _.template(notFoundTmpl),

        clearTooltips: function () {
            $('.tooltip').remove();
        },

        render: function () {
            var template = this.model ? this.template : this.notFoundTemplate,
                html = template({
                    q: this.q,
                    member: this.model && this.model.toJSON() || null
                });

            this.$el.html(html);
            this.registerTooltip();
            this.clearTooltips();

            return this.$el;
        },

        renderCollage: function () {
            var collageItems = pickRandItems(this.collection.toJSON(), COLLAGE_SIZE),
                html = this.collageTemplate({
                    items: collageItems
                });

            this.$el.html(html);
            this.registerCollageEvent();
            this.clearTooltips();

            this.$el.show();
        },

        registerCollageEvent: function () {
            var that = this;

            $('.collage-img', this.el)
                .tooltip()
                .click(function () {
                    var $this = $(this),
                        name = $this.attr('data-title');
                    that.search(name);
                });
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

