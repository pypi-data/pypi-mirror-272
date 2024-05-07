"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[1900],{

/***/ 31900:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "modelica": () => (/* binding */ modelica)
/* harmony export */ });
function words(str) {
  var obj = {},
    words = str.split(" ");
  for (var i = 0; i < words.length; ++i) obj[words[i]] = true;
  return obj;
}
var keywords = words("algorithm and annotation assert block break class connect connector constant constrainedby der discrete each else elseif elsewhen encapsulated end enumeration equation expandable extends external false final flow for function if import impure in initial inner input loop model not operator or outer output package parameter partial protected public pure record redeclare replaceable return stream then true type when while within");
var builtin = words("abs acos actualStream asin atan atan2 cardinality ceil cos cosh delay div edge exp floor getInstanceName homotopy inStream integer log log10 mod pre reinit rem semiLinear sign sin sinh spatialDistribution sqrt tan tanh");
var atoms = words("Real Boolean Integer String");
var completions = [].concat(Object.keys(keywords), Object.keys(builtin), Object.keys(atoms));
var isSingleOperatorChar = /[;=\(:\),{}.*<>+\-\/^\[\]]/;
var isDoubleOperatorChar = /(:=|<=|>=|==|<>|\.\+|\.\-|\.\*|\.\/|\.\^)/;
var isDigit = /[0-9]/;
var isNonDigit = /[_a-zA-Z]/;
function tokenLineComment(stream, state) {
  stream.skipToEnd();
  state.tokenize = null;
  return "comment";
}
function tokenBlockComment(stream, state) {
  var maybeEnd = false,
    ch;
  while (ch = stream.next()) {
    if (maybeEnd && ch == "/") {
      state.tokenize = null;
      break;
    }
    maybeEnd = ch == "*";
  }
  return "comment";
}
function tokenString(stream, state) {
  var escaped = false,
    ch;
  while ((ch = stream.next()) != null) {
    if (ch == '"' && !escaped) {
      state.tokenize = null;
      state.sol = false;
      break;
    }
    escaped = !escaped && ch == "\\";
  }
  return "string";
}
function tokenIdent(stream, state) {
  stream.eatWhile(isDigit);
  while (stream.eat(isDigit) || stream.eat(isNonDigit)) {}
  var cur = stream.current();
  if (state.sol && (cur == "package" || cur == "model" || cur == "when" || cur == "connector")) state.level++;else if (state.sol && cur == "end" && state.level > 0) state.level--;
  state.tokenize = null;
  state.sol = false;
  if (keywords.propertyIsEnumerable(cur)) return "keyword";else if (builtin.propertyIsEnumerable(cur)) return "builtin";else if (atoms.propertyIsEnumerable(cur)) return "atom";else return "variable";
}
function tokenQIdent(stream, state) {
  while (stream.eat(/[^']/)) {}
  state.tokenize = null;
  state.sol = false;
  if (stream.eat("'")) return "variable";else return "error";
}
function tokenUnsignedNumber(stream, state) {
  stream.eatWhile(isDigit);
  if (stream.eat('.')) {
    stream.eatWhile(isDigit);
  }
  if (stream.eat('e') || stream.eat('E')) {
    if (!stream.eat('-')) stream.eat('+');
    stream.eatWhile(isDigit);
  }
  state.tokenize = null;
  state.sol = false;
  return "number";
}

// Interface
const modelica = {
  name: "modelica",
  startState: function () {
    return {
      tokenize: null,
      level: 0,
      sol: true
    };
  },
  token: function (stream, state) {
    if (state.tokenize != null) {
      return state.tokenize(stream, state);
    }
    if (stream.sol()) {
      state.sol = true;
    }

    // WHITESPACE
    if (stream.eatSpace()) {
      state.tokenize = null;
      return null;
    }
    var ch = stream.next();

    // LINECOMMENT
    if (ch == '/' && stream.eat('/')) {
      state.tokenize = tokenLineComment;
    }
    // BLOCKCOMMENT
    else if (ch == '/' && stream.eat('*')) {
      state.tokenize = tokenBlockComment;
    }
    // TWO SYMBOL TOKENS
    else if (isDoubleOperatorChar.test(ch + stream.peek())) {
      stream.next();
      state.tokenize = null;
      return "operator";
    }
    // SINGLE SYMBOL TOKENS
    else if (isSingleOperatorChar.test(ch)) {
      state.tokenize = null;
      return "operator";
    }
    // IDENT
    else if (isNonDigit.test(ch)) {
      state.tokenize = tokenIdent;
    }
    // Q-IDENT
    else if (ch == "'" && stream.peek() && stream.peek() != "'") {
      state.tokenize = tokenQIdent;
    }
    // STRING
    else if (ch == '"') {
      state.tokenize = tokenString;
    }
    // UNSIGNED_NUMBER
    else if (isDigit.test(ch)) {
      state.tokenize = tokenUnsignedNumber;
    }
    // ERROR
    else {
      state.tokenize = null;
      return "error";
    }
    return state.tokenize(stream, state);
  },
  indent: function (state, textAfter, cx) {
    if (state.tokenize != null) return null;
    var level = state.level;
    if (/(algorithm)/.test(textAfter)) level--;
    if (/(equation)/.test(textAfter)) level--;
    if (/(initial algorithm)/.test(textAfter)) level--;
    if (/(initial equation)/.test(textAfter)) level--;
    if (/(end)/.test(textAfter)) level--;
    if (level > 0) return cx.unit * level;else return 0;
  },
  languageData: {
    commentTokens: {
      line: "//",
      block: {
        open: "/*",
        close: "*/"
      }
    },
    autocomplete: completions
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiMTkwMC5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGNvZGVtaXJyb3IvbGVnYWN5LW1vZGVzL21vZGUvbW9kZWxpY2EuanMiXSwic291cmNlc0NvbnRlbnQiOlsiZnVuY3Rpb24gd29yZHMoc3RyKSB7XG4gIHZhciBvYmogPSB7fSxcbiAgICB3b3JkcyA9IHN0ci5zcGxpdChcIiBcIik7XG4gIGZvciAodmFyIGkgPSAwOyBpIDwgd29yZHMubGVuZ3RoOyArK2kpIG9ialt3b3Jkc1tpXV0gPSB0cnVlO1xuICByZXR1cm4gb2JqO1xufVxudmFyIGtleXdvcmRzID0gd29yZHMoXCJhbGdvcml0aG0gYW5kIGFubm90YXRpb24gYXNzZXJ0IGJsb2NrIGJyZWFrIGNsYXNzIGNvbm5lY3QgY29ubmVjdG9yIGNvbnN0YW50IGNvbnN0cmFpbmVkYnkgZGVyIGRpc2NyZXRlIGVhY2ggZWxzZSBlbHNlaWYgZWxzZXdoZW4gZW5jYXBzdWxhdGVkIGVuZCBlbnVtZXJhdGlvbiBlcXVhdGlvbiBleHBhbmRhYmxlIGV4dGVuZHMgZXh0ZXJuYWwgZmFsc2UgZmluYWwgZmxvdyBmb3IgZnVuY3Rpb24gaWYgaW1wb3J0IGltcHVyZSBpbiBpbml0aWFsIGlubmVyIGlucHV0IGxvb3AgbW9kZWwgbm90IG9wZXJhdG9yIG9yIG91dGVyIG91dHB1dCBwYWNrYWdlIHBhcmFtZXRlciBwYXJ0aWFsIHByb3RlY3RlZCBwdWJsaWMgcHVyZSByZWNvcmQgcmVkZWNsYXJlIHJlcGxhY2VhYmxlIHJldHVybiBzdHJlYW0gdGhlbiB0cnVlIHR5cGUgd2hlbiB3aGlsZSB3aXRoaW5cIik7XG52YXIgYnVpbHRpbiA9IHdvcmRzKFwiYWJzIGFjb3MgYWN0dWFsU3RyZWFtIGFzaW4gYXRhbiBhdGFuMiBjYXJkaW5hbGl0eSBjZWlsIGNvcyBjb3NoIGRlbGF5IGRpdiBlZGdlIGV4cCBmbG9vciBnZXRJbnN0YW5jZU5hbWUgaG9tb3RvcHkgaW5TdHJlYW0gaW50ZWdlciBsb2cgbG9nMTAgbW9kIHByZSByZWluaXQgcmVtIHNlbWlMaW5lYXIgc2lnbiBzaW4gc2luaCBzcGF0aWFsRGlzdHJpYnV0aW9uIHNxcnQgdGFuIHRhbmhcIik7XG52YXIgYXRvbXMgPSB3b3JkcyhcIlJlYWwgQm9vbGVhbiBJbnRlZ2VyIFN0cmluZ1wiKTtcbnZhciBjb21wbGV0aW9ucyA9IFtdLmNvbmNhdChPYmplY3Qua2V5cyhrZXl3b3JkcyksIE9iamVjdC5rZXlzKGJ1aWx0aW4pLCBPYmplY3Qua2V5cyhhdG9tcykpO1xudmFyIGlzU2luZ2xlT3BlcmF0b3JDaGFyID0gL1s7PVxcKDpcXCkse30uKjw+K1xcLVxcL15cXFtcXF1dLztcbnZhciBpc0RvdWJsZU9wZXJhdG9yQ2hhciA9IC8oOj18PD18Pj18PT18PD58XFwuXFwrfFxcLlxcLXxcXC5cXCp8XFwuXFwvfFxcLlxcXikvO1xudmFyIGlzRGlnaXQgPSAvWzAtOV0vO1xudmFyIGlzTm9uRGlnaXQgPSAvW19hLXpBLVpdLztcbmZ1bmN0aW9uIHRva2VuTGluZUNvbW1lbnQoc3RyZWFtLCBzdGF0ZSkge1xuICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gIHN0YXRlLnRva2VuaXplID0gbnVsbDtcbiAgcmV0dXJuIFwiY29tbWVudFwiO1xufVxuZnVuY3Rpb24gdG9rZW5CbG9ja0NvbW1lbnQoc3RyZWFtLCBzdGF0ZSkge1xuICB2YXIgbWF5YmVFbmQgPSBmYWxzZSxcbiAgICBjaDtcbiAgd2hpbGUgKGNoID0gc3RyZWFtLm5leHQoKSkge1xuICAgIGlmIChtYXliZUVuZCAmJiBjaCA9PSBcIi9cIikge1xuICAgICAgc3RhdGUudG9rZW5pemUgPSBudWxsO1xuICAgICAgYnJlYWs7XG4gICAgfVxuICAgIG1heWJlRW5kID0gY2ggPT0gXCIqXCI7XG4gIH1cbiAgcmV0dXJuIFwiY29tbWVudFwiO1xufVxuZnVuY3Rpb24gdG9rZW5TdHJpbmcoc3RyZWFtLCBzdGF0ZSkge1xuICB2YXIgZXNjYXBlZCA9IGZhbHNlLFxuICAgIGNoO1xuICB3aGlsZSAoKGNoID0gc3RyZWFtLm5leHQoKSkgIT0gbnVsbCkge1xuICAgIGlmIChjaCA9PSAnXCInICYmICFlc2NhcGVkKSB7XG4gICAgICBzdGF0ZS50b2tlbml6ZSA9IG51bGw7XG4gICAgICBzdGF0ZS5zb2wgPSBmYWxzZTtcbiAgICAgIGJyZWFrO1xuICAgIH1cbiAgICBlc2NhcGVkID0gIWVzY2FwZWQgJiYgY2ggPT0gXCJcXFxcXCI7XG4gIH1cbiAgcmV0dXJuIFwic3RyaW5nXCI7XG59XG5mdW5jdGlvbiB0b2tlbklkZW50KHN0cmVhbSwgc3RhdGUpIHtcbiAgc3RyZWFtLmVhdFdoaWxlKGlzRGlnaXQpO1xuICB3aGlsZSAoc3RyZWFtLmVhdChpc0RpZ2l0KSB8fCBzdHJlYW0uZWF0KGlzTm9uRGlnaXQpKSB7fVxuICB2YXIgY3VyID0gc3RyZWFtLmN1cnJlbnQoKTtcbiAgaWYgKHN0YXRlLnNvbCAmJiAoY3VyID09IFwicGFja2FnZVwiIHx8IGN1ciA9PSBcIm1vZGVsXCIgfHwgY3VyID09IFwid2hlblwiIHx8IGN1ciA9PSBcImNvbm5lY3RvclwiKSkgc3RhdGUubGV2ZWwrKztlbHNlIGlmIChzdGF0ZS5zb2wgJiYgY3VyID09IFwiZW5kXCIgJiYgc3RhdGUubGV2ZWwgPiAwKSBzdGF0ZS5sZXZlbC0tO1xuICBzdGF0ZS50b2tlbml6ZSA9IG51bGw7XG4gIHN0YXRlLnNvbCA9IGZhbHNlO1xuICBpZiAoa2V5d29yZHMucHJvcGVydHlJc0VudW1lcmFibGUoY3VyKSkgcmV0dXJuIFwia2V5d29yZFwiO2Vsc2UgaWYgKGJ1aWx0aW4ucHJvcGVydHlJc0VudW1lcmFibGUoY3VyKSkgcmV0dXJuIFwiYnVpbHRpblwiO2Vsc2UgaWYgKGF0b21zLnByb3BlcnR5SXNFbnVtZXJhYmxlKGN1cikpIHJldHVybiBcImF0b21cIjtlbHNlIHJldHVybiBcInZhcmlhYmxlXCI7XG59XG5mdW5jdGlvbiB0b2tlblFJZGVudChzdHJlYW0sIHN0YXRlKSB7XG4gIHdoaWxlIChzdHJlYW0uZWF0KC9bXiddLykpIHt9XG4gIHN0YXRlLnRva2VuaXplID0gbnVsbDtcbiAgc3RhdGUuc29sID0gZmFsc2U7XG4gIGlmIChzdHJlYW0uZWF0KFwiJ1wiKSkgcmV0dXJuIFwidmFyaWFibGVcIjtlbHNlIHJldHVybiBcImVycm9yXCI7XG59XG5mdW5jdGlvbiB0b2tlblVuc2lnbmVkTnVtYmVyKHN0cmVhbSwgc3RhdGUpIHtcbiAgc3RyZWFtLmVhdFdoaWxlKGlzRGlnaXQpO1xuICBpZiAoc3RyZWFtLmVhdCgnLicpKSB7XG4gICAgc3RyZWFtLmVhdFdoaWxlKGlzRGlnaXQpO1xuICB9XG4gIGlmIChzdHJlYW0uZWF0KCdlJykgfHwgc3RyZWFtLmVhdCgnRScpKSB7XG4gICAgaWYgKCFzdHJlYW0uZWF0KCctJykpIHN0cmVhbS5lYXQoJysnKTtcbiAgICBzdHJlYW0uZWF0V2hpbGUoaXNEaWdpdCk7XG4gIH1cbiAgc3RhdGUudG9rZW5pemUgPSBudWxsO1xuICBzdGF0ZS5zb2wgPSBmYWxzZTtcbiAgcmV0dXJuIFwibnVtYmVyXCI7XG59XG5cbi8vIEludGVyZmFjZVxuZXhwb3J0IGNvbnN0IG1vZGVsaWNhID0ge1xuICBuYW1lOiBcIm1vZGVsaWNhXCIsXG4gIHN0YXJ0U3RhdGU6IGZ1bmN0aW9uICgpIHtcbiAgICByZXR1cm4ge1xuICAgICAgdG9rZW5pemU6IG51bGwsXG4gICAgICBsZXZlbDogMCxcbiAgICAgIHNvbDogdHJ1ZVxuICAgIH07XG4gIH0sXG4gIHRva2VuOiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIGlmIChzdGF0ZS50b2tlbml6ZSAhPSBudWxsKSB7XG4gICAgICByZXR1cm4gc3RhdGUudG9rZW5pemUoc3RyZWFtLCBzdGF0ZSk7XG4gICAgfVxuICAgIGlmIChzdHJlYW0uc29sKCkpIHtcbiAgICAgIHN0YXRlLnNvbCA9IHRydWU7XG4gICAgfVxuXG4gICAgLy8gV0hJVEVTUEFDRVxuICAgIGlmIChzdHJlYW0uZWF0U3BhY2UoKSkge1xuICAgICAgc3RhdGUudG9rZW5pemUgPSBudWxsO1xuICAgICAgcmV0dXJuIG51bGw7XG4gICAgfVxuICAgIHZhciBjaCA9IHN0cmVhbS5uZXh0KCk7XG5cbiAgICAvLyBMSU5FQ09NTUVOVFxuICAgIGlmIChjaCA9PSAnLycgJiYgc3RyZWFtLmVhdCgnLycpKSB7XG4gICAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuTGluZUNvbW1lbnQ7XG4gICAgfVxuICAgIC8vIEJMT0NLQ09NTUVOVFxuICAgIGVsc2UgaWYgKGNoID09ICcvJyAmJiBzdHJlYW0uZWF0KCcqJykpIHtcbiAgICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5CbG9ja0NvbW1lbnQ7XG4gICAgfVxuICAgIC8vIFRXTyBTWU1CT0wgVE9LRU5TXG4gICAgZWxzZSBpZiAoaXNEb3VibGVPcGVyYXRvckNoYXIudGVzdChjaCArIHN0cmVhbS5wZWVrKCkpKSB7XG4gICAgICBzdHJlYW0ubmV4dCgpO1xuICAgICAgc3RhdGUudG9rZW5pemUgPSBudWxsO1xuICAgICAgcmV0dXJuIFwib3BlcmF0b3JcIjtcbiAgICB9XG4gICAgLy8gU0lOR0xFIFNZTUJPTCBUT0tFTlNcbiAgICBlbHNlIGlmIChpc1NpbmdsZU9wZXJhdG9yQ2hhci50ZXN0KGNoKSkge1xuICAgICAgc3RhdGUudG9rZW5pemUgPSBudWxsO1xuICAgICAgcmV0dXJuIFwib3BlcmF0b3JcIjtcbiAgICB9XG4gICAgLy8gSURFTlRcbiAgICBlbHNlIGlmIChpc05vbkRpZ2l0LnRlc3QoY2gpKSB7XG4gICAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuSWRlbnQ7XG4gICAgfVxuICAgIC8vIFEtSURFTlRcbiAgICBlbHNlIGlmIChjaCA9PSBcIidcIiAmJiBzdHJlYW0ucGVlaygpICYmIHN0cmVhbS5wZWVrKCkgIT0gXCInXCIpIHtcbiAgICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5RSWRlbnQ7XG4gICAgfVxuICAgIC8vIFNUUklOR1xuICAgIGVsc2UgaWYgKGNoID09ICdcIicpIHtcbiAgICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5TdHJpbmc7XG4gICAgfVxuICAgIC8vIFVOU0lHTkVEX05VTUJFUlxuICAgIGVsc2UgaWYgKGlzRGlnaXQudGVzdChjaCkpIHtcbiAgICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5VbnNpZ25lZE51bWJlcjtcbiAgICB9XG4gICAgLy8gRVJST1JcbiAgICBlbHNlIHtcbiAgICAgIHN0YXRlLnRva2VuaXplID0gbnVsbDtcbiAgICAgIHJldHVybiBcImVycm9yXCI7XG4gICAgfVxuICAgIHJldHVybiBzdGF0ZS50b2tlbml6ZShzdHJlYW0sIHN0YXRlKTtcbiAgfSxcbiAgaW5kZW50OiBmdW5jdGlvbiAoc3RhdGUsIHRleHRBZnRlciwgY3gpIHtcbiAgICBpZiAoc3RhdGUudG9rZW5pemUgIT0gbnVsbCkgcmV0dXJuIG51bGw7XG4gICAgdmFyIGxldmVsID0gc3RhdGUubGV2ZWw7XG4gICAgaWYgKC8oYWxnb3JpdGhtKS8udGVzdCh0ZXh0QWZ0ZXIpKSBsZXZlbC0tO1xuICAgIGlmICgvKGVxdWF0aW9uKS8udGVzdCh0ZXh0QWZ0ZXIpKSBsZXZlbC0tO1xuICAgIGlmICgvKGluaXRpYWwgYWxnb3JpdGhtKS8udGVzdCh0ZXh0QWZ0ZXIpKSBsZXZlbC0tO1xuICAgIGlmICgvKGluaXRpYWwgZXF1YXRpb24pLy50ZXN0KHRleHRBZnRlcikpIGxldmVsLS07XG4gICAgaWYgKC8oZW5kKS8udGVzdCh0ZXh0QWZ0ZXIpKSBsZXZlbC0tO1xuICAgIGlmIChsZXZlbCA+IDApIHJldHVybiBjeC51bml0ICogbGV2ZWw7ZWxzZSByZXR1cm4gMDtcbiAgfSxcbiAgbGFuZ3VhZ2VEYXRhOiB7XG4gICAgY29tbWVudFRva2Vuczoge1xuICAgICAgbGluZTogXCIvL1wiLFxuICAgICAgYmxvY2s6IHtcbiAgICAgICAgb3BlbjogXCIvKlwiLFxuICAgICAgICBjbG9zZTogXCIqL1wiXG4gICAgICB9XG4gICAgfSxcbiAgICBhdXRvY29tcGxldGU6IGNvbXBsZXRpb25zXG4gIH1cbn07Il0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9