"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[7478],{

/***/ 27478:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "factor": () => (/* binding */ factor)
/* harmony export */ });
/* harmony import */ var _simple_mode_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(58053);

const factor = (0,_simple_mode_js__WEBPACK_IMPORTED_MODULE_0__/* .simpleMode */ .Q)({
  start: [
  // comments
  {
    regex: /#?!.*/,
    token: "comment"
  },
  // strings """, multiline --> state
  {
    regex: /"""/,
    token: "string",
    next: "string3"
  }, {
    regex: /(STRING:)(\s)/,
    token: ["keyword", null],
    next: "string2"
  }, {
    regex: /\S*?"/,
    token: "string",
    next: "string"
  },
  // numbers: dec, hex, unicode, bin, fractional, complex
  {
    regex: /(?:0x[\d,a-f]+)|(?:0o[0-7]+)|(?:0b[0,1]+)|(?:\-?\d+.?\d*)(?=\s)/,
    token: "number"
  },
  //{regex: /[+-]?/} //fractional
  // definition: defining word, defined word, etc
  {
    regex: /((?:GENERIC)|\:?\:)(\s+)(\S+)(\s+)(\()/,
    token: ["keyword", null, "def", null, "bracket"],
    next: "stack"
  },
  // method definition: defining word, type, defined word, etc
  {
    regex: /(M\:)(\s+)(\S+)(\s+)(\S+)/,
    token: ["keyword", null, "def", null, "tag"]
  },
  // vocabulary using --> state
  {
    regex: /USING\:/,
    token: "keyword",
    next: "vocabulary"
  },
  // vocabulary definition/use
  {
    regex: /(USE\:|IN\:)(\s+)(\S+)(?=\s|$)/,
    token: ["keyword", null, "tag"]
  },
  // definition: a defining word, defined word
  {
    regex: /(\S+\:)(\s+)(\S+)(?=\s|$)/,
    token: ["keyword", null, "def"]
  },
  // "keywords", incl. ; t f . [ ] { } defining words
  {
    regex: /(?:;|\\|t|f|if|loop|while|until|do|PRIVATE>|<PRIVATE|\.|\S*\[|\]|\S*\{|\})(?=\s|$)/,
    token: "keyword"
  },
  // <constructors> and the like
  {
    regex: /\S+[\)>\.\*\?]+(?=\s|$)/,
    token: "builtin"
  }, {
    regex: /[\)><]+\S+(?=\s|$)/,
    token: "builtin"
  },
  // operators
  {
    regex: /(?:[\+\-\=\/\*<>])(?=\s|$)/,
    token: "keyword"
  },
  // any id (?)
  {
    regex: /\S+/,
    token: "variable"
  }, {
    regex: /\s+|./,
    token: null
  }],
  vocabulary: [{
    regex: /;/,
    token: "keyword",
    next: "start"
  }, {
    regex: /\S+/,
    token: "tag"
  }, {
    regex: /\s+|./,
    token: null
  }],
  string: [{
    regex: /(?:[^\\]|\\.)*?"/,
    token: "string",
    next: "start"
  }, {
    regex: /.*/,
    token: "string"
  }],
  string2: [{
    regex: /^;/,
    token: "keyword",
    next: "start"
  }, {
    regex: /.*/,
    token: "string"
  }],
  string3: [{
    regex: /(?:[^\\]|\\.)*?"""/,
    token: "string",
    next: "start"
  }, {
    regex: /.*/,
    token: "string"
  }],
  stack: [{
    regex: /\)/,
    token: "bracket",
    next: "start"
  }, {
    regex: /--/,
    token: "bracket"
  }, {
    regex: /\S+/,
    token: "meta"
  }, {
    regex: /\s+|./,
    token: null
  }],
  languageData: {
    name: "factor",
    dontIndentStates: ["start", "vocabulary", "string", "string3", "stack"],
    commentTokens: {
      line: "!"
    }
  }
});

/***/ }),

