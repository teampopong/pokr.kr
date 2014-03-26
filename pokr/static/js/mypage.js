(function () {
// TODO: refactoring

$(function () {

    $('#form-add-favorite-keyword').submit(function () {
        var $this = $(this),
            keyword = $('input[name="keyword"]', this).val();
            $.post($(this).attr('action') + keyword).done(function () {
                window.location.reload();
            }).fail(function () {
                errLog(arguments);
            });
        return false;
    });

    $('#btn-change-region').click(function () {
        $('#form-search-region').show();
    });
    $('.btn-show-pledge-description').click(function () {
        var id = $(this).data('pledge_description_id');
        $('#' + id).toggleClass('hide');
        return false;
    });
    $('#form-search-region button[type="submit"]').click(searchRegion);

});

function searchRegion() {
    var $formSearchRegion = $('#form-search-region'),
        $findRegionList = $('#find-region-list'),
        urlSearchRegion = $formSearchRegion.attr('action');
    var query = $('[name="query"]', $formSearchRegion).val();
    $.get(urlSearchRegion, {
        query: query
    }).done(function (html) {
        $findRegionList.html(html);
        $('.choose-region', $findRegionList).click(function () {
            updateRegion($(this).data('region_id'));
            $formSearchRegion.hide();
            $findRegionList.empty();
        });
    }).fail(function () {
        errLog(arguments);
    });
    return false;
}

function updateRegion(region_id) {
    var urlUpdateRegion = $('#urlUpdateRegion').attr('action');
    $.ajax(urlUpdateRegion, {
        data: {
            region_id: region_id
        },
        type: 'PUT'
    }).done(function () {
        window.location.reload();
    }).fail(function () {
        errLog(arguments);
    });
}

}());

