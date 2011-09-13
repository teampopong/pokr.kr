var MAX_NUM_CHOSEN = 2;

module.load = function (path) {
	module.display('frame.html').then(function () {
		// FIXME: remove duplicated data loading
		module.loadJSON('members', 'members.json', false).then(function () {
			var parties = _.groupBy(module.members, function (member) {
				return member.party;
			});

			module.template('list.html').then(
					function (template) {
						var context = { parties: parties };
						$('#member-select').html(template(context));

						module.loadJS('chosen.jquery.js', function () {
							$('.chzn-select').chosen();
							$('.chzn-select').change(onMemberChange);
						});
					},
					function (error) {
						alert('error loading list');
					}
					);
		});

		module.loadCSS('chosen.css');
		module.loadCSS('style.css');
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
		var newmembers = $(this).val();
		// FIXME: it should work just with _.difference()
		// however, since it doesn't, this ugly workaround is applied.
		var diff = difference(newmembers, members);
		members.push(diff);

		while (members.length > MAX_NUM_CHOSEN) {
			members.shift();
		}

		// update selectbox
		$(this).val(members);
		$('.chzn-select').trigger('liszt:updated');
	};
})();
