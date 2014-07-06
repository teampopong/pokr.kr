(function () {

$('.map.clickable .region').off('click.map');
$('.map.clickable .region').on('click.map', function () {
    var id = $(this).data('region_id'),
        url = Mustache.render(tmpl_region_url, { region_id: id });
    location.href = url;
});

$('.map').each(function () {
    var $this = $(this),
        region_id = $this.data('default_region_id');
    if (region_id) {
        $this.find('text').css('display', 'none');
        selectRegion($this, region_id);
        $this.data('default_region_id', null);
    }
});

function selectRegion($map, region_id) {
    $map.find('.region').removeClass('selected');
    $map.find('.region[data-region_id="'+region_id+'"]').addSvgClass('selected');
    $map.find('text[data-region_id="'+region_id+'"]').css('display', 'block');
}

}());
