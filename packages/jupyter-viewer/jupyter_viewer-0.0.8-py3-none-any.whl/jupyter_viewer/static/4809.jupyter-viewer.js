"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[4809],{

/***/ 14809:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "spreadsheet": () => (/* binding */ spreadsheet)
/* harmony export */ });
const spreadsheet = {
  name: "spreadsheet",
  startState: function () {
    return {
      stringType: null,
      stack: []
    };
  },
  token: function (stream, state) {
    if (!stream) return;

    //check for state changes
    if (state.stack.length === 0) {
      //strings
      if (stream.peek() == '"' || stream.peek() == "'") {
        state.stringType = stream.peek();
        stream.next(); // Skip quote
        state.stack.unshift("string");
      }
    }

    //return state
    //stack has
    switch (state.stack[0]) {
      case "string":
        while (state.stack[0] === "string" && !stream.eol()) {
          if (stream.peek() === state.stringType) {
            stream.next(); // Skip quote
            state.stack.shift(); // Clear flag
          } else if (stream.peek() === "\\") {
            stream.next();
            stream.next();
          } else {
            stream.match(/^.[^\\\"\']*/);
          }
        }
        return "string";
      case "characterClass":
        while (state.stack[0] === "characterClass" && !stream.eol()) {
          if (!(stream.match(/^[^\]\\]+/) || stream.match(/^\\./))) state.stack.shift();
        }
        return "operator";
    }
    var peek = stream.peek();

    //no stack
    switch (peek) {
      case "[":
        stream.next();
        state.stack.unshift("characterClass");
        return "bracket";
      case ":":
        stream.next();
        return "operator";
      case "\\":
        if (stream.match(/\\[a-z]+/)) return "string.special";else {
          stream.next();
          return "atom";
        }
      case ".":
      case ",":
      case ";":
      case "*":
      case "-":
      case "+":
      case "^":
      case "<":
      case "/":
      case "=":
        stream.next();
        return "atom";
      case "$":
        stream.next();
        return "builtin";
    }
    if (stream.match(/\d+/)) {
      if (stream.match(/^\w+/)) return "error";
      return "number";
    } else if (stream.match(/^[a-zA-Z_]\w*/)) {
      if (stream.match(/(?=[\(.])/, false)) return "keyword";
      return "variable";
    } else if (["[", "]", "(", ")", "{", "}"].indexOf(peek) != -1) {
      stream.next();
      return "bracket";
    } else if (!stream.eatSpace()) {
      stream.next();
    }
    return null;
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNDgwOS5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9AY29kZW1pcnJvci9sZWdhY3ktbW9kZXMvbW9kZS9zcHJlYWRzaGVldC5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyJleHBvcnQgY29uc3Qgc3ByZWFkc2hlZXQgPSB7XG4gIG5hbWU6IFwic3ByZWFkc2hlZXRcIixcbiAgc3RhcnRTdGF0ZTogZnVuY3Rpb24gKCkge1xuICAgIHJldHVybiB7XG4gICAgICBzdHJpbmdUeXBlOiBudWxsLFxuICAgICAgc3RhY2s6IFtdXG4gICAgfTtcbiAgfSxcbiAgdG9rZW46IGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgaWYgKCFzdHJlYW0pIHJldHVybjtcblxuICAgIC8vY2hlY2sgZm9yIHN0YXRlIGNoYW5nZXNcbiAgICBpZiAoc3RhdGUuc3RhY2subGVuZ3RoID09PSAwKSB7XG4gICAgICAvL3N0cmluZ3NcbiAgICAgIGlmIChzdHJlYW0ucGVlaygpID09ICdcIicgfHwgc3RyZWFtLnBlZWsoKSA9PSBcIidcIikge1xuICAgICAgICBzdGF0ZS5zdHJpbmdUeXBlID0gc3RyZWFtLnBlZWsoKTtcbiAgICAgICAgc3RyZWFtLm5leHQoKTsgLy8gU2tpcCBxdW90ZVxuICAgICAgICBzdGF0ZS5zdGFjay51bnNoaWZ0KFwic3RyaW5nXCIpO1xuICAgICAgfVxuICAgIH1cblxuICAgIC8vcmV0dXJuIHN0YXRlXG4gICAgLy9zdGFjayBoYXNcbiAgICBzd2l0Y2ggKHN0YXRlLnN0YWNrWzBdKSB7XG4gICAgICBjYXNlIFwic3RyaW5nXCI6XG4gICAgICAgIHdoaWxlIChzdGF0ZS5zdGFja1swXSA9PT0gXCJzdHJpbmdcIiAmJiAhc3RyZWFtLmVvbCgpKSB7XG4gICAgICAgICAgaWYgKHN0cmVhbS5wZWVrKCkgPT09IHN0YXRlLnN0cmluZ1R5cGUpIHtcbiAgICAgICAgICAgIHN0cmVhbS5uZXh0KCk7IC8vIFNraXAgcXVvdGVcbiAgICAgICAgICAgIHN0YXRlLnN0YWNrLnNoaWZ0KCk7IC8vIENsZWFyIGZsYWdcbiAgICAgICAgICB9IGVsc2UgaWYgKHN0cmVhbS5wZWVrKCkgPT09IFwiXFxcXFwiKSB7XG4gICAgICAgICAgICBzdHJlYW0ubmV4dCgpO1xuICAgICAgICAgICAgc3RyZWFtLm5leHQoKTtcbiAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgc3RyZWFtLm1hdGNoKC9eLlteXFxcXFxcXCJcXCddKi8pO1xuICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gXCJzdHJpbmdcIjtcbiAgICAgIGNhc2UgXCJjaGFyYWN0ZXJDbGFzc1wiOlxuICAgICAgICB3aGlsZSAoc3RhdGUuc3RhY2tbMF0gPT09IFwiY2hhcmFjdGVyQ2xhc3NcIiAmJiAhc3RyZWFtLmVvbCgpKSB7XG4gICAgICAgICAgaWYgKCEoc3RyZWFtLm1hdGNoKC9eW15cXF1cXFxcXSsvKSB8fCBzdHJlYW0ubWF0Y2goL15cXFxcLi8pKSkgc3RhdGUuc3RhY2suc2hpZnQoKTtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gXCJvcGVyYXRvclwiO1xuICAgIH1cbiAgICB2YXIgcGVlayA9IHN0cmVhbS5wZWVrKCk7XG5cbiAgICAvL25vIHN0YWNrXG4gICAgc3dpdGNoIChwZWVrKSB7XG4gICAgICBjYXNlIFwiW1wiOlxuICAgICAgICBzdHJlYW0ubmV4dCgpO1xuICAgICAgICBzdGF0ZS5zdGFjay51bnNoaWZ0KFwiY2hhcmFjdGVyQ2xhc3NcIik7XG4gICAgICAgIHJldHVybiBcImJyYWNrZXRcIjtcbiAgICAgIGNhc2UgXCI6XCI6XG4gICAgICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgICAgIHJldHVybiBcIm9wZXJhdG9yXCI7XG4gICAgICBjYXNlIFwiXFxcXFwiOlxuICAgICAgICBpZiAoc3RyZWFtLm1hdGNoKC9cXFxcW2Etel0rLykpIHJldHVybiBcInN0cmluZy5zcGVjaWFsXCI7ZWxzZSB7XG4gICAgICAgICAgc3RyZWFtLm5leHQoKTtcbiAgICAgICAgICByZXR1cm4gXCJhdG9tXCI7XG4gICAgICAgIH1cbiAgICAgIGNhc2UgXCIuXCI6XG4gICAgICBjYXNlIFwiLFwiOlxuICAgICAgY2FzZSBcIjtcIjpcbiAgICAgIGNhc2UgXCIqXCI6XG4gICAgICBjYXNlIFwiLVwiOlxuICAgICAgY2FzZSBcIitcIjpcbiAgICAgIGNhc2UgXCJeXCI6XG4gICAgICBjYXNlIFwiPFwiOlxuICAgICAgY2FzZSBcIi9cIjpcbiAgICAgIGNhc2UgXCI9XCI6XG4gICAgICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgICAgIHJldHVybiBcImF0b21cIjtcbiAgICAgIGNhc2UgXCIkXCI6XG4gICAgICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgICAgIHJldHVybiBcImJ1aWx0aW5cIjtcbiAgICB9XG4gICAgaWYgKHN0cmVhbS5tYXRjaCgvXFxkKy8pKSB7XG4gICAgICBpZiAoc3RyZWFtLm1hdGNoKC9eXFx3Ky8pKSByZXR1cm4gXCJlcnJvclwiO1xuICAgICAgcmV0dXJuIFwibnVtYmVyXCI7XG4gICAgfSBlbHNlIGlmIChzdHJlYW0ubWF0Y2goL15bYS16QS1aX11cXHcqLykpIHtcbiAgICAgIGlmIChzdHJlYW0ubWF0Y2goLyg/PVtcXCguXSkvLCBmYWxzZSkpIHJldHVybiBcImtleXdvcmRcIjtcbiAgICAgIHJldHVybiBcInZhcmlhYmxlXCI7XG4gICAgfSBlbHNlIGlmIChbXCJbXCIsIFwiXVwiLCBcIihcIiwgXCIpXCIsIFwie1wiLCBcIn1cIl0uaW5kZXhPZihwZWVrKSAhPSAtMSkge1xuICAgICAgc3RyZWFtLm5leHQoKTtcbiAgICAgIHJldHVybiBcImJyYWNrZXRcIjtcbiAgICB9IGVsc2UgaWYgKCFzdHJlYW0uZWF0U3BhY2UoKSkge1xuICAgICAgc3RyZWFtLm5leHQoKTtcbiAgICB9XG4gICAgcmV0dXJuIG51bGw7XG4gIH1cbn07Il0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9