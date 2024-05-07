"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[3841],{

/***/ 83841:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "fcl": () => (/* binding */ fcl)
/* harmony export */ });
var keywords = {
  "term": true,
  "method": true,
  "accu": true,
  "rule": true,
  "then": true,
  "is": true,
  "and": true,
  "or": true,
  "if": true,
  "default": true
};
var start_blocks = {
  "var_input": true,
  "var_output": true,
  "fuzzify": true,
  "defuzzify": true,
  "function_block": true,
  "ruleblock": true
};
var end_blocks = {
  "end_ruleblock": true,
  "end_defuzzify": true,
  "end_function_block": true,
  "end_fuzzify": true,
  "end_var": true
};
var atoms = {
  "true": true,
  "false": true,
  "nan": true,
  "real": true,
  "min": true,
  "max": true,
  "cog": true,
  "cogs": true
};
var isOperatorChar = /[+\-*&^%:=<>!|\/]/;
function tokenBase(stream, state) {
  var ch = stream.next();
  if (/[\d\.]/.test(ch)) {
    if (ch == ".") {
      stream.match(/^[0-9]+([eE][\-+]?[0-9]+)?/);
    } else if (ch == "0") {
      stream.match(/^[xX][0-9a-fA-F]+/) || stream.match(/^0[0-7]+/);
    } else {
      stream.match(/^[0-9]*\.?[0-9]*([eE][\-+]?[0-9]+)?/);
    }
    return "number";
  }
  if (ch == "/" || ch == "(") {
    if (stream.eat("*")) {
      state.tokenize = tokenComment;
      return tokenComment(stream, state);
    }
    if (stream.eat("/")) {
      stream.skipToEnd();
      return "comment";
    }
  }
  if (isOperatorChar.test(ch)) {
    stream.eatWhile(isOperatorChar);
    return "operator";
  }
  stream.eatWhile(/[\w\$_\xa1-\uffff]/);
  var cur = stream.current().toLowerCase();
  if (keywords.propertyIsEnumerable(cur) || start_blocks.propertyIsEnumerable(cur) || end_blocks.propertyIsEnumerable(cur)) {
    return "keyword";
  }
  if (atoms.propertyIsEnumerable(cur)) return "atom";
  return "variable";
}
function tokenComment(stream, state) {
  var maybeEnd = false,
    ch;
  while (ch = stream.next()) {
    if ((ch == "/" || ch == ")") && maybeEnd) {
      state.tokenize = tokenBase;
      break;
    }
    maybeEnd = ch == "*";
  }
  return "comment";
}
function Context(indented, column, type, align, prev) {
  this.indented = indented;
  this.column = column;
  this.type = type;
  this.align = align;
  this.prev = prev;
}
function pushContext(state, col, type) {
  return state.context = new Context(state.indented, col, type, null, state.context);
}
function popContext(state) {
  if (!state.context.prev) return;
  var t = state.context.type;
  if (t == "end_block") state.indented = state.context.indented;
  return state.context = state.context.prev;
}

// Interface

