"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[2218],{

/***/ 72218:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "asciiArmor": () => (/* binding */ asciiArmor)
/* harmony export */ });
function errorIfNotEmpty(stream) {
  var nonWS = stream.match(/^\s*\S/);
  stream.skipToEnd();
  return nonWS ? "error" : null;
}
const asciiArmor = {
  name: "asciiarmor",
  token: function (stream, state) {
    var m;
    if (state.state == "top") {
      if (stream.sol() && (m = stream.match(/^-----BEGIN (.*)?-----\s*$/))) {
        state.state = "headers";
        state.type = m[1];
        return "tag";
      }
      return errorIfNotEmpty(stream);
    } else if (state.state == "headers") {
      if (stream.sol() && stream.match(/^\w+:/)) {
        state.state = "header";
        return "atom";
      } else {
        var result = errorIfNotEmpty(stream);
        if (result) state.state = "body";
        return result;
      }
    } else if (state.state == "header") {
      stream.skipToEnd();
      state.state = "headers";
      return "string";
    } else if (state.state == "body") {
      if (stream.sol() && (m = stream.match(/^-----END (.*)?-----\s*$/))) {
        if (m[1] != state.type) return "error";
        state.state = "end";
        return "tag";
      } else {
        if (stream.eatWhile(/[A-Za-z0-9+\/=]/)) {
          return null;
        } else {
          stream.next();
          return "error";
        }
      }
    } else if (state.state == "end") {
      return errorIfNotEmpty(stream);
    }
  },
  blankLine: function (state) {
    if (state.state == "headers") state.state = "body";
  },
  startState: function () {
    return {
      state: "top",
      type: null
    };
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiMjIxOC5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGNvZGVtaXJyb3IvbGVnYWN5LW1vZGVzL21vZGUvYXNjaWlhcm1vci5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyJmdW5jdGlvbiBlcnJvcklmTm90RW1wdHkoc3RyZWFtKSB7XG4gIHZhciBub25XUyA9IHN0cmVhbS5tYXRjaCgvXlxccypcXFMvKTtcbiAgc3RyZWFtLnNraXBUb0VuZCgpO1xuICByZXR1cm4gbm9uV1MgPyBcImVycm9yXCIgOiBudWxsO1xufVxuZXhwb3J0IGNvbnN0IGFzY2lpQXJtb3IgPSB7XG4gIG5hbWU6IFwiYXNjaWlhcm1vclwiLFxuICB0b2tlbjogZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICB2YXIgbTtcbiAgICBpZiAoc3RhdGUuc3RhdGUgPT0gXCJ0b3BcIikge1xuICAgICAgaWYgKHN0cmVhbS5zb2woKSAmJiAobSA9IHN0cmVhbS5tYXRjaCgvXi0tLS0tQkVHSU4gKC4qKT8tLS0tLVxccyokLykpKSB7XG4gICAgICAgIHN0YXRlLnN0YXRlID0gXCJoZWFkZXJzXCI7XG4gICAgICAgIHN0YXRlLnR5cGUgPSBtWzFdO1xuICAgICAgICByZXR1cm4gXCJ0YWdcIjtcbiAgICAgIH1cbiAgICAgIHJldHVybiBlcnJvcklmTm90RW1wdHkoc3RyZWFtKTtcbiAgICB9IGVsc2UgaWYgKHN0YXRlLnN0YXRlID09IFwiaGVhZGVyc1wiKSB7XG4gICAgICBpZiAoc3RyZWFtLnNvbCgpICYmIHN0cmVhbS5tYXRjaCgvXlxcdys6LykpIHtcbiAgICAgICAgc3RhdGUuc3RhdGUgPSBcImhlYWRlclwiO1xuICAgICAgICByZXR1cm4gXCJhdG9tXCI7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICB2YXIgcmVzdWx0ID0gZXJyb3JJZk5vdEVtcHR5KHN0cmVhbSk7XG4gICAgICAgIGlmIChyZXN1bHQpIHN0YXRlLnN0YXRlID0gXCJib2R5XCI7XG4gICAgICAgIHJldHVybiByZXN1bHQ7XG4gICAgICB9XG4gICAgfSBlbHNlIGlmIChzdGF0ZS5zdGF0ZSA9PSBcImhlYWRlclwiKSB7XG4gICAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgICBzdGF0ZS5zdGF0ZSA9IFwiaGVhZGVyc1wiO1xuICAgICAgcmV0dXJuIFwic3RyaW5nXCI7XG4gICAgfSBlbHNlIGlmIChzdGF0ZS5zdGF0ZSA9PSBcImJvZHlcIikge1xuICAgICAgaWYgKHN0cmVhbS5zb2woKSAmJiAobSA9IHN0cmVhbS5tYXRjaCgvXi0tLS0tRU5EICguKik/LS0tLS1cXHMqJC8pKSkge1xuICAgICAgICBpZiAobVsxXSAhPSBzdGF0ZS50eXBlKSByZXR1cm4gXCJlcnJvclwiO1xuICAgICAgICBzdGF0ZS5zdGF0ZSA9IFwiZW5kXCI7XG4gICAgICAgIHJldHVybiBcInRhZ1wiO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgaWYgKHN0cmVhbS5lYXRXaGlsZSgvW0EtWmEtejAtOStcXC89XS8pKSB7XG4gICAgICAgICAgcmV0dXJuIG51bGw7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgc3RyZWFtLm5leHQoKTtcbiAgICAgICAgICByZXR1cm4gXCJlcnJvclwiO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfSBlbHNlIGlmIChzdGF0ZS5zdGF0ZSA9PSBcImVuZFwiKSB7XG4gICAgICByZXR1cm4gZXJyb3JJZk5vdEVtcHR5KHN0cmVhbSk7XG4gICAgfVxuICB9LFxuICBibGFua0xpbmU6IGZ1bmN0aW9uIChzdGF0ZSkge1xuICAgIGlmIChzdGF0ZS5zdGF0ZSA9PSBcImhlYWRlcnNcIikgc3RhdGUuc3RhdGUgPSBcImJvZHlcIjtcbiAgfSxcbiAgc3RhcnRTdGF0ZTogZnVuY3Rpb24gKCkge1xuICAgIHJldHVybiB7XG4gICAgICBzdGF0ZTogXCJ0b3BcIixcbiAgICAgIHR5cGU6IG51bGxcbiAgICB9O1xuICB9XG59OyJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==