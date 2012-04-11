(function (global) { // prevent global scope

define([
    'require',

    // Templates
    'text!./main.tmpl.html',

    // Data
    'json!data/member-profile.json',

    // MVC Components
    'userlib/base.view',
    './collage.view',
    './member.view',
    './member.collection',
    './search.view',

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
        MemberCollection,
        SearchView
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

        show: function (path) {
            var name = path.substr(1); // strip '/'

            BaseView.prototype.show.apply(this, arguments);

            this.createMemberView();
            this.createSearchView();
            this.createCollageView();

            this.initInput(name);
            $('.tooltip').remove();

            if (name) {
                this.collageView.hide();
                this.searchView.search(name);
            } else {
                this.searchView.hide();
                this.collageView.show();
            }
        },

        hide: function () {
            this.searchView.hide();
            this.collageView.hide();

            BaseView.prototype.hide.apply(this, arguments);
        },

        query: function (name) {
            POPONG.router.navigate('!/member/' + name, { trigger: true });
        },

        initInput: function (name) {
            $('input[name="q"]', this.el).val(name);
        },

        createMemberView: function () {
            if (!_.isUndefined(this.memberView)) return;

            this.memberView = new MemberView({
                el: document.getElementById('member-result'),
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

        initSearchForm: function () {
            var that = this;

            $('#member-search-form', this.el).submit(function () {
                var $input = $('input[name="q"]', this.el),
                    name = $input.val();

                that.query(name);

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
