"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[5767],{

/***/ 55767:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "coffeeScript": () => (/* binding */ coffeeScript)
/* harmony export */ });
var ERRORCLASS = "error";
function wordRegexp(words) {
  return new RegExp("^((" + words.join(")|(") + "))\\b");
}
var operators = /^(?:->|=>|\+[+=]?|-[\-=]?|\*[\*=]?|\/[\/=]?|[=!]=|<[><]?=?|>>?=?|%=?|&=?|\|=?|\^=?|\~|!|\?|(or|and|\|\||&&|\?)=)/;
var delimiters = /^(?:[()\[\]{},:`=;]|\.\.?\.?)/;
var identifiers = /^[_A-Za-z$][_A-Za-z$0-9]*/;
var atProp = /^@[_A-Za-z$][_A-Za-z$0-9]*/;
var wordOperators = wordRegexp(["and", "or", "not", "is", "isnt", "in", "instanceof", "typeof"]);
var indentKeywords = ["for", "while", "loop", "if", "unless", "else", "switch", "try", "catch", "finally", "class"];
var commonKeywords = ["break", "by", "continue", "debugger", "delete", "do", "in", "of", "new", "return", "then", "this", "@", "throw", "when", "until", "extends"];
var keywords = wordRegexp(indentKeywords.concat(commonKeywords));
indentKeywords = wordRegexp(indentKeywords);
var stringPrefixes = /^('{3}|\"{3}|['\"])/;
var regexPrefixes = /^(\/{3}|\/)/;
var commonConstants = ["Infinity", "NaN", "undefined", "null", "true", "false", "on", "off", "yes", "no"];
var constants = wordRegexp(commonConstants);

// Tokenizers
function tokenBase(stream, state) {
  // Handle scope changes
  if (stream.sol()) {
    if (state.scope.align === null) state.scope.align = false;
    var scopeOffset = state.scope.offset;
    if (stream.eatSpace()) {
      var lineOffset = stream.indentation();
      if (lineOffset > scopeOffset && state.scope.type == "coffee") {
        return "indent";
      } else if (lineOffset < scopeOffset) {
        return "dedent";
      }
      return null;
    } else {
      if (scopeOffset > 0) {
        dedent(stream, state);
      }
    }
  }
  if (stream.eatSpace()) {
    return null;
  }
  var ch = stream.peek();

  // Handle docco title comment (single line)
  if (stream.match("####")) {
    stream.skipToEnd();
    return "comment";
  }

  // Handle multi line comments
  if (stream.match("###")) {
    state.tokenize = longComment;
    return state.tokenize(stream, state);
  }

  // Single line comment
  if (ch === "#") {
    stream.skipToEnd();
    return "comment";
  }

  // Handle number literals
  if (stream.match(/^-?[0-9\.]/, false)) {
    var floatLiteral = false;
    // Floats
    if (stream.match(/^-?\d*\.\d+(e[\+\-]?\d+)?/i)) {
      floatLiteral = true;
    }
    if (stream.match(/^-?\d+\.\d*/)) {
      floatLiteral = true;
    }
    if (stream.match(/^-?\.\d+/)) {
      floatLiteral = true;
    }
    if (floatLiteral) {
      // prevent from getting extra . on 1..
      if (stream.peek() == ".") {
        stream.backUp(1);
      }
      return "number";
    }
    // Integers
    var intLiteral = false;
    // Hex
    if (stream.match(/^-?0x[0-9a-f]+/i)) {
      intLiteral = true;
    }
    // Decimal
    if (stream.match(/^-?[1-9]\d*(e[\+\-]?\d+)?/)) {
      intLiteral = true;
    }
    // Zero by itself with no other piece of number.
    if (stream.match(/^-?0(?![\dx])/i)) {
      intLiteral = true;
    }
    if (intLiteral) {
      return "number";
    }
  }

  // Handle strings
  if (stream.match(stringPrefixes)) {
    state.tokenize = tokenFactory(stream.current(), false, "string");
    return state.tokenize(stream, state);
  }
  // Handle regex literals
  if (stream.match(regexPrefixes)) {
    if (stream.current() != "/" || stream.match(/^.*\//, false)) {
      // prevent highlight of division
      state.tokenize = tokenFactory(stream.current(), true, "string.special");
      return state.tokenize(stream, state);
    } else {
      stream.backUp(1);
    }
  }

  // Handle operators and delimiters
  if (stream.match(operators) || stream.match(wordOperators)) {
    return "operator";
  }
  if (stream.match(delimiters)) {
    return "punctuation";
  }
  if (stream.match(constants)) {
    return "atom";
  }
  if (stream.match(atProp) || state.prop && stream.match(identifiers)) {
    return "property";
  }
  if (stream.match(keywords)) {
    return "keyword";
  }
  if (stream.match(identifiers)) {
    return "variable";
  }

  // Handle non-detected items
  stream.next();
  return ERRORCLASS;
}
function tokenFactory(delimiter, singleline, outclass) {
  return function (stream, state) {
    while (!stream.eol()) {
      stream.eatWhile(/[^'"\/\\]/);
      if (stream.eat("\\")) {
        stream.next();
        if (singleline && stream.eol()) {
          return outclass;
        }
      } else if (stream.match(delimiter)) {
        state.tokenize = tokenBase;
        return outclass;
      } else {
        stream.eat(/['"\/]/);
      }
    }
    if (singleline) {
      state.tokenize = tokenBase;
    }
    return outclass;
  };
}
function longComment(stream, state) {
  while (!stream.eol()) {
    stream.eatWhile(/[^#]/);
    if (stream.match("###")) {
      state.tokenize = tokenBase;
      break;
    }
    stream.eatWhile("#");
  }
  return "comment";
}
function indent(stream, state, type = "coffee") {
  var offset = 0,
    align = false,
    alignOffset = null;
  for (var scope = state.scope; scope; scope = scope.prev) {
    if (scope.type === "coffee" || scope.type == "}") {
      offset = scope.offset + stream.indentUnit;
      break;
    }
  }
  if (type !== "coffee") {
    align = null;
    alignOffset = stream.column() + stream.current().length;
  } else if (state.scope.align) {
    state.scope.align = false;
  }
  state.scope = {
    offset: offset,
    type: type,
    prev: state.scope,
    align: align,
    alignOffset: alignOffset
  };
}
function dedent(stream, state) {
  if (!state.scope.prev) return;
  if (state.scope.type === "coffee") {
    var _indent = stream.indentation();
    var matched = false;
    for (var scope = state.scope; scope; scope = scope.prev) {
      if (_indent === scope.offset) {
        matched = true;
        break;
      }
    }
    if (!matched) {
      return true;
    }
    while (state.scope.prev && state.scope.offset !== _indent) {
      state.scope = state.scope.prev;
    }
    return false;
  } else {
    state.scope = state.scope.prev;
    return false;
  }
}
function tokenLexer(stream, state) {
  var style = state.tokenize(stream, state);
  var current = stream.current();

  // Handle scope changes.
  if (current === "return") {
    state.dedent = true;
  }
  if ((current === "->" || current === "=>") && stream.eol() || style === "indent") {
    indent(stream, state);
  }
  var delimiter_index = "[({".indexOf(current);
  if (delimiter_index !== -1) {
    indent(stream, state, "])}".slice(delimiter_index, delimiter_index + 1));
  }
  if (indentKeywords.exec(current)) {
    indent(stream, state);
  }
  if (current == "then") {
    dedent(stream, state);
  }
  if (style === "dedent") {
    if (dedent(stream, state)) {
      return ERRORCLASS;
    }
  }
  delimiter_index = "])}".indexOf(current);
  if (delimiter_index !== -1) {
    while (state.scope.type == "coffee" && state.scope.prev) state.scope = state.scope.prev;
    if (state.scope.type == current) state.scope = state.scope.prev;
  }
  if (state.dedent && stream.eol()) {
    if (state.scope.type == "coffee" && state.scope.prev) state.scope = state.scope.prev;
    state.dedent = false;
  }
  return style == "indent" || style == "dedent" ? null : style;
}
const coffeeScript = {
  name: "coffeescript",
  startState: function () {
    return {
      tokenize: tokenBase,
      scope: {
        offset: 0,
        type: "coffee",
        prev: null,
        align: false
      },
      prop: false,
      dedent: 0
    };
  },
  token: function (stream, state) {
    var fillAlign = state.scope.align === null && state.scope;
    if (fillAlign && stream.sol()) fillAlign.align = false;
    var style = tokenLexer(stream, state);
    if (style && style != "comment") {
      if (fillAlign) fillAlign.align = true;
      state.prop = style == "punctuation" && stream.current() == ".";
    }
    return style;
  },
  indent: function (state, text) {
    if (state.tokenize != tokenBase) return 0;
    var scope = state.scope;
    var closer = text && "])}".indexOf(text.charAt(0)) > -1;
    if (closer) while (scope.type == "coffee" && scope.prev) scope = scope.prev;
    var closes = closer && scope.type === text.charAt(0);
    if (scope.align) return scope.alignOffset - (closes ? 1 : 0);else return (closes ? scope.prev : scope).offset;
  },
  languageData: {
    commentTokens: {
      line: "#"
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNTc2Ny5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGNvZGVtaXJyb3IvbGVnYWN5LW1vZGVzL21vZGUvY29mZmVlc2NyaXB0LmpzIl0sInNvdXJjZXNDb250ZW50IjpbInZhciBFUlJPUkNMQVNTID0gXCJlcnJvclwiO1xuZnVuY3Rpb24gd29yZFJlZ2V4cCh3b3Jkcykge1xuICByZXR1cm4gbmV3IFJlZ0V4cChcIl4oKFwiICsgd29yZHMuam9pbihcIil8KFwiKSArIFwiKSlcXFxcYlwiKTtcbn1cbnZhciBvcGVyYXRvcnMgPSAvXig/Oi0+fD0+fFxcK1srPV0/fC1bXFwtPV0/fFxcKltcXCo9XT98XFwvW1xcLz1dP3xbPSFdPXw8Wz48XT89P3w+Pj89P3wlPT98Jj0/fFxcfD0/fFxcXj0/fFxcfnwhfFxcP3wob3J8YW5kfFxcfFxcfHwmJnxcXD8pPSkvO1xudmFyIGRlbGltaXRlcnMgPSAvXig/OlsoKVxcW1xcXXt9LDpgPTtdfFxcLlxcLj9cXC4/KS87XG52YXIgaWRlbnRpZmllcnMgPSAvXltfQS1aYS16JF1bX0EtWmEteiQwLTldKi87XG52YXIgYXRQcm9wID0gL15AW19BLVphLXokXVtfQS1aYS16JDAtOV0qLztcbnZhciB3b3JkT3BlcmF0b3JzID0gd29yZFJlZ2V4cChbXCJhbmRcIiwgXCJvclwiLCBcIm5vdFwiLCBcImlzXCIsIFwiaXNudFwiLCBcImluXCIsIFwiaW5zdGFuY2VvZlwiLCBcInR5cGVvZlwiXSk7XG52YXIgaW5kZW50S2V5d29yZHMgPSBbXCJmb3JcIiwgXCJ3aGlsZVwiLCBcImxvb3BcIiwgXCJpZlwiLCBcInVubGVzc1wiLCBcImVsc2VcIiwgXCJzd2l0Y2hcIiwgXCJ0cnlcIiwgXCJjYXRjaFwiLCBcImZpbmFsbHlcIiwgXCJjbGFzc1wiXTtcbnZhciBjb21tb25LZXl3b3JkcyA9IFtcImJyZWFrXCIsIFwiYnlcIiwgXCJjb250aW51ZVwiLCBcImRlYnVnZ2VyXCIsIFwiZGVsZXRlXCIsIFwiZG9cIiwgXCJpblwiLCBcIm9mXCIsIFwibmV3XCIsIFwicmV0dXJuXCIsIFwidGhlblwiLCBcInRoaXNcIiwgXCJAXCIsIFwidGhyb3dcIiwgXCJ3aGVuXCIsIFwidW50aWxcIiwgXCJleHRlbmRzXCJdO1xudmFyIGtleXdvcmRzID0gd29yZFJlZ2V4cChpbmRlbnRLZXl3b3Jkcy5jb25jYXQoY29tbW9uS2V5d29yZHMpKTtcbmluZGVudEtleXdvcmRzID0gd29yZFJlZ2V4cChpbmRlbnRLZXl3b3Jkcyk7XG52YXIgc3RyaW5nUHJlZml4ZXMgPSAvXignezN9fFxcXCJ7M318WydcXFwiXSkvO1xudmFyIHJlZ2V4UHJlZml4ZXMgPSAvXihcXC97M318XFwvKS87XG52YXIgY29tbW9uQ29uc3RhbnRzID0gW1wiSW5maW5pdHlcIiwgXCJOYU5cIiwgXCJ1bmRlZmluZWRcIiwgXCJudWxsXCIsIFwidHJ1ZVwiLCBcImZhbHNlXCIsIFwib25cIiwgXCJvZmZcIiwgXCJ5ZXNcIiwgXCJub1wiXTtcbnZhciBjb25zdGFudHMgPSB3b3JkUmVnZXhwKGNvbW1vbkNvbnN0YW50cyk7XG5cbi8vIFRva2VuaXplcnNcbmZ1bmN0aW9uIHRva2VuQmFzZShzdHJlYW0sIHN0YXRlKSB7XG4gIC8vIEhhbmRsZSBzY29wZSBjaGFuZ2VzXG4gIGlmIChzdHJlYW0uc29sKCkpIHtcbiAgICBpZiAoc3RhdGUuc2NvcGUuYWxpZ24gPT09IG51bGwpIHN0YXRlLnNjb3BlLmFsaWduID0gZmFsc2U7XG4gICAgdmFyIHNjb3BlT2Zmc2V0ID0gc3RhdGUuc2NvcGUub2Zmc2V0O1xuICAgIGlmIChzdHJlYW0uZWF0U3BhY2UoKSkge1xuICAgICAgdmFyIGxpbmVPZmZzZXQgPSBzdHJlYW0uaW5kZW50YXRpb24oKTtcbiAgICAgIGlmIChsaW5lT2Zmc2V0ID4gc2NvcGVPZmZzZXQgJiYgc3RhdGUuc2NvcGUudHlwZSA9PSBcImNvZmZlZVwiKSB7XG4gICAgICAgIHJldHVybiBcImluZGVudFwiO1xuICAgICAgfSBlbHNlIGlmIChsaW5lT2Zmc2V0IDwgc2NvcGVPZmZzZXQpIHtcbiAgICAgICAgcmV0dXJuIFwiZGVkZW50XCI7XG4gICAgICB9XG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9IGVsc2Uge1xuICAgICAgaWYgKHNjb3BlT2Zmc2V0ID4gMCkge1xuICAgICAgICBkZWRlbnQoc3RyZWFtLCBzdGF0ZSk7XG4gICAgICB9XG4gICAgfVxuICB9XG4gIGlmIChzdHJlYW0uZWF0U3BhY2UoKSkge1xuICAgIHJldHVybiBudWxsO1xuICB9XG4gIHZhciBjaCA9IHN0cmVhbS5wZWVrKCk7XG5cbiAgLy8gSGFuZGxlIGRvY2NvIHRpdGxlIGNvbW1lbnQgKHNpbmdsZSBsaW5lKVxuICBpZiAoc3RyZWFtLm1hdGNoKFwiIyMjI1wiKSkge1xuICAgIHN0cmVhbS5za2lwVG9FbmQoKTtcbiAgICByZXR1cm4gXCJjb21tZW50XCI7XG4gIH1cblxuICAvLyBIYW5kbGUgbXVsdGkgbGluZSBjb21tZW50c1xuICBpZiAoc3RyZWFtLm1hdGNoKFwiIyMjXCIpKSB7XG4gICAgc3RhdGUudG9rZW5pemUgPSBsb25nQ29tbWVudDtcbiAgICByZXR1cm4gc3RhdGUudG9rZW5pemUoc3RyZWFtLCBzdGF0ZSk7XG4gIH1cblxuICAvLyBTaW5nbGUgbGluZSBjb21tZW50XG4gIGlmIChjaCA9PT0gXCIjXCIpIHtcbiAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICB9XG5cbiAgLy8gSGFuZGxlIG51bWJlciBsaXRlcmFsc1xuICBpZiAoc3RyZWFtLm1hdGNoKC9eLT9bMC05XFwuXS8sIGZhbHNlKSkge1xuICAgIHZhciBmbG9hdExpdGVyYWwgPSBmYWxzZTtcbiAgICAvLyBGbG9hdHNcbiAgICBpZiAoc3RyZWFtLm1hdGNoKC9eLT9cXGQqXFwuXFxkKyhlW1xcK1xcLV0/XFxkKyk/L2kpKSB7XG4gICAgICBmbG9hdExpdGVyYWwgPSB0cnVlO1xuICAgIH1cbiAgICBpZiAoc3RyZWFtLm1hdGNoKC9eLT9cXGQrXFwuXFxkKi8pKSB7XG4gICAgICBmbG9hdExpdGVyYWwgPSB0cnVlO1xuICAgIH1cbiAgICBpZiAoc3RyZWFtLm1hdGNoKC9eLT9cXC5cXGQrLykpIHtcbiAgICAgIGZsb2F0TGl0ZXJhbCA9IHRydWU7XG4gICAgfVxuICAgIGlmIChmbG9hdExpdGVyYWwpIHtcbiAgICAgIC8vIHByZXZlbnQgZnJvbSBnZXR0aW5nIGV4dHJhIC4gb24gMS4uXG4gICAgICBpZiAoc3RyZWFtLnBlZWsoKSA9PSBcIi5cIikge1xuICAgICAgICBzdHJlYW0uYmFja1VwKDEpO1xuICAgICAgfVxuICAgICAgcmV0dXJuIFwibnVtYmVyXCI7XG4gICAgfVxuICAgIC8vIEludGVnZXJzXG4gICAgdmFyIGludExpdGVyYWwgPSBmYWxzZTtcbiAgICAvLyBIZXhcbiAgICBpZiAoc3RyZWFtLm1hdGNoKC9eLT8weFswLTlhLWZdKy9pKSkge1xuICAgICAgaW50TGl0ZXJhbCA9IHRydWU7XG4gICAgfVxuICAgIC8vIERlY2ltYWxcbiAgICBpZiAoc3RyZWFtLm1hdGNoKC9eLT9bMS05XVxcZCooZVtcXCtcXC1dP1xcZCspPy8pKSB7XG4gICAgICBpbnRMaXRlcmFsID0gdHJ1ZTtcbiAgICB9XG4gICAgLy8gWmVybyBieSBpdHNlbGYgd2l0aCBubyBvdGhlciBwaWVjZSBvZiBudW1iZXIuXG4gICAgaWYgKHN0cmVhbS5tYXRjaCgvXi0/MCg/IVtcXGR4XSkvaSkpIHtcbiAgICAgIGludExpdGVyYWwgPSB0cnVlO1xuICAgIH1cbiAgICBpZiAoaW50TGl0ZXJhbCkge1xuICAgICAgcmV0dXJuIFwibnVtYmVyXCI7XG4gICAgfVxuICB9XG5cbiAgLy8gSGFuZGxlIHN0cmluZ3NcbiAgaWYgKHN0cmVhbS5tYXRjaChzdHJpbmdQcmVmaXhlcykpIHtcbiAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuRmFjdG9yeShzdHJlYW0uY3VycmVudCgpLCBmYWxzZSwgXCJzdHJpbmdcIik7XG4gICAgcmV0dXJuIHN0YXRlLnRva2VuaXplKHN0cmVhbSwgc3RhdGUpO1xuICB9XG4gIC8vIEhhbmRsZSByZWdleCBsaXRlcmFsc1xuICBpZiAoc3RyZWFtLm1hdGNoKHJlZ2V4UHJlZml4ZXMpKSB7XG4gICAgaWYgKHN0cmVhbS5jdXJyZW50KCkgIT0gXCIvXCIgfHwgc3RyZWFtLm1hdGNoKC9eLipcXC8vLCBmYWxzZSkpIHtcbiAgICAgIC8vIHByZXZlbnQgaGlnaGxpZ2h0IG9mIGRpdmlzaW9uXG4gICAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuRmFjdG9yeShzdHJlYW0uY3VycmVudCgpLCB0cnVlLCBcInN0cmluZy5zcGVjaWFsXCIpO1xuICAgICAgcmV0dXJuIHN0YXRlLnRva2VuaXplKHN0cmVhbSwgc3RhdGUpO1xuICAgIH0gZWxzZSB7XG4gICAgICBzdHJlYW0uYmFja1VwKDEpO1xuICAgIH1cbiAgfVxuXG4gIC8vIEhhbmRsZSBvcGVyYXRvcnMgYW5kIGRlbGltaXRlcnNcbiAgaWYgKHN0cmVhbS5tYXRjaChvcGVyYXRvcnMpIHx8IHN0cmVhbS5tYXRjaCh3b3JkT3BlcmF0b3JzKSkge1xuICAgIHJldHVybiBcIm9wZXJhdG9yXCI7XG4gIH1cbiAgaWYgKHN0cmVhbS5tYXRjaChkZWxpbWl0ZXJzKSkge1xuICAgIHJldHVybiBcInB1bmN0dWF0aW9uXCI7XG4gIH1cbiAgaWYgKHN0cmVhbS5tYXRjaChjb25zdGFudHMpKSB7XG4gICAgcmV0dXJuIFwiYXRvbVwiO1xuICB9XG4gIGlmIChzdHJlYW0ubWF0Y2goYXRQcm9wKSB8fCBzdGF0ZS5wcm9wICYmIHN0cmVhbS5tYXRjaChpZGVudGlmaWVycykpIHtcbiAgICByZXR1cm4gXCJwcm9wZXJ0eVwiO1xuICB9XG4gIGlmIChzdHJlYW0ubWF0Y2goa2V5d29yZHMpKSB7XG4gICAgcmV0dXJuIFwia2V5d29yZFwiO1xuICB9XG4gIGlmIChzdHJlYW0ubWF0Y2goaWRlbnRpZmllcnMpKSB7XG4gICAgcmV0dXJuIFwidmFyaWFibGVcIjtcbiAgfVxuXG4gIC8vIEhhbmRsZSBub24tZGV0ZWN0ZWQgaXRlbXNcbiAgc3RyZWFtLm5leHQoKTtcbiAgcmV0dXJuIEVSUk9SQ0xBU1M7XG59XG5mdW5jdGlvbiB0b2tlbkZhY3RvcnkoZGVsaW1pdGVyLCBzaW5nbGVsaW5lLCBvdXRjbGFzcykge1xuICByZXR1cm4gZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICB3aGlsZSAoIXN0cmVhbS5lb2woKSkge1xuICAgICAgc3RyZWFtLmVhdFdoaWxlKC9bXidcIlxcL1xcXFxdLyk7XG4gICAgICBpZiAoc3RyZWFtLmVhdChcIlxcXFxcIikpIHtcbiAgICAgICAgc3RyZWFtLm5leHQoKTtcbiAgICAgICAgaWYgKHNpbmdsZWxpbmUgJiYgc3RyZWFtLmVvbCgpKSB7XG4gICAgICAgICAgcmV0dXJuIG91dGNsYXNzO1xuICAgICAgICB9XG4gICAgICB9IGVsc2UgaWYgKHN0cmVhbS5tYXRjaChkZWxpbWl0ZXIpKSB7XG4gICAgICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlO1xuICAgICAgICByZXR1cm4gb3V0Y2xhc3M7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBzdHJlYW0uZWF0KC9bJ1wiXFwvXS8pO1xuICAgICAgfVxuICAgIH1cbiAgICBpZiAoc2luZ2xlbGluZSkge1xuICAgICAgc3RhdGUudG9rZW5pemUgPSB0b2tlbkJhc2U7XG4gICAgfVxuICAgIHJldHVybiBvdXRjbGFzcztcbiAgfTtcbn1cbmZ1bmN0aW9uIGxvbmdDb21tZW50KHN0cmVhbSwgc3RhdGUpIHtcbiAgd2hpbGUgKCFzdHJlYW0uZW9sKCkpIHtcbiAgICBzdHJlYW0uZWF0V2hpbGUoL1teI10vKTtcbiAgICBpZiAoc3RyZWFtLm1hdGNoKFwiIyMjXCIpKSB7XG4gICAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQmFzZTtcbiAgICAgIGJyZWFrO1xuICAgIH1cbiAgICBzdHJlYW0uZWF0V2hpbGUoXCIjXCIpO1xuICB9XG4gIHJldHVybiBcImNvbW1lbnRcIjtcbn1cbmZ1bmN0aW9uIGluZGVudChzdHJlYW0sIHN0YXRlLCB0eXBlID0gXCJjb2ZmZWVcIikge1xuICB2YXIgb2Zmc2V0ID0gMCxcbiAgICBhbGlnbiA9IGZhbHNlLFxuICAgIGFsaWduT2Zmc2V0ID0gbnVsbDtcbiAgZm9yICh2YXIgc2NvcGUgPSBzdGF0ZS5zY29wZTsgc2NvcGU7IHNjb3BlID0gc2NvcGUucHJldikge1xuICAgIGlmIChzY29wZS50eXBlID09PSBcImNvZmZlZVwiIHx8IHNjb3BlLnR5cGUgPT0gXCJ9XCIpIHtcbiAgICAgIG9mZnNldCA9IHNjb3BlLm9mZnNldCArIHN0cmVhbS5pbmRlbnRVbml0O1xuICAgICAgYnJlYWs7XG4gICAgfVxuICB9XG4gIGlmICh0eXBlICE9PSBcImNvZmZlZVwiKSB7XG4gICAgYWxpZ24gPSBudWxsO1xuICAgIGFsaWduT2Zmc2V0ID0gc3RyZWFtLmNvbHVtbigpICsgc3RyZWFtLmN1cnJlbnQoKS5sZW5ndGg7XG4gIH0gZWxzZSBpZiAoc3RhdGUuc2NvcGUuYWxpZ24pIHtcbiAgICBzdGF0ZS5zY29wZS5hbGlnbiA9IGZhbHNlO1xuICB9XG4gIHN0YXRlLnNjb3BlID0ge1xuICAgIG9mZnNldDogb2Zmc2V0LFxuICAgIHR5cGU6IHR5cGUsXG4gICAgcHJldjogc3RhdGUuc2NvcGUsXG4gICAgYWxpZ246IGFsaWduLFxuICAgIGFsaWduT2Zmc2V0OiBhbGlnbk9mZnNldFxuICB9O1xufVxuZnVuY3Rpb24gZGVkZW50KHN0cmVhbSwgc3RhdGUpIHtcbiAgaWYgKCFzdGF0ZS5zY29wZS5wcmV2KSByZXR1cm47XG4gIGlmIChzdGF0ZS5zY29wZS50eXBlID09PSBcImNvZmZlZVwiKSB7XG4gICAgdmFyIF9pbmRlbnQgPSBzdHJlYW0uaW5kZW50YXRpb24oKTtcbiAgICB2YXIgbWF0Y2hlZCA9IGZhbHNlO1xuICAgIGZvciAodmFyIHNjb3BlID0gc3RhdGUuc2NvcGU7IHNjb3BlOyBzY29wZSA9IHNjb3BlLnByZXYpIHtcbiAgICAgIGlmIChfaW5kZW50ID09PSBzY29wZS5vZmZzZXQpIHtcbiAgICAgICAgbWF0Y2hlZCA9IHRydWU7XG4gICAgICAgIGJyZWFrO1xuICAgICAgfVxuICAgIH1cbiAgICBpZiAoIW1hdGNoZWQpIHtcbiAgICAgIHJldHVybiB0cnVlO1xuICAgIH1cbiAgICB3aGlsZSAoc3RhdGUuc2NvcGUucHJldiAmJiBzdGF0ZS5zY29wZS5vZmZzZXQgIT09IF9pbmRlbnQpIHtcbiAgICAgIHN0YXRlLnNjb3BlID0gc3RhdGUuc2NvcGUucHJldjtcbiAgICB9XG4gICAgcmV0dXJuIGZhbHNlO1xuICB9IGVsc2Uge1xuICAgIHN0YXRlLnNjb3BlID0gc3RhdGUuc2NvcGUucHJldjtcbiAgICByZXR1cm4gZmFsc2U7XG4gIH1cbn1cbmZ1bmN0aW9uIHRva2VuTGV4ZXIoc3RyZWFtLCBzdGF0ZSkge1xuICB2YXIgc3R5bGUgPSBzdGF0ZS50b2tlbml6ZShzdHJlYW0sIHN0YXRlKTtcbiAgdmFyIGN1cnJlbnQgPSBzdHJlYW0uY3VycmVudCgpO1xuXG4gIC8vIEhhbmRsZSBzY29wZSBjaGFuZ2VzLlxuICBpZiAoY3VycmVudCA9PT0gXCJyZXR1cm5cIikge1xuICAgIHN0YXRlLmRlZGVudCA9IHRydWU7XG4gIH1cbiAgaWYgKChjdXJyZW50ID09PSBcIi0+XCIgfHwgY3VycmVudCA9PT0gXCI9PlwiKSAmJiBzdHJlYW0uZW9sKCkgfHwgc3R5bGUgPT09IFwiaW5kZW50XCIpIHtcbiAgICBpbmRlbnQoc3RyZWFtLCBzdGF0ZSk7XG4gIH1cbiAgdmFyIGRlbGltaXRlcl9pbmRleCA9IFwiWyh7XCIuaW5kZXhPZihjdXJyZW50KTtcbiAgaWYgKGRlbGltaXRlcl9pbmRleCAhPT0gLTEpIHtcbiAgICBpbmRlbnQoc3RyZWFtLCBzdGF0ZSwgXCJdKX1cIi5zbGljZShkZWxpbWl0ZXJfaW5kZXgsIGRlbGltaXRlcl9pbmRleCArIDEpKTtcbiAgfVxuICBpZiAoaW5kZW50S2V5d29yZHMuZXhlYyhjdXJyZW50KSkge1xuICAgIGluZGVudChzdHJlYW0sIHN0YXRlKTtcbiAgfVxuICBpZiAoY3VycmVudCA9PSBcInRoZW5cIikge1xuICAgIGRlZGVudChzdHJlYW0sIHN0YXRlKTtcbiAgfVxuICBpZiAoc3R5bGUgPT09IFwiZGVkZW50XCIpIHtcbiAgICBpZiAoZGVkZW50KHN0cmVhbSwgc3RhdGUpKSB7XG4gICAgICByZXR1cm4gRVJST1JDTEFTUztcbiAgICB9XG4gIH1cbiAgZGVsaW1pdGVyX2luZGV4ID0gXCJdKX1cIi5pbmRleE9mKGN1cnJlbnQpO1xuICBpZiAoZGVsaW1pdGVyX2luZGV4ICE9PSAtMSkge1xuICAgIHdoaWxlIChzdGF0ZS5zY29wZS50eXBlID09IFwiY29mZmVlXCIgJiYgc3RhdGUuc2NvcGUucHJldikgc3RhdGUuc2NvcGUgPSBzdGF0ZS5zY29wZS5wcmV2O1xuICAgIGlmIChzdGF0ZS5zY29wZS50eXBlID09IGN1cnJlbnQpIHN0YXRlLnNjb3BlID0gc3RhdGUuc2NvcGUucHJldjtcbiAgfVxuICBpZiAoc3RhdGUuZGVkZW50ICYmIHN0cmVhbS5lb2woKSkge1xuICAgIGlmIChzdGF0ZS5zY29wZS50eXBlID09IFwiY29mZmVlXCIgJiYgc3RhdGUuc2NvcGUucHJldikgc3RhdGUuc2NvcGUgPSBzdGF0ZS5zY29wZS5wcmV2O1xuICAgIHN0YXRlLmRlZGVudCA9IGZhbHNlO1xuICB9XG4gIHJldHVybiBzdHlsZSA9PSBcImluZGVudFwiIHx8IHN0eWxlID09IFwiZGVkZW50XCIgPyBudWxsIDogc3R5bGU7XG59XG5leHBvcnQgY29uc3QgY29mZmVlU2NyaXB0ID0ge1xuICBuYW1lOiBcImNvZmZlZXNjcmlwdFwiLFxuICBzdGFydFN0YXRlOiBmdW5jdGlvbiAoKSB7XG4gICAgcmV0dXJuIHtcbiAgICAgIHRva2VuaXplOiB0b2tlbkJhc2UsXG4gICAgICBzY29wZToge1xuICAgICAgICBvZmZzZXQ6IDAsXG4gICAgICAgIHR5cGU6IFwiY29mZmVlXCIsXG4gICAgICAgIHByZXY6IG51bGwsXG4gICAgICAgIGFsaWduOiBmYWxzZVxuICAgICAgfSxcbiAgICAgIHByb3A6IGZhbHNlLFxuICAgICAgZGVkZW50OiAwXG4gICAgfTtcbiAgfSxcbiAgdG9rZW46IGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgdmFyIGZpbGxBbGlnbiA9IHN0YXRlLnNjb3BlLmFsaWduID09PSBudWxsICYmIHN0YXRlLnNjb3BlO1xuICAgIGlmIChmaWxsQWxpZ24gJiYgc3RyZWFtLnNvbCgpKSBmaWxsQWxpZ24uYWxpZ24gPSBmYWxzZTtcbiAgICB2YXIgc3R5bGUgPSB0b2tlbkxleGVyKHN0cmVhbSwgc3RhdGUpO1xuICAgIGlmIChzdHlsZSAmJiBzdHlsZSAhPSBcImNvbW1lbnRcIikge1xuICAgICAgaWYgKGZpbGxBbGlnbikgZmlsbEFsaWduLmFsaWduID0gdHJ1ZTtcbiAgICAgIHN0YXRlLnByb3AgPSBzdHlsZSA9PSBcInB1bmN0dWF0aW9uXCIgJiYgc3RyZWFtLmN1cnJlbnQoKSA9PSBcIi5cIjtcbiAgICB9XG4gICAgcmV0dXJuIHN0eWxlO1xuICB9LFxuICBpbmRlbnQ6IGZ1bmN0aW9uIChzdGF0ZSwgdGV4dCkge1xuICAgIGlmIChzdGF0ZS50b2tlbml6ZSAhPSB0b2tlbkJhc2UpIHJldHVybiAwO1xuICAgIHZhciBzY29wZSA9IHN0YXRlLnNjb3BlO1xuICAgIHZhciBjbG9zZXIgPSB0ZXh0ICYmIFwiXSl9XCIuaW5kZXhPZih0ZXh0LmNoYXJBdCgwKSkgPiAtMTtcbiAgICBpZiAoY2xvc2VyKSB3aGlsZSAoc2NvcGUudHlwZSA9PSBcImNvZmZlZVwiICYmIHNjb3BlLnByZXYpIHNjb3BlID0gc2NvcGUucHJldjtcbiAgICB2YXIgY2xvc2VzID0gY2xvc2VyICYmIHNjb3BlLnR5cGUgPT09IHRleHQuY2hhckF0KDApO1xuICAgIGlmIChzY29wZS5hbGlnbikgcmV0dXJuIHNjb3BlLmFsaWduT2Zmc2V0IC0gKGNsb3NlcyA/IDEgOiAwKTtlbHNlIHJldHVybiAoY2xvc2VzID8gc2NvcGUucHJldiA6IHNjb3BlKS5vZmZzZXQ7XG4gIH0sXG4gIGxhbmd1YWdlRGF0YToge1xuICAgIGNvbW1lbnRUb2tlbnM6IHtcbiAgICAgIGxpbmU6IFwiI1wiXG4gICAgfVxuICB9XG59OyJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==