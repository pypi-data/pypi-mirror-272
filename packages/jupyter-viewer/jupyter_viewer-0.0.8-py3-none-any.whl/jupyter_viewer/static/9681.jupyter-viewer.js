"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[9681],{

/***/ 79681:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "sparql": () => (/* binding */ sparql)
/* harmony export */ });
var curPunc;
function wordRegexp(words) {
  return new RegExp("^(?:" + words.join("|") + ")$", "i");
}
var ops = wordRegexp(["str", "lang", "langmatches", "datatype", "bound", "sameterm", "isiri", "isuri", "iri", "uri", "bnode", "count", "sum", "min", "max", "avg", "sample", "group_concat", "rand", "abs", "ceil", "floor", "round", "concat", "substr", "strlen", "replace", "ucase", "lcase", "encode_for_uri", "contains", "strstarts", "strends", "strbefore", "strafter", "year", "month", "day", "hours", "minutes", "seconds", "timezone", "tz", "now", "uuid", "struuid", "md5", "sha1", "sha256", "sha384", "sha512", "coalesce", "if", "strlang", "strdt", "isnumeric", "regex", "exists", "isblank", "isliteral", "a", "bind"]);
var keywords = wordRegexp(["base", "prefix", "select", "distinct", "reduced", "construct", "describe", "ask", "from", "named", "where", "order", "limit", "offset", "filter", "optional", "graph", "by", "asc", "desc", "as", "having", "undef", "values", "group", "minus", "in", "not", "service", "silent", "using", "insert", "delete", "union", "true", "false", "with", "data", "copy", "to", "move", "add", "create", "drop", "clear", "load", "into"]);
var operatorChars = /[*+\-<>=&|\^\/!\?]/;
var PN_CHARS = "[A-Za-z_\\-0-9]";
var PREFIX_START = new RegExp("[A-Za-z]");
var PREFIX_REMAINDER = new RegExp("((" + PN_CHARS + "|\\.)*(" + PN_CHARS + "))?:");
function tokenBase(stream, state) {
  var ch = stream.next();
  curPunc = null;
  if (ch == "$" || ch == "?") {
    if (ch == "?" && stream.match(/\s/, false)) {
      return "operator";
    }
    stream.match(/^[A-Za-z0-9_\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD][A-Za-z0-9_\u00B7\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u037D\u037F-\u1FFF\u200C-\u200D\u203F-\u2040\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD]*/);
    return "variableName.local";
  } else if (ch == "<" && !stream.match(/^[\s\u00a0=]/, false)) {
    stream.match(/^[^\s\u00a0>]*>?/);
    return "atom";
  } else if (ch == "\"" || ch == "'") {
    state.tokenize = tokenLiteral(ch);
    return state.tokenize(stream, state);
  } else if (/[{}\(\),\.;\[\]]/.test(ch)) {
    curPunc = ch;
    return "bracket";
  } else if (ch == "#") {
    stream.skipToEnd();
    return "comment";
  } else if (operatorChars.test(ch)) {
    return "operator";
  } else if (ch == ":") {
    eatPnLocal(stream);
    return "atom";
  } else if (ch == "@") {
    stream.eatWhile(/[a-z\d\-]/i);
    return "meta";
  } else if (PREFIX_START.test(ch) && stream.match(PREFIX_REMAINDER)) {
    eatPnLocal(stream);
    return "atom";
  }
  stream.eatWhile(/[_\w\d]/);
  var word = stream.current();
  if (ops.test(word)) return "builtin";else if (keywords.test(word)) return "keyword";else return "variable";
}
function eatPnLocal(stream) {
  stream.match(/(\.(?=[\w_\-\\%])|[:\w_-]|\\[-\\_~.!$&'()*+,;=/?#@%]|%[a-f\d][a-f\d])+/i);
}
function tokenLiteral(quote) {
  return function (stream, state) {
    var escaped = false,
      ch;
    while ((ch = stream.next()) != null) {
      if (ch == quote && !escaped) {
        state.tokenize = tokenBase;
        break;
      }
      escaped = !escaped && ch == "\\";
    }
    return "string";
  };
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
const sparql = {
  name: "sparql",
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
    if (stream.eatSpace()) return null;
    var style = state.tokenize(stream, state);
    if (style != "comment" && state.context && state.context.align == null && state.context.type != "pattern") {
      state.context.align = true;
    }
    if (curPunc == "(") pushContext(state, ")", stream.column());else if (curPunc == "[") pushContext(state, "]", stream.column());else if (curPunc == "{") pushContext(state, "}", stream.column());else if (/[\]\}\)]/.test(curPunc)) {
      while (state.context && state.context.type == "pattern") popContext(state);
      if (state.context && curPunc == state.context.type) {
        popContext(state);
        if (curPunc == "}" && state.context && state.context.type == "pattern") popContext(state);
      }
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
  },
  languageData: {
    commentTokens: {
      line: "#"
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiOTY4MS5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9AY29kZW1pcnJvci9sZWdhY3ktbW9kZXMvbW9kZS9zcGFycWwuanMiXSwic291cmNlc0NvbnRlbnQiOlsidmFyIGN1clB1bmM7XG5mdW5jdGlvbiB3b3JkUmVnZXhwKHdvcmRzKSB7XG4gIHJldHVybiBuZXcgUmVnRXhwKFwiXig/OlwiICsgd29yZHMuam9pbihcInxcIikgKyBcIikkXCIsIFwiaVwiKTtcbn1cbnZhciBvcHMgPSB3b3JkUmVnZXhwKFtcInN0clwiLCBcImxhbmdcIiwgXCJsYW5nbWF0Y2hlc1wiLCBcImRhdGF0eXBlXCIsIFwiYm91bmRcIiwgXCJzYW1ldGVybVwiLCBcImlzaXJpXCIsIFwiaXN1cmlcIiwgXCJpcmlcIiwgXCJ1cmlcIiwgXCJibm9kZVwiLCBcImNvdW50XCIsIFwic3VtXCIsIFwibWluXCIsIFwibWF4XCIsIFwiYXZnXCIsIFwic2FtcGxlXCIsIFwiZ3JvdXBfY29uY2F0XCIsIFwicmFuZFwiLCBcImFic1wiLCBcImNlaWxcIiwgXCJmbG9vclwiLCBcInJvdW5kXCIsIFwiY29uY2F0XCIsIFwic3Vic3RyXCIsIFwic3RybGVuXCIsIFwicmVwbGFjZVwiLCBcInVjYXNlXCIsIFwibGNhc2VcIiwgXCJlbmNvZGVfZm9yX3VyaVwiLCBcImNvbnRhaW5zXCIsIFwic3Ryc3RhcnRzXCIsIFwic3RyZW5kc1wiLCBcInN0cmJlZm9yZVwiLCBcInN0cmFmdGVyXCIsIFwieWVhclwiLCBcIm1vbnRoXCIsIFwiZGF5XCIsIFwiaG91cnNcIiwgXCJtaW51dGVzXCIsIFwic2Vjb25kc1wiLCBcInRpbWV6b25lXCIsIFwidHpcIiwgXCJub3dcIiwgXCJ1dWlkXCIsIFwic3RydXVpZFwiLCBcIm1kNVwiLCBcInNoYTFcIiwgXCJzaGEyNTZcIiwgXCJzaGEzODRcIiwgXCJzaGE1MTJcIiwgXCJjb2FsZXNjZVwiLCBcImlmXCIsIFwic3RybGFuZ1wiLCBcInN0cmR0XCIsIFwiaXNudW1lcmljXCIsIFwicmVnZXhcIiwgXCJleGlzdHNcIiwgXCJpc2JsYW5rXCIsIFwiaXNsaXRlcmFsXCIsIFwiYVwiLCBcImJpbmRcIl0pO1xudmFyIGtleXdvcmRzID0gd29yZFJlZ2V4cChbXCJiYXNlXCIsIFwicHJlZml4XCIsIFwic2VsZWN0XCIsIFwiZGlzdGluY3RcIiwgXCJyZWR1Y2VkXCIsIFwiY29uc3RydWN0XCIsIFwiZGVzY3JpYmVcIiwgXCJhc2tcIiwgXCJmcm9tXCIsIFwibmFtZWRcIiwgXCJ3aGVyZVwiLCBcIm9yZGVyXCIsIFwibGltaXRcIiwgXCJvZmZzZXRcIiwgXCJmaWx0ZXJcIiwgXCJvcHRpb25hbFwiLCBcImdyYXBoXCIsIFwiYnlcIiwgXCJhc2NcIiwgXCJkZXNjXCIsIFwiYXNcIiwgXCJoYXZpbmdcIiwgXCJ1bmRlZlwiLCBcInZhbHVlc1wiLCBcImdyb3VwXCIsIFwibWludXNcIiwgXCJpblwiLCBcIm5vdFwiLCBcInNlcnZpY2VcIiwgXCJzaWxlbnRcIiwgXCJ1c2luZ1wiLCBcImluc2VydFwiLCBcImRlbGV0ZVwiLCBcInVuaW9uXCIsIFwidHJ1ZVwiLCBcImZhbHNlXCIsIFwid2l0aFwiLCBcImRhdGFcIiwgXCJjb3B5XCIsIFwidG9cIiwgXCJtb3ZlXCIsIFwiYWRkXCIsIFwiY3JlYXRlXCIsIFwiZHJvcFwiLCBcImNsZWFyXCIsIFwibG9hZFwiLCBcImludG9cIl0pO1xudmFyIG9wZXJhdG9yQ2hhcnMgPSAvWyorXFwtPD49JnxcXF5cXC8hXFw/XS87XG52YXIgUE5fQ0hBUlMgPSBcIltBLVphLXpfXFxcXC0wLTldXCI7XG52YXIgUFJFRklYX1NUQVJUID0gbmV3IFJlZ0V4cChcIltBLVphLXpdXCIpO1xudmFyIFBSRUZJWF9SRU1BSU5ERVIgPSBuZXcgUmVnRXhwKFwiKChcIiArIFBOX0NIQVJTICsgXCJ8XFxcXC4pKihcIiArIFBOX0NIQVJTICsgXCIpKT86XCIpO1xuZnVuY3Rpb24gdG9rZW5CYXNlKHN0cmVhbSwgc3RhdGUpIHtcbiAgdmFyIGNoID0gc3RyZWFtLm5leHQoKTtcbiAgY3VyUHVuYyA9IG51bGw7XG4gIGlmIChjaCA9PSBcIiRcIiB8fCBjaCA9PSBcIj9cIikge1xuICAgIGlmIChjaCA9PSBcIj9cIiAmJiBzdHJlYW0ubWF0Y2goL1xccy8sIGZhbHNlKSkge1xuICAgICAgcmV0dXJuIFwib3BlcmF0b3JcIjtcbiAgICB9XG4gICAgc3RyZWFtLm1hdGNoKC9eW0EtWmEtejAtOV9cXHUwMEMwLVxcdTAwRDZcXHUwMEQ4LVxcdTAwRjZcXHUwMEY4LVxcdTAyRkZcXHUwMzcwLVxcdTAzN0RcXHUwMzdGLVxcdTFGRkZcXHUyMDBDLVxcdTIwMERcXHUyMDcwLVxcdTIxOEZcXHUyQzAwLVxcdTJGRUZcXHUzMDAxLVxcdUQ3RkZcXHVGOTAwLVxcdUZEQ0ZcXHVGREYwLVxcdUZGRkRdW0EtWmEtejAtOV9cXHUwMEI3XFx1MDBDMC1cXHUwMEQ2XFx1MDBEOC1cXHUwMEY2XFx1MDBGOC1cXHUwMzdEXFx1MDM3Ri1cXHUxRkZGXFx1MjAwQy1cXHUyMDBEXFx1MjAzRi1cXHUyMDQwXFx1MjA3MC1cXHUyMThGXFx1MkMwMC1cXHUyRkVGXFx1MzAwMS1cXHVEN0ZGXFx1RjkwMC1cXHVGRENGXFx1RkRGMC1cXHVGRkZEXSovKTtcbiAgICByZXR1cm4gXCJ2YXJpYWJsZU5hbWUubG9jYWxcIjtcbiAgfSBlbHNlIGlmIChjaCA9PSBcIjxcIiAmJiAhc3RyZWFtLm1hdGNoKC9eW1xcc1xcdTAwYTA9XS8sIGZhbHNlKSkge1xuICAgIHN0cmVhbS5tYXRjaCgvXlteXFxzXFx1MDBhMD5dKj4/Lyk7XG4gICAgcmV0dXJuIFwiYXRvbVwiO1xuICB9IGVsc2UgaWYgKGNoID09IFwiXFxcIlwiIHx8IGNoID09IFwiJ1wiKSB7XG4gICAgc3RhdGUudG9rZW5pemUgPSB0b2tlbkxpdGVyYWwoY2gpO1xuICAgIHJldHVybiBzdGF0ZS50b2tlbml6ZShzdHJlYW0sIHN0YXRlKTtcbiAgfSBlbHNlIGlmICgvW3t9XFwoXFwpLFxcLjtcXFtcXF1dLy50ZXN0KGNoKSkge1xuICAgIGN1clB1bmMgPSBjaDtcbiAgICByZXR1cm4gXCJicmFja2V0XCI7XG4gIH0gZWxzZSBpZiAoY2ggPT0gXCIjXCIpIHtcbiAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICB9IGVsc2UgaWYgKG9wZXJhdG9yQ2hhcnMudGVzdChjaCkpIHtcbiAgICByZXR1cm4gXCJvcGVyYXRvclwiO1xuICB9IGVsc2UgaWYgKGNoID09IFwiOlwiKSB7XG4gICAgZWF0UG5Mb2NhbChzdHJlYW0pO1xuICAgIHJldHVybiBcImF0b21cIjtcbiAgfSBlbHNlIGlmIChjaCA9PSBcIkBcIikge1xuICAgIHN0cmVhbS5lYXRXaGlsZSgvW2EtelxcZFxcLV0vaSk7XG4gICAgcmV0dXJuIFwibWV0YVwiO1xuICB9IGVsc2UgaWYgKFBSRUZJWF9TVEFSVC50ZXN0KGNoKSAmJiBzdHJlYW0ubWF0Y2goUFJFRklYX1JFTUFJTkRFUikpIHtcbiAgICBlYXRQbkxvY2FsKHN0cmVhbSk7XG4gICAgcmV0dXJuIFwiYXRvbVwiO1xuICB9XG4gIHN0cmVhbS5lYXRXaGlsZSgvW19cXHdcXGRdLyk7XG4gIHZhciB3b3JkID0gc3RyZWFtLmN1cnJlbnQoKTtcbiAgaWYgKG9wcy50ZXN0KHdvcmQpKSByZXR1cm4gXCJidWlsdGluXCI7ZWxzZSBpZiAoa2V5d29yZHMudGVzdCh3b3JkKSkgcmV0dXJuIFwia2V5d29yZFwiO2Vsc2UgcmV0dXJuIFwidmFyaWFibGVcIjtcbn1cbmZ1bmN0aW9uIGVhdFBuTG9jYWwoc3RyZWFtKSB7XG4gIHN0cmVhbS5tYXRjaCgvKFxcLig/PVtcXHdfXFwtXFxcXCVdKXxbOlxcd18tXXxcXFxcWy1cXFxcX34uISQmJygpKissOz0vPyNAJV18JVthLWZcXGRdW2EtZlxcZF0pKy9pKTtcbn1cbmZ1bmN0aW9uIHRva2VuTGl0ZXJhbChxdW90ZSkge1xuICByZXR1cm4gZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICB2YXIgZXNjYXBlZCA9IGZhbHNlLFxuICAgICAgY2g7XG4gICAgd2hpbGUgKChjaCA9IHN0cmVhbS5uZXh0KCkpICE9IG51bGwpIHtcbiAgICAgIGlmIChjaCA9PSBxdW90ZSAmJiAhZXNjYXBlZCkge1xuICAgICAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQmFzZTtcbiAgICAgICAgYnJlYWs7XG4gICAgICB9XG4gICAgICBlc2NhcGVkID0gIWVzY2FwZWQgJiYgY2ggPT0gXCJcXFxcXCI7XG4gICAgfVxuICAgIHJldHVybiBcInN0cmluZ1wiO1xuICB9O1xufVxuZnVuY3Rpb24gcHVzaENvbnRleHQoc3RhdGUsIHR5cGUsIGNvbCkge1xuICBzdGF0ZS5jb250ZXh0ID0ge1xuICAgIHByZXY6IHN0YXRlLmNvbnRleHQsXG4gICAgaW5kZW50OiBzdGF0ZS5pbmRlbnQsXG4gICAgY29sOiBjb2wsXG4gICAgdHlwZTogdHlwZVxuICB9O1xufVxuZnVuY3Rpb24gcG9wQ29udGV4dChzdGF0ZSkge1xuICBzdGF0ZS5pbmRlbnQgPSBzdGF0ZS5jb250ZXh0LmluZGVudDtcbiAgc3RhdGUuY29udGV4dCA9IHN0YXRlLmNvbnRleHQucHJldjtcbn1cbmV4cG9ydCBjb25zdCBzcGFycWwgPSB7XG4gIG5hbWU6IFwic3BhcnFsXCIsXG4gIHN0YXJ0U3RhdGU6IGZ1bmN0aW9uICgpIHtcbiAgICByZXR1cm4ge1xuICAgICAgdG9rZW5pemU6IHRva2VuQmFzZSxcbiAgICAgIGNvbnRleHQ6IG51bGwsXG4gICAgICBpbmRlbnQ6IDAsXG4gICAgICBjb2w6IDBcbiAgICB9O1xuICB9LFxuICB0b2tlbjogZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICBpZiAoc3RyZWFtLnNvbCgpKSB7XG4gICAgICBpZiAoc3RhdGUuY29udGV4dCAmJiBzdGF0ZS5jb250ZXh0LmFsaWduID09IG51bGwpIHN0YXRlLmNvbnRleHQuYWxpZ24gPSBmYWxzZTtcbiAgICAgIHN0YXRlLmluZGVudCA9IHN0cmVhbS5pbmRlbnRhdGlvbigpO1xuICAgIH1cbiAgICBpZiAoc3RyZWFtLmVhdFNwYWNlKCkpIHJldHVybiBudWxsO1xuICAgIHZhciBzdHlsZSA9IHN0YXRlLnRva2VuaXplKHN0cmVhbSwgc3RhdGUpO1xuICAgIGlmIChzdHlsZSAhPSBcImNvbW1lbnRcIiAmJiBzdGF0ZS5jb250ZXh0ICYmIHN0YXRlLmNvbnRleHQuYWxpZ24gPT0gbnVsbCAmJiBzdGF0ZS5jb250ZXh0LnR5cGUgIT0gXCJwYXR0ZXJuXCIpIHtcbiAgICAgIHN0YXRlLmNvbnRleHQuYWxpZ24gPSB0cnVlO1xuICAgIH1cbiAgICBpZiAoY3VyUHVuYyA9PSBcIihcIikgcHVzaENvbnRleHQoc3RhdGUsIFwiKVwiLCBzdHJlYW0uY29sdW1uKCkpO2Vsc2UgaWYgKGN1clB1bmMgPT0gXCJbXCIpIHB1c2hDb250ZXh0KHN0YXRlLCBcIl1cIiwgc3RyZWFtLmNvbHVtbigpKTtlbHNlIGlmIChjdXJQdW5jID09IFwie1wiKSBwdXNoQ29udGV4dChzdGF0ZSwgXCJ9XCIsIHN0cmVhbS5jb2x1bW4oKSk7ZWxzZSBpZiAoL1tcXF1cXH1cXCldLy50ZXN0KGN1clB1bmMpKSB7XG4gICAgICB3aGlsZSAoc3RhdGUuY29udGV4dCAmJiBzdGF0ZS5jb250ZXh0LnR5cGUgPT0gXCJwYXR0ZXJuXCIpIHBvcENvbnRleHQoc3RhdGUpO1xuICAgICAgaWYgKHN0YXRlLmNvbnRleHQgJiYgY3VyUHVuYyA9PSBzdGF0ZS5jb250ZXh0LnR5cGUpIHtcbiAgICAgICAgcG9wQ29udGV4dChzdGF0ZSk7XG4gICAgICAgIGlmIChjdXJQdW5jID09IFwifVwiICYmIHN0YXRlLmNvbnRleHQgJiYgc3RhdGUuY29udGV4dC50eXBlID09IFwicGF0dGVyblwiKSBwb3BDb250ZXh0KHN0YXRlKTtcbiAgICAgIH1cbiAgICB9IGVsc2UgaWYgKGN1clB1bmMgPT0gXCIuXCIgJiYgc3RhdGUuY29udGV4dCAmJiBzdGF0ZS5jb250ZXh0LnR5cGUgPT0gXCJwYXR0ZXJuXCIpIHBvcENvbnRleHQoc3RhdGUpO2Vsc2UgaWYgKC9hdG9tfHN0cmluZ3x2YXJpYWJsZS8udGVzdChzdHlsZSkgJiYgc3RhdGUuY29udGV4dCkge1xuICAgICAgaWYgKC9bXFx9XFxdXS8udGVzdChzdGF0ZS5jb250ZXh0LnR5cGUpKSBwdXNoQ29udGV4dChzdGF0ZSwgXCJwYXR0ZXJuXCIsIHN0cmVhbS5jb2x1bW4oKSk7ZWxzZSBpZiAoc3RhdGUuY29udGV4dC50eXBlID09IFwicGF0dGVyblwiICYmICFzdGF0ZS5jb250ZXh0LmFsaWduKSB7XG4gICAgICAgIHN0YXRlLmNvbnRleHQuYWxpZ24gPSB0cnVlO1xuICAgICAgICBzdGF0ZS5jb250ZXh0LmNvbCA9IHN0cmVhbS5jb2x1bW4oKTtcbiAgICAgIH1cbiAgICB9XG4gICAgcmV0dXJuIHN0eWxlO1xuICB9LFxuICBpbmRlbnQ6IGZ1bmN0aW9uIChzdGF0ZSwgdGV4dEFmdGVyLCBjeCkge1xuICAgIHZhciBmaXJzdENoYXIgPSB0ZXh0QWZ0ZXIgJiYgdGV4dEFmdGVyLmNoYXJBdCgwKTtcbiAgICB2YXIgY29udGV4dCA9IHN0YXRlLmNvbnRleHQ7XG4gICAgaWYgKC9bXFxdXFx9XS8udGVzdChmaXJzdENoYXIpKSB3aGlsZSAoY29udGV4dCAmJiBjb250ZXh0LnR5cGUgPT0gXCJwYXR0ZXJuXCIpIGNvbnRleHQgPSBjb250ZXh0LnByZXY7XG4gICAgdmFyIGNsb3NpbmcgPSBjb250ZXh0ICYmIGZpcnN0Q2hhciA9PSBjb250ZXh0LnR5cGU7XG4gICAgaWYgKCFjb250ZXh0KSByZXR1cm4gMDtlbHNlIGlmIChjb250ZXh0LnR5cGUgPT0gXCJwYXR0ZXJuXCIpIHJldHVybiBjb250ZXh0LmNvbDtlbHNlIGlmIChjb250ZXh0LmFsaWduKSByZXR1cm4gY29udGV4dC5jb2wgKyAoY2xvc2luZyA/IDAgOiAxKTtlbHNlIHJldHVybiBjb250ZXh0LmluZGVudCArIChjbG9zaW5nID8gMCA6IGN4LnVuaXQpO1xuICB9LFxuICBsYW5ndWFnZURhdGE6IHtcbiAgICBjb21tZW50VG9rZW5zOiB7XG4gICAgICBsaW5lOiBcIiNcIlxuICAgIH1cbiAgfVxufTsiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=