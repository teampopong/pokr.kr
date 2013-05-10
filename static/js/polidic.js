(function () {

// event triggers
$('a.person-link').live('click.linkPerson', function (e) {
    var $this = $(this);

    // Preserve hashtag if the current page is of a person
    if (window.currentPage == 'person' && location.hash) {
        location.href = $this.attr('href') + location.hash;
        return false;
    }
});

/* Warm-up scripts */
$(window).load(onLoad);

function onLoad() {
    $('.person-img').clipImage();
    $('.tooltipped:not(.tooltipped-delay)').tooltip();
    $('.tooltipped-delay').tooltip({
        delay: {
            show: 1000,
            hide: 0
        }
    });
};

}());
