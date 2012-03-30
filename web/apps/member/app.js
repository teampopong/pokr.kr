(function (global) { // prevent global scope

define([
    'require',

    // Templates
    'text!./main.tmpl.html',

    // Data
    'json!data/member-profile.json',

    // MVC Components
    'userlib/base.view',
    './member.view',
    './member.collection',

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
        MemberView,
        MemberCollection
    ) {

    POPONG.Utils.loadCss(require.toUrl('./member.css'));

    return BaseView.extend({

        template: _.template(mainTmpl),

        context: {},

        render: function () {
            BaseView.prototype.render.apply(this, arguments);
            this.registerEvents();
            this.registerTypeahead();
            return this.$el;
        },

        show: function (path) {
            BaseView.prototype.show.apply(this, arguments);
            this.clearInput();
            this.createMemberView();
            this.memberView.renderCollage();
        },

        clearInput: function () {
            $('input[name="q"]', this.el).val('');
        },

        createMemberView: function () {
            if (this.memberView) return;

            var memberCollection = new MemberCollection(members);
            this.memberView = new MemberView({
                el: document.getElementById('member-result'),
                collection: memberCollection
            });
        },

        registerEvents: function () {
            var that = this;

            $('#member-search-form', this.el).submit(function () {
                var $input = $('input[name="q"]', this.el),
                    name = $input.val();

                that.memberView.search(name);

                return false;
            });
        },

        registerTypeahead: function () {
            var names = _.map(members, function (member) { return member.name; });

            $('input[name="q"]', this.el).typeahead({
                source: names,
                matcher: function (item) {
                    return item.indexOf(this.query) != -1;
                }
            });
        }
    });
});

}(window));
