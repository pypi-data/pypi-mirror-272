"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[2604],{

/***/ 2604:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "dylan": () => (/* binding */ dylan)
/* harmony export */ });
function forEach(arr, f) {
  for (var i = 0; i < arr.length; i++) f(arr[i], i);
}
function some(arr, f) {
  for (var i = 0; i < arr.length; i++) if (f(arr[i], i)) return true;
  return false;
}

// Words
var words = {
  // Words that introduce unnamed definitions like "define interface"
  unnamedDefinition: ["interface"],
  // Words that introduce simple named definitions like "define library"
  namedDefinition: ["module", "library", "macro", "C-struct", "C-union", "C-function", "C-callable-wrapper"],
  // Words that introduce type definitions like "define class".
  // These are also parameterized like "define method" and are
  // appended to otherParameterizedDefinitionWords
  typeParameterizedDefinition: ["class", "C-subtype", "C-mapped-subtype"],
  // Words that introduce trickier definitions like "define method".
  // These require special definitions to be added to startExpressions
  otherParameterizedDefinition: ["method", "function", "C-variable", "C-address"],
  // Words that introduce module constant definitions.
  // These must also be simple definitions and are
  // appended to otherSimpleDefinitionWords
  constantSimpleDefinition: ["constant"],
  // Words that introduce module variable definitions.
  // These must also be simple definitions and are
  // appended to otherSimpleDefinitionWords
  variableSimpleDefinition: ["variable"],
  // Other words that introduce simple definitions
  // (without implicit bodies).
  otherSimpleDefinition: ["generic", "domain", "C-pointer-type", "table"],
  // Words that begin statements with implicit bodies.
  statement: ["if", "block", "begin", "method", "case", "for", "select", "when", "unless", "until", "while", "iterate", "profiling", "dynamic-bind"],
  // Patterns that act as separators in compound statements.
  // This may include any general pattern that must be indented
  // specially.
  separator: ["finally", "exception", "cleanup", "else", "elseif", "afterwards"],
  // Keywords that do not require special indentation handling,
  // but which should be highlighted
  other: ["above", "below", "by", "from", "handler", "in", "instance", "let", "local", "otherwise", "slot", "subclass", "then", "to", "keyed-by", "virtual"],
  // Condition signaling function calls
  signalingCalls: ["signal", "error", "cerror", "break", "check-type", "abort"]
};
words["otherDefinition"] = words["unnamedDefinition"].concat(words["namedDefinition"]).concat(words["otherParameterizedDefinition"]);
words["definition"] = words["typeParameterizedDefinition"].concat(words["otherDefinition"]);
words["parameterizedDefinition"] = words["typeParameterizedDefinition"].concat(words["otherParameterizedDefinition"]);
words["simpleDefinition"] = words["constantSimpleDefinition"].concat(words["variableSimpleDefinition"]).concat(words["otherSimpleDefinition"]);
words["keyword"] = words["statement"].concat(words["separator"]).concat(words["other"]);

// Patterns
var symbolPattern = "[-_a-zA-Z?!*@<>$%]+";
var symbol = new RegExp("^" + symbolPattern);
var patterns = {
  // Symbols with special syntax
  symbolKeyword: symbolPattern + ":",
  symbolClass: "<" + symbolPattern + ">",
  symbolGlobal: "\\*" + symbolPattern + "\\*",
  symbolConstant: "\\$" + symbolPattern
};
var patternStyles = {
  symbolKeyword: "atom",
  symbolClass: "tag",
  symbolGlobal: "variableName.standard",
  symbolConstant: "variableName.constant"
};

// Compile all patterns to regular expressions
for (var patternName in patterns) if (patterns.hasOwnProperty(patternName)) patterns[patternName] = new RegExp("^" + patterns[patternName]);

// Names beginning "with-" and "without-" are commonly
// used as statement macro
patterns["keyword"] = [/^with(?:out)?-[-_a-zA-Z?!*@<>$%]+/];
var styles = {};
styles["keyword"] = "keyword";
styles["definition"] = "def";
styles["simpleDefinition"] = "def";
styles["signalingCalls"] = "builtin";

