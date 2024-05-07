"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[3554],{

/***/ 63554:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "yaml": () => (/* binding */ yaml)
/* harmony export */ });
var cons = ['true', 'false', 'on', 'off', 'yes', 'no'];
var keywordRegex = new RegExp("\\b((" + cons.join(")|(") + "))$", 'i');
const yaml = {
  name: "yaml",
  token: function (stream, state) {
    var ch = stream.peek();
    var esc = state.escaped;
    state.escaped = false;
    /* comments */
    if (ch == "#" && (stream.pos == 0 || /\s/.test(stream.string.charAt(stream.pos - 1)))) {
      stream.skipToEnd();
      return "comment";
    }
    if (stream.match(/^('([^']|\\.)*'?|"([^"]|\\.)*"?)/)) return "string";
    if (state.literal && stream.indentation() > state.keyCol) {
      stream.skipToEnd();
      return "string";
    } else if (state.literal) {
      state.literal = false;
    }
    if (stream.sol()) {
      state.keyCol = 0;
      state.pair = false;
      state.pairStart = false;
      /* document start */
      if (stream.match('---')) {
        return "def";
      }
      /* document end */
      if (stream.match('...')) {
        return "def";
      }
      /* array list item */
      if (stream.match(/^\s*-\s+/)) {
        return 'meta';
      }
    }
    /* inline pairs/lists */
    if (stream.match(/^(\{|\}|\[|\])/)) {
      if (ch == '{') state.inlinePairs++;else if (ch == '}') state.inlinePairs--;else if (ch == '[') state.inlineList++;else state.inlineList--;
      return 'meta';
    }

    /* list separator */
    if (state.inlineList > 0 && !esc && ch == ',') {
      stream.next();
      return 'meta';
    }
    /* pairs separator */
    if (state.inlinePairs > 0 && !esc && ch == ',') {
      state.keyCol = 0;
      state.pair = false;
      state.pairStart = false;
      stream.next();
      return 'meta';
    }

    /* start of value of a pair */
    if (state.pairStart) {
      /* block literals */
      if (stream.match(/^\s*(\||\>)\s*/)) {
        state.literal = true;
        return 'meta';
      }
      ;
      /* references */
      if (stream.match(/^\s*(\&|\*)[a-z0-9\._-]+\b/i)) {
        return 'variable';
      }
      /* numbers */
      if (state.inlinePairs == 0 && stream.match(/^\s*-?[0-9\.\,]+\s?$/)) {
        return 'number';
      }
      if (state.inlinePairs > 0 && stream.match(/^\s*-?[0-9\.\,]+\s?(?=(,|}))/)) {
        return 'number';
      }
      /* keywords */
      if (stream.match(keywordRegex)) {
        return 'keyword';
      }
    }

    /* pairs (associative arrays) -> key */
    if (!state.pair && stream.match(/^\s*(?:[,\[\]{}&*!|>'"%@`][^\s'":]|[^,\[\]{}#&*!|>'"%@`])[^#]*?(?=\s*:($|\s))/)) {
      state.pair = true;
      state.keyCol = stream.indentation();
      return "atom";
    }
    if (state.pair && stream.match(/^:\s*/)) {
      state.pairStart = true;
      return 'meta';
    }

    /* nothing found, continue */
    state.pairStart = false;
    state.escaped = ch == '\\';
    stream.next();
    return null;
  },
  startState: function () {
    return {
      pair: false,
      pairStart: false,
      keyCol: 0,
      inlinePairs: 0,
      inlineList: 0,
      literal: false,
      escaped: false
    };
  },
  languageData: {
    commentTokens: {
      line: "#"
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiMzU1NC5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGNvZGVtaXJyb3IvbGVnYWN5LW1vZGVzL21vZGUveWFtbC5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyJ2YXIgY29ucyA9IFsndHJ1ZScsICdmYWxzZScsICdvbicsICdvZmYnLCAneWVzJywgJ25vJ107XG52YXIga2V5d29yZFJlZ2V4ID0gbmV3IFJlZ0V4cChcIlxcXFxiKChcIiArIGNvbnMuam9pbihcIil8KFwiKSArIFwiKSkkXCIsICdpJyk7XG5leHBvcnQgY29uc3QgeWFtbCA9IHtcbiAgbmFtZTogXCJ5YW1sXCIsXG4gIHRva2VuOiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIHZhciBjaCA9IHN0cmVhbS5wZWVrKCk7XG4gICAgdmFyIGVzYyA9IHN0YXRlLmVzY2FwZWQ7XG4gICAgc3RhdGUuZXNjYXBlZCA9IGZhbHNlO1xuICAgIC8qIGNvbW1lbnRzICovXG4gICAgaWYgKGNoID09IFwiI1wiICYmIChzdHJlYW0ucG9zID09IDAgfHwgL1xccy8udGVzdChzdHJlYW0uc3RyaW5nLmNoYXJBdChzdHJlYW0ucG9zIC0gMSkpKSkge1xuICAgICAgc3RyZWFtLnNraXBUb0VuZCgpO1xuICAgICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICAgIH1cbiAgICBpZiAoc3RyZWFtLm1hdGNoKC9eKCcoW14nXXxcXFxcLikqJz98XCIoW15cIl18XFxcXC4pKlwiPykvKSkgcmV0dXJuIFwic3RyaW5nXCI7XG4gICAgaWYgKHN0YXRlLmxpdGVyYWwgJiYgc3RyZWFtLmluZGVudGF0aW9uKCkgPiBzdGF0ZS5rZXlDb2wpIHtcbiAgICAgIHN0cmVhbS5za2lwVG9FbmQoKTtcbiAgICAgIHJldHVybiBcInN0cmluZ1wiO1xuICAgIH0gZWxzZSBpZiAoc3RhdGUubGl0ZXJhbCkge1xuICAgICAgc3RhdGUubGl0ZXJhbCA9IGZhbHNlO1xuICAgIH1cbiAgICBpZiAoc3RyZWFtLnNvbCgpKSB7XG4gICAgICBzdGF0ZS5rZXlDb2wgPSAwO1xuICAgICAgc3RhdGUucGFpciA9IGZhbHNlO1xuICAgICAgc3RhdGUucGFpclN0YXJ0ID0gZmFsc2U7XG4gICAgICAvKiBkb2N1bWVudCBzdGFydCAqL1xuICAgICAgaWYgKHN0cmVhbS5tYXRjaCgnLS0tJykpIHtcbiAgICAgICAgcmV0dXJuIFwiZGVmXCI7XG4gICAgICB9XG4gICAgICAvKiBkb2N1bWVudCBlbmQgKi9cbiAgICAgIGlmIChzdHJlYW0ubWF0Y2goJy4uLicpKSB7XG4gICAgICAgIHJldHVybiBcImRlZlwiO1xuICAgICAgfVxuICAgICAgLyogYXJyYXkgbGlzdCBpdGVtICovXG4gICAgICBpZiAoc3RyZWFtLm1hdGNoKC9eXFxzKi1cXHMrLykpIHtcbiAgICAgICAgcmV0dXJuICdtZXRhJztcbiAgICAgIH1cbiAgICB9XG4gICAgLyogaW5saW5lIHBhaXJzL2xpc3RzICovXG4gICAgaWYgKHN0cmVhbS5tYXRjaCgvXihcXHt8XFx9fFxcW3xcXF0pLykpIHtcbiAgICAgIGlmIChjaCA9PSAneycpIHN0YXRlLmlubGluZVBhaXJzKys7ZWxzZSBpZiAoY2ggPT0gJ30nKSBzdGF0ZS5pbmxpbmVQYWlycy0tO2Vsc2UgaWYgKGNoID09ICdbJykgc3RhdGUuaW5saW5lTGlzdCsrO2Vsc2Ugc3RhdGUuaW5saW5lTGlzdC0tO1xuICAgICAgcmV0dXJuICdtZXRhJztcbiAgICB9XG5cbiAgICAvKiBsaXN0IHNlcGFyYXRvciAqL1xuICAgIGlmIChzdGF0ZS5pbmxpbmVMaXN0ID4gMCAmJiAhZXNjICYmIGNoID09ICcsJykge1xuICAgICAgc3RyZWFtLm5leHQoKTtcbiAgICAgIHJldHVybiAnbWV0YSc7XG4gICAgfVxuICAgIC8qIHBhaXJzIHNlcGFyYXRvciAqL1xuICAgIGlmIChzdGF0ZS5pbmxpbmVQYWlycyA+IDAgJiYgIWVzYyAmJiBjaCA9PSAnLCcpIHtcbiAgICAgIHN0YXRlLmtleUNvbCA9IDA7XG4gICAgICBzdGF0ZS5wYWlyID0gZmFsc2U7XG4gICAgICBzdGF0ZS5wYWlyU3RhcnQgPSBmYWxzZTtcbiAgICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgICByZXR1cm4gJ21ldGEnO1xuICAgIH1cblxuICAgIC8qIHN0YXJ0IG9mIHZhbHVlIG9mIGEgcGFpciAqL1xuICAgIGlmIChzdGF0ZS5wYWlyU3RhcnQpIHtcbiAgICAgIC8qIGJsb2NrIGxpdGVyYWxzICovXG4gICAgICBpZiAoc3RyZWFtLm1hdGNoKC9eXFxzKihcXHx8XFw+KVxccyovKSkge1xuICAgICAgICBzdGF0ZS5saXRlcmFsID0gdHJ1ZTtcbiAgICAgICAgcmV0dXJuICdtZXRhJztcbiAgICAgIH1cbiAgICAgIDtcbiAgICAgIC8qIHJlZmVyZW5jZXMgKi9cbiAgICAgIGlmIChzdHJlYW0ubWF0Y2goL15cXHMqKFxcJnxcXCopW2EtejAtOVxcLl8tXStcXGIvaSkpIHtcbiAgICAgICAgcmV0dXJuICd2YXJpYWJsZSc7XG4gICAgICB9XG4gICAgICAvKiBudW1iZXJzICovXG4gICAgICBpZiAoc3RhdGUuaW5saW5lUGFpcnMgPT0gMCAmJiBzdHJlYW0ubWF0Y2goL15cXHMqLT9bMC05XFwuXFwsXStcXHM/JC8pKSB7XG4gICAgICAgIHJldHVybiAnbnVtYmVyJztcbiAgICAgIH1cbiAgICAgIGlmIChzdGF0ZS5pbmxpbmVQYWlycyA+IDAgJiYgc3RyZWFtLm1hdGNoKC9eXFxzKi0/WzAtOVxcLlxcLF0rXFxzPyg/PSgsfH0pKS8pKSB7XG4gICAgICAgIHJldHVybiAnbnVtYmVyJztcbiAgICAgIH1cbiAgICAgIC8qIGtleXdvcmRzICovXG4gICAgICBpZiAoc3RyZWFtLm1hdGNoKGtleXdvcmRSZWdleCkpIHtcbiAgICAgICAgcmV0dXJuICdrZXl3b3JkJztcbiAgICAgIH1cbiAgICB9XG5cbiAgICAvKiBwYWlycyAoYXNzb2NpYXRpdmUgYXJyYXlzKSAtPiBrZXkgKi9cbiAgICBpZiAoIXN0YXRlLnBhaXIgJiYgc3RyZWFtLm1hdGNoKC9eXFxzKig/OlssXFxbXFxde30mKiF8PidcIiVAYF1bXlxccydcIjpdfFteLFxcW1xcXXt9IyYqIXw+J1wiJUBgXSlbXiNdKj8oPz1cXHMqOigkfFxccykpLykpIHtcbiAgICAgIHN0YXRlLnBhaXIgPSB0cnVlO1xuICAgICAgc3RhdGUua2V5Q29sID0gc3RyZWFtLmluZGVudGF0aW9uKCk7XG4gICAgICByZXR1cm4gXCJhdG9tXCI7XG4gICAgfVxuICAgIGlmIChzdGF0ZS5wYWlyICYmIHN0cmVhbS5tYXRjaCgvXjpcXHMqLykpIHtcbiAgICAgIHN0YXRlLnBhaXJTdGFydCA9IHRydWU7XG4gICAgICByZXR1cm4gJ21ldGEnO1xuICAgIH1cblxuICAgIC8qIG5vdGhpbmcgZm91bmQsIGNvbnRpbnVlICovXG4gICAgc3RhdGUucGFpclN0YXJ0ID0gZmFsc2U7XG4gICAgc3RhdGUuZXNjYXBlZCA9IGNoID09ICdcXFxcJztcbiAgICBzdHJlYW0ubmV4dCgpO1xuICAgIHJldHVybiBudWxsO1xuICB9LFxuICBzdGFydFN0YXRlOiBmdW5jdGlvbiAoKSB7XG4gICAgcmV0dXJuIHtcbiAgICAgIHBhaXI6IGZhbHNlLFxuICAgICAgcGFpclN0YXJ0OiBmYWxzZSxcbiAgICAgIGtleUNvbDogMCxcbiAgICAgIGlubGluZVBhaXJzOiAwLFxuICAgICAgaW5saW5lTGlzdDogMCxcbiAgICAgIGxpdGVyYWw6IGZhbHNlLFxuICAgICAgZXNjYXBlZDogZmFsc2VcbiAgICB9O1xuICB9LFxuICBsYW5ndWFnZURhdGE6IHtcbiAgICBjb21tZW50VG9rZW5zOiB7XG4gICAgICBsaW5lOiBcIiNcIlxuICAgIH1cbiAgfVxufTsiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=