var editor = {};

var Base64 = {
    _keyStr: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",
    encode: function(input) {
        var output = "";
        var chr1, chr2, chr3, enc1, enc2, enc3, enc4;
        var i = 0;
        input = Base64._utf8_encode(input);
        while (i < input.length) {
            chr1 = input.charCodeAt(i++);
            chr2 = input.charCodeAt(i++);
            chr3 = input.charCodeAt(i++);
            enc1 = chr1 >> 2;
            enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
            enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
            enc4 = chr3 & 63;
            if (isNaN(chr2)) {
                enc3 = enc4 = 64;
            } else if (isNaN(chr3)) {
                enc4 = 64;
            }
            output = output + this._keyStr.charAt(enc1) + this._keyStr.charAt(enc2) + this._keyStr.charAt(enc3) + this._keyStr.charAt(enc4);
        }
        return output;
    },
    decode: function(input) {
        var output = "";
        var chr1, chr2, chr3;
        var enc1, enc2, enc3, enc4;
        var i = 0;
        input = input.replace(/[^A-Za-z0-9\+\/\=]/g, "");
        while (i < input.length) {
            enc1 = this._keyStr.indexOf(input.charAt(i++));
            enc2 = this._keyStr.indexOf(input.charAt(i++));
            enc3 = this._keyStr.indexOf(input.charAt(i++));
            enc4 = this._keyStr.indexOf(input.charAt(i++));
            chr1 = (enc1 << 2) | (enc2 >> 4);
            chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);
            chr3 = ((enc3 & 3) << 6) | enc4;
            output = output + String.fromCharCode(chr1);
            if (enc3 != 64) {
                output = output + String.fromCharCode(chr2);
            }
            if (enc4 != 64) {
                output = output + String.fromCharCode(chr3);
            }
        }
        output = Base64._utf8_decode(output);
        return output;
    },
    _utf8_encode: function(string) {
        string = string.replace(/\r\n/g, "\n");
        var utftext = "";
        for (var n = 0; n < string.length; n++) {
            var c = string.charCodeAt(n);
            if (c < 128) {
                utftext += String.fromCharCode(c);
            }
            else if ((c > 127) && (c < 2048)) {
                utftext += String.fromCharCode((c >> 6) | 192);
                utftext += String.fromCharCode((c & 63) | 128);
            }
            else {
                utftext += String.fromCharCode((c >> 12) | 224);
                utftext += String.fromCharCode(((c >> 6) & 63) | 128);
                utftext += String.fromCharCode((c & 63) | 128);
            }
        }
        return utftext;
    },
    _utf8_decode: function(utftext) {
        var string = "";
        var i = 0;
        var c = c1 = c2 = 0;
        while (i < utftext.length) {
            c = utftext.charCodeAt(i);
            if (c < 128) {
                string += String.fromCharCode(c);
                i++;
            }
            else if ((c > 191) && (c < 224)) {
                c2 = utftext.charCodeAt(i + 1);
                string += String.fromCharCode(((c & 31) << 6) | (c2 & 63));
                i += 2;
            }
            else {
                c2 = utftext.charCodeAt(i + 1);
                c3 = utftext.charCodeAt(i + 2);
                string += String.fromCharCode(((c & 15) << 12) | ((c2 & 63) << 6) | (c3 & 63));
                i += 3;
            }
        }
        return string;
    }
};

var ACE = {
	init: function () {
		editor = ace.edit("Editor");


        base64ToText = function() {
            var encoded = editor.getValue();
            var decoded = Base64.decode(encoded);
            editor.getSession().setValue(decoded);
        }

        base64ToText();

        max = function(a, b) {
            if (a >= b) return a;
            return b;
        }

		editor.setTheme("ace/theme/Dawn");
        editor.setReadOnly(true);
	    editor.setAutoScrollEditorIntoView(true);
        editor.setOption("minLines", max(editor.getSession().getValue().split('\n').length, 10));
        editor.setOption("maxLines", max(editor.getSession().getValue().split('\n').length, 10));
	    editor.getSession().setUseWrapMode(true);
	    editor.setOptions({fontSize :"13pt"});

		$('#pasteLanguage').change(function() {
				set_language();
		});

		set_syntax = function(mode) {
			editor.getSession().setMode("ace/mode/"+mode);
		};

		set_language = function() {
			var lang = $('#pasteLanguage').val();
			mode = lang;
            console.log("setting syntax " + mode);
			set_syntax(mode);
		};

		set_language();

	}
};


$(document).ready(function() {
    $('select').material_select();
    $('.modal').modal({
        dismissible: false
    });
    var encryption = $('#pasteEncryption').val();
    if (encryption == "passwd") {
        $("#passwdDialog").modal('open');
        $('#passwdSubmit').click(function() {
            var encryptedData = Base64.decode($('#Editor').html());
            var secret = $('#passwd').val();
            if (!secret) {
                $('#passwdError').show();
                return 0;
            }
            var plainData = "";
            for(var i = 0, j = 0; i < encryptedData.length; i++, j = (j+1) % secret.length) {
                var curTxt = encryptedData[i].charCodeAt();
                var curSec = secret[j].charCodeAt();
                plainData += String.fromCharCode(curTxt ^ curSec);
            }
            $('#Editor').html(Base64.encode(plainData));
            $('#passwd').val("");
            $("#passwdDialog").modal('close');
            ACE.init();
        });
    }else if (encryption == "pgp") {
        $('#pgpDialog').modal('open');
        $('#pgpSubmit').click(function() {
            var secret = $('#pgpkey').val();
            if (!secret) {
                $('#pgpError').show();
                return 0;
            }
            var pass = $('#pgppass').val();
            var encryptedData = $('#Editor').html(), priv = openpgp.key.readArmored(secret);
            var success = priv.keys[0].decrypt(pass);
            var options;
            openpgp.initWorker({ path: '/static/js/openpgp.worker.min.js'})
            options = {
                message: openpgp.message.readArmored(encryptedData),
                privateKey: priv.keys[0]
            };

            openpgp.decrypt(options).then(function(plaintext) {
                //console.log("txt = " + plaintext.data);
                $('#Editor').html(Base64.encode(plaintext.data));
                $('#pgpDialog').modal('close');
                ACE.init();
                return plaintext.data;
            });
        });
    } else{
        ACE.init();
    }
});
