"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[1020],{

/***/ 11020:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "octave": () => (/* binding */ octave)
/* harmony export */ });
function wordRegexp(words) {
  return new RegExp("^((" + words.join(")|(") + "))\\b");
}
var singleOperators = new RegExp("^[\\+\\-\\*/&|\\^~<>!@'\\\\]");
var singleDelimiters = new RegExp('^[\\(\\[\\{\\},:=;\\.]');
var doubleOperators = new RegExp("^((==)|(~=)|(<=)|(>=)|(<<)|(>>)|(\\.[\\+\\-\\*/\\^\\\\]))");
var doubleDelimiters = new RegExp("^((!=)|(\\+=)|(\\-=)|(\\*=)|(/=)|(&=)|(\\|=)|(\\^=))");
var tripleDelimiters = new RegExp("^((>>=)|(<<=))");
var expressionEnd = new RegExp("^[\\]\\)]");
var identifiers = new RegExp("^[_A-Za-z\xa1-\uffff][_A-Za-z0-9\xa1-\uffff]*");
var builtins = wordRegexp(['error', 'eval', 'function', 'abs', 'acos', 'atan', 'asin', 'cos', 'cosh', 'exp', 'log', 'prod', 'sum', 'log10', 'max', 'min', 'sign', 'sin', 'sinh', 'sqrt', 'tan', 'reshape', 'break', 'zeros', 'default', 'margin', 'round', 'ones', 'rand', 'syn', 'ceil', 'floor', 'size', 'clear', 'zeros', 'eye', 'mean', 'std', 'cov', 'det', 'eig', 'inv', 'norm', 'rank', 'trace', 'expm', 'logm', 'sqrtm', 'linspace', 'plot', 'title', 'xlabel', 'ylabel', 'legend', 'text', 'grid', 'meshgrid', 'mesh', 'num2str', 'fft', 'ifft', 'arrayfun', 'cellfun', 'input', 'fliplr', 'flipud', 'ismember']);
var keywords = wordRegexp(['return', 'case', 'switch', 'else', 'elseif', 'end', 'endif', 'endfunction', 'if', 'otherwise', 'do', 'for', 'while', 'try', 'catch', 'classdef', 'properties', 'events', 'methods', 'global', 'persistent', 'endfor', 'endwhile', 'printf', 'sprintf', 'disp', 'until', 'continue', 'pkg']);

