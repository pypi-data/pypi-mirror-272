"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[5936],{

/***/ 75936:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "haxe": () => (/* binding */ haxe),
/* harmony export */   "hxml": () => (/* binding */ hxml)
/* harmony export */ });
// Tokenizer

function kw(type) {
  return {
    type: type,
    style: "keyword"
  };
}
var A = kw("keyword a"),
  B = kw("keyword b"),
  C = kw("keyword c");
var operator = kw("operator"),
  atom = {
    type: "atom",
    style: "atom"
  },
  attribute = {
    type: "attribute",
    style: "attribute"
  };
var type = kw("typedef");
var keywords = {
  "if": A,
  "while": A,
  "else": B,
  "do": B,
  "try": B,
  "return": C,
  "break": C,
  "continue": C,
  "new": C,
  "throw": C,
  "var": kw("var"),
  "inline": attribute,
  "static": attribute,
  "using": kw("import"),
  "public": attribute,
  "private": attribute,
  "cast": kw("cast"),
  "import": kw("import"),
  "macro": kw("macro"),
  "function": kw("function"),
  "catch": kw("catch"),
  "untyped": kw("untyped"),
  "callback": kw("cb"),
  "for": kw("for"),
  "switch": kw("switch"),
  "case": kw("case"),
  "default": kw("default"),
  "in": operator,
  "never": kw("property_access"),
  "trace": kw("trace"),
  "class": type,
  "abstract": type,
  "enum": type,
  "interface": type,
  "typedef": type,
  "extends": type,
  "implements": type,
  "dynamic": type,
  "true": atom,
  "false": atom,
  "null": atom
};
var isOperatorChar = /[+\-*&%=<>!?|]/;
function chain(stream, state, f) {
  state.tokenize = f;
  return f(stream, state);
}
function toUnescaped(stream, end) {
  var escaped = false,
    next;
  while ((next = stream.next()) != null) {
    if (next == end && !escaped) return true;
    escaped = !escaped && next == "\\";
  }
}

// Used as scratch variables to communicate multiple values without
// consing up tons of objects.
var type, content;
function ret(tp, style, cont) {
  type = tp;
  content = cont;
  return style;
}
function haxeTokenBase(stream, state) {
  var ch = stream.next();
  if (ch == '"' || ch == "'") {
    return chain(stream, state, haxeTokenString(ch));
  } else if (/[\[\]{}\(\),;\:\.]/.test(ch)) {
    return ret(ch);
  } else if (ch == "0" && stream.eat(/x/i)) {
    stream.eatWhile(/[\da-f]/i);
    return ret("number", "number");
  } else if (/\d/.test(ch) || ch == "-" && stream.eat(/\d/)) {
    stream.match(/^\d*(?:\.\d*(?!\.))?(?:[eE][+\-]?\d+)?/);
    return ret("number", "number");
  } else if (state.reAllowed && ch == "~" && stream.eat(/\//)) {
    toUnescaped(stream, "/");
    stream.eatWhile(/[gimsu]/);
    return ret("regexp", "string.special");
  } else if (ch == "/") {
    if (stream.eat("*")) {
      return chain(stream, state, haxeTokenComment);
    } else if (stream.eat("/")) {
      stream.skipToEnd();
      return ret("comment", "comment");
    } else {
      stream.eatWhile(isOperatorChar);
      return ret("operator", null, stream.current());
    }
  } else if (ch == "#") {
    stream.skipToEnd();
    return ret("conditional", "meta");
  } else if (ch == "@") {
    stream.eat(/:/);
    stream.eatWhile(/[\w_]/);
    return ret("metadata", "meta");
  } else if (isOperatorChar.test(ch)) {
    stream.eatWhile(isOperatorChar);
    return ret("operator", null, stream.current());
  } else {
    var word;
    if (/[A-Z]/.test(ch)) {
      stream.eatWhile(/[\w_<>]/);
      word = stream.current();
      return ret("type", "type", word);
    } else {
      stream.eatWhile(/[\w_]/);
      var word = stream.current(),
        known = keywords.propertyIsEnumerable(word) && keywords[word];
      return known && state.kwAllowed ? ret(known.type, known.style, word) : ret("variable", "variable", word);
    }
  }
}
function haxeTokenString(quote) {
  return function (stream, state) {
    if (toUnescaped(stream, quote)) state.tokenize = haxeTokenBase;
    return ret("string", "string");
  };
}
function haxeTokenComment(stream, state) {
  var maybeEnd = false,
    ch;
  while (ch = stream.next()) {
    if (ch == "/" && maybeEnd) {
      state.tokenize = haxeTokenBase;
      break;
    }
    maybeEnd = ch == "*";
  }
  return ret("comment", "comment");
}

// Parser

var atomicTypes = {
  "atom": true,
  "number": true,
  "variable": true,
  "string": true,
  "regexp": true
};
function HaxeLexical(indented, column, type, align, prev, info) {
  this.indented = indented;
  this.column = column;
  this.type = type;
  this.prev = prev;
  this.info = info;
  if (align != null) this.align = align;
}
function inScope(state, varname) {
  for (var v = state.localVars; v; v = v.next) if (v.name == varname) return true;
}
function parseHaxe(state, style, type, content, stream) {
  var cc = state.cc;
  // Communicate our context to the combinators.
  // (Less wasteful than consing up a hundred closures on every call.)
  cx.state = state;
  cx.stream = stream;
  cx.marked = null, cx.cc = cc;
  if (!state.lexical.hasOwnProperty("align")) state.lexical.align = true;
  while (true) {
    var combinator = cc.length ? cc.pop() : statement;
    if (combinator(type, content)) {
      while (cc.length && cc[cc.length - 1].lex) cc.pop()();
      if (cx.marked) return cx.marked;
      if (type == "variable" && inScope(state, content)) return "variableName.local";
      if (type == "variable" && imported(state, content)) return "variableName.special";
      return style;
    }
  }
}
function imported(state, typename) {
  if (/[a-z]/.test(typename.charAt(0))) return false;
  var len = state.importedtypes.length;
  for (var i = 0; i < len; i++) if (state.importedtypes[i] == typename) return true;
}
function registerimport(importname) {
  var state = cx.state;
  for (var t = state.importedtypes; t; t = t.next) if (t.name == importname) return;
  state.importedtypes = {
    name: importname,
    next: state.importedtypes
  };
}
// Combinator utils

var cx = {
  state: null,
  column: null,
  marked: null,
  cc: null
};
function pass() {
  for (var i = arguments.length - 1; i >= 0; i--) cx.cc.push(arguments[i]);
}
function cont() {
  pass.apply(null, arguments);
  return true;
}
function inList(name, list) {
  for (var v = list; v; v = v.next) if (v.name == name) return true;
  return false;
}
function register(varname) {
  var state = cx.state;
  if (state.context) {
    cx.marked = "def";
    if (inList(varname, state.localVars)) return;
    state.localVars = {
      name: varname,
      next: state.localVars
    };
  } else if (state.globalVars) {
    if (inList(varname, state.globalVars)) return;
    state.globalVars = {
      name: varname,
      next: state.globalVars
    };
  }
}

// Combinators

var defaultVars = {
  name: "this",
  next: null
};
function pushcontext() {
  if (!cx.state.context) cx.state.localVars = defaultVars;
  cx.state.context = {
    prev: cx.state.context,
    vars: cx.state.localVars
  };
}
function popcontext() {
  cx.state.localVars = cx.state.context.vars;
  cx.state.context = cx.state.context.prev;
}
popcontext.lex = true;
function pushlex(type, info) {
  var result = function () {
    var state = cx.state;
    state.lexical = new HaxeLexical(state.indented, cx.stream.column(), type, null, state.lexical, info);
  };
  result.lex = true;
  return result;
}
function poplex() {
  var state = cx.state;
  if (state.lexical.prev) {
    if (state.lexical.type == ")") state.indented = state.lexical.indented;
    state.lexical = state.lexical.prev;
  }
}
poplex.lex = true;
function expect(wanted) {
  function f(type) {
    if (type == wanted) return cont();else if (wanted == ";") return pass();else return cont(f);
  }
  return f;
}
function statement(type) {
  if (type == "@") return cont(metadef);
  if (type == "var") return cont(pushlex("vardef"), vardef1, expect(";"), poplex);
  if (type == "keyword a") return cont(pushlex("form"), expression, statement, poplex);
  if (type == "keyword b") return cont(pushlex("form"), statement, poplex);
  if (type == "{") return cont(pushlex("}"), pushcontext, block, poplex, popcontext);
  if (type == ";") return cont();
  if (type == "attribute") return cont(maybeattribute);
  if (type == "function") return cont(functiondef);
  if (type == "for") return cont(pushlex("form"), expect("("), pushlex(")"), forspec1, expect(")"), poplex, statement, poplex);
  if (type == "variable") return cont(pushlex("stat"), maybelabel);
  if (type == "switch") return cont(pushlex("form"), expression, pushlex("}", "switch"), expect("{"), block, poplex, poplex);
  if (type == "case") return cont(expression, expect(":"));
  if (type == "default") return cont(expect(":"));
  if (type == "catch") return cont(pushlex("form"), pushcontext, expect("("), funarg, expect(")"), statement, poplex, popcontext);
  if (type == "import") return cont(importdef, expect(";"));
  if (type == "typedef") return cont(typedef);
  return pass(pushlex("stat"), expression, expect(";"), poplex);
}
function expression(type) {
  if (atomicTypes.hasOwnProperty(type)) return cont(maybeoperator);
  if (type == "type") return cont(maybeoperator);
  if (type == "function") return cont(functiondef);
  if (type == "keyword c") return cont(maybeexpression);
  if (type == "(") return cont(pushlex(")"), maybeexpression, expect(")"), poplex, maybeoperator);
  if (type == "operator") return cont(expression);
  if (type == "[") return cont(pushlex("]"), commasep(maybeexpression, "]"), poplex, maybeoperator);
  if (type == "{") return cont(pushlex("}"), commasep(objprop, "}"), poplex, maybeoperator);
  return cont();
}
function maybeexpression(type) {
  if (type.match(/[;\}\)\],]/)) return pass();
  return pass(expression);
}
function maybeoperator(type, value) {
  if (type == "operator" && /\+\+|--/.test(value)) return cont(maybeoperator);
  if (type == "operator" || type == ":") return cont(expression);
  if (type == ";") return;
  if (type == "(") return cont(pushlex(")"), commasep(expression, ")"), poplex, maybeoperator);
  if (type == ".") return cont(property, maybeoperator);
  if (type == "[") return cont(pushlex("]"), expression, expect("]"), poplex, maybeoperator);
}
function maybeattribute(type) {
  if (type == "attribute") return cont(maybeattribute);
  if (type == "function") return cont(functiondef);
  if (type == "var") return cont(vardef1);
}
function metadef(type) {
  if (type == ":") return cont(metadef);
  if (type == "variable") return cont(metadef);
  if (type == "(") return cont(pushlex(")"), commasep(metaargs, ")"), poplex, statement);
}
function metaargs(type) {
  if (type == "variable") return cont();
}
function importdef(type, value) {
  if (type == "variable" && /[A-Z]/.test(value.charAt(0))) {
    registerimport(value);
    return cont();
  } else if (type == "variable" || type == "property" || type == "." || value == "*") return cont(importdef);
}
function typedef(type, value) {
  if (type == "variable" && /[A-Z]/.test(value.charAt(0))) {
    registerimport(value);
    return cont();
  } else if (type == "type" && /[A-Z]/.test(value.charAt(0))) {
    return cont();
  }
}
function maybelabel(type) {
  if (type == ":") return cont(poplex, statement);
  return pass(maybeoperator, expect(";"), poplex);
}
function property(type) {
  if (type == "variable") {
    cx.marked = "property";
    return cont();
  }
}
function objprop(type) {
  if (type == "variable") cx.marked = "property";
  if (atomicTypes.hasOwnProperty(type)) return cont(expect(":"), expression);
}
function commasep(what, end) {
  function proceed(type) {
    if (type == ",") return cont(what, proceed);
    if (type == end) return cont();
    return cont(expect(end));
  }
  return function (type) {
    if (type == end) return cont();else return pass(what, proceed);
  };
}
function block(type) {
  if (type == "}") return cont();
  return pass(statement, block);
}
function vardef1(type, value) {
  if (type == "variable") {
    register(value);
    return cont(typeuse, vardef2);
  }
  return cont();
}
function vardef2(type, value) {
  if (value == "=") return cont(expression, vardef2);
  if (type == ",") return cont(vardef1);
}
function forspec1(type, value) {
  if (type == "variable") {
    register(value);
    return cont(forin, expression);
  } else {
    return pass();
  }
}
function forin(_type, value) {
  if (value == "in") return cont();
}
function functiondef(type, value) {
  //function names starting with upper-case letters are recognised as types, so cludging them together here.
  if (type == "variable" || type == "type") {
    register(value);
    return cont(functiondef);
  }
  if (value == "new") return cont(functiondef);
  if (type == "(") return cont(pushlex(")"), pushcontext, commasep(funarg, ")"), poplex, typeuse, statement, popcontext);
}
function typeuse(type) {
  if (type == ":") return cont(typestring);
}
function typestring(type) {
  if (type == "type") return cont();
  if (type == "variable") return cont();
  if (type == "{") return cont(pushlex("}"), commasep(typeprop, "}"), poplex);
}
function typeprop(type) {
  if (type == "variable") return cont(typeuse);
}
function funarg(type, value) {
  if (type == "variable") {
    register(value);
    return cont(typeuse);
  }
}

// Interface
const haxe = {
  name: "haxe",
  startState: function (indentUnit) {
    var defaulttypes = ["Int", "Float", "String", "Void", "Std", "Bool", "Dynamic", "Array"];
    var state = {
      tokenize: haxeTokenBase,
      reAllowed: true,
      kwAllowed: true,
      cc: [],
      lexical: new HaxeLexical(-indentUnit, 0, "block", false),
      importedtypes: defaulttypes,
      context: null,
      indented: 0
    };
    return state;
  },
  token: function (stream, state) {
    if (stream.sol()) {
      if (!state.lexical.hasOwnProperty("align")) state.lexical.align = false;
      state.indented = stream.indentation();
    }
    if (stream.eatSpace()) return null;
    var style = state.tokenize(stream, state);
    if (type == "comment") return style;
    state.reAllowed = !!(type == "operator" || type == "keyword c" || type.match(/^[\[{}\(,;:]$/));
    state.kwAllowed = type != '.';
    return parseHaxe(state, style, type, content, stream);
  },
  indent: function (state, textAfter, cx) {
    if (state.tokenize != haxeTokenBase) return 0;
    var firstChar = textAfter && textAfter.charAt(0),
      lexical = state.lexical;
    if (lexical.type == "stat" && firstChar == "}") lexical = lexical.prev;
    var type = lexical.type,
      closing = firstChar == type;
    if (type == "vardef") return lexical.indented + 4;else if (type == "form" && firstChar == "{") return lexical.indented;else if (type == "stat" || type == "form") return lexical.indented + cx.unit;else if (lexical.info == "switch" && !closing) return lexical.indented + (/^(?:case|default)\b/.test(textAfter) ? cx.unit : 2 * cx.unit);else if (lexical.align) return lexical.column + (closing ? 0 : 1);else return lexical.indented + (closing ? 0 : cx.unit);
  },
  languageData: {
    indentOnInput: /^\s*[{}]$/,
    commentTokens: {
      line: "//",
      block: {
        open: "/*",
        close: "*/"
      }
    }
  }
};
const hxml = {
  name: "hxml",
  startState: function () {
    return {
      define: false,
      inString: false
    };
  },
  token: function (stream, state) {
    var ch = stream.peek();
    var sol = stream.sol();

    ///* comments */
    if (ch == "#") {
      stream.skipToEnd();
      return "comment";
    }
    if (sol && ch == "-") {
      var style = "variable-2";
      stream.eat(/-/);
      if (stream.peek() == "-") {
        stream.eat(/-/);
        style = "keyword a";
      }
      if (stream.peek() == "D") {
        stream.eat(/[D]/);
        style = "keyword c";
        state.define = true;
      }
      stream.eatWhile(/[A-Z]/i);
      return style;
    }
    var ch = stream.peek();
    if (state.inString == false && ch == "'") {
      state.inString = true;
      stream.next();
    }
    if (state.inString == true) {
      if (stream.skipTo("'")) {} else {
        stream.skipToEnd();
      }
      if (stream.peek() == "'") {
        stream.next();
        state.inString = false;
      }
      return "string";
    }
    stream.next();
    return null;
  },
  languageData: {
    commentTokens: {
      line: "#"
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNTkzNi5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9AY29kZW1pcnJvci9sZWdhY3ktbW9kZXMvbW9kZS9oYXhlLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8vIFRva2VuaXplclxuXG5mdW5jdGlvbiBrdyh0eXBlKSB7XG4gIHJldHVybiB7XG4gICAgdHlwZTogdHlwZSxcbiAgICBzdHlsZTogXCJrZXl3b3JkXCJcbiAgfTtcbn1cbnZhciBBID0ga3coXCJrZXl3b3JkIGFcIiksXG4gIEIgPSBrdyhcImtleXdvcmQgYlwiKSxcbiAgQyA9IGt3KFwia2V5d29yZCBjXCIpO1xudmFyIG9wZXJhdG9yID0ga3coXCJvcGVyYXRvclwiKSxcbiAgYXRvbSA9IHtcbiAgICB0eXBlOiBcImF0b21cIixcbiAgICBzdHlsZTogXCJhdG9tXCJcbiAgfSxcbiAgYXR0cmlidXRlID0ge1xuICAgIHR5cGU6IFwiYXR0cmlidXRlXCIsXG4gICAgc3R5bGU6IFwiYXR0cmlidXRlXCJcbiAgfTtcbnZhciB0eXBlID0ga3coXCJ0eXBlZGVmXCIpO1xudmFyIGtleXdvcmRzID0ge1xuICBcImlmXCI6IEEsXG4gIFwid2hpbGVcIjogQSxcbiAgXCJlbHNlXCI6IEIsXG4gIFwiZG9cIjogQixcbiAgXCJ0cnlcIjogQixcbiAgXCJyZXR1cm5cIjogQyxcbiAgXCJicmVha1wiOiBDLFxuICBcImNvbnRpbnVlXCI6IEMsXG4gIFwibmV3XCI6IEMsXG4gIFwidGhyb3dcIjogQyxcbiAgXCJ2YXJcIjoga3coXCJ2YXJcIiksXG4gIFwiaW5saW5lXCI6IGF0dHJpYnV0ZSxcbiAgXCJzdGF0aWNcIjogYXR0cmlidXRlLFxuICBcInVzaW5nXCI6IGt3KFwiaW1wb3J0XCIpLFxuICBcInB1YmxpY1wiOiBhdHRyaWJ1dGUsXG4gIFwicHJpdmF0ZVwiOiBhdHRyaWJ1dGUsXG4gIFwiY2FzdFwiOiBrdyhcImNhc3RcIiksXG4gIFwiaW1wb3J0XCI6IGt3KFwiaW1wb3J0XCIpLFxuICBcIm1hY3JvXCI6IGt3KFwibWFjcm9cIiksXG4gIFwiZnVuY3Rpb25cIjoga3coXCJmdW5jdGlvblwiKSxcbiAgXCJjYXRjaFwiOiBrdyhcImNhdGNoXCIpLFxuICBcInVudHlwZWRcIjoga3coXCJ1bnR5cGVkXCIpLFxuICBcImNhbGxiYWNrXCI6IGt3KFwiY2JcIiksXG4gIFwiZm9yXCI6IGt3KFwiZm9yXCIpLFxuICBcInN3aXRjaFwiOiBrdyhcInN3aXRjaFwiKSxcbiAgXCJjYXNlXCI6IGt3KFwiY2FzZVwiKSxcbiAgXCJkZWZhdWx0XCI6IGt3KFwiZGVmYXVsdFwiKSxcbiAgXCJpblwiOiBvcGVyYXRvcixcbiAgXCJuZXZlclwiOiBrdyhcInByb3BlcnR5X2FjY2Vzc1wiKSxcbiAgXCJ0cmFjZVwiOiBrdyhcInRyYWNlXCIpLFxuICBcImNsYXNzXCI6IHR5cGUsXG4gIFwiYWJzdHJhY3RcIjogdHlwZSxcbiAgXCJlbnVtXCI6IHR5cGUsXG4gIFwiaW50ZXJmYWNlXCI6IHR5cGUsXG4gIFwidHlwZWRlZlwiOiB0eXBlLFxuICBcImV4dGVuZHNcIjogdHlwZSxcbiAgXCJpbXBsZW1lbnRzXCI6IHR5cGUsXG4gIFwiZHluYW1pY1wiOiB0eXBlLFxuICBcInRydWVcIjogYXRvbSxcbiAgXCJmYWxzZVwiOiBhdG9tLFxuICBcIm51bGxcIjogYXRvbVxufTtcbnZhciBpc09wZXJhdG9yQ2hhciA9IC9bK1xcLSomJT08PiE/fF0vO1xuZnVuY3Rpb24gY2hhaW4oc3RyZWFtLCBzdGF0ZSwgZikge1xuICBzdGF0ZS50b2tlbml6ZSA9IGY7XG4gIHJldHVybiBmKHN0cmVhbSwgc3RhdGUpO1xufVxuZnVuY3Rpb24gdG9VbmVzY2FwZWQoc3RyZWFtLCBlbmQpIHtcbiAgdmFyIGVzY2FwZWQgPSBmYWxzZSxcbiAgICBuZXh0O1xuICB3aGlsZSAoKG5leHQgPSBzdHJlYW0ubmV4dCgpKSAhPSBudWxsKSB7XG4gICAgaWYgKG5leHQgPT0gZW5kICYmICFlc2NhcGVkKSByZXR1cm4gdHJ1ZTtcbiAgICBlc2NhcGVkID0gIWVzY2FwZWQgJiYgbmV4dCA9PSBcIlxcXFxcIjtcbiAgfVxufVxuXG4vLyBVc2VkIGFzIHNjcmF0Y2ggdmFyaWFibGVzIHRvIGNvbW11bmljYXRlIG11bHRpcGxlIHZhbHVlcyB3aXRob3V0XG4vLyBjb25zaW5nIHVwIHRvbnMgb2Ygb2JqZWN0cy5cbnZhciB0eXBlLCBjb250ZW50O1xuZnVuY3Rpb24gcmV0KHRwLCBzdHlsZSwgY29udCkge1xuICB0eXBlID0gdHA7XG4gIGNvbnRlbnQgPSBjb250O1xuICByZXR1cm4gc3R5bGU7XG59XG5mdW5jdGlvbiBoYXhlVG9rZW5CYXNlKHN0cmVhbSwgc3RhdGUpIHtcbiAgdmFyIGNoID0gc3RyZWFtLm5leHQoKTtcbiAgaWYgKGNoID09ICdcIicgfHwgY2ggPT0gXCInXCIpIHtcbiAgICByZXR1cm4gY2hhaW4oc3RyZWFtLCBzdGF0ZSwgaGF4ZVRva2VuU3RyaW5nKGNoKSk7XG4gIH0gZWxzZSBpZiAoL1tcXFtcXF17fVxcKFxcKSw7XFw6XFwuXS8udGVzdChjaCkpIHtcbiAgICByZXR1cm4gcmV0KGNoKTtcbiAgfSBlbHNlIGlmIChjaCA9PSBcIjBcIiAmJiBzdHJlYW0uZWF0KC94L2kpKSB7XG4gICAgc3RyZWFtLmVhdFdoaWxlKC9bXFxkYS1mXS9pKTtcbiAgICByZXR1cm4gcmV0KFwibnVtYmVyXCIsIFwibnVtYmVyXCIpO1xuICB9IGVsc2UgaWYgKC9cXGQvLnRlc3QoY2gpIHx8IGNoID09IFwiLVwiICYmIHN0cmVhbS5lYXQoL1xcZC8pKSB7XG4gICAgc3RyZWFtLm1hdGNoKC9eXFxkKig/OlxcLlxcZCooPyFcXC4pKT8oPzpbZUVdWytcXC1dP1xcZCspPy8pO1xuICAgIHJldHVybiByZXQoXCJudW1iZXJcIiwgXCJudW1iZXJcIik7XG4gIH0gZWxzZSBpZiAoc3RhdGUucmVBbGxvd2VkICYmIGNoID09IFwiflwiICYmIHN0cmVhbS5lYXQoL1xcLy8pKSB7XG4gICAgdG9VbmVzY2FwZWQoc3RyZWFtLCBcIi9cIik7XG4gICAgc3RyZWFtLmVhdFdoaWxlKC9bZ2ltc3VdLyk7XG4gICAgcmV0dXJuIHJldChcInJlZ2V4cFwiLCBcInN0cmluZy5zcGVjaWFsXCIpO1xuICB9IGVsc2UgaWYgKGNoID09IFwiL1wiKSB7XG4gICAgaWYgKHN0cmVhbS5lYXQoXCIqXCIpKSB7XG4gICAgICByZXR1cm4gY2hhaW4oc3RyZWFtLCBzdGF0ZSwgaGF4ZVRva2VuQ29tbWVudCk7XG4gICAgfSBlbHNlIGlmIChzdHJlYW0uZWF0KFwiL1wiKSkge1xuICAgICAgc3RyZWFtLnNraXBUb0VuZCgpO1xuICAgICAgcmV0dXJuIHJldChcImNvbW1lbnRcIiwgXCJjb21tZW50XCIpO1xuICAgIH0gZWxzZSB7XG4gICAgICBzdHJlYW0uZWF0V2hpbGUoaXNPcGVyYXRvckNoYXIpO1xuICAgICAgcmV0dXJuIHJldChcIm9wZXJhdG9yXCIsIG51bGwsIHN0cmVhbS5jdXJyZW50KCkpO1xuICAgIH1cbiAgfSBlbHNlIGlmIChjaCA9PSBcIiNcIikge1xuICAgIHN0cmVhbS5za2lwVG9FbmQoKTtcbiAgICByZXR1cm4gcmV0KFwiY29uZGl0aW9uYWxcIiwgXCJtZXRhXCIpO1xuICB9IGVsc2UgaWYgKGNoID09IFwiQFwiKSB7XG4gICAgc3RyZWFtLmVhdCgvOi8pO1xuICAgIHN0cmVhbS5lYXRXaGlsZSgvW1xcd19dLyk7XG4gICAgcmV0dXJuIHJldChcIm1ldGFkYXRhXCIsIFwibWV0YVwiKTtcbiAgfSBlbHNlIGlmIChpc09wZXJhdG9yQ2hhci50ZXN0KGNoKSkge1xuICAgIHN0cmVhbS5lYXRXaGlsZShpc09wZXJhdG9yQ2hhcik7XG4gICAgcmV0dXJuIHJldChcIm9wZXJhdG9yXCIsIG51bGwsIHN0cmVhbS5jdXJyZW50KCkpO1xuICB9IGVsc2Uge1xuICAgIHZhciB3b3JkO1xuICAgIGlmICgvW0EtWl0vLnRlc3QoY2gpKSB7XG4gICAgICBzdHJlYW0uZWF0V2hpbGUoL1tcXHdfPD5dLyk7XG4gICAgICB3b3JkID0gc3RyZWFtLmN1cnJlbnQoKTtcbiAgICAgIHJldHVybiByZXQoXCJ0eXBlXCIsIFwidHlwZVwiLCB3b3JkKTtcbiAgICB9IGVsc2Uge1xuICAgICAgc3RyZWFtLmVhdFdoaWxlKC9bXFx3X10vKTtcbiAgICAgIHZhciB3b3JkID0gc3RyZWFtLmN1cnJlbnQoKSxcbiAgICAgICAga25vd24gPSBrZXl3b3Jkcy5wcm9wZXJ0eUlzRW51bWVyYWJsZSh3b3JkKSAmJiBrZXl3b3Jkc1t3b3JkXTtcbiAgICAgIHJldHVybiBrbm93biAmJiBzdGF0ZS5rd0FsbG93ZWQgPyByZXQoa25vd24udHlwZSwga25vd24uc3R5bGUsIHdvcmQpIDogcmV0KFwidmFyaWFibGVcIiwgXCJ2YXJpYWJsZVwiLCB3b3JkKTtcbiAgICB9XG4gIH1cbn1cbmZ1bmN0aW9uIGhheGVUb2tlblN0cmluZyhxdW90ZSkge1xuICByZXR1cm4gZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICBpZiAodG9VbmVzY2FwZWQoc3RyZWFtLCBxdW90ZSkpIHN0YXRlLnRva2VuaXplID0gaGF4ZVRva2VuQmFzZTtcbiAgICByZXR1cm4gcmV0KFwic3RyaW5nXCIsIFwic3RyaW5nXCIpO1xuICB9O1xufVxuZnVuY3Rpb24gaGF4ZVRva2VuQ29tbWVudChzdHJlYW0sIHN0YXRlKSB7XG4gIHZhciBtYXliZUVuZCA9IGZhbHNlLFxuICAgIGNoO1xuICB3aGlsZSAoY2ggPSBzdHJlYW0ubmV4dCgpKSB7XG4gICAgaWYgKGNoID09IFwiL1wiICYmIG1heWJlRW5kKSB7XG4gICAgICBzdGF0ZS50b2tlbml6ZSA9IGhheGVUb2tlbkJhc2U7XG4gICAgICBicmVhaztcbiAgICB9XG4gICAgbWF5YmVFbmQgPSBjaCA9PSBcIipcIjtcbiAgfVxuICByZXR1cm4gcmV0KFwiY29tbWVudFwiLCBcImNvbW1lbnRcIik7XG59XG5cbi8vIFBhcnNlclxuXG52YXIgYXRvbWljVHlwZXMgPSB7XG4gIFwiYXRvbVwiOiB0cnVlLFxuICBcIm51bWJlclwiOiB0cnVlLFxuICBcInZhcmlhYmxlXCI6IHRydWUsXG4gIFwic3RyaW5nXCI6IHRydWUsXG4gIFwicmVnZXhwXCI6IHRydWVcbn07XG5mdW5jdGlvbiBIYXhlTGV4aWNhbChpbmRlbnRlZCwgY29sdW1uLCB0eXBlLCBhbGlnbiwgcHJldiwgaW5mbykge1xuICB0aGlzLmluZGVudGVkID0gaW5kZW50ZWQ7XG4gIHRoaXMuY29sdW1uID0gY29sdW1uO1xuICB0aGlzLnR5cGUgPSB0eXBlO1xuICB0aGlzLnByZXYgPSBwcmV2O1xuICB0aGlzLmluZm8gPSBpbmZvO1xuICBpZiAoYWxpZ24gIT0gbnVsbCkgdGhpcy5hbGlnbiA9IGFsaWduO1xufVxuZnVuY3Rpb24gaW5TY29wZShzdGF0ZSwgdmFybmFtZSkge1xuICBmb3IgKHZhciB2ID0gc3RhdGUubG9jYWxWYXJzOyB2OyB2ID0gdi5uZXh0KSBpZiAodi5uYW1lID09IHZhcm5hbWUpIHJldHVybiB0cnVlO1xufVxuZnVuY3Rpb24gcGFyc2VIYXhlKHN0YXRlLCBzdHlsZSwgdHlwZSwgY29udGVudCwgc3RyZWFtKSB7XG4gIHZhciBjYyA9IHN0YXRlLmNjO1xuICAvLyBDb21tdW5pY2F0ZSBvdXIgY29udGV4dCB0byB0aGUgY29tYmluYXRvcnMuXG4gIC8vIChMZXNzIHdhc3RlZnVsIHRoYW4gY29uc2luZyB1cCBhIGh1bmRyZWQgY2xvc3VyZXMgb24gZXZlcnkgY2FsbC4pXG4gIGN4LnN0YXRlID0gc3RhdGU7XG4gIGN4LnN0cmVhbSA9IHN0cmVhbTtcbiAgY3gubWFya2VkID0gbnVsbCwgY3guY2MgPSBjYztcbiAgaWYgKCFzdGF0ZS5sZXhpY2FsLmhhc093blByb3BlcnR5KFwiYWxpZ25cIikpIHN0YXRlLmxleGljYWwuYWxpZ24gPSB0cnVlO1xuICB3aGlsZSAodHJ1ZSkge1xuICAgIHZhciBjb21iaW5hdG9yID0gY2MubGVuZ3RoID8gY2MucG9wKCkgOiBzdGF0ZW1lbnQ7XG4gICAgaWYgKGNvbWJpbmF0b3IodHlwZSwgY29udGVudCkpIHtcbiAgICAgIHdoaWxlIChjYy5sZW5ndGggJiYgY2NbY2MubGVuZ3RoIC0gMV0ubGV4KSBjYy5wb3AoKSgpO1xuICAgICAgaWYgKGN4Lm1hcmtlZCkgcmV0dXJuIGN4Lm1hcmtlZDtcbiAgICAgIGlmICh0eXBlID09IFwidmFyaWFibGVcIiAmJiBpblNjb3BlKHN0YXRlLCBjb250ZW50KSkgcmV0dXJuIFwidmFyaWFibGVOYW1lLmxvY2FsXCI7XG4gICAgICBpZiAodHlwZSA9PSBcInZhcmlhYmxlXCIgJiYgaW1wb3J0ZWQoc3RhdGUsIGNvbnRlbnQpKSByZXR1cm4gXCJ2YXJpYWJsZU5hbWUuc3BlY2lhbFwiO1xuICAgICAgcmV0dXJuIHN0eWxlO1xuICAgIH1cbiAgfVxufVxuZnVuY3Rpb24gaW1wb3J0ZWQoc3RhdGUsIHR5cGVuYW1lKSB7XG4gIGlmICgvW2Etel0vLnRlc3QodHlwZW5hbWUuY2hhckF0KDApKSkgcmV0dXJuIGZhbHNlO1xuICB2YXIgbGVuID0gc3RhdGUuaW1wb3J0ZWR0eXBlcy5sZW5ndGg7XG4gIGZvciAodmFyIGkgPSAwOyBpIDwgbGVuOyBpKyspIGlmIChzdGF0ZS5pbXBvcnRlZHR5cGVzW2ldID09IHR5cGVuYW1lKSByZXR1cm4gdHJ1ZTtcbn1cbmZ1bmN0aW9uIHJlZ2lzdGVyaW1wb3J0KGltcG9ydG5hbWUpIHtcbiAgdmFyIHN0YXRlID0gY3guc3RhdGU7XG4gIGZvciAodmFyIHQgPSBzdGF0ZS5pbXBvcnRlZHR5cGVzOyB0OyB0ID0gdC5uZXh0KSBpZiAodC5uYW1lID09IGltcG9ydG5hbWUpIHJldHVybjtcbiAgc3RhdGUuaW1wb3J0ZWR0eXBlcyA9IHtcbiAgICBuYW1lOiBpbXBvcnRuYW1lLFxuICAgIG5leHQ6IHN0YXRlLmltcG9ydGVkdHlwZXNcbiAgfTtcbn1cbi8vIENvbWJpbmF0b3IgdXRpbHNcblxudmFyIGN4ID0ge1xuICBzdGF0ZTogbnVsbCxcbiAgY29sdW1uOiBudWxsLFxuICBtYXJrZWQ6IG51bGwsXG4gIGNjOiBudWxsXG59O1xuZnVuY3Rpb24gcGFzcygpIHtcbiAgZm9yICh2YXIgaSA9IGFyZ3VtZW50cy5sZW5ndGggLSAxOyBpID49IDA7IGktLSkgY3guY2MucHVzaChhcmd1bWVudHNbaV0pO1xufVxuZnVuY3Rpb24gY29udCgpIHtcbiAgcGFzcy5hcHBseShudWxsLCBhcmd1bWVudHMpO1xuICByZXR1cm4gdHJ1ZTtcbn1cbmZ1bmN0aW9uIGluTGlzdChuYW1lLCBsaXN0KSB7XG4gIGZvciAodmFyIHYgPSBsaXN0OyB2OyB2ID0gdi5uZXh0KSBpZiAodi5uYW1lID09IG5hbWUpIHJldHVybiB0cnVlO1xuICByZXR1cm4gZmFsc2U7XG59XG5mdW5jdGlvbiByZWdpc3Rlcih2YXJuYW1lKSB7XG4gIHZhciBzdGF0ZSA9IGN4LnN0YXRlO1xuICBpZiAoc3RhdGUuY29udGV4dCkge1xuICAgIGN4Lm1hcmtlZCA9IFwiZGVmXCI7XG4gICAgaWYgKGluTGlzdCh2YXJuYW1lLCBzdGF0ZS5sb2NhbFZhcnMpKSByZXR1cm47XG4gICAgc3RhdGUubG9jYWxWYXJzID0ge1xuICAgICAgbmFtZTogdmFybmFtZSxcbiAgICAgIG5leHQ6IHN0YXRlLmxvY2FsVmFyc1xuICAgIH07XG4gIH0gZWxzZSBpZiAoc3RhdGUuZ2xvYmFsVmFycykge1xuICAgIGlmIChpbkxpc3QodmFybmFtZSwgc3RhdGUuZ2xvYmFsVmFycykpIHJldHVybjtcbiAgICBzdGF0ZS5nbG9iYWxWYXJzID0ge1xuICAgICAgbmFtZTogdmFybmFtZSxcbiAgICAgIG5leHQ6IHN0YXRlLmdsb2JhbFZhcnNcbiAgICB9O1xuICB9XG59XG5cbi8vIENvbWJpbmF0b3JzXG5cbnZhciBkZWZhdWx0VmFycyA9IHtcbiAgbmFtZTogXCJ0aGlzXCIsXG4gIG5leHQ6IG51bGxcbn07XG5mdW5jdGlvbiBwdXNoY29udGV4dCgpIHtcbiAgaWYgKCFjeC5zdGF0ZS5jb250ZXh0KSBjeC5zdGF0ZS5sb2NhbFZhcnMgPSBkZWZhdWx0VmFycztcbiAgY3guc3RhdGUuY29udGV4dCA9IHtcbiAgICBwcmV2OiBjeC5zdGF0ZS5jb250ZXh0LFxuICAgIHZhcnM6IGN4LnN0YXRlLmxvY2FsVmFyc1xuICB9O1xufVxuZnVuY3Rpb24gcG9wY29udGV4dCgpIHtcbiAgY3guc3RhdGUubG9jYWxWYXJzID0gY3guc3RhdGUuY29udGV4dC52YXJzO1xuICBjeC5zdGF0ZS5jb250ZXh0ID0gY3guc3RhdGUuY29udGV4dC5wcmV2O1xufVxucG9wY29udGV4dC5sZXggPSB0cnVlO1xuZnVuY3Rpb24gcHVzaGxleCh0eXBlLCBpbmZvKSB7XG4gIHZhciByZXN1bHQgPSBmdW5jdGlvbiAoKSB7XG4gICAgdmFyIHN0YXRlID0gY3guc3RhdGU7XG4gICAgc3RhdGUubGV4aWNhbCA9IG5ldyBIYXhlTGV4aWNhbChzdGF0ZS5pbmRlbnRlZCwgY3guc3RyZWFtLmNvbHVtbigpLCB0eXBlLCBudWxsLCBzdGF0ZS5sZXhpY2FsLCBpbmZvKTtcbiAgfTtcbiAgcmVzdWx0LmxleCA9IHRydWU7XG4gIHJldHVybiByZXN1bHQ7XG59XG5mdW5jdGlvbiBwb3BsZXgoKSB7XG4gIHZhciBzdGF0ZSA9IGN4LnN0YXRlO1xuICBpZiAoc3RhdGUubGV4aWNhbC5wcmV2KSB7XG4gICAgaWYgKHN0YXRlLmxleGljYWwudHlwZSA9PSBcIilcIikgc3RhdGUuaW5kZW50ZWQgPSBzdGF0ZS5sZXhpY2FsLmluZGVudGVkO1xuICAgIHN0YXRlLmxleGljYWwgPSBzdGF0ZS5sZXhpY2FsLnByZXY7XG4gIH1cbn1cbnBvcGxleC5sZXggPSB0cnVlO1xuZnVuY3Rpb24gZXhwZWN0KHdhbnRlZCkge1xuICBmdW5jdGlvbiBmKHR5cGUpIHtcbiAgICBpZiAodHlwZSA9PSB3YW50ZWQpIHJldHVybiBjb250KCk7ZWxzZSBpZiAod2FudGVkID09IFwiO1wiKSByZXR1cm4gcGFzcygpO2Vsc2UgcmV0dXJuIGNvbnQoZik7XG4gIH1cbiAgcmV0dXJuIGY7XG59XG5mdW5jdGlvbiBzdGF0ZW1lbnQodHlwZSkge1xuICBpZiAodHlwZSA9PSBcIkBcIikgcmV0dXJuIGNvbnQobWV0YWRlZik7XG4gIGlmICh0eXBlID09IFwidmFyXCIpIHJldHVybiBjb250KHB1c2hsZXgoXCJ2YXJkZWZcIiksIHZhcmRlZjEsIGV4cGVjdChcIjtcIiksIHBvcGxleCk7XG4gIGlmICh0eXBlID09IFwia2V5d29yZCBhXCIpIHJldHVybiBjb250KHB1c2hsZXgoXCJmb3JtXCIpLCBleHByZXNzaW9uLCBzdGF0ZW1lbnQsIHBvcGxleCk7XG4gIGlmICh0eXBlID09IFwia2V5d29yZCBiXCIpIHJldHVybiBjb250KHB1c2hsZXgoXCJmb3JtXCIpLCBzdGF0ZW1lbnQsIHBvcGxleCk7XG4gIGlmICh0eXBlID09IFwie1wiKSByZXR1cm4gY29udChwdXNobGV4KFwifVwiKSwgcHVzaGNvbnRleHQsIGJsb2NrLCBwb3BsZXgsIHBvcGNvbnRleHQpO1xuICBpZiAodHlwZSA9PSBcIjtcIikgcmV0dXJuIGNvbnQoKTtcbiAgaWYgKHR5cGUgPT0gXCJhdHRyaWJ1dGVcIikgcmV0dXJuIGNvbnQobWF5YmVhdHRyaWJ1dGUpO1xuICBpZiAodHlwZSA9PSBcImZ1bmN0aW9uXCIpIHJldHVybiBjb250KGZ1bmN0aW9uZGVmKTtcbiAgaWYgKHR5cGUgPT0gXCJmb3JcIikgcmV0dXJuIGNvbnQocHVzaGxleChcImZvcm1cIiksIGV4cGVjdChcIihcIiksIHB1c2hsZXgoXCIpXCIpLCBmb3JzcGVjMSwgZXhwZWN0KFwiKVwiKSwgcG9wbGV4LCBzdGF0ZW1lbnQsIHBvcGxleCk7XG4gIGlmICh0eXBlID09IFwidmFyaWFibGVcIikgcmV0dXJuIGNvbnQocHVzaGxleChcInN0YXRcIiksIG1heWJlbGFiZWwpO1xuICBpZiAodHlwZSA9PSBcInN3aXRjaFwiKSByZXR1cm4gY29udChwdXNobGV4KFwiZm9ybVwiKSwgZXhwcmVzc2lvbiwgcHVzaGxleChcIn1cIiwgXCJzd2l0Y2hcIiksIGV4cGVjdChcIntcIiksIGJsb2NrLCBwb3BsZXgsIHBvcGxleCk7XG4gIGlmICh0eXBlID09IFwiY2FzZVwiKSByZXR1cm4gY29udChleHByZXNzaW9uLCBleHBlY3QoXCI6XCIpKTtcbiAgaWYgKHR5cGUgPT0gXCJkZWZhdWx0XCIpIHJldHVybiBjb250KGV4cGVjdChcIjpcIikpO1xuICBpZiAodHlwZSA9PSBcImNhdGNoXCIpIHJldHVybiBjb250KHB1c2hsZXgoXCJmb3JtXCIpLCBwdXNoY29udGV4dCwgZXhwZWN0KFwiKFwiKSwgZnVuYXJnLCBleHBlY3QoXCIpXCIpLCBzdGF0ZW1lbnQsIHBvcGxleCwgcG9wY29udGV4dCk7XG4gIGlmICh0eXBlID09IFwiaW1wb3J0XCIpIHJldHVybiBjb250KGltcG9ydGRlZiwgZXhwZWN0KFwiO1wiKSk7XG4gIGlmICh0eXBlID09IFwidHlwZWRlZlwiKSByZXR1cm4gY29udCh0eXBlZGVmKTtcbiAgcmV0dXJuIHBhc3MocHVzaGxleChcInN0YXRcIiksIGV4cHJlc3Npb24sIGV4cGVjdChcIjtcIiksIHBvcGxleCk7XG59XG5mdW5jdGlvbiBleHByZXNzaW9uKHR5cGUpIHtcbiAgaWYgKGF0b21pY1R5cGVzLmhhc093blByb3BlcnR5KHR5cGUpKSByZXR1cm4gY29udChtYXliZW9wZXJhdG9yKTtcbiAgaWYgKHR5cGUgPT0gXCJ0eXBlXCIpIHJldHVybiBjb250KG1heWJlb3BlcmF0b3IpO1xuICBpZiAodHlwZSA9PSBcImZ1bmN0aW9uXCIpIHJldHVybiBjb250KGZ1bmN0aW9uZGVmKTtcbiAgaWYgKHR5cGUgPT0gXCJrZXl3b3JkIGNcIikgcmV0dXJuIGNvbnQobWF5YmVleHByZXNzaW9uKTtcbiAgaWYgKHR5cGUgPT0gXCIoXCIpIHJldHVybiBjb250KHB1c2hsZXgoXCIpXCIpLCBtYXliZWV4cHJlc3Npb24sIGV4cGVjdChcIilcIiksIHBvcGxleCwgbWF5YmVvcGVyYXRvcik7XG4gIGlmICh0eXBlID09IFwib3BlcmF0b3JcIikgcmV0dXJuIGNvbnQoZXhwcmVzc2lvbik7XG4gIGlmICh0eXBlID09IFwiW1wiKSByZXR1cm4gY29udChwdXNobGV4KFwiXVwiKSwgY29tbWFzZXAobWF5YmVleHByZXNzaW9uLCBcIl1cIiksIHBvcGxleCwgbWF5YmVvcGVyYXRvcik7XG4gIGlmICh0eXBlID09IFwie1wiKSByZXR1cm4gY29udChwdXNobGV4KFwifVwiKSwgY29tbWFzZXAob2JqcHJvcCwgXCJ9XCIpLCBwb3BsZXgsIG1heWJlb3BlcmF0b3IpO1xuICByZXR1cm4gY29udCgpO1xufVxuZnVuY3Rpb24gbWF5YmVleHByZXNzaW9uKHR5cGUpIHtcbiAgaWYgKHR5cGUubWF0Y2goL1s7XFx9XFwpXFxdLF0vKSkgcmV0dXJuIHBhc3MoKTtcbiAgcmV0dXJuIHBhc3MoZXhwcmVzc2lvbik7XG59XG5mdW5jdGlvbiBtYXliZW9wZXJhdG9yKHR5cGUsIHZhbHVlKSB7XG4gIGlmICh0eXBlID09IFwib3BlcmF0b3JcIiAmJiAvXFwrXFwrfC0tLy50ZXN0KHZhbHVlKSkgcmV0dXJuIGNvbnQobWF5YmVvcGVyYXRvcik7XG4gIGlmICh0eXBlID09IFwib3BlcmF0b3JcIiB8fCB0eXBlID09IFwiOlwiKSByZXR1cm4gY29udChleHByZXNzaW9uKTtcbiAgaWYgKHR5cGUgPT0gXCI7XCIpIHJldHVybjtcbiAgaWYgKHR5cGUgPT0gXCIoXCIpIHJldHVybiBjb250KHB1c2hsZXgoXCIpXCIpLCBjb21tYXNlcChleHByZXNzaW9uLCBcIilcIiksIHBvcGxleCwgbWF5YmVvcGVyYXRvcik7XG4gIGlmICh0eXBlID09IFwiLlwiKSByZXR1cm4gY29udChwcm9wZXJ0eSwgbWF5YmVvcGVyYXRvcik7XG4gIGlmICh0eXBlID09IFwiW1wiKSByZXR1cm4gY29udChwdXNobGV4KFwiXVwiKSwgZXhwcmVzc2lvbiwgZXhwZWN0KFwiXVwiKSwgcG9wbGV4LCBtYXliZW9wZXJhdG9yKTtcbn1cbmZ1bmN0aW9uIG1heWJlYXR0cmlidXRlKHR5cGUpIHtcbiAgaWYgKHR5cGUgPT0gXCJhdHRyaWJ1dGVcIikgcmV0dXJuIGNvbnQobWF5YmVhdHRyaWJ1dGUpO1xuICBpZiAodHlwZSA9PSBcImZ1bmN0aW9uXCIpIHJldHVybiBjb250KGZ1bmN0aW9uZGVmKTtcbiAgaWYgKHR5cGUgPT0gXCJ2YXJcIikgcmV0dXJuIGNvbnQodmFyZGVmMSk7XG59XG5mdW5jdGlvbiBtZXRhZGVmKHR5cGUpIHtcbiAgaWYgKHR5cGUgPT0gXCI6XCIpIHJldHVybiBjb250KG1ldGFkZWYpO1xuICBpZiAodHlwZSA9PSBcInZhcmlhYmxlXCIpIHJldHVybiBjb250KG1ldGFkZWYpO1xuICBpZiAodHlwZSA9PSBcIihcIikgcmV0dXJuIGNvbnQocHVzaGxleChcIilcIiksIGNvbW1hc2VwKG1ldGFhcmdzLCBcIilcIiksIHBvcGxleCwgc3RhdGVtZW50KTtcbn1cbmZ1bmN0aW9uIG1ldGFhcmdzKHR5cGUpIHtcbiAgaWYgKHR5cGUgPT0gXCJ2YXJpYWJsZVwiKSByZXR1cm4gY29udCgpO1xufVxuZnVuY3Rpb24gaW1wb3J0ZGVmKHR5cGUsIHZhbHVlKSB7XG4gIGlmICh0eXBlID09IFwidmFyaWFibGVcIiAmJiAvW0EtWl0vLnRlc3QodmFsdWUuY2hhckF0KDApKSkge1xuICAgIHJlZ2lzdGVyaW1wb3J0KHZhbHVlKTtcbiAgICByZXR1cm4gY29udCgpO1xuICB9IGVsc2UgaWYgKHR5cGUgPT0gXCJ2YXJpYWJsZVwiIHx8IHR5cGUgPT0gXCJwcm9wZXJ0eVwiIHx8IHR5cGUgPT0gXCIuXCIgfHwgdmFsdWUgPT0gXCIqXCIpIHJldHVybiBjb250KGltcG9ydGRlZik7XG59XG5mdW5jdGlvbiB0eXBlZGVmKHR5cGUsIHZhbHVlKSB7XG4gIGlmICh0eXBlID09IFwidmFyaWFibGVcIiAmJiAvW0EtWl0vLnRlc3QodmFsdWUuY2hhckF0KDApKSkge1xuICAgIHJlZ2lzdGVyaW1wb3J0KHZhbHVlKTtcbiAgICByZXR1cm4gY29udCgpO1xuICB9IGVsc2UgaWYgKHR5cGUgPT0gXCJ0eXBlXCIgJiYgL1tBLVpdLy50ZXN0KHZhbHVlLmNoYXJBdCgwKSkpIHtcbiAgICByZXR1cm4gY29udCgpO1xuICB9XG59XG5mdW5jdGlvbiBtYXliZWxhYmVsKHR5cGUpIHtcbiAgaWYgKHR5cGUgPT0gXCI6XCIpIHJldHVybiBjb250KHBvcGxleCwgc3RhdGVtZW50KTtcbiAgcmV0dXJuIHBhc3MobWF5YmVvcGVyYXRvciwgZXhwZWN0KFwiO1wiKSwgcG9wbGV4KTtcbn1cbmZ1bmN0aW9uIHByb3BlcnR5KHR5cGUpIHtcbiAgaWYgKHR5cGUgPT0gXCJ2YXJpYWJsZVwiKSB7XG4gICAgY3gubWFya2VkID0gXCJwcm9wZXJ0eVwiO1xuICAgIHJldHVybiBjb250KCk7XG4gIH1cbn1cbmZ1bmN0aW9uIG9ianByb3AodHlwZSkge1xuICBpZiAodHlwZSA9PSBcInZhcmlhYmxlXCIpIGN4Lm1hcmtlZCA9IFwicHJvcGVydHlcIjtcbiAgaWYgKGF0b21pY1R5cGVzLmhhc093blByb3BlcnR5KHR5cGUpKSByZXR1cm4gY29udChleHBlY3QoXCI6XCIpLCBleHByZXNzaW9uKTtcbn1cbmZ1bmN0aW9uIGNvbW1hc2VwKHdoYXQsIGVuZCkge1xuICBmdW5jdGlvbiBwcm9jZWVkKHR5cGUpIHtcbiAgICBpZiAodHlwZSA9PSBcIixcIikgcmV0dXJuIGNvbnQod2hhdCwgcHJvY2VlZCk7XG4gICAgaWYgKHR5cGUgPT0gZW5kKSByZXR1cm4gY29udCgpO1xuICAgIHJldHVybiBjb250KGV4cGVjdChlbmQpKTtcbiAgfVxuICByZXR1cm4gZnVuY3Rpb24gKHR5cGUpIHtcbiAgICBpZiAodHlwZSA9PSBlbmQpIHJldHVybiBjb250KCk7ZWxzZSByZXR1cm4gcGFzcyh3aGF0LCBwcm9jZWVkKTtcbiAgfTtcbn1cbmZ1bmN0aW9uIGJsb2NrKHR5cGUpIHtcbiAgaWYgKHR5cGUgPT0gXCJ9XCIpIHJldHVybiBjb250KCk7XG4gIHJldHVybiBwYXNzKHN0YXRlbWVudCwgYmxvY2spO1xufVxuZnVuY3Rpb24gdmFyZGVmMSh0eXBlLCB2YWx1ZSkge1xuICBpZiAodHlwZSA9PSBcInZhcmlhYmxlXCIpIHtcbiAgICByZWdpc3Rlcih2YWx1ZSk7XG4gICAgcmV0dXJuIGNvbnQodHlwZXVzZSwgdmFyZGVmMik7XG4gIH1cbiAgcmV0dXJuIGNvbnQoKTtcbn1cbmZ1bmN0aW9uIHZhcmRlZjIodHlwZSwgdmFsdWUpIHtcbiAgaWYgKHZhbHVlID09IFwiPVwiKSByZXR1cm4gY29udChleHByZXNzaW9uLCB2YXJkZWYyKTtcbiAgaWYgKHR5cGUgPT0gXCIsXCIpIHJldHVybiBjb250KHZhcmRlZjEpO1xufVxuZnVuY3Rpb24gZm9yc3BlYzEodHlwZSwgdmFsdWUpIHtcbiAgaWYgKHR5cGUgPT0gXCJ2YXJpYWJsZVwiKSB7XG4gICAgcmVnaXN0ZXIodmFsdWUpO1xuICAgIHJldHVybiBjb250KGZvcmluLCBleHByZXNzaW9uKTtcbiAgfSBlbHNlIHtcbiAgICByZXR1cm4gcGFzcygpO1xuICB9XG59XG5mdW5jdGlvbiBmb3JpbihfdHlwZSwgdmFsdWUpIHtcbiAgaWYgKHZhbHVlID09IFwiaW5cIikgcmV0dXJuIGNvbnQoKTtcbn1cbmZ1bmN0aW9uIGZ1bmN0aW9uZGVmKHR5cGUsIHZhbHVlKSB7XG4gIC8vZnVuY3Rpb24gbmFtZXMgc3RhcnRpbmcgd2l0aCB1cHBlci1jYXNlIGxldHRlcnMgYXJlIHJlY29nbmlzZWQgYXMgdHlwZXMsIHNvIGNsdWRnaW5nIHRoZW0gdG9nZXRoZXIgaGVyZS5cbiAgaWYgKHR5cGUgPT0gXCJ2YXJpYWJsZVwiIHx8IHR5cGUgPT0gXCJ0eXBlXCIpIHtcbiAgICByZWdpc3Rlcih2YWx1ZSk7XG4gICAgcmV0dXJuIGNvbnQoZnVuY3Rpb25kZWYpO1xuICB9XG4gIGlmICh2YWx1ZSA9PSBcIm5ld1wiKSByZXR1cm4gY29udChmdW5jdGlvbmRlZik7XG4gIGlmICh0eXBlID09IFwiKFwiKSByZXR1cm4gY29udChwdXNobGV4KFwiKVwiKSwgcHVzaGNvbnRleHQsIGNvbW1hc2VwKGZ1bmFyZywgXCIpXCIpLCBwb3BsZXgsIHR5cGV1c2UsIHN0YXRlbWVudCwgcG9wY29udGV4dCk7XG59XG5mdW5jdGlvbiB0eXBldXNlKHR5cGUpIHtcbiAgaWYgKHR5cGUgPT0gXCI6XCIpIHJldHVybiBjb250KHR5cGVzdHJpbmcpO1xufVxuZnVuY3Rpb24gdHlwZXN0cmluZyh0eXBlKSB7XG4gIGlmICh0eXBlID09IFwidHlwZVwiKSByZXR1cm4gY29udCgpO1xuICBpZiAodHlwZSA9PSBcInZhcmlhYmxlXCIpIHJldHVybiBjb250KCk7XG4gIGlmICh0eXBlID09IFwie1wiKSByZXR1cm4gY29udChwdXNobGV4KFwifVwiKSwgY29tbWFzZXAodHlwZXByb3AsIFwifVwiKSwgcG9wbGV4KTtcbn1cbmZ1bmN0aW9uIHR5cGVwcm9wKHR5cGUpIHtcbiAgaWYgKHR5cGUgPT0gXCJ2YXJpYWJsZVwiKSByZXR1cm4gY29udCh0eXBldXNlKTtcbn1cbmZ1bmN0aW9uIGZ1bmFyZyh0eXBlLCB2YWx1ZSkge1xuICBpZiAodHlwZSA9PSBcInZhcmlhYmxlXCIpIHtcbiAgICByZWdpc3Rlcih2YWx1ZSk7XG4gICAgcmV0dXJuIGNvbnQodHlwZXVzZSk7XG4gIH1cbn1cblxuLy8gSW50ZXJmYWNlXG5leHBvcnQgY29uc3QgaGF4ZSA9IHtcbiAgbmFtZTogXCJoYXhlXCIsXG4gIHN0YXJ0U3RhdGU6IGZ1bmN0aW9uIChpbmRlbnRVbml0KSB7XG4gICAgdmFyIGRlZmF1bHR0eXBlcyA9IFtcIkludFwiLCBcIkZsb2F0XCIsIFwiU3RyaW5nXCIsIFwiVm9pZFwiLCBcIlN0ZFwiLCBcIkJvb2xcIiwgXCJEeW5hbWljXCIsIFwiQXJyYXlcIl07XG4gICAgdmFyIHN0YXRlID0ge1xuICAgICAgdG9rZW5pemU6IGhheGVUb2tlbkJhc2UsXG4gICAgICByZUFsbG93ZWQ6IHRydWUsXG4gICAgICBrd0FsbG93ZWQ6IHRydWUsXG4gICAgICBjYzogW10sXG4gICAgICBsZXhpY2FsOiBuZXcgSGF4ZUxleGljYWwoLWluZGVudFVuaXQsIDAsIFwiYmxvY2tcIiwgZmFsc2UpLFxuICAgICAgaW1wb3J0ZWR0eXBlczogZGVmYXVsdHR5cGVzLFxuICAgICAgY29udGV4dDogbnVsbCxcbiAgICAgIGluZGVudGVkOiAwXG4gICAgfTtcbiAgICByZXR1cm4gc3RhdGU7XG4gIH0sXG4gIHRva2VuOiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIGlmIChzdHJlYW0uc29sKCkpIHtcbiAgICAgIGlmICghc3RhdGUubGV4aWNhbC5oYXNPd25Qcm9wZXJ0eShcImFsaWduXCIpKSBzdGF0ZS5sZXhpY2FsLmFsaWduID0gZmFsc2U7XG4gICAgICBzdGF0ZS5pbmRlbnRlZCA9IHN0cmVhbS5pbmRlbnRhdGlvbigpO1xuICAgIH1cbiAgICBpZiAoc3RyZWFtLmVhdFNwYWNlKCkpIHJldHVybiBudWxsO1xuICAgIHZhciBzdHlsZSA9IHN0YXRlLnRva2VuaXplKHN0cmVhbSwgc3RhdGUpO1xuICAgIGlmICh0eXBlID09IFwiY29tbWVudFwiKSByZXR1cm4gc3R5bGU7XG4gICAgc3RhdGUucmVBbGxvd2VkID0gISEodHlwZSA9PSBcIm9wZXJhdG9yXCIgfHwgdHlwZSA9PSBcImtleXdvcmQgY1wiIHx8IHR5cGUubWF0Y2goL15bXFxbe31cXCgsOzpdJC8pKTtcbiAgICBzdGF0ZS5rd0FsbG93ZWQgPSB0eXBlICE9ICcuJztcbiAgICByZXR1cm4gcGFyc2VIYXhlKHN0YXRlLCBzdHlsZSwgdHlwZSwgY29udGVudCwgc3RyZWFtKTtcbiAgfSxcbiAgaW5kZW50OiBmdW5jdGlvbiAoc3RhdGUsIHRleHRBZnRlciwgY3gpIHtcbiAgICBpZiAoc3RhdGUudG9rZW5pemUgIT0gaGF4ZVRva2VuQmFzZSkgcmV0dXJuIDA7XG4gICAgdmFyIGZpcnN0Q2hhciA9IHRleHRBZnRlciAmJiB0ZXh0QWZ0ZXIuY2hhckF0KDApLFxuICAgICAgbGV4aWNhbCA9IHN0YXRlLmxleGljYWw7XG4gICAgaWYgKGxleGljYWwudHlwZSA9PSBcInN0YXRcIiAmJiBmaXJzdENoYXIgPT0gXCJ9XCIpIGxleGljYWwgPSBsZXhpY2FsLnByZXY7XG4gICAgdmFyIHR5cGUgPSBsZXhpY2FsLnR5cGUsXG4gICAgICBjbG9zaW5nID0gZmlyc3RDaGFyID09IHR5cGU7XG4gICAgaWYgKHR5cGUgPT0gXCJ2YXJkZWZcIikgcmV0dXJuIGxleGljYWwuaW5kZW50ZWQgKyA0O2Vsc2UgaWYgKHR5cGUgPT0gXCJmb3JtXCIgJiYgZmlyc3RDaGFyID09IFwie1wiKSByZXR1cm4gbGV4aWNhbC5pbmRlbnRlZDtlbHNlIGlmICh0eXBlID09IFwic3RhdFwiIHx8IHR5cGUgPT0gXCJmb3JtXCIpIHJldHVybiBsZXhpY2FsLmluZGVudGVkICsgY3gudW5pdDtlbHNlIGlmIChsZXhpY2FsLmluZm8gPT0gXCJzd2l0Y2hcIiAmJiAhY2xvc2luZykgcmV0dXJuIGxleGljYWwuaW5kZW50ZWQgKyAoL14oPzpjYXNlfGRlZmF1bHQpXFxiLy50ZXN0KHRleHRBZnRlcikgPyBjeC51bml0IDogMiAqIGN4LnVuaXQpO2Vsc2UgaWYgKGxleGljYWwuYWxpZ24pIHJldHVybiBsZXhpY2FsLmNvbHVtbiArIChjbG9zaW5nID8gMCA6IDEpO2Vsc2UgcmV0dXJuIGxleGljYWwuaW5kZW50ZWQgKyAoY2xvc2luZyA/IDAgOiBjeC51bml0KTtcbiAgfSxcbiAgbGFuZ3VhZ2VEYXRhOiB7XG4gICAgaW5kZW50T25JbnB1dDogL15cXHMqW3t9XSQvLFxuICAgIGNvbW1lbnRUb2tlbnM6IHtcbiAgICAgIGxpbmU6IFwiLy9cIixcbiAgICAgIGJsb2NrOiB7XG4gICAgICAgIG9wZW46IFwiLypcIixcbiAgICAgICAgY2xvc2U6IFwiKi9cIlxuICAgICAgfVxuICAgIH1cbiAgfVxufTtcbmV4cG9ydCBjb25zdCBoeG1sID0ge1xuICBuYW1lOiBcImh4bWxcIixcbiAgc3RhcnRTdGF0ZTogZnVuY3Rpb24gKCkge1xuICAgIHJldHVybiB7XG4gICAgICBkZWZpbmU6IGZhbHNlLFxuICAgICAgaW5TdHJpbmc6IGZhbHNlXG4gICAgfTtcbiAgfSxcbiAgdG9rZW46IGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgdmFyIGNoID0gc3RyZWFtLnBlZWsoKTtcbiAgICB2YXIgc29sID0gc3RyZWFtLnNvbCgpO1xuXG4gICAgLy8vKiBjb21tZW50cyAqL1xuICAgIGlmIChjaCA9PSBcIiNcIikge1xuICAgICAgc3RyZWFtLnNraXBUb0VuZCgpO1xuICAgICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICAgIH1cbiAgICBpZiAoc29sICYmIGNoID09IFwiLVwiKSB7XG4gICAgICB2YXIgc3R5bGUgPSBcInZhcmlhYmxlLTJcIjtcbiAgICAgIHN0cmVhbS5lYXQoLy0vKTtcbiAgICAgIGlmIChzdHJlYW0ucGVlaygpID09IFwiLVwiKSB7XG4gICAgICAgIHN0cmVhbS5lYXQoLy0vKTtcbiAgICAgICAgc3R5bGUgPSBcImtleXdvcmQgYVwiO1xuICAgICAgfVxuICAgICAgaWYgKHN0cmVhbS5wZWVrKCkgPT0gXCJEXCIpIHtcbiAgICAgICAgc3RyZWFtLmVhdCgvW0RdLyk7XG4gICAgICAgIHN0eWxlID0gXCJrZXl3b3JkIGNcIjtcbiAgICAgICAgc3RhdGUuZGVmaW5lID0gdHJ1ZTtcbiAgICAgIH1cbiAgICAgIHN0cmVhbS5lYXRXaGlsZSgvW0EtWl0vaSk7XG4gICAgICByZXR1cm4gc3R5bGU7XG4gICAgfVxuICAgIHZhciBjaCA9IHN0cmVhbS5wZWVrKCk7XG4gICAgaWYgKHN0YXRlLmluU3RyaW5nID09IGZhbHNlICYmIGNoID09IFwiJ1wiKSB7XG4gICAgICBzdGF0ZS5pblN0cmluZyA9IHRydWU7XG4gICAgICBzdHJlYW0ubmV4dCgpO1xuICAgIH1cbiAgICBpZiAoc3RhdGUuaW5TdHJpbmcgPT0gdHJ1ZSkge1xuICAgICAgaWYgKHN0cmVhbS5za2lwVG8oXCInXCIpKSB7fSBlbHNlIHtcbiAgICAgICAgc3RyZWFtLnNraXBUb0VuZCgpO1xuICAgICAgfVxuICAgICAgaWYgKHN0cmVhbS5wZWVrKCkgPT0gXCInXCIpIHtcbiAgICAgICAgc3RyZWFtLm5leHQoKTtcbiAgICAgICAgc3RhdGUuaW5TdHJpbmcgPSBmYWxzZTtcbiAgICAgIH1cbiAgICAgIHJldHVybiBcInN0cmluZ1wiO1xuICAgIH1cbiAgICBzdHJlYW0ubmV4dCgpO1xuICAgIHJldHVybiBudWxsO1xuICB9LFxuICBsYW5ndWFnZURhdGE6IHtcbiAgICBjb21tZW50VG9rZW5zOiB7XG4gICAgICBsaW5lOiBcIiNcIlxuICAgIH1cbiAgfVxufTsiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=