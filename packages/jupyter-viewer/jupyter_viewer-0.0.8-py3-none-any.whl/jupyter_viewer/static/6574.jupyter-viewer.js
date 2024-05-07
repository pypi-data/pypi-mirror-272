"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[6574],{

/***/ 47413:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "dockerFile": () => (/* binding */ dockerFile)
/* harmony export */ });
/* harmony import */ var _simple_mode_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(58053);

var from = "from";
var fromRegex = new RegExp("^(\\s*)\\b(" + from + ")\\b", "i");
var shells = ["run", "cmd", "entrypoint", "shell"];
var shellsAsArrayRegex = new RegExp("^(\\s*)(" + shells.join('|') + ")(\\s+\\[)", "i");
var expose = "expose";
var exposeRegex = new RegExp("^(\\s*)(" + expose + ")(\\s+)", "i");
var others = ["arg", "from", "maintainer", "label", "env", "add", "copy", "volume", "user", "workdir", "onbuild", "stopsignal", "healthcheck", "shell"];

// Collect all Dockerfile directives
var instructions = [from, expose].concat(shells).concat(others),
  instructionRegex = "(" + instructions.join('|') + ")",
  instructionOnlyLine = new RegExp("^(\\s*)" + instructionRegex + "(\\s*)(#.*)?$", "i"),
  instructionWithArguments = new RegExp("^(\\s*)" + instructionRegex + "(\\s+)", "i");
