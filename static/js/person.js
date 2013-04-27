(function () {

$(function () {
    // FIXME: .tab-aggregated should be #id
    // but bootstrap seems not to support that
    $('.tab-aggregated').click(function () {
        $('#member-view .tab-pane').addClass('active');
        $('#member-view .nav-tabs li').removeClass('active');
        $(this).parent('li').addClass('active');
        return false;
    });
});

}());