// protected words lookup table
var wordLookup = {};
var styleLookup = {};
forEach(["keyword", "definition", "simpleDefinition", "signalingCalls"], function (type) {
  forEach(words[type], function (word) {
    wordLookup[word] = type;
    styleLookup[word] = styles[type];
  });
});
function chain(stream, state, f) {
  state.tokenize = f;
  return f(stream, state);
}
function tokenBase(stream, state) {
  // String
  var ch = stream.peek();
  if (ch == "'" || ch == '"') {
    stream.next();
    return chain(stream, state, tokenString(ch, "string"));
  }
  // Comment
  else if (ch == "/") {
    stream.next();
    if (stream.eat("*")) {
      return chain(stream, state, tokenComment);
    } else if (stream.eat("/")) {
      stream.skipToEnd();
      return "comment";
    }
    stream.backUp(1);
  }
  // Decimal
  else if (/[+\-\d\.]/.test(ch)) {
    if (stream.match(/^[+-]?[0-9]*\.[0-9]*([esdx][+-]?[0-9]+)?/i) || stream.match(/^[+-]?[0-9]+([esdx][+-]?[0-9]+)/i) || stream.match(/^[+-]?\d+/)) {
      return "number";
    }
  }
  // Hash
  else if (ch == "#") {
    stream.next();
    // Symbol with string syntax
    ch = stream.peek();
    if (ch == '"') {
      stream.next();
      return chain(stream, state, tokenString('"', "string"));
    }
    // Binary number
    else if (ch == "b") {
      stream.next();
      stream.eatWhile(/[01]/);
      return "number";
    }
    // Hex number
    else if (ch == "x") {
      stream.next();
      stream.eatWhile(/[\da-f]/i);
      return "number";
    }
    // Octal number
    else if (ch == "o") {
      stream.next();
      stream.eatWhile(/[0-7]/);
      return "number";
    }
    // Token concatenation in macros
    else if (ch == '#') {
      stream.next();
      return "punctuation";
    }
    // Sequence literals
    else if (ch == '[' || ch == '(') {
      stream.next();
      return "bracket";
      // Hash symbol
    } else if (stream.match(/f|t|all-keys|include|key|next|rest/i)) {
      return "atom";
    } else {
      stream.eatWhile(/[-a-zA-Z]/);
      return "error";
    }
  } else if (ch == "~") {
    stream.next();
    ch = stream.peek();
    if (ch == "=") {
      stream.next();
      ch = stream.peek();
      if (ch == "=") {
        stream.next();
        return "operator";
      }
      return "operator";
    }
    return "operator";
  } else if (ch == ":") {
    stream.next();
    ch = stream.peek();
    if (ch == "=") {
      stream.next();
      return "operator";
    } else if (ch == ":") {
      stream.next();
      return "punctuation";
    }
  } else if ("[](){}".indexOf(ch) != -1) {
    stream.next();
    return "bracket";
  } else if (".,".indexOf(ch) != -1) {
    stream.next();
    return "punctuation";
  } else if (stream.match("end")) {
    return "keyword";
  }
  for (var name in patterns) {
    if (patterns.hasOwnProperty(name)) {
      var pattern = patterns[name];
      if (pattern instanceof Array && some(pattern, function (p) {
        return stream.match(p);
      }) || stream.match(pattern)) return patternStyles[name];
    }
  }
  if (/[+\-*\/^=<>&|]/.test(ch)) {
    stream.next();
    return "operator";
  }
  if (stream.match("define")) {
    return "def";
  } else {
    stream.eatWhile(/[\w\-]/);
    // Keyword
    if (wordLookup.hasOwnProperty(stream.current())) {
      return styleLookup[stream.current()];
    } else if (stream.current().match(symbol)) {
      return "variable";
    } else {
      stream.next();
      return "variableName.standard";
    }
  }
}
function tokenComment(stream, state) {
  var maybeEnd = false,
    maybeNested = false,
    nestedCount = 0,
    ch;
  while (ch = stream.next()) {
    if (ch == "/" && maybeEnd) {
      if (nestedCount > 0) {
        nestedCount--;
      } else {
        state.tokenize = tokenBase;
        break;
      }
    } else if (ch == "*" && maybeNested) {
      nestedCount++;
    }
    maybeEnd = ch == "*";
    maybeNested = ch == "/";
  }
  return "comment";
}
function tokenString(quote, style) {
  return function (stream, state) {
    var escaped = false,
      next,
      end = false;
    while ((next = stream.next()) != null) {
      if (next == quote && !escaped) {
        end = true;
        break;
      }
      escaped = !escaped && next == "\\";
    }
    if (end || !escaped) {
      state.tokenize = tokenBase;
    }
    return style;
  };
}

