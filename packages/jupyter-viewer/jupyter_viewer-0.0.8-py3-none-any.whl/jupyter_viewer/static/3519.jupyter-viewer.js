"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[3519],{

/***/ 3519:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "elm": () => (/* binding */ elm)
/* harmony export */ });
function switchState(source, setState, f) {
  setState(f);
  return f(source, setState);
}
var lowerRE = /[a-z]/;
var upperRE = /[A-Z]/;
var innerRE = /[a-zA-Z0-9_]/;
var digitRE = /[0-9]/;
var hexRE = /[0-9A-Fa-f]/;
var symbolRE = /[-&*+.\\/<>=?^|:]/;
var specialRE = /[(),[\]{}]/;
var spacesRE = /[ \v\f]/; // newlines are handled in tokenizer

function normal() {
  return function (source, setState) {
    if (source.eatWhile(spacesRE)) {
      return null;
    }
    var char = source.next();
    if (specialRE.test(char)) {
      return char === '{' && source.eat('-') ? switchState(source, setState, chompMultiComment(1)) : char === '[' && source.match('glsl|') ? switchState(source, setState, chompGlsl) : 'builtin';
    }
    if (char === '\'') {
      return switchState(source, setState, chompChar);
    }
    if (char === '"') {
      return source.eat('"') ? source.eat('"') ? switchState(source, setState, chompMultiString) : 'string' : switchState(source, setState, chompSingleString);
    }
    if (upperRE.test(char)) {
      source.eatWhile(innerRE);
      return 'type';
    }
    if (lowerRE.test(char)) {
      var isDef = source.pos === 1;
      source.eatWhile(innerRE);
      return isDef ? "def" : "variable";
    }
    if (digitRE.test(char)) {
      if (char === '0') {
        if (source.eat(/[xX]/)) {
          source.eatWhile(hexRE); // should require at least 1
          return "number";
        }
      } else {
        source.eatWhile(digitRE);
      }
      if (source.eat('.')) {
        source.eatWhile(digitRE); // should require at least 1
      }
      if (source.eat(/[eE]/)) {
        source.eat(/[-+]/);
        source.eatWhile(digitRE); // should require at least 1
      }
      return "number";
    }
    if (symbolRE.test(char)) {
      if (char === '-' && source.eat('-')) {
        source.skipToEnd();
        return "comment";
      }
      source.eatWhile(symbolRE);
      return "keyword";
    }
    if (char === '_') {
      return "keyword";
    }
    return "error";
  };
}
function chompMultiComment(nest) {
  if (nest == 0) {
    return normal();
  }
  return function (source, setState) {
    while (!source.eol()) {
      var char = source.next();
      if (char == '{' && source.eat('-')) {
        ++nest;
      } else if (char == '-' && source.eat('}')) {
        --nest;
        if (nest === 0) {
          setState(normal());
          return 'comment';
        }
      }
    }
    setState(chompMultiComment(nest));
    return 'comment';
  };
}
function chompMultiString(source, setState) {
  while (!source.eol()) {
    var char = source.next();
    if (char === '"' && source.eat('"') && source.eat('"')) {
      setState(normal());
      return 'string';
    }
  }
  return 'string';
}
function chompSingleString(source, setState) {
  while (source.skipTo('\\"')) {
    source.next();
    source.next();
  }
  if (source.skipTo('"')) {
    source.next();
    setState(normal());
    return 'string';
  }
  source.skipToEnd();
  setState(normal());
  return 'error';
}
function chompChar(source, setState) {
  while (source.skipTo("\\'")) {
    source.next();
    source.next();
  }
  if (source.skipTo("'")) {
    source.next();
    setState(normal());
    return 'string';
  }
  source.skipToEnd();
  setState(normal());
  return 'error';
}
function chompGlsl(source, setState) {
  while (!source.eol()) {
    var char = source.next();
    if (char === '|' && source.eat(']')) {
      setState(normal());
      return 'string';
    }
  }
  return 'string';
}
var wellKnownWords = {
  case: 1,
  of: 1,
  as: 1,
  if: 1,
  then: 1,
  else: 1,
  let: 1,
  in: 1,
  type: 1,
  alias: 1,
  module: 1,
  where: 1,
  import: 1,
  exposing: 1,
  port: 1
};
const elm = {
  name: "elm",
  startState: function () {
    return {
      f: normal()
    };
  },
  copyState: function (s) {
    return {
      f: s.f
    };
  },
  token: function (stream, state) {
    var type = state.f(stream, function (s) {
      state.f = s;
    });
    var word = stream.current();
    return wellKnownWords.hasOwnProperty(word) ? 'keyword' : type;
  },
  languageData: {
    commentTokens: {
      line: "--"
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiMzUxOS5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9AY29kZW1pcnJvci9sZWdhY3ktbW9kZXMvbW9kZS9lbG0uanMiXSwic291cmNlc0NvbnRlbnQiOlsiZnVuY3Rpb24gc3dpdGNoU3RhdGUoc291cmNlLCBzZXRTdGF0ZSwgZikge1xuICBzZXRTdGF0ZShmKTtcbiAgcmV0dXJuIGYoc291cmNlLCBzZXRTdGF0ZSk7XG59XG52YXIgbG93ZXJSRSA9IC9bYS16XS87XG52YXIgdXBwZXJSRSA9IC9bQS1aXS87XG52YXIgaW5uZXJSRSA9IC9bYS16QS1aMC05X10vO1xudmFyIGRpZ2l0UkUgPSAvWzAtOV0vO1xudmFyIGhleFJFID0gL1swLTlBLUZhLWZdLztcbnZhciBzeW1ib2xSRSA9IC9bLSYqKy5cXFxcLzw+PT9efDpdLztcbnZhciBzcGVjaWFsUkUgPSAvWygpLFtcXF17fV0vO1xudmFyIHNwYWNlc1JFID0gL1sgXFx2XFxmXS87IC8vIG5ld2xpbmVzIGFyZSBoYW5kbGVkIGluIHRva2VuaXplclxuXG5mdW5jdGlvbiBub3JtYWwoKSB7XG4gIHJldHVybiBmdW5jdGlvbiAoc291cmNlLCBzZXRTdGF0ZSkge1xuICAgIGlmIChzb3VyY2UuZWF0V2hpbGUoc3BhY2VzUkUpKSB7XG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9XG4gICAgdmFyIGNoYXIgPSBzb3VyY2UubmV4dCgpO1xuICAgIGlmIChzcGVjaWFsUkUudGVzdChjaGFyKSkge1xuICAgICAgcmV0dXJuIGNoYXIgPT09ICd7JyAmJiBzb3VyY2UuZWF0KCctJykgPyBzd2l0Y2hTdGF0ZShzb3VyY2UsIHNldFN0YXRlLCBjaG9tcE11bHRpQ29tbWVudCgxKSkgOiBjaGFyID09PSAnWycgJiYgc291cmNlLm1hdGNoKCdnbHNsfCcpID8gc3dpdGNoU3RhdGUoc291cmNlLCBzZXRTdGF0ZSwgY2hvbXBHbHNsKSA6ICdidWlsdGluJztcbiAgICB9XG4gICAgaWYgKGNoYXIgPT09ICdcXCcnKSB7XG4gICAgICByZXR1cm4gc3dpdGNoU3RhdGUoc291cmNlLCBzZXRTdGF0ZSwgY2hvbXBDaGFyKTtcbiAgICB9XG4gICAgaWYgKGNoYXIgPT09ICdcIicpIHtcbiAgICAgIHJldHVybiBzb3VyY2UuZWF0KCdcIicpID8gc291cmNlLmVhdCgnXCInKSA/IHN3aXRjaFN0YXRlKHNvdXJjZSwgc2V0U3RhdGUsIGNob21wTXVsdGlTdHJpbmcpIDogJ3N0cmluZycgOiBzd2l0Y2hTdGF0ZShzb3VyY2UsIHNldFN0YXRlLCBjaG9tcFNpbmdsZVN0cmluZyk7XG4gICAgfVxuICAgIGlmICh1cHBlclJFLnRlc3QoY2hhcikpIHtcbiAgICAgIHNvdXJjZS5lYXRXaGlsZShpbm5lclJFKTtcbiAgICAgIHJldHVybiAndHlwZSc7XG4gICAgfVxuICAgIGlmIChsb3dlclJFLnRlc3QoY2hhcikpIHtcbiAgICAgIHZhciBpc0RlZiA9IHNvdXJjZS5wb3MgPT09IDE7XG4gICAgICBzb3VyY2UuZWF0V2hpbGUoaW5uZXJSRSk7XG4gICAgICByZXR1cm4gaXNEZWYgPyBcImRlZlwiIDogXCJ2YXJpYWJsZVwiO1xuICAgIH1cbiAgICBpZiAoZGlnaXRSRS50ZXN0KGNoYXIpKSB7XG4gICAgICBpZiAoY2hhciA9PT0gJzAnKSB7XG4gICAgICAgIGlmIChzb3VyY2UuZWF0KC9beFhdLykpIHtcbiAgICAgICAgICBzb3VyY2UuZWF0V2hpbGUoaGV4UkUpOyAvLyBzaG91bGQgcmVxdWlyZSBhdCBsZWFzdCAxXG4gICAgICAgICAgcmV0dXJuIFwibnVtYmVyXCI7XG4gICAgICAgIH1cbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHNvdXJjZS5lYXRXaGlsZShkaWdpdFJFKTtcbiAgICAgIH1cbiAgICAgIGlmIChzb3VyY2UuZWF0KCcuJykpIHtcbiAgICAgICAgc291cmNlLmVhdFdoaWxlKGRpZ2l0UkUpOyAvLyBzaG91bGQgcmVxdWlyZSBhdCBsZWFzdCAxXG4gICAgICB9XG4gICAgICBpZiAoc291cmNlLmVhdCgvW2VFXS8pKSB7XG4gICAgICAgIHNvdXJjZS5lYXQoL1stK10vKTtcbiAgICAgICAgc291cmNlLmVhdFdoaWxlKGRpZ2l0UkUpOyAvLyBzaG91bGQgcmVxdWlyZSBhdCBsZWFzdCAxXG4gICAgICB9XG4gICAgICByZXR1cm4gXCJudW1iZXJcIjtcbiAgICB9XG4gICAgaWYgKHN5bWJvbFJFLnRlc3QoY2hhcikpIHtcbiAgICAgIGlmIChjaGFyID09PSAnLScgJiYgc291cmNlLmVhdCgnLScpKSB7XG4gICAgICAgIHNvdXJjZS5za2lwVG9FbmQoKTtcbiAgICAgICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICAgICAgfVxuICAgICAgc291cmNlLmVhdFdoaWxlKHN5bWJvbFJFKTtcbiAgICAgIHJldHVybiBcImtleXdvcmRcIjtcbiAgICB9XG4gICAgaWYgKGNoYXIgPT09ICdfJykge1xuICAgICAgcmV0dXJuIFwia2V5d29yZFwiO1xuICAgIH1cbiAgICByZXR1cm4gXCJlcnJvclwiO1xuICB9O1xufVxuZnVuY3Rpb24gY2hvbXBNdWx0aUNvbW1lbnQobmVzdCkge1xuICBpZiAobmVzdCA9PSAwKSB7XG4gICAgcmV0dXJuIG5vcm1hbCgpO1xuICB9XG4gIHJldHVybiBmdW5jdGlvbiAoc291cmNlLCBzZXRTdGF0ZSkge1xuICAgIHdoaWxlICghc291cmNlLmVvbCgpKSB7XG4gICAgICB2YXIgY2hhciA9IHNvdXJjZS5uZXh0KCk7XG4gICAgICBpZiAoY2hhciA9PSAneycgJiYgc291cmNlLmVhdCgnLScpKSB7XG4gICAgICAgICsrbmVzdDtcbiAgICAgIH0gZWxzZSBpZiAoY2hhciA9PSAnLScgJiYgc291cmNlLmVhdCgnfScpKSB7XG4gICAgICAgIC0tbmVzdDtcbiAgICAgICAgaWYgKG5lc3QgPT09IDApIHtcbiAgICAgICAgICBzZXRTdGF0ZShub3JtYWwoKSk7XG4gICAgICAgICAgcmV0dXJuICdjb21tZW50JztcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH1cbiAgICBzZXRTdGF0ZShjaG9tcE11bHRpQ29tbWVudChuZXN0KSk7XG4gICAgcmV0dXJuICdjb21tZW50JztcbiAgfTtcbn1cbmZ1bmN0aW9uIGNob21wTXVsdGlTdHJpbmcoc291cmNlLCBzZXRTdGF0ZSkge1xuICB3aGlsZSAoIXNvdXJjZS5lb2woKSkge1xuICAgIHZhciBjaGFyID0gc291cmNlLm5leHQoKTtcbiAgICBpZiAoY2hhciA9PT0gJ1wiJyAmJiBzb3VyY2UuZWF0KCdcIicpICYmIHNvdXJjZS5lYXQoJ1wiJykpIHtcbiAgICAgIHNldFN0YXRlKG5vcm1hbCgpKTtcbiAgICAgIHJldHVybiAnc3RyaW5nJztcbiAgICB9XG4gIH1cbiAgcmV0dXJuICdzdHJpbmcnO1xufVxuZnVuY3Rpb24gY2hvbXBTaW5nbGVTdHJpbmcoc291cmNlLCBzZXRTdGF0ZSkge1xuICB3aGlsZSAoc291cmNlLnNraXBUbygnXFxcXFwiJykpIHtcbiAgICBzb3VyY2UubmV4dCgpO1xuICAgIHNvdXJjZS5uZXh0KCk7XG4gIH1cbiAgaWYgKHNvdXJjZS5za2lwVG8oJ1wiJykpIHtcbiAgICBzb3VyY2UubmV4dCgpO1xuICAgIHNldFN0YXRlKG5vcm1hbCgpKTtcbiAgICByZXR1cm4gJ3N0cmluZyc7XG4gIH1cbiAgc291cmNlLnNraXBUb0VuZCgpO1xuICBzZXRTdGF0ZShub3JtYWwoKSk7XG4gIHJldHVybiAnZXJyb3InO1xufVxuZnVuY3Rpb24gY2hvbXBDaGFyKHNvdXJjZSwgc2V0U3RhdGUpIHtcbiAgd2hpbGUgKHNvdXJjZS5za2lwVG8oXCJcXFxcJ1wiKSkge1xuICAgIHNvdXJjZS5uZXh0KCk7XG4gICAgc291cmNlLm5leHQoKTtcbiAgfVxuICBpZiAoc291cmNlLnNraXBUbyhcIidcIikpIHtcbiAgICBzb3VyY2UubmV4dCgpO1xuICAgIHNldFN0YXRlKG5vcm1hbCgpKTtcbiAgICByZXR1cm4gJ3N0cmluZyc7XG4gIH1cbiAgc291cmNlLnNraXBUb0VuZCgpO1xuICBzZXRTdGF0ZShub3JtYWwoKSk7XG4gIHJldHVybiAnZXJyb3InO1xufVxuZnVuY3Rpb24gY2hvbXBHbHNsKHNvdXJjZSwgc2V0U3RhdGUpIHtcbiAgd2hpbGUgKCFzb3VyY2UuZW9sKCkpIHtcbiAgICB2YXIgY2hhciA9IHNvdXJjZS5uZXh0KCk7XG4gICAgaWYgKGNoYXIgPT09ICd8JyAmJiBzb3VyY2UuZWF0KCddJykpIHtcbiAgICAgIHNldFN0YXRlKG5vcm1hbCgpKTtcbiAgICAgIHJldHVybiAnc3RyaW5nJztcbiAgICB9XG4gIH1cbiAgcmV0dXJuICdzdHJpbmcnO1xufVxudmFyIHdlbGxLbm93bldvcmRzID0ge1xuICBjYXNlOiAxLFxuICBvZjogMSxcbiAgYXM6IDEsXG4gIGlmOiAxLFxuICB0aGVuOiAxLFxuICBlbHNlOiAxLFxuICBsZXQ6IDEsXG4gIGluOiAxLFxuICB0eXBlOiAxLFxuICBhbGlhczogMSxcbiAgbW9kdWxlOiAxLFxuICB3aGVyZTogMSxcbiAgaW1wb3J0OiAxLFxuICBleHBvc2luZzogMSxcbiAgcG9ydDogMVxufTtcbmV4cG9ydCBjb25zdCBlbG0gPSB7XG4gIG5hbWU6IFwiZWxtXCIsXG4gIHN0YXJ0U3RhdGU6IGZ1bmN0aW9uICgpIHtcbiAgICByZXR1cm4ge1xuICAgICAgZjogbm9ybWFsKClcbiAgICB9O1xuICB9LFxuICBjb3B5U3RhdGU6IGZ1bmN0aW9uIChzKSB7XG4gICAgcmV0dXJuIHtcbiAgICAgIGY6IHMuZlxuICAgIH07XG4gIH0sXG4gIHRva2VuOiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIHZhciB0eXBlID0gc3RhdGUuZihzdHJlYW0sIGZ1bmN0aW9uIChzKSB7XG4gICAgICBzdGF0ZS5mID0gcztcbiAgICB9KTtcbiAgICB2YXIgd29yZCA9IHN0cmVhbS5jdXJyZW50KCk7XG4gICAgcmV0dXJuIHdlbGxLbm93bldvcmRzLmhhc093blByb3BlcnR5KHdvcmQpID8gJ2tleXdvcmQnIDogdHlwZTtcbiAgfSxcbiAgbGFuZ3VhZ2VEYXRhOiB7XG4gICAgY29tbWVudFRva2Vuczoge1xuICAgICAgbGluZTogXCItLVwiXG4gICAgfVxuICB9XG59OyJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==