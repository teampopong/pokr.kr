(function (global) { // prevent global scope

define([
    'require',

    // Templates
    'text!./intimacy.tmpl.html',
    'text!./list.tmpl.html',
    'text!./member.tmpl.html',

    // Data
    'json!data/members.json', // 나중엔 server에서 받기
    'json!data/similarity_top10.json',

    // MVC Components
    'userlib/base.view',
    ], function (
        require,

        // Templates
        intimacyTmpl, // TODO: template plugin 만들자
        listTmpl,
        memberTmpl,

        // Data
        members,
        similarities,

        // MVC Components
        BaseView
    ) {

    // TODO: namespace 충돌이 나지 않도록, css 잘 짜기
    // TODO: Bootstrap을 최대한 이용하도록 css 수정
    POPONG.Utils.loadCss(require.toUrl('./intimacy.css'));

    (function processData() {
        // put similarity data
        _.each(members, function (member) {
            member.similars = similarities[member.name_kr];
        });

        // sort by name_kr
        members = _.sortBy(members, function (member) {
            return member.name_kr;
        });

        // group by parties
        parties = _.groupBy(members, function (member) {
            return member.party;
        });
    }());

    return BaseView.extend({

        template: _.template(intimacyTmpl),
        listTemplate: _.template(listTmpl),
        memberTemplate: _.template(memberTmpl),

        context: {
            parties: parties
        },

        show: function () {
            BaseView.prototype.show.apply(this, arguments);
            this.renderList();
        },

        renderList: function () {
            var that = this;

            $('#member-navi').html(this.listTemplate(this.context));
            $('#shortcuts a').unbind('click').click(scrollTo);
            $('#member-list a').unbind('click').click(function () {
                var $this = $(this),
                    name_kr = $this.attr('name_kr');

                $this.parent().find('li.selected').removeClass('selected');
                $this.find('li').addClass('selected');
                that.renderMember(name_kr);
            });
        },

        renderMember: function (name_kr) {
            var member = _.detect(members, function (member) {
                    return member.name_kr == name_kr;
                });
            $('#col2').html(this.memberTemplate(member));
        }
    });
});

function scrollTo() {
    var party = $(this).text(),
        scroll = $('#party_'+party).offset().top
            - $('#member-list ul').offset().top;

    $('#member-list').animate({
            scrollTop: scroll
        }, 300);
}

}(window));
