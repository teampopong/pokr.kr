define([
    './member.model'
    ], function (
        MemberModel
    ) {

    return Backbone.Collection.extend({
        model: MemberModel,
    });
});