// Interface
const dylan = {
  name: "dylan",
  startState: function () {
    return {
      tokenize: tokenBase,
      currentIndent: 0
    };
  },
  token: function (stream, state) {
    if (stream.eatSpace()) return null;
    var style = state.tokenize(stream, state);
    return style;
  },
  languageData: {
    commentTokens: {
      block: {
        open: "/*",
        close: "*/"
      }
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiMjYwNC5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGNvZGVtaXJyb3IvbGVnYWN5LW1vZGVzL21vZGUvZHlsYW4uanMiXSwic291cmNlc0NvbnRlbnQiOlsiZnVuY3Rpb24gZm9yRWFjaChhcnIsIGYpIHtcbiAgZm9yICh2YXIgaSA9IDA7IGkgPCBhcnIubGVuZ3RoOyBpKyspIGYoYXJyW2ldLCBpKTtcbn1cbmZ1bmN0aW9uIHNvbWUoYXJyLCBmKSB7XG4gIGZvciAodmFyIGkgPSAwOyBpIDwgYXJyLmxlbmd0aDsgaSsrKSBpZiAoZihhcnJbaV0sIGkpKSByZXR1cm4gdHJ1ZTtcbiAgcmV0dXJuIGZhbHNlO1xufVxuXG4vLyBXb3Jkc1xudmFyIHdvcmRzID0ge1xuICAvLyBXb3JkcyB0aGF0IGludHJvZHVjZSB1bm5hbWVkIGRlZmluaXRpb25zIGxpa2UgXCJkZWZpbmUgaW50ZXJmYWNlXCJcbiAgdW5uYW1lZERlZmluaXRpb246IFtcImludGVyZmFjZVwiXSxcbiAgLy8gV29yZHMgdGhhdCBpbnRyb2R1Y2Ugc2ltcGxlIG5hbWVkIGRlZmluaXRpb25zIGxpa2UgXCJkZWZpbmUgbGlicmFyeVwiXG4gIG5hbWVkRGVmaW5pdGlvbjogW1wibW9kdWxlXCIsIFwibGlicmFyeVwiLCBcIm1hY3JvXCIsIFwiQy1zdHJ1Y3RcIiwgXCJDLXVuaW9uXCIsIFwiQy1mdW5jdGlvblwiLCBcIkMtY2FsbGFibGUtd3JhcHBlclwiXSxcbiAgLy8gV29yZHMgdGhhdCBpbnRyb2R1Y2UgdHlwZSBkZWZpbml0aW9ucyBsaWtlIFwiZGVmaW5lIGNsYXNzXCIuXG4gIC8vIFRoZXNlIGFyZSBhbHNvIHBhcmFtZXRlcml6ZWQgbGlrZSBcImRlZmluZSBtZXRob2RcIiBhbmQgYXJlXG4gIC8vIGFwcGVuZGVkIHRvIG90aGVyUGFyYW1ldGVyaXplZERlZmluaXRpb25Xb3Jkc1xuICB0eXBlUGFyYW1ldGVyaXplZERlZmluaXRpb246IFtcImNsYXNzXCIsIFwiQy1zdWJ0eXBlXCIsIFwiQy1tYXBwZWQtc3VidHlwZVwiXSxcbiAgLy8gV29yZHMgdGhhdCBpbnRyb2R1Y2UgdHJpY2tpZXIgZGVmaW5pdGlvbnMgbGlrZSBcImRlZmluZSBtZXRob2RcIi5cbiAgLy8gVGhlc2UgcmVxdWlyZSBzcGVjaWFsIGRlZmluaXRpb25zIHRvIGJlIGFkZGVkIHRvIHN0YXJ0RXhwcmVzc2lvbnNcbiAgb3RoZXJQYXJhbWV0ZXJpemVkRGVmaW5pdGlvbjogW1wibWV0aG9kXCIsIFwiZnVuY3Rpb25cIiwgXCJDLXZhcmlhYmxlXCIsIFwiQy1hZGRyZXNzXCJdLFxuICAvLyBXb3JkcyB0aGF0IGludHJvZHVjZSBtb2R1bGUgY29uc3RhbnQgZGVmaW5pdGlvbnMuXG4gIC8vIFRoZXNlIG11c3QgYWxzbyBiZSBzaW1wbGUgZGVmaW5pdGlvbnMgYW5kIGFyZVxuICAvLyBhcHBlbmRlZCB0byBvdGhlclNpbXBsZURlZmluaXRpb25Xb3Jkc1xuICBjb25zdGFudFNpbXBsZURlZmluaXRpb246IFtcImNvbnN0YW50XCJdLFxuICAvLyBXb3JkcyB0aGF0IGludHJvZHVjZSBtb2R1bGUgdmFyaWFibGUgZGVmaW5pdGlvbnMuXG4gIC8vIFRoZXNlIG11c3QgYWxzbyBiZSBzaW1wbGUgZGVmaW5pdGlvbnMgYW5kIGFyZVxuICAvLyBhcHBlbmRlZCB0byBvdGhlclNpbXBsZURlZmluaXRpb25Xb3Jkc1xuICB2YXJpYWJsZVNpbXBsZURlZmluaXRpb246IFtcInZhcmlhYmxlXCJdLFxuICAvLyBPdGhlciB3b3JkcyB0aGF0IGludHJvZHVjZSBzaW1wbGUgZGVmaW5pdGlvbnNcbiAgLy8gKHdpdGhvdXQgaW1wbGljaXQgYm9kaWVzKS5cbiAgb3RoZXJTaW1wbGVEZWZpbml0aW9uOiBbXCJnZW5lcmljXCIsIFwiZG9tYWluXCIsIFwiQy1wb2ludGVyLXR5cGVcIiwgXCJ0YWJsZVwiXSxcbiAgLy8gV29yZHMgdGhhdCBiZWdpbiBzdGF0ZW1lbnRzIHdpdGggaW1wbGljaXQgYm9kaWVzLlxuICBzdGF0ZW1lbnQ6IFtcImlmXCIsIFwiYmxvY2tcIiwgXCJiZWdpblwiLCBcIm1ldGhvZFwiLCBcImNhc2VcIiwgXCJmb3JcIiwgXCJzZWxlY3RcIiwgXCJ3aGVuXCIsIFwidW5sZXNzXCIsIFwidW50aWxcIiwgXCJ3aGlsZVwiLCBcIml0ZXJhdGVcIiwgXCJwcm9maWxpbmdcIiwgXCJkeW5hbWljLWJpbmRcIl0sXG4gIC8vIFBhdHRlcm5zIHRoYXQgYWN0IGFzIHNlcGFyYXRvcnMgaW4gY29tcG91bmQgc3RhdGVtZW50cy5cbiAgLy8gVGhpcyBtYXkgaW5jbHVkZSBhbnkgZ2VuZXJhbCBwYXR0ZXJuIHRoYXQgbXVzdCBiZSBpbmRlbnRlZFxuICAvLyBzcGVjaWFsbHkuXG4gIHNlcGFyYXRvcjogW1wiZmluYWxseVwiLCBcImV4Y2VwdGlvblwiLCBcImNsZWFudXBcIiwgXCJlbHNlXCIsIFwiZWxzZWlmXCIsIFwiYWZ0ZXJ3YXJkc1wiXSxcbiAgLy8gS2V5d29yZHMgdGhhdCBkbyBub3QgcmVxdWlyZSBzcGVjaWFsIGluZGVudGF0aW9uIGhhbmRsaW5nLFxuICAvLyBidXQgd2hpY2ggc2hvdWxkIGJlIGhpZ2hsaWdodGVkXG4gIG90aGVyOiBbXCJhYm92ZVwiLCBcImJlbG93XCIsIFwiYnlcIiwgXCJmcm9tXCIsIFwiaGFuZGxlclwiLCBcImluXCIsIFwiaW5zdGFuY2VcIiwgXCJsZXRcIiwgXCJsb2NhbFwiLCBcIm90aGVyd2lzZVwiLCBcInNsb3RcIiwgXCJzdWJjbGFzc1wiLCBcInRoZW5cIiwgXCJ0b1wiLCBcImtleWVkLWJ5XCIsIFwidmlydHVhbFwiXSxcbiAgLy8gQ29uZGl0aW9uIHNpZ25hbGluZyBmdW5jdGlvbiBjYWxsc1xuICBzaWduYWxpbmdDYWxsczogW1wic2lnbmFsXCIsIFwiZXJyb3JcIiwgXCJjZXJyb3JcIiwgXCJicmVha1wiLCBcImNoZWNrLXR5cGVcIiwgXCJhYm9ydFwiXVxufTtcbndvcmRzW1wib3RoZXJEZWZpbml0aW9uXCJdID0gd29yZHNbXCJ1bm5hbWVkRGVmaW5pdGlvblwiXS5jb25jYXQod29yZHNbXCJuYW1lZERlZmluaXRpb25cIl0pLmNvbmNhdCh3b3Jkc1tcIm90aGVyUGFyYW1ldGVyaXplZERlZmluaXRpb25cIl0pO1xud29yZHNbXCJkZWZpbml0aW9uXCJdID0gd29yZHNbXCJ0eXBlUGFyYW1ldGVyaXplZERlZmluaXRpb25cIl0uY29uY2F0KHdvcmRzW1wib3RoZXJEZWZpbml0aW9uXCJdKTtcbndvcmRzW1wicGFyYW1ldGVyaXplZERlZmluaXRpb25cIl0gPSB3b3Jkc1tcInR5cGVQYXJhbWV0ZXJpemVkRGVmaW5pdGlvblwiXS5jb25jYXQod29yZHNbXCJvdGhlclBhcmFtZXRlcml6ZWREZWZpbml0aW9uXCJdKTtcbndvcmRzW1wic2ltcGxlRGVmaW5pdGlvblwiXSA9IHdvcmRzW1wiY29uc3RhbnRTaW1wbGVEZWZpbml0aW9uXCJdLmNvbmNhdCh3b3Jkc1tcInZhcmlhYmxlU2ltcGxlRGVmaW5pdGlvblwiXSkuY29uY2F0KHdvcmRzW1wib3RoZXJTaW1wbGVEZWZpbml0aW9uXCJdKTtcbndvcmRzW1wia2V5d29yZFwiXSA9IHdvcmRzW1wic3RhdGVtZW50XCJdLmNvbmNhdCh3b3Jkc1tcInNlcGFyYXRvclwiXSkuY29uY2F0KHdvcmRzW1wib3RoZXJcIl0pO1xuXG4vLyBQYXR0ZXJuc1xudmFyIHN5bWJvbFBhdHRlcm4gPSBcIlstX2EtekEtWj8hKkA8PiQlXStcIjtcbnZhciBzeW1ib2wgPSBuZXcgUmVnRXhwKFwiXlwiICsgc3ltYm9sUGF0dGVybik7XG52YXIgcGF0dGVybnMgPSB7XG4gIC8vIFN5bWJvbHMgd2l0aCBzcGVjaWFsIHN5bnRheFxuICBzeW1ib2xLZXl3b3JkOiBzeW1ib2xQYXR0ZXJuICsgXCI6XCIsXG4gIHN5bWJvbENsYXNzOiBcIjxcIiArIHN5bWJvbFBhdHRlcm4gKyBcIj5cIixcbiAgc3ltYm9sR2xvYmFsOiBcIlxcXFwqXCIgKyBzeW1ib2xQYXR0ZXJuICsgXCJcXFxcKlwiLFxuICBzeW1ib2xDb25zdGFudDogXCJcXFxcJFwiICsgc3ltYm9sUGF0dGVyblxufTtcbnZhciBwYXR0ZXJuU3R5bGVzID0ge1xuICBzeW1ib2xLZXl3b3JkOiBcImF0b21cIixcbiAgc3ltYm9sQ2xhc3M6IFwidGFnXCIsXG4gIHN5bWJvbEdsb2JhbDogXCJ2YXJpYWJsZU5hbWUuc3RhbmRhcmRcIixcbiAgc3ltYm9sQ29uc3RhbnQ6IFwidmFyaWFibGVOYW1lLmNvbnN0YW50XCJcbn07XG5cbi8vIENvbXBpbGUgYWxsIHBhdHRlcm5zIHRvIHJlZ3VsYXIgZXhwcmVzc2lvbnNcbmZvciAodmFyIHBhdHRlcm5OYW1lIGluIHBhdHRlcm5zKSBpZiAocGF0dGVybnMuaGFzT3duUHJvcGVydHkocGF0dGVybk5hbWUpKSBwYXR0ZXJuc1twYXR0ZXJuTmFtZV0gPSBuZXcgUmVnRXhwKFwiXlwiICsgcGF0dGVybnNbcGF0dGVybk5hbWVdKTtcblxuLy8gTmFtZXMgYmVnaW5uaW5nIFwid2l0aC1cIiBhbmQgXCJ3aXRob3V0LVwiIGFyZSBjb21tb25seVxuLy8gdXNlZCBhcyBzdGF0ZW1lbnQgbWFjcm9cbnBhdHRlcm5zW1wia2V5d29yZFwiXSA9IFsvXndpdGgoPzpvdXQpPy1bLV9hLXpBLVo/ISpAPD4kJV0rL107XG52YXIgc3R5bGVzID0ge307XG5zdHlsZXNbXCJrZXl3b3JkXCJdID0gXCJrZXl3b3JkXCI7XG5zdHlsZXNbXCJkZWZpbml0aW9uXCJdID0gXCJkZWZcIjtcbnN0eWxlc1tcInNpbXBsZURlZmluaXRpb25cIl0gPSBcImRlZlwiO1xuc3R5bGVzW1wic2lnbmFsaW5nQ2FsbHNcIl0gPSBcImJ1aWx0aW5cIjtcblxuLy8gcHJvdGVjdGVkIHdvcmRzIGxvb2t1cCB0YWJsZVxudmFyIHdvcmRMb29rdXAgPSB7fTtcbnZhciBzdHlsZUxvb2t1cCA9IHt9O1xuZm9yRWFjaChbXCJrZXl3b3JkXCIsIFwiZGVmaW5pdGlvblwiLCBcInNpbXBsZURlZmluaXRpb25cIiwgXCJzaWduYWxpbmdDYWxsc1wiXSwgZnVuY3Rpb24gKHR5cGUpIHtcbiAgZm9yRWFjaCh3b3Jkc1t0eXBlXSwgZnVuY3Rpb24gKHdvcmQpIHtcbiAgICB3b3JkTG9va3VwW3dvcmRdID0gdHlwZTtcbiAgICBzdHlsZUxvb2t1cFt3b3JkXSA9IHN0eWxlc1t0eXBlXTtcbiAgfSk7XG59KTtcbmZ1bmN0aW9uIGNoYWluKHN0cmVhbSwgc3RhdGUsIGYpIHtcbiAgc3RhdGUudG9rZW5pemUgPSBmO1xuICByZXR1cm4gZihzdHJlYW0sIHN0YXRlKTtcbn1cbmZ1bmN0aW9uIHRva2VuQmFzZShzdHJlYW0sIHN0YXRlKSB7XG4gIC8vIFN0cmluZ1xuICB2YXIgY2ggPSBzdHJlYW0ucGVlaygpO1xuICBpZiAoY2ggPT0gXCInXCIgfHwgY2ggPT0gJ1wiJykge1xuICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgcmV0dXJuIGNoYWluKHN0cmVhbSwgc3RhdGUsIHRva2VuU3RyaW5nKGNoLCBcInN0cmluZ1wiKSk7XG4gIH1cbiAgLy8gQ29tbWVudFxuICBlbHNlIGlmIChjaCA9PSBcIi9cIikge1xuICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgaWYgKHN0cmVhbS5lYXQoXCIqXCIpKSB7XG4gICAgICByZXR1cm4gY2hhaW4oc3RyZWFtLCBzdGF0ZSwgdG9rZW5Db21tZW50KTtcbiAgICB9IGVsc2UgaWYgKHN0cmVhbS5lYXQoXCIvXCIpKSB7XG4gICAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgICByZXR1cm4gXCJjb21tZW50XCI7XG4gICAgfVxuICAgIHN0cmVhbS5iYWNrVXAoMSk7XG4gIH1cbiAgLy8gRGVjaW1hbFxuICBlbHNlIGlmICgvWytcXC1cXGRcXC5dLy50ZXN0KGNoKSkge1xuICAgIGlmIChzdHJlYW0ubWF0Y2goL15bKy1dP1swLTldKlxcLlswLTldKihbZXNkeF1bKy1dP1swLTldKyk/L2kpIHx8IHN0cmVhbS5tYXRjaCgvXlsrLV0/WzAtOV0rKFtlc2R4XVsrLV0/WzAtOV0rKS9pKSB8fCBzdHJlYW0ubWF0Y2goL15bKy1dP1xcZCsvKSkge1xuICAgICAgcmV0dXJuIFwibnVtYmVyXCI7XG4gICAgfVxuICB9XG4gIC8vIEhhc2hcbiAgZWxzZSBpZiAoY2ggPT0gXCIjXCIpIHtcbiAgICBzdHJlYW0ubmV4dCgpO1xuICAgIC8vIFN5bWJvbCB3aXRoIHN0cmluZyBzeW50YXhcbiAgICBjaCA9IHN0cmVhbS5wZWVrKCk7XG4gICAgaWYgKGNoID09ICdcIicpIHtcbiAgICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgICByZXR1cm4gY2hhaW4oc3RyZWFtLCBzdGF0ZSwgdG9rZW5TdHJpbmcoJ1wiJywgXCJzdHJpbmdcIikpO1xuICAgIH1cbiAgICAvLyBCaW5hcnkgbnVtYmVyXG4gICAgZWxzZSBpZiAoY2ggPT0gXCJiXCIpIHtcbiAgICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgICBzdHJlYW0uZWF0V2hpbGUoL1swMV0vKTtcbiAgICAgIHJldHVybiBcIm51bWJlclwiO1xuICAgIH1cbiAgICAvLyBIZXggbnVtYmVyXG4gICAgZWxzZSBpZiAoY2ggPT0gXCJ4XCIpIHtcbiAgICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgICBzdHJlYW0uZWF0V2hpbGUoL1tcXGRhLWZdL2kpO1xuICAgICAgcmV0dXJuIFwibnVtYmVyXCI7XG4gICAgfVxuICAgIC8vIE9jdGFsIG51bWJlclxuICAgIGVsc2UgaWYgKGNoID09IFwib1wiKSB7XG4gICAgICBzdHJlYW0ubmV4dCgpO1xuICAgICAgc3RyZWFtLmVhdFdoaWxlKC9bMC03XS8pO1xuICAgICAgcmV0dXJuIFwibnVtYmVyXCI7XG4gICAgfVxuICAgIC8vIFRva2VuIGNvbmNhdGVuYXRpb24gaW4gbWFjcm9zXG4gICAgZWxzZSBpZiAoY2ggPT0gJyMnKSB7XG4gICAgICBzdHJlYW0ubmV4dCgpO1xuICAgICAgcmV0dXJuIFwicHVuY3R1YXRpb25cIjtcbiAgICB9XG4gICAgLy8gU2VxdWVuY2UgbGl0ZXJhbHNcbiAgICBlbHNlIGlmIChjaCA9PSAnWycgfHwgY2ggPT0gJygnKSB7XG4gICAgICBzdHJlYW0ubmV4dCgpO1xuICAgICAgcmV0dXJuIFwiYnJhY2tldFwiO1xuICAgICAgLy8gSGFzaCBzeW1ib2xcbiAgICB9IGVsc2UgaWYgKHN0cmVhbS5tYXRjaCgvZnx0fGFsbC1rZXlzfGluY2x1ZGV8a2V5fG5leHR8cmVzdC9pKSkge1xuICAgICAgcmV0dXJuIFwiYXRvbVwiO1xuICAgIH0gZWxzZSB7XG4gICAgICBzdHJlYW0uZWF0V2hpbGUoL1stYS16QS1aXS8pO1xuICAgICAgcmV0dXJuIFwiZXJyb3JcIjtcbiAgICB9XG4gIH0gZWxzZSBpZiAoY2ggPT0gXCJ+XCIpIHtcbiAgICBzdHJlYW0ubmV4dCgpO1xuICAgIGNoID0gc3RyZWFtLnBlZWsoKTtcbiAgICBpZiAoY2ggPT0gXCI9XCIpIHtcbiAgICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgICBjaCA9IHN0cmVhbS5wZWVrKCk7XG4gICAgICBpZiAoY2ggPT0gXCI9XCIpIHtcbiAgICAgICAgc3RyZWFtLm5leHQoKTtcbiAgICAgICAgcmV0dXJuIFwib3BlcmF0b3JcIjtcbiAgICAgIH1cbiAgICAgIHJldHVybiBcIm9wZXJhdG9yXCI7XG4gICAgfVxuICAgIHJldHVybiBcIm9wZXJhdG9yXCI7XG4gIH0gZWxzZSBpZiAoY2ggPT0gXCI6XCIpIHtcbiAgICBzdHJlYW0ubmV4dCgpO1xuICAgIGNoID0gc3RyZWFtLnBlZWsoKTtcbiAgICBpZiAoY2ggPT0gXCI9XCIpIHtcbiAgICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgICByZXR1cm4gXCJvcGVyYXRvclwiO1xuICAgIH0gZWxzZSBpZiAoY2ggPT0gXCI6XCIpIHtcbiAgICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgICByZXR1cm4gXCJwdW5jdHVhdGlvblwiO1xuICAgIH1cbiAgfSBlbHNlIGlmIChcIltdKCl7fVwiLmluZGV4T2YoY2gpICE9IC0xKSB7XG4gICAgc3RyZWFtLm5leHQoKTtcbiAgICByZXR1cm4gXCJicmFja2V0XCI7XG4gIH0gZWxzZSBpZiAoXCIuLFwiLmluZGV4T2YoY2gpICE9IC0xKSB7XG4gICAgc3RyZWFtLm5leHQoKTtcbiAgICByZXR1cm4gXCJwdW5jdHVhdGlvblwiO1xuICB9IGVsc2UgaWYgKHN0cmVhbS5tYXRjaChcImVuZFwiKSkge1xuICAgIHJldHVybiBcImtleXdvcmRcIjtcbiAgfVxuICBmb3IgKHZhciBuYW1lIGluIHBhdHRlcm5zKSB7XG4gICAgaWYgKHBhdHRlcm5zLmhhc093blByb3BlcnR5KG5hbWUpKSB7XG4gICAgICB2YXIgcGF0dGVybiA9IHBhdHRlcm5zW25hbWVdO1xuICAgICAgaWYgKHBhdHRlcm4gaW5zdGFuY2VvZiBBcnJheSAmJiBzb21lKHBhdHRlcm4sIGZ1bmN0aW9uIChwKSB7XG4gICAgICAgIHJldHVybiBzdHJlYW0ubWF0Y2gocCk7XG4gICAgICB9KSB8fCBzdHJlYW0ubWF0Y2gocGF0dGVybikpIHJldHVybiBwYXR0ZXJuU3R5bGVzW25hbWVdO1xuICAgIH1cbiAgfVxuICBpZiAoL1srXFwtKlxcL149PD4mfF0vLnRlc3QoY2gpKSB7XG4gICAgc3RyZWFtLm5leHQoKTtcbiAgICByZXR1cm4gXCJvcGVyYXRvclwiO1xuICB9XG4gIGlmIChzdHJlYW0ubWF0Y2goXCJkZWZpbmVcIikpIHtcbiAgICByZXR1cm4gXCJkZWZcIjtcbiAgfSBlbHNlIHtcbiAgICBzdHJlYW0uZWF0V2hpbGUoL1tcXHdcXC1dLyk7XG4gICAgLy8gS2V5d29yZFxuICAgIGlmICh3b3JkTG9va3VwLmhhc093blByb3BlcnR5KHN0cmVhbS5jdXJyZW50KCkpKSB7XG4gICAgICByZXR1cm4gc3R5bGVMb29rdXBbc3RyZWFtLmN1cnJlbnQoKV07XG4gICAgfSBlbHNlIGlmIChzdHJlYW0uY3VycmVudCgpLm1hdGNoKHN5bWJvbCkpIHtcbiAgICAgIHJldHVybiBcInZhcmlhYmxlXCI7XG4gICAgfSBlbHNlIHtcbiAgICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgICByZXR1cm4gXCJ2YXJpYWJsZU5hbWUuc3RhbmRhcmRcIjtcbiAgICB9XG4gIH1cbn1cbmZ1bmN0aW9uIHRva2VuQ29tbWVudChzdHJlYW0sIHN0YXRlKSB7XG4gIHZhciBtYXliZUVuZCA9IGZhbHNlLFxuICAgIG1heWJlTmVzdGVkID0gZmFsc2UsXG4gICAgbmVzdGVkQ291bnQgPSAwLFxuICAgIGNoO1xuICB3aGlsZSAoY2ggPSBzdHJlYW0ubmV4dCgpKSB7XG4gICAgaWYgKGNoID09IFwiL1wiICYmIG1heWJlRW5kKSB7XG4gICAgICBpZiAobmVzdGVkQ291bnQgPiAwKSB7XG4gICAgICAgIG5lc3RlZENvdW50LS07XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQmFzZTtcbiAgICAgICAgYnJlYWs7XG4gICAgICB9XG4gICAgfSBlbHNlIGlmIChjaCA9PSBcIipcIiAmJiBtYXliZU5lc3RlZCkge1xuICAgICAgbmVzdGVkQ291bnQrKztcbiAgICB9XG4gICAgbWF5YmVFbmQgPSBjaCA9PSBcIipcIjtcbiAgICBtYXliZU5lc3RlZCA9IGNoID09IFwiL1wiO1xuICB9XG4gIHJldHVybiBcImNvbW1lbnRcIjtcbn1cbmZ1bmN0aW9uIHRva2VuU3RyaW5nKHF1b3RlLCBzdHlsZSkge1xuICByZXR1cm4gZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICB2YXIgZXNjYXBlZCA9IGZhbHNlLFxuICAgICAgbmV4dCxcbiAgICAgIGVuZCA9IGZhbHNlO1xuICAgIHdoaWxlICgobmV4dCA9IHN0cmVhbS5uZXh0KCkpICE9IG51bGwpIHtcbiAgICAgIGlmIChuZXh0ID09IHF1b3RlICYmICFlc2NhcGVkKSB7XG4gICAgICAgIGVuZCA9IHRydWU7XG4gICAgICAgIGJyZWFrO1xuICAgICAgfVxuICAgICAgZXNjYXBlZCA9ICFlc2NhcGVkICYmIG5leHQgPT0gXCJcXFxcXCI7XG4gICAgfVxuICAgIGlmIChlbmQgfHwgIWVzY2FwZWQpIHtcbiAgICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlO1xuICAgIH1cbiAgICByZXR1cm4gc3R5bGU7XG4gIH07XG59XG5cbi8vIEludGVyZmFjZVxuZXhwb3J0IGNvbnN0IGR5bGFuID0ge1xuICBuYW1lOiBcImR5bGFuXCIsXG4gIHN0YXJ0U3RhdGU6IGZ1bmN0aW9uICgpIHtcbiAgICByZXR1cm4ge1xuICAgICAgdG9rZW5pemU6IHRva2VuQmFzZSxcbiAgICAgIGN1cnJlbnRJbmRlbnQ6IDBcbiAgICB9O1xuICB9LFxuICB0b2tlbjogZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICBpZiAoc3RyZWFtLmVhdFNwYWNlKCkpIHJldHVybiBudWxsO1xuICAgIHZhciBzdHlsZSA9IHN0YXRlLnRva2VuaXplKHN0cmVhbSwgc3RhdGUpO1xuICAgIHJldHVybiBzdHlsZTtcbiAgfSxcbiAgbGFuZ3VhZ2VEYXRhOiB7XG4gICAgY29tbWVudFRva2Vuczoge1xuICAgICAgYmxvY2s6IHtcbiAgICAgICAgb3BlbjogXCIvKlwiLFxuICAgICAgICBjbG9zZTogXCIqL1wiXG4gICAgICB9XG4gICAgfVxuICB9XG59OyJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==