"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[4049],{

/***/ 44049:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "solr": () => (/* binding */ solr)
/* harmony export */ });
var isStringChar = /[^\s\|\!\+\-\*\?\~\^\&\:\(\)\[\]\{\}\"\\]/;
var isOperatorChar = /[\|\!\+\-\*\?\~\^\&]/;
var isOperatorString = /^(OR|AND|NOT|TO)$/;
function isNumber(word) {
  return parseFloat(word).toString() === word;
}
function tokenString(quote) {
  return function (stream, state) {
    var escaped = false,
      next;
    while ((next = stream.next()) != null) {
      if (next == quote && !escaped) break;
      escaped = !escaped && next == "\\";
    }
    if (!escaped) state.tokenize = tokenBase;
    return "string";
  };
}
function tokenOperator(operator) {
  return function (stream, state) {
    if (operator == "|") stream.eat(/\|/);else if (operator == "&") stream.eat(/\&/);
    state.tokenize = tokenBase;
    return "operator";
  };
}
function tokenWord(ch) {
  return function (stream, state) {
    var word = ch;
    while ((ch = stream.peek()) && ch.match(isStringChar) != null) {
      word += stream.next();
    }
    state.tokenize = tokenBase;
    if (isOperatorString.test(word)) return "operator";else if (isNumber(word)) return "number";else if (stream.peek() == ":") return "propertyName";else return "string";
  };
}
function tokenBase(stream, state) {
  var ch = stream.next();
  if (ch == '"') state.tokenize = tokenString(ch);else if (isOperatorChar.test(ch)) state.tokenize = tokenOperator(ch);else if (isStringChar.test(ch)) state.tokenize = tokenWord(ch);
  return state.tokenize != tokenBase ? state.tokenize(stream, state) : null;
}
const solr = {
  name: "solr",
  startState: function () {
    return {
      tokenize: tokenBase
    };
  },
  token: function (stream, state) {
    if (stream.eatSpace()) return null;
    return state.tokenize(stream, state);
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNDA0OS5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL0Bjb2RlbWlycm9yL2xlZ2FjeS1tb2Rlcy9tb2RlL3NvbHIuanMiXSwic291cmNlc0NvbnRlbnQiOlsidmFyIGlzU3RyaW5nQ2hhciA9IC9bXlxcc1xcfFxcIVxcK1xcLVxcKlxcP1xcflxcXlxcJlxcOlxcKFxcKVxcW1xcXVxce1xcfVxcXCJcXFxcXS87XG52YXIgaXNPcGVyYXRvckNoYXIgPSAvW1xcfFxcIVxcK1xcLVxcKlxcP1xcflxcXlxcJl0vO1xudmFyIGlzT3BlcmF0b3JTdHJpbmcgPSAvXihPUnxBTkR8Tk9UfFRPKSQvO1xuZnVuY3Rpb24gaXNOdW1iZXIod29yZCkge1xuICByZXR1cm4gcGFyc2VGbG9hdCh3b3JkKS50b1N0cmluZygpID09PSB3b3JkO1xufVxuZnVuY3Rpb24gdG9rZW5TdHJpbmcocXVvdGUpIHtcbiAgcmV0dXJuIGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgdmFyIGVzY2FwZWQgPSBmYWxzZSxcbiAgICAgIG5leHQ7XG4gICAgd2hpbGUgKChuZXh0ID0gc3RyZWFtLm5leHQoKSkgIT0gbnVsbCkge1xuICAgICAgaWYgKG5leHQgPT0gcXVvdGUgJiYgIWVzY2FwZWQpIGJyZWFrO1xuICAgICAgZXNjYXBlZCA9ICFlc2NhcGVkICYmIG5leHQgPT0gXCJcXFxcXCI7XG4gICAgfVxuICAgIGlmICghZXNjYXBlZCkgc3RhdGUudG9rZW5pemUgPSB0b2tlbkJhc2U7XG4gICAgcmV0dXJuIFwic3RyaW5nXCI7XG4gIH07XG59XG5mdW5jdGlvbiB0b2tlbk9wZXJhdG9yKG9wZXJhdG9yKSB7XG4gIHJldHVybiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIGlmIChvcGVyYXRvciA9PSBcInxcIikgc3RyZWFtLmVhdCgvXFx8Lyk7ZWxzZSBpZiAob3BlcmF0b3IgPT0gXCImXCIpIHN0cmVhbS5lYXQoL1xcJi8pO1xuICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlO1xuICAgIHJldHVybiBcIm9wZXJhdG9yXCI7XG4gIH07XG59XG5mdW5jdGlvbiB0b2tlbldvcmQoY2gpIHtcbiAgcmV0dXJuIGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgdmFyIHdvcmQgPSBjaDtcbiAgICB3aGlsZSAoKGNoID0gc3RyZWFtLnBlZWsoKSkgJiYgY2gubWF0Y2goaXNTdHJpbmdDaGFyKSAhPSBudWxsKSB7XG4gICAgICB3b3JkICs9IHN0cmVhbS5uZXh0KCk7XG4gICAgfVxuICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlO1xuICAgIGlmIChpc09wZXJhdG9yU3RyaW5nLnRlc3Qod29yZCkpIHJldHVybiBcIm9wZXJhdG9yXCI7ZWxzZSBpZiAoaXNOdW1iZXIod29yZCkpIHJldHVybiBcIm51bWJlclwiO2Vsc2UgaWYgKHN0cmVhbS5wZWVrKCkgPT0gXCI6XCIpIHJldHVybiBcInByb3BlcnR5TmFtZVwiO2Vsc2UgcmV0dXJuIFwic3RyaW5nXCI7XG4gIH07XG59XG5mdW5jdGlvbiB0b2tlbkJhc2Uoc3RyZWFtLCBzdGF0ZSkge1xuICB2YXIgY2ggPSBzdHJlYW0ubmV4dCgpO1xuICBpZiAoY2ggPT0gJ1wiJykgc3RhdGUudG9rZW5pemUgPSB0b2tlblN0cmluZyhjaCk7ZWxzZSBpZiAoaXNPcGVyYXRvckNoYXIudGVzdChjaCkpIHN0YXRlLnRva2VuaXplID0gdG9rZW5PcGVyYXRvcihjaCk7ZWxzZSBpZiAoaXNTdHJpbmdDaGFyLnRlc3QoY2gpKSBzdGF0ZS50b2tlbml6ZSA9IHRva2VuV29yZChjaCk7XG4gIHJldHVybiBzdGF0ZS50b2tlbml6ZSAhPSB0b2tlbkJhc2UgPyBzdGF0ZS50b2tlbml6ZShzdHJlYW0sIHN0YXRlKSA6IG51bGw7XG59XG5leHBvcnQgY29uc3Qgc29sciA9IHtcbiAgbmFtZTogXCJzb2xyXCIsXG4gIHN0YXJ0U3RhdGU6IGZ1bmN0aW9uICgpIHtcbiAgICByZXR1cm4ge1xuICAgICAgdG9rZW5pemU6IHRva2VuQmFzZVxuICAgIH07XG4gIH0sXG4gIHRva2VuOiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIGlmIChzdHJlYW0uZWF0U3BhY2UoKSkgcmV0dXJuIG51bGw7XG4gICAgcmV0dXJuIHN0YXRlLnRva2VuaXplKHN0cmVhbSwgc3RhdGUpO1xuICB9XG59OyJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==