(function () {

$('#person-section-tabs a').click(function () {
    var href = $(this).attr('href'),
        $elem = $(href);
    selectTab(href);
    $('#spec-container').animate({
        scrollTop: $elem.position().top
    }, 300);
    return false;
});

$(window).load(function () {
    $('#spec-container').scrollspy();
    $('.tooltipped').tooltip();
});

$('#spec-container').scroll(function () {
    $('#spec-container').scrollspy('refresh');
});

function selectTab(target) {
    var $list = $('#person-section-tabs li');
    $list.removeClass('active');
    $list.children('[href="'+target+'"]').parent('li').addClass('active');
}

}());
