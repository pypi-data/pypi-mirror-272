"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[5909],{

/***/ 65909:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "troff": () => (/* binding */ troff)
/* harmony export */ });
var words = {};
function tokenBase(stream) {
  if (stream.eatSpace()) return null;
  var sol = stream.sol();
  var ch = stream.next();
  if (ch === '\\') {
    if (stream.match('fB') || stream.match('fR') || stream.match('fI') || stream.match('u') || stream.match('d') || stream.match('%') || stream.match('&')) {
      return 'string';
    }
    if (stream.match('m[')) {
      stream.skipTo(']');
      stream.next();
      return 'string';
    }
    if (stream.match('s+') || stream.match('s-')) {
      stream.eatWhile(/[\d-]/);
      return 'string';
    }
    if (stream.match('\(') || stream.match('*\(')) {
      stream.eatWhile(/[\w-]/);
      return 'string';
    }
    return 'string';
  }
  if (sol && (ch === '.' || ch === '\'')) {
    if (stream.eat('\\') && stream.eat('\"')) {
      stream.skipToEnd();
      return 'comment';
    }
  }
  if (sol && ch === '.') {
    if (stream.match('B ') || stream.match('I ') || stream.match('R ')) {
      return 'attribute';
    }
    if (stream.match('TH ') || stream.match('SH ') || stream.match('SS ') || stream.match('HP ')) {
      stream.skipToEnd();
      return 'quote';
    }
    if (stream.match(/[A-Z]/) && stream.match(/[A-Z]/) || stream.match(/[a-z]/) && stream.match(/[a-z]/)) {
      return 'attribute';
    }
  }
  stream.eatWhile(/[\w-]/);
  var cur = stream.current();
  return words.hasOwnProperty(cur) ? words[cur] : null;
}
function tokenize(stream, state) {
  return (state.tokens[0] || tokenBase)(stream, state);
}
;
const troff = {
  name: "troff",
  startState: function () {
    return {
      tokens: []
    };
  },
  token: function (stream, state) {
    return tokenize(stream, state);
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNTkwOS5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL0Bjb2RlbWlycm9yL2xlZ2FjeS1tb2Rlcy9tb2RlL3Ryb2ZmLmpzIl0sInNvdXJjZXNDb250ZW50IjpbInZhciB3b3JkcyA9IHt9O1xuZnVuY3Rpb24gdG9rZW5CYXNlKHN0cmVhbSkge1xuICBpZiAoc3RyZWFtLmVhdFNwYWNlKCkpIHJldHVybiBudWxsO1xuICB2YXIgc29sID0gc3RyZWFtLnNvbCgpO1xuICB2YXIgY2ggPSBzdHJlYW0ubmV4dCgpO1xuICBpZiAoY2ggPT09ICdcXFxcJykge1xuICAgIGlmIChzdHJlYW0ubWF0Y2goJ2ZCJykgfHwgc3RyZWFtLm1hdGNoKCdmUicpIHx8IHN0cmVhbS5tYXRjaCgnZkknKSB8fCBzdHJlYW0ubWF0Y2goJ3UnKSB8fCBzdHJlYW0ubWF0Y2goJ2QnKSB8fCBzdHJlYW0ubWF0Y2goJyUnKSB8fCBzdHJlYW0ubWF0Y2goJyYnKSkge1xuICAgICAgcmV0dXJuICdzdHJpbmcnO1xuICAgIH1cbiAgICBpZiAoc3RyZWFtLm1hdGNoKCdtWycpKSB7XG4gICAgICBzdHJlYW0uc2tpcFRvKCddJyk7XG4gICAgICBzdHJlYW0ubmV4dCgpO1xuICAgICAgcmV0dXJuICdzdHJpbmcnO1xuICAgIH1cbiAgICBpZiAoc3RyZWFtLm1hdGNoKCdzKycpIHx8IHN0cmVhbS5tYXRjaCgncy0nKSkge1xuICAgICAgc3RyZWFtLmVhdFdoaWxlKC9bXFxkLV0vKTtcbiAgICAgIHJldHVybiAnc3RyaW5nJztcbiAgICB9XG4gICAgaWYgKHN0cmVhbS5tYXRjaCgnXFwoJykgfHwgc3RyZWFtLm1hdGNoKCcqXFwoJykpIHtcbiAgICAgIHN0cmVhbS5lYXRXaGlsZSgvW1xcdy1dLyk7XG4gICAgICByZXR1cm4gJ3N0cmluZyc7XG4gICAgfVxuICAgIHJldHVybiAnc3RyaW5nJztcbiAgfVxuICBpZiAoc29sICYmIChjaCA9PT0gJy4nIHx8IGNoID09PSAnXFwnJykpIHtcbiAgICBpZiAoc3RyZWFtLmVhdCgnXFxcXCcpICYmIHN0cmVhbS5lYXQoJ1xcXCInKSkge1xuICAgICAgc3RyZWFtLnNraXBUb0VuZCgpO1xuICAgICAgcmV0dXJuICdjb21tZW50JztcbiAgICB9XG4gIH1cbiAgaWYgKHNvbCAmJiBjaCA9PT0gJy4nKSB7XG4gICAgaWYgKHN0cmVhbS5tYXRjaCgnQiAnKSB8fCBzdHJlYW0ubWF0Y2goJ0kgJykgfHwgc3RyZWFtLm1hdGNoKCdSICcpKSB7XG4gICAgICByZXR1cm4gJ2F0dHJpYnV0ZSc7XG4gICAgfVxuICAgIGlmIChzdHJlYW0ubWF0Y2goJ1RIICcpIHx8IHN0cmVhbS5tYXRjaCgnU0ggJykgfHwgc3RyZWFtLm1hdGNoKCdTUyAnKSB8fCBzdHJlYW0ubWF0Y2goJ0hQICcpKSB7XG4gICAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgICByZXR1cm4gJ3F1b3RlJztcbiAgICB9XG4gICAgaWYgKHN0cmVhbS5tYXRjaCgvW0EtWl0vKSAmJiBzdHJlYW0ubWF0Y2goL1tBLVpdLykgfHwgc3RyZWFtLm1hdGNoKC9bYS16XS8pICYmIHN0cmVhbS5tYXRjaCgvW2Etel0vKSkge1xuICAgICAgcmV0dXJuICdhdHRyaWJ1dGUnO1xuICAgIH1cbiAgfVxuICBzdHJlYW0uZWF0V2hpbGUoL1tcXHctXS8pO1xuICB2YXIgY3VyID0gc3RyZWFtLmN1cnJlbnQoKTtcbiAgcmV0dXJuIHdvcmRzLmhhc093blByb3BlcnR5KGN1cikgPyB3b3Jkc1tjdXJdIDogbnVsbDtcbn1cbmZ1bmN0aW9uIHRva2VuaXplKHN0cmVhbSwgc3RhdGUpIHtcbiAgcmV0dXJuIChzdGF0ZS50b2tlbnNbMF0gfHwgdG9rZW5CYXNlKShzdHJlYW0sIHN0YXRlKTtcbn1cbjtcbmV4cG9ydCBjb25zdCB0cm9mZiA9IHtcbiAgbmFtZTogXCJ0cm9mZlwiLFxuICBzdGFydFN0YXRlOiBmdW5jdGlvbiAoKSB7XG4gICAgcmV0dXJuIHtcbiAgICAgIHRva2VuczogW11cbiAgICB9O1xuICB9LFxuICB0b2tlbjogZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICByZXR1cm4gdG9rZW5pemUoc3RyZWFtLCBzdGF0ZSk7XG4gIH1cbn07Il0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9