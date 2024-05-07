"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[746],{

/***/ 60746:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "turtle": () => (/* binding */ turtle)
/* harmony export */ });
var curPunc;
function wordRegexp(words) {
  return new RegExp("^(?:" + words.join("|") + ")$", "i");
}
var ops = wordRegexp([]);
var keywords = wordRegexp(["@prefix", "@base", "a"]);
var operatorChars = /[*+\-<>=&|]/;
function tokenBase(stream, state) {
  var ch = stream.next();
  curPunc = null;
  if (ch == "<" && !stream.match(/^[\s\u00a0=]/, false)) {
    stream.match(/^[^\s\u00a0>]*>?/);
    return "atom";
  } else if (ch == "\"" || ch == "'") {
    state.tokenize = tokenLiteral(ch);
    return state.tokenize(stream, state);
  } else if (/[{}\(\),\.;\[\]]/.test(ch)) {
    curPunc = ch;
    return null;
  } else if (ch == "#") {
    stream.skipToEnd();
    return "comment";
  } else if (operatorChars.test(ch)) {
    stream.eatWhile(operatorChars);
    return null;
  } else if (ch == ":") {
    return "operator";
  } else {
    stream.eatWhile(/[_\w\d]/);
    if (stream.peek() == ":") {
      return "variableName.special";
    } else {
      var word = stream.current();
      if (keywords.test(word)) {
        return "meta";
      }
      if (ch >= "A" && ch <= "Z") {
        return "comment";
      } else {
        return "keyword";
      }
    }
    var word = stream.current();
    if (ops.test(word)) return null;else if (keywords.test(word)) return "meta";else return "variable";
  }
}
function tokenLiteral(quote) {
  return function (stream, state) {
    var escaped = false,
      ch;
    while ((ch = stream.next()) != null) {
      if (ch == quote && !escaped) {
        state.tokenize = tokenBase;
        break;
      }
      escaped = !escaped && ch == "\\";
    }
    return "string";
  };
}
function pushContext(state, type, col) {
  state.context = {
    prev: state.context,
    indent: state.indent,
    col: col,
    type: type
  };
}
function popContext(state) {
  state.indent = state.context.indent;
  state.context = state.context.prev;
}
const turtle = {
  name: "turtle",
  startState: function () {
    return {
      tokenize: tokenBase,
      context: null,
      indent: 0,
      col: 0
    };
  },
  token: function (stream, state) {
    if (stream.sol()) {
      if (state.context && state.context.align == null) state.context.align = false;
      state.indent = stream.indentation();
    }
    if (stream.eatSpace()) return null;
    var style = state.tokenize(stream, state);
    if (style != "comment" && state.context && state.context.align == null && state.context.type != "pattern") {
      state.context.align = true;
    }
    if (curPunc == "(") pushContext(state, ")", stream.column());else if (curPunc == "[") pushContext(state, "]", stream.column());else if (curPunc == "{") pushContext(state, "}", stream.column());else if (/[\]\}\)]/.test(curPunc)) {
      while (state.context && state.context.type == "pattern") popContext(state);
      if (state.context && curPunc == state.context.type) popContext(state);
    } else if (curPunc == "." && state.context && state.context.type == "pattern") popContext(state);else if (/atom|string|variable/.test(style) && state.context) {
      if (/[\}\]]/.test(state.context.type)) pushContext(state, "pattern", stream.column());else if (state.context.type == "pattern" && !state.context.align) {
        state.context.align = true;
        state.context.col = stream.column();
      }
    }
    return style;
  },
  indent: function (state, textAfter, cx) {
    var firstChar = textAfter && textAfter.charAt(0);
    var context = state.context;
    if (/[\]\}]/.test(firstChar)) while (context && context.type == "pattern") context = context.prev;
    var closing = context && firstChar == context.type;
    if (!context) return 0;else if (context.type == "pattern") return context.col;else if (context.align) return context.col + (closing ? 0 : 1);else return context.indent + (closing ? 0 : cx.unit);
  },
  languageData: {
    commentTokens: {
      line: "#"
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNzQ2Lmp1cHl0ZXItdmlld2VyLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9AY29kZW1pcnJvci9sZWdhY3ktbW9kZXMvbW9kZS90dXJ0bGUuanMiXSwic291cmNlc0NvbnRlbnQiOlsidmFyIGN1clB1bmM7XG5mdW5jdGlvbiB3b3JkUmVnZXhwKHdvcmRzKSB7XG4gIHJldHVybiBuZXcgUmVnRXhwKFwiXig/OlwiICsgd29yZHMuam9pbihcInxcIikgKyBcIikkXCIsIFwiaVwiKTtcbn1cbnZhciBvcHMgPSB3b3JkUmVnZXhwKFtdKTtcbnZhciBrZXl3b3JkcyA9IHdvcmRSZWdleHAoW1wiQHByZWZpeFwiLCBcIkBiYXNlXCIsIFwiYVwiXSk7XG52YXIgb3BlcmF0b3JDaGFycyA9IC9bKitcXC08Pj0mfF0vO1xuZnVuY3Rpb24gdG9rZW5CYXNlKHN0cmVhbSwgc3RhdGUpIHtcbiAgdmFyIGNoID0gc3RyZWFtLm5leHQoKTtcbiAgY3VyUHVuYyA9IG51bGw7XG4gIGlmIChjaCA9PSBcIjxcIiAmJiAhc3RyZWFtLm1hdGNoKC9eW1xcc1xcdTAwYTA9XS8sIGZhbHNlKSkge1xuICAgIHN0cmVhbS5tYXRjaCgvXlteXFxzXFx1MDBhMD5dKj4/Lyk7XG4gICAgcmV0dXJuIFwiYXRvbVwiO1xuICB9IGVsc2UgaWYgKGNoID09IFwiXFxcIlwiIHx8IGNoID09IFwiJ1wiKSB7XG4gICAgc3RhdGUudG9rZW5pemUgPSB0b2tlbkxpdGVyYWwoY2gpO1xuICAgIHJldHVybiBzdGF0ZS50b2tlbml6ZShzdHJlYW0sIHN0YXRlKTtcbiAgfSBlbHNlIGlmICgvW3t9XFwoXFwpLFxcLjtcXFtcXF1dLy50ZXN0KGNoKSkge1xuICAgIGN1clB1bmMgPSBjaDtcbiAgICByZXR1cm4gbnVsbDtcbiAgfSBlbHNlIGlmIChjaCA9PSBcIiNcIikge1xuICAgIHN0cmVhbS5za2lwVG9FbmQoKTtcbiAgICByZXR1cm4gXCJjb21tZW50XCI7XG4gIH0gZWxzZSBpZiAob3BlcmF0b3JDaGFycy50ZXN0KGNoKSkge1xuICAgIHN0cmVhbS5lYXRXaGlsZShvcGVyYXRvckNoYXJzKTtcbiAgICByZXR1cm4gbnVsbDtcbiAgfSBlbHNlIGlmIChjaCA9PSBcIjpcIikge1xuICAgIHJldHVybiBcIm9wZXJhdG9yXCI7XG4gIH0gZWxzZSB7XG4gICAgc3RyZWFtLmVhdFdoaWxlKC9bX1xcd1xcZF0vKTtcbiAgICBpZiAoc3RyZWFtLnBlZWsoKSA9PSBcIjpcIikge1xuICAgICAgcmV0dXJuIFwidmFyaWFibGVOYW1lLnNwZWNpYWxcIjtcbiAgICB9IGVsc2Uge1xuICAgICAgdmFyIHdvcmQgPSBzdHJlYW0uY3VycmVudCgpO1xuICAgICAgaWYgKGtleXdvcmRzLnRlc3Qod29yZCkpIHtcbiAgICAgICAgcmV0dXJuIFwibWV0YVwiO1xuICAgICAgfVxuICAgICAgaWYgKGNoID49IFwiQVwiICYmIGNoIDw9IFwiWlwiKSB7XG4gICAgICAgIHJldHVybiBcImNvbW1lbnRcIjtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHJldHVybiBcImtleXdvcmRcIjtcbiAgICAgIH1cbiAgICB9XG4gICAgdmFyIHdvcmQgPSBzdHJlYW0uY3VycmVudCgpO1xuICAgIGlmIChvcHMudGVzdCh3b3JkKSkgcmV0dXJuIG51bGw7ZWxzZSBpZiAoa2V5d29yZHMudGVzdCh3b3JkKSkgcmV0dXJuIFwibWV0YVwiO2Vsc2UgcmV0dXJuIFwidmFyaWFibGVcIjtcbiAgfVxufVxuZnVuY3Rpb24gdG9rZW5MaXRlcmFsKHF1b3RlKSB7XG4gIHJldHVybiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIHZhciBlc2NhcGVkID0gZmFsc2UsXG4gICAgICBjaDtcbiAgICB3aGlsZSAoKGNoID0gc3RyZWFtLm5leHQoKSkgIT0gbnVsbCkge1xuICAgICAgaWYgKGNoID09IHF1b3RlICYmICFlc2NhcGVkKSB7XG4gICAgICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlO1xuICAgICAgICBicmVhaztcbiAgICAgIH1cbiAgICAgIGVzY2FwZWQgPSAhZXNjYXBlZCAmJiBjaCA9PSBcIlxcXFxcIjtcbiAgICB9XG4gICAgcmV0dXJuIFwic3RyaW5nXCI7XG4gIH07XG59XG5mdW5jdGlvbiBwdXNoQ29udGV4dChzdGF0ZSwgdHlwZSwgY29sKSB7XG4gIHN0YXRlLmNvbnRleHQgPSB7XG4gICAgcHJldjogc3RhdGUuY29udGV4dCxcbiAgICBpbmRlbnQ6IHN0YXRlLmluZGVudCxcbiAgICBjb2w6IGNvbCxcbiAgICB0eXBlOiB0eXBlXG4gIH07XG59XG5mdW5jdGlvbiBwb3BDb250ZXh0KHN0YXRlKSB7XG4gIHN0YXRlLmluZGVudCA9IHN0YXRlLmNvbnRleHQuaW5kZW50O1xuICBzdGF0ZS5jb250ZXh0ID0gc3RhdGUuY29udGV4dC5wcmV2O1xufVxuZXhwb3J0IGNvbnN0IHR1cnRsZSA9IHtcbiAgbmFtZTogXCJ0dXJ0bGVcIixcbiAgc3RhcnRTdGF0ZTogZnVuY3Rpb24gKCkge1xuICAgIHJldHVybiB7XG4gICAgICB0b2tlbml6ZTogdG9rZW5CYXNlLFxuICAgICAgY29udGV4dDogbnVsbCxcbiAgICAgIGluZGVudDogMCxcbiAgICAgIGNvbDogMFxuICAgIH07XG4gIH0sXG4gIHRva2VuOiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIGlmIChzdHJlYW0uc29sKCkpIHtcbiAgICAgIGlmIChzdGF0ZS5jb250ZXh0ICYmIHN0YXRlLmNvbnRleHQuYWxpZ24gPT0gbnVsbCkgc3RhdGUuY29udGV4dC5hbGlnbiA9IGZhbHNlO1xuICAgICAgc3RhdGUuaW5kZW50ID0gc3RyZWFtLmluZGVudGF0aW9uKCk7XG4gICAgfVxuICAgIGlmIChzdHJlYW0uZWF0U3BhY2UoKSkgcmV0dXJuIG51bGw7XG4gICAgdmFyIHN0eWxlID0gc3RhdGUudG9rZW5pemUoc3RyZWFtLCBzdGF0ZSk7XG4gICAgaWYgKHN0eWxlICE9IFwiY29tbWVudFwiICYmIHN0YXRlLmNvbnRleHQgJiYgc3RhdGUuY29udGV4dC5hbGlnbiA9PSBudWxsICYmIHN0YXRlLmNvbnRleHQudHlwZSAhPSBcInBhdHRlcm5cIikge1xuICAgICAgc3RhdGUuY29udGV4dC5hbGlnbiA9IHRydWU7XG4gICAgfVxuICAgIGlmIChjdXJQdW5jID09IFwiKFwiKSBwdXNoQ29udGV4dChzdGF0ZSwgXCIpXCIsIHN0cmVhbS5jb2x1bW4oKSk7ZWxzZSBpZiAoY3VyUHVuYyA9PSBcIltcIikgcHVzaENvbnRleHQoc3RhdGUsIFwiXVwiLCBzdHJlYW0uY29sdW1uKCkpO2Vsc2UgaWYgKGN1clB1bmMgPT0gXCJ7XCIpIHB1c2hDb250ZXh0KHN0YXRlLCBcIn1cIiwgc3RyZWFtLmNvbHVtbigpKTtlbHNlIGlmICgvW1xcXVxcfVxcKV0vLnRlc3QoY3VyUHVuYykpIHtcbiAgICAgIHdoaWxlIChzdGF0ZS5jb250ZXh0ICYmIHN0YXRlLmNvbnRleHQudHlwZSA9PSBcInBhdHRlcm5cIikgcG9wQ29udGV4dChzdGF0ZSk7XG4gICAgICBpZiAoc3RhdGUuY29udGV4dCAmJiBjdXJQdW5jID09IHN0YXRlLmNvbnRleHQudHlwZSkgcG9wQ29udGV4dChzdGF0ZSk7XG4gICAgfSBlbHNlIGlmIChjdXJQdW5jID09IFwiLlwiICYmIHN0YXRlLmNvbnRleHQgJiYgc3RhdGUuY29udGV4dC50eXBlID09IFwicGF0dGVyblwiKSBwb3BDb250ZXh0KHN0YXRlKTtlbHNlIGlmICgvYXRvbXxzdHJpbmd8dmFyaWFibGUvLnRlc3Qoc3R5bGUpICYmIHN0YXRlLmNvbnRleHQpIHtcbiAgICAgIGlmICgvW1xcfVxcXV0vLnRlc3Qoc3RhdGUuY29udGV4dC50eXBlKSkgcHVzaENvbnRleHQoc3RhdGUsIFwicGF0dGVyblwiLCBzdHJlYW0uY29sdW1uKCkpO2Vsc2UgaWYgKHN0YXRlLmNvbnRleHQudHlwZSA9PSBcInBhdHRlcm5cIiAmJiAhc3RhdGUuY29udGV4dC5hbGlnbikge1xuICAgICAgICBzdGF0ZS5jb250ZXh0LmFsaWduID0gdHJ1ZTtcbiAgICAgICAgc3RhdGUuY29udGV4dC5jb2wgPSBzdHJlYW0uY29sdW1uKCk7XG4gICAgICB9XG4gICAgfVxuICAgIHJldHVybiBzdHlsZTtcbiAgfSxcbiAgaW5kZW50OiBmdW5jdGlvbiAoc3RhdGUsIHRleHRBZnRlciwgY3gpIHtcbiAgICB2YXIgZmlyc3RDaGFyID0gdGV4dEFmdGVyICYmIHRleHRBZnRlci5jaGFyQXQoMCk7XG4gICAgdmFyIGNvbnRleHQgPSBzdGF0ZS5jb250ZXh0O1xuICAgIGlmICgvW1xcXVxcfV0vLnRlc3QoZmlyc3RDaGFyKSkgd2hpbGUgKGNvbnRleHQgJiYgY29udGV4dC50eXBlID09IFwicGF0dGVyblwiKSBjb250ZXh0ID0gY29udGV4dC5wcmV2O1xuICAgIHZhciBjbG9zaW5nID0gY29udGV4dCAmJiBmaXJzdENoYXIgPT0gY29udGV4dC50eXBlO1xuICAgIGlmICghY29udGV4dCkgcmV0dXJuIDA7ZWxzZSBpZiAoY29udGV4dC50eXBlID09IFwicGF0dGVyblwiKSByZXR1cm4gY29udGV4dC5jb2w7ZWxzZSBpZiAoY29udGV4dC5hbGlnbikgcmV0dXJuIGNvbnRleHQuY29sICsgKGNsb3NpbmcgPyAwIDogMSk7ZWxzZSByZXR1cm4gY29udGV4dC5pbmRlbnQgKyAoY2xvc2luZyA/IDAgOiBjeC51bml0KTtcbiAgfSxcbiAgbGFuZ3VhZ2VEYXRhOiB7XG4gICAgY29tbWVudFRva2Vuczoge1xuICAgICAgbGluZTogXCIjXCJcbiAgICB9XG4gIH1cbn07Il0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9