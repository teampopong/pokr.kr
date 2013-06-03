(function () {

var $specContainer = $('#spec-container');

if (!isMobile) {
    $('.section-tabs a').click(function () {
        var href = $(this).attr('href');
        gotoTab(href);
        return false;
    });

    $specContainer.scrollspy({
            'data-spy': 'scroll',
            'data-target': '.section-tabs',
            'offset': 100
        })
        .on('activate.changehash', function () {
            var target = $('.section-tabs li.active a').attr('href');
            selectTab(target);
        });

    function gotoTab(target) {
        selectTab(target);

        var $elem = $(target);

        $specContainer.animate({
            scrollTop: $specContainer.scrollTop() + $elem.position().top
        }, 300);
    }

    function selectTab(target) {
        var $list = $('.section-tabs li');
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
}

}());
