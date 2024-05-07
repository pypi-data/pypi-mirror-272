"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[577],{

/***/ 90577:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "groovy": () => (/* binding */ groovy)
/* harmony export */ });
function words(str) {
  var obj = {},
    words = str.split(" ");
  for (var i = 0; i < words.length; ++i) obj[words[i]] = true;
  return obj;
}
var keywords = words("abstract as assert boolean break byte case catch char class const continue def default " + "do double else enum extends final finally float for goto if implements import in " + "instanceof int interface long native new package private protected public return " + "short static strictfp super switch synchronized threadsafe throw throws trait transient " + "try void volatile while");
var blockKeywords = words("catch class def do else enum finally for if interface switch trait try while");
var standaloneKeywords = words("return break continue");
var atoms = words("null true false this");
var curPunc;
function tokenBase(stream, state) {
  var ch = stream.next();
  if (ch == '"' || ch == "'") {
    return startString(ch, stream, state);
  }
  if (/[\[\]{}\(\),;\:\.]/.test(ch)) {
    curPunc = ch;
    return null;
  }
  if (/\d/.test(ch)) {
    stream.eatWhile(/[\w\.]/);
    if (stream.eat(/eE/)) {
      stream.eat(/\+\-/);
      stream.eatWhile(/\d/);
    }
    return "number";
  }
  if (ch == "/") {
    if (stream.eat("*")) {
      state.tokenize.push(tokenComment);
      return tokenComment(stream, state);
    }
    if (stream.eat("/")) {
      stream.skipToEnd();
      return "comment";
    }
    if (expectExpression(state.lastToken, false)) {
      return startString(ch, stream, state);
    }
  }
  if (ch == "-" && stream.eat(">")) {
    curPunc = "->";
    return null;
  }
  if (/[+\-*&%=<>!?|\/~]/.test(ch)) {
    stream.eatWhile(/[+\-*&%=<>|~]/);
    return "operator";
  }
  stream.eatWhile(/[\w\$_]/);
  if (ch == "@") {
    stream.eatWhile(/[\w\$_\.]/);
    return "meta";
  }
  if (state.lastToken == ".") return "property";
  if (stream.eat(":")) {
    curPunc = "proplabel";
    return "property";
  }
  var cur = stream.current();
  if (atoms.propertyIsEnumerable(cur)) {
    return "atom";
  }
  if (keywords.propertyIsEnumerable(cur)) {
    if (blockKeywords.propertyIsEnumerable(cur)) curPunc = "newstatement";else if (standaloneKeywords.propertyIsEnumerable(cur)) curPunc = "standalone";
    return "keyword";
  }
  return "variable";
}
tokenBase.isBase = true;
function startString(quote, stream, state) {
  var tripleQuoted = false;
  if (quote != "/" && stream.eat(quote)) {
    if (stream.eat(quote)) tripleQuoted = true;else return "string";
  }
  function t(stream, state) {
    var escaped = false,
      next,
      end = !tripleQuoted;
    while ((next = stream.next()) != null) {
      if (next == quote && !escaped) {
        if (!tripleQuoted) {
          break;
        }
        if (stream.match(quote + quote)) {
          end = true;
          break;
        }
      }
      if (quote == '"' && next == "$" && !escaped) {
        if (stream.eat("{")) {
          state.tokenize.push(tokenBaseUntilBrace());
          return "string";
        } else if (stream.match(/^\w/, false)) {
          state.tokenize.push(tokenVariableDeref);
          return "string";
        }
      }
      escaped = !escaped && next == "\\";
    }
    if (end) state.tokenize.pop();
    return "string";
  }
  state.tokenize.push(t);
  return t(stream, state);
}
function tokenBaseUntilBrace() {
  var depth = 1;
  function t(stream, state) {
    if (stream.peek() == "}") {
      depth--;
      if (depth == 0) {
        state.tokenize.pop();
        return state.tokenize[state.tokenize.length - 1](stream, state);
      }
    } else if (stream.peek() == "{") {
      depth++;
    }
    return tokenBase(stream, state);
  }
  t.isBase = true;
  return t;
}
function tokenVariableDeref(stream, state) {
  var next = stream.match(/^(\.|[\w\$_]+)/);
  if (!next) {
    state.tokenize.pop();
    return state.tokenize[state.tokenize.length - 1](stream, state);
  }
  return next[0] == "." ? null : "variable";
}
function tokenComment(stream, state) {
  var maybeEnd = false,
    ch;
  while (ch = stream.next()) {
    if (ch == "/" && maybeEnd) {
      state.tokenize.pop();
      break;
    }
    maybeEnd = ch == "*";
  }
  return "comment";
}
function expectExpression(last, newline) {
  return !last || last == "operator" || last == "->" || /[\.\[\{\(,;:]/.test(last) || last == "newstatement" || last == "keyword" || last == "proplabel" || last == "standalone" && !newline;
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
  var t = state.context.type;
  if (t == ")" || t == "]" || t == "}") state.indented = state.context.indented;
  return state.context = state.context.prev;
}

// Interface

const groovy = {
  name: "groovy",
  startState: function (indentUnit) {
    return {
      tokenize: [tokenBase],
      context: new Context(-indentUnit, 0, "top", false),
      indented: 0,
      startOfLine: true,
      lastToken: null
    };
  },
  token: function (stream, state) {
    var ctx = state.context;
    if (stream.sol()) {
      if (ctx.align == null) ctx.align = false;
      state.indented = stream.indentation();
      state.startOfLine = true;
      // Automatic semicolon insertion
      if (ctx.type == "statement" && !expectExpression(state.lastToken, true)) {
        popContext(state);
        ctx = state.context;
      }
    }
    if (stream.eatSpace()) return null;
    curPunc = null;
    var style = state.tokenize[state.tokenize.length - 1](stream, state);
    if (style == "comment") return style;
    if (ctx.align == null) ctx.align = true;
    if ((curPunc == ";" || curPunc == ":") && ctx.type == "statement") popContext(state);
    // Handle indentation for {x -> \n ... }
    else if (curPunc == "->" && ctx.type == "statement" && ctx.prev.type == "}") {
      popContext(state);
      state.context.align = false;
    } else if (curPunc == "{") pushContext(state, stream.column(), "}");else if (curPunc == "[") pushContext(state, stream.column(), "]");else if (curPunc == "(") pushContext(state, stream.column(), ")");else if (curPunc == "}") {
      while (ctx.type == "statement") ctx = popContext(state);
      if (ctx.type == "}") ctx = popContext(state);
      while (ctx.type == "statement") ctx = popContext(state);
    } else if (curPunc == ctx.type) popContext(state);else if (ctx.type == "}" || ctx.type == "top" || ctx.type == "statement" && curPunc == "newstatement") pushContext(state, stream.column(), "statement");
    state.startOfLine = false;
    state.lastToken = curPunc || style;
    return style;
  },
  indent: function (state, textAfter, cx) {
    if (!state.tokenize[state.tokenize.length - 1].isBase) return null;
    var firstChar = textAfter && textAfter.charAt(0),
      ctx = state.context;
    if (ctx.type == "statement" && !expectExpression(state.lastToken, true)) ctx = ctx.prev;
    var closing = firstChar == ctx.type;
    if (ctx.type == "statement") return ctx.indented + (firstChar == "{" ? 0 : cx.unit);else if (ctx.align) return ctx.column + (closing ? 0 : 1);else return ctx.indented + (closing ? 0 : cx.unit);
  },
  languageData: {
    indentOnInput: /^\s*[{}]$/,
    commentTokens: {
      line: "//",
      block: {
        open: "/*",
        close: "*/"
      }
    },
    closeBrackets: {
      brackets: ["(", "[", "{", "'", '"', "'''", '"""']
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNTc3Lmp1cHl0ZXItdmlld2VyLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL0Bjb2RlbWlycm9yL2xlZ2FjeS1tb2Rlcy9tb2RlL2dyb292eS5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyJmdW5jdGlvbiB3b3JkcyhzdHIpIHtcbiAgdmFyIG9iaiA9IHt9LFxuICAgIHdvcmRzID0gc3RyLnNwbGl0KFwiIFwiKTtcbiAgZm9yICh2YXIgaSA9IDA7IGkgPCB3b3Jkcy5sZW5ndGg7ICsraSkgb2JqW3dvcmRzW2ldXSA9IHRydWU7XG4gIHJldHVybiBvYmo7XG59XG52YXIga2V5d29yZHMgPSB3b3JkcyhcImFic3RyYWN0IGFzIGFzc2VydCBib29sZWFuIGJyZWFrIGJ5dGUgY2FzZSBjYXRjaCBjaGFyIGNsYXNzIGNvbnN0IGNvbnRpbnVlIGRlZiBkZWZhdWx0IFwiICsgXCJkbyBkb3VibGUgZWxzZSBlbnVtIGV4dGVuZHMgZmluYWwgZmluYWxseSBmbG9hdCBmb3IgZ290byBpZiBpbXBsZW1lbnRzIGltcG9ydCBpbiBcIiArIFwiaW5zdGFuY2VvZiBpbnQgaW50ZXJmYWNlIGxvbmcgbmF0aXZlIG5ldyBwYWNrYWdlIHByaXZhdGUgcHJvdGVjdGVkIHB1YmxpYyByZXR1cm4gXCIgKyBcInNob3J0IHN0YXRpYyBzdHJpY3RmcCBzdXBlciBzd2l0Y2ggc3luY2hyb25pemVkIHRocmVhZHNhZmUgdGhyb3cgdGhyb3dzIHRyYWl0IHRyYW5zaWVudCBcIiArIFwidHJ5IHZvaWQgdm9sYXRpbGUgd2hpbGVcIik7XG52YXIgYmxvY2tLZXl3b3JkcyA9IHdvcmRzKFwiY2F0Y2ggY2xhc3MgZGVmIGRvIGVsc2UgZW51bSBmaW5hbGx5IGZvciBpZiBpbnRlcmZhY2Ugc3dpdGNoIHRyYWl0IHRyeSB3aGlsZVwiKTtcbnZhciBzdGFuZGFsb25lS2V5d29yZHMgPSB3b3JkcyhcInJldHVybiBicmVhayBjb250aW51ZVwiKTtcbnZhciBhdG9tcyA9IHdvcmRzKFwibnVsbCB0cnVlIGZhbHNlIHRoaXNcIik7XG52YXIgY3VyUHVuYztcbmZ1bmN0aW9uIHRva2VuQmFzZShzdHJlYW0sIHN0YXRlKSB7XG4gIHZhciBjaCA9IHN0cmVhbS5uZXh0KCk7XG4gIGlmIChjaCA9PSAnXCInIHx8IGNoID09IFwiJ1wiKSB7XG4gICAgcmV0dXJuIHN0YXJ0U3RyaW5nKGNoLCBzdHJlYW0sIHN0YXRlKTtcbiAgfVxuICBpZiAoL1tcXFtcXF17fVxcKFxcKSw7XFw6XFwuXS8udGVzdChjaCkpIHtcbiAgICBjdXJQdW5jID0gY2g7XG4gICAgcmV0dXJuIG51bGw7XG4gIH1cbiAgaWYgKC9cXGQvLnRlc3QoY2gpKSB7XG4gICAgc3RyZWFtLmVhdFdoaWxlKC9bXFx3XFwuXS8pO1xuICAgIGlmIChzdHJlYW0uZWF0KC9lRS8pKSB7XG4gICAgICBzdHJlYW0uZWF0KC9cXCtcXC0vKTtcbiAgICAgIHN0cmVhbS5lYXRXaGlsZSgvXFxkLyk7XG4gICAgfVxuICAgIHJldHVybiBcIm51bWJlclwiO1xuICB9XG4gIGlmIChjaCA9PSBcIi9cIikge1xuICAgIGlmIChzdHJlYW0uZWF0KFwiKlwiKSkge1xuICAgICAgc3RhdGUudG9rZW5pemUucHVzaCh0b2tlbkNvbW1lbnQpO1xuICAgICAgcmV0dXJuIHRva2VuQ29tbWVudChzdHJlYW0sIHN0YXRlKTtcbiAgICB9XG4gICAgaWYgKHN0cmVhbS5lYXQoXCIvXCIpKSB7XG4gICAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgICByZXR1cm4gXCJjb21tZW50XCI7XG4gICAgfVxuICAgIGlmIChleHBlY3RFeHByZXNzaW9uKHN0YXRlLmxhc3RUb2tlbiwgZmFsc2UpKSB7XG4gICAgICByZXR1cm4gc3RhcnRTdHJpbmcoY2gsIHN0cmVhbSwgc3RhdGUpO1xuICAgIH1cbiAgfVxuICBpZiAoY2ggPT0gXCItXCIgJiYgc3RyZWFtLmVhdChcIj5cIikpIHtcbiAgICBjdXJQdW5jID0gXCItPlwiO1xuICAgIHJldHVybiBudWxsO1xuICB9XG4gIGlmICgvWytcXC0qJiU9PD4hP3xcXC9+XS8udGVzdChjaCkpIHtcbiAgICBzdHJlYW0uZWF0V2hpbGUoL1srXFwtKiYlPTw+fH5dLyk7XG4gICAgcmV0dXJuIFwib3BlcmF0b3JcIjtcbiAgfVxuICBzdHJlYW0uZWF0V2hpbGUoL1tcXHdcXCRfXS8pO1xuICBpZiAoY2ggPT0gXCJAXCIpIHtcbiAgICBzdHJlYW0uZWF0V2hpbGUoL1tcXHdcXCRfXFwuXS8pO1xuICAgIHJldHVybiBcIm1ldGFcIjtcbiAgfVxuICBpZiAoc3RhdGUubGFzdFRva2VuID09IFwiLlwiKSByZXR1cm4gXCJwcm9wZXJ0eVwiO1xuICBpZiAoc3RyZWFtLmVhdChcIjpcIikpIHtcbiAgICBjdXJQdW5jID0gXCJwcm9wbGFiZWxcIjtcbiAgICByZXR1cm4gXCJwcm9wZXJ0eVwiO1xuICB9XG4gIHZhciBjdXIgPSBzdHJlYW0uY3VycmVudCgpO1xuICBpZiAoYXRvbXMucHJvcGVydHlJc0VudW1lcmFibGUoY3VyKSkge1xuICAgIHJldHVybiBcImF0b21cIjtcbiAgfVxuICBpZiAoa2V5d29yZHMucHJvcGVydHlJc0VudW1lcmFibGUoY3VyKSkge1xuICAgIGlmIChibG9ja0tleXdvcmRzLnByb3BlcnR5SXNFbnVtZXJhYmxlKGN1cikpIGN1clB1bmMgPSBcIm5ld3N0YXRlbWVudFwiO2Vsc2UgaWYgKHN0YW5kYWxvbmVLZXl3b3Jkcy5wcm9wZXJ0eUlzRW51bWVyYWJsZShjdXIpKSBjdXJQdW5jID0gXCJzdGFuZGFsb25lXCI7XG4gICAgcmV0dXJuIFwia2V5d29yZFwiO1xuICB9XG4gIHJldHVybiBcInZhcmlhYmxlXCI7XG59XG50b2tlbkJhc2UuaXNCYXNlID0gdHJ1ZTtcbmZ1bmN0aW9uIHN0YXJ0U3RyaW5nKHF1b3RlLCBzdHJlYW0sIHN0YXRlKSB7XG4gIHZhciB0cmlwbGVRdW90ZWQgPSBmYWxzZTtcbiAgaWYgKHF1b3RlICE9IFwiL1wiICYmIHN0cmVhbS5lYXQocXVvdGUpKSB7XG4gICAgaWYgKHN0cmVhbS5lYXQocXVvdGUpKSB0cmlwbGVRdW90ZWQgPSB0cnVlO2Vsc2UgcmV0dXJuIFwic3RyaW5nXCI7XG4gIH1cbiAgZnVuY3Rpb24gdChzdHJlYW0sIHN0YXRlKSB7XG4gICAgdmFyIGVzY2FwZWQgPSBmYWxzZSxcbiAgICAgIG5leHQsXG4gICAgICBlbmQgPSAhdHJpcGxlUXVvdGVkO1xuICAgIHdoaWxlICgobmV4dCA9IHN0cmVhbS5uZXh0KCkpICE9IG51bGwpIHtcbiAgICAgIGlmIChuZXh0ID09IHF1b3RlICYmICFlc2NhcGVkKSB7XG4gICAgICAgIGlmICghdHJpcGxlUXVvdGVkKSB7XG4gICAgICAgICAgYnJlYWs7XG4gICAgICAgIH1cbiAgICAgICAgaWYgKHN0cmVhbS5tYXRjaChxdW90ZSArIHF1b3RlKSkge1xuICAgICAgICAgIGVuZCA9IHRydWU7XG4gICAgICAgICAgYnJlYWs7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICAgIGlmIChxdW90ZSA9PSAnXCInICYmIG5leHQgPT0gXCIkXCIgJiYgIWVzY2FwZWQpIHtcbiAgICAgICAgaWYgKHN0cmVhbS5lYXQoXCJ7XCIpKSB7XG4gICAgICAgICAgc3RhdGUudG9rZW5pemUucHVzaCh0b2tlbkJhc2VVbnRpbEJyYWNlKCkpO1xuICAgICAgICAgIHJldHVybiBcInN0cmluZ1wiO1xuICAgICAgICB9IGVsc2UgaWYgKHN0cmVhbS5tYXRjaCgvXlxcdy8sIGZhbHNlKSkge1xuICAgICAgICAgIHN0YXRlLnRva2VuaXplLnB1c2godG9rZW5WYXJpYWJsZURlcmVmKTtcbiAgICAgICAgICByZXR1cm4gXCJzdHJpbmdcIjtcbiAgICAgICAgfVxuICAgICAgfVxuICAgICAgZXNjYXBlZCA9ICFlc2NhcGVkICYmIG5leHQgPT0gXCJcXFxcXCI7XG4gICAgfVxuICAgIGlmIChlbmQpIHN0YXRlLnRva2VuaXplLnBvcCgpO1xuICAgIHJldHVybiBcInN0cmluZ1wiO1xuICB9XG4gIHN0YXRlLnRva2VuaXplLnB1c2godCk7XG4gIHJldHVybiB0KHN0cmVhbSwgc3RhdGUpO1xufVxuZnVuY3Rpb24gdG9rZW5CYXNlVW50aWxCcmFjZSgpIHtcbiAgdmFyIGRlcHRoID0gMTtcbiAgZnVuY3Rpb24gdChzdHJlYW0sIHN0YXRlKSB7XG4gICAgaWYgKHN0cmVhbS5wZWVrKCkgPT0gXCJ9XCIpIHtcbiAgICAgIGRlcHRoLS07XG4gICAgICBpZiAoZGVwdGggPT0gMCkge1xuICAgICAgICBzdGF0ZS50b2tlbml6ZS5wb3AoKTtcbiAgICAgICAgcmV0dXJuIHN0YXRlLnRva2VuaXplW3N0YXRlLnRva2VuaXplLmxlbmd0aCAtIDFdKHN0cmVhbSwgc3RhdGUpO1xuICAgICAgfVxuICAgIH0gZWxzZSBpZiAoc3RyZWFtLnBlZWsoKSA9PSBcIntcIikge1xuICAgICAgZGVwdGgrKztcbiAgICB9XG4gICAgcmV0dXJuIHRva2VuQmFzZShzdHJlYW0sIHN0YXRlKTtcbiAgfVxuICB0LmlzQmFzZSA9IHRydWU7XG4gIHJldHVybiB0O1xufVxuZnVuY3Rpb24gdG9rZW5WYXJpYWJsZURlcmVmKHN0cmVhbSwgc3RhdGUpIHtcbiAgdmFyIG5leHQgPSBzdHJlYW0ubWF0Y2goL14oXFwufFtcXHdcXCRfXSspLyk7XG4gIGlmICghbmV4dCkge1xuICAgIHN0YXRlLnRva2VuaXplLnBvcCgpO1xuICAgIHJldHVybiBzdGF0ZS50b2tlbml6ZVtzdGF0ZS50b2tlbml6ZS5sZW5ndGggLSAxXShzdHJlYW0sIHN0YXRlKTtcbiAgfVxuICByZXR1cm4gbmV4dFswXSA9PSBcIi5cIiA/IG51bGwgOiBcInZhcmlhYmxlXCI7XG59XG5mdW5jdGlvbiB0b2tlbkNvbW1lbnQoc3RyZWFtLCBzdGF0ZSkge1xuICB2YXIgbWF5YmVFbmQgPSBmYWxzZSxcbiAgICBjaDtcbiAgd2hpbGUgKGNoID0gc3RyZWFtLm5leHQoKSkge1xuICAgIGlmIChjaCA9PSBcIi9cIiAmJiBtYXliZUVuZCkge1xuICAgICAgc3RhdGUudG9rZW5pemUucG9wKCk7XG4gICAgICBicmVhaztcbiAgICB9XG4gICAgbWF5YmVFbmQgPSBjaCA9PSBcIipcIjtcbiAgfVxuICByZXR1cm4gXCJjb21tZW50XCI7XG59XG5mdW5jdGlvbiBleHBlY3RFeHByZXNzaW9uKGxhc3QsIG5ld2xpbmUpIHtcbiAgcmV0dXJuICFsYXN0IHx8IGxhc3QgPT0gXCJvcGVyYXRvclwiIHx8IGxhc3QgPT0gXCItPlwiIHx8IC9bXFwuXFxbXFx7XFwoLDs6XS8udGVzdChsYXN0KSB8fCBsYXN0ID09IFwibmV3c3RhdGVtZW50XCIgfHwgbGFzdCA9PSBcImtleXdvcmRcIiB8fCBsYXN0ID09IFwicHJvcGxhYmVsXCIgfHwgbGFzdCA9PSBcInN0YW5kYWxvbmVcIiAmJiAhbmV3bGluZTtcbn1cbmZ1bmN0aW9uIENvbnRleHQoaW5kZW50ZWQsIGNvbHVtbiwgdHlwZSwgYWxpZ24sIHByZXYpIHtcbiAgdGhpcy5pbmRlbnRlZCA9IGluZGVudGVkO1xuICB0aGlzLmNvbHVtbiA9IGNvbHVtbjtcbiAgdGhpcy50eXBlID0gdHlwZTtcbiAgdGhpcy5hbGlnbiA9IGFsaWduO1xuICB0aGlzLnByZXYgPSBwcmV2O1xufVxuZnVuY3Rpb24gcHVzaENvbnRleHQoc3RhdGUsIGNvbCwgdHlwZSkge1xuICByZXR1cm4gc3RhdGUuY29udGV4dCA9IG5ldyBDb250ZXh0KHN0YXRlLmluZGVudGVkLCBjb2wsIHR5cGUsIG51bGwsIHN0YXRlLmNvbnRleHQpO1xufVxuZnVuY3Rpb24gcG9wQ29udGV4dChzdGF0ZSkge1xuICB2YXIgdCA9IHN0YXRlLmNvbnRleHQudHlwZTtcbiAgaWYgKHQgPT0gXCIpXCIgfHwgdCA9PSBcIl1cIiB8fCB0ID09IFwifVwiKSBzdGF0ZS5pbmRlbnRlZCA9IHN0YXRlLmNvbnRleHQuaW5kZW50ZWQ7XG4gIHJldHVybiBzdGF0ZS5jb250ZXh0ID0gc3RhdGUuY29udGV4dC5wcmV2O1xufVxuXG4vLyBJbnRlcmZhY2VcblxuZXhwb3J0IGNvbnN0IGdyb292eSA9IHtcbiAgbmFtZTogXCJncm9vdnlcIixcbiAgc3RhcnRTdGF0ZTogZnVuY3Rpb24gKGluZGVudFVuaXQpIHtcbiAgICByZXR1cm4ge1xuICAgICAgdG9rZW5pemU6IFt0b2tlbkJhc2VdLFxuICAgICAgY29udGV4dDogbmV3IENvbnRleHQoLWluZGVudFVuaXQsIDAsIFwidG9wXCIsIGZhbHNlKSxcbiAgICAgIGluZGVudGVkOiAwLFxuICAgICAgc3RhcnRPZkxpbmU6IHRydWUsXG4gICAgICBsYXN0VG9rZW46IG51bGxcbiAgICB9O1xuICB9LFxuICB0b2tlbjogZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICB2YXIgY3R4ID0gc3RhdGUuY29udGV4dDtcbiAgICBpZiAoc3RyZWFtLnNvbCgpKSB7XG4gICAgICBpZiAoY3R4LmFsaWduID09IG51bGwpIGN0eC5hbGlnbiA9IGZhbHNlO1xuICAgICAgc3RhdGUuaW5kZW50ZWQgPSBzdHJlYW0uaW5kZW50YXRpb24oKTtcbiAgICAgIHN0YXRlLnN0YXJ0T2ZMaW5lID0gdHJ1ZTtcbiAgICAgIC8vIEF1dG9tYXRpYyBzZW1pY29sb24gaW5zZXJ0aW9uXG4gICAgICBpZiAoY3R4LnR5cGUgPT0gXCJzdGF0ZW1lbnRcIiAmJiAhZXhwZWN0RXhwcmVzc2lvbihzdGF0ZS5sYXN0VG9rZW4sIHRydWUpKSB7XG4gICAgICAgIHBvcENvbnRleHQoc3RhdGUpO1xuICAgICAgICBjdHggPSBzdGF0ZS5jb250ZXh0O1xuICAgICAgfVxuICAgIH1cbiAgICBpZiAoc3RyZWFtLmVhdFNwYWNlKCkpIHJldHVybiBudWxsO1xuICAgIGN1clB1bmMgPSBudWxsO1xuICAgIHZhciBzdHlsZSA9IHN0YXRlLnRva2VuaXplW3N0YXRlLnRva2VuaXplLmxlbmd0aCAtIDFdKHN0cmVhbSwgc3RhdGUpO1xuICAgIGlmIChzdHlsZSA9PSBcImNvbW1lbnRcIikgcmV0dXJuIHN0eWxlO1xuICAgIGlmIChjdHguYWxpZ24gPT0gbnVsbCkgY3R4LmFsaWduID0gdHJ1ZTtcbiAgICBpZiAoKGN1clB1bmMgPT0gXCI7XCIgfHwgY3VyUHVuYyA9PSBcIjpcIikgJiYgY3R4LnR5cGUgPT0gXCJzdGF0ZW1lbnRcIikgcG9wQ29udGV4dChzdGF0ZSk7XG4gICAgLy8gSGFuZGxlIGluZGVudGF0aW9uIGZvciB7eCAtPiBcXG4gLi4uIH1cbiAgICBlbHNlIGlmIChjdXJQdW5jID09IFwiLT5cIiAmJiBjdHgudHlwZSA9PSBcInN0YXRlbWVudFwiICYmIGN0eC5wcmV2LnR5cGUgPT0gXCJ9XCIpIHtcbiAgICAgIHBvcENvbnRleHQoc3RhdGUpO1xuICAgICAgc3RhdGUuY29udGV4dC5hbGlnbiA9IGZhbHNlO1xuICAgIH0gZWxzZSBpZiAoY3VyUHVuYyA9PSBcIntcIikgcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbS5jb2x1bW4oKSwgXCJ9XCIpO2Vsc2UgaWYgKGN1clB1bmMgPT0gXCJbXCIpIHB1c2hDb250ZXh0KHN0YXRlLCBzdHJlYW0uY29sdW1uKCksIFwiXVwiKTtlbHNlIGlmIChjdXJQdW5jID09IFwiKFwiKSBwdXNoQ29udGV4dChzdGF0ZSwgc3RyZWFtLmNvbHVtbigpLCBcIilcIik7ZWxzZSBpZiAoY3VyUHVuYyA9PSBcIn1cIikge1xuICAgICAgd2hpbGUgKGN0eC50eXBlID09IFwic3RhdGVtZW50XCIpIGN0eCA9IHBvcENvbnRleHQoc3RhdGUpO1xuICAgICAgaWYgKGN0eC50eXBlID09IFwifVwiKSBjdHggPSBwb3BDb250ZXh0KHN0YXRlKTtcbiAgICAgIHdoaWxlIChjdHgudHlwZSA9PSBcInN0YXRlbWVudFwiKSBjdHggPSBwb3BDb250ZXh0KHN0YXRlKTtcbiAgICB9IGVsc2UgaWYgKGN1clB1bmMgPT0gY3R4LnR5cGUpIHBvcENvbnRleHQoc3RhdGUpO2Vsc2UgaWYgKGN0eC50eXBlID09IFwifVwiIHx8IGN0eC50eXBlID09IFwidG9wXCIgfHwgY3R4LnR5cGUgPT0gXCJzdGF0ZW1lbnRcIiAmJiBjdXJQdW5jID09IFwibmV3c3RhdGVtZW50XCIpIHB1c2hDb250ZXh0KHN0YXRlLCBzdHJlYW0uY29sdW1uKCksIFwic3RhdGVtZW50XCIpO1xuICAgIHN0YXRlLnN0YXJ0T2ZMaW5lID0gZmFsc2U7XG4gICAgc3RhdGUubGFzdFRva2VuID0gY3VyUHVuYyB8fCBzdHlsZTtcbiAgICByZXR1cm4gc3R5bGU7XG4gIH0sXG4gIGluZGVudDogZnVuY3Rpb24gKHN0YXRlLCB0ZXh0QWZ0ZXIsIGN4KSB7XG4gICAgaWYgKCFzdGF0ZS50b2tlbml6ZVtzdGF0ZS50b2tlbml6ZS5sZW5ndGggLSAxXS5pc0Jhc2UpIHJldHVybiBudWxsO1xuICAgIHZhciBmaXJzdENoYXIgPSB0ZXh0QWZ0ZXIgJiYgdGV4dEFmdGVyLmNoYXJBdCgwKSxcbiAgICAgIGN0eCA9IHN0YXRlLmNvbnRleHQ7XG4gICAgaWYgKGN0eC50eXBlID09IFwic3RhdGVtZW50XCIgJiYgIWV4cGVjdEV4cHJlc3Npb24oc3RhdGUubGFzdFRva2VuLCB0cnVlKSkgY3R4ID0gY3R4LnByZXY7XG4gICAgdmFyIGNsb3NpbmcgPSBmaXJzdENoYXIgPT0gY3R4LnR5cGU7XG4gICAgaWYgKGN0eC50eXBlID09IFwic3RhdGVtZW50XCIpIHJldHVybiBjdHguaW5kZW50ZWQgKyAoZmlyc3RDaGFyID09IFwie1wiID8gMCA6IGN4LnVuaXQpO2Vsc2UgaWYgKGN0eC5hbGlnbikgcmV0dXJuIGN0eC5jb2x1bW4gKyAoY2xvc2luZyA/IDAgOiAxKTtlbHNlIHJldHVybiBjdHguaW5kZW50ZWQgKyAoY2xvc2luZyA/IDAgOiBjeC51bml0KTtcbiAgfSxcbiAgbGFuZ3VhZ2VEYXRhOiB7XG4gICAgaW5kZW50T25JbnB1dDogL15cXHMqW3t9XSQvLFxuICAgIGNvbW1lbnRUb2tlbnM6IHtcbiAgICAgIGxpbmU6IFwiLy9cIixcbiAgICAgIGJsb2NrOiB7XG4gICAgICAgIG9wZW46IFwiLypcIixcbiAgICAgICAgY2xvc2U6IFwiKi9cIlxuICAgICAgfVxuICAgIH0sXG4gICAgY2xvc2VCcmFja2V0czoge1xuICAgICAgYnJhY2tldHM6IFtcIihcIiwgXCJbXCIsIFwie1wiLCBcIidcIiwgJ1wiJywgXCInJydcIiwgJ1wiXCJcIiddXG4gICAgfVxuICB9XG59OyJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==