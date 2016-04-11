(function () {

/**
 * 이미지들을 크기에 맞게 clip
 * (이미지 비율은 조정하지 않고, 넘치는 부분을 숨김)
 */
$.fn.clipImage = (function() {

    function px(n) {
        return n === 'auto' ? n : parseInt(n, 10) + 'px';
    }

	function setViewport($img, x, y, width, height) {
        $img.css({
            left: px(x),
            top: px(y),
            width: px(width),
            height: px(height),
            'max-width': 'none',
            'max-height': 'none'
        });
	}

	function position($img, vWidth, vHeight) {
        $img.css({
            display: 'block',
            position: 'absolute'
        });
		
		var cImage = new Image();
		cImage.onload = function () {
			var rx = cImage.width / vWidth,
				ry = cImage.height / vHeight;

			if(rx > ry){
				var dx = parseInt((cImage.width/ry - vWidth) / 2);
				setViewport($img, -dx, 0, 'auto', vHeight);
			} else {
				var dy = parseInt((cImage.height/rx - vHeight) / 2);
				setViewport($img, 0, -dy, vWidth, 'auto');
			}
		};
		cImage.src = $img.attr('src');
	}

	return function () {
        return this.each(function () {
            var $img = $(this),
                vWidth = parseInt($img.width(), 10),
                vHeight = parseInt($img.height(), 10);

            $img.removeAttr('width')
                .removeAttr('height');
    
            // clip하기 위한 프레임
            var $viewport = $('<div></div>').css({
                overflow: 'hidden',
                position: 'relative',
                width: vWidth,
                height: vHeight
            });
    
            // 이미지를 $viewport로 감쌈
            $img.before($viewport);
            $viewport.append($img);
    
            // 이미지 크기,위치 조정
            position($img, vWidth, vHeight);
        });
	};
})();

$.fn.addSvgClass = function (className) {
    var $this = $(this),
        oldclass = $this.attr('class'),
        classes = oldclass.split(/\s/g);
    if ($.inArray(className, classes) === -1) {
        $this.attr('class', oldclass + ' ' + className);
    }
};

$.fn.removeSvgClass = function (className) {
    var $this = $(this),
        oldclass = $this.attr('class'),
        classes = oldclass.split(/\s/g),
        idx;
    if ((idx = $.inArray(className, classes)) !== -1) {
        classes.splice(idx, 1);
        $this.attr('class', classes.join(' '));
    }
};

window.getRandomColor = function () {
    // source: http://stackoverflow.com/questions/1484506/random-color-generator-in-javascript
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++ ) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

}());
