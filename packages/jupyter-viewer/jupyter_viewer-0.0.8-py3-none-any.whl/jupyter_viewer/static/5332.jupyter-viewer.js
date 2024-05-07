"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[5332],{

/***/ 5332:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "tiki": () => (/* binding */ tiki)
/* harmony export */ });
function inBlock(style, terminator, returnTokenizer) {
  return function (stream, state) {
    while (!stream.eol()) {
      if (stream.match(terminator)) {
        state.tokenize = inText;
        break;
      }
      stream.next();
    }
    if (returnTokenizer) state.tokenize = returnTokenizer;
    return style;
  };
}
function inLine(style) {
  return function (stream, state) {
    while (!stream.eol()) {
      stream.next();
    }
    state.tokenize = inText;
    return style;
  };
}
function inText(stream, state) {
  function chain(parser) {
    state.tokenize = parser;
    return parser(stream, state);
  }
  var sol = stream.sol();
  var ch = stream.next();

  //non start of line
  switch (ch) {
    //switch is generally much faster than if, so it is used here
    case "{":
      //plugin
      stream.eat("/");
      stream.eatSpace();
      stream.eatWhile(/[^\s\u00a0=\"\'\/?(}]/);
      state.tokenize = inPlugin;
      return "tag";
    case "_":
      //bold
      if (stream.eat("_")) return chain(inBlock("strong", "__", inText));
      break;
    case "'":
      //italics
      if (stream.eat("'")) return chain(inBlock("em", "''", inText));
      break;
    case "(":
      // Wiki Link
      if (stream.eat("(")) return chain(inBlock("link", "))", inText));
      break;
    case "[":
      // Weblink
      return chain(inBlock("url", "]", inText));
      break;
    case "|":
      //table
      if (stream.eat("|")) return chain(inBlock("comment", "||"));
      break;
    case "-":
      if (stream.eat("=")) {
        //titleBar
        return chain(inBlock("header string", "=-", inText));
      } else if (stream.eat("-")) {
        //deleted
        return chain(inBlock("error tw-deleted", "--", inText));
      }
      break;
    case "=":
      //underline
      if (stream.match("==")) return chain(inBlock("tw-underline", "===", inText));
      break;
    case ":":
      if (stream.eat(":")) return chain(inBlock("comment", "::"));
      break;
    case "^":
      //box
      return chain(inBlock("tw-box", "^"));
      break;
    case "~":
      //np
      if (stream.match("np~")) return chain(inBlock("meta", "~/np~"));
      break;
  }

  //start of line types
  if (sol) {
    switch (ch) {
      case "!":
        //header at start of line
        if (stream.match('!!!!!')) {
          return chain(inLine("header string"));
        } else if (stream.match('!!!!')) {
          return chain(inLine("header string"));
        } else if (stream.match('!!!')) {
          return chain(inLine("header string"));
        } else if (stream.match('!!')) {
          return chain(inLine("header string"));
        } else {
          return chain(inLine("header string"));
        }
        break;
      case "*": //unordered list line item, or <li /> at start of line
      case "#": //ordered list line item, or <li /> at start of line
      case "+":
        //ordered list line item, or <li /> at start of line
        return chain(inLine("tw-listitem bracket"));
        break;
    }
  }

  //stream.eatWhile(/[&{]/); was eating up plugins, turned off to act less like html and more like tiki
  return null;
}

// Return variables for tokenizers
var pluginName, type;
function inPlugin(stream, state) {
  var ch = stream.next();
  var peek = stream.peek();
  if (ch == "}") {
    state.tokenize = inText;
    //type = ch == ")" ? "endPlugin" : "selfclosePlugin"; inPlugin
    return "tag";
  } else if (ch == "(" || ch == ")") {
    return "bracket";
  } else if (ch == "=") {
    type = "equals";
    if (peek == ">") {
      stream.next();
      peek = stream.peek();
    }

    //here we detect values directly after equal character with no quotes
    if (!/[\'\"]/.test(peek)) {
      state.tokenize = inAttributeNoQuote();
    }
    //end detect values

    return "operator";
  } else if (/[\'\"]/.test(ch)) {
    state.tokenize = inAttribute(ch);
    return state.tokenize(stream, state);
  } else {
    stream.eatWhile(/[^\s\u00a0=\"\'\/?]/);
    return "keyword";
  }
}
function inAttribute(quote) {
  return function (stream, state) {
    while (!stream.eol()) {
      if (stream.next() == quote) {
        state.tokenize = inPlugin;
        break;
      }
    }
    return "string";
  };
}
function inAttributeNoQuote() {
  return function (stream, state) {
    while (!stream.eol()) {
      var ch = stream.next();
      var peek = stream.peek();
      if (ch == " " || ch == "," || /[ )}]/.test(peek)) {
        state.tokenize = inPlugin;
        break;
      }
    }
    return "string";
  };
}
var curState, setStyle;
function pass() {
  for (var i = arguments.length - 1; i >= 0; i--) curState.cc.push(arguments[i]);
}
function cont() {
  pass.apply(null, arguments);
  return true;
}
function pushContext(pluginName, startOfLine) {
  var noIndent = curState.context && curState.context.noIndent;
  curState.context = {
    prev: curState.context,
    pluginName: pluginName,
    indent: curState.indented,
    startOfLine: startOfLine,
    noIndent: noIndent
  };
}
function popContext() {
  if (curState.context) curState.context = curState.context.prev;
}
function element(type) {
  if (type == "openPlugin") {
    curState.pluginName = pluginName;
    return cont(attributes, endplugin(curState.startOfLine));
  } else if (type == "closePlugin") {
    var err = false;
    if (curState.context) {
      err = curState.context.pluginName != pluginName;
      popContext();
    } else {
      err = true;
    }
    if (err) setStyle = "error";
    return cont(endcloseplugin(err));
  } else if (type == "string") {
    if (!curState.context || curState.context.name != "!cdata") pushContext("!cdata");
    if (curState.tokenize == inText) popContext();
    return cont();
  } else return cont();
}
function endplugin(startOfLine) {
  return function (type) {
    if (type == "selfclosePlugin" || type == "endPlugin") return cont();
    if (type == "endPlugin") {
      pushContext(curState.pluginName, startOfLine);
      return cont();
    }
    return cont();
  };
}
function endcloseplugin(err) {
  return function (type) {
    if (err) setStyle = "error";
    if (type == "endPlugin") return cont();
    return pass();
  };
}
function attributes(type) {
  if (type == "keyword") {
    setStyle = "attribute";
    return cont(attributes);
  }
  if (type == "equals") return cont(attvalue, attributes);
  return pass();
}
function attvalue(type) {
  if (type == "keyword") {
    setStyle = "string";
    return cont();
  }
  if (type == "string") return cont(attvaluemaybe);
  return pass();
}
function attvaluemaybe(type) {
  if (type == "string") return cont(attvaluemaybe);else return pass();
}
const tiki = {
  name: "tiki",
  startState: function () {
    return {
      tokenize: inText,
      cc: [],
      indented: 0,
      startOfLine: true,
      pluginName: null,
      context: null
    };
  },
  token: function (stream, state) {
    if (stream.sol()) {
      state.startOfLine = true;
      state.indented = stream.indentation();
    }
    if (stream.eatSpace()) return null;
    setStyle = type = pluginName = null;
    var style = state.tokenize(stream, state);
    if ((style || type) && style != "comment") {
      curState = state;
      while (true) {
        var comb = state.cc.pop() || element;
        if (comb(type || style)) break;
      }
    }
    state.startOfLine = false;
    return setStyle || style;
  },
  indent: function (state, textAfter, cx) {
    var context = state.context;
    if (context && context.noIndent) return 0;
    if (context && /^{\//.test(textAfter)) context = context.prev;
    while (context && !context.startOfLine) context = context.prev;
    if (context) return context.indent + cx.unit;else return 0;
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNTMzMi5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9AY29kZW1pcnJvci9sZWdhY3ktbW9kZXMvbW9kZS90aWtpLmpzIl0sInNvdXJjZXNDb250ZW50IjpbImZ1bmN0aW9uIGluQmxvY2soc3R5bGUsIHRlcm1pbmF0b3IsIHJldHVyblRva2VuaXplcikge1xuICByZXR1cm4gZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICB3aGlsZSAoIXN0cmVhbS5lb2woKSkge1xuICAgICAgaWYgKHN0cmVhbS5tYXRjaCh0ZXJtaW5hdG9yKSkge1xuICAgICAgICBzdGF0ZS50b2tlbml6ZSA9IGluVGV4dDtcbiAgICAgICAgYnJlYWs7XG4gICAgICB9XG4gICAgICBzdHJlYW0ubmV4dCgpO1xuICAgIH1cbiAgICBpZiAocmV0dXJuVG9rZW5pemVyKSBzdGF0ZS50b2tlbml6ZSA9IHJldHVyblRva2VuaXplcjtcbiAgICByZXR1cm4gc3R5bGU7XG4gIH07XG59XG5mdW5jdGlvbiBpbkxpbmUoc3R5bGUpIHtcbiAgcmV0dXJuIGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgd2hpbGUgKCFzdHJlYW0uZW9sKCkpIHtcbiAgICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgfVxuICAgIHN0YXRlLnRva2VuaXplID0gaW5UZXh0O1xuICAgIHJldHVybiBzdHlsZTtcbiAgfTtcbn1cbmZ1bmN0aW9uIGluVGV4dChzdHJlYW0sIHN0YXRlKSB7XG4gIGZ1bmN0aW9uIGNoYWluKHBhcnNlcikge1xuICAgIHN0YXRlLnRva2VuaXplID0gcGFyc2VyO1xuICAgIHJldHVybiBwYXJzZXIoc3RyZWFtLCBzdGF0ZSk7XG4gIH1cbiAgdmFyIHNvbCA9IHN0cmVhbS5zb2woKTtcbiAgdmFyIGNoID0gc3RyZWFtLm5leHQoKTtcblxuICAvL25vbiBzdGFydCBvZiBsaW5lXG4gIHN3aXRjaCAoY2gpIHtcbiAgICAvL3N3aXRjaCBpcyBnZW5lcmFsbHkgbXVjaCBmYXN0ZXIgdGhhbiBpZiwgc28gaXQgaXMgdXNlZCBoZXJlXG4gICAgY2FzZSBcIntcIjpcbiAgICAgIC8vcGx1Z2luXG4gICAgICBzdHJlYW0uZWF0KFwiL1wiKTtcbiAgICAgIHN0cmVhbS5lYXRTcGFjZSgpO1xuICAgICAgc3RyZWFtLmVhdFdoaWxlKC9bXlxcc1xcdTAwYTA9XFxcIlxcJ1xcLz8ofV0vKTtcbiAgICAgIHN0YXRlLnRva2VuaXplID0gaW5QbHVnaW47XG4gICAgICByZXR1cm4gXCJ0YWdcIjtcbiAgICBjYXNlIFwiX1wiOlxuICAgICAgLy9ib2xkXG4gICAgICBpZiAoc3RyZWFtLmVhdChcIl9cIikpIHJldHVybiBjaGFpbihpbkJsb2NrKFwic3Ryb25nXCIsIFwiX19cIiwgaW5UZXh0KSk7XG4gICAgICBicmVhaztcbiAgICBjYXNlIFwiJ1wiOlxuICAgICAgLy9pdGFsaWNzXG4gICAgICBpZiAoc3RyZWFtLmVhdChcIidcIikpIHJldHVybiBjaGFpbihpbkJsb2NrKFwiZW1cIiwgXCInJ1wiLCBpblRleHQpKTtcbiAgICAgIGJyZWFrO1xuICAgIGNhc2UgXCIoXCI6XG4gICAgICAvLyBXaWtpIExpbmtcbiAgICAgIGlmIChzdHJlYW0uZWF0KFwiKFwiKSkgcmV0dXJuIGNoYWluKGluQmxvY2soXCJsaW5rXCIsIFwiKSlcIiwgaW5UZXh0KSk7XG4gICAgICBicmVhaztcbiAgICBjYXNlIFwiW1wiOlxuICAgICAgLy8gV2VibGlua1xuICAgICAgcmV0dXJuIGNoYWluKGluQmxvY2soXCJ1cmxcIiwgXCJdXCIsIGluVGV4dCkpO1xuICAgICAgYnJlYWs7XG4gICAgY2FzZSBcInxcIjpcbiAgICAgIC8vdGFibGVcbiAgICAgIGlmIChzdHJlYW0uZWF0KFwifFwiKSkgcmV0dXJuIGNoYWluKGluQmxvY2soXCJjb21tZW50XCIsIFwifHxcIikpO1xuICAgICAgYnJlYWs7XG4gICAgY2FzZSBcIi1cIjpcbiAgICAgIGlmIChzdHJlYW0uZWF0KFwiPVwiKSkge1xuICAgICAgICAvL3RpdGxlQmFyXG4gICAgICAgIHJldHVybiBjaGFpbihpbkJsb2NrKFwiaGVhZGVyIHN0cmluZ1wiLCBcIj0tXCIsIGluVGV4dCkpO1xuICAgICAgfSBlbHNlIGlmIChzdHJlYW0uZWF0KFwiLVwiKSkge1xuICAgICAgICAvL2RlbGV0ZWRcbiAgICAgICAgcmV0dXJuIGNoYWluKGluQmxvY2soXCJlcnJvciB0dy1kZWxldGVkXCIsIFwiLS1cIiwgaW5UZXh0KSk7XG4gICAgICB9XG4gICAgICBicmVhaztcbiAgICBjYXNlIFwiPVwiOlxuICAgICAgLy91bmRlcmxpbmVcbiAgICAgIGlmIChzdHJlYW0ubWF0Y2goXCI9PVwiKSkgcmV0dXJuIGNoYWluKGluQmxvY2soXCJ0dy11bmRlcmxpbmVcIiwgXCI9PT1cIiwgaW5UZXh0KSk7XG4gICAgICBicmVhaztcbiAgICBjYXNlIFwiOlwiOlxuICAgICAgaWYgKHN0cmVhbS5lYXQoXCI6XCIpKSByZXR1cm4gY2hhaW4oaW5CbG9jayhcImNvbW1lbnRcIiwgXCI6OlwiKSk7XG4gICAgICBicmVhaztcbiAgICBjYXNlIFwiXlwiOlxuICAgICAgLy9ib3hcbiAgICAgIHJldHVybiBjaGFpbihpbkJsb2NrKFwidHctYm94XCIsIFwiXlwiKSk7XG4gICAgICBicmVhaztcbiAgICBjYXNlIFwiflwiOlxuICAgICAgLy9ucFxuICAgICAgaWYgKHN0cmVhbS5tYXRjaChcIm5wflwiKSkgcmV0dXJuIGNoYWluKGluQmxvY2soXCJtZXRhXCIsIFwifi9ucH5cIikpO1xuICAgICAgYnJlYWs7XG4gIH1cblxuICAvL3N0YXJ0IG9mIGxpbmUgdHlwZXNcbiAgaWYgKHNvbCkge1xuICAgIHN3aXRjaCAoY2gpIHtcbiAgICAgIGNhc2UgXCIhXCI6XG4gICAgICAgIC8vaGVhZGVyIGF0IHN0YXJ0IG9mIGxpbmVcbiAgICAgICAgaWYgKHN0cmVhbS5tYXRjaCgnISEhISEnKSkge1xuICAgICAgICAgIHJldHVybiBjaGFpbihpbkxpbmUoXCJoZWFkZXIgc3RyaW5nXCIpKTtcbiAgICAgICAgfSBlbHNlIGlmIChzdHJlYW0ubWF0Y2goJyEhISEnKSkge1xuICAgICAgICAgIHJldHVybiBjaGFpbihpbkxpbmUoXCJoZWFkZXIgc3RyaW5nXCIpKTtcbiAgICAgICAgfSBlbHNlIGlmIChzdHJlYW0ubWF0Y2goJyEhIScpKSB7XG4gICAgICAgICAgcmV0dXJuIGNoYWluKGluTGluZShcImhlYWRlciBzdHJpbmdcIikpO1xuICAgICAgICB9IGVsc2UgaWYgKHN0cmVhbS5tYXRjaCgnISEnKSkge1xuICAgICAgICAgIHJldHVybiBjaGFpbihpbkxpbmUoXCJoZWFkZXIgc3RyaW5nXCIpKTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICByZXR1cm4gY2hhaW4oaW5MaW5lKFwiaGVhZGVyIHN0cmluZ1wiKSk7XG4gICAgICAgIH1cbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlIFwiKlwiOiAvL3Vub3JkZXJlZCBsaXN0IGxpbmUgaXRlbSwgb3IgPGxpIC8+IGF0IHN0YXJ0IG9mIGxpbmVcbiAgICAgIGNhc2UgXCIjXCI6IC8vb3JkZXJlZCBsaXN0IGxpbmUgaXRlbSwgb3IgPGxpIC8+IGF0IHN0YXJ0IG9mIGxpbmVcbiAgICAgIGNhc2UgXCIrXCI6XG4gICAgICAgIC8vb3JkZXJlZCBsaXN0IGxpbmUgaXRlbSwgb3IgPGxpIC8+IGF0IHN0YXJ0IG9mIGxpbmVcbiAgICAgICAgcmV0dXJuIGNoYWluKGluTGluZShcInR3LWxpc3RpdGVtIGJyYWNrZXRcIikpO1xuICAgICAgICBicmVhaztcbiAgICB9XG4gIH1cblxuICAvL3N0cmVhbS5lYXRXaGlsZSgvWyZ7XS8pOyB3YXMgZWF0aW5nIHVwIHBsdWdpbnMsIHR1cm5lZCBvZmYgdG8gYWN0IGxlc3MgbGlrZSBodG1sIGFuZCBtb3JlIGxpa2UgdGlraVxuICByZXR1cm4gbnVsbDtcbn1cblxuLy8gUmV0dXJuIHZhcmlhYmxlcyBmb3IgdG9rZW5pemVyc1xudmFyIHBsdWdpbk5hbWUsIHR5cGU7XG5mdW5jdGlvbiBpblBsdWdpbihzdHJlYW0sIHN0YXRlKSB7XG4gIHZhciBjaCA9IHN0cmVhbS5uZXh0KCk7XG4gIHZhciBwZWVrID0gc3RyZWFtLnBlZWsoKTtcbiAgaWYgKGNoID09IFwifVwiKSB7XG4gICAgc3RhdGUudG9rZW5pemUgPSBpblRleHQ7XG4gICAgLy90eXBlID0gY2ggPT0gXCIpXCIgPyBcImVuZFBsdWdpblwiIDogXCJzZWxmY2xvc2VQbHVnaW5cIjsgaW5QbHVnaW5cbiAgICByZXR1cm4gXCJ0YWdcIjtcbiAgfSBlbHNlIGlmIChjaCA9PSBcIihcIiB8fCBjaCA9PSBcIilcIikge1xuICAgIHJldHVybiBcImJyYWNrZXRcIjtcbiAgfSBlbHNlIGlmIChjaCA9PSBcIj1cIikge1xuICAgIHR5cGUgPSBcImVxdWFsc1wiO1xuICAgIGlmIChwZWVrID09IFwiPlwiKSB7XG4gICAgICBzdHJlYW0ubmV4dCgpO1xuICAgICAgcGVlayA9IHN0cmVhbS5wZWVrKCk7XG4gICAgfVxuXG4gICAgLy9oZXJlIHdlIGRldGVjdCB2YWx1ZXMgZGlyZWN0bHkgYWZ0ZXIgZXF1YWwgY2hhcmFjdGVyIHdpdGggbm8gcXVvdGVzXG4gICAgaWYgKCEvW1xcJ1xcXCJdLy50ZXN0KHBlZWspKSB7XG4gICAgICBzdGF0ZS50b2tlbml6ZSA9IGluQXR0cmlidXRlTm9RdW90ZSgpO1xuICAgIH1cbiAgICAvL2VuZCBkZXRlY3QgdmFsdWVzXG5cbiAgICByZXR1cm4gXCJvcGVyYXRvclwiO1xuICB9IGVsc2UgaWYgKC9bXFwnXFxcIl0vLnRlc3QoY2gpKSB7XG4gICAgc3RhdGUudG9rZW5pemUgPSBpbkF0dHJpYnV0ZShjaCk7XG4gICAgcmV0dXJuIHN0YXRlLnRva2VuaXplKHN0cmVhbSwgc3RhdGUpO1xuICB9IGVsc2Uge1xuICAgIHN0cmVhbS5lYXRXaGlsZSgvW15cXHNcXHUwMGEwPVxcXCJcXCdcXC8/XS8pO1xuICAgIHJldHVybiBcImtleXdvcmRcIjtcbiAgfVxufVxuZnVuY3Rpb24gaW5BdHRyaWJ1dGUocXVvdGUpIHtcbiAgcmV0dXJuIGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgd2hpbGUgKCFzdHJlYW0uZW9sKCkpIHtcbiAgICAgIGlmIChzdHJlYW0ubmV4dCgpID09IHF1b3RlKSB7XG4gICAgICAgIHN0YXRlLnRva2VuaXplID0gaW5QbHVnaW47XG4gICAgICAgIGJyZWFrO1xuICAgICAgfVxuICAgIH1cbiAgICByZXR1cm4gXCJzdHJpbmdcIjtcbiAgfTtcbn1cbmZ1bmN0aW9uIGluQXR0cmlidXRlTm9RdW90ZSgpIHtcbiAgcmV0dXJuIGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgd2hpbGUgKCFzdHJlYW0uZW9sKCkpIHtcbiAgICAgIHZhciBjaCA9IHN0cmVhbS5uZXh0KCk7XG4gICAgICB2YXIgcGVlayA9IHN0cmVhbS5wZWVrKCk7XG4gICAgICBpZiAoY2ggPT0gXCIgXCIgfHwgY2ggPT0gXCIsXCIgfHwgL1sgKX1dLy50ZXN0KHBlZWspKSB7XG4gICAgICAgIHN0YXRlLnRva2VuaXplID0gaW5QbHVnaW47XG4gICAgICAgIGJyZWFrO1xuICAgICAgfVxuICAgIH1cbiAgICByZXR1cm4gXCJzdHJpbmdcIjtcbiAgfTtcbn1cbnZhciBjdXJTdGF0ZSwgc2V0U3R5bGU7XG5mdW5jdGlvbiBwYXNzKCkge1xuICBmb3IgKHZhciBpID0gYXJndW1lbnRzLmxlbmd0aCAtIDE7IGkgPj0gMDsgaS0tKSBjdXJTdGF0ZS5jYy5wdXNoKGFyZ3VtZW50c1tpXSk7XG59XG5mdW5jdGlvbiBjb250KCkge1xuICBwYXNzLmFwcGx5KG51bGwsIGFyZ3VtZW50cyk7XG4gIHJldHVybiB0cnVlO1xufVxuZnVuY3Rpb24gcHVzaENvbnRleHQocGx1Z2luTmFtZSwgc3RhcnRPZkxpbmUpIHtcbiAgdmFyIG5vSW5kZW50ID0gY3VyU3RhdGUuY29udGV4dCAmJiBjdXJTdGF0ZS5jb250ZXh0Lm5vSW5kZW50O1xuICBjdXJTdGF0ZS5jb250ZXh0ID0ge1xuICAgIHByZXY6IGN1clN0YXRlLmNvbnRleHQsXG4gICAgcGx1Z2luTmFtZTogcGx1Z2luTmFtZSxcbiAgICBpbmRlbnQ6IGN1clN0YXRlLmluZGVudGVkLFxuICAgIHN0YXJ0T2ZMaW5lOiBzdGFydE9mTGluZSxcbiAgICBub0luZGVudDogbm9JbmRlbnRcbiAgfTtcbn1cbmZ1bmN0aW9uIHBvcENvbnRleHQoKSB7XG4gIGlmIChjdXJTdGF0ZS5jb250ZXh0KSBjdXJTdGF0ZS5jb250ZXh0ID0gY3VyU3RhdGUuY29udGV4dC5wcmV2O1xufVxuZnVuY3Rpb24gZWxlbWVudCh0eXBlKSB7XG4gIGlmICh0eXBlID09IFwib3BlblBsdWdpblwiKSB7XG4gICAgY3VyU3RhdGUucGx1Z2luTmFtZSA9IHBsdWdpbk5hbWU7XG4gICAgcmV0dXJuIGNvbnQoYXR0cmlidXRlcywgZW5kcGx1Z2luKGN1clN0YXRlLnN0YXJ0T2ZMaW5lKSk7XG4gIH0gZWxzZSBpZiAodHlwZSA9PSBcImNsb3NlUGx1Z2luXCIpIHtcbiAgICB2YXIgZXJyID0gZmFsc2U7XG4gICAgaWYgKGN1clN0YXRlLmNvbnRleHQpIHtcbiAgICAgIGVyciA9IGN1clN0YXRlLmNvbnRleHQucGx1Z2luTmFtZSAhPSBwbHVnaW5OYW1lO1xuICAgICAgcG9wQ29udGV4dCgpO1xuICAgIH0gZWxzZSB7XG4gICAgICBlcnIgPSB0cnVlO1xuICAgIH1cbiAgICBpZiAoZXJyKSBzZXRTdHlsZSA9IFwiZXJyb3JcIjtcbiAgICByZXR1cm4gY29udChlbmRjbG9zZXBsdWdpbihlcnIpKTtcbiAgfSBlbHNlIGlmICh0eXBlID09IFwic3RyaW5nXCIpIHtcbiAgICBpZiAoIWN1clN0YXRlLmNvbnRleHQgfHwgY3VyU3RhdGUuY29udGV4dC5uYW1lICE9IFwiIWNkYXRhXCIpIHB1c2hDb250ZXh0KFwiIWNkYXRhXCIpO1xuICAgIGlmIChjdXJTdGF0ZS50b2tlbml6ZSA9PSBpblRleHQpIHBvcENvbnRleHQoKTtcbiAgICByZXR1cm4gY29udCgpO1xuICB9IGVsc2UgcmV0dXJuIGNvbnQoKTtcbn1cbmZ1bmN0aW9uIGVuZHBsdWdpbihzdGFydE9mTGluZSkge1xuICByZXR1cm4gZnVuY3Rpb24gKHR5cGUpIHtcbiAgICBpZiAodHlwZSA9PSBcInNlbGZjbG9zZVBsdWdpblwiIHx8IHR5cGUgPT0gXCJlbmRQbHVnaW5cIikgcmV0dXJuIGNvbnQoKTtcbiAgICBpZiAodHlwZSA9PSBcImVuZFBsdWdpblwiKSB7XG4gICAgICBwdXNoQ29udGV4dChjdXJTdGF0ZS5wbHVnaW5OYW1lLCBzdGFydE9mTGluZSk7XG4gICAgICByZXR1cm4gY29udCgpO1xuICAgIH1cbiAgICByZXR1cm4gY29udCgpO1xuICB9O1xufVxuZnVuY3Rpb24gZW5kY2xvc2VwbHVnaW4oZXJyKSB7XG4gIHJldHVybiBmdW5jdGlvbiAodHlwZSkge1xuICAgIGlmIChlcnIpIHNldFN0eWxlID0gXCJlcnJvclwiO1xuICAgIGlmICh0eXBlID09IFwiZW5kUGx1Z2luXCIpIHJldHVybiBjb250KCk7XG4gICAgcmV0dXJuIHBhc3MoKTtcbiAgfTtcbn1cbmZ1bmN0aW9uIGF0dHJpYnV0ZXModHlwZSkge1xuICBpZiAodHlwZSA9PSBcImtleXdvcmRcIikge1xuICAgIHNldFN0eWxlID0gXCJhdHRyaWJ1dGVcIjtcbiAgICByZXR1cm4gY29udChhdHRyaWJ1dGVzKTtcbiAgfVxuICBpZiAodHlwZSA9PSBcImVxdWFsc1wiKSByZXR1cm4gY29udChhdHR2YWx1ZSwgYXR0cmlidXRlcyk7XG4gIHJldHVybiBwYXNzKCk7XG59XG5mdW5jdGlvbiBhdHR2YWx1ZSh0eXBlKSB7XG4gIGlmICh0eXBlID09IFwia2V5d29yZFwiKSB7XG4gICAgc2V0U3R5bGUgPSBcInN0cmluZ1wiO1xuICAgIHJldHVybiBjb250KCk7XG4gIH1cbiAgaWYgKHR5cGUgPT0gXCJzdHJpbmdcIikgcmV0dXJuIGNvbnQoYXR0dmFsdWVtYXliZSk7XG4gIHJldHVybiBwYXNzKCk7XG59XG5mdW5jdGlvbiBhdHR2YWx1ZW1heWJlKHR5cGUpIHtcbiAgaWYgKHR5cGUgPT0gXCJzdHJpbmdcIikgcmV0dXJuIGNvbnQoYXR0dmFsdWVtYXliZSk7ZWxzZSByZXR1cm4gcGFzcygpO1xufVxuZXhwb3J0IGNvbnN0IHRpa2kgPSB7XG4gIG5hbWU6IFwidGlraVwiLFxuICBzdGFydFN0YXRlOiBmdW5jdGlvbiAoKSB7XG4gICAgcmV0dXJuIHtcbiAgICAgIHRva2VuaXplOiBpblRleHQsXG4gICAgICBjYzogW10sXG4gICAgICBpbmRlbnRlZDogMCxcbiAgICAgIHN0YXJ0T2ZMaW5lOiB0cnVlLFxuICAgICAgcGx1Z2luTmFtZTogbnVsbCxcbiAgICAgIGNvbnRleHQ6IG51bGxcbiAgICB9O1xuICB9LFxuICB0b2tlbjogZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICBpZiAoc3RyZWFtLnNvbCgpKSB7XG4gICAgICBzdGF0ZS5zdGFydE9mTGluZSA9IHRydWU7XG4gICAgICBzdGF0ZS5pbmRlbnRlZCA9IHN0cmVhbS5pbmRlbnRhdGlvbigpO1xuICAgIH1cbiAgICBpZiAoc3RyZWFtLmVhdFNwYWNlKCkpIHJldHVybiBudWxsO1xuICAgIHNldFN0eWxlID0gdHlwZSA9IHBsdWdpbk5hbWUgPSBudWxsO1xuICAgIHZhciBzdHlsZSA9IHN0YXRlLnRva2VuaXplKHN0cmVhbSwgc3RhdGUpO1xuICAgIGlmICgoc3R5bGUgfHwgdHlwZSkgJiYgc3R5bGUgIT0gXCJjb21tZW50XCIpIHtcbiAgICAgIGN1clN0YXRlID0gc3RhdGU7XG4gICAgICB3aGlsZSAodHJ1ZSkge1xuICAgICAgICB2YXIgY29tYiA9IHN0YXRlLmNjLnBvcCgpIHx8IGVsZW1lbnQ7XG4gICAgICAgIGlmIChjb21iKHR5cGUgfHwgc3R5bGUpKSBicmVhaztcbiAgICAgIH1cbiAgICB9XG4gICAgc3RhdGUuc3RhcnRPZkxpbmUgPSBmYWxzZTtcbiAgICByZXR1cm4gc2V0U3R5bGUgfHwgc3R5bGU7XG4gIH0sXG4gIGluZGVudDogZnVuY3Rpb24gKHN0YXRlLCB0ZXh0QWZ0ZXIsIGN4KSB7XG4gICAgdmFyIGNvbnRleHQgPSBzdGF0ZS5jb250ZXh0O1xuICAgIGlmIChjb250ZXh0ICYmIGNvbnRleHQubm9JbmRlbnQpIHJldHVybiAwO1xuICAgIGlmIChjb250ZXh0ICYmIC9ee1xcLy8udGVzdCh0ZXh0QWZ0ZXIpKSBjb250ZXh0ID0gY29udGV4dC5wcmV2O1xuICAgIHdoaWxlIChjb250ZXh0ICYmICFjb250ZXh0LnN0YXJ0T2ZMaW5lKSBjb250ZXh0ID0gY29udGV4dC5wcmV2O1xuICAgIGlmIChjb250ZXh0KSByZXR1cm4gY29udGV4dC5pbmRlbnQgKyBjeC51bml0O2Vsc2UgcmV0dXJuIDA7XG4gIH1cbn07Il0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9