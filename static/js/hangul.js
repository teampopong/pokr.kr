/*!
 * Hangul Jamo Library v0.1
 * https://github.com/teampopong/hangul-jamo-js
 *
 * Copyright 2013 Team POPONG
 * Released under the MIT license
 * https://github.com/teampopong/hangul-jamo-js/blob/master/LICENSE
 */
(function () {

var global = this;  // either window or global

var // 초성
    FIRST_CONSONANTS = [
        'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ',
        'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
    ],
    // 중성
    VOWELS = [
        'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅗㅏ', 'ㅗㅐ',
        'ㅗㅣ', 'ㅛ', 'ㅜ', 'ㅜㅓ', 'ㅜㅔ', 'ㅜㅣ', 'ㅠ', 'ㅡ', 'ㅡㅣ', 'ㅣ'
    ],
    // 종성
    LAST_CONSONANTS = [
        '', 'ㄱ', 'ㄲ', 'ㄱㅅ', 'ㄴ', 'ㄴㅈ', 'ㄴㅎ', 'ㄷ', 'ㄹ', 'ㄹㄱ',
        'ㄹㅁ', 'ㄹㅂ', 'ㄹㅅ', 'ㄹㅌ', 'ㄹㅍ', 'ㄹㅎ', 'ㅁ', 'ㅂ', 'ㅂㅅ',
        'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
    ],
    // 독립적인 자음
    SINGLE_CONSONANTS = [
        'ㄱ', 'ㄲ', 'ㄱㅅ', 'ㄴ', 'ㄴㅈ', 'ㄴㅎ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㄹㄱ',
        'ㄹㅁ', 'ㄹㅂ', 'ㄹㅅ', 'ㄹㅌ', 'ㄹㅍ', 'ㄹㅎ', 'ㅁ', 'ㅂ', 'ㅃ',
        'ㅂㅅ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
    ];

var HANGUL = global.HANGUL = global.HANGUL || {};

HANGUL.toJamos = function (str) {
    var jamos = [];

    for (var i = 0, len = str.length; i < len; i++) {
        var _char = str[i];

        jamos.push(this.toChosungs(_char));
        jamos.push(this.toJoongsungs(_char));
        jamos.push(this.toJongsungs(_char));
    }
    return jamos.join('');
};

HANGUL.toChosungs = function (str) {
    var consonants = [];

    for (var i = 0, len = str.length; i < len; i++) {
        var code = str.charCodeAt(i),
            offset,
            consonant;

        if (0x3131 <= code && code < 0x314f) {
            offset = parseInt(code - 0x3131);
            consonant = SINGLE_CONSONANTS[offset];
        } else if (0xac00 <= code && code < 0xd7a4) {
            offset = parseInt((code - 0xac00) / 28 / 21);
            consonant = FIRST_CONSONANTS[offset];
        } else {
            consonant = str.charAt(i);
        }

        consonants.push(consonant);
    }

    return consonants.join('');
};

HANGUL.toJoongsungs = function (str) {
    var vowels = [];

    for (var i = 0, len = str.length; i < len; i++) {
        var code = str.charCodeAt(i),
            offset,
            vowel;

        if (0xac00 <= code && code < 0xd7a4) {
            offset = parseInt((code - 0xac00) / 28) % 21;
            vowel = VOWELS[offset];
        } else {
            vowel = '';
        }

        vowels.push(vowel);
    }

    return vowels.join('');
};

HANGUL.toJongsungs = function (str) {
    var consonants = [];

    for (var i = 0, len = str.length; i < len; i++) {
        var code = str.charCodeAt(i),
            offset,
            consonant;

        if (0xac00 <= code && code < 0xd7a4) {
            offset = (code - 0xac00) % 28;
            consonant = LAST_CONSONANTS[offset];
        } else {
            consonant = '';
        }

        consonants.push(consonant);
    }

    return consonants.join('');
};

HANGUL.indexOf = function (haystack, needle) {
    var jamoHaystack = HANGUL.toJamos(haystack),
        jamoNeedle = HANGUL.toJamos(needle);
    return jamoHaystack.indexOf(jamoNeedle);
};

HANGUL.startsWith = function (haystack, needle) {
    return HANGUL.indexOf(haystack, needle) === 0;
};

}());
