require([
    'json!settings.json',
    'userlib/utils',
    'userlib/router',
    'userlib/menu.view'
    ], function (
        Settings,
        Utils,
        Router,
        MenuView
    ) {

    window.App = {
        Settings: Settings,
        Router: Router,
        Utils: Utils,

        views: [],

        start: function () {
            this.menuView = new MenuView(this.Settings.apps);
            this.router = new Router({
                apps: this.Settings.apps,
                menuView: this.menuView
            });
        }
    };

    $(function () {
        App.start();
    });

});
