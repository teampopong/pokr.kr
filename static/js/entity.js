(function () {

var $body = $('body');

if (!isMobile) {
    $('.section-tabs a').click(function () {
        var href = $(this).attr('href');
        gotoTab(href);
        return false;
    });

    $body.scrollspy({
            'data-spy': 'scroll',
            'data-target': '.section-tabs',
            'offset': 100
        })
        .on('activate.changehash', function () {
            var target = $('.section-tabs li.active a').attr('href');
            selectTab(target);
        });

    setTimeout(function () {
        $('.section-tabs-nav').affix({
            offset: {
                top: 360
            }
        });
    }, 100);

    function gotoTab(target) {
        selectTab(target);

        var $elem = $(target);

        $body.animate({
            scrollTop: $elem.offset().top
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
