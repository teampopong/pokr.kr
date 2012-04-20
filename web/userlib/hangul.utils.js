define(function () {
    var FIRST_CONSONANTS = [
            'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ',
            'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
        ],
        VOWELS = [
            'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅗㅏ', 'ㅗㅐ',
            'ㅗㅣ', 'ㅛ', 'ㅜ', 'ㅜㅓ', 'ㅜㅔ', 'ㅜㅣ', 'ㅠ', 'ㅡ', 'ㅡㅣ', 'ㅣ'
        ],
        LAST_CONSONANTS = [
            '', 'ㄱ', 'ㄲ', 'ㄱㅅ', 'ㄴ', 'ㄴㅈ', 'ㄴㅎ', 'ㄷ', 'ㄹ', 'ㄹㄱ',
            'ㄹㅁ', 'ㄹㅂ', 'ㄹㅅ', 'ㄹㅌ', 'ㄹㅍ', 'ㄹㅎ', 'ㅁ', 'ㅂ', 'ㅂㅅ',
            'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
        ],
        SINGLE_CONSONANTS = [
            'ㄱ', 'ㄲ', 'ㄱㅅ', 'ㄴ', 'ㄴㅈ', 'ㄴㅎ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㄹㄱ',
            'ㄹㅁ', 'ㄹㅂ', 'ㄹㅅ', 'ㄹㅌ', 'ㄹㅍ', 'ㄹㅎ', 'ㅁ', 'ㅂ', 'ㅃ',
            'ㅂㅅ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
        ];

    return {
        toJamos: function (str) {
            var jamos = [];

            for (var i = 0, len = str.length; i < len; i++) {
                var char_ = str[i];

                jamos.push(this.toChosungs(char_));
                jamos.push(this.toJoongsungs(char_));
                jamos.push(this.toJongsungs(char_));
            }
            return jamos.join('');
        },

        toChosungs: function (str) {
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
        },

        toJoongsungs: function (str) {
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
        },

        toJongsungs: function (str) {
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
        }
    };
});
