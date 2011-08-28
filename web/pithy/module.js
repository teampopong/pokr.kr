var SUMMARIZE_LENGTH = 16;
// FIXME: this is because PHP is not supported on the local webserver
var URL_GET_MEMBERS = 'http://localhost/~cornchz/popong/web/pithy/get_members.php';

module.load = function (path) {
	// detect at which tab the user is
	var splitted = path && path.split('/') || ['abc'];
	var sectionTab = splitted[0];
	var query = splitted[1] || '';

	// load page
	module.display('frame.html').then(function () { 
		// load member list
		module.loadJSON('members', URL_GET_MEMBERS, false).then(function () {

			// fill the page
			updateList(sectionTab, query);
		});

		// they're on the bottom because the above is executed asynchronously
		module.loadCSS('style.css');
		initEvents(sectionTab, query);
	});
};

function updateList(sectionTab, query) {
	// filter if a query exists
	if (query) {
		var members = _.select(module.members, function (member) {
			return member.name_kr.contains(query) ||
					member.party.contains(query) ||
					member.district.contains(query) ||
					member.committee.contains(query);
		});
	} else {
		var members = module.members;
	}

	// summarize if a committee field is too long
	// TODO: do this just once
	_.each(members, function (member) {
		member.committee = member.committee.summarize(SUMMARIZE_LENGTH);
	});

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

	return function (members, sectionTab) {
		// TODO: search
		var sections = _.groupBy(members, getSection[sectionTab]);
		var sections = sortObject(sections);
		return sections;
	};
})();
