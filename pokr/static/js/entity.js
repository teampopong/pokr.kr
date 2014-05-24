(function () {

$(function () {
    var $body= $('body');

    if (!isMobile) {
        $('a.animated').click(function () {
            var href = $(this).attr('href');
            gotoTab(href);
            return false;
        });

        function gotoTab(target) {
            selectTab(target);

            var $elem = $(target);

            $body.stop().animate({
                scrollTop: $elem.position().top
            }, 700, 'easeInOutQuart');
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
});

}());
