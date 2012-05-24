define([
    './hangul.utils.js',
    './html.utils.js',
    './misc.utils.js'
    ], function (
        HangulUtils,
        HtmlUtils,
        MiscUtils
    ) {

    return _.extend({},
            HangulUtils,
            HtmlUtils,
            MiscUtils
        );

});
