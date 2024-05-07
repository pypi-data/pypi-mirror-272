"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[1450],{

/***/ 1450:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "brainfuck": () => (/* binding */ brainfuck)
/* harmony export */ });
var reserve = "><+-.,[]".split("");
/*
  comments can be either:
  placed behind lines

  +++    this is a comment

  where reserved characters cannot be used
  or in a loop
  [
  this is ok to use [ ] and stuff
  ]
  or preceded by #
*/
const brainfuck = {
  name: "brainfuck",
  startState: function () {
    return {
      commentLine: false,
      left: 0,
      right: 0,
      commentLoop: false
    };
  },
  token: function (stream, state) {
    if (stream.eatSpace()) return null;
    if (stream.sol()) {
      state.commentLine = false;
    }
    var ch = stream.next().toString();
    if (reserve.indexOf(ch) !== -1) {
      if (state.commentLine === true) {
        if (stream.eol()) {
          state.commentLine = false;
        }
        return "comment";
      }
      if (ch === "]" || ch === "[") {
        if (ch === "[") {
          state.left++;
        } else {
          state.right++;
        }
        return "bracket";
      } else if (ch === "+" || ch === "-") {
        return "keyword";
      } else if (ch === "<" || ch === ">") {
        return "atom";
      } else if (ch === "." || ch === ",") {
        return "def";
      }
    } else {
      state.commentLine = true;
      if (stream.eol()) {
        state.commentLine = false;
      }
      return "comment";
    }
    if (stream.eol()) {
      state.commentLine = false;
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiMTQ1MC5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9AY29kZW1pcnJvci9sZWdhY3ktbW9kZXMvbW9kZS9icmFpbmZ1Y2suanMiXSwic291cmNlc0NvbnRlbnQiOlsidmFyIHJlc2VydmUgPSBcIj48Ky0uLFtdXCIuc3BsaXQoXCJcIik7XG4vKlxuICBjb21tZW50cyBjYW4gYmUgZWl0aGVyOlxuICBwbGFjZWQgYmVoaW5kIGxpbmVzXG5cbiAgKysrICAgIHRoaXMgaXMgYSBjb21tZW50XG5cbiAgd2hlcmUgcmVzZXJ2ZWQgY2hhcmFjdGVycyBjYW5ub3QgYmUgdXNlZFxuICBvciBpbiBhIGxvb3BcbiAgW1xuICB0aGlzIGlzIG9rIHRvIHVzZSBbIF0gYW5kIHN0dWZmXG4gIF1cbiAgb3IgcHJlY2VkZWQgYnkgI1xuKi9cbmV4cG9ydCBjb25zdCBicmFpbmZ1Y2sgPSB7XG4gIG5hbWU6IFwiYnJhaW5mdWNrXCIsXG4gIHN0YXJ0U3RhdGU6IGZ1bmN0aW9uICgpIHtcbiAgICByZXR1cm4ge1xuICAgICAgY29tbWVudExpbmU6IGZhbHNlLFxuICAgICAgbGVmdDogMCxcbiAgICAgIHJpZ2h0OiAwLFxuICAgICAgY29tbWVudExvb3A6IGZhbHNlXG4gICAgfTtcbiAgfSxcbiAgdG9rZW46IGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgaWYgKHN0cmVhbS5lYXRTcGFjZSgpKSByZXR1cm4gbnVsbDtcbiAgICBpZiAoc3RyZWFtLnNvbCgpKSB7XG4gICAgICBzdGF0ZS5jb21tZW50TGluZSA9IGZhbHNlO1xuICAgIH1cbiAgICB2YXIgY2ggPSBzdHJlYW0ubmV4dCgpLnRvU3RyaW5nKCk7XG4gICAgaWYgKHJlc2VydmUuaW5kZXhPZihjaCkgIT09IC0xKSB7XG4gICAgICBpZiAoc3RhdGUuY29tbWVudExpbmUgPT09IHRydWUpIHtcbiAgICAgICAgaWYgKHN0cmVhbS5lb2woKSkge1xuICAgICAgICAgIHN0YXRlLmNvbW1lbnRMaW5lID0gZmFsc2U7XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICAgICAgfVxuICAgICAgaWYgKGNoID09PSBcIl1cIiB8fCBjaCA9PT0gXCJbXCIpIHtcbiAgICAgICAgaWYgKGNoID09PSBcIltcIikge1xuICAgICAgICAgIHN0YXRlLmxlZnQrKztcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICBzdGF0ZS5yaWdodCsrO1xuICAgICAgICB9XG4gICAgICAgIHJldHVybiBcImJyYWNrZXRcIjtcbiAgICAgIH0gZWxzZSBpZiAoY2ggPT09IFwiK1wiIHx8IGNoID09PSBcIi1cIikge1xuICAgICAgICByZXR1cm4gXCJrZXl3b3JkXCI7XG4gICAgICB9IGVsc2UgaWYgKGNoID09PSBcIjxcIiB8fCBjaCA9PT0gXCI+XCIpIHtcbiAgICAgICAgcmV0dXJuIFwiYXRvbVwiO1xuICAgICAgfSBlbHNlIGlmIChjaCA9PT0gXCIuXCIgfHwgY2ggPT09IFwiLFwiKSB7XG4gICAgICAgIHJldHVybiBcImRlZlwiO1xuICAgICAgfVxuICAgIH0gZWxzZSB7XG4gICAgICBzdGF0ZS5jb21tZW50TGluZSA9IHRydWU7XG4gICAgICBpZiAoc3RyZWFtLmVvbCgpKSB7XG4gICAgICAgIHN0YXRlLmNvbW1lbnRMaW5lID0gZmFsc2U7XG4gICAgICB9XG4gICAgICByZXR1cm4gXCJjb21tZW50XCI7XG4gICAgfVxuICAgIGlmIChzdHJlYW0uZW9sKCkpIHtcbiAgICAgIHN0YXRlLmNvbW1lbnRMaW5lID0gZmFsc2U7XG4gICAgfVxuICB9XG59OyJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==