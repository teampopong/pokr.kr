require([
    'text!settings.json',
    'userlib/router',
    'userlib/menu.view'
    ], function (
        Settings,
        Router,
        MenuView
    ) {

    window.App = {
        Settings: JSON.parse(Settings),
        Router: Router,

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
