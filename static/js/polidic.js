(function () {


/* POPONG common library */

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


/* Warm-up scripts */

$(document).ready(onReady);
$(window).load(onLoad);

function onReady() {
    $('input#search').typeahead({
        name: 'people_names',
        prefetch: "{{url_for('person_all_names')}}"
    });
}

function onLoad() {
    $('.member-img').clipImage();
    $('.tooltipped').tooltip();
};

}());
