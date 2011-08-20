module.load = function (path) {
	path = path || 'abc';
	section = path.split("/")[0];
	module.display('frame.html').then(function () { 
		module.loadCSS('style.css');
		module.loadJSON('members',
				module.base + '/get_members.php').done(function () {
			//createMemberElements();
			updateList(section);
		});
	});
};

/*
function createMemberElements() {
	// Create HTML element of each member if it doesn't exist
	if (typeof memberElements == 'undefined') {
		memberElements = {};
		for (var i in members) {
			var member = members[i];
			var $member = create$Member(member);
			memberElements[member.id] = $member;
		}
		db.memberElements = memberElements;
	}
}
*/

var updateList = (function () {
	// TOOD: fill it
	var getSection = {
				abc: function abc () {
					var sections = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ',
							'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ','ㅊ', 'ㅋ',
							'ㅌ', 'ㅍ', 'ㅎ'];

					var code = member.name_kr[0].charCodeAt();
					var index = parseInt((code - 0xac00) / 21 / 28);
					return sections[index];
				}, 
				district: function district () {
					return member.district.split(' ')[0];
				},
				party: function party () {
					return member.party;
				},
				committee: function committee () {
					return member.committee.split(', ');
				},
				age: function age () {
					var sections = ['31-40', '41-50', '51-60',
							'61-70', '71-80', '81-90'];

					var cur_year = parseInt((new Date()).getFullYear());
					var birth_year = parseInt(member.birth.substr(0, 4));
					var age = cur_year - birth_year + 1;
					return sections[parseInt((age+9)/10)-4];
				}
			};

	var sections = module.sections || _.groupBy(module.members, getSection[section]);
	if (!module.sections[section]) module.sections[section] = sections;
	view(sections);

})();

function Viewer(getSection) {
	this.sections = getSection.sections;
	this.getSection = getSection;

	this.view = function (query) {
		this.sortMembers();
		this.dispSections();
		var used_sections = this.registerMembers(query);
		this.hideUnusedSections(used_sections);
	};

	this.dispSections = function () {
		var $main = $('div#main');
		$main.children().hide();
		for (var i in this.sections) {
			var section = this.sections[i];
			var sectionId = 'section-{0}'.format(section);
			if ($(sectionId).length) {
				$(sectionId).show();
			} else {
				var mainElement = document.getElementById('main');
				var sectionElement = WM.addHTMLElement('div', {
							attributes: {
								class: 'section',
								id: sectionId
							}
							target: mainElement
						});
				WM.addHTMLElement('div', {
							attributes: {
								class: 'clear',
							}
							target: mainElement
						});
				WM.addHTMLElement('p', {
							attributes: {
								class: 'section_name'
							}
							target: sectionElement
						});
				WM.addHTMLElement('ul', {
							target: sectionElement
						});
			}
		}
	};

	this.registerMembers = function (query) {

		function match(member, query) {
			return member.name_kr.contains(query) ||
					member.party.contains(query) ||
					member.district.contains(query) ||
					member.committee.contains(query);
		};

		var usedSections = new Set();

		for (var i in members) {
			var member = members[i];
			if (!query || match(member, query)) {
				var section = this.getSection(member);
				// TODO: 여기 하던 중이었음 - get$SectionUl이 없음 지금
				var $section_ul = get$SectionUl(section);

				var $member = this.memberElements[member.id];
				$section_ul.append($member);
				usedSections.add(section);
				setSectionUsed(section);
			}
		}

		return usedSections;
	};

	this.hideUnusedSections = function (used_sections) {
		for (var i in this.sections) {
			var section = this.sections[i];
			if (!used_sections[section]) {
				var $section = get$Section(section);
				$section.hide();
			}
		}
	};

	// Sort members lexicographically
	this.sortMembers = function () {
		members.sort(function (a, b) {
			if (a.name_kr < b.name_kr) return -1;
			else if (a.name_kr > b.name_kr) return 1;
			else return 0;
		});
	}

	this.getSection = getSection;

	return this;
}
