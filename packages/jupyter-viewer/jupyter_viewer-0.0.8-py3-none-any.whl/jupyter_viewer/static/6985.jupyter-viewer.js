"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[6985],{

/***/ 16985:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "shell": () => (/* binding */ shell)
/* harmony export */ });
var words = {};
function define(style, dict) {
  for (var i = 0; i < dict.length; i++) {
    words[dict[i]] = style;
  }
}
;
var commonAtoms = ["true", "false"];
var commonKeywords = ["if", "then", "do", "else", "elif", "while", "until", "for", "in", "esac", "fi", "fin", "fil", "done", "exit", "set", "unset", "export", "function"];
var commonCommands = ["ab", "awk", "bash", "beep", "cat", "cc", "cd", "chown", "chmod", "chroot", "clear", "cp", "curl", "cut", "diff", "echo", "find", "gawk", "gcc", "get", "git", "grep", "hg", "kill", "killall", "ln", "ls", "make", "mkdir", "openssl", "mv", "nc", "nl", "node", "npm", "ping", "ps", "restart", "rm", "rmdir", "sed", "service", "sh", "shopt", "shred", "source", "sort", "sleep", "ssh", "start", "stop", "su", "sudo", "svn", "tee", "telnet", "top", "touch", "vi", "vim", "wall", "wc", "wget", "who", "write", "yes", "zsh"];
define('atom', commonAtoms);
define('keyword', commonKeywords);
define('builtin', commonCommands);
function tokenBase(stream, state) {
  if (stream.eatSpace()) return null;
  var sol = stream.sol();
  var ch = stream.next();
  if (ch === '\\') {
    stream.next();
    return null;
  }
  if (ch === '\'' || ch === '"' || ch === '`') {
    state.tokens.unshift(tokenString(ch, ch === "`" ? "quote" : "string"));
    return tokenize(stream, state);
  }
  if (ch === '#') {
    if (sol && stream.eat('!')) {
      stream.skipToEnd();
      return 'meta'; // 'comment'?
    }
    stream.skipToEnd();
    return 'comment';
  }
  if (ch === '$') {
    state.tokens.unshift(tokenDollar);
    return tokenize(stream, state);
  }
  if (ch === '+' || ch === '=') {
    return 'operator';
  }
  if (ch === '-') {
    stream.eat('-');
    stream.eatWhile(/\w/);
    return 'attribute';
  }
  if (ch == "<") {
    if (stream.match("<<")) return "operator";
    var heredoc = stream.match(/^<-?\s*(?:['"]([^'"]*)['"]|([^'"\s]*))/);
    if (heredoc) {
      state.tokens.unshift(tokenHeredoc(heredoc[1] || heredoc[2]));
      return 'string.special';
    }
  }
  if (/\d/.test(ch)) {
    stream.eatWhile(/\d/);
    if (stream.eol() || !/\w/.test(stream.peek())) {
      return 'number';
    }
  }
  stream.eatWhile(/[\w-]/);
  var cur = stream.current();
  if (stream.peek() === '=' && /\w+/.test(cur)) return 'def';
  return words.hasOwnProperty(cur) ? words[cur] : null;
}
function tokenString(quote, style) {
  var close = quote == "(" ? ")" : quote == "{" ? "}" : quote;
  return function (stream, state) {
    var next,
      escaped = false;
    while ((next = stream.next()) != null) {
      if (next === close && !escaped) {
        state.tokens.shift();
        break;
      } else if (next === '$' && !escaped && quote !== "'" && stream.peek() != close) {
        escaped = true;
        stream.backUp(1);
        state.tokens.unshift(tokenDollar);
        break;
      } else if (!escaped && quote !== close && next === quote) {
        state.tokens.unshift(tokenString(quote, style));
        return tokenize(stream, state);
      } else if (!escaped && /['"]/.test(next) && !/['"]/.test(quote)) {
        state.tokens.unshift(tokenStringStart(next, "string"));
        stream.backUp(1);
        break;
      }
      escaped = !escaped && next === '\\';
    }
    return style;
  };
}
;
function tokenStringStart(quote, style) {
  return function (stream, state) {
    state.tokens[0] = tokenString(quote, style);
    stream.next();
    return tokenize(stream, state);
  };
}
var tokenDollar = function (stream, state) {
  if (state.tokens.length > 1) stream.eat('$');
  var ch = stream.next();
  if (/['"({]/.test(ch)) {
    state.tokens[0] = tokenString(ch, ch == "(" ? "quote" : ch == "{" ? "def" : "string");
    return tokenize(stream, state);
  }
  if (!/\d/.test(ch)) stream.eatWhile(/\w/);
  state.tokens.shift();
  return 'def';
};
function tokenHeredoc(delim) {
  return function (stream, state) {
    if (stream.sol() && stream.string == delim) state.tokens.shift();
    stream.skipToEnd();
    return "string.special";
  };
}
function tokenize(stream, state) {
  return (state.tokens[0] || tokenBase)(stream, state);
}
;
const shell = {
  name: "shell",
  startState: function () {
    return {
      tokens: []
    };
  },
  token: function (stream, state) {
    return tokenize(stream, state);
  },
  languageData: {
    autocomplete: commonAtoms.concat(commonKeywords, commonCommands),
    closeBrackets: {
      brackets: ["(", "[", "{", "'", '"', "`"]
    },
    commentTokens: {
      line: "#"
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNjk4NS5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9AY29kZW1pcnJvci9sZWdhY3ktbW9kZXMvbW9kZS9zaGVsbC5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyJ2YXIgd29yZHMgPSB7fTtcbmZ1bmN0aW9uIGRlZmluZShzdHlsZSwgZGljdCkge1xuICBmb3IgKHZhciBpID0gMDsgaSA8IGRpY3QubGVuZ3RoOyBpKyspIHtcbiAgICB3b3Jkc1tkaWN0W2ldXSA9IHN0eWxlO1xuICB9XG59XG47XG52YXIgY29tbW9uQXRvbXMgPSBbXCJ0cnVlXCIsIFwiZmFsc2VcIl07XG52YXIgY29tbW9uS2V5d29yZHMgPSBbXCJpZlwiLCBcInRoZW5cIiwgXCJkb1wiLCBcImVsc2VcIiwgXCJlbGlmXCIsIFwid2hpbGVcIiwgXCJ1bnRpbFwiLCBcImZvclwiLCBcImluXCIsIFwiZXNhY1wiLCBcImZpXCIsIFwiZmluXCIsIFwiZmlsXCIsIFwiZG9uZVwiLCBcImV4aXRcIiwgXCJzZXRcIiwgXCJ1bnNldFwiLCBcImV4cG9ydFwiLCBcImZ1bmN0aW9uXCJdO1xudmFyIGNvbW1vbkNvbW1hbmRzID0gW1wiYWJcIiwgXCJhd2tcIiwgXCJiYXNoXCIsIFwiYmVlcFwiLCBcImNhdFwiLCBcImNjXCIsIFwiY2RcIiwgXCJjaG93blwiLCBcImNobW9kXCIsIFwiY2hyb290XCIsIFwiY2xlYXJcIiwgXCJjcFwiLCBcImN1cmxcIiwgXCJjdXRcIiwgXCJkaWZmXCIsIFwiZWNob1wiLCBcImZpbmRcIiwgXCJnYXdrXCIsIFwiZ2NjXCIsIFwiZ2V0XCIsIFwiZ2l0XCIsIFwiZ3JlcFwiLCBcImhnXCIsIFwia2lsbFwiLCBcImtpbGxhbGxcIiwgXCJsblwiLCBcImxzXCIsIFwibWFrZVwiLCBcIm1rZGlyXCIsIFwib3BlbnNzbFwiLCBcIm12XCIsIFwibmNcIiwgXCJubFwiLCBcIm5vZGVcIiwgXCJucG1cIiwgXCJwaW5nXCIsIFwicHNcIiwgXCJyZXN0YXJ0XCIsIFwicm1cIiwgXCJybWRpclwiLCBcInNlZFwiLCBcInNlcnZpY2VcIiwgXCJzaFwiLCBcInNob3B0XCIsIFwic2hyZWRcIiwgXCJzb3VyY2VcIiwgXCJzb3J0XCIsIFwic2xlZXBcIiwgXCJzc2hcIiwgXCJzdGFydFwiLCBcInN0b3BcIiwgXCJzdVwiLCBcInN1ZG9cIiwgXCJzdm5cIiwgXCJ0ZWVcIiwgXCJ0ZWxuZXRcIiwgXCJ0b3BcIiwgXCJ0b3VjaFwiLCBcInZpXCIsIFwidmltXCIsIFwid2FsbFwiLCBcIndjXCIsIFwid2dldFwiLCBcIndob1wiLCBcIndyaXRlXCIsIFwieWVzXCIsIFwienNoXCJdO1xuZGVmaW5lKCdhdG9tJywgY29tbW9uQXRvbXMpO1xuZGVmaW5lKCdrZXl3b3JkJywgY29tbW9uS2V5d29yZHMpO1xuZGVmaW5lKCdidWlsdGluJywgY29tbW9uQ29tbWFuZHMpO1xuZnVuY3Rpb24gdG9rZW5CYXNlKHN0cmVhbSwgc3RhdGUpIHtcbiAgaWYgKHN0cmVhbS5lYXRTcGFjZSgpKSByZXR1cm4gbnVsbDtcbiAgdmFyIHNvbCA9IHN0cmVhbS5zb2woKTtcbiAgdmFyIGNoID0gc3RyZWFtLm5leHQoKTtcbiAgaWYgKGNoID09PSAnXFxcXCcpIHtcbiAgICBzdHJlYW0ubmV4dCgpO1xuICAgIHJldHVybiBudWxsO1xuICB9XG4gIGlmIChjaCA9PT0gJ1xcJycgfHwgY2ggPT09ICdcIicgfHwgY2ggPT09ICdgJykge1xuICAgIHN0YXRlLnRva2Vucy51bnNoaWZ0KHRva2VuU3RyaW5nKGNoLCBjaCA9PT0gXCJgXCIgPyBcInF1b3RlXCIgOiBcInN0cmluZ1wiKSk7XG4gICAgcmV0dXJuIHRva2VuaXplKHN0cmVhbSwgc3RhdGUpO1xuICB9XG4gIGlmIChjaCA9PT0gJyMnKSB7XG4gICAgaWYgKHNvbCAmJiBzdHJlYW0uZWF0KCchJykpIHtcbiAgICAgIHN0cmVhbS5za2lwVG9FbmQoKTtcbiAgICAgIHJldHVybiAnbWV0YSc7IC8vICdjb21tZW50Jz9cbiAgICB9XG4gICAgc3RyZWFtLnNraXBUb0VuZCgpO1xuICAgIHJldHVybiAnY29tbWVudCc7XG4gIH1cbiAgaWYgKGNoID09PSAnJCcpIHtcbiAgICBzdGF0ZS50b2tlbnMudW5zaGlmdCh0b2tlbkRvbGxhcik7XG4gICAgcmV0dXJuIHRva2VuaXplKHN0cmVhbSwgc3RhdGUpO1xuICB9XG4gIGlmIChjaCA9PT0gJysnIHx8IGNoID09PSAnPScpIHtcbiAgICByZXR1cm4gJ29wZXJhdG9yJztcbiAgfVxuICBpZiAoY2ggPT09ICctJykge1xuICAgIHN0cmVhbS5lYXQoJy0nKTtcbiAgICBzdHJlYW0uZWF0V2hpbGUoL1xcdy8pO1xuICAgIHJldHVybiAnYXR0cmlidXRlJztcbiAgfVxuICBpZiAoY2ggPT0gXCI8XCIpIHtcbiAgICBpZiAoc3RyZWFtLm1hdGNoKFwiPDxcIikpIHJldHVybiBcIm9wZXJhdG9yXCI7XG4gICAgdmFyIGhlcmVkb2MgPSBzdHJlYW0ubWF0Y2goL148LT9cXHMqKD86WydcIl0oW14nXCJdKilbJ1wiXXwoW14nXCJcXHNdKikpLyk7XG4gICAgaWYgKGhlcmVkb2MpIHtcbiAgICAgIHN0YXRlLnRva2Vucy51bnNoaWZ0KHRva2VuSGVyZWRvYyhoZXJlZG9jWzFdIHx8IGhlcmVkb2NbMl0pKTtcbiAgICAgIHJldHVybiAnc3RyaW5nLnNwZWNpYWwnO1xuICAgIH1cbiAgfVxuICBpZiAoL1xcZC8udGVzdChjaCkpIHtcbiAgICBzdHJlYW0uZWF0V2hpbGUoL1xcZC8pO1xuICAgIGlmIChzdHJlYW0uZW9sKCkgfHwgIS9cXHcvLnRlc3Qoc3RyZWFtLnBlZWsoKSkpIHtcbiAgICAgIHJldHVybiAnbnVtYmVyJztcbiAgICB9XG4gIH1cbiAgc3RyZWFtLmVhdFdoaWxlKC9bXFx3LV0vKTtcbiAgdmFyIGN1ciA9IHN0cmVhbS5jdXJyZW50KCk7XG4gIGlmIChzdHJlYW0ucGVlaygpID09PSAnPScgJiYgL1xcdysvLnRlc3QoY3VyKSkgcmV0dXJuICdkZWYnO1xuICByZXR1cm4gd29yZHMuaGFzT3duUHJvcGVydHkoY3VyKSA/IHdvcmRzW2N1cl0gOiBudWxsO1xufVxuZnVuY3Rpb24gdG9rZW5TdHJpbmcocXVvdGUsIHN0eWxlKSB7XG4gIHZhciBjbG9zZSA9IHF1b3RlID09IFwiKFwiID8gXCIpXCIgOiBxdW90ZSA9PSBcIntcIiA/IFwifVwiIDogcXVvdGU7XG4gIHJldHVybiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIHZhciBuZXh0LFxuICAgICAgZXNjYXBlZCA9IGZhbHNlO1xuICAgIHdoaWxlICgobmV4dCA9IHN0cmVhbS5uZXh0KCkpICE9IG51bGwpIHtcbiAgICAgIGlmIChuZXh0ID09PSBjbG9zZSAmJiAhZXNjYXBlZCkge1xuICAgICAgICBzdGF0ZS50b2tlbnMuc2hpZnQoKTtcbiAgICAgICAgYnJlYWs7XG4gICAgICB9IGVsc2UgaWYgKG5leHQgPT09ICckJyAmJiAhZXNjYXBlZCAmJiBxdW90ZSAhPT0gXCInXCIgJiYgc3RyZWFtLnBlZWsoKSAhPSBjbG9zZSkge1xuICAgICAgICBlc2NhcGVkID0gdHJ1ZTtcbiAgICAgICAgc3RyZWFtLmJhY2tVcCgxKTtcbiAgICAgICAgc3RhdGUudG9rZW5zLnVuc2hpZnQodG9rZW5Eb2xsYXIpO1xuICAgICAgICBicmVhaztcbiAgICAgIH0gZWxzZSBpZiAoIWVzY2FwZWQgJiYgcXVvdGUgIT09IGNsb3NlICYmIG5leHQgPT09IHF1b3RlKSB7XG4gICAgICAgIHN0YXRlLnRva2Vucy51bnNoaWZ0KHRva2VuU3RyaW5nKHF1b3RlLCBzdHlsZSkpO1xuICAgICAgICByZXR1cm4gdG9rZW5pemUoc3RyZWFtLCBzdGF0ZSk7XG4gICAgICB9IGVsc2UgaWYgKCFlc2NhcGVkICYmIC9bJ1wiXS8udGVzdChuZXh0KSAmJiAhL1snXCJdLy50ZXN0KHF1b3RlKSkge1xuICAgICAgICBzdGF0ZS50b2tlbnMudW5zaGlmdCh0b2tlblN0cmluZ1N0YXJ0KG5leHQsIFwic3RyaW5nXCIpKTtcbiAgICAgICAgc3RyZWFtLmJhY2tVcCgxKTtcbiAgICAgICAgYnJlYWs7XG4gICAgICB9XG4gICAgICBlc2NhcGVkID0gIWVzY2FwZWQgJiYgbmV4dCA9PT0gJ1xcXFwnO1xuICAgIH1cbiAgICByZXR1cm4gc3R5bGU7XG4gIH07XG59XG47XG5mdW5jdGlvbiB0b2tlblN0cmluZ1N0YXJ0KHF1b3RlLCBzdHlsZSkge1xuICByZXR1cm4gZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICBzdGF0ZS50b2tlbnNbMF0gPSB0b2tlblN0cmluZyhxdW90ZSwgc3R5bGUpO1xuICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgcmV0dXJuIHRva2VuaXplKHN0cmVhbSwgc3RhdGUpO1xuICB9O1xufVxudmFyIHRva2VuRG9sbGFyID0gZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgaWYgKHN0YXRlLnRva2Vucy5sZW5ndGggPiAxKSBzdHJlYW0uZWF0KCckJyk7XG4gIHZhciBjaCA9IHN0cmVhbS5uZXh0KCk7XG4gIGlmICgvWydcIih7XS8udGVzdChjaCkpIHtcbiAgICBzdGF0ZS50b2tlbnNbMF0gPSB0b2tlblN0cmluZyhjaCwgY2ggPT0gXCIoXCIgPyBcInF1b3RlXCIgOiBjaCA9PSBcIntcIiA/IFwiZGVmXCIgOiBcInN0cmluZ1wiKTtcbiAgICByZXR1cm4gdG9rZW5pemUoc3RyZWFtLCBzdGF0ZSk7XG4gIH1cbiAgaWYgKCEvXFxkLy50ZXN0KGNoKSkgc3RyZWFtLmVhdFdoaWxlKC9cXHcvKTtcbiAgc3RhdGUudG9rZW5zLnNoaWZ0KCk7XG4gIHJldHVybiAnZGVmJztcbn07XG5mdW5jdGlvbiB0b2tlbkhlcmVkb2MoZGVsaW0pIHtcbiAgcmV0dXJuIGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgaWYgKHN0cmVhbS5zb2woKSAmJiBzdHJlYW0uc3RyaW5nID09IGRlbGltKSBzdGF0ZS50b2tlbnMuc2hpZnQoKTtcbiAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgcmV0dXJuIFwic3RyaW5nLnNwZWNpYWxcIjtcbiAgfTtcbn1cbmZ1bmN0aW9uIHRva2VuaXplKHN0cmVhbSwgc3RhdGUpIHtcbiAgcmV0dXJuIChzdGF0ZS50b2tlbnNbMF0gfHwgdG9rZW5CYXNlKShzdHJlYW0sIHN0YXRlKTtcbn1cbjtcbmV4cG9ydCBjb25zdCBzaGVsbCA9IHtcbiAgbmFtZTogXCJzaGVsbFwiLFxuICBzdGFydFN0YXRlOiBmdW5jdGlvbiAoKSB7XG4gICAgcmV0dXJuIHtcbiAgICAgIHRva2VuczogW11cbiAgICB9O1xuICB9LFxuICB0b2tlbjogZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICByZXR1cm4gdG9rZW5pemUoc3RyZWFtLCBzdGF0ZSk7XG4gIH0sXG4gIGxhbmd1YWdlRGF0YToge1xuICAgIGF1dG9jb21wbGV0ZTogY29tbW9uQXRvbXMuY29uY2F0KGNvbW1vbktleXdvcmRzLCBjb21tb25Db21tYW5kcyksXG4gICAgY2xvc2VCcmFja2V0czoge1xuICAgICAgYnJhY2tldHM6IFtcIihcIiwgXCJbXCIsIFwie1wiLCBcIidcIiwgJ1wiJywgXCJgXCJdXG4gICAgfSxcbiAgICBjb21tZW50VG9rZW5zOiB7XG4gICAgICBsaW5lOiBcIiNcIlxuICAgIH1cbiAgfVxufTsiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=