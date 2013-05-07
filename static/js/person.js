(function () {

$('#person-section-tabs a').click(function () {
    var href = $(this).attr('href');
    gotoTab(href);
    return false;
});

$('#spec-container').scrollspy({
        'data-spy': 'scroll',
        'data-target': '#person-section-tabs',
        'offset': 100
    })
    .on('activate.changehash', function () {
        var target = $('#person-section-tabs li.active a').attr('href');
        selectTab(target);
    });

function gotoTab(target) {
    selectTab(target);

    var $elem = $(target);
    $('#spec-container').animate({
        scrollTop: $elem.position().top
    }, 300);
}

function selectTab(target) {
    var $list = $('#person-section-tabs li');
    $list.removeClass('active');
    $list.children('[href="'+target+'"]').parent('li').addClass('active');

    if (location.hash != target) {
        if (history.pushState) {
            history.pushState({}, null, target);
        } else {
            location.hash = target;
        }
    }
}

}());