// tokenizers
function tokenTranspose(stream, state) {
  if (!stream.sol() && stream.peek() === '\'') {
    stream.next();
    state.tokenize = tokenBase;
    return 'operator';
  }
  state.tokenize = tokenBase;
  return tokenBase(stream, state);
}
function tokenComment(stream, state) {
  if (stream.match(/^.*%}/)) {
    state.tokenize = tokenBase;
    return 'comment';
  }
  ;
  stream.skipToEnd();
  return 'comment';
}
function tokenBase(stream, state) {
  // whitespaces
  if (stream.eatSpace()) return null;

  // Handle one line Comments
  if (stream.match('%{')) {
    state.tokenize = tokenComment;
    stream.skipToEnd();
    return 'comment';
  }
  if (stream.match(/^[%#]/)) {
    stream.skipToEnd();
    return 'comment';
  }

  // Handle Number Literals
  if (stream.match(/^[0-9\.+-]/, false)) {
    if (stream.match(/^[+-]?0x[0-9a-fA-F]+[ij]?/)) {
      stream.tokenize = tokenBase;
      return 'number';
    }
    ;
    if (stream.match(/^[+-]?\d*\.\d+([EeDd][+-]?\d+)?[ij]?/)) {
      return 'number';
    }
    ;
    if (stream.match(/^[+-]?\d+([EeDd][+-]?\d+)?[ij]?/)) {
      return 'number';
    }
    ;
  }
  if (stream.match(wordRegexp(['nan', 'NaN', 'inf', 'Inf']))) {
    return 'number';
  }
  ;

  // Handle Strings
  var m = stream.match(/^"(?:[^"]|"")*("|$)/) || stream.match(/^'(?:[^']|'')*('|$)/);
  if (m) {
    return m[1] ? 'string' : "error";
  }

  // Handle words
  if (stream.match(keywords)) {
    return 'keyword';
  }
  ;
  if (stream.match(builtins)) {
    return 'builtin';
  }
  ;
  if (stream.match(identifiers)) {
    return 'variable';
  }
  ;
  if (stream.match(singleOperators) || stream.match(doubleOperators)) {
    return 'operator';
  }
  ;
  if (stream.match(singleDelimiters) || stream.match(doubleDelimiters) || stream.match(tripleDelimiters)) {
    return null;
  }
  ;
  if (stream.match(expressionEnd)) {
    state.tokenize = tokenTranspose;
    return null;
  }
  ;

  // Handle non-detected items
  stream.next();
  return 'error';
}
;
const octave = {
  name: "octave",
  startState: function () {
    return {
      tokenize: tokenBase
    };
  },
  token: function (stream, state) {
    var style = state.tokenize(stream, state);
    if (style === 'number' || style === 'variable') {
      state.tokenize = tokenTranspose;
    }
    return style;
  },
  languageData: {
    commentTokens: {
      line: "%"
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiMTAyMC5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9AY29kZW1pcnJvci9sZWdhY3ktbW9kZXMvbW9kZS9vY3RhdmUuanMiXSwic291cmNlc0NvbnRlbnQiOlsiZnVuY3Rpb24gd29yZFJlZ2V4cCh3b3Jkcykge1xuICByZXR1cm4gbmV3IFJlZ0V4cChcIl4oKFwiICsgd29yZHMuam9pbihcIil8KFwiKSArIFwiKSlcXFxcYlwiKTtcbn1cbnZhciBzaW5nbGVPcGVyYXRvcnMgPSBuZXcgUmVnRXhwKFwiXltcXFxcK1xcXFwtXFxcXCovJnxcXFxcXn48PiFAJ1xcXFxcXFxcXVwiKTtcbnZhciBzaW5nbGVEZWxpbWl0ZXJzID0gbmV3IFJlZ0V4cCgnXltcXFxcKFxcXFxbXFxcXHtcXFxcfSw6PTtcXFxcLl0nKTtcbnZhciBkb3VibGVPcGVyYXRvcnMgPSBuZXcgUmVnRXhwKFwiXigoPT0pfCh+PSl8KDw9KXwoPj0pfCg8PCl8KD4+KXwoXFxcXC5bXFxcXCtcXFxcLVxcXFwqL1xcXFxeXFxcXFxcXFxdKSlcIik7XG52YXIgZG91YmxlRGVsaW1pdGVycyA9IG5ldyBSZWdFeHAoXCJeKCghPSl8KFxcXFwrPSl8KFxcXFwtPSl8KFxcXFwqPSl8KC89KXwoJj0pfChcXFxcfD0pfChcXFxcXj0pKVwiKTtcbnZhciB0cmlwbGVEZWxpbWl0ZXJzID0gbmV3IFJlZ0V4cChcIl4oKD4+PSl8KDw8PSkpXCIpO1xudmFyIGV4cHJlc3Npb25FbmQgPSBuZXcgUmVnRXhwKFwiXltcXFxcXVxcXFwpXVwiKTtcbnZhciBpZGVudGlmaWVycyA9IG5ldyBSZWdFeHAoXCJeW19BLVphLXpcXHhhMS1cXHVmZmZmXVtfQS1aYS16MC05XFx4YTEtXFx1ZmZmZl0qXCIpO1xudmFyIGJ1aWx0aW5zID0gd29yZFJlZ2V4cChbJ2Vycm9yJywgJ2V2YWwnLCAnZnVuY3Rpb24nLCAnYWJzJywgJ2Fjb3MnLCAnYXRhbicsICdhc2luJywgJ2NvcycsICdjb3NoJywgJ2V4cCcsICdsb2cnLCAncHJvZCcsICdzdW0nLCAnbG9nMTAnLCAnbWF4JywgJ21pbicsICdzaWduJywgJ3NpbicsICdzaW5oJywgJ3NxcnQnLCAndGFuJywgJ3Jlc2hhcGUnLCAnYnJlYWsnLCAnemVyb3MnLCAnZGVmYXVsdCcsICdtYXJnaW4nLCAncm91bmQnLCAnb25lcycsICdyYW5kJywgJ3N5bicsICdjZWlsJywgJ2Zsb29yJywgJ3NpemUnLCAnY2xlYXInLCAnemVyb3MnLCAnZXllJywgJ21lYW4nLCAnc3RkJywgJ2NvdicsICdkZXQnLCAnZWlnJywgJ2ludicsICdub3JtJywgJ3JhbmsnLCAndHJhY2UnLCAnZXhwbScsICdsb2dtJywgJ3NxcnRtJywgJ2xpbnNwYWNlJywgJ3Bsb3QnLCAndGl0bGUnLCAneGxhYmVsJywgJ3lsYWJlbCcsICdsZWdlbmQnLCAndGV4dCcsICdncmlkJywgJ21lc2hncmlkJywgJ21lc2gnLCAnbnVtMnN0cicsICdmZnQnLCAnaWZmdCcsICdhcnJheWZ1bicsICdjZWxsZnVuJywgJ2lucHV0JywgJ2ZsaXBscicsICdmbGlwdWQnLCAnaXNtZW1iZXInXSk7XG52YXIga2V5d29yZHMgPSB3b3JkUmVnZXhwKFsncmV0dXJuJywgJ2Nhc2UnLCAnc3dpdGNoJywgJ2Vsc2UnLCAnZWxzZWlmJywgJ2VuZCcsICdlbmRpZicsICdlbmRmdW5jdGlvbicsICdpZicsICdvdGhlcndpc2UnLCAnZG8nLCAnZm9yJywgJ3doaWxlJywgJ3RyeScsICdjYXRjaCcsICdjbGFzc2RlZicsICdwcm9wZXJ0aWVzJywgJ2V2ZW50cycsICdtZXRob2RzJywgJ2dsb2JhbCcsICdwZXJzaXN0ZW50JywgJ2VuZGZvcicsICdlbmR3aGlsZScsICdwcmludGYnLCAnc3ByaW50ZicsICdkaXNwJywgJ3VudGlsJywgJ2NvbnRpbnVlJywgJ3BrZyddKTtcblxuLy8gdG9rZW5pemVyc1xuZnVuY3Rpb24gdG9rZW5UcmFuc3Bvc2Uoc3RyZWFtLCBzdGF0ZSkge1xuICBpZiAoIXN0cmVhbS5zb2woKSAmJiBzdHJlYW0ucGVlaygpID09PSAnXFwnJykge1xuICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgc3RhdGUudG9rZW5pemUgPSB0b2tlbkJhc2U7XG4gICAgcmV0dXJuICdvcGVyYXRvcic7XG4gIH1cbiAgc3RhdGUudG9rZW5pemUgPSB0b2tlbkJhc2U7XG4gIHJldHVybiB0b2tlbkJhc2Uoc3RyZWFtLCBzdGF0ZSk7XG59XG5mdW5jdGlvbiB0b2tlbkNvbW1lbnQoc3RyZWFtLCBzdGF0ZSkge1xuICBpZiAoc3RyZWFtLm1hdGNoKC9eLiolfS8pKSB7XG4gICAgc3RhdGUudG9rZW5pemUgPSB0b2tlbkJhc2U7XG4gICAgcmV0dXJuICdjb21tZW50JztcbiAgfVxuICA7XG4gIHN0cmVhbS5za2lwVG9FbmQoKTtcbiAgcmV0dXJuICdjb21tZW50Jztcbn1cbmZ1bmN0aW9uIHRva2VuQmFzZShzdHJlYW0sIHN0YXRlKSB7XG4gIC8vIHdoaXRlc3BhY2VzXG4gIGlmIChzdHJlYW0uZWF0U3BhY2UoKSkgcmV0dXJuIG51bGw7XG5cbiAgLy8gSGFuZGxlIG9uZSBsaW5lIENvbW1lbnRzXG4gIGlmIChzdHJlYW0ubWF0Y2goJyV7JykpIHtcbiAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQ29tbWVudDtcbiAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgcmV0dXJuICdjb21tZW50JztcbiAgfVxuICBpZiAoc3RyZWFtLm1hdGNoKC9eWyUjXS8pKSB7XG4gICAgc3RyZWFtLnNraXBUb0VuZCgpO1xuICAgIHJldHVybiAnY29tbWVudCc7XG4gIH1cblxuICAvLyBIYW5kbGUgTnVtYmVyIExpdGVyYWxzXG4gIGlmIChzdHJlYW0ubWF0Y2goL15bMC05XFwuKy1dLywgZmFsc2UpKSB7XG4gICAgaWYgKHN0cmVhbS5tYXRjaCgvXlsrLV0/MHhbMC05YS1mQS1GXStbaWpdPy8pKSB7XG4gICAgICBzdHJlYW0udG9rZW5pemUgPSB0b2tlbkJhc2U7XG4gICAgICByZXR1cm4gJ251bWJlcic7XG4gICAgfVxuICAgIDtcbiAgICBpZiAoc3RyZWFtLm1hdGNoKC9eWystXT9cXGQqXFwuXFxkKyhbRWVEZF1bKy1dP1xcZCspP1tpal0/LykpIHtcbiAgICAgIHJldHVybiAnbnVtYmVyJztcbiAgICB9XG4gICAgO1xuICAgIGlmIChzdHJlYW0ubWF0Y2goL15bKy1dP1xcZCsoW0VlRGRdWystXT9cXGQrKT9baWpdPy8pKSB7XG4gICAgICByZXR1cm4gJ251bWJlcic7XG4gICAgfVxuICAgIDtcbiAgfVxuICBpZiAoc3RyZWFtLm1hdGNoKHdvcmRSZWdleHAoWyduYW4nLCAnTmFOJywgJ2luZicsICdJbmYnXSkpKSB7XG4gICAgcmV0dXJuICdudW1iZXInO1xuICB9XG4gIDtcblxuICAvLyBIYW5kbGUgU3RyaW5nc1xuICB2YXIgbSA9IHN0cmVhbS5tYXRjaCgvXlwiKD86W15cIl18XCJcIikqKFwifCQpLykgfHwgc3RyZWFtLm1hdGNoKC9eJyg/OlteJ118JycpKignfCQpLyk7XG4gIGlmIChtKSB7XG4gICAgcmV0dXJuIG1bMV0gPyAnc3RyaW5nJyA6IFwiZXJyb3JcIjtcbiAgfVxuXG4gIC8vIEhhbmRsZSB3b3Jkc1xuICBpZiAoc3RyZWFtLm1hdGNoKGtleXdvcmRzKSkge1xuICAgIHJldHVybiAna2V5d29yZCc7XG4gIH1cbiAgO1xuICBpZiAoc3RyZWFtLm1hdGNoKGJ1aWx0aW5zKSkge1xuICAgIHJldHVybiAnYnVpbHRpbic7XG4gIH1cbiAgO1xuICBpZiAoc3RyZWFtLm1hdGNoKGlkZW50aWZpZXJzKSkge1xuICAgIHJldHVybiAndmFyaWFibGUnO1xuICB9XG4gIDtcbiAgaWYgKHN0cmVhbS5tYXRjaChzaW5nbGVPcGVyYXRvcnMpIHx8IHN0cmVhbS5tYXRjaChkb3VibGVPcGVyYXRvcnMpKSB7XG4gICAgcmV0dXJuICdvcGVyYXRvcic7XG4gIH1cbiAgO1xuICBpZiAoc3RyZWFtLm1hdGNoKHNpbmdsZURlbGltaXRlcnMpIHx8IHN0cmVhbS5tYXRjaChkb3VibGVEZWxpbWl0ZXJzKSB8fCBzdHJlYW0ubWF0Y2godHJpcGxlRGVsaW1pdGVycykpIHtcbiAgICByZXR1cm4gbnVsbDtcbiAgfVxuICA7XG4gIGlmIChzdHJlYW0ubWF0Y2goZXhwcmVzc2lvbkVuZCkpIHtcbiAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuVHJhbnNwb3NlO1xuICAgIHJldHVybiBudWxsO1xuICB9XG4gIDtcblxuICAvLyBIYW5kbGUgbm9uLWRldGVjdGVkIGl0ZW1zXG4gIHN0cmVhbS5uZXh0KCk7XG4gIHJldHVybiAnZXJyb3InO1xufVxuO1xuZXhwb3J0IGNvbnN0IG9jdGF2ZSA9IHtcbiAgbmFtZTogXCJvY3RhdmVcIixcbiAgc3RhcnRTdGF0ZTogZnVuY3Rpb24gKCkge1xuICAgIHJldHVybiB7XG4gICAgICB0b2tlbml6ZTogdG9rZW5CYXNlXG4gICAgfTtcbiAgfSxcbiAgdG9rZW46IGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgdmFyIHN0eWxlID0gc3RhdGUudG9rZW5pemUoc3RyZWFtLCBzdGF0ZSk7XG4gICAgaWYgKHN0eWxlID09PSAnbnVtYmVyJyB8fCBzdHlsZSA9PT0gJ3ZhcmlhYmxlJykge1xuICAgICAgc3RhdGUudG9rZW5pemUgPSB0b2tlblRyYW5zcG9zZTtcbiAgICB9XG4gICAgcmV0dXJuIHN0eWxlO1xuICB9LFxuICBsYW5ndWFnZURhdGE6IHtcbiAgICBjb21tZW50VG9rZW5zOiB7XG4gICAgICBsaW5lOiBcIiVcIlxuICAgIH1cbiAgfVxufTsiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=