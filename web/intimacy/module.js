var MAX_NUM_CHOSEN = module.MAX_NUM_CHOSEN = 2;
var selected = [];
var template_member_info;

module.load = function (path) {
	var context = {};
	selected = [];

	// TODO: 각 프로세스에 주석 달기
	var defer = module.display('frame.html');
	defer = defer.pipe(function () { 
		module.loadCSS('chosen.css');
		module.loadCSS('style.css');

		return module.loadJSON('members', 'members.json', false); 
	});
	defer = defer.pipe(function () {
		module.members = _.sortBy(module.members, function (member) {
			return member.name_kr;
		});
		var parties = _.groupBy(module.members, function (member) {
			return member.party;
		});
		// TODO: 각 정당에 대해 의원을 이름순으로 정렬
		context.parties = parties;

		return module.template('select.html');
	});
	defer = defer.pipe(function (template) {
		$('#member-select').html(template(context));
		return module.template('member_info.html');
	});
	defer = defer.pipe(function (template) {
		template_member_info = template;
		return module.template('list.html');
	});
	defer.then(function (template) {
		$('#member-navi').html(template(context));

		module.loadJS('chosen.jquery.js', function () {
			$('.chzn-select').chosen();
			$('.chzn-select').change(onSearchboxChanged);

			displaySelected(path);
		});
	}, function (error) {
		alert(error);
	});
};

var displaySelected = module.reload = function (path) {
	var newselected = path ? path.split(/-/g) : [];

	// insert operation
	if (selected.length < newselected.length) {
		var diffset = difference(newselected, selected);
		$.each(diffset, function (i, diff) {
			insertSelected(diff);
		});

	// delete operation
	} else {
		var diffset = difference(selected, newselected);
		$.each(diffset, function (i, diff) {
			removeSelected(diff);
		});
	}

	markSelected();
};

function markSelected() {
	$('#member-list li.member.selected').removeClass('selected');
	for (var i in selected) {
		var member = selected[i];
		$('#member-list li.member#member_'+member).addClass('selected');
	}

	$('.chzn-select').val(selected);
	$('.chzn-select').trigger('liszt:updated');
}

function insertSelected(member_name) {
	selected.push(member_name);

	var member = getMemberData(member_name);
	$('#col2').append($(template_member_info(member)));

	if (selected.length === MAX_NUM_CHOSEN) {
		disableChosen();
	}
}

function getMemberData(member_name) {
	return _.detect(module.members, function (member) {
				return member.name_kr == member_name;
			});
}

function removeSelected(member_name) {
	selected = _.without(selected, member_name);

	$('#col2 #member_info_'+member_name).remove();

	enableChosen();
}

function enableChosen() {
	$('.chzn-select option').attr('disabled', null);
}

function disableChosen() {
	$('.chzn-select option')
			.not(function (i) {
				return _.include(selected, $(this).val());
			}).attr('disabled', 'disabled');
}

var updateSelected = module.updateSelected = function (newselected) {
	parent.location.hash = '#!/intimacy/'+newselected.join('-');
};

function difference(seta, setb) {
	// FIXME: _.difference() should work for this purpose.
	// however, since it doesn't, this ugly workaround is applied.
	var seta = _.map(seta, escape);
	var setb = _.map(setb, escape);
	var diffset = _.difference(seta, setb);
	return _.map(diffset, unescape);
}

function onSearchboxChanged() {
	var newselected = $(this).val() || [];
	if (newselected.length <= MAX_NUM_CHOSEN) {
		updateSelected(newselected);
	}
}
