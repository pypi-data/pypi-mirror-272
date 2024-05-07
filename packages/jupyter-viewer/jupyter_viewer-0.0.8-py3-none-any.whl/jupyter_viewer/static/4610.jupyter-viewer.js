"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[4610],{

/***/ 74610:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "swift": () => (/* binding */ swift)
/* harmony export */ });
function wordSet(words) {
  var set = {};
  for (var i = 0; i < words.length; i++) set[words[i]] = true;
  return set;
}
var keywords = wordSet(["_", "var", "let", "actor", "class", "enum", "extension", "import", "protocol", "struct", "func", "typealias", "associatedtype", "open", "public", "internal", "fileprivate", "private", "deinit", "init", "new", "override", "self", "subscript", "super", "convenience", "dynamic", "final", "indirect", "lazy", "required", "static", "unowned", "unowned(safe)", "unowned(unsafe)", "weak", "as", "is", "break", "case", "continue", "default", "else", "fallthrough", "for", "guard", "if", "in", "repeat", "switch", "where", "while", "defer", "return", "inout", "mutating", "nonmutating", "isolated", "nonisolated", "catch", "do", "rethrows", "throw", "throws", "async", "await", "try", "didSet", "get", "set", "willSet", "assignment", "associativity", "infix", "left", "none", "operator", "postfix", "precedence", "precedencegroup", "prefix", "right", "Any", "AnyObject", "Type", "dynamicType", "Self", "Protocol", "__COLUMN__", "__FILE__", "__FUNCTION__", "__LINE__"]);
var definingKeywords = wordSet(["var", "let", "actor", "class", "enum", "extension", "import", "protocol", "struct", "func", "typealias", "associatedtype", "for"]);
var atoms = wordSet(["true", "false", "nil", "self", "super", "_"]);
var types = wordSet(["Array", "Bool", "Character", "Dictionary", "Double", "Float", "Int", "Int8", "Int16", "Int32", "Int64", "Never", "Optional", "Set", "String", "UInt8", "UInt16", "UInt32", "UInt64", "Void"]);
var operators = "+-/*%=|&<>~^?!";
var punc = ":;,.(){}[]";
var binary = /^\-?0b[01][01_]*/;
var octal = /^\-?0o[0-7][0-7_]*/;
var hexadecimal = /^\-?0x[\dA-Fa-f][\dA-Fa-f_]*(?:(?:\.[\dA-Fa-f][\dA-Fa-f_]*)?[Pp]\-?\d[\d_]*)?/;
var decimal = /^\-?\d[\d_]*(?:\.\d[\d_]*)?(?:[Ee]\-?\d[\d_]*)?/;
var identifier = /^\$\d+|(`?)[_A-Za-z][_A-Za-z$0-9]*\1/;
var property = /^\.(?:\$\d+|(`?)[_A-Za-z][_A-Za-z$0-9]*\1)/;
var instruction = /^\#[A-Za-z]+/;
var attribute = /^@(?:\$\d+|(`?)[_A-Za-z][_A-Za-z$0-9]*\1)/;
//var regexp = /^\/(?!\s)(?:\/\/)?(?:\\.|[^\/])+\//

function tokenBase(stream, state, prev) {
  if (stream.sol()) state.indented = stream.indentation();
  if (stream.eatSpace()) return null;
  var ch = stream.peek();
  if (ch == "/") {
    if (stream.match("//")) {
      stream.skipToEnd();
      return "comment";
    }
    if (stream.match("/*")) {
      state.tokenize.push(tokenComment);
      return tokenComment(stream, state);
    }
  }
  if (stream.match(instruction)) return "builtin";
  if (stream.match(attribute)) return "attribute";
  if (stream.match(binary)) return "number";
  if (stream.match(octal)) return "number";
  if (stream.match(hexadecimal)) return "number";
  if (stream.match(decimal)) return "number";
  if (stream.match(property)) return "property";
  if (operators.indexOf(ch) > -1) {
    stream.next();
    return "operator";
  }
  if (punc.indexOf(ch) > -1) {
    stream.next();
    stream.match("..");
    return "punctuation";
  }
  var stringMatch;
  if (stringMatch = stream.match(/("""|"|')/)) {
    var tokenize = tokenString.bind(null, stringMatch[0]);
    state.tokenize.push(tokenize);
    return tokenize(stream, state);
  }
  if (stream.match(identifier)) {
    var ident = stream.current();
    if (types.hasOwnProperty(ident)) return "type";
    if (atoms.hasOwnProperty(ident)) return "atom";
    if (keywords.hasOwnProperty(ident)) {
      if (definingKeywords.hasOwnProperty(ident)) state.prev = "define";
      return "keyword";
    }
    if (prev == "define") return "def";
    return "variable";
  }
  stream.next();
  return null;
}
function tokenUntilClosingParen() {
  var depth = 0;
  return function (stream, state, prev) {
    var inner = tokenBase(stream, state, prev);
    if (inner == "punctuation") {
      if (stream.current() == "(") ++depth;else if (stream.current() == ")") {
        if (depth == 0) {
          stream.backUp(1);
          state.tokenize.pop();
          return state.tokenize[state.tokenize.length - 1](stream, state);
        } else --depth;
      }
    }
    return inner;
  };
}
function tokenString(openQuote, stream, state) {
  var singleLine = openQuote.length == 1;
  var ch,
    escaped = false;
  while (ch = stream.peek()) {
    if (escaped) {
      stream.next();
      if (ch == "(") {
        state.tokenize.push(tokenUntilClosingParen());
        return "string";
      }
      escaped = false;
    } else if (stream.match(openQuote)) {
      state.tokenize.pop();
      return "string";
    } else {
      stream.next();
      escaped = ch == "\\";
    }
  }
  if (singleLine) {
    state.tokenize.pop();
  }
  return "string";
}
function tokenComment(stream, state) {
  var ch;
  while (ch = stream.next()) {
    if (ch === "/" && stream.eat("*")) {
      state.tokenize.push(tokenComment);
    } else if (ch === "*" && stream.eat("/")) {
      state.tokenize.pop();
      break;
    }
  }
  return "comment";
}
function Context(prev, align, indented) {
  this.prev = prev;
  this.align = align;
  this.indented = indented;
}
function pushContext(state, stream) {
  var align = stream.match(/^\s*($|\/[\/\*]|[)}\]])/, false) ? null : stream.column() + 1;
  state.context = new Context(state.context, align, state.indented);
}
function popContext(state) {
  if (state.context) {
    state.indented = state.context.indented;
    state.context = state.context.prev;
  }
}
const swift = {
  name: "swift",
  startState: function () {
    return {
      prev: null,
      context: null,
      indented: 0,
      tokenize: []
    };
  },
  token: function (stream, state) {
    var prev = state.prev;
    state.prev = null;
    var tokenize = state.tokenize[state.tokenize.length - 1] || tokenBase;
    var style = tokenize(stream, state, prev);
    if (!style || style == "comment") state.prev = prev;else if (!state.prev) state.prev = style;
    if (style == "punctuation") {
      var bracket = /[\(\[\{]|([\]\)\}])/.exec(stream.current());
      if (bracket) (bracket[1] ? popContext : pushContext)(state, stream);
    }
    return style;
  },
  indent: function (state, textAfter, iCx) {
    var cx = state.context;
    if (!cx) return 0;
    var closing = /^[\]\}\)]/.test(textAfter);
    if (cx.align != null) return cx.align - (closing ? 1 : 0);
    return cx.indented + (closing ? 0 : iCx.unit);
  },
  languageData: {
    indentOnInput: /^\s*[\)\}\]]$/,
    commentTokens: {
      line: "//",
      block: {
        open: "/*",
        close: "*/"
      }
    },
    closeBrackets: {
      brackets: ["(", "[", "{", "'", '"', "`"]
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNDYxMC5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGNvZGVtaXJyb3IvbGVnYWN5LW1vZGVzL21vZGUvc3dpZnQuanMiXSwic291cmNlc0NvbnRlbnQiOlsiZnVuY3Rpb24gd29yZFNldCh3b3Jkcykge1xuICB2YXIgc2V0ID0ge307XG4gIGZvciAodmFyIGkgPSAwOyBpIDwgd29yZHMubGVuZ3RoOyBpKyspIHNldFt3b3Jkc1tpXV0gPSB0cnVlO1xuICByZXR1cm4gc2V0O1xufVxudmFyIGtleXdvcmRzID0gd29yZFNldChbXCJfXCIsIFwidmFyXCIsIFwibGV0XCIsIFwiYWN0b3JcIiwgXCJjbGFzc1wiLCBcImVudW1cIiwgXCJleHRlbnNpb25cIiwgXCJpbXBvcnRcIiwgXCJwcm90b2NvbFwiLCBcInN0cnVjdFwiLCBcImZ1bmNcIiwgXCJ0eXBlYWxpYXNcIiwgXCJhc3NvY2lhdGVkdHlwZVwiLCBcIm9wZW5cIiwgXCJwdWJsaWNcIiwgXCJpbnRlcm5hbFwiLCBcImZpbGVwcml2YXRlXCIsIFwicHJpdmF0ZVwiLCBcImRlaW5pdFwiLCBcImluaXRcIiwgXCJuZXdcIiwgXCJvdmVycmlkZVwiLCBcInNlbGZcIiwgXCJzdWJzY3JpcHRcIiwgXCJzdXBlclwiLCBcImNvbnZlbmllbmNlXCIsIFwiZHluYW1pY1wiLCBcImZpbmFsXCIsIFwiaW5kaXJlY3RcIiwgXCJsYXp5XCIsIFwicmVxdWlyZWRcIiwgXCJzdGF0aWNcIiwgXCJ1bm93bmVkXCIsIFwidW5vd25lZChzYWZlKVwiLCBcInVub3duZWQodW5zYWZlKVwiLCBcIndlYWtcIiwgXCJhc1wiLCBcImlzXCIsIFwiYnJlYWtcIiwgXCJjYXNlXCIsIFwiY29udGludWVcIiwgXCJkZWZhdWx0XCIsIFwiZWxzZVwiLCBcImZhbGx0aHJvdWdoXCIsIFwiZm9yXCIsIFwiZ3VhcmRcIiwgXCJpZlwiLCBcImluXCIsIFwicmVwZWF0XCIsIFwic3dpdGNoXCIsIFwid2hlcmVcIiwgXCJ3aGlsZVwiLCBcImRlZmVyXCIsIFwicmV0dXJuXCIsIFwiaW5vdXRcIiwgXCJtdXRhdGluZ1wiLCBcIm5vbm11dGF0aW5nXCIsIFwiaXNvbGF0ZWRcIiwgXCJub25pc29sYXRlZFwiLCBcImNhdGNoXCIsIFwiZG9cIiwgXCJyZXRocm93c1wiLCBcInRocm93XCIsIFwidGhyb3dzXCIsIFwiYXN5bmNcIiwgXCJhd2FpdFwiLCBcInRyeVwiLCBcImRpZFNldFwiLCBcImdldFwiLCBcInNldFwiLCBcIndpbGxTZXRcIiwgXCJhc3NpZ25tZW50XCIsIFwiYXNzb2NpYXRpdml0eVwiLCBcImluZml4XCIsIFwibGVmdFwiLCBcIm5vbmVcIiwgXCJvcGVyYXRvclwiLCBcInBvc3RmaXhcIiwgXCJwcmVjZWRlbmNlXCIsIFwicHJlY2VkZW5jZWdyb3VwXCIsIFwicHJlZml4XCIsIFwicmlnaHRcIiwgXCJBbnlcIiwgXCJBbnlPYmplY3RcIiwgXCJUeXBlXCIsIFwiZHluYW1pY1R5cGVcIiwgXCJTZWxmXCIsIFwiUHJvdG9jb2xcIiwgXCJfX0NPTFVNTl9fXCIsIFwiX19GSUxFX19cIiwgXCJfX0ZVTkNUSU9OX19cIiwgXCJfX0xJTkVfX1wiXSk7XG52YXIgZGVmaW5pbmdLZXl3b3JkcyA9IHdvcmRTZXQoW1widmFyXCIsIFwibGV0XCIsIFwiYWN0b3JcIiwgXCJjbGFzc1wiLCBcImVudW1cIiwgXCJleHRlbnNpb25cIiwgXCJpbXBvcnRcIiwgXCJwcm90b2NvbFwiLCBcInN0cnVjdFwiLCBcImZ1bmNcIiwgXCJ0eXBlYWxpYXNcIiwgXCJhc3NvY2lhdGVkdHlwZVwiLCBcImZvclwiXSk7XG52YXIgYXRvbXMgPSB3b3JkU2V0KFtcInRydWVcIiwgXCJmYWxzZVwiLCBcIm5pbFwiLCBcInNlbGZcIiwgXCJzdXBlclwiLCBcIl9cIl0pO1xudmFyIHR5cGVzID0gd29yZFNldChbXCJBcnJheVwiLCBcIkJvb2xcIiwgXCJDaGFyYWN0ZXJcIiwgXCJEaWN0aW9uYXJ5XCIsIFwiRG91YmxlXCIsIFwiRmxvYXRcIiwgXCJJbnRcIiwgXCJJbnQ4XCIsIFwiSW50MTZcIiwgXCJJbnQzMlwiLCBcIkludDY0XCIsIFwiTmV2ZXJcIiwgXCJPcHRpb25hbFwiLCBcIlNldFwiLCBcIlN0cmluZ1wiLCBcIlVJbnQ4XCIsIFwiVUludDE2XCIsIFwiVUludDMyXCIsIFwiVUludDY0XCIsIFwiVm9pZFwiXSk7XG52YXIgb3BlcmF0b3JzID0gXCIrLS8qJT18Jjw+fl4/IVwiO1xudmFyIHB1bmMgPSBcIjo7LC4oKXt9W11cIjtcbnZhciBiaW5hcnkgPSAvXlxcLT8wYlswMV1bMDFfXSovO1xudmFyIG9jdGFsID0gL15cXC0/MG9bMC03XVswLTdfXSovO1xudmFyIGhleGFkZWNpbWFsID0gL15cXC0/MHhbXFxkQS1GYS1mXVtcXGRBLUZhLWZfXSooPzooPzpcXC5bXFxkQS1GYS1mXVtcXGRBLUZhLWZfXSopP1tQcF1cXC0/XFxkW1xcZF9dKik/LztcbnZhciBkZWNpbWFsID0gL15cXC0/XFxkW1xcZF9dKig/OlxcLlxcZFtcXGRfXSopPyg/OltFZV1cXC0/XFxkW1xcZF9dKik/LztcbnZhciBpZGVudGlmaWVyID0gL15cXCRcXGQrfChgPylbX0EtWmEtel1bX0EtWmEteiQwLTldKlxcMS87XG52YXIgcHJvcGVydHkgPSAvXlxcLig/OlxcJFxcZCt8KGA/KVtfQS1aYS16XVtfQS1aYS16JDAtOV0qXFwxKS87XG52YXIgaW5zdHJ1Y3Rpb24gPSAvXlxcI1tBLVphLXpdKy87XG52YXIgYXR0cmlidXRlID0gL15AKD86XFwkXFxkK3woYD8pW19BLVphLXpdW19BLVphLXokMC05XSpcXDEpLztcbi8vdmFyIHJlZ2V4cCA9IC9eXFwvKD8hXFxzKSg/OlxcL1xcLyk/KD86XFxcXC58W15cXC9dKStcXC8vXG5cbmZ1bmN0aW9uIHRva2VuQmFzZShzdHJlYW0sIHN0YXRlLCBwcmV2KSB7XG4gIGlmIChzdHJlYW0uc29sKCkpIHN0YXRlLmluZGVudGVkID0gc3RyZWFtLmluZGVudGF0aW9uKCk7XG4gIGlmIChzdHJlYW0uZWF0U3BhY2UoKSkgcmV0dXJuIG51bGw7XG4gIHZhciBjaCA9IHN0cmVhbS5wZWVrKCk7XG4gIGlmIChjaCA9PSBcIi9cIikge1xuICAgIGlmIChzdHJlYW0ubWF0Y2goXCIvL1wiKSkge1xuICAgICAgc3RyZWFtLnNraXBUb0VuZCgpO1xuICAgICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICAgIH1cbiAgICBpZiAoc3RyZWFtLm1hdGNoKFwiLypcIikpIHtcbiAgICAgIHN0YXRlLnRva2VuaXplLnB1c2godG9rZW5Db21tZW50KTtcbiAgICAgIHJldHVybiB0b2tlbkNvbW1lbnQoc3RyZWFtLCBzdGF0ZSk7XG4gICAgfVxuICB9XG4gIGlmIChzdHJlYW0ubWF0Y2goaW5zdHJ1Y3Rpb24pKSByZXR1cm4gXCJidWlsdGluXCI7XG4gIGlmIChzdHJlYW0ubWF0Y2goYXR0cmlidXRlKSkgcmV0dXJuIFwiYXR0cmlidXRlXCI7XG4gIGlmIChzdHJlYW0ubWF0Y2goYmluYXJ5KSkgcmV0dXJuIFwibnVtYmVyXCI7XG4gIGlmIChzdHJlYW0ubWF0Y2gob2N0YWwpKSByZXR1cm4gXCJudW1iZXJcIjtcbiAgaWYgKHN0cmVhbS5tYXRjaChoZXhhZGVjaW1hbCkpIHJldHVybiBcIm51bWJlclwiO1xuICBpZiAoc3RyZWFtLm1hdGNoKGRlY2ltYWwpKSByZXR1cm4gXCJudW1iZXJcIjtcbiAgaWYgKHN0cmVhbS5tYXRjaChwcm9wZXJ0eSkpIHJldHVybiBcInByb3BlcnR5XCI7XG4gIGlmIChvcGVyYXRvcnMuaW5kZXhPZihjaCkgPiAtMSkge1xuICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgcmV0dXJuIFwib3BlcmF0b3JcIjtcbiAgfVxuICBpZiAocHVuYy5pbmRleE9mKGNoKSA+IC0xKSB7XG4gICAgc3RyZWFtLm5leHQoKTtcbiAgICBzdHJlYW0ubWF0Y2goXCIuLlwiKTtcbiAgICByZXR1cm4gXCJwdW5jdHVhdGlvblwiO1xuICB9XG4gIHZhciBzdHJpbmdNYXRjaDtcbiAgaWYgKHN0cmluZ01hdGNoID0gc3RyZWFtLm1hdGNoKC8oXCJcIlwifFwifCcpLykpIHtcbiAgICB2YXIgdG9rZW5pemUgPSB0b2tlblN0cmluZy5iaW5kKG51bGwsIHN0cmluZ01hdGNoWzBdKTtcbiAgICBzdGF0ZS50b2tlbml6ZS5wdXNoKHRva2VuaXplKTtcbiAgICByZXR1cm4gdG9rZW5pemUoc3RyZWFtLCBzdGF0ZSk7XG4gIH1cbiAgaWYgKHN0cmVhbS5tYXRjaChpZGVudGlmaWVyKSkge1xuICAgIHZhciBpZGVudCA9IHN0cmVhbS5jdXJyZW50KCk7XG4gICAgaWYgKHR5cGVzLmhhc093blByb3BlcnR5KGlkZW50KSkgcmV0dXJuIFwidHlwZVwiO1xuICAgIGlmIChhdG9tcy5oYXNPd25Qcm9wZXJ0eShpZGVudCkpIHJldHVybiBcImF0b21cIjtcbiAgICBpZiAoa2V5d29yZHMuaGFzT3duUHJvcGVydHkoaWRlbnQpKSB7XG4gICAgICBpZiAoZGVmaW5pbmdLZXl3b3Jkcy5oYXNPd25Qcm9wZXJ0eShpZGVudCkpIHN0YXRlLnByZXYgPSBcImRlZmluZVwiO1xuICAgICAgcmV0dXJuIFwia2V5d29yZFwiO1xuICAgIH1cbiAgICBpZiAocHJldiA9PSBcImRlZmluZVwiKSByZXR1cm4gXCJkZWZcIjtcbiAgICByZXR1cm4gXCJ2YXJpYWJsZVwiO1xuICB9XG4gIHN0cmVhbS5uZXh0KCk7XG4gIHJldHVybiBudWxsO1xufVxuZnVuY3Rpb24gdG9rZW5VbnRpbENsb3NpbmdQYXJlbigpIHtcbiAgdmFyIGRlcHRoID0gMDtcbiAgcmV0dXJuIGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlLCBwcmV2KSB7XG4gICAgdmFyIGlubmVyID0gdG9rZW5CYXNlKHN0cmVhbSwgc3RhdGUsIHByZXYpO1xuICAgIGlmIChpbm5lciA9PSBcInB1bmN0dWF0aW9uXCIpIHtcbiAgICAgIGlmIChzdHJlYW0uY3VycmVudCgpID09IFwiKFwiKSArK2RlcHRoO2Vsc2UgaWYgKHN0cmVhbS5jdXJyZW50KCkgPT0gXCIpXCIpIHtcbiAgICAgICAgaWYgKGRlcHRoID09IDApIHtcbiAgICAgICAgICBzdHJlYW0uYmFja1VwKDEpO1xuICAgICAgICAgIHN0YXRlLnRva2VuaXplLnBvcCgpO1xuICAgICAgICAgIHJldHVybiBzdGF0ZS50b2tlbml6ZVtzdGF0ZS50b2tlbml6ZS5sZW5ndGggLSAxXShzdHJlYW0sIHN0YXRlKTtcbiAgICAgICAgfSBlbHNlIC0tZGVwdGg7XG4gICAgICB9XG4gICAgfVxuICAgIHJldHVybiBpbm5lcjtcbiAgfTtcbn1cbmZ1bmN0aW9uIHRva2VuU3RyaW5nKG9wZW5RdW90ZSwgc3RyZWFtLCBzdGF0ZSkge1xuICB2YXIgc2luZ2xlTGluZSA9IG9wZW5RdW90ZS5sZW5ndGggPT0gMTtcbiAgdmFyIGNoLFxuICAgIGVzY2FwZWQgPSBmYWxzZTtcbiAgd2hpbGUgKGNoID0gc3RyZWFtLnBlZWsoKSkge1xuICAgIGlmIChlc2NhcGVkKSB7XG4gICAgICBzdHJlYW0ubmV4dCgpO1xuICAgICAgaWYgKGNoID09IFwiKFwiKSB7XG4gICAgICAgIHN0YXRlLnRva2VuaXplLnB1c2godG9rZW5VbnRpbENsb3NpbmdQYXJlbigpKTtcbiAgICAgICAgcmV0dXJuIFwic3RyaW5nXCI7XG4gICAgICB9XG4gICAgICBlc2NhcGVkID0gZmFsc2U7XG4gICAgfSBlbHNlIGlmIChzdHJlYW0ubWF0Y2gob3BlblF1b3RlKSkge1xuICAgICAgc3RhdGUudG9rZW5pemUucG9wKCk7XG4gICAgICByZXR1cm4gXCJzdHJpbmdcIjtcbiAgICB9IGVsc2Uge1xuICAgICAgc3RyZWFtLm5leHQoKTtcbiAgICAgIGVzY2FwZWQgPSBjaCA9PSBcIlxcXFxcIjtcbiAgICB9XG4gIH1cbiAgaWYgKHNpbmdsZUxpbmUpIHtcbiAgICBzdGF0ZS50b2tlbml6ZS5wb3AoKTtcbiAgfVxuICByZXR1cm4gXCJzdHJpbmdcIjtcbn1cbmZ1bmN0aW9uIHRva2VuQ29tbWVudChzdHJlYW0sIHN0YXRlKSB7XG4gIHZhciBjaDtcbiAgd2hpbGUgKGNoID0gc3RyZWFtLm5leHQoKSkge1xuICAgIGlmIChjaCA9PT0gXCIvXCIgJiYgc3RyZWFtLmVhdChcIipcIikpIHtcbiAgICAgIHN0YXRlLnRva2VuaXplLnB1c2godG9rZW5Db21tZW50KTtcbiAgICB9IGVsc2UgaWYgKGNoID09PSBcIipcIiAmJiBzdHJlYW0uZWF0KFwiL1wiKSkge1xuICAgICAgc3RhdGUudG9rZW5pemUucG9wKCk7XG4gICAgICBicmVhaztcbiAgICB9XG4gIH1cbiAgcmV0dXJuIFwiY29tbWVudFwiO1xufVxuZnVuY3Rpb24gQ29udGV4dChwcmV2LCBhbGlnbiwgaW5kZW50ZWQpIHtcbiAgdGhpcy5wcmV2ID0gcHJldjtcbiAgdGhpcy5hbGlnbiA9IGFsaWduO1xuICB0aGlzLmluZGVudGVkID0gaW5kZW50ZWQ7XG59XG5mdW5jdGlvbiBwdXNoQ29udGV4dChzdGF0ZSwgc3RyZWFtKSB7XG4gIHZhciBhbGlnbiA9IHN0cmVhbS5tYXRjaCgvXlxccyooJHxcXC9bXFwvXFwqXXxbKX1cXF1dKS8sIGZhbHNlKSA/IG51bGwgOiBzdHJlYW0uY29sdW1uKCkgKyAxO1xuICBzdGF0ZS5jb250ZXh0ID0gbmV3IENvbnRleHQoc3RhdGUuY29udGV4dCwgYWxpZ24sIHN0YXRlLmluZGVudGVkKTtcbn1cbmZ1bmN0aW9uIHBvcENvbnRleHQoc3RhdGUpIHtcbiAgaWYgKHN0YXRlLmNvbnRleHQpIHtcbiAgICBzdGF0ZS5pbmRlbnRlZCA9IHN0YXRlLmNvbnRleHQuaW5kZW50ZWQ7XG4gICAgc3RhdGUuY29udGV4dCA9IHN0YXRlLmNvbnRleHQucHJldjtcbiAgfVxufVxuZXhwb3J0IGNvbnN0IHN3aWZ0ID0ge1xuICBuYW1lOiBcInN3aWZ0XCIsXG4gIHN0YXJ0U3RhdGU6IGZ1bmN0aW9uICgpIHtcbiAgICByZXR1cm4ge1xuICAgICAgcHJldjogbnVsbCxcbiAgICAgIGNvbnRleHQ6IG51bGwsXG4gICAgICBpbmRlbnRlZDogMCxcbiAgICAgIHRva2VuaXplOiBbXVxuICAgIH07XG4gIH0sXG4gIHRva2VuOiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIHZhciBwcmV2ID0gc3RhdGUucHJldjtcbiAgICBzdGF0ZS5wcmV2ID0gbnVsbDtcbiAgICB2YXIgdG9rZW5pemUgPSBzdGF0ZS50b2tlbml6ZVtzdGF0ZS50b2tlbml6ZS5sZW5ndGggLSAxXSB8fCB0b2tlbkJhc2U7XG4gICAgdmFyIHN0eWxlID0gdG9rZW5pemUoc3RyZWFtLCBzdGF0ZSwgcHJldik7XG4gICAgaWYgKCFzdHlsZSB8fCBzdHlsZSA9PSBcImNvbW1lbnRcIikgc3RhdGUucHJldiA9IHByZXY7ZWxzZSBpZiAoIXN0YXRlLnByZXYpIHN0YXRlLnByZXYgPSBzdHlsZTtcbiAgICBpZiAoc3R5bGUgPT0gXCJwdW5jdHVhdGlvblwiKSB7XG4gICAgICB2YXIgYnJhY2tldCA9IC9bXFwoXFxbXFx7XXwoW1xcXVxcKVxcfV0pLy5leGVjKHN0cmVhbS5jdXJyZW50KCkpO1xuICAgICAgaWYgKGJyYWNrZXQpIChicmFja2V0WzFdID8gcG9wQ29udGV4dCA6IHB1c2hDb250ZXh0KShzdGF0ZSwgc3RyZWFtKTtcbiAgICB9XG4gICAgcmV0dXJuIHN0eWxlO1xuICB9LFxuICBpbmRlbnQ6IGZ1bmN0aW9uIChzdGF0ZSwgdGV4dEFmdGVyLCBpQ3gpIHtcbiAgICB2YXIgY3ggPSBzdGF0ZS5jb250ZXh0O1xuICAgIGlmICghY3gpIHJldHVybiAwO1xuICAgIHZhciBjbG9zaW5nID0gL15bXFxdXFx9XFwpXS8udGVzdCh0ZXh0QWZ0ZXIpO1xuICAgIGlmIChjeC5hbGlnbiAhPSBudWxsKSByZXR1cm4gY3guYWxpZ24gLSAoY2xvc2luZyA/IDEgOiAwKTtcbiAgICByZXR1cm4gY3guaW5kZW50ZWQgKyAoY2xvc2luZyA/IDAgOiBpQ3gudW5pdCk7XG4gIH0sXG4gIGxhbmd1YWdlRGF0YToge1xuICAgIGluZGVudE9uSW5wdXQ6IC9eXFxzKltcXClcXH1cXF1dJC8sXG4gICAgY29tbWVudFRva2Vuczoge1xuICAgICAgbGluZTogXCIvL1wiLFxuICAgICAgYmxvY2s6IHtcbiAgICAgICAgb3BlbjogXCIvKlwiLFxuICAgICAgICBjbG9zZTogXCIqL1wiXG4gICAgICB9XG4gICAgfSxcbiAgICBjbG9zZUJyYWNrZXRzOiB7XG4gICAgICBicmFja2V0czogW1wiKFwiLCBcIltcIiwgXCJ7XCIsIFwiJ1wiLCAnXCInLCBcImBcIl1cbiAgICB9XG4gIH1cbn07Il0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9