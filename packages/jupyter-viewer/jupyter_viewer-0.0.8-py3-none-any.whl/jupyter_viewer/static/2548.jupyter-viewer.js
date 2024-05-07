"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[2548],{

/***/ 22548:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "javascript": () => (/* binding */ javascript),
/* harmony export */   "json": () => (/* binding */ json),
/* harmony export */   "jsonld": () => (/* binding */ jsonld),
/* harmony export */   "typescript": () => (/* binding */ typescript)
/* harmony export */ });
function mkJavaScript(parserConfig) {
  var statementIndent = parserConfig.statementIndent;
  var jsonldMode = parserConfig.jsonld;
  var jsonMode = parserConfig.json || jsonldMode;
  var isTS = parserConfig.typescript;
  var wordRE = parserConfig.wordCharacters || /[\w$\xa1-\uffff]/;

  // Tokenizer

  var keywords = function () {
    function kw(type) {
      return {
        type: type,
        style: "keyword"
      };
    }
    var A = kw("keyword a"),
      B = kw("keyword b"),
      C = kw("keyword c"),
      D = kw("keyword d");
    var operator = kw("operator"),
      atom = {
        type: "atom",
        style: "atom"
      };
    return {
      "if": kw("if"),
      "while": A,
      "with": A,
      "else": B,
      "do": B,
      "try": B,
      "finally": B,
      "return": D,
      "break": D,
      "continue": D,
      "new": kw("new"),
      "delete": C,
      "void": C,
      "throw": C,
      "debugger": kw("debugger"),
      "var": kw("var"),
      "const": kw("var"),
      "let": kw("var"),
      "function": kw("function"),
      "catch": kw("catch"),
      "for": kw("for"),
      "switch": kw("switch"),
      "case": kw("case"),
      "default": kw("default"),
      "in": operator,
      "typeof": operator,
      "instanceof": operator,
      "true": atom,
      "false": atom,
      "null": atom,
      "undefined": atom,
      "NaN": atom,
      "Infinity": atom,
      "this": kw("this"),
      "class": kw("class"),
      "super": kw("atom"),
      "yield": C,
      "export": kw("export"),
      "import": kw("import"),
      "extends": C,
      "await": C
    };
  }();
  var isOperatorChar = /[+\-*&%=<>!?|~^@]/;
  var isJsonldKeyword = /^@(context|id|value|language|type|container|list|set|reverse|index|base|vocab|graph)"/;
  function readRegexp(stream) {
    var escaped = false,
      next,
      inSet = false;
    while ((next = stream.next()) != null) {
      if (!escaped) {
        if (next == "/" && !inSet) return;
        if (next == "[") inSet = true;else if (inSet && next == "]") inSet = false;
      }
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
  function tokenBase(stream, state) {
    var ch = stream.next();
    if (ch == '"' || ch == "'") {
      state.tokenize = tokenString(ch);
      return state.tokenize(stream, state);
    } else if (ch == "." && stream.match(/^\d[\d_]*(?:[eE][+\-]?[\d_]+)?/)) {
      return ret("number", "number");
    } else if (ch == "." && stream.match("..")) {
      return ret("spread", "meta");
    } else if (/[\[\]{}\(\),;\:\.]/.test(ch)) {
      return ret(ch);
    } else if (ch == "=" && stream.eat(">")) {
      return ret("=>", "operator");
    } else if (ch == "0" && stream.match(/^(?:x[\dA-Fa-f_]+|o[0-7_]+|b[01_]+)n?/)) {
      return ret("number", "number");
    } else if (/\d/.test(ch)) {
      stream.match(/^[\d_]*(?:n|(?:\.[\d_]*)?(?:[eE][+\-]?[\d_]+)?)?/);
      return ret("number", "number");
    } else if (ch == "/") {
      if (stream.eat("*")) {
        state.tokenize = tokenComment;
        return tokenComment(stream, state);
      } else if (stream.eat("/")) {
        stream.skipToEnd();
        return ret("comment", "comment");
      } else if (expressionAllowed(stream, state, 1)) {
        readRegexp(stream);
        stream.match(/^\b(([gimyus])(?![gimyus]*\2))+\b/);
        return ret("regexp", "string.special");
      } else {
        stream.eat("=");
        return ret("operator", "operator", stream.current());
      }
    } else if (ch == "`") {
      state.tokenize = tokenQuasi;
      return tokenQuasi(stream, state);
    } else if (ch == "#" && stream.peek() == "!") {
      stream.skipToEnd();
      return ret("meta", "meta");
    } else if (ch == "#" && stream.eatWhile(wordRE)) {
      return ret("variable", "property");
    } else if (ch == "<" && stream.match("!--") || ch == "-" && stream.match("->") && !/\S/.test(stream.string.slice(0, stream.start))) {
      stream.skipToEnd();
      return ret("comment", "comment");
    } else if (isOperatorChar.test(ch)) {
      if (ch != ">" || !state.lexical || state.lexical.type != ">") {
        if (stream.eat("=")) {
          if (ch == "!" || ch == "=") stream.eat("=");
        } else if (/[<>*+\-|&?]/.test(ch)) {
          stream.eat(ch);
          if (ch == ">") stream.eat(ch);
        }
      }
      if (ch == "?" && stream.eat(".")) return ret(".");
      return ret("operator", "operator", stream.current());
    } else if (wordRE.test(ch)) {
      stream.eatWhile(wordRE);
      var word = stream.current();
      if (state.lastType != ".") {
        if (keywords.propertyIsEnumerable(word)) {
          var kw = keywords[word];
          return ret(kw.type, kw.style, word);
        }
        if (word == "async" && stream.match(/^(\s|\/\*([^*]|\*(?!\/))*?\*\/)*[\[\(\w]/, false)) return ret("async", "keyword", word);
      }
      return ret("variable", "variable", word);
    }
  }
  function tokenString(quote) {
    return function (stream, state) {
      var escaped = false,
        next;
      if (jsonldMode && stream.peek() == "@" && stream.match(isJsonldKeyword)) {
        state.tokenize = tokenBase;
        return ret("jsonld-keyword", "meta");
      }
      while ((next = stream.next()) != null) {
        if (next == quote && !escaped) break;
        escaped = !escaped && next == "\\";
      }
      if (!escaped) state.tokenize = tokenBase;
      return ret("string", "string");
    };
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
    return ret("comment", "comment");
  }
  function tokenQuasi(stream, state) {
    var escaped = false,
      next;
    while ((next = stream.next()) != null) {
      if (!escaped && (next == "`" || next == "$" && stream.eat("{"))) {
        state.tokenize = tokenBase;
        break;
      }
      escaped = !escaped && next == "\\";
    }
    return ret("quasi", "string.special", stream.current());
  }
  var brackets = "([{}])";
  // This is a crude lookahead trick to try and notice that we're
  // parsing the argument patterns for a fat-arrow function before we
  // actually hit the arrow token. It only works if the arrow is on
  // the same line as the arguments and there's no strange noise
  // (comments) in between. Fallback is to only notice when we hit the
  // arrow, and not declare the arguments as locals for the arrow
  // body.
  function findFatArrow(stream, state) {
    if (state.fatArrowAt) state.fatArrowAt = null;
    var arrow = stream.string.indexOf("=>", stream.start);
    if (arrow < 0) return;
    if (isTS) {
      // Try to skip TypeScript return type declarations after the arguments
      var m = /:\s*(?:\w+(?:<[^>]*>|\[\])?|\{[^}]*\})\s*$/.exec(stream.string.slice(stream.start, arrow));
      if (m) arrow = m.index;
    }
    var depth = 0,
      sawSomething = false;
    for (var pos = arrow - 1; pos >= 0; --pos) {
      var ch = stream.string.charAt(pos);
      var bracket = brackets.indexOf(ch);
      if (bracket >= 0 && bracket < 3) {
        if (!depth) {
          ++pos;
          break;
        }
        if (--depth == 0) {
          if (ch == "(") sawSomething = true;
          break;
        }
      } else if (bracket >= 3 && bracket < 6) {
        ++depth;
      } else if (wordRE.test(ch)) {
        sawSomething = true;
      } else if (/["'\/`]/.test(ch)) {
        for (;; --pos) {
          if (pos == 0) return;
          var next = stream.string.charAt(pos - 1);
          if (next == ch && stream.string.charAt(pos - 2) != "\\") {
            pos--;
            break;
          }
        }
      } else if (sawSomething && !depth) {
        ++pos;
        break;
      }
    }
    if (sawSomething && !depth) state.fatArrowAt = pos;
  }

  // Parser

  var atomicTypes = {
    "atom": true,
    "number": true,
    "variable": true,
    "string": true,
    "regexp": true,
    "this": true,
    "import": true,
    "jsonld-keyword": true
  };
  function JSLexical(indented, column, type, align, prev, info) {
    this.indented = indented;
    this.column = column;
    this.type = type;
    this.prev = prev;
    this.info = info;
    if (align != null) this.align = align;
  }
  function inScope(state, varname) {
    for (var v = state.localVars; v; v = v.next) if (v.name == varname) return true;
    for (var cx = state.context; cx; cx = cx.prev) {
      for (var v = cx.vars; v; v = v.next) if (v.name == varname) return true;
    }
  }
  function parseJS(state, style, type, content, stream) {
    var cc = state.cc;
    // Communicate our context to the combinators.
    // (Less wasteful than consing up a hundred closures on every call.)
    cx.state = state;
    cx.stream = stream;
    cx.marked = null;
    cx.cc = cc;
    cx.style = style;
    if (!state.lexical.hasOwnProperty("align")) state.lexical.align = true;
    while (true) {
      var combinator = cc.length ? cc.pop() : jsonMode ? expression : statement;
      if (combinator(type, content)) {
        while (cc.length && cc[cc.length - 1].lex) cc.pop()();
        if (cx.marked) return cx.marked;
        if (type == "variable" && inScope(state, content)) return "variableName.local";
        return style;
      }
    }
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
    cx.marked = "def";
    if (state.context) {
      if (state.lexical.info == "var" && state.context && state.context.block) {
        // FIXME function decls are also not block scoped
        var newContext = registerVarScoped(varname, state.context);
        if (newContext != null) {
          state.context = newContext;
          return;
        }
      } else if (!inList(varname, state.localVars)) {
        state.localVars = new Var(varname, state.localVars);
        return;
      }
    }
    // Fall through means this is global
    if (parserConfig.globalVars && !inList(varname, state.globalVars)) state.globalVars = new Var(varname, state.globalVars);
  }
  function registerVarScoped(varname, context) {
    if (!context) {
      return null;
    } else if (context.block) {
      var inner = registerVarScoped(varname, context.prev);
      if (!inner) return null;
      if (inner == context.prev) return context;
      return new Context(inner, context.vars, true);
    } else if (inList(varname, context.vars)) {
      return context;
    } else {
      return new Context(context.prev, new Var(varname, context.vars), false);
    }
  }
  function isModifier(name) {
    return name == "public" || name == "private" || name == "protected" || name == "abstract" || name == "readonly";
  }

  // Combinators

  function Context(prev, vars, block) {
    this.prev = prev;
    this.vars = vars;
    this.block = block;
  }
  function Var(name, next) {
    this.name = name;
    this.next = next;
  }
  var defaultVars = new Var("this", new Var("arguments", null));
  function pushcontext() {
    cx.state.context = new Context(cx.state.context, cx.state.localVars, false);
    cx.state.localVars = defaultVars;
  }
  function pushblockcontext() {
    cx.state.context = new Context(cx.state.context, cx.state.localVars, true);
    cx.state.localVars = null;
  }
  pushcontext.lex = pushblockcontext.lex = true;
  function popcontext() {
    cx.state.localVars = cx.state.context.vars;
    cx.state.context = cx.state.context.prev;
  }
  popcontext.lex = true;
  function pushlex(type, info) {
    var result = function () {
      var state = cx.state,
        indent = state.indented;
      if (state.lexical.type == "stat") indent = state.lexical.indented;else for (var outer = state.lexical; outer && outer.type == ")" && outer.align; outer = outer.prev) indent = outer.indented;
      state.lexical = new JSLexical(indent, cx.stream.column(), type, null, state.lexical, info);
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
    function exp(type) {
      if (type == wanted) return cont();else if (wanted == ";" || type == "}" || type == ")" || type == "]") return pass();else return cont(exp);
    }
    ;
    return exp;
  }
  function statement(type, value) {
    if (type == "var") return cont(pushlex("vardef", value), vardef, expect(";"), poplex);
    if (type == "keyword a") return cont(pushlex("form"), parenExpr, statement, poplex);
    if (type == "keyword b") return cont(pushlex("form"), statement, poplex);
    if (type == "keyword d") return cx.stream.match(/^\s*$/, false) ? cont() : cont(pushlex("stat"), maybeexpression, expect(";"), poplex);
    if (type == "debugger") return cont(expect(";"));
    if (type == "{") return cont(pushlex("}"), pushblockcontext, block, poplex, popcontext);
    if (type == ";") return cont();
    if (type == "if") {
      if (cx.state.lexical.info == "else" && cx.state.cc[cx.state.cc.length - 1] == poplex) cx.state.cc.pop()();
      return cont(pushlex("form"), parenExpr, statement, poplex, maybeelse);
    }
    if (type == "function") return cont(functiondef);
    if (type == "for") return cont(pushlex("form"), pushblockcontext, forspec, statement, popcontext, poplex);
    if (type == "class" || isTS && value == "interface") {
      cx.marked = "keyword";
      return cont(pushlex("form", type == "class" ? type : value), className, poplex);
    }
    if (type == "variable") {
      if (isTS && value == "declare") {
        cx.marked = "keyword";
        return cont(statement);
      } else if (isTS && (value == "module" || value == "enum" || value == "type") && cx.stream.match(/^\s*\w/, false)) {
        cx.marked = "keyword";
        if (value == "enum") return cont(enumdef);else if (value == "type") return cont(typename, expect("operator"), typeexpr, expect(";"));else return cont(pushlex("form"), pattern, expect("{"), pushlex("}"), block, poplex, poplex);
      } else if (isTS && value == "namespace") {
        cx.marked = "keyword";
        return cont(pushlex("form"), expression, statement, poplex);
      } else if (isTS && value == "abstract") {
        cx.marked = "keyword";
        return cont(statement);
      } else {
        return cont(pushlex("stat"), maybelabel);
      }
    }
    if (type == "switch") return cont(pushlex("form"), parenExpr, expect("{"), pushlex("}", "switch"), pushblockcontext, block, poplex, poplex, popcontext);
    if (type == "case") return cont(expression, expect(":"));
    if (type == "default") return cont(expect(":"));
    if (type == "catch") return cont(pushlex("form"), pushcontext, maybeCatchBinding, statement, poplex, popcontext);
    if (type == "export") return cont(pushlex("stat"), afterExport, poplex);
    if (type == "import") return cont(pushlex("stat"), afterImport, poplex);
    if (type == "async") return cont(statement);
    if (value == "@") return cont(expression, statement);
    return pass(pushlex("stat"), expression, expect(";"), poplex);
  }
  function maybeCatchBinding(type) {
    if (type == "(") return cont(funarg, expect(")"));
  }
  function expression(type, value) {
    return expressionInner(type, value, false);
  }
  function expressionNoComma(type, value) {
    return expressionInner(type, value, true);
  }
  function parenExpr(type) {
    if (type != "(") return pass();
    return cont(pushlex(")"), maybeexpression, expect(")"), poplex);
  }
  function expressionInner(type, value, noComma) {
    if (cx.state.fatArrowAt == cx.stream.start) {
      var body = noComma ? arrowBodyNoComma : arrowBody;
      if (type == "(") return cont(pushcontext, pushlex(")"), commasep(funarg, ")"), poplex, expect("=>"), body, popcontext);else if (type == "variable") return pass(pushcontext, pattern, expect("=>"), body, popcontext);
    }
    var maybeop = noComma ? maybeoperatorNoComma : maybeoperatorComma;
    if (atomicTypes.hasOwnProperty(type)) return cont(maybeop);
    if (type == "function") return cont(functiondef, maybeop);
    if (type == "class" || isTS && value == "interface") {
      cx.marked = "keyword";
      return cont(pushlex("form"), classExpression, poplex);
    }
    if (type == "keyword c" || type == "async") return cont(noComma ? expressionNoComma : expression);
    if (type == "(") return cont(pushlex(")"), maybeexpression, expect(")"), poplex, maybeop);
    if (type == "operator" || type == "spread") return cont(noComma ? expressionNoComma : expression);
    if (type == "[") return cont(pushlex("]"), arrayLiteral, poplex, maybeop);
    if (type == "{") return contCommasep(objprop, "}", null, maybeop);
    if (type == "quasi") return pass(quasi, maybeop);
    if (type == "new") return cont(maybeTarget(noComma));
    return cont();
  }
  function maybeexpression(type) {
    if (type.match(/[;\}\)\],]/)) return pass();
    return pass(expression);
  }
  function maybeoperatorComma(type, value) {
    if (type == ",") return cont(maybeexpression);
    return maybeoperatorNoComma(type, value, false);
  }
  function maybeoperatorNoComma(type, value, noComma) {
    var me = noComma == false ? maybeoperatorComma : maybeoperatorNoComma;
    var expr = noComma == false ? expression : expressionNoComma;
    if (type == "=>") return cont(pushcontext, noComma ? arrowBodyNoComma : arrowBody, popcontext);
    if (type == "operator") {
      if (/\+\+|--/.test(value) || isTS && value == "!") return cont(me);
      if (isTS && value == "<" && cx.stream.match(/^([^<>]|<[^<>]*>)*>\s*\(/, false)) return cont(pushlex(">"), commasep(typeexpr, ">"), poplex, me);
      if (value == "?") return cont(expression, expect(":"), expr);
      return cont(expr);
    }
    if (type == "quasi") {
      return pass(quasi, me);
    }
    if (type == ";") return;
    if (type == "(") return contCommasep(expressionNoComma, ")", "call", me);
    if (type == ".") return cont(property, me);
    if (type == "[") return cont(pushlex("]"), maybeexpression, expect("]"), poplex, me);
    if (isTS && value == "as") {
      cx.marked = "keyword";
      return cont(typeexpr, me);
    }
    if (type == "regexp") {
      cx.state.lastType = cx.marked = "operator";
      cx.stream.backUp(cx.stream.pos - cx.stream.start - 1);
      return cont(expr);
    }
  }
  function quasi(type, value) {
    if (type != "quasi") return pass();
    if (value.slice(value.length - 2) != "${") return cont(quasi);
    return cont(maybeexpression, continueQuasi);
  }
  function continueQuasi(type) {
    if (type == "}") {
      cx.marked = "string.special";
      cx.state.tokenize = tokenQuasi;
      return cont(quasi);
    }
  }
  function arrowBody(type) {
    findFatArrow(cx.stream, cx.state);
    return pass(type == "{" ? statement : expression);
  }
  function arrowBodyNoComma(type) {
    findFatArrow(cx.stream, cx.state);
    return pass(type == "{" ? statement : expressionNoComma);
  }
  function maybeTarget(noComma) {
    return function (type) {
      if (type == ".") return cont(noComma ? targetNoComma : target);else if (type == "variable" && isTS) return cont(maybeTypeArgs, noComma ? maybeoperatorNoComma : maybeoperatorComma);else return pass(noComma ? expressionNoComma : expression);
    };
  }
  function target(_, value) {
    if (value == "target") {
      cx.marked = "keyword";
      return cont(maybeoperatorComma);
    }
  }
  function targetNoComma(_, value) {
    if (value == "target") {
      cx.marked = "keyword";
      return cont(maybeoperatorNoComma);
    }
  }
  function maybelabel(type) {
    if (type == ":") return cont(poplex, statement);
    return pass(maybeoperatorComma, expect(";"), poplex);
  }
  function property(type) {
    if (type == "variable") {
      cx.marked = "property";
      return cont();
    }
  }
  function objprop(type, value) {
    if (type == "async") {
      cx.marked = "property";
      return cont(objprop);
    } else if (type == "variable" || cx.style == "keyword") {
      cx.marked = "property";
      if (value == "get" || value == "set") return cont(getterSetter);
      var m; // Work around fat-arrow-detection complication for detecting typescript typed arrow params
      if (isTS && cx.state.fatArrowAt == cx.stream.start && (m = cx.stream.match(/^\s*:\s*/, false))) cx.state.fatArrowAt = cx.stream.pos + m[0].length;
      return cont(afterprop);
    } else if (type == "number" || type == "string") {
      cx.marked = jsonldMode ? "property" : cx.style + " property";
      return cont(afterprop);
    } else if (type == "jsonld-keyword") {
      return cont(afterprop);
    } else if (isTS && isModifier(value)) {
      cx.marked = "keyword";
      return cont(objprop);
    } else if (type == "[") {
      return cont(expression, maybetype, expect("]"), afterprop);
    } else if (type == "spread") {
      return cont(expressionNoComma, afterprop);
    } else if (value == "*") {
      cx.marked = "keyword";
      return cont(objprop);
    } else if (type == ":") {
      return pass(afterprop);
    }
  }
  function getterSetter(type) {
    if (type != "variable") return pass(afterprop);
    cx.marked = "property";
    return cont(functiondef);
  }
  function afterprop(type) {
    if (type == ":") return cont(expressionNoComma);
    if (type == "(") return pass(functiondef);
  }
  function commasep(what, end, sep) {
    function proceed(type, value) {
      if (sep ? sep.indexOf(type) > -1 : type == ",") {
        var lex = cx.state.lexical;
        if (lex.info == "call") lex.pos = (lex.pos || 0) + 1;
        return cont(function (type, value) {
          if (type == end || value == end) return pass();
          return pass(what);
        }, proceed);
      }
      if (type == end || value == end) return cont();
      if (sep && sep.indexOf(";") > -1) return pass(what);
      return cont(expect(end));
    }
    return function (type, value) {
      if (type == end || value == end) return cont();
      return pass(what, proceed);
    };
  }
  function contCommasep(what, end, info) {
    for (var i = 3; i < arguments.length; i++) cx.cc.push(arguments[i]);
    return cont(pushlex(end, info), commasep(what, end), poplex);
  }
  function block(type) {
    if (type == "}") return cont();
    return pass(statement, block);
  }
  function maybetype(type, value) {
    if (isTS) {
      if (type == ":") return cont(typeexpr);
      if (value == "?") return cont(maybetype);
    }
  }
  function maybetypeOrIn(type, value) {
    if (isTS && (type == ":" || value == "in")) return cont(typeexpr);
  }
  function mayberettype(type) {
    if (isTS && type == ":") {
      if (cx.stream.match(/^\s*\w+\s+is\b/, false)) return cont(expression, isKW, typeexpr);else return cont(typeexpr);
    }
  }
  function isKW(_, value) {
    if (value == "is") {
      cx.marked = "keyword";
      return cont();
    }
  }
  function typeexpr(type, value) {
    if (value == "keyof" || value == "typeof" || value == "infer" || value == "readonly") {
      cx.marked = "keyword";
      return cont(value == "typeof" ? expressionNoComma : typeexpr);
    }
    if (type == "variable" || value == "void") {
      cx.marked = "type";
      return cont(afterType);
    }
    if (value == "|" || value == "&") return cont(typeexpr);
    if (type == "string" || type == "number" || type == "atom") return cont(afterType);
    if (type == "[") return cont(pushlex("]"), commasep(typeexpr, "]", ","), poplex, afterType);
    if (type == "{") return cont(pushlex("}"), typeprops, poplex, afterType);
    if (type == "(") return cont(commasep(typearg, ")"), maybeReturnType, afterType);
    if (type == "<") return cont(commasep(typeexpr, ">"), typeexpr);
    if (type == "quasi") return pass(quasiType, afterType);
  }
  function maybeReturnType(type) {
    if (type == "=>") return cont(typeexpr);
  }
  function typeprops(type) {
    if (type.match(/[\}\)\]]/)) return cont();
    if (type == "," || type == ";") return cont(typeprops);
    return pass(typeprop, typeprops);
  }
  function typeprop(type, value) {
    if (type == "variable" || cx.style == "keyword") {
      cx.marked = "property";
      return cont(typeprop);
    } else if (value == "?" || type == "number" || type == "string") {
      return cont(typeprop);
    } else if (type == ":") {
      return cont(typeexpr);
    } else if (type == "[") {
      return cont(expect("variable"), maybetypeOrIn, expect("]"), typeprop);
    } else if (type == "(") {
      return pass(functiondecl, typeprop);
    } else if (!type.match(/[;\}\)\],]/)) {
      return cont();
    }
  }
  function quasiType(type, value) {
    if (type != "quasi") return pass();
    if (value.slice(value.length - 2) != "${") return cont(quasiType);
    return cont(typeexpr, continueQuasiType);
  }
  function continueQuasiType(type) {
    if (type == "}") {
      cx.marked = "string.special";
      cx.state.tokenize = tokenQuasi;
      return cont(quasiType);
    }
  }
  function typearg(type, value) {
    if (type == "variable" && cx.stream.match(/^\s*[?:]/, false) || value == "?") return cont(typearg);
    if (type == ":") return cont(typeexpr);
    if (type == "spread") return cont(typearg);
    return pass(typeexpr);
  }
  function afterType(type, value) {
    if (value == "<") return cont(pushlex(">"), commasep(typeexpr, ">"), poplex, afterType);
    if (value == "|" || type == "." || value == "&") return cont(typeexpr);
    if (type == "[") return cont(typeexpr, expect("]"), afterType);
    if (value == "extends" || value == "implements") {
      cx.marked = "keyword";
      return cont(typeexpr);
    }
    if (value == "?") return cont(typeexpr, expect(":"), typeexpr);
  }
  function maybeTypeArgs(_, value) {
    if (value == "<") return cont(pushlex(">"), commasep(typeexpr, ">"), poplex, afterType);
  }
  function typeparam() {
    return pass(typeexpr, maybeTypeDefault);
  }
  function maybeTypeDefault(_, value) {
    if (value == "=") return cont(typeexpr);
  }
  function vardef(_, value) {
    if (value == "enum") {
      cx.marked = "keyword";
      return cont(enumdef);
    }
    return pass(pattern, maybetype, maybeAssign, vardefCont);
  }
  function pattern(type, value) {
    if (isTS && isModifier(value)) {
      cx.marked = "keyword";
      return cont(pattern);
    }
    if (type == "variable") {
      register(value);
      return cont();
    }
    if (type == "spread") return cont(pattern);
    if (type == "[") return contCommasep(eltpattern, "]");
    if (type == "{") return contCommasep(proppattern, "}");
  }
  function proppattern(type, value) {
    if (type == "variable" && !cx.stream.match(/^\s*:/, false)) {
      register(value);
      return cont(maybeAssign);
    }
    if (type == "variable") cx.marked = "property";
    if (type == "spread") return cont(pattern);
    if (type == "}") return pass();
    if (type == "[") return cont(expression, expect(']'), expect(':'), proppattern);
    return cont(expect(":"), pattern, maybeAssign);
  }
  function eltpattern() {
    return pass(pattern, maybeAssign);
  }
  function maybeAssign(_type, value) {
    if (value == "=") return cont(expressionNoComma);
  }
  function vardefCont(type) {
    if (type == ",") return cont(vardef);
  }
  function maybeelse(type, value) {
    if (type == "keyword b" && value == "else") return cont(pushlex("form", "else"), statement, poplex);
  }
  function forspec(type, value) {
    if (value == "await") return cont(forspec);
    if (type == "(") return cont(pushlex(")"), forspec1, poplex);
  }
  function forspec1(type) {
    if (type == "var") return cont(vardef, forspec2);
    if (type == "variable") return cont(forspec2);
    return pass(forspec2);
  }
  function forspec2(type, value) {
    if (type == ")") return cont();
    if (type == ";") return cont(forspec2);
    if (value == "in" || value == "of") {
      cx.marked = "keyword";
      return cont(expression, forspec2);
    }
    return pass(expression, forspec2);
  }
  function functiondef(type, value) {
    if (value == "*") {
      cx.marked = "keyword";
      return cont(functiondef);
    }
    if (type == "variable") {
      register(value);
      return cont(functiondef);
    }
    if (type == "(") return cont(pushcontext, pushlex(")"), commasep(funarg, ")"), poplex, mayberettype, statement, popcontext);
    if (isTS && value == "<") return cont(pushlex(">"), commasep(typeparam, ">"), poplex, functiondef);
  }
  function functiondecl(type, value) {
    if (value == "*") {
      cx.marked = "keyword";
      return cont(functiondecl);
    }
    if (type == "variable") {
      register(value);
      return cont(functiondecl);
    }
    if (type == "(") return cont(pushcontext, pushlex(")"), commasep(funarg, ")"), poplex, mayberettype, popcontext);
    if (isTS && value == "<") return cont(pushlex(">"), commasep(typeparam, ">"), poplex, functiondecl);
  }
  function typename(type, value) {
    if (type == "keyword" || type == "variable") {
      cx.marked = "type";
      return cont(typename);
    } else if (value == "<") {
      return cont(pushlex(">"), commasep(typeparam, ">"), poplex);
    }
  }
  function funarg(type, value) {
    if (value == "@") cont(expression, funarg);
    if (type == "spread") return cont(funarg);
    if (isTS && isModifier(value)) {
      cx.marked = "keyword";
      return cont(funarg);
    }
    if (isTS && type == "this") return cont(maybetype, maybeAssign);
    return pass(pattern, maybetype, maybeAssign);
  }
  function classExpression(type, value) {
    // Class expressions may have an optional name.
    if (type == "variable") return className(type, value);
    return classNameAfter(type, value);
  }
  function className(type, value) {
    if (type == "variable") {
      register(value);
      return cont(classNameAfter);
    }
  }
  function classNameAfter(type, value) {
    if (value == "<") return cont(pushlex(">"), commasep(typeparam, ">"), poplex, classNameAfter);
    if (value == "extends" || value == "implements" || isTS && type == ",") {
      if (value == "implements") cx.marked = "keyword";
      return cont(isTS ? typeexpr : expression, classNameAfter);
    }
    if (type == "{") return cont(pushlex("}"), classBody, poplex);
  }
  function classBody(type, value) {
    if (type == "async" || type == "variable" && (value == "static" || value == "get" || value == "set" || isTS && isModifier(value)) && cx.stream.match(/^\s+#?[\w$\xa1-\uffff]/, false)) {
      cx.marked = "keyword";
      return cont(classBody);
    }
    if (type == "variable" || cx.style == "keyword") {
      cx.marked = "property";
      return cont(classfield, classBody);
    }
    if (type == "number" || type == "string") return cont(classfield, classBody);
    if (type == "[") return cont(expression, maybetype, expect("]"), classfield, classBody);
    if (value == "*") {
      cx.marked = "keyword";
      return cont(classBody);
    }
    if (isTS && type == "(") return pass(functiondecl, classBody);
    if (type == ";" || type == ",") return cont(classBody);
    if (type == "}") return cont();
    if (value == "@") return cont(expression, classBody);
  }
  function classfield(type, value) {
    if (value == "!" || value == "?") return cont(classfield);
    if (type == ":") return cont(typeexpr, maybeAssign);
    if (value == "=") return cont(expressionNoComma);
    var context = cx.state.lexical.prev,
      isInterface = context && context.info == "interface";
    return pass(isInterface ? functiondecl : functiondef);
  }
  function afterExport(type, value) {
    if (value == "*") {
      cx.marked = "keyword";
      return cont(maybeFrom, expect(";"));
    }
    if (value == "default") {
      cx.marked = "keyword";
      return cont(expression, expect(";"));
    }
    if (type == "{") return cont(commasep(exportField, "}"), maybeFrom, expect(";"));
    return pass(statement);
  }
  function exportField(type, value) {
    if (value == "as") {
      cx.marked = "keyword";
      return cont(expect("variable"));
    }
    if (type == "variable") return pass(expressionNoComma, exportField);
  }
  function afterImport(type) {
    if (type == "string") return cont();
    if (type == "(") return pass(expression);
    if (type == ".") return pass(maybeoperatorComma);
    return pass(importSpec, maybeMoreImports, maybeFrom);
  }
  function importSpec(type, value) {
    if (type == "{") return contCommasep(importSpec, "}");
    if (type == "variable") register(value);
    if (value == "*") cx.marked = "keyword";
    return cont(maybeAs);
  }
  function maybeMoreImports(type) {
    if (type == ",") return cont(importSpec, maybeMoreImports);
  }
  function maybeAs(_type, value) {
    if (value == "as") {
      cx.marked = "keyword";
      return cont(importSpec);
    }
  }
  function maybeFrom(_type, value) {
    if (value == "from") {
      cx.marked = "keyword";
      return cont(expression);
    }
  }
  function arrayLiteral(type) {
    if (type == "]") return cont();
    return pass(commasep(expressionNoComma, "]"));
  }
  function enumdef() {
    return pass(pushlex("form"), pattern, expect("{"), pushlex("}"), commasep(enummember, "}"), poplex, poplex);
  }
  function enummember() {
    return pass(pattern, maybeAssign);
  }
  function isContinuedStatement(state, textAfter) {
    return state.lastType == "operator" || state.lastType == "," || isOperatorChar.test(textAfter.charAt(0)) || /[,.]/.test(textAfter.charAt(0));
  }
  function expressionAllowed(stream, state, backUp) {
    return state.tokenize == tokenBase && /^(?:operator|sof|keyword [bcd]|case|new|export|default|spread|[\[{}\(,;:]|=>)$/.test(state.lastType) || state.lastType == "quasi" && /\{\s*$/.test(stream.string.slice(0, stream.pos - (backUp || 0)));
  }

  // Interface

  return {
    name: parserConfig.name,
    startState: function (indentUnit) {
      var state = {
        tokenize: tokenBase,
        lastType: "sof",
        cc: [],
        lexical: new JSLexical(-indentUnit, 0, "block", false),
        localVars: parserConfig.localVars,
        context: parserConfig.localVars && new Context(null, null, false),
        indented: 0
      };
      if (parserConfig.globalVars && typeof parserConfig.globalVars == "object") state.globalVars = parserConfig.globalVars;
      return state;
    },
    token: function (stream, state) {
      if (stream.sol()) {
        if (!state.lexical.hasOwnProperty("align")) state.lexical.align = false;
        state.indented = stream.indentation();
        findFatArrow(stream, state);
      }
      if (state.tokenize != tokenComment && stream.eatSpace()) return null;
      var style = state.tokenize(stream, state);
      if (type == "comment") return style;
      state.lastType = type == "operator" && (content == "++" || content == "--") ? "incdec" : type;
      return parseJS(state, style, type, content, stream);
    },
    indent: function (state, textAfter, cx) {
      if (state.tokenize == tokenComment || state.tokenize == tokenQuasi) return null;
      if (state.tokenize != tokenBase) return 0;
      var firstChar = textAfter && textAfter.charAt(0),
        lexical = state.lexical,
        top;
      // Kludge to prevent 'maybelse' from blocking lexical scope pops
      if (!/^\s*else\b/.test(textAfter)) for (var i = state.cc.length - 1; i >= 0; --i) {
        var c = state.cc[i];
        if (c == poplex) lexical = lexical.prev;else if (c != maybeelse && c != popcontext) break;
      }
      while ((lexical.type == "stat" || lexical.type == "form") && (firstChar == "}" || (top = state.cc[state.cc.length - 1]) && (top == maybeoperatorComma || top == maybeoperatorNoComma) && !/^[,\.=+\-*:?[\(]/.test(textAfter))) lexical = lexical.prev;
      if (statementIndent && lexical.type == ")" && lexical.prev.type == "stat") lexical = lexical.prev;
      var type = lexical.type,
        closing = firstChar == type;
      if (type == "vardef") return lexical.indented + (state.lastType == "operator" || state.lastType == "," ? lexical.info.length + 1 : 0);else if (type == "form" && firstChar == "{") return lexical.indented;else if (type == "form") return lexical.indented + cx.unit;else if (type == "stat") return lexical.indented + (isContinuedStatement(state, textAfter) ? statementIndent || cx.unit : 0);else if (lexical.info == "switch" && !closing && parserConfig.doubleIndentSwitch != false) return lexical.indented + (/^(?:case|default)\b/.test(textAfter) ? cx.unit : 2 * cx.unit);else if (lexical.align) return lexical.column + (closing ? 0 : 1);else return lexical.indented + (closing ? 0 : cx.unit);
    },
    languageData: {
      indentOnInput: /^\s*(?:case .*?:|default:|\{|\})$/,
      commentTokens: jsonMode ? undefined : {
        line: "//",
        block: {
          open: "/*",
          close: "*/"
        }
      },
      closeBrackets: {
        brackets: ["(", "[", "{", "'", '"', "`"]
      },
      wordChars: "$"
    }
  };
}
;
const javascript = mkJavaScript({
  name: "javascript"
});
const json = mkJavaScript({
  name: "json",
  json: true
});
const jsonld = mkJavaScript({
  name: "json",
  jsonld: true
});
const typescript = mkJavaScript({
  name: "typescript",
  typescript: true
});

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiMjU0OC5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL0Bjb2RlbWlycm9yL2xlZ2FjeS1tb2Rlcy9tb2RlL2phdmFzY3JpcHQuanMiXSwic291cmNlc0NvbnRlbnQiOlsiZnVuY3Rpb24gbWtKYXZhU2NyaXB0KHBhcnNlckNvbmZpZykge1xuICB2YXIgc3RhdGVtZW50SW5kZW50ID0gcGFyc2VyQ29uZmlnLnN0YXRlbWVudEluZGVudDtcbiAgdmFyIGpzb25sZE1vZGUgPSBwYXJzZXJDb25maWcuanNvbmxkO1xuICB2YXIganNvbk1vZGUgPSBwYXJzZXJDb25maWcuanNvbiB8fCBqc29ubGRNb2RlO1xuICB2YXIgaXNUUyA9IHBhcnNlckNvbmZpZy50eXBlc2NyaXB0O1xuICB2YXIgd29yZFJFID0gcGFyc2VyQ29uZmlnLndvcmRDaGFyYWN0ZXJzIHx8IC9bXFx3JFxceGExLVxcdWZmZmZdLztcblxuICAvLyBUb2tlbml6ZXJcblxuICB2YXIga2V5d29yZHMgPSBmdW5jdGlvbiAoKSB7XG4gICAgZnVuY3Rpb24ga3codHlwZSkge1xuICAgICAgcmV0dXJuIHtcbiAgICAgICAgdHlwZTogdHlwZSxcbiAgICAgICAgc3R5bGU6IFwia2V5d29yZFwiXG4gICAgICB9O1xuICAgIH1cbiAgICB2YXIgQSA9IGt3KFwia2V5d29yZCBhXCIpLFxuICAgICAgQiA9IGt3KFwia2V5d29yZCBiXCIpLFxuICAgICAgQyA9IGt3KFwia2V5d29yZCBjXCIpLFxuICAgICAgRCA9IGt3KFwia2V5d29yZCBkXCIpO1xuICAgIHZhciBvcGVyYXRvciA9IGt3KFwib3BlcmF0b3JcIiksXG4gICAgICBhdG9tID0ge1xuICAgICAgICB0eXBlOiBcImF0b21cIixcbiAgICAgICAgc3R5bGU6IFwiYXRvbVwiXG4gICAgICB9O1xuICAgIHJldHVybiB7XG4gICAgICBcImlmXCI6IGt3KFwiaWZcIiksXG4gICAgICBcIndoaWxlXCI6IEEsXG4gICAgICBcIndpdGhcIjogQSxcbiAgICAgIFwiZWxzZVwiOiBCLFxuICAgICAgXCJkb1wiOiBCLFxuICAgICAgXCJ0cnlcIjogQixcbiAgICAgIFwiZmluYWxseVwiOiBCLFxuICAgICAgXCJyZXR1cm5cIjogRCxcbiAgICAgIFwiYnJlYWtcIjogRCxcbiAgICAgIFwiY29udGludWVcIjogRCxcbiAgICAgIFwibmV3XCI6IGt3KFwibmV3XCIpLFxuICAgICAgXCJkZWxldGVcIjogQyxcbiAgICAgIFwidm9pZFwiOiBDLFxuICAgICAgXCJ0aHJvd1wiOiBDLFxuICAgICAgXCJkZWJ1Z2dlclwiOiBrdyhcImRlYnVnZ2VyXCIpLFxuICAgICAgXCJ2YXJcIjoga3coXCJ2YXJcIiksXG4gICAgICBcImNvbnN0XCI6IGt3KFwidmFyXCIpLFxuICAgICAgXCJsZXRcIjoga3coXCJ2YXJcIiksXG4gICAgICBcImZ1bmN0aW9uXCI6IGt3KFwiZnVuY3Rpb25cIiksXG4gICAgICBcImNhdGNoXCI6IGt3KFwiY2F0Y2hcIiksXG4gICAgICBcImZvclwiOiBrdyhcImZvclwiKSxcbiAgICAgIFwic3dpdGNoXCI6IGt3KFwic3dpdGNoXCIpLFxuICAgICAgXCJjYXNlXCI6IGt3KFwiY2FzZVwiKSxcbiAgICAgIFwiZGVmYXVsdFwiOiBrdyhcImRlZmF1bHRcIiksXG4gICAgICBcImluXCI6IG9wZXJhdG9yLFxuICAgICAgXCJ0eXBlb2ZcIjogb3BlcmF0b3IsXG4gICAgICBcImluc3RhbmNlb2ZcIjogb3BlcmF0b3IsXG4gICAgICBcInRydWVcIjogYXRvbSxcbiAgICAgIFwiZmFsc2VcIjogYXRvbSxcbiAgICAgIFwibnVsbFwiOiBhdG9tLFxuICAgICAgXCJ1bmRlZmluZWRcIjogYXRvbSxcbiAgICAgIFwiTmFOXCI6IGF0b20sXG4gICAgICBcIkluZmluaXR5XCI6IGF0b20sXG4gICAgICBcInRoaXNcIjoga3coXCJ0aGlzXCIpLFxuICAgICAgXCJjbGFzc1wiOiBrdyhcImNsYXNzXCIpLFxuICAgICAgXCJzdXBlclwiOiBrdyhcImF0b21cIiksXG4gICAgICBcInlpZWxkXCI6IEMsXG4gICAgICBcImV4cG9ydFwiOiBrdyhcImV4cG9ydFwiKSxcbiAgICAgIFwiaW1wb3J0XCI6IGt3KFwiaW1wb3J0XCIpLFxuICAgICAgXCJleHRlbmRzXCI6IEMsXG4gICAgICBcImF3YWl0XCI6IENcbiAgICB9O1xuICB9KCk7XG4gIHZhciBpc09wZXJhdG9yQ2hhciA9IC9bK1xcLSomJT08PiE/fH5eQF0vO1xuICB2YXIgaXNKc29ubGRLZXl3b3JkID0gL15AKGNvbnRleHR8aWR8dmFsdWV8bGFuZ3VhZ2V8dHlwZXxjb250YWluZXJ8bGlzdHxzZXR8cmV2ZXJzZXxpbmRleHxiYXNlfHZvY2FifGdyYXBoKVwiLztcbiAgZnVuY3Rpb24gcmVhZFJlZ2V4cChzdHJlYW0pIHtcbiAgICB2YXIgZXNjYXBlZCA9IGZhbHNlLFxuICAgICAgbmV4dCxcbiAgICAgIGluU2V0ID0gZmFsc2U7XG4gICAgd2hpbGUgKChuZXh0ID0gc3RyZWFtLm5leHQoKSkgIT0gbnVsbCkge1xuICAgICAgaWYgKCFlc2NhcGVkKSB7XG4gICAgICAgIGlmIChuZXh0ID09IFwiL1wiICYmICFpblNldCkgcmV0dXJuO1xuICAgICAgICBpZiAobmV4dCA9PSBcIltcIikgaW5TZXQgPSB0cnVlO2Vsc2UgaWYgKGluU2V0ICYmIG5leHQgPT0gXCJdXCIpIGluU2V0ID0gZmFsc2U7XG4gICAgICB9XG4gICAgICBlc2NhcGVkID0gIWVzY2FwZWQgJiYgbmV4dCA9PSBcIlxcXFxcIjtcbiAgICB9XG4gIH1cblxuICAvLyBVc2VkIGFzIHNjcmF0Y2ggdmFyaWFibGVzIHRvIGNvbW11bmljYXRlIG11bHRpcGxlIHZhbHVlcyB3aXRob3V0XG4gIC8vIGNvbnNpbmcgdXAgdG9ucyBvZiBvYmplY3RzLlxuICB2YXIgdHlwZSwgY29udGVudDtcbiAgZnVuY3Rpb24gcmV0KHRwLCBzdHlsZSwgY29udCkge1xuICAgIHR5cGUgPSB0cDtcbiAgICBjb250ZW50ID0gY29udDtcbiAgICByZXR1cm4gc3R5bGU7XG4gIH1cbiAgZnVuY3Rpb24gdG9rZW5CYXNlKHN0cmVhbSwgc3RhdGUpIHtcbiAgICB2YXIgY2ggPSBzdHJlYW0ubmV4dCgpO1xuICAgIGlmIChjaCA9PSAnXCInIHx8IGNoID09IFwiJ1wiKSB7XG4gICAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuU3RyaW5nKGNoKTtcbiAgICAgIHJldHVybiBzdGF0ZS50b2tlbml6ZShzdHJlYW0sIHN0YXRlKTtcbiAgICB9IGVsc2UgaWYgKGNoID09IFwiLlwiICYmIHN0cmVhbS5tYXRjaCgvXlxcZFtcXGRfXSooPzpbZUVdWytcXC1dP1tcXGRfXSspPy8pKSB7XG4gICAgICByZXR1cm4gcmV0KFwibnVtYmVyXCIsIFwibnVtYmVyXCIpO1xuICAgIH0gZWxzZSBpZiAoY2ggPT0gXCIuXCIgJiYgc3RyZWFtLm1hdGNoKFwiLi5cIikpIHtcbiAgICAgIHJldHVybiByZXQoXCJzcHJlYWRcIiwgXCJtZXRhXCIpO1xuICAgIH0gZWxzZSBpZiAoL1tcXFtcXF17fVxcKFxcKSw7XFw6XFwuXS8udGVzdChjaCkpIHtcbiAgICAgIHJldHVybiByZXQoY2gpO1xuICAgIH0gZWxzZSBpZiAoY2ggPT0gXCI9XCIgJiYgc3RyZWFtLmVhdChcIj5cIikpIHtcbiAgICAgIHJldHVybiByZXQoXCI9PlwiLCBcIm9wZXJhdG9yXCIpO1xuICAgIH0gZWxzZSBpZiAoY2ggPT0gXCIwXCIgJiYgc3RyZWFtLm1hdGNoKC9eKD86eFtcXGRBLUZhLWZfXSt8b1swLTdfXSt8YlswMV9dKyluPy8pKSB7XG4gICAgICByZXR1cm4gcmV0KFwibnVtYmVyXCIsIFwibnVtYmVyXCIpO1xuICAgIH0gZWxzZSBpZiAoL1xcZC8udGVzdChjaCkpIHtcbiAgICAgIHN0cmVhbS5tYXRjaCgvXltcXGRfXSooPzpufCg/OlxcLltcXGRfXSopPyg/OltlRV1bK1xcLV0/W1xcZF9dKyk/KT8vKTtcbiAgICAgIHJldHVybiByZXQoXCJudW1iZXJcIiwgXCJudW1iZXJcIik7XG4gICAgfSBlbHNlIGlmIChjaCA9PSBcIi9cIikge1xuICAgICAgaWYgKHN0cmVhbS5lYXQoXCIqXCIpKSB7XG4gICAgICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5Db21tZW50O1xuICAgICAgICByZXR1cm4gdG9rZW5Db21tZW50KHN0cmVhbSwgc3RhdGUpO1xuICAgICAgfSBlbHNlIGlmIChzdHJlYW0uZWF0KFwiL1wiKSkge1xuICAgICAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgICAgIHJldHVybiByZXQoXCJjb21tZW50XCIsIFwiY29tbWVudFwiKTtcbiAgICAgIH0gZWxzZSBpZiAoZXhwcmVzc2lvbkFsbG93ZWQoc3RyZWFtLCBzdGF0ZSwgMSkpIHtcbiAgICAgICAgcmVhZFJlZ2V4cChzdHJlYW0pO1xuICAgICAgICBzdHJlYW0ubWF0Y2goL15cXGIoKFtnaW15dXNdKSg/IVtnaW15dXNdKlxcMikpK1xcYi8pO1xuICAgICAgICByZXR1cm4gcmV0KFwicmVnZXhwXCIsIFwic3RyaW5nLnNwZWNpYWxcIik7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBzdHJlYW0uZWF0KFwiPVwiKTtcbiAgICAgICAgcmV0dXJuIHJldChcIm9wZXJhdG9yXCIsIFwib3BlcmF0b3JcIiwgc3RyZWFtLmN1cnJlbnQoKSk7XG4gICAgICB9XG4gICAgfSBlbHNlIGlmIChjaCA9PSBcImBcIikge1xuICAgICAgc3RhdGUudG9rZW5pemUgPSB0b2tlblF1YXNpO1xuICAgICAgcmV0dXJuIHRva2VuUXVhc2koc3RyZWFtLCBzdGF0ZSk7XG4gICAgfSBlbHNlIGlmIChjaCA9PSBcIiNcIiAmJiBzdHJlYW0ucGVlaygpID09IFwiIVwiKSB7XG4gICAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgICByZXR1cm4gcmV0KFwibWV0YVwiLCBcIm1ldGFcIik7XG4gICAgfSBlbHNlIGlmIChjaCA9PSBcIiNcIiAmJiBzdHJlYW0uZWF0V2hpbGUod29yZFJFKSkge1xuICAgICAgcmV0dXJuIHJldChcInZhcmlhYmxlXCIsIFwicHJvcGVydHlcIik7XG4gICAgfSBlbHNlIGlmIChjaCA9PSBcIjxcIiAmJiBzdHJlYW0ubWF0Y2goXCIhLS1cIikgfHwgY2ggPT0gXCItXCIgJiYgc3RyZWFtLm1hdGNoKFwiLT5cIikgJiYgIS9cXFMvLnRlc3Qoc3RyZWFtLnN0cmluZy5zbGljZSgwLCBzdHJlYW0uc3RhcnQpKSkge1xuICAgICAgc3RyZWFtLnNraXBUb0VuZCgpO1xuICAgICAgcmV0dXJuIHJldChcImNvbW1lbnRcIiwgXCJjb21tZW50XCIpO1xuICAgIH0gZWxzZSBpZiAoaXNPcGVyYXRvckNoYXIudGVzdChjaCkpIHtcbiAgICAgIGlmIChjaCAhPSBcIj5cIiB8fCAhc3RhdGUubGV4aWNhbCB8fCBzdGF0ZS5sZXhpY2FsLnR5cGUgIT0gXCI+XCIpIHtcbiAgICAgICAgaWYgKHN0cmVhbS5lYXQoXCI9XCIpKSB7XG4gICAgICAgICAgaWYgKGNoID09IFwiIVwiIHx8IGNoID09IFwiPVwiKSBzdHJlYW0uZWF0KFwiPVwiKTtcbiAgICAgICAgfSBlbHNlIGlmICgvWzw+KitcXC18Jj9dLy50ZXN0KGNoKSkge1xuICAgICAgICAgIHN0cmVhbS5lYXQoY2gpO1xuICAgICAgICAgIGlmIChjaCA9PSBcIj5cIikgc3RyZWFtLmVhdChjaCk7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICAgIGlmIChjaCA9PSBcIj9cIiAmJiBzdHJlYW0uZWF0KFwiLlwiKSkgcmV0dXJuIHJldChcIi5cIik7XG4gICAgICByZXR1cm4gcmV0KFwib3BlcmF0b3JcIiwgXCJvcGVyYXRvclwiLCBzdHJlYW0uY3VycmVudCgpKTtcbiAgICB9IGVsc2UgaWYgKHdvcmRSRS50ZXN0KGNoKSkge1xuICAgICAgc3RyZWFtLmVhdFdoaWxlKHdvcmRSRSk7XG4gICAgICB2YXIgd29yZCA9IHN0cmVhbS5jdXJyZW50KCk7XG4gICAgICBpZiAoc3RhdGUubGFzdFR5cGUgIT0gXCIuXCIpIHtcbiAgICAgICAgaWYgKGtleXdvcmRzLnByb3BlcnR5SXNFbnVtZXJhYmxlKHdvcmQpKSB7XG4gICAgICAgICAgdmFyIGt3ID0ga2V5d29yZHNbd29yZF07XG4gICAgICAgICAgcmV0dXJuIHJldChrdy50eXBlLCBrdy5zdHlsZSwgd29yZCk7XG4gICAgICAgIH1cbiAgICAgICAgaWYgKHdvcmQgPT0gXCJhc3luY1wiICYmIHN0cmVhbS5tYXRjaCgvXihcXHN8XFwvXFwqKFteKl18XFwqKD8hXFwvKSkqP1xcKlxcLykqW1xcW1xcKFxcd10vLCBmYWxzZSkpIHJldHVybiByZXQoXCJhc3luY1wiLCBcImtleXdvcmRcIiwgd29yZCk7XG4gICAgICB9XG4gICAgICByZXR1cm4gcmV0KFwidmFyaWFibGVcIiwgXCJ2YXJpYWJsZVwiLCB3b3JkKTtcbiAgICB9XG4gIH1cbiAgZnVuY3Rpb24gdG9rZW5TdHJpbmcocXVvdGUpIHtcbiAgICByZXR1cm4gZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICAgIHZhciBlc2NhcGVkID0gZmFsc2UsXG4gICAgICAgIG5leHQ7XG4gICAgICBpZiAoanNvbmxkTW9kZSAmJiBzdHJlYW0ucGVlaygpID09IFwiQFwiICYmIHN0cmVhbS5tYXRjaChpc0pzb25sZEtleXdvcmQpKSB7XG4gICAgICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlO1xuICAgICAgICByZXR1cm4gcmV0KFwianNvbmxkLWtleXdvcmRcIiwgXCJtZXRhXCIpO1xuICAgICAgfVxuICAgICAgd2hpbGUgKChuZXh0ID0gc3RyZWFtLm5leHQoKSkgIT0gbnVsbCkge1xuICAgICAgICBpZiAobmV4dCA9PSBxdW90ZSAmJiAhZXNjYXBlZCkgYnJlYWs7XG4gICAgICAgIGVzY2FwZWQgPSAhZXNjYXBlZCAmJiBuZXh0ID09IFwiXFxcXFwiO1xuICAgICAgfVxuICAgICAgaWYgKCFlc2NhcGVkKSBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQmFzZTtcbiAgICAgIHJldHVybiByZXQoXCJzdHJpbmdcIiwgXCJzdHJpbmdcIik7XG4gICAgfTtcbiAgfVxuICBmdW5jdGlvbiB0b2tlbkNvbW1lbnQoc3RyZWFtLCBzdGF0ZSkge1xuICAgIHZhciBtYXliZUVuZCA9IGZhbHNlLFxuICAgICAgY2g7XG4gICAgd2hpbGUgKGNoID0gc3RyZWFtLm5leHQoKSkge1xuICAgICAgaWYgKGNoID09IFwiL1wiICYmIG1heWJlRW5kKSB7XG4gICAgICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlO1xuICAgICAgICBicmVhaztcbiAgICAgIH1cbiAgICAgIG1heWJlRW5kID0gY2ggPT0gXCIqXCI7XG4gICAgfVxuICAgIHJldHVybiByZXQoXCJjb21tZW50XCIsIFwiY29tbWVudFwiKTtcbiAgfVxuICBmdW5jdGlvbiB0b2tlblF1YXNpKHN0cmVhbSwgc3RhdGUpIHtcbiAgICB2YXIgZXNjYXBlZCA9IGZhbHNlLFxuICAgICAgbmV4dDtcbiAgICB3aGlsZSAoKG5leHQgPSBzdHJlYW0ubmV4dCgpKSAhPSBudWxsKSB7XG4gICAgICBpZiAoIWVzY2FwZWQgJiYgKG5leHQgPT0gXCJgXCIgfHwgbmV4dCA9PSBcIiRcIiAmJiBzdHJlYW0uZWF0KFwie1wiKSkpIHtcbiAgICAgICAgc3RhdGUudG9rZW5pemUgPSB0b2tlbkJhc2U7XG4gICAgICAgIGJyZWFrO1xuICAgICAgfVxuICAgICAgZXNjYXBlZCA9ICFlc2NhcGVkICYmIG5leHQgPT0gXCJcXFxcXCI7XG4gICAgfVxuICAgIHJldHVybiByZXQoXCJxdWFzaVwiLCBcInN0cmluZy5zcGVjaWFsXCIsIHN0cmVhbS5jdXJyZW50KCkpO1xuICB9XG4gIHZhciBicmFja2V0cyA9IFwiKFt7fV0pXCI7XG4gIC8vIFRoaXMgaXMgYSBjcnVkZSBsb29rYWhlYWQgdHJpY2sgdG8gdHJ5IGFuZCBub3RpY2UgdGhhdCB3ZSdyZVxuICAvLyBwYXJzaW5nIHRoZSBhcmd1bWVudCBwYXR0ZXJucyBmb3IgYSBmYXQtYXJyb3cgZnVuY3Rpb24gYmVmb3JlIHdlXG4gIC8vIGFjdHVhbGx5IGhpdCB0aGUgYXJyb3cgdG9rZW4uIEl0IG9ubHkgd29ya3MgaWYgdGhlIGFycm93IGlzIG9uXG4gIC8vIHRoZSBzYW1lIGxpbmUgYXMgdGhlIGFyZ3VtZW50cyBhbmQgdGhlcmUncyBubyBzdHJhbmdlIG5vaXNlXG4gIC8vIChjb21tZW50cykgaW4gYmV0d2Vlbi4gRmFsbGJhY2sgaXMgdG8gb25seSBub3RpY2Ugd2hlbiB3ZSBoaXQgdGhlXG4gIC8vIGFycm93LCBhbmQgbm90IGRlY2xhcmUgdGhlIGFyZ3VtZW50cyBhcyBsb2NhbHMgZm9yIHRoZSBhcnJvd1xuICAvLyBib2R5LlxuICBmdW5jdGlvbiBmaW5kRmF0QXJyb3coc3RyZWFtLCBzdGF0ZSkge1xuICAgIGlmIChzdGF0ZS5mYXRBcnJvd0F0KSBzdGF0ZS5mYXRBcnJvd0F0ID0gbnVsbDtcbiAgICB2YXIgYXJyb3cgPSBzdHJlYW0uc3RyaW5nLmluZGV4T2YoXCI9PlwiLCBzdHJlYW0uc3RhcnQpO1xuICAgIGlmIChhcnJvdyA8IDApIHJldHVybjtcbiAgICBpZiAoaXNUUykge1xuICAgICAgLy8gVHJ5IHRvIHNraXAgVHlwZVNjcmlwdCByZXR1cm4gdHlwZSBkZWNsYXJhdGlvbnMgYWZ0ZXIgdGhlIGFyZ3VtZW50c1xuICAgICAgdmFyIG0gPSAvOlxccyooPzpcXHcrKD86PFtePl0qPnxcXFtcXF0pP3xcXHtbXn1dKlxcfSlcXHMqJC8uZXhlYyhzdHJlYW0uc3RyaW5nLnNsaWNlKHN0cmVhbS5zdGFydCwgYXJyb3cpKTtcbiAgICAgIGlmIChtKSBhcnJvdyA9IG0uaW5kZXg7XG4gICAgfVxuICAgIHZhciBkZXB0aCA9IDAsXG4gICAgICBzYXdTb21ldGhpbmcgPSBmYWxzZTtcbiAgICBmb3IgKHZhciBwb3MgPSBhcnJvdyAtIDE7IHBvcyA+PSAwOyAtLXBvcykge1xuICAgICAgdmFyIGNoID0gc3RyZWFtLnN0cmluZy5jaGFyQXQocG9zKTtcbiAgICAgIHZhciBicmFja2V0ID0gYnJhY2tldHMuaW5kZXhPZihjaCk7XG4gICAgICBpZiAoYnJhY2tldCA+PSAwICYmIGJyYWNrZXQgPCAzKSB7XG4gICAgICAgIGlmICghZGVwdGgpIHtcbiAgICAgICAgICArK3BvcztcbiAgICAgICAgICBicmVhaztcbiAgICAgICAgfVxuICAgICAgICBpZiAoLS1kZXB0aCA9PSAwKSB7XG4gICAgICAgICAgaWYgKGNoID09IFwiKFwiKSBzYXdTb21ldGhpbmcgPSB0cnVlO1xuICAgICAgICAgIGJyZWFrO1xuICAgICAgICB9XG4gICAgICB9IGVsc2UgaWYgKGJyYWNrZXQgPj0gMyAmJiBicmFja2V0IDwgNikge1xuICAgICAgICArK2RlcHRoO1xuICAgICAgfSBlbHNlIGlmICh3b3JkUkUudGVzdChjaCkpIHtcbiAgICAgICAgc2F3U29tZXRoaW5nID0gdHJ1ZTtcbiAgICAgIH0gZWxzZSBpZiAoL1tcIidcXC9gXS8udGVzdChjaCkpIHtcbiAgICAgICAgZm9yICg7OyAtLXBvcykge1xuICAgICAgICAgIGlmIChwb3MgPT0gMCkgcmV0dXJuO1xuICAgICAgICAgIHZhciBuZXh0ID0gc3RyZWFtLnN0cmluZy5jaGFyQXQocG9zIC0gMSk7XG4gICAgICAgICAgaWYgKG5leHQgPT0gY2ggJiYgc3RyZWFtLnN0cmluZy5jaGFyQXQocG9zIC0gMikgIT0gXCJcXFxcXCIpIHtcbiAgICAgICAgICAgIHBvcy0tO1xuICAgICAgICAgICAgYnJlYWs7XG4gICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICB9IGVsc2UgaWYgKHNhd1NvbWV0aGluZyAmJiAhZGVwdGgpIHtcbiAgICAgICAgKytwb3M7XG4gICAgICAgIGJyZWFrO1xuICAgICAgfVxuICAgIH1cbiAgICBpZiAoc2F3U29tZXRoaW5nICYmICFkZXB0aCkgc3RhdGUuZmF0QXJyb3dBdCA9IHBvcztcbiAgfVxuXG4gIC8vIFBhcnNlclxuXG4gIHZhciBhdG9taWNUeXBlcyA9IHtcbiAgICBcImF0b21cIjogdHJ1ZSxcbiAgICBcIm51bWJlclwiOiB0cnVlLFxuICAgIFwidmFyaWFibGVcIjogdHJ1ZSxcbiAgICBcInN0cmluZ1wiOiB0cnVlLFxuICAgIFwicmVnZXhwXCI6IHRydWUsXG4gICAgXCJ0aGlzXCI6IHRydWUsXG4gICAgXCJpbXBvcnRcIjogdHJ1ZSxcbiAgICBcImpzb25sZC1rZXl3b3JkXCI6IHRydWVcbiAgfTtcbiAgZnVuY3Rpb24gSlNMZXhpY2FsKGluZGVudGVkLCBjb2x1bW4sIHR5cGUsIGFsaWduLCBwcmV2LCBpbmZvKSB7XG4gICAgdGhpcy5pbmRlbnRlZCA9IGluZGVudGVkO1xuICAgIHRoaXMuY29sdW1uID0gY29sdW1uO1xuICAgIHRoaXMudHlwZSA9IHR5cGU7XG4gICAgdGhpcy5wcmV2ID0gcHJldjtcbiAgICB0aGlzLmluZm8gPSBpbmZvO1xuICAgIGlmIChhbGlnbiAhPSBudWxsKSB0aGlzLmFsaWduID0gYWxpZ247XG4gIH1cbiAgZnVuY3Rpb24gaW5TY29wZShzdGF0ZSwgdmFybmFtZSkge1xuICAgIGZvciAodmFyIHYgPSBzdGF0ZS5sb2NhbFZhcnM7IHY7IHYgPSB2Lm5leHQpIGlmICh2Lm5hbWUgPT0gdmFybmFtZSkgcmV0dXJuIHRydWU7XG4gICAgZm9yICh2YXIgY3ggPSBzdGF0ZS5jb250ZXh0OyBjeDsgY3ggPSBjeC5wcmV2KSB7XG4gICAgICBmb3IgKHZhciB2ID0gY3gudmFyczsgdjsgdiA9IHYubmV4dCkgaWYgKHYubmFtZSA9PSB2YXJuYW1lKSByZXR1cm4gdHJ1ZTtcbiAgICB9XG4gIH1cbiAgZnVuY3Rpb24gcGFyc2VKUyhzdGF0ZSwgc3R5bGUsIHR5cGUsIGNvbnRlbnQsIHN0cmVhbSkge1xuICAgIHZhciBjYyA9IHN0YXRlLmNjO1xuICAgIC8vIENvbW11bmljYXRlIG91ciBjb250ZXh0IHRvIHRoZSBjb21iaW5hdG9ycy5cbiAgICAvLyAoTGVzcyB3YXN0ZWZ1bCB0aGFuIGNvbnNpbmcgdXAgYSBodW5kcmVkIGNsb3N1cmVzIG9uIGV2ZXJ5IGNhbGwuKVxuICAgIGN4LnN0YXRlID0gc3RhdGU7XG4gICAgY3guc3RyZWFtID0gc3RyZWFtO1xuICAgIGN4Lm1hcmtlZCA9IG51bGw7XG4gICAgY3guY2MgPSBjYztcbiAgICBjeC5zdHlsZSA9IHN0eWxlO1xuICAgIGlmICghc3RhdGUubGV4aWNhbC5oYXNPd25Qcm9wZXJ0eShcImFsaWduXCIpKSBzdGF0ZS5sZXhpY2FsLmFsaWduID0gdHJ1ZTtcbiAgICB3aGlsZSAodHJ1ZSkge1xuICAgICAgdmFyIGNvbWJpbmF0b3IgPSBjYy5sZW5ndGggPyBjYy5wb3AoKSA6IGpzb25Nb2RlID8gZXhwcmVzc2lvbiA6IHN0YXRlbWVudDtcbiAgICAgIGlmIChjb21iaW5hdG9yKHR5cGUsIGNvbnRlbnQpKSB7XG4gICAgICAgIHdoaWxlIChjYy5sZW5ndGggJiYgY2NbY2MubGVuZ3RoIC0gMV0ubGV4KSBjYy5wb3AoKSgpO1xuICAgICAgICBpZiAoY3gubWFya2VkKSByZXR1cm4gY3gubWFya2VkO1xuICAgICAgICBpZiAodHlwZSA9PSBcInZhcmlhYmxlXCIgJiYgaW5TY29wZShzdGF0ZSwgY29udGVudCkpIHJldHVybiBcInZhcmlhYmxlTmFtZS5sb2NhbFwiO1xuICAgICAgICByZXR1cm4gc3R5bGU7XG4gICAgICB9XG4gICAgfVxuICB9XG5cbiAgLy8gQ29tYmluYXRvciB1dGlsc1xuXG4gIHZhciBjeCA9IHtcbiAgICBzdGF0ZTogbnVsbCxcbiAgICBjb2x1bW46IG51bGwsXG4gICAgbWFya2VkOiBudWxsLFxuICAgIGNjOiBudWxsXG4gIH07XG4gIGZ1bmN0aW9uIHBhc3MoKSB7XG4gICAgZm9yICh2YXIgaSA9IGFyZ3VtZW50cy5sZW5ndGggLSAxOyBpID49IDA7IGktLSkgY3guY2MucHVzaChhcmd1bWVudHNbaV0pO1xuICB9XG4gIGZ1bmN0aW9uIGNvbnQoKSB7XG4gICAgcGFzcy5hcHBseShudWxsLCBhcmd1bWVudHMpO1xuICAgIHJldHVybiB0cnVlO1xuICB9XG4gIGZ1bmN0aW9uIGluTGlzdChuYW1lLCBsaXN0KSB7XG4gICAgZm9yICh2YXIgdiA9IGxpc3Q7IHY7IHYgPSB2Lm5leHQpIGlmICh2Lm5hbWUgPT0gbmFtZSkgcmV0dXJuIHRydWU7XG4gICAgcmV0dXJuIGZhbHNlO1xuICB9XG4gIGZ1bmN0aW9uIHJlZ2lzdGVyKHZhcm5hbWUpIHtcbiAgICB2YXIgc3RhdGUgPSBjeC5zdGF0ZTtcbiAgICBjeC5tYXJrZWQgPSBcImRlZlwiO1xuICAgIGlmIChzdGF0ZS5jb250ZXh0KSB7XG4gICAgICBpZiAoc3RhdGUubGV4aWNhbC5pbmZvID09IFwidmFyXCIgJiYgc3RhdGUuY29udGV4dCAmJiBzdGF0ZS5jb250ZXh0LmJsb2NrKSB7XG4gICAgICAgIC8vIEZJWE1FIGZ1bmN0aW9uIGRlY2xzIGFyZSBhbHNvIG5vdCBibG9jayBzY29wZWRcbiAgICAgICAgdmFyIG5ld0NvbnRleHQgPSByZWdpc3RlclZhclNjb3BlZCh2YXJuYW1lLCBzdGF0ZS5jb250ZXh0KTtcbiAgICAgICAgaWYgKG5ld0NvbnRleHQgIT0gbnVsbCkge1xuICAgICAgICAgIHN0YXRlLmNvbnRleHQgPSBuZXdDb250ZXh0O1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuICAgICAgfSBlbHNlIGlmICghaW5MaXN0KHZhcm5hbWUsIHN0YXRlLmxvY2FsVmFycykpIHtcbiAgICAgICAgc3RhdGUubG9jYWxWYXJzID0gbmV3IFZhcih2YXJuYW1lLCBzdGF0ZS5sb2NhbFZhcnMpO1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG4gICAgfVxuICAgIC8vIEZhbGwgdGhyb3VnaCBtZWFucyB0aGlzIGlzIGdsb2JhbFxuICAgIGlmIChwYXJzZXJDb25maWcuZ2xvYmFsVmFycyAmJiAhaW5MaXN0KHZhcm5hbWUsIHN0YXRlLmdsb2JhbFZhcnMpKSBzdGF0ZS5nbG9iYWxWYXJzID0gbmV3IFZhcih2YXJuYW1lLCBzdGF0ZS5nbG9iYWxWYXJzKTtcbiAgfVxuICBmdW5jdGlvbiByZWdpc3RlclZhclNjb3BlZCh2YXJuYW1lLCBjb250ZXh0KSB7XG4gICAgaWYgKCFjb250ZXh0KSB7XG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9IGVsc2UgaWYgKGNvbnRleHQuYmxvY2spIHtcbiAgICAgIHZhciBpbm5lciA9IHJlZ2lzdGVyVmFyU2NvcGVkKHZhcm5hbWUsIGNvbnRleHQucHJldik7XG4gICAgICBpZiAoIWlubmVyKSByZXR1cm4gbnVsbDtcbiAgICAgIGlmIChpbm5lciA9PSBjb250ZXh0LnByZXYpIHJldHVybiBjb250ZXh0O1xuICAgICAgcmV0dXJuIG5ldyBDb250ZXh0KGlubmVyLCBjb250ZXh0LnZhcnMsIHRydWUpO1xuICAgIH0gZWxzZSBpZiAoaW5MaXN0KHZhcm5hbWUsIGNvbnRleHQudmFycykpIHtcbiAgICAgIHJldHVybiBjb250ZXh0O1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gbmV3IENvbnRleHQoY29udGV4dC5wcmV2LCBuZXcgVmFyKHZhcm5hbWUsIGNvbnRleHQudmFycyksIGZhbHNlKTtcbiAgICB9XG4gIH1cbiAgZnVuY3Rpb24gaXNNb2RpZmllcihuYW1lKSB7XG4gICAgcmV0dXJuIG5hbWUgPT0gXCJwdWJsaWNcIiB8fCBuYW1lID09IFwicHJpdmF0ZVwiIHx8IG5hbWUgPT0gXCJwcm90ZWN0ZWRcIiB8fCBuYW1lID09IFwiYWJzdHJhY3RcIiB8fCBuYW1lID09IFwicmVhZG9ubHlcIjtcbiAgfVxuXG4gIC8vIENvbWJpbmF0b3JzXG5cbiAgZnVuY3Rpb24gQ29udGV4dChwcmV2LCB2YXJzLCBibG9jaykge1xuICAgIHRoaXMucHJldiA9IHByZXY7XG4gICAgdGhpcy52YXJzID0gdmFycztcbiAgICB0aGlzLmJsb2NrID0gYmxvY2s7XG4gIH1cbiAgZnVuY3Rpb24gVmFyKG5hbWUsIG5leHQpIHtcbiAgICB0aGlzLm5hbWUgPSBuYW1lO1xuICAgIHRoaXMubmV4dCA9IG5leHQ7XG4gIH1cbiAgdmFyIGRlZmF1bHRWYXJzID0gbmV3IFZhcihcInRoaXNcIiwgbmV3IFZhcihcImFyZ3VtZW50c1wiLCBudWxsKSk7XG4gIGZ1bmN0aW9uIHB1c2hjb250ZXh0KCkge1xuICAgIGN4LnN0YXRlLmNvbnRleHQgPSBuZXcgQ29udGV4dChjeC5zdGF0ZS5jb250ZXh0LCBjeC5zdGF0ZS5sb2NhbFZhcnMsIGZhbHNlKTtcbiAgICBjeC5zdGF0ZS5sb2NhbFZhcnMgPSBkZWZhdWx0VmFycztcbiAgfVxuICBmdW5jdGlvbiBwdXNoYmxvY2tjb250ZXh0KCkge1xuICAgIGN4LnN0YXRlLmNvbnRleHQgPSBuZXcgQ29udGV4dChjeC5zdGF0ZS5jb250ZXh0LCBjeC5zdGF0ZS5sb2NhbFZhcnMsIHRydWUpO1xuICAgIGN4LnN0YXRlLmxvY2FsVmFycyA9IG51bGw7XG4gIH1cbiAgcHVzaGNvbnRleHQubGV4ID0gcHVzaGJsb2NrY29udGV4dC5sZXggPSB0cnVlO1xuICBmdW5jdGlvbiBwb3Bjb250ZXh0KCkge1xuICAgIGN4LnN0YXRlLmxvY2FsVmFycyA9IGN4LnN0YXRlLmNvbnRleHQudmFycztcbiAgICBjeC5zdGF0ZS5jb250ZXh0ID0gY3guc3RhdGUuY29udGV4dC5wcmV2O1xuICB9XG4gIHBvcGNvbnRleHQubGV4ID0gdHJ1ZTtcbiAgZnVuY3Rpb24gcHVzaGxleCh0eXBlLCBpbmZvKSB7XG4gICAgdmFyIHJlc3VsdCA9IGZ1bmN0aW9uICgpIHtcbiAgICAgIHZhciBzdGF0ZSA9IGN4LnN0YXRlLFxuICAgICAgICBpbmRlbnQgPSBzdGF0ZS5pbmRlbnRlZDtcbiAgICAgIGlmIChzdGF0ZS5sZXhpY2FsLnR5cGUgPT0gXCJzdGF0XCIpIGluZGVudCA9IHN0YXRlLmxleGljYWwuaW5kZW50ZWQ7ZWxzZSBmb3IgKHZhciBvdXRlciA9IHN0YXRlLmxleGljYWw7IG91dGVyICYmIG91dGVyLnR5cGUgPT0gXCIpXCIgJiYgb3V0ZXIuYWxpZ247IG91dGVyID0gb3V0ZXIucHJldikgaW5kZW50ID0gb3V0ZXIuaW5kZW50ZWQ7XG4gICAgICBzdGF0ZS5sZXhpY2FsID0gbmV3IEpTTGV4aWNhbChpbmRlbnQsIGN4LnN0cmVhbS5jb2x1bW4oKSwgdHlwZSwgbnVsbCwgc3RhdGUubGV4aWNhbCwgaW5mbyk7XG4gICAgfTtcbiAgICByZXN1bHQubGV4ID0gdHJ1ZTtcbiAgICByZXR1cm4gcmVzdWx0O1xuICB9XG4gIGZ1bmN0aW9uIHBvcGxleCgpIHtcbiAgICB2YXIgc3RhdGUgPSBjeC5zdGF0ZTtcbiAgICBpZiAoc3RhdGUubGV4aWNhbC5wcmV2KSB7XG4gICAgICBpZiAoc3RhdGUubGV4aWNhbC50eXBlID09IFwiKVwiKSBzdGF0ZS5pbmRlbnRlZCA9IHN0YXRlLmxleGljYWwuaW5kZW50ZWQ7XG4gICAgICBzdGF0ZS5sZXhpY2FsID0gc3RhdGUubGV4aWNhbC5wcmV2O1xuICAgIH1cbiAgfVxuICBwb3BsZXgubGV4ID0gdHJ1ZTtcbiAgZnVuY3Rpb24gZXhwZWN0KHdhbnRlZCkge1xuICAgIGZ1bmN0aW9uIGV4cCh0eXBlKSB7XG4gICAgICBpZiAodHlwZSA9PSB3YW50ZWQpIHJldHVybiBjb250KCk7ZWxzZSBpZiAod2FudGVkID09IFwiO1wiIHx8IHR5cGUgPT0gXCJ9XCIgfHwgdHlwZSA9PSBcIilcIiB8fCB0eXBlID09IFwiXVwiKSByZXR1cm4gcGFzcygpO2Vsc2UgcmV0dXJuIGNvbnQoZXhwKTtcbiAgICB9XG4gICAgO1xuICAgIHJldHVybiBleHA7XG4gIH1cbiAgZnVuY3Rpb24gc3RhdGVtZW50KHR5cGUsIHZhbHVlKSB7XG4gICAgaWYgKHR5cGUgPT0gXCJ2YXJcIikgcmV0dXJuIGNvbnQocHVzaGxleChcInZhcmRlZlwiLCB2YWx1ZSksIHZhcmRlZiwgZXhwZWN0KFwiO1wiKSwgcG9wbGV4KTtcbiAgICBpZiAodHlwZSA9PSBcImtleXdvcmQgYVwiKSByZXR1cm4gY29udChwdXNobGV4KFwiZm9ybVwiKSwgcGFyZW5FeHByLCBzdGF0ZW1lbnQsIHBvcGxleCk7XG4gICAgaWYgKHR5cGUgPT0gXCJrZXl3b3JkIGJcIikgcmV0dXJuIGNvbnQocHVzaGxleChcImZvcm1cIiksIHN0YXRlbWVudCwgcG9wbGV4KTtcbiAgICBpZiAodHlwZSA9PSBcImtleXdvcmQgZFwiKSByZXR1cm4gY3guc3RyZWFtLm1hdGNoKC9eXFxzKiQvLCBmYWxzZSkgPyBjb250KCkgOiBjb250KHB1c2hsZXgoXCJzdGF0XCIpLCBtYXliZWV4cHJlc3Npb24sIGV4cGVjdChcIjtcIiksIHBvcGxleCk7XG4gICAgaWYgKHR5cGUgPT0gXCJkZWJ1Z2dlclwiKSByZXR1cm4gY29udChleHBlY3QoXCI7XCIpKTtcbiAgICBpZiAodHlwZSA9PSBcIntcIikgcmV0dXJuIGNvbnQocHVzaGxleChcIn1cIiksIHB1c2hibG9ja2NvbnRleHQsIGJsb2NrLCBwb3BsZXgsIHBvcGNvbnRleHQpO1xuICAgIGlmICh0eXBlID09IFwiO1wiKSByZXR1cm4gY29udCgpO1xuICAgIGlmICh0eXBlID09IFwiaWZcIikge1xuICAgICAgaWYgKGN4LnN0YXRlLmxleGljYWwuaW5mbyA9PSBcImVsc2VcIiAmJiBjeC5zdGF0ZS5jY1tjeC5zdGF0ZS5jYy5sZW5ndGggLSAxXSA9PSBwb3BsZXgpIGN4LnN0YXRlLmNjLnBvcCgpKCk7XG4gICAgICByZXR1cm4gY29udChwdXNobGV4KFwiZm9ybVwiKSwgcGFyZW5FeHByLCBzdGF0ZW1lbnQsIHBvcGxleCwgbWF5YmVlbHNlKTtcbiAgICB9XG4gICAgaWYgKHR5cGUgPT0gXCJmdW5jdGlvblwiKSByZXR1cm4gY29udChmdW5jdGlvbmRlZik7XG4gICAgaWYgKHR5cGUgPT0gXCJmb3JcIikgcmV0dXJuIGNvbnQocHVzaGxleChcImZvcm1cIiksIHB1c2hibG9ja2NvbnRleHQsIGZvcnNwZWMsIHN0YXRlbWVudCwgcG9wY29udGV4dCwgcG9wbGV4KTtcbiAgICBpZiAodHlwZSA9PSBcImNsYXNzXCIgfHwgaXNUUyAmJiB2YWx1ZSA9PSBcImludGVyZmFjZVwiKSB7XG4gICAgICBjeC5tYXJrZWQgPSBcImtleXdvcmRcIjtcbiAgICAgIHJldHVybiBjb250KHB1c2hsZXgoXCJmb3JtXCIsIHR5cGUgPT0gXCJjbGFzc1wiID8gdHlwZSA6IHZhbHVlKSwgY2xhc3NOYW1lLCBwb3BsZXgpO1xuICAgIH1cbiAgICBpZiAodHlwZSA9PSBcInZhcmlhYmxlXCIpIHtcbiAgICAgIGlmIChpc1RTICYmIHZhbHVlID09IFwiZGVjbGFyZVwiKSB7XG4gICAgICAgIGN4Lm1hcmtlZCA9IFwia2V5d29yZFwiO1xuICAgICAgICByZXR1cm4gY29udChzdGF0ZW1lbnQpO1xuICAgICAgfSBlbHNlIGlmIChpc1RTICYmICh2YWx1ZSA9PSBcIm1vZHVsZVwiIHx8IHZhbHVlID09IFwiZW51bVwiIHx8IHZhbHVlID09IFwidHlwZVwiKSAmJiBjeC5zdHJlYW0ubWF0Y2goL15cXHMqXFx3LywgZmFsc2UpKSB7XG4gICAgICAgIGN4Lm1hcmtlZCA9IFwia2V5d29yZFwiO1xuICAgICAgICBpZiAodmFsdWUgPT0gXCJlbnVtXCIpIHJldHVybiBjb250KGVudW1kZWYpO2Vsc2UgaWYgKHZhbHVlID09IFwidHlwZVwiKSByZXR1cm4gY29udCh0eXBlbmFtZSwgZXhwZWN0KFwib3BlcmF0b3JcIiksIHR5cGVleHByLCBleHBlY3QoXCI7XCIpKTtlbHNlIHJldHVybiBjb250KHB1c2hsZXgoXCJmb3JtXCIpLCBwYXR0ZXJuLCBleHBlY3QoXCJ7XCIpLCBwdXNobGV4KFwifVwiKSwgYmxvY2ssIHBvcGxleCwgcG9wbGV4KTtcbiAgICAgIH0gZWxzZSBpZiAoaXNUUyAmJiB2YWx1ZSA9PSBcIm5hbWVzcGFjZVwiKSB7XG4gICAgICAgIGN4Lm1hcmtlZCA9IFwia2V5d29yZFwiO1xuICAgICAgICByZXR1cm4gY29udChwdXNobGV4KFwiZm9ybVwiKSwgZXhwcmVzc2lvbiwgc3RhdGVtZW50LCBwb3BsZXgpO1xuICAgICAgfSBlbHNlIGlmIChpc1RTICYmIHZhbHVlID09IFwiYWJzdHJhY3RcIikge1xuICAgICAgICBjeC5tYXJrZWQgPSBcImtleXdvcmRcIjtcbiAgICAgICAgcmV0dXJuIGNvbnQoc3RhdGVtZW50KTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHJldHVybiBjb250KHB1c2hsZXgoXCJzdGF0XCIpLCBtYXliZWxhYmVsKTtcbiAgICAgIH1cbiAgICB9XG4gICAgaWYgKHR5cGUgPT0gXCJzd2l0Y2hcIikgcmV0dXJuIGNvbnQocHVzaGxleChcImZvcm1cIiksIHBhcmVuRXhwciwgZXhwZWN0KFwie1wiKSwgcHVzaGxleChcIn1cIiwgXCJzd2l0Y2hcIiksIHB1c2hibG9ja2NvbnRleHQsIGJsb2NrLCBwb3BsZXgsIHBvcGxleCwgcG9wY29udGV4dCk7XG4gICAgaWYgKHR5cGUgPT0gXCJjYXNlXCIpIHJldHVybiBjb250KGV4cHJlc3Npb24sIGV4cGVjdChcIjpcIikpO1xuICAgIGlmICh0eXBlID09IFwiZGVmYXVsdFwiKSByZXR1cm4gY29udChleHBlY3QoXCI6XCIpKTtcbiAgICBpZiAodHlwZSA9PSBcImNhdGNoXCIpIHJldHVybiBjb250KHB1c2hsZXgoXCJmb3JtXCIpLCBwdXNoY29udGV4dCwgbWF5YmVDYXRjaEJpbmRpbmcsIHN0YXRlbWVudCwgcG9wbGV4LCBwb3Bjb250ZXh0KTtcbiAgICBpZiAodHlwZSA9PSBcImV4cG9ydFwiKSByZXR1cm4gY29udChwdXNobGV4KFwic3RhdFwiKSwgYWZ0ZXJFeHBvcnQsIHBvcGxleCk7XG4gICAgaWYgKHR5cGUgPT0gXCJpbXBvcnRcIikgcmV0dXJuIGNvbnQocHVzaGxleChcInN0YXRcIiksIGFmdGVySW1wb3J0LCBwb3BsZXgpO1xuICAgIGlmICh0eXBlID09IFwiYXN5bmNcIikgcmV0dXJuIGNvbnQoc3RhdGVtZW50KTtcbiAgICBpZiAodmFsdWUgPT0gXCJAXCIpIHJldHVybiBjb250KGV4cHJlc3Npb24sIHN0YXRlbWVudCk7XG4gICAgcmV0dXJuIHBhc3MocHVzaGxleChcInN0YXRcIiksIGV4cHJlc3Npb24sIGV4cGVjdChcIjtcIiksIHBvcGxleCk7XG4gIH1cbiAgZnVuY3Rpb24gbWF5YmVDYXRjaEJpbmRpbmcodHlwZSkge1xuICAgIGlmICh0eXBlID09IFwiKFwiKSByZXR1cm4gY29udChmdW5hcmcsIGV4cGVjdChcIilcIikpO1xuICB9XG4gIGZ1bmN0aW9uIGV4cHJlc3Npb24odHlwZSwgdmFsdWUpIHtcbiAgICByZXR1cm4gZXhwcmVzc2lvbklubmVyKHR5cGUsIHZhbHVlLCBmYWxzZSk7XG4gIH1cbiAgZnVuY3Rpb24gZXhwcmVzc2lvbk5vQ29tbWEodHlwZSwgdmFsdWUpIHtcbiAgICByZXR1cm4gZXhwcmVzc2lvbklubmVyKHR5cGUsIHZhbHVlLCB0cnVlKTtcbiAgfVxuICBmdW5jdGlvbiBwYXJlbkV4cHIodHlwZSkge1xuICAgIGlmICh0eXBlICE9IFwiKFwiKSByZXR1cm4gcGFzcygpO1xuICAgIHJldHVybiBjb250KHB1c2hsZXgoXCIpXCIpLCBtYXliZWV4cHJlc3Npb24sIGV4cGVjdChcIilcIiksIHBvcGxleCk7XG4gIH1cbiAgZnVuY3Rpb24gZXhwcmVzc2lvbklubmVyKHR5cGUsIHZhbHVlLCBub0NvbW1hKSB7XG4gICAgaWYgKGN4LnN0YXRlLmZhdEFycm93QXQgPT0gY3guc3RyZWFtLnN0YXJ0KSB7XG4gICAgICB2YXIgYm9keSA9IG5vQ29tbWEgPyBhcnJvd0JvZHlOb0NvbW1hIDogYXJyb3dCb2R5O1xuICAgICAgaWYgKHR5cGUgPT0gXCIoXCIpIHJldHVybiBjb250KHB1c2hjb250ZXh0LCBwdXNobGV4KFwiKVwiKSwgY29tbWFzZXAoZnVuYXJnLCBcIilcIiksIHBvcGxleCwgZXhwZWN0KFwiPT5cIiksIGJvZHksIHBvcGNvbnRleHQpO2Vsc2UgaWYgKHR5cGUgPT0gXCJ2YXJpYWJsZVwiKSByZXR1cm4gcGFzcyhwdXNoY29udGV4dCwgcGF0dGVybiwgZXhwZWN0KFwiPT5cIiksIGJvZHksIHBvcGNvbnRleHQpO1xuICAgIH1cbiAgICB2YXIgbWF5YmVvcCA9IG5vQ29tbWEgPyBtYXliZW9wZXJhdG9yTm9Db21tYSA6IG1heWJlb3BlcmF0b3JDb21tYTtcbiAgICBpZiAoYXRvbWljVHlwZXMuaGFzT3duUHJvcGVydHkodHlwZSkpIHJldHVybiBjb250KG1heWJlb3ApO1xuICAgIGlmICh0eXBlID09IFwiZnVuY3Rpb25cIikgcmV0dXJuIGNvbnQoZnVuY3Rpb25kZWYsIG1heWJlb3ApO1xuICAgIGlmICh0eXBlID09IFwiY2xhc3NcIiB8fCBpc1RTICYmIHZhbHVlID09IFwiaW50ZXJmYWNlXCIpIHtcbiAgICAgIGN4Lm1hcmtlZCA9IFwia2V5d29yZFwiO1xuICAgICAgcmV0dXJuIGNvbnQocHVzaGxleChcImZvcm1cIiksIGNsYXNzRXhwcmVzc2lvbiwgcG9wbGV4KTtcbiAgICB9XG4gICAgaWYgKHR5cGUgPT0gXCJrZXl3b3JkIGNcIiB8fCB0eXBlID09IFwiYXN5bmNcIikgcmV0dXJuIGNvbnQobm9Db21tYSA/IGV4cHJlc3Npb25Ob0NvbW1hIDogZXhwcmVzc2lvbik7XG4gICAgaWYgKHR5cGUgPT0gXCIoXCIpIHJldHVybiBjb250KHB1c2hsZXgoXCIpXCIpLCBtYXliZWV4cHJlc3Npb24sIGV4cGVjdChcIilcIiksIHBvcGxleCwgbWF5YmVvcCk7XG4gICAgaWYgKHR5cGUgPT0gXCJvcGVyYXRvclwiIHx8IHR5cGUgPT0gXCJzcHJlYWRcIikgcmV0dXJuIGNvbnQobm9Db21tYSA/IGV4cHJlc3Npb25Ob0NvbW1hIDogZXhwcmVzc2lvbik7XG4gICAgaWYgKHR5cGUgPT0gXCJbXCIpIHJldHVybiBjb250KHB1c2hsZXgoXCJdXCIpLCBhcnJheUxpdGVyYWwsIHBvcGxleCwgbWF5YmVvcCk7XG4gICAgaWYgKHR5cGUgPT0gXCJ7XCIpIHJldHVybiBjb250Q29tbWFzZXAob2JqcHJvcCwgXCJ9XCIsIG51bGwsIG1heWJlb3ApO1xuICAgIGlmICh0eXBlID09IFwicXVhc2lcIikgcmV0dXJuIHBhc3MocXVhc2ksIG1heWJlb3ApO1xuICAgIGlmICh0eXBlID09IFwibmV3XCIpIHJldHVybiBjb250KG1heWJlVGFyZ2V0KG5vQ29tbWEpKTtcbiAgICByZXR1cm4gY29udCgpO1xuICB9XG4gIGZ1bmN0aW9uIG1heWJlZXhwcmVzc2lvbih0eXBlKSB7XG4gICAgaWYgKHR5cGUubWF0Y2goL1s7XFx9XFwpXFxdLF0vKSkgcmV0dXJuIHBhc3MoKTtcbiAgICByZXR1cm4gcGFzcyhleHByZXNzaW9uKTtcbiAgfVxuICBmdW5jdGlvbiBtYXliZW9wZXJhdG9yQ29tbWEodHlwZSwgdmFsdWUpIHtcbiAgICBpZiAodHlwZSA9PSBcIixcIikgcmV0dXJuIGNvbnQobWF5YmVleHByZXNzaW9uKTtcbiAgICByZXR1cm4gbWF5YmVvcGVyYXRvck5vQ29tbWEodHlwZSwgdmFsdWUsIGZhbHNlKTtcbiAgfVxuICBmdW5jdGlvbiBtYXliZW9wZXJhdG9yTm9Db21tYSh0eXBlLCB2YWx1ZSwgbm9Db21tYSkge1xuICAgIHZhciBtZSA9IG5vQ29tbWEgPT0gZmFsc2UgPyBtYXliZW9wZXJhdG9yQ29tbWEgOiBtYXliZW9wZXJhdG9yTm9Db21tYTtcbiAgICB2YXIgZXhwciA9IG5vQ29tbWEgPT0gZmFsc2UgPyBleHByZXNzaW9uIDogZXhwcmVzc2lvbk5vQ29tbWE7XG4gICAgaWYgKHR5cGUgPT0gXCI9PlwiKSByZXR1cm4gY29udChwdXNoY29udGV4dCwgbm9Db21tYSA/IGFycm93Qm9keU5vQ29tbWEgOiBhcnJvd0JvZHksIHBvcGNvbnRleHQpO1xuICAgIGlmICh0eXBlID09IFwib3BlcmF0b3JcIikge1xuICAgICAgaWYgKC9cXCtcXCt8LS0vLnRlc3QodmFsdWUpIHx8IGlzVFMgJiYgdmFsdWUgPT0gXCIhXCIpIHJldHVybiBjb250KG1lKTtcbiAgICAgIGlmIChpc1RTICYmIHZhbHVlID09IFwiPFwiICYmIGN4LnN0cmVhbS5tYXRjaCgvXihbXjw+XXw8W148Pl0qPikqPlxccypcXCgvLCBmYWxzZSkpIHJldHVybiBjb250KHB1c2hsZXgoXCI+XCIpLCBjb21tYXNlcCh0eXBlZXhwciwgXCI+XCIpLCBwb3BsZXgsIG1lKTtcbiAgICAgIGlmICh2YWx1ZSA9PSBcIj9cIikgcmV0dXJuIGNvbnQoZXhwcmVzc2lvbiwgZXhwZWN0KFwiOlwiKSwgZXhwcik7XG4gICAgICByZXR1cm4gY29udChleHByKTtcbiAgICB9XG4gICAgaWYgKHR5cGUgPT0gXCJxdWFzaVwiKSB7XG4gICAgICByZXR1cm4gcGFzcyhxdWFzaSwgbWUpO1xuICAgIH1cbiAgICBpZiAodHlwZSA9PSBcIjtcIikgcmV0dXJuO1xuICAgIGlmICh0eXBlID09IFwiKFwiKSByZXR1cm4gY29udENvbW1hc2VwKGV4cHJlc3Npb25Ob0NvbW1hLCBcIilcIiwgXCJjYWxsXCIsIG1lKTtcbiAgICBpZiAodHlwZSA9PSBcIi5cIikgcmV0dXJuIGNvbnQocHJvcGVydHksIG1lKTtcbiAgICBpZiAodHlwZSA9PSBcIltcIikgcmV0dXJuIGNvbnQocHVzaGxleChcIl1cIiksIG1heWJlZXhwcmVzc2lvbiwgZXhwZWN0KFwiXVwiKSwgcG9wbGV4LCBtZSk7XG4gICAgaWYgKGlzVFMgJiYgdmFsdWUgPT0gXCJhc1wiKSB7XG4gICAgICBjeC5tYXJrZWQgPSBcImtleXdvcmRcIjtcbiAgICAgIHJldHVybiBjb250KHR5cGVleHByLCBtZSk7XG4gICAgfVxuICAgIGlmICh0eXBlID09IFwicmVnZXhwXCIpIHtcbiAgICAgIGN4LnN0YXRlLmxhc3RUeXBlID0gY3gubWFya2VkID0gXCJvcGVyYXRvclwiO1xuICAgICAgY3guc3RyZWFtLmJhY2tVcChjeC5zdHJlYW0ucG9zIC0gY3guc3RyZWFtLnN0YXJ0IC0gMSk7XG4gICAgICByZXR1cm4gY29udChleHByKTtcbiAgICB9XG4gIH1cbiAgZnVuY3Rpb24gcXVhc2kodHlwZSwgdmFsdWUpIHtcbiAgICBpZiAodHlwZSAhPSBcInF1YXNpXCIpIHJldHVybiBwYXNzKCk7XG4gICAgaWYgKHZhbHVlLnNsaWNlKHZhbHVlLmxlbmd0aCAtIDIpICE9IFwiJHtcIikgcmV0dXJuIGNvbnQocXVhc2kpO1xuICAgIHJldHVybiBjb250KG1heWJlZXhwcmVzc2lvbiwgY29udGludWVRdWFzaSk7XG4gIH1cbiAgZnVuY3Rpb24gY29udGludWVRdWFzaSh0eXBlKSB7XG4gICAgaWYgKHR5cGUgPT0gXCJ9XCIpIHtcbiAgICAgIGN4Lm1hcmtlZCA9IFwic3RyaW5nLnNwZWNpYWxcIjtcbiAgICAgIGN4LnN0YXRlLnRva2VuaXplID0gdG9rZW5RdWFzaTtcbiAgICAgIHJldHVybiBjb250KHF1YXNpKTtcbiAgICB9XG4gIH1cbiAgZnVuY3Rpb24gYXJyb3dCb2R5KHR5cGUpIHtcbiAgICBmaW5kRmF0QXJyb3coY3guc3RyZWFtLCBjeC5zdGF0ZSk7XG4gICAgcmV0dXJuIHBhc3ModHlwZSA9PSBcIntcIiA/IHN0YXRlbWVudCA6IGV4cHJlc3Npb24pO1xuICB9XG4gIGZ1bmN0aW9uIGFycm93Qm9keU5vQ29tbWEodHlwZSkge1xuICAgIGZpbmRGYXRBcnJvdyhjeC5zdHJlYW0sIGN4LnN0YXRlKTtcbiAgICByZXR1cm4gcGFzcyh0eXBlID09IFwie1wiID8gc3RhdGVtZW50IDogZXhwcmVzc2lvbk5vQ29tbWEpO1xuICB9XG4gIGZ1bmN0aW9uIG1heWJlVGFyZ2V0KG5vQ29tbWEpIHtcbiAgICByZXR1cm4gZnVuY3Rpb24gKHR5cGUpIHtcbiAgICAgIGlmICh0eXBlID09IFwiLlwiKSByZXR1cm4gY29udChub0NvbW1hID8gdGFyZ2V0Tm9Db21tYSA6IHRhcmdldCk7ZWxzZSBpZiAodHlwZSA9PSBcInZhcmlhYmxlXCIgJiYgaXNUUykgcmV0dXJuIGNvbnQobWF5YmVUeXBlQXJncywgbm9Db21tYSA/IG1heWJlb3BlcmF0b3JOb0NvbW1hIDogbWF5YmVvcGVyYXRvckNvbW1hKTtlbHNlIHJldHVybiBwYXNzKG5vQ29tbWEgPyBleHByZXNzaW9uTm9Db21tYSA6IGV4cHJlc3Npb24pO1xuICAgIH07XG4gIH1cbiAgZnVuY3Rpb24gdGFyZ2V0KF8sIHZhbHVlKSB7XG4gICAgaWYgKHZhbHVlID09IFwidGFyZ2V0XCIpIHtcbiAgICAgIGN4Lm1hcmtlZCA9IFwia2V5d29yZFwiO1xuICAgICAgcmV0dXJuIGNvbnQobWF5YmVvcGVyYXRvckNvbW1hKTtcbiAgICB9XG4gIH1cbiAgZnVuY3Rpb24gdGFyZ2V0Tm9Db21tYShfLCB2YWx1ZSkge1xuICAgIGlmICh2YWx1ZSA9PSBcInRhcmdldFwiKSB7XG4gICAgICBjeC5tYXJrZWQgPSBcImtleXdvcmRcIjtcbiAgICAgIHJldHVybiBjb250KG1heWJlb3BlcmF0b3JOb0NvbW1hKTtcbiAgICB9XG4gIH1cbiAgZnVuY3Rpb24gbWF5YmVsYWJlbCh0eXBlKSB7XG4gICAgaWYgKHR5cGUgPT0gXCI6XCIpIHJldHVybiBjb250KHBvcGxleCwgc3RhdGVtZW50KTtcbiAgICByZXR1cm4gcGFzcyhtYXliZW9wZXJhdG9yQ29tbWEsIGV4cGVjdChcIjtcIiksIHBvcGxleCk7XG4gIH1cbiAgZnVuY3Rpb24gcHJvcGVydHkodHlwZSkge1xuICAgIGlmICh0eXBlID09IFwidmFyaWFibGVcIikge1xuICAgICAgY3gubWFya2VkID0gXCJwcm9wZXJ0eVwiO1xuICAgICAgcmV0dXJuIGNvbnQoKTtcbiAgICB9XG4gIH1cbiAgZnVuY3Rpb24gb2JqcHJvcCh0eXBlLCB2YWx1ZSkge1xuICAgIGlmICh0eXBlID09IFwiYXN5bmNcIikge1xuICAgICAgY3gubWFya2VkID0gXCJwcm9wZXJ0eVwiO1xuICAgICAgcmV0dXJuIGNvbnQob2JqcHJvcCk7XG4gICAgfSBlbHNlIGlmICh0eXBlID09IFwidmFyaWFibGVcIiB8fCBjeC5zdHlsZSA9PSBcImtleXdvcmRcIikge1xuICAgICAgY3gubWFya2VkID0gXCJwcm9wZXJ0eVwiO1xuICAgICAgaWYgKHZhbHVlID09IFwiZ2V0XCIgfHwgdmFsdWUgPT0gXCJzZXRcIikgcmV0dXJuIGNvbnQoZ2V0dGVyU2V0dGVyKTtcbiAgICAgIHZhciBtOyAvLyBXb3JrIGFyb3VuZCBmYXQtYXJyb3ctZGV0ZWN0aW9uIGNvbXBsaWNhdGlvbiBmb3IgZGV0ZWN0aW5nIHR5cGVzY3JpcHQgdHlwZWQgYXJyb3cgcGFyYW1zXG4gICAgICBpZiAoaXNUUyAmJiBjeC5zdGF0ZS5mYXRBcnJvd0F0ID09IGN4LnN0cmVhbS5zdGFydCAmJiAobSA9IGN4LnN0cmVhbS5tYXRjaCgvXlxccyo6XFxzKi8sIGZhbHNlKSkpIGN4LnN0YXRlLmZhdEFycm93QXQgPSBjeC5zdHJlYW0ucG9zICsgbVswXS5sZW5ndGg7XG4gICAgICByZXR1cm4gY29udChhZnRlcnByb3ApO1xuICAgIH0gZWxzZSBpZiAodHlwZSA9PSBcIm51bWJlclwiIHx8IHR5cGUgPT0gXCJzdHJpbmdcIikge1xuICAgICAgY3gubWFya2VkID0ganNvbmxkTW9kZSA/IFwicHJvcGVydHlcIiA6IGN4LnN0eWxlICsgXCIgcHJvcGVydHlcIjtcbiAgICAgIHJldHVybiBjb250KGFmdGVycHJvcCk7XG4gICAgfSBlbHNlIGlmICh0eXBlID09IFwianNvbmxkLWtleXdvcmRcIikge1xuICAgICAgcmV0dXJuIGNvbnQoYWZ0ZXJwcm9wKTtcbiAgICB9IGVsc2UgaWYgKGlzVFMgJiYgaXNNb2RpZmllcih2YWx1ZSkpIHtcbiAgICAgIGN4Lm1hcmtlZCA9IFwia2V5d29yZFwiO1xuICAgICAgcmV0dXJuIGNvbnQob2JqcHJvcCk7XG4gICAgfSBlbHNlIGlmICh0eXBlID09IFwiW1wiKSB7XG4gICAgICByZXR1cm4gY29udChleHByZXNzaW9uLCBtYXliZXR5cGUsIGV4cGVjdChcIl1cIiksIGFmdGVycHJvcCk7XG4gICAgfSBlbHNlIGlmICh0eXBlID09IFwic3ByZWFkXCIpIHtcbiAgICAgIHJldHVybiBjb250KGV4cHJlc3Npb25Ob0NvbW1hLCBhZnRlcnByb3ApO1xuICAgIH0gZWxzZSBpZiAodmFsdWUgPT0gXCIqXCIpIHtcbiAgICAgIGN4Lm1hcmtlZCA9IFwia2V5d29yZFwiO1xuICAgICAgcmV0dXJuIGNvbnQob2JqcHJvcCk7XG4gICAgfSBlbHNlIGlmICh0eXBlID09IFwiOlwiKSB7XG4gICAgICByZXR1cm4gcGFzcyhhZnRlcnByb3ApO1xuICAgIH1cbiAgfVxuICBmdW5jdGlvbiBnZXR0ZXJTZXR0ZXIodHlwZSkge1xuICAgIGlmICh0eXBlICE9IFwidmFyaWFibGVcIikgcmV0dXJuIHBhc3MoYWZ0ZXJwcm9wKTtcbiAgICBjeC5tYXJrZWQgPSBcInByb3BlcnR5XCI7XG4gICAgcmV0dXJuIGNvbnQoZnVuY3Rpb25kZWYpO1xuICB9XG4gIGZ1bmN0aW9uIGFmdGVycHJvcCh0eXBlKSB7XG4gICAgaWYgKHR5cGUgPT0gXCI6XCIpIHJldHVybiBjb250KGV4cHJlc3Npb25Ob0NvbW1hKTtcbiAgICBpZiAodHlwZSA9PSBcIihcIikgcmV0dXJuIHBhc3MoZnVuY3Rpb25kZWYpO1xuICB9XG4gIGZ1bmN0aW9uIGNvbW1hc2VwKHdoYXQsIGVuZCwgc2VwKSB7XG4gICAgZnVuY3Rpb24gcHJvY2VlZCh0eXBlLCB2YWx1ZSkge1xuICAgICAgaWYgKHNlcCA/IHNlcC5pbmRleE9mKHR5cGUpID4gLTEgOiB0eXBlID09IFwiLFwiKSB7XG4gICAgICAgIHZhciBsZXggPSBjeC5zdGF0ZS5sZXhpY2FsO1xuICAgICAgICBpZiAobGV4LmluZm8gPT0gXCJjYWxsXCIpIGxleC5wb3MgPSAobGV4LnBvcyB8fCAwKSArIDE7XG4gICAgICAgIHJldHVybiBjb250KGZ1bmN0aW9uICh0eXBlLCB2YWx1ZSkge1xuICAgICAgICAgIGlmICh0eXBlID09IGVuZCB8fCB2YWx1ZSA9PSBlbmQpIHJldHVybiBwYXNzKCk7XG4gICAgICAgICAgcmV0dXJuIHBhc3Mod2hhdCk7XG4gICAgICAgIH0sIHByb2NlZWQpO1xuICAgICAgfVxuICAgICAgaWYgKHR5cGUgPT0gZW5kIHx8IHZhbHVlID09IGVuZCkgcmV0dXJuIGNvbnQoKTtcbiAgICAgIGlmIChzZXAgJiYgc2VwLmluZGV4T2YoXCI7XCIpID4gLTEpIHJldHVybiBwYXNzKHdoYXQpO1xuICAgICAgcmV0dXJuIGNvbnQoZXhwZWN0KGVuZCkpO1xuICAgIH1cbiAgICByZXR1cm4gZnVuY3Rpb24gKHR5cGUsIHZhbHVlKSB7XG4gICAgICBpZiAodHlwZSA9PSBlbmQgfHwgdmFsdWUgPT0gZW5kKSByZXR1cm4gY29udCgpO1xuICAgICAgcmV0dXJuIHBhc3Mod2hhdCwgcHJvY2VlZCk7XG4gICAgfTtcbiAgfVxuICBmdW5jdGlvbiBjb250Q29tbWFzZXAod2hhdCwgZW5kLCBpbmZvKSB7XG4gICAgZm9yICh2YXIgaSA9IDM7IGkgPCBhcmd1bWVudHMubGVuZ3RoOyBpKyspIGN4LmNjLnB1c2goYXJndW1lbnRzW2ldKTtcbiAgICByZXR1cm4gY29udChwdXNobGV4KGVuZCwgaW5mbyksIGNvbW1hc2VwKHdoYXQsIGVuZCksIHBvcGxleCk7XG4gIH1cbiAgZnVuY3Rpb24gYmxvY2sodHlwZSkge1xuICAgIGlmICh0eXBlID09IFwifVwiKSByZXR1cm4gY29udCgpO1xuICAgIHJldHVybiBwYXNzKHN0YXRlbWVudCwgYmxvY2spO1xuICB9XG4gIGZ1bmN0aW9uIG1heWJldHlwZSh0eXBlLCB2YWx1ZSkge1xuICAgIGlmIChpc1RTKSB7XG4gICAgICBpZiAodHlwZSA9PSBcIjpcIikgcmV0dXJuIGNvbnQodHlwZWV4cHIpO1xuICAgICAgaWYgKHZhbHVlID09IFwiP1wiKSByZXR1cm4gY29udChtYXliZXR5cGUpO1xuICAgIH1cbiAgfVxuICBmdW5jdGlvbiBtYXliZXR5cGVPckluKHR5cGUsIHZhbHVlKSB7XG4gICAgaWYgKGlzVFMgJiYgKHR5cGUgPT0gXCI6XCIgfHwgdmFsdWUgPT0gXCJpblwiKSkgcmV0dXJuIGNvbnQodHlwZWV4cHIpO1xuICB9XG4gIGZ1bmN0aW9uIG1heWJlcmV0dHlwZSh0eXBlKSB7XG4gICAgaWYgKGlzVFMgJiYgdHlwZSA9PSBcIjpcIikge1xuICAgICAgaWYgKGN4LnN0cmVhbS5tYXRjaCgvXlxccypcXHcrXFxzK2lzXFxiLywgZmFsc2UpKSByZXR1cm4gY29udChleHByZXNzaW9uLCBpc0tXLCB0eXBlZXhwcik7ZWxzZSByZXR1cm4gY29udCh0eXBlZXhwcik7XG4gICAgfVxuICB9XG4gIGZ1bmN0aW9uIGlzS1coXywgdmFsdWUpIHtcbiAgICBpZiAodmFsdWUgPT0gXCJpc1wiKSB7XG4gICAgICBjeC5tYXJrZWQgPSBcImtleXdvcmRcIjtcbiAgICAgIHJldHVybiBjb250KCk7XG4gICAgfVxuICB9XG4gIGZ1bmN0aW9uIHR5cGVleHByKHR5cGUsIHZhbHVlKSB7XG4gICAgaWYgKHZhbHVlID09IFwia2V5b2ZcIiB8fCB2YWx1ZSA9PSBcInR5cGVvZlwiIHx8IHZhbHVlID09IFwiaW5mZXJcIiB8fCB2YWx1ZSA9PSBcInJlYWRvbmx5XCIpIHtcbiAgICAgIGN4Lm1hcmtlZCA9IFwia2V5d29yZFwiO1xuICAgICAgcmV0dXJuIGNvbnQodmFsdWUgPT0gXCJ0eXBlb2ZcIiA/IGV4cHJlc3Npb25Ob0NvbW1hIDogdHlwZWV4cHIpO1xuICAgIH1cbiAgICBpZiAodHlwZSA9PSBcInZhcmlhYmxlXCIgfHwgdmFsdWUgPT0gXCJ2b2lkXCIpIHtcbiAgICAgIGN4Lm1hcmtlZCA9IFwidHlwZVwiO1xuICAgICAgcmV0dXJuIGNvbnQoYWZ0ZXJUeXBlKTtcbiAgICB9XG4gICAgaWYgKHZhbHVlID09IFwifFwiIHx8IHZhbHVlID09IFwiJlwiKSByZXR1cm4gY29udCh0eXBlZXhwcik7XG4gICAgaWYgKHR5cGUgPT0gXCJzdHJpbmdcIiB8fCB0eXBlID09IFwibnVtYmVyXCIgfHwgdHlwZSA9PSBcImF0b21cIikgcmV0dXJuIGNvbnQoYWZ0ZXJUeXBlKTtcbiAgICBpZiAodHlwZSA9PSBcIltcIikgcmV0dXJuIGNvbnQocHVzaGxleChcIl1cIiksIGNvbW1hc2VwKHR5cGVleHByLCBcIl1cIiwgXCIsXCIpLCBwb3BsZXgsIGFmdGVyVHlwZSk7XG4gICAgaWYgKHR5cGUgPT0gXCJ7XCIpIHJldHVybiBjb250KHB1c2hsZXgoXCJ9XCIpLCB0eXBlcHJvcHMsIHBvcGxleCwgYWZ0ZXJUeXBlKTtcbiAgICBpZiAodHlwZSA9PSBcIihcIikgcmV0dXJuIGNvbnQoY29tbWFzZXAodHlwZWFyZywgXCIpXCIpLCBtYXliZVJldHVyblR5cGUsIGFmdGVyVHlwZSk7XG4gICAgaWYgKHR5cGUgPT0gXCI8XCIpIHJldHVybiBjb250KGNvbW1hc2VwKHR5cGVleHByLCBcIj5cIiksIHR5cGVleHByKTtcbiAgICBpZiAodHlwZSA9PSBcInF1YXNpXCIpIHJldHVybiBwYXNzKHF1YXNpVHlwZSwgYWZ0ZXJUeXBlKTtcbiAgfVxuICBmdW5jdGlvbiBtYXliZVJldHVyblR5cGUodHlwZSkge1xuICAgIGlmICh0eXBlID09IFwiPT5cIikgcmV0dXJuIGNvbnQodHlwZWV4cHIpO1xuICB9XG4gIGZ1bmN0aW9uIHR5cGVwcm9wcyh0eXBlKSB7XG4gICAgaWYgKHR5cGUubWF0Y2goL1tcXH1cXClcXF1dLykpIHJldHVybiBjb250KCk7XG4gICAgaWYgKHR5cGUgPT0gXCIsXCIgfHwgdHlwZSA9PSBcIjtcIikgcmV0dXJuIGNvbnQodHlwZXByb3BzKTtcbiAgICByZXR1cm4gcGFzcyh0eXBlcHJvcCwgdHlwZXByb3BzKTtcbiAgfVxuICBmdW5jdGlvbiB0eXBlcHJvcCh0eXBlLCB2YWx1ZSkge1xuICAgIGlmICh0eXBlID09IFwidmFyaWFibGVcIiB8fCBjeC5zdHlsZSA9PSBcImtleXdvcmRcIikge1xuICAgICAgY3gubWFya2VkID0gXCJwcm9wZXJ0eVwiO1xuICAgICAgcmV0dXJuIGNvbnQodHlwZXByb3ApO1xuICAgIH0gZWxzZSBpZiAodmFsdWUgPT0gXCI/XCIgfHwgdHlwZSA9PSBcIm51bWJlclwiIHx8IHR5cGUgPT0gXCJzdHJpbmdcIikge1xuICAgICAgcmV0dXJuIGNvbnQodHlwZXByb3ApO1xuICAgIH0gZWxzZSBpZiAodHlwZSA9PSBcIjpcIikge1xuICAgICAgcmV0dXJuIGNvbnQodHlwZWV4cHIpO1xuICAgIH0gZWxzZSBpZiAodHlwZSA9PSBcIltcIikge1xuICAgICAgcmV0dXJuIGNvbnQoZXhwZWN0KFwidmFyaWFibGVcIiksIG1heWJldHlwZU9ySW4sIGV4cGVjdChcIl1cIiksIHR5cGVwcm9wKTtcbiAgICB9IGVsc2UgaWYgKHR5cGUgPT0gXCIoXCIpIHtcbiAgICAgIHJldHVybiBwYXNzKGZ1bmN0aW9uZGVjbCwgdHlwZXByb3ApO1xuICAgIH0gZWxzZSBpZiAoIXR5cGUubWF0Y2goL1s7XFx9XFwpXFxdLF0vKSkge1xuICAgICAgcmV0dXJuIGNvbnQoKTtcbiAgICB9XG4gIH1cbiAgZnVuY3Rpb24gcXVhc2lUeXBlKHR5cGUsIHZhbHVlKSB7XG4gICAgaWYgKHR5cGUgIT0gXCJxdWFzaVwiKSByZXR1cm4gcGFzcygpO1xuICAgIGlmICh2YWx1ZS5zbGljZSh2YWx1ZS5sZW5ndGggLSAyKSAhPSBcIiR7XCIpIHJldHVybiBjb250KHF1YXNpVHlwZSk7XG4gICAgcmV0dXJuIGNvbnQodHlwZWV4cHIsIGNvbnRpbnVlUXVhc2lUeXBlKTtcbiAgfVxuICBmdW5jdGlvbiBjb250aW51ZVF1YXNpVHlwZSh0eXBlKSB7XG4gICAgaWYgKHR5cGUgPT0gXCJ9XCIpIHtcbiAgICAgIGN4Lm1hcmtlZCA9IFwic3RyaW5nLnNwZWNpYWxcIjtcbiAgICAgIGN4LnN0YXRlLnRva2VuaXplID0gdG9rZW5RdWFzaTtcbiAgICAgIHJldHVybiBjb250KHF1YXNpVHlwZSk7XG4gICAgfVxuICB9XG4gIGZ1bmN0aW9uIHR5cGVhcmcodHlwZSwgdmFsdWUpIHtcbiAgICBpZiAodHlwZSA9PSBcInZhcmlhYmxlXCIgJiYgY3guc3RyZWFtLm1hdGNoKC9eXFxzKls/Ol0vLCBmYWxzZSkgfHwgdmFsdWUgPT0gXCI/XCIpIHJldHVybiBjb250KHR5cGVhcmcpO1xuICAgIGlmICh0eXBlID09IFwiOlwiKSByZXR1cm4gY29udCh0eXBlZXhwcik7XG4gICAgaWYgKHR5cGUgPT0gXCJzcHJlYWRcIikgcmV0dXJuIGNvbnQodHlwZWFyZyk7XG4gICAgcmV0dXJuIHBhc3ModHlwZWV4cHIpO1xuICB9XG4gIGZ1bmN0aW9uIGFmdGVyVHlwZSh0eXBlLCB2YWx1ZSkge1xuICAgIGlmICh2YWx1ZSA9PSBcIjxcIikgcmV0dXJuIGNvbnQocHVzaGxleChcIj5cIiksIGNvbW1hc2VwKHR5cGVleHByLCBcIj5cIiksIHBvcGxleCwgYWZ0ZXJUeXBlKTtcbiAgICBpZiAodmFsdWUgPT0gXCJ8XCIgfHwgdHlwZSA9PSBcIi5cIiB8fCB2YWx1ZSA9PSBcIiZcIikgcmV0dXJuIGNvbnQodHlwZWV4cHIpO1xuICAgIGlmICh0eXBlID09IFwiW1wiKSByZXR1cm4gY29udCh0eXBlZXhwciwgZXhwZWN0KFwiXVwiKSwgYWZ0ZXJUeXBlKTtcbiAgICBpZiAodmFsdWUgPT0gXCJleHRlbmRzXCIgfHwgdmFsdWUgPT0gXCJpbXBsZW1lbnRzXCIpIHtcbiAgICAgIGN4Lm1hcmtlZCA9IFwia2V5d29yZFwiO1xuICAgICAgcmV0dXJuIGNvbnQodHlwZWV4cHIpO1xuICAgIH1cbiAgICBpZiAodmFsdWUgPT0gXCI/XCIpIHJldHVybiBjb250KHR5cGVleHByLCBleHBlY3QoXCI6XCIpLCB0eXBlZXhwcik7XG4gIH1cbiAgZnVuY3Rpb24gbWF5YmVUeXBlQXJncyhfLCB2YWx1ZSkge1xuICAgIGlmICh2YWx1ZSA9PSBcIjxcIikgcmV0dXJuIGNvbnQocHVzaGxleChcIj5cIiksIGNvbW1hc2VwKHR5cGVleHByLCBcIj5cIiksIHBvcGxleCwgYWZ0ZXJUeXBlKTtcbiAgfVxuICBmdW5jdGlvbiB0eXBlcGFyYW0oKSB7XG4gICAgcmV0dXJuIHBhc3ModHlwZWV4cHIsIG1heWJlVHlwZURlZmF1bHQpO1xuICB9XG4gIGZ1bmN0aW9uIG1heWJlVHlwZURlZmF1bHQoXywgdmFsdWUpIHtcbiAgICBpZiAodmFsdWUgPT0gXCI9XCIpIHJldHVybiBjb250KHR5cGVleHByKTtcbiAgfVxuICBmdW5jdGlvbiB2YXJkZWYoXywgdmFsdWUpIHtcbiAgICBpZiAodmFsdWUgPT0gXCJlbnVtXCIpIHtcbiAgICAgIGN4Lm1hcmtlZCA9IFwia2V5d29yZFwiO1xuICAgICAgcmV0dXJuIGNvbnQoZW51bWRlZik7XG4gICAgfVxuICAgIHJldHVybiBwYXNzKHBhdHRlcm4sIG1heWJldHlwZSwgbWF5YmVBc3NpZ24sIHZhcmRlZkNvbnQpO1xuICB9XG4gIGZ1bmN0aW9uIHBhdHRlcm4odHlwZSwgdmFsdWUpIHtcbiAgICBpZiAoaXNUUyAmJiBpc01vZGlmaWVyKHZhbHVlKSkge1xuICAgICAgY3gubWFya2VkID0gXCJrZXl3b3JkXCI7XG4gICAgICByZXR1cm4gY29udChwYXR0ZXJuKTtcbiAgICB9XG4gICAgaWYgKHR5cGUgPT0gXCJ2YXJpYWJsZVwiKSB7XG4gICAgICByZWdpc3Rlcih2YWx1ZSk7XG4gICAgICByZXR1cm4gY29udCgpO1xuICAgIH1cbiAgICBpZiAodHlwZSA9PSBcInNwcmVhZFwiKSByZXR1cm4gY29udChwYXR0ZXJuKTtcbiAgICBpZiAodHlwZSA9PSBcIltcIikgcmV0dXJuIGNvbnRDb21tYXNlcChlbHRwYXR0ZXJuLCBcIl1cIik7XG4gICAgaWYgKHR5cGUgPT0gXCJ7XCIpIHJldHVybiBjb250Q29tbWFzZXAocHJvcHBhdHRlcm4sIFwifVwiKTtcbiAgfVxuICBmdW5jdGlvbiBwcm9wcGF0dGVybih0eXBlLCB2YWx1ZSkge1xuICAgIGlmICh0eXBlID09IFwidmFyaWFibGVcIiAmJiAhY3guc3RyZWFtLm1hdGNoKC9eXFxzKjovLCBmYWxzZSkpIHtcbiAgICAgIHJlZ2lzdGVyKHZhbHVlKTtcbiAgICAgIHJldHVybiBjb250KG1heWJlQXNzaWduKTtcbiAgICB9XG4gICAgaWYgKHR5cGUgPT0gXCJ2YXJpYWJsZVwiKSBjeC5tYXJrZWQgPSBcInByb3BlcnR5XCI7XG4gICAgaWYgKHR5cGUgPT0gXCJzcHJlYWRcIikgcmV0dXJuIGNvbnQocGF0dGVybik7XG4gICAgaWYgKHR5cGUgPT0gXCJ9XCIpIHJldHVybiBwYXNzKCk7XG4gICAgaWYgKHR5cGUgPT0gXCJbXCIpIHJldHVybiBjb250KGV4cHJlc3Npb24sIGV4cGVjdCgnXScpLCBleHBlY3QoJzonKSwgcHJvcHBhdHRlcm4pO1xuICAgIHJldHVybiBjb250KGV4cGVjdChcIjpcIiksIHBhdHRlcm4sIG1heWJlQXNzaWduKTtcbiAgfVxuICBmdW5jdGlvbiBlbHRwYXR0ZXJuKCkge1xuICAgIHJldHVybiBwYXNzKHBhdHRlcm4sIG1heWJlQXNzaWduKTtcbiAgfVxuICBmdW5jdGlvbiBtYXliZUFzc2lnbihfdHlwZSwgdmFsdWUpIHtcbiAgICBpZiAodmFsdWUgPT0gXCI9XCIpIHJldHVybiBjb250KGV4cHJlc3Npb25Ob0NvbW1hKTtcbiAgfVxuICBmdW5jdGlvbiB2YXJkZWZDb250KHR5cGUpIHtcbiAgICBpZiAodHlwZSA9PSBcIixcIikgcmV0dXJuIGNvbnQodmFyZGVmKTtcbiAgfVxuICBmdW5jdGlvbiBtYXliZWVsc2UodHlwZSwgdmFsdWUpIHtcbiAgICBpZiAodHlwZSA9PSBcImtleXdvcmQgYlwiICYmIHZhbHVlID09IFwiZWxzZVwiKSByZXR1cm4gY29udChwdXNobGV4KFwiZm9ybVwiLCBcImVsc2VcIiksIHN0YXRlbWVudCwgcG9wbGV4KTtcbiAgfVxuICBmdW5jdGlvbiBmb3JzcGVjKHR5cGUsIHZhbHVlKSB7XG4gICAgaWYgKHZhbHVlID09IFwiYXdhaXRcIikgcmV0dXJuIGNvbnQoZm9yc3BlYyk7XG4gICAgaWYgKHR5cGUgPT0gXCIoXCIpIHJldHVybiBjb250KHB1c2hsZXgoXCIpXCIpLCBmb3JzcGVjMSwgcG9wbGV4KTtcbiAgfVxuICBmdW5jdGlvbiBmb3JzcGVjMSh0eXBlKSB7XG4gICAgaWYgKHR5cGUgPT0gXCJ2YXJcIikgcmV0dXJuIGNvbnQodmFyZGVmLCBmb3JzcGVjMik7XG4gICAgaWYgKHR5cGUgPT0gXCJ2YXJpYWJsZVwiKSByZXR1cm4gY29udChmb3JzcGVjMik7XG4gICAgcmV0dXJuIHBhc3MoZm9yc3BlYzIpO1xuICB9XG4gIGZ1bmN0aW9uIGZvcnNwZWMyKHR5cGUsIHZhbHVlKSB7XG4gICAgaWYgKHR5cGUgPT0gXCIpXCIpIHJldHVybiBjb250KCk7XG4gICAgaWYgKHR5cGUgPT0gXCI7XCIpIHJldHVybiBjb250KGZvcnNwZWMyKTtcbiAgICBpZiAodmFsdWUgPT0gXCJpblwiIHx8IHZhbHVlID09IFwib2ZcIikge1xuICAgICAgY3gubWFya2VkID0gXCJrZXl3b3JkXCI7XG4gICAgICByZXR1cm4gY29udChleHByZXNzaW9uLCBmb3JzcGVjMik7XG4gICAgfVxuICAgIHJldHVybiBwYXNzKGV4cHJlc3Npb24sIGZvcnNwZWMyKTtcbiAgfVxuICBmdW5jdGlvbiBmdW5jdGlvbmRlZih0eXBlLCB2YWx1ZSkge1xuICAgIGlmICh2YWx1ZSA9PSBcIipcIikge1xuICAgICAgY3gubWFya2VkID0gXCJrZXl3b3JkXCI7XG4gICAgICByZXR1cm4gY29udChmdW5jdGlvbmRlZik7XG4gICAgfVxuICAgIGlmICh0eXBlID09IFwidmFyaWFibGVcIikge1xuICAgICAgcmVnaXN0ZXIodmFsdWUpO1xuICAgICAgcmV0dXJuIGNvbnQoZnVuY3Rpb25kZWYpO1xuICAgIH1cbiAgICBpZiAodHlwZSA9PSBcIihcIikgcmV0dXJuIGNvbnQocHVzaGNvbnRleHQsIHB1c2hsZXgoXCIpXCIpLCBjb21tYXNlcChmdW5hcmcsIFwiKVwiKSwgcG9wbGV4LCBtYXliZXJldHR5cGUsIHN0YXRlbWVudCwgcG9wY29udGV4dCk7XG4gICAgaWYgKGlzVFMgJiYgdmFsdWUgPT0gXCI8XCIpIHJldHVybiBjb250KHB1c2hsZXgoXCI+XCIpLCBjb21tYXNlcCh0eXBlcGFyYW0sIFwiPlwiKSwgcG9wbGV4LCBmdW5jdGlvbmRlZik7XG4gIH1cbiAgZnVuY3Rpb24gZnVuY3Rpb25kZWNsKHR5cGUsIHZhbHVlKSB7XG4gICAgaWYgKHZhbHVlID09IFwiKlwiKSB7XG4gICAgICBjeC5tYXJrZWQgPSBcImtleXdvcmRcIjtcbiAgICAgIHJldHVybiBjb250KGZ1bmN0aW9uZGVjbCk7XG4gICAgfVxuICAgIGlmICh0eXBlID09IFwidmFyaWFibGVcIikge1xuICAgICAgcmVnaXN0ZXIodmFsdWUpO1xuICAgICAgcmV0dXJuIGNvbnQoZnVuY3Rpb25kZWNsKTtcbiAgICB9XG4gICAgaWYgKHR5cGUgPT0gXCIoXCIpIHJldHVybiBjb250KHB1c2hjb250ZXh0LCBwdXNobGV4KFwiKVwiKSwgY29tbWFzZXAoZnVuYXJnLCBcIilcIiksIHBvcGxleCwgbWF5YmVyZXR0eXBlLCBwb3Bjb250ZXh0KTtcbiAgICBpZiAoaXNUUyAmJiB2YWx1ZSA9PSBcIjxcIikgcmV0dXJuIGNvbnQocHVzaGxleChcIj5cIiksIGNvbW1hc2VwKHR5cGVwYXJhbSwgXCI+XCIpLCBwb3BsZXgsIGZ1bmN0aW9uZGVjbCk7XG4gIH1cbiAgZnVuY3Rpb24gdHlwZW5hbWUodHlwZSwgdmFsdWUpIHtcbiAgICBpZiAodHlwZSA9PSBcImtleXdvcmRcIiB8fCB0eXBlID09IFwidmFyaWFibGVcIikge1xuICAgICAgY3gubWFya2VkID0gXCJ0eXBlXCI7XG4gICAgICByZXR1cm4gY29udCh0eXBlbmFtZSk7XG4gICAgfSBlbHNlIGlmICh2YWx1ZSA9PSBcIjxcIikge1xuICAgICAgcmV0dXJuIGNvbnQocHVzaGxleChcIj5cIiksIGNvbW1hc2VwKHR5cGVwYXJhbSwgXCI+XCIpLCBwb3BsZXgpO1xuICAgIH1cbiAgfVxuICBmdW5jdGlvbiBmdW5hcmcodHlwZSwgdmFsdWUpIHtcbiAgICBpZiAodmFsdWUgPT0gXCJAXCIpIGNvbnQoZXhwcmVzc2lvbiwgZnVuYXJnKTtcbiAgICBpZiAodHlwZSA9PSBcInNwcmVhZFwiKSByZXR1cm4gY29udChmdW5hcmcpO1xuICAgIGlmIChpc1RTICYmIGlzTW9kaWZpZXIodmFsdWUpKSB7XG4gICAgICBjeC5tYXJrZWQgPSBcImtleXdvcmRcIjtcbiAgICAgIHJldHVybiBjb250KGZ1bmFyZyk7XG4gICAgfVxuICAgIGlmIChpc1RTICYmIHR5cGUgPT0gXCJ0aGlzXCIpIHJldHVybiBjb250KG1heWJldHlwZSwgbWF5YmVBc3NpZ24pO1xuICAgIHJldHVybiBwYXNzKHBhdHRlcm4sIG1heWJldHlwZSwgbWF5YmVBc3NpZ24pO1xuICB9XG4gIGZ1bmN0aW9uIGNsYXNzRXhwcmVzc2lvbih0eXBlLCB2YWx1ZSkge1xuICAgIC8vIENsYXNzIGV4cHJlc3Npb25zIG1heSBoYXZlIGFuIG9wdGlvbmFsIG5hbWUuXG4gICAgaWYgKHR5cGUgPT0gXCJ2YXJpYWJsZVwiKSByZXR1cm4gY2xhc3NOYW1lKHR5cGUsIHZhbHVlKTtcbiAgICByZXR1cm4gY2xhc3NOYW1lQWZ0ZXIodHlwZSwgdmFsdWUpO1xuICB9XG4gIGZ1bmN0aW9uIGNsYXNzTmFtZSh0eXBlLCB2YWx1ZSkge1xuICAgIGlmICh0eXBlID09IFwidmFyaWFibGVcIikge1xuICAgICAgcmVnaXN0ZXIodmFsdWUpO1xuICAgICAgcmV0dXJuIGNvbnQoY2xhc3NOYW1lQWZ0ZXIpO1xuICAgIH1cbiAgfVxuICBmdW5jdGlvbiBjbGFzc05hbWVBZnRlcih0eXBlLCB2YWx1ZSkge1xuICAgIGlmICh2YWx1ZSA9PSBcIjxcIikgcmV0dXJuIGNvbnQocHVzaGxleChcIj5cIiksIGNvbW1hc2VwKHR5cGVwYXJhbSwgXCI+XCIpLCBwb3BsZXgsIGNsYXNzTmFtZUFmdGVyKTtcbiAgICBpZiAodmFsdWUgPT0gXCJleHRlbmRzXCIgfHwgdmFsdWUgPT0gXCJpbXBsZW1lbnRzXCIgfHwgaXNUUyAmJiB0eXBlID09IFwiLFwiKSB7XG4gICAgICBpZiAodmFsdWUgPT0gXCJpbXBsZW1lbnRzXCIpIGN4Lm1hcmtlZCA9IFwia2V5d29yZFwiO1xuICAgICAgcmV0dXJuIGNvbnQoaXNUUyA/IHR5cGVleHByIDogZXhwcmVzc2lvbiwgY2xhc3NOYW1lQWZ0ZXIpO1xuICAgIH1cbiAgICBpZiAodHlwZSA9PSBcIntcIikgcmV0dXJuIGNvbnQocHVzaGxleChcIn1cIiksIGNsYXNzQm9keSwgcG9wbGV4KTtcbiAgfVxuICBmdW5jdGlvbiBjbGFzc0JvZHkodHlwZSwgdmFsdWUpIHtcbiAgICBpZiAodHlwZSA9PSBcImFzeW5jXCIgfHwgdHlwZSA9PSBcInZhcmlhYmxlXCIgJiYgKHZhbHVlID09IFwic3RhdGljXCIgfHwgdmFsdWUgPT0gXCJnZXRcIiB8fCB2YWx1ZSA9PSBcInNldFwiIHx8IGlzVFMgJiYgaXNNb2RpZmllcih2YWx1ZSkpICYmIGN4LnN0cmVhbS5tYXRjaCgvXlxccysjP1tcXHckXFx4YTEtXFx1ZmZmZl0vLCBmYWxzZSkpIHtcbiAgICAgIGN4Lm1hcmtlZCA9IFwia2V5d29yZFwiO1xuICAgICAgcmV0dXJuIGNvbnQoY2xhc3NCb2R5KTtcbiAgICB9XG4gICAgaWYgKHR5cGUgPT0gXCJ2YXJpYWJsZVwiIHx8IGN4LnN0eWxlID09IFwia2V5d29yZFwiKSB7XG4gICAgICBjeC5tYXJrZWQgPSBcInByb3BlcnR5XCI7XG4gICAgICByZXR1cm4gY29udChjbGFzc2ZpZWxkLCBjbGFzc0JvZHkpO1xuICAgIH1cbiAgICBpZiAodHlwZSA9PSBcIm51bWJlclwiIHx8IHR5cGUgPT0gXCJzdHJpbmdcIikgcmV0dXJuIGNvbnQoY2xhc3NmaWVsZCwgY2xhc3NCb2R5KTtcbiAgICBpZiAodHlwZSA9PSBcIltcIikgcmV0dXJuIGNvbnQoZXhwcmVzc2lvbiwgbWF5YmV0eXBlLCBleHBlY3QoXCJdXCIpLCBjbGFzc2ZpZWxkLCBjbGFzc0JvZHkpO1xuICAgIGlmICh2YWx1ZSA9PSBcIipcIikge1xuICAgICAgY3gubWFya2VkID0gXCJrZXl3b3JkXCI7XG4gICAgICByZXR1cm4gY29udChjbGFzc0JvZHkpO1xuICAgIH1cbiAgICBpZiAoaXNUUyAmJiB0eXBlID09IFwiKFwiKSByZXR1cm4gcGFzcyhmdW5jdGlvbmRlY2wsIGNsYXNzQm9keSk7XG4gICAgaWYgKHR5cGUgPT0gXCI7XCIgfHwgdHlwZSA9PSBcIixcIikgcmV0dXJuIGNvbnQoY2xhc3NCb2R5KTtcbiAgICBpZiAodHlwZSA9PSBcIn1cIikgcmV0dXJuIGNvbnQoKTtcbiAgICBpZiAodmFsdWUgPT0gXCJAXCIpIHJldHVybiBjb250KGV4cHJlc3Npb24sIGNsYXNzQm9keSk7XG4gIH1cbiAgZnVuY3Rpb24gY2xhc3NmaWVsZCh0eXBlLCB2YWx1ZSkge1xuICAgIGlmICh2YWx1ZSA9PSBcIiFcIiB8fCB2YWx1ZSA9PSBcIj9cIikgcmV0dXJuIGNvbnQoY2xhc3NmaWVsZCk7XG4gICAgaWYgKHR5cGUgPT0gXCI6XCIpIHJldHVybiBjb250KHR5cGVleHByLCBtYXliZUFzc2lnbik7XG4gICAgaWYgKHZhbHVlID09IFwiPVwiKSByZXR1cm4gY29udChleHByZXNzaW9uTm9Db21tYSk7XG4gICAgdmFyIGNvbnRleHQgPSBjeC5zdGF0ZS5sZXhpY2FsLnByZXYsXG4gICAgICBpc0ludGVyZmFjZSA9IGNvbnRleHQgJiYgY29udGV4dC5pbmZvID09IFwiaW50ZXJmYWNlXCI7XG4gICAgcmV0dXJuIHBhc3MoaXNJbnRlcmZhY2UgPyBmdW5jdGlvbmRlY2wgOiBmdW5jdGlvbmRlZik7XG4gIH1cbiAgZnVuY3Rpb24gYWZ0ZXJFeHBvcnQodHlwZSwgdmFsdWUpIHtcbiAgICBpZiAodmFsdWUgPT0gXCIqXCIpIHtcbiAgICAgIGN4Lm1hcmtlZCA9IFwia2V5d29yZFwiO1xuICAgICAgcmV0dXJuIGNvbnQobWF5YmVGcm9tLCBleHBlY3QoXCI7XCIpKTtcbiAgICB9XG4gICAgaWYgKHZhbHVlID09IFwiZGVmYXVsdFwiKSB7XG4gICAgICBjeC5tYXJrZWQgPSBcImtleXdvcmRcIjtcbiAgICAgIHJldHVybiBjb250KGV4cHJlc3Npb24sIGV4cGVjdChcIjtcIikpO1xuICAgIH1cbiAgICBpZiAodHlwZSA9PSBcIntcIikgcmV0dXJuIGNvbnQoY29tbWFzZXAoZXhwb3J0RmllbGQsIFwifVwiKSwgbWF5YmVGcm9tLCBleHBlY3QoXCI7XCIpKTtcbiAgICByZXR1cm4gcGFzcyhzdGF0ZW1lbnQpO1xuICB9XG4gIGZ1bmN0aW9uIGV4cG9ydEZpZWxkKHR5cGUsIHZhbHVlKSB7XG4gICAgaWYgKHZhbHVlID09IFwiYXNcIikge1xuICAgICAgY3gubWFya2VkID0gXCJrZXl3b3JkXCI7XG4gICAgICByZXR1cm4gY29udChleHBlY3QoXCJ2YXJpYWJsZVwiKSk7XG4gICAgfVxuICAgIGlmICh0eXBlID09IFwidmFyaWFibGVcIikgcmV0dXJuIHBhc3MoZXhwcmVzc2lvbk5vQ29tbWEsIGV4cG9ydEZpZWxkKTtcbiAgfVxuICBmdW5jdGlvbiBhZnRlckltcG9ydCh0eXBlKSB7XG4gICAgaWYgKHR5cGUgPT0gXCJzdHJpbmdcIikgcmV0dXJuIGNvbnQoKTtcbiAgICBpZiAodHlwZSA9PSBcIihcIikgcmV0dXJuIHBhc3MoZXhwcmVzc2lvbik7XG4gICAgaWYgKHR5cGUgPT0gXCIuXCIpIHJldHVybiBwYXNzKG1heWJlb3BlcmF0b3JDb21tYSk7XG4gICAgcmV0dXJuIHBhc3MoaW1wb3J0U3BlYywgbWF5YmVNb3JlSW1wb3J0cywgbWF5YmVGcm9tKTtcbiAgfVxuICBmdW5jdGlvbiBpbXBvcnRTcGVjKHR5cGUsIHZhbHVlKSB7XG4gICAgaWYgKHR5cGUgPT0gXCJ7XCIpIHJldHVybiBjb250Q29tbWFzZXAoaW1wb3J0U3BlYywgXCJ9XCIpO1xuICAgIGlmICh0eXBlID09IFwidmFyaWFibGVcIikgcmVnaXN0ZXIodmFsdWUpO1xuICAgIGlmICh2YWx1ZSA9PSBcIipcIikgY3gubWFya2VkID0gXCJrZXl3b3JkXCI7XG4gICAgcmV0dXJuIGNvbnQobWF5YmVBcyk7XG4gIH1cbiAgZnVuY3Rpb24gbWF5YmVNb3JlSW1wb3J0cyh0eXBlKSB7XG4gICAgaWYgKHR5cGUgPT0gXCIsXCIpIHJldHVybiBjb250KGltcG9ydFNwZWMsIG1heWJlTW9yZUltcG9ydHMpO1xuICB9XG4gIGZ1bmN0aW9uIG1heWJlQXMoX3R5cGUsIHZhbHVlKSB7XG4gICAgaWYgKHZhbHVlID09IFwiYXNcIikge1xuICAgICAgY3gubWFya2VkID0gXCJrZXl3b3JkXCI7XG4gICAgICByZXR1cm4gY29udChpbXBvcnRTcGVjKTtcbiAgICB9XG4gIH1cbiAgZnVuY3Rpb24gbWF5YmVGcm9tKF90eXBlLCB2YWx1ZSkge1xuICAgIGlmICh2YWx1ZSA9PSBcImZyb21cIikge1xuICAgICAgY3gubWFya2VkID0gXCJrZXl3b3JkXCI7XG4gICAgICByZXR1cm4gY29udChleHByZXNzaW9uKTtcbiAgICB9XG4gIH1cbiAgZnVuY3Rpb24gYXJyYXlMaXRlcmFsKHR5cGUpIHtcbiAgICBpZiAodHlwZSA9PSBcIl1cIikgcmV0dXJuIGNvbnQoKTtcbiAgICByZXR1cm4gcGFzcyhjb21tYXNlcChleHByZXNzaW9uTm9Db21tYSwgXCJdXCIpKTtcbiAgfVxuICBmdW5jdGlvbiBlbnVtZGVmKCkge1xuICAgIHJldHVybiBwYXNzKHB1c2hsZXgoXCJmb3JtXCIpLCBwYXR0ZXJuLCBleHBlY3QoXCJ7XCIpLCBwdXNobGV4KFwifVwiKSwgY29tbWFzZXAoZW51bW1lbWJlciwgXCJ9XCIpLCBwb3BsZXgsIHBvcGxleCk7XG4gIH1cbiAgZnVuY3Rpb24gZW51bW1lbWJlcigpIHtcbiAgICByZXR1cm4gcGFzcyhwYXR0ZXJuLCBtYXliZUFzc2lnbik7XG4gIH1cbiAgZnVuY3Rpb24gaXNDb250aW51ZWRTdGF0ZW1lbnQoc3RhdGUsIHRleHRBZnRlcikge1xuICAgIHJldHVybiBzdGF0ZS5sYXN0VHlwZSA9PSBcIm9wZXJhdG9yXCIgfHwgc3RhdGUubGFzdFR5cGUgPT0gXCIsXCIgfHwgaXNPcGVyYXRvckNoYXIudGVzdCh0ZXh0QWZ0ZXIuY2hhckF0KDApKSB8fCAvWywuXS8udGVzdCh0ZXh0QWZ0ZXIuY2hhckF0KDApKTtcbiAgfVxuICBmdW5jdGlvbiBleHByZXNzaW9uQWxsb3dlZChzdHJlYW0sIHN0YXRlLCBiYWNrVXApIHtcbiAgICByZXR1cm4gc3RhdGUudG9rZW5pemUgPT0gdG9rZW5CYXNlICYmIC9eKD86b3BlcmF0b3J8c29mfGtleXdvcmQgW2JjZF18Y2FzZXxuZXd8ZXhwb3J0fGRlZmF1bHR8c3ByZWFkfFtcXFt7fVxcKCw7Ol18PT4pJC8udGVzdChzdGF0ZS5sYXN0VHlwZSkgfHwgc3RhdGUubGFzdFR5cGUgPT0gXCJxdWFzaVwiICYmIC9cXHtcXHMqJC8udGVzdChzdHJlYW0uc3RyaW5nLnNsaWNlKDAsIHN0cmVhbS5wb3MgLSAoYmFja1VwIHx8IDApKSk7XG4gIH1cblxuICAvLyBJbnRlcmZhY2VcblxuICByZXR1cm4ge1xuICAgIG5hbWU6IHBhcnNlckNvbmZpZy5uYW1lLFxuICAgIHN0YXJ0U3RhdGU6IGZ1bmN0aW9uIChpbmRlbnRVbml0KSB7XG4gICAgICB2YXIgc3RhdGUgPSB7XG4gICAgICAgIHRva2VuaXplOiB0b2tlbkJhc2UsXG4gICAgICAgIGxhc3RUeXBlOiBcInNvZlwiLFxuICAgICAgICBjYzogW10sXG4gICAgICAgIGxleGljYWw6IG5ldyBKU0xleGljYWwoLWluZGVudFVuaXQsIDAsIFwiYmxvY2tcIiwgZmFsc2UpLFxuICAgICAgICBsb2NhbFZhcnM6IHBhcnNlckNvbmZpZy5sb2NhbFZhcnMsXG4gICAgICAgIGNvbnRleHQ6IHBhcnNlckNvbmZpZy5sb2NhbFZhcnMgJiYgbmV3IENvbnRleHQobnVsbCwgbnVsbCwgZmFsc2UpLFxuICAgICAgICBpbmRlbnRlZDogMFxuICAgICAgfTtcbiAgICAgIGlmIChwYXJzZXJDb25maWcuZ2xvYmFsVmFycyAmJiB0eXBlb2YgcGFyc2VyQ29uZmlnLmdsb2JhbFZhcnMgPT0gXCJvYmplY3RcIikgc3RhdGUuZ2xvYmFsVmFycyA9IHBhcnNlckNvbmZpZy5nbG9iYWxWYXJzO1xuICAgICAgcmV0dXJuIHN0YXRlO1xuICAgIH0sXG4gICAgdG9rZW46IGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgICBpZiAoc3RyZWFtLnNvbCgpKSB7XG4gICAgICAgIGlmICghc3RhdGUubGV4aWNhbC5oYXNPd25Qcm9wZXJ0eShcImFsaWduXCIpKSBzdGF0ZS5sZXhpY2FsLmFsaWduID0gZmFsc2U7XG4gICAgICAgIHN0YXRlLmluZGVudGVkID0gc3RyZWFtLmluZGVudGF0aW9uKCk7XG4gICAgICAgIGZpbmRGYXRBcnJvdyhzdHJlYW0sIHN0YXRlKTtcbiAgICAgIH1cbiAgICAgIGlmIChzdGF0ZS50b2tlbml6ZSAhPSB0b2tlbkNvbW1lbnQgJiYgc3RyZWFtLmVhdFNwYWNlKCkpIHJldHVybiBudWxsO1xuICAgICAgdmFyIHN0eWxlID0gc3RhdGUudG9rZW5pemUoc3RyZWFtLCBzdGF0ZSk7XG4gICAgICBpZiAodHlwZSA9PSBcImNvbW1lbnRcIikgcmV0dXJuIHN0eWxlO1xuICAgICAgc3RhdGUubGFzdFR5cGUgPSB0eXBlID09IFwib3BlcmF0b3JcIiAmJiAoY29udGVudCA9PSBcIisrXCIgfHwgY29udGVudCA9PSBcIi0tXCIpID8gXCJpbmNkZWNcIiA6IHR5cGU7XG4gICAgICByZXR1cm4gcGFyc2VKUyhzdGF0ZSwgc3R5bGUsIHR5cGUsIGNvbnRlbnQsIHN0cmVhbSk7XG4gICAgfSxcbiAgICBpbmRlbnQ6IGZ1bmN0aW9uIChzdGF0ZSwgdGV4dEFmdGVyLCBjeCkge1xuICAgICAgaWYgKHN0YXRlLnRva2VuaXplID09IHRva2VuQ29tbWVudCB8fCBzdGF0ZS50b2tlbml6ZSA9PSB0b2tlblF1YXNpKSByZXR1cm4gbnVsbDtcbiAgICAgIGlmIChzdGF0ZS50b2tlbml6ZSAhPSB0b2tlbkJhc2UpIHJldHVybiAwO1xuICAgICAgdmFyIGZpcnN0Q2hhciA9IHRleHRBZnRlciAmJiB0ZXh0QWZ0ZXIuY2hhckF0KDApLFxuICAgICAgICBsZXhpY2FsID0gc3RhdGUubGV4aWNhbCxcbiAgICAgICAgdG9wO1xuICAgICAgLy8gS2x1ZGdlIHRvIHByZXZlbnQgJ21heWJlbHNlJyBmcm9tIGJsb2NraW5nIGxleGljYWwgc2NvcGUgcG9wc1xuICAgICAgaWYgKCEvXlxccyplbHNlXFxiLy50ZXN0KHRleHRBZnRlcikpIGZvciAodmFyIGkgPSBzdGF0ZS5jYy5sZW5ndGggLSAxOyBpID49IDA7IC0taSkge1xuICAgICAgICB2YXIgYyA9IHN0YXRlLmNjW2ldO1xuICAgICAgICBpZiAoYyA9PSBwb3BsZXgpIGxleGljYWwgPSBsZXhpY2FsLnByZXY7ZWxzZSBpZiAoYyAhPSBtYXliZWVsc2UgJiYgYyAhPSBwb3Bjb250ZXh0KSBicmVhaztcbiAgICAgIH1cbiAgICAgIHdoaWxlICgobGV4aWNhbC50eXBlID09IFwic3RhdFwiIHx8IGxleGljYWwudHlwZSA9PSBcImZvcm1cIikgJiYgKGZpcnN0Q2hhciA9PSBcIn1cIiB8fCAodG9wID0gc3RhdGUuY2Nbc3RhdGUuY2MubGVuZ3RoIC0gMV0pICYmICh0b3AgPT0gbWF5YmVvcGVyYXRvckNvbW1hIHx8IHRvcCA9PSBtYXliZW9wZXJhdG9yTm9Db21tYSkgJiYgIS9eWyxcXC49K1xcLSo6P1tcXChdLy50ZXN0KHRleHRBZnRlcikpKSBsZXhpY2FsID0gbGV4aWNhbC5wcmV2O1xuICAgICAgaWYgKHN0YXRlbWVudEluZGVudCAmJiBsZXhpY2FsLnR5cGUgPT0gXCIpXCIgJiYgbGV4aWNhbC5wcmV2LnR5cGUgPT0gXCJzdGF0XCIpIGxleGljYWwgPSBsZXhpY2FsLnByZXY7XG4gICAgICB2YXIgdHlwZSA9IGxleGljYWwudHlwZSxcbiAgICAgICAgY2xvc2luZyA9IGZpcnN0Q2hhciA9PSB0eXBlO1xuICAgICAgaWYgKHR5cGUgPT0gXCJ2YXJkZWZcIikgcmV0dXJuIGxleGljYWwuaW5kZW50ZWQgKyAoc3RhdGUubGFzdFR5cGUgPT0gXCJvcGVyYXRvclwiIHx8IHN0YXRlLmxhc3RUeXBlID09IFwiLFwiID8gbGV4aWNhbC5pbmZvLmxlbmd0aCArIDEgOiAwKTtlbHNlIGlmICh0eXBlID09IFwiZm9ybVwiICYmIGZpcnN0Q2hhciA9PSBcIntcIikgcmV0dXJuIGxleGljYWwuaW5kZW50ZWQ7ZWxzZSBpZiAodHlwZSA9PSBcImZvcm1cIikgcmV0dXJuIGxleGljYWwuaW5kZW50ZWQgKyBjeC51bml0O2Vsc2UgaWYgKHR5cGUgPT0gXCJzdGF0XCIpIHJldHVybiBsZXhpY2FsLmluZGVudGVkICsgKGlzQ29udGludWVkU3RhdGVtZW50KHN0YXRlLCB0ZXh0QWZ0ZXIpID8gc3RhdGVtZW50SW5kZW50IHx8IGN4LnVuaXQgOiAwKTtlbHNlIGlmIChsZXhpY2FsLmluZm8gPT0gXCJzd2l0Y2hcIiAmJiAhY2xvc2luZyAmJiBwYXJzZXJDb25maWcuZG91YmxlSW5kZW50U3dpdGNoICE9IGZhbHNlKSByZXR1cm4gbGV4aWNhbC5pbmRlbnRlZCArICgvXig/OmNhc2V8ZGVmYXVsdClcXGIvLnRlc3QodGV4dEFmdGVyKSA/IGN4LnVuaXQgOiAyICogY3gudW5pdCk7ZWxzZSBpZiAobGV4aWNhbC5hbGlnbikgcmV0dXJuIGxleGljYWwuY29sdW1uICsgKGNsb3NpbmcgPyAwIDogMSk7ZWxzZSByZXR1cm4gbGV4aWNhbC5pbmRlbnRlZCArIChjbG9zaW5nID8gMCA6IGN4LnVuaXQpO1xuICAgIH0sXG4gICAgbGFuZ3VhZ2VEYXRhOiB7XG4gICAgICBpbmRlbnRPbklucHV0OiAvXlxccyooPzpjYXNlIC4qPzp8ZGVmYXVsdDp8XFx7fFxcfSkkLyxcbiAgICAgIGNvbW1lbnRUb2tlbnM6IGpzb25Nb2RlID8gdW5kZWZpbmVkIDoge1xuICAgICAgICBsaW5lOiBcIi8vXCIsXG4gICAgICAgIGJsb2NrOiB7XG4gICAgICAgICAgb3BlbjogXCIvKlwiLFxuICAgICAgICAgIGNsb3NlOiBcIiovXCJcbiAgICAgICAgfVxuICAgICAgfSxcbiAgICAgIGNsb3NlQnJhY2tldHM6IHtcbiAgICAgICAgYnJhY2tldHM6IFtcIihcIiwgXCJbXCIsIFwie1wiLCBcIidcIiwgJ1wiJywgXCJgXCJdXG4gICAgICB9LFxuICAgICAgd29yZENoYXJzOiBcIiRcIlxuICAgIH1cbiAgfTtcbn1cbjtcbmV4cG9ydCBjb25zdCBqYXZhc2NyaXB0ID0gbWtKYXZhU2NyaXB0KHtcbiAgbmFtZTogXCJqYXZhc2NyaXB0XCJcbn0pO1xuZXhwb3J0IGNvbnN0IGpzb24gPSBta0phdmFTY3JpcHQoe1xuICBuYW1lOiBcImpzb25cIixcbiAganNvbjogdHJ1ZVxufSk7XG5leHBvcnQgY29uc3QganNvbmxkID0gbWtKYXZhU2NyaXB0KHtcbiAgbmFtZTogXCJqc29uXCIsXG4gIGpzb25sZDogdHJ1ZVxufSk7XG5leHBvcnQgY29uc3QgdHlwZXNjcmlwdCA9IG1rSmF2YVNjcmlwdCh7XG4gIG5hbWU6IFwidHlwZXNjcmlwdFwiLFxuICB0eXBlc2NyaXB0OiB0cnVlXG59KTsiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=