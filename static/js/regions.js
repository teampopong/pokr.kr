(function () {
$('.map .region').click(function () {
    var id = $(this).data('region_id'),
        region_name = $('.region-'+id).data('text');
    $('.region-link').removeClass('show');
    $('.region-link.region-sub-'+id).addClass('show');
    $('#province').text(region_name);
});

$(window).load(function () {
    $('.map path[data-region_id="11"]').click();
});
}());
