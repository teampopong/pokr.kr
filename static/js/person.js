$(function () {
    $(document).on('click', 'a.post-request', function(e) {
        e.preventDefault();
        if (!$('form#post-request').size()) {
            $('<form></form>')
                .attr('id', 'post-request')
                .attr('style', 'display: none;')
                .attr('method', 'POST')
                .insertAfter($(this));
        }
        $('form#post-request')
            .attr('action', $(this).attr('href'))
            .submit();
    });
});