const dockerFile = (0,_simple_mode_js__WEBPACK_IMPORTED_MODULE_0__/* .simpleMode */ .Q)({
  start: [
  // Block comment: This is a line starting with a comment
  {
    regex: /^\s*#.*$/,
    sol: true,
    token: "comment"
  }, {
    regex: fromRegex,
    token: [null, "keyword"],
    sol: true,
    next: "from"
  },
  // Highlight an instruction without any arguments (for convenience)
  {
    regex: instructionOnlyLine,
    token: [null, "keyword", null, "error"],
    sol: true
  }, {
    regex: shellsAsArrayRegex,
    token: [null, "keyword", null],
    sol: true,
    next: "array"
  }, {
    regex: exposeRegex,
    token: [null, "keyword", null],
    sol: true,
    next: "expose"
  },
  // Highlight an instruction followed by arguments
  {
    regex: instructionWithArguments,
    token: [null, "keyword", null],
    sol: true,
    next: "arguments"
  }, {
    regex: /./,
    token: null
  }],
  from: [{
    regex: /\s*$/,
    token: null,
    next: "start"
  }, {
    // Line comment without instruction arguments is an error
    regex: /(\s*)(#.*)$/,
    token: [null, "error"],
    next: "start"
  }, {
    regex: /(\s*\S+\s+)(as)/i,
    token: [null, "keyword"],
    next: "start"
  },
  // Fail safe return to start
  {
    token: null,
    next: "start"
  }],
  single: [{
    regex: /(?:[^\\']|\\.)/,
    token: "string"
  }, {
    regex: /'/,
    token: "string",
    pop: true
  }],
  double: [{
    regex: /(?:[^\\"]|\\.)/,
    token: "string"
  }, {
    regex: /"/,
    token: "string",
    pop: true
  }],
  array: [{
    regex: /\]/,
    token: null,
    next: "start"
  }, {
    regex: /"(?:[^\\"]|\\.)*"?/,
    token: "string"
  }],
  expose: [{
    regex: /\d+$/,
    token: "number",
    next: "start"
  }, {
    regex: /[^\d]+$/,
    token: null,
    next: "start"
  }, {
    regex: /\d+/,
    token: "number"
  }, {
    regex: /[^\d]+/,
    token: null
  },
  // Fail safe return to start
  {
    token: null,
    next: "start"
  }],
  arguments: [{
    regex: /^\s*#.*$/,
    sol: true,
    token: "comment"
  }, {
    regex: /"(?:[^\\"]|\\.)*"?$/,
    token: "string",
    next: "start"
  }, {
    regex: /"/,
    token: "string",
    push: "double"
  }, {
    regex: /'(?:[^\\']|\\.)*'?$/,
    token: "string",
    next: "start"
  }, {
    regex: /'/,
    token: "string",
    push: "single"
  }, {
    regex: /[^#"']+[\\`]$/,
    token: null
  }, {
    regex: /[^#"']+$/,
    token: null,
    next: "start"
  }, {
    regex: /[^#"']+/,
    token: null
  },
  // Fail safe return to start
  {
    token: null,
    next: "start"
  }],
  languageData: {
    commentTokens: {
      line: "#"
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
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNjU3NC5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7Ozs7Ozs7Ozs7QUM3SkE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL0Bjb2RlbWlycm9yL2xlZ2FjeS1tb2Rlcy9tb2RlL2RvY2tlcmZpbGUuanMiLCJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9AY29kZW1pcnJvci9sZWdhY3ktbW9kZXMvbW9kZS9zaW1wbGUtbW9kZS5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgeyBzaW1wbGVNb2RlIH0gZnJvbSBcIi4vc2ltcGxlLW1vZGUuanNcIjtcbnZhciBmcm9tID0gXCJmcm9tXCI7XG52YXIgZnJvbVJlZ2V4ID0gbmV3IFJlZ0V4cChcIl4oXFxcXHMqKVxcXFxiKFwiICsgZnJvbSArIFwiKVxcXFxiXCIsIFwiaVwiKTtcbnZhciBzaGVsbHMgPSBbXCJydW5cIiwgXCJjbWRcIiwgXCJlbnRyeXBvaW50XCIsIFwic2hlbGxcIl07XG52YXIgc2hlbGxzQXNBcnJheVJlZ2V4ID0gbmV3IFJlZ0V4cChcIl4oXFxcXHMqKShcIiArIHNoZWxscy5qb2luKCd8JykgKyBcIikoXFxcXHMrXFxcXFspXCIsIFwiaVwiKTtcbnZhciBleHBvc2UgPSBcImV4cG9zZVwiO1xudmFyIGV4cG9zZVJlZ2V4ID0gbmV3IFJlZ0V4cChcIl4oXFxcXHMqKShcIiArIGV4cG9zZSArIFwiKShcXFxccyspXCIsIFwiaVwiKTtcbnZhciBvdGhlcnMgPSBbXCJhcmdcIiwgXCJmcm9tXCIsIFwibWFpbnRhaW5lclwiLCBcImxhYmVsXCIsIFwiZW52XCIsIFwiYWRkXCIsIFwiY29weVwiLCBcInZvbHVtZVwiLCBcInVzZXJcIiwgXCJ3b3JrZGlyXCIsIFwib25idWlsZFwiLCBcInN0b3BzaWduYWxcIiwgXCJoZWFsdGhjaGVja1wiLCBcInNoZWxsXCJdO1xuXG4vLyBDb2xsZWN0IGFsbCBEb2NrZXJmaWxlIGRpcmVjdGl2ZXNcbnZhciBpbnN0cnVjdGlvbnMgPSBbZnJvbSwgZXhwb3NlXS5jb25jYXQoc2hlbGxzKS5jb25jYXQob3RoZXJzKSxcbiAgaW5zdHJ1Y3Rpb25SZWdleCA9IFwiKFwiICsgaW5zdHJ1Y3Rpb25zLmpvaW4oJ3wnKSArIFwiKVwiLFxuICBpbnN0cnVjdGlvbk9ubHlMaW5lID0gbmV3IFJlZ0V4cChcIl4oXFxcXHMqKVwiICsgaW5zdHJ1Y3Rpb25SZWdleCArIFwiKFxcXFxzKikoIy4qKT8kXCIsIFwiaVwiKSxcbiAgaW5zdHJ1Y3Rpb25XaXRoQXJndW1lbnRzID0gbmV3IFJlZ0V4cChcIl4oXFxcXHMqKVwiICsgaW5zdHJ1Y3Rpb25SZWdleCArIFwiKFxcXFxzKylcIiwgXCJpXCIpO1xuZXhwb3J0IGNvbnN0IGRvY2tlckZpbGUgPSBzaW1wbGVNb2RlKHtcbiAgc3RhcnQ6IFtcbiAgLy8gQmxvY2sgY29tbWVudDogVGhpcyBpcyBhIGxpbmUgc3RhcnRpbmcgd2l0aCBhIGNvbW1lbnRcbiAge1xuICAgIHJlZ2V4OiAvXlxccyojLiokLyxcbiAgICBzb2w6IHRydWUsXG4gICAgdG9rZW46IFwiY29tbWVudFwiXG4gIH0sIHtcbiAgICByZWdleDogZnJvbVJlZ2V4LFxuICAgIHRva2VuOiBbbnVsbCwgXCJrZXl3b3JkXCJdLFxuICAgIHNvbDogdHJ1ZSxcbiAgICBuZXh0OiBcImZyb21cIlxuICB9LFxuICAvLyBIaWdobGlnaHQgYW4gaW5zdHJ1Y3Rpb24gd2l0aG91dCBhbnkgYXJndW1lbnRzIChmb3IgY29udmVuaWVuY2UpXG4gIHtcbiAgICByZWdleDogaW5zdHJ1Y3Rpb25Pbmx5TGluZSxcbiAgICB0b2tlbjogW251bGwsIFwia2V5d29yZFwiLCBudWxsLCBcImVycm9yXCJdLFxuICAgIHNvbDogdHJ1ZVxuICB9LCB7XG4gICAgcmVnZXg6IHNoZWxsc0FzQXJyYXlSZWdleCxcbiAgICB0b2tlbjogW251bGwsIFwia2V5d29yZFwiLCBudWxsXSxcbiAgICBzb2w6IHRydWUsXG4gICAgbmV4dDogXCJhcnJheVwiXG4gIH0sIHtcbiAgICByZWdleDogZXhwb3NlUmVnZXgsXG4gICAgdG9rZW46IFtudWxsLCBcImtleXdvcmRcIiwgbnVsbF0sXG4gICAgc29sOiB0cnVlLFxuICAgIG5leHQ6IFwiZXhwb3NlXCJcbiAgfSxcbiAgLy8gSGlnaGxpZ2h0IGFuIGluc3RydWN0aW9uIGZvbGxvd2VkIGJ5IGFyZ3VtZW50c1xuICB7XG4gICAgcmVnZXg6IGluc3RydWN0aW9uV2l0aEFyZ3VtZW50cyxcbiAgICB0b2tlbjogW251bGwsIFwia2V5d29yZFwiLCBudWxsXSxcbiAgICBzb2w6IHRydWUsXG4gICAgbmV4dDogXCJhcmd1bWVudHNcIlxuICB9LCB7XG4gICAgcmVnZXg6IC8uLyxcbiAgICB0b2tlbjogbnVsbFxuICB9XSxcbiAgZnJvbTogW3tcbiAgICByZWdleDogL1xccyokLyxcbiAgICB0b2tlbjogbnVsbCxcbiAgICBuZXh0OiBcInN0YXJ0XCJcbiAgfSwge1xuICAgIC8vIExpbmUgY29tbWVudCB3aXRob3V0IGluc3RydWN0aW9uIGFyZ3VtZW50cyBpcyBhbiBlcnJvclxuICAgIHJlZ2V4OiAvKFxccyopKCMuKikkLyxcbiAgICB0b2tlbjogW251bGwsIFwiZXJyb3JcIl0sXG4gICAgbmV4dDogXCJzdGFydFwiXG4gIH0sIHtcbiAgICByZWdleDogLyhcXHMqXFxTK1xccyspKGFzKS9pLFxuICAgIHRva2VuOiBbbnVsbCwgXCJrZXl3b3JkXCJdLFxuICAgIG5leHQ6IFwic3RhcnRcIlxuICB9LFxuICAvLyBGYWlsIHNhZmUgcmV0dXJuIHRvIHN0YXJ0XG4gIHtcbiAgICB0b2tlbjogbnVsbCxcbiAgICBuZXh0OiBcInN0YXJ0XCJcbiAgfV0sXG4gIHNpbmdsZTogW3tcbiAgICByZWdleDogLyg/OlteXFxcXCddfFxcXFwuKS8sXG4gICAgdG9rZW46IFwic3RyaW5nXCJcbiAgfSwge1xuICAgIHJlZ2V4OiAvJy8sXG4gICAgdG9rZW46IFwic3RyaW5nXCIsXG4gICAgcG9wOiB0cnVlXG4gIH1dLFxuICBkb3VibGU6IFt7XG4gICAgcmVnZXg6IC8oPzpbXlxcXFxcIl18XFxcXC4pLyxcbiAgICB0b2tlbjogXCJzdHJpbmdcIlxuICB9LCB7XG4gICAgcmVnZXg6IC9cIi8sXG4gICAgdG9rZW46IFwic3RyaW5nXCIsXG4gICAgcG9wOiB0cnVlXG4gIH1dLFxuICBhcnJheTogW3tcbiAgICByZWdleDogL1xcXS8sXG4gICAgdG9rZW46IG51bGwsXG4gICAgbmV4dDogXCJzdGFydFwiXG4gIH0sIHtcbiAgICByZWdleDogL1wiKD86W15cXFxcXCJdfFxcXFwuKSpcIj8vLFxuICAgIHRva2VuOiBcInN0cmluZ1wiXG4gIH1dLFxuICBleHBvc2U6IFt7XG4gICAgcmVnZXg6IC9cXGQrJC8sXG4gICAgdG9rZW46IFwibnVtYmVyXCIsXG4gICAgbmV4dDogXCJzdGFydFwiXG4gIH0sIHtcbiAgICByZWdleDogL1teXFxkXSskLyxcbiAgICB0b2tlbjogbnVsbCxcbiAgICBuZXh0OiBcInN0YXJ0XCJcbiAgfSwge1xuICAgIHJlZ2V4OiAvXFxkKy8sXG4gICAgdG9rZW46IFwibnVtYmVyXCJcbiAgfSwge1xuICAgIHJlZ2V4OiAvW15cXGRdKy8sXG4gICAgdG9rZW46IG51bGxcbiAgfSxcbiAgLy8gRmFpbCBzYWZlIHJldHVybiB0byBzdGFydFxuICB7XG4gICAgdG9rZW46IG51bGwsXG4gICAgbmV4dDogXCJzdGFydFwiXG4gIH1dLFxuICBhcmd1bWVudHM6IFt7XG4gICAgcmVnZXg6IC9eXFxzKiMuKiQvLFxuICAgIHNvbDogdHJ1ZSxcbiAgICB0b2tlbjogXCJjb21tZW50XCJcbiAgfSwge1xuICAgIHJlZ2V4OiAvXCIoPzpbXlxcXFxcIl18XFxcXC4pKlwiPyQvLFxuICAgIHRva2VuOiBcInN0cmluZ1wiLFxuICAgIG5leHQ6IFwic3RhcnRcIlxuICB9LCB7XG4gICAgcmVnZXg6IC9cIi8sXG4gICAgdG9rZW46IFwic3RyaW5nXCIsXG4gICAgcHVzaDogXCJkb3VibGVcIlxuICB9LCB7XG4gICAgcmVnZXg6IC8nKD86W15cXFxcJ118XFxcXC4pKic/JC8sXG4gICAgdG9rZW46IFwic3RyaW5nXCIsXG4gICAgbmV4dDogXCJzdGFydFwiXG4gIH0sIHtcbiAgICByZWdleDogLycvLFxuICAgIHRva2VuOiBcInN0cmluZ1wiLFxuICAgIHB1c2g6IFwic2luZ2xlXCJcbiAgfSwge1xuICAgIHJlZ2V4OiAvW14jXCInXStbXFxcXGBdJC8sXG4gICAgdG9rZW46IG51bGxcbiAgfSwge1xuICAgIHJlZ2V4OiAvW14jXCInXSskLyxcbiAgICB0b2tlbjogbnVsbCxcbiAgICBuZXh0OiBcInN0YXJ0XCJcbiAgfSwge1xuICAgIHJlZ2V4OiAvW14jXCInXSsvLFxuICAgIHRva2VuOiBudWxsXG4gIH0sXG4gIC8vIEZhaWwgc2FmZSByZXR1cm4gdG8gc3RhcnRcbiAge1xuICAgIHRva2VuOiBudWxsLFxuICAgIG5leHQ6IFwic3RhcnRcIlxuICB9XSxcbiAgbGFuZ3VhZ2VEYXRhOiB7XG4gICAgY29tbWVudFRva2Vuczoge1xuICAgICAgbGluZTogXCIjXCJcbiAgICB9XG4gIH1cbn0pOyIsImV4cG9ydCBmdW5jdGlvbiBzaW1wbGVNb2RlKHN0YXRlcykge1xuICBlbnN1cmVTdGF0ZShzdGF0ZXMsIFwic3RhcnRcIik7XG4gIHZhciBzdGF0ZXNfID0ge30sXG4gICAgbWV0YSA9IHN0YXRlcy5sYW5ndWFnZURhdGEgfHwge30sXG4gICAgaGFzSW5kZW50YXRpb24gPSBmYWxzZTtcbiAgZm9yICh2YXIgc3RhdGUgaW4gc3RhdGVzKSBpZiAoc3RhdGUgIT0gbWV0YSAmJiBzdGF0ZXMuaGFzT3duUHJvcGVydHkoc3RhdGUpKSB7XG4gICAgdmFyIGxpc3QgPSBzdGF0ZXNfW3N0YXRlXSA9IFtdLFxuICAgICAgb3JpZyA9IHN0YXRlc1tzdGF0ZV07XG4gICAgZm9yICh2YXIgaSA9IDA7IGkgPCBvcmlnLmxlbmd0aDsgaSsrKSB7XG4gICAgICB2YXIgZGF0YSA9IG9yaWdbaV07XG4gICAgICBsaXN0LnB1c2gobmV3IFJ1bGUoZGF0YSwgc3RhdGVzKSk7XG4gICAgICBpZiAoZGF0YS5pbmRlbnQgfHwgZGF0YS5kZWRlbnQpIGhhc0luZGVudGF0aW9uID0gdHJ1ZTtcbiAgICB9XG4gIH1cbiAgcmV0dXJuIHtcbiAgICBuYW1lOiBtZXRhLm5hbWUsXG4gICAgc3RhcnRTdGF0ZTogZnVuY3Rpb24gKCkge1xuICAgICAgcmV0dXJuIHtcbiAgICAgICAgc3RhdGU6IFwic3RhcnRcIixcbiAgICAgICAgcGVuZGluZzogbnVsbCxcbiAgICAgICAgaW5kZW50OiBoYXNJbmRlbnRhdGlvbiA/IFtdIDogbnVsbFxuICAgICAgfTtcbiAgICB9LFxuICAgIGNvcHlTdGF0ZTogZnVuY3Rpb24gKHN0YXRlKSB7XG4gICAgICB2YXIgcyA9IHtcbiAgICAgICAgc3RhdGU6IHN0YXRlLnN0YXRlLFxuICAgICAgICBwZW5kaW5nOiBzdGF0ZS5wZW5kaW5nLFxuICAgICAgICBpbmRlbnQ6IHN0YXRlLmluZGVudCAmJiBzdGF0ZS5pbmRlbnQuc2xpY2UoMClcbiAgICAgIH07XG4gICAgICBpZiAoc3RhdGUuc3RhY2spIHMuc3RhY2sgPSBzdGF0ZS5zdGFjay5zbGljZSgwKTtcbiAgICAgIHJldHVybiBzO1xuICAgIH0sXG4gICAgdG9rZW46IHRva2VuRnVuY3Rpb24oc3RhdGVzXyksXG4gICAgaW5kZW50OiBpbmRlbnRGdW5jdGlvbihzdGF0ZXNfLCBtZXRhKSxcbiAgICBsYW5ndWFnZURhdGE6IG1ldGFcbiAgfTtcbn1cbjtcbmZ1bmN0aW9uIGVuc3VyZVN0YXRlKHN0YXRlcywgbmFtZSkge1xuICBpZiAoIXN0YXRlcy5oYXNPd25Qcm9wZXJ0eShuYW1lKSkgdGhyb3cgbmV3IEVycm9yKFwiVW5kZWZpbmVkIHN0YXRlIFwiICsgbmFtZSArIFwiIGluIHNpbXBsZSBtb2RlXCIpO1xufVxuZnVuY3Rpb24gdG9SZWdleCh2YWwsIGNhcmV0KSB7XG4gIGlmICghdmFsKSByZXR1cm4gLyg/OikvO1xuICB2YXIgZmxhZ3MgPSBcIlwiO1xuICBpZiAodmFsIGluc3RhbmNlb2YgUmVnRXhwKSB7XG4gICAgaWYgKHZhbC5pZ25vcmVDYXNlKSBmbGFncyA9IFwiaVwiO1xuICAgIHZhbCA9IHZhbC5zb3VyY2U7XG4gIH0gZWxzZSB7XG4gICAgdmFsID0gU3RyaW5nKHZhbCk7XG4gIH1cbiAgcmV0dXJuIG5ldyBSZWdFeHAoKGNhcmV0ID09PSBmYWxzZSA/IFwiXCIgOiBcIl5cIikgKyBcIig/OlwiICsgdmFsICsgXCIpXCIsIGZsYWdzKTtcbn1cbmZ1bmN0aW9uIGFzVG9rZW4odmFsKSB7XG4gIGlmICghdmFsKSByZXR1cm4gbnVsbDtcbiAgaWYgKHZhbC5hcHBseSkgcmV0dXJuIHZhbDtcbiAgaWYgKHR5cGVvZiB2YWwgPT0gXCJzdHJpbmdcIikgcmV0dXJuIHZhbC5yZXBsYWNlKC9cXC4vZywgXCIgXCIpO1xuICB2YXIgcmVzdWx0ID0gW107XG4gIGZvciAodmFyIGkgPSAwOyBpIDwgdmFsLmxlbmd0aDsgaSsrKSByZXN1bHQucHVzaCh2YWxbaV0gJiYgdmFsW2ldLnJlcGxhY2UoL1xcLi9nLCBcIiBcIikpO1xuICByZXR1cm4gcmVzdWx0O1xufVxuZnVuY3Rpb24gUnVsZShkYXRhLCBzdGF0ZXMpIHtcbiAgaWYgKGRhdGEubmV4dCB8fCBkYXRhLnB1c2gpIGVuc3VyZVN0YXRlKHN0YXRlcywgZGF0YS5uZXh0IHx8IGRhdGEucHVzaCk7XG4gIHRoaXMucmVnZXggPSB0b1JlZ2V4KGRhdGEucmVnZXgpO1xuICB0aGlzLnRva2VuID0gYXNUb2tlbihkYXRhLnRva2VuKTtcbiAgdGhpcy5kYXRhID0gZGF0YTtcbn1cbmZ1bmN0aW9uIHRva2VuRnVuY3Rpb24oc3RhdGVzKSB7XG4gIHJldHVybiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIGlmIChzdGF0ZS5wZW5kaW5nKSB7XG4gICAgICB2YXIgcGVuZCA9IHN0YXRlLnBlbmRpbmcuc2hpZnQoKTtcbiAgICAgIGlmIChzdGF0ZS5wZW5kaW5nLmxlbmd0aCA9PSAwKSBzdGF0ZS5wZW5kaW5nID0gbnVsbDtcbiAgICAgIHN0cmVhbS5wb3MgKz0gcGVuZC50ZXh0Lmxlbmd0aDtcbiAgICAgIHJldHVybiBwZW5kLnRva2VuO1xuICAgIH1cbiAgICB2YXIgY3VyU3RhdGUgPSBzdGF0ZXNbc3RhdGUuc3RhdGVdO1xuICAgIGZvciAodmFyIGkgPSAwOyBpIDwgY3VyU3RhdGUubGVuZ3RoOyBpKyspIHtcbiAgICAgIHZhciBydWxlID0gY3VyU3RhdGVbaV07XG4gICAgICB2YXIgbWF0Y2hlcyA9ICghcnVsZS5kYXRhLnNvbCB8fCBzdHJlYW0uc29sKCkpICYmIHN0cmVhbS5tYXRjaChydWxlLnJlZ2V4KTtcbiAgICAgIGlmIChtYXRjaGVzKSB7XG4gICAgICAgIGlmIChydWxlLmRhdGEubmV4dCkge1xuICAgICAgICAgIHN0YXRlLnN0YXRlID0gcnVsZS5kYXRhLm5leHQ7XG4gICAgICAgIH0gZWxzZSBpZiAocnVsZS5kYXRhLnB1c2gpIHtcbiAgICAgICAgICAoc3RhdGUuc3RhY2sgfHwgKHN0YXRlLnN0YWNrID0gW10pKS5wdXNoKHN0YXRlLnN0YXRlKTtcbiAgICAgICAgICBzdGF0ZS5zdGF0ZSA9IHJ1bGUuZGF0YS5wdXNoO1xuICAgICAgICB9IGVsc2UgaWYgKHJ1bGUuZGF0YS5wb3AgJiYgc3RhdGUuc3RhY2sgJiYgc3RhdGUuc3RhY2subGVuZ3RoKSB7XG4gICAgICAgICAgc3RhdGUuc3RhdGUgPSBzdGF0ZS5zdGFjay5wb3AoKTtcbiAgICAgICAgfVxuICAgICAgICBpZiAocnVsZS5kYXRhLmluZGVudCkgc3RhdGUuaW5kZW50LnB1c2goc3RyZWFtLmluZGVudGF0aW9uKCkgKyBzdHJlYW0uaW5kZW50VW5pdCk7XG4gICAgICAgIGlmIChydWxlLmRhdGEuZGVkZW50KSBzdGF0ZS5pbmRlbnQucG9wKCk7XG4gICAgICAgIHZhciB0b2tlbiA9IHJ1bGUudG9rZW47XG4gICAgICAgIGlmICh0b2tlbiAmJiB0b2tlbi5hcHBseSkgdG9rZW4gPSB0b2tlbihtYXRjaGVzKTtcbiAgICAgICAgaWYgKG1hdGNoZXMubGVuZ3RoID4gMiAmJiBydWxlLnRva2VuICYmIHR5cGVvZiBydWxlLnRva2VuICE9IFwic3RyaW5nXCIpIHtcbiAgICAgICAgICBzdGF0ZS5wZW5kaW5nID0gW107XG4gICAgICAgICAgZm9yICh2YXIgaiA9IDI7IGogPCBtYXRjaGVzLmxlbmd0aDsgaisrKSBpZiAobWF0Y2hlc1tqXSkgc3RhdGUucGVuZGluZy5wdXNoKHtcbiAgICAgICAgICAgIHRleHQ6IG1hdGNoZXNbal0sXG4gICAgICAgICAgICB0b2tlbjogcnVsZS50b2tlbltqIC0gMV1cbiAgICAgICAgICB9KTtcbiAgICAgICAgICBzdHJlYW0uYmFja1VwKG1hdGNoZXNbMF0ubGVuZ3RoIC0gKG1hdGNoZXNbMV0gPyBtYXRjaGVzWzFdLmxlbmd0aCA6IDApKTtcbiAgICAgICAgICByZXR1cm4gdG9rZW5bMF07XG4gICAgICAgIH0gZWxzZSBpZiAodG9rZW4gJiYgdG9rZW4uam9pbikge1xuICAgICAgICAgIHJldHVybiB0b2tlblswXTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICByZXR1cm4gdG9rZW47XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9XG4gICAgc3RyZWFtLm5leHQoKTtcbiAgICByZXR1cm4gbnVsbDtcbiAgfTtcbn1cbmZ1bmN0aW9uIGluZGVudEZ1bmN0aW9uKHN0YXRlcywgbWV0YSkge1xuICByZXR1cm4gZnVuY3Rpb24gKHN0YXRlLCB0ZXh0QWZ0ZXIpIHtcbiAgICBpZiAoc3RhdGUuaW5kZW50ID09IG51bGwgfHwgbWV0YS5kb250SW5kZW50U3RhdGVzICYmIG1ldGEuZG9uZUluZGVudFN0YXRlLmluZGV4T2Yoc3RhdGUuc3RhdGUpID4gLTEpIHJldHVybiBudWxsO1xuICAgIHZhciBwb3MgPSBzdGF0ZS5pbmRlbnQubGVuZ3RoIC0gMSxcbiAgICAgIHJ1bGVzID0gc3RhdGVzW3N0YXRlLnN0YXRlXTtcbiAgICBzY2FuOiBmb3IgKDs7KSB7XG4gICAgICBmb3IgKHZhciBpID0gMDsgaSA8IHJ1bGVzLmxlbmd0aDsgaSsrKSB7XG4gICAgICAgIHZhciBydWxlID0gcnVsZXNbaV07XG4gICAgICAgIGlmIChydWxlLmRhdGEuZGVkZW50ICYmIHJ1bGUuZGF0YS5kZWRlbnRJZkxpbmVTdGFydCAhPT0gZmFsc2UpIHtcbiAgICAgICAgICB2YXIgbSA9IHJ1bGUucmVnZXguZXhlYyh0ZXh0QWZ0ZXIpO1xuICAgICAgICAgIGlmIChtICYmIG1bMF0pIHtcbiAgICAgICAgICAgIHBvcy0tO1xuICAgICAgICAgICAgaWYgKHJ1bGUubmV4dCB8fCBydWxlLnB1c2gpIHJ1bGVzID0gc3RhdGVzW3J1bGUubmV4dCB8fCBydWxlLnB1c2hdO1xuICAgICAgICAgICAgdGV4dEFmdGVyID0gdGV4dEFmdGVyLnNsaWNlKG1bMF0ubGVuZ3RoKTtcbiAgICAgICAgICAgIGNvbnRpbnVlIHNjYW47XG4gICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICB9XG4gICAgICBicmVhaztcbiAgICB9XG4gICAgcmV0dXJuIHBvcyA8IDAgPyAwIDogc3RhdGUuaW5kZW50W3Bvc107XG4gIH07XG59Il0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9