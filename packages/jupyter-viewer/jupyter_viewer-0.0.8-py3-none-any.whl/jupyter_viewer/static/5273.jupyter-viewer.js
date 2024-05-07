"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[5273],{

/***/ 55273:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "go": () => (/* binding */ go)
/* harmony export */ });
var keywords = {
  "break": true,
  "case": true,
  "chan": true,
  "const": true,
  "continue": true,
  "default": true,
  "defer": true,
  "else": true,
  "fallthrough": true,
  "for": true,
  "func": true,
  "go": true,
  "goto": true,
  "if": true,
  "import": true,
  "interface": true,
  "map": true,
  "package": true,
  "range": true,
  "return": true,
  "select": true,
  "struct": true,
  "switch": true,
  "type": true,
  "var": true,
  "bool": true,
  "byte": true,
  "complex64": true,
  "complex128": true,
  "float32": true,
  "float64": true,
  "int8": true,
  "int16": true,
  "int32": true,
  "int64": true,
  "string": true,
  "uint8": true,
  "uint16": true,
  "uint32": true,
  "uint64": true,
  "int": true,
  "uint": true,
  "uintptr": true,
  "error": true,
  "rune": true,
  "any": true,
  "comparable": true
};
var atoms = {
  "true": true,
  "false": true,
  "iota": true,
  "nil": true,
  "append": true,
  "cap": true,
  "close": true,
  "complex": true,
  "copy": true,
  "delete": true,
  "imag": true,
  "len": true,
  "make": true,
  "new": true,
  "panic": true,
  "print": true,
  "println": true,
  "real": true,
  "recover": true
};
var isOperatorChar = /[+\-*&^%:=<>!|\/]/;
var curPunc;
function tokenBase(stream, state) {
  var ch = stream.next();
  if (ch == '"' || ch == "'" || ch == "`") {
    state.tokenize = tokenString(ch);
    return state.tokenize(stream, state);
  }
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
  if (/[\[\]{}\(\),;\:\.]/.test(ch)) {
    curPunc = ch;
    return null;
  }
  if (ch == "/") {
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
  var cur = stream.current();
  if (keywords.propertyIsEnumerable(cur)) {
    if (cur == "case" || cur == "default") curPunc = "case";
    return "keyword";
  }
  if (atoms.propertyIsEnumerable(cur)) return "atom";
  return "variable";
}
function tokenString(quote) {
  return function (stream, state) {
    var escaped = false,
      next,
      end = false;
    while ((next = stream.next()) != null) {
      if (next == quote && !escaped) {
        end = true;
        break;
      }
      escaped = !escaped && quote != "`" && next == "\\";
    }
    if (end || !(escaped || quote == "`")) state.tokenize = tokenBase;
    return "string";
  };
}
function tokenComment(stream, state) {
  var maybeEnd = false,
    ch;
  while (ch = stream.next()) {
    if (ch == "/" && maybeEnd) {
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
  if (t == ")" || t == "]" || t == "}") state.indented = state.context.indented;
  return state.context = state.context.prev;
}

// Interface

const go = {
  name: "go",
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
      if (ctx.type == "case") ctx.type = "}";
    }
    if (stream.eatSpace()) return null;
    curPunc = null;
    var style = (state.tokenize || tokenBase)(stream, state);
    if (style == "comment") return style;
    if (ctx.align == null) ctx.align = true;
    if (curPunc == "{") pushContext(state, stream.column(), "}");else if (curPunc == "[") pushContext(state, stream.column(), "]");else if (curPunc == "(") pushContext(state, stream.column(), ")");else if (curPunc == "case") ctx.type = "case";else if (curPunc == "}" && ctx.type == "}") popContext(state);else if (curPunc == ctx.type) popContext(state);
    state.startOfLine = false;
    return style;
  },
  indent: function (state, textAfter, cx) {
    if (state.tokenize != tokenBase && state.tokenize != null) return null;
    var ctx = state.context,
      firstChar = textAfter && textAfter.charAt(0);
    if (ctx.type == "case" && /^(?:case|default)\b/.test(textAfter)) return ctx.indented;
    var closing = firstChar == ctx.type;
    if (ctx.align) return ctx.column + (closing ? 0 : 1);else return ctx.indented + (closing ? 0 : cx.unit);
  },
  languageData: {
    indentOnInput: /^\s([{}]|case |default\s*:)$/,
    commentTokens: {
      line: "//",
      block: {
        open: "/*",
        close: "*/"
      }
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNTI3My5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL0Bjb2RlbWlycm9yL2xlZ2FjeS1tb2Rlcy9tb2RlL2dvLmpzIl0sInNvdXJjZXNDb250ZW50IjpbInZhciBrZXl3b3JkcyA9IHtcbiAgXCJicmVha1wiOiB0cnVlLFxuICBcImNhc2VcIjogdHJ1ZSxcbiAgXCJjaGFuXCI6IHRydWUsXG4gIFwiY29uc3RcIjogdHJ1ZSxcbiAgXCJjb250aW51ZVwiOiB0cnVlLFxuICBcImRlZmF1bHRcIjogdHJ1ZSxcbiAgXCJkZWZlclwiOiB0cnVlLFxuICBcImVsc2VcIjogdHJ1ZSxcbiAgXCJmYWxsdGhyb3VnaFwiOiB0cnVlLFxuICBcImZvclwiOiB0cnVlLFxuICBcImZ1bmNcIjogdHJ1ZSxcbiAgXCJnb1wiOiB0cnVlLFxuICBcImdvdG9cIjogdHJ1ZSxcbiAgXCJpZlwiOiB0cnVlLFxuICBcImltcG9ydFwiOiB0cnVlLFxuICBcImludGVyZmFjZVwiOiB0cnVlLFxuICBcIm1hcFwiOiB0cnVlLFxuICBcInBhY2thZ2VcIjogdHJ1ZSxcbiAgXCJyYW5nZVwiOiB0cnVlLFxuICBcInJldHVyblwiOiB0cnVlLFxuICBcInNlbGVjdFwiOiB0cnVlLFxuICBcInN0cnVjdFwiOiB0cnVlLFxuICBcInN3aXRjaFwiOiB0cnVlLFxuICBcInR5cGVcIjogdHJ1ZSxcbiAgXCJ2YXJcIjogdHJ1ZSxcbiAgXCJib29sXCI6IHRydWUsXG4gIFwiYnl0ZVwiOiB0cnVlLFxuICBcImNvbXBsZXg2NFwiOiB0cnVlLFxuICBcImNvbXBsZXgxMjhcIjogdHJ1ZSxcbiAgXCJmbG9hdDMyXCI6IHRydWUsXG4gIFwiZmxvYXQ2NFwiOiB0cnVlLFxuICBcImludDhcIjogdHJ1ZSxcbiAgXCJpbnQxNlwiOiB0cnVlLFxuICBcImludDMyXCI6IHRydWUsXG4gIFwiaW50NjRcIjogdHJ1ZSxcbiAgXCJzdHJpbmdcIjogdHJ1ZSxcbiAgXCJ1aW50OFwiOiB0cnVlLFxuICBcInVpbnQxNlwiOiB0cnVlLFxuICBcInVpbnQzMlwiOiB0cnVlLFxuICBcInVpbnQ2NFwiOiB0cnVlLFxuICBcImludFwiOiB0cnVlLFxuICBcInVpbnRcIjogdHJ1ZSxcbiAgXCJ1aW50cHRyXCI6IHRydWUsXG4gIFwiZXJyb3JcIjogdHJ1ZSxcbiAgXCJydW5lXCI6IHRydWUsXG4gIFwiYW55XCI6IHRydWUsXG4gIFwiY29tcGFyYWJsZVwiOiB0cnVlXG59O1xudmFyIGF0b21zID0ge1xuICBcInRydWVcIjogdHJ1ZSxcbiAgXCJmYWxzZVwiOiB0cnVlLFxuICBcImlvdGFcIjogdHJ1ZSxcbiAgXCJuaWxcIjogdHJ1ZSxcbiAgXCJhcHBlbmRcIjogdHJ1ZSxcbiAgXCJjYXBcIjogdHJ1ZSxcbiAgXCJjbG9zZVwiOiB0cnVlLFxuICBcImNvbXBsZXhcIjogdHJ1ZSxcbiAgXCJjb3B5XCI6IHRydWUsXG4gIFwiZGVsZXRlXCI6IHRydWUsXG4gIFwiaW1hZ1wiOiB0cnVlLFxuICBcImxlblwiOiB0cnVlLFxuICBcIm1ha2VcIjogdHJ1ZSxcbiAgXCJuZXdcIjogdHJ1ZSxcbiAgXCJwYW5pY1wiOiB0cnVlLFxuICBcInByaW50XCI6IHRydWUsXG4gIFwicHJpbnRsblwiOiB0cnVlLFxuICBcInJlYWxcIjogdHJ1ZSxcbiAgXCJyZWNvdmVyXCI6IHRydWVcbn07XG52YXIgaXNPcGVyYXRvckNoYXIgPSAvWytcXC0qJl4lOj08PiF8XFwvXS87XG52YXIgY3VyUHVuYztcbmZ1bmN0aW9uIHRva2VuQmFzZShzdHJlYW0sIHN0YXRlKSB7XG4gIHZhciBjaCA9IHN0cmVhbS5uZXh0KCk7XG4gIGlmIChjaCA9PSAnXCInIHx8IGNoID09IFwiJ1wiIHx8IGNoID09IFwiYFwiKSB7XG4gICAgc3RhdGUudG9rZW5pemUgPSB0b2tlblN0cmluZyhjaCk7XG4gICAgcmV0dXJuIHN0YXRlLnRva2VuaXplKHN0cmVhbSwgc3RhdGUpO1xuICB9XG4gIGlmICgvW1xcZFxcLl0vLnRlc3QoY2gpKSB7XG4gICAgaWYgKGNoID09IFwiLlwiKSB7XG4gICAgICBzdHJlYW0ubWF0Y2goL15bMC05XSsoW2VFXVtcXC0rXT9bMC05XSspPy8pO1xuICAgIH0gZWxzZSBpZiAoY2ggPT0gXCIwXCIpIHtcbiAgICAgIHN0cmVhbS5tYXRjaCgvXlt4WF1bMC05YS1mQS1GXSsvKSB8fCBzdHJlYW0ubWF0Y2goL14wWzAtN10rLyk7XG4gICAgfSBlbHNlIHtcbiAgICAgIHN0cmVhbS5tYXRjaCgvXlswLTldKlxcLj9bMC05XSooW2VFXVtcXC0rXT9bMC05XSspPy8pO1xuICAgIH1cbiAgICByZXR1cm4gXCJudW1iZXJcIjtcbiAgfVxuICBpZiAoL1tcXFtcXF17fVxcKFxcKSw7XFw6XFwuXS8udGVzdChjaCkpIHtcbiAgICBjdXJQdW5jID0gY2g7XG4gICAgcmV0dXJuIG51bGw7XG4gIH1cbiAgaWYgKGNoID09IFwiL1wiKSB7XG4gICAgaWYgKHN0cmVhbS5lYXQoXCIqXCIpKSB7XG4gICAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQ29tbWVudDtcbiAgICAgIHJldHVybiB0b2tlbkNvbW1lbnQoc3RyZWFtLCBzdGF0ZSk7XG4gICAgfVxuICAgIGlmIChzdHJlYW0uZWF0KFwiL1wiKSkge1xuICAgICAgc3RyZWFtLnNraXBUb0VuZCgpO1xuICAgICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICAgIH1cbiAgfVxuICBpZiAoaXNPcGVyYXRvckNoYXIudGVzdChjaCkpIHtcbiAgICBzdHJlYW0uZWF0V2hpbGUoaXNPcGVyYXRvckNoYXIpO1xuICAgIHJldHVybiBcIm9wZXJhdG9yXCI7XG4gIH1cbiAgc3RyZWFtLmVhdFdoaWxlKC9bXFx3XFwkX1xceGExLVxcdWZmZmZdLyk7XG4gIHZhciBjdXIgPSBzdHJlYW0uY3VycmVudCgpO1xuICBpZiAoa2V5d29yZHMucHJvcGVydHlJc0VudW1lcmFibGUoY3VyKSkge1xuICAgIGlmIChjdXIgPT0gXCJjYXNlXCIgfHwgY3VyID09IFwiZGVmYXVsdFwiKSBjdXJQdW5jID0gXCJjYXNlXCI7XG4gICAgcmV0dXJuIFwia2V5d29yZFwiO1xuICB9XG4gIGlmIChhdG9tcy5wcm9wZXJ0eUlzRW51bWVyYWJsZShjdXIpKSByZXR1cm4gXCJhdG9tXCI7XG4gIHJldHVybiBcInZhcmlhYmxlXCI7XG59XG5mdW5jdGlvbiB0b2tlblN0cmluZyhxdW90ZSkge1xuICByZXR1cm4gZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICB2YXIgZXNjYXBlZCA9IGZhbHNlLFxuICAgICAgbmV4dCxcbiAgICAgIGVuZCA9IGZhbHNlO1xuICAgIHdoaWxlICgobmV4dCA9IHN0cmVhbS5uZXh0KCkpICE9IG51bGwpIHtcbiAgICAgIGlmIChuZXh0ID09IHF1b3RlICYmICFlc2NhcGVkKSB7XG4gICAgICAgIGVuZCA9IHRydWU7XG4gICAgICAgIGJyZWFrO1xuICAgICAgfVxuICAgICAgZXNjYXBlZCA9ICFlc2NhcGVkICYmIHF1b3RlICE9IFwiYFwiICYmIG5leHQgPT0gXCJcXFxcXCI7XG4gICAgfVxuICAgIGlmIChlbmQgfHwgIShlc2NhcGVkIHx8IHF1b3RlID09IFwiYFwiKSkgc3RhdGUudG9rZW5pemUgPSB0b2tlbkJhc2U7XG4gICAgcmV0dXJuIFwic3RyaW5nXCI7XG4gIH07XG59XG5mdW5jdGlvbiB0b2tlbkNvbW1lbnQoc3RyZWFtLCBzdGF0ZSkge1xuICB2YXIgbWF5YmVFbmQgPSBmYWxzZSxcbiAgICBjaDtcbiAgd2hpbGUgKGNoID0gc3RyZWFtLm5leHQoKSkge1xuICAgIGlmIChjaCA9PSBcIi9cIiAmJiBtYXliZUVuZCkge1xuICAgICAgc3RhdGUudG9rZW5pemUgPSB0b2tlbkJhc2U7XG4gICAgICBicmVhaztcbiAgICB9XG4gICAgbWF5YmVFbmQgPSBjaCA9PSBcIipcIjtcbiAgfVxuICByZXR1cm4gXCJjb21tZW50XCI7XG59XG5mdW5jdGlvbiBDb250ZXh0KGluZGVudGVkLCBjb2x1bW4sIHR5cGUsIGFsaWduLCBwcmV2KSB7XG4gIHRoaXMuaW5kZW50ZWQgPSBpbmRlbnRlZDtcbiAgdGhpcy5jb2x1bW4gPSBjb2x1bW47XG4gIHRoaXMudHlwZSA9IHR5cGU7XG4gIHRoaXMuYWxpZ24gPSBhbGlnbjtcbiAgdGhpcy5wcmV2ID0gcHJldjtcbn1cbmZ1bmN0aW9uIHB1c2hDb250ZXh0KHN0YXRlLCBjb2wsIHR5cGUpIHtcbiAgcmV0dXJuIHN0YXRlLmNvbnRleHQgPSBuZXcgQ29udGV4dChzdGF0ZS5pbmRlbnRlZCwgY29sLCB0eXBlLCBudWxsLCBzdGF0ZS5jb250ZXh0KTtcbn1cbmZ1bmN0aW9uIHBvcENvbnRleHQoc3RhdGUpIHtcbiAgaWYgKCFzdGF0ZS5jb250ZXh0LnByZXYpIHJldHVybjtcbiAgdmFyIHQgPSBzdGF0ZS5jb250ZXh0LnR5cGU7XG4gIGlmICh0ID09IFwiKVwiIHx8IHQgPT0gXCJdXCIgfHwgdCA9PSBcIn1cIikgc3RhdGUuaW5kZW50ZWQgPSBzdGF0ZS5jb250ZXh0LmluZGVudGVkO1xuICByZXR1cm4gc3RhdGUuY29udGV4dCA9IHN0YXRlLmNvbnRleHQucHJldjtcbn1cblxuLy8gSW50ZXJmYWNlXG5cbmV4cG9ydCBjb25zdCBnbyA9IHtcbiAgbmFtZTogXCJnb1wiLFxuICBzdGFydFN0YXRlOiBmdW5jdGlvbiAoaW5kZW50VW5pdCkge1xuICAgIHJldHVybiB7XG4gICAgICB0b2tlbml6ZTogbnVsbCxcbiAgICAgIGNvbnRleHQ6IG5ldyBDb250ZXh0KC1pbmRlbnRVbml0LCAwLCBcInRvcFwiLCBmYWxzZSksXG4gICAgICBpbmRlbnRlZDogMCxcbiAgICAgIHN0YXJ0T2ZMaW5lOiB0cnVlXG4gICAgfTtcbiAgfSxcbiAgdG9rZW46IGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgdmFyIGN0eCA9IHN0YXRlLmNvbnRleHQ7XG4gICAgaWYgKHN0cmVhbS5zb2woKSkge1xuICAgICAgaWYgKGN0eC5hbGlnbiA9PSBudWxsKSBjdHguYWxpZ24gPSBmYWxzZTtcbiAgICAgIHN0YXRlLmluZGVudGVkID0gc3RyZWFtLmluZGVudGF0aW9uKCk7XG4gICAgICBzdGF0ZS5zdGFydE9mTGluZSA9IHRydWU7XG4gICAgICBpZiAoY3R4LnR5cGUgPT0gXCJjYXNlXCIpIGN0eC50eXBlID0gXCJ9XCI7XG4gICAgfVxuICAgIGlmIChzdHJlYW0uZWF0U3BhY2UoKSkgcmV0dXJuIG51bGw7XG4gICAgY3VyUHVuYyA9IG51bGw7XG4gICAgdmFyIHN0eWxlID0gKHN0YXRlLnRva2VuaXplIHx8IHRva2VuQmFzZSkoc3RyZWFtLCBzdGF0ZSk7XG4gICAgaWYgKHN0eWxlID09IFwiY29tbWVudFwiKSByZXR1cm4gc3R5bGU7XG4gICAgaWYgKGN0eC5hbGlnbiA9PSBudWxsKSBjdHguYWxpZ24gPSB0cnVlO1xuICAgIGlmIChjdXJQdW5jID09IFwie1wiKSBwdXNoQ29udGV4dChzdGF0ZSwgc3RyZWFtLmNvbHVtbigpLCBcIn1cIik7ZWxzZSBpZiAoY3VyUHVuYyA9PSBcIltcIikgcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbS5jb2x1bW4oKSwgXCJdXCIpO2Vsc2UgaWYgKGN1clB1bmMgPT0gXCIoXCIpIHB1c2hDb250ZXh0KHN0YXRlLCBzdHJlYW0uY29sdW1uKCksIFwiKVwiKTtlbHNlIGlmIChjdXJQdW5jID09IFwiY2FzZVwiKSBjdHgudHlwZSA9IFwiY2FzZVwiO2Vsc2UgaWYgKGN1clB1bmMgPT0gXCJ9XCIgJiYgY3R4LnR5cGUgPT0gXCJ9XCIpIHBvcENvbnRleHQoc3RhdGUpO2Vsc2UgaWYgKGN1clB1bmMgPT0gY3R4LnR5cGUpIHBvcENvbnRleHQoc3RhdGUpO1xuICAgIHN0YXRlLnN0YXJ0T2ZMaW5lID0gZmFsc2U7XG4gICAgcmV0dXJuIHN0eWxlO1xuICB9LFxuICBpbmRlbnQ6IGZ1bmN0aW9uIChzdGF0ZSwgdGV4dEFmdGVyLCBjeCkge1xuICAgIGlmIChzdGF0ZS50b2tlbml6ZSAhPSB0b2tlbkJhc2UgJiYgc3RhdGUudG9rZW5pemUgIT0gbnVsbCkgcmV0dXJuIG51bGw7XG4gICAgdmFyIGN0eCA9IHN0YXRlLmNvbnRleHQsXG4gICAgICBmaXJzdENoYXIgPSB0ZXh0QWZ0ZXIgJiYgdGV4dEFmdGVyLmNoYXJBdCgwKTtcbiAgICBpZiAoY3R4LnR5cGUgPT0gXCJjYXNlXCIgJiYgL14oPzpjYXNlfGRlZmF1bHQpXFxiLy50ZXN0KHRleHRBZnRlcikpIHJldHVybiBjdHguaW5kZW50ZWQ7XG4gICAgdmFyIGNsb3NpbmcgPSBmaXJzdENoYXIgPT0gY3R4LnR5cGU7XG4gICAgaWYgKGN0eC5hbGlnbikgcmV0dXJuIGN0eC5jb2x1bW4gKyAoY2xvc2luZyA/IDAgOiAxKTtlbHNlIHJldHVybiBjdHguaW5kZW50ZWQgKyAoY2xvc2luZyA/IDAgOiBjeC51bml0KTtcbiAgfSxcbiAgbGFuZ3VhZ2VEYXRhOiB7XG4gICAgaW5kZW50T25JbnB1dDogL15cXHMoW3t9XXxjYXNlIHxkZWZhdWx0XFxzKjopJC8sXG4gICAgY29tbWVudFRva2Vuczoge1xuICAgICAgbGluZTogXCIvL1wiLFxuICAgICAgYmxvY2s6IHtcbiAgICAgICAgb3BlbjogXCIvKlwiLFxuICAgICAgICBjbG9zZTogXCIqL1wiXG4gICAgICB9XG4gICAgfVxuICB9XG59OyJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==