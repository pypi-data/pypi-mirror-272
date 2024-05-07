"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[4895],{

/***/ 24895:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ez80": () => (/* binding */ ez80),
/* harmony export */   "z80": () => (/* binding */ z80)
/* harmony export */ });
function mkZ80(ez80) {
  var keywords1, keywords2;
  if (ez80) {
    keywords1 = /^(exx?|(ld|cp)([di]r?)?|[lp]ea|pop|push|ad[cd]|cpl|daa|dec|inc|neg|sbc|sub|and|bit|[cs]cf|x?or|res|set|r[lr]c?a?|r[lr]d|s[lr]a|srl|djnz|nop|[de]i|halt|im|in([di]mr?|ir?|irx|2r?)|ot(dmr?|[id]rx|imr?)|out(0?|[di]r?|[di]2r?)|tst(io)?|slp)(\.([sl]?i)?[sl])?\b/i;
    keywords2 = /^(((call|j[pr]|rst|ret[in]?)(\.([sl]?i)?[sl])?)|(rs|st)mix)\b/i;
  } else {
    keywords1 = /^(exx?|(ld|cp|in)([di]r?)?|pop|push|ad[cd]|cpl|daa|dec|inc|neg|sbc|sub|and|bit|[cs]cf|x?or|res|set|r[lr]c?a?|r[lr]d|s[lr]a|srl|djnz|nop|rst|[de]i|halt|im|ot[di]r|out[di]?)\b/i;
    keywords2 = /^(call|j[pr]|ret[in]?|b_?(call|jump))\b/i;
  }
  var variables1 = /^(af?|bc?|c|de?|e|hl?|l|i[xy]?|r|sp)\b/i;
  var variables2 = /^(n?[zc]|p[oe]?|m)\b/i;
  var errors = /^([hl][xy]|i[xy][hl]|slia|sll)\b/i;
  var numbers = /^([\da-f]+h|[0-7]+o|[01]+b|\d+d?)\b/i;
  return {
    name: "z80",
    startState: function () {
      return {
        context: 0
      };
    },
    token: function (stream, state) {
      if (!stream.column()) state.context = 0;
      if (stream.eatSpace()) return null;
      var w;
      if (stream.eatWhile(/\w/)) {
        if (ez80 && stream.eat('.')) {
          stream.eatWhile(/\w/);
        }
        w = stream.current();
        if (stream.indentation()) {
          if ((state.context == 1 || state.context == 4) && variables1.test(w)) {
            state.context = 4;
            return 'variable';
          }
          if (state.context == 2 && variables2.test(w)) {
            state.context = 4;
            return 'variableName.special';
          }
          if (keywords1.test(w)) {
            state.context = 1;
            return 'keyword';
          } else if (keywords2.test(w)) {
            state.context = 2;
            return 'keyword';
          } else if (state.context == 4 && numbers.test(w)) {
            return 'number';
          }
          if (errors.test(w)) return 'error';
        } else if (stream.match(numbers)) {
          return 'number';
        } else {
          return null;
        }
      } else if (stream.eat(';')) {
        stream.skipToEnd();
        return 'comment';
      } else if (stream.eat('"')) {
        while (w = stream.next()) {
          if (w == '"') break;
          if (w == '\\') stream.next();
        }
        return 'string';
      } else if (stream.eat('\'')) {
        if (stream.match(/\\?.'/)) return 'number';
      } else if (stream.eat('.') || stream.sol() && stream.eat('#')) {
        state.context = 5;
        if (stream.eatWhile(/\w/)) return 'def';
      } else if (stream.eat('$')) {
        if (stream.eatWhile(/[\da-f]/i)) return 'number';
      } else if (stream.eat('%')) {
        if (stream.eatWhile(/[01]/)) return 'number';
      } else {
        stream.next();
      }
      return null;
    }
  };
}
;
const z80 = mkZ80(false);
const ez80 = mkZ80(true);

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNDg5NS5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGNvZGVtaXJyb3IvbGVnYWN5LW1vZGVzL21vZGUvejgwLmpzIl0sInNvdXJjZXNDb250ZW50IjpbImZ1bmN0aW9uIG1rWjgwKGV6ODApIHtcbiAgdmFyIGtleXdvcmRzMSwga2V5d29yZHMyO1xuICBpZiAoZXo4MCkge1xuICAgIGtleXdvcmRzMSA9IC9eKGV4eD98KGxkfGNwKShbZGldcj8pP3xbbHBdZWF8cG9wfHB1c2h8YWRbY2RdfGNwbHxkYWF8ZGVjfGluY3xuZWd8c2JjfHN1YnxhbmR8Yml0fFtjc11jZnx4P29yfHJlc3xzZXR8cltscl1jP2E/fHJbbHJdZHxzW2xyXWF8c3JsfGRqbnp8bm9wfFtkZV1pfGhhbHR8aW18aW4oW2RpXW1yP3xpcj98aXJ4fDJyPyl8b3QoZG1yP3xbaWRdcnh8aW1yPyl8b3V0KDA/fFtkaV1yP3xbZGldMnI/KXx0c3QoaW8pP3xzbHApKFxcLihbc2xdP2kpP1tzbF0pP1xcYi9pO1xuICAgIGtleXdvcmRzMiA9IC9eKCgoY2FsbHxqW3ByXXxyc3R8cmV0W2luXT8pKFxcLihbc2xdP2kpP1tzbF0pPyl8KHJzfHN0KW1peClcXGIvaTtcbiAgfSBlbHNlIHtcbiAgICBrZXl3b3JkczEgPSAvXihleHg/fChsZHxjcHxpbikoW2RpXXI/KT98cG9wfHB1c2h8YWRbY2RdfGNwbHxkYWF8ZGVjfGluY3xuZWd8c2JjfHN1YnxhbmR8Yml0fFtjc11jZnx4P29yfHJlc3xzZXR8cltscl1jP2E/fHJbbHJdZHxzW2xyXWF8c3JsfGRqbnp8bm9wfHJzdHxbZGVdaXxoYWx0fGltfG90W2RpXXJ8b3V0W2RpXT8pXFxiL2k7XG4gICAga2V5d29yZHMyID0gL14oY2FsbHxqW3ByXXxyZXRbaW5dP3xiXz8oY2FsbHxqdW1wKSlcXGIvaTtcbiAgfVxuICB2YXIgdmFyaWFibGVzMSA9IC9eKGFmP3xiYz98Y3xkZT98ZXxobD98bHxpW3h5XT98cnxzcClcXGIvaTtcbiAgdmFyIHZhcmlhYmxlczIgPSAvXihuP1t6Y118cFtvZV0/fG0pXFxiL2k7XG4gIHZhciBlcnJvcnMgPSAvXihbaGxdW3h5XXxpW3h5XVtobF18c2xpYXxzbGwpXFxiL2k7XG4gIHZhciBudW1iZXJzID0gL14oW1xcZGEtZl0raHxbMC03XStvfFswMV0rYnxcXGQrZD8pXFxiL2k7XG4gIHJldHVybiB7XG4gICAgbmFtZTogXCJ6ODBcIixcbiAgICBzdGFydFN0YXRlOiBmdW5jdGlvbiAoKSB7XG4gICAgICByZXR1cm4ge1xuICAgICAgICBjb250ZXh0OiAwXG4gICAgICB9O1xuICAgIH0sXG4gICAgdG9rZW46IGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgICBpZiAoIXN0cmVhbS5jb2x1bW4oKSkgc3RhdGUuY29udGV4dCA9IDA7XG4gICAgICBpZiAoc3RyZWFtLmVhdFNwYWNlKCkpIHJldHVybiBudWxsO1xuICAgICAgdmFyIHc7XG4gICAgICBpZiAoc3RyZWFtLmVhdFdoaWxlKC9cXHcvKSkge1xuICAgICAgICBpZiAoZXo4MCAmJiBzdHJlYW0uZWF0KCcuJykpIHtcbiAgICAgICAgICBzdHJlYW0uZWF0V2hpbGUoL1xcdy8pO1xuICAgICAgICB9XG4gICAgICAgIHcgPSBzdHJlYW0uY3VycmVudCgpO1xuICAgICAgICBpZiAoc3RyZWFtLmluZGVudGF0aW9uKCkpIHtcbiAgICAgICAgICBpZiAoKHN0YXRlLmNvbnRleHQgPT0gMSB8fCBzdGF0ZS5jb250ZXh0ID09IDQpICYmIHZhcmlhYmxlczEudGVzdCh3KSkge1xuICAgICAgICAgICAgc3RhdGUuY29udGV4dCA9IDQ7XG4gICAgICAgICAgICByZXR1cm4gJ3ZhcmlhYmxlJztcbiAgICAgICAgICB9XG4gICAgICAgICAgaWYgKHN0YXRlLmNvbnRleHQgPT0gMiAmJiB2YXJpYWJsZXMyLnRlc3QodykpIHtcbiAgICAgICAgICAgIHN0YXRlLmNvbnRleHQgPSA0O1xuICAgICAgICAgICAgcmV0dXJuICd2YXJpYWJsZU5hbWUuc3BlY2lhbCc7XG4gICAgICAgICAgfVxuICAgICAgICAgIGlmIChrZXl3b3JkczEudGVzdCh3KSkge1xuICAgICAgICAgICAgc3RhdGUuY29udGV4dCA9IDE7XG4gICAgICAgICAgICByZXR1cm4gJ2tleXdvcmQnO1xuICAgICAgICAgIH0gZWxzZSBpZiAoa2V5d29yZHMyLnRlc3QodykpIHtcbiAgICAgICAgICAgIHN0YXRlLmNvbnRleHQgPSAyO1xuICAgICAgICAgICAgcmV0dXJuICdrZXl3b3JkJztcbiAgICAgICAgICB9IGVsc2UgaWYgKHN0YXRlLmNvbnRleHQgPT0gNCAmJiBudW1iZXJzLnRlc3QodykpIHtcbiAgICAgICAgICAgIHJldHVybiAnbnVtYmVyJztcbiAgICAgICAgICB9XG4gICAgICAgICAgaWYgKGVycm9ycy50ZXN0KHcpKSByZXR1cm4gJ2Vycm9yJztcbiAgICAgICAgfSBlbHNlIGlmIChzdHJlYW0ubWF0Y2gobnVtYmVycykpIHtcbiAgICAgICAgICByZXR1cm4gJ251bWJlcic7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgcmV0dXJuIG51bGw7XG4gICAgICAgIH1cbiAgICAgIH0gZWxzZSBpZiAoc3RyZWFtLmVhdCgnOycpKSB7XG4gICAgICAgIHN0cmVhbS5za2lwVG9FbmQoKTtcbiAgICAgICAgcmV0dXJuICdjb21tZW50JztcbiAgICAgIH0gZWxzZSBpZiAoc3RyZWFtLmVhdCgnXCInKSkge1xuICAgICAgICB3aGlsZSAodyA9IHN0cmVhbS5uZXh0KCkpIHtcbiAgICAgICAgICBpZiAodyA9PSAnXCInKSBicmVhaztcbiAgICAgICAgICBpZiAodyA9PSAnXFxcXCcpIHN0cmVhbS5uZXh0KCk7XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuICdzdHJpbmcnO1xuICAgICAgfSBlbHNlIGlmIChzdHJlYW0uZWF0KCdcXCcnKSkge1xuICAgICAgICBpZiAoc3RyZWFtLm1hdGNoKC9cXFxcPy4nLykpIHJldHVybiAnbnVtYmVyJztcbiAgICAgIH0gZWxzZSBpZiAoc3RyZWFtLmVhdCgnLicpIHx8IHN0cmVhbS5zb2woKSAmJiBzdHJlYW0uZWF0KCcjJykpIHtcbiAgICAgICAgc3RhdGUuY29udGV4dCA9IDU7XG4gICAgICAgIGlmIChzdHJlYW0uZWF0V2hpbGUoL1xcdy8pKSByZXR1cm4gJ2RlZic7XG4gICAgICB9IGVsc2UgaWYgKHN0cmVhbS5lYXQoJyQnKSkge1xuICAgICAgICBpZiAoc3RyZWFtLmVhdFdoaWxlKC9bXFxkYS1mXS9pKSkgcmV0dXJuICdudW1iZXInO1xuICAgICAgfSBlbHNlIGlmIChzdHJlYW0uZWF0KCclJykpIHtcbiAgICAgICAgaWYgKHN0cmVhbS5lYXRXaGlsZSgvWzAxXS8pKSByZXR1cm4gJ251bWJlcic7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBzdHJlYW0ubmV4dCgpO1xuICAgICAgfVxuICAgICAgcmV0dXJuIG51bGw7XG4gICAgfVxuICB9O1xufVxuO1xuZXhwb3J0IGNvbnN0IHo4MCA9IG1rWjgwKGZhbHNlKTtcbmV4cG9ydCBjb25zdCBlejgwID0gbWtaODAodHJ1ZSk7Il0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9