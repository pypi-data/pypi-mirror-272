"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[3504],{

/***/ 3504:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "http": () => (/* binding */ http)
/* harmony export */ });
function failFirstLine(stream, state) {
  stream.skipToEnd();
  state.cur = header;
  return "error";
}
function start(stream, state) {
  if (stream.match(/^HTTP\/\d\.\d/)) {
    state.cur = responseStatusCode;
    return "keyword";
  } else if (stream.match(/^[A-Z]+/) && /[ \t]/.test(stream.peek())) {
    state.cur = requestPath;
    return "keyword";
  } else {
    return failFirstLine(stream, state);
  }
}
function responseStatusCode(stream, state) {
  var code = stream.match(/^\d+/);
  if (!code) return failFirstLine(stream, state);
  state.cur = responseStatusText;
  var status = Number(code[0]);
  if (status >= 100 && status < 400) {
    return "atom";
  } else {
    return "error";
  }
}
function responseStatusText(stream, state) {
  stream.skipToEnd();
  state.cur = header;
  return null;
}
function requestPath(stream, state) {
  stream.eatWhile(/\S/);
  state.cur = requestProtocol;
  return "string.special";
}
function requestProtocol(stream, state) {
  if (stream.match(/^HTTP\/\d\.\d$/)) {
    state.cur = header;
    return "keyword";
  } else {
    return failFirstLine(stream, state);
  }
}
function header(stream) {
  if (stream.sol() && !stream.eat(/[ \t]/)) {
    if (stream.match(/^.*?:/)) {
      return "atom";
    } else {
      stream.skipToEnd();
      return "error";
    }
  } else {
    stream.skipToEnd();
    return "string";
  }
}
function body(stream) {
  stream.skipToEnd();
  return null;
}
const http = {
  name: "http",
  token: function (stream, state) {
    var cur = state.cur;
    if (cur != header && cur != body && stream.eatSpace()) return null;
    return cur(stream, state);
  },
  blankLine: function (state) {
    state.cur = body;
  },
  startState: function () {
    return {
      cur: start
    };
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiMzUwNC5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9AY29kZW1pcnJvci9sZWdhY3ktbW9kZXMvbW9kZS9odHRwLmpzIl0sInNvdXJjZXNDb250ZW50IjpbImZ1bmN0aW9uIGZhaWxGaXJzdExpbmUoc3RyZWFtLCBzdGF0ZSkge1xuICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gIHN0YXRlLmN1ciA9IGhlYWRlcjtcbiAgcmV0dXJuIFwiZXJyb3JcIjtcbn1cbmZ1bmN0aW9uIHN0YXJ0KHN0cmVhbSwgc3RhdGUpIHtcbiAgaWYgKHN0cmVhbS5tYXRjaCgvXkhUVFBcXC9cXGRcXC5cXGQvKSkge1xuICAgIHN0YXRlLmN1ciA9IHJlc3BvbnNlU3RhdHVzQ29kZTtcbiAgICByZXR1cm4gXCJrZXl3b3JkXCI7XG4gIH0gZWxzZSBpZiAoc3RyZWFtLm1hdGNoKC9eW0EtWl0rLykgJiYgL1sgXFx0XS8udGVzdChzdHJlYW0ucGVlaygpKSkge1xuICAgIHN0YXRlLmN1ciA9IHJlcXVlc3RQYXRoO1xuICAgIHJldHVybiBcImtleXdvcmRcIjtcbiAgfSBlbHNlIHtcbiAgICByZXR1cm4gZmFpbEZpcnN0TGluZShzdHJlYW0sIHN0YXRlKTtcbiAgfVxufVxuZnVuY3Rpb24gcmVzcG9uc2VTdGF0dXNDb2RlKHN0cmVhbSwgc3RhdGUpIHtcbiAgdmFyIGNvZGUgPSBzdHJlYW0ubWF0Y2goL15cXGQrLyk7XG4gIGlmICghY29kZSkgcmV0dXJuIGZhaWxGaXJzdExpbmUoc3RyZWFtLCBzdGF0ZSk7XG4gIHN0YXRlLmN1ciA9IHJlc3BvbnNlU3RhdHVzVGV4dDtcbiAgdmFyIHN0YXR1cyA9IE51bWJlcihjb2RlWzBdKTtcbiAgaWYgKHN0YXR1cyA+PSAxMDAgJiYgc3RhdHVzIDwgNDAwKSB7XG4gICAgcmV0dXJuIFwiYXRvbVwiO1xuICB9IGVsc2Uge1xuICAgIHJldHVybiBcImVycm9yXCI7XG4gIH1cbn1cbmZ1bmN0aW9uIHJlc3BvbnNlU3RhdHVzVGV4dChzdHJlYW0sIHN0YXRlKSB7XG4gIHN0cmVhbS5za2lwVG9FbmQoKTtcbiAgc3RhdGUuY3VyID0gaGVhZGVyO1xuICByZXR1cm4gbnVsbDtcbn1cbmZ1bmN0aW9uIHJlcXVlc3RQYXRoKHN0cmVhbSwgc3RhdGUpIHtcbiAgc3RyZWFtLmVhdFdoaWxlKC9cXFMvKTtcbiAgc3RhdGUuY3VyID0gcmVxdWVzdFByb3RvY29sO1xuICByZXR1cm4gXCJzdHJpbmcuc3BlY2lhbFwiO1xufVxuZnVuY3Rpb24gcmVxdWVzdFByb3RvY29sKHN0cmVhbSwgc3RhdGUpIHtcbiAgaWYgKHN0cmVhbS5tYXRjaCgvXkhUVFBcXC9cXGRcXC5cXGQkLykpIHtcbiAgICBzdGF0ZS5jdXIgPSBoZWFkZXI7XG4gICAgcmV0dXJuIFwia2V5d29yZFwiO1xuICB9IGVsc2Uge1xuICAgIHJldHVybiBmYWlsRmlyc3RMaW5lKHN0cmVhbSwgc3RhdGUpO1xuICB9XG59XG5mdW5jdGlvbiBoZWFkZXIoc3RyZWFtKSB7XG4gIGlmIChzdHJlYW0uc29sKCkgJiYgIXN0cmVhbS5lYXQoL1sgXFx0XS8pKSB7XG4gICAgaWYgKHN0cmVhbS5tYXRjaCgvXi4qPzovKSkge1xuICAgICAgcmV0dXJuIFwiYXRvbVwiO1xuICAgIH0gZWxzZSB7XG4gICAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgICByZXR1cm4gXCJlcnJvclwiO1xuICAgIH1cbiAgfSBlbHNlIHtcbiAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgcmV0dXJuIFwic3RyaW5nXCI7XG4gIH1cbn1cbmZ1bmN0aW9uIGJvZHkoc3RyZWFtKSB7XG4gIHN0cmVhbS5za2lwVG9FbmQoKTtcbiAgcmV0dXJuIG51bGw7XG59XG5leHBvcnQgY29uc3QgaHR0cCA9IHtcbiAgbmFtZTogXCJodHRwXCIsXG4gIHRva2VuOiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIHZhciBjdXIgPSBzdGF0ZS5jdXI7XG4gICAgaWYgKGN1ciAhPSBoZWFkZXIgJiYgY3VyICE9IGJvZHkgJiYgc3RyZWFtLmVhdFNwYWNlKCkpIHJldHVybiBudWxsO1xuICAgIHJldHVybiBjdXIoc3RyZWFtLCBzdGF0ZSk7XG4gIH0sXG4gIGJsYW5rTGluZTogZnVuY3Rpb24gKHN0YXRlKSB7XG4gICAgc3RhdGUuY3VyID0gYm9keTtcbiAgfSxcbiAgc3RhcnRTdGF0ZTogZnVuY3Rpb24gKCkge1xuICAgIHJldHVybiB7XG4gICAgICBjdXI6IHN0YXJ0XG4gICAgfTtcbiAgfVxufTsiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=