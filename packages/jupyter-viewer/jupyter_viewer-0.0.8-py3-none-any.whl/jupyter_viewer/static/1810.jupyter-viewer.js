"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[1810],{

/***/ 91810:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "cython": () => (/* binding */ cython),
/* harmony export */   "mkPython": () => (/* binding */ mkPython),
/* harmony export */   "python": () => (/* binding */ python)
/* harmony export */ });
function wordRegexp(words) {
  return new RegExp("^((" + words.join(")|(") + "))\\b");
}
var wordOperators = wordRegexp(["and", "or", "not", "is"]);
var commonKeywords = ["as", "assert", "break", "class", "continue", "def", "del", "elif", "else", "except", "finally", "for", "from", "global", "if", "import", "lambda", "pass", "raise", "return", "try", "while", "with", "yield", "in", "False", "True"];
var commonBuiltins = ["abs", "all", "any", "bin", "bool", "bytearray", "callable", "chr", "classmethod", "compile", "complex", "delattr", "dict", "dir", "divmod", "enumerate", "eval", "filter", "float", "format", "frozenset", "getattr", "globals", "hasattr", "hash", "help", "hex", "id", "input", "int", "isinstance", "issubclass", "iter", "len", "list", "locals", "map", "max", "memoryview", "min", "next", "object", "oct", "open", "ord", "pow", "property", "range", "repr", "reversed", "round", "set", "setattr", "slice", "sorted", "staticmethod", "str", "sum", "super", "tuple", "type", "vars", "zip", "__import__", "NotImplemented", "Ellipsis", "__debug__"];
function top(state) {
  return state.scopes[state.scopes.length - 1];
}
function mkPython(parserConf) {
  var ERRORCLASS = "error";
  var delimiters = parserConf.delimiters || parserConf.singleDelimiters || /^[\(\)\[\]\{\}@,:`=;\.\\]/;
  //               (Backwards-compatibility with old, cumbersome config system)
  var operators = [parserConf.singleOperators, parserConf.doubleOperators, parserConf.doubleDelimiters, parserConf.tripleDelimiters, parserConf.operators || /^([-+*/%\/&|^]=?|[<>=]+|\/\/=?|\*\*=?|!=|[~!@]|\.\.\.)/];
  for (var i = 0; i < operators.length; i++) if (!operators[i]) operators.splice(i--, 1);
  var hangingIndent = parserConf.hangingIndent;
  var myKeywords = commonKeywords,
    myBuiltins = commonBuiltins;
  if (parserConf.extra_keywords != undefined) myKeywords = myKeywords.concat(parserConf.extra_keywords);
  if (parserConf.extra_builtins != undefined) myBuiltins = myBuiltins.concat(parserConf.extra_builtins);
  var py3 = !(parserConf.version && Number(parserConf.version) < 3);
  if (py3) {
    // since http://legacy.python.org/dev/peps/pep-0465/ @ is also an operator
    var identifiers = parserConf.identifiers || /^[_A-Za-z\u00A1-\uFFFF][_A-Za-z0-9\u00A1-\uFFFF]*/;
    myKeywords = myKeywords.concat(["nonlocal", "None", "aiter", "anext", "async", "await", "breakpoint", "match", "case"]);
    myBuiltins = myBuiltins.concat(["ascii", "bytes", "exec", "print"]);
    var stringPrefixes = new RegExp("^(([rbuf]|(br)|(rb)|(fr)|(rf))?('{3}|\"{3}|['\"]))", "i");
  } else {
    var identifiers = parserConf.identifiers || /^[_A-Za-z][_A-Za-z0-9]*/;
    myKeywords = myKeywords.concat(["exec", "print"]);
    myBuiltins = myBuiltins.concat(["apply", "basestring", "buffer", "cmp", "coerce", "execfile", "file", "intern", "long", "raw_input", "reduce", "reload", "unichr", "unicode", "xrange", "None"]);
    var stringPrefixes = new RegExp("^(([rubf]|(ur)|(br))?('{3}|\"{3}|['\"]))", "i");
  }
  var keywords = wordRegexp(myKeywords);
  var builtins = wordRegexp(myBuiltins);

  // tokenizers
  function tokenBase(stream, state) {
    var sol = stream.sol() && state.lastToken != "\\";
    if (sol) state.indent = stream.indentation();
    // Handle scope changes
    if (sol && top(state).type == "py") {
      var scopeOffset = top(state).offset;
      if (stream.eatSpace()) {
        var lineOffset = stream.indentation();
        if (lineOffset > scopeOffset) pushPyScope(stream, state);else if (lineOffset < scopeOffset && dedent(stream, state) && stream.peek() != "#") state.errorToken = true;
        return null;
      } else {
        var style = tokenBaseInner(stream, state);
        if (scopeOffset > 0 && dedent(stream, state)) style += " " + ERRORCLASS;
        return style;
      }
    }
    return tokenBaseInner(stream, state);
  }
  function tokenBaseInner(stream, state, inFormat) {
    if (stream.eatSpace()) return null;

    // Handle Comments
    if (!inFormat && stream.match(/^#.*/)) return "comment";

    // Handle Number Literals
    if (stream.match(/^[0-9\.]/, false)) {
      var floatLiteral = false;
      // Floats
      if (stream.match(/^[\d_]*\.\d+(e[\+\-]?\d+)?/i)) {
        floatLiteral = true;
      }
      if (stream.match(/^[\d_]+\.\d*/)) {
        floatLiteral = true;
      }
      if (stream.match(/^\.\d+/)) {
        floatLiteral = true;
      }
      if (floatLiteral) {
        // Float literals may be "imaginary"
        stream.eat(/J/i);
        return "number";
      }
      // Integers
      var intLiteral = false;
      // Hex
      if (stream.match(/^0x[0-9a-f_]+/i)) intLiteral = true;
      // Binary
      if (stream.match(/^0b[01_]+/i)) intLiteral = true;
      // Octal
      if (stream.match(/^0o[0-7_]+/i)) intLiteral = true;
      // Decimal
      if (stream.match(/^[1-9][\d_]*(e[\+\-]?[\d_]+)?/)) {
        // Decimal literals may be "imaginary"
        stream.eat(/J/i);
        // TODO - Can you have imaginary longs?
        intLiteral = true;
      }
      // Zero by itself with no other piece of number.
      if (stream.match(/^0(?![\dx])/i)) intLiteral = true;
      if (intLiteral) {
        // Integer literals may be "long"
        stream.eat(/L/i);
        return "number";
      }
    }

    // Handle Strings
    if (stream.match(stringPrefixes)) {
      var isFmtString = stream.current().toLowerCase().indexOf('f') !== -1;
      if (!isFmtString) {
        state.tokenize = tokenStringFactory(stream.current(), state.tokenize);
        return state.tokenize(stream, state);
      } else {
        state.tokenize = formatStringFactory(stream.current(), state.tokenize);
        return state.tokenize(stream, state);
      }
    }
    for (var i = 0; i < operators.length; i++) if (stream.match(operators[i])) return "operator";
    if (stream.match(delimiters)) return "punctuation";
    if (state.lastToken == "." && stream.match(identifiers)) return "property";
    if (stream.match(keywords) || stream.match(wordOperators)) return "keyword";
    if (stream.match(builtins)) return "builtin";
    if (stream.match(/^(self|cls)\b/)) return "self";
    if (stream.match(identifiers)) {
      if (state.lastToken == "def" || state.lastToken == "class") return "def";
      return "variable";
    }

    // Handle non-detected items
    stream.next();
    return inFormat ? null : ERRORCLASS;
  }
  function formatStringFactory(delimiter, tokenOuter) {
    while ("rubf".indexOf(delimiter.charAt(0).toLowerCase()) >= 0) delimiter = delimiter.substr(1);
    var singleline = delimiter.length == 1;
    var OUTCLASS = "string";
    function tokenNestedExpr(depth) {
      return function (stream, state) {
        var inner = tokenBaseInner(stream, state, true);
        if (inner == "punctuation") {
          if (stream.current() == "{") {
            state.tokenize = tokenNestedExpr(depth + 1);
          } else if (stream.current() == "}") {
            if (depth > 1) state.tokenize = tokenNestedExpr(depth - 1);else state.tokenize = tokenString;
          }
        }
        return inner;
      };
    }
    function tokenString(stream, state) {
      while (!stream.eol()) {
        stream.eatWhile(/[^'"\{\}\\]/);
        if (stream.eat("\\")) {
          stream.next();
          if (singleline && stream.eol()) return OUTCLASS;
        } else if (stream.match(delimiter)) {
          state.tokenize = tokenOuter;
          return OUTCLASS;
        } else if (stream.match('{{')) {
          // ignore {{ in f-str
          return OUTCLASS;
        } else if (stream.match('{', false)) {
          // switch to nested mode
          state.tokenize = tokenNestedExpr(0);
          if (stream.current()) return OUTCLASS;else return state.tokenize(stream, state);
        } else if (stream.match('}}')) {
          return OUTCLASS;
        } else if (stream.match('}')) {
          // single } in f-string is an error
          return ERRORCLASS;
        } else {
          stream.eat(/['"]/);
        }
      }
      if (singleline) {
        if (parserConf.singleLineStringErrors) return ERRORCLASS;else state.tokenize = tokenOuter;
      }
      return OUTCLASS;
    }
    tokenString.isString = true;
    return tokenString;
  }
  function tokenStringFactory(delimiter, tokenOuter) {
    while ("rubf".indexOf(delimiter.charAt(0).toLowerCase()) >= 0) delimiter = delimiter.substr(1);
    var singleline = delimiter.length == 1;
    var OUTCLASS = "string";
    function tokenString(stream, state) {
      while (!stream.eol()) {
        stream.eatWhile(/[^'"\\]/);
        if (stream.eat("\\")) {
          stream.next();
          if (singleline && stream.eol()) return OUTCLASS;
        } else if (stream.match(delimiter)) {
          state.tokenize = tokenOuter;
          return OUTCLASS;
        } else {
          stream.eat(/['"]/);
        }
      }
      if (singleline) {
        if (parserConf.singleLineStringErrors) return ERRORCLASS;else state.tokenize = tokenOuter;
      }
      return OUTCLASS;
    }
    tokenString.isString = true;
    return tokenString;
  }
  function pushPyScope(stream, state) {
    while (top(state).type != "py") state.scopes.pop();
    state.scopes.push({
      offset: top(state).offset + stream.indentUnit,
      type: "py",
      align: null
    });
  }
  function pushBracketScope(stream, state, type) {
    var align = stream.match(/^[\s\[\{\(]*(?:#|$)/, false) ? null : stream.column() + 1;
    state.scopes.push({
      offset: state.indent + (hangingIndent || stream.indentUnit),
      type: type,
      align: align
    });
  }
  function dedent(stream, state) {
    var indented = stream.indentation();
    while (state.scopes.length > 1 && top(state).offset > indented) {
      if (top(state).type != "py") return true;
      state.scopes.pop();
    }
    return top(state).offset != indented;
  }
  function tokenLexer(stream, state) {
    if (stream.sol()) {
      state.beginningOfLine = true;
      state.dedent = false;
    }
    var style = state.tokenize(stream, state);
    var current = stream.current();

    // Handle decorators
    if (state.beginningOfLine && current == "@") return stream.match(identifiers, false) ? "meta" : py3 ? "operator" : ERRORCLASS;
    if (/\S/.test(current)) state.beginningOfLine = false;
    if ((style == "variable" || style == "builtin") && state.lastToken == "meta") style = "meta";

    // Handle scope changes.
    if (current == "pass" || current == "return") state.dedent = true;
    if (current == "lambda") state.lambda = true;
    if (current == ":" && !state.lambda && top(state).type == "py" && stream.match(/^\s*(?:#|$)/, false)) pushPyScope(stream, state);
    if (current.length == 1 && !/string|comment/.test(style)) {
      var delimiter_index = "[({".indexOf(current);
      if (delimiter_index != -1) pushBracketScope(stream, state, "])}".slice(delimiter_index, delimiter_index + 1));
      delimiter_index = "])}".indexOf(current);
      if (delimiter_index != -1) {
        if (top(state).type == current) state.indent = state.scopes.pop().offset - (hangingIndent || stream.indentUnit);else return ERRORCLASS;
      }
    }
    if (state.dedent && stream.eol() && top(state).type == "py" && state.scopes.length > 1) state.scopes.pop();
    return style;
  }
  return {
    name: "python",
    startState: function () {
      return {
        tokenize: tokenBase,
        scopes: [{
          offset: 0,
          type: "py",
          align: null
        }],
        indent: 0,
        lastToken: null,
        lambda: false,
        dedent: 0
      };
    },
    token: function (stream, state) {
      var addErr = state.errorToken;
      if (addErr) state.errorToken = false;
      var style = tokenLexer(stream, state);
      if (style && style != "comment") state.lastToken = style == "keyword" || style == "punctuation" ? stream.current() : style;
      if (style == "punctuation") style = null;
      if (stream.eol() && state.lambda) state.lambda = false;
      return addErr ? ERRORCLASS : style;
    },
    indent: function (state, textAfter, cx) {
      if (state.tokenize != tokenBase) return state.tokenize.isString ? null : 0;
      var scope = top(state);
      var closing = scope.type == textAfter.charAt(0) || scope.type == "py" && !state.dedent && /^(else:|elif |except |finally:)/.test(textAfter);
      if (scope.align != null) return scope.align - (closing ? 1 : 0);else return scope.offset - (closing ? hangingIndent || cx.unit : 0);
    },
    languageData: {
      autocomplete: commonKeywords.concat(commonBuiltins).concat(["exec", "print"]),
      indentOnInput: /^\s*([\}\]\)]|else:|elif |except |finally:)$/,
      commentTokens: {
        line: "#"
      },
      closeBrackets: {
        brackets: ["(", "[", "{", "'", '"', "'''", '"""']
      }
    }
  };
}
;
var words = function (str) {
  return str.split(" ");
};
const python = mkPython({});
const cython = mkPython({
  extra_keywords: words("by cdef cimport cpdef ctypedef enum except " + "extern gil include nogil property public " + "readonly struct union DEF IF ELIF ELSE")
});

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiMTgxMC5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGNvZGVtaXJyb3IvbGVnYWN5LW1vZGVzL21vZGUvcHl0aG9uLmpzIl0sInNvdXJjZXNDb250ZW50IjpbImZ1bmN0aW9uIHdvcmRSZWdleHAod29yZHMpIHtcbiAgcmV0dXJuIG5ldyBSZWdFeHAoXCJeKChcIiArIHdvcmRzLmpvaW4oXCIpfChcIikgKyBcIikpXFxcXGJcIik7XG59XG52YXIgd29yZE9wZXJhdG9ycyA9IHdvcmRSZWdleHAoW1wiYW5kXCIsIFwib3JcIiwgXCJub3RcIiwgXCJpc1wiXSk7XG52YXIgY29tbW9uS2V5d29yZHMgPSBbXCJhc1wiLCBcImFzc2VydFwiLCBcImJyZWFrXCIsIFwiY2xhc3NcIiwgXCJjb250aW51ZVwiLCBcImRlZlwiLCBcImRlbFwiLCBcImVsaWZcIiwgXCJlbHNlXCIsIFwiZXhjZXB0XCIsIFwiZmluYWxseVwiLCBcImZvclwiLCBcImZyb21cIiwgXCJnbG9iYWxcIiwgXCJpZlwiLCBcImltcG9ydFwiLCBcImxhbWJkYVwiLCBcInBhc3NcIiwgXCJyYWlzZVwiLCBcInJldHVyblwiLCBcInRyeVwiLCBcIndoaWxlXCIsIFwid2l0aFwiLCBcInlpZWxkXCIsIFwiaW5cIiwgXCJGYWxzZVwiLCBcIlRydWVcIl07XG52YXIgY29tbW9uQnVpbHRpbnMgPSBbXCJhYnNcIiwgXCJhbGxcIiwgXCJhbnlcIiwgXCJiaW5cIiwgXCJib29sXCIsIFwiYnl0ZWFycmF5XCIsIFwiY2FsbGFibGVcIiwgXCJjaHJcIiwgXCJjbGFzc21ldGhvZFwiLCBcImNvbXBpbGVcIiwgXCJjb21wbGV4XCIsIFwiZGVsYXR0clwiLCBcImRpY3RcIiwgXCJkaXJcIiwgXCJkaXZtb2RcIiwgXCJlbnVtZXJhdGVcIiwgXCJldmFsXCIsIFwiZmlsdGVyXCIsIFwiZmxvYXRcIiwgXCJmb3JtYXRcIiwgXCJmcm96ZW5zZXRcIiwgXCJnZXRhdHRyXCIsIFwiZ2xvYmFsc1wiLCBcImhhc2F0dHJcIiwgXCJoYXNoXCIsIFwiaGVscFwiLCBcImhleFwiLCBcImlkXCIsIFwiaW5wdXRcIiwgXCJpbnRcIiwgXCJpc2luc3RhbmNlXCIsIFwiaXNzdWJjbGFzc1wiLCBcIml0ZXJcIiwgXCJsZW5cIiwgXCJsaXN0XCIsIFwibG9jYWxzXCIsIFwibWFwXCIsIFwibWF4XCIsIFwibWVtb3J5dmlld1wiLCBcIm1pblwiLCBcIm5leHRcIiwgXCJvYmplY3RcIiwgXCJvY3RcIiwgXCJvcGVuXCIsIFwib3JkXCIsIFwicG93XCIsIFwicHJvcGVydHlcIiwgXCJyYW5nZVwiLCBcInJlcHJcIiwgXCJyZXZlcnNlZFwiLCBcInJvdW5kXCIsIFwic2V0XCIsIFwic2V0YXR0clwiLCBcInNsaWNlXCIsIFwic29ydGVkXCIsIFwic3RhdGljbWV0aG9kXCIsIFwic3RyXCIsIFwic3VtXCIsIFwic3VwZXJcIiwgXCJ0dXBsZVwiLCBcInR5cGVcIiwgXCJ2YXJzXCIsIFwiemlwXCIsIFwiX19pbXBvcnRfX1wiLCBcIk5vdEltcGxlbWVudGVkXCIsIFwiRWxsaXBzaXNcIiwgXCJfX2RlYnVnX19cIl07XG5mdW5jdGlvbiB0b3Aoc3RhdGUpIHtcbiAgcmV0dXJuIHN0YXRlLnNjb3Blc1tzdGF0ZS5zY29wZXMubGVuZ3RoIC0gMV07XG59XG5leHBvcnQgZnVuY3Rpb24gbWtQeXRob24ocGFyc2VyQ29uZikge1xuICB2YXIgRVJST1JDTEFTUyA9IFwiZXJyb3JcIjtcbiAgdmFyIGRlbGltaXRlcnMgPSBwYXJzZXJDb25mLmRlbGltaXRlcnMgfHwgcGFyc2VyQ29uZi5zaW5nbGVEZWxpbWl0ZXJzIHx8IC9eW1xcKFxcKVxcW1xcXVxce1xcfUAsOmA9O1xcLlxcXFxdLztcbiAgLy8gICAgICAgICAgICAgICAoQmFja3dhcmRzLWNvbXBhdGliaWxpdHkgd2l0aCBvbGQsIGN1bWJlcnNvbWUgY29uZmlnIHN5c3RlbSlcbiAgdmFyIG9wZXJhdG9ycyA9IFtwYXJzZXJDb25mLnNpbmdsZU9wZXJhdG9ycywgcGFyc2VyQ29uZi5kb3VibGVPcGVyYXRvcnMsIHBhcnNlckNvbmYuZG91YmxlRGVsaW1pdGVycywgcGFyc2VyQ29uZi50cmlwbGVEZWxpbWl0ZXJzLCBwYXJzZXJDb25mLm9wZXJhdG9ycyB8fCAvXihbLSsqLyVcXC8mfF5dPT98Wzw+PV0rfFxcL1xcLz0/fFxcKlxcKj0/fCE9fFt+IUBdfFxcLlxcLlxcLikvXTtcbiAgZm9yICh2YXIgaSA9IDA7IGkgPCBvcGVyYXRvcnMubGVuZ3RoOyBpKyspIGlmICghb3BlcmF0b3JzW2ldKSBvcGVyYXRvcnMuc3BsaWNlKGktLSwgMSk7XG4gIHZhciBoYW5naW5nSW5kZW50ID0gcGFyc2VyQ29uZi5oYW5naW5nSW5kZW50O1xuICB2YXIgbXlLZXl3b3JkcyA9IGNvbW1vbktleXdvcmRzLFxuICAgIG15QnVpbHRpbnMgPSBjb21tb25CdWlsdGlucztcbiAgaWYgKHBhcnNlckNvbmYuZXh0cmFfa2V5d29yZHMgIT0gdW5kZWZpbmVkKSBteUtleXdvcmRzID0gbXlLZXl3b3Jkcy5jb25jYXQocGFyc2VyQ29uZi5leHRyYV9rZXl3b3Jkcyk7XG4gIGlmIChwYXJzZXJDb25mLmV4dHJhX2J1aWx0aW5zICE9IHVuZGVmaW5lZCkgbXlCdWlsdGlucyA9IG15QnVpbHRpbnMuY29uY2F0KHBhcnNlckNvbmYuZXh0cmFfYnVpbHRpbnMpO1xuICB2YXIgcHkzID0gIShwYXJzZXJDb25mLnZlcnNpb24gJiYgTnVtYmVyKHBhcnNlckNvbmYudmVyc2lvbikgPCAzKTtcbiAgaWYgKHB5Mykge1xuICAgIC8vIHNpbmNlIGh0dHA6Ly9sZWdhY3kucHl0aG9uLm9yZy9kZXYvcGVwcy9wZXAtMDQ2NS8gQCBpcyBhbHNvIGFuIG9wZXJhdG9yXG4gICAgdmFyIGlkZW50aWZpZXJzID0gcGFyc2VyQ29uZi5pZGVudGlmaWVycyB8fCAvXltfQS1aYS16XFx1MDBBMS1cXHVGRkZGXVtfQS1aYS16MC05XFx1MDBBMS1cXHVGRkZGXSovO1xuICAgIG15S2V5d29yZHMgPSBteUtleXdvcmRzLmNvbmNhdChbXCJub25sb2NhbFwiLCBcIk5vbmVcIiwgXCJhaXRlclwiLCBcImFuZXh0XCIsIFwiYXN5bmNcIiwgXCJhd2FpdFwiLCBcImJyZWFrcG9pbnRcIiwgXCJtYXRjaFwiLCBcImNhc2VcIl0pO1xuICAgIG15QnVpbHRpbnMgPSBteUJ1aWx0aW5zLmNvbmNhdChbXCJhc2NpaVwiLCBcImJ5dGVzXCIsIFwiZXhlY1wiLCBcInByaW50XCJdKTtcbiAgICB2YXIgc3RyaW5nUHJlZml4ZXMgPSBuZXcgUmVnRXhwKFwiXigoW3JidWZdfChicil8KHJiKXwoZnIpfChyZikpPygnezN9fFxcXCJ7M318WydcXFwiXSkpXCIsIFwiaVwiKTtcbiAgfSBlbHNlIHtcbiAgICB2YXIgaWRlbnRpZmllcnMgPSBwYXJzZXJDb25mLmlkZW50aWZpZXJzIHx8IC9eW19BLVphLXpdW19BLVphLXowLTldKi87XG4gICAgbXlLZXl3b3JkcyA9IG15S2V5d29yZHMuY29uY2F0KFtcImV4ZWNcIiwgXCJwcmludFwiXSk7XG4gICAgbXlCdWlsdGlucyA9IG15QnVpbHRpbnMuY29uY2F0KFtcImFwcGx5XCIsIFwiYmFzZXN0cmluZ1wiLCBcImJ1ZmZlclwiLCBcImNtcFwiLCBcImNvZXJjZVwiLCBcImV4ZWNmaWxlXCIsIFwiZmlsZVwiLCBcImludGVyblwiLCBcImxvbmdcIiwgXCJyYXdfaW5wdXRcIiwgXCJyZWR1Y2VcIiwgXCJyZWxvYWRcIiwgXCJ1bmljaHJcIiwgXCJ1bmljb2RlXCIsIFwieHJhbmdlXCIsIFwiTm9uZVwiXSk7XG4gICAgdmFyIHN0cmluZ1ByZWZpeGVzID0gbmV3IFJlZ0V4cChcIl4oKFtydWJmXXwodXIpfChicikpPygnezN9fFxcXCJ7M318WydcXFwiXSkpXCIsIFwiaVwiKTtcbiAgfVxuICB2YXIga2V5d29yZHMgPSB3b3JkUmVnZXhwKG15S2V5d29yZHMpO1xuICB2YXIgYnVpbHRpbnMgPSB3b3JkUmVnZXhwKG15QnVpbHRpbnMpO1xuXG4gIC8vIHRva2VuaXplcnNcbiAgZnVuY3Rpb24gdG9rZW5CYXNlKHN0cmVhbSwgc3RhdGUpIHtcbiAgICB2YXIgc29sID0gc3RyZWFtLnNvbCgpICYmIHN0YXRlLmxhc3RUb2tlbiAhPSBcIlxcXFxcIjtcbiAgICBpZiAoc29sKSBzdGF0ZS5pbmRlbnQgPSBzdHJlYW0uaW5kZW50YXRpb24oKTtcbiAgICAvLyBIYW5kbGUgc2NvcGUgY2hhbmdlc1xuICAgIGlmIChzb2wgJiYgdG9wKHN0YXRlKS50eXBlID09IFwicHlcIikge1xuICAgICAgdmFyIHNjb3BlT2Zmc2V0ID0gdG9wKHN0YXRlKS5vZmZzZXQ7XG4gICAgICBpZiAoc3RyZWFtLmVhdFNwYWNlKCkpIHtcbiAgICAgICAgdmFyIGxpbmVPZmZzZXQgPSBzdHJlYW0uaW5kZW50YXRpb24oKTtcbiAgICAgICAgaWYgKGxpbmVPZmZzZXQgPiBzY29wZU9mZnNldCkgcHVzaFB5U2NvcGUoc3RyZWFtLCBzdGF0ZSk7ZWxzZSBpZiAobGluZU9mZnNldCA8IHNjb3BlT2Zmc2V0ICYmIGRlZGVudChzdHJlYW0sIHN0YXRlKSAmJiBzdHJlYW0ucGVlaygpICE9IFwiI1wiKSBzdGF0ZS5lcnJvclRva2VuID0gdHJ1ZTtcbiAgICAgICAgcmV0dXJuIG51bGw7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICB2YXIgc3R5bGUgPSB0b2tlbkJhc2VJbm5lcihzdHJlYW0sIHN0YXRlKTtcbiAgICAgICAgaWYgKHNjb3BlT2Zmc2V0ID4gMCAmJiBkZWRlbnQoc3RyZWFtLCBzdGF0ZSkpIHN0eWxlICs9IFwiIFwiICsgRVJST1JDTEFTUztcbiAgICAgICAgcmV0dXJuIHN0eWxlO1xuICAgICAgfVxuICAgIH1cbiAgICByZXR1cm4gdG9rZW5CYXNlSW5uZXIoc3RyZWFtLCBzdGF0ZSk7XG4gIH1cbiAgZnVuY3Rpb24gdG9rZW5CYXNlSW5uZXIoc3RyZWFtLCBzdGF0ZSwgaW5Gb3JtYXQpIHtcbiAgICBpZiAoc3RyZWFtLmVhdFNwYWNlKCkpIHJldHVybiBudWxsO1xuXG4gICAgLy8gSGFuZGxlIENvbW1lbnRzXG4gICAgaWYgKCFpbkZvcm1hdCAmJiBzdHJlYW0ubWF0Y2goL14jLiovKSkgcmV0dXJuIFwiY29tbWVudFwiO1xuXG4gICAgLy8gSGFuZGxlIE51bWJlciBMaXRlcmFsc1xuICAgIGlmIChzdHJlYW0ubWF0Y2goL15bMC05XFwuXS8sIGZhbHNlKSkge1xuICAgICAgdmFyIGZsb2F0TGl0ZXJhbCA9IGZhbHNlO1xuICAgICAgLy8gRmxvYXRzXG4gICAgICBpZiAoc3RyZWFtLm1hdGNoKC9eW1xcZF9dKlxcLlxcZCsoZVtcXCtcXC1dP1xcZCspPy9pKSkge1xuICAgICAgICBmbG9hdExpdGVyYWwgPSB0cnVlO1xuICAgICAgfVxuICAgICAgaWYgKHN0cmVhbS5tYXRjaCgvXltcXGRfXStcXC5cXGQqLykpIHtcbiAgICAgICAgZmxvYXRMaXRlcmFsID0gdHJ1ZTtcbiAgICAgIH1cbiAgICAgIGlmIChzdHJlYW0ubWF0Y2goL15cXC5cXGQrLykpIHtcbiAgICAgICAgZmxvYXRMaXRlcmFsID0gdHJ1ZTtcbiAgICAgIH1cbiAgICAgIGlmIChmbG9hdExpdGVyYWwpIHtcbiAgICAgICAgLy8gRmxvYXQgbGl0ZXJhbHMgbWF5IGJlIFwiaW1hZ2luYXJ5XCJcbiAgICAgICAgc3RyZWFtLmVhdCgvSi9pKTtcbiAgICAgICAgcmV0dXJuIFwibnVtYmVyXCI7XG4gICAgICB9XG4gICAgICAvLyBJbnRlZ2Vyc1xuICAgICAgdmFyIGludExpdGVyYWwgPSBmYWxzZTtcbiAgICAgIC8vIEhleFxuICAgICAgaWYgKHN0cmVhbS5tYXRjaCgvXjB4WzAtOWEtZl9dKy9pKSkgaW50TGl0ZXJhbCA9IHRydWU7XG4gICAgICAvLyBCaW5hcnlcbiAgICAgIGlmIChzdHJlYW0ubWF0Y2goL14wYlswMV9dKy9pKSkgaW50TGl0ZXJhbCA9IHRydWU7XG4gICAgICAvLyBPY3RhbFxuICAgICAgaWYgKHN0cmVhbS5tYXRjaCgvXjBvWzAtN19dKy9pKSkgaW50TGl0ZXJhbCA9IHRydWU7XG4gICAgICAvLyBEZWNpbWFsXG4gICAgICBpZiAoc3RyZWFtLm1hdGNoKC9eWzEtOV1bXFxkX10qKGVbXFwrXFwtXT9bXFxkX10rKT8vKSkge1xuICAgICAgICAvLyBEZWNpbWFsIGxpdGVyYWxzIG1heSBiZSBcImltYWdpbmFyeVwiXG4gICAgICAgIHN0cmVhbS5lYXQoL0ovaSk7XG4gICAgICAgIC8vIFRPRE8gLSBDYW4geW91IGhhdmUgaW1hZ2luYXJ5IGxvbmdzP1xuICAgICAgICBpbnRMaXRlcmFsID0gdHJ1ZTtcbiAgICAgIH1cbiAgICAgIC8vIFplcm8gYnkgaXRzZWxmIHdpdGggbm8gb3RoZXIgcGllY2Ugb2YgbnVtYmVyLlxuICAgICAgaWYgKHN0cmVhbS5tYXRjaCgvXjAoPyFbXFxkeF0pL2kpKSBpbnRMaXRlcmFsID0gdHJ1ZTtcbiAgICAgIGlmIChpbnRMaXRlcmFsKSB7XG4gICAgICAgIC8vIEludGVnZXIgbGl0ZXJhbHMgbWF5IGJlIFwibG9uZ1wiXG4gICAgICAgIHN0cmVhbS5lYXQoL0wvaSk7XG4gICAgICAgIHJldHVybiBcIm51bWJlclwiO1xuICAgICAgfVxuICAgIH1cblxuICAgIC8vIEhhbmRsZSBTdHJpbmdzXG4gICAgaWYgKHN0cmVhbS5tYXRjaChzdHJpbmdQcmVmaXhlcykpIHtcbiAgICAgIHZhciBpc0ZtdFN0cmluZyA9IHN0cmVhbS5jdXJyZW50KCkudG9Mb3dlckNhc2UoKS5pbmRleE9mKCdmJykgIT09IC0xO1xuICAgICAgaWYgKCFpc0ZtdFN0cmluZykge1xuICAgICAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuU3RyaW5nRmFjdG9yeShzdHJlYW0uY3VycmVudCgpLCBzdGF0ZS50b2tlbml6ZSk7XG4gICAgICAgIHJldHVybiBzdGF0ZS50b2tlbml6ZShzdHJlYW0sIHN0YXRlKTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHN0YXRlLnRva2VuaXplID0gZm9ybWF0U3RyaW5nRmFjdG9yeShzdHJlYW0uY3VycmVudCgpLCBzdGF0ZS50b2tlbml6ZSk7XG4gICAgICAgIHJldHVybiBzdGF0ZS50b2tlbml6ZShzdHJlYW0sIHN0YXRlKTtcbiAgICAgIH1cbiAgICB9XG4gICAgZm9yICh2YXIgaSA9IDA7IGkgPCBvcGVyYXRvcnMubGVuZ3RoOyBpKyspIGlmIChzdHJlYW0ubWF0Y2gob3BlcmF0b3JzW2ldKSkgcmV0dXJuIFwib3BlcmF0b3JcIjtcbiAgICBpZiAoc3RyZWFtLm1hdGNoKGRlbGltaXRlcnMpKSByZXR1cm4gXCJwdW5jdHVhdGlvblwiO1xuICAgIGlmIChzdGF0ZS5sYXN0VG9rZW4gPT0gXCIuXCIgJiYgc3RyZWFtLm1hdGNoKGlkZW50aWZpZXJzKSkgcmV0dXJuIFwicHJvcGVydHlcIjtcbiAgICBpZiAoc3RyZWFtLm1hdGNoKGtleXdvcmRzKSB8fCBzdHJlYW0ubWF0Y2god29yZE9wZXJhdG9ycykpIHJldHVybiBcImtleXdvcmRcIjtcbiAgICBpZiAoc3RyZWFtLm1hdGNoKGJ1aWx0aW5zKSkgcmV0dXJuIFwiYnVpbHRpblwiO1xuICAgIGlmIChzdHJlYW0ubWF0Y2goL14oc2VsZnxjbHMpXFxiLykpIHJldHVybiBcInNlbGZcIjtcbiAgICBpZiAoc3RyZWFtLm1hdGNoKGlkZW50aWZpZXJzKSkge1xuICAgICAgaWYgKHN0YXRlLmxhc3RUb2tlbiA9PSBcImRlZlwiIHx8IHN0YXRlLmxhc3RUb2tlbiA9PSBcImNsYXNzXCIpIHJldHVybiBcImRlZlwiO1xuICAgICAgcmV0dXJuIFwidmFyaWFibGVcIjtcbiAgICB9XG5cbiAgICAvLyBIYW5kbGUgbm9uLWRldGVjdGVkIGl0ZW1zXG4gICAgc3RyZWFtLm5leHQoKTtcbiAgICByZXR1cm4gaW5Gb3JtYXQgPyBudWxsIDogRVJST1JDTEFTUztcbiAgfVxuICBmdW5jdGlvbiBmb3JtYXRTdHJpbmdGYWN0b3J5KGRlbGltaXRlciwgdG9rZW5PdXRlcikge1xuICAgIHdoaWxlIChcInJ1YmZcIi5pbmRleE9mKGRlbGltaXRlci5jaGFyQXQoMCkudG9Mb3dlckNhc2UoKSkgPj0gMCkgZGVsaW1pdGVyID0gZGVsaW1pdGVyLnN1YnN0cigxKTtcbiAgICB2YXIgc2luZ2xlbGluZSA9IGRlbGltaXRlci5sZW5ndGggPT0gMTtcbiAgICB2YXIgT1VUQ0xBU1MgPSBcInN0cmluZ1wiO1xuICAgIGZ1bmN0aW9uIHRva2VuTmVzdGVkRXhwcihkZXB0aCkge1xuICAgICAgcmV0dXJuIGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgICAgIHZhciBpbm5lciA9IHRva2VuQmFzZUlubmVyKHN0cmVhbSwgc3RhdGUsIHRydWUpO1xuICAgICAgICBpZiAoaW5uZXIgPT0gXCJwdW5jdHVhdGlvblwiKSB7XG4gICAgICAgICAgaWYgKHN0cmVhbS5jdXJyZW50KCkgPT0gXCJ7XCIpIHtcbiAgICAgICAgICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5OZXN0ZWRFeHByKGRlcHRoICsgMSk7XG4gICAgICAgICAgfSBlbHNlIGlmIChzdHJlYW0uY3VycmVudCgpID09IFwifVwiKSB7XG4gICAgICAgICAgICBpZiAoZGVwdGggPiAxKSBzdGF0ZS50b2tlbml6ZSA9IHRva2VuTmVzdGVkRXhwcihkZXB0aCAtIDEpO2Vsc2Ugc3RhdGUudG9rZW5pemUgPSB0b2tlblN0cmluZztcbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIGlubmVyO1xuICAgICAgfTtcbiAgICB9XG4gICAgZnVuY3Rpb24gdG9rZW5TdHJpbmcoc3RyZWFtLCBzdGF0ZSkge1xuICAgICAgd2hpbGUgKCFzdHJlYW0uZW9sKCkpIHtcbiAgICAgICAgc3RyZWFtLmVhdFdoaWxlKC9bXidcIlxce1xcfVxcXFxdLyk7XG4gICAgICAgIGlmIChzdHJlYW0uZWF0KFwiXFxcXFwiKSkge1xuICAgICAgICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgICAgICAgaWYgKHNpbmdsZWxpbmUgJiYgc3RyZWFtLmVvbCgpKSByZXR1cm4gT1VUQ0xBU1M7XG4gICAgICAgIH0gZWxzZSBpZiAoc3RyZWFtLm1hdGNoKGRlbGltaXRlcikpIHtcbiAgICAgICAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuT3V0ZXI7XG4gICAgICAgICAgcmV0dXJuIE9VVENMQVNTO1xuICAgICAgICB9IGVsc2UgaWYgKHN0cmVhbS5tYXRjaCgne3snKSkge1xuICAgICAgICAgIC8vIGlnbm9yZSB7eyBpbiBmLXN0clxuICAgICAgICAgIHJldHVybiBPVVRDTEFTUztcbiAgICAgICAgfSBlbHNlIGlmIChzdHJlYW0ubWF0Y2goJ3snLCBmYWxzZSkpIHtcbiAgICAgICAgICAvLyBzd2l0Y2ggdG8gbmVzdGVkIG1vZGVcbiAgICAgICAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuTmVzdGVkRXhwcigwKTtcbiAgICAgICAgICBpZiAoc3RyZWFtLmN1cnJlbnQoKSkgcmV0dXJuIE9VVENMQVNTO2Vsc2UgcmV0dXJuIHN0YXRlLnRva2VuaXplKHN0cmVhbSwgc3RhdGUpO1xuICAgICAgICB9IGVsc2UgaWYgKHN0cmVhbS5tYXRjaCgnfX0nKSkge1xuICAgICAgICAgIHJldHVybiBPVVRDTEFTUztcbiAgICAgICAgfSBlbHNlIGlmIChzdHJlYW0ubWF0Y2goJ30nKSkge1xuICAgICAgICAgIC8vIHNpbmdsZSB9IGluIGYtc3RyaW5nIGlzIGFuIGVycm9yXG4gICAgICAgICAgcmV0dXJuIEVSUk9SQ0xBU1M7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgc3RyZWFtLmVhdCgvWydcIl0vKTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgICAgaWYgKHNpbmdsZWxpbmUpIHtcbiAgICAgICAgaWYgKHBhcnNlckNvbmYuc2luZ2xlTGluZVN0cmluZ0Vycm9ycykgcmV0dXJuIEVSUk9SQ0xBU1M7ZWxzZSBzdGF0ZS50b2tlbml6ZSA9IHRva2VuT3V0ZXI7XG4gICAgICB9XG4gICAgICByZXR1cm4gT1VUQ0xBU1M7XG4gICAgfVxuICAgIHRva2VuU3RyaW5nLmlzU3RyaW5nID0gdHJ1ZTtcbiAgICByZXR1cm4gdG9rZW5TdHJpbmc7XG4gIH1cbiAgZnVuY3Rpb24gdG9rZW5TdHJpbmdGYWN0b3J5KGRlbGltaXRlciwgdG9rZW5PdXRlcikge1xuICAgIHdoaWxlIChcInJ1YmZcIi5pbmRleE9mKGRlbGltaXRlci5jaGFyQXQoMCkudG9Mb3dlckNhc2UoKSkgPj0gMCkgZGVsaW1pdGVyID0gZGVsaW1pdGVyLnN1YnN0cigxKTtcbiAgICB2YXIgc2luZ2xlbGluZSA9IGRlbGltaXRlci5sZW5ndGggPT0gMTtcbiAgICB2YXIgT1VUQ0xBU1MgPSBcInN0cmluZ1wiO1xuICAgIGZ1bmN0aW9uIHRva2VuU3RyaW5nKHN0cmVhbSwgc3RhdGUpIHtcbiAgICAgIHdoaWxlICghc3RyZWFtLmVvbCgpKSB7XG4gICAgICAgIHN0cmVhbS5lYXRXaGlsZSgvW14nXCJcXFxcXS8pO1xuICAgICAgICBpZiAoc3RyZWFtLmVhdChcIlxcXFxcIikpIHtcbiAgICAgICAgICBzdHJlYW0ubmV4dCgpO1xuICAgICAgICAgIGlmIChzaW5nbGVsaW5lICYmIHN0cmVhbS5lb2woKSkgcmV0dXJuIE9VVENMQVNTO1xuICAgICAgICB9IGVsc2UgaWYgKHN0cmVhbS5tYXRjaChkZWxpbWl0ZXIpKSB7XG4gICAgICAgICAgc3RhdGUudG9rZW5pemUgPSB0b2tlbk91dGVyO1xuICAgICAgICAgIHJldHVybiBPVVRDTEFTUztcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICBzdHJlYW0uZWF0KC9bJ1wiXS8pO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgICBpZiAoc2luZ2xlbGluZSkge1xuICAgICAgICBpZiAocGFyc2VyQ29uZi5zaW5nbGVMaW5lU3RyaW5nRXJyb3JzKSByZXR1cm4gRVJST1JDTEFTUztlbHNlIHN0YXRlLnRva2VuaXplID0gdG9rZW5PdXRlcjtcbiAgICAgIH1cbiAgICAgIHJldHVybiBPVVRDTEFTUztcbiAgICB9XG4gICAgdG9rZW5TdHJpbmcuaXNTdHJpbmcgPSB0cnVlO1xuICAgIHJldHVybiB0b2tlblN0cmluZztcbiAgfVxuICBmdW5jdGlvbiBwdXNoUHlTY29wZShzdHJlYW0sIHN0YXRlKSB7XG4gICAgd2hpbGUgKHRvcChzdGF0ZSkudHlwZSAhPSBcInB5XCIpIHN0YXRlLnNjb3Blcy5wb3AoKTtcbiAgICBzdGF0ZS5zY29wZXMucHVzaCh7XG4gICAgICBvZmZzZXQ6IHRvcChzdGF0ZSkub2Zmc2V0ICsgc3RyZWFtLmluZGVudFVuaXQsXG4gICAgICB0eXBlOiBcInB5XCIsXG4gICAgICBhbGlnbjogbnVsbFxuICAgIH0pO1xuICB9XG4gIGZ1bmN0aW9uIHB1c2hCcmFja2V0U2NvcGUoc3RyZWFtLCBzdGF0ZSwgdHlwZSkge1xuICAgIHZhciBhbGlnbiA9IHN0cmVhbS5tYXRjaCgvXltcXHNcXFtcXHtcXChdKig/OiN8JCkvLCBmYWxzZSkgPyBudWxsIDogc3RyZWFtLmNvbHVtbigpICsgMTtcbiAgICBzdGF0ZS5zY29wZXMucHVzaCh7XG4gICAgICBvZmZzZXQ6IHN0YXRlLmluZGVudCArIChoYW5naW5nSW5kZW50IHx8IHN0cmVhbS5pbmRlbnRVbml0KSxcbiAgICAgIHR5cGU6IHR5cGUsXG4gICAgICBhbGlnbjogYWxpZ25cbiAgICB9KTtcbiAgfVxuICBmdW5jdGlvbiBkZWRlbnQoc3RyZWFtLCBzdGF0ZSkge1xuICAgIHZhciBpbmRlbnRlZCA9IHN0cmVhbS5pbmRlbnRhdGlvbigpO1xuICAgIHdoaWxlIChzdGF0ZS5zY29wZXMubGVuZ3RoID4gMSAmJiB0b3Aoc3RhdGUpLm9mZnNldCA+IGluZGVudGVkKSB7XG4gICAgICBpZiAodG9wKHN0YXRlKS50eXBlICE9IFwicHlcIikgcmV0dXJuIHRydWU7XG4gICAgICBzdGF0ZS5zY29wZXMucG9wKCk7XG4gICAgfVxuICAgIHJldHVybiB0b3Aoc3RhdGUpLm9mZnNldCAhPSBpbmRlbnRlZDtcbiAgfVxuICBmdW5jdGlvbiB0b2tlbkxleGVyKHN0cmVhbSwgc3RhdGUpIHtcbiAgICBpZiAoc3RyZWFtLnNvbCgpKSB7XG4gICAgICBzdGF0ZS5iZWdpbm5pbmdPZkxpbmUgPSB0cnVlO1xuICAgICAgc3RhdGUuZGVkZW50ID0gZmFsc2U7XG4gICAgfVxuICAgIHZhciBzdHlsZSA9IHN0YXRlLnRva2VuaXplKHN0cmVhbSwgc3RhdGUpO1xuICAgIHZhciBjdXJyZW50ID0gc3RyZWFtLmN1cnJlbnQoKTtcblxuICAgIC8vIEhhbmRsZSBkZWNvcmF0b3JzXG4gICAgaWYgKHN0YXRlLmJlZ2lubmluZ09mTGluZSAmJiBjdXJyZW50ID09IFwiQFwiKSByZXR1cm4gc3RyZWFtLm1hdGNoKGlkZW50aWZpZXJzLCBmYWxzZSkgPyBcIm1ldGFcIiA6IHB5MyA/IFwib3BlcmF0b3JcIiA6IEVSUk9SQ0xBU1M7XG4gICAgaWYgKC9cXFMvLnRlc3QoY3VycmVudCkpIHN0YXRlLmJlZ2lubmluZ09mTGluZSA9IGZhbHNlO1xuICAgIGlmICgoc3R5bGUgPT0gXCJ2YXJpYWJsZVwiIHx8IHN0eWxlID09IFwiYnVpbHRpblwiKSAmJiBzdGF0ZS5sYXN0VG9rZW4gPT0gXCJtZXRhXCIpIHN0eWxlID0gXCJtZXRhXCI7XG5cbiAgICAvLyBIYW5kbGUgc2NvcGUgY2hhbmdlcy5cbiAgICBpZiAoY3VycmVudCA9PSBcInBhc3NcIiB8fCBjdXJyZW50ID09IFwicmV0dXJuXCIpIHN0YXRlLmRlZGVudCA9IHRydWU7XG4gICAgaWYgKGN1cnJlbnQgPT0gXCJsYW1iZGFcIikgc3RhdGUubGFtYmRhID0gdHJ1ZTtcbiAgICBpZiAoY3VycmVudCA9PSBcIjpcIiAmJiAhc3RhdGUubGFtYmRhICYmIHRvcChzdGF0ZSkudHlwZSA9PSBcInB5XCIgJiYgc3RyZWFtLm1hdGNoKC9eXFxzKig/OiN8JCkvLCBmYWxzZSkpIHB1c2hQeVNjb3BlKHN0cmVhbSwgc3RhdGUpO1xuICAgIGlmIChjdXJyZW50Lmxlbmd0aCA9PSAxICYmICEvc3RyaW5nfGNvbW1lbnQvLnRlc3Qoc3R5bGUpKSB7XG4gICAgICB2YXIgZGVsaW1pdGVyX2luZGV4ID0gXCJbKHtcIi5pbmRleE9mKGN1cnJlbnQpO1xuICAgICAgaWYgKGRlbGltaXRlcl9pbmRleCAhPSAtMSkgcHVzaEJyYWNrZXRTY29wZShzdHJlYW0sIHN0YXRlLCBcIl0pfVwiLnNsaWNlKGRlbGltaXRlcl9pbmRleCwgZGVsaW1pdGVyX2luZGV4ICsgMSkpO1xuICAgICAgZGVsaW1pdGVyX2luZGV4ID0gXCJdKX1cIi5pbmRleE9mKGN1cnJlbnQpO1xuICAgICAgaWYgKGRlbGltaXRlcl9pbmRleCAhPSAtMSkge1xuICAgICAgICBpZiAodG9wKHN0YXRlKS50eXBlID09IGN1cnJlbnQpIHN0YXRlLmluZGVudCA9IHN0YXRlLnNjb3Blcy5wb3AoKS5vZmZzZXQgLSAoaGFuZ2luZ0luZGVudCB8fCBzdHJlYW0uaW5kZW50VW5pdCk7ZWxzZSByZXR1cm4gRVJST1JDTEFTUztcbiAgICAgIH1cbiAgICB9XG4gICAgaWYgKHN0YXRlLmRlZGVudCAmJiBzdHJlYW0uZW9sKCkgJiYgdG9wKHN0YXRlKS50eXBlID09IFwicHlcIiAmJiBzdGF0ZS5zY29wZXMubGVuZ3RoID4gMSkgc3RhdGUuc2NvcGVzLnBvcCgpO1xuICAgIHJldHVybiBzdHlsZTtcbiAgfVxuICByZXR1cm4ge1xuICAgIG5hbWU6IFwicHl0aG9uXCIsXG4gICAgc3RhcnRTdGF0ZTogZnVuY3Rpb24gKCkge1xuICAgICAgcmV0dXJuIHtcbiAgICAgICAgdG9rZW5pemU6IHRva2VuQmFzZSxcbiAgICAgICAgc2NvcGVzOiBbe1xuICAgICAgICAgIG9mZnNldDogMCxcbiAgICAgICAgICB0eXBlOiBcInB5XCIsXG4gICAgICAgICAgYWxpZ246IG51bGxcbiAgICAgICAgfV0sXG4gICAgICAgIGluZGVudDogMCxcbiAgICAgICAgbGFzdFRva2VuOiBudWxsLFxuICAgICAgICBsYW1iZGE6IGZhbHNlLFxuICAgICAgICBkZWRlbnQ6IDBcbiAgICAgIH07XG4gICAgfSxcbiAgICB0b2tlbjogZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICAgIHZhciBhZGRFcnIgPSBzdGF0ZS5lcnJvclRva2VuO1xuICAgICAgaWYgKGFkZEVycikgc3RhdGUuZXJyb3JUb2tlbiA9IGZhbHNlO1xuICAgICAgdmFyIHN0eWxlID0gdG9rZW5MZXhlcihzdHJlYW0sIHN0YXRlKTtcbiAgICAgIGlmIChzdHlsZSAmJiBzdHlsZSAhPSBcImNvbW1lbnRcIikgc3RhdGUubGFzdFRva2VuID0gc3R5bGUgPT0gXCJrZXl3b3JkXCIgfHwgc3R5bGUgPT0gXCJwdW5jdHVhdGlvblwiID8gc3RyZWFtLmN1cnJlbnQoKSA6IHN0eWxlO1xuICAgICAgaWYgKHN0eWxlID09IFwicHVuY3R1YXRpb25cIikgc3R5bGUgPSBudWxsO1xuICAgICAgaWYgKHN0cmVhbS5lb2woKSAmJiBzdGF0ZS5sYW1iZGEpIHN0YXRlLmxhbWJkYSA9IGZhbHNlO1xuICAgICAgcmV0dXJuIGFkZEVyciA/IEVSUk9SQ0xBU1MgOiBzdHlsZTtcbiAgICB9LFxuICAgIGluZGVudDogZnVuY3Rpb24gKHN0YXRlLCB0ZXh0QWZ0ZXIsIGN4KSB7XG4gICAgICBpZiAoc3RhdGUudG9rZW5pemUgIT0gdG9rZW5CYXNlKSByZXR1cm4gc3RhdGUudG9rZW5pemUuaXNTdHJpbmcgPyBudWxsIDogMDtcbiAgICAgIHZhciBzY29wZSA9IHRvcChzdGF0ZSk7XG4gICAgICB2YXIgY2xvc2luZyA9IHNjb3BlLnR5cGUgPT0gdGV4dEFmdGVyLmNoYXJBdCgwKSB8fCBzY29wZS50eXBlID09IFwicHlcIiAmJiAhc3RhdGUuZGVkZW50ICYmIC9eKGVsc2U6fGVsaWYgfGV4Y2VwdCB8ZmluYWxseTopLy50ZXN0KHRleHRBZnRlcik7XG4gICAgICBpZiAoc2NvcGUuYWxpZ24gIT0gbnVsbCkgcmV0dXJuIHNjb3BlLmFsaWduIC0gKGNsb3NpbmcgPyAxIDogMCk7ZWxzZSByZXR1cm4gc2NvcGUub2Zmc2V0IC0gKGNsb3NpbmcgPyBoYW5naW5nSW5kZW50IHx8IGN4LnVuaXQgOiAwKTtcbiAgICB9LFxuICAgIGxhbmd1YWdlRGF0YToge1xuICAgICAgYXV0b2NvbXBsZXRlOiBjb21tb25LZXl3b3Jkcy5jb25jYXQoY29tbW9uQnVpbHRpbnMpLmNvbmNhdChbXCJleGVjXCIsIFwicHJpbnRcIl0pLFxuICAgICAgaW5kZW50T25JbnB1dDogL15cXHMqKFtcXH1cXF1cXCldfGVsc2U6fGVsaWYgfGV4Y2VwdCB8ZmluYWxseTopJC8sXG4gICAgICBjb21tZW50VG9rZW5zOiB7XG4gICAgICAgIGxpbmU6IFwiI1wiXG4gICAgICB9LFxuICAgICAgY2xvc2VCcmFja2V0czoge1xuICAgICAgICBicmFja2V0czogW1wiKFwiLCBcIltcIiwgXCJ7XCIsIFwiJ1wiLCAnXCInLCBcIicnJ1wiLCAnXCJcIlwiJ11cbiAgICAgIH1cbiAgICB9XG4gIH07XG59XG47XG52YXIgd29yZHMgPSBmdW5jdGlvbiAoc3RyKSB7XG4gIHJldHVybiBzdHIuc3BsaXQoXCIgXCIpO1xufTtcbmV4cG9ydCBjb25zdCBweXRob24gPSBta1B5dGhvbih7fSk7XG5leHBvcnQgY29uc3QgY3l0aG9uID0gbWtQeXRob24oe1xuICBleHRyYV9rZXl3b3Jkczogd29yZHMoXCJieSBjZGVmIGNpbXBvcnQgY3BkZWYgY3R5cGVkZWYgZW51bSBleGNlcHQgXCIgKyBcImV4dGVybiBnaWwgaW5jbHVkZSBub2dpbCBwcm9wZXJ0eSBwdWJsaWMgXCIgKyBcInJlYWRvbmx5IHN0cnVjdCB1bmlvbiBERUYgSUYgRUxJRiBFTFNFXCIpXG59KTsiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=