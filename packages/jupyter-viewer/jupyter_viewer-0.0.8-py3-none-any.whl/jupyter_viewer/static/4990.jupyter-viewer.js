"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[4990],{

/***/ 34990:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "r": () => (/* binding */ r)
/* harmony export */ });
function wordObj(words) {
  var res = {};
  for (var i = 0; i < words.length; ++i) res[words[i]] = true;
  return res;
}
var commonAtoms = ["NULL", "NA", "Inf", "NaN", "NA_integer_", "NA_real_", "NA_complex_", "NA_character_", "TRUE", "FALSE"];
var commonBuiltins = ["list", "quote", "bquote", "eval", "return", "call", "parse", "deparse"];
var commonKeywords = ["if", "else", "repeat", "while", "function", "for", "in", "next", "break"];
var commonBlockKeywords = ["if", "else", "repeat", "while", "function", "for"];
var atoms = wordObj(commonAtoms);
var builtins = wordObj(commonBuiltins);
var keywords = wordObj(commonKeywords);
var blockkeywords = wordObj(commonBlockKeywords);
var opChars = /[+\-*\/^<>=!&|~$:]/;
var curPunc;
function tokenBase(stream, state) {
  curPunc = null;
  var ch = stream.next();
  if (ch == "#") {
    stream.skipToEnd();
    return "comment";
  } else if (ch == "0" && stream.eat("x")) {
    stream.eatWhile(/[\da-f]/i);
    return "number";
  } else if (ch == "." && stream.eat(/\d/)) {
    stream.match(/\d*(?:e[+\-]?\d+)?/);
    return "number";
  } else if (/\d/.test(ch)) {
    stream.match(/\d*(?:\.\d+)?(?:e[+\-]\d+)?L?/);
    return "number";
  } else if (ch == "'" || ch == '"') {
    state.tokenize = tokenString(ch);
    return "string";
  } else if (ch == "`") {
    stream.match(/[^`]+`/);
    return "string.special";
  } else if (ch == "." && stream.match(/.(?:[.]|\d+)/)) {
    return "keyword";
  } else if (/[a-zA-Z\.]/.test(ch)) {
    stream.eatWhile(/[\w\.]/);
    var word = stream.current();
    if (atoms.propertyIsEnumerable(word)) return "atom";
    if (keywords.propertyIsEnumerable(word)) {
      // Block keywords start new blocks, except 'else if', which only starts
      // one new block for the 'if', no block for the 'else'.
      if (blockkeywords.propertyIsEnumerable(word) && !stream.match(/\s*if(\s+|$)/, false)) curPunc = "block";
      return "keyword";
    }
    if (builtins.propertyIsEnumerable(word)) return "builtin";
    return "variable";
  } else if (ch == "%") {
    if (stream.skipTo("%")) stream.next();
    return "variableName.special";
  } else if (ch == "<" && stream.eat("-") || ch == "<" && stream.match("<-") || ch == "-" && stream.match(/>>?/)) {
    return "operator";
  } else if (ch == "=" && state.ctx.argList) {
    return "operator";
  } else if (opChars.test(ch)) {
    if (ch == "$") return "operator";
    stream.eatWhile(opChars);
    return "operator";
  } else if (/[\(\){}\[\];]/.test(ch)) {
    curPunc = ch;
    if (ch == ";") return "punctuation";
    return null;
  } else {
    return null;
  }
}
function tokenString(quote) {
  return function (stream, state) {
    if (stream.eat("\\")) {
      var ch = stream.next();
      if (ch == "x") stream.match(/^[a-f0-9]{2}/i);else if ((ch == "u" || ch == "U") && stream.eat("{") && stream.skipTo("}")) stream.next();else if (ch == "u") stream.match(/^[a-f0-9]{4}/i);else if (ch == "U") stream.match(/^[a-f0-9]{8}/i);else if (/[0-7]/.test(ch)) stream.match(/^[0-7]{1,2}/);
      return "string.special";
    } else {
      var next;
      while ((next = stream.next()) != null) {
        if (next == quote) {
          state.tokenize = tokenBase;
          break;
        }
        if (next == "\\") {
          stream.backUp(1);
          break;
        }
      }
      return "string";
    }
  };
}
var ALIGN_YES = 1,
  ALIGN_NO = 2,
  BRACELESS = 4;
function push(state, type, stream) {
  state.ctx = {
    type: type,
    indent: state.indent,
    flags: 0,
    column: stream.column(),
    prev: state.ctx
  };
}
function setFlag(state, flag) {
  var ctx = state.ctx;
  state.ctx = {
    type: ctx.type,
    indent: ctx.indent,
    flags: ctx.flags | flag,
    column: ctx.column,
    prev: ctx.prev
  };
}
function pop(state) {
  state.indent = state.ctx.indent;
  state.ctx = state.ctx.prev;
}
const r = {
  name: "r",
  startState: function (indentUnit) {
    return {
      tokenize: tokenBase,
      ctx: {
        type: "top",
        indent: -indentUnit,
        flags: ALIGN_NO
      },
      indent: 0,
      afterIdent: false
    };
  },
  token: function (stream, state) {
    if (stream.sol()) {
      if ((state.ctx.flags & 3) == 0) state.ctx.flags |= ALIGN_NO;
      if (state.ctx.flags & BRACELESS) pop(state);
      state.indent = stream.indentation();
    }
    if (stream.eatSpace()) return null;
    var style = state.tokenize(stream, state);
    if (style != "comment" && (state.ctx.flags & ALIGN_NO) == 0) setFlag(state, ALIGN_YES);
    if ((curPunc == ";" || curPunc == "{" || curPunc == "}") && state.ctx.type == "block") pop(state);
    if (curPunc == "{") push(state, "}", stream);else if (curPunc == "(") {
      push(state, ")", stream);
      if (state.afterIdent) state.ctx.argList = true;
    } else if (curPunc == "[") push(state, "]", stream);else if (curPunc == "block") push(state, "block", stream);else if (curPunc == state.ctx.type) pop(state);else if (state.ctx.type == "block" && style != "comment") setFlag(state, BRACELESS);
    state.afterIdent = style == "variable" || style == "keyword";
    return style;
  },
  indent: function (state, textAfter, cx) {
    if (state.tokenize != tokenBase) return 0;
    var firstChar = textAfter && textAfter.charAt(0),
      ctx = state.ctx,
      closing = firstChar == ctx.type;
    if (ctx.flags & BRACELESS) ctx = ctx.prev;
    if (ctx.type == "block") return ctx.indent + (firstChar == "{" ? 0 : cx.unit);else if (ctx.flags & ALIGN_YES) return ctx.column + (closing ? 0 : 1);else return ctx.indent + (closing ? 0 : cx.unit);
  },
  languageData: {
    wordChars: ".",
    commentTokens: {
      line: "#"
    },
    autocomplete: commonAtoms.concat(commonBuiltins, commonKeywords)
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNDk5MC5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGNvZGVtaXJyb3IvbGVnYWN5LW1vZGVzL21vZGUvci5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyJmdW5jdGlvbiB3b3JkT2JqKHdvcmRzKSB7XG4gIHZhciByZXMgPSB7fTtcbiAgZm9yICh2YXIgaSA9IDA7IGkgPCB3b3Jkcy5sZW5ndGg7ICsraSkgcmVzW3dvcmRzW2ldXSA9IHRydWU7XG4gIHJldHVybiByZXM7XG59XG52YXIgY29tbW9uQXRvbXMgPSBbXCJOVUxMXCIsIFwiTkFcIiwgXCJJbmZcIiwgXCJOYU5cIiwgXCJOQV9pbnRlZ2VyX1wiLCBcIk5BX3JlYWxfXCIsIFwiTkFfY29tcGxleF9cIiwgXCJOQV9jaGFyYWN0ZXJfXCIsIFwiVFJVRVwiLCBcIkZBTFNFXCJdO1xudmFyIGNvbW1vbkJ1aWx0aW5zID0gW1wibGlzdFwiLCBcInF1b3RlXCIsIFwiYnF1b3RlXCIsIFwiZXZhbFwiLCBcInJldHVyblwiLCBcImNhbGxcIiwgXCJwYXJzZVwiLCBcImRlcGFyc2VcIl07XG52YXIgY29tbW9uS2V5d29yZHMgPSBbXCJpZlwiLCBcImVsc2VcIiwgXCJyZXBlYXRcIiwgXCJ3aGlsZVwiLCBcImZ1bmN0aW9uXCIsIFwiZm9yXCIsIFwiaW5cIiwgXCJuZXh0XCIsIFwiYnJlYWtcIl07XG52YXIgY29tbW9uQmxvY2tLZXl3b3JkcyA9IFtcImlmXCIsIFwiZWxzZVwiLCBcInJlcGVhdFwiLCBcIndoaWxlXCIsIFwiZnVuY3Rpb25cIiwgXCJmb3JcIl07XG52YXIgYXRvbXMgPSB3b3JkT2JqKGNvbW1vbkF0b21zKTtcbnZhciBidWlsdGlucyA9IHdvcmRPYmooY29tbW9uQnVpbHRpbnMpO1xudmFyIGtleXdvcmRzID0gd29yZE9iaihjb21tb25LZXl3b3Jkcyk7XG52YXIgYmxvY2trZXl3b3JkcyA9IHdvcmRPYmooY29tbW9uQmxvY2tLZXl3b3Jkcyk7XG52YXIgb3BDaGFycyA9IC9bK1xcLSpcXC9ePD49ISZ8fiQ6XS87XG52YXIgY3VyUHVuYztcbmZ1bmN0aW9uIHRva2VuQmFzZShzdHJlYW0sIHN0YXRlKSB7XG4gIGN1clB1bmMgPSBudWxsO1xuICB2YXIgY2ggPSBzdHJlYW0ubmV4dCgpO1xuICBpZiAoY2ggPT0gXCIjXCIpIHtcbiAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICB9IGVsc2UgaWYgKGNoID09IFwiMFwiICYmIHN0cmVhbS5lYXQoXCJ4XCIpKSB7XG4gICAgc3RyZWFtLmVhdFdoaWxlKC9bXFxkYS1mXS9pKTtcbiAgICByZXR1cm4gXCJudW1iZXJcIjtcbiAgfSBlbHNlIGlmIChjaCA9PSBcIi5cIiAmJiBzdHJlYW0uZWF0KC9cXGQvKSkge1xuICAgIHN0cmVhbS5tYXRjaCgvXFxkKig/OmVbK1xcLV0/XFxkKyk/Lyk7XG4gICAgcmV0dXJuIFwibnVtYmVyXCI7XG4gIH0gZWxzZSBpZiAoL1xcZC8udGVzdChjaCkpIHtcbiAgICBzdHJlYW0ubWF0Y2goL1xcZCooPzpcXC5cXGQrKT8oPzplWytcXC1dXFxkKyk/TD8vKTtcbiAgICByZXR1cm4gXCJudW1iZXJcIjtcbiAgfSBlbHNlIGlmIChjaCA9PSBcIidcIiB8fCBjaCA9PSAnXCInKSB7XG4gICAgc3RhdGUudG9rZW5pemUgPSB0b2tlblN0cmluZyhjaCk7XG4gICAgcmV0dXJuIFwic3RyaW5nXCI7XG4gIH0gZWxzZSBpZiAoY2ggPT0gXCJgXCIpIHtcbiAgICBzdHJlYW0ubWF0Y2goL1teYF0rYC8pO1xuICAgIHJldHVybiBcInN0cmluZy5zcGVjaWFsXCI7XG4gIH0gZWxzZSBpZiAoY2ggPT0gXCIuXCIgJiYgc3RyZWFtLm1hdGNoKC8uKD86Wy5dfFxcZCspLykpIHtcbiAgICByZXR1cm4gXCJrZXl3b3JkXCI7XG4gIH0gZWxzZSBpZiAoL1thLXpBLVpcXC5dLy50ZXN0KGNoKSkge1xuICAgIHN0cmVhbS5lYXRXaGlsZSgvW1xcd1xcLl0vKTtcbiAgICB2YXIgd29yZCA9IHN0cmVhbS5jdXJyZW50KCk7XG4gICAgaWYgKGF0b21zLnByb3BlcnR5SXNFbnVtZXJhYmxlKHdvcmQpKSByZXR1cm4gXCJhdG9tXCI7XG4gICAgaWYgKGtleXdvcmRzLnByb3BlcnR5SXNFbnVtZXJhYmxlKHdvcmQpKSB7XG4gICAgICAvLyBCbG9jayBrZXl3b3JkcyBzdGFydCBuZXcgYmxvY2tzLCBleGNlcHQgJ2Vsc2UgaWYnLCB3aGljaCBvbmx5IHN0YXJ0c1xuICAgICAgLy8gb25lIG5ldyBibG9jayBmb3IgdGhlICdpZicsIG5vIGJsb2NrIGZvciB0aGUgJ2Vsc2UnLlxuICAgICAgaWYgKGJsb2Nra2V5d29yZHMucHJvcGVydHlJc0VudW1lcmFibGUod29yZCkgJiYgIXN0cmVhbS5tYXRjaCgvXFxzKmlmKFxccyt8JCkvLCBmYWxzZSkpIGN1clB1bmMgPSBcImJsb2NrXCI7XG4gICAgICByZXR1cm4gXCJrZXl3b3JkXCI7XG4gICAgfVxuICAgIGlmIChidWlsdGlucy5wcm9wZXJ0eUlzRW51bWVyYWJsZSh3b3JkKSkgcmV0dXJuIFwiYnVpbHRpblwiO1xuICAgIHJldHVybiBcInZhcmlhYmxlXCI7XG4gIH0gZWxzZSBpZiAoY2ggPT0gXCIlXCIpIHtcbiAgICBpZiAoc3RyZWFtLnNraXBUbyhcIiVcIikpIHN0cmVhbS5uZXh0KCk7XG4gICAgcmV0dXJuIFwidmFyaWFibGVOYW1lLnNwZWNpYWxcIjtcbiAgfSBlbHNlIGlmIChjaCA9PSBcIjxcIiAmJiBzdHJlYW0uZWF0KFwiLVwiKSB8fCBjaCA9PSBcIjxcIiAmJiBzdHJlYW0ubWF0Y2goXCI8LVwiKSB8fCBjaCA9PSBcIi1cIiAmJiBzdHJlYW0ubWF0Y2goLz4+Py8pKSB7XG4gICAgcmV0dXJuIFwib3BlcmF0b3JcIjtcbiAgfSBlbHNlIGlmIChjaCA9PSBcIj1cIiAmJiBzdGF0ZS5jdHguYXJnTGlzdCkge1xuICAgIHJldHVybiBcIm9wZXJhdG9yXCI7XG4gIH0gZWxzZSBpZiAob3BDaGFycy50ZXN0KGNoKSkge1xuICAgIGlmIChjaCA9PSBcIiRcIikgcmV0dXJuIFwib3BlcmF0b3JcIjtcbiAgICBzdHJlYW0uZWF0V2hpbGUob3BDaGFycyk7XG4gICAgcmV0dXJuIFwib3BlcmF0b3JcIjtcbiAgfSBlbHNlIGlmICgvW1xcKFxcKXt9XFxbXFxdO10vLnRlc3QoY2gpKSB7XG4gICAgY3VyUHVuYyA9IGNoO1xuICAgIGlmIChjaCA9PSBcIjtcIikgcmV0dXJuIFwicHVuY3R1YXRpb25cIjtcbiAgICByZXR1cm4gbnVsbDtcbiAgfSBlbHNlIHtcbiAgICByZXR1cm4gbnVsbDtcbiAgfVxufVxuZnVuY3Rpb24gdG9rZW5TdHJpbmcocXVvdGUpIHtcbiAgcmV0dXJuIGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgaWYgKHN0cmVhbS5lYXQoXCJcXFxcXCIpKSB7XG4gICAgICB2YXIgY2ggPSBzdHJlYW0ubmV4dCgpO1xuICAgICAgaWYgKGNoID09IFwieFwiKSBzdHJlYW0ubWF0Y2goL15bYS1mMC05XXsyfS9pKTtlbHNlIGlmICgoY2ggPT0gXCJ1XCIgfHwgY2ggPT0gXCJVXCIpICYmIHN0cmVhbS5lYXQoXCJ7XCIpICYmIHN0cmVhbS5za2lwVG8oXCJ9XCIpKSBzdHJlYW0ubmV4dCgpO2Vsc2UgaWYgKGNoID09IFwidVwiKSBzdHJlYW0ubWF0Y2goL15bYS1mMC05XXs0fS9pKTtlbHNlIGlmIChjaCA9PSBcIlVcIikgc3RyZWFtLm1hdGNoKC9eW2EtZjAtOV17OH0vaSk7ZWxzZSBpZiAoL1swLTddLy50ZXN0KGNoKSkgc3RyZWFtLm1hdGNoKC9eWzAtN117MSwyfS8pO1xuICAgICAgcmV0dXJuIFwic3RyaW5nLnNwZWNpYWxcIjtcbiAgICB9IGVsc2Uge1xuICAgICAgdmFyIG5leHQ7XG4gICAgICB3aGlsZSAoKG5leHQgPSBzdHJlYW0ubmV4dCgpKSAhPSBudWxsKSB7XG4gICAgICAgIGlmIChuZXh0ID09IHF1b3RlKSB7XG4gICAgICAgICAgc3RhdGUudG9rZW5pemUgPSB0b2tlbkJhc2U7XG4gICAgICAgICAgYnJlYWs7XG4gICAgICAgIH1cbiAgICAgICAgaWYgKG5leHQgPT0gXCJcXFxcXCIpIHtcbiAgICAgICAgICBzdHJlYW0uYmFja1VwKDEpO1xuICAgICAgICAgIGJyZWFrO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgICByZXR1cm4gXCJzdHJpbmdcIjtcbiAgICB9XG4gIH07XG59XG52YXIgQUxJR05fWUVTID0gMSxcbiAgQUxJR05fTk8gPSAyLFxuICBCUkFDRUxFU1MgPSA0O1xuZnVuY3Rpb24gcHVzaChzdGF0ZSwgdHlwZSwgc3RyZWFtKSB7XG4gIHN0YXRlLmN0eCA9IHtcbiAgICB0eXBlOiB0eXBlLFxuICAgIGluZGVudDogc3RhdGUuaW5kZW50LFxuICAgIGZsYWdzOiAwLFxuICAgIGNvbHVtbjogc3RyZWFtLmNvbHVtbigpLFxuICAgIHByZXY6IHN0YXRlLmN0eFxuICB9O1xufVxuZnVuY3Rpb24gc2V0RmxhZyhzdGF0ZSwgZmxhZykge1xuICB2YXIgY3R4ID0gc3RhdGUuY3R4O1xuICBzdGF0ZS5jdHggPSB7XG4gICAgdHlwZTogY3R4LnR5cGUsXG4gICAgaW5kZW50OiBjdHguaW5kZW50LFxuICAgIGZsYWdzOiBjdHguZmxhZ3MgfCBmbGFnLFxuICAgIGNvbHVtbjogY3R4LmNvbHVtbixcbiAgICBwcmV2OiBjdHgucHJldlxuICB9O1xufVxuZnVuY3Rpb24gcG9wKHN0YXRlKSB7XG4gIHN0YXRlLmluZGVudCA9IHN0YXRlLmN0eC5pbmRlbnQ7XG4gIHN0YXRlLmN0eCA9IHN0YXRlLmN0eC5wcmV2O1xufVxuZXhwb3J0IGNvbnN0IHIgPSB7XG4gIG5hbWU6IFwiclwiLFxuICBzdGFydFN0YXRlOiBmdW5jdGlvbiAoaW5kZW50VW5pdCkge1xuICAgIHJldHVybiB7XG4gICAgICB0b2tlbml6ZTogdG9rZW5CYXNlLFxuICAgICAgY3R4OiB7XG4gICAgICAgIHR5cGU6IFwidG9wXCIsXG4gICAgICAgIGluZGVudDogLWluZGVudFVuaXQsXG4gICAgICAgIGZsYWdzOiBBTElHTl9OT1xuICAgICAgfSxcbiAgICAgIGluZGVudDogMCxcbiAgICAgIGFmdGVySWRlbnQ6IGZhbHNlXG4gICAgfTtcbiAgfSxcbiAgdG9rZW46IGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgaWYgKHN0cmVhbS5zb2woKSkge1xuICAgICAgaWYgKChzdGF0ZS5jdHguZmxhZ3MgJiAzKSA9PSAwKSBzdGF0ZS5jdHguZmxhZ3MgfD0gQUxJR05fTk87XG4gICAgICBpZiAoc3RhdGUuY3R4LmZsYWdzICYgQlJBQ0VMRVNTKSBwb3Aoc3RhdGUpO1xuICAgICAgc3RhdGUuaW5kZW50ID0gc3RyZWFtLmluZGVudGF0aW9uKCk7XG4gICAgfVxuICAgIGlmIChzdHJlYW0uZWF0U3BhY2UoKSkgcmV0dXJuIG51bGw7XG4gICAgdmFyIHN0eWxlID0gc3RhdGUudG9rZW5pemUoc3RyZWFtLCBzdGF0ZSk7XG4gICAgaWYgKHN0eWxlICE9IFwiY29tbWVudFwiICYmIChzdGF0ZS5jdHguZmxhZ3MgJiBBTElHTl9OTykgPT0gMCkgc2V0RmxhZyhzdGF0ZSwgQUxJR05fWUVTKTtcbiAgICBpZiAoKGN1clB1bmMgPT0gXCI7XCIgfHwgY3VyUHVuYyA9PSBcIntcIiB8fCBjdXJQdW5jID09IFwifVwiKSAmJiBzdGF0ZS5jdHgudHlwZSA9PSBcImJsb2NrXCIpIHBvcChzdGF0ZSk7XG4gICAgaWYgKGN1clB1bmMgPT0gXCJ7XCIpIHB1c2goc3RhdGUsIFwifVwiLCBzdHJlYW0pO2Vsc2UgaWYgKGN1clB1bmMgPT0gXCIoXCIpIHtcbiAgICAgIHB1c2goc3RhdGUsIFwiKVwiLCBzdHJlYW0pO1xuICAgICAgaWYgKHN0YXRlLmFmdGVySWRlbnQpIHN0YXRlLmN0eC5hcmdMaXN0ID0gdHJ1ZTtcbiAgICB9IGVsc2UgaWYgKGN1clB1bmMgPT0gXCJbXCIpIHB1c2goc3RhdGUsIFwiXVwiLCBzdHJlYW0pO2Vsc2UgaWYgKGN1clB1bmMgPT0gXCJibG9ja1wiKSBwdXNoKHN0YXRlLCBcImJsb2NrXCIsIHN0cmVhbSk7ZWxzZSBpZiAoY3VyUHVuYyA9PSBzdGF0ZS5jdHgudHlwZSkgcG9wKHN0YXRlKTtlbHNlIGlmIChzdGF0ZS5jdHgudHlwZSA9PSBcImJsb2NrXCIgJiYgc3R5bGUgIT0gXCJjb21tZW50XCIpIHNldEZsYWcoc3RhdGUsIEJSQUNFTEVTUyk7XG4gICAgc3RhdGUuYWZ0ZXJJZGVudCA9IHN0eWxlID09IFwidmFyaWFibGVcIiB8fCBzdHlsZSA9PSBcImtleXdvcmRcIjtcbiAgICByZXR1cm4gc3R5bGU7XG4gIH0sXG4gIGluZGVudDogZnVuY3Rpb24gKHN0YXRlLCB0ZXh0QWZ0ZXIsIGN4KSB7XG4gICAgaWYgKHN0YXRlLnRva2VuaXplICE9IHRva2VuQmFzZSkgcmV0dXJuIDA7XG4gICAgdmFyIGZpcnN0Q2hhciA9IHRleHRBZnRlciAmJiB0ZXh0QWZ0ZXIuY2hhckF0KDApLFxuICAgICAgY3R4ID0gc3RhdGUuY3R4LFxuICAgICAgY2xvc2luZyA9IGZpcnN0Q2hhciA9PSBjdHgudHlwZTtcbiAgICBpZiAoY3R4LmZsYWdzICYgQlJBQ0VMRVNTKSBjdHggPSBjdHgucHJldjtcbiAgICBpZiAoY3R4LnR5cGUgPT0gXCJibG9ja1wiKSByZXR1cm4gY3R4LmluZGVudCArIChmaXJzdENoYXIgPT0gXCJ7XCIgPyAwIDogY3gudW5pdCk7ZWxzZSBpZiAoY3R4LmZsYWdzICYgQUxJR05fWUVTKSByZXR1cm4gY3R4LmNvbHVtbiArIChjbG9zaW5nID8gMCA6IDEpO2Vsc2UgcmV0dXJuIGN0eC5pbmRlbnQgKyAoY2xvc2luZyA/IDAgOiBjeC51bml0KTtcbiAgfSxcbiAgbGFuZ3VhZ2VEYXRhOiB7XG4gICAgd29yZENoYXJzOiBcIi5cIixcbiAgICBjb21tZW50VG9rZW5zOiB7XG4gICAgICBsaW5lOiBcIiNcIlxuICAgIH0sXG4gICAgYXV0b2NvbXBsZXRlOiBjb21tb25BdG9tcy5jb25jYXQoY29tbW9uQnVpbHRpbnMsIGNvbW1vbktleXdvcmRzKVxuICB9XG59OyJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==