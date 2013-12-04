(function () {

// event triggers
if (!isMobile) {
    $('a.person-link').live('click.linkPerson', function (e) {
        var $this = $(this);

        // Preserve hashtag if the current page is of a person
        if (window.currentPage == 'person' && location.hash) {
            location.href = $this.attr('href') + location.hash;
            return false;
        }
    });
}

/* Warm-up scripts */
$(window).load(onLoad);

function onLoad() {
    $('.person-img').clipImage();
    if (!isMobile) {
        $('.tooltipped:not(.tooltipped-delay)').tooltip();
        $('.tooltipped-delay').tooltip({
            delay: {
                show: 3000,
                hide: 0
            }
        });
    }

    $('h1[id], h2[id], h3[id], h4[id], h5[id], h6[id], .anchor').each(function () {
        var $this = $(this),
            target = $this.data('target-id') || $this.attr('id');
        $('<a class="permalink" href="#'+target+'"><i class="icon-link"></i></a>').appendTo($this);
    });
};

$(function () {
    $('.btn-more-ajax').click(function (e) {
        e.preventDefault();
        var $this = $(this),
            href = $this.attr('href'),
            target = $this.attr('target'),
            method = $this.attr('method') || 'POST';
        $.ajax(href, {
            type: method,
            cache: false,
            dataType: 'json'
        })
        .done(function (data, textStatus) {
            try {
                $(data.html).appendTo($(target));
            } catch (e) {
                errLog('Failed to render.\n' + e);
            }

            if (typeof data.next !== 'undefined') {
                $this.attr('href', data.next);
            } else {
                $this.addClass('hide');
            }
        })
        .fail(function (jqxhr, textStatus, error) {
            errLog('Request failed\n' + error);
        });
    });
});

$(function () {
    $(document).on('click', 'a.request', function(e) {
        e.preventDefault();
        var $this = $(this);
        var data = $this.data();
        $.ajax($this.attr('href'), {
            type: data.method,
            data: data
        }).done(function () {
            window.location.reload();
        }).fail(function () {
            errLog(arguments);
        });
    });
});

function errLog(message) {
    if (isDebug) {
        alert(message);
    } else {
        console.error(message);
    }
}

}());
