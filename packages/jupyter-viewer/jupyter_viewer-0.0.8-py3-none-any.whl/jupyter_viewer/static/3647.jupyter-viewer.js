"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[3647],{

/***/ 73647:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "pascal": () => (/* binding */ pascal)
/* harmony export */ });
function words(str) {
  var obj = {},
    words = str.split(" ");
  for (var i = 0; i < words.length; ++i) obj[words[i]] = true;
  return obj;
}
var keywords = words("absolute and array asm begin case const constructor destructor div do " + "downto else end file for function goto if implementation in inherited " + "inline interface label mod nil not object of operator or packed procedure " + "program record reintroduce repeat self set shl shr string then to type " + "unit until uses var while with xor as class dispinterface except exports " + "finalization finally initialization inline is library on out packed " + "property raise resourcestring threadvar try absolute abstract alias " + "assembler bitpacked break cdecl continue cppdecl cvar default deprecated " + "dynamic enumerator experimental export external far far16 forward generic " + "helper implements index interrupt iocheck local message name near " + "nodefault noreturn nostackframe oldfpccall otherwise overload override " + "pascal platform private protected public published read register " + "reintroduce result safecall saveregisters softfloat specialize static " + "stdcall stored strict unaligned unimplemented varargs virtual write");
var atoms = {
  "null": true
};
var isOperatorChar = /[+\-*&%=<>!?|\/]/;
function tokenBase(stream, state) {
  var ch = stream.next();
  if (ch == "#" && state.startOfLine) {
    stream.skipToEnd();
    return "meta";
  }
  if (ch == '"' || ch == "'") {
    state.tokenize = tokenString(ch);
    return state.tokenize(stream, state);
  }
  if (ch == "(" && stream.eat("*")) {
    state.tokenize = tokenComment;
    return tokenComment(stream, state);
  }
  if (ch == "{") {
    state.tokenize = tokenCommentBraces;
    return tokenCommentBraces(stream, state);
  }
  if (/[\[\]\(\),;\:\.]/.test(ch)) {
    return null;
  }
  if (/\d/.test(ch)) {
    stream.eatWhile(/[\w\.]/);
    return "number";
  }
  if (ch == "/") {
    if (stream.eat("/")) {
      stream.skipToEnd();
      return "comment";
    }
  }
  if (isOperatorChar.test(ch)) {
    stream.eatWhile(isOperatorChar);
    return "operator";
  }
  stream.eatWhile(/[\w\$_]/);
  var cur = stream.current();
  if (keywords.propertyIsEnumerable(cur)) return "keyword";
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
      escaped = !escaped && next == "\\";
    }
    if (end || !escaped) state.tokenize = null;
    return "string";
  };
}
function tokenComment(stream, state) {
  var maybeEnd = false,
    ch;
  while (ch = stream.next()) {
    if (ch == ")" && maybeEnd) {
      state.tokenize = null;
      break;
    }
    maybeEnd = ch == "*";
  }
  return "comment";
}
function tokenCommentBraces(stream, state) {
  var ch;
  while (ch = stream.next()) {
    if (ch == "}") {
      state.tokenize = null;
      break;
    }
  }
  return "comment";
}

// Interface

