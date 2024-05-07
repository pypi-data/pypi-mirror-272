"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[2839],{

/***/ 2839:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "toml": () => (/* binding */ toml)
/* harmony export */ });
const toml = {
  name: "toml",
  startState: function () {
    return {
      inString: false,
      stringType: "",
      lhs: true,
      inArray: 0
    };
  },
  token: function (stream, state) {
    //check for state changes
    if (!state.inString && (stream.peek() == '"' || stream.peek() == "'")) {
      state.stringType = stream.peek();
      stream.next(); // Skip quote
      state.inString = true; // Update state
    }
    if (stream.sol() && state.inArray === 0) {
      state.lhs = true;
    }
    //return state
    if (state.inString) {
      while (state.inString && !stream.eol()) {
        if (stream.peek() === state.stringType) {
          stream.next(); // Skip quote
          state.inString = false; // Clear flag
        } else if (stream.peek() === '\\') {
          stream.next();
          stream.next();
        } else {
          stream.match(/^.[^\\\"\']*/);
        }
      }
      return state.lhs ? "property" : "string"; // Token style
    } else if (state.inArray && stream.peek() === ']') {
      stream.next();
      state.inArray--;
      return 'bracket';
    } else if (state.lhs && stream.peek() === '[' && stream.skipTo(']')) {
      stream.next(); //skip closing ]
      // array of objects has an extra open & close []
      if (stream.peek() === ']') stream.next();
      return "atom";
    } else if (stream.peek() === "#") {
      stream.skipToEnd();
      return "comment";
    } else if (stream.eatSpace()) {
      return null;
    } else if (state.lhs && stream.eatWhile(function (c) {
      return c != '=' && c != ' ';
    })) {
      return "property";
    } else if (state.lhs && stream.peek() === "=") {
      stream.next();
      state.lhs = false;
      return null;
    } else if (!state.lhs && stream.match(/^\d\d\d\d[\d\-\:\.T]*Z/)) {
      return 'atom'; //date
    } else if (!state.lhs && (stream.match('true') || stream.match('false'))) {
      return 'atom';
    } else if (!state.lhs && stream.peek() === '[') {
      state.inArray++;
      stream.next();
      return 'bracket';
    } else if (!state.lhs && stream.match(/^\-?\d+(?:\.\d+)?/)) {
      return 'number';
    } else if (!stream.eatSpace()) {
      stream.next();
    }
    return null;
  },
  languageData: {
    commentTokens: {
      line: '#'
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiMjgzOS5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGNvZGVtaXJyb3IvbGVnYWN5LW1vZGVzL21vZGUvdG9tbC5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyJleHBvcnQgY29uc3QgdG9tbCA9IHtcbiAgbmFtZTogXCJ0b21sXCIsXG4gIHN0YXJ0U3RhdGU6IGZ1bmN0aW9uICgpIHtcbiAgICByZXR1cm4ge1xuICAgICAgaW5TdHJpbmc6IGZhbHNlLFxuICAgICAgc3RyaW5nVHlwZTogXCJcIixcbiAgICAgIGxoczogdHJ1ZSxcbiAgICAgIGluQXJyYXk6IDBcbiAgICB9O1xuICB9LFxuICB0b2tlbjogZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICAvL2NoZWNrIGZvciBzdGF0ZSBjaGFuZ2VzXG4gICAgaWYgKCFzdGF0ZS5pblN0cmluZyAmJiAoc3RyZWFtLnBlZWsoKSA9PSAnXCInIHx8IHN0cmVhbS5wZWVrKCkgPT0gXCInXCIpKSB7XG4gICAgICBzdGF0ZS5zdHJpbmdUeXBlID0gc3RyZWFtLnBlZWsoKTtcbiAgICAgIHN0cmVhbS5uZXh0KCk7IC8vIFNraXAgcXVvdGVcbiAgICAgIHN0YXRlLmluU3RyaW5nID0gdHJ1ZTsgLy8gVXBkYXRlIHN0YXRlXG4gICAgfVxuICAgIGlmIChzdHJlYW0uc29sKCkgJiYgc3RhdGUuaW5BcnJheSA9PT0gMCkge1xuICAgICAgc3RhdGUubGhzID0gdHJ1ZTtcbiAgICB9XG4gICAgLy9yZXR1cm4gc3RhdGVcbiAgICBpZiAoc3RhdGUuaW5TdHJpbmcpIHtcbiAgICAgIHdoaWxlIChzdGF0ZS5pblN0cmluZyAmJiAhc3RyZWFtLmVvbCgpKSB7XG4gICAgICAgIGlmIChzdHJlYW0ucGVlaygpID09PSBzdGF0ZS5zdHJpbmdUeXBlKSB7XG4gICAgICAgICAgc3RyZWFtLm5leHQoKTsgLy8gU2tpcCBxdW90ZVxuICAgICAgICAgIHN0YXRlLmluU3RyaW5nID0gZmFsc2U7IC8vIENsZWFyIGZsYWdcbiAgICAgICAgfSBlbHNlIGlmIChzdHJlYW0ucGVlaygpID09PSAnXFxcXCcpIHtcbiAgICAgICAgICBzdHJlYW0ubmV4dCgpO1xuICAgICAgICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgc3RyZWFtLm1hdGNoKC9eLlteXFxcXFxcXCJcXCddKi8pO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgICByZXR1cm4gc3RhdGUubGhzID8gXCJwcm9wZXJ0eVwiIDogXCJzdHJpbmdcIjsgLy8gVG9rZW4gc3R5bGVcbiAgICB9IGVsc2UgaWYgKHN0YXRlLmluQXJyYXkgJiYgc3RyZWFtLnBlZWsoKSA9PT0gJ10nKSB7XG4gICAgICBzdHJlYW0ubmV4dCgpO1xuICAgICAgc3RhdGUuaW5BcnJheS0tO1xuICAgICAgcmV0dXJuICdicmFja2V0JztcbiAgICB9IGVsc2UgaWYgKHN0YXRlLmxocyAmJiBzdHJlYW0ucGVlaygpID09PSAnWycgJiYgc3RyZWFtLnNraXBUbygnXScpKSB7XG4gICAgICBzdHJlYW0ubmV4dCgpOyAvL3NraXAgY2xvc2luZyBdXG4gICAgICAvLyBhcnJheSBvZiBvYmplY3RzIGhhcyBhbiBleHRyYSBvcGVuICYgY2xvc2UgW11cbiAgICAgIGlmIChzdHJlYW0ucGVlaygpID09PSAnXScpIHN0cmVhbS5uZXh0KCk7XG4gICAgICByZXR1cm4gXCJhdG9tXCI7XG4gICAgfSBlbHNlIGlmIChzdHJlYW0ucGVlaygpID09PSBcIiNcIikge1xuICAgICAgc3RyZWFtLnNraXBUb0VuZCgpO1xuICAgICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICAgIH0gZWxzZSBpZiAoc3RyZWFtLmVhdFNwYWNlKCkpIHtcbiAgICAgIHJldHVybiBudWxsO1xuICAgIH0gZWxzZSBpZiAoc3RhdGUubGhzICYmIHN0cmVhbS5lYXRXaGlsZShmdW5jdGlvbiAoYykge1xuICAgICAgcmV0dXJuIGMgIT0gJz0nICYmIGMgIT0gJyAnO1xuICAgIH0pKSB7XG4gICAgICByZXR1cm4gXCJwcm9wZXJ0eVwiO1xuICAgIH0gZWxzZSBpZiAoc3RhdGUubGhzICYmIHN0cmVhbS5wZWVrKCkgPT09IFwiPVwiKSB7XG4gICAgICBzdHJlYW0ubmV4dCgpO1xuICAgICAgc3RhdGUubGhzID0gZmFsc2U7XG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9IGVsc2UgaWYgKCFzdGF0ZS5saHMgJiYgc3RyZWFtLm1hdGNoKC9eXFxkXFxkXFxkXFxkW1xcZFxcLVxcOlxcLlRdKlovKSkge1xuICAgICAgcmV0dXJuICdhdG9tJzsgLy9kYXRlXG4gICAgfSBlbHNlIGlmICghc3RhdGUubGhzICYmIChzdHJlYW0ubWF0Y2goJ3RydWUnKSB8fCBzdHJlYW0ubWF0Y2goJ2ZhbHNlJykpKSB7XG4gICAgICByZXR1cm4gJ2F0b20nO1xuICAgIH0gZWxzZSBpZiAoIXN0YXRlLmxocyAmJiBzdHJlYW0ucGVlaygpID09PSAnWycpIHtcbiAgICAgIHN0YXRlLmluQXJyYXkrKztcbiAgICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgICByZXR1cm4gJ2JyYWNrZXQnO1xuICAgIH0gZWxzZSBpZiAoIXN0YXRlLmxocyAmJiBzdHJlYW0ubWF0Y2goL15cXC0/XFxkKyg/OlxcLlxcZCspPy8pKSB7XG4gICAgICByZXR1cm4gJ251bWJlcic7XG4gICAgfSBlbHNlIGlmICghc3RyZWFtLmVhdFNwYWNlKCkpIHtcbiAgICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgfVxuICAgIHJldHVybiBudWxsO1xuICB9LFxuICBsYW5ndWFnZURhdGE6IHtcbiAgICBjb21tZW50VG9rZW5zOiB7XG4gICAgICBsaW5lOiAnIydcbiAgICB9XG4gIH1cbn07Il0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9