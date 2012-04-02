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

    var COLLAGE_SIZE = 30,
        REPLACE_INTERVAL = 3 * 1000, // 3 secs
        replaceTimer;

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
            this.clearTooltips();

            return this.$el;
        },

        renderCollage: function () {
            var collageItems = pickRandItems(this.collection.toJSON(), COLLAGE_SIZE),
                html = this.collageTemplate({
                    items: collageItems
                });

            this.$el.html(html);
            this.registerCollageEvents();
            this.clearTooltips();

            if (replaceTimer) clearTimeout(replaceTimer);
            replaceTimer = setTimeout(_.bind(this.replaceRandom, this), REPLACE_INTERVAL);

            this.$el.show();
        },

        registerCollageEvents: function () {
            var that = this;

            $('.collage-img', this.el)
                .css('visibility', 'hidden')
                .tooltip()
                .click(function () {
                    var $this = $(this),
                        name = $this.attr('data-title');
                    that.query(name);
                })
                .each(function (i, elem) {
                    var $elem = $(elem),
                        delay = POPONG.Utils.randInt(1, 30) * 100; // 0.1 ~ 3 secs

                    _.delay(function () {
                        $elem.stop(true, true)
                            .css('visibility', 'visible').hide().fadeIn();
                    }, delay);
                });
        },

        query: function (name) {
            POPONG.router.navigate('!/member/' + name, { trigger: true });
        },

        search: function (name) {
            this.q = name;
            this.model = this.collection.find(function (member) {
                    // TODO: n-gram w/ misspell tolerance
                    return member.get('name') == name;
                });
            this.render().show();
        },

        replaceRandom: function () {
            // FIXME: 퍼포먼스 개선의 여지 많음 -_-;
            var oldItemIndex = POPONG.Utils.randInt(0, COLLAGE_SIZE-1),
                $elem = $('.collage-img:eq('+oldItemIndex+')'),
                collectionSize = this.collection.length,
                newItemIndex = POPONG.Utils.randInt(0, collectionSize-1),
                newItem = this.collection.toJSON()[newItemIndex];

            if (!$elem.size()) return;

            $elem.stop(true, true).fadeOut(400, function () {
                $elem.attr({
                    src: newItem.image ? newItem.image : 'images/default_profile.jpg',
                    'data-title': newItem.name
                });
                $elem.stop(true, true)
                    .css('visibility', 'visible').hide().fadeIn();
            });

            if (replaceTimer) clearTimeout(replaceTimer);
            replaceTimer = setTimeout(_.bind(this.replaceRandom, this), REPLACE_INTERVAL);
        }
    });
});