/***/ 58053:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Q": () => (/* binding */ simpleMode)
/* harmony export */ });
function simpleMode(states) {
  ensureState(states, "start");
  var states_ = {},
    meta = states.languageData || {},
    hasIndentation = false;
  for (var state in states) if (state != meta && states.hasOwnProperty(state)) {
    var list = states_[state] = [],
      orig = states[state];
    for (var i = 0; i < orig.length; i++) {
      var data = orig[i];
      list.push(new Rule(data, states));
      if (data.indent || data.dedent) hasIndentation = true;
    }
  }
  return {
    name: meta.name,
    startState: function () {
      return {
        state: "start",
        pending: null,
        indent: hasIndentation ? [] : null
      };
    },
    copyState: function (state) {
      var s = {
        state: state.state,
        pending: state.pending,
        indent: state.indent && state.indent.slice(0)
      };
      if (state.stack) s.stack = state.stack.slice(0);
      return s;
    },
    token: tokenFunction(states_),
    indent: indentFunction(states_, meta),
    languageData: meta
  };
}
;
function ensureState(states, name) {
  if (!states.hasOwnProperty(name)) throw new Error("Undefined state " + name + " in simple mode");
}
function toRegex(val, caret) {
  if (!val) return /(?:)/;
  var flags = "";
  if (val instanceof RegExp) {
    if (val.ignoreCase) flags = "i";
    val = val.source;
  } else {
    val = String(val);
  }
  return new RegExp((caret === false ? "" : "^") + "(?:" + val + ")", flags);
}
function asToken(val) {
  if (!val) return null;
  if (val.apply) return val;
  if (typeof val == "string") return val.replace(/\./g, " ");
  var result = [];
  for (var i = 0; i < val.length; i++) result.push(val[i] && val[i].replace(/\./g, " "));
  return result;
}
function Rule(data, states) {
  if (data.next || data.push) ensureState(states, data.next || data.push);
  this.regex = toRegex(data.regex);
  this.token = asToken(data.token);
  this.data = data;
}
function tokenFunction(states) {
  return function (stream, state) {
    if (state.pending) {
      var pend = state.pending.shift();
      if (state.pending.length == 0) state.pending = null;
      stream.pos += pend.text.length;
      return pend.token;
    }
    var curState = states[state.state];
    for (var i = 0; i < curState.length; i++) {
      var rule = curState[i];
      var matches = (!rule.data.sol || stream.sol()) && stream.match(rule.regex);
      if (matches) {
        if (rule.data.next) {
          state.state = rule.data.next;
        } else if (rule.data.push) {
          (state.stack || (state.stack = [])).push(state.state);
          state.state = rule.data.push;
        } else if (rule.data.pop && state.stack && state.stack.length) {
          state.state = state.stack.pop();
        }
        if (rule.data.indent) state.indent.push(stream.indentation() + stream.indentUnit);
        if (rule.data.dedent) state.indent.pop();
        var token = rule.token;
        if (token && token.apply) token = token(matches);
        if (matches.length > 2 && rule.token && typeof rule.token != "string") {
          state.pending = [];
          for (var j = 2; j < matches.length; j++) if (matches[j]) state.pending.push({
            text: matches[j],
            token: rule.token[j - 1]
          });
          stream.backUp(matches[0].length - (matches[1] ? matches[1].length : 0));
          return token[0];
        } else if (token && token.join) {
          return token[0];
        } else {
          return token;
        }
      }
    }
    stream.next();
    return null;
  };
}
function indentFunction(states, meta) {
  return function (state, textAfter) {
    if (state.indent == null || meta.dontIndentStates && meta.doneIndentState.indexOf(state.state) > -1) return null;
    var pos = state.indent.length - 1,
      rules = states[state.state];
    scan: for (;;) {
      for (var i = 0; i < rules.length; i++) {
        var rule = rules[i];
        if (rule.data.dedent && rule.data.dedentIfLineStart !== false) {
          var m = rule.regex.exec(textAfter);
          if (m && m[0]) {
            pos--;
            if (rule.next || rule.push) rules = states[rule.next || rule.push];
            textAfter = textAfter.slice(m[0].length);
            continue scan;
          }
        }
      }
      break;
    }
    return pos < 0 ? 0 : state.indent[pos];
  };
}

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNzQ3OC5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7Ozs7Ozs7OztBQ3pJQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGNvZGVtaXJyb3IvbGVnYWN5LW1vZGVzL21vZGUvZmFjdG9yLmpzIiwid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGNvZGVtaXJyb3IvbGVnYWN5LW1vZGVzL21vZGUvc2ltcGxlLW1vZGUuanMiXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IHsgc2ltcGxlTW9kZSB9IGZyb20gXCIuL3NpbXBsZS1tb2RlLmpzXCI7XG5leHBvcnQgY29uc3QgZmFjdG9yID0gc2ltcGxlTW9kZSh7XG4gIHN0YXJ0OiBbXG4gIC8vIGNvbW1lbnRzXG4gIHtcbiAgICByZWdleDogLyM/IS4qLyxcbiAgICB0b2tlbjogXCJjb21tZW50XCJcbiAgfSxcbiAgLy8gc3RyaW5ncyBcIlwiXCIsIG11bHRpbGluZSAtLT4gc3RhdGVcbiAge1xuICAgIHJlZ2V4OiAvXCJcIlwiLyxcbiAgICB0b2tlbjogXCJzdHJpbmdcIixcbiAgICBuZXh0OiBcInN0cmluZzNcIlxuICB9LCB7XG4gICAgcmVnZXg6IC8oU1RSSU5HOikoXFxzKS8sXG4gICAgdG9rZW46IFtcImtleXdvcmRcIiwgbnVsbF0sXG4gICAgbmV4dDogXCJzdHJpbmcyXCJcbiAgfSwge1xuICAgIHJlZ2V4OiAvXFxTKj9cIi8sXG4gICAgdG9rZW46IFwic3RyaW5nXCIsXG4gICAgbmV4dDogXCJzdHJpbmdcIlxuICB9LFxuICAvLyBudW1iZXJzOiBkZWMsIGhleCwgdW5pY29kZSwgYmluLCBmcmFjdGlvbmFsLCBjb21wbGV4XG4gIHtcbiAgICByZWdleDogLyg/OjB4W1xcZCxhLWZdKyl8KD86MG9bMC03XSspfCg/OjBiWzAsMV0rKXwoPzpcXC0/XFxkKy4/XFxkKikoPz1cXHMpLyxcbiAgICB0b2tlbjogXCJudW1iZXJcIlxuICB9LFxuICAvL3tyZWdleDogL1srLV0/L30gLy9mcmFjdGlvbmFsXG4gIC8vIGRlZmluaXRpb246IGRlZmluaW5nIHdvcmQsIGRlZmluZWQgd29yZCwgZXRjXG4gIHtcbiAgICByZWdleDogLygoPzpHRU5FUklDKXxcXDo/XFw6KShcXHMrKShcXFMrKShcXHMrKShcXCgpLyxcbiAgICB0b2tlbjogW1wia2V5d29yZFwiLCBudWxsLCBcImRlZlwiLCBudWxsLCBcImJyYWNrZXRcIl0sXG4gICAgbmV4dDogXCJzdGFja1wiXG4gIH0sXG4gIC8vIG1ldGhvZCBkZWZpbml0aW9uOiBkZWZpbmluZyB3b3JkLCB0eXBlLCBkZWZpbmVkIHdvcmQsIGV0Y1xuICB7XG4gICAgcmVnZXg6IC8oTVxcOikoXFxzKykoXFxTKykoXFxzKykoXFxTKykvLFxuICAgIHRva2VuOiBbXCJrZXl3b3JkXCIsIG51bGwsIFwiZGVmXCIsIG51bGwsIFwidGFnXCJdXG4gIH0sXG4gIC8vIHZvY2FidWxhcnkgdXNpbmcgLS0+IHN0YXRlXG4gIHtcbiAgICByZWdleDogL1VTSU5HXFw6LyxcbiAgICB0b2tlbjogXCJrZXl3b3JkXCIsXG4gICAgbmV4dDogXCJ2b2NhYnVsYXJ5XCJcbiAgfSxcbiAgLy8gdm9jYWJ1bGFyeSBkZWZpbml0aW9uL3VzZVxuICB7XG4gICAgcmVnZXg6IC8oVVNFXFw6fElOXFw6KShcXHMrKShcXFMrKSg/PVxcc3wkKS8sXG4gICAgdG9rZW46IFtcImtleXdvcmRcIiwgbnVsbCwgXCJ0YWdcIl1cbiAgfSxcbiAgLy8gZGVmaW5pdGlvbjogYSBkZWZpbmluZyB3b3JkLCBkZWZpbmVkIHdvcmRcbiAge1xuICAgIHJlZ2V4OiAvKFxcUytcXDopKFxccyspKFxcUyspKD89XFxzfCQpLyxcbiAgICB0b2tlbjogW1wia2V5d29yZFwiLCBudWxsLCBcImRlZlwiXVxuICB9LFxuICAvLyBcImtleXdvcmRzXCIsIGluY2wuIDsgdCBmIC4gWyBdIHsgfSBkZWZpbmluZyB3b3Jkc1xuICB7XG4gICAgcmVnZXg6IC8oPzo7fFxcXFx8dHxmfGlmfGxvb3B8d2hpbGV8dW50aWx8ZG98UFJJVkFURT58PFBSSVZBVEV8XFwufFxcUypcXFt8XFxdfFxcUypcXHt8XFx9KSg/PVxcc3wkKS8sXG4gICAgdG9rZW46IFwia2V5d29yZFwiXG4gIH0sXG4gIC8vIDxjb25zdHJ1Y3RvcnM+IGFuZCB0aGUgbGlrZVxuICB7XG4gICAgcmVnZXg6IC9cXFMrW1xcKT5cXC5cXCpcXD9dKyg/PVxcc3wkKS8sXG4gICAgdG9rZW46IFwiYnVpbHRpblwiXG4gIH0sIHtcbiAgICByZWdleDogL1tcXCk+PF0rXFxTKyg/PVxcc3wkKS8sXG4gICAgdG9rZW46IFwiYnVpbHRpblwiXG4gIH0sXG4gIC8vIG9wZXJhdG9yc1xuICB7XG4gICAgcmVnZXg6IC8oPzpbXFwrXFwtXFw9XFwvXFwqPD5dKSg/PVxcc3wkKS8sXG4gICAgdG9rZW46IFwia2V5d29yZFwiXG4gIH0sXG4gIC8vIGFueSBpZCAoPylcbiAge1xuICAgIHJlZ2V4OiAvXFxTKy8sXG4gICAgdG9rZW46IFwidmFyaWFibGVcIlxuICB9LCB7XG4gICAgcmVnZXg6IC9cXHMrfC4vLFxuICAgIHRva2VuOiBudWxsXG4gIH1dLFxuICB2b2NhYnVsYXJ5OiBbe1xuICAgIHJlZ2V4OiAvOy8sXG4gICAgdG9rZW46IFwia2V5d29yZFwiLFxuICAgIG5leHQ6IFwic3RhcnRcIlxuICB9LCB7XG4gICAgcmVnZXg6IC9cXFMrLyxcbiAgICB0b2tlbjogXCJ0YWdcIlxuICB9LCB7XG4gICAgcmVnZXg6IC9cXHMrfC4vLFxuICAgIHRva2VuOiBudWxsXG4gIH1dLFxuICBzdHJpbmc6IFt7XG4gICAgcmVnZXg6IC8oPzpbXlxcXFxdfFxcXFwuKSo/XCIvLFxuICAgIHRva2VuOiBcInN0cmluZ1wiLFxuICAgIG5leHQ6IFwic3RhcnRcIlxuICB9LCB7XG4gICAgcmVnZXg6IC8uKi8sXG4gICAgdG9rZW46IFwic3RyaW5nXCJcbiAgfV0sXG4gIHN0cmluZzI6IFt7XG4gICAgcmVnZXg6IC9eOy8sXG4gICAgdG9rZW46IFwia2V5d29yZFwiLFxuICAgIG5leHQ6IFwic3RhcnRcIlxuICB9LCB7XG4gICAgcmVnZXg6IC8uKi8sXG4gICAgdG9rZW46IFwic3RyaW5nXCJcbiAgfV0sXG4gIHN0cmluZzM6IFt7XG4gICAgcmVnZXg6IC8oPzpbXlxcXFxdfFxcXFwuKSo/XCJcIlwiLyxcbiAgICB0b2tlbjogXCJzdHJpbmdcIixcbiAgICBuZXh0OiBcInN0YXJ0XCJcbiAgfSwge1xuICAgIHJlZ2V4OiAvLiovLFxuICAgIHRva2VuOiBcInN0cmluZ1wiXG4gIH1dLFxuICBzdGFjazogW3tcbiAgICByZWdleDogL1xcKS8sXG4gICAgdG9rZW46IFwiYnJhY2tldFwiLFxuICAgIG5leHQ6IFwic3RhcnRcIlxuICB9LCB7XG4gICAgcmVnZXg6IC8tLS8sXG4gICAgdG9rZW46IFwiYnJhY2tldFwiXG4gIH0sIHtcbiAgICByZWdleDogL1xcUysvLFxuICAgIHRva2VuOiBcIm1ldGFcIlxuICB9LCB7XG4gICAgcmVnZXg6IC9cXHMrfC4vLFxuICAgIHRva2VuOiBudWxsXG4gIH1dLFxuICBsYW5ndWFnZURhdGE6IHtcbiAgICBuYW1lOiBcImZhY3RvclwiLFxuICAgIGRvbnRJbmRlbnRTdGF0ZXM6IFtcInN0YXJ0XCIsIFwidm9jYWJ1bGFyeVwiLCBcInN0cmluZ1wiLCBcInN0cmluZzNcIiwgXCJzdGFja1wiXSxcbiAgICBjb21tZW50VG9rZW5zOiB7XG4gICAgICBsaW5lOiBcIiFcIlxuICAgIH1cbiAgfVxufSk7IiwiZXhwb3J0IGZ1bmN0aW9uIHNpbXBsZU1vZGUoc3RhdGVzKSB7XG4gIGVuc3VyZVN0YXRlKHN0YXRlcywgXCJzdGFydFwiKTtcbiAgdmFyIHN0YXRlc18gPSB7fSxcbiAgICBtZXRhID0gc3RhdGVzLmxhbmd1YWdlRGF0YSB8fCB7fSxcbiAgICBoYXNJbmRlbnRhdGlvbiA9IGZhbHNlO1xuICBmb3IgKHZhciBzdGF0ZSBpbiBzdGF0ZXMpIGlmIChzdGF0ZSAhPSBtZXRhICYmIHN0YXRlcy5oYXNPd25Qcm9wZXJ0eShzdGF0ZSkpIHtcbiAgICB2YXIgbGlzdCA9IHN0YXRlc19bc3RhdGVdID0gW10sXG4gICAgICBvcmlnID0gc3RhdGVzW3N0YXRlXTtcbiAgICBmb3IgKHZhciBpID0gMDsgaSA8IG9yaWcubGVuZ3RoOyBpKyspIHtcbiAgICAgIHZhciBkYXRhID0gb3JpZ1tpXTtcbiAgICAgIGxpc3QucHVzaChuZXcgUnVsZShkYXRhLCBzdGF0ZXMpKTtcbiAgICAgIGlmIChkYXRhLmluZGVudCB8fCBkYXRhLmRlZGVudCkgaGFzSW5kZW50YXRpb24gPSB0cnVlO1xuICAgIH1cbiAgfVxuICByZXR1cm4ge1xuICAgIG5hbWU6IG1ldGEubmFtZSxcbiAgICBzdGFydFN0YXRlOiBmdW5jdGlvbiAoKSB7XG4gICAgICByZXR1cm4ge1xuICAgICAgICBzdGF0ZTogXCJzdGFydFwiLFxuICAgICAgICBwZW5kaW5nOiBudWxsLFxuICAgICAgICBpbmRlbnQ6IGhhc0luZGVudGF0aW9uID8gW10gOiBudWxsXG4gICAgICB9O1xuICAgIH0sXG4gICAgY29weVN0YXRlOiBmdW5jdGlvbiAoc3RhdGUpIHtcbiAgICAgIHZhciBzID0ge1xuICAgICAgICBzdGF0ZTogc3RhdGUuc3RhdGUsXG4gICAgICAgIHBlbmRpbmc6IHN0YXRlLnBlbmRpbmcsXG4gICAgICAgIGluZGVudDogc3RhdGUuaW5kZW50ICYmIHN0YXRlLmluZGVudC5zbGljZSgwKVxuICAgICAgfTtcbiAgICAgIGlmIChzdGF0ZS5zdGFjaykgcy5zdGFjayA9IHN0YXRlLnN0YWNrLnNsaWNlKDApO1xuICAgICAgcmV0dXJuIHM7XG4gICAgfSxcbiAgICB0b2tlbjogdG9rZW5GdW5jdGlvbihzdGF0ZXNfKSxcbiAgICBpbmRlbnQ6IGluZGVudEZ1bmN0aW9uKHN0YXRlc18sIG1ldGEpLFxuICAgIGxhbmd1YWdlRGF0YTogbWV0YVxuICB9O1xufVxuO1xuZnVuY3Rpb24gZW5zdXJlU3RhdGUoc3RhdGVzLCBuYW1lKSB7XG4gIGlmICghc3RhdGVzLmhhc093blByb3BlcnR5KG5hbWUpKSB0aHJvdyBuZXcgRXJyb3IoXCJVbmRlZmluZWQgc3RhdGUgXCIgKyBuYW1lICsgXCIgaW4gc2ltcGxlIG1vZGVcIik7XG59XG5mdW5jdGlvbiB0b1JlZ2V4KHZhbCwgY2FyZXQpIHtcbiAgaWYgKCF2YWwpIHJldHVybiAvKD86KS87XG4gIHZhciBmbGFncyA9IFwiXCI7XG4gIGlmICh2YWwgaW5zdGFuY2VvZiBSZWdFeHApIHtcbiAgICBpZiAodmFsLmlnbm9yZUNhc2UpIGZsYWdzID0gXCJpXCI7XG4gICAgdmFsID0gdmFsLnNvdXJjZTtcbiAgfSBlbHNlIHtcbiAgICB2YWwgPSBTdHJpbmcodmFsKTtcbiAgfVxuICByZXR1cm4gbmV3IFJlZ0V4cCgoY2FyZXQgPT09IGZhbHNlID8gXCJcIiA6IFwiXlwiKSArIFwiKD86XCIgKyB2YWwgKyBcIilcIiwgZmxhZ3MpO1xufVxuZnVuY3Rpb24gYXNUb2tlbih2YWwpIHtcbiAgaWYgKCF2YWwpIHJldHVybiBudWxsO1xuICBpZiAodmFsLmFwcGx5KSByZXR1cm4gdmFsO1xuICBpZiAodHlwZW9mIHZhbCA9PSBcInN0cmluZ1wiKSByZXR1cm4gdmFsLnJlcGxhY2UoL1xcLi9nLCBcIiBcIik7XG4gIHZhciByZXN1bHQgPSBbXTtcbiAgZm9yICh2YXIgaSA9IDA7IGkgPCB2YWwubGVuZ3RoOyBpKyspIHJlc3VsdC5wdXNoKHZhbFtpXSAmJiB2YWxbaV0ucmVwbGFjZSgvXFwuL2csIFwiIFwiKSk7XG4gIHJldHVybiByZXN1bHQ7XG59XG5mdW5jdGlvbiBSdWxlKGRhdGEsIHN0YXRlcykge1xuICBpZiAoZGF0YS5uZXh0IHx8IGRhdGEucHVzaCkgZW5zdXJlU3RhdGUoc3RhdGVzLCBkYXRhLm5leHQgfHwgZGF0YS5wdXNoKTtcbiAgdGhpcy5yZWdleCA9IHRvUmVnZXgoZGF0YS5yZWdleCk7XG4gIHRoaXMudG9rZW4gPSBhc1Rva2VuKGRhdGEudG9rZW4pO1xuICB0aGlzLmRhdGEgPSBkYXRhO1xufVxuZnVuY3Rpb24gdG9rZW5GdW5jdGlvbihzdGF0ZXMpIHtcbiAgcmV0dXJuIGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgaWYgKHN0YXRlLnBlbmRpbmcpIHtcbiAgICAgIHZhciBwZW5kID0gc3RhdGUucGVuZGluZy5zaGlmdCgpO1xuICAgICAgaWYgKHN0YXRlLnBlbmRpbmcubGVuZ3RoID09IDApIHN0YXRlLnBlbmRpbmcgPSBudWxsO1xuICAgICAgc3RyZWFtLnBvcyArPSBwZW5kLnRleHQubGVuZ3RoO1xuICAgICAgcmV0dXJuIHBlbmQudG9rZW47XG4gICAgfVxuICAgIHZhciBjdXJTdGF0ZSA9IHN0YXRlc1tzdGF0ZS5zdGF0ZV07XG4gICAgZm9yICh2YXIgaSA9IDA7IGkgPCBjdXJTdGF0ZS5sZW5ndGg7IGkrKykge1xuICAgICAgdmFyIHJ1bGUgPSBjdXJTdGF0ZVtpXTtcbiAgICAgIHZhciBtYXRjaGVzID0gKCFydWxlLmRhdGEuc29sIHx8IHN0cmVhbS5zb2woKSkgJiYgc3RyZWFtLm1hdGNoKHJ1bGUucmVnZXgpO1xuICAgICAgaWYgKG1hdGNoZXMpIHtcbiAgICAgICAgaWYgKHJ1bGUuZGF0YS5uZXh0KSB7XG4gICAgICAgICAgc3RhdGUuc3RhdGUgPSBydWxlLmRhdGEubmV4dDtcbiAgICAgICAgfSBlbHNlIGlmIChydWxlLmRhdGEucHVzaCkge1xuICAgICAgICAgIChzdGF0ZS5zdGFjayB8fCAoc3RhdGUuc3RhY2sgPSBbXSkpLnB1c2goc3RhdGUuc3RhdGUpO1xuICAgICAgICAgIHN0YXRlLnN0YXRlID0gcnVsZS5kYXRhLnB1c2g7XG4gICAgICAgIH0gZWxzZSBpZiAocnVsZS5kYXRhLnBvcCAmJiBzdGF0ZS5zdGFjayAmJiBzdGF0ZS5zdGFjay5sZW5ndGgpIHtcbiAgICAgICAgICBzdGF0ZS5zdGF0ZSA9IHN0YXRlLnN0YWNrLnBvcCgpO1xuICAgICAgICB9XG4gICAgICAgIGlmIChydWxlLmRhdGEuaW5kZW50KSBzdGF0ZS5pbmRlbnQucHVzaChzdHJlYW0uaW5kZW50YXRpb24oKSArIHN0cmVhbS5pbmRlbnRVbml0KTtcbiAgICAgICAgaWYgKHJ1bGUuZGF0YS5kZWRlbnQpIHN0YXRlLmluZGVudC5wb3AoKTtcbiAgICAgICAgdmFyIHRva2VuID0gcnVsZS50b2tlbjtcbiAgICAgICAgaWYgKHRva2VuICYmIHRva2VuLmFwcGx5KSB0b2tlbiA9IHRva2VuKG1hdGNoZXMpO1xuICAgICAgICBpZiAobWF0Y2hlcy5sZW5ndGggPiAyICYmIHJ1bGUudG9rZW4gJiYgdHlwZW9mIHJ1bGUudG9rZW4gIT0gXCJzdHJpbmdcIikge1xuICAgICAgICAgIHN0YXRlLnBlbmRpbmcgPSBbXTtcbiAgICAgICAgICBmb3IgKHZhciBqID0gMjsgaiA8IG1hdGNoZXMubGVuZ3RoOyBqKyspIGlmIChtYXRjaGVzW2pdKSBzdGF0ZS5wZW5kaW5nLnB1c2goe1xuICAgICAgICAgICAgdGV4dDogbWF0Y2hlc1tqXSxcbiAgICAgICAgICAgIHRva2VuOiBydWxlLnRva2VuW2ogLSAxXVxuICAgICAgICAgIH0pO1xuICAgICAgICAgIHN0cmVhbS5iYWNrVXAobWF0Y2hlc1swXS5sZW5ndGggLSAobWF0Y2hlc1sxXSA/IG1hdGNoZXNbMV0ubGVuZ3RoIDogMCkpO1xuICAgICAgICAgIHJldHVybiB0b2tlblswXTtcbiAgICAgICAgfSBlbHNlIGlmICh0b2tlbiAmJiB0b2tlbi5qb2luKSB7XG4gICAgICAgICAgcmV0dXJuIHRva2VuWzBdO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgIHJldHVybiB0b2tlbjtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH1cbiAgICBzdHJlYW0ubmV4dCgpO1xuICAgIHJldHVybiBudWxsO1xuICB9O1xufVxuZnVuY3Rpb24gaW5kZW50RnVuY3Rpb24oc3RhdGVzLCBtZXRhKSB7XG4gIHJldHVybiBmdW5jdGlvbiAoc3RhdGUsIHRleHRBZnRlcikge1xuICAgIGlmIChzdGF0ZS5pbmRlbnQgPT0gbnVsbCB8fCBtZXRhLmRvbnRJbmRlbnRTdGF0ZXMgJiYgbWV0YS5kb25lSW5kZW50U3RhdGUuaW5kZXhPZihzdGF0ZS5zdGF0ZSkgPiAtMSkgcmV0dXJuIG51bGw7XG4gICAgdmFyIHBvcyA9IHN0YXRlLmluZGVudC5sZW5ndGggLSAxLFxuICAgICAgcnVsZXMgPSBzdGF0ZXNbc3RhdGUuc3RhdGVdO1xuICAgIHNjYW46IGZvciAoOzspIHtcbiAgICAgIGZvciAodmFyIGkgPSAwOyBpIDwgcnVsZXMubGVuZ3RoOyBpKyspIHtcbiAgICAgICAgdmFyIHJ1bGUgPSBydWxlc1tpXTtcbiAgICAgICAgaWYgKHJ1bGUuZGF0YS5kZWRlbnQgJiYgcnVsZS5kYXRhLmRlZGVudElmTGluZVN0YXJ0ICE9PSBmYWxzZSkge1xuICAgICAgICAgIHZhciBtID0gcnVsZS5yZWdleC5leGVjKHRleHRBZnRlcik7XG4gICAgICAgICAgaWYgKG0gJiYgbVswXSkge1xuICAgICAgICAgICAgcG9zLS07XG4gICAgICAgICAgICBpZiAocnVsZS5uZXh0IHx8IHJ1bGUucHVzaCkgcnVsZXMgPSBzdGF0ZXNbcnVsZS5uZXh0IHx8IHJ1bGUucHVzaF07XG4gICAgICAgICAgICB0ZXh0QWZ0ZXIgPSB0ZXh0QWZ0ZXIuc2xpY2UobVswXS5sZW5ndGgpO1xuICAgICAgICAgICAgY29udGludWUgc2NhbjtcbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICAgIGJyZWFrO1xuICAgIH1cbiAgICByZXR1cm4gcG9zIDwgMCA/IDAgOiBzdGF0ZS5pbmRlbnRbcG9zXTtcbiAgfTtcbn0iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=