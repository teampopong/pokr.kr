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
						$('#member-list').html(template(context));
					},
					function (error) {
						alert('error loading list');
					}
					);

			module.loadJS('chosen.jquery.js', function () {
				$('.chzn-select').chosen();
			});
		});

		module.loadCSS('chosen.css');
	});
};
