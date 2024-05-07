"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[912],{

/***/ 40912:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "lua": () => (/* binding */ lua)
/* harmony export */ });
function prefixRE(words) {
  return new RegExp("^(?:" + words.join("|") + ")", "i");
}
function wordRE(words) {
  return new RegExp("^(?:" + words.join("|") + ")$", "i");
}

// long list of standard functions from lua manual
var builtins = wordRE(["_G", "_VERSION", "assert", "collectgarbage", "dofile", "error", "getfenv", "getmetatable", "ipairs", "load", "loadfile", "loadstring", "module", "next", "pairs", "pcall", "print", "rawequal", "rawget", "rawset", "require", "select", "setfenv", "setmetatable", "tonumber", "tostring", "type", "unpack", "xpcall", "coroutine.create", "coroutine.resume", "coroutine.running", "coroutine.status", "coroutine.wrap", "coroutine.yield", "debug.debug", "debug.getfenv", "debug.gethook", "debug.getinfo", "debug.getlocal", "debug.getmetatable", "debug.getregistry", "debug.getupvalue", "debug.setfenv", "debug.sethook", "debug.setlocal", "debug.setmetatable", "debug.setupvalue", "debug.traceback", "close", "flush", "lines", "read", "seek", "setvbuf", "write", "io.close", "io.flush", "io.input", "io.lines", "io.open", "io.output", "io.popen", "io.read", "io.stderr", "io.stdin", "io.stdout", "io.tmpfile", "io.type", "io.write", "math.abs", "math.acos", "math.asin", "math.atan", "math.atan2", "math.ceil", "math.cos", "math.cosh", "math.deg", "math.exp", "math.floor", "math.fmod", "math.frexp", "math.huge", "math.ldexp", "math.log", "math.log10", "math.max", "math.min", "math.modf", "math.pi", "math.pow", "math.rad", "math.random", "math.randomseed", "math.sin", "math.sinh", "math.sqrt", "math.tan", "math.tanh", "os.clock", "os.date", "os.difftime", "os.execute", "os.exit", "os.getenv", "os.remove", "os.rename", "os.setlocale", "os.time", "os.tmpname", "package.cpath", "package.loaded", "package.loaders", "package.loadlib", "package.path", "package.preload", "package.seeall", "string.byte", "string.char", "string.dump", "string.find", "string.format", "string.gmatch", "string.gsub", "string.len", "string.lower", "string.match", "string.rep", "string.reverse", "string.sub", "string.upper", "table.concat", "table.insert", "table.maxn", "table.remove", "table.sort"]);
var keywords = wordRE(["and", "break", "elseif", "false", "nil", "not", "or", "return", "true", "function", "end", "if", "then", "else", "do", "while", "repeat", "until", "for", "in", "local"]);
var indentTokens = wordRE(["function", "if", "repeat", "do", "\\(", "{"]);
var dedentTokens = wordRE(["end", "until", "\\)", "}"]);
var dedentPartial = prefixRE(["end", "until", "\\)", "}", "else", "elseif"]);
function readBracket(stream) {
  var level = 0;
  while (stream.eat("=")) ++level;
  stream.eat("[");
  return level;
}
function normal(stream, state) {
  var ch = stream.next();
  if (ch == "-" && stream.eat("-")) {
    if (stream.eat("[") && stream.eat("[")) return (state.cur = bracketed(readBracket(stream), "comment"))(stream, state);
    stream.skipToEnd();
    return "comment";
  }
  if (ch == "\"" || ch == "'") return (state.cur = string(ch))(stream, state);
  if (ch == "[" && /[\[=]/.test(stream.peek())) return (state.cur = bracketed(readBracket(stream), "string"))(stream, state);
  if (/\d/.test(ch)) {
    stream.eatWhile(/[\w.%]/);
    return "number";
  }
  if (/[\w_]/.test(ch)) {
    stream.eatWhile(/[\w\\\-_.]/);
    return "variable";
  }
  return null;
}
function bracketed(level, style) {
  return function (stream, state) {
    var curlev = null,
      ch;
    while ((ch = stream.next()) != null) {
      if (curlev == null) {
        if (ch == "]") curlev = 0;
      } else if (ch == "=") ++curlev;else if (ch == "]" && curlev == level) {
        state.cur = normal;
        break;
      } else curlev = null;
    }
    return style;
  };
}
function string(quote) {
  return function (stream, state) {
    var escaped = false,
      ch;
    while ((ch = stream.next()) != null) {
      if (ch == quote && !escaped) break;
      escaped = !escaped && ch == "\\";
    }
    if (!escaped) state.cur = normal;
    return "string";
  };
}
const lua = {
  name: "lua",
  startState: function () {
    return {
      basecol: 0,
      indentDepth: 0,
      cur: normal
    };
  },
  token: function (stream, state) {
    if (stream.eatSpace()) return null;
    var style = state.cur(stream, state);
    var word = stream.current();
    if (style == "variable") {
      if (keywords.test(word)) style = "keyword";else if (builtins.test(word)) style = "builtin";
    }
    if (style != "comment" && style != "string") {
      if (indentTokens.test(word)) ++state.indentDepth;else if (dedentTokens.test(word)) --state.indentDepth;
    }
    return style;
  },
  indent: function (state, textAfter, cx) {
    var closing = dedentPartial.test(textAfter);
    return state.basecol + cx.unit * (state.indentDepth - (closing ? 1 : 0));
  },
  languageData: {
    indentOnInput: /^\s*(?:end|until|else|\)|\})$/,
    commentTokens: {
      line: "--",
      block: {
        open: "--[[",
        close: "]]--"
      }
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiOTEyLmp1cHl0ZXItdmlld2VyLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9AY29kZW1pcnJvci9sZWdhY3ktbW9kZXMvbW9kZS9sdWEuanMiXSwic291cmNlc0NvbnRlbnQiOlsiZnVuY3Rpb24gcHJlZml4UkUod29yZHMpIHtcbiAgcmV0dXJuIG5ldyBSZWdFeHAoXCJeKD86XCIgKyB3b3Jkcy5qb2luKFwifFwiKSArIFwiKVwiLCBcImlcIik7XG59XG5mdW5jdGlvbiB3b3JkUkUod29yZHMpIHtcbiAgcmV0dXJuIG5ldyBSZWdFeHAoXCJeKD86XCIgKyB3b3Jkcy5qb2luKFwifFwiKSArIFwiKSRcIiwgXCJpXCIpO1xufVxuXG4vLyBsb25nIGxpc3Qgb2Ygc3RhbmRhcmQgZnVuY3Rpb25zIGZyb20gbHVhIG1hbnVhbFxudmFyIGJ1aWx0aW5zID0gd29yZFJFKFtcIl9HXCIsIFwiX1ZFUlNJT05cIiwgXCJhc3NlcnRcIiwgXCJjb2xsZWN0Z2FyYmFnZVwiLCBcImRvZmlsZVwiLCBcImVycm9yXCIsIFwiZ2V0ZmVudlwiLCBcImdldG1ldGF0YWJsZVwiLCBcImlwYWlyc1wiLCBcImxvYWRcIiwgXCJsb2FkZmlsZVwiLCBcImxvYWRzdHJpbmdcIiwgXCJtb2R1bGVcIiwgXCJuZXh0XCIsIFwicGFpcnNcIiwgXCJwY2FsbFwiLCBcInByaW50XCIsIFwicmF3ZXF1YWxcIiwgXCJyYXdnZXRcIiwgXCJyYXdzZXRcIiwgXCJyZXF1aXJlXCIsIFwic2VsZWN0XCIsIFwic2V0ZmVudlwiLCBcInNldG1ldGF0YWJsZVwiLCBcInRvbnVtYmVyXCIsIFwidG9zdHJpbmdcIiwgXCJ0eXBlXCIsIFwidW5wYWNrXCIsIFwieHBjYWxsXCIsIFwiY29yb3V0aW5lLmNyZWF0ZVwiLCBcImNvcm91dGluZS5yZXN1bWVcIiwgXCJjb3JvdXRpbmUucnVubmluZ1wiLCBcImNvcm91dGluZS5zdGF0dXNcIiwgXCJjb3JvdXRpbmUud3JhcFwiLCBcImNvcm91dGluZS55aWVsZFwiLCBcImRlYnVnLmRlYnVnXCIsIFwiZGVidWcuZ2V0ZmVudlwiLCBcImRlYnVnLmdldGhvb2tcIiwgXCJkZWJ1Zy5nZXRpbmZvXCIsIFwiZGVidWcuZ2V0bG9jYWxcIiwgXCJkZWJ1Zy5nZXRtZXRhdGFibGVcIiwgXCJkZWJ1Zy5nZXRyZWdpc3RyeVwiLCBcImRlYnVnLmdldHVwdmFsdWVcIiwgXCJkZWJ1Zy5zZXRmZW52XCIsIFwiZGVidWcuc2V0aG9va1wiLCBcImRlYnVnLnNldGxvY2FsXCIsIFwiZGVidWcuc2V0bWV0YXRhYmxlXCIsIFwiZGVidWcuc2V0dXB2YWx1ZVwiLCBcImRlYnVnLnRyYWNlYmFja1wiLCBcImNsb3NlXCIsIFwiZmx1c2hcIiwgXCJsaW5lc1wiLCBcInJlYWRcIiwgXCJzZWVrXCIsIFwic2V0dmJ1ZlwiLCBcIndyaXRlXCIsIFwiaW8uY2xvc2VcIiwgXCJpby5mbHVzaFwiLCBcImlvLmlucHV0XCIsIFwiaW8ubGluZXNcIiwgXCJpby5vcGVuXCIsIFwiaW8ub3V0cHV0XCIsIFwiaW8ucG9wZW5cIiwgXCJpby5yZWFkXCIsIFwiaW8uc3RkZXJyXCIsIFwiaW8uc3RkaW5cIiwgXCJpby5zdGRvdXRcIiwgXCJpby50bXBmaWxlXCIsIFwiaW8udHlwZVwiLCBcImlvLndyaXRlXCIsIFwibWF0aC5hYnNcIiwgXCJtYXRoLmFjb3NcIiwgXCJtYXRoLmFzaW5cIiwgXCJtYXRoLmF0YW5cIiwgXCJtYXRoLmF0YW4yXCIsIFwibWF0aC5jZWlsXCIsIFwibWF0aC5jb3NcIiwgXCJtYXRoLmNvc2hcIiwgXCJtYXRoLmRlZ1wiLCBcIm1hdGguZXhwXCIsIFwibWF0aC5mbG9vclwiLCBcIm1hdGguZm1vZFwiLCBcIm1hdGguZnJleHBcIiwgXCJtYXRoLmh1Z2VcIiwgXCJtYXRoLmxkZXhwXCIsIFwibWF0aC5sb2dcIiwgXCJtYXRoLmxvZzEwXCIsIFwibWF0aC5tYXhcIiwgXCJtYXRoLm1pblwiLCBcIm1hdGgubW9kZlwiLCBcIm1hdGgucGlcIiwgXCJtYXRoLnBvd1wiLCBcIm1hdGgucmFkXCIsIFwibWF0aC5yYW5kb21cIiwgXCJtYXRoLnJhbmRvbXNlZWRcIiwgXCJtYXRoLnNpblwiLCBcIm1hdGguc2luaFwiLCBcIm1hdGguc3FydFwiLCBcIm1hdGgudGFuXCIsIFwibWF0aC50YW5oXCIsIFwib3MuY2xvY2tcIiwgXCJvcy5kYXRlXCIsIFwib3MuZGlmZnRpbWVcIiwgXCJvcy5leGVjdXRlXCIsIFwib3MuZXhpdFwiLCBcIm9zLmdldGVudlwiLCBcIm9zLnJlbW92ZVwiLCBcIm9zLnJlbmFtZVwiLCBcIm9zLnNldGxvY2FsZVwiLCBcIm9zLnRpbWVcIiwgXCJvcy50bXBuYW1lXCIsIFwicGFja2FnZS5jcGF0aFwiLCBcInBhY2thZ2UubG9hZGVkXCIsIFwicGFja2FnZS5sb2FkZXJzXCIsIFwicGFja2FnZS5sb2FkbGliXCIsIFwicGFja2FnZS5wYXRoXCIsIFwicGFja2FnZS5wcmVsb2FkXCIsIFwicGFja2FnZS5zZWVhbGxcIiwgXCJzdHJpbmcuYnl0ZVwiLCBcInN0cmluZy5jaGFyXCIsIFwic3RyaW5nLmR1bXBcIiwgXCJzdHJpbmcuZmluZFwiLCBcInN0cmluZy5mb3JtYXRcIiwgXCJzdHJpbmcuZ21hdGNoXCIsIFwic3RyaW5nLmdzdWJcIiwgXCJzdHJpbmcubGVuXCIsIFwic3RyaW5nLmxvd2VyXCIsIFwic3RyaW5nLm1hdGNoXCIsIFwic3RyaW5nLnJlcFwiLCBcInN0cmluZy5yZXZlcnNlXCIsIFwic3RyaW5nLnN1YlwiLCBcInN0cmluZy51cHBlclwiLCBcInRhYmxlLmNvbmNhdFwiLCBcInRhYmxlLmluc2VydFwiLCBcInRhYmxlLm1heG5cIiwgXCJ0YWJsZS5yZW1vdmVcIiwgXCJ0YWJsZS5zb3J0XCJdKTtcbnZhciBrZXl3b3JkcyA9IHdvcmRSRShbXCJhbmRcIiwgXCJicmVha1wiLCBcImVsc2VpZlwiLCBcImZhbHNlXCIsIFwibmlsXCIsIFwibm90XCIsIFwib3JcIiwgXCJyZXR1cm5cIiwgXCJ0cnVlXCIsIFwiZnVuY3Rpb25cIiwgXCJlbmRcIiwgXCJpZlwiLCBcInRoZW5cIiwgXCJlbHNlXCIsIFwiZG9cIiwgXCJ3aGlsZVwiLCBcInJlcGVhdFwiLCBcInVudGlsXCIsIFwiZm9yXCIsIFwiaW5cIiwgXCJsb2NhbFwiXSk7XG52YXIgaW5kZW50VG9rZW5zID0gd29yZFJFKFtcImZ1bmN0aW9uXCIsIFwiaWZcIiwgXCJyZXBlYXRcIiwgXCJkb1wiLCBcIlxcXFwoXCIsIFwie1wiXSk7XG52YXIgZGVkZW50VG9rZW5zID0gd29yZFJFKFtcImVuZFwiLCBcInVudGlsXCIsIFwiXFxcXClcIiwgXCJ9XCJdKTtcbnZhciBkZWRlbnRQYXJ0aWFsID0gcHJlZml4UkUoW1wiZW5kXCIsIFwidW50aWxcIiwgXCJcXFxcKVwiLCBcIn1cIiwgXCJlbHNlXCIsIFwiZWxzZWlmXCJdKTtcbmZ1bmN0aW9uIHJlYWRCcmFja2V0KHN0cmVhbSkge1xuICB2YXIgbGV2ZWwgPSAwO1xuICB3aGlsZSAoc3RyZWFtLmVhdChcIj1cIikpICsrbGV2ZWw7XG4gIHN0cmVhbS5lYXQoXCJbXCIpO1xuICByZXR1cm4gbGV2ZWw7XG59XG5mdW5jdGlvbiBub3JtYWwoc3RyZWFtLCBzdGF0ZSkge1xuICB2YXIgY2ggPSBzdHJlYW0ubmV4dCgpO1xuICBpZiAoY2ggPT0gXCItXCIgJiYgc3RyZWFtLmVhdChcIi1cIikpIHtcbiAgICBpZiAoc3RyZWFtLmVhdChcIltcIikgJiYgc3RyZWFtLmVhdChcIltcIikpIHJldHVybiAoc3RhdGUuY3VyID0gYnJhY2tldGVkKHJlYWRCcmFja2V0KHN0cmVhbSksIFwiY29tbWVudFwiKSkoc3RyZWFtLCBzdGF0ZSk7XG4gICAgc3RyZWFtLnNraXBUb0VuZCgpO1xuICAgIHJldHVybiBcImNvbW1lbnRcIjtcbiAgfVxuICBpZiAoY2ggPT0gXCJcXFwiXCIgfHwgY2ggPT0gXCInXCIpIHJldHVybiAoc3RhdGUuY3VyID0gc3RyaW5nKGNoKSkoc3RyZWFtLCBzdGF0ZSk7XG4gIGlmIChjaCA9PSBcIltcIiAmJiAvW1xcWz1dLy50ZXN0KHN0cmVhbS5wZWVrKCkpKSByZXR1cm4gKHN0YXRlLmN1ciA9IGJyYWNrZXRlZChyZWFkQnJhY2tldChzdHJlYW0pLCBcInN0cmluZ1wiKSkoc3RyZWFtLCBzdGF0ZSk7XG4gIGlmICgvXFxkLy50ZXN0KGNoKSkge1xuICAgIHN0cmVhbS5lYXRXaGlsZSgvW1xcdy4lXS8pO1xuICAgIHJldHVybiBcIm51bWJlclwiO1xuICB9XG4gIGlmICgvW1xcd19dLy50ZXN0KGNoKSkge1xuICAgIHN0cmVhbS5lYXRXaGlsZSgvW1xcd1xcXFxcXC1fLl0vKTtcbiAgICByZXR1cm4gXCJ2YXJpYWJsZVwiO1xuICB9XG4gIHJldHVybiBudWxsO1xufVxuZnVuY3Rpb24gYnJhY2tldGVkKGxldmVsLCBzdHlsZSkge1xuICByZXR1cm4gZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICB2YXIgY3VybGV2ID0gbnVsbCxcbiAgICAgIGNoO1xuICAgIHdoaWxlICgoY2ggPSBzdHJlYW0ubmV4dCgpKSAhPSBudWxsKSB7XG4gICAgICBpZiAoY3VybGV2ID09IG51bGwpIHtcbiAgICAgICAgaWYgKGNoID09IFwiXVwiKSBjdXJsZXYgPSAwO1xuICAgICAgfSBlbHNlIGlmIChjaCA9PSBcIj1cIikgKytjdXJsZXY7ZWxzZSBpZiAoY2ggPT0gXCJdXCIgJiYgY3VybGV2ID09IGxldmVsKSB7XG4gICAgICAgIHN0YXRlLmN1ciA9IG5vcm1hbDtcbiAgICAgICAgYnJlYWs7XG4gICAgICB9IGVsc2UgY3VybGV2ID0gbnVsbDtcbiAgICB9XG4gICAgcmV0dXJuIHN0eWxlO1xuICB9O1xufVxuZnVuY3Rpb24gc3RyaW5nKHF1b3RlKSB7XG4gIHJldHVybiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIHZhciBlc2NhcGVkID0gZmFsc2UsXG4gICAgICBjaDtcbiAgICB3aGlsZSAoKGNoID0gc3RyZWFtLm5leHQoKSkgIT0gbnVsbCkge1xuICAgICAgaWYgKGNoID09IHF1b3RlICYmICFlc2NhcGVkKSBicmVhaztcbiAgICAgIGVzY2FwZWQgPSAhZXNjYXBlZCAmJiBjaCA9PSBcIlxcXFxcIjtcbiAgICB9XG4gICAgaWYgKCFlc2NhcGVkKSBzdGF0ZS5jdXIgPSBub3JtYWw7XG4gICAgcmV0dXJuIFwic3RyaW5nXCI7XG4gIH07XG59XG5leHBvcnQgY29uc3QgbHVhID0ge1xuICBuYW1lOiBcImx1YVwiLFxuICBzdGFydFN0YXRlOiBmdW5jdGlvbiAoKSB7XG4gICAgcmV0dXJuIHtcbiAgICAgIGJhc2Vjb2w6IDAsXG4gICAgICBpbmRlbnREZXB0aDogMCxcbiAgICAgIGN1cjogbm9ybWFsXG4gICAgfTtcbiAgfSxcbiAgdG9rZW46IGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgaWYgKHN0cmVhbS5lYXRTcGFjZSgpKSByZXR1cm4gbnVsbDtcbiAgICB2YXIgc3R5bGUgPSBzdGF0ZS5jdXIoc3RyZWFtLCBzdGF0ZSk7XG4gICAgdmFyIHdvcmQgPSBzdHJlYW0uY3VycmVudCgpO1xuICAgIGlmIChzdHlsZSA9PSBcInZhcmlhYmxlXCIpIHtcbiAgICAgIGlmIChrZXl3b3Jkcy50ZXN0KHdvcmQpKSBzdHlsZSA9IFwia2V5d29yZFwiO2Vsc2UgaWYgKGJ1aWx0aW5zLnRlc3Qod29yZCkpIHN0eWxlID0gXCJidWlsdGluXCI7XG4gICAgfVxuICAgIGlmIChzdHlsZSAhPSBcImNvbW1lbnRcIiAmJiBzdHlsZSAhPSBcInN0cmluZ1wiKSB7XG4gICAgICBpZiAoaW5kZW50VG9rZW5zLnRlc3Qod29yZCkpICsrc3RhdGUuaW5kZW50RGVwdGg7ZWxzZSBpZiAoZGVkZW50VG9rZW5zLnRlc3Qod29yZCkpIC0tc3RhdGUuaW5kZW50RGVwdGg7XG4gICAgfVxuICAgIHJldHVybiBzdHlsZTtcbiAgfSxcbiAgaW5kZW50OiBmdW5jdGlvbiAoc3RhdGUsIHRleHRBZnRlciwgY3gpIHtcbiAgICB2YXIgY2xvc2luZyA9IGRlZGVudFBhcnRpYWwudGVzdCh0ZXh0QWZ0ZXIpO1xuICAgIHJldHVybiBzdGF0ZS5iYXNlY29sICsgY3gudW5pdCAqIChzdGF0ZS5pbmRlbnREZXB0aCAtIChjbG9zaW5nID8gMSA6IDApKTtcbiAgfSxcbiAgbGFuZ3VhZ2VEYXRhOiB7XG4gICAgaW5kZW50T25JbnB1dDogL15cXHMqKD86ZW5kfHVudGlsfGVsc2V8XFwpfFxcfSkkLyxcbiAgICBjb21tZW50VG9rZW5zOiB7XG4gICAgICBsaW5lOiBcIi0tXCIsXG4gICAgICBibG9jazoge1xuICAgICAgICBvcGVuOiBcIi0tW1tcIixcbiAgICAgICAgY2xvc2U6IFwiXV0tLVwiXG4gICAgICB9XG4gICAgfVxuICB9XG59OyJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==