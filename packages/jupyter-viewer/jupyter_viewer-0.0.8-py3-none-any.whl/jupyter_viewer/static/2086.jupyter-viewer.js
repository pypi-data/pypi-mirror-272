"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[2086],{

/***/ 92086:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "dtd": () => (/* binding */ dtd)
/* harmony export */ });
var type;
function ret(style, tp) {
  type = tp;
  return style;
}
function tokenBase(stream, state) {
  var ch = stream.next();
  if (ch == "<" && stream.eat("!")) {
    if (stream.eatWhile(/[\-]/)) {
      state.tokenize = tokenSGMLComment;
      return tokenSGMLComment(stream, state);
    } else if (stream.eatWhile(/[\w]/)) return ret("keyword", "doindent");
  } else if (ch == "<" && stream.eat("?")) {
    //xml declaration
    state.tokenize = inBlock("meta", "?>");
    return ret("meta", ch);
  } else if (ch == "#" && stream.eatWhile(/[\w]/)) return ret("atom", "tag");else if (ch == "|") return ret("keyword", "separator");else if (ch.match(/[\(\)\[\]\-\.,\+\?>]/)) return ret(null, ch); //if(ch === ">") return ret(null, "endtag"); else
  else if (ch.match(/[\[\]]/)) return ret("rule", ch);else if (ch == "\"" || ch == "'") {
    state.tokenize = tokenString(ch);
    return state.tokenize(stream, state);
  } else if (stream.eatWhile(/[a-zA-Z\?\+\d]/)) {
    var sc = stream.current();
    if (sc.substr(sc.length - 1, sc.length).match(/\?|\+/) !== null) stream.backUp(1);
    return ret("tag", "tag");
  } else if (ch == "%" || ch == "*") return ret("number", "number");else {
    stream.eatWhile(/[\w\\\-_%.{,]/);
    return ret(null, null);
  }
}
function tokenSGMLComment(stream, state) {
  var dashes = 0,
    ch;
  while ((ch = stream.next()) != null) {
    if (dashes >= 2 && ch == ">") {
      state.tokenize = tokenBase;
      break;
    }
    dashes = ch == "-" ? dashes + 1 : 0;
  }
  return ret("comment", "comment");
}
function tokenString(quote) {
  return function (stream, state) {
    var escaped = false,
      ch;
    while ((ch = stream.next()) != null) {
      if (ch == quote && !escaped) {
        state.tokenize = tokenBase;
        break;
      }
      escaped = !escaped && ch == "\\";
    }
    return ret("string", "tag");
  };
}
function inBlock(style, terminator) {
  return function (stream, state) {
    while (!stream.eol()) {
      if (stream.match(terminator)) {
        state.tokenize = tokenBase;
        break;
      }
      stream.next();
    }
    return style;
  };
}
const dtd = {
  name: "dtd",
  startState: function () {
    return {
      tokenize: tokenBase,
      baseIndent: 0,
      stack: []
    };
  },
  token: function (stream, state) {
    if (stream.eatSpace()) return null;
    var style = state.tokenize(stream, state);
    var context = state.stack[state.stack.length - 1];
    if (stream.current() == "[" || type === "doindent" || type == "[") state.stack.push("rule");else if (type === "endtag") state.stack[state.stack.length - 1] = "endtag";else if (stream.current() == "]" || type == "]" || type == ">" && context == "rule") state.stack.pop();else if (type == "[") state.stack.push("[");
    return style;
  },
  indent: function (state, textAfter, cx) {
    var n = state.stack.length;
    if (textAfter.charAt(0) === ']') n--;else if (textAfter.substr(textAfter.length - 1, textAfter.length) === ">") {
      if (textAfter.substr(0, 1) === "<") {} else if (type == "doindent" && textAfter.length > 1) {} else if (type == "doindent") n--;else if (type == ">" && textAfter.length > 1) {} else if (type == "tag" && textAfter !== ">") {} else if (type == "tag" && state.stack[state.stack.length - 1] == "rule") n--;else if (type == "tag") n++;else if (textAfter === ">" && state.stack[state.stack.length - 1] == "rule" && type === ">") n--;else if (textAfter === ">" && state.stack[state.stack.length - 1] == "rule") {} else if (textAfter.substr(0, 1) !== "<" && textAfter.substr(0, 1) === ">") n = n - 1;else if (textAfter === ">") {} else n = n - 1;
      //over rule them all
      if (type == null || type == "]") n--;
    }
    return state.baseIndent + n * cx.unit;
  },
  languageData: {
    indentOnInput: /^\s*[\]>]$/
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiMjA4Ni5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9AY29kZW1pcnJvci9sZWdhY3ktbW9kZXMvbW9kZS9kdGQuanMiXSwic291cmNlc0NvbnRlbnQiOlsidmFyIHR5cGU7XG5mdW5jdGlvbiByZXQoc3R5bGUsIHRwKSB7XG4gIHR5cGUgPSB0cDtcbiAgcmV0dXJuIHN0eWxlO1xufVxuZnVuY3Rpb24gdG9rZW5CYXNlKHN0cmVhbSwgc3RhdGUpIHtcbiAgdmFyIGNoID0gc3RyZWFtLm5leHQoKTtcbiAgaWYgKGNoID09IFwiPFwiICYmIHN0cmVhbS5lYXQoXCIhXCIpKSB7XG4gICAgaWYgKHN0cmVhbS5lYXRXaGlsZSgvW1xcLV0vKSkge1xuICAgICAgc3RhdGUudG9rZW5pemUgPSB0b2tlblNHTUxDb21tZW50O1xuICAgICAgcmV0dXJuIHRva2VuU0dNTENvbW1lbnQoc3RyZWFtLCBzdGF0ZSk7XG4gICAgfSBlbHNlIGlmIChzdHJlYW0uZWF0V2hpbGUoL1tcXHddLykpIHJldHVybiByZXQoXCJrZXl3b3JkXCIsIFwiZG9pbmRlbnRcIik7XG4gIH0gZWxzZSBpZiAoY2ggPT0gXCI8XCIgJiYgc3RyZWFtLmVhdChcIj9cIikpIHtcbiAgICAvL3htbCBkZWNsYXJhdGlvblxuICAgIHN0YXRlLnRva2VuaXplID0gaW5CbG9jayhcIm1ldGFcIiwgXCI/PlwiKTtcbiAgICByZXR1cm4gcmV0KFwibWV0YVwiLCBjaCk7XG4gIH0gZWxzZSBpZiAoY2ggPT0gXCIjXCIgJiYgc3RyZWFtLmVhdFdoaWxlKC9bXFx3XS8pKSByZXR1cm4gcmV0KFwiYXRvbVwiLCBcInRhZ1wiKTtlbHNlIGlmIChjaCA9PSBcInxcIikgcmV0dXJuIHJldChcImtleXdvcmRcIiwgXCJzZXBhcmF0b3JcIik7ZWxzZSBpZiAoY2gubWF0Y2goL1tcXChcXClcXFtcXF1cXC1cXC4sXFwrXFw/Pl0vKSkgcmV0dXJuIHJldChudWxsLCBjaCk7IC8vaWYoY2ggPT09IFwiPlwiKSByZXR1cm4gcmV0KG51bGwsIFwiZW5kdGFnXCIpOyBlbHNlXG4gIGVsc2UgaWYgKGNoLm1hdGNoKC9bXFxbXFxdXS8pKSByZXR1cm4gcmV0KFwicnVsZVwiLCBjaCk7ZWxzZSBpZiAoY2ggPT0gXCJcXFwiXCIgfHwgY2ggPT0gXCInXCIpIHtcbiAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuU3RyaW5nKGNoKTtcbiAgICByZXR1cm4gc3RhdGUudG9rZW5pemUoc3RyZWFtLCBzdGF0ZSk7XG4gIH0gZWxzZSBpZiAoc3RyZWFtLmVhdFdoaWxlKC9bYS16QS1aXFw/XFwrXFxkXS8pKSB7XG4gICAgdmFyIHNjID0gc3RyZWFtLmN1cnJlbnQoKTtcbiAgICBpZiAoc2Muc3Vic3RyKHNjLmxlbmd0aCAtIDEsIHNjLmxlbmd0aCkubWF0Y2goL1xcP3xcXCsvKSAhPT0gbnVsbCkgc3RyZWFtLmJhY2tVcCgxKTtcbiAgICByZXR1cm4gcmV0KFwidGFnXCIsIFwidGFnXCIpO1xuICB9IGVsc2UgaWYgKGNoID09IFwiJVwiIHx8IGNoID09IFwiKlwiKSByZXR1cm4gcmV0KFwibnVtYmVyXCIsIFwibnVtYmVyXCIpO2Vsc2Uge1xuICAgIHN0cmVhbS5lYXRXaGlsZSgvW1xcd1xcXFxcXC1fJS57LF0vKTtcbiAgICByZXR1cm4gcmV0KG51bGwsIG51bGwpO1xuICB9XG59XG5mdW5jdGlvbiB0b2tlblNHTUxDb21tZW50KHN0cmVhbSwgc3RhdGUpIHtcbiAgdmFyIGRhc2hlcyA9IDAsXG4gICAgY2g7XG4gIHdoaWxlICgoY2ggPSBzdHJlYW0ubmV4dCgpKSAhPSBudWxsKSB7XG4gICAgaWYgKGRhc2hlcyA+PSAyICYmIGNoID09IFwiPlwiKSB7XG4gICAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQmFzZTtcbiAgICAgIGJyZWFrO1xuICAgIH1cbiAgICBkYXNoZXMgPSBjaCA9PSBcIi1cIiA/IGRhc2hlcyArIDEgOiAwO1xuICB9XG4gIHJldHVybiByZXQoXCJjb21tZW50XCIsIFwiY29tbWVudFwiKTtcbn1cbmZ1bmN0aW9uIHRva2VuU3RyaW5nKHF1b3RlKSB7XG4gIHJldHVybiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIHZhciBlc2NhcGVkID0gZmFsc2UsXG4gICAgICBjaDtcbiAgICB3aGlsZSAoKGNoID0gc3RyZWFtLm5leHQoKSkgIT0gbnVsbCkge1xuICAgICAgaWYgKGNoID09IHF1b3RlICYmICFlc2NhcGVkKSB7XG4gICAgICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlO1xuICAgICAgICBicmVhaztcbiAgICAgIH1cbiAgICAgIGVzY2FwZWQgPSAhZXNjYXBlZCAmJiBjaCA9PSBcIlxcXFxcIjtcbiAgICB9XG4gICAgcmV0dXJuIHJldChcInN0cmluZ1wiLCBcInRhZ1wiKTtcbiAgfTtcbn1cbmZ1bmN0aW9uIGluQmxvY2soc3R5bGUsIHRlcm1pbmF0b3IpIHtcbiAgcmV0dXJuIGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgd2hpbGUgKCFzdHJlYW0uZW9sKCkpIHtcbiAgICAgIGlmIChzdHJlYW0ubWF0Y2godGVybWluYXRvcikpIHtcbiAgICAgICAgc3RhdGUudG9rZW5pemUgPSB0b2tlbkJhc2U7XG4gICAgICAgIGJyZWFrO1xuICAgICAgfVxuICAgICAgc3RyZWFtLm5leHQoKTtcbiAgICB9XG4gICAgcmV0dXJuIHN0eWxlO1xuICB9O1xufVxuZXhwb3J0IGNvbnN0IGR0ZCA9IHtcbiAgbmFtZTogXCJkdGRcIixcbiAgc3RhcnRTdGF0ZTogZnVuY3Rpb24gKCkge1xuICAgIHJldHVybiB7XG4gICAgICB0b2tlbml6ZTogdG9rZW5CYXNlLFxuICAgICAgYmFzZUluZGVudDogMCxcbiAgICAgIHN0YWNrOiBbXVxuICAgIH07XG4gIH0sXG4gIHRva2VuOiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIGlmIChzdHJlYW0uZWF0U3BhY2UoKSkgcmV0dXJuIG51bGw7XG4gICAgdmFyIHN0eWxlID0gc3RhdGUudG9rZW5pemUoc3RyZWFtLCBzdGF0ZSk7XG4gICAgdmFyIGNvbnRleHQgPSBzdGF0ZS5zdGFja1tzdGF0ZS5zdGFjay5sZW5ndGggLSAxXTtcbiAgICBpZiAoc3RyZWFtLmN1cnJlbnQoKSA9PSBcIltcIiB8fCB0eXBlID09PSBcImRvaW5kZW50XCIgfHwgdHlwZSA9PSBcIltcIikgc3RhdGUuc3RhY2sucHVzaChcInJ1bGVcIik7ZWxzZSBpZiAodHlwZSA9PT0gXCJlbmR0YWdcIikgc3RhdGUuc3RhY2tbc3RhdGUuc3RhY2subGVuZ3RoIC0gMV0gPSBcImVuZHRhZ1wiO2Vsc2UgaWYgKHN0cmVhbS5jdXJyZW50KCkgPT0gXCJdXCIgfHwgdHlwZSA9PSBcIl1cIiB8fCB0eXBlID09IFwiPlwiICYmIGNvbnRleHQgPT0gXCJydWxlXCIpIHN0YXRlLnN0YWNrLnBvcCgpO2Vsc2UgaWYgKHR5cGUgPT0gXCJbXCIpIHN0YXRlLnN0YWNrLnB1c2goXCJbXCIpO1xuICAgIHJldHVybiBzdHlsZTtcbiAgfSxcbiAgaW5kZW50OiBmdW5jdGlvbiAoc3RhdGUsIHRleHRBZnRlciwgY3gpIHtcbiAgICB2YXIgbiA9IHN0YXRlLnN0YWNrLmxlbmd0aDtcbiAgICBpZiAodGV4dEFmdGVyLmNoYXJBdCgwKSA9PT0gJ10nKSBuLS07ZWxzZSBpZiAodGV4dEFmdGVyLnN1YnN0cih0ZXh0QWZ0ZXIubGVuZ3RoIC0gMSwgdGV4dEFmdGVyLmxlbmd0aCkgPT09IFwiPlwiKSB7XG4gICAgICBpZiAodGV4dEFmdGVyLnN1YnN0cigwLCAxKSA9PT0gXCI8XCIpIHt9IGVsc2UgaWYgKHR5cGUgPT0gXCJkb2luZGVudFwiICYmIHRleHRBZnRlci5sZW5ndGggPiAxKSB7fSBlbHNlIGlmICh0eXBlID09IFwiZG9pbmRlbnRcIikgbi0tO2Vsc2UgaWYgKHR5cGUgPT0gXCI+XCIgJiYgdGV4dEFmdGVyLmxlbmd0aCA+IDEpIHt9IGVsc2UgaWYgKHR5cGUgPT0gXCJ0YWdcIiAmJiB0ZXh0QWZ0ZXIgIT09IFwiPlwiKSB7fSBlbHNlIGlmICh0eXBlID09IFwidGFnXCIgJiYgc3RhdGUuc3RhY2tbc3RhdGUuc3RhY2subGVuZ3RoIC0gMV0gPT0gXCJydWxlXCIpIG4tLTtlbHNlIGlmICh0eXBlID09IFwidGFnXCIpIG4rKztlbHNlIGlmICh0ZXh0QWZ0ZXIgPT09IFwiPlwiICYmIHN0YXRlLnN0YWNrW3N0YXRlLnN0YWNrLmxlbmd0aCAtIDFdID09IFwicnVsZVwiICYmIHR5cGUgPT09IFwiPlwiKSBuLS07ZWxzZSBpZiAodGV4dEFmdGVyID09PSBcIj5cIiAmJiBzdGF0ZS5zdGFja1tzdGF0ZS5zdGFjay5sZW5ndGggLSAxXSA9PSBcInJ1bGVcIikge30gZWxzZSBpZiAodGV4dEFmdGVyLnN1YnN0cigwLCAxKSAhPT0gXCI8XCIgJiYgdGV4dEFmdGVyLnN1YnN0cigwLCAxKSA9PT0gXCI+XCIpIG4gPSBuIC0gMTtlbHNlIGlmICh0ZXh0QWZ0ZXIgPT09IFwiPlwiKSB7fSBlbHNlIG4gPSBuIC0gMTtcbiAgICAgIC8vb3ZlciBydWxlIHRoZW0gYWxsXG4gICAgICBpZiAodHlwZSA9PSBudWxsIHx8IHR5cGUgPT0gXCJdXCIpIG4tLTtcbiAgICB9XG4gICAgcmV0dXJuIHN0YXRlLmJhc2VJbmRlbnQgKyBuICogY3gudW5pdDtcbiAgfSxcbiAgbGFuZ3VhZ2VEYXRhOiB7XG4gICAgaW5kZW50T25JbnB1dDogL15cXHMqW1xcXT5dJC9cbiAgfVxufTsiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=