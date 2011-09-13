var MAX_NUM_CHOSEN = 2;
var selected = [];

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
		// TODO: 각 정당에 대해 의원을 이름순으로 정렬
		context.parties = parties;

		return module.template('select.html');
	});
	defer = defer.pipe(function (template) {
		$('#member-select').html(template(context));
		return module.template('list.html');
	});
	defer.then(function (template) {
		$('#member-list').html(template(context));

		module.loadJS('chosen.jquery.js', function () {
			$('.chzn-select').chosen();
			$('.chzn-select').change(onSearchboxChanged);
		});
	}, function (error) {
		alert(error);
	});
};

var insertSelected = module.insertSelected = function (member) {
	// TODO: check if the given member is already selected.
	if (selected.length === MAX_NUM_CHOSEN) return;
	selected.push(member);

	// limit the # of selected members
	if (selected.length === MAX_NUM_CHOSEN) {
		$('.chzn-select option')
				.not(function (i) {
					return selected.indexOf($(this).val()) > -1;
				}).attr('disabled', 'disabled');
	}

	updateSelected();
}

var removeSelected = module.removeSelected = function (member) {
	// TODO: check if the given member is not selected.
	var idx = selected.indexOf(member);
	if (idx === -1) return;
	selected.splice(idx, 1);

	// can select more members
	$('.chzn-select option').attr('disabled', null);

	updateSelected();
}

function updateSelected() {
	$('#member-list li.member.selected').removeClass('selected');
	for (var i in selected) {
		var member = selected[i];
		$('#member-list li.member#member_'+member).addClass('selected');
	}

	$('.chzn-select').val(selected);
	$('.chzn-select').trigger('liszt:updated');
}

function difference(seta, setb) {
	// FIXME: _.difference() should work for this purpose.
	// however, since it doesn't, this ugly workaround is applied.
	var seta = _.map(seta, function (x) { return escape(x); });
	var setb = _.map(setb, function (x) { return escape(x); });
	return unescape(_.difference(seta, setb)[0]);
}

function onSearchboxChanged() {
	var newselected = $(this).val() || [];

	// insert operation
	if (selected.length < newselected.length) {
		var diff = difference(newselected, selected);
		insertSelected(diff);

	// delete operation
	} else {
		var diff = difference(selected, newselected);
		removeSelected(diff);
	}

}
