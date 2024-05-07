"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[8731],{

/***/ 38731:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "commonLisp": () => (/* binding */ commonLisp)
/* harmony export */ });
var specialForm = /^(block|let*|return-from|catch|load-time-value|setq|eval-when|locally|symbol-macrolet|flet|macrolet|tagbody|function|multiple-value-call|the|go|multiple-value-prog1|throw|if|progn|unwind-protect|labels|progv|let|quote)$/;
var assumeBody = /^with|^def|^do|^prog|case$|^cond$|bind$|when$|unless$/;
var numLiteral = /^(?:[+\-]?(?:\d+|\d*\.\d+)(?:[efd][+\-]?\d+)?|[+\-]?\d+(?:\/[+\-]?\d+)?|#b[+\-]?[01]+|#o[+\-]?[0-7]+|#x[+\-]?[\da-f]+)/;
var symbol = /[^\s'`,@()\[\]";]/;
var type;
function readSym(stream) {
  var ch;
  while (ch = stream.next()) {
    if (ch == "\\") stream.next();else if (!symbol.test(ch)) {
      stream.backUp(1);
      break;
    }
  }
  return stream.current();
}
function base(stream, state) {
  if (stream.eatSpace()) {
    type = "ws";
    return null;
  }
  if (stream.match(numLiteral)) return "number";
  var ch = stream.next();
  if (ch == "\\") ch = stream.next();
  if (ch == '"') return (state.tokenize = inString)(stream, state);else if (ch == "(") {
    type = "open";
    return "bracket";
  } else if (ch == ")" || ch == "]") {
    type = "close";
    return "bracket";
  } else if (ch == ";") {
    stream.skipToEnd();
    type = "ws";
    return "comment";
  } else if (/['`,@]/.test(ch)) return null;else if (ch == "|") {
    if (stream.skipTo("|")) {
      stream.next();
      return "variableName";
    } else {
      stream.skipToEnd();
      return "error";
    }
  } else if (ch == "#") {
    var ch = stream.next();
    if (ch == "(") {
      type = "open";
      return "bracket";
    } else if (/[+\-=\.']/.test(ch)) return null;else if (/\d/.test(ch) && stream.match(/^\d*#/)) return null;else if (ch == "|") return (state.tokenize = inComment)(stream, state);else if (ch == ":") {
      readSym(stream);
      return "meta";
    } else if (ch == "\\") {
      stream.next();
      readSym(stream);
      return "string.special";
    } else return "error";
  } else {
    var name = readSym(stream);
    if (name == ".") return null;
    type = "symbol";
    if (name == "nil" || name == "t" || name.charAt(0) == ":") return "atom";
    if (state.lastType == "open" && (specialForm.test(name) || assumeBody.test(name))) return "keyword";
    if (name.charAt(0) == "&") return "variableName.special";
    return "variableName";
  }
}
function inString(stream, state) {
  var escaped = false,
    next;
  while (next = stream.next()) {
    if (next == '"' && !escaped) {
      state.tokenize = base;
      break;
    }
    escaped = !escaped && next == "\\";
  }
  return "string";
}
function inComment(stream, state) {
  var next, last;
  while (next = stream.next()) {
    if (next == "#" && last == "|") {
      state.tokenize = base;
      break;
    }
    last = next;
  }
  type = "ws";
  return "comment";
}
const commonLisp = {
  name: "commonlisp",
  startState: function () {
    return {
      ctx: {
        prev: null,
        start: 0,
        indentTo: 0
      },
      lastType: null,
      tokenize: base
    };
  },
  token: function (stream, state) {
    if (stream.sol() && typeof state.ctx.indentTo != "number") state.ctx.indentTo = state.ctx.start + 1;
    type = null;
    var style = state.tokenize(stream, state);
    if (type != "ws") {
      if (state.ctx.indentTo == null) {
        if (type == "symbol" && assumeBody.test(stream.current())) state.ctx.indentTo = state.ctx.start + stream.indentUnit;else state.ctx.indentTo = "next";
      } else if (state.ctx.indentTo == "next") {
        state.ctx.indentTo = stream.column();
      }
      state.lastType = type;
    }
    if (type == "open") state.ctx = {
      prev: state.ctx,
      start: stream.column(),
      indentTo: null
    };else if (type == "close") state.ctx = state.ctx.prev || state.ctx;
    return style;
  },
  indent: function (state) {
    var i = state.ctx.indentTo;
    return typeof i == "number" ? i : state.ctx.start + 1;
  },
  languageData: {
    commentTokens: {
      line: ";;",
      block: {
        open: "#|",
        close: "|#"
      }
    },
    closeBrackets: {
      brackets: ["(", "[", "{", '"']
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiODczMS5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGNvZGVtaXJyb3IvbGVnYWN5LW1vZGVzL21vZGUvY29tbW9ubGlzcC5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyJ2YXIgc3BlY2lhbEZvcm0gPSAvXihibG9ja3xsZXQqfHJldHVybi1mcm9tfGNhdGNofGxvYWQtdGltZS12YWx1ZXxzZXRxfGV2YWwtd2hlbnxsb2NhbGx5fHN5bWJvbC1tYWNyb2xldHxmbGV0fG1hY3JvbGV0fHRhZ2JvZHl8ZnVuY3Rpb258bXVsdGlwbGUtdmFsdWUtY2FsbHx0aGV8Z298bXVsdGlwbGUtdmFsdWUtcHJvZzF8dGhyb3d8aWZ8cHJvZ258dW53aW5kLXByb3RlY3R8bGFiZWxzfHByb2d2fGxldHxxdW90ZSkkLztcbnZhciBhc3N1bWVCb2R5ID0gL153aXRofF5kZWZ8XmRvfF5wcm9nfGNhc2UkfF5jb25kJHxiaW5kJHx3aGVuJHx1bmxlc3MkLztcbnZhciBudW1MaXRlcmFsID0gL14oPzpbK1xcLV0/KD86XFxkK3xcXGQqXFwuXFxkKykoPzpbZWZkXVsrXFwtXT9cXGQrKT98WytcXC1dP1xcZCsoPzpcXC9bK1xcLV0/XFxkKyk/fCNiWytcXC1dP1swMV0rfCNvWytcXC1dP1swLTddK3wjeFsrXFwtXT9bXFxkYS1mXSspLztcbnZhciBzeW1ib2wgPSAvW15cXHMnYCxAKClcXFtcXF1cIjtdLztcbnZhciB0eXBlO1xuZnVuY3Rpb24gcmVhZFN5bShzdHJlYW0pIHtcbiAgdmFyIGNoO1xuICB3aGlsZSAoY2ggPSBzdHJlYW0ubmV4dCgpKSB7XG4gICAgaWYgKGNoID09IFwiXFxcXFwiKSBzdHJlYW0ubmV4dCgpO2Vsc2UgaWYgKCFzeW1ib2wudGVzdChjaCkpIHtcbiAgICAgIHN0cmVhbS5iYWNrVXAoMSk7XG4gICAgICBicmVhaztcbiAgICB9XG4gIH1cbiAgcmV0dXJuIHN0cmVhbS5jdXJyZW50KCk7XG59XG5mdW5jdGlvbiBiYXNlKHN0cmVhbSwgc3RhdGUpIHtcbiAgaWYgKHN0cmVhbS5lYXRTcGFjZSgpKSB7XG4gICAgdHlwZSA9IFwid3NcIjtcbiAgICByZXR1cm4gbnVsbDtcbiAgfVxuICBpZiAoc3RyZWFtLm1hdGNoKG51bUxpdGVyYWwpKSByZXR1cm4gXCJudW1iZXJcIjtcbiAgdmFyIGNoID0gc3RyZWFtLm5leHQoKTtcbiAgaWYgKGNoID09IFwiXFxcXFwiKSBjaCA9IHN0cmVhbS5uZXh0KCk7XG4gIGlmIChjaCA9PSAnXCInKSByZXR1cm4gKHN0YXRlLnRva2VuaXplID0gaW5TdHJpbmcpKHN0cmVhbSwgc3RhdGUpO2Vsc2UgaWYgKGNoID09IFwiKFwiKSB7XG4gICAgdHlwZSA9IFwib3BlblwiO1xuICAgIHJldHVybiBcImJyYWNrZXRcIjtcbiAgfSBlbHNlIGlmIChjaCA9PSBcIilcIiB8fCBjaCA9PSBcIl1cIikge1xuICAgIHR5cGUgPSBcImNsb3NlXCI7XG4gICAgcmV0dXJuIFwiYnJhY2tldFwiO1xuICB9IGVsc2UgaWYgKGNoID09IFwiO1wiKSB7XG4gICAgc3RyZWFtLnNraXBUb0VuZCgpO1xuICAgIHR5cGUgPSBcIndzXCI7XG4gICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICB9IGVsc2UgaWYgKC9bJ2AsQF0vLnRlc3QoY2gpKSByZXR1cm4gbnVsbDtlbHNlIGlmIChjaCA9PSBcInxcIikge1xuICAgIGlmIChzdHJlYW0uc2tpcFRvKFwifFwiKSkge1xuICAgICAgc3RyZWFtLm5leHQoKTtcbiAgICAgIHJldHVybiBcInZhcmlhYmxlTmFtZVwiO1xuICAgIH0gZWxzZSB7XG4gICAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgICByZXR1cm4gXCJlcnJvclwiO1xuICAgIH1cbiAgfSBlbHNlIGlmIChjaCA9PSBcIiNcIikge1xuICAgIHZhciBjaCA9IHN0cmVhbS5uZXh0KCk7XG4gICAgaWYgKGNoID09IFwiKFwiKSB7XG4gICAgICB0eXBlID0gXCJvcGVuXCI7XG4gICAgICByZXR1cm4gXCJicmFja2V0XCI7XG4gICAgfSBlbHNlIGlmICgvWytcXC09XFwuJ10vLnRlc3QoY2gpKSByZXR1cm4gbnVsbDtlbHNlIGlmICgvXFxkLy50ZXN0KGNoKSAmJiBzdHJlYW0ubWF0Y2goL15cXGQqIy8pKSByZXR1cm4gbnVsbDtlbHNlIGlmIChjaCA9PSBcInxcIikgcmV0dXJuIChzdGF0ZS50b2tlbml6ZSA9IGluQ29tbWVudCkoc3RyZWFtLCBzdGF0ZSk7ZWxzZSBpZiAoY2ggPT0gXCI6XCIpIHtcbiAgICAgIHJlYWRTeW0oc3RyZWFtKTtcbiAgICAgIHJldHVybiBcIm1ldGFcIjtcbiAgICB9IGVsc2UgaWYgKGNoID09IFwiXFxcXFwiKSB7XG4gICAgICBzdHJlYW0ubmV4dCgpO1xuICAgICAgcmVhZFN5bShzdHJlYW0pO1xuICAgICAgcmV0dXJuIFwic3RyaW5nLnNwZWNpYWxcIjtcbiAgICB9IGVsc2UgcmV0dXJuIFwiZXJyb3JcIjtcbiAgfSBlbHNlIHtcbiAgICB2YXIgbmFtZSA9IHJlYWRTeW0oc3RyZWFtKTtcbiAgICBpZiAobmFtZSA9PSBcIi5cIikgcmV0dXJuIG51bGw7XG4gICAgdHlwZSA9IFwic3ltYm9sXCI7XG4gICAgaWYgKG5hbWUgPT0gXCJuaWxcIiB8fCBuYW1lID09IFwidFwiIHx8IG5hbWUuY2hhckF0KDApID09IFwiOlwiKSByZXR1cm4gXCJhdG9tXCI7XG4gICAgaWYgKHN0YXRlLmxhc3RUeXBlID09IFwib3BlblwiICYmIChzcGVjaWFsRm9ybS50ZXN0KG5hbWUpIHx8IGFzc3VtZUJvZHkudGVzdChuYW1lKSkpIHJldHVybiBcImtleXdvcmRcIjtcbiAgICBpZiAobmFtZS5jaGFyQXQoMCkgPT0gXCImXCIpIHJldHVybiBcInZhcmlhYmxlTmFtZS5zcGVjaWFsXCI7XG4gICAgcmV0dXJuIFwidmFyaWFibGVOYW1lXCI7XG4gIH1cbn1cbmZ1bmN0aW9uIGluU3RyaW5nKHN0cmVhbSwgc3RhdGUpIHtcbiAgdmFyIGVzY2FwZWQgPSBmYWxzZSxcbiAgICBuZXh0O1xuICB3aGlsZSAobmV4dCA9IHN0cmVhbS5uZXh0KCkpIHtcbiAgICBpZiAobmV4dCA9PSAnXCInICYmICFlc2NhcGVkKSB7XG4gICAgICBzdGF0ZS50b2tlbml6ZSA9IGJhc2U7XG4gICAgICBicmVhaztcbiAgICB9XG4gICAgZXNjYXBlZCA9ICFlc2NhcGVkICYmIG5leHQgPT0gXCJcXFxcXCI7XG4gIH1cbiAgcmV0dXJuIFwic3RyaW5nXCI7XG59XG5mdW5jdGlvbiBpbkNvbW1lbnQoc3RyZWFtLCBzdGF0ZSkge1xuICB2YXIgbmV4dCwgbGFzdDtcbiAgd2hpbGUgKG5leHQgPSBzdHJlYW0ubmV4dCgpKSB7XG4gICAgaWYgKG5leHQgPT0gXCIjXCIgJiYgbGFzdCA9PSBcInxcIikge1xuICAgICAgc3RhdGUudG9rZW5pemUgPSBiYXNlO1xuICAgICAgYnJlYWs7XG4gICAgfVxuICAgIGxhc3QgPSBuZXh0O1xuICB9XG4gIHR5cGUgPSBcIndzXCI7XG4gIHJldHVybiBcImNvbW1lbnRcIjtcbn1cbmV4cG9ydCBjb25zdCBjb21tb25MaXNwID0ge1xuICBuYW1lOiBcImNvbW1vbmxpc3BcIixcbiAgc3RhcnRTdGF0ZTogZnVuY3Rpb24gKCkge1xuICAgIHJldHVybiB7XG4gICAgICBjdHg6IHtcbiAgICAgICAgcHJldjogbnVsbCxcbiAgICAgICAgc3RhcnQ6IDAsXG4gICAgICAgIGluZGVudFRvOiAwXG4gICAgICB9LFxuICAgICAgbGFzdFR5cGU6IG51bGwsXG4gICAgICB0b2tlbml6ZTogYmFzZVxuICAgIH07XG4gIH0sXG4gIHRva2VuOiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIGlmIChzdHJlYW0uc29sKCkgJiYgdHlwZW9mIHN0YXRlLmN0eC5pbmRlbnRUbyAhPSBcIm51bWJlclwiKSBzdGF0ZS5jdHguaW5kZW50VG8gPSBzdGF0ZS5jdHguc3RhcnQgKyAxO1xuICAgIHR5cGUgPSBudWxsO1xuICAgIHZhciBzdHlsZSA9IHN0YXRlLnRva2VuaXplKHN0cmVhbSwgc3RhdGUpO1xuICAgIGlmICh0eXBlICE9IFwid3NcIikge1xuICAgICAgaWYgKHN0YXRlLmN0eC5pbmRlbnRUbyA9PSBudWxsKSB7XG4gICAgICAgIGlmICh0eXBlID09IFwic3ltYm9sXCIgJiYgYXNzdW1lQm9keS50ZXN0KHN0cmVhbS5jdXJyZW50KCkpKSBzdGF0ZS5jdHguaW5kZW50VG8gPSBzdGF0ZS5jdHguc3RhcnQgKyBzdHJlYW0uaW5kZW50VW5pdDtlbHNlIHN0YXRlLmN0eC5pbmRlbnRUbyA9IFwibmV4dFwiO1xuICAgICAgfSBlbHNlIGlmIChzdGF0ZS5jdHguaW5kZW50VG8gPT0gXCJuZXh0XCIpIHtcbiAgICAgICAgc3RhdGUuY3R4LmluZGVudFRvID0gc3RyZWFtLmNvbHVtbigpO1xuICAgICAgfVxuICAgICAgc3RhdGUubGFzdFR5cGUgPSB0eXBlO1xuICAgIH1cbiAgICBpZiAodHlwZSA9PSBcIm9wZW5cIikgc3RhdGUuY3R4ID0ge1xuICAgICAgcHJldjogc3RhdGUuY3R4LFxuICAgICAgc3RhcnQ6IHN0cmVhbS5jb2x1bW4oKSxcbiAgICAgIGluZGVudFRvOiBudWxsXG4gICAgfTtlbHNlIGlmICh0eXBlID09IFwiY2xvc2VcIikgc3RhdGUuY3R4ID0gc3RhdGUuY3R4LnByZXYgfHwgc3RhdGUuY3R4O1xuICAgIHJldHVybiBzdHlsZTtcbiAgfSxcbiAgaW5kZW50OiBmdW5jdGlvbiAoc3RhdGUpIHtcbiAgICB2YXIgaSA9IHN0YXRlLmN0eC5pbmRlbnRUbztcbiAgICByZXR1cm4gdHlwZW9mIGkgPT0gXCJudW1iZXJcIiA/IGkgOiBzdGF0ZS5jdHguc3RhcnQgKyAxO1xuICB9LFxuICBsYW5ndWFnZURhdGE6IHtcbiAgICBjb21tZW50VG9rZW5zOiB7XG4gICAgICBsaW5lOiBcIjs7XCIsXG4gICAgICBibG9jazoge1xuICAgICAgICBvcGVuOiBcIiN8XCIsXG4gICAgICAgIGNsb3NlOiBcInwjXCJcbiAgICAgIH1cbiAgICB9LFxuICAgIGNsb3NlQnJhY2tldHM6IHtcbiAgICAgIGJyYWNrZXRzOiBbXCIoXCIsIFwiW1wiLCBcIntcIiwgJ1wiJ11cbiAgICB9XG4gIH1cbn07Il0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9