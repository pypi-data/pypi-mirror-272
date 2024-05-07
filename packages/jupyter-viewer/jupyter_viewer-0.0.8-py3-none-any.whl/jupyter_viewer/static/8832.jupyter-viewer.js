"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[8832],{

/***/ 8832:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "julia": () => (/* binding */ julia)
/* harmony export */ });
function wordRegexp(words, end, pre) {
  if (typeof pre === "undefined") pre = "";
  if (typeof end === "undefined") {
    end = "\\b";
  }
  return new RegExp("^" + pre + "((" + words.join(")|(") + "))" + end);
}
var octChar = "\\\\[0-7]{1,3}";
var hexChar = "\\\\x[A-Fa-f0-9]{1,2}";
var sChar = "\\\\[abefnrtv0%?'\"\\\\]";
var uChar = "([^\\u0027\\u005C\\uD800-\\uDFFF]|[\\uD800-\\uDFFF][\\uDC00-\\uDFFF])";
var asciiOperatorsList = ["[<>]:", "[<>=]=", "<<=?", ">>>?=?", "=>", "--?>", "<--[->]?", "\\/\\/", "\\.{2,3}", "[\\.\\\\%*+\\-<>!\\/^|&]=?", "\\?", "\\$", "~", ":"];
var operators = wordRegexp(["[<>]:", "[<>=]=", "[!=]==", "<<=?", ">>>?=?", "=>?", "--?>", "<--[->]?", "\\/\\/", "[\\\\%*+\\-<>!\\/^|&\\u00F7\\u22BB]=?", "\\?", "\\$", "~", ":", "\\u00D7", "\\u2208", "\\u2209", "\\u220B", "\\u220C", "\\u2218", "\\u221A", "\\u221B", "\\u2229", "\\u222A", "\\u2260", "\\u2264", "\\u2265", "\\u2286", "\\u2288", "\\u228A", "\\u22C5", "\\b(in|isa)\\b(?!\.?\\()"], "");
var delimiters = /^[;,()[\]{}]/;
var identifiers = /^[_A-Za-z\u00A1-\u2217\u2219-\uFFFF][\w\u00A1-\u2217\u2219-\uFFFF]*!*/;
var chars = wordRegexp([octChar, hexChar, sChar, uChar], "'");
var openersList = ["begin", "function", "type", "struct", "immutable", "let", "macro", "for", "while", "quote", "if", "else", "elseif", "try", "finally", "catch", "do"];
var closersList = ["end", "else", "elseif", "catch", "finally"];
var keywordsList = ["if", "else", "elseif", "while", "for", "begin", "let", "end", "do", "try", "catch", "finally", "return", "break", "continue", "global", "local", "const", "export", "import", "importall", "using", "function", "where", "macro", "module", "baremodule", "struct", "type", "mutable", "immutable", "quote", "typealias", "abstract", "primitive", "bitstype"];
var builtinsList = ["true", "false", "nothing", "NaN", "Inf"];
var openers = wordRegexp(openersList);
var closers = wordRegexp(closersList);
var keywords = wordRegexp(keywordsList);
var builtins = wordRegexp(builtinsList);
var macro = /^@[_A-Za-z\u00A1-\uFFFF][\w\u00A1-\uFFFF]*!*/;
var symbol = /^:[_A-Za-z\u00A1-\uFFFF][\w\u00A1-\uFFFF]*!*/;
var stringPrefixes = /^(`|([_A-Za-z\u00A1-\uFFFF]*"("")?))/;
var macroOperators = wordRegexp(asciiOperatorsList, "", "@");
var symbolOperators = wordRegexp(asciiOperatorsList, "", ":");
function inArray(state) {
  return state.nestedArrays > 0;
}
function inGenerator(state) {
  return state.nestedGenerators > 0;
}
function currentScope(state, n) {
  if (typeof n === "undefined") {
    n = 0;
  }
  if (state.scopes.length <= n) {
    return null;
  }
  return state.scopes[state.scopes.length - (n + 1)];
}

// tokenizers
function tokenBase(stream, state) {
  // Handle multiline comments
  if (stream.match('#=', false)) {
    state.tokenize = tokenComment;
    return state.tokenize(stream, state);
  }

  // Handle scope changes
  var leavingExpr = state.leavingExpr;
  if (stream.sol()) {
    leavingExpr = false;
  }
  state.leavingExpr = false;
  if (leavingExpr) {
    if (stream.match(/^'+/)) {
      return "operator";
    }
  }
  if (stream.match(/\.{4,}/)) {
    return "error";
  } else if (stream.match(/\.{1,3}/)) {
    return "operator";
  }
  if (stream.eatSpace()) {
    return null;
  }
  var ch = stream.peek();

  // Handle single line comments
  if (ch === '#') {
    stream.skipToEnd();
    return "comment";
  }
  if (ch === '[') {
    state.scopes.push('[');
    state.nestedArrays++;
  }
  if (ch === '(') {
    state.scopes.push('(');
    state.nestedGenerators++;
  }
  if (inArray(state) && ch === ']') {
    while (state.scopes.length && currentScope(state) !== "[") {
      state.scopes.pop();
    }
    state.scopes.pop();
    state.nestedArrays--;
    state.leavingExpr = true;
  }
  if (inGenerator(state) && ch === ')') {
    while (state.scopes.length && currentScope(state) !== "(") {
      state.scopes.pop();
    }
    state.scopes.pop();
    state.nestedGenerators--;
    state.leavingExpr = true;
  }
  if (inArray(state)) {
    if (state.lastToken == "end" && stream.match(':')) {
      return "operator";
    }
    if (stream.match('end')) {
      return "number";
    }
  }
  var match;
  if (match = stream.match(openers, false)) {
    state.scopes.push(match[0]);
  }
  if (stream.match(closers, false)) {
    state.scopes.pop();
  }

  // Handle type annotations
  if (stream.match(/^::(?![:\$])/)) {
    state.tokenize = tokenAnnotation;
    return state.tokenize(stream, state);
  }

  // Handle symbols
  if (!leavingExpr && (stream.match(symbol) || stream.match(symbolOperators))) {
    return "builtin";
  }

  // Handle parametric types
  //if (stream.match(/^{[^}]*}(?=\()/)) {
  //  return "builtin";
  //}

  // Handle operators and Delimiters
  if (stream.match(operators)) {
    return "operator";
  }

  // Handle Number Literals
  if (stream.match(/^\.?\d/, false)) {
    var imMatcher = RegExp(/^im\b/);
    var numberLiteral = false;
    if (stream.match(/^0x\.[0-9a-f_]+p[\+\-]?[_\d]+/i)) {
      numberLiteral = true;
    }
    // Integers
    if (stream.match(/^0x[0-9a-f_]+/i)) {
      numberLiteral = true;
    } // Hex
    if (stream.match(/^0b[01_]+/i)) {
      numberLiteral = true;
    } // Binary
    if (stream.match(/^0o[0-7_]+/i)) {
      numberLiteral = true;
    } // Octal
    // Floats
    if (stream.match(/^(?:(?:\d[_\d]*)?\.(?!\.)(?:\d[_\d]*)?|\d[_\d]*\.(?!\.)(?:\d[_\d]*))?([Eef][\+\-]?[_\d]+)?/i)) {
      numberLiteral = true;
    }
    if (stream.match(/^\d[_\d]*(e[\+\-]?\d+)?/i)) {
      numberLiteral = true;
    } // Decimal
    if (numberLiteral) {
      // Integer literals may be "long"
      stream.match(imMatcher);
      state.leavingExpr = true;
      return "number";
    }
  }

  // Handle Chars
  if (stream.match("'")) {
    state.tokenize = tokenChar;
    return state.tokenize(stream, state);
  }

  // Handle Strings
  if (stream.match(stringPrefixes)) {
    state.tokenize = tokenStringFactory(stream.current());
    return state.tokenize(stream, state);
  }
  if (stream.match(macro) || stream.match(macroOperators)) {
    return "meta";
  }
  if (stream.match(delimiters)) {
    return null;
  }
  if (stream.match(keywords)) {
    return "keyword";
  }
  if (stream.match(builtins)) {
    return "builtin";
  }
  var isDefinition = state.isDefinition || state.lastToken == "function" || state.lastToken == "macro" || state.lastToken == "type" || state.lastToken == "struct" || state.lastToken == "immutable";
  if (stream.match(identifiers)) {
    if (isDefinition) {
      if (stream.peek() === '.') {
        state.isDefinition = true;
        return "variable";
      }
      state.isDefinition = false;
      return "def";
    }
    state.leavingExpr = true;
    return "variable";
  }

  // Handle non-detected items
  stream.next();
  return "error";
}
function tokenAnnotation(stream, state) {
  stream.match(/.*?(?=[,;{}()=\s]|$)/);
  if (stream.match('{')) {
    state.nestedParameters++;
  } else if (stream.match('}') && state.nestedParameters > 0) {
    state.nestedParameters--;
  }
  if (state.nestedParameters > 0) {
    stream.match(/.*?(?={|})/) || stream.next();
  } else if (state.nestedParameters == 0) {
    state.tokenize = tokenBase;
  }
  return "builtin";
}
function tokenComment(stream, state) {
  if (stream.match('#=')) {
    state.nestedComments++;
  }
  if (!stream.match(/.*?(?=(#=|=#))/)) {
    stream.skipToEnd();
  }
  if (stream.match('=#')) {
    state.nestedComments--;
    if (state.nestedComments == 0) state.tokenize = tokenBase;
  }
  return "comment";
}
function tokenChar(stream, state) {
  var isChar = false,
    match;
  if (stream.match(chars)) {
    isChar = true;
  } else if (match = stream.match(/\\u([a-f0-9]{1,4})(?=')/i)) {
    var value = parseInt(match[1], 16);
    if (value <= 55295 || value >= 57344) {
      // (U+0,U+D7FF), (U+E000,U+FFFF)
      isChar = true;
      stream.next();
    }
  } else if (match = stream.match(/\\U([A-Fa-f0-9]{5,8})(?=')/)) {
    var value = parseInt(match[1], 16);
    if (value <= 1114111) {
      // U+10FFFF
      isChar = true;
      stream.next();
    }
  }
  if (isChar) {
    state.leavingExpr = true;
    state.tokenize = tokenBase;
    return "string";
  }
  if (!stream.match(/^[^']+(?=')/)) {
    stream.skipToEnd();
  }
  if (stream.match("'")) {
    state.tokenize = tokenBase;
  }
  return "error";
}
function tokenStringFactory(delimiter) {
  if (delimiter.substr(-3) === '"""') {
    delimiter = '"""';
  } else if (delimiter.substr(-1) === '"') {
    delimiter = '"';
  }
  function tokenString(stream, state) {
    if (stream.eat('\\')) {
      stream.next();
    } else if (stream.match(delimiter)) {
      state.tokenize = tokenBase;
      state.leavingExpr = true;
      return "string";
    } else {
      stream.eat(/[`"]/);
    }
    stream.eatWhile(/[^\\`"]/);
    return "string";
  }
  return tokenString;
}
const julia = {
  name: "julia",
  startState: function () {
    return {
      tokenize: tokenBase,
      scopes: [],
      lastToken: null,
      leavingExpr: false,
      isDefinition: false,
      nestedArrays: 0,
      nestedComments: 0,
      nestedGenerators: 0,
      nestedParameters: 0,
      firstParenPos: -1
    };
  },
  token: function (stream, state) {
    var style = state.tokenize(stream, state);
    var current = stream.current();
    if (current && style) {
      state.lastToken = current;
    }
    return style;
  },
  indent: function (state, textAfter, cx) {
    var delta = 0;
    if (textAfter === ']' || textAfter === ')' || /^end\b/.test(textAfter) || /^else/.test(textAfter) || /^catch\b/.test(textAfter) || /^elseif\b/.test(textAfter) || /^finally/.test(textAfter)) {
      delta = -1;
    }
    return (state.scopes.length + delta) * cx.unit;
  },
  languageData: {
    indentOnInput: /^\s*(end|else|catch|finally)\b$/,
    commentTokens: {
      line: "#",
      block: {
        open: "#=",
        close: "=#"
      }
    },
    closeBrackets: {
      brackets: ["(", "[", "{", '"']
    },
    autocomplete: keywordsList.concat(builtinsList)
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiODgzMi5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL0Bjb2RlbWlycm9yL2xlZ2FjeS1tb2Rlcy9tb2RlL2p1bGlhLmpzIl0sInNvdXJjZXNDb250ZW50IjpbImZ1bmN0aW9uIHdvcmRSZWdleHAod29yZHMsIGVuZCwgcHJlKSB7XG4gIGlmICh0eXBlb2YgcHJlID09PSBcInVuZGVmaW5lZFwiKSBwcmUgPSBcIlwiO1xuICBpZiAodHlwZW9mIGVuZCA9PT0gXCJ1bmRlZmluZWRcIikge1xuICAgIGVuZCA9IFwiXFxcXGJcIjtcbiAgfVxuICByZXR1cm4gbmV3IFJlZ0V4cChcIl5cIiArIHByZSArIFwiKChcIiArIHdvcmRzLmpvaW4oXCIpfChcIikgKyBcIikpXCIgKyBlbmQpO1xufVxudmFyIG9jdENoYXIgPSBcIlxcXFxcXFxcWzAtN117MSwzfVwiO1xudmFyIGhleENoYXIgPSBcIlxcXFxcXFxceFtBLUZhLWYwLTldezEsMn1cIjtcbnZhciBzQ2hhciA9IFwiXFxcXFxcXFxbYWJlZm5ydHYwJT8nXFxcIlxcXFxcXFxcXVwiO1xudmFyIHVDaGFyID0gXCIoW15cXFxcdTAwMjdcXFxcdTAwNUNcXFxcdUQ4MDAtXFxcXHVERkZGXXxbXFxcXHVEODAwLVxcXFx1REZGRl1bXFxcXHVEQzAwLVxcXFx1REZGRl0pXCI7XG52YXIgYXNjaWlPcGVyYXRvcnNMaXN0ID0gW1wiWzw+XTpcIiwgXCJbPD49XT1cIiwgXCI8PD0/XCIsIFwiPj4+Pz0/XCIsIFwiPT5cIiwgXCItLT8+XCIsIFwiPC0tWy0+XT9cIiwgXCJcXFxcL1xcXFwvXCIsIFwiXFxcXC57MiwzfVwiLCBcIltcXFxcLlxcXFxcXFxcJSorXFxcXC08PiFcXFxcL158Jl09P1wiLCBcIlxcXFw/XCIsIFwiXFxcXCRcIiwgXCJ+XCIsIFwiOlwiXTtcbnZhciBvcGVyYXRvcnMgPSB3b3JkUmVnZXhwKFtcIls8Pl06XCIsIFwiWzw+PV09XCIsIFwiWyE9XT09XCIsIFwiPDw9P1wiLCBcIj4+Pj89P1wiLCBcIj0+P1wiLCBcIi0tPz5cIiwgXCI8LS1bLT5dP1wiLCBcIlxcXFwvXFxcXC9cIiwgXCJbXFxcXFxcXFwlKitcXFxcLTw+IVxcXFwvXnwmXFxcXHUwMEY3XFxcXHUyMkJCXT0/XCIsIFwiXFxcXD9cIiwgXCJcXFxcJFwiLCBcIn5cIiwgXCI6XCIsIFwiXFxcXHUwMEQ3XCIsIFwiXFxcXHUyMjA4XCIsIFwiXFxcXHUyMjA5XCIsIFwiXFxcXHUyMjBCXCIsIFwiXFxcXHUyMjBDXCIsIFwiXFxcXHUyMjE4XCIsIFwiXFxcXHUyMjFBXCIsIFwiXFxcXHUyMjFCXCIsIFwiXFxcXHUyMjI5XCIsIFwiXFxcXHUyMjJBXCIsIFwiXFxcXHUyMjYwXCIsIFwiXFxcXHUyMjY0XCIsIFwiXFxcXHUyMjY1XCIsIFwiXFxcXHUyMjg2XCIsIFwiXFxcXHUyMjg4XCIsIFwiXFxcXHUyMjhBXCIsIFwiXFxcXHUyMkM1XCIsIFwiXFxcXGIoaW58aXNhKVxcXFxiKD8hXFwuP1xcXFwoKVwiXSwgXCJcIik7XG52YXIgZGVsaW1pdGVycyA9IC9eWzssKClbXFxde31dLztcbnZhciBpZGVudGlmaWVycyA9IC9eW19BLVphLXpcXHUwMEExLVxcdTIyMTdcXHUyMjE5LVxcdUZGRkZdW1xcd1xcdTAwQTEtXFx1MjIxN1xcdTIyMTktXFx1RkZGRl0qISovO1xudmFyIGNoYXJzID0gd29yZFJlZ2V4cChbb2N0Q2hhciwgaGV4Q2hhciwgc0NoYXIsIHVDaGFyXSwgXCInXCIpO1xudmFyIG9wZW5lcnNMaXN0ID0gW1wiYmVnaW5cIiwgXCJmdW5jdGlvblwiLCBcInR5cGVcIiwgXCJzdHJ1Y3RcIiwgXCJpbW11dGFibGVcIiwgXCJsZXRcIiwgXCJtYWNyb1wiLCBcImZvclwiLCBcIndoaWxlXCIsIFwicXVvdGVcIiwgXCJpZlwiLCBcImVsc2VcIiwgXCJlbHNlaWZcIiwgXCJ0cnlcIiwgXCJmaW5hbGx5XCIsIFwiY2F0Y2hcIiwgXCJkb1wiXTtcbnZhciBjbG9zZXJzTGlzdCA9IFtcImVuZFwiLCBcImVsc2VcIiwgXCJlbHNlaWZcIiwgXCJjYXRjaFwiLCBcImZpbmFsbHlcIl07XG52YXIga2V5d29yZHNMaXN0ID0gW1wiaWZcIiwgXCJlbHNlXCIsIFwiZWxzZWlmXCIsIFwid2hpbGVcIiwgXCJmb3JcIiwgXCJiZWdpblwiLCBcImxldFwiLCBcImVuZFwiLCBcImRvXCIsIFwidHJ5XCIsIFwiY2F0Y2hcIiwgXCJmaW5hbGx5XCIsIFwicmV0dXJuXCIsIFwiYnJlYWtcIiwgXCJjb250aW51ZVwiLCBcImdsb2JhbFwiLCBcImxvY2FsXCIsIFwiY29uc3RcIiwgXCJleHBvcnRcIiwgXCJpbXBvcnRcIiwgXCJpbXBvcnRhbGxcIiwgXCJ1c2luZ1wiLCBcImZ1bmN0aW9uXCIsIFwid2hlcmVcIiwgXCJtYWNyb1wiLCBcIm1vZHVsZVwiLCBcImJhcmVtb2R1bGVcIiwgXCJzdHJ1Y3RcIiwgXCJ0eXBlXCIsIFwibXV0YWJsZVwiLCBcImltbXV0YWJsZVwiLCBcInF1b3RlXCIsIFwidHlwZWFsaWFzXCIsIFwiYWJzdHJhY3RcIiwgXCJwcmltaXRpdmVcIiwgXCJiaXRzdHlwZVwiXTtcbnZhciBidWlsdGluc0xpc3QgPSBbXCJ0cnVlXCIsIFwiZmFsc2VcIiwgXCJub3RoaW5nXCIsIFwiTmFOXCIsIFwiSW5mXCJdO1xudmFyIG9wZW5lcnMgPSB3b3JkUmVnZXhwKG9wZW5lcnNMaXN0KTtcbnZhciBjbG9zZXJzID0gd29yZFJlZ2V4cChjbG9zZXJzTGlzdCk7XG52YXIga2V5d29yZHMgPSB3b3JkUmVnZXhwKGtleXdvcmRzTGlzdCk7XG52YXIgYnVpbHRpbnMgPSB3b3JkUmVnZXhwKGJ1aWx0aW5zTGlzdCk7XG52YXIgbWFjcm8gPSAvXkBbX0EtWmEtelxcdTAwQTEtXFx1RkZGRl1bXFx3XFx1MDBBMS1cXHVGRkZGXSohKi87XG52YXIgc3ltYm9sID0gL146W19BLVphLXpcXHUwMEExLVxcdUZGRkZdW1xcd1xcdTAwQTEtXFx1RkZGRl0qISovO1xudmFyIHN0cmluZ1ByZWZpeGVzID0gL14oYHwoW19BLVphLXpcXHUwMEExLVxcdUZGRkZdKlwiKFwiXCIpPykpLztcbnZhciBtYWNyb09wZXJhdG9ycyA9IHdvcmRSZWdleHAoYXNjaWlPcGVyYXRvcnNMaXN0LCBcIlwiLCBcIkBcIik7XG52YXIgc3ltYm9sT3BlcmF0b3JzID0gd29yZFJlZ2V4cChhc2NpaU9wZXJhdG9yc0xpc3QsIFwiXCIsIFwiOlwiKTtcbmZ1bmN0aW9uIGluQXJyYXkoc3RhdGUpIHtcbiAgcmV0dXJuIHN0YXRlLm5lc3RlZEFycmF5cyA+IDA7XG59XG5mdW5jdGlvbiBpbkdlbmVyYXRvcihzdGF0ZSkge1xuICByZXR1cm4gc3RhdGUubmVzdGVkR2VuZXJhdG9ycyA+IDA7XG59XG5mdW5jdGlvbiBjdXJyZW50U2NvcGUoc3RhdGUsIG4pIHtcbiAgaWYgKHR5cGVvZiBuID09PSBcInVuZGVmaW5lZFwiKSB7XG4gICAgbiA9IDA7XG4gIH1cbiAgaWYgKHN0YXRlLnNjb3Blcy5sZW5ndGggPD0gbikge1xuICAgIHJldHVybiBudWxsO1xuICB9XG4gIHJldHVybiBzdGF0ZS5zY29wZXNbc3RhdGUuc2NvcGVzLmxlbmd0aCAtIChuICsgMSldO1xufVxuXG4vLyB0b2tlbml6ZXJzXG5mdW5jdGlvbiB0b2tlbkJhc2Uoc3RyZWFtLCBzdGF0ZSkge1xuICAvLyBIYW5kbGUgbXVsdGlsaW5lIGNvbW1lbnRzXG4gIGlmIChzdHJlYW0ubWF0Y2goJyM9JywgZmFsc2UpKSB7XG4gICAgc3RhdGUudG9rZW5pemUgPSB0b2tlbkNvbW1lbnQ7XG4gICAgcmV0dXJuIHN0YXRlLnRva2VuaXplKHN0cmVhbSwgc3RhdGUpO1xuICB9XG5cbiAgLy8gSGFuZGxlIHNjb3BlIGNoYW5nZXNcbiAgdmFyIGxlYXZpbmdFeHByID0gc3RhdGUubGVhdmluZ0V4cHI7XG4gIGlmIChzdHJlYW0uc29sKCkpIHtcbiAgICBsZWF2aW5nRXhwciA9IGZhbHNlO1xuICB9XG4gIHN0YXRlLmxlYXZpbmdFeHByID0gZmFsc2U7XG4gIGlmIChsZWF2aW5nRXhwcikge1xuICAgIGlmIChzdHJlYW0ubWF0Y2goL14nKy8pKSB7XG4gICAgICByZXR1cm4gXCJvcGVyYXRvclwiO1xuICAgIH1cbiAgfVxuICBpZiAoc3RyZWFtLm1hdGNoKC9cXC57NCx9LykpIHtcbiAgICByZXR1cm4gXCJlcnJvclwiO1xuICB9IGVsc2UgaWYgKHN0cmVhbS5tYXRjaCgvXFwuezEsM30vKSkge1xuICAgIHJldHVybiBcIm9wZXJhdG9yXCI7XG4gIH1cbiAgaWYgKHN0cmVhbS5lYXRTcGFjZSgpKSB7XG4gICAgcmV0dXJuIG51bGw7XG4gIH1cbiAgdmFyIGNoID0gc3RyZWFtLnBlZWsoKTtcblxuICAvLyBIYW5kbGUgc2luZ2xlIGxpbmUgY29tbWVudHNcbiAgaWYgKGNoID09PSAnIycpIHtcbiAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICB9XG4gIGlmIChjaCA9PT0gJ1snKSB7XG4gICAgc3RhdGUuc2NvcGVzLnB1c2goJ1snKTtcbiAgICBzdGF0ZS5uZXN0ZWRBcnJheXMrKztcbiAgfVxuICBpZiAoY2ggPT09ICcoJykge1xuICAgIHN0YXRlLnNjb3Blcy5wdXNoKCcoJyk7XG4gICAgc3RhdGUubmVzdGVkR2VuZXJhdG9ycysrO1xuICB9XG4gIGlmIChpbkFycmF5KHN0YXRlKSAmJiBjaCA9PT0gJ10nKSB7XG4gICAgd2hpbGUgKHN0YXRlLnNjb3Blcy5sZW5ndGggJiYgY3VycmVudFNjb3BlKHN0YXRlKSAhPT0gXCJbXCIpIHtcbiAgICAgIHN0YXRlLnNjb3Blcy5wb3AoKTtcbiAgICB9XG4gICAgc3RhdGUuc2NvcGVzLnBvcCgpO1xuICAgIHN0YXRlLm5lc3RlZEFycmF5cy0tO1xuICAgIHN0YXRlLmxlYXZpbmdFeHByID0gdHJ1ZTtcbiAgfVxuICBpZiAoaW5HZW5lcmF0b3Ioc3RhdGUpICYmIGNoID09PSAnKScpIHtcbiAgICB3aGlsZSAoc3RhdGUuc2NvcGVzLmxlbmd0aCAmJiBjdXJyZW50U2NvcGUoc3RhdGUpICE9PSBcIihcIikge1xuICAgICAgc3RhdGUuc2NvcGVzLnBvcCgpO1xuICAgIH1cbiAgICBzdGF0ZS5zY29wZXMucG9wKCk7XG4gICAgc3RhdGUubmVzdGVkR2VuZXJhdG9ycy0tO1xuICAgIHN0YXRlLmxlYXZpbmdFeHByID0gdHJ1ZTtcbiAgfVxuICBpZiAoaW5BcnJheShzdGF0ZSkpIHtcbiAgICBpZiAoc3RhdGUubGFzdFRva2VuID09IFwiZW5kXCIgJiYgc3RyZWFtLm1hdGNoKCc6JykpIHtcbiAgICAgIHJldHVybiBcIm9wZXJhdG9yXCI7XG4gICAgfVxuICAgIGlmIChzdHJlYW0ubWF0Y2goJ2VuZCcpKSB7XG4gICAgICByZXR1cm4gXCJudW1iZXJcIjtcbiAgICB9XG4gIH1cbiAgdmFyIG1hdGNoO1xuICBpZiAobWF0Y2ggPSBzdHJlYW0ubWF0Y2gob3BlbmVycywgZmFsc2UpKSB7XG4gICAgc3RhdGUuc2NvcGVzLnB1c2gobWF0Y2hbMF0pO1xuICB9XG4gIGlmIChzdHJlYW0ubWF0Y2goY2xvc2VycywgZmFsc2UpKSB7XG4gICAgc3RhdGUuc2NvcGVzLnBvcCgpO1xuICB9XG5cbiAgLy8gSGFuZGxlIHR5cGUgYW5ub3RhdGlvbnNcbiAgaWYgKHN0cmVhbS5tYXRjaCgvXjo6KD8hWzpcXCRdKS8pKSB7XG4gICAgc3RhdGUudG9rZW5pemUgPSB0b2tlbkFubm90YXRpb247XG4gICAgcmV0dXJuIHN0YXRlLnRva2VuaXplKHN0cmVhbSwgc3RhdGUpO1xuICB9XG5cbiAgLy8gSGFuZGxlIHN5bWJvbHNcbiAgaWYgKCFsZWF2aW5nRXhwciAmJiAoc3RyZWFtLm1hdGNoKHN5bWJvbCkgfHwgc3RyZWFtLm1hdGNoKHN5bWJvbE9wZXJhdG9ycykpKSB7XG4gICAgcmV0dXJuIFwiYnVpbHRpblwiO1xuICB9XG5cbiAgLy8gSGFuZGxlIHBhcmFtZXRyaWMgdHlwZXNcbiAgLy9pZiAoc3RyZWFtLm1hdGNoKC9ee1tefV0qfSg/PVxcKCkvKSkge1xuICAvLyAgcmV0dXJuIFwiYnVpbHRpblwiO1xuICAvL31cblxuICAvLyBIYW5kbGUgb3BlcmF0b3JzIGFuZCBEZWxpbWl0ZXJzXG4gIGlmIChzdHJlYW0ubWF0Y2gob3BlcmF0b3JzKSkge1xuICAgIHJldHVybiBcIm9wZXJhdG9yXCI7XG4gIH1cblxuICAvLyBIYW5kbGUgTnVtYmVyIExpdGVyYWxzXG4gIGlmIChzdHJlYW0ubWF0Y2goL15cXC4/XFxkLywgZmFsc2UpKSB7XG4gICAgdmFyIGltTWF0Y2hlciA9IFJlZ0V4cCgvXmltXFxiLyk7XG4gICAgdmFyIG51bWJlckxpdGVyYWwgPSBmYWxzZTtcbiAgICBpZiAoc3RyZWFtLm1hdGNoKC9eMHhcXC5bMC05YS1mX10rcFtcXCtcXC1dP1tfXFxkXSsvaSkpIHtcbiAgICAgIG51bWJlckxpdGVyYWwgPSB0cnVlO1xuICAgIH1cbiAgICAvLyBJbnRlZ2Vyc1xuICAgIGlmIChzdHJlYW0ubWF0Y2goL14weFswLTlhLWZfXSsvaSkpIHtcbiAgICAgIG51bWJlckxpdGVyYWwgPSB0cnVlO1xuICAgIH0gLy8gSGV4XG4gICAgaWYgKHN0cmVhbS5tYXRjaCgvXjBiWzAxX10rL2kpKSB7XG4gICAgICBudW1iZXJMaXRlcmFsID0gdHJ1ZTtcbiAgICB9IC8vIEJpbmFyeVxuICAgIGlmIChzdHJlYW0ubWF0Y2goL14wb1swLTdfXSsvaSkpIHtcbiAgICAgIG51bWJlckxpdGVyYWwgPSB0cnVlO1xuICAgIH0gLy8gT2N0YWxcbiAgICAvLyBGbG9hdHNcbiAgICBpZiAoc3RyZWFtLm1hdGNoKC9eKD86KD86XFxkW19cXGRdKik/XFwuKD8hXFwuKSg/OlxcZFtfXFxkXSopP3xcXGRbX1xcZF0qXFwuKD8hXFwuKSg/OlxcZFtfXFxkXSopKT8oW0VlZl1bXFwrXFwtXT9bX1xcZF0rKT8vaSkpIHtcbiAgICAgIG51bWJlckxpdGVyYWwgPSB0cnVlO1xuICAgIH1cbiAgICBpZiAoc3RyZWFtLm1hdGNoKC9eXFxkW19cXGRdKihlW1xcK1xcLV0/XFxkKyk/L2kpKSB7XG4gICAgICBudW1iZXJMaXRlcmFsID0gdHJ1ZTtcbiAgICB9IC8vIERlY2ltYWxcbiAgICBpZiAobnVtYmVyTGl0ZXJhbCkge1xuICAgICAgLy8gSW50ZWdlciBsaXRlcmFscyBtYXkgYmUgXCJsb25nXCJcbiAgICAgIHN0cmVhbS5tYXRjaChpbU1hdGNoZXIpO1xuICAgICAgc3RhdGUubGVhdmluZ0V4cHIgPSB0cnVlO1xuICAgICAgcmV0dXJuIFwibnVtYmVyXCI7XG4gICAgfVxuICB9XG5cbiAgLy8gSGFuZGxlIENoYXJzXG4gIGlmIChzdHJlYW0ubWF0Y2goXCInXCIpKSB7XG4gICAgc3RhdGUudG9rZW5pemUgPSB0b2tlbkNoYXI7XG4gICAgcmV0dXJuIHN0YXRlLnRva2VuaXplKHN0cmVhbSwgc3RhdGUpO1xuICB9XG5cbiAgLy8gSGFuZGxlIFN0cmluZ3NcbiAgaWYgKHN0cmVhbS5tYXRjaChzdHJpbmdQcmVmaXhlcykpIHtcbiAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuU3RyaW5nRmFjdG9yeShzdHJlYW0uY3VycmVudCgpKTtcbiAgICByZXR1cm4gc3RhdGUudG9rZW5pemUoc3RyZWFtLCBzdGF0ZSk7XG4gIH1cbiAgaWYgKHN0cmVhbS5tYXRjaChtYWNybykgfHwgc3RyZWFtLm1hdGNoKG1hY3JvT3BlcmF0b3JzKSkge1xuICAgIHJldHVybiBcIm1ldGFcIjtcbiAgfVxuICBpZiAoc3RyZWFtLm1hdGNoKGRlbGltaXRlcnMpKSB7XG4gICAgcmV0dXJuIG51bGw7XG4gIH1cbiAgaWYgKHN0cmVhbS5tYXRjaChrZXl3b3JkcykpIHtcbiAgICByZXR1cm4gXCJrZXl3b3JkXCI7XG4gIH1cbiAgaWYgKHN0cmVhbS5tYXRjaChidWlsdGlucykpIHtcbiAgICByZXR1cm4gXCJidWlsdGluXCI7XG4gIH1cbiAgdmFyIGlzRGVmaW5pdGlvbiA9IHN0YXRlLmlzRGVmaW5pdGlvbiB8fCBzdGF0ZS5sYXN0VG9rZW4gPT0gXCJmdW5jdGlvblwiIHx8IHN0YXRlLmxhc3RUb2tlbiA9PSBcIm1hY3JvXCIgfHwgc3RhdGUubGFzdFRva2VuID09IFwidHlwZVwiIHx8IHN0YXRlLmxhc3RUb2tlbiA9PSBcInN0cnVjdFwiIHx8IHN0YXRlLmxhc3RUb2tlbiA9PSBcImltbXV0YWJsZVwiO1xuICBpZiAoc3RyZWFtLm1hdGNoKGlkZW50aWZpZXJzKSkge1xuICAgIGlmIChpc0RlZmluaXRpb24pIHtcbiAgICAgIGlmIChzdHJlYW0ucGVlaygpID09PSAnLicpIHtcbiAgICAgICAgc3RhdGUuaXNEZWZpbml0aW9uID0gdHJ1ZTtcbiAgICAgICAgcmV0dXJuIFwidmFyaWFibGVcIjtcbiAgICAgIH1cbiAgICAgIHN0YXRlLmlzRGVmaW5pdGlvbiA9IGZhbHNlO1xuICAgICAgcmV0dXJuIFwiZGVmXCI7XG4gICAgfVxuICAgIHN0YXRlLmxlYXZpbmdFeHByID0gdHJ1ZTtcbiAgICByZXR1cm4gXCJ2YXJpYWJsZVwiO1xuICB9XG5cbiAgLy8gSGFuZGxlIG5vbi1kZXRlY3RlZCBpdGVtc1xuICBzdHJlYW0ubmV4dCgpO1xuICByZXR1cm4gXCJlcnJvclwiO1xufVxuZnVuY3Rpb24gdG9rZW5Bbm5vdGF0aW9uKHN0cmVhbSwgc3RhdGUpIHtcbiAgc3RyZWFtLm1hdGNoKC8uKj8oPz1bLDt7fSgpPVxcc118JCkvKTtcbiAgaWYgKHN0cmVhbS5tYXRjaCgneycpKSB7XG4gICAgc3RhdGUubmVzdGVkUGFyYW1ldGVycysrO1xuICB9IGVsc2UgaWYgKHN0cmVhbS5tYXRjaCgnfScpICYmIHN0YXRlLm5lc3RlZFBhcmFtZXRlcnMgPiAwKSB7XG4gICAgc3RhdGUubmVzdGVkUGFyYW1ldGVycy0tO1xuICB9XG4gIGlmIChzdGF0ZS5uZXN0ZWRQYXJhbWV0ZXJzID4gMCkge1xuICAgIHN0cmVhbS5tYXRjaCgvLio/KD89e3x9KS8pIHx8IHN0cmVhbS5uZXh0KCk7XG4gIH0gZWxzZSBpZiAoc3RhdGUubmVzdGVkUGFyYW1ldGVycyA9PSAwKSB7XG4gICAgc3RhdGUudG9rZW5pemUgPSB0b2tlbkJhc2U7XG4gIH1cbiAgcmV0dXJuIFwiYnVpbHRpblwiO1xufVxuZnVuY3Rpb24gdG9rZW5Db21tZW50KHN0cmVhbSwgc3RhdGUpIHtcbiAgaWYgKHN0cmVhbS5tYXRjaCgnIz0nKSkge1xuICAgIHN0YXRlLm5lc3RlZENvbW1lbnRzKys7XG4gIH1cbiAgaWYgKCFzdHJlYW0ubWF0Y2goLy4qPyg/PSgjPXw9IykpLykpIHtcbiAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gIH1cbiAgaWYgKHN0cmVhbS5tYXRjaCgnPSMnKSkge1xuICAgIHN0YXRlLm5lc3RlZENvbW1lbnRzLS07XG4gICAgaWYgKHN0YXRlLm5lc3RlZENvbW1lbnRzID09IDApIHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlO1xuICB9XG4gIHJldHVybiBcImNvbW1lbnRcIjtcbn1cbmZ1bmN0aW9uIHRva2VuQ2hhcihzdHJlYW0sIHN0YXRlKSB7XG4gIHZhciBpc0NoYXIgPSBmYWxzZSxcbiAgICBtYXRjaDtcbiAgaWYgKHN0cmVhbS5tYXRjaChjaGFycykpIHtcbiAgICBpc0NoYXIgPSB0cnVlO1xuICB9IGVsc2UgaWYgKG1hdGNoID0gc3RyZWFtLm1hdGNoKC9cXFxcdShbYS1mMC05XXsxLDR9KSg/PScpL2kpKSB7XG4gICAgdmFyIHZhbHVlID0gcGFyc2VJbnQobWF0Y2hbMV0sIDE2KTtcbiAgICBpZiAodmFsdWUgPD0gNTUyOTUgfHwgdmFsdWUgPj0gNTczNDQpIHtcbiAgICAgIC8vIChVKzAsVStEN0ZGKSwgKFUrRTAwMCxVK0ZGRkYpXG4gICAgICBpc0NoYXIgPSB0cnVlO1xuICAgICAgc3RyZWFtLm5leHQoKTtcbiAgICB9XG4gIH0gZWxzZSBpZiAobWF0Y2ggPSBzdHJlYW0ubWF0Y2goL1xcXFxVKFtBLUZhLWYwLTldezUsOH0pKD89JykvKSkge1xuICAgIHZhciB2YWx1ZSA9IHBhcnNlSW50KG1hdGNoWzFdLCAxNik7XG4gICAgaWYgKHZhbHVlIDw9IDExMTQxMTEpIHtcbiAgICAgIC8vIFUrMTBGRkZGXG4gICAgICBpc0NoYXIgPSB0cnVlO1xuICAgICAgc3RyZWFtLm5leHQoKTtcbiAgICB9XG4gIH1cbiAgaWYgKGlzQ2hhcikge1xuICAgIHN0YXRlLmxlYXZpbmdFeHByID0gdHJ1ZTtcbiAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQmFzZTtcbiAgICByZXR1cm4gXCJzdHJpbmdcIjtcbiAgfVxuICBpZiAoIXN0cmVhbS5tYXRjaCgvXlteJ10rKD89JykvKSkge1xuICAgIHN0cmVhbS5za2lwVG9FbmQoKTtcbiAgfVxuICBpZiAoc3RyZWFtLm1hdGNoKFwiJ1wiKSkge1xuICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlO1xuICB9XG4gIHJldHVybiBcImVycm9yXCI7XG59XG5mdW5jdGlvbiB0b2tlblN0cmluZ0ZhY3RvcnkoZGVsaW1pdGVyKSB7XG4gIGlmIChkZWxpbWl0ZXIuc3Vic3RyKC0zKSA9PT0gJ1wiXCJcIicpIHtcbiAgICBkZWxpbWl0ZXIgPSAnXCJcIlwiJztcbiAgfSBlbHNlIGlmIChkZWxpbWl0ZXIuc3Vic3RyKC0xKSA9PT0gJ1wiJykge1xuICAgIGRlbGltaXRlciA9ICdcIic7XG4gIH1cbiAgZnVuY3Rpb24gdG9rZW5TdHJpbmcoc3RyZWFtLCBzdGF0ZSkge1xuICAgIGlmIChzdHJlYW0uZWF0KCdcXFxcJykpIHtcbiAgICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgfSBlbHNlIGlmIChzdHJlYW0ubWF0Y2goZGVsaW1pdGVyKSkge1xuICAgICAgc3RhdGUudG9rZW5pemUgPSB0b2tlbkJhc2U7XG4gICAgICBzdGF0ZS5sZWF2aW5nRXhwciA9IHRydWU7XG4gICAgICByZXR1cm4gXCJzdHJpbmdcIjtcbiAgICB9IGVsc2Uge1xuICAgICAgc3RyZWFtLmVhdCgvW2BcIl0vKTtcbiAgICB9XG4gICAgc3RyZWFtLmVhdFdoaWxlKC9bXlxcXFxgXCJdLyk7XG4gICAgcmV0dXJuIFwic3RyaW5nXCI7XG4gIH1cbiAgcmV0dXJuIHRva2VuU3RyaW5nO1xufVxuZXhwb3J0IGNvbnN0IGp1bGlhID0ge1xuICBuYW1lOiBcImp1bGlhXCIsXG4gIHN0YXJ0U3RhdGU6IGZ1bmN0aW9uICgpIHtcbiAgICByZXR1cm4ge1xuICAgICAgdG9rZW5pemU6IHRva2VuQmFzZSxcbiAgICAgIHNjb3BlczogW10sXG4gICAgICBsYXN0VG9rZW46IG51bGwsXG4gICAgICBsZWF2aW5nRXhwcjogZmFsc2UsXG4gICAgICBpc0RlZmluaXRpb246IGZhbHNlLFxuICAgICAgbmVzdGVkQXJyYXlzOiAwLFxuICAgICAgbmVzdGVkQ29tbWVudHM6IDAsXG4gICAgICBuZXN0ZWRHZW5lcmF0b3JzOiAwLFxuICAgICAgbmVzdGVkUGFyYW1ldGVyczogMCxcbiAgICAgIGZpcnN0UGFyZW5Qb3M6IC0xXG4gICAgfTtcbiAgfSxcbiAgdG9rZW46IGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgdmFyIHN0eWxlID0gc3RhdGUudG9rZW5pemUoc3RyZWFtLCBzdGF0ZSk7XG4gICAgdmFyIGN1cnJlbnQgPSBzdHJlYW0uY3VycmVudCgpO1xuICAgIGlmIChjdXJyZW50ICYmIHN0eWxlKSB7XG4gICAgICBzdGF0ZS5sYXN0VG9rZW4gPSBjdXJyZW50O1xuICAgIH1cbiAgICByZXR1cm4gc3R5bGU7XG4gIH0sXG4gIGluZGVudDogZnVuY3Rpb24gKHN0YXRlLCB0ZXh0QWZ0ZXIsIGN4KSB7XG4gICAgdmFyIGRlbHRhID0gMDtcbiAgICBpZiAodGV4dEFmdGVyID09PSAnXScgfHwgdGV4dEFmdGVyID09PSAnKScgfHwgL15lbmRcXGIvLnRlc3QodGV4dEFmdGVyKSB8fCAvXmVsc2UvLnRlc3QodGV4dEFmdGVyKSB8fCAvXmNhdGNoXFxiLy50ZXN0KHRleHRBZnRlcikgfHwgL15lbHNlaWZcXGIvLnRlc3QodGV4dEFmdGVyKSB8fCAvXmZpbmFsbHkvLnRlc3QodGV4dEFmdGVyKSkge1xuICAgICAgZGVsdGEgPSAtMTtcbiAgICB9XG4gICAgcmV0dXJuIChzdGF0ZS5zY29wZXMubGVuZ3RoICsgZGVsdGEpICogY3gudW5pdDtcbiAgfSxcbiAgbGFuZ3VhZ2VEYXRhOiB7XG4gICAgaW5kZW50T25JbnB1dDogL15cXHMqKGVuZHxlbHNlfGNhdGNofGZpbmFsbHkpXFxiJC8sXG4gICAgY29tbWVudFRva2Vuczoge1xuICAgICAgbGluZTogXCIjXCIsXG4gICAgICBibG9jazoge1xuICAgICAgICBvcGVuOiBcIiM9XCIsXG4gICAgICAgIGNsb3NlOiBcIj0jXCJcbiAgICAgIH1cbiAgICB9LFxuICAgIGNsb3NlQnJhY2tldHM6IHtcbiAgICAgIGJyYWNrZXRzOiBbXCIoXCIsIFwiW1wiLCBcIntcIiwgJ1wiJ11cbiAgICB9LFxuICAgIGF1dG9jb21wbGV0ZToga2V5d29yZHNMaXN0LmNvbmNhdChidWlsdGluc0xpc3QpXG4gIH1cbn07Il0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9