define(function () {
    var CONSONANTS = [
            'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ',
            'ㅇ', 'ㅈ', 'ㅉ','ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
        ],
        loadedCss = {};

    return {
        getFirstConsonant: function (str, index) {
            index = index || 0;

            var code = str.charCodeAt(index),
                offset = parseInt((code - 0xac00) / 21 / 28);

            return CONSONANTS[offset];
        },

        getFirstConsonants: function (str) {
            var consonants = [];
            for (var i in str) {
                var consonant = this.getFirstConsonant(str, i);
                consonants.push(consonant);
            }
            return consonants.join('');
        },

        randInt: function (min, max) {
            return Math.floor(Math.random() * (max - min + 1)) + min;
        },

        loadCss: function (url) {
            if (loadedCss[url]) return;

            var link = document.createElement("link");
            link.type = "text/css";
            link.rel = "stylesheet";
            link.href = url;
            document.getElementsByTagName("head")[0].appendChild(link);

            loadedCss[url] = true;
        }
    };
});
