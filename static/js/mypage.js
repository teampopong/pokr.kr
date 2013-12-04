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
});

