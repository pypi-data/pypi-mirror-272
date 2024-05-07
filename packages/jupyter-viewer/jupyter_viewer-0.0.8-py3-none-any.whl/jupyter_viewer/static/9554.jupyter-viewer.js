"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[9554],{

/***/ 89554:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "mathematica": () => (/* binding */ mathematica)
/* harmony export */ });
// used pattern building blocks
var Identifier = '[a-zA-Z\\$][a-zA-Z0-9\\$]*';
var pBase = "(?:\\d+)";
var pFloat = "(?:\\.\\d+|\\d+\\.\\d*|\\d+)";
var pFloatBase = "(?:\\.\\w+|\\w+\\.\\w*|\\w+)";
var pPrecision = "(?:`(?:`?" + pFloat + ")?)";

// regular expressions
var reBaseForm = new RegExp('(?:' + pBase + '(?:\\^\\^' + pFloatBase + pPrecision + '?(?:\\*\\^[+-]?\\d+)?))');
var reFloatForm = new RegExp('(?:' + pFloat + pPrecision + '?(?:\\*\\^[+-]?\\d+)?)');
var reIdInContext = new RegExp('(?:`?)(?:' + Identifier + ')(?:`(?:' + Identifier + '))*(?:`?)');
function tokenBase(stream, state) {
  var ch;

  // get next character
  ch = stream.next();

  // string
  if (ch === '"') {
    state.tokenize = tokenString;
    return state.tokenize(stream, state);
  }

  // comment
  if (ch === '(') {
    if (stream.eat('*')) {
      state.commentLevel++;
      state.tokenize = tokenComment;
      return state.tokenize(stream, state);
    }
  }

  // go back one character
  stream.backUp(1);

  // look for numbers
  // Numbers in a baseform
  if (stream.match(reBaseForm, true, false)) {
    return 'number';
  }

  // Mathematica numbers. Floats (1.2, .2, 1.) can have optionally a precision (`float) or an accuracy definition
  // (``float). Note: while 1.2` is possible 1.2`` is not. At the end an exponent (float*^+12) can follow.
  if (stream.match(reFloatForm, true, false)) {
    return 'number';
  }

  /* In[23] and Out[34] */
  if (stream.match(/(?:In|Out)\[[0-9]*\]/, true, false)) {
    return 'atom';
  }

  // usage
  if (stream.match(/([a-zA-Z\$][a-zA-Z0-9\$]*(?:`[a-zA-Z0-9\$]+)*::usage)/, true, false)) {
    return 'meta';
  }

  // message
  if (stream.match(/([a-zA-Z\$][a-zA-Z0-9\$]*(?:`[a-zA-Z0-9\$]+)*::[a-zA-Z\$][a-zA-Z0-9\$]*):?/, true, false)) {
    return 'string.special';
  }

  // this makes a look-ahead match for something like variable:{_Integer}
  // the match is then forwarded to the mma-patterns tokenizer.
  if (stream.match(/([a-zA-Z\$][a-zA-Z0-9\$]*\s*:)(?:(?:[a-zA-Z\$][a-zA-Z0-9\$]*)|(?:[^:=>~@\^\&\*\)\[\]'\?,\|])).*/, true, false)) {
    return 'variableName.special';
  }

  // catch variables which are used together with Blank (_), BlankSequence (__) or BlankNullSequence (___)
  // Cannot start with a number, but can have numbers at any other position. Examples
  // blub__Integer, a1_, b34_Integer32
  if (stream.match(/[a-zA-Z\$][a-zA-Z0-9\$]*_+[a-zA-Z\$][a-zA-Z0-9\$]*/, true, false)) {
    return 'variableName.special';
  }
  if (stream.match(/[a-zA-Z\$][a-zA-Z0-9\$]*_+/, true, false)) {
    return 'variableName.special';
  }
  if (stream.match(/_+[a-zA-Z\$][a-zA-Z0-9\$]*/, true, false)) {
    return 'variableName.special';
  }

  // Named characters in Mathematica, like \[Gamma].
  if (stream.match(/\\\[[a-zA-Z\$][a-zA-Z0-9\$]*\]/, true, false)) {
    return 'character';
  }

  // Match all braces separately
  if (stream.match(/(?:\[|\]|{|}|\(|\))/, true, false)) {
    return 'bracket';
  }

  // Catch Slots (#, ##, #3, ##9 and the V10 named slots #name). I have never seen someone using more than one digit after #, so we match
  // only one.
  if (stream.match(/(?:#[a-zA-Z\$][a-zA-Z0-9\$]*|#+[0-9]?)/, true, false)) {
    return 'variableName.constant';
  }

  // Literals like variables, keywords, functions
  if (stream.match(reIdInContext, true, false)) {
    return 'keyword';
  }

  // operators. Note that operators like @@ or /; are matched separately for each symbol.
  if (stream.match(/(?:\\|\+|\-|\*|\/|,|;|\.|:|@|~|=|>|<|&|\||_|`|'|\^|\?|!|%)/, true, false)) {
    return 'operator';
  }

  // everything else is an error
  stream.next(); // advance the stream.
  return 'error';
}
function tokenString(stream, state) {
  var next,
    end = false,
    escaped = false;
  while ((next = stream.next()) != null) {
    if (next === '"' && !escaped) {
      end = true;
      break;
    }
    escaped = !escaped && next === '\\';
  }
  if (end && !escaped) {
    state.tokenize = tokenBase;
  }
  return 'string';
}
;
function tokenComment(stream, state) {
  var prev, next;
  while (state.commentLevel > 0 && (next = stream.next()) != null) {
    if (prev === '(' && next === '*') state.commentLevel++;
    if (prev === '*' && next === ')') state.commentLevel--;
    prev = next;
  }
  if (state.commentLevel <= 0) {
    state.tokenize = tokenBase;
  }
  return 'comment';
}
const mathematica = {
  name: "mathematica",
  startState: function () {
    return {
      tokenize: tokenBase,
      commentLevel: 0
    };
  },
  token: function (stream, state) {
    if (stream.eatSpace()) return null;
    return state.tokenize(stream, state);
  },
  languageData: {
    commentTokens: {
      block: {
        open: "(*",
        close: "*)"
      }
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiOTU1NC5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGNvZGVtaXJyb3IvbGVnYWN5LW1vZGVzL21vZGUvbWF0aGVtYXRpY2EuanMiXSwic291cmNlc0NvbnRlbnQiOlsiLy8gdXNlZCBwYXR0ZXJuIGJ1aWxkaW5nIGJsb2Nrc1xudmFyIElkZW50aWZpZXIgPSAnW2EtekEtWlxcXFwkXVthLXpBLVowLTlcXFxcJF0qJztcbnZhciBwQmFzZSA9IFwiKD86XFxcXGQrKVwiO1xudmFyIHBGbG9hdCA9IFwiKD86XFxcXC5cXFxcZCt8XFxcXGQrXFxcXC5cXFxcZCp8XFxcXGQrKVwiO1xudmFyIHBGbG9hdEJhc2UgPSBcIig/OlxcXFwuXFxcXHcrfFxcXFx3K1xcXFwuXFxcXHcqfFxcXFx3KylcIjtcbnZhciBwUHJlY2lzaW9uID0gXCIoPzpgKD86YD9cIiArIHBGbG9hdCArIFwiKT8pXCI7XG5cbi8vIHJlZ3VsYXIgZXhwcmVzc2lvbnNcbnZhciByZUJhc2VGb3JtID0gbmV3IFJlZ0V4cCgnKD86JyArIHBCYXNlICsgJyg/OlxcXFxeXFxcXF4nICsgcEZsb2F0QmFzZSArIHBQcmVjaXNpb24gKyAnPyg/OlxcXFwqXFxcXF5bKy1dP1xcXFxkKyk/KSknKTtcbnZhciByZUZsb2F0Rm9ybSA9IG5ldyBSZWdFeHAoJyg/OicgKyBwRmxvYXQgKyBwUHJlY2lzaW9uICsgJz8oPzpcXFxcKlxcXFxeWystXT9cXFxcZCspPyknKTtcbnZhciByZUlkSW5Db250ZXh0ID0gbmV3IFJlZ0V4cCgnKD86YD8pKD86JyArIElkZW50aWZpZXIgKyAnKSg/OmAoPzonICsgSWRlbnRpZmllciArICcpKSooPzpgPyknKTtcbmZ1bmN0aW9uIHRva2VuQmFzZShzdHJlYW0sIHN0YXRlKSB7XG4gIHZhciBjaDtcblxuICAvLyBnZXQgbmV4dCBjaGFyYWN0ZXJcbiAgY2ggPSBzdHJlYW0ubmV4dCgpO1xuXG4gIC8vIHN0cmluZ1xuICBpZiAoY2ggPT09ICdcIicpIHtcbiAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuU3RyaW5nO1xuICAgIHJldHVybiBzdGF0ZS50b2tlbml6ZShzdHJlYW0sIHN0YXRlKTtcbiAgfVxuXG4gIC8vIGNvbW1lbnRcbiAgaWYgKGNoID09PSAnKCcpIHtcbiAgICBpZiAoc3RyZWFtLmVhdCgnKicpKSB7XG4gICAgICBzdGF0ZS5jb21tZW50TGV2ZWwrKztcbiAgICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5Db21tZW50O1xuICAgICAgcmV0dXJuIHN0YXRlLnRva2VuaXplKHN0cmVhbSwgc3RhdGUpO1xuICAgIH1cbiAgfVxuXG4gIC8vIGdvIGJhY2sgb25lIGNoYXJhY3RlclxuICBzdHJlYW0uYmFja1VwKDEpO1xuXG4gIC8vIGxvb2sgZm9yIG51bWJlcnNcbiAgLy8gTnVtYmVycyBpbiBhIGJhc2Vmb3JtXG4gIGlmIChzdHJlYW0ubWF0Y2gocmVCYXNlRm9ybSwgdHJ1ZSwgZmFsc2UpKSB7XG4gICAgcmV0dXJuICdudW1iZXInO1xuICB9XG5cbiAgLy8gTWF0aGVtYXRpY2EgbnVtYmVycy4gRmxvYXRzICgxLjIsIC4yLCAxLikgY2FuIGhhdmUgb3B0aW9uYWxseSBhIHByZWNpc2lvbiAoYGZsb2F0KSBvciBhbiBhY2N1cmFjeSBkZWZpbml0aW9uXG4gIC8vIChgYGZsb2F0KS4gTm90ZTogd2hpbGUgMS4yYCBpcyBwb3NzaWJsZSAxLjJgYCBpcyBub3QuIEF0IHRoZSBlbmQgYW4gZXhwb25lbnQgKGZsb2F0Kl4rMTIpIGNhbiBmb2xsb3cuXG4gIGlmIChzdHJlYW0ubWF0Y2gocmVGbG9hdEZvcm0sIHRydWUsIGZhbHNlKSkge1xuICAgIHJldHVybiAnbnVtYmVyJztcbiAgfVxuXG4gIC8qIEluWzIzXSBhbmQgT3V0WzM0XSAqL1xuICBpZiAoc3RyZWFtLm1hdGNoKC8oPzpJbnxPdXQpXFxbWzAtOV0qXFxdLywgdHJ1ZSwgZmFsc2UpKSB7XG4gICAgcmV0dXJuICdhdG9tJztcbiAgfVxuXG4gIC8vIHVzYWdlXG4gIGlmIChzdHJlYW0ubWF0Y2goLyhbYS16QS1aXFwkXVthLXpBLVowLTlcXCRdKig/OmBbYS16QS1aMC05XFwkXSspKjo6dXNhZ2UpLywgdHJ1ZSwgZmFsc2UpKSB7XG4gICAgcmV0dXJuICdtZXRhJztcbiAgfVxuXG4gIC8vIG1lc3NhZ2VcbiAgaWYgKHN0cmVhbS5tYXRjaCgvKFthLXpBLVpcXCRdW2EtekEtWjAtOVxcJF0qKD86YFthLXpBLVowLTlcXCRdKykqOjpbYS16QS1aXFwkXVthLXpBLVowLTlcXCRdKik6Py8sIHRydWUsIGZhbHNlKSkge1xuICAgIHJldHVybiAnc3RyaW5nLnNwZWNpYWwnO1xuICB9XG5cbiAgLy8gdGhpcyBtYWtlcyBhIGxvb2stYWhlYWQgbWF0Y2ggZm9yIHNvbWV0aGluZyBsaWtlIHZhcmlhYmxlOntfSW50ZWdlcn1cbiAgLy8gdGhlIG1hdGNoIGlzIHRoZW4gZm9yd2FyZGVkIHRvIHRoZSBtbWEtcGF0dGVybnMgdG9rZW5pemVyLlxuICBpZiAoc3RyZWFtLm1hdGNoKC8oW2EtekEtWlxcJF1bYS16QS1aMC05XFwkXSpcXHMqOikoPzooPzpbYS16QS1aXFwkXVthLXpBLVowLTlcXCRdKil8KD86W146PT5+QFxcXlxcJlxcKlxcKVxcW1xcXSdcXD8sXFx8XSkpLiovLCB0cnVlLCBmYWxzZSkpIHtcbiAgICByZXR1cm4gJ3ZhcmlhYmxlTmFtZS5zcGVjaWFsJztcbiAgfVxuXG4gIC8vIGNhdGNoIHZhcmlhYmxlcyB3aGljaCBhcmUgdXNlZCB0b2dldGhlciB3aXRoIEJsYW5rIChfKSwgQmxhbmtTZXF1ZW5jZSAoX18pIG9yIEJsYW5rTnVsbFNlcXVlbmNlIChfX18pXG4gIC8vIENhbm5vdCBzdGFydCB3aXRoIGEgbnVtYmVyLCBidXQgY2FuIGhhdmUgbnVtYmVycyBhdCBhbnkgb3RoZXIgcG9zaXRpb24uIEV4YW1wbGVzXG4gIC8vIGJsdWJfX0ludGVnZXIsIGExXywgYjM0X0ludGVnZXIzMlxuICBpZiAoc3RyZWFtLm1hdGNoKC9bYS16QS1aXFwkXVthLXpBLVowLTlcXCRdKl8rW2EtekEtWlxcJF1bYS16QS1aMC05XFwkXSovLCB0cnVlLCBmYWxzZSkpIHtcbiAgICByZXR1cm4gJ3ZhcmlhYmxlTmFtZS5zcGVjaWFsJztcbiAgfVxuICBpZiAoc3RyZWFtLm1hdGNoKC9bYS16QS1aXFwkXVthLXpBLVowLTlcXCRdKl8rLywgdHJ1ZSwgZmFsc2UpKSB7XG4gICAgcmV0dXJuICd2YXJpYWJsZU5hbWUuc3BlY2lhbCc7XG4gIH1cbiAgaWYgKHN0cmVhbS5tYXRjaCgvXytbYS16QS1aXFwkXVthLXpBLVowLTlcXCRdKi8sIHRydWUsIGZhbHNlKSkge1xuICAgIHJldHVybiAndmFyaWFibGVOYW1lLnNwZWNpYWwnO1xuICB9XG5cbiAgLy8gTmFtZWQgY2hhcmFjdGVycyBpbiBNYXRoZW1hdGljYSwgbGlrZSBcXFtHYW1tYV0uXG4gIGlmIChzdHJlYW0ubWF0Y2goL1xcXFxcXFtbYS16QS1aXFwkXVthLXpBLVowLTlcXCRdKlxcXS8sIHRydWUsIGZhbHNlKSkge1xuICAgIHJldHVybiAnY2hhcmFjdGVyJztcbiAgfVxuXG4gIC8vIE1hdGNoIGFsbCBicmFjZXMgc2VwYXJhdGVseVxuICBpZiAoc3RyZWFtLm1hdGNoKC8oPzpcXFt8XFxdfHt8fXxcXCh8XFwpKS8sIHRydWUsIGZhbHNlKSkge1xuICAgIHJldHVybiAnYnJhY2tldCc7XG4gIH1cblxuICAvLyBDYXRjaCBTbG90cyAoIywgIyMsICMzLCAjIzkgYW5kIHRoZSBWMTAgbmFtZWQgc2xvdHMgI25hbWUpLiBJIGhhdmUgbmV2ZXIgc2VlbiBzb21lb25lIHVzaW5nIG1vcmUgdGhhbiBvbmUgZGlnaXQgYWZ0ZXIgIywgc28gd2UgbWF0Y2hcbiAgLy8gb25seSBvbmUuXG4gIGlmIChzdHJlYW0ubWF0Y2goLyg/OiNbYS16QS1aXFwkXVthLXpBLVowLTlcXCRdKnwjK1swLTldPykvLCB0cnVlLCBmYWxzZSkpIHtcbiAgICByZXR1cm4gJ3ZhcmlhYmxlTmFtZS5jb25zdGFudCc7XG4gIH1cblxuICAvLyBMaXRlcmFscyBsaWtlIHZhcmlhYmxlcywga2V5d29yZHMsIGZ1bmN0aW9uc1xuICBpZiAoc3RyZWFtLm1hdGNoKHJlSWRJbkNvbnRleHQsIHRydWUsIGZhbHNlKSkge1xuICAgIHJldHVybiAna2V5d29yZCc7XG4gIH1cblxuICAvLyBvcGVyYXRvcnMuIE5vdGUgdGhhdCBvcGVyYXRvcnMgbGlrZSBAQCBvciAvOyBhcmUgbWF0Y2hlZCBzZXBhcmF0ZWx5IGZvciBlYWNoIHN5bWJvbC5cbiAgaWYgKHN0cmVhbS5tYXRjaCgvKD86XFxcXHxcXCt8XFwtfFxcKnxcXC98LHw7fFxcLnw6fEB8fnw9fD58PHwmfFxcfHxffGB8J3xcXF58XFw/fCF8JSkvLCB0cnVlLCBmYWxzZSkpIHtcbiAgICByZXR1cm4gJ29wZXJhdG9yJztcbiAgfVxuXG4gIC8vIGV2ZXJ5dGhpbmcgZWxzZSBpcyBhbiBlcnJvclxuICBzdHJlYW0ubmV4dCgpOyAvLyBhZHZhbmNlIHRoZSBzdHJlYW0uXG4gIHJldHVybiAnZXJyb3InO1xufVxuZnVuY3Rpb24gdG9rZW5TdHJpbmcoc3RyZWFtLCBzdGF0ZSkge1xuICB2YXIgbmV4dCxcbiAgICBlbmQgPSBmYWxzZSxcbiAgICBlc2NhcGVkID0gZmFsc2U7XG4gIHdoaWxlICgobmV4dCA9IHN0cmVhbS5uZXh0KCkpICE9IG51bGwpIHtcbiAgICBpZiAobmV4dCA9PT0gJ1wiJyAmJiAhZXNjYXBlZCkge1xuICAgICAgZW5kID0gdHJ1ZTtcbiAgICAgIGJyZWFrO1xuICAgIH1cbiAgICBlc2NhcGVkID0gIWVzY2FwZWQgJiYgbmV4dCA9PT0gJ1xcXFwnO1xuICB9XG4gIGlmIChlbmQgJiYgIWVzY2FwZWQpIHtcbiAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQmFzZTtcbiAgfVxuICByZXR1cm4gJ3N0cmluZyc7XG59XG47XG5mdW5jdGlvbiB0b2tlbkNvbW1lbnQoc3RyZWFtLCBzdGF0ZSkge1xuICB2YXIgcHJldiwgbmV4dDtcbiAgd2hpbGUgKHN0YXRlLmNvbW1lbnRMZXZlbCA+IDAgJiYgKG5leHQgPSBzdHJlYW0ubmV4dCgpKSAhPSBudWxsKSB7XG4gICAgaWYgKHByZXYgPT09ICcoJyAmJiBuZXh0ID09PSAnKicpIHN0YXRlLmNvbW1lbnRMZXZlbCsrO1xuICAgIGlmIChwcmV2ID09PSAnKicgJiYgbmV4dCA9PT0gJyknKSBzdGF0ZS5jb21tZW50TGV2ZWwtLTtcbiAgICBwcmV2ID0gbmV4dDtcbiAgfVxuICBpZiAoc3RhdGUuY29tbWVudExldmVsIDw9IDApIHtcbiAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQmFzZTtcbiAgfVxuICByZXR1cm4gJ2NvbW1lbnQnO1xufVxuZXhwb3J0IGNvbnN0IG1hdGhlbWF0aWNhID0ge1xuICBuYW1lOiBcIm1hdGhlbWF0aWNhXCIsXG4gIHN0YXJ0U3RhdGU6IGZ1bmN0aW9uICgpIHtcbiAgICByZXR1cm4ge1xuICAgICAgdG9rZW5pemU6IHRva2VuQmFzZSxcbiAgICAgIGNvbW1lbnRMZXZlbDogMFxuICAgIH07XG4gIH0sXG4gIHRva2VuOiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIGlmIChzdHJlYW0uZWF0U3BhY2UoKSkgcmV0dXJuIG51bGw7XG4gICAgcmV0dXJuIHN0YXRlLnRva2VuaXplKHN0cmVhbSwgc3RhdGUpO1xuICB9LFxuICBsYW5ndWFnZURhdGE6IHtcbiAgICBjb21tZW50VG9rZW5zOiB7XG4gICAgICBibG9jazoge1xuICAgICAgICBvcGVuOiBcIigqXCIsXG4gICAgICAgIGNsb3NlOiBcIiopXCJcbiAgICAgIH1cbiAgICB9XG4gIH1cbn07Il0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9