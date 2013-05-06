(function () {

$('#person-section-tabs a').click(function () {
    var href = $(this).attr('href');
    gotoTab(href);
    return false;
});

$(window).load(function () {
    $('#spec-container').scrollspy();
});

$('#spec-container').scroll(function () {
    $('#spec-container').scrollspy('refresh');
});

function gotoTab(target) {
    var $elem = $(target);
    location.hash = target;
    selectTab(target);
    $('#spec-container').animate({
        scrollTop: $elem.position().top
    }, 300);
}

function selectTab(target) {
    var $list = $('#person-section-tabs li');
    $list.removeClass('active');
    $list.children('[href="'+target+'"]').parent('li').addClass('active');
}

}());
