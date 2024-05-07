"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[8678],{

/***/ 28678:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "stex": () => (/* binding */ stex),
/* harmony export */   "stexMath": () => (/* binding */ stexMath)
/* harmony export */ });
function mkStex(mathMode) {
  function pushCommand(state, command) {
    state.cmdState.push(command);
  }
  function peekCommand(state) {
    if (state.cmdState.length > 0) {
      return state.cmdState[state.cmdState.length - 1];
    } else {
      return null;
    }
  }
  function popCommand(state) {
    var plug = state.cmdState.pop();
    if (plug) {
      plug.closeBracket();
    }
  }

  // returns the non-default plugin closest to the end of the list
  function getMostPowerful(state) {
    var context = state.cmdState;
    for (var i = context.length - 1; i >= 0; i--) {
      var plug = context[i];
      if (plug.name == "DEFAULT") {
        continue;
      }
      return plug;
    }
    return {
      styleIdentifier: function () {
        return null;
      }
    };
  }
  function addPluginPattern(pluginName, cmdStyle, styles) {
    return function () {
      this.name = pluginName;
      this.bracketNo = 0;
      this.style = cmdStyle;
      this.styles = styles;
      this.argument = null; // \begin and \end have arguments that follow. These are stored in the plugin

      this.styleIdentifier = function () {
        return this.styles[this.bracketNo - 1] || null;
      };
      this.openBracket = function () {
        this.bracketNo++;
        return "bracket";
      };
      this.closeBracket = function () {};
    };
  }
  var plugins = {};
  plugins["importmodule"] = addPluginPattern("importmodule", "tag", ["string", "builtin"]);
  plugins["documentclass"] = addPluginPattern("documentclass", "tag", ["", "atom"]);
  plugins["usepackage"] = addPluginPattern("usepackage", "tag", ["atom"]);
  plugins["begin"] = addPluginPattern("begin", "tag", ["atom"]);
  plugins["end"] = addPluginPattern("end", "tag", ["atom"]);
  plugins["label"] = addPluginPattern("label", "tag", ["atom"]);
  plugins["ref"] = addPluginPattern("ref", "tag", ["atom"]);
  plugins["eqref"] = addPluginPattern("eqref", "tag", ["atom"]);
  plugins["cite"] = addPluginPattern("cite", "tag", ["atom"]);
  plugins["bibitem"] = addPluginPattern("bibitem", "tag", ["atom"]);
  plugins["Bibitem"] = addPluginPattern("Bibitem", "tag", ["atom"]);
  plugins["RBibitem"] = addPluginPattern("RBibitem", "tag", ["atom"]);
  plugins["DEFAULT"] = function () {
    this.name = "DEFAULT";
    this.style = "tag";
    this.styleIdentifier = this.openBracket = this.closeBracket = function () {};
  };
  function setState(state, f) {
    state.f = f;
  }

  // called when in a normal (no environment) context
  function normal(source, state) {
    var plug;
    // Do we look like '\command' ?  If so, attempt to apply the plugin 'command'
    if (source.match(/^\\[a-zA-Z@\xc0-\u1fff\u2060-\uffff]+/)) {
      var cmdName = source.current().slice(1);
      plug = plugins.hasOwnProperty(cmdName) ? plugins[cmdName] : plugins["DEFAULT"];
      plug = new plug();
      pushCommand(state, plug);
      setState(state, beginParams);
      return plug.style;
    }

    // escape characters
    if (source.match(/^\\[$&%#{}_]/)) {
      return "tag";
    }

    // white space control characters
    if (source.match(/^\\[,;!\/\\]/)) {
      return "tag";
    }

    // find if we're starting various math modes
    if (source.match("\\[")) {
      setState(state, function (source, state) {
        return inMathMode(source, state, "\\]");
      });
      return "keyword";
    }
    if (source.match("\\(")) {
      setState(state, function (source, state) {
        return inMathMode(source, state, "\\)");
      });
      return "keyword";
    }
    if (source.match("$$")) {
      setState(state, function (source, state) {
        return inMathMode(source, state, "$$");
      });
      return "keyword";
    }
    if (source.match("$")) {
      setState(state, function (source, state) {
        return inMathMode(source, state, "$");
      });
      return "keyword";
    }
    var ch = source.next();
    if (ch == "%") {
      source.skipToEnd();
      return "comment";
    } else if (ch == '}' || ch == ']') {
      plug = peekCommand(state);
      if (plug) {
        plug.closeBracket(ch);
        setState(state, beginParams);
      } else {
        return "error";
      }
      return "bracket";
    } else if (ch == '{' || ch == '[') {
      plug = plugins["DEFAULT"];
      plug = new plug();
      pushCommand(state, plug);
      return "bracket";
    } else if (/\d/.test(ch)) {
      source.eatWhile(/[\w.%]/);
      return "atom";
    } else {
      source.eatWhile(/[\w\-_]/);
      plug = getMostPowerful(state);
      if (plug.name == 'begin') {
        plug.argument = source.current();
      }
      return plug.styleIdentifier();
    }
  }
  function inMathMode(source, state, endModeSeq) {
    if (source.eatSpace()) {
      return null;
    }
    if (endModeSeq && source.match(endModeSeq)) {
      setState(state, normal);
      return "keyword";
    }
    if (source.match(/^\\[a-zA-Z@]+/)) {
      return "tag";
    }
    if (source.match(/^[a-zA-Z]+/)) {
      return "variableName.special";
    }
    // escape characters
    if (source.match(/^\\[$&%#{}_]/)) {
      return "tag";
    }
    // white space control characters
    if (source.match(/^\\[,;!\/]/)) {
      return "tag";
    }
    // special math-mode characters
    if (source.match(/^[\^_&]/)) {
      return "tag";
    }
    // non-special characters
    if (source.match(/^[+\-<>|=,\/@!*:;'"`~#?]/)) {
      return null;
    }
    if (source.match(/^(\d+\.\d*|\d*\.\d+|\d+)/)) {
      return "number";
    }
    var ch = source.next();
    if (ch == "{" || ch == "}" || ch == "[" || ch == "]" || ch == "(" || ch == ")") {
      return "bracket";
    }
    if (ch == "%") {
      source.skipToEnd();
      return "comment";
    }
    return "error";
  }
  function beginParams(source, state) {
    var ch = source.peek(),
      lastPlug;
    if (ch == '{' || ch == '[') {
      lastPlug = peekCommand(state);
      lastPlug.openBracket(ch);
      source.eat(ch);
      setState(state, normal);
      return "bracket";
    }
    if (/[ \t\r]/.test(ch)) {
      source.eat(ch);
      return null;
    }
    setState(state, normal);
    popCommand(state);
    return normal(source, state);
  }
  return {
    name: "stex",
    startState: function () {
      var f = mathMode ? function (source, state) {
        return inMathMode(source, state);
      } : normal;
      return {
        cmdState: [],
        f: f
      };
    },
    copyState: function (s) {
      return {
        cmdState: s.cmdState.slice(),
        f: s.f
      };
    },
    token: function (stream, state) {
      return state.f(stream, state);
    },
    blankLine: function (state) {
      state.f = normal;
      state.cmdState.length = 0;
    },
    languageData: {
      commentTokens: {
        line: "%"
      }
    }
  };
}
;
const stex = mkStex(false);
const stexMath = mkStex(true);

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiODY3OC5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9AY29kZW1pcnJvci9sZWdhY3ktbW9kZXMvbW9kZS9zdGV4LmpzIl0sInNvdXJjZXNDb250ZW50IjpbImZ1bmN0aW9uIG1rU3RleChtYXRoTW9kZSkge1xuICBmdW5jdGlvbiBwdXNoQ29tbWFuZChzdGF0ZSwgY29tbWFuZCkge1xuICAgIHN0YXRlLmNtZFN0YXRlLnB1c2goY29tbWFuZCk7XG4gIH1cbiAgZnVuY3Rpb24gcGVla0NvbW1hbmQoc3RhdGUpIHtcbiAgICBpZiAoc3RhdGUuY21kU3RhdGUubGVuZ3RoID4gMCkge1xuICAgICAgcmV0dXJuIHN0YXRlLmNtZFN0YXRlW3N0YXRlLmNtZFN0YXRlLmxlbmd0aCAtIDFdO1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9XG4gIH1cbiAgZnVuY3Rpb24gcG9wQ29tbWFuZChzdGF0ZSkge1xuICAgIHZhciBwbHVnID0gc3RhdGUuY21kU3RhdGUucG9wKCk7XG4gICAgaWYgKHBsdWcpIHtcbiAgICAgIHBsdWcuY2xvc2VCcmFja2V0KCk7XG4gICAgfVxuICB9XG5cbiAgLy8gcmV0dXJucyB0aGUgbm9uLWRlZmF1bHQgcGx1Z2luIGNsb3Nlc3QgdG8gdGhlIGVuZCBvZiB0aGUgbGlzdFxuICBmdW5jdGlvbiBnZXRNb3N0UG93ZXJmdWwoc3RhdGUpIHtcbiAgICB2YXIgY29udGV4dCA9IHN0YXRlLmNtZFN0YXRlO1xuICAgIGZvciAodmFyIGkgPSBjb250ZXh0Lmxlbmd0aCAtIDE7IGkgPj0gMDsgaS0tKSB7XG4gICAgICB2YXIgcGx1ZyA9IGNvbnRleHRbaV07XG4gICAgICBpZiAocGx1Zy5uYW1lID09IFwiREVGQVVMVFwiKSB7XG4gICAgICAgIGNvbnRpbnVlO1xuICAgICAgfVxuICAgICAgcmV0dXJuIHBsdWc7XG4gICAgfVxuICAgIHJldHVybiB7XG4gICAgICBzdHlsZUlkZW50aWZpZXI6IGZ1bmN0aW9uICgpIHtcbiAgICAgICAgcmV0dXJuIG51bGw7XG4gICAgICB9XG4gICAgfTtcbiAgfVxuICBmdW5jdGlvbiBhZGRQbHVnaW5QYXR0ZXJuKHBsdWdpbk5hbWUsIGNtZFN0eWxlLCBzdHlsZXMpIHtcbiAgICByZXR1cm4gZnVuY3Rpb24gKCkge1xuICAgICAgdGhpcy5uYW1lID0gcGx1Z2luTmFtZTtcbiAgICAgIHRoaXMuYnJhY2tldE5vID0gMDtcbiAgICAgIHRoaXMuc3R5bGUgPSBjbWRTdHlsZTtcbiAgICAgIHRoaXMuc3R5bGVzID0gc3R5bGVzO1xuICAgICAgdGhpcy5hcmd1bWVudCA9IG51bGw7IC8vIFxcYmVnaW4gYW5kIFxcZW5kIGhhdmUgYXJndW1lbnRzIHRoYXQgZm9sbG93LiBUaGVzZSBhcmUgc3RvcmVkIGluIHRoZSBwbHVnaW5cblxuICAgICAgdGhpcy5zdHlsZUlkZW50aWZpZXIgPSBmdW5jdGlvbiAoKSB7XG4gICAgICAgIHJldHVybiB0aGlzLnN0eWxlc1t0aGlzLmJyYWNrZXRObyAtIDFdIHx8IG51bGw7XG4gICAgICB9O1xuICAgICAgdGhpcy5vcGVuQnJhY2tldCA9IGZ1bmN0aW9uICgpIHtcbiAgICAgICAgdGhpcy5icmFja2V0Tm8rKztcbiAgICAgICAgcmV0dXJuIFwiYnJhY2tldFwiO1xuICAgICAgfTtcbiAgICAgIHRoaXMuY2xvc2VCcmFja2V0ID0gZnVuY3Rpb24gKCkge307XG4gICAgfTtcbiAgfVxuICB2YXIgcGx1Z2lucyA9IHt9O1xuICBwbHVnaW5zW1wiaW1wb3J0bW9kdWxlXCJdID0gYWRkUGx1Z2luUGF0dGVybihcImltcG9ydG1vZHVsZVwiLCBcInRhZ1wiLCBbXCJzdHJpbmdcIiwgXCJidWlsdGluXCJdKTtcbiAgcGx1Z2luc1tcImRvY3VtZW50Y2xhc3NcIl0gPSBhZGRQbHVnaW5QYXR0ZXJuKFwiZG9jdW1lbnRjbGFzc1wiLCBcInRhZ1wiLCBbXCJcIiwgXCJhdG9tXCJdKTtcbiAgcGx1Z2luc1tcInVzZXBhY2thZ2VcIl0gPSBhZGRQbHVnaW5QYXR0ZXJuKFwidXNlcGFja2FnZVwiLCBcInRhZ1wiLCBbXCJhdG9tXCJdKTtcbiAgcGx1Z2luc1tcImJlZ2luXCJdID0gYWRkUGx1Z2luUGF0dGVybihcImJlZ2luXCIsIFwidGFnXCIsIFtcImF0b21cIl0pO1xuICBwbHVnaW5zW1wiZW5kXCJdID0gYWRkUGx1Z2luUGF0dGVybihcImVuZFwiLCBcInRhZ1wiLCBbXCJhdG9tXCJdKTtcbiAgcGx1Z2luc1tcImxhYmVsXCJdID0gYWRkUGx1Z2luUGF0dGVybihcImxhYmVsXCIsIFwidGFnXCIsIFtcImF0b21cIl0pO1xuICBwbHVnaW5zW1wicmVmXCJdID0gYWRkUGx1Z2luUGF0dGVybihcInJlZlwiLCBcInRhZ1wiLCBbXCJhdG9tXCJdKTtcbiAgcGx1Z2luc1tcImVxcmVmXCJdID0gYWRkUGx1Z2luUGF0dGVybihcImVxcmVmXCIsIFwidGFnXCIsIFtcImF0b21cIl0pO1xuICBwbHVnaW5zW1wiY2l0ZVwiXSA9IGFkZFBsdWdpblBhdHRlcm4oXCJjaXRlXCIsIFwidGFnXCIsIFtcImF0b21cIl0pO1xuICBwbHVnaW5zW1wiYmliaXRlbVwiXSA9IGFkZFBsdWdpblBhdHRlcm4oXCJiaWJpdGVtXCIsIFwidGFnXCIsIFtcImF0b21cIl0pO1xuICBwbHVnaW5zW1wiQmliaXRlbVwiXSA9IGFkZFBsdWdpblBhdHRlcm4oXCJCaWJpdGVtXCIsIFwidGFnXCIsIFtcImF0b21cIl0pO1xuICBwbHVnaW5zW1wiUkJpYml0ZW1cIl0gPSBhZGRQbHVnaW5QYXR0ZXJuKFwiUkJpYml0ZW1cIiwgXCJ0YWdcIiwgW1wiYXRvbVwiXSk7XG4gIHBsdWdpbnNbXCJERUZBVUxUXCJdID0gZnVuY3Rpb24gKCkge1xuICAgIHRoaXMubmFtZSA9IFwiREVGQVVMVFwiO1xuICAgIHRoaXMuc3R5bGUgPSBcInRhZ1wiO1xuICAgIHRoaXMuc3R5bGVJZGVudGlmaWVyID0gdGhpcy5vcGVuQnJhY2tldCA9IHRoaXMuY2xvc2VCcmFja2V0ID0gZnVuY3Rpb24gKCkge307XG4gIH07XG4gIGZ1bmN0aW9uIHNldFN0YXRlKHN0YXRlLCBmKSB7XG4gICAgc3RhdGUuZiA9IGY7XG4gIH1cblxuICAvLyBjYWxsZWQgd2hlbiBpbiBhIG5vcm1hbCAobm8gZW52aXJvbm1lbnQpIGNvbnRleHRcbiAgZnVuY3Rpb24gbm9ybWFsKHNvdXJjZSwgc3RhdGUpIHtcbiAgICB2YXIgcGx1ZztcbiAgICAvLyBEbyB3ZSBsb29rIGxpa2UgJ1xcY29tbWFuZCcgPyAgSWYgc28sIGF0dGVtcHQgdG8gYXBwbHkgdGhlIHBsdWdpbiAnY29tbWFuZCdcbiAgICBpZiAoc291cmNlLm1hdGNoKC9eXFxcXFthLXpBLVpAXFx4YzAtXFx1MWZmZlxcdTIwNjAtXFx1ZmZmZl0rLykpIHtcbiAgICAgIHZhciBjbWROYW1lID0gc291cmNlLmN1cnJlbnQoKS5zbGljZSgxKTtcbiAgICAgIHBsdWcgPSBwbHVnaW5zLmhhc093blByb3BlcnR5KGNtZE5hbWUpID8gcGx1Z2luc1tjbWROYW1lXSA6IHBsdWdpbnNbXCJERUZBVUxUXCJdO1xuICAgICAgcGx1ZyA9IG5ldyBwbHVnKCk7XG4gICAgICBwdXNoQ29tbWFuZChzdGF0ZSwgcGx1Zyk7XG4gICAgICBzZXRTdGF0ZShzdGF0ZSwgYmVnaW5QYXJhbXMpO1xuICAgICAgcmV0dXJuIHBsdWcuc3R5bGU7XG4gICAgfVxuXG4gICAgLy8gZXNjYXBlIGNoYXJhY3RlcnNcbiAgICBpZiAoc291cmNlLm1hdGNoKC9eXFxcXFskJiUje31fXS8pKSB7XG4gICAgICByZXR1cm4gXCJ0YWdcIjtcbiAgICB9XG5cbiAgICAvLyB3aGl0ZSBzcGFjZSBjb250cm9sIGNoYXJhY3RlcnNcbiAgICBpZiAoc291cmNlLm1hdGNoKC9eXFxcXFssOyFcXC9cXFxcXS8pKSB7XG4gICAgICByZXR1cm4gXCJ0YWdcIjtcbiAgICB9XG5cbiAgICAvLyBmaW5kIGlmIHdlJ3JlIHN0YXJ0aW5nIHZhcmlvdXMgbWF0aCBtb2Rlc1xuICAgIGlmIChzb3VyY2UubWF0Y2goXCJcXFxcW1wiKSkge1xuICAgICAgc2V0U3RhdGUoc3RhdGUsIGZ1bmN0aW9uIChzb3VyY2UsIHN0YXRlKSB7XG4gICAgICAgIHJldHVybiBpbk1hdGhNb2RlKHNvdXJjZSwgc3RhdGUsIFwiXFxcXF1cIik7XG4gICAgICB9KTtcbiAgICAgIHJldHVybiBcImtleXdvcmRcIjtcbiAgICB9XG4gICAgaWYgKHNvdXJjZS5tYXRjaChcIlxcXFwoXCIpKSB7XG4gICAgICBzZXRTdGF0ZShzdGF0ZSwgZnVuY3Rpb24gKHNvdXJjZSwgc3RhdGUpIHtcbiAgICAgICAgcmV0dXJuIGluTWF0aE1vZGUoc291cmNlLCBzdGF0ZSwgXCJcXFxcKVwiKTtcbiAgICAgIH0pO1xuICAgICAgcmV0dXJuIFwia2V5d29yZFwiO1xuICAgIH1cbiAgICBpZiAoc291cmNlLm1hdGNoKFwiJCRcIikpIHtcbiAgICAgIHNldFN0YXRlKHN0YXRlLCBmdW5jdGlvbiAoc291cmNlLCBzdGF0ZSkge1xuICAgICAgICByZXR1cm4gaW5NYXRoTW9kZShzb3VyY2UsIHN0YXRlLCBcIiQkXCIpO1xuICAgICAgfSk7XG4gICAgICByZXR1cm4gXCJrZXl3b3JkXCI7XG4gICAgfVxuICAgIGlmIChzb3VyY2UubWF0Y2goXCIkXCIpKSB7XG4gICAgICBzZXRTdGF0ZShzdGF0ZSwgZnVuY3Rpb24gKHNvdXJjZSwgc3RhdGUpIHtcbiAgICAgICAgcmV0dXJuIGluTWF0aE1vZGUoc291cmNlLCBzdGF0ZSwgXCIkXCIpO1xuICAgICAgfSk7XG4gICAgICByZXR1cm4gXCJrZXl3b3JkXCI7XG4gICAgfVxuICAgIHZhciBjaCA9IHNvdXJjZS5uZXh0KCk7XG4gICAgaWYgKGNoID09IFwiJVwiKSB7XG4gICAgICBzb3VyY2Uuc2tpcFRvRW5kKCk7XG4gICAgICByZXR1cm4gXCJjb21tZW50XCI7XG4gICAgfSBlbHNlIGlmIChjaCA9PSAnfScgfHwgY2ggPT0gJ10nKSB7XG4gICAgICBwbHVnID0gcGVla0NvbW1hbmQoc3RhdGUpO1xuICAgICAgaWYgKHBsdWcpIHtcbiAgICAgICAgcGx1Zy5jbG9zZUJyYWNrZXQoY2gpO1xuICAgICAgICBzZXRTdGF0ZShzdGF0ZSwgYmVnaW5QYXJhbXMpO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgcmV0dXJuIFwiZXJyb3JcIjtcbiAgICAgIH1cbiAgICAgIHJldHVybiBcImJyYWNrZXRcIjtcbiAgICB9IGVsc2UgaWYgKGNoID09ICd7JyB8fCBjaCA9PSAnWycpIHtcbiAgICAgIHBsdWcgPSBwbHVnaW5zW1wiREVGQVVMVFwiXTtcbiAgICAgIHBsdWcgPSBuZXcgcGx1ZygpO1xuICAgICAgcHVzaENvbW1hbmQoc3RhdGUsIHBsdWcpO1xuICAgICAgcmV0dXJuIFwiYnJhY2tldFwiO1xuICAgIH0gZWxzZSBpZiAoL1xcZC8udGVzdChjaCkpIHtcbiAgICAgIHNvdXJjZS5lYXRXaGlsZSgvW1xcdy4lXS8pO1xuICAgICAgcmV0dXJuIFwiYXRvbVwiO1xuICAgIH0gZWxzZSB7XG4gICAgICBzb3VyY2UuZWF0V2hpbGUoL1tcXHdcXC1fXS8pO1xuICAgICAgcGx1ZyA9IGdldE1vc3RQb3dlcmZ1bChzdGF0ZSk7XG4gICAgICBpZiAocGx1Zy5uYW1lID09ICdiZWdpbicpIHtcbiAgICAgICAgcGx1Zy5hcmd1bWVudCA9IHNvdXJjZS5jdXJyZW50KCk7XG4gICAgICB9XG4gICAgICByZXR1cm4gcGx1Zy5zdHlsZUlkZW50aWZpZXIoKTtcbiAgICB9XG4gIH1cbiAgZnVuY3Rpb24gaW5NYXRoTW9kZShzb3VyY2UsIHN0YXRlLCBlbmRNb2RlU2VxKSB7XG4gICAgaWYgKHNvdXJjZS5lYXRTcGFjZSgpKSB7XG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9XG4gICAgaWYgKGVuZE1vZGVTZXEgJiYgc291cmNlLm1hdGNoKGVuZE1vZGVTZXEpKSB7XG4gICAgICBzZXRTdGF0ZShzdGF0ZSwgbm9ybWFsKTtcbiAgICAgIHJldHVybiBcImtleXdvcmRcIjtcbiAgICB9XG4gICAgaWYgKHNvdXJjZS5tYXRjaCgvXlxcXFxbYS16QS1aQF0rLykpIHtcbiAgICAgIHJldHVybiBcInRhZ1wiO1xuICAgIH1cbiAgICBpZiAoc291cmNlLm1hdGNoKC9eW2EtekEtWl0rLykpIHtcbiAgICAgIHJldHVybiBcInZhcmlhYmxlTmFtZS5zcGVjaWFsXCI7XG4gICAgfVxuICAgIC8vIGVzY2FwZSBjaGFyYWN0ZXJzXG4gICAgaWYgKHNvdXJjZS5tYXRjaCgvXlxcXFxbJCYlI3t9X10vKSkge1xuICAgICAgcmV0dXJuIFwidGFnXCI7XG4gICAgfVxuICAgIC8vIHdoaXRlIHNwYWNlIGNvbnRyb2wgY2hhcmFjdGVyc1xuICAgIGlmIChzb3VyY2UubWF0Y2goL15cXFxcWyw7IVxcL10vKSkge1xuICAgICAgcmV0dXJuIFwidGFnXCI7XG4gICAgfVxuICAgIC8vIHNwZWNpYWwgbWF0aC1tb2RlIGNoYXJhY3RlcnNcbiAgICBpZiAoc291cmNlLm1hdGNoKC9eW1xcXl8mXS8pKSB7XG4gICAgICByZXR1cm4gXCJ0YWdcIjtcbiAgICB9XG4gICAgLy8gbm9uLXNwZWNpYWwgY2hhcmFjdGVyc1xuICAgIGlmIChzb3VyY2UubWF0Y2goL15bK1xcLTw+fD0sXFwvQCEqOjsnXCJgfiM/XS8pKSB7XG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9XG4gICAgaWYgKHNvdXJjZS5tYXRjaCgvXihcXGQrXFwuXFxkKnxcXGQqXFwuXFxkK3xcXGQrKS8pKSB7XG4gICAgICByZXR1cm4gXCJudW1iZXJcIjtcbiAgICB9XG4gICAgdmFyIGNoID0gc291cmNlLm5leHQoKTtcbiAgICBpZiAoY2ggPT0gXCJ7XCIgfHwgY2ggPT0gXCJ9XCIgfHwgY2ggPT0gXCJbXCIgfHwgY2ggPT0gXCJdXCIgfHwgY2ggPT0gXCIoXCIgfHwgY2ggPT0gXCIpXCIpIHtcbiAgICAgIHJldHVybiBcImJyYWNrZXRcIjtcbiAgICB9XG4gICAgaWYgKGNoID09IFwiJVwiKSB7XG4gICAgICBzb3VyY2Uuc2tpcFRvRW5kKCk7XG4gICAgICByZXR1cm4gXCJjb21tZW50XCI7XG4gICAgfVxuICAgIHJldHVybiBcImVycm9yXCI7XG4gIH1cbiAgZnVuY3Rpb24gYmVnaW5QYXJhbXMoc291cmNlLCBzdGF0ZSkge1xuICAgIHZhciBjaCA9IHNvdXJjZS5wZWVrKCksXG4gICAgICBsYXN0UGx1ZztcbiAgICBpZiAoY2ggPT0gJ3snIHx8IGNoID09ICdbJykge1xuICAgICAgbGFzdFBsdWcgPSBwZWVrQ29tbWFuZChzdGF0ZSk7XG4gICAgICBsYXN0UGx1Zy5vcGVuQnJhY2tldChjaCk7XG4gICAgICBzb3VyY2UuZWF0KGNoKTtcbiAgICAgIHNldFN0YXRlKHN0YXRlLCBub3JtYWwpO1xuICAgICAgcmV0dXJuIFwiYnJhY2tldFwiO1xuICAgIH1cbiAgICBpZiAoL1sgXFx0XFxyXS8udGVzdChjaCkpIHtcbiAgICAgIHNvdXJjZS5lYXQoY2gpO1xuICAgICAgcmV0dXJuIG51bGw7XG4gICAgfVxuICAgIHNldFN0YXRlKHN0YXRlLCBub3JtYWwpO1xuICAgIHBvcENvbW1hbmQoc3RhdGUpO1xuICAgIHJldHVybiBub3JtYWwoc291cmNlLCBzdGF0ZSk7XG4gIH1cbiAgcmV0dXJuIHtcbiAgICBuYW1lOiBcInN0ZXhcIixcbiAgICBzdGFydFN0YXRlOiBmdW5jdGlvbiAoKSB7XG4gICAgICB2YXIgZiA9IG1hdGhNb2RlID8gZnVuY3Rpb24gKHNvdXJjZSwgc3RhdGUpIHtcbiAgICAgICAgcmV0dXJuIGluTWF0aE1vZGUoc291cmNlLCBzdGF0ZSk7XG4gICAgICB9IDogbm9ybWFsO1xuICAgICAgcmV0dXJuIHtcbiAgICAgICAgY21kU3RhdGU6IFtdLFxuICAgICAgICBmOiBmXG4gICAgICB9O1xuICAgIH0sXG4gICAgY29weVN0YXRlOiBmdW5jdGlvbiAocykge1xuICAgICAgcmV0dXJuIHtcbiAgICAgICAgY21kU3RhdGU6IHMuY21kU3RhdGUuc2xpY2UoKSxcbiAgICAgICAgZjogcy5mXG4gICAgICB9O1xuICAgIH0sXG4gICAgdG9rZW46IGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgICByZXR1cm4gc3RhdGUuZihzdHJlYW0sIHN0YXRlKTtcbiAgICB9LFxuICAgIGJsYW5rTGluZTogZnVuY3Rpb24gKHN0YXRlKSB7XG4gICAgICBzdGF0ZS5mID0gbm9ybWFsO1xuICAgICAgc3RhdGUuY21kU3RhdGUubGVuZ3RoID0gMDtcbiAgICB9LFxuICAgIGxhbmd1YWdlRGF0YToge1xuICAgICAgY29tbWVudFRva2Vuczoge1xuICAgICAgICBsaW5lOiBcIiVcIlxuICAgICAgfVxuICAgIH1cbiAgfTtcbn1cbjtcbmV4cG9ydCBjb25zdCBzdGV4ID0gbWtTdGV4KGZhbHNlKTtcbmV4cG9ydCBjb25zdCBzdGV4TWF0aCA9IG1rU3RleCh0cnVlKTsiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=