"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[9000],{

/***/ 9000:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "forth": () => (/* binding */ forth)
/* harmony export */ });
function toWordList(words) {
  var ret = [];
  words.split(' ').forEach(function (e) {
    ret.push({
      name: e
    });
  });
  return ret;
}
var coreWordList = toWordList('INVERT AND OR XOR\
 2* 2/ LSHIFT RSHIFT\
 0= = 0< < > U< MIN MAX\
 2DROP 2DUP 2OVER 2SWAP ?DUP DEPTH DROP DUP OVER ROT SWAP\
 >R R> R@\
 + - 1+ 1- ABS NEGATE\
 S>D * M* UM*\
 FM/MOD SM/REM UM/MOD */ */MOD / /MOD MOD\
 HERE , @ ! CELL+ CELLS C, C@ C! CHARS 2@ 2!\
 ALIGN ALIGNED +! ALLOT\
 CHAR [CHAR] [ ] BL\
 FIND EXECUTE IMMEDIATE COUNT LITERAL STATE\
 ; DOES> >BODY\
 EVALUATE\
 SOURCE >IN\
 <# # #S #> HOLD SIGN BASE >NUMBER HEX DECIMAL\
 FILL MOVE\
 . CR EMIT SPACE SPACES TYPE U. .R U.R\
 ACCEPT\
 TRUE FALSE\
 <> U> 0<> 0>\
 NIP TUCK ROLL PICK\
 2>R 2R@ 2R>\
 WITHIN UNUSED MARKER\
 I J\
 TO\
 COMPILE, [COMPILE]\
 SAVE-INPUT RESTORE-INPUT\
 PAD ERASE\
 2LITERAL DNEGATE\
 D- D+ D0< D0= D2* D2/ D< D= DMAX DMIN D>S DABS\
 M+ M*/ D. D.R 2ROT DU<\
 CATCH THROW\
 FREE RESIZE ALLOCATE\
 CS-PICK CS-ROLL\
 GET-CURRENT SET-CURRENT FORTH-WORDLIST GET-ORDER SET-ORDER\
 PREVIOUS SEARCH-WORDLIST WORDLIST FIND ALSO ONLY FORTH DEFINITIONS ORDER\
 -TRAILING /STRING SEARCH COMPARE CMOVE CMOVE> BLANK SLITERAL');
var immediateWordList = toWordList('IF ELSE THEN BEGIN WHILE REPEAT UNTIL RECURSE [IF] [ELSE] [THEN] ?DO DO LOOP +LOOP UNLOOP LEAVE EXIT AGAIN CASE OF ENDOF ENDCASE');
function searchWordList(wordList, word) {
  var i;
  for (i = wordList.length - 1; i >= 0; i--) {
    if (wordList[i].name === word.toUpperCase()) {
      return wordList[i];
    }
  }
  return undefined;
}
const forth = {
  name: "forth",
  startState: function () {
    return {
      state: '',
      base: 10,
      coreWordList: coreWordList,
      immediateWordList: immediateWordList,
      wordList: []
    };
  },
  token: function (stream, stt) {
    var mat;
    if (stream.eatSpace()) {
      return null;
    }
    if (stt.state === '') {
      // interpretation
      if (stream.match(/^(\]|:NONAME)(\s|$)/i)) {
        stt.state = ' compilation';
        return 'builtin';
      }
      mat = stream.match(/^(\:)\s+(\S+)(\s|$)+/);
      if (mat) {
        stt.wordList.push({
          name: mat[2].toUpperCase()
        });
        stt.state = ' compilation';
        return 'def';
      }
      mat = stream.match(/^(VARIABLE|2VARIABLE|CONSTANT|2CONSTANT|CREATE|POSTPONE|VALUE|WORD)\s+(\S+)(\s|$)+/i);
      if (mat) {
        stt.wordList.push({
          name: mat[2].toUpperCase()
        });
        return 'def';
      }
      mat = stream.match(/^(\'|\[\'\])\s+(\S+)(\s|$)+/);
      if (mat) {
        return 'builtin';
      }
    } else {
      // compilation
      // ; [
      if (stream.match(/^(\;|\[)(\s)/)) {
        stt.state = '';
        stream.backUp(1);
        return 'builtin';
      }
      if (stream.match(/^(\;|\[)($)/)) {
        stt.state = '';
        return 'builtin';
      }
      if (stream.match(/^(POSTPONE)\s+\S+(\s|$)+/)) {
        return 'builtin';
      }
    }

    // dynamic wordlist
    mat = stream.match(/^(\S+)(\s+|$)/);
    if (mat) {
      if (searchWordList(stt.wordList, mat[1]) !== undefined) {
        return 'variable';
      }

      // comments
      if (mat[1] === '\\') {
        stream.skipToEnd();
        return 'comment';
      }

      // core words
      if (searchWordList(stt.coreWordList, mat[1]) !== undefined) {
        return 'builtin';
      }
      if (searchWordList(stt.immediateWordList, mat[1]) !== undefined) {
        return 'keyword';
      }
      if (mat[1] === '(') {
        stream.eatWhile(function (s) {
          return s !== ')';
        });
        stream.eat(')');
        return 'comment';
      }

      // // strings
      if (mat[1] === '.(') {
        stream.eatWhile(function (s) {
          return s !== ')';
        });
        stream.eat(')');
        return 'string';
      }
      if (mat[1] === 'S"' || mat[1] === '."' || mat[1] === 'C"') {
        stream.eatWhile(function (s) {
          return s !== '"';
        });
        stream.eat('"');
        return 'string';
      }

      // numbers
      if (mat[1] - 0xfffffffff) {
        return 'number';
      }
      // if (mat[1].match(/^[-+]?[0-9]+\.[0-9]*/)) {
      //     return 'number';
      // }

      return 'atom';
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiOTAwMC5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9AY29kZW1pcnJvci9sZWdhY3ktbW9kZXMvbW9kZS9mb3J0aC5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyJmdW5jdGlvbiB0b1dvcmRMaXN0KHdvcmRzKSB7XG4gIHZhciByZXQgPSBbXTtcbiAgd29yZHMuc3BsaXQoJyAnKS5mb3JFYWNoKGZ1bmN0aW9uIChlKSB7XG4gICAgcmV0LnB1c2goe1xuICAgICAgbmFtZTogZVxuICAgIH0pO1xuICB9KTtcbiAgcmV0dXJuIHJldDtcbn1cbnZhciBjb3JlV29yZExpc3QgPSB0b1dvcmRMaXN0KCdJTlZFUlQgQU5EIE9SIFhPUlxcXG4gMiogMi8gTFNISUZUIFJTSElGVFxcXG4gMD0gPSAwPCA8ID4gVTwgTUlOIE1BWFxcXG4gMkRST1AgMkRVUCAyT1ZFUiAyU1dBUCA/RFVQIERFUFRIIERST1AgRFVQIE9WRVIgUk9UIFNXQVBcXFxuID5SIFI+IFJAXFxcbiArIC0gMSsgMS0gQUJTIE5FR0FURVxcXG4gUz5EICogTSogVU0qXFxcbiBGTS9NT0QgU00vUkVNIFVNL01PRCAqLyAqL01PRCAvIC9NT0QgTU9EXFxcbiBIRVJFICwgQCAhIENFTEwrIENFTExTIEMsIENAIEMhIENIQVJTIDJAIDIhXFxcbiBBTElHTiBBTElHTkVEICshIEFMTE9UXFxcbiBDSEFSIFtDSEFSXSBbIF0gQkxcXFxuIEZJTkQgRVhFQ1VURSBJTU1FRElBVEUgQ09VTlQgTElURVJBTCBTVEFURVxcXG4gOyBET0VTPiA+Qk9EWVxcXG4gRVZBTFVBVEVcXFxuIFNPVVJDRSA+SU5cXFxuIDwjICMgI1MgIz4gSE9MRCBTSUdOIEJBU0UgPk5VTUJFUiBIRVggREVDSU1BTFxcXG4gRklMTCBNT1ZFXFxcbiAuIENSIEVNSVQgU1BBQ0UgU1BBQ0VTIFRZUEUgVS4gLlIgVS5SXFxcbiBBQ0NFUFRcXFxuIFRSVUUgRkFMU0VcXFxuIDw+IFU+IDA8PiAwPlxcXG4gTklQIFRVQ0sgUk9MTCBQSUNLXFxcbiAyPlIgMlJAIDJSPlxcXG4gV0lUSElOIFVOVVNFRCBNQVJLRVJcXFxuIEkgSlxcXG4gVE9cXFxuIENPTVBJTEUsIFtDT01QSUxFXVxcXG4gU0FWRS1JTlBVVCBSRVNUT1JFLUlOUFVUXFxcbiBQQUQgRVJBU0VcXFxuIDJMSVRFUkFMIERORUdBVEVcXFxuIEQtIEQrIEQwPCBEMD0gRDIqIEQyLyBEPCBEPSBETUFYIERNSU4gRD5TIERBQlNcXFxuIE0rIE0qLyBELiBELlIgMlJPVCBEVTxcXFxuIENBVENIIFRIUk9XXFxcbiBGUkVFIFJFU0laRSBBTExPQ0FURVxcXG4gQ1MtUElDSyBDUy1ST0xMXFxcbiBHRVQtQ1VSUkVOVCBTRVQtQ1VSUkVOVCBGT1JUSC1XT1JETElTVCBHRVQtT1JERVIgU0VULU9SREVSXFxcbiBQUkVWSU9VUyBTRUFSQ0gtV09SRExJU1QgV09SRExJU1QgRklORCBBTFNPIE9OTFkgRk9SVEggREVGSU5JVElPTlMgT1JERVJcXFxuIC1UUkFJTElORyAvU1RSSU5HIFNFQVJDSCBDT01QQVJFIENNT1ZFIENNT1ZFPiBCTEFOSyBTTElURVJBTCcpO1xudmFyIGltbWVkaWF0ZVdvcmRMaXN0ID0gdG9Xb3JkTGlzdCgnSUYgRUxTRSBUSEVOIEJFR0lOIFdISUxFIFJFUEVBVCBVTlRJTCBSRUNVUlNFIFtJRl0gW0VMU0VdIFtUSEVOXSA/RE8gRE8gTE9PUCArTE9PUCBVTkxPT1AgTEVBVkUgRVhJVCBBR0FJTiBDQVNFIE9GIEVORE9GIEVORENBU0UnKTtcbmZ1bmN0aW9uIHNlYXJjaFdvcmRMaXN0KHdvcmRMaXN0LCB3b3JkKSB7XG4gIHZhciBpO1xuICBmb3IgKGkgPSB3b3JkTGlzdC5sZW5ndGggLSAxOyBpID49IDA7IGktLSkge1xuICAgIGlmICh3b3JkTGlzdFtpXS5uYW1lID09PSB3b3JkLnRvVXBwZXJDYXNlKCkpIHtcbiAgICAgIHJldHVybiB3b3JkTGlzdFtpXTtcbiAgICB9XG4gIH1cbiAgcmV0dXJuIHVuZGVmaW5lZDtcbn1cbmV4cG9ydCBjb25zdCBmb3J0aCA9IHtcbiAgbmFtZTogXCJmb3J0aFwiLFxuICBzdGFydFN0YXRlOiBmdW5jdGlvbiAoKSB7XG4gICAgcmV0dXJuIHtcbiAgICAgIHN0YXRlOiAnJyxcbiAgICAgIGJhc2U6IDEwLFxuICAgICAgY29yZVdvcmRMaXN0OiBjb3JlV29yZExpc3QsXG4gICAgICBpbW1lZGlhdGVXb3JkTGlzdDogaW1tZWRpYXRlV29yZExpc3QsXG4gICAgICB3b3JkTGlzdDogW11cbiAgICB9O1xuICB9LFxuICB0b2tlbjogZnVuY3Rpb24gKHN0cmVhbSwgc3R0KSB7XG4gICAgdmFyIG1hdDtcbiAgICBpZiAoc3RyZWFtLmVhdFNwYWNlKCkpIHtcbiAgICAgIHJldHVybiBudWxsO1xuICAgIH1cbiAgICBpZiAoc3R0LnN0YXRlID09PSAnJykge1xuICAgICAgLy8gaW50ZXJwcmV0YXRpb25cbiAgICAgIGlmIChzdHJlYW0ubWF0Y2goL14oXFxdfDpOT05BTUUpKFxcc3wkKS9pKSkge1xuICAgICAgICBzdHQuc3RhdGUgPSAnIGNvbXBpbGF0aW9uJztcbiAgICAgICAgcmV0dXJuICdidWlsdGluJztcbiAgICAgIH1cbiAgICAgIG1hdCA9IHN0cmVhbS5tYXRjaCgvXihcXDopXFxzKyhcXFMrKShcXHN8JCkrLyk7XG4gICAgICBpZiAobWF0KSB7XG4gICAgICAgIHN0dC53b3JkTGlzdC5wdXNoKHtcbiAgICAgICAgICBuYW1lOiBtYXRbMl0udG9VcHBlckNhc2UoKVxuICAgICAgICB9KTtcbiAgICAgICAgc3R0LnN0YXRlID0gJyBjb21waWxhdGlvbic7XG4gICAgICAgIHJldHVybiAnZGVmJztcbiAgICAgIH1cbiAgICAgIG1hdCA9IHN0cmVhbS5tYXRjaCgvXihWQVJJQUJMRXwyVkFSSUFCTEV8Q09OU1RBTlR8MkNPTlNUQU5UfENSRUFURXxQT1NUUE9ORXxWQUxVRXxXT1JEKVxccysoXFxTKykoXFxzfCQpKy9pKTtcbiAgICAgIGlmIChtYXQpIHtcbiAgICAgICAgc3R0LndvcmRMaXN0LnB1c2goe1xuICAgICAgICAgIG5hbWU6IG1hdFsyXS50b1VwcGVyQ2FzZSgpXG4gICAgICAgIH0pO1xuICAgICAgICByZXR1cm4gJ2RlZic7XG4gICAgICB9XG4gICAgICBtYXQgPSBzdHJlYW0ubWF0Y2goL14oXFwnfFxcW1xcJ1xcXSlcXHMrKFxcUyspKFxcc3wkKSsvKTtcbiAgICAgIGlmIChtYXQpIHtcbiAgICAgICAgcmV0dXJuICdidWlsdGluJztcbiAgICAgIH1cbiAgICB9IGVsc2Uge1xuICAgICAgLy8gY29tcGlsYXRpb25cbiAgICAgIC8vIDsgW1xuICAgICAgaWYgKHN0cmVhbS5tYXRjaCgvXihcXDt8XFxbKShcXHMpLykpIHtcbiAgICAgICAgc3R0LnN0YXRlID0gJyc7XG4gICAgICAgIHN0cmVhbS5iYWNrVXAoMSk7XG4gICAgICAgIHJldHVybiAnYnVpbHRpbic7XG4gICAgICB9XG4gICAgICBpZiAoc3RyZWFtLm1hdGNoKC9eKFxcO3xcXFspKCQpLykpIHtcbiAgICAgICAgc3R0LnN0YXRlID0gJyc7XG4gICAgICAgIHJldHVybiAnYnVpbHRpbic7XG4gICAgICB9XG4gICAgICBpZiAoc3RyZWFtLm1hdGNoKC9eKFBPU1RQT05FKVxccytcXFMrKFxcc3wkKSsvKSkge1xuICAgICAgICByZXR1cm4gJ2J1aWx0aW4nO1xuICAgICAgfVxuICAgIH1cblxuICAgIC8vIGR5bmFtaWMgd29yZGxpc3RcbiAgICBtYXQgPSBzdHJlYW0ubWF0Y2goL14oXFxTKykoXFxzK3wkKS8pO1xuICAgIGlmIChtYXQpIHtcbiAgICAgIGlmIChzZWFyY2hXb3JkTGlzdChzdHQud29yZExpc3QsIG1hdFsxXSkgIT09IHVuZGVmaW5lZCkge1xuICAgICAgICByZXR1cm4gJ3ZhcmlhYmxlJztcbiAgICAgIH1cblxuICAgICAgLy8gY29tbWVudHNcbiAgICAgIGlmIChtYXRbMV0gPT09ICdcXFxcJykge1xuICAgICAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgICAgIHJldHVybiAnY29tbWVudCc7XG4gICAgICB9XG5cbiAgICAgIC8vIGNvcmUgd29yZHNcbiAgICAgIGlmIChzZWFyY2hXb3JkTGlzdChzdHQuY29yZVdvcmRMaXN0LCBtYXRbMV0pICE9PSB1bmRlZmluZWQpIHtcbiAgICAgICAgcmV0dXJuICdidWlsdGluJztcbiAgICAgIH1cbiAgICAgIGlmIChzZWFyY2hXb3JkTGlzdChzdHQuaW1tZWRpYXRlV29yZExpc3QsIG1hdFsxXSkgIT09IHVuZGVmaW5lZCkge1xuICAgICAgICByZXR1cm4gJ2tleXdvcmQnO1xuICAgICAgfVxuICAgICAgaWYgKG1hdFsxXSA9PT0gJygnKSB7XG4gICAgICAgIHN0cmVhbS5lYXRXaGlsZShmdW5jdGlvbiAocykge1xuICAgICAgICAgIHJldHVybiBzICE9PSAnKSc7XG4gICAgICAgIH0pO1xuICAgICAgICBzdHJlYW0uZWF0KCcpJyk7XG4gICAgICAgIHJldHVybiAnY29tbWVudCc7XG4gICAgICB9XG5cbiAgICAgIC8vIC8vIHN0cmluZ3NcbiAgICAgIGlmIChtYXRbMV0gPT09ICcuKCcpIHtcbiAgICAgICAgc3RyZWFtLmVhdFdoaWxlKGZ1bmN0aW9uIChzKSB7XG4gICAgICAgICAgcmV0dXJuIHMgIT09ICcpJztcbiAgICAgICAgfSk7XG4gICAgICAgIHN0cmVhbS5lYXQoJyknKTtcbiAgICAgICAgcmV0dXJuICdzdHJpbmcnO1xuICAgICAgfVxuICAgICAgaWYgKG1hdFsxXSA9PT0gJ1NcIicgfHwgbWF0WzFdID09PSAnLlwiJyB8fCBtYXRbMV0gPT09ICdDXCInKSB7XG4gICAgICAgIHN0cmVhbS5lYXRXaGlsZShmdW5jdGlvbiAocykge1xuICAgICAgICAgIHJldHVybiBzICE9PSAnXCInO1xuICAgICAgICB9KTtcbiAgICAgICAgc3RyZWFtLmVhdCgnXCInKTtcbiAgICAgICAgcmV0dXJuICdzdHJpbmcnO1xuICAgICAgfVxuXG4gICAgICAvLyBudW1iZXJzXG4gICAgICBpZiAobWF0WzFdIC0gMHhmZmZmZmZmZmYpIHtcbiAgICAgICAgcmV0dXJuICdudW1iZXInO1xuICAgICAgfVxuICAgICAgLy8gaWYgKG1hdFsxXS5tYXRjaCgvXlstK10/WzAtOV0rXFwuWzAtOV0qLykpIHtcbiAgICAgIC8vICAgICByZXR1cm4gJ251bWJlcic7XG4gICAgICAvLyB9XG5cbiAgICAgIHJldHVybiAnYXRvbSc7XG4gICAgfVxuICB9XG59OyJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==