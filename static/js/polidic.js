(function () {

if (window.PO) {
    return;
}

window.PO = PO = {};

PO.linkPeople = function (elem) {
    $(elem || '.person-link').each(function () {
        $(this).off('click.linkPeople');
        $(this).on('click.linkPeople', function () {
            var isPersonPageNow = location.hash.substr(1, 7) == 'section';
            location.href = $(this).attr('href')
                    + (isPersonPageNow && location.hash || '');
            return false;
        });
    });
};

$(window).load(function () {
    $('.tooltipped').tooltip();
});

}());
