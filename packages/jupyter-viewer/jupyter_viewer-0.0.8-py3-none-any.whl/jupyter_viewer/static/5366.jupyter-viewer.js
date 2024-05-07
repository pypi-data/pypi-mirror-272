"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[5366],{

/***/ 95366:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "yacas": () => (/* binding */ yacas)
/* harmony export */ });
function words(str) {
  var obj = {},
    words = str.split(" ");
  for (var i = 0; i < words.length; ++i) obj[words[i]] = true;
  return obj;
}
var bodiedOps = words("Assert BackQuote D Defun Deriv For ForEach FromFile " + "FromString Function Integrate InverseTaylor Limit " + "LocalSymbols Macro MacroRule MacroRulePattern " + "NIntegrate Rule RulePattern Subst TD TExplicitSum " + "TSum Taylor Taylor1 Taylor2 Taylor3 ToFile " + "ToStdout ToString TraceRule Until While");

// patterns
var pFloatForm = "(?:(?:\\.\\d+|\\d+\\.\\d*|\\d+)(?:[eE][+-]?\\d+)?)";
var pIdentifier = "(?:[a-zA-Z\\$'][a-zA-Z0-9\\$']*)";

// regular expressions
var reFloatForm = new RegExp(pFloatForm);
var reIdentifier = new RegExp(pIdentifier);
var rePattern = new RegExp(pIdentifier + "?_" + pIdentifier);
var reFunctionLike = new RegExp(pIdentifier + "\\s*\\(");
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
  if (ch === '/') {
    if (stream.eat('*')) {
      state.tokenize = tokenComment;
      return state.tokenize(stream, state);
    }
    if (stream.eat("/")) {
      stream.skipToEnd();
      return "comment";
    }
  }

  // go back one character
  stream.backUp(1);

  // update scope info
  var m = stream.match(/^(\w+)\s*\(/, false);
  if (m !== null && bodiedOps.hasOwnProperty(m[1])) state.scopes.push('bodied');
  var scope = currentScope(state);
  if (scope === 'bodied' && ch === '[') state.scopes.pop();
  if (ch === '[' || ch === '{' || ch === '(') state.scopes.push(ch);
  scope = currentScope(state);
  if (scope === '[' && ch === ']' || scope === '{' && ch === '}' || scope === '(' && ch === ')') state.scopes.pop();
  if (ch === ';') {
    while (scope === 'bodied') {
      state.scopes.pop();
      scope = currentScope(state);
    }
  }

  // look for ordered rules
  if (stream.match(/\d+ *#/, true, false)) {
    return 'qualifier';
  }

  // look for numbers
  if (stream.match(reFloatForm, true, false)) {
    return 'number';
  }

  // look for placeholders
  if (stream.match(rePattern, true, false)) {
    return 'variableName.special';
  }

  // match all braces separately
  if (stream.match(/(?:\[|\]|{|}|\(|\))/, true, false)) {
    return 'bracket';
  }

  // literals looking like function calls
  if (stream.match(reFunctionLike, true, false)) {
    stream.backUp(1);
    return 'variableName.function';
  }

  // all other identifiers
  if (stream.match(reIdentifier, true, false)) {
    return 'variable';
  }

  // operators; note that operators like @@ or /; are matched separately for each symbol.
  if (stream.match(/(?:\\|\+|\-|\*|\/|,|;|\.|:|@|~|=|>|<|&|\||_|`|'|\^|\?|!|%|#)/, true, false)) {
    return 'operator';
  }

  // everything else is an error
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
  while ((next = stream.next()) != null) {
    if (prev === '*' && next === '/') {
      state.tokenize = tokenBase;
      break;
    }
    prev = next;
  }
  return 'comment';
}
function currentScope(state) {
  var scope = null;
  if (state.scopes.length > 0) scope = state.scopes[state.scopes.length - 1];
  return scope;
}
const yacas = {
  name: "yacas",
  startState: function () {
    return {
      tokenize: tokenBase,
      scopes: []
    };
  },
  token: function (stream, state) {
    if (stream.eatSpace()) return null;
    return state.tokenize(stream, state);
  },
  indent: function (state, textAfter, cx) {
    if (state.tokenize !== tokenBase && state.tokenize !== null) return null;
    var delta = 0;
    if (textAfter === ']' || textAfter === '];' || textAfter === '}' || textAfter === '};' || textAfter === ');') delta = -1;
    return (state.scopes.length + delta) * cx.unit;
  },
  languageData: {
    electricInput: /[{}\[\]()\;]/,
    commentTokens: {
      line: "//",
      block: {
        open: "/*",
        close: "*/"
      }
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNTM2Ni5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL0Bjb2RlbWlycm9yL2xlZ2FjeS1tb2Rlcy9tb2RlL3lhY2FzLmpzIl0sInNvdXJjZXNDb250ZW50IjpbImZ1bmN0aW9uIHdvcmRzKHN0cikge1xuICB2YXIgb2JqID0ge30sXG4gICAgd29yZHMgPSBzdHIuc3BsaXQoXCIgXCIpO1xuICBmb3IgKHZhciBpID0gMDsgaSA8IHdvcmRzLmxlbmd0aDsgKytpKSBvYmpbd29yZHNbaV1dID0gdHJ1ZTtcbiAgcmV0dXJuIG9iajtcbn1cbnZhciBib2RpZWRPcHMgPSB3b3JkcyhcIkFzc2VydCBCYWNrUXVvdGUgRCBEZWZ1biBEZXJpdiBGb3IgRm9yRWFjaCBGcm9tRmlsZSBcIiArIFwiRnJvbVN0cmluZyBGdW5jdGlvbiBJbnRlZ3JhdGUgSW52ZXJzZVRheWxvciBMaW1pdCBcIiArIFwiTG9jYWxTeW1ib2xzIE1hY3JvIE1hY3JvUnVsZSBNYWNyb1J1bGVQYXR0ZXJuIFwiICsgXCJOSW50ZWdyYXRlIFJ1bGUgUnVsZVBhdHRlcm4gU3Vic3QgVEQgVEV4cGxpY2l0U3VtIFwiICsgXCJUU3VtIFRheWxvciBUYXlsb3IxIFRheWxvcjIgVGF5bG9yMyBUb0ZpbGUgXCIgKyBcIlRvU3Rkb3V0IFRvU3RyaW5nIFRyYWNlUnVsZSBVbnRpbCBXaGlsZVwiKTtcblxuLy8gcGF0dGVybnNcbnZhciBwRmxvYXRGb3JtID0gXCIoPzooPzpcXFxcLlxcXFxkK3xcXFxcZCtcXFxcLlxcXFxkKnxcXFxcZCspKD86W2VFXVsrLV0/XFxcXGQrKT8pXCI7XG52YXIgcElkZW50aWZpZXIgPSBcIig/OlthLXpBLVpcXFxcJCddW2EtekEtWjAtOVxcXFwkJ10qKVwiO1xuXG4vLyByZWd1bGFyIGV4cHJlc3Npb25zXG52YXIgcmVGbG9hdEZvcm0gPSBuZXcgUmVnRXhwKHBGbG9hdEZvcm0pO1xudmFyIHJlSWRlbnRpZmllciA9IG5ldyBSZWdFeHAocElkZW50aWZpZXIpO1xudmFyIHJlUGF0dGVybiA9IG5ldyBSZWdFeHAocElkZW50aWZpZXIgKyBcIj9fXCIgKyBwSWRlbnRpZmllcik7XG52YXIgcmVGdW5jdGlvbkxpa2UgPSBuZXcgUmVnRXhwKHBJZGVudGlmaWVyICsgXCJcXFxccypcXFxcKFwiKTtcbmZ1bmN0aW9uIHRva2VuQmFzZShzdHJlYW0sIHN0YXRlKSB7XG4gIHZhciBjaDtcblxuICAvLyBnZXQgbmV4dCBjaGFyYWN0ZXJcbiAgY2ggPSBzdHJlYW0ubmV4dCgpO1xuXG4gIC8vIHN0cmluZ1xuICBpZiAoY2ggPT09ICdcIicpIHtcbiAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuU3RyaW5nO1xuICAgIHJldHVybiBzdGF0ZS50b2tlbml6ZShzdHJlYW0sIHN0YXRlKTtcbiAgfVxuXG4gIC8vIGNvbW1lbnRcbiAgaWYgKGNoID09PSAnLycpIHtcbiAgICBpZiAoc3RyZWFtLmVhdCgnKicpKSB7XG4gICAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQ29tbWVudDtcbiAgICAgIHJldHVybiBzdGF0ZS50b2tlbml6ZShzdHJlYW0sIHN0YXRlKTtcbiAgICB9XG4gICAgaWYgKHN0cmVhbS5lYXQoXCIvXCIpKSB7XG4gICAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgICByZXR1cm4gXCJjb21tZW50XCI7XG4gICAgfVxuICB9XG5cbiAgLy8gZ28gYmFjayBvbmUgY2hhcmFjdGVyXG4gIHN0cmVhbS5iYWNrVXAoMSk7XG5cbiAgLy8gdXBkYXRlIHNjb3BlIGluZm9cbiAgdmFyIG0gPSBzdHJlYW0ubWF0Y2goL14oXFx3KylcXHMqXFwoLywgZmFsc2UpO1xuICBpZiAobSAhPT0gbnVsbCAmJiBib2RpZWRPcHMuaGFzT3duUHJvcGVydHkobVsxXSkpIHN0YXRlLnNjb3Blcy5wdXNoKCdib2RpZWQnKTtcbiAgdmFyIHNjb3BlID0gY3VycmVudFNjb3BlKHN0YXRlKTtcbiAgaWYgKHNjb3BlID09PSAnYm9kaWVkJyAmJiBjaCA9PT0gJ1snKSBzdGF0ZS5zY29wZXMucG9wKCk7XG4gIGlmIChjaCA9PT0gJ1snIHx8IGNoID09PSAneycgfHwgY2ggPT09ICcoJykgc3RhdGUuc2NvcGVzLnB1c2goY2gpO1xuICBzY29wZSA9IGN1cnJlbnRTY29wZShzdGF0ZSk7XG4gIGlmIChzY29wZSA9PT0gJ1snICYmIGNoID09PSAnXScgfHwgc2NvcGUgPT09ICd7JyAmJiBjaCA9PT0gJ30nIHx8IHNjb3BlID09PSAnKCcgJiYgY2ggPT09ICcpJykgc3RhdGUuc2NvcGVzLnBvcCgpO1xuICBpZiAoY2ggPT09ICc7Jykge1xuICAgIHdoaWxlIChzY29wZSA9PT0gJ2JvZGllZCcpIHtcbiAgICAgIHN0YXRlLnNjb3Blcy5wb3AoKTtcbiAgICAgIHNjb3BlID0gY3VycmVudFNjb3BlKHN0YXRlKTtcbiAgICB9XG4gIH1cblxuICAvLyBsb29rIGZvciBvcmRlcmVkIHJ1bGVzXG4gIGlmIChzdHJlYW0ubWF0Y2goL1xcZCsgKiMvLCB0cnVlLCBmYWxzZSkpIHtcbiAgICByZXR1cm4gJ3F1YWxpZmllcic7XG4gIH1cblxuICAvLyBsb29rIGZvciBudW1iZXJzXG4gIGlmIChzdHJlYW0ubWF0Y2gocmVGbG9hdEZvcm0sIHRydWUsIGZhbHNlKSkge1xuICAgIHJldHVybiAnbnVtYmVyJztcbiAgfVxuXG4gIC8vIGxvb2sgZm9yIHBsYWNlaG9sZGVyc1xuICBpZiAoc3RyZWFtLm1hdGNoKHJlUGF0dGVybiwgdHJ1ZSwgZmFsc2UpKSB7XG4gICAgcmV0dXJuICd2YXJpYWJsZU5hbWUuc3BlY2lhbCc7XG4gIH1cblxuICAvLyBtYXRjaCBhbGwgYnJhY2VzIHNlcGFyYXRlbHlcbiAgaWYgKHN0cmVhbS5tYXRjaCgvKD86XFxbfFxcXXx7fH18XFwofFxcKSkvLCB0cnVlLCBmYWxzZSkpIHtcbiAgICByZXR1cm4gJ2JyYWNrZXQnO1xuICB9XG5cbiAgLy8gbGl0ZXJhbHMgbG9va2luZyBsaWtlIGZ1bmN0aW9uIGNhbGxzXG4gIGlmIChzdHJlYW0ubWF0Y2gocmVGdW5jdGlvbkxpa2UsIHRydWUsIGZhbHNlKSkge1xuICAgIHN0cmVhbS5iYWNrVXAoMSk7XG4gICAgcmV0dXJuICd2YXJpYWJsZU5hbWUuZnVuY3Rpb24nO1xuICB9XG5cbiAgLy8gYWxsIG90aGVyIGlkZW50aWZpZXJzXG4gIGlmIChzdHJlYW0ubWF0Y2gocmVJZGVudGlmaWVyLCB0cnVlLCBmYWxzZSkpIHtcbiAgICByZXR1cm4gJ3ZhcmlhYmxlJztcbiAgfVxuXG4gIC8vIG9wZXJhdG9yczsgbm90ZSB0aGF0IG9wZXJhdG9ycyBsaWtlIEBAIG9yIC87IGFyZSBtYXRjaGVkIHNlcGFyYXRlbHkgZm9yIGVhY2ggc3ltYm9sLlxuICBpZiAoc3RyZWFtLm1hdGNoKC8oPzpcXFxcfFxcK3xcXC18XFwqfFxcL3wsfDt8XFwufDp8QHx+fD18Pnw8fCZ8XFx8fF98YHwnfFxcXnxcXD98IXwlfCMpLywgdHJ1ZSwgZmFsc2UpKSB7XG4gICAgcmV0dXJuICdvcGVyYXRvcic7XG4gIH1cblxuICAvLyBldmVyeXRoaW5nIGVsc2UgaXMgYW4gZXJyb3JcbiAgcmV0dXJuICdlcnJvcic7XG59XG5mdW5jdGlvbiB0b2tlblN0cmluZyhzdHJlYW0sIHN0YXRlKSB7XG4gIHZhciBuZXh0LFxuICAgIGVuZCA9IGZhbHNlLFxuICAgIGVzY2FwZWQgPSBmYWxzZTtcbiAgd2hpbGUgKChuZXh0ID0gc3RyZWFtLm5leHQoKSkgIT0gbnVsbCkge1xuICAgIGlmIChuZXh0ID09PSAnXCInICYmICFlc2NhcGVkKSB7XG4gICAgICBlbmQgPSB0cnVlO1xuICAgICAgYnJlYWs7XG4gICAgfVxuICAgIGVzY2FwZWQgPSAhZXNjYXBlZCAmJiBuZXh0ID09PSAnXFxcXCc7XG4gIH1cbiAgaWYgKGVuZCAmJiAhZXNjYXBlZCkge1xuICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlO1xuICB9XG4gIHJldHVybiAnc3RyaW5nJztcbn1cbjtcbmZ1bmN0aW9uIHRva2VuQ29tbWVudChzdHJlYW0sIHN0YXRlKSB7XG4gIHZhciBwcmV2LCBuZXh0O1xuICB3aGlsZSAoKG5leHQgPSBzdHJlYW0ubmV4dCgpKSAhPSBudWxsKSB7XG4gICAgaWYgKHByZXYgPT09ICcqJyAmJiBuZXh0ID09PSAnLycpIHtcbiAgICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlO1xuICAgICAgYnJlYWs7XG4gICAgfVxuICAgIHByZXYgPSBuZXh0O1xuICB9XG4gIHJldHVybiAnY29tbWVudCc7XG59XG5mdW5jdGlvbiBjdXJyZW50U2NvcGUoc3RhdGUpIHtcbiAgdmFyIHNjb3BlID0gbnVsbDtcbiAgaWYgKHN0YXRlLnNjb3Blcy5sZW5ndGggPiAwKSBzY29wZSA9IHN0YXRlLnNjb3Blc1tzdGF0ZS5zY29wZXMubGVuZ3RoIC0gMV07XG4gIHJldHVybiBzY29wZTtcbn1cbmV4cG9ydCBjb25zdCB5YWNhcyA9IHtcbiAgbmFtZTogXCJ5YWNhc1wiLFxuICBzdGFydFN0YXRlOiBmdW5jdGlvbiAoKSB7XG4gICAgcmV0dXJuIHtcbiAgICAgIHRva2VuaXplOiB0b2tlbkJhc2UsXG4gICAgICBzY29wZXM6IFtdXG4gICAgfTtcbiAgfSxcbiAgdG9rZW46IGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgaWYgKHN0cmVhbS5lYXRTcGFjZSgpKSByZXR1cm4gbnVsbDtcbiAgICByZXR1cm4gc3RhdGUudG9rZW5pemUoc3RyZWFtLCBzdGF0ZSk7XG4gIH0sXG4gIGluZGVudDogZnVuY3Rpb24gKHN0YXRlLCB0ZXh0QWZ0ZXIsIGN4KSB7XG4gICAgaWYgKHN0YXRlLnRva2VuaXplICE9PSB0b2tlbkJhc2UgJiYgc3RhdGUudG9rZW5pemUgIT09IG51bGwpIHJldHVybiBudWxsO1xuICAgIHZhciBkZWx0YSA9IDA7XG4gICAgaWYgKHRleHRBZnRlciA9PT0gJ10nIHx8IHRleHRBZnRlciA9PT0gJ107JyB8fCB0ZXh0QWZ0ZXIgPT09ICd9JyB8fCB0ZXh0QWZ0ZXIgPT09ICd9OycgfHwgdGV4dEFmdGVyID09PSAnKTsnKSBkZWx0YSA9IC0xO1xuICAgIHJldHVybiAoc3RhdGUuc2NvcGVzLmxlbmd0aCArIGRlbHRhKSAqIGN4LnVuaXQ7XG4gIH0sXG4gIGxhbmd1YWdlRGF0YToge1xuICAgIGVsZWN0cmljSW5wdXQ6IC9be31cXFtcXF0oKVxcO10vLFxuICAgIGNvbW1lbnRUb2tlbnM6IHtcbiAgICAgIGxpbmU6IFwiLy9cIixcbiAgICAgIGJsb2NrOiB7XG4gICAgICAgIG9wZW46IFwiLypcIixcbiAgICAgICAgY2xvc2U6IFwiKi9cIlxuICAgICAgfVxuICAgIH1cbiAgfVxufTsiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=