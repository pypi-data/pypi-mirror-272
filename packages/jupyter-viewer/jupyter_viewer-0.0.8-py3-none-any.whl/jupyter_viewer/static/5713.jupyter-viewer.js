"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[5713],{

/***/ 35713:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "q": () => (/* binding */ q)
/* harmony export */ });
var curPunc,
  keywords = buildRE(["abs", "acos", "aj", "aj0", "all", "and", "any", "asc", "asin", "asof", "atan", "attr", "avg", "avgs", "bin", "by", "ceiling", "cols", "cor", "cos", "count", "cov", "cross", "csv", "cut", "delete", "deltas", "desc", "dev", "differ", "distinct", "div", "do", "each", "ej", "enlist", "eval", "except", "exec", "exit", "exp", "fby", "fills", "first", "fkeys", "flip", "floor", "from", "get", "getenv", "group", "gtime", "hclose", "hcount", "hdel", "hopen", "hsym", "iasc", "idesc", "if", "ij", "in", "insert", "inter", "inv", "key", "keys", "last", "like", "list", "lj", "load", "log", "lower", "lsq", "ltime", "ltrim", "mavg", "max", "maxs", "mcount", "md5", "mdev", "med", "meta", "min", "mins", "mmax", "mmin", "mmu", "mod", "msum", "neg", "next", "not", "null", "or", "over", "parse", "peach", "pj", "plist", "prd", "prds", "prev", "prior", "rand", "rank", "ratios", "raze", "read0", "read1", "reciprocal", "reverse", "rload", "rotate", "rsave", "rtrim", "save", "scan", "select", "set", "setenv", "show", "signum", "sin", "sqrt", "ss", "ssr", "string", "sublist", "sum", "sums", "sv", "system", "tables", "tan", "til", "trim", "txf", "type", "uj", "ungroup", "union", "update", "upper", "upsert", "value", "var", "view", "views", "vs", "wavg", "where", "where", "while", "within", "wj", "wj1", "wsum", "xasc", "xbar", "xcol", "xcols", "xdesc", "xexp", "xgroup", "xkey", "xlog", "xprev", "xrank"]),
  E = /[|/&^!+:\\\-*%$=~#;@><,?_\'\"\[\(\]\)\s{}]/;
function buildRE(w) {
  return new RegExp("^(" + w.join("|") + ")$");
}
function tokenBase(stream, state) {
  var sol = stream.sol(),
    c = stream.next();
  curPunc = null;
  if (sol) if (c == "/") return (state.tokenize = tokenLineComment)(stream, state);else if (c == "\\") {
    if (stream.eol() || /\s/.test(stream.peek())) return stream.skipToEnd(), /^\\\s*$/.test(stream.current()) ? (state.tokenize = tokenCommentToEOF)(stream) : state.tokenize = tokenBase, "comment";else return state.tokenize = tokenBase, "builtin";
  }
  if (/\s/.test(c)) return stream.peek() == "/" ? (stream.skipToEnd(), "comment") : "null";
  if (c == '"') return (state.tokenize = tokenString)(stream, state);
  if (c == '`') return stream.eatWhile(/[A-Za-z\d_:\/.]/), "macroName";
  if ("." == c && /\d/.test(stream.peek()) || /\d/.test(c)) {
    var t = null;
    stream.backUp(1);
    if (stream.match(/^\d{4}\.\d{2}(m|\.\d{2}([DT](\d{2}(:\d{2}(:\d{2}(\.\d{1,9})?)?)?)?)?)/) || stream.match(/^\d+D(\d{2}(:\d{2}(:\d{2}(\.\d{1,9})?)?)?)/) || stream.match(/^\d{2}:\d{2}(:\d{2}(\.\d{1,9})?)?/) || stream.match(/^\d+[ptuv]{1}/)) t = "temporal";else if (stream.match(/^0[NwW]{1}/) || stream.match(/^0x[\da-fA-F]*/) || stream.match(/^[01]+[b]{1}/) || stream.match(/^\d+[chijn]{1}/) || stream.match(/-?\d*(\.\d*)?(e[+\-]?\d+)?(e|f)?/)) t = "number";
    return t && (!(c = stream.peek()) || E.test(c)) ? t : (stream.next(), "error");
  }
  if (/[A-Za-z]|\./.test(c)) return stream.eatWhile(/[A-Za-z._\d]/), keywords.test(stream.current()) ? "keyword" : "variable";
  if (/[|/&^!+:\\\-*%$=~#;@><\.,?_\']/.test(c)) return null;
  if (/[{}\(\[\]\)]/.test(c)) return null;
  return "error";
}
function tokenLineComment(stream, state) {
  return stream.skipToEnd(), /\/\s*$/.test(stream.current()) ? (state.tokenize = tokenBlockComment)(stream, state) : state.tokenize = tokenBase, "comment";
}
function tokenBlockComment(stream, state) {
  var f = stream.sol() && stream.peek() == "\\";
  stream.skipToEnd();
  if (f && /^\\\s*$/.test(stream.current())) state.tokenize = tokenBase;
  return "comment";
}
function tokenCommentToEOF(stream) {
  return stream.skipToEnd(), "comment";
}
function tokenString(stream, state) {
  var escaped = false,
    next,
    end = false;
  while (next = stream.next()) {
    if (next == "\"" && !escaped) {
      end = true;
      break;
    }
    escaped = !escaped && next == "\\";
  }
  if (end) state.tokenize = tokenBase;
  return "string";
}
function pushContext(state, type, col) {
  state.context = {
    prev: state.context,
    indent: state.indent,
    col: col,
    type: type
  };
}
function popContext(state) {
  state.indent = state.context.indent;
  state.context = state.context.prev;
}
const q = {
  name: "q",
  startState: function () {
    return {
      tokenize: tokenBase,
      context: null,
      indent: 0,
      col: 0
    };
  },
  token: function (stream, state) {
    if (stream.sol()) {
      if (state.context && state.context.align == null) state.context.align = false;
      state.indent = stream.indentation();
    }
    //if (stream.eatSpace()) return null;
    var style = state.tokenize(stream, state);
    if (style != "comment" && state.context && state.context.align == null && state.context.type != "pattern") {
      state.context.align = true;
    }
    if (curPunc == "(") pushContext(state, ")", stream.column());else if (curPunc == "[") pushContext(state, "]", stream.column());else if (curPunc == "{") pushContext(state, "}", stream.column());else if (/[\]\}\)]/.test(curPunc)) {
      while (state.context && state.context.type == "pattern") popContext(state);
      if (state.context && curPunc == state.context.type) popContext(state);
    } else if (curPunc == "." && state.context && state.context.type == "pattern") popContext(state);else if (/atom|string|variable/.test(style) && state.context) {
      if (/[\}\]]/.test(state.context.type)) pushContext(state, "pattern", stream.column());else if (state.context.type == "pattern" && !state.context.align) {
        state.context.align = true;
        state.context.col = stream.column();
      }
    }
    return style;
  },
  indent: function (state, textAfter, cx) {
    var firstChar = textAfter && textAfter.charAt(0);
    var context = state.context;
    if (/[\]\}]/.test(firstChar)) while (context && context.type == "pattern") context = context.prev;
    var closing = context && firstChar == context.type;
    if (!context) return 0;else if (context.type == "pattern") return context.col;else if (context.align) return context.col + (closing ? 0 : 1);else return context.indent + (closing ? 0 : cx.unit);
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNTcxMy5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGNvZGVtaXJyb3IvbGVnYWN5LW1vZGVzL21vZGUvcS5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyJ2YXIgY3VyUHVuYyxcbiAga2V5d29yZHMgPSBidWlsZFJFKFtcImFic1wiLCBcImFjb3NcIiwgXCJhalwiLCBcImFqMFwiLCBcImFsbFwiLCBcImFuZFwiLCBcImFueVwiLCBcImFzY1wiLCBcImFzaW5cIiwgXCJhc29mXCIsIFwiYXRhblwiLCBcImF0dHJcIiwgXCJhdmdcIiwgXCJhdmdzXCIsIFwiYmluXCIsIFwiYnlcIiwgXCJjZWlsaW5nXCIsIFwiY29sc1wiLCBcImNvclwiLCBcImNvc1wiLCBcImNvdW50XCIsIFwiY292XCIsIFwiY3Jvc3NcIiwgXCJjc3ZcIiwgXCJjdXRcIiwgXCJkZWxldGVcIiwgXCJkZWx0YXNcIiwgXCJkZXNjXCIsIFwiZGV2XCIsIFwiZGlmZmVyXCIsIFwiZGlzdGluY3RcIiwgXCJkaXZcIiwgXCJkb1wiLCBcImVhY2hcIiwgXCJlalwiLCBcImVubGlzdFwiLCBcImV2YWxcIiwgXCJleGNlcHRcIiwgXCJleGVjXCIsIFwiZXhpdFwiLCBcImV4cFwiLCBcImZieVwiLCBcImZpbGxzXCIsIFwiZmlyc3RcIiwgXCJma2V5c1wiLCBcImZsaXBcIiwgXCJmbG9vclwiLCBcImZyb21cIiwgXCJnZXRcIiwgXCJnZXRlbnZcIiwgXCJncm91cFwiLCBcImd0aW1lXCIsIFwiaGNsb3NlXCIsIFwiaGNvdW50XCIsIFwiaGRlbFwiLCBcImhvcGVuXCIsIFwiaHN5bVwiLCBcImlhc2NcIiwgXCJpZGVzY1wiLCBcImlmXCIsIFwiaWpcIiwgXCJpblwiLCBcImluc2VydFwiLCBcImludGVyXCIsIFwiaW52XCIsIFwia2V5XCIsIFwia2V5c1wiLCBcImxhc3RcIiwgXCJsaWtlXCIsIFwibGlzdFwiLCBcImxqXCIsIFwibG9hZFwiLCBcImxvZ1wiLCBcImxvd2VyXCIsIFwibHNxXCIsIFwibHRpbWVcIiwgXCJsdHJpbVwiLCBcIm1hdmdcIiwgXCJtYXhcIiwgXCJtYXhzXCIsIFwibWNvdW50XCIsIFwibWQ1XCIsIFwibWRldlwiLCBcIm1lZFwiLCBcIm1ldGFcIiwgXCJtaW5cIiwgXCJtaW5zXCIsIFwibW1heFwiLCBcIm1taW5cIiwgXCJtbXVcIiwgXCJtb2RcIiwgXCJtc3VtXCIsIFwibmVnXCIsIFwibmV4dFwiLCBcIm5vdFwiLCBcIm51bGxcIiwgXCJvclwiLCBcIm92ZXJcIiwgXCJwYXJzZVwiLCBcInBlYWNoXCIsIFwicGpcIiwgXCJwbGlzdFwiLCBcInByZFwiLCBcInByZHNcIiwgXCJwcmV2XCIsIFwicHJpb3JcIiwgXCJyYW5kXCIsIFwicmFua1wiLCBcInJhdGlvc1wiLCBcInJhemVcIiwgXCJyZWFkMFwiLCBcInJlYWQxXCIsIFwicmVjaXByb2NhbFwiLCBcInJldmVyc2VcIiwgXCJybG9hZFwiLCBcInJvdGF0ZVwiLCBcInJzYXZlXCIsIFwicnRyaW1cIiwgXCJzYXZlXCIsIFwic2NhblwiLCBcInNlbGVjdFwiLCBcInNldFwiLCBcInNldGVudlwiLCBcInNob3dcIiwgXCJzaWdudW1cIiwgXCJzaW5cIiwgXCJzcXJ0XCIsIFwic3NcIiwgXCJzc3JcIiwgXCJzdHJpbmdcIiwgXCJzdWJsaXN0XCIsIFwic3VtXCIsIFwic3Vtc1wiLCBcInN2XCIsIFwic3lzdGVtXCIsIFwidGFibGVzXCIsIFwidGFuXCIsIFwidGlsXCIsIFwidHJpbVwiLCBcInR4ZlwiLCBcInR5cGVcIiwgXCJ1alwiLCBcInVuZ3JvdXBcIiwgXCJ1bmlvblwiLCBcInVwZGF0ZVwiLCBcInVwcGVyXCIsIFwidXBzZXJ0XCIsIFwidmFsdWVcIiwgXCJ2YXJcIiwgXCJ2aWV3XCIsIFwidmlld3NcIiwgXCJ2c1wiLCBcIndhdmdcIiwgXCJ3aGVyZVwiLCBcIndoZXJlXCIsIFwid2hpbGVcIiwgXCJ3aXRoaW5cIiwgXCJ3alwiLCBcIndqMVwiLCBcIndzdW1cIiwgXCJ4YXNjXCIsIFwieGJhclwiLCBcInhjb2xcIiwgXCJ4Y29sc1wiLCBcInhkZXNjXCIsIFwieGV4cFwiLCBcInhncm91cFwiLCBcInhrZXlcIiwgXCJ4bG9nXCIsIFwieHByZXZcIiwgXCJ4cmFua1wiXSksXG4gIEUgPSAvW3wvJl4hKzpcXFxcXFwtKiUkPX4jO0A+PCw/X1xcJ1xcXCJcXFtcXChcXF1cXClcXHN7fV0vO1xuZnVuY3Rpb24gYnVpbGRSRSh3KSB7XG4gIHJldHVybiBuZXcgUmVnRXhwKFwiXihcIiArIHcuam9pbihcInxcIikgKyBcIikkXCIpO1xufVxuZnVuY3Rpb24gdG9rZW5CYXNlKHN0cmVhbSwgc3RhdGUpIHtcbiAgdmFyIHNvbCA9IHN0cmVhbS5zb2woKSxcbiAgICBjID0gc3RyZWFtLm5leHQoKTtcbiAgY3VyUHVuYyA9IG51bGw7XG4gIGlmIChzb2wpIGlmIChjID09IFwiL1wiKSByZXR1cm4gKHN0YXRlLnRva2VuaXplID0gdG9rZW5MaW5lQ29tbWVudCkoc3RyZWFtLCBzdGF0ZSk7ZWxzZSBpZiAoYyA9PSBcIlxcXFxcIikge1xuICAgIGlmIChzdHJlYW0uZW9sKCkgfHwgL1xccy8udGVzdChzdHJlYW0ucGVlaygpKSkgcmV0dXJuIHN0cmVhbS5za2lwVG9FbmQoKSwgL15cXFxcXFxzKiQvLnRlc3Qoc3RyZWFtLmN1cnJlbnQoKSkgPyAoc3RhdGUudG9rZW5pemUgPSB0b2tlbkNvbW1lbnRUb0VPRikoc3RyZWFtKSA6IHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlLCBcImNvbW1lbnRcIjtlbHNlIHJldHVybiBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQmFzZSwgXCJidWlsdGluXCI7XG4gIH1cbiAgaWYgKC9cXHMvLnRlc3QoYykpIHJldHVybiBzdHJlYW0ucGVlaygpID09IFwiL1wiID8gKHN0cmVhbS5za2lwVG9FbmQoKSwgXCJjb21tZW50XCIpIDogXCJudWxsXCI7XG4gIGlmIChjID09ICdcIicpIHJldHVybiAoc3RhdGUudG9rZW5pemUgPSB0b2tlblN0cmluZykoc3RyZWFtLCBzdGF0ZSk7XG4gIGlmIChjID09ICdgJykgcmV0dXJuIHN0cmVhbS5lYXRXaGlsZSgvW0EtWmEtelxcZF86XFwvLl0vKSwgXCJtYWNyb05hbWVcIjtcbiAgaWYgKFwiLlwiID09IGMgJiYgL1xcZC8udGVzdChzdHJlYW0ucGVlaygpKSB8fCAvXFxkLy50ZXN0KGMpKSB7XG4gICAgdmFyIHQgPSBudWxsO1xuICAgIHN0cmVhbS5iYWNrVXAoMSk7XG4gICAgaWYgKHN0cmVhbS5tYXRjaCgvXlxcZHs0fVxcLlxcZHsyfShtfFxcLlxcZHsyfShbRFRdKFxcZHsyfSg6XFxkezJ9KDpcXGR7Mn0oXFwuXFxkezEsOX0pPyk/KT8pPyk/KS8pIHx8IHN0cmVhbS5tYXRjaCgvXlxcZCtEKFxcZHsyfSg6XFxkezJ9KDpcXGR7Mn0oXFwuXFxkezEsOX0pPyk/KT8pLykgfHwgc3RyZWFtLm1hdGNoKC9eXFxkezJ9OlxcZHsyfSg6XFxkezJ9KFxcLlxcZHsxLDl9KT8pPy8pIHx8IHN0cmVhbS5tYXRjaCgvXlxcZCtbcHR1dl17MX0vKSkgdCA9IFwidGVtcG9yYWxcIjtlbHNlIGlmIChzdHJlYW0ubWF0Y2goL14wW053V117MX0vKSB8fCBzdHJlYW0ubWF0Y2goL14weFtcXGRhLWZBLUZdKi8pIHx8IHN0cmVhbS5tYXRjaCgvXlswMV0rW2JdezF9LykgfHwgc3RyZWFtLm1hdGNoKC9eXFxkK1tjaGlqbl17MX0vKSB8fCBzdHJlYW0ubWF0Y2goLy0/XFxkKihcXC5cXGQqKT8oZVsrXFwtXT9cXGQrKT8oZXxmKT8vKSkgdCA9IFwibnVtYmVyXCI7XG4gICAgcmV0dXJuIHQgJiYgKCEoYyA9IHN0cmVhbS5wZWVrKCkpIHx8IEUudGVzdChjKSkgPyB0IDogKHN0cmVhbS5uZXh0KCksIFwiZXJyb3JcIik7XG4gIH1cbiAgaWYgKC9bQS1aYS16XXxcXC4vLnRlc3QoYykpIHJldHVybiBzdHJlYW0uZWF0V2hpbGUoL1tBLVphLXouX1xcZF0vKSwga2V5d29yZHMudGVzdChzdHJlYW0uY3VycmVudCgpKSA/IFwia2V5d29yZFwiIDogXCJ2YXJpYWJsZVwiO1xuICBpZiAoL1t8LyZeISs6XFxcXFxcLSolJD1+IztAPjxcXC4sP19cXCddLy50ZXN0KGMpKSByZXR1cm4gbnVsbDtcbiAgaWYgKC9be31cXChcXFtcXF1cXCldLy50ZXN0KGMpKSByZXR1cm4gbnVsbDtcbiAgcmV0dXJuIFwiZXJyb3JcIjtcbn1cbmZ1bmN0aW9uIHRva2VuTGluZUNvbW1lbnQoc3RyZWFtLCBzdGF0ZSkge1xuICByZXR1cm4gc3RyZWFtLnNraXBUb0VuZCgpLCAvXFwvXFxzKiQvLnRlc3Qoc3RyZWFtLmN1cnJlbnQoKSkgPyAoc3RhdGUudG9rZW5pemUgPSB0b2tlbkJsb2NrQ29tbWVudCkoc3RyZWFtLCBzdGF0ZSkgOiBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQmFzZSwgXCJjb21tZW50XCI7XG59XG5mdW5jdGlvbiB0b2tlbkJsb2NrQ29tbWVudChzdHJlYW0sIHN0YXRlKSB7XG4gIHZhciBmID0gc3RyZWFtLnNvbCgpICYmIHN0cmVhbS5wZWVrKCkgPT0gXCJcXFxcXCI7XG4gIHN0cmVhbS5za2lwVG9FbmQoKTtcbiAgaWYgKGYgJiYgL15cXFxcXFxzKiQvLnRlc3Qoc3RyZWFtLmN1cnJlbnQoKSkpIHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlO1xuICByZXR1cm4gXCJjb21tZW50XCI7XG59XG5mdW5jdGlvbiB0b2tlbkNvbW1lbnRUb0VPRihzdHJlYW0pIHtcbiAgcmV0dXJuIHN0cmVhbS5za2lwVG9FbmQoKSwgXCJjb21tZW50XCI7XG59XG5mdW5jdGlvbiB0b2tlblN0cmluZyhzdHJlYW0sIHN0YXRlKSB7XG4gIHZhciBlc2NhcGVkID0gZmFsc2UsXG4gICAgbmV4dCxcbiAgICBlbmQgPSBmYWxzZTtcbiAgd2hpbGUgKG5leHQgPSBzdHJlYW0ubmV4dCgpKSB7XG4gICAgaWYgKG5leHQgPT0gXCJcXFwiXCIgJiYgIWVzY2FwZWQpIHtcbiAgICAgIGVuZCA9IHRydWU7XG4gICAgICBicmVhaztcbiAgICB9XG4gICAgZXNjYXBlZCA9ICFlc2NhcGVkICYmIG5leHQgPT0gXCJcXFxcXCI7XG4gIH1cbiAgaWYgKGVuZCkgc3RhdGUudG9rZW5pemUgPSB0b2tlbkJhc2U7XG4gIHJldHVybiBcInN0cmluZ1wiO1xufVxuZnVuY3Rpb24gcHVzaENvbnRleHQoc3RhdGUsIHR5cGUsIGNvbCkge1xuICBzdGF0ZS5jb250ZXh0ID0ge1xuICAgIHByZXY6IHN0YXRlLmNvbnRleHQsXG4gICAgaW5kZW50OiBzdGF0ZS5pbmRlbnQsXG4gICAgY29sOiBjb2wsXG4gICAgdHlwZTogdHlwZVxuICB9O1xufVxuZnVuY3Rpb24gcG9wQ29udGV4dChzdGF0ZSkge1xuICBzdGF0ZS5pbmRlbnQgPSBzdGF0ZS5jb250ZXh0LmluZGVudDtcbiAgc3RhdGUuY29udGV4dCA9IHN0YXRlLmNvbnRleHQucHJldjtcbn1cbmV4cG9ydCBjb25zdCBxID0ge1xuICBuYW1lOiBcInFcIixcbiAgc3RhcnRTdGF0ZTogZnVuY3Rpb24gKCkge1xuICAgIHJldHVybiB7XG4gICAgICB0b2tlbml6ZTogdG9rZW5CYXNlLFxuICAgICAgY29udGV4dDogbnVsbCxcbiAgICAgIGluZGVudDogMCxcbiAgICAgIGNvbDogMFxuICAgIH07XG4gIH0sXG4gIHRva2VuOiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIGlmIChzdHJlYW0uc29sKCkpIHtcbiAgICAgIGlmIChzdGF0ZS5jb250ZXh0ICYmIHN0YXRlLmNvbnRleHQuYWxpZ24gPT0gbnVsbCkgc3RhdGUuY29udGV4dC5hbGlnbiA9IGZhbHNlO1xuICAgICAgc3RhdGUuaW5kZW50ID0gc3RyZWFtLmluZGVudGF0aW9uKCk7XG4gICAgfVxuICAgIC8vaWYgKHN0cmVhbS5lYXRTcGFjZSgpKSByZXR1cm4gbnVsbDtcbiAgICB2YXIgc3R5bGUgPSBzdGF0ZS50b2tlbml6ZShzdHJlYW0sIHN0YXRlKTtcbiAgICBpZiAoc3R5bGUgIT0gXCJjb21tZW50XCIgJiYgc3RhdGUuY29udGV4dCAmJiBzdGF0ZS5jb250ZXh0LmFsaWduID09IG51bGwgJiYgc3RhdGUuY29udGV4dC50eXBlICE9IFwicGF0dGVyblwiKSB7XG4gICAgICBzdGF0ZS5jb250ZXh0LmFsaWduID0gdHJ1ZTtcbiAgICB9XG4gICAgaWYgKGN1clB1bmMgPT0gXCIoXCIpIHB1c2hDb250ZXh0KHN0YXRlLCBcIilcIiwgc3RyZWFtLmNvbHVtbigpKTtlbHNlIGlmIChjdXJQdW5jID09IFwiW1wiKSBwdXNoQ29udGV4dChzdGF0ZSwgXCJdXCIsIHN0cmVhbS5jb2x1bW4oKSk7ZWxzZSBpZiAoY3VyUHVuYyA9PSBcIntcIikgcHVzaENvbnRleHQoc3RhdGUsIFwifVwiLCBzdHJlYW0uY29sdW1uKCkpO2Vsc2UgaWYgKC9bXFxdXFx9XFwpXS8udGVzdChjdXJQdW5jKSkge1xuICAgICAgd2hpbGUgKHN0YXRlLmNvbnRleHQgJiYgc3RhdGUuY29udGV4dC50eXBlID09IFwicGF0dGVyblwiKSBwb3BDb250ZXh0KHN0YXRlKTtcbiAgICAgIGlmIChzdGF0ZS5jb250ZXh0ICYmIGN1clB1bmMgPT0gc3RhdGUuY29udGV4dC50eXBlKSBwb3BDb250ZXh0KHN0YXRlKTtcbiAgICB9IGVsc2UgaWYgKGN1clB1bmMgPT0gXCIuXCIgJiYgc3RhdGUuY29udGV4dCAmJiBzdGF0ZS5jb250ZXh0LnR5cGUgPT0gXCJwYXR0ZXJuXCIpIHBvcENvbnRleHQoc3RhdGUpO2Vsc2UgaWYgKC9hdG9tfHN0cmluZ3x2YXJpYWJsZS8udGVzdChzdHlsZSkgJiYgc3RhdGUuY29udGV4dCkge1xuICAgICAgaWYgKC9bXFx9XFxdXS8udGVzdChzdGF0ZS5jb250ZXh0LnR5cGUpKSBwdXNoQ29udGV4dChzdGF0ZSwgXCJwYXR0ZXJuXCIsIHN0cmVhbS5jb2x1bW4oKSk7ZWxzZSBpZiAoc3RhdGUuY29udGV4dC50eXBlID09IFwicGF0dGVyblwiICYmICFzdGF0ZS5jb250ZXh0LmFsaWduKSB7XG4gICAgICAgIHN0YXRlLmNvbnRleHQuYWxpZ24gPSB0cnVlO1xuICAgICAgICBzdGF0ZS5jb250ZXh0LmNvbCA9IHN0cmVhbS5jb2x1bW4oKTtcbiAgICAgIH1cbiAgICB9XG4gICAgcmV0dXJuIHN0eWxlO1xuICB9LFxuICBpbmRlbnQ6IGZ1bmN0aW9uIChzdGF0ZSwgdGV4dEFmdGVyLCBjeCkge1xuICAgIHZhciBmaXJzdENoYXIgPSB0ZXh0QWZ0ZXIgJiYgdGV4dEFmdGVyLmNoYXJBdCgwKTtcbiAgICB2YXIgY29udGV4dCA9IHN0YXRlLmNvbnRleHQ7XG4gICAgaWYgKC9bXFxdXFx9XS8udGVzdChmaXJzdENoYXIpKSB3aGlsZSAoY29udGV4dCAmJiBjb250ZXh0LnR5cGUgPT0gXCJwYXR0ZXJuXCIpIGNvbnRleHQgPSBjb250ZXh0LnByZXY7XG4gICAgdmFyIGNsb3NpbmcgPSBjb250ZXh0ICYmIGZpcnN0Q2hhciA9PSBjb250ZXh0LnR5cGU7XG4gICAgaWYgKCFjb250ZXh0KSByZXR1cm4gMDtlbHNlIGlmIChjb250ZXh0LnR5cGUgPT0gXCJwYXR0ZXJuXCIpIHJldHVybiBjb250ZXh0LmNvbDtlbHNlIGlmIChjb250ZXh0LmFsaWduKSByZXR1cm4gY29udGV4dC5jb2wgKyAoY2xvc2luZyA/IDAgOiAxKTtlbHNlIHJldHVybiBjb250ZXh0LmluZGVudCArIChjbG9zaW5nID8gMCA6IGN4LnVuaXQpO1xuICB9XG59OyJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==