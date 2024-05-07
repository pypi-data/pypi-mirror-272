"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[6951],{

/***/ 46951:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "jinja2": () => (/* binding */ jinja2)
/* harmony export */ });
var keywords = ["and", "as", "block", "endblock", "by", "cycle", "debug", "else", "elif", "extends", "filter", "endfilter", "firstof", "do", "for", "endfor", "if", "endif", "ifchanged", "endifchanged", "ifequal", "endifequal", "ifnotequal", "set", "raw", "endraw", "endifnotequal", "in", "include", "load", "not", "now", "or", "parsed", "regroup", "reversed", "spaceless", "call", "endcall", "macro", "endmacro", "endspaceless", "ssi", "templatetag", "openblock", "closeblock", "openvariable", "closevariable", "without", "context", "openbrace", "closebrace", "opencomment", "closecomment", "widthratio", "url", "with", "endwith", "get_current_language", "trans", "endtrans", "noop", "blocktrans", "endblocktrans", "get_available_languages", "get_current_language_bidi", "pluralize", "autoescape", "endautoescape"],
  operator = /^[+\-*&%=<>!?|~^]/,
  sign = /^[:\[\(\{]/,
  atom = ["true", "false"],
  number = /^(\d[+\-\*\/])?\d+(\.\d+)?/;
keywords = new RegExp("((" + keywords.join(")|(") + "))\\b");
atom = new RegExp("((" + atom.join(")|(") + "))\\b");
function tokenBase(stream, state) {
  var ch = stream.peek();

  //Comment
  if (state.incomment) {
    if (!stream.skipTo("#}")) {
      stream.skipToEnd();
    } else {
      stream.eatWhile(/\#|}/);
      state.incomment = false;
    }
    return "comment";
    //Tag
  } else if (state.intag) {
    //After operator
    if (state.operator) {
      state.operator = false;
      if (stream.match(atom)) {
        return "atom";
      }
      if (stream.match(number)) {
        return "number";
      }
    }
    //After sign
    if (state.sign) {
      state.sign = false;
      if (stream.match(atom)) {
        return "atom";
      }
      if (stream.match(number)) {
        return "number";
      }
    }
    if (state.instring) {
      if (ch == state.instring) {
        state.instring = false;
      }
      stream.next();
      return "string";
    } else if (ch == "'" || ch == '"') {
      state.instring = ch;
      stream.next();
      return "string";
    } else if (state.inbraces > 0 && ch == ")") {
      stream.next();
      state.inbraces--;
    } else if (ch == "(") {
      stream.next();
      state.inbraces++;
    } else if (state.inbrackets > 0 && ch == "]") {
      stream.next();
      state.inbrackets--;
    } else if (ch == "[") {
      stream.next();
      state.inbrackets++;
    } else if (!state.lineTag && (stream.match(state.intag + "}") || stream.eat("-") && stream.match(state.intag + "}"))) {
      state.intag = false;
      return "tag";
    } else if (stream.match(operator)) {
      state.operator = true;
      return "operator";
    } else if (stream.match(sign)) {
      state.sign = true;
    } else {
      if (stream.column() == 1 && state.lineTag && stream.match(keywords)) {
        //allow nospace after tag before the keyword
        return "keyword";
      }
      if (stream.eat(" ") || stream.sol()) {
        if (stream.match(keywords)) {
          return "keyword";
        }
        if (stream.match(atom)) {
          return "atom";
        }
        if (stream.match(number)) {
          return "number";
        }
        if (stream.sol()) {
          stream.next();
        }
      } else {
        stream.next();
      }
    }
    return "variable";
  } else if (stream.eat("{")) {
    if (stream.eat("#")) {
      state.incomment = true;
      if (!stream.skipTo("#}")) {
        stream.skipToEnd();
      } else {
        stream.eatWhile(/\#|}/);
        state.incomment = false;
      }
      return "comment";
      //Open tag
    } else if (ch = stream.eat(/\{|%/)) {
      //Cache close tag
      state.intag = ch;
      state.inbraces = 0;
      state.inbrackets = 0;
      if (ch == "{") {
        state.intag = "}";
      }
      stream.eat("-");
      return "tag";
    }
    //Line statements
  } else if (stream.eat('#')) {
    if (stream.peek() == '#') {
      stream.skipToEnd();
      return "comment";
    } else if (!stream.eol()) {
      state.intag = true;
      state.lineTag = true;
      state.inbraces = 0;
      state.inbrackets = 0;
      return "tag";
    }
  }
  stream.next();
}
;
const jinja2 = {
  name: "jinja2",
  startState: function () {
    return {
      tokenize: tokenBase,
      inbrackets: 0,
      inbraces: 0
    };
  },
  token: function (stream, state) {
    var style = state.tokenize(stream, state);
    if (stream.eol() && state.lineTag && !state.instring && state.inbraces == 0 && state.inbrackets == 0) {
      //Close line statement at the EOL
      state.intag = false;
      state.lineTag = false;
    }
    return style;
  },
  languageData: {
    commentTokens: {
      block: {
        open: "{#",
        close: "#}",
        line: "##"
      }
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNjk1MS5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL0Bjb2RlbWlycm9yL2xlZ2FjeS1tb2Rlcy9tb2RlL2ppbmphMi5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyJ2YXIga2V5d29yZHMgPSBbXCJhbmRcIiwgXCJhc1wiLCBcImJsb2NrXCIsIFwiZW5kYmxvY2tcIiwgXCJieVwiLCBcImN5Y2xlXCIsIFwiZGVidWdcIiwgXCJlbHNlXCIsIFwiZWxpZlwiLCBcImV4dGVuZHNcIiwgXCJmaWx0ZXJcIiwgXCJlbmRmaWx0ZXJcIiwgXCJmaXJzdG9mXCIsIFwiZG9cIiwgXCJmb3JcIiwgXCJlbmRmb3JcIiwgXCJpZlwiLCBcImVuZGlmXCIsIFwiaWZjaGFuZ2VkXCIsIFwiZW5kaWZjaGFuZ2VkXCIsIFwiaWZlcXVhbFwiLCBcImVuZGlmZXF1YWxcIiwgXCJpZm5vdGVxdWFsXCIsIFwic2V0XCIsIFwicmF3XCIsIFwiZW5kcmF3XCIsIFwiZW5kaWZub3RlcXVhbFwiLCBcImluXCIsIFwiaW5jbHVkZVwiLCBcImxvYWRcIiwgXCJub3RcIiwgXCJub3dcIiwgXCJvclwiLCBcInBhcnNlZFwiLCBcInJlZ3JvdXBcIiwgXCJyZXZlcnNlZFwiLCBcInNwYWNlbGVzc1wiLCBcImNhbGxcIiwgXCJlbmRjYWxsXCIsIFwibWFjcm9cIiwgXCJlbmRtYWNyb1wiLCBcImVuZHNwYWNlbGVzc1wiLCBcInNzaVwiLCBcInRlbXBsYXRldGFnXCIsIFwib3BlbmJsb2NrXCIsIFwiY2xvc2VibG9ja1wiLCBcIm9wZW52YXJpYWJsZVwiLCBcImNsb3NldmFyaWFibGVcIiwgXCJ3aXRob3V0XCIsIFwiY29udGV4dFwiLCBcIm9wZW5icmFjZVwiLCBcImNsb3NlYnJhY2VcIiwgXCJvcGVuY29tbWVudFwiLCBcImNsb3NlY29tbWVudFwiLCBcIndpZHRocmF0aW9cIiwgXCJ1cmxcIiwgXCJ3aXRoXCIsIFwiZW5kd2l0aFwiLCBcImdldF9jdXJyZW50X2xhbmd1YWdlXCIsIFwidHJhbnNcIiwgXCJlbmR0cmFuc1wiLCBcIm5vb3BcIiwgXCJibG9ja3RyYW5zXCIsIFwiZW5kYmxvY2t0cmFuc1wiLCBcImdldF9hdmFpbGFibGVfbGFuZ3VhZ2VzXCIsIFwiZ2V0X2N1cnJlbnRfbGFuZ3VhZ2VfYmlkaVwiLCBcInBsdXJhbGl6ZVwiLCBcImF1dG9lc2NhcGVcIiwgXCJlbmRhdXRvZXNjYXBlXCJdLFxuICBvcGVyYXRvciA9IC9eWytcXC0qJiU9PD4hP3x+Xl0vLFxuICBzaWduID0gL15bOlxcW1xcKFxce10vLFxuICBhdG9tID0gW1widHJ1ZVwiLCBcImZhbHNlXCJdLFxuICBudW1iZXIgPSAvXihcXGRbK1xcLVxcKlxcL10pP1xcZCsoXFwuXFxkKyk/LztcbmtleXdvcmRzID0gbmV3IFJlZ0V4cChcIigoXCIgKyBrZXl3b3Jkcy5qb2luKFwiKXwoXCIpICsgXCIpKVxcXFxiXCIpO1xuYXRvbSA9IG5ldyBSZWdFeHAoXCIoKFwiICsgYXRvbS5qb2luKFwiKXwoXCIpICsgXCIpKVxcXFxiXCIpO1xuZnVuY3Rpb24gdG9rZW5CYXNlKHN0cmVhbSwgc3RhdGUpIHtcbiAgdmFyIGNoID0gc3RyZWFtLnBlZWsoKTtcblxuICAvL0NvbW1lbnRcbiAgaWYgKHN0YXRlLmluY29tbWVudCkge1xuICAgIGlmICghc3RyZWFtLnNraXBUbyhcIiN9XCIpKSB7XG4gICAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgfSBlbHNlIHtcbiAgICAgIHN0cmVhbS5lYXRXaGlsZSgvXFwjfH0vKTtcbiAgICAgIHN0YXRlLmluY29tbWVudCA9IGZhbHNlO1xuICAgIH1cbiAgICByZXR1cm4gXCJjb21tZW50XCI7XG4gICAgLy9UYWdcbiAgfSBlbHNlIGlmIChzdGF0ZS5pbnRhZykge1xuICAgIC8vQWZ0ZXIgb3BlcmF0b3JcbiAgICBpZiAoc3RhdGUub3BlcmF0b3IpIHtcbiAgICAgIHN0YXRlLm9wZXJhdG9yID0gZmFsc2U7XG4gICAgICBpZiAoc3RyZWFtLm1hdGNoKGF0b20pKSB7XG4gICAgICAgIHJldHVybiBcImF0b21cIjtcbiAgICAgIH1cbiAgICAgIGlmIChzdHJlYW0ubWF0Y2gobnVtYmVyKSkge1xuICAgICAgICByZXR1cm4gXCJudW1iZXJcIjtcbiAgICAgIH1cbiAgICB9XG4gICAgLy9BZnRlciBzaWduXG4gICAgaWYgKHN0YXRlLnNpZ24pIHtcbiAgICAgIHN0YXRlLnNpZ24gPSBmYWxzZTtcbiAgICAgIGlmIChzdHJlYW0ubWF0Y2goYXRvbSkpIHtcbiAgICAgICAgcmV0dXJuIFwiYXRvbVwiO1xuICAgICAgfVxuICAgICAgaWYgKHN0cmVhbS5tYXRjaChudW1iZXIpKSB7XG4gICAgICAgIHJldHVybiBcIm51bWJlclwiO1xuICAgICAgfVxuICAgIH1cbiAgICBpZiAoc3RhdGUuaW5zdHJpbmcpIHtcbiAgICAgIGlmIChjaCA9PSBzdGF0ZS5pbnN0cmluZykge1xuICAgICAgICBzdGF0ZS5pbnN0cmluZyA9IGZhbHNlO1xuICAgICAgfVxuICAgICAgc3RyZWFtLm5leHQoKTtcbiAgICAgIHJldHVybiBcInN0cmluZ1wiO1xuICAgIH0gZWxzZSBpZiAoY2ggPT0gXCInXCIgfHwgY2ggPT0gJ1wiJykge1xuICAgICAgc3RhdGUuaW5zdHJpbmcgPSBjaDtcbiAgICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgICByZXR1cm4gXCJzdHJpbmdcIjtcbiAgICB9IGVsc2UgaWYgKHN0YXRlLmluYnJhY2VzID4gMCAmJiBjaCA9PSBcIilcIikge1xuICAgICAgc3RyZWFtLm5leHQoKTtcbiAgICAgIHN0YXRlLmluYnJhY2VzLS07XG4gICAgfSBlbHNlIGlmIChjaCA9PSBcIihcIikge1xuICAgICAgc3RyZWFtLm5leHQoKTtcbiAgICAgIHN0YXRlLmluYnJhY2VzKys7XG4gICAgfSBlbHNlIGlmIChzdGF0ZS5pbmJyYWNrZXRzID4gMCAmJiBjaCA9PSBcIl1cIikge1xuICAgICAgc3RyZWFtLm5leHQoKTtcbiAgICAgIHN0YXRlLmluYnJhY2tldHMtLTtcbiAgICB9IGVsc2UgaWYgKGNoID09IFwiW1wiKSB7XG4gICAgICBzdHJlYW0ubmV4dCgpO1xuICAgICAgc3RhdGUuaW5icmFja2V0cysrO1xuICAgIH0gZWxzZSBpZiAoIXN0YXRlLmxpbmVUYWcgJiYgKHN0cmVhbS5tYXRjaChzdGF0ZS5pbnRhZyArIFwifVwiKSB8fCBzdHJlYW0uZWF0KFwiLVwiKSAmJiBzdHJlYW0ubWF0Y2goc3RhdGUuaW50YWcgKyBcIn1cIikpKSB7XG4gICAgICBzdGF0ZS5pbnRhZyA9IGZhbHNlO1xuICAgICAgcmV0dXJuIFwidGFnXCI7XG4gICAgfSBlbHNlIGlmIChzdHJlYW0ubWF0Y2gob3BlcmF0b3IpKSB7XG4gICAgICBzdGF0ZS5vcGVyYXRvciA9IHRydWU7XG4gICAgICByZXR1cm4gXCJvcGVyYXRvclwiO1xuICAgIH0gZWxzZSBpZiAoc3RyZWFtLm1hdGNoKHNpZ24pKSB7XG4gICAgICBzdGF0ZS5zaWduID0gdHJ1ZTtcbiAgICB9IGVsc2Uge1xuICAgICAgaWYgKHN0cmVhbS5jb2x1bW4oKSA9PSAxICYmIHN0YXRlLmxpbmVUYWcgJiYgc3RyZWFtLm1hdGNoKGtleXdvcmRzKSkge1xuICAgICAgICAvL2FsbG93IG5vc3BhY2UgYWZ0ZXIgdGFnIGJlZm9yZSB0aGUga2V5d29yZFxuICAgICAgICByZXR1cm4gXCJrZXl3b3JkXCI7XG4gICAgICB9XG4gICAgICBpZiAoc3RyZWFtLmVhdChcIiBcIikgfHwgc3RyZWFtLnNvbCgpKSB7XG4gICAgICAgIGlmIChzdHJlYW0ubWF0Y2goa2V5d29yZHMpKSB7XG4gICAgICAgICAgcmV0dXJuIFwia2V5d29yZFwiO1xuICAgICAgICB9XG4gICAgICAgIGlmIChzdHJlYW0ubWF0Y2goYXRvbSkpIHtcbiAgICAgICAgICByZXR1cm4gXCJhdG9tXCI7XG4gICAgICAgIH1cbiAgICAgICAgaWYgKHN0cmVhbS5tYXRjaChudW1iZXIpKSB7XG4gICAgICAgICAgcmV0dXJuIFwibnVtYmVyXCI7XG4gICAgICAgIH1cbiAgICAgICAgaWYgKHN0cmVhbS5zb2woKSkge1xuICAgICAgICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgICAgIH1cbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgICB9XG4gICAgfVxuICAgIHJldHVybiBcInZhcmlhYmxlXCI7XG4gIH0gZWxzZSBpZiAoc3RyZWFtLmVhdChcIntcIikpIHtcbiAgICBpZiAoc3RyZWFtLmVhdChcIiNcIikpIHtcbiAgICAgIHN0YXRlLmluY29tbWVudCA9IHRydWU7XG4gICAgICBpZiAoIXN0cmVhbS5za2lwVG8oXCIjfVwiKSkge1xuICAgICAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBzdHJlYW0uZWF0V2hpbGUoL1xcI3x9Lyk7XG4gICAgICAgIHN0YXRlLmluY29tbWVudCA9IGZhbHNlO1xuICAgICAgfVxuICAgICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICAgICAgLy9PcGVuIHRhZ1xuICAgIH0gZWxzZSBpZiAoY2ggPSBzdHJlYW0uZWF0KC9cXHt8JS8pKSB7XG4gICAgICAvL0NhY2hlIGNsb3NlIHRhZ1xuICAgICAgc3RhdGUuaW50YWcgPSBjaDtcbiAgICAgIHN0YXRlLmluYnJhY2VzID0gMDtcbiAgICAgIHN0YXRlLmluYnJhY2tldHMgPSAwO1xuICAgICAgaWYgKGNoID09IFwie1wiKSB7XG4gICAgICAgIHN0YXRlLmludGFnID0gXCJ9XCI7XG4gICAgICB9XG4gICAgICBzdHJlYW0uZWF0KFwiLVwiKTtcbiAgICAgIHJldHVybiBcInRhZ1wiO1xuICAgIH1cbiAgICAvL0xpbmUgc3RhdGVtZW50c1xuICB9IGVsc2UgaWYgKHN0cmVhbS5lYXQoJyMnKSkge1xuICAgIGlmIChzdHJlYW0ucGVlaygpID09ICcjJykge1xuICAgICAgc3RyZWFtLnNraXBUb0VuZCgpO1xuICAgICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICAgIH0gZWxzZSBpZiAoIXN0cmVhbS5lb2woKSkge1xuICAgICAgc3RhdGUuaW50YWcgPSB0cnVlO1xuICAgICAgc3RhdGUubGluZVRhZyA9IHRydWU7XG4gICAgICBzdGF0ZS5pbmJyYWNlcyA9IDA7XG4gICAgICBzdGF0ZS5pbmJyYWNrZXRzID0gMDtcbiAgICAgIHJldHVybiBcInRhZ1wiO1xuICAgIH1cbiAgfVxuICBzdHJlYW0ubmV4dCgpO1xufVxuO1xuZXhwb3J0IGNvbnN0IGppbmphMiA9IHtcbiAgbmFtZTogXCJqaW5qYTJcIixcbiAgc3RhcnRTdGF0ZTogZnVuY3Rpb24gKCkge1xuICAgIHJldHVybiB7XG4gICAgICB0b2tlbml6ZTogdG9rZW5CYXNlLFxuICAgICAgaW5icmFja2V0czogMCxcbiAgICAgIGluYnJhY2VzOiAwXG4gICAgfTtcbiAgfSxcbiAgdG9rZW46IGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgdmFyIHN0eWxlID0gc3RhdGUudG9rZW5pemUoc3RyZWFtLCBzdGF0ZSk7XG4gICAgaWYgKHN0cmVhbS5lb2woKSAmJiBzdGF0ZS5saW5lVGFnICYmICFzdGF0ZS5pbnN0cmluZyAmJiBzdGF0ZS5pbmJyYWNlcyA9PSAwICYmIHN0YXRlLmluYnJhY2tldHMgPT0gMCkge1xuICAgICAgLy9DbG9zZSBsaW5lIHN0YXRlbWVudCBhdCB0aGUgRU9MXG4gICAgICBzdGF0ZS5pbnRhZyA9IGZhbHNlO1xuICAgICAgc3RhdGUubGluZVRhZyA9IGZhbHNlO1xuICAgIH1cbiAgICByZXR1cm4gc3R5bGU7XG4gIH0sXG4gIGxhbmd1YWdlRGF0YToge1xuICAgIGNvbW1lbnRUb2tlbnM6IHtcbiAgICAgIGJsb2NrOiB7XG4gICAgICAgIG9wZW46IFwieyNcIixcbiAgICAgICAgY2xvc2U6IFwiI31cIixcbiAgICAgICAgbGluZTogXCIjI1wiXG4gICAgICB9XG4gICAgfVxuICB9XG59OyJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==