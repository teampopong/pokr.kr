define([
    'text!./collage.tmpl.html',
    'lib/js/bootstrap-tooltip'
    ], function (
        collageTmpl
    ) {

    var COLLAGE_SIZE = 30,
        REPLACE_INTERVAL = 3 * 1000, // 3 secs
        replaceTimer;

    function pickRandItems(list, num) {
        var size = Math.min(list.length, num);
        return _.shuffle(list).slice(0, size);
    }

    return Backbone.View.extend({

        template: _.template(collageTmpl),

        isRendered: false,

        initialize: function (options) {
            this.app = options.app;
            this.numImgs = this.collection.length;
        },

        show: function () {
            this.render().show();
        },

        hide: function () {
            if (replaceTimer) clearTimeout(replaceTimer);
            this.$el.hide();
        },

        render: function () {
            var collageItems = pickRandItems(this.collection.toJSON(), COLLAGE_SIZE),
                html = this.template({
                    items: collageItems
                });

            this.$el.html(html);
            this.cacheImageElems();
            this.registerCollageEvents();

            if (replaceTimer) clearTimeout(replaceTimer);
            replaceTimer = setTimeout(_.bind(this.replaceRandom, this), REPLACE_INTERVAL);

            return this.$el;
        },

        cacheImageElems: function () {
            this.$imgs = $('.collage-img', this.el);
            this.cacheNumVisibleImage();

            // invalidate on resize (rarely happens)
            $(window).resize(_.bind(this.cacheNumVisibleImage, this));
        },

        cacheNumVisibleImage: function () {
            this.numVisibleImgs = this.$imgs.filter(function () {
                var $elem = $(this),
                    offsetY = $elem.offset().top - $elem.parent().offset().top;

                return offsetY <= $elem.parent().height()-0.1;
            }).size();
        },

        registerCollageEvents: function () {
            var that = this;

            this.$imgs
                .css('visibility', 'hidden')
                .tooltip()
                .click(function () {
                    var $this = $(this),
                        name = $this.attr('data-title');
                    that.app.query(name);
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

        replaceRandom: function () {
            var oldItemIndex = POPONG.Utils.randInt(0, this.numVisibleImgs - 1),
                $elem = this.$imgs.eq(oldItemIndex),
                newItemIndex = POPONG.Utils.randInt(0, this.numImgs - 1),
                newItem = this.collection.toJSON()[newItemIndex];

            if (!$elem.size()) return;

            $elem.stop(true, true).fadeOut(400, function () {
                $elem.attr({
                    src: newItem.image ? newItem.image : 'images/default_profile.jpg',
                    'data-title': newItem.name,
                    title: newItem.name
                });
                $elem.data('tooltip').fixTitle();
                $elem.stop(true, true)
                    .css('visibility', 'visible').hide().fadeIn();
            });

            if (replaceTimer) clearTimeout(replaceTimer);
            replaceTimer = setTimeout(_.bind(this.replaceRandom, this), REPLACE_INTERVAL);
        }
    });
});
