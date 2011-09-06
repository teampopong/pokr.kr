var SUMMARIZE_LENGTH = 16;

var is_first = true;

module.load = function (path) {
	// detect at which tab the user is
	var splitted = path && path.split('/') || ['abc'];
	var sectionTab = splitted[0];
	var query = splitted[1] || '';

	// load page
	module.display('frame.html').then(function () { 
		// load member list
		module.loadJSON('members', 'members.json', false).then(function () {

			// Data processing
			// TODO: do this not here, but on crawler
			if (is_first) {
				// summarize if a committee field is too long
				_.each(module.members, function (member) {
					member.committee_summarized = member.committee.summarize(SUMMARIZE_LENGTH);
				});

				parseCommittee();

				is_first = false;
			}

			// fill the page
			updateList(sectionTab, query);
		});

		// they're on the bottom because the above is executed asynchronously
		module.loadCSS('style.css');
		initEvents(sectionTab, query);
	});
};

function updateList(sectionTab, query) {
	// 'committee' tab needs a special treatment
	var members = sectionTab === 'committee' ? module.members_for_committee
			: module.members;

	// filter if a query exists
	if (query) {
		var members = _.select(members, function (member) {
			return member.name_kr.contains(query) ||
					member.party.contains(query) ||
					member.district.contains(query) ||
					member.committee.contains(query);
		});
	}

	// groups member data
	var context = { sections: getMembersInSections(members, sectionTab) };

	// fill list data
	module.template('list.html').then(
			function(template) {
				$('#main').html(template(context));
			},
			function(error) {
				alert('error loading list');
			}
			);
}

function parseCommittee() {
	var members = [];
	for (var i in module.members) {
		var member = module.members[i];
		var committees = member.committee.split(', ');
		for (var j in committees) {
			var _member = _.clone(member);
			_member._committee = committees[j];
			members.push(_member);
		}
	}
	module.members_for_committee = members;
}

function initEvents(sectionTab, query) {

	function getQueryLink(query) {
		return '#!/pithy/{0}/{1}'.format(sectionTab, query);
	}

	function updateQueryLink(query) {
		$('#searchlink').attr('href', getQueryLink(query));
	}

	$('.navitab#{0}'.format(sectionTab)).addClass('activenavitab');
	$('#querytext').val(query);
	updateQueryLink(query);

	$('#querytext').keyup(function (e) {
		var query = $(this).val();

		// 'enter' key
		if (e.keyCode == 13) {
			parent.window.location.href = getQueryLink(query);

		// else
		} else {
			updateQueryLink(query);

		}
	});
}

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
					return member._committee;
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

	return function (members, sectionTab) {
		// TODO: search
		var sections = _.groupBy(members, getSection[sectionTab]);
		var sections = sortObject(sections);
		return sections;
	};
})();
