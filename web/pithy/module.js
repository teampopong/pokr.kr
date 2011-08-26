var SUMMARIZE_LENGTH = 16;
// FIXME: this is because PHP is not supported on the local webserver
var GET_MEMBERS_URL = 'http://localhost/~cornchz/popong/web/pithy/get_members.php';

module.load = function (path) {
	// detect at which tab the user is
	path = path || 'abc';
	var sectionTab = path.split("/")[0];

	// load member data
	module.loadJSON('members', 'http://localhost/~cornchz/popong/web/pithy/get_members.php').then(function () {
		module.members = _.map(module.members, function (member) {
			member.committee = member.committee.summarize(SUMMARIZE_LENGTH);
			return member;
		});
		var context = { sections: getMembersInSections(sectionTab) };

		module.display('frame.html', context).then(function () { 
			module.loadCSS('style.css');
			$('.navitab#{0}'.format(sectionTab)).addClass('activenavitab');
		});
	});
};

var getMembersInSections = (function () {
	var getSection = {
				abc: function abc (member) {
					var sections = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ',
							'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ','ㅊ', 'ㅋ',
							'ㅌ', 'ㅍ', 'ㅎ'];

					var code = member.name_kr[0].charCodeAt();
					var index = parseInt((code - 0xac00) / 21 / 28);
					return sections[index];
				}, 
				district: function district (member) {
					return member.district.split(' ')[0];
				},
				party: function party (member) {
					return member.party;
				},
				committee: function committee (member) {
					return member.committee.split(', ');
				},
				age: function age (member) {
					var sections = ['31-40', '41-50', '51-60',
							'61-70', '71-80', '81-90'];

					var cur_year = parseInt((new Date()).getFullYear());
					var birth_year = parseInt(member.birth.substr(0, 4));
					var age = cur_year - birth_year + 1;
					return sections[parseInt((age+9)/10)-4];
				}
			};

	return function (sectionTab) {
		// TODO: search
		var sections = _.groupBy(module.members, getSection[sectionTab]);
		var sections = sortObject(sections);
		return sections;
	};
})();
