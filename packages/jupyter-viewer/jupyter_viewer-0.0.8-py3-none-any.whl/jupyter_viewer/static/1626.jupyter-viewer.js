"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[1626],{

/***/ 51626:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "crystal": () => (/* binding */ crystal)
/* harmony export */ });
function wordRegExp(words, end) {
  return new RegExp((end ? "" : "^") + "(?:" + words.join("|") + ")" + (end ? "$" : "\\b"));
}
function chain(tokenize, stream, state) {
  state.tokenize.push(tokenize);
  return tokenize(stream, state);
}
var operators = /^(?:[-+/%|&^]|\*\*?|[<>]{2})/;
var conditionalOperators = /^(?:[=!]~|===|<=>|[<>=!]=?|[|&]{2}|~)/;
var indexingOperators = /^(?:\[\][?=]?)/;
var anotherOperators = /^(?:\.(?:\.{2})?|->|[?:])/;
var idents = /^[a-z_\u009F-\uFFFF][a-zA-Z0-9_\u009F-\uFFFF]*/;
var types = /^[A-Z_\u009F-\uFFFF][a-zA-Z0-9_\u009F-\uFFFF]*/;
var keywords = wordRegExp(["abstract", "alias", "as", "asm", "begin", "break", "case", "class", "def", "do", "else", "elsif", "end", "ensure", "enum", "extend", "for", "fun", "if", "include", "instance_sizeof", "lib", "macro", "module", "next", "of", "out", "pointerof", "private", "protected", "rescue", "return", "require", "select", "sizeof", "struct", "super", "then", "type", "typeof", "uninitialized", "union", "unless", "until", "when", "while", "with", "yield", "__DIR__", "__END_LINE__", "__FILE__", "__LINE__"]);
var atomWords = wordRegExp(["true", "false", "nil", "self"]);
var indentKeywordsArray = ["def", "fun", "macro", "class", "module", "struct", "lib", "enum", "union", "do", "for"];
var indentKeywords = wordRegExp(indentKeywordsArray);
var indentExpressionKeywordsArray = ["if", "unless", "case", "while", "until", "begin", "then"];
var indentExpressionKeywords = wordRegExp(indentExpressionKeywordsArray);
var dedentKeywordsArray = ["end", "else", "elsif", "rescue", "ensure"];
var dedentKeywords = wordRegExp(dedentKeywordsArray);
var dedentPunctualsArray = ["\\)", "\\}", "\\]"];
var dedentPunctuals = new RegExp("^(?:" + dedentPunctualsArray.join("|") + ")$");
var nextTokenizer = {
  "def": tokenFollowIdent,
  "fun": tokenFollowIdent,
  "macro": tokenMacroDef,
  "class": tokenFollowType,
  "module": tokenFollowType,
  "struct": tokenFollowType,
  "lib": tokenFollowType,
  "enum": tokenFollowType,
  "union": tokenFollowType
};
var matching = {
  "[": "]",
  "{": "}",
  "(": ")",
  "<": ">"
};
function tokenBase(stream, state) {
  if (stream.eatSpace()) {
    return null;
  }

  // Macros
  if (state.lastToken != "\\" && stream.match("{%", false)) {
    return chain(tokenMacro("%", "%"), stream, state);
  }
  if (state.lastToken != "\\" && stream.match("{{", false)) {
    return chain(tokenMacro("{", "}"), stream, state);
  }

  // Comments
  if (stream.peek() == "#") {
    stream.skipToEnd();
    return "comment";
  }

  // Variables and keywords
  var matched;
  if (stream.match(idents)) {
    stream.eat(/[?!]/);
    matched = stream.current();
    if (stream.eat(":")) {
      return "atom";
    } else if (state.lastToken == ".") {
      return "property";
    } else if (keywords.test(matched)) {
      if (indentKeywords.test(matched)) {
        if (!(matched == "fun" && state.blocks.indexOf("lib") >= 0) && !(matched == "def" && state.lastToken == "abstract")) {
          state.blocks.push(matched);
          state.currentIndent += 1;
        }
      } else if ((state.lastStyle == "operator" || !state.lastStyle) && indentExpressionKeywords.test(matched)) {
        state.blocks.push(matched);
        state.currentIndent += 1;
      } else if (matched == "end") {
        state.blocks.pop();
        state.currentIndent -= 1;
      }
      if (nextTokenizer.hasOwnProperty(matched)) {
        state.tokenize.push(nextTokenizer[matched]);
      }
      return "keyword";
    } else if (atomWords.test(matched)) {
      return "atom";
    }
    return "variable";
  }

  // Class variables and instance variables
  // or attributes
  if (stream.eat("@")) {
    if (stream.peek() == "[") {
      return chain(tokenNest("[", "]", "meta"), stream, state);
    }
    stream.eat("@");
    stream.match(idents) || stream.match(types);
    return "propertyName";
  }

  // Constants and types
  if (stream.match(types)) {
    return "tag";
  }

  // Symbols or ':' operator
  if (stream.eat(":")) {
    if (stream.eat("\"")) {
      return chain(tokenQuote("\"", "atom", false), stream, state);
    } else if (stream.match(idents) || stream.match(types) || stream.match(operators) || stream.match(conditionalOperators) || stream.match(indexingOperators)) {
      return "atom";
    }
    stream.eat(":");
    return "operator";
  }

  // Strings
  if (stream.eat("\"")) {
    return chain(tokenQuote("\"", "string", true), stream, state);
  }

  // Strings or regexps or macro variables or '%' operator
  if (stream.peek() == "%") {
    var style = "string";
    var embed = true;
    var delim;
    if (stream.match("%r")) {
      // Regexps
      style = "string.special";
      delim = stream.next();
    } else if (stream.match("%w")) {
      embed = false;
      delim = stream.next();
    } else if (stream.match("%q")) {
      embed = false;
      delim = stream.next();
    } else {
      if (delim = stream.match(/^%([^\w\s=])/)) {
        delim = delim[1];
      } else if (stream.match(/^%[a-zA-Z_\u009F-\uFFFF][\w\u009F-\uFFFF]*/)) {
        // Macro variables
        return "meta";
      } else if (stream.eat('%')) {
        // '%' operator
        return "operator";
      }
    }
    if (matching.hasOwnProperty(delim)) {
      delim = matching[delim];
    }
    return chain(tokenQuote(delim, style, embed), stream, state);
  }

  // Here Docs
  if (matched = stream.match(/^<<-('?)([A-Z]\w*)\1/)) {
    return chain(tokenHereDoc(matched[2], !matched[1]), stream, state);
  }

  // Characters
  if (stream.eat("'")) {
    stream.match(/^(?:[^']|\\(?:[befnrtv0'"]|[0-7]{3}|u(?:[0-9a-fA-F]{4}|\{[0-9a-fA-F]{1,6}\})))/);
    stream.eat("'");
    return "atom";
  }

  // Numbers
  if (stream.eat("0")) {
    if (stream.eat("x")) {
      stream.match(/^[0-9a-fA-F_]+/);
    } else if (stream.eat("o")) {
      stream.match(/^[0-7_]+/);
    } else if (stream.eat("b")) {
      stream.match(/^[01_]+/);
    }
    return "number";
  }
  if (stream.eat(/^\d/)) {
    stream.match(/^[\d_]*(?:\.[\d_]+)?(?:[eE][+-]?\d+)?/);
    return "number";
  }

  // Operators
  if (stream.match(operators)) {
    stream.eat("="); // Operators can follow assign symbol.
    return "operator";
  }
  if (stream.match(conditionalOperators) || stream.match(anotherOperators)) {
    return "operator";
  }

  // Parens and braces
  if (matched = stream.match(/[({[]/, false)) {
    matched = matched[0];
    return chain(tokenNest(matched, matching[matched], null), stream, state);
  }

  // Escapes
  if (stream.eat("\\")) {
    stream.next();
    return "meta";
  }
  stream.next();
  return null;
}
function tokenNest(begin, end, style, started) {
  return function (stream, state) {
    if (!started && stream.match(begin)) {
      state.tokenize[state.tokenize.length - 1] = tokenNest(begin, end, style, true);
      state.currentIndent += 1;
      return style;
    }
    var nextStyle = tokenBase(stream, state);
    if (stream.current() === end) {
      state.tokenize.pop();
      state.currentIndent -= 1;
      nextStyle = style;
    }
    return nextStyle;
  };
}
function tokenMacro(begin, end, started) {
  return function (stream, state) {
    if (!started && stream.match("{" + begin)) {
      state.currentIndent += 1;
      state.tokenize[state.tokenize.length - 1] = tokenMacro(begin, end, true);
      return "meta";
    }
    if (stream.match(end + "}")) {
      state.currentIndent -= 1;
      state.tokenize.pop();
      return "meta";
    }
    return tokenBase(stream, state);
  };
}
function tokenMacroDef(stream, state) {
  if (stream.eatSpace()) {
    return null;
  }
  var matched;
  if (matched = stream.match(idents)) {
    if (matched == "def") {
      return "keyword";
    }
    stream.eat(/[?!]/);
  }
  state.tokenize.pop();
  return "def";
}
function tokenFollowIdent(stream, state) {
  if (stream.eatSpace()) {
    return null;
  }
  if (stream.match(idents)) {
    stream.eat(/[!?]/);
  } else {
    stream.match(operators) || stream.match(conditionalOperators) || stream.match(indexingOperators);
  }
  state.tokenize.pop();
  return "def";
}
function tokenFollowType(stream, state) {
  if (stream.eatSpace()) {
    return null;
  }
  stream.match(types);
  state.tokenize.pop();
  return "def";
}
function tokenQuote(end, style, embed) {
  return function (stream, state) {
    var escaped = false;
    while (stream.peek()) {
      if (!escaped) {
        if (stream.match("{%", false)) {
          state.tokenize.push(tokenMacro("%", "%"));
          return style;
        }
        if (stream.match("{{", false)) {
          state.tokenize.push(tokenMacro("{", "}"));
          return style;
        }
        if (embed && stream.match("#{", false)) {
          state.tokenize.push(tokenNest("#{", "}", "meta"));
          return style;
        }
        var ch = stream.next();
        if (ch == end) {
          state.tokenize.pop();
          return style;
        }
        escaped = embed && ch == "\\";
      } else {
        stream.next();
        escaped = false;
      }
    }
    return style;
  };
}
function tokenHereDoc(phrase, embed) {
  return function (stream, state) {
    if (stream.sol()) {
      stream.eatSpace();
      if (stream.match(phrase)) {
        state.tokenize.pop();
        return "string";
      }
    }
    var escaped = false;
    while (stream.peek()) {
      if (!escaped) {
        if (stream.match("{%", false)) {
          state.tokenize.push(tokenMacro("%", "%"));
          return "string";
        }
        if (stream.match("{{", false)) {
          state.tokenize.push(tokenMacro("{", "}"));
          return "string";
        }
        if (embed && stream.match("#{", false)) {
          state.tokenize.push(tokenNest("#{", "}", "meta"));
          return "string";
        }
        escaped = stream.next() == "\\" && embed;
      } else {
        stream.next();
        escaped = false;
      }
    }
    return "string";
  };
}
const crystal = {
  name: "crystal",
  startState: function () {
    return {
      tokenize: [tokenBase],
      currentIndent: 0,
      lastToken: null,
      lastStyle: null,
      blocks: []
    };
  },
  token: function (stream, state) {
    var style = state.tokenize[state.tokenize.length - 1](stream, state);
    var token = stream.current();
    if (style && style != "comment") {
      state.lastToken = token;
      state.lastStyle = style;
    }
    return style;
  },
  indent: function (state, textAfter, cx) {
    textAfter = textAfter.replace(/^\s*(?:\{%)?\s*|\s*(?:%\})?\s*$/g, "");
    if (dedentKeywords.test(textAfter) || dedentPunctuals.test(textAfter)) {
      return cx.unit * (state.currentIndent - 1);
    }
    return cx.unit * state.currentIndent;
  },
  languageData: {
    indentOnInput: wordRegExp(dedentPunctualsArray.concat(dedentKeywordsArray), true),
    commentTokens: {
      line: "#"
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiMTYyNi5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9AY29kZW1pcnJvci9sZWdhY3ktbW9kZXMvbW9kZS9jcnlzdGFsLmpzIl0sInNvdXJjZXNDb250ZW50IjpbImZ1bmN0aW9uIHdvcmRSZWdFeHAod29yZHMsIGVuZCkge1xuICByZXR1cm4gbmV3IFJlZ0V4cCgoZW5kID8gXCJcIiA6IFwiXlwiKSArIFwiKD86XCIgKyB3b3Jkcy5qb2luKFwifFwiKSArIFwiKVwiICsgKGVuZCA/IFwiJFwiIDogXCJcXFxcYlwiKSk7XG59XG5mdW5jdGlvbiBjaGFpbih0b2tlbml6ZSwgc3RyZWFtLCBzdGF0ZSkge1xuICBzdGF0ZS50b2tlbml6ZS5wdXNoKHRva2VuaXplKTtcbiAgcmV0dXJuIHRva2VuaXplKHN0cmVhbSwgc3RhdGUpO1xufVxudmFyIG9wZXJhdG9ycyA9IC9eKD86Wy0rLyV8Jl5dfFxcKlxcKj98Wzw+XXsyfSkvO1xudmFyIGNvbmRpdGlvbmFsT3BlcmF0b3JzID0gL14oPzpbPSFdfnw9PT18PD0+fFs8Pj0hXT0/fFt8Jl17Mn18fikvO1xudmFyIGluZGV4aW5nT3BlcmF0b3JzID0gL14oPzpcXFtcXF1bPz1dPykvO1xudmFyIGFub3RoZXJPcGVyYXRvcnMgPSAvXig/OlxcLig/OlxcLnsyfSk/fC0+fFs/Ol0pLztcbnZhciBpZGVudHMgPSAvXlthLXpfXFx1MDA5Ri1cXHVGRkZGXVthLXpBLVowLTlfXFx1MDA5Ri1cXHVGRkZGXSovO1xudmFyIHR5cGVzID0gL15bQS1aX1xcdTAwOUYtXFx1RkZGRl1bYS16QS1aMC05X1xcdTAwOUYtXFx1RkZGRl0qLztcbnZhciBrZXl3b3JkcyA9IHdvcmRSZWdFeHAoW1wiYWJzdHJhY3RcIiwgXCJhbGlhc1wiLCBcImFzXCIsIFwiYXNtXCIsIFwiYmVnaW5cIiwgXCJicmVha1wiLCBcImNhc2VcIiwgXCJjbGFzc1wiLCBcImRlZlwiLCBcImRvXCIsIFwiZWxzZVwiLCBcImVsc2lmXCIsIFwiZW5kXCIsIFwiZW5zdXJlXCIsIFwiZW51bVwiLCBcImV4dGVuZFwiLCBcImZvclwiLCBcImZ1blwiLCBcImlmXCIsIFwiaW5jbHVkZVwiLCBcImluc3RhbmNlX3NpemVvZlwiLCBcImxpYlwiLCBcIm1hY3JvXCIsIFwibW9kdWxlXCIsIFwibmV4dFwiLCBcIm9mXCIsIFwib3V0XCIsIFwicG9pbnRlcm9mXCIsIFwicHJpdmF0ZVwiLCBcInByb3RlY3RlZFwiLCBcInJlc2N1ZVwiLCBcInJldHVyblwiLCBcInJlcXVpcmVcIiwgXCJzZWxlY3RcIiwgXCJzaXplb2ZcIiwgXCJzdHJ1Y3RcIiwgXCJzdXBlclwiLCBcInRoZW5cIiwgXCJ0eXBlXCIsIFwidHlwZW9mXCIsIFwidW5pbml0aWFsaXplZFwiLCBcInVuaW9uXCIsIFwidW5sZXNzXCIsIFwidW50aWxcIiwgXCJ3aGVuXCIsIFwid2hpbGVcIiwgXCJ3aXRoXCIsIFwieWllbGRcIiwgXCJfX0RJUl9fXCIsIFwiX19FTkRfTElORV9fXCIsIFwiX19GSUxFX19cIiwgXCJfX0xJTkVfX1wiXSk7XG52YXIgYXRvbVdvcmRzID0gd29yZFJlZ0V4cChbXCJ0cnVlXCIsIFwiZmFsc2VcIiwgXCJuaWxcIiwgXCJzZWxmXCJdKTtcbnZhciBpbmRlbnRLZXl3b3Jkc0FycmF5ID0gW1wiZGVmXCIsIFwiZnVuXCIsIFwibWFjcm9cIiwgXCJjbGFzc1wiLCBcIm1vZHVsZVwiLCBcInN0cnVjdFwiLCBcImxpYlwiLCBcImVudW1cIiwgXCJ1bmlvblwiLCBcImRvXCIsIFwiZm9yXCJdO1xudmFyIGluZGVudEtleXdvcmRzID0gd29yZFJlZ0V4cChpbmRlbnRLZXl3b3Jkc0FycmF5KTtcbnZhciBpbmRlbnRFeHByZXNzaW9uS2V5d29yZHNBcnJheSA9IFtcImlmXCIsIFwidW5sZXNzXCIsIFwiY2FzZVwiLCBcIndoaWxlXCIsIFwidW50aWxcIiwgXCJiZWdpblwiLCBcInRoZW5cIl07XG52YXIgaW5kZW50RXhwcmVzc2lvbktleXdvcmRzID0gd29yZFJlZ0V4cChpbmRlbnRFeHByZXNzaW9uS2V5d29yZHNBcnJheSk7XG52YXIgZGVkZW50S2V5d29yZHNBcnJheSA9IFtcImVuZFwiLCBcImVsc2VcIiwgXCJlbHNpZlwiLCBcInJlc2N1ZVwiLCBcImVuc3VyZVwiXTtcbnZhciBkZWRlbnRLZXl3b3JkcyA9IHdvcmRSZWdFeHAoZGVkZW50S2V5d29yZHNBcnJheSk7XG52YXIgZGVkZW50UHVuY3R1YWxzQXJyYXkgPSBbXCJcXFxcKVwiLCBcIlxcXFx9XCIsIFwiXFxcXF1cIl07XG52YXIgZGVkZW50UHVuY3R1YWxzID0gbmV3IFJlZ0V4cChcIl4oPzpcIiArIGRlZGVudFB1bmN0dWFsc0FycmF5LmpvaW4oXCJ8XCIpICsgXCIpJFwiKTtcbnZhciBuZXh0VG9rZW5pemVyID0ge1xuICBcImRlZlwiOiB0b2tlbkZvbGxvd0lkZW50LFxuICBcImZ1blwiOiB0b2tlbkZvbGxvd0lkZW50LFxuICBcIm1hY3JvXCI6IHRva2VuTWFjcm9EZWYsXG4gIFwiY2xhc3NcIjogdG9rZW5Gb2xsb3dUeXBlLFxuICBcIm1vZHVsZVwiOiB0b2tlbkZvbGxvd1R5cGUsXG4gIFwic3RydWN0XCI6IHRva2VuRm9sbG93VHlwZSxcbiAgXCJsaWJcIjogdG9rZW5Gb2xsb3dUeXBlLFxuICBcImVudW1cIjogdG9rZW5Gb2xsb3dUeXBlLFxuICBcInVuaW9uXCI6IHRva2VuRm9sbG93VHlwZVxufTtcbnZhciBtYXRjaGluZyA9IHtcbiAgXCJbXCI6IFwiXVwiLFxuICBcIntcIjogXCJ9XCIsXG4gIFwiKFwiOiBcIilcIixcbiAgXCI8XCI6IFwiPlwiXG59O1xuZnVuY3Rpb24gdG9rZW5CYXNlKHN0cmVhbSwgc3RhdGUpIHtcbiAgaWYgKHN0cmVhbS5lYXRTcGFjZSgpKSB7XG4gICAgcmV0dXJuIG51bGw7XG4gIH1cblxuICAvLyBNYWNyb3NcbiAgaWYgKHN0YXRlLmxhc3RUb2tlbiAhPSBcIlxcXFxcIiAmJiBzdHJlYW0ubWF0Y2goXCJ7JVwiLCBmYWxzZSkpIHtcbiAgICByZXR1cm4gY2hhaW4odG9rZW5NYWNybyhcIiVcIiwgXCIlXCIpLCBzdHJlYW0sIHN0YXRlKTtcbiAgfVxuICBpZiAoc3RhdGUubGFzdFRva2VuICE9IFwiXFxcXFwiICYmIHN0cmVhbS5tYXRjaChcInt7XCIsIGZhbHNlKSkge1xuICAgIHJldHVybiBjaGFpbih0b2tlbk1hY3JvKFwie1wiLCBcIn1cIiksIHN0cmVhbSwgc3RhdGUpO1xuICB9XG5cbiAgLy8gQ29tbWVudHNcbiAgaWYgKHN0cmVhbS5wZWVrKCkgPT0gXCIjXCIpIHtcbiAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICB9XG5cbiAgLy8gVmFyaWFibGVzIGFuZCBrZXl3b3Jkc1xuICB2YXIgbWF0Y2hlZDtcbiAgaWYgKHN0cmVhbS5tYXRjaChpZGVudHMpKSB7XG4gICAgc3RyZWFtLmVhdCgvWz8hXS8pO1xuICAgIG1hdGNoZWQgPSBzdHJlYW0uY3VycmVudCgpO1xuICAgIGlmIChzdHJlYW0uZWF0KFwiOlwiKSkge1xuICAgICAgcmV0dXJuIFwiYXRvbVwiO1xuICAgIH0gZWxzZSBpZiAoc3RhdGUubGFzdFRva2VuID09IFwiLlwiKSB7XG4gICAgICByZXR1cm4gXCJwcm9wZXJ0eVwiO1xuICAgIH0gZWxzZSBpZiAoa2V5d29yZHMudGVzdChtYXRjaGVkKSkge1xuICAgICAgaWYgKGluZGVudEtleXdvcmRzLnRlc3QobWF0Y2hlZCkpIHtcbiAgICAgICAgaWYgKCEobWF0Y2hlZCA9PSBcImZ1blwiICYmIHN0YXRlLmJsb2Nrcy5pbmRleE9mKFwibGliXCIpID49IDApICYmICEobWF0Y2hlZCA9PSBcImRlZlwiICYmIHN0YXRlLmxhc3RUb2tlbiA9PSBcImFic3RyYWN0XCIpKSB7XG4gICAgICAgICAgc3RhdGUuYmxvY2tzLnB1c2gobWF0Y2hlZCk7XG4gICAgICAgICAgc3RhdGUuY3VycmVudEluZGVudCArPSAxO1xuICAgICAgICB9XG4gICAgICB9IGVsc2UgaWYgKChzdGF0ZS5sYXN0U3R5bGUgPT0gXCJvcGVyYXRvclwiIHx8ICFzdGF0ZS5sYXN0U3R5bGUpICYmIGluZGVudEV4cHJlc3Npb25LZXl3b3Jkcy50ZXN0KG1hdGNoZWQpKSB7XG4gICAgICAgIHN0YXRlLmJsb2Nrcy5wdXNoKG1hdGNoZWQpO1xuICAgICAgICBzdGF0ZS5jdXJyZW50SW5kZW50ICs9IDE7XG4gICAgICB9IGVsc2UgaWYgKG1hdGNoZWQgPT0gXCJlbmRcIikge1xuICAgICAgICBzdGF0ZS5ibG9ja3MucG9wKCk7XG4gICAgICAgIHN0YXRlLmN1cnJlbnRJbmRlbnQgLT0gMTtcbiAgICAgIH1cbiAgICAgIGlmIChuZXh0VG9rZW5pemVyLmhhc093blByb3BlcnR5KG1hdGNoZWQpKSB7XG4gICAgICAgIHN0YXRlLnRva2VuaXplLnB1c2gobmV4dFRva2VuaXplclttYXRjaGVkXSk7XG4gICAgICB9XG4gICAgICByZXR1cm4gXCJrZXl3b3JkXCI7XG4gICAgfSBlbHNlIGlmIChhdG9tV29yZHMudGVzdChtYXRjaGVkKSkge1xuICAgICAgcmV0dXJuIFwiYXRvbVwiO1xuICAgIH1cbiAgICByZXR1cm4gXCJ2YXJpYWJsZVwiO1xuICB9XG5cbiAgLy8gQ2xhc3MgdmFyaWFibGVzIGFuZCBpbnN0YW5jZSB2YXJpYWJsZXNcbiAgLy8gb3IgYXR0cmlidXRlc1xuICBpZiAoc3RyZWFtLmVhdChcIkBcIikpIHtcbiAgICBpZiAoc3RyZWFtLnBlZWsoKSA9PSBcIltcIikge1xuICAgICAgcmV0dXJuIGNoYWluKHRva2VuTmVzdChcIltcIiwgXCJdXCIsIFwibWV0YVwiKSwgc3RyZWFtLCBzdGF0ZSk7XG4gICAgfVxuICAgIHN0cmVhbS5lYXQoXCJAXCIpO1xuICAgIHN0cmVhbS5tYXRjaChpZGVudHMpIHx8IHN0cmVhbS5tYXRjaCh0eXBlcyk7XG4gICAgcmV0dXJuIFwicHJvcGVydHlOYW1lXCI7XG4gIH1cblxuICAvLyBDb25zdGFudHMgYW5kIHR5cGVzXG4gIGlmIChzdHJlYW0ubWF0Y2godHlwZXMpKSB7XG4gICAgcmV0dXJuIFwidGFnXCI7XG4gIH1cblxuICAvLyBTeW1ib2xzIG9yICc6JyBvcGVyYXRvclxuICBpZiAoc3RyZWFtLmVhdChcIjpcIikpIHtcbiAgICBpZiAoc3RyZWFtLmVhdChcIlxcXCJcIikpIHtcbiAgICAgIHJldHVybiBjaGFpbih0b2tlblF1b3RlKFwiXFxcIlwiLCBcImF0b21cIiwgZmFsc2UpLCBzdHJlYW0sIHN0YXRlKTtcbiAgICB9IGVsc2UgaWYgKHN0cmVhbS5tYXRjaChpZGVudHMpIHx8IHN0cmVhbS5tYXRjaCh0eXBlcykgfHwgc3RyZWFtLm1hdGNoKG9wZXJhdG9ycykgfHwgc3RyZWFtLm1hdGNoKGNvbmRpdGlvbmFsT3BlcmF0b3JzKSB8fCBzdHJlYW0ubWF0Y2goaW5kZXhpbmdPcGVyYXRvcnMpKSB7XG4gICAgICByZXR1cm4gXCJhdG9tXCI7XG4gICAgfVxuICAgIHN0cmVhbS5lYXQoXCI6XCIpO1xuICAgIHJldHVybiBcIm9wZXJhdG9yXCI7XG4gIH1cblxuICAvLyBTdHJpbmdzXG4gIGlmIChzdHJlYW0uZWF0KFwiXFxcIlwiKSkge1xuICAgIHJldHVybiBjaGFpbih0b2tlblF1b3RlKFwiXFxcIlwiLCBcInN0cmluZ1wiLCB0cnVlKSwgc3RyZWFtLCBzdGF0ZSk7XG4gIH1cblxuICAvLyBTdHJpbmdzIG9yIHJlZ2V4cHMgb3IgbWFjcm8gdmFyaWFibGVzIG9yICclJyBvcGVyYXRvclxuICBpZiAoc3RyZWFtLnBlZWsoKSA9PSBcIiVcIikge1xuICAgIHZhciBzdHlsZSA9IFwic3RyaW5nXCI7XG4gICAgdmFyIGVtYmVkID0gdHJ1ZTtcbiAgICB2YXIgZGVsaW07XG4gICAgaWYgKHN0cmVhbS5tYXRjaChcIiVyXCIpKSB7XG4gICAgICAvLyBSZWdleHBzXG4gICAgICBzdHlsZSA9IFwic3RyaW5nLnNwZWNpYWxcIjtcbiAgICAgIGRlbGltID0gc3RyZWFtLm5leHQoKTtcbiAgICB9IGVsc2UgaWYgKHN0cmVhbS5tYXRjaChcIiV3XCIpKSB7XG4gICAgICBlbWJlZCA9IGZhbHNlO1xuICAgICAgZGVsaW0gPSBzdHJlYW0ubmV4dCgpO1xuICAgIH0gZWxzZSBpZiAoc3RyZWFtLm1hdGNoKFwiJXFcIikpIHtcbiAgICAgIGVtYmVkID0gZmFsc2U7XG4gICAgICBkZWxpbSA9IHN0cmVhbS5uZXh0KCk7XG4gICAgfSBlbHNlIHtcbiAgICAgIGlmIChkZWxpbSA9IHN0cmVhbS5tYXRjaCgvXiUoW15cXHdcXHM9XSkvKSkge1xuICAgICAgICBkZWxpbSA9IGRlbGltWzFdO1xuICAgICAgfSBlbHNlIGlmIChzdHJlYW0ubWF0Y2goL14lW2EtekEtWl9cXHUwMDlGLVxcdUZGRkZdW1xcd1xcdTAwOUYtXFx1RkZGRl0qLykpIHtcbiAgICAgICAgLy8gTWFjcm8gdmFyaWFibGVzXG4gICAgICAgIHJldHVybiBcIm1ldGFcIjtcbiAgICAgIH0gZWxzZSBpZiAoc3RyZWFtLmVhdCgnJScpKSB7XG4gICAgICAgIC8vICclJyBvcGVyYXRvclxuICAgICAgICByZXR1cm4gXCJvcGVyYXRvclwiO1xuICAgICAgfVxuICAgIH1cbiAgICBpZiAobWF0Y2hpbmcuaGFzT3duUHJvcGVydHkoZGVsaW0pKSB7XG4gICAgICBkZWxpbSA9IG1hdGNoaW5nW2RlbGltXTtcbiAgICB9XG4gICAgcmV0dXJuIGNoYWluKHRva2VuUXVvdGUoZGVsaW0sIHN0eWxlLCBlbWJlZCksIHN0cmVhbSwgc3RhdGUpO1xuICB9XG5cbiAgLy8gSGVyZSBEb2NzXG4gIGlmIChtYXRjaGVkID0gc3RyZWFtLm1hdGNoKC9ePDwtKCc/KShbQS1aXVxcdyopXFwxLykpIHtcbiAgICByZXR1cm4gY2hhaW4odG9rZW5IZXJlRG9jKG1hdGNoZWRbMl0sICFtYXRjaGVkWzFdKSwgc3RyZWFtLCBzdGF0ZSk7XG4gIH1cblxuICAvLyBDaGFyYWN0ZXJzXG4gIGlmIChzdHJlYW0uZWF0KFwiJ1wiKSkge1xuICAgIHN0cmVhbS5tYXRjaCgvXig/OlteJ118XFxcXCg/OltiZWZucnR2MCdcIl18WzAtN117M318dSg/OlswLTlhLWZBLUZdezR9fFxce1swLTlhLWZBLUZdezEsNn1cXH0pKSkvKTtcbiAgICBzdHJlYW0uZWF0KFwiJ1wiKTtcbiAgICByZXR1cm4gXCJhdG9tXCI7XG4gIH1cblxuICAvLyBOdW1iZXJzXG4gIGlmIChzdHJlYW0uZWF0KFwiMFwiKSkge1xuICAgIGlmIChzdHJlYW0uZWF0KFwieFwiKSkge1xuICAgICAgc3RyZWFtLm1hdGNoKC9eWzAtOWEtZkEtRl9dKy8pO1xuICAgIH0gZWxzZSBpZiAoc3RyZWFtLmVhdChcIm9cIikpIHtcbiAgICAgIHN0cmVhbS5tYXRjaCgvXlswLTdfXSsvKTtcbiAgICB9IGVsc2UgaWYgKHN0cmVhbS5lYXQoXCJiXCIpKSB7XG4gICAgICBzdHJlYW0ubWF0Y2goL15bMDFfXSsvKTtcbiAgICB9XG4gICAgcmV0dXJuIFwibnVtYmVyXCI7XG4gIH1cbiAgaWYgKHN0cmVhbS5lYXQoL15cXGQvKSkge1xuICAgIHN0cmVhbS5tYXRjaCgvXltcXGRfXSooPzpcXC5bXFxkX10rKT8oPzpbZUVdWystXT9cXGQrKT8vKTtcbiAgICByZXR1cm4gXCJudW1iZXJcIjtcbiAgfVxuXG4gIC8vIE9wZXJhdG9yc1xuICBpZiAoc3RyZWFtLm1hdGNoKG9wZXJhdG9ycykpIHtcbiAgICBzdHJlYW0uZWF0KFwiPVwiKTsgLy8gT3BlcmF0b3JzIGNhbiBmb2xsb3cgYXNzaWduIHN5bWJvbC5cbiAgICByZXR1cm4gXCJvcGVyYXRvclwiO1xuICB9XG4gIGlmIChzdHJlYW0ubWF0Y2goY29uZGl0aW9uYWxPcGVyYXRvcnMpIHx8IHN0cmVhbS5tYXRjaChhbm90aGVyT3BlcmF0b3JzKSkge1xuICAgIHJldHVybiBcIm9wZXJhdG9yXCI7XG4gIH1cblxuICAvLyBQYXJlbnMgYW5kIGJyYWNlc1xuICBpZiAobWF0Y2hlZCA9IHN0cmVhbS5tYXRjaCgvWyh7W10vLCBmYWxzZSkpIHtcbiAgICBtYXRjaGVkID0gbWF0Y2hlZFswXTtcbiAgICByZXR1cm4gY2hhaW4odG9rZW5OZXN0KG1hdGNoZWQsIG1hdGNoaW5nW21hdGNoZWRdLCBudWxsKSwgc3RyZWFtLCBzdGF0ZSk7XG4gIH1cblxuICAvLyBFc2NhcGVzXG4gIGlmIChzdHJlYW0uZWF0KFwiXFxcXFwiKSkge1xuICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgcmV0dXJuIFwibWV0YVwiO1xuICB9XG4gIHN0cmVhbS5uZXh0KCk7XG4gIHJldHVybiBudWxsO1xufVxuZnVuY3Rpb24gdG9rZW5OZXN0KGJlZ2luLCBlbmQsIHN0eWxlLCBzdGFydGVkKSB7XG4gIHJldHVybiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIGlmICghc3RhcnRlZCAmJiBzdHJlYW0ubWF0Y2goYmVnaW4pKSB7XG4gICAgICBzdGF0ZS50b2tlbml6ZVtzdGF0ZS50b2tlbml6ZS5sZW5ndGggLSAxXSA9IHRva2VuTmVzdChiZWdpbiwgZW5kLCBzdHlsZSwgdHJ1ZSk7XG4gICAgICBzdGF0ZS5jdXJyZW50SW5kZW50ICs9IDE7XG4gICAgICByZXR1cm4gc3R5bGU7XG4gICAgfVxuICAgIHZhciBuZXh0U3R5bGUgPSB0b2tlbkJhc2Uoc3RyZWFtLCBzdGF0ZSk7XG4gICAgaWYgKHN0cmVhbS5jdXJyZW50KCkgPT09IGVuZCkge1xuICAgICAgc3RhdGUudG9rZW5pemUucG9wKCk7XG4gICAgICBzdGF0ZS5jdXJyZW50SW5kZW50IC09IDE7XG4gICAgICBuZXh0U3R5bGUgPSBzdHlsZTtcbiAgICB9XG4gICAgcmV0dXJuIG5leHRTdHlsZTtcbiAgfTtcbn1cbmZ1bmN0aW9uIHRva2VuTWFjcm8oYmVnaW4sIGVuZCwgc3RhcnRlZCkge1xuICByZXR1cm4gZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICBpZiAoIXN0YXJ0ZWQgJiYgc3RyZWFtLm1hdGNoKFwie1wiICsgYmVnaW4pKSB7XG4gICAgICBzdGF0ZS5jdXJyZW50SW5kZW50ICs9IDE7XG4gICAgICBzdGF0ZS50b2tlbml6ZVtzdGF0ZS50b2tlbml6ZS5sZW5ndGggLSAxXSA9IHRva2VuTWFjcm8oYmVnaW4sIGVuZCwgdHJ1ZSk7XG4gICAgICByZXR1cm4gXCJtZXRhXCI7XG4gICAgfVxuICAgIGlmIChzdHJlYW0ubWF0Y2goZW5kICsgXCJ9XCIpKSB7XG4gICAgICBzdGF0ZS5jdXJyZW50SW5kZW50IC09IDE7XG4gICAgICBzdGF0ZS50b2tlbml6ZS5wb3AoKTtcbiAgICAgIHJldHVybiBcIm1ldGFcIjtcbiAgICB9XG4gICAgcmV0dXJuIHRva2VuQmFzZShzdHJlYW0sIHN0YXRlKTtcbiAgfTtcbn1cbmZ1bmN0aW9uIHRva2VuTWFjcm9EZWYoc3RyZWFtLCBzdGF0ZSkge1xuICBpZiAoc3RyZWFtLmVhdFNwYWNlKCkpIHtcbiAgICByZXR1cm4gbnVsbDtcbiAgfVxuICB2YXIgbWF0Y2hlZDtcbiAgaWYgKG1hdGNoZWQgPSBzdHJlYW0ubWF0Y2goaWRlbnRzKSkge1xuICAgIGlmIChtYXRjaGVkID09IFwiZGVmXCIpIHtcbiAgICAgIHJldHVybiBcImtleXdvcmRcIjtcbiAgICB9XG4gICAgc3RyZWFtLmVhdCgvWz8hXS8pO1xuICB9XG4gIHN0YXRlLnRva2VuaXplLnBvcCgpO1xuICByZXR1cm4gXCJkZWZcIjtcbn1cbmZ1bmN0aW9uIHRva2VuRm9sbG93SWRlbnQoc3RyZWFtLCBzdGF0ZSkge1xuICBpZiAoc3RyZWFtLmVhdFNwYWNlKCkpIHtcbiAgICByZXR1cm4gbnVsbDtcbiAgfVxuICBpZiAoc3RyZWFtLm1hdGNoKGlkZW50cykpIHtcbiAgICBzdHJlYW0uZWF0KC9bIT9dLyk7XG4gIH0gZWxzZSB7XG4gICAgc3RyZWFtLm1hdGNoKG9wZXJhdG9ycykgfHwgc3RyZWFtLm1hdGNoKGNvbmRpdGlvbmFsT3BlcmF0b3JzKSB8fCBzdHJlYW0ubWF0Y2goaW5kZXhpbmdPcGVyYXRvcnMpO1xuICB9XG4gIHN0YXRlLnRva2VuaXplLnBvcCgpO1xuICByZXR1cm4gXCJkZWZcIjtcbn1cbmZ1bmN0aW9uIHRva2VuRm9sbG93VHlwZShzdHJlYW0sIHN0YXRlKSB7XG4gIGlmIChzdHJlYW0uZWF0U3BhY2UoKSkge1xuICAgIHJldHVybiBudWxsO1xuICB9XG4gIHN0cmVhbS5tYXRjaCh0eXBlcyk7XG4gIHN0YXRlLnRva2VuaXplLnBvcCgpO1xuICByZXR1cm4gXCJkZWZcIjtcbn1cbmZ1bmN0aW9uIHRva2VuUXVvdGUoZW5kLCBzdHlsZSwgZW1iZWQpIHtcbiAgcmV0dXJuIGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgdmFyIGVzY2FwZWQgPSBmYWxzZTtcbiAgICB3aGlsZSAoc3RyZWFtLnBlZWsoKSkge1xuICAgICAgaWYgKCFlc2NhcGVkKSB7XG4gICAgICAgIGlmIChzdHJlYW0ubWF0Y2goXCJ7JVwiLCBmYWxzZSkpIHtcbiAgICAgICAgICBzdGF0ZS50b2tlbml6ZS5wdXNoKHRva2VuTWFjcm8oXCIlXCIsIFwiJVwiKSk7XG4gICAgICAgICAgcmV0dXJuIHN0eWxlO1xuICAgICAgICB9XG4gICAgICAgIGlmIChzdHJlYW0ubWF0Y2goXCJ7e1wiLCBmYWxzZSkpIHtcbiAgICAgICAgICBzdGF0ZS50b2tlbml6ZS5wdXNoKHRva2VuTWFjcm8oXCJ7XCIsIFwifVwiKSk7XG4gICAgICAgICAgcmV0dXJuIHN0eWxlO1xuICAgICAgICB9XG4gICAgICAgIGlmIChlbWJlZCAmJiBzdHJlYW0ubWF0Y2goXCIje1wiLCBmYWxzZSkpIHtcbiAgICAgICAgICBzdGF0ZS50b2tlbml6ZS5wdXNoKHRva2VuTmVzdChcIiN7XCIsIFwifVwiLCBcIm1ldGFcIikpO1xuICAgICAgICAgIHJldHVybiBzdHlsZTtcbiAgICAgICAgfVxuICAgICAgICB2YXIgY2ggPSBzdHJlYW0ubmV4dCgpO1xuICAgICAgICBpZiAoY2ggPT0gZW5kKSB7XG4gICAgICAgICAgc3RhdGUudG9rZW5pemUucG9wKCk7XG4gICAgICAgICAgcmV0dXJuIHN0eWxlO1xuICAgICAgICB9XG4gICAgICAgIGVzY2FwZWQgPSBlbWJlZCAmJiBjaCA9PSBcIlxcXFxcIjtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgICAgIGVzY2FwZWQgPSBmYWxzZTtcbiAgICAgIH1cbiAgICB9XG4gICAgcmV0dXJuIHN0eWxlO1xuICB9O1xufVxuZnVuY3Rpb24gdG9rZW5IZXJlRG9jKHBocmFzZSwgZW1iZWQpIHtcbiAgcmV0dXJuIGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgaWYgKHN0cmVhbS5zb2woKSkge1xuICAgICAgc3RyZWFtLmVhdFNwYWNlKCk7XG4gICAgICBpZiAoc3RyZWFtLm1hdGNoKHBocmFzZSkpIHtcbiAgICAgICAgc3RhdGUudG9rZW5pemUucG9wKCk7XG4gICAgICAgIHJldHVybiBcInN0cmluZ1wiO1xuICAgICAgfVxuICAgIH1cbiAgICB2YXIgZXNjYXBlZCA9IGZhbHNlO1xuICAgIHdoaWxlIChzdHJlYW0ucGVlaygpKSB7XG4gICAgICBpZiAoIWVzY2FwZWQpIHtcbiAgICAgICAgaWYgKHN0cmVhbS5tYXRjaChcInslXCIsIGZhbHNlKSkge1xuICAgICAgICAgIHN0YXRlLnRva2VuaXplLnB1c2godG9rZW5NYWNybyhcIiVcIiwgXCIlXCIpKTtcbiAgICAgICAgICByZXR1cm4gXCJzdHJpbmdcIjtcbiAgICAgICAgfVxuICAgICAgICBpZiAoc3RyZWFtLm1hdGNoKFwie3tcIiwgZmFsc2UpKSB7XG4gICAgICAgICAgc3RhdGUudG9rZW5pemUucHVzaCh0b2tlbk1hY3JvKFwie1wiLCBcIn1cIikpO1xuICAgICAgICAgIHJldHVybiBcInN0cmluZ1wiO1xuICAgICAgICB9XG4gICAgICAgIGlmIChlbWJlZCAmJiBzdHJlYW0ubWF0Y2goXCIje1wiLCBmYWxzZSkpIHtcbiAgICAgICAgICBzdGF0ZS50b2tlbml6ZS5wdXNoKHRva2VuTmVzdChcIiN7XCIsIFwifVwiLCBcIm1ldGFcIikpO1xuICAgICAgICAgIHJldHVybiBcInN0cmluZ1wiO1xuICAgICAgICB9XG4gICAgICAgIGVzY2FwZWQgPSBzdHJlYW0ubmV4dCgpID09IFwiXFxcXFwiICYmIGVtYmVkO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgc3RyZWFtLm5leHQoKTtcbiAgICAgICAgZXNjYXBlZCA9IGZhbHNlO1xuICAgICAgfVxuICAgIH1cbiAgICByZXR1cm4gXCJzdHJpbmdcIjtcbiAgfTtcbn1cbmV4cG9ydCBjb25zdCBjcnlzdGFsID0ge1xuICBuYW1lOiBcImNyeXN0YWxcIixcbiAgc3RhcnRTdGF0ZTogZnVuY3Rpb24gKCkge1xuICAgIHJldHVybiB7XG4gICAgICB0b2tlbml6ZTogW3Rva2VuQmFzZV0sXG4gICAgICBjdXJyZW50SW5kZW50OiAwLFxuICAgICAgbGFzdFRva2VuOiBudWxsLFxuICAgICAgbGFzdFN0eWxlOiBudWxsLFxuICAgICAgYmxvY2tzOiBbXVxuICAgIH07XG4gIH0sXG4gIHRva2VuOiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIHZhciBzdHlsZSA9IHN0YXRlLnRva2VuaXplW3N0YXRlLnRva2VuaXplLmxlbmd0aCAtIDFdKHN0cmVhbSwgc3RhdGUpO1xuICAgIHZhciB0b2tlbiA9IHN0cmVhbS5jdXJyZW50KCk7XG4gICAgaWYgKHN0eWxlICYmIHN0eWxlICE9IFwiY29tbWVudFwiKSB7XG4gICAgICBzdGF0ZS5sYXN0VG9rZW4gPSB0b2tlbjtcbiAgICAgIHN0YXRlLmxhc3RTdHlsZSA9IHN0eWxlO1xuICAgIH1cbiAgICByZXR1cm4gc3R5bGU7XG4gIH0sXG4gIGluZGVudDogZnVuY3Rpb24gKHN0YXRlLCB0ZXh0QWZ0ZXIsIGN4KSB7XG4gICAgdGV4dEFmdGVyID0gdGV4dEFmdGVyLnJlcGxhY2UoL15cXHMqKD86XFx7JSk/XFxzKnxcXHMqKD86JVxcfSk/XFxzKiQvZywgXCJcIik7XG4gICAgaWYgKGRlZGVudEtleXdvcmRzLnRlc3QodGV4dEFmdGVyKSB8fCBkZWRlbnRQdW5jdHVhbHMudGVzdCh0ZXh0QWZ0ZXIpKSB7XG4gICAgICByZXR1cm4gY3gudW5pdCAqIChzdGF0ZS5jdXJyZW50SW5kZW50IC0gMSk7XG4gICAgfVxuICAgIHJldHVybiBjeC51bml0ICogc3RhdGUuY3VycmVudEluZGVudDtcbiAgfSxcbiAgbGFuZ3VhZ2VEYXRhOiB7XG4gICAgaW5kZW50T25JbnB1dDogd29yZFJlZ0V4cChkZWRlbnRQdW5jdHVhbHNBcnJheS5jb25jYXQoZGVkZW50S2V5d29yZHNBcnJheSksIHRydWUpLFxuICAgIGNvbW1lbnRUb2tlbnM6IHtcbiAgICAgIGxpbmU6IFwiI1wiXG4gICAgfVxuICB9XG59OyJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==