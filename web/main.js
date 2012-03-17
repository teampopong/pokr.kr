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

    window.POPONG = {
        Settings: Settings,
        Router: Router,
        Utils: Utils,

        apps: [],

        start: function () {
            this.menuView = new MenuView(this.Settings.apps);
            this.router = new Router({
                apps: this.Settings.apps,
                menuView: this.menuView
            });
        }
    };

    $(function () {
        POPONG.start();
    });

});