const fcl = {
  name: "fcl",
  startState: function (indentUnit) {
    return {
      tokenize: null,
      context: new Context(-indentUnit, 0, "top", false),
      indented: 0,
      startOfLine: true
    };
  },
  token: function (stream, state) {
    var ctx = state.context;
    if (stream.sol()) {
      if (ctx.align == null) ctx.align = false;
      state.indented = stream.indentation();
      state.startOfLine = true;
    }
    if (stream.eatSpace()) return null;
    var style = (state.tokenize || tokenBase)(stream, state);
    if (style == "comment") return style;
    if (ctx.align == null) ctx.align = true;
    var cur = stream.current().toLowerCase();
    if (start_blocks.propertyIsEnumerable(cur)) pushContext(state, stream.column(), "end_block");else if (end_blocks.propertyIsEnumerable(cur)) popContext(state);
    state.startOfLine = false;
    return style;
  },
  indent: function (state, textAfter, cx) {
    if (state.tokenize != tokenBase && state.tokenize != null) return 0;
    var ctx = state.context;
    var closing = end_blocks.propertyIsEnumerable(textAfter);
    if (ctx.align) return ctx.column + (closing ? 0 : 1);else return ctx.indented + (closing ? 0 : cx.unit);
  },
  languageData: {
    commentTokens: {
      line: "//",
      block: {
        open: "(*",
        close: "*)"
      }
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiMzg0MS5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL0Bjb2RlbWlycm9yL2xlZ2FjeS1tb2Rlcy9tb2RlL2ZjbC5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyJ2YXIga2V5d29yZHMgPSB7XG4gIFwidGVybVwiOiB0cnVlLFxuICBcIm1ldGhvZFwiOiB0cnVlLFxuICBcImFjY3VcIjogdHJ1ZSxcbiAgXCJydWxlXCI6IHRydWUsXG4gIFwidGhlblwiOiB0cnVlLFxuICBcImlzXCI6IHRydWUsXG4gIFwiYW5kXCI6IHRydWUsXG4gIFwib3JcIjogdHJ1ZSxcbiAgXCJpZlwiOiB0cnVlLFxuICBcImRlZmF1bHRcIjogdHJ1ZVxufTtcbnZhciBzdGFydF9ibG9ja3MgPSB7XG4gIFwidmFyX2lucHV0XCI6IHRydWUsXG4gIFwidmFyX291dHB1dFwiOiB0cnVlLFxuICBcImZ1enppZnlcIjogdHJ1ZSxcbiAgXCJkZWZ1enppZnlcIjogdHJ1ZSxcbiAgXCJmdW5jdGlvbl9ibG9ja1wiOiB0cnVlLFxuICBcInJ1bGVibG9ja1wiOiB0cnVlXG59O1xudmFyIGVuZF9ibG9ja3MgPSB7XG4gIFwiZW5kX3J1bGVibG9ja1wiOiB0cnVlLFxuICBcImVuZF9kZWZ1enppZnlcIjogdHJ1ZSxcbiAgXCJlbmRfZnVuY3Rpb25fYmxvY2tcIjogdHJ1ZSxcbiAgXCJlbmRfZnV6emlmeVwiOiB0cnVlLFxuICBcImVuZF92YXJcIjogdHJ1ZVxufTtcbnZhciBhdG9tcyA9IHtcbiAgXCJ0cnVlXCI6IHRydWUsXG4gIFwiZmFsc2VcIjogdHJ1ZSxcbiAgXCJuYW5cIjogdHJ1ZSxcbiAgXCJyZWFsXCI6IHRydWUsXG4gIFwibWluXCI6IHRydWUsXG4gIFwibWF4XCI6IHRydWUsXG4gIFwiY29nXCI6IHRydWUsXG4gIFwiY29nc1wiOiB0cnVlXG59O1xudmFyIGlzT3BlcmF0b3JDaGFyID0gL1srXFwtKiZeJTo9PD4hfFxcL10vO1xuZnVuY3Rpb24gdG9rZW5CYXNlKHN0cmVhbSwgc3RhdGUpIHtcbiAgdmFyIGNoID0gc3RyZWFtLm5leHQoKTtcbiAgaWYgKC9bXFxkXFwuXS8udGVzdChjaCkpIHtcbiAgICBpZiAoY2ggPT0gXCIuXCIpIHtcbiAgICAgIHN0cmVhbS5tYXRjaCgvXlswLTldKyhbZUVdW1xcLStdP1swLTldKyk/Lyk7XG4gICAgfSBlbHNlIGlmIChjaCA9PSBcIjBcIikge1xuICAgICAgc3RyZWFtLm1hdGNoKC9eW3hYXVswLTlhLWZBLUZdKy8pIHx8IHN0cmVhbS5tYXRjaCgvXjBbMC03XSsvKTtcbiAgICB9IGVsc2Uge1xuICAgICAgc3RyZWFtLm1hdGNoKC9eWzAtOV0qXFwuP1swLTldKihbZUVdW1xcLStdP1swLTldKyk/Lyk7XG4gICAgfVxuICAgIHJldHVybiBcIm51bWJlclwiO1xuICB9XG4gIGlmIChjaCA9PSBcIi9cIiB8fCBjaCA9PSBcIihcIikge1xuICAgIGlmIChzdHJlYW0uZWF0KFwiKlwiKSkge1xuICAgICAgc3RhdGUudG9rZW5pemUgPSB0b2tlbkNvbW1lbnQ7XG4gICAgICByZXR1cm4gdG9rZW5Db21tZW50KHN0cmVhbSwgc3RhdGUpO1xuICAgIH1cbiAgICBpZiAoc3RyZWFtLmVhdChcIi9cIikpIHtcbiAgICAgIHN0cmVhbS5za2lwVG9FbmQoKTtcbiAgICAgIHJldHVybiBcImNvbW1lbnRcIjtcbiAgICB9XG4gIH1cbiAgaWYgKGlzT3BlcmF0b3JDaGFyLnRlc3QoY2gpKSB7XG4gICAgc3RyZWFtLmVhdFdoaWxlKGlzT3BlcmF0b3JDaGFyKTtcbiAgICByZXR1cm4gXCJvcGVyYXRvclwiO1xuICB9XG4gIHN0cmVhbS5lYXRXaGlsZSgvW1xcd1xcJF9cXHhhMS1cXHVmZmZmXS8pO1xuICB2YXIgY3VyID0gc3RyZWFtLmN1cnJlbnQoKS50b0xvd2VyQ2FzZSgpO1xuICBpZiAoa2V5d29yZHMucHJvcGVydHlJc0VudW1lcmFibGUoY3VyKSB8fCBzdGFydF9ibG9ja3MucHJvcGVydHlJc0VudW1lcmFibGUoY3VyKSB8fCBlbmRfYmxvY2tzLnByb3BlcnR5SXNFbnVtZXJhYmxlKGN1cikpIHtcbiAgICByZXR1cm4gXCJrZXl3b3JkXCI7XG4gIH1cbiAgaWYgKGF0b21zLnByb3BlcnR5SXNFbnVtZXJhYmxlKGN1cikpIHJldHVybiBcImF0b21cIjtcbiAgcmV0dXJuIFwidmFyaWFibGVcIjtcbn1cbmZ1bmN0aW9uIHRva2VuQ29tbWVudChzdHJlYW0sIHN0YXRlKSB7XG4gIHZhciBtYXliZUVuZCA9IGZhbHNlLFxuICAgIGNoO1xuICB3aGlsZSAoY2ggPSBzdHJlYW0ubmV4dCgpKSB7XG4gICAgaWYgKChjaCA9PSBcIi9cIiB8fCBjaCA9PSBcIilcIikgJiYgbWF5YmVFbmQpIHtcbiAgICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlO1xuICAgICAgYnJlYWs7XG4gICAgfVxuICAgIG1heWJlRW5kID0gY2ggPT0gXCIqXCI7XG4gIH1cbiAgcmV0dXJuIFwiY29tbWVudFwiO1xufVxuZnVuY3Rpb24gQ29udGV4dChpbmRlbnRlZCwgY29sdW1uLCB0eXBlLCBhbGlnbiwgcHJldikge1xuICB0aGlzLmluZGVudGVkID0gaW5kZW50ZWQ7XG4gIHRoaXMuY29sdW1uID0gY29sdW1uO1xuICB0aGlzLnR5cGUgPSB0eXBlO1xuICB0aGlzLmFsaWduID0gYWxpZ247XG4gIHRoaXMucHJldiA9IHByZXY7XG59XG5mdW5jdGlvbiBwdXNoQ29udGV4dChzdGF0ZSwgY29sLCB0eXBlKSB7XG4gIHJldHVybiBzdGF0ZS5jb250ZXh0ID0gbmV3IENvbnRleHQoc3RhdGUuaW5kZW50ZWQsIGNvbCwgdHlwZSwgbnVsbCwgc3RhdGUuY29udGV4dCk7XG59XG5mdW5jdGlvbiBwb3BDb250ZXh0KHN0YXRlKSB7XG4gIGlmICghc3RhdGUuY29udGV4dC5wcmV2KSByZXR1cm47XG4gIHZhciB0ID0gc3RhdGUuY29udGV4dC50eXBlO1xuICBpZiAodCA9PSBcImVuZF9ibG9ja1wiKSBzdGF0ZS5pbmRlbnRlZCA9IHN0YXRlLmNvbnRleHQuaW5kZW50ZWQ7XG4gIHJldHVybiBzdGF0ZS5jb250ZXh0ID0gc3RhdGUuY29udGV4dC5wcmV2O1xufVxuXG4vLyBJbnRlcmZhY2VcblxuZXhwb3J0IGNvbnN0IGZjbCA9IHtcbiAgbmFtZTogXCJmY2xcIixcbiAgc3RhcnRTdGF0ZTogZnVuY3Rpb24gKGluZGVudFVuaXQpIHtcbiAgICByZXR1cm4ge1xuICAgICAgdG9rZW5pemU6IG51bGwsXG4gICAgICBjb250ZXh0OiBuZXcgQ29udGV4dCgtaW5kZW50VW5pdCwgMCwgXCJ0b3BcIiwgZmFsc2UpLFxuICAgICAgaW5kZW50ZWQ6IDAsXG4gICAgICBzdGFydE9mTGluZTogdHJ1ZVxuICAgIH07XG4gIH0sXG4gIHRva2VuOiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIHZhciBjdHggPSBzdGF0ZS5jb250ZXh0O1xuICAgIGlmIChzdHJlYW0uc29sKCkpIHtcbiAgICAgIGlmIChjdHguYWxpZ24gPT0gbnVsbCkgY3R4LmFsaWduID0gZmFsc2U7XG4gICAgICBzdGF0ZS5pbmRlbnRlZCA9IHN0cmVhbS5pbmRlbnRhdGlvbigpO1xuICAgICAgc3RhdGUuc3RhcnRPZkxpbmUgPSB0cnVlO1xuICAgIH1cbiAgICBpZiAoc3RyZWFtLmVhdFNwYWNlKCkpIHJldHVybiBudWxsO1xuICAgIHZhciBzdHlsZSA9IChzdGF0ZS50b2tlbml6ZSB8fCB0b2tlbkJhc2UpKHN0cmVhbSwgc3RhdGUpO1xuICAgIGlmIChzdHlsZSA9PSBcImNvbW1lbnRcIikgcmV0dXJuIHN0eWxlO1xuICAgIGlmIChjdHguYWxpZ24gPT0gbnVsbCkgY3R4LmFsaWduID0gdHJ1ZTtcbiAgICB2YXIgY3VyID0gc3RyZWFtLmN1cnJlbnQoKS50b0xvd2VyQ2FzZSgpO1xuICAgIGlmIChzdGFydF9ibG9ja3MucHJvcGVydHlJc0VudW1lcmFibGUoY3VyKSkgcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbS5jb2x1bW4oKSwgXCJlbmRfYmxvY2tcIik7ZWxzZSBpZiAoZW5kX2Jsb2Nrcy5wcm9wZXJ0eUlzRW51bWVyYWJsZShjdXIpKSBwb3BDb250ZXh0KHN0YXRlKTtcbiAgICBzdGF0ZS5zdGFydE9mTGluZSA9IGZhbHNlO1xuICAgIHJldHVybiBzdHlsZTtcbiAgfSxcbiAgaW5kZW50OiBmdW5jdGlvbiAoc3RhdGUsIHRleHRBZnRlciwgY3gpIHtcbiAgICBpZiAoc3RhdGUudG9rZW5pemUgIT0gdG9rZW5CYXNlICYmIHN0YXRlLnRva2VuaXplICE9IG51bGwpIHJldHVybiAwO1xuICAgIHZhciBjdHggPSBzdGF0ZS5jb250ZXh0O1xuICAgIHZhciBjbG9zaW5nID0gZW5kX2Jsb2Nrcy5wcm9wZXJ0eUlzRW51bWVyYWJsZSh0ZXh0QWZ0ZXIpO1xuICAgIGlmIChjdHguYWxpZ24pIHJldHVybiBjdHguY29sdW1uICsgKGNsb3NpbmcgPyAwIDogMSk7ZWxzZSByZXR1cm4gY3R4LmluZGVudGVkICsgKGNsb3NpbmcgPyAwIDogY3gudW5pdCk7XG4gIH0sXG4gIGxhbmd1YWdlRGF0YToge1xuICAgIGNvbW1lbnRUb2tlbnM6IHtcbiAgICAgIGxpbmU6IFwiLy9cIixcbiAgICAgIGJsb2NrOiB7XG4gICAgICAgIG9wZW46IFwiKCpcIixcbiAgICAgICAgY2xvc2U6IFwiKilcIlxuICAgICAgfVxuICAgIH1cbiAgfVxufTsiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=