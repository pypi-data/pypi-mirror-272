"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[8819],{

/***/ 78819:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "sieve": () => (/* binding */ sieve)
/* harmony export */ });
function words(str) {
  var obj = {},
    words = str.split(" ");
  for (var i = 0; i < words.length; ++i) obj[words[i]] = true;
  return obj;
}
var keywords = words("if elsif else stop require");
var atoms = words("true false not");
function tokenBase(stream, state) {
  var ch = stream.next();
  if (ch == "/" && stream.eat("*")) {
    state.tokenize = tokenCComment;
    return tokenCComment(stream, state);
  }
  if (ch === '#') {
    stream.skipToEnd();
    return "comment";
  }
  if (ch == "\"") {
    state.tokenize = tokenString(ch);
    return state.tokenize(stream, state);
  }
  if (ch == "(") {
    state._indent.push("(");
    // add virtual angel wings so that editor behaves...
    // ...more sane incase of broken brackets
    state._indent.push("{");
    return null;
  }
  if (ch === "{") {
    state._indent.push("{");
    return null;
  }
  if (ch == ")") {
    state._indent.pop();
    state._indent.pop();
  }
  if (ch === "}") {
    state._indent.pop();
    return null;
  }
  if (ch == ",") return null;
  if (ch == ";") return null;
  if (/[{}\(\),;]/.test(ch)) return null;

  // 1*DIGIT "K" / "M" / "G"
  if (/\d/.test(ch)) {
    stream.eatWhile(/[\d]/);
    stream.eat(/[KkMmGg]/);
    return "number";
  }

  // ":" (ALPHA / "_") *(ALPHA / DIGIT / "_")
  if (ch == ":") {
    stream.eatWhile(/[a-zA-Z_]/);
    stream.eatWhile(/[a-zA-Z0-9_]/);
    return "operator";
  }
  stream.eatWhile(/\w/);
  var cur = stream.current();

  // "text:" *(SP / HTAB) (hash-comment / CRLF)
  // *(multiline-literal / multiline-dotstart)
  // "." CRLF
  if (cur == "text" && stream.eat(":")) {
    state.tokenize = tokenMultiLineString;
    return "string";
  }
  if (keywords.propertyIsEnumerable(cur)) return "keyword";
  if (atoms.propertyIsEnumerable(cur)) return "atom";
  return null;
}
function tokenMultiLineString(stream, state) {
  state._multiLineString = true;
  // the first line is special it may contain a comment
  if (!stream.sol()) {
    stream.eatSpace();
    if (stream.peek() == "#") {
      stream.skipToEnd();
      return "comment";
    }
    stream.skipToEnd();
    return "string";
  }
  if (stream.next() == "." && stream.eol()) {
    state._multiLineString = false;
    state.tokenize = tokenBase;
  }
  return "string";
}
function tokenCComment(stream, state) {
  var maybeEnd = false,
    ch;
  while ((ch = stream.next()) != null) {
    if (maybeEnd && ch == "/") {
      state.tokenize = tokenBase;
      break;
    }
    maybeEnd = ch == "*";
  }
  return "comment";
}
function tokenString(quote) {
  return function (stream, state) {
    var escaped = false,
      ch;
    while ((ch = stream.next()) != null) {
      if (ch == quote && !escaped) break;
      escaped = !escaped && ch == "\\";
    }
    if (!escaped) state.tokenize = tokenBase;
    return "string";
  };
}
const sieve = {
  name: "sieve",
  startState: function (base) {
    return {
      tokenize: tokenBase,
      baseIndent: base || 0,
      _indent: []
    };
  },
  token: function (stream, state) {
    if (stream.eatSpace()) return null;
    return (state.tokenize || tokenBase)(stream, state);
  },
  indent: function (state, _textAfter, cx) {
    var length = state._indent.length;
    if (_textAfter && _textAfter[0] == "}") length--;
    if (length < 0) length = 0;
    return length * cx.unit;
  },
  languageData: {
    indentOnInput: /^\s*\}$/
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiODgxOS5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGNvZGVtaXJyb3IvbGVnYWN5LW1vZGVzL21vZGUvc2lldmUuanMiXSwic291cmNlc0NvbnRlbnQiOlsiZnVuY3Rpb24gd29yZHMoc3RyKSB7XG4gIHZhciBvYmogPSB7fSxcbiAgICB3b3JkcyA9IHN0ci5zcGxpdChcIiBcIik7XG4gIGZvciAodmFyIGkgPSAwOyBpIDwgd29yZHMubGVuZ3RoOyArK2kpIG9ialt3b3Jkc1tpXV0gPSB0cnVlO1xuICByZXR1cm4gb2JqO1xufVxudmFyIGtleXdvcmRzID0gd29yZHMoXCJpZiBlbHNpZiBlbHNlIHN0b3AgcmVxdWlyZVwiKTtcbnZhciBhdG9tcyA9IHdvcmRzKFwidHJ1ZSBmYWxzZSBub3RcIik7XG5mdW5jdGlvbiB0b2tlbkJhc2Uoc3RyZWFtLCBzdGF0ZSkge1xuICB2YXIgY2ggPSBzdHJlYW0ubmV4dCgpO1xuICBpZiAoY2ggPT0gXCIvXCIgJiYgc3RyZWFtLmVhdChcIipcIikpIHtcbiAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQ0NvbW1lbnQ7XG4gICAgcmV0dXJuIHRva2VuQ0NvbW1lbnQoc3RyZWFtLCBzdGF0ZSk7XG4gIH1cbiAgaWYgKGNoID09PSAnIycpIHtcbiAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICB9XG4gIGlmIChjaCA9PSBcIlxcXCJcIikge1xuICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5TdHJpbmcoY2gpO1xuICAgIHJldHVybiBzdGF0ZS50b2tlbml6ZShzdHJlYW0sIHN0YXRlKTtcbiAgfVxuICBpZiAoY2ggPT0gXCIoXCIpIHtcbiAgICBzdGF0ZS5faW5kZW50LnB1c2goXCIoXCIpO1xuICAgIC8vIGFkZCB2aXJ0dWFsIGFuZ2VsIHdpbmdzIHNvIHRoYXQgZWRpdG9yIGJlaGF2ZXMuLi5cbiAgICAvLyAuLi5tb3JlIHNhbmUgaW5jYXNlIG9mIGJyb2tlbiBicmFja2V0c1xuICAgIHN0YXRlLl9pbmRlbnQucHVzaChcIntcIik7XG4gICAgcmV0dXJuIG51bGw7XG4gIH1cbiAgaWYgKGNoID09PSBcIntcIikge1xuICAgIHN0YXRlLl9pbmRlbnQucHVzaChcIntcIik7XG4gICAgcmV0dXJuIG51bGw7XG4gIH1cbiAgaWYgKGNoID09IFwiKVwiKSB7XG4gICAgc3RhdGUuX2luZGVudC5wb3AoKTtcbiAgICBzdGF0ZS5faW5kZW50LnBvcCgpO1xuICB9XG4gIGlmIChjaCA9PT0gXCJ9XCIpIHtcbiAgICBzdGF0ZS5faW5kZW50LnBvcCgpO1xuICAgIHJldHVybiBudWxsO1xuICB9XG4gIGlmIChjaCA9PSBcIixcIikgcmV0dXJuIG51bGw7XG4gIGlmIChjaCA9PSBcIjtcIikgcmV0dXJuIG51bGw7XG4gIGlmICgvW3t9XFwoXFwpLDtdLy50ZXN0KGNoKSkgcmV0dXJuIG51bGw7XG5cbiAgLy8gMSpESUdJVCBcIktcIiAvIFwiTVwiIC8gXCJHXCJcbiAgaWYgKC9cXGQvLnRlc3QoY2gpKSB7XG4gICAgc3RyZWFtLmVhdFdoaWxlKC9bXFxkXS8pO1xuICAgIHN0cmVhbS5lYXQoL1tLa01tR2ddLyk7XG4gICAgcmV0dXJuIFwibnVtYmVyXCI7XG4gIH1cblxuICAvLyBcIjpcIiAoQUxQSEEgLyBcIl9cIikgKihBTFBIQSAvIERJR0lUIC8gXCJfXCIpXG4gIGlmIChjaCA9PSBcIjpcIikge1xuICAgIHN0cmVhbS5lYXRXaGlsZSgvW2EtekEtWl9dLyk7XG4gICAgc3RyZWFtLmVhdFdoaWxlKC9bYS16QS1aMC05X10vKTtcbiAgICByZXR1cm4gXCJvcGVyYXRvclwiO1xuICB9XG4gIHN0cmVhbS5lYXRXaGlsZSgvXFx3Lyk7XG4gIHZhciBjdXIgPSBzdHJlYW0uY3VycmVudCgpO1xuXG4gIC8vIFwidGV4dDpcIiAqKFNQIC8gSFRBQikgKGhhc2gtY29tbWVudCAvIENSTEYpXG4gIC8vICoobXVsdGlsaW5lLWxpdGVyYWwgLyBtdWx0aWxpbmUtZG90c3RhcnQpXG4gIC8vIFwiLlwiIENSTEZcbiAgaWYgKGN1ciA9PSBcInRleHRcIiAmJiBzdHJlYW0uZWF0KFwiOlwiKSkge1xuICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5NdWx0aUxpbmVTdHJpbmc7XG4gICAgcmV0dXJuIFwic3RyaW5nXCI7XG4gIH1cbiAgaWYgKGtleXdvcmRzLnByb3BlcnR5SXNFbnVtZXJhYmxlKGN1cikpIHJldHVybiBcImtleXdvcmRcIjtcbiAgaWYgKGF0b21zLnByb3BlcnR5SXNFbnVtZXJhYmxlKGN1cikpIHJldHVybiBcImF0b21cIjtcbiAgcmV0dXJuIG51bGw7XG59XG5mdW5jdGlvbiB0b2tlbk11bHRpTGluZVN0cmluZyhzdHJlYW0sIHN0YXRlKSB7XG4gIHN0YXRlLl9tdWx0aUxpbmVTdHJpbmcgPSB0cnVlO1xuICAvLyB0aGUgZmlyc3QgbGluZSBpcyBzcGVjaWFsIGl0IG1heSBjb250YWluIGEgY29tbWVudFxuICBpZiAoIXN0cmVhbS5zb2woKSkge1xuICAgIHN0cmVhbS5lYXRTcGFjZSgpO1xuICAgIGlmIChzdHJlYW0ucGVlaygpID09IFwiI1wiKSB7XG4gICAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgICByZXR1cm4gXCJjb21tZW50XCI7XG4gICAgfVxuICAgIHN0cmVhbS5za2lwVG9FbmQoKTtcbiAgICByZXR1cm4gXCJzdHJpbmdcIjtcbiAgfVxuICBpZiAoc3RyZWFtLm5leHQoKSA9PSBcIi5cIiAmJiBzdHJlYW0uZW9sKCkpIHtcbiAgICBzdGF0ZS5fbXVsdGlMaW5lU3RyaW5nID0gZmFsc2U7XG4gICAgc3RhdGUudG9rZW5pemUgPSB0b2tlbkJhc2U7XG4gIH1cbiAgcmV0dXJuIFwic3RyaW5nXCI7XG59XG5mdW5jdGlvbiB0b2tlbkNDb21tZW50KHN0cmVhbSwgc3RhdGUpIHtcbiAgdmFyIG1heWJlRW5kID0gZmFsc2UsXG4gICAgY2g7XG4gIHdoaWxlICgoY2ggPSBzdHJlYW0ubmV4dCgpKSAhPSBudWxsKSB7XG4gICAgaWYgKG1heWJlRW5kICYmIGNoID09IFwiL1wiKSB7XG4gICAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQmFzZTtcbiAgICAgIGJyZWFrO1xuICAgIH1cbiAgICBtYXliZUVuZCA9IGNoID09IFwiKlwiO1xuICB9XG4gIHJldHVybiBcImNvbW1lbnRcIjtcbn1cbmZ1bmN0aW9uIHRva2VuU3RyaW5nKHF1b3RlKSB7XG4gIHJldHVybiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIHZhciBlc2NhcGVkID0gZmFsc2UsXG4gICAgICBjaDtcbiAgICB3aGlsZSAoKGNoID0gc3RyZWFtLm5leHQoKSkgIT0gbnVsbCkge1xuICAgICAgaWYgKGNoID09IHF1b3RlICYmICFlc2NhcGVkKSBicmVhaztcbiAgICAgIGVzY2FwZWQgPSAhZXNjYXBlZCAmJiBjaCA9PSBcIlxcXFxcIjtcbiAgICB9XG4gICAgaWYgKCFlc2NhcGVkKSBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQmFzZTtcbiAgICByZXR1cm4gXCJzdHJpbmdcIjtcbiAgfTtcbn1cbmV4cG9ydCBjb25zdCBzaWV2ZSA9IHtcbiAgbmFtZTogXCJzaWV2ZVwiLFxuICBzdGFydFN0YXRlOiBmdW5jdGlvbiAoYmFzZSkge1xuICAgIHJldHVybiB7XG4gICAgICB0b2tlbml6ZTogdG9rZW5CYXNlLFxuICAgICAgYmFzZUluZGVudDogYmFzZSB8fCAwLFxuICAgICAgX2luZGVudDogW11cbiAgICB9O1xuICB9LFxuICB0b2tlbjogZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICBpZiAoc3RyZWFtLmVhdFNwYWNlKCkpIHJldHVybiBudWxsO1xuICAgIHJldHVybiAoc3RhdGUudG9rZW5pemUgfHwgdG9rZW5CYXNlKShzdHJlYW0sIHN0YXRlKTtcbiAgfSxcbiAgaW5kZW50OiBmdW5jdGlvbiAoc3RhdGUsIF90ZXh0QWZ0ZXIsIGN4KSB7XG4gICAgdmFyIGxlbmd0aCA9IHN0YXRlLl9pbmRlbnQubGVuZ3RoO1xuICAgIGlmIChfdGV4dEFmdGVyICYmIF90ZXh0QWZ0ZXJbMF0gPT0gXCJ9XCIpIGxlbmd0aC0tO1xuICAgIGlmIChsZW5ndGggPCAwKSBsZW5ndGggPSAwO1xuICAgIHJldHVybiBsZW5ndGggKiBjeC51bml0O1xuICB9LFxuICBsYW5ndWFnZURhdGE6IHtcbiAgICBpbmRlbnRPbklucHV0OiAvXlxccypcXH0kL1xuICB9XG59OyJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==