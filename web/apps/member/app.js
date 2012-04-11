(function (global) { // prevent global scope

define([
    'require',

    // Templates
    'text!./template/main.tmpl.html',

    // Data
    'json!data/member-profile.json',

    // MVC Components
    'userlib/base.view',
    './view/collage.view',
    './view/member.view',
    './view/search.view',
    './collection/member.collection',

    // Anonymous libraries
    'lib/js/bootstrap-typeahead'
    ], function (
        require,

        // Templates
        mainTmpl,

        // Data
        members,

        // MVC Components
        BaseView,
        CollageView,
        MemberView,
        SearchView,
        MemberCollection
    ) {

    POPONG.Utils.loadCss(require.toUrl('./member.css'));

    var memberCollection = new MemberCollection(members);

    return BaseView.extend({

        template: _.template(mainTmpl),

        context: {},

        render: function () {
            BaseView.prototype.render.apply(this, arguments);
            this.initSearchForm();
            this.initTypeahead();
            return this.$el;
        },

        show: function (params) {
            BaseView.prototype.show.apply(this, arguments);

            this.createViews();
            this.clear();
            this.route(params);
        },

        hide: function () {
            this.searchView.hide();
            this.collageView.hide();

            BaseView.prototype.hide.apply(this, arguments);
        },

        initInput: function (name) {
            $('input[name="q"]', this.el).val(name);
        },

        createViews: function () {
            this.createMemberView();
            this.createSearchView();
            this.createCollageView();
        },

        createMemberView: function () {
            if (!_.isUndefined(this.memberView)) return;

            this.memberView = new MemberView({
                el: document.getElementById('member-result'),
                collection: memberCollection,
                app: this
            });
        },

        createSearchView: function () {
            if (!_.isUndefined(this.searchView)) return;

            this.searchView = new SearchView({
                el: document.getElementById('member-result'),
                collection: memberCollection,
                app: this
            });
        },

        createCollageView: function () {
            if (!_.isUndefined(this.collageView)) return;

            this.collageView = new CollageView({
                el: document.getElementById('member-collage'),
                collection: memberCollection,
                app: this
            });
        },

        clear: function () {
            this.initInput(''); // FIXME
            $('.tooltip').remove();
        },

        route: function (params) {
            var inst = params[0] || '';

            switch (inst) {
            case 'q':
                var name = params[1] || '';

                this.collageView.hide();
                this.searchView.search(name);
                break;

            case 'id':
                var id = params[1] || '';

                this.collageView.hide();
                this.memberView.show(id);
                break;

            default:
                this.searchView.hide();
                this.collageView.show();
                break;
            }
        },

        initSearchForm: function () {
            var that = this;

            $('#member-search-form', this.el).submit(function () {
                var $input = $('input[name="q"]', this.el),
                    name = $input.val();

                POPONG.router.navigate('!/member/q/' + name, { trigger: true });

                return false;
            });
        },

        initTypeahead: function () {
            var names = _.map(members, function (member) { return member.name; }),
                that = this;

            $('input[name="q"]', this.el).typeahead({
                source: names,
                matcher: function (item) {
                    return that.nameMatcher(item, this.query);
                }
            });
        },

        nameMatcher: function (name, query) {
            var chosungs = POPONG.Utils.toChosungs(name),
                nameJamos = POPONG.Utils.toJamos(name),
                queryJamos = POPONG.Utils.toJamos(query);

            // TODO: n-gram w/ misspell tolerance
            return name.indexOf(query) === 0
                || chosungs.indexOf(query) === 0
                || nameJamos.indexOf(queryJamos) === 0;
        }
    });
});

}(window));
