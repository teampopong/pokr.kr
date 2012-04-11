define(function () {
    return Router = Backbone.Router.extend({

        initialize: function (options) {
            this.options = options;
            this.appNames = _.pluck(options.apps, 'name');

            Backbone.history.start();

            // 접근한 url에 hashbang이 없는 경우
            if (!location.hash) {
                this.navigate('!/home', { trigger: true });
            }
        },

        routes: {
            '!/:app*path': 'defaultRoute'
        },

        defaultRoute: function (app, path) {
            // TODO: 예쁜데, 좋은 구현은 아님 -_-;
            POPONG.filter(function (_, name) {
                return name != app;
            }).each(function (app) {
                app.hide();
            });

            this.options.menuView.setActive(app);

            // 404 not found
            if (!_.contains(this.appNames, app)) {
                $('#page-not-found').show();
                return;
            }

            var appPath = _.string.sprintf('apps/%s/app', app),
                params = path.substr(1).split('/');

            require([appPath], function (App) {

                if (!POPONG.apps[app]) {
                    POPONG.apps[app] = new App({
                        id: _.string.sprintf('page-%s', app)
                    });
                }

                POPONG.apps[app].show(params);
            });
        }
    });
});
