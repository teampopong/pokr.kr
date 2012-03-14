define(function () {
    var TMPL_TXT = '<li class="menu-item" id="menu-<%=name%>"><a href="#!/<%=name%>"><%=title%></a></li>',
        template = _.template(TMPL_TXT);

    function menu(app) {
        // 대상이 지정된 경우
        if (app) {
            var menuId = _.string.sprintf('#menu-%s', app);
            return $(menuId);

        // 대상이 지정되지 않았으면 전체
        } else {
            return $('.menu-item');
        }
    }

    return Backbone.View.extend({

        el: '#menu',

        initialize: function (apps) {
            this.apps = apps;
            this.render();
        },

        render: function () {
            var $el = this.$el.empty();

            _.each(this.apps, function (app) {
                $(template(app)).appendTo($el);
            });
        },

        setActive: function (app) {
            menu().removeClass('active');
            menu(app).addClass('active');
        }
    });
});
