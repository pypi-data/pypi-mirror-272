"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[8568],{

/***/ 8568:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ebnf": () => (/* binding */ ebnf)
/* harmony export */ });
var commentType = {
  slash: 0,
  parenthesis: 1
};
var stateType = {
  comment: 0,
  _string: 1,
  characterClass: 2
};
const ebnf = {
  name: "ebnf",
  startState: function () {
    return {
      stringType: null,
      commentType: null,
      braced: 0,
      lhs: true,
      localState: null,
      stack: [],
      inDefinition: false
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
        state.stack.unshift(stateType._string);
      } else if (stream.match('/*')) {
        //comments starting with /*
        state.stack.unshift(stateType.comment);
        state.commentType = commentType.slash;
      } else if (stream.match('(*')) {
        //comments starting with (*
        state.stack.unshift(stateType.comment);
        state.commentType = commentType.parenthesis;
      }
    }

    //return state
    //stack has
    switch (state.stack[0]) {
      case stateType._string:
        while (state.stack[0] === stateType._string && !stream.eol()) {
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
        return state.lhs ? "property" : "string";
      // Token style

      case stateType.comment:
        while (state.stack[0] === stateType.comment && !stream.eol()) {
          if (state.commentType === commentType.slash && stream.match('*/')) {
            state.stack.shift(); // Clear flag
            state.commentType = null;
          } else if (state.commentType === commentType.parenthesis && stream.match('*)')) {
            state.stack.shift(); // Clear flag
            state.commentType = null;
          } else {
            stream.match(/^.[^\*]*/);
          }
        }
        return "comment";
      case stateType.characterClass:
        while (state.stack[0] === stateType.characterClass && !stream.eol()) {
          if (!(stream.match(/^[^\]\\]+/) || stream.match('.'))) {
            state.stack.shift();
          }
        }
        return "operator";
    }
    var peek = stream.peek();

    //no stack
    switch (peek) {
      case "[":
        stream.next();
        state.stack.unshift(stateType.characterClass);
        return "bracket";
      case ":":
      case "|":
      case ";":
        stream.next();
        return "operator";
      case "%":
        if (stream.match("%%")) {
          return "header";
        } else if (stream.match(/[%][A-Za-z]+/)) {
          return "keyword";
        } else if (stream.match(/[%][}]/)) {
          return "bracket";
        }
        break;
      case "/":
        if (stream.match(/[\/][A-Za-z]+/)) {
          return "keyword";
        }
      case "\\":
        if (stream.match(/[\][a-z]+/)) {
          return "string.special";
        }
      case ".":
        if (stream.match(".")) {
          return "atom";
        }
      case "*":
      case "-":
      case "+":
      case "^":
        if (stream.match(peek)) {
          return "atom";
        }
      case "$":
        if (stream.match("$$")) {
          return "builtin";
        } else if (stream.match(/[$][0-9]+/)) {
          return "variableName.special";
        }
      case "<":
        if (stream.match(/<<[a-zA-Z_]+>>/)) {
          return "builtin";
        }
    }
    if (stream.match('//')) {
      stream.skipToEnd();
      return "comment";
    } else if (stream.match('return')) {
      return "operator";
    } else if (stream.match(/^[a-zA-Z_][a-zA-Z0-9_]*/)) {
      if (stream.match(/(?=[\(.])/)) {
        return "variable";
      } else if (stream.match(/(?=[\s\n]*[:=])/)) {
        return "def";
      }
      return "variableName.special";
    } else if (["[", "]", "(", ")"].indexOf(stream.peek()) != -1) {
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
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiODU2OC5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGNvZGVtaXJyb3IvbGVnYWN5LW1vZGVzL21vZGUvZWJuZi5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyJ2YXIgY29tbWVudFR5cGUgPSB7XG4gIHNsYXNoOiAwLFxuICBwYXJlbnRoZXNpczogMVxufTtcbnZhciBzdGF0ZVR5cGUgPSB7XG4gIGNvbW1lbnQ6IDAsXG4gIF9zdHJpbmc6IDEsXG4gIGNoYXJhY3RlckNsYXNzOiAyXG59O1xuZXhwb3J0IGNvbnN0IGVibmYgPSB7XG4gIG5hbWU6IFwiZWJuZlwiLFxuICBzdGFydFN0YXRlOiBmdW5jdGlvbiAoKSB7XG4gICAgcmV0dXJuIHtcbiAgICAgIHN0cmluZ1R5cGU6IG51bGwsXG4gICAgICBjb21tZW50VHlwZTogbnVsbCxcbiAgICAgIGJyYWNlZDogMCxcbiAgICAgIGxoczogdHJ1ZSxcbiAgICAgIGxvY2FsU3RhdGU6IG51bGwsXG4gICAgICBzdGFjazogW10sXG4gICAgICBpbkRlZmluaXRpb246IGZhbHNlXG4gICAgfTtcbiAgfSxcbiAgdG9rZW46IGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgaWYgKCFzdHJlYW0pIHJldHVybjtcblxuICAgIC8vY2hlY2sgZm9yIHN0YXRlIGNoYW5nZXNcbiAgICBpZiAoc3RhdGUuc3RhY2subGVuZ3RoID09PSAwKSB7XG4gICAgICAvL3N0cmluZ3NcbiAgICAgIGlmIChzdHJlYW0ucGVlaygpID09ICdcIicgfHwgc3RyZWFtLnBlZWsoKSA9PSBcIidcIikge1xuICAgICAgICBzdGF0ZS5zdHJpbmdUeXBlID0gc3RyZWFtLnBlZWsoKTtcbiAgICAgICAgc3RyZWFtLm5leHQoKTsgLy8gU2tpcCBxdW90ZVxuICAgICAgICBzdGF0ZS5zdGFjay51bnNoaWZ0KHN0YXRlVHlwZS5fc3RyaW5nKTtcbiAgICAgIH0gZWxzZSBpZiAoc3RyZWFtLm1hdGNoKCcvKicpKSB7XG4gICAgICAgIC8vY29tbWVudHMgc3RhcnRpbmcgd2l0aCAvKlxuICAgICAgICBzdGF0ZS5zdGFjay51bnNoaWZ0KHN0YXRlVHlwZS5jb21tZW50KTtcbiAgICAgICAgc3RhdGUuY29tbWVudFR5cGUgPSBjb21tZW50VHlwZS5zbGFzaDtcbiAgICAgIH0gZWxzZSBpZiAoc3RyZWFtLm1hdGNoKCcoKicpKSB7XG4gICAgICAgIC8vY29tbWVudHMgc3RhcnRpbmcgd2l0aCAoKlxuICAgICAgICBzdGF0ZS5zdGFjay51bnNoaWZ0KHN0YXRlVHlwZS5jb21tZW50KTtcbiAgICAgICAgc3RhdGUuY29tbWVudFR5cGUgPSBjb21tZW50VHlwZS5wYXJlbnRoZXNpcztcbiAgICAgIH1cbiAgICB9XG5cbiAgICAvL3JldHVybiBzdGF0ZVxuICAgIC8vc3RhY2sgaGFzXG4gICAgc3dpdGNoIChzdGF0ZS5zdGFja1swXSkge1xuICAgICAgY2FzZSBzdGF0ZVR5cGUuX3N0cmluZzpcbiAgICAgICAgd2hpbGUgKHN0YXRlLnN0YWNrWzBdID09PSBzdGF0ZVR5cGUuX3N0cmluZyAmJiAhc3RyZWFtLmVvbCgpKSB7XG4gICAgICAgICAgaWYgKHN0cmVhbS5wZWVrKCkgPT09IHN0YXRlLnN0cmluZ1R5cGUpIHtcbiAgICAgICAgICAgIHN0cmVhbS5uZXh0KCk7IC8vIFNraXAgcXVvdGVcbiAgICAgICAgICAgIHN0YXRlLnN0YWNrLnNoaWZ0KCk7IC8vIENsZWFyIGZsYWdcbiAgICAgICAgICB9IGVsc2UgaWYgKHN0cmVhbS5wZWVrKCkgPT09IFwiXFxcXFwiKSB7XG4gICAgICAgICAgICBzdHJlYW0ubmV4dCgpO1xuICAgICAgICAgICAgc3RyZWFtLm5leHQoKTtcbiAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgc3RyZWFtLm1hdGNoKC9eLlteXFxcXFxcXCJcXCddKi8pO1xuICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gc3RhdGUubGhzID8gXCJwcm9wZXJ0eVwiIDogXCJzdHJpbmdcIjtcbiAgICAgIC8vIFRva2VuIHN0eWxlXG5cbiAgICAgIGNhc2Ugc3RhdGVUeXBlLmNvbW1lbnQ6XG4gICAgICAgIHdoaWxlIChzdGF0ZS5zdGFja1swXSA9PT0gc3RhdGVUeXBlLmNvbW1lbnQgJiYgIXN0cmVhbS5lb2woKSkge1xuICAgICAgICAgIGlmIChzdGF0ZS5jb21tZW50VHlwZSA9PT0gY29tbWVudFR5cGUuc2xhc2ggJiYgc3RyZWFtLm1hdGNoKCcqLycpKSB7XG4gICAgICAgICAgICBzdGF0ZS5zdGFjay5zaGlmdCgpOyAvLyBDbGVhciBmbGFnXG4gICAgICAgICAgICBzdGF0ZS5jb21tZW50VHlwZSA9IG51bGw7XG4gICAgICAgICAgfSBlbHNlIGlmIChzdGF0ZS5jb21tZW50VHlwZSA9PT0gY29tbWVudFR5cGUucGFyZW50aGVzaXMgJiYgc3RyZWFtLm1hdGNoKCcqKScpKSB7XG4gICAgICAgICAgICBzdGF0ZS5zdGFjay5zaGlmdCgpOyAvLyBDbGVhciBmbGFnXG4gICAgICAgICAgICBzdGF0ZS5jb21tZW50VHlwZSA9IG51bGw7XG4gICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIHN0cmVhbS5tYXRjaCgvXi5bXlxcKl0qLyk7XG4gICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICAgIHJldHVybiBcImNvbW1lbnRcIjtcbiAgICAgIGNhc2Ugc3RhdGVUeXBlLmNoYXJhY3RlckNsYXNzOlxuICAgICAgICB3aGlsZSAoc3RhdGUuc3RhY2tbMF0gPT09IHN0YXRlVHlwZS5jaGFyYWN0ZXJDbGFzcyAmJiAhc3RyZWFtLmVvbCgpKSB7XG4gICAgICAgICAgaWYgKCEoc3RyZWFtLm1hdGNoKC9eW15cXF1cXFxcXSsvKSB8fCBzdHJlYW0ubWF0Y2goJy4nKSkpIHtcbiAgICAgICAgICAgIHN0YXRlLnN0YWNrLnNoaWZ0KCk7XG4gICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICAgIHJldHVybiBcIm9wZXJhdG9yXCI7XG4gICAgfVxuICAgIHZhciBwZWVrID0gc3RyZWFtLnBlZWsoKTtcblxuICAgIC8vbm8gc3RhY2tcbiAgICBzd2l0Y2ggKHBlZWspIHtcbiAgICAgIGNhc2UgXCJbXCI6XG4gICAgICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgICAgIHN0YXRlLnN0YWNrLnVuc2hpZnQoc3RhdGVUeXBlLmNoYXJhY3RlckNsYXNzKTtcbiAgICAgICAgcmV0dXJuIFwiYnJhY2tldFwiO1xuICAgICAgY2FzZSBcIjpcIjpcbiAgICAgIGNhc2UgXCJ8XCI6XG4gICAgICBjYXNlIFwiO1wiOlxuICAgICAgICBzdHJlYW0ubmV4dCgpO1xuICAgICAgICByZXR1cm4gXCJvcGVyYXRvclwiO1xuICAgICAgY2FzZSBcIiVcIjpcbiAgICAgICAgaWYgKHN0cmVhbS5tYXRjaChcIiUlXCIpKSB7XG4gICAgICAgICAgcmV0dXJuIFwiaGVhZGVyXCI7XG4gICAgICAgIH0gZWxzZSBpZiAoc3RyZWFtLm1hdGNoKC9bJV1bQS1aYS16XSsvKSkge1xuICAgICAgICAgIHJldHVybiBcImtleXdvcmRcIjtcbiAgICAgICAgfSBlbHNlIGlmIChzdHJlYW0ubWF0Y2goL1slXVt9XS8pKSB7XG4gICAgICAgICAgcmV0dXJuIFwiYnJhY2tldFwiO1xuICAgICAgICB9XG4gICAgICAgIGJyZWFrO1xuICAgICAgY2FzZSBcIi9cIjpcbiAgICAgICAgaWYgKHN0cmVhbS5tYXRjaCgvW1xcL11bQS1aYS16XSsvKSkge1xuICAgICAgICAgIHJldHVybiBcImtleXdvcmRcIjtcbiAgICAgICAgfVxuICAgICAgY2FzZSBcIlxcXFxcIjpcbiAgICAgICAgaWYgKHN0cmVhbS5tYXRjaCgvW1xcXVthLXpdKy8pKSB7XG4gICAgICAgICAgcmV0dXJuIFwic3RyaW5nLnNwZWNpYWxcIjtcbiAgICAgICAgfVxuICAgICAgY2FzZSBcIi5cIjpcbiAgICAgICAgaWYgKHN0cmVhbS5tYXRjaChcIi5cIikpIHtcbiAgICAgICAgICByZXR1cm4gXCJhdG9tXCI7XG4gICAgICAgIH1cbiAgICAgIGNhc2UgXCIqXCI6XG4gICAgICBjYXNlIFwiLVwiOlxuICAgICAgY2FzZSBcIitcIjpcbiAgICAgIGNhc2UgXCJeXCI6XG4gICAgICAgIGlmIChzdHJlYW0ubWF0Y2gocGVlaykpIHtcbiAgICAgICAgICByZXR1cm4gXCJhdG9tXCI7XG4gICAgICAgIH1cbiAgICAgIGNhc2UgXCIkXCI6XG4gICAgICAgIGlmIChzdHJlYW0ubWF0Y2goXCIkJFwiKSkge1xuICAgICAgICAgIHJldHVybiBcImJ1aWx0aW5cIjtcbiAgICAgICAgfSBlbHNlIGlmIChzdHJlYW0ubWF0Y2goL1skXVswLTldKy8pKSB7XG4gICAgICAgICAgcmV0dXJuIFwidmFyaWFibGVOYW1lLnNwZWNpYWxcIjtcbiAgICAgICAgfVxuICAgICAgY2FzZSBcIjxcIjpcbiAgICAgICAgaWYgKHN0cmVhbS5tYXRjaCgvPDxbYS16QS1aX10rPj4vKSkge1xuICAgICAgICAgIHJldHVybiBcImJ1aWx0aW5cIjtcbiAgICAgICAgfVxuICAgIH1cbiAgICBpZiAoc3RyZWFtLm1hdGNoKCcvLycpKSB7XG4gICAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgICByZXR1cm4gXCJjb21tZW50XCI7XG4gICAgfSBlbHNlIGlmIChzdHJlYW0ubWF0Y2goJ3JldHVybicpKSB7XG4gICAgICByZXR1cm4gXCJvcGVyYXRvclwiO1xuICAgIH0gZWxzZSBpZiAoc3RyZWFtLm1hdGNoKC9eW2EtekEtWl9dW2EtekEtWjAtOV9dKi8pKSB7XG4gICAgICBpZiAoc3RyZWFtLm1hdGNoKC8oPz1bXFwoLl0pLykpIHtcbiAgICAgICAgcmV0dXJuIFwidmFyaWFibGVcIjtcbiAgICAgIH0gZWxzZSBpZiAoc3RyZWFtLm1hdGNoKC8oPz1bXFxzXFxuXSpbOj1dKS8pKSB7XG4gICAgICAgIHJldHVybiBcImRlZlwiO1xuICAgICAgfVxuICAgICAgcmV0dXJuIFwidmFyaWFibGVOYW1lLnNwZWNpYWxcIjtcbiAgICB9IGVsc2UgaWYgKFtcIltcIiwgXCJdXCIsIFwiKFwiLCBcIilcIl0uaW5kZXhPZihzdHJlYW0ucGVlaygpKSAhPSAtMSkge1xuICAgICAgc3RyZWFtLm5leHQoKTtcbiAgICAgIHJldHVybiBcImJyYWNrZXRcIjtcbiAgICB9IGVsc2UgaWYgKCFzdHJlYW0uZWF0U3BhY2UoKSkge1xuICAgICAgc3RyZWFtLm5leHQoKTtcbiAgICB9XG4gICAgcmV0dXJuIG51bGw7XG4gIH1cbn07Il0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9