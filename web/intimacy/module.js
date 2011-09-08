module.load = function (path) {
	module.display('frame.html').then(function () {
		module.loadCSS('chosen.css');
		module.loadJS('chosen.jquery.js', function () {
					$('.chzn-select').chosen();
				});
	});
};