const pascal = {
  name: "pascal",
  startState: function () {
    return {
      tokenize: null
    };
  },
  token: function (stream, state) {
    if (stream.eatSpace()) return null;
    var style = (state.tokenize || tokenBase)(stream, state);
    if (style == "comment" || style == "meta") return style;
    return style;
  },
  languageData: {
    indentOnInput: /^\s*[{}]$/,
    commentTokens: {
      block: {
        open: "(*",
        close: "*)"
      }
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiMzY0Ny5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGNvZGVtaXJyb3IvbGVnYWN5LW1vZGVzL21vZGUvcGFzY2FsLmpzIl0sInNvdXJjZXNDb250ZW50IjpbImZ1bmN0aW9uIHdvcmRzKHN0cikge1xuICB2YXIgb2JqID0ge30sXG4gICAgd29yZHMgPSBzdHIuc3BsaXQoXCIgXCIpO1xuICBmb3IgKHZhciBpID0gMDsgaSA8IHdvcmRzLmxlbmd0aDsgKytpKSBvYmpbd29yZHNbaV1dID0gdHJ1ZTtcbiAgcmV0dXJuIG9iajtcbn1cbnZhciBrZXl3b3JkcyA9IHdvcmRzKFwiYWJzb2x1dGUgYW5kIGFycmF5IGFzbSBiZWdpbiBjYXNlIGNvbnN0IGNvbnN0cnVjdG9yIGRlc3RydWN0b3IgZGl2IGRvIFwiICsgXCJkb3dudG8gZWxzZSBlbmQgZmlsZSBmb3IgZnVuY3Rpb24gZ290byBpZiBpbXBsZW1lbnRhdGlvbiBpbiBpbmhlcml0ZWQgXCIgKyBcImlubGluZSBpbnRlcmZhY2UgbGFiZWwgbW9kIG5pbCBub3Qgb2JqZWN0IG9mIG9wZXJhdG9yIG9yIHBhY2tlZCBwcm9jZWR1cmUgXCIgKyBcInByb2dyYW0gcmVjb3JkIHJlaW50cm9kdWNlIHJlcGVhdCBzZWxmIHNldCBzaGwgc2hyIHN0cmluZyB0aGVuIHRvIHR5cGUgXCIgKyBcInVuaXQgdW50aWwgdXNlcyB2YXIgd2hpbGUgd2l0aCB4b3IgYXMgY2xhc3MgZGlzcGludGVyZmFjZSBleGNlcHQgZXhwb3J0cyBcIiArIFwiZmluYWxpemF0aW9uIGZpbmFsbHkgaW5pdGlhbGl6YXRpb24gaW5saW5lIGlzIGxpYnJhcnkgb24gb3V0IHBhY2tlZCBcIiArIFwicHJvcGVydHkgcmFpc2UgcmVzb3VyY2VzdHJpbmcgdGhyZWFkdmFyIHRyeSBhYnNvbHV0ZSBhYnN0cmFjdCBhbGlhcyBcIiArIFwiYXNzZW1ibGVyIGJpdHBhY2tlZCBicmVhayBjZGVjbCBjb250aW51ZSBjcHBkZWNsIGN2YXIgZGVmYXVsdCBkZXByZWNhdGVkIFwiICsgXCJkeW5hbWljIGVudW1lcmF0b3IgZXhwZXJpbWVudGFsIGV4cG9ydCBleHRlcm5hbCBmYXIgZmFyMTYgZm9yd2FyZCBnZW5lcmljIFwiICsgXCJoZWxwZXIgaW1wbGVtZW50cyBpbmRleCBpbnRlcnJ1cHQgaW9jaGVjayBsb2NhbCBtZXNzYWdlIG5hbWUgbmVhciBcIiArIFwibm9kZWZhdWx0IG5vcmV0dXJuIG5vc3RhY2tmcmFtZSBvbGRmcGNjYWxsIG90aGVyd2lzZSBvdmVybG9hZCBvdmVycmlkZSBcIiArIFwicGFzY2FsIHBsYXRmb3JtIHByaXZhdGUgcHJvdGVjdGVkIHB1YmxpYyBwdWJsaXNoZWQgcmVhZCByZWdpc3RlciBcIiArIFwicmVpbnRyb2R1Y2UgcmVzdWx0IHNhZmVjYWxsIHNhdmVyZWdpc3RlcnMgc29mdGZsb2F0IHNwZWNpYWxpemUgc3RhdGljIFwiICsgXCJzdGRjYWxsIHN0b3JlZCBzdHJpY3QgdW5hbGlnbmVkIHVuaW1wbGVtZW50ZWQgdmFyYXJncyB2aXJ0dWFsIHdyaXRlXCIpO1xudmFyIGF0b21zID0ge1xuICBcIm51bGxcIjogdHJ1ZVxufTtcbnZhciBpc09wZXJhdG9yQ2hhciA9IC9bK1xcLSomJT08PiE/fFxcL10vO1xuZnVuY3Rpb24gdG9rZW5CYXNlKHN0cmVhbSwgc3RhdGUpIHtcbiAgdmFyIGNoID0gc3RyZWFtLm5leHQoKTtcbiAgaWYgKGNoID09IFwiI1wiICYmIHN0YXRlLnN0YXJ0T2ZMaW5lKSB7XG4gICAgc3RyZWFtLnNraXBUb0VuZCgpO1xuICAgIHJldHVybiBcIm1ldGFcIjtcbiAgfVxuICBpZiAoY2ggPT0gJ1wiJyB8fCBjaCA9PSBcIidcIikge1xuICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5TdHJpbmcoY2gpO1xuICAgIHJldHVybiBzdGF0ZS50b2tlbml6ZShzdHJlYW0sIHN0YXRlKTtcbiAgfVxuICBpZiAoY2ggPT0gXCIoXCIgJiYgc3RyZWFtLmVhdChcIipcIikpIHtcbiAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQ29tbWVudDtcbiAgICByZXR1cm4gdG9rZW5Db21tZW50KHN0cmVhbSwgc3RhdGUpO1xuICB9XG4gIGlmIChjaCA9PSBcIntcIikge1xuICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5Db21tZW50QnJhY2VzO1xuICAgIHJldHVybiB0b2tlbkNvbW1lbnRCcmFjZXMoc3RyZWFtLCBzdGF0ZSk7XG4gIH1cbiAgaWYgKC9bXFxbXFxdXFwoXFwpLDtcXDpcXC5dLy50ZXN0KGNoKSkge1xuICAgIHJldHVybiBudWxsO1xuICB9XG4gIGlmICgvXFxkLy50ZXN0KGNoKSkge1xuICAgIHN0cmVhbS5lYXRXaGlsZSgvW1xcd1xcLl0vKTtcbiAgICByZXR1cm4gXCJudW1iZXJcIjtcbiAgfVxuICBpZiAoY2ggPT0gXCIvXCIpIHtcbiAgICBpZiAoc3RyZWFtLmVhdChcIi9cIikpIHtcbiAgICAgIHN0cmVhbS5za2lwVG9FbmQoKTtcbiAgICAgIHJldHVybiBcImNvbW1lbnRcIjtcbiAgICB9XG4gIH1cbiAgaWYgKGlzT3BlcmF0b3JDaGFyLnRlc3QoY2gpKSB7XG4gICAgc3RyZWFtLmVhdFdoaWxlKGlzT3BlcmF0b3JDaGFyKTtcbiAgICByZXR1cm4gXCJvcGVyYXRvclwiO1xuICB9XG4gIHN0cmVhbS5lYXRXaGlsZSgvW1xcd1xcJF9dLyk7XG4gIHZhciBjdXIgPSBzdHJlYW0uY3VycmVudCgpO1xuICBpZiAoa2V5d29yZHMucHJvcGVydHlJc0VudW1lcmFibGUoY3VyKSkgcmV0dXJuIFwia2V5d29yZFwiO1xuICBpZiAoYXRvbXMucHJvcGVydHlJc0VudW1lcmFibGUoY3VyKSkgcmV0dXJuIFwiYXRvbVwiO1xuICByZXR1cm4gXCJ2YXJpYWJsZVwiO1xufVxuZnVuY3Rpb24gdG9rZW5TdHJpbmcocXVvdGUpIHtcbiAgcmV0dXJuIGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgdmFyIGVzY2FwZWQgPSBmYWxzZSxcbiAgICAgIG5leHQsXG4gICAgICBlbmQgPSBmYWxzZTtcbiAgICB3aGlsZSAoKG5leHQgPSBzdHJlYW0ubmV4dCgpKSAhPSBudWxsKSB7XG4gICAgICBpZiAobmV4dCA9PSBxdW90ZSAmJiAhZXNjYXBlZCkge1xuICAgICAgICBlbmQgPSB0cnVlO1xuICAgICAgICBicmVhaztcbiAgICAgIH1cbiAgICAgIGVzY2FwZWQgPSAhZXNjYXBlZCAmJiBuZXh0ID09IFwiXFxcXFwiO1xuICAgIH1cbiAgICBpZiAoZW5kIHx8ICFlc2NhcGVkKSBzdGF0ZS50b2tlbml6ZSA9IG51bGw7XG4gICAgcmV0dXJuIFwic3RyaW5nXCI7XG4gIH07XG59XG5mdW5jdGlvbiB0b2tlbkNvbW1lbnQoc3RyZWFtLCBzdGF0ZSkge1xuICB2YXIgbWF5YmVFbmQgPSBmYWxzZSxcbiAgICBjaDtcbiAgd2hpbGUgKGNoID0gc3RyZWFtLm5leHQoKSkge1xuICAgIGlmIChjaCA9PSBcIilcIiAmJiBtYXliZUVuZCkge1xuICAgICAgc3RhdGUudG9rZW5pemUgPSBudWxsO1xuICAgICAgYnJlYWs7XG4gICAgfVxuICAgIG1heWJlRW5kID0gY2ggPT0gXCIqXCI7XG4gIH1cbiAgcmV0dXJuIFwiY29tbWVudFwiO1xufVxuZnVuY3Rpb24gdG9rZW5Db21tZW50QnJhY2VzKHN0cmVhbSwgc3RhdGUpIHtcbiAgdmFyIGNoO1xuICB3aGlsZSAoY2ggPSBzdHJlYW0ubmV4dCgpKSB7XG4gICAgaWYgKGNoID09IFwifVwiKSB7XG4gICAgICBzdGF0ZS50b2tlbml6ZSA9IG51bGw7XG4gICAgICBicmVhaztcbiAgICB9XG4gIH1cbiAgcmV0dXJuIFwiY29tbWVudFwiO1xufVxuXG4vLyBJbnRlcmZhY2VcblxuZXhwb3J0IGNvbnN0IHBhc2NhbCA9IHtcbiAgbmFtZTogXCJwYXNjYWxcIixcbiAgc3RhcnRTdGF0ZTogZnVuY3Rpb24gKCkge1xuICAgIHJldHVybiB7XG4gICAgICB0b2tlbml6ZTogbnVsbFxuICAgIH07XG4gIH0sXG4gIHRva2VuOiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIGlmIChzdHJlYW0uZWF0U3BhY2UoKSkgcmV0dXJuIG51bGw7XG4gICAgdmFyIHN0eWxlID0gKHN0YXRlLnRva2VuaXplIHx8IHRva2VuQmFzZSkoc3RyZWFtLCBzdGF0ZSk7XG4gICAgaWYgKHN0eWxlID09IFwiY29tbWVudFwiIHx8IHN0eWxlID09IFwibWV0YVwiKSByZXR1cm4gc3R5bGU7XG4gICAgcmV0dXJuIHN0eWxlO1xuICB9LFxuICBsYW5ndWFnZURhdGE6IHtcbiAgICBpbmRlbnRPbklucHV0OiAvXlxccypbe31dJC8sXG4gICAgY29tbWVudFRva2Vuczoge1xuICAgICAgYmxvY2s6IHtcbiAgICAgICAgb3BlbjogXCIoKlwiLFxuICAgICAgICBjbG9zZTogXCIqKVwiXG4gICAgICB9XG4gICAgfVxuICB9XG59OyJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==