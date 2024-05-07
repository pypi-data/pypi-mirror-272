"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[7962],{

/***/ 7962:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "oz": () => (/* binding */ oz)
/* harmony export */ });
function wordRegexp(words) {
  return new RegExp("^((" + words.join(")|(") + "))\\b");
}
var singleOperators = /[\^@!\|<>#~\.\*\-\+\\/,=]/;
var doubleOperators = /(<-)|(:=)|(=<)|(>=)|(<=)|(<:)|(>:)|(=:)|(\\=)|(\\=:)|(!!)|(==)|(::)/;
var tripleOperators = /(:::)|(\.\.\.)|(=<:)|(>=:)/;
var middle = ["in", "then", "else", "of", "elseof", "elsecase", "elseif", "catch", "finally", "with", "require", "prepare", "import", "export", "define", "do"];
var end = ["end"];
var atoms = wordRegexp(["true", "false", "nil", "unit"]);
var commonKeywords = wordRegexp(["andthen", "at", "attr", "declare", "feat", "from", "lex", "mod", "div", "mode", "orelse", "parser", "prod", "prop", "scanner", "self", "syn", "token"]);
var openingKeywords = wordRegexp(["local", "proc", "fun", "case", "class", "if", "cond", "or", "dis", "choice", "not", "thread", "try", "raise", "lock", "for", "suchthat", "meth", "functor"]);
var middleKeywords = wordRegexp(middle);
var endKeywords = wordRegexp(end);

// Tokenizers
function tokenBase(stream, state) {
  if (stream.eatSpace()) {
    return null;
  }

  // Brackets
  if (stream.match(/[{}]/)) {
    return "bracket";
  }

  // Special [] keyword
  if (stream.match('[]')) {
    return "keyword";
  }

  // Operators
  if (stream.match(tripleOperators) || stream.match(doubleOperators)) {
    return "operator";
  }

  // Atoms
  if (stream.match(atoms)) {
    return 'atom';
  }

  // Opening keywords
  var matched = stream.match(openingKeywords);
  if (matched) {
    if (!state.doInCurrentLine) state.currentIndent++;else state.doInCurrentLine = false;

    // Special matching for signatures
    if (matched[0] == "proc" || matched[0] == "fun") state.tokenize = tokenFunProc;else if (matched[0] == "class") state.tokenize = tokenClass;else if (matched[0] == "meth") state.tokenize = tokenMeth;
    return 'keyword';
  }

  // Middle and other keywords
  if (stream.match(middleKeywords) || stream.match(commonKeywords)) {
    return "keyword";
  }

  // End keywords
  if (stream.match(endKeywords)) {
    state.currentIndent--;
    return 'keyword';
  }

  // Eat the next char for next comparisons
  var ch = stream.next();

  // Strings
  if (ch == '"' || ch == "'") {
    state.tokenize = tokenString(ch);
    return state.tokenize(stream, state);
  }

  // Numbers
  if (/[~\d]/.test(ch)) {
    if (ch == "~") {
      if (!/^[0-9]/.test(stream.peek())) return null;else if (stream.next() == "0" && stream.match(/^[xX][0-9a-fA-F]+/) || stream.match(/^[0-9]*(\.[0-9]+)?([eE][~+]?[0-9]+)?/)) return "number";
    }
    if (ch == "0" && stream.match(/^[xX][0-9a-fA-F]+/) || stream.match(/^[0-9]*(\.[0-9]+)?([eE][~+]?[0-9]+)?/)) return "number";
    return null;
  }

  // Comments
  if (ch == "%") {
    stream.skipToEnd();
    return 'comment';
  } else if (ch == "/") {
    if (stream.eat("*")) {
      state.tokenize = tokenComment;
      return tokenComment(stream, state);
    }
  }

  // Single operators
  if (singleOperators.test(ch)) {
    return "operator";
  }

  // If nothing match, we skip the entire alphanumerical block
  stream.eatWhile(/\w/);
  return "variable";
}
function tokenClass(stream, state) {
  if (stream.eatSpace()) {
    return null;
  }
  stream.match(/([A-Z][A-Za-z0-9_]*)|(`.+`)/);
  state.tokenize = tokenBase;
  return "type";
}
function tokenMeth(stream, state) {
  if (stream.eatSpace()) {
    return null;
  }
  stream.match(/([a-zA-Z][A-Za-z0-9_]*)|(`.+`)/);
  state.tokenize = tokenBase;
  return "def";
}
function tokenFunProc(stream, state) {
  if (stream.eatSpace()) {
    return null;
  }
  if (!state.hasPassedFirstStage && stream.eat("{")) {
    state.hasPassedFirstStage = true;
    return "bracket";
  } else if (state.hasPassedFirstStage) {
    stream.match(/([A-Z][A-Za-z0-9_]*)|(`.+`)|\$/);
    state.hasPassedFirstStage = false;
    state.tokenize = tokenBase;
    return "def";
  } else {
    state.tokenize = tokenBase;
    return null;
  }
}
function tokenComment(stream, state) {
  var maybeEnd = false,
    ch;
  while (ch = stream.next()) {
    if (ch == "/" && maybeEnd) {
      state.tokenize = tokenBase;
      break;
    }
    maybeEnd = ch == "*";
  }
  return "comment";
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
    if (end || !escaped) state.tokenize = tokenBase;
    return "string";
  };
}
function buildElectricInputRegEx() {
  // Reindentation should occur on [] or on a match of any of
  // the block closing keywords, at the end of a line.
  var allClosings = middle.concat(end);
  return new RegExp("[\\[\\]]|(" + allClosings.join("|") + ")$");
}
const oz = {
  name: "oz",
  startState: function () {
    return {
      tokenize: tokenBase,
      currentIndent: 0,
      doInCurrentLine: false,
      hasPassedFirstStage: false
    };
  },
  token: function (stream, state) {
    if (stream.sol()) state.doInCurrentLine = 0;
    return state.tokenize(stream, state);
  },
  indent: function (state, textAfter, cx) {
    var trueText = textAfter.replace(/^\s+|\s+$/g, '');
    if (trueText.match(endKeywords) || trueText.match(middleKeywords) || trueText.match(/(\[])/)) return cx.unit * (state.currentIndent - 1);
    if (state.currentIndent < 0) return 0;
    return state.currentIndent * cx.unit;
  },
  languageData: {
    indentOnInut: buildElectricInputRegEx(),
    commentTokens: {
      line: "%",
      block: {
        open: "/*",
        close: "*/"
      }
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNzk2Mi5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGNvZGVtaXJyb3IvbGVnYWN5LW1vZGVzL21vZGUvb3ouanMiXSwic291cmNlc0NvbnRlbnQiOlsiZnVuY3Rpb24gd29yZFJlZ2V4cCh3b3Jkcykge1xuICByZXR1cm4gbmV3IFJlZ0V4cChcIl4oKFwiICsgd29yZHMuam9pbihcIil8KFwiKSArIFwiKSlcXFxcYlwiKTtcbn1cbnZhciBzaW5nbGVPcGVyYXRvcnMgPSAvW1xcXkAhXFx8PD4jflxcLlxcKlxcLVxcK1xcXFwvLD1dLztcbnZhciBkb3VibGVPcGVyYXRvcnMgPSAvKDwtKXwoOj0pfCg9PCl8KD49KXwoPD0pfCg8Oil8KD46KXwoPTopfChcXFxcPSl8KFxcXFw9Oil8KCEhKXwoPT0pfCg6OikvO1xudmFyIHRyaXBsZU9wZXJhdG9ycyA9IC8oOjo6KXwoXFwuXFwuXFwuKXwoPTw6KXwoPj06KS87XG52YXIgbWlkZGxlID0gW1wiaW5cIiwgXCJ0aGVuXCIsIFwiZWxzZVwiLCBcIm9mXCIsIFwiZWxzZW9mXCIsIFwiZWxzZWNhc2VcIiwgXCJlbHNlaWZcIiwgXCJjYXRjaFwiLCBcImZpbmFsbHlcIiwgXCJ3aXRoXCIsIFwicmVxdWlyZVwiLCBcInByZXBhcmVcIiwgXCJpbXBvcnRcIiwgXCJleHBvcnRcIiwgXCJkZWZpbmVcIiwgXCJkb1wiXTtcbnZhciBlbmQgPSBbXCJlbmRcIl07XG52YXIgYXRvbXMgPSB3b3JkUmVnZXhwKFtcInRydWVcIiwgXCJmYWxzZVwiLCBcIm5pbFwiLCBcInVuaXRcIl0pO1xudmFyIGNvbW1vbktleXdvcmRzID0gd29yZFJlZ2V4cChbXCJhbmR0aGVuXCIsIFwiYXRcIiwgXCJhdHRyXCIsIFwiZGVjbGFyZVwiLCBcImZlYXRcIiwgXCJmcm9tXCIsIFwibGV4XCIsIFwibW9kXCIsIFwiZGl2XCIsIFwibW9kZVwiLCBcIm9yZWxzZVwiLCBcInBhcnNlclwiLCBcInByb2RcIiwgXCJwcm9wXCIsIFwic2Nhbm5lclwiLCBcInNlbGZcIiwgXCJzeW5cIiwgXCJ0b2tlblwiXSk7XG52YXIgb3BlbmluZ0tleXdvcmRzID0gd29yZFJlZ2V4cChbXCJsb2NhbFwiLCBcInByb2NcIiwgXCJmdW5cIiwgXCJjYXNlXCIsIFwiY2xhc3NcIiwgXCJpZlwiLCBcImNvbmRcIiwgXCJvclwiLCBcImRpc1wiLCBcImNob2ljZVwiLCBcIm5vdFwiLCBcInRocmVhZFwiLCBcInRyeVwiLCBcInJhaXNlXCIsIFwibG9ja1wiLCBcImZvclwiLCBcInN1Y2h0aGF0XCIsIFwibWV0aFwiLCBcImZ1bmN0b3JcIl0pO1xudmFyIG1pZGRsZUtleXdvcmRzID0gd29yZFJlZ2V4cChtaWRkbGUpO1xudmFyIGVuZEtleXdvcmRzID0gd29yZFJlZ2V4cChlbmQpO1xuXG4vLyBUb2tlbml6ZXJzXG5mdW5jdGlvbiB0b2tlbkJhc2Uoc3RyZWFtLCBzdGF0ZSkge1xuICBpZiAoc3RyZWFtLmVhdFNwYWNlKCkpIHtcbiAgICByZXR1cm4gbnVsbDtcbiAgfVxuXG4gIC8vIEJyYWNrZXRzXG4gIGlmIChzdHJlYW0ubWF0Y2goL1t7fV0vKSkge1xuICAgIHJldHVybiBcImJyYWNrZXRcIjtcbiAgfVxuXG4gIC8vIFNwZWNpYWwgW10ga2V5d29yZFxuICBpZiAoc3RyZWFtLm1hdGNoKCdbXScpKSB7XG4gICAgcmV0dXJuIFwia2V5d29yZFwiO1xuICB9XG5cbiAgLy8gT3BlcmF0b3JzXG4gIGlmIChzdHJlYW0ubWF0Y2godHJpcGxlT3BlcmF0b3JzKSB8fCBzdHJlYW0ubWF0Y2goZG91YmxlT3BlcmF0b3JzKSkge1xuICAgIHJldHVybiBcIm9wZXJhdG9yXCI7XG4gIH1cblxuICAvLyBBdG9tc1xuICBpZiAoc3RyZWFtLm1hdGNoKGF0b21zKSkge1xuICAgIHJldHVybiAnYXRvbSc7XG4gIH1cblxuICAvLyBPcGVuaW5nIGtleXdvcmRzXG4gIHZhciBtYXRjaGVkID0gc3RyZWFtLm1hdGNoKG9wZW5pbmdLZXl3b3Jkcyk7XG4gIGlmIChtYXRjaGVkKSB7XG4gICAgaWYgKCFzdGF0ZS5kb0luQ3VycmVudExpbmUpIHN0YXRlLmN1cnJlbnRJbmRlbnQrKztlbHNlIHN0YXRlLmRvSW5DdXJyZW50TGluZSA9IGZhbHNlO1xuXG4gICAgLy8gU3BlY2lhbCBtYXRjaGluZyBmb3Igc2lnbmF0dXJlc1xuICAgIGlmIChtYXRjaGVkWzBdID09IFwicHJvY1wiIHx8IG1hdGNoZWRbMF0gPT0gXCJmdW5cIikgc3RhdGUudG9rZW5pemUgPSB0b2tlbkZ1blByb2M7ZWxzZSBpZiAobWF0Y2hlZFswXSA9PSBcImNsYXNzXCIpIHN0YXRlLnRva2VuaXplID0gdG9rZW5DbGFzcztlbHNlIGlmIChtYXRjaGVkWzBdID09IFwibWV0aFwiKSBzdGF0ZS50b2tlbml6ZSA9IHRva2VuTWV0aDtcbiAgICByZXR1cm4gJ2tleXdvcmQnO1xuICB9XG5cbiAgLy8gTWlkZGxlIGFuZCBvdGhlciBrZXl3b3Jkc1xuICBpZiAoc3RyZWFtLm1hdGNoKG1pZGRsZUtleXdvcmRzKSB8fCBzdHJlYW0ubWF0Y2goY29tbW9uS2V5d29yZHMpKSB7XG4gICAgcmV0dXJuIFwia2V5d29yZFwiO1xuICB9XG5cbiAgLy8gRW5kIGtleXdvcmRzXG4gIGlmIChzdHJlYW0ubWF0Y2goZW5kS2V5d29yZHMpKSB7XG4gICAgc3RhdGUuY3VycmVudEluZGVudC0tO1xuICAgIHJldHVybiAna2V5d29yZCc7XG4gIH1cblxuICAvLyBFYXQgdGhlIG5leHQgY2hhciBmb3IgbmV4dCBjb21wYXJpc29uc1xuICB2YXIgY2ggPSBzdHJlYW0ubmV4dCgpO1xuXG4gIC8vIFN0cmluZ3NcbiAgaWYgKGNoID09ICdcIicgfHwgY2ggPT0gXCInXCIpIHtcbiAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuU3RyaW5nKGNoKTtcbiAgICByZXR1cm4gc3RhdGUudG9rZW5pemUoc3RyZWFtLCBzdGF0ZSk7XG4gIH1cblxuICAvLyBOdW1iZXJzXG4gIGlmICgvW35cXGRdLy50ZXN0KGNoKSkge1xuICAgIGlmIChjaCA9PSBcIn5cIikge1xuICAgICAgaWYgKCEvXlswLTldLy50ZXN0KHN0cmVhbS5wZWVrKCkpKSByZXR1cm4gbnVsbDtlbHNlIGlmIChzdHJlYW0ubmV4dCgpID09IFwiMFwiICYmIHN0cmVhbS5tYXRjaCgvXlt4WF1bMC05YS1mQS1GXSsvKSB8fCBzdHJlYW0ubWF0Y2goL15bMC05XSooXFwuWzAtOV0rKT8oW2VFXVt+K10/WzAtOV0rKT8vKSkgcmV0dXJuIFwibnVtYmVyXCI7XG4gICAgfVxuICAgIGlmIChjaCA9PSBcIjBcIiAmJiBzdHJlYW0ubWF0Y2goL15beFhdWzAtOWEtZkEtRl0rLykgfHwgc3RyZWFtLm1hdGNoKC9eWzAtOV0qKFxcLlswLTldKyk/KFtlRV1bfitdP1swLTldKyk/LykpIHJldHVybiBcIm51bWJlclwiO1xuICAgIHJldHVybiBudWxsO1xuICB9XG5cbiAgLy8gQ29tbWVudHNcbiAgaWYgKGNoID09IFwiJVwiKSB7XG4gICAgc3RyZWFtLnNraXBUb0VuZCgpO1xuICAgIHJldHVybiAnY29tbWVudCc7XG4gIH0gZWxzZSBpZiAoY2ggPT0gXCIvXCIpIHtcbiAgICBpZiAoc3RyZWFtLmVhdChcIipcIikpIHtcbiAgICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5Db21tZW50O1xuICAgICAgcmV0dXJuIHRva2VuQ29tbWVudChzdHJlYW0sIHN0YXRlKTtcbiAgICB9XG4gIH1cblxuICAvLyBTaW5nbGUgb3BlcmF0b3JzXG4gIGlmIChzaW5nbGVPcGVyYXRvcnMudGVzdChjaCkpIHtcbiAgICByZXR1cm4gXCJvcGVyYXRvclwiO1xuICB9XG5cbiAgLy8gSWYgbm90aGluZyBtYXRjaCwgd2Ugc2tpcCB0aGUgZW50aXJlIGFscGhhbnVtZXJpY2FsIGJsb2NrXG4gIHN0cmVhbS5lYXRXaGlsZSgvXFx3Lyk7XG4gIHJldHVybiBcInZhcmlhYmxlXCI7XG59XG5mdW5jdGlvbiB0b2tlbkNsYXNzKHN0cmVhbSwgc3RhdGUpIHtcbiAgaWYgKHN0cmVhbS5lYXRTcGFjZSgpKSB7XG4gICAgcmV0dXJuIG51bGw7XG4gIH1cbiAgc3RyZWFtLm1hdGNoKC8oW0EtWl1bQS1aYS16MC05X10qKXwoYC4rYCkvKTtcbiAgc3RhdGUudG9rZW5pemUgPSB0b2tlbkJhc2U7XG4gIHJldHVybiBcInR5cGVcIjtcbn1cbmZ1bmN0aW9uIHRva2VuTWV0aChzdHJlYW0sIHN0YXRlKSB7XG4gIGlmIChzdHJlYW0uZWF0U3BhY2UoKSkge1xuICAgIHJldHVybiBudWxsO1xuICB9XG4gIHN0cmVhbS5tYXRjaCgvKFthLXpBLVpdW0EtWmEtejAtOV9dKil8KGAuK2ApLyk7XG4gIHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlO1xuICByZXR1cm4gXCJkZWZcIjtcbn1cbmZ1bmN0aW9uIHRva2VuRnVuUHJvYyhzdHJlYW0sIHN0YXRlKSB7XG4gIGlmIChzdHJlYW0uZWF0U3BhY2UoKSkge1xuICAgIHJldHVybiBudWxsO1xuICB9XG4gIGlmICghc3RhdGUuaGFzUGFzc2VkRmlyc3RTdGFnZSAmJiBzdHJlYW0uZWF0KFwie1wiKSkge1xuICAgIHN0YXRlLmhhc1Bhc3NlZEZpcnN0U3RhZ2UgPSB0cnVlO1xuICAgIHJldHVybiBcImJyYWNrZXRcIjtcbiAgfSBlbHNlIGlmIChzdGF0ZS5oYXNQYXNzZWRGaXJzdFN0YWdlKSB7XG4gICAgc3RyZWFtLm1hdGNoKC8oW0EtWl1bQS1aYS16MC05X10qKXwoYC4rYCl8XFwkLyk7XG4gICAgc3RhdGUuaGFzUGFzc2VkRmlyc3RTdGFnZSA9IGZhbHNlO1xuICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlO1xuICAgIHJldHVybiBcImRlZlwiO1xuICB9IGVsc2Uge1xuICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlO1xuICAgIHJldHVybiBudWxsO1xuICB9XG59XG5mdW5jdGlvbiB0b2tlbkNvbW1lbnQoc3RyZWFtLCBzdGF0ZSkge1xuICB2YXIgbWF5YmVFbmQgPSBmYWxzZSxcbiAgICBjaDtcbiAgd2hpbGUgKGNoID0gc3RyZWFtLm5leHQoKSkge1xuICAgIGlmIChjaCA9PSBcIi9cIiAmJiBtYXliZUVuZCkge1xuICAgICAgc3RhdGUudG9rZW5pemUgPSB0b2tlbkJhc2U7XG4gICAgICBicmVhaztcbiAgICB9XG4gICAgbWF5YmVFbmQgPSBjaCA9PSBcIipcIjtcbiAgfVxuICByZXR1cm4gXCJjb21tZW50XCI7XG59XG5mdW5jdGlvbiB0b2tlblN0cmluZyhxdW90ZSkge1xuICByZXR1cm4gZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICB2YXIgZXNjYXBlZCA9IGZhbHNlLFxuICAgICAgbmV4dCxcbiAgICAgIGVuZCA9IGZhbHNlO1xuICAgIHdoaWxlICgobmV4dCA9IHN0cmVhbS5uZXh0KCkpICE9IG51bGwpIHtcbiAgICAgIGlmIChuZXh0ID09IHF1b3RlICYmICFlc2NhcGVkKSB7XG4gICAgICAgIGVuZCA9IHRydWU7XG4gICAgICAgIGJyZWFrO1xuICAgICAgfVxuICAgICAgZXNjYXBlZCA9ICFlc2NhcGVkICYmIG5leHQgPT0gXCJcXFxcXCI7XG4gICAgfVxuICAgIGlmIChlbmQgfHwgIWVzY2FwZWQpIHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlO1xuICAgIHJldHVybiBcInN0cmluZ1wiO1xuICB9O1xufVxuZnVuY3Rpb24gYnVpbGRFbGVjdHJpY0lucHV0UmVnRXgoKSB7XG4gIC8vIFJlaW5kZW50YXRpb24gc2hvdWxkIG9jY3VyIG9uIFtdIG9yIG9uIGEgbWF0Y2ggb2YgYW55IG9mXG4gIC8vIHRoZSBibG9jayBjbG9zaW5nIGtleXdvcmRzLCBhdCB0aGUgZW5kIG9mIGEgbGluZS5cbiAgdmFyIGFsbENsb3NpbmdzID0gbWlkZGxlLmNvbmNhdChlbmQpO1xuICByZXR1cm4gbmV3IFJlZ0V4cChcIltcXFxcW1xcXFxdXXwoXCIgKyBhbGxDbG9zaW5ncy5qb2luKFwifFwiKSArIFwiKSRcIik7XG59XG5leHBvcnQgY29uc3Qgb3ogPSB7XG4gIG5hbWU6IFwib3pcIixcbiAgc3RhcnRTdGF0ZTogZnVuY3Rpb24gKCkge1xuICAgIHJldHVybiB7XG4gICAgICB0b2tlbml6ZTogdG9rZW5CYXNlLFxuICAgICAgY3VycmVudEluZGVudDogMCxcbiAgICAgIGRvSW5DdXJyZW50TGluZTogZmFsc2UsXG4gICAgICBoYXNQYXNzZWRGaXJzdFN0YWdlOiBmYWxzZVxuICAgIH07XG4gIH0sXG4gIHRva2VuOiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIGlmIChzdHJlYW0uc29sKCkpIHN0YXRlLmRvSW5DdXJyZW50TGluZSA9IDA7XG4gICAgcmV0dXJuIHN0YXRlLnRva2VuaXplKHN0cmVhbSwgc3RhdGUpO1xuICB9LFxuICBpbmRlbnQ6IGZ1bmN0aW9uIChzdGF0ZSwgdGV4dEFmdGVyLCBjeCkge1xuICAgIHZhciB0cnVlVGV4dCA9IHRleHRBZnRlci5yZXBsYWNlKC9eXFxzK3xcXHMrJC9nLCAnJyk7XG4gICAgaWYgKHRydWVUZXh0Lm1hdGNoKGVuZEtleXdvcmRzKSB8fCB0cnVlVGV4dC5tYXRjaChtaWRkbGVLZXl3b3JkcykgfHwgdHJ1ZVRleHQubWF0Y2goLyhcXFtdKS8pKSByZXR1cm4gY3gudW5pdCAqIChzdGF0ZS5jdXJyZW50SW5kZW50IC0gMSk7XG4gICAgaWYgKHN0YXRlLmN1cnJlbnRJbmRlbnQgPCAwKSByZXR1cm4gMDtcbiAgICByZXR1cm4gc3RhdGUuY3VycmVudEluZGVudCAqIGN4LnVuaXQ7XG4gIH0sXG4gIGxhbmd1YWdlRGF0YToge1xuICAgIGluZGVudE9uSW51dDogYnVpbGRFbGVjdHJpY0lucHV0UmVnRXgoKSxcbiAgICBjb21tZW50VG9rZW5zOiB7XG4gICAgICBsaW5lOiBcIiVcIixcbiAgICAgIGJsb2NrOiB7XG4gICAgICAgIG9wZW46IFwiLypcIixcbiAgICAgICAgY2xvc2U6IFwiKi9cIlxuICAgICAgfVxuICAgIH1cbiAgfVxufTsiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=