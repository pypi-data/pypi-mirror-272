"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[3833],{

/***/ 93833:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ruby": () => (/* binding */ ruby)
/* harmony export */ });
function wordObj(words) {
  var o = {};
  for (var i = 0, e = words.length; i < e; ++i) o[words[i]] = true;
  return o;
}
var keywordList = ["alias", "and", "BEGIN", "begin", "break", "case", "class", "def", "defined?", "do", "else", "elsif", "END", "end", "ensure", "false", "for", "if", "in", "module", "next", "not", "or", "redo", "rescue", "retry", "return", "self", "super", "then", "true", "undef", "unless", "until", "when", "while", "yield", "nil", "raise", "throw", "catch", "fail", "loop", "callcc", "caller", "lambda", "proc", "public", "protected", "private", "require", "load", "require_relative", "extend", "autoload", "__END__", "__FILE__", "__LINE__", "__dir__"],
  keywords = wordObj(keywordList);
var indentWords = wordObj(["def", "class", "case", "for", "while", "until", "module", "catch", "loop", "proc", "begin"]);
var dedentWords = wordObj(["end", "until"]);
var opening = {
  "[": "]",
  "{": "}",
  "(": ")"
};
var closing = {
  "]": "[",
  "}": "{",
  ")": "("
};
var curPunc;
function chain(newtok, stream, state) {
  state.tokenize.push(newtok);
  return newtok(stream, state);
}
function tokenBase(stream, state) {
  if (stream.sol() && stream.match("=begin") && stream.eol()) {
    state.tokenize.push(readBlockComment);
    return "comment";
  }
  if (stream.eatSpace()) return null;
  var ch = stream.next(),
    m;
  if (ch == "`" || ch == "'" || ch == '"') {
    return chain(readQuoted(ch, "string", ch == '"' || ch == "`"), stream, state);
  } else if (ch == "/") {
    if (regexpAhead(stream)) return chain(readQuoted(ch, "string.special", true), stream, state);else return "operator";
  } else if (ch == "%") {
    var style = "string",
      embed = true;
    if (stream.eat("s")) style = "atom";else if (stream.eat(/[WQ]/)) style = "string";else if (stream.eat(/[r]/)) style = "string.special";else if (stream.eat(/[wxq]/)) {
      style = "string";
      embed = false;
    }
    var delim = stream.eat(/[^\w\s=]/);
    if (!delim) return "operator";
    if (opening.propertyIsEnumerable(delim)) delim = opening[delim];
    return chain(readQuoted(delim, style, embed, true), stream, state);
  } else if (ch == "#") {
    stream.skipToEnd();
    return "comment";
  } else if (ch == "<" && (m = stream.match(/^<([-~])[\`\"\']?([a-zA-Z_?]\w*)[\`\"\']?(?:;|$)/))) {
    return chain(readHereDoc(m[2], m[1]), stream, state);
  } else if (ch == "0") {
    if (stream.eat("x")) stream.eatWhile(/[\da-fA-F]/);else if (stream.eat("b")) stream.eatWhile(/[01]/);else stream.eatWhile(/[0-7]/);
    return "number";
  } else if (/\d/.test(ch)) {
    stream.match(/^[\d_]*(?:\.[\d_]+)?(?:[eE][+\-]?[\d_]+)?/);
    return "number";
  } else if (ch == "?") {
    while (stream.match(/^\\[CM]-/)) {}
    if (stream.eat("\\")) stream.eatWhile(/\w/);else stream.next();
    return "string";
  } else if (ch == ":") {
    if (stream.eat("'")) return chain(readQuoted("'", "atom", false), stream, state);
    if (stream.eat('"')) return chain(readQuoted('"', "atom", true), stream, state);

    // :> :>> :< :<< are valid symbols
    if (stream.eat(/[\<\>]/)) {
      stream.eat(/[\<\>]/);
      return "atom";
    }

    // :+ :- :/ :* :| :& :! are valid symbols
    if (stream.eat(/[\+\-\*\/\&\|\:\!]/)) {
      return "atom";
    }

    // Symbols can't start by a digit
    if (stream.eat(/[a-zA-Z$@_\xa1-\uffff]/)) {
      stream.eatWhile(/[\w$\xa1-\uffff]/);
      // Only one ? ! = is allowed and only as the last character
      stream.eat(/[\?\!\=]/);
      return "atom";
    }
    return "operator";
  } else if (ch == "@" && stream.match(/^@?[a-zA-Z_\xa1-\uffff]/)) {
    stream.eat("@");
    stream.eatWhile(/[\w\xa1-\uffff]/);
    return "propertyName";
  } else if (ch == "$") {
    if (stream.eat(/[a-zA-Z_]/)) {
      stream.eatWhile(/[\w]/);
    } else if (stream.eat(/\d/)) {
      stream.eat(/\d/);
    } else {
      stream.next(); // Must be a special global like $: or $!
    }
    return "variableName.special";
  } else if (/[a-zA-Z_\xa1-\uffff]/.test(ch)) {
    stream.eatWhile(/[\w\xa1-\uffff]/);
    stream.eat(/[\?\!]/);
    if (stream.eat(":")) return "atom";
    return "variable";
  } else if (ch == "|" && (state.varList || state.lastTok == "{" || state.lastTok == "do")) {
    curPunc = "|";
    return null;
  } else if (/[\(\)\[\]{}\\;]/.test(ch)) {
    curPunc = ch;
    return null;
  } else if (ch == "-" && stream.eat(">")) {
    return "operator";
  } else if (/[=+\-\/*:\.^%<>~|]/.test(ch)) {
    var more = stream.eatWhile(/[=+\-\/*:\.^%<>~|]/);
    if (ch == "." && !more) curPunc = ".";
    return "operator";
  } else {
    return null;
  }
}
function regexpAhead(stream) {
  var start = stream.pos,
    depth = 0,
    next,
    found = false,
    escaped = false;
  while ((next = stream.next()) != null) {
    if (!escaped) {
      if ("[{(".indexOf(next) > -1) {
        depth++;
      } else if ("]})".indexOf(next) > -1) {
        depth--;
        if (depth < 0) break;
      } else if (next == "/" && depth == 0) {
        found = true;
        break;
      }
      escaped = next == "\\";
    } else {
      escaped = false;
    }
  }
  stream.backUp(stream.pos - start);
  return found;
}
function tokenBaseUntilBrace(depth) {
  if (!depth) depth = 1;
  return function (stream, state) {
    if (stream.peek() == "}") {
      if (depth == 1) {
        state.tokenize.pop();
        return state.tokenize[state.tokenize.length - 1](stream, state);
      } else {
        state.tokenize[state.tokenize.length - 1] = tokenBaseUntilBrace(depth - 1);
      }
    } else if (stream.peek() == "{") {
      state.tokenize[state.tokenize.length - 1] = tokenBaseUntilBrace(depth + 1);
    }
    return tokenBase(stream, state);
  };
}
function tokenBaseOnce() {
  var alreadyCalled = false;
  return function (stream, state) {
    if (alreadyCalled) {
      state.tokenize.pop();
      return state.tokenize[state.tokenize.length - 1](stream, state);
    }
    alreadyCalled = true;
    return tokenBase(stream, state);
  };
}
function readQuoted(quote, style, embed, unescaped) {
  return function (stream, state) {
    var escaped = false,
      ch;
    if (state.context.type === 'read-quoted-paused') {
      state.context = state.context.prev;
      stream.eat("}");
    }
    while ((ch = stream.next()) != null) {
      if (ch == quote && (unescaped || !escaped)) {
        state.tokenize.pop();
        break;
      }
      if (embed && ch == "#" && !escaped) {
        if (stream.eat("{")) {
          if (quote == "}") {
            state.context = {
              prev: state.context,
              type: 'read-quoted-paused'
            };
          }
          state.tokenize.push(tokenBaseUntilBrace());
          break;
        } else if (/[@\$]/.test(stream.peek())) {
          state.tokenize.push(tokenBaseOnce());
          break;
        }
      }
      escaped = !escaped && ch == "\\";
    }
    return style;
  };
}
function readHereDoc(phrase, mayIndent) {
  return function (stream, state) {
    if (mayIndent) stream.eatSpace();
    if (stream.match(phrase)) state.tokenize.pop();else stream.skipToEnd();
    return "string";
  };
}
function readBlockComment(stream, state) {
  if (stream.sol() && stream.match("=end") && stream.eol()) state.tokenize.pop();
  stream.skipToEnd();
  return "comment";
}
const ruby = {
  name: "ruby",
  startState: function (indentUnit) {
    return {
      tokenize: [tokenBase],
      indented: 0,
      context: {
        type: "top",
        indented: -indentUnit
      },
      continuedLine: false,
      lastTok: null,
      varList: false
    };
  },
  token: function (stream, state) {
    curPunc = null;
    if (stream.sol()) state.indented = stream.indentation();
    var style = state.tokenize[state.tokenize.length - 1](stream, state),
      kwtype;
    var thisTok = curPunc;
    if (style == "variable") {
      var word = stream.current();
      style = state.lastTok == "." ? "property" : keywords.propertyIsEnumerable(stream.current()) ? "keyword" : /^[A-Z]/.test(word) ? "tag" : state.lastTok == "def" || state.lastTok == "class" || state.varList ? "def" : "variable";
      if (style == "keyword") {
        thisTok = word;
        if (indentWords.propertyIsEnumerable(word)) kwtype = "indent";else if (dedentWords.propertyIsEnumerable(word)) kwtype = "dedent";else if ((word == "if" || word == "unless") && stream.column() == stream.indentation()) kwtype = "indent";else if (word == "do" && state.context.indented < state.indented) kwtype = "indent";
      }
    }
    if (curPunc || style && style != "comment") state.lastTok = thisTok;
    if (curPunc == "|") state.varList = !state.varList;
    if (kwtype == "indent" || /[\(\[\{]/.test(curPunc)) state.context = {
      prev: state.context,
      type: curPunc || style,
      indented: state.indented
    };else if ((kwtype == "dedent" || /[\)\]\}]/.test(curPunc)) && state.context.prev) state.context = state.context.prev;
    if (stream.eol()) state.continuedLine = curPunc == "\\" || style == "operator";
    return style;
  },
  indent: function (state, textAfter, cx) {
    if (state.tokenize[state.tokenize.length - 1] != tokenBase) return null;
    var firstChar = textAfter && textAfter.charAt(0);
    var ct = state.context;
    var closed = ct.type == closing[firstChar] || ct.type == "keyword" && /^(?:end|until|else|elsif|when|rescue)\b/.test(textAfter);
    return ct.indented + (closed ? 0 : cx.unit) + (state.continuedLine ? cx.unit : 0);
  },
  languageData: {
    indentOnInput: /^\s*(?:end|rescue|elsif|else|\})$/,
    commentTokens: {
      line: "#"
    },
    autocomplete: keywordList
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiMzgzMy5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9AY29kZW1pcnJvci9sZWdhY3ktbW9kZXMvbW9kZS9ydWJ5LmpzIl0sInNvdXJjZXNDb250ZW50IjpbImZ1bmN0aW9uIHdvcmRPYmood29yZHMpIHtcbiAgdmFyIG8gPSB7fTtcbiAgZm9yICh2YXIgaSA9IDAsIGUgPSB3b3Jkcy5sZW5ndGg7IGkgPCBlOyArK2kpIG9bd29yZHNbaV1dID0gdHJ1ZTtcbiAgcmV0dXJuIG87XG59XG52YXIga2V5d29yZExpc3QgPSBbXCJhbGlhc1wiLCBcImFuZFwiLCBcIkJFR0lOXCIsIFwiYmVnaW5cIiwgXCJicmVha1wiLCBcImNhc2VcIiwgXCJjbGFzc1wiLCBcImRlZlwiLCBcImRlZmluZWQ/XCIsIFwiZG9cIiwgXCJlbHNlXCIsIFwiZWxzaWZcIiwgXCJFTkRcIiwgXCJlbmRcIiwgXCJlbnN1cmVcIiwgXCJmYWxzZVwiLCBcImZvclwiLCBcImlmXCIsIFwiaW5cIiwgXCJtb2R1bGVcIiwgXCJuZXh0XCIsIFwibm90XCIsIFwib3JcIiwgXCJyZWRvXCIsIFwicmVzY3VlXCIsIFwicmV0cnlcIiwgXCJyZXR1cm5cIiwgXCJzZWxmXCIsIFwic3VwZXJcIiwgXCJ0aGVuXCIsIFwidHJ1ZVwiLCBcInVuZGVmXCIsIFwidW5sZXNzXCIsIFwidW50aWxcIiwgXCJ3aGVuXCIsIFwid2hpbGVcIiwgXCJ5aWVsZFwiLCBcIm5pbFwiLCBcInJhaXNlXCIsIFwidGhyb3dcIiwgXCJjYXRjaFwiLCBcImZhaWxcIiwgXCJsb29wXCIsIFwiY2FsbGNjXCIsIFwiY2FsbGVyXCIsIFwibGFtYmRhXCIsIFwicHJvY1wiLCBcInB1YmxpY1wiLCBcInByb3RlY3RlZFwiLCBcInByaXZhdGVcIiwgXCJyZXF1aXJlXCIsIFwibG9hZFwiLCBcInJlcXVpcmVfcmVsYXRpdmVcIiwgXCJleHRlbmRcIiwgXCJhdXRvbG9hZFwiLCBcIl9fRU5EX19cIiwgXCJfX0ZJTEVfX1wiLCBcIl9fTElORV9fXCIsIFwiX19kaXJfX1wiXSxcbiAga2V5d29yZHMgPSB3b3JkT2JqKGtleXdvcmRMaXN0KTtcbnZhciBpbmRlbnRXb3JkcyA9IHdvcmRPYmooW1wiZGVmXCIsIFwiY2xhc3NcIiwgXCJjYXNlXCIsIFwiZm9yXCIsIFwid2hpbGVcIiwgXCJ1bnRpbFwiLCBcIm1vZHVsZVwiLCBcImNhdGNoXCIsIFwibG9vcFwiLCBcInByb2NcIiwgXCJiZWdpblwiXSk7XG52YXIgZGVkZW50V29yZHMgPSB3b3JkT2JqKFtcImVuZFwiLCBcInVudGlsXCJdKTtcbnZhciBvcGVuaW5nID0ge1xuICBcIltcIjogXCJdXCIsXG4gIFwie1wiOiBcIn1cIixcbiAgXCIoXCI6IFwiKVwiXG59O1xudmFyIGNsb3NpbmcgPSB7XG4gIFwiXVwiOiBcIltcIixcbiAgXCJ9XCI6IFwie1wiLFxuICBcIilcIjogXCIoXCJcbn07XG52YXIgY3VyUHVuYztcbmZ1bmN0aW9uIGNoYWluKG5ld3Rvaywgc3RyZWFtLCBzdGF0ZSkge1xuICBzdGF0ZS50b2tlbml6ZS5wdXNoKG5ld3Rvayk7XG4gIHJldHVybiBuZXd0b2soc3RyZWFtLCBzdGF0ZSk7XG59XG5mdW5jdGlvbiB0b2tlbkJhc2Uoc3RyZWFtLCBzdGF0ZSkge1xuICBpZiAoc3RyZWFtLnNvbCgpICYmIHN0cmVhbS5tYXRjaChcIj1iZWdpblwiKSAmJiBzdHJlYW0uZW9sKCkpIHtcbiAgICBzdGF0ZS50b2tlbml6ZS5wdXNoKHJlYWRCbG9ja0NvbW1lbnQpO1xuICAgIHJldHVybiBcImNvbW1lbnRcIjtcbiAgfVxuICBpZiAoc3RyZWFtLmVhdFNwYWNlKCkpIHJldHVybiBudWxsO1xuICB2YXIgY2ggPSBzdHJlYW0ubmV4dCgpLFxuICAgIG07XG4gIGlmIChjaCA9PSBcImBcIiB8fCBjaCA9PSBcIidcIiB8fCBjaCA9PSAnXCInKSB7XG4gICAgcmV0dXJuIGNoYWluKHJlYWRRdW90ZWQoY2gsIFwic3RyaW5nXCIsIGNoID09ICdcIicgfHwgY2ggPT0gXCJgXCIpLCBzdHJlYW0sIHN0YXRlKTtcbiAgfSBlbHNlIGlmIChjaCA9PSBcIi9cIikge1xuICAgIGlmIChyZWdleHBBaGVhZChzdHJlYW0pKSByZXR1cm4gY2hhaW4ocmVhZFF1b3RlZChjaCwgXCJzdHJpbmcuc3BlY2lhbFwiLCB0cnVlKSwgc3RyZWFtLCBzdGF0ZSk7ZWxzZSByZXR1cm4gXCJvcGVyYXRvclwiO1xuICB9IGVsc2UgaWYgKGNoID09IFwiJVwiKSB7XG4gICAgdmFyIHN0eWxlID0gXCJzdHJpbmdcIixcbiAgICAgIGVtYmVkID0gdHJ1ZTtcbiAgICBpZiAoc3RyZWFtLmVhdChcInNcIikpIHN0eWxlID0gXCJhdG9tXCI7ZWxzZSBpZiAoc3RyZWFtLmVhdCgvW1dRXS8pKSBzdHlsZSA9IFwic3RyaW5nXCI7ZWxzZSBpZiAoc3RyZWFtLmVhdCgvW3JdLykpIHN0eWxlID0gXCJzdHJpbmcuc3BlY2lhbFwiO2Vsc2UgaWYgKHN0cmVhbS5lYXQoL1t3eHFdLykpIHtcbiAgICAgIHN0eWxlID0gXCJzdHJpbmdcIjtcbiAgICAgIGVtYmVkID0gZmFsc2U7XG4gICAgfVxuICAgIHZhciBkZWxpbSA9IHN0cmVhbS5lYXQoL1teXFx3XFxzPV0vKTtcbiAgICBpZiAoIWRlbGltKSByZXR1cm4gXCJvcGVyYXRvclwiO1xuICAgIGlmIChvcGVuaW5nLnByb3BlcnR5SXNFbnVtZXJhYmxlKGRlbGltKSkgZGVsaW0gPSBvcGVuaW5nW2RlbGltXTtcbiAgICByZXR1cm4gY2hhaW4ocmVhZFF1b3RlZChkZWxpbSwgc3R5bGUsIGVtYmVkLCB0cnVlKSwgc3RyZWFtLCBzdGF0ZSk7XG4gIH0gZWxzZSBpZiAoY2ggPT0gXCIjXCIpIHtcbiAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICB9IGVsc2UgaWYgKGNoID09IFwiPFwiICYmIChtID0gc3RyZWFtLm1hdGNoKC9ePChbLX5dKVtcXGBcXFwiXFwnXT8oW2EtekEtWl8/XVxcdyopW1xcYFxcXCJcXCddPyg/Ojt8JCkvKSkpIHtcbiAgICByZXR1cm4gY2hhaW4ocmVhZEhlcmVEb2MobVsyXSwgbVsxXSksIHN0cmVhbSwgc3RhdGUpO1xuICB9IGVsc2UgaWYgKGNoID09IFwiMFwiKSB7XG4gICAgaWYgKHN0cmVhbS5lYXQoXCJ4XCIpKSBzdHJlYW0uZWF0V2hpbGUoL1tcXGRhLWZBLUZdLyk7ZWxzZSBpZiAoc3RyZWFtLmVhdChcImJcIikpIHN0cmVhbS5lYXRXaGlsZSgvWzAxXS8pO2Vsc2Ugc3RyZWFtLmVhdFdoaWxlKC9bMC03XS8pO1xuICAgIHJldHVybiBcIm51bWJlclwiO1xuICB9IGVsc2UgaWYgKC9cXGQvLnRlc3QoY2gpKSB7XG4gICAgc3RyZWFtLm1hdGNoKC9eW1xcZF9dKig/OlxcLltcXGRfXSspPyg/OltlRV1bK1xcLV0/W1xcZF9dKyk/Lyk7XG4gICAgcmV0dXJuIFwibnVtYmVyXCI7XG4gIH0gZWxzZSBpZiAoY2ggPT0gXCI/XCIpIHtcbiAgICB3aGlsZSAoc3RyZWFtLm1hdGNoKC9eXFxcXFtDTV0tLykpIHt9XG4gICAgaWYgKHN0cmVhbS5lYXQoXCJcXFxcXCIpKSBzdHJlYW0uZWF0V2hpbGUoL1xcdy8pO2Vsc2Ugc3RyZWFtLm5leHQoKTtcbiAgICByZXR1cm4gXCJzdHJpbmdcIjtcbiAgfSBlbHNlIGlmIChjaCA9PSBcIjpcIikge1xuICAgIGlmIChzdHJlYW0uZWF0KFwiJ1wiKSkgcmV0dXJuIGNoYWluKHJlYWRRdW90ZWQoXCInXCIsIFwiYXRvbVwiLCBmYWxzZSksIHN0cmVhbSwgc3RhdGUpO1xuICAgIGlmIChzdHJlYW0uZWF0KCdcIicpKSByZXR1cm4gY2hhaW4ocmVhZFF1b3RlZCgnXCInLCBcImF0b21cIiwgdHJ1ZSksIHN0cmVhbSwgc3RhdGUpO1xuXG4gICAgLy8gOj4gOj4+IDo8IDo8PCBhcmUgdmFsaWQgc3ltYm9sc1xuICAgIGlmIChzdHJlYW0uZWF0KC9bXFw8XFw+XS8pKSB7XG4gICAgICBzdHJlYW0uZWF0KC9bXFw8XFw+XS8pO1xuICAgICAgcmV0dXJuIFwiYXRvbVwiO1xuICAgIH1cblxuICAgIC8vIDorIDotIDovIDoqIDp8IDomIDohIGFyZSB2YWxpZCBzeW1ib2xzXG4gICAgaWYgKHN0cmVhbS5lYXQoL1tcXCtcXC1cXCpcXC9cXCZcXHxcXDpcXCFdLykpIHtcbiAgICAgIHJldHVybiBcImF0b21cIjtcbiAgICB9XG5cbiAgICAvLyBTeW1ib2xzIGNhbid0IHN0YXJ0IGJ5IGEgZGlnaXRcbiAgICBpZiAoc3RyZWFtLmVhdCgvW2EtekEtWiRAX1xceGExLVxcdWZmZmZdLykpIHtcbiAgICAgIHN0cmVhbS5lYXRXaGlsZSgvW1xcdyRcXHhhMS1cXHVmZmZmXS8pO1xuICAgICAgLy8gT25seSBvbmUgPyAhID0gaXMgYWxsb3dlZCBhbmQgb25seSBhcyB0aGUgbGFzdCBjaGFyYWN0ZXJcbiAgICAgIHN0cmVhbS5lYXQoL1tcXD9cXCFcXD1dLyk7XG4gICAgICByZXR1cm4gXCJhdG9tXCI7XG4gICAgfVxuICAgIHJldHVybiBcIm9wZXJhdG9yXCI7XG4gIH0gZWxzZSBpZiAoY2ggPT0gXCJAXCIgJiYgc3RyZWFtLm1hdGNoKC9eQD9bYS16QS1aX1xceGExLVxcdWZmZmZdLykpIHtcbiAgICBzdHJlYW0uZWF0KFwiQFwiKTtcbiAgICBzdHJlYW0uZWF0V2hpbGUoL1tcXHdcXHhhMS1cXHVmZmZmXS8pO1xuICAgIHJldHVybiBcInByb3BlcnR5TmFtZVwiO1xuICB9IGVsc2UgaWYgKGNoID09IFwiJFwiKSB7XG4gICAgaWYgKHN0cmVhbS5lYXQoL1thLXpBLVpfXS8pKSB7XG4gICAgICBzdHJlYW0uZWF0V2hpbGUoL1tcXHddLyk7XG4gICAgfSBlbHNlIGlmIChzdHJlYW0uZWF0KC9cXGQvKSkge1xuICAgICAgc3RyZWFtLmVhdCgvXFxkLyk7XG4gICAgfSBlbHNlIHtcbiAgICAgIHN0cmVhbS5uZXh0KCk7IC8vIE11c3QgYmUgYSBzcGVjaWFsIGdsb2JhbCBsaWtlICQ6IG9yICQhXG4gICAgfVxuICAgIHJldHVybiBcInZhcmlhYmxlTmFtZS5zcGVjaWFsXCI7XG4gIH0gZWxzZSBpZiAoL1thLXpBLVpfXFx4YTEtXFx1ZmZmZl0vLnRlc3QoY2gpKSB7XG4gICAgc3RyZWFtLmVhdFdoaWxlKC9bXFx3XFx4YTEtXFx1ZmZmZl0vKTtcbiAgICBzdHJlYW0uZWF0KC9bXFw/XFwhXS8pO1xuICAgIGlmIChzdHJlYW0uZWF0KFwiOlwiKSkgcmV0dXJuIFwiYXRvbVwiO1xuICAgIHJldHVybiBcInZhcmlhYmxlXCI7XG4gIH0gZWxzZSBpZiAoY2ggPT0gXCJ8XCIgJiYgKHN0YXRlLnZhckxpc3QgfHwgc3RhdGUubGFzdFRvayA9PSBcIntcIiB8fCBzdGF0ZS5sYXN0VG9rID09IFwiZG9cIikpIHtcbiAgICBjdXJQdW5jID0gXCJ8XCI7XG4gICAgcmV0dXJuIG51bGw7XG4gIH0gZWxzZSBpZiAoL1tcXChcXClcXFtcXF17fVxcXFw7XS8udGVzdChjaCkpIHtcbiAgICBjdXJQdW5jID0gY2g7XG4gICAgcmV0dXJuIG51bGw7XG4gIH0gZWxzZSBpZiAoY2ggPT0gXCItXCIgJiYgc3RyZWFtLmVhdChcIj5cIikpIHtcbiAgICByZXR1cm4gXCJvcGVyYXRvclwiO1xuICB9IGVsc2UgaWYgKC9bPStcXC1cXC8qOlxcLl4lPD5+fF0vLnRlc3QoY2gpKSB7XG4gICAgdmFyIG1vcmUgPSBzdHJlYW0uZWF0V2hpbGUoL1s9K1xcLVxcLyo6XFwuXiU8Pn58XS8pO1xuICAgIGlmIChjaCA9PSBcIi5cIiAmJiAhbW9yZSkgY3VyUHVuYyA9IFwiLlwiO1xuICAgIHJldHVybiBcIm9wZXJhdG9yXCI7XG4gIH0gZWxzZSB7XG4gICAgcmV0dXJuIG51bGw7XG4gIH1cbn1cbmZ1bmN0aW9uIHJlZ2V4cEFoZWFkKHN0cmVhbSkge1xuICB2YXIgc3RhcnQgPSBzdHJlYW0ucG9zLFxuICAgIGRlcHRoID0gMCxcbiAgICBuZXh0LFxuICAgIGZvdW5kID0gZmFsc2UsXG4gICAgZXNjYXBlZCA9IGZhbHNlO1xuICB3aGlsZSAoKG5leHQgPSBzdHJlYW0ubmV4dCgpKSAhPSBudWxsKSB7XG4gICAgaWYgKCFlc2NhcGVkKSB7XG4gICAgICBpZiAoXCJbeyhcIi5pbmRleE9mKG5leHQpID4gLTEpIHtcbiAgICAgICAgZGVwdGgrKztcbiAgICAgIH0gZWxzZSBpZiAoXCJdfSlcIi5pbmRleE9mKG5leHQpID4gLTEpIHtcbiAgICAgICAgZGVwdGgtLTtcbiAgICAgICAgaWYgKGRlcHRoIDwgMCkgYnJlYWs7XG4gICAgICB9IGVsc2UgaWYgKG5leHQgPT0gXCIvXCIgJiYgZGVwdGggPT0gMCkge1xuICAgICAgICBmb3VuZCA9IHRydWU7XG4gICAgICAgIGJyZWFrO1xuICAgICAgfVxuICAgICAgZXNjYXBlZCA9IG5leHQgPT0gXCJcXFxcXCI7XG4gICAgfSBlbHNlIHtcbiAgICAgIGVzY2FwZWQgPSBmYWxzZTtcbiAgICB9XG4gIH1cbiAgc3RyZWFtLmJhY2tVcChzdHJlYW0ucG9zIC0gc3RhcnQpO1xuICByZXR1cm4gZm91bmQ7XG59XG5mdW5jdGlvbiB0b2tlbkJhc2VVbnRpbEJyYWNlKGRlcHRoKSB7XG4gIGlmICghZGVwdGgpIGRlcHRoID0gMTtcbiAgcmV0dXJuIGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgaWYgKHN0cmVhbS5wZWVrKCkgPT0gXCJ9XCIpIHtcbiAgICAgIGlmIChkZXB0aCA9PSAxKSB7XG4gICAgICAgIHN0YXRlLnRva2VuaXplLnBvcCgpO1xuICAgICAgICByZXR1cm4gc3RhdGUudG9rZW5pemVbc3RhdGUudG9rZW5pemUubGVuZ3RoIC0gMV0oc3RyZWFtLCBzdGF0ZSk7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBzdGF0ZS50b2tlbml6ZVtzdGF0ZS50b2tlbml6ZS5sZW5ndGggLSAxXSA9IHRva2VuQmFzZVVudGlsQnJhY2UoZGVwdGggLSAxKTtcbiAgICAgIH1cbiAgICB9IGVsc2UgaWYgKHN0cmVhbS5wZWVrKCkgPT0gXCJ7XCIpIHtcbiAgICAgIHN0YXRlLnRva2VuaXplW3N0YXRlLnRva2VuaXplLmxlbmd0aCAtIDFdID0gdG9rZW5CYXNlVW50aWxCcmFjZShkZXB0aCArIDEpO1xuICAgIH1cbiAgICByZXR1cm4gdG9rZW5CYXNlKHN0cmVhbSwgc3RhdGUpO1xuICB9O1xufVxuZnVuY3Rpb24gdG9rZW5CYXNlT25jZSgpIHtcbiAgdmFyIGFscmVhZHlDYWxsZWQgPSBmYWxzZTtcbiAgcmV0dXJuIGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgaWYgKGFscmVhZHlDYWxsZWQpIHtcbiAgICAgIHN0YXRlLnRva2VuaXplLnBvcCgpO1xuICAgICAgcmV0dXJuIHN0YXRlLnRva2VuaXplW3N0YXRlLnRva2VuaXplLmxlbmd0aCAtIDFdKHN0cmVhbSwgc3RhdGUpO1xuICAgIH1cbiAgICBhbHJlYWR5Q2FsbGVkID0gdHJ1ZTtcbiAgICByZXR1cm4gdG9rZW5CYXNlKHN0cmVhbSwgc3RhdGUpO1xuICB9O1xufVxuZnVuY3Rpb24gcmVhZFF1b3RlZChxdW90ZSwgc3R5bGUsIGVtYmVkLCB1bmVzY2FwZWQpIHtcbiAgcmV0dXJuIGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgdmFyIGVzY2FwZWQgPSBmYWxzZSxcbiAgICAgIGNoO1xuICAgIGlmIChzdGF0ZS5jb250ZXh0LnR5cGUgPT09ICdyZWFkLXF1b3RlZC1wYXVzZWQnKSB7XG4gICAgICBzdGF0ZS5jb250ZXh0ID0gc3RhdGUuY29udGV4dC5wcmV2O1xuICAgICAgc3RyZWFtLmVhdChcIn1cIik7XG4gICAgfVxuICAgIHdoaWxlICgoY2ggPSBzdHJlYW0ubmV4dCgpKSAhPSBudWxsKSB7XG4gICAgICBpZiAoY2ggPT0gcXVvdGUgJiYgKHVuZXNjYXBlZCB8fCAhZXNjYXBlZCkpIHtcbiAgICAgICAgc3RhdGUudG9rZW5pemUucG9wKCk7XG4gICAgICAgIGJyZWFrO1xuICAgICAgfVxuICAgICAgaWYgKGVtYmVkICYmIGNoID09IFwiI1wiICYmICFlc2NhcGVkKSB7XG4gICAgICAgIGlmIChzdHJlYW0uZWF0KFwie1wiKSkge1xuICAgICAgICAgIGlmIChxdW90ZSA9PSBcIn1cIikge1xuICAgICAgICAgICAgc3RhdGUuY29udGV4dCA9IHtcbiAgICAgICAgICAgICAgcHJldjogc3RhdGUuY29udGV4dCxcbiAgICAgICAgICAgICAgdHlwZTogJ3JlYWQtcXVvdGVkLXBhdXNlZCdcbiAgICAgICAgICAgIH07XG4gICAgICAgICAgfVxuICAgICAgICAgIHN0YXRlLnRva2VuaXplLnB1c2godG9rZW5CYXNlVW50aWxCcmFjZSgpKTtcbiAgICAgICAgICBicmVhaztcbiAgICAgICAgfSBlbHNlIGlmICgvW0BcXCRdLy50ZXN0KHN0cmVhbS5wZWVrKCkpKSB7XG4gICAgICAgICAgc3RhdGUudG9rZW5pemUucHVzaCh0b2tlbkJhc2VPbmNlKCkpO1xuICAgICAgICAgIGJyZWFrO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgICBlc2NhcGVkID0gIWVzY2FwZWQgJiYgY2ggPT0gXCJcXFxcXCI7XG4gICAgfVxuICAgIHJldHVybiBzdHlsZTtcbiAgfTtcbn1cbmZ1bmN0aW9uIHJlYWRIZXJlRG9jKHBocmFzZSwgbWF5SW5kZW50KSB7XG4gIHJldHVybiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIGlmIChtYXlJbmRlbnQpIHN0cmVhbS5lYXRTcGFjZSgpO1xuICAgIGlmIChzdHJlYW0ubWF0Y2gocGhyYXNlKSkgc3RhdGUudG9rZW5pemUucG9wKCk7ZWxzZSBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgcmV0dXJuIFwic3RyaW5nXCI7XG4gIH07XG59XG5mdW5jdGlvbiByZWFkQmxvY2tDb21tZW50KHN0cmVhbSwgc3RhdGUpIHtcbiAgaWYgKHN0cmVhbS5zb2woKSAmJiBzdHJlYW0ubWF0Y2goXCI9ZW5kXCIpICYmIHN0cmVhbS5lb2woKSkgc3RhdGUudG9rZW5pemUucG9wKCk7XG4gIHN0cmVhbS5za2lwVG9FbmQoKTtcbiAgcmV0dXJuIFwiY29tbWVudFwiO1xufVxuZXhwb3J0IGNvbnN0IHJ1YnkgPSB7XG4gIG5hbWU6IFwicnVieVwiLFxuICBzdGFydFN0YXRlOiBmdW5jdGlvbiAoaW5kZW50VW5pdCkge1xuICAgIHJldHVybiB7XG4gICAgICB0b2tlbml6ZTogW3Rva2VuQmFzZV0sXG4gICAgICBpbmRlbnRlZDogMCxcbiAgICAgIGNvbnRleHQ6IHtcbiAgICAgICAgdHlwZTogXCJ0b3BcIixcbiAgICAgICAgaW5kZW50ZWQ6IC1pbmRlbnRVbml0XG4gICAgICB9LFxuICAgICAgY29udGludWVkTGluZTogZmFsc2UsXG4gICAgICBsYXN0VG9rOiBudWxsLFxuICAgICAgdmFyTGlzdDogZmFsc2VcbiAgICB9O1xuICB9LFxuICB0b2tlbjogZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICBjdXJQdW5jID0gbnVsbDtcbiAgICBpZiAoc3RyZWFtLnNvbCgpKSBzdGF0ZS5pbmRlbnRlZCA9IHN0cmVhbS5pbmRlbnRhdGlvbigpO1xuICAgIHZhciBzdHlsZSA9IHN0YXRlLnRva2VuaXplW3N0YXRlLnRva2VuaXplLmxlbmd0aCAtIDFdKHN0cmVhbSwgc3RhdGUpLFxuICAgICAga3d0eXBlO1xuICAgIHZhciB0aGlzVG9rID0gY3VyUHVuYztcbiAgICBpZiAoc3R5bGUgPT0gXCJ2YXJpYWJsZVwiKSB7XG4gICAgICB2YXIgd29yZCA9IHN0cmVhbS5jdXJyZW50KCk7XG4gICAgICBzdHlsZSA9IHN0YXRlLmxhc3RUb2sgPT0gXCIuXCIgPyBcInByb3BlcnR5XCIgOiBrZXl3b3Jkcy5wcm9wZXJ0eUlzRW51bWVyYWJsZShzdHJlYW0uY3VycmVudCgpKSA/IFwia2V5d29yZFwiIDogL15bQS1aXS8udGVzdCh3b3JkKSA/IFwidGFnXCIgOiBzdGF0ZS5sYXN0VG9rID09IFwiZGVmXCIgfHwgc3RhdGUubGFzdFRvayA9PSBcImNsYXNzXCIgfHwgc3RhdGUudmFyTGlzdCA/IFwiZGVmXCIgOiBcInZhcmlhYmxlXCI7XG4gICAgICBpZiAoc3R5bGUgPT0gXCJrZXl3b3JkXCIpIHtcbiAgICAgICAgdGhpc1RvayA9IHdvcmQ7XG4gICAgICAgIGlmIChpbmRlbnRXb3Jkcy5wcm9wZXJ0eUlzRW51bWVyYWJsZSh3b3JkKSkga3d0eXBlID0gXCJpbmRlbnRcIjtlbHNlIGlmIChkZWRlbnRXb3Jkcy5wcm9wZXJ0eUlzRW51bWVyYWJsZSh3b3JkKSkga3d0eXBlID0gXCJkZWRlbnRcIjtlbHNlIGlmICgod29yZCA9PSBcImlmXCIgfHwgd29yZCA9PSBcInVubGVzc1wiKSAmJiBzdHJlYW0uY29sdW1uKCkgPT0gc3RyZWFtLmluZGVudGF0aW9uKCkpIGt3dHlwZSA9IFwiaW5kZW50XCI7ZWxzZSBpZiAod29yZCA9PSBcImRvXCIgJiYgc3RhdGUuY29udGV4dC5pbmRlbnRlZCA8IHN0YXRlLmluZGVudGVkKSBrd3R5cGUgPSBcImluZGVudFwiO1xuICAgICAgfVxuICAgIH1cbiAgICBpZiAoY3VyUHVuYyB8fCBzdHlsZSAmJiBzdHlsZSAhPSBcImNvbW1lbnRcIikgc3RhdGUubGFzdFRvayA9IHRoaXNUb2s7XG4gICAgaWYgKGN1clB1bmMgPT0gXCJ8XCIpIHN0YXRlLnZhckxpc3QgPSAhc3RhdGUudmFyTGlzdDtcbiAgICBpZiAoa3d0eXBlID09IFwiaW5kZW50XCIgfHwgL1tcXChcXFtcXHtdLy50ZXN0KGN1clB1bmMpKSBzdGF0ZS5jb250ZXh0ID0ge1xuICAgICAgcHJldjogc3RhdGUuY29udGV4dCxcbiAgICAgIHR5cGU6IGN1clB1bmMgfHwgc3R5bGUsXG4gICAgICBpbmRlbnRlZDogc3RhdGUuaW5kZW50ZWRcbiAgICB9O2Vsc2UgaWYgKChrd3R5cGUgPT0gXCJkZWRlbnRcIiB8fCAvW1xcKVxcXVxcfV0vLnRlc3QoY3VyUHVuYykpICYmIHN0YXRlLmNvbnRleHQucHJldikgc3RhdGUuY29udGV4dCA9IHN0YXRlLmNvbnRleHQucHJldjtcbiAgICBpZiAoc3RyZWFtLmVvbCgpKSBzdGF0ZS5jb250aW51ZWRMaW5lID0gY3VyUHVuYyA9PSBcIlxcXFxcIiB8fCBzdHlsZSA9PSBcIm9wZXJhdG9yXCI7XG4gICAgcmV0dXJuIHN0eWxlO1xuICB9LFxuICBpbmRlbnQ6IGZ1bmN0aW9uIChzdGF0ZSwgdGV4dEFmdGVyLCBjeCkge1xuICAgIGlmIChzdGF0ZS50b2tlbml6ZVtzdGF0ZS50b2tlbml6ZS5sZW5ndGggLSAxXSAhPSB0b2tlbkJhc2UpIHJldHVybiBudWxsO1xuICAgIHZhciBmaXJzdENoYXIgPSB0ZXh0QWZ0ZXIgJiYgdGV4dEFmdGVyLmNoYXJBdCgwKTtcbiAgICB2YXIgY3QgPSBzdGF0ZS5jb250ZXh0O1xuICAgIHZhciBjbG9zZWQgPSBjdC50eXBlID09IGNsb3NpbmdbZmlyc3RDaGFyXSB8fCBjdC50eXBlID09IFwia2V5d29yZFwiICYmIC9eKD86ZW5kfHVudGlsfGVsc2V8ZWxzaWZ8d2hlbnxyZXNjdWUpXFxiLy50ZXN0KHRleHRBZnRlcik7XG4gICAgcmV0dXJuIGN0LmluZGVudGVkICsgKGNsb3NlZCA/IDAgOiBjeC51bml0KSArIChzdGF0ZS5jb250aW51ZWRMaW5lID8gY3gudW5pdCA6IDApO1xuICB9LFxuICBsYW5ndWFnZURhdGE6IHtcbiAgICBpbmRlbnRPbklucHV0OiAvXlxccyooPzplbmR8cmVzY3VlfGVsc2lmfGVsc2V8XFx9KSQvLFxuICAgIGNvbW1lbnRUb2tlbnM6IHtcbiAgICAgIGxpbmU6IFwiI1wiXG4gICAgfSxcbiAgICBhdXRvY29tcGxldGU6IGtleXdvcmRMaXN0XG4gIH1cbn07Il0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9