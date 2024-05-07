"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[8263],{

/***/ 88263:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "cypher": () => (/* binding */ cypher)
/* harmony export */ });
var wordRegexp = function (words) {
  return new RegExp("^(?:" + words.join("|") + ")$", "i");
};
var tokenBase = function (stream /*, state*/) {
  curPunc = null;
  var ch = stream.next();
  if (ch === '"') {
    stream.match(/^.*?"/);
    return "string";
  }
  if (ch === "'") {
    stream.match(/^.*?'/);
    return "string";
  }
  if (/[{}\(\),\.;\[\]]/.test(ch)) {
    curPunc = ch;
    return "punctuation";
  } else if (ch === "/" && stream.eat("/")) {
    stream.skipToEnd();
    return "comment";
  } else if (operatorChars.test(ch)) {
    stream.eatWhile(operatorChars);
    return null;
  } else {
    stream.eatWhile(/[_\w\d]/);
    if (stream.eat(":")) {
      stream.eatWhile(/[\w\d_\-]/);
      return "atom";
    }
    var word = stream.current();
    if (funcs.test(word)) return "builtin";
    if (preds.test(word)) return "def";
    if (keywords.test(word) || systemKeywords.test(word)) return "keyword";
    return "variable";
  }
};
var pushContext = function (state, type, col) {
  return state.context = {
    prev: state.context,
    indent: state.indent,
    col: col,
    type: type
  };
};
var popContext = function (state) {
  state.indent = state.context.indent;
  return state.context = state.context.prev;
};
var curPunc;
var funcs = wordRegexp(["abs", "acos", "allShortestPaths", "asin", "atan", "atan2", "avg", "ceil", "coalesce", "collect", "cos", "cot", "count", "degrees", "e", "endnode", "exp", "extract", "filter", "floor", "haversin", "head", "id", "keys", "labels", "last", "left", "length", "log", "log10", "lower", "ltrim", "max", "min", "node", "nodes", "percentileCont", "percentileDisc", "pi", "radians", "rand", "range", "reduce", "rel", "relationship", "relationships", "replace", "reverse", "right", "round", "rtrim", "shortestPath", "sign", "sin", "size", "split", "sqrt", "startnode", "stdev", "stdevp", "str", "substring", "sum", "tail", "tan", "timestamp", "toFloat", "toInt", "toString", "trim", "type", "upper"]);
var preds = wordRegexp(["all", "and", "any", "contains", "exists", "has", "in", "none", "not", "or", "single", "xor"]);
var keywords = wordRegexp(["as", "asc", "ascending", "assert", "by", "case", "commit", "constraint", "create", "csv", "cypher", "delete", "desc", "descending", "detach", "distinct", "drop", "else", "end", "ends", "explain", "false", "fieldterminator", "foreach", "from", "headers", "in", "index", "is", "join", "limit", "load", "match", "merge", "null", "on", "optional", "order", "periodic", "profile", "remove", "return", "scan", "set", "skip", "start", "starts", "then", "true", "union", "unique", "unwind", "using", "when", "where", "with", "call", "yield"]);
var systemKeywords = wordRegexp(["access", "active", "assign", "all", "alter", "as", "catalog", "change", "copy", "create", "constraint", "constraints", "current", "database", "databases", "dbms", "default", "deny", "drop", "element", "elements", "exists", "from", "grant", "graph", "graphs", "if", "index", "indexes", "label", "labels", "management", "match", "name", "names", "new", "node", "nodes", "not", "of", "on", "or", "password", "populated", "privileges", "property", "read", "relationship", "relationships", "remove", "replace", "required", "revoke", "role", "roles", "set", "show", "start", "status", "stop", "suspended", "to", "traverse", "type", "types", "user", "users", "with", "write"]);
var operatorChars = /[*+\-<>=&|~%^]/;
const cypher = {
  name: "cypher",
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
      if (state.context && state.context.align == null) {
        state.context.align = false;
      }
      state.indent = stream.indentation();
    }
    if (stream.eatSpace()) {
      return null;
    }
    var style = state.tokenize(stream, state);
    if (style !== "comment" && state.context && state.context.align == null && state.context.type !== "pattern") {
      state.context.align = true;
    }
    if (curPunc === "(") {
      pushContext(state, ")", stream.column());
    } else if (curPunc === "[") {
      pushContext(state, "]", stream.column());
    } else if (curPunc === "{") {
      pushContext(state, "}", stream.column());
    } else if (/[\]\}\)]/.test(curPunc)) {
      while (state.context && state.context.type === "pattern") {
        popContext(state);
      }
      if (state.context && curPunc === state.context.type) {
        popContext(state);
      }
    } else if (curPunc === "." && state.context && state.context.type === "pattern") {
      popContext(state);
    } else if (/atom|string|variable/.test(style) && state.context) {
      if (/[\}\]]/.test(state.context.type)) {
        pushContext(state, "pattern", stream.column());
      } else if (state.context.type === "pattern" && !state.context.align) {
        state.context.align = true;
        state.context.col = stream.column();
      }
    }
    return style;
  },
  indent: function (state, textAfter, cx) {
    var firstChar = textAfter && textAfter.charAt(0);
    var context = state.context;
    if (/[\]\}]/.test(firstChar)) {
      while (context && context.type === "pattern") {
        context = context.prev;
      }
    }
    var closing = context && firstChar === context.type;
    if (!context) return 0;
    if (context.type === "keywords") return null;
    if (context.align) return context.col + (closing ? 0 : 1);
    return context.indent + (closing ? 0 : cx.unit);
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiODI2My5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL0Bjb2RlbWlycm9yL2xlZ2FjeS1tb2Rlcy9tb2RlL2N5cGhlci5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyJ2YXIgd29yZFJlZ2V4cCA9IGZ1bmN0aW9uICh3b3Jkcykge1xuICByZXR1cm4gbmV3IFJlZ0V4cChcIl4oPzpcIiArIHdvcmRzLmpvaW4oXCJ8XCIpICsgXCIpJFwiLCBcImlcIik7XG59O1xudmFyIHRva2VuQmFzZSA9IGZ1bmN0aW9uIChzdHJlYW0gLyosIHN0YXRlKi8pIHtcbiAgY3VyUHVuYyA9IG51bGw7XG4gIHZhciBjaCA9IHN0cmVhbS5uZXh0KCk7XG4gIGlmIChjaCA9PT0gJ1wiJykge1xuICAgIHN0cmVhbS5tYXRjaCgvXi4qP1wiLyk7XG4gICAgcmV0dXJuIFwic3RyaW5nXCI7XG4gIH1cbiAgaWYgKGNoID09PSBcIidcIikge1xuICAgIHN0cmVhbS5tYXRjaCgvXi4qPycvKTtcbiAgICByZXR1cm4gXCJzdHJpbmdcIjtcbiAgfVxuICBpZiAoL1t7fVxcKFxcKSxcXC47XFxbXFxdXS8udGVzdChjaCkpIHtcbiAgICBjdXJQdW5jID0gY2g7XG4gICAgcmV0dXJuIFwicHVuY3R1YXRpb25cIjtcbiAgfSBlbHNlIGlmIChjaCA9PT0gXCIvXCIgJiYgc3RyZWFtLmVhdChcIi9cIikpIHtcbiAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICB9IGVsc2UgaWYgKG9wZXJhdG9yQ2hhcnMudGVzdChjaCkpIHtcbiAgICBzdHJlYW0uZWF0V2hpbGUob3BlcmF0b3JDaGFycyk7XG4gICAgcmV0dXJuIG51bGw7XG4gIH0gZWxzZSB7XG4gICAgc3RyZWFtLmVhdFdoaWxlKC9bX1xcd1xcZF0vKTtcbiAgICBpZiAoc3RyZWFtLmVhdChcIjpcIikpIHtcbiAgICAgIHN0cmVhbS5lYXRXaGlsZSgvW1xcd1xcZF9cXC1dLyk7XG4gICAgICByZXR1cm4gXCJhdG9tXCI7XG4gICAgfVxuICAgIHZhciB3b3JkID0gc3RyZWFtLmN1cnJlbnQoKTtcbiAgICBpZiAoZnVuY3MudGVzdCh3b3JkKSkgcmV0dXJuIFwiYnVpbHRpblwiO1xuICAgIGlmIChwcmVkcy50ZXN0KHdvcmQpKSByZXR1cm4gXCJkZWZcIjtcbiAgICBpZiAoa2V5d29yZHMudGVzdCh3b3JkKSB8fCBzeXN0ZW1LZXl3b3Jkcy50ZXN0KHdvcmQpKSByZXR1cm4gXCJrZXl3b3JkXCI7XG4gICAgcmV0dXJuIFwidmFyaWFibGVcIjtcbiAgfVxufTtcbnZhciBwdXNoQ29udGV4dCA9IGZ1bmN0aW9uIChzdGF0ZSwgdHlwZSwgY29sKSB7XG4gIHJldHVybiBzdGF0ZS5jb250ZXh0ID0ge1xuICAgIHByZXY6IHN0YXRlLmNvbnRleHQsXG4gICAgaW5kZW50OiBzdGF0ZS5pbmRlbnQsXG4gICAgY29sOiBjb2wsXG4gICAgdHlwZTogdHlwZVxuICB9O1xufTtcbnZhciBwb3BDb250ZXh0ID0gZnVuY3Rpb24gKHN0YXRlKSB7XG4gIHN0YXRlLmluZGVudCA9IHN0YXRlLmNvbnRleHQuaW5kZW50O1xuICByZXR1cm4gc3RhdGUuY29udGV4dCA9IHN0YXRlLmNvbnRleHQucHJldjtcbn07XG52YXIgY3VyUHVuYztcbnZhciBmdW5jcyA9IHdvcmRSZWdleHAoW1wiYWJzXCIsIFwiYWNvc1wiLCBcImFsbFNob3J0ZXN0UGF0aHNcIiwgXCJhc2luXCIsIFwiYXRhblwiLCBcImF0YW4yXCIsIFwiYXZnXCIsIFwiY2VpbFwiLCBcImNvYWxlc2NlXCIsIFwiY29sbGVjdFwiLCBcImNvc1wiLCBcImNvdFwiLCBcImNvdW50XCIsIFwiZGVncmVlc1wiLCBcImVcIiwgXCJlbmRub2RlXCIsIFwiZXhwXCIsIFwiZXh0cmFjdFwiLCBcImZpbHRlclwiLCBcImZsb29yXCIsIFwiaGF2ZXJzaW5cIiwgXCJoZWFkXCIsIFwiaWRcIiwgXCJrZXlzXCIsIFwibGFiZWxzXCIsIFwibGFzdFwiLCBcImxlZnRcIiwgXCJsZW5ndGhcIiwgXCJsb2dcIiwgXCJsb2cxMFwiLCBcImxvd2VyXCIsIFwibHRyaW1cIiwgXCJtYXhcIiwgXCJtaW5cIiwgXCJub2RlXCIsIFwibm9kZXNcIiwgXCJwZXJjZW50aWxlQ29udFwiLCBcInBlcmNlbnRpbGVEaXNjXCIsIFwicGlcIiwgXCJyYWRpYW5zXCIsIFwicmFuZFwiLCBcInJhbmdlXCIsIFwicmVkdWNlXCIsIFwicmVsXCIsIFwicmVsYXRpb25zaGlwXCIsIFwicmVsYXRpb25zaGlwc1wiLCBcInJlcGxhY2VcIiwgXCJyZXZlcnNlXCIsIFwicmlnaHRcIiwgXCJyb3VuZFwiLCBcInJ0cmltXCIsIFwic2hvcnRlc3RQYXRoXCIsIFwic2lnblwiLCBcInNpblwiLCBcInNpemVcIiwgXCJzcGxpdFwiLCBcInNxcnRcIiwgXCJzdGFydG5vZGVcIiwgXCJzdGRldlwiLCBcInN0ZGV2cFwiLCBcInN0clwiLCBcInN1YnN0cmluZ1wiLCBcInN1bVwiLCBcInRhaWxcIiwgXCJ0YW5cIiwgXCJ0aW1lc3RhbXBcIiwgXCJ0b0Zsb2F0XCIsIFwidG9JbnRcIiwgXCJ0b1N0cmluZ1wiLCBcInRyaW1cIiwgXCJ0eXBlXCIsIFwidXBwZXJcIl0pO1xudmFyIHByZWRzID0gd29yZFJlZ2V4cChbXCJhbGxcIiwgXCJhbmRcIiwgXCJhbnlcIiwgXCJjb250YWluc1wiLCBcImV4aXN0c1wiLCBcImhhc1wiLCBcImluXCIsIFwibm9uZVwiLCBcIm5vdFwiLCBcIm9yXCIsIFwic2luZ2xlXCIsIFwieG9yXCJdKTtcbnZhciBrZXl3b3JkcyA9IHdvcmRSZWdleHAoW1wiYXNcIiwgXCJhc2NcIiwgXCJhc2NlbmRpbmdcIiwgXCJhc3NlcnRcIiwgXCJieVwiLCBcImNhc2VcIiwgXCJjb21taXRcIiwgXCJjb25zdHJhaW50XCIsIFwiY3JlYXRlXCIsIFwiY3N2XCIsIFwiY3lwaGVyXCIsIFwiZGVsZXRlXCIsIFwiZGVzY1wiLCBcImRlc2NlbmRpbmdcIiwgXCJkZXRhY2hcIiwgXCJkaXN0aW5jdFwiLCBcImRyb3BcIiwgXCJlbHNlXCIsIFwiZW5kXCIsIFwiZW5kc1wiLCBcImV4cGxhaW5cIiwgXCJmYWxzZVwiLCBcImZpZWxkdGVybWluYXRvclwiLCBcImZvcmVhY2hcIiwgXCJmcm9tXCIsIFwiaGVhZGVyc1wiLCBcImluXCIsIFwiaW5kZXhcIiwgXCJpc1wiLCBcImpvaW5cIiwgXCJsaW1pdFwiLCBcImxvYWRcIiwgXCJtYXRjaFwiLCBcIm1lcmdlXCIsIFwibnVsbFwiLCBcIm9uXCIsIFwib3B0aW9uYWxcIiwgXCJvcmRlclwiLCBcInBlcmlvZGljXCIsIFwicHJvZmlsZVwiLCBcInJlbW92ZVwiLCBcInJldHVyblwiLCBcInNjYW5cIiwgXCJzZXRcIiwgXCJza2lwXCIsIFwic3RhcnRcIiwgXCJzdGFydHNcIiwgXCJ0aGVuXCIsIFwidHJ1ZVwiLCBcInVuaW9uXCIsIFwidW5pcXVlXCIsIFwidW53aW5kXCIsIFwidXNpbmdcIiwgXCJ3aGVuXCIsIFwid2hlcmVcIiwgXCJ3aXRoXCIsIFwiY2FsbFwiLCBcInlpZWxkXCJdKTtcbnZhciBzeXN0ZW1LZXl3b3JkcyA9IHdvcmRSZWdleHAoW1wiYWNjZXNzXCIsIFwiYWN0aXZlXCIsIFwiYXNzaWduXCIsIFwiYWxsXCIsIFwiYWx0ZXJcIiwgXCJhc1wiLCBcImNhdGFsb2dcIiwgXCJjaGFuZ2VcIiwgXCJjb3B5XCIsIFwiY3JlYXRlXCIsIFwiY29uc3RyYWludFwiLCBcImNvbnN0cmFpbnRzXCIsIFwiY3VycmVudFwiLCBcImRhdGFiYXNlXCIsIFwiZGF0YWJhc2VzXCIsIFwiZGJtc1wiLCBcImRlZmF1bHRcIiwgXCJkZW55XCIsIFwiZHJvcFwiLCBcImVsZW1lbnRcIiwgXCJlbGVtZW50c1wiLCBcImV4aXN0c1wiLCBcImZyb21cIiwgXCJncmFudFwiLCBcImdyYXBoXCIsIFwiZ3JhcGhzXCIsIFwiaWZcIiwgXCJpbmRleFwiLCBcImluZGV4ZXNcIiwgXCJsYWJlbFwiLCBcImxhYmVsc1wiLCBcIm1hbmFnZW1lbnRcIiwgXCJtYXRjaFwiLCBcIm5hbWVcIiwgXCJuYW1lc1wiLCBcIm5ld1wiLCBcIm5vZGVcIiwgXCJub2Rlc1wiLCBcIm5vdFwiLCBcIm9mXCIsIFwib25cIiwgXCJvclwiLCBcInBhc3N3b3JkXCIsIFwicG9wdWxhdGVkXCIsIFwicHJpdmlsZWdlc1wiLCBcInByb3BlcnR5XCIsIFwicmVhZFwiLCBcInJlbGF0aW9uc2hpcFwiLCBcInJlbGF0aW9uc2hpcHNcIiwgXCJyZW1vdmVcIiwgXCJyZXBsYWNlXCIsIFwicmVxdWlyZWRcIiwgXCJyZXZva2VcIiwgXCJyb2xlXCIsIFwicm9sZXNcIiwgXCJzZXRcIiwgXCJzaG93XCIsIFwic3RhcnRcIiwgXCJzdGF0dXNcIiwgXCJzdG9wXCIsIFwic3VzcGVuZGVkXCIsIFwidG9cIiwgXCJ0cmF2ZXJzZVwiLCBcInR5cGVcIiwgXCJ0eXBlc1wiLCBcInVzZXJcIiwgXCJ1c2Vyc1wiLCBcIndpdGhcIiwgXCJ3cml0ZVwiXSk7XG52YXIgb3BlcmF0b3JDaGFycyA9IC9bKitcXC08Pj0mfH4lXl0vO1xuZXhwb3J0IGNvbnN0IGN5cGhlciA9IHtcbiAgbmFtZTogXCJjeXBoZXJcIixcbiAgc3RhcnRTdGF0ZTogZnVuY3Rpb24gKCkge1xuICAgIHJldHVybiB7XG4gICAgICB0b2tlbml6ZTogdG9rZW5CYXNlLFxuICAgICAgY29udGV4dDogbnVsbCxcbiAgICAgIGluZGVudDogMCxcbiAgICAgIGNvbDogMFxuICAgIH07XG4gIH0sXG4gIHRva2VuOiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIGlmIChzdHJlYW0uc29sKCkpIHtcbiAgICAgIGlmIChzdGF0ZS5jb250ZXh0ICYmIHN0YXRlLmNvbnRleHQuYWxpZ24gPT0gbnVsbCkge1xuICAgICAgICBzdGF0ZS5jb250ZXh0LmFsaWduID0gZmFsc2U7XG4gICAgICB9XG4gICAgICBzdGF0ZS5pbmRlbnQgPSBzdHJlYW0uaW5kZW50YXRpb24oKTtcbiAgICB9XG4gICAgaWYgKHN0cmVhbS5lYXRTcGFjZSgpKSB7XG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9XG4gICAgdmFyIHN0eWxlID0gc3RhdGUudG9rZW5pemUoc3RyZWFtLCBzdGF0ZSk7XG4gICAgaWYgKHN0eWxlICE9PSBcImNvbW1lbnRcIiAmJiBzdGF0ZS5jb250ZXh0ICYmIHN0YXRlLmNvbnRleHQuYWxpZ24gPT0gbnVsbCAmJiBzdGF0ZS5jb250ZXh0LnR5cGUgIT09IFwicGF0dGVyblwiKSB7XG4gICAgICBzdGF0ZS5jb250ZXh0LmFsaWduID0gdHJ1ZTtcbiAgICB9XG4gICAgaWYgKGN1clB1bmMgPT09IFwiKFwiKSB7XG4gICAgICBwdXNoQ29udGV4dChzdGF0ZSwgXCIpXCIsIHN0cmVhbS5jb2x1bW4oKSk7XG4gICAgfSBlbHNlIGlmIChjdXJQdW5jID09PSBcIltcIikge1xuICAgICAgcHVzaENvbnRleHQoc3RhdGUsIFwiXVwiLCBzdHJlYW0uY29sdW1uKCkpO1xuICAgIH0gZWxzZSBpZiAoY3VyUHVuYyA9PT0gXCJ7XCIpIHtcbiAgICAgIHB1c2hDb250ZXh0KHN0YXRlLCBcIn1cIiwgc3RyZWFtLmNvbHVtbigpKTtcbiAgICB9IGVsc2UgaWYgKC9bXFxdXFx9XFwpXS8udGVzdChjdXJQdW5jKSkge1xuICAgICAgd2hpbGUgKHN0YXRlLmNvbnRleHQgJiYgc3RhdGUuY29udGV4dC50eXBlID09PSBcInBhdHRlcm5cIikge1xuICAgICAgICBwb3BDb250ZXh0KHN0YXRlKTtcbiAgICAgIH1cbiAgICAgIGlmIChzdGF0ZS5jb250ZXh0ICYmIGN1clB1bmMgPT09IHN0YXRlLmNvbnRleHQudHlwZSkge1xuICAgICAgICBwb3BDb250ZXh0KHN0YXRlKTtcbiAgICAgIH1cbiAgICB9IGVsc2UgaWYgKGN1clB1bmMgPT09IFwiLlwiICYmIHN0YXRlLmNvbnRleHQgJiYgc3RhdGUuY29udGV4dC50eXBlID09PSBcInBhdHRlcm5cIikge1xuICAgICAgcG9wQ29udGV4dChzdGF0ZSk7XG4gICAgfSBlbHNlIGlmICgvYXRvbXxzdHJpbmd8dmFyaWFibGUvLnRlc3Qoc3R5bGUpICYmIHN0YXRlLmNvbnRleHQpIHtcbiAgICAgIGlmICgvW1xcfVxcXV0vLnRlc3Qoc3RhdGUuY29udGV4dC50eXBlKSkge1xuICAgICAgICBwdXNoQ29udGV4dChzdGF0ZSwgXCJwYXR0ZXJuXCIsIHN0cmVhbS5jb2x1bW4oKSk7XG4gICAgICB9IGVsc2UgaWYgKHN0YXRlLmNvbnRleHQudHlwZSA9PT0gXCJwYXR0ZXJuXCIgJiYgIXN0YXRlLmNvbnRleHQuYWxpZ24pIHtcbiAgICAgICAgc3RhdGUuY29udGV4dC5hbGlnbiA9IHRydWU7XG4gICAgICAgIHN0YXRlLmNvbnRleHQuY29sID0gc3RyZWFtLmNvbHVtbigpO1xuICAgICAgfVxuICAgIH1cbiAgICByZXR1cm4gc3R5bGU7XG4gIH0sXG4gIGluZGVudDogZnVuY3Rpb24gKHN0YXRlLCB0ZXh0QWZ0ZXIsIGN4KSB7XG4gICAgdmFyIGZpcnN0Q2hhciA9IHRleHRBZnRlciAmJiB0ZXh0QWZ0ZXIuY2hhckF0KDApO1xuICAgIHZhciBjb250ZXh0ID0gc3RhdGUuY29udGV4dDtcbiAgICBpZiAoL1tcXF1cXH1dLy50ZXN0KGZpcnN0Q2hhcikpIHtcbiAgICAgIHdoaWxlIChjb250ZXh0ICYmIGNvbnRleHQudHlwZSA9PT0gXCJwYXR0ZXJuXCIpIHtcbiAgICAgICAgY29udGV4dCA9IGNvbnRleHQucHJldjtcbiAgICAgIH1cbiAgICB9XG4gICAgdmFyIGNsb3NpbmcgPSBjb250ZXh0ICYmIGZpcnN0Q2hhciA9PT0gY29udGV4dC50eXBlO1xuICAgIGlmICghY29udGV4dCkgcmV0dXJuIDA7XG4gICAgaWYgKGNvbnRleHQudHlwZSA9PT0gXCJrZXl3b3Jkc1wiKSByZXR1cm4gbnVsbDtcbiAgICBpZiAoY29udGV4dC5hbGlnbikgcmV0dXJuIGNvbnRleHQuY29sICsgKGNsb3NpbmcgPyAwIDogMSk7XG4gICAgcmV0dXJuIGNvbnRleHQuaW5kZW50ICsgKGNsb3NpbmcgPyAwIDogY3gudW5pdCk7XG4gIH1cbn07Il0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9