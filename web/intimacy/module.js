var MAX_NUM_CHOSEN = 2;

module.load = function (path) {
	var context = {};

	var defer = module.display('frame.html');
	defer = defer.pipe(function () { 
		module.loadCSS('chosen.css');
		module.loadCSS('style.css');

		return module.loadJSON('members', 'members.json', false); 
	});
	defer = defer.pipe(function () {
		var parties = _.groupBy(module.members, function (member) {
			return member.party;
		});
		context.parties = parties;

		return module.template('list.html');
	});
	defer.then(function (template) {
		$('#member-select').html(template(context));

		module.loadJS('chosen.jquery.js', function () {
			$('.chzn-select').chosen();
			$('.chzn-select').change(onMemberChange);
		});
	}, function (error) {
		alert(error);
	});
};

var onMemberChange = (function () {
	var members = [];

	function difference(seta, setb) {
		var seta = _.map(seta, function (x) { return escape(x); });
		var setb = _.map(setb, function (x) { return escape(x); });
		return unescape(_.difference(seta, setb)[0]);
	}

	return function () {
		var newmembers = $(this).val() || [];

		// insert operation
		if (members.length < newmembers.length) {
			// FIXME: it should work just with _.difference()
			// however, since it doesn't, this ugly workaround is applied.
			var diff = difference(newmembers, members);
			members.push(diff);

			// limit the # of selected members
			if (members.length === MAX_NUM_CHOSEN) {
				$('.chzn-select option')
						.not(function (i) {
							return members.indexOf($(this).val()) > -1;
						}).attr('disabled', 'disabled');
			}

		// delete operation
		} else {
			members = newmembers;

			// can select more members
			$('.chzn-select option').attr('disabled', null);
		}

		// update selectbox
		$(this).val(members);
		$('.chzn-select').trigger('liszt:updated');
	};
})();
