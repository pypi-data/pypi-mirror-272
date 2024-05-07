"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[6177],{

/***/ 86177:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "vb": () => (/* binding */ vb)
/* harmony export */ });
var ERRORCLASS = 'error';
function wordRegexp(words) {
  return new RegExp("^((" + words.join(")|(") + "))\\b", "i");
}
var singleOperators = new RegExp("^[\\+\\-\\*/%&\\\\|\\^~<>!]");
var singleDelimiters = new RegExp('^[\\(\\)\\[\\]\\{\\}@,:`=;\\.]');
var doubleOperators = new RegExp("^((==)|(<>)|(<=)|(>=)|(<>)|(<<)|(>>)|(//)|(\\*\\*))");
var doubleDelimiters = new RegExp("^((\\+=)|(\\-=)|(\\*=)|(%=)|(/=)|(&=)|(\\|=)|(\\^=))");
var tripleDelimiters = new RegExp("^((//=)|(>>=)|(<<=)|(\\*\\*=))");
var identifiers = new RegExp("^[_A-Za-z][_A-Za-z0-9]*");
var openingKeywords = ['class', 'module', 'sub', 'enum', 'select', 'while', 'if', 'function', 'get', 'set', 'property', 'try', 'structure', 'synclock', 'using', 'with'];
var middleKeywords = ['else', 'elseif', 'case', 'catch', 'finally'];
var endKeywords = ['next', 'loop'];
var operatorKeywords = ['and', "andalso", 'or', 'orelse', 'xor', 'in', 'not', 'is', 'isnot', 'like'];
var wordOperators = wordRegexp(operatorKeywords);
var commonKeywords = ["#const", "#else", "#elseif", "#end", "#if", "#region", "addhandler", "addressof", "alias", "as", "byref", "byval", "cbool", "cbyte", "cchar", "cdate", "cdbl", "cdec", "cint", "clng", "cobj", "compare", "const", "continue", "csbyte", "cshort", "csng", "cstr", "cuint", "culng", "cushort", "declare", "default", "delegate", "dim", "directcast", "each", "erase", "error", "event", "exit", "explicit", "false", "for", "friend", "gettype", "goto", "handles", "implements", "imports", "infer", "inherits", "interface", "isfalse", "istrue", "lib", "me", "mod", "mustinherit", "mustoverride", "my", "mybase", "myclass", "namespace", "narrowing", "new", "nothing", "notinheritable", "notoverridable", "of", "off", "on", "operator", "option", "optional", "out", "overloads", "overridable", "overrides", "paramarray", "partial", "private", "protected", "public", "raiseevent", "readonly", "redim", "removehandler", "resume", "return", "shadows", "shared", "static", "step", "stop", "strict", "then", "throw", "to", "true", "trycast", "typeof", "until", "until", "when", "widening", "withevents", "writeonly"];
var commontypes = ['object', 'boolean', 'char', 'string', 'byte', 'sbyte', 'short', 'ushort', 'int16', 'uint16', 'integer', 'uinteger', 'int32', 'uint32', 'long', 'ulong', 'int64', 'uint64', 'decimal', 'single', 'double', 'float', 'date', 'datetime', 'intptr', 'uintptr'];
var keywords = wordRegexp(commonKeywords);
var types = wordRegexp(commontypes);
var stringPrefixes = '"';
var opening = wordRegexp(openingKeywords);
var middle = wordRegexp(middleKeywords);
var closing = wordRegexp(endKeywords);
var doubleClosing = wordRegexp(['end']);
var doOpening = wordRegexp(['do']);
var indentInfo = null;
function indent(_stream, state) {
  state.currentIndent++;
}
function dedent(_stream, state) {
  state.currentIndent--;
}
// tokenizers
function tokenBase(stream, state) {
  if (stream.eatSpace()) {
    return null;
  }
  var ch = stream.peek();

  // Handle Comments
  if (ch === "'") {
    stream.skipToEnd();
    return 'comment';
  }

  // Handle Number Literals
  if (stream.match(/^((&H)|(&O))?[0-9\.a-f]/i, false)) {
    var floatLiteral = false;
    // Floats
    if (stream.match(/^\d*\.\d+F?/i)) {
      floatLiteral = true;
    } else if (stream.match(/^\d+\.\d*F?/)) {
      floatLiteral = true;
    } else if (stream.match(/^\.\d+F?/)) {
      floatLiteral = true;
    }
    if (floatLiteral) {
      // Float literals may be "imaginary"
      stream.eat(/J/i);
      return 'number';
    }
    // Integers
    var intLiteral = false;
    // Hex
    if (stream.match(/^&H[0-9a-f]+/i)) {
      intLiteral = true;
    }
    // Octal
    else if (stream.match(/^&O[0-7]+/i)) {
      intLiteral = true;
    }
    // Decimal
    else if (stream.match(/^[1-9]\d*F?/)) {
      // Decimal literals may be "imaginary"
      stream.eat(/J/i);
      // TODO - Can you have imaginary longs?
      intLiteral = true;
    }
    // Zero by itself with no other piece of number.
    else if (stream.match(/^0(?![\dx])/i)) {
      intLiteral = true;
    }
    if (intLiteral) {
      // Integer literals may be "long"
      stream.eat(/L/i);
      return 'number';
    }
  }

  // Handle Strings
  if (stream.match(stringPrefixes)) {
    state.tokenize = tokenStringFactory(stream.current());
    return state.tokenize(stream, state);
  }

  // Handle operators and Delimiters
  if (stream.match(tripleDelimiters) || stream.match(doubleDelimiters)) {
    return null;
  }
  if (stream.match(doubleOperators) || stream.match(singleOperators) || stream.match(wordOperators)) {
    return 'operator';
  }
  if (stream.match(singleDelimiters)) {
    return null;
  }
  if (stream.match(doOpening)) {
    indent(stream, state);
    state.doInCurrentLine = true;
    return 'keyword';
  }
  if (stream.match(opening)) {
    if (!state.doInCurrentLine) indent(stream, state);else state.doInCurrentLine = false;
    return 'keyword';
  }
  if (stream.match(middle)) {
    return 'keyword';
  }
  if (stream.match(doubleClosing)) {
    dedent(stream, state);
    dedent(stream, state);
    return 'keyword';
  }
  if (stream.match(closing)) {
    dedent(stream, state);
    return 'keyword';
  }
  if (stream.match(types)) {
    return 'keyword';
  }
  if (stream.match(keywords)) {
    return 'keyword';
  }
  if (stream.match(identifiers)) {
    return 'variable';
  }

  // Handle non-detected items
  stream.next();
  return ERRORCLASS;
}
function tokenStringFactory(delimiter) {
  var singleline = delimiter.length == 1;
  var OUTCLASS = 'string';
  return function (stream, state) {
    while (!stream.eol()) {
      stream.eatWhile(/[^'"]/);
      if (stream.match(delimiter)) {
        state.tokenize = tokenBase;
        return OUTCLASS;
      } else {
        stream.eat(/['"]/);
      }
    }
    if (singleline) {
      state.tokenize = tokenBase;
    }
    return OUTCLASS;
  };
}
function tokenLexer(stream, state) {
  var style = state.tokenize(stream, state);
  var current = stream.current();

  // Handle '.' connected identifiers
  if (current === '.') {
    style = state.tokenize(stream, state);
    if (style === 'variable') {
      return 'variable';
    } else {
      return ERRORCLASS;
    }
  }
  var delimiter_index = '[({'.indexOf(current);
  if (delimiter_index !== -1) {
    indent(stream, state);
  }
  if (indentInfo === 'dedent') {
    if (dedent(stream, state)) {
      return ERRORCLASS;
    }
  }
  delimiter_index = '])}'.indexOf(current);
  if (delimiter_index !== -1) {
    if (dedent(stream, state)) {
      return ERRORCLASS;
    }
  }
  return style;
}
const vb = {
  name: "vb",
  startState: function () {
    return {
      tokenize: tokenBase,
      lastToken: null,
      currentIndent: 0,
      nextLineIndent: 0,
      doInCurrentLine: false
    };
  },
  token: function (stream, state) {
    if (stream.sol()) {
      state.currentIndent += state.nextLineIndent;
      state.nextLineIndent = 0;
      state.doInCurrentLine = 0;
    }
    var style = tokenLexer(stream, state);
    state.lastToken = {
      style: style,
      content: stream.current()
    };
    return style;
  },
  indent: function (state, textAfter, cx) {
    var trueText = textAfter.replace(/^\s+|\s+$/g, '');
    if (trueText.match(closing) || trueText.match(doubleClosing) || trueText.match(middle)) return cx.unit * (state.currentIndent - 1);
    if (state.currentIndent < 0) return 0;
    return state.currentIndent * cx.unit;
  },
  languageData: {
    closeBrackets: {
      brackets: ["(", "[", "{", '"']
    },
    commentTokens: {
      line: "'"
    },
    autocomplete: openingKeywords.concat(middleKeywords).concat(endKeywords).concat(operatorKeywords).concat(commonKeywords).concat(commontypes)
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNjE3Ny5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL0Bjb2RlbWlycm9yL2xlZ2FjeS1tb2Rlcy9tb2RlL3ZiLmpzIl0sInNvdXJjZXNDb250ZW50IjpbInZhciBFUlJPUkNMQVNTID0gJ2Vycm9yJztcbmZ1bmN0aW9uIHdvcmRSZWdleHAod29yZHMpIHtcbiAgcmV0dXJuIG5ldyBSZWdFeHAoXCJeKChcIiArIHdvcmRzLmpvaW4oXCIpfChcIikgKyBcIikpXFxcXGJcIiwgXCJpXCIpO1xufVxudmFyIHNpbmdsZU9wZXJhdG9ycyA9IG5ldyBSZWdFeHAoXCJeW1xcXFwrXFxcXC1cXFxcKi8lJlxcXFxcXFxcfFxcXFxefjw+IV1cIik7XG52YXIgc2luZ2xlRGVsaW1pdGVycyA9IG5ldyBSZWdFeHAoJ15bXFxcXChcXFxcKVxcXFxbXFxcXF1cXFxce1xcXFx9QCw6YD07XFxcXC5dJyk7XG52YXIgZG91YmxlT3BlcmF0b3JzID0gbmV3IFJlZ0V4cChcIl4oKD09KXwoPD4pfCg8PSl8KD49KXwoPD4pfCg8PCl8KD4+KXwoLy8pfChcXFxcKlxcXFwqKSlcIik7XG52YXIgZG91YmxlRGVsaW1pdGVycyA9IG5ldyBSZWdFeHAoXCJeKChcXFxcKz0pfChcXFxcLT0pfChcXFxcKj0pfCglPSl8KC89KXwoJj0pfChcXFxcfD0pfChcXFxcXj0pKVwiKTtcbnZhciB0cmlwbGVEZWxpbWl0ZXJzID0gbmV3IFJlZ0V4cChcIl4oKC8vPSl8KD4+PSl8KDw8PSl8KFxcXFwqXFxcXCo9KSlcIik7XG52YXIgaWRlbnRpZmllcnMgPSBuZXcgUmVnRXhwKFwiXltfQS1aYS16XVtfQS1aYS16MC05XSpcIik7XG52YXIgb3BlbmluZ0tleXdvcmRzID0gWydjbGFzcycsICdtb2R1bGUnLCAnc3ViJywgJ2VudW0nLCAnc2VsZWN0JywgJ3doaWxlJywgJ2lmJywgJ2Z1bmN0aW9uJywgJ2dldCcsICdzZXQnLCAncHJvcGVydHknLCAndHJ5JywgJ3N0cnVjdHVyZScsICdzeW5jbG9jaycsICd1c2luZycsICd3aXRoJ107XG52YXIgbWlkZGxlS2V5d29yZHMgPSBbJ2Vsc2UnLCAnZWxzZWlmJywgJ2Nhc2UnLCAnY2F0Y2gnLCAnZmluYWxseSddO1xudmFyIGVuZEtleXdvcmRzID0gWyduZXh0JywgJ2xvb3AnXTtcbnZhciBvcGVyYXRvcktleXdvcmRzID0gWydhbmQnLCBcImFuZGFsc29cIiwgJ29yJywgJ29yZWxzZScsICd4b3InLCAnaW4nLCAnbm90JywgJ2lzJywgJ2lzbm90JywgJ2xpa2UnXTtcbnZhciB3b3JkT3BlcmF0b3JzID0gd29yZFJlZ2V4cChvcGVyYXRvcktleXdvcmRzKTtcbnZhciBjb21tb25LZXl3b3JkcyA9IFtcIiNjb25zdFwiLCBcIiNlbHNlXCIsIFwiI2Vsc2VpZlwiLCBcIiNlbmRcIiwgXCIjaWZcIiwgXCIjcmVnaW9uXCIsIFwiYWRkaGFuZGxlclwiLCBcImFkZHJlc3NvZlwiLCBcImFsaWFzXCIsIFwiYXNcIiwgXCJieXJlZlwiLCBcImJ5dmFsXCIsIFwiY2Jvb2xcIiwgXCJjYnl0ZVwiLCBcImNjaGFyXCIsIFwiY2RhdGVcIiwgXCJjZGJsXCIsIFwiY2RlY1wiLCBcImNpbnRcIiwgXCJjbG5nXCIsIFwiY29ialwiLCBcImNvbXBhcmVcIiwgXCJjb25zdFwiLCBcImNvbnRpbnVlXCIsIFwiY3NieXRlXCIsIFwiY3Nob3J0XCIsIFwiY3NuZ1wiLCBcImNzdHJcIiwgXCJjdWludFwiLCBcImN1bG5nXCIsIFwiY3VzaG9ydFwiLCBcImRlY2xhcmVcIiwgXCJkZWZhdWx0XCIsIFwiZGVsZWdhdGVcIiwgXCJkaW1cIiwgXCJkaXJlY3RjYXN0XCIsIFwiZWFjaFwiLCBcImVyYXNlXCIsIFwiZXJyb3JcIiwgXCJldmVudFwiLCBcImV4aXRcIiwgXCJleHBsaWNpdFwiLCBcImZhbHNlXCIsIFwiZm9yXCIsIFwiZnJpZW5kXCIsIFwiZ2V0dHlwZVwiLCBcImdvdG9cIiwgXCJoYW5kbGVzXCIsIFwiaW1wbGVtZW50c1wiLCBcImltcG9ydHNcIiwgXCJpbmZlclwiLCBcImluaGVyaXRzXCIsIFwiaW50ZXJmYWNlXCIsIFwiaXNmYWxzZVwiLCBcImlzdHJ1ZVwiLCBcImxpYlwiLCBcIm1lXCIsIFwibW9kXCIsIFwibXVzdGluaGVyaXRcIiwgXCJtdXN0b3ZlcnJpZGVcIiwgXCJteVwiLCBcIm15YmFzZVwiLCBcIm15Y2xhc3NcIiwgXCJuYW1lc3BhY2VcIiwgXCJuYXJyb3dpbmdcIiwgXCJuZXdcIiwgXCJub3RoaW5nXCIsIFwibm90aW5oZXJpdGFibGVcIiwgXCJub3RvdmVycmlkYWJsZVwiLCBcIm9mXCIsIFwib2ZmXCIsIFwib25cIiwgXCJvcGVyYXRvclwiLCBcIm9wdGlvblwiLCBcIm9wdGlvbmFsXCIsIFwib3V0XCIsIFwib3ZlcmxvYWRzXCIsIFwib3ZlcnJpZGFibGVcIiwgXCJvdmVycmlkZXNcIiwgXCJwYXJhbWFycmF5XCIsIFwicGFydGlhbFwiLCBcInByaXZhdGVcIiwgXCJwcm90ZWN0ZWRcIiwgXCJwdWJsaWNcIiwgXCJyYWlzZWV2ZW50XCIsIFwicmVhZG9ubHlcIiwgXCJyZWRpbVwiLCBcInJlbW92ZWhhbmRsZXJcIiwgXCJyZXN1bWVcIiwgXCJyZXR1cm5cIiwgXCJzaGFkb3dzXCIsIFwic2hhcmVkXCIsIFwic3RhdGljXCIsIFwic3RlcFwiLCBcInN0b3BcIiwgXCJzdHJpY3RcIiwgXCJ0aGVuXCIsIFwidGhyb3dcIiwgXCJ0b1wiLCBcInRydWVcIiwgXCJ0cnljYXN0XCIsIFwidHlwZW9mXCIsIFwidW50aWxcIiwgXCJ1bnRpbFwiLCBcIndoZW5cIiwgXCJ3aWRlbmluZ1wiLCBcIndpdGhldmVudHNcIiwgXCJ3cml0ZW9ubHlcIl07XG52YXIgY29tbW9udHlwZXMgPSBbJ29iamVjdCcsICdib29sZWFuJywgJ2NoYXInLCAnc3RyaW5nJywgJ2J5dGUnLCAnc2J5dGUnLCAnc2hvcnQnLCAndXNob3J0JywgJ2ludDE2JywgJ3VpbnQxNicsICdpbnRlZ2VyJywgJ3VpbnRlZ2VyJywgJ2ludDMyJywgJ3VpbnQzMicsICdsb25nJywgJ3Vsb25nJywgJ2ludDY0JywgJ3VpbnQ2NCcsICdkZWNpbWFsJywgJ3NpbmdsZScsICdkb3VibGUnLCAnZmxvYXQnLCAnZGF0ZScsICdkYXRldGltZScsICdpbnRwdHInLCAndWludHB0ciddO1xudmFyIGtleXdvcmRzID0gd29yZFJlZ2V4cChjb21tb25LZXl3b3Jkcyk7XG52YXIgdHlwZXMgPSB3b3JkUmVnZXhwKGNvbW1vbnR5cGVzKTtcbnZhciBzdHJpbmdQcmVmaXhlcyA9ICdcIic7XG52YXIgb3BlbmluZyA9IHdvcmRSZWdleHAob3BlbmluZ0tleXdvcmRzKTtcbnZhciBtaWRkbGUgPSB3b3JkUmVnZXhwKG1pZGRsZUtleXdvcmRzKTtcbnZhciBjbG9zaW5nID0gd29yZFJlZ2V4cChlbmRLZXl3b3Jkcyk7XG52YXIgZG91YmxlQ2xvc2luZyA9IHdvcmRSZWdleHAoWydlbmQnXSk7XG52YXIgZG9PcGVuaW5nID0gd29yZFJlZ2V4cChbJ2RvJ10pO1xudmFyIGluZGVudEluZm8gPSBudWxsO1xuZnVuY3Rpb24gaW5kZW50KF9zdHJlYW0sIHN0YXRlKSB7XG4gIHN0YXRlLmN1cnJlbnRJbmRlbnQrKztcbn1cbmZ1bmN0aW9uIGRlZGVudChfc3RyZWFtLCBzdGF0ZSkge1xuICBzdGF0ZS5jdXJyZW50SW5kZW50LS07XG59XG4vLyB0b2tlbml6ZXJzXG5mdW5jdGlvbiB0b2tlbkJhc2Uoc3RyZWFtLCBzdGF0ZSkge1xuICBpZiAoc3RyZWFtLmVhdFNwYWNlKCkpIHtcbiAgICByZXR1cm4gbnVsbDtcbiAgfVxuICB2YXIgY2ggPSBzdHJlYW0ucGVlaygpO1xuXG4gIC8vIEhhbmRsZSBDb21tZW50c1xuICBpZiAoY2ggPT09IFwiJ1wiKSB7XG4gICAgc3RyZWFtLnNraXBUb0VuZCgpO1xuICAgIHJldHVybiAnY29tbWVudCc7XG4gIH1cblxuICAvLyBIYW5kbGUgTnVtYmVyIExpdGVyYWxzXG4gIGlmIChzdHJlYW0ubWF0Y2goL14oKCZIKXwoJk8pKT9bMC05XFwuYS1mXS9pLCBmYWxzZSkpIHtcbiAgICB2YXIgZmxvYXRMaXRlcmFsID0gZmFsc2U7XG4gICAgLy8gRmxvYXRzXG4gICAgaWYgKHN0cmVhbS5tYXRjaCgvXlxcZCpcXC5cXGQrRj8vaSkpIHtcbiAgICAgIGZsb2F0TGl0ZXJhbCA9IHRydWU7XG4gICAgfSBlbHNlIGlmIChzdHJlYW0ubWF0Y2goL15cXGQrXFwuXFxkKkY/LykpIHtcbiAgICAgIGZsb2F0TGl0ZXJhbCA9IHRydWU7XG4gICAgfSBlbHNlIGlmIChzdHJlYW0ubWF0Y2goL15cXC5cXGQrRj8vKSkge1xuICAgICAgZmxvYXRMaXRlcmFsID0gdHJ1ZTtcbiAgICB9XG4gICAgaWYgKGZsb2F0TGl0ZXJhbCkge1xuICAgICAgLy8gRmxvYXQgbGl0ZXJhbHMgbWF5IGJlIFwiaW1hZ2luYXJ5XCJcbiAgICAgIHN0cmVhbS5lYXQoL0ovaSk7XG4gICAgICByZXR1cm4gJ251bWJlcic7XG4gICAgfVxuICAgIC8vIEludGVnZXJzXG4gICAgdmFyIGludExpdGVyYWwgPSBmYWxzZTtcbiAgICAvLyBIZXhcbiAgICBpZiAoc3RyZWFtLm1hdGNoKC9eJkhbMC05YS1mXSsvaSkpIHtcbiAgICAgIGludExpdGVyYWwgPSB0cnVlO1xuICAgIH1cbiAgICAvLyBPY3RhbFxuICAgIGVsc2UgaWYgKHN0cmVhbS5tYXRjaCgvXiZPWzAtN10rL2kpKSB7XG4gICAgICBpbnRMaXRlcmFsID0gdHJ1ZTtcbiAgICB9XG4gICAgLy8gRGVjaW1hbFxuICAgIGVsc2UgaWYgKHN0cmVhbS5tYXRjaCgvXlsxLTldXFxkKkY/LykpIHtcbiAgICAgIC8vIERlY2ltYWwgbGl0ZXJhbHMgbWF5IGJlIFwiaW1hZ2luYXJ5XCJcbiAgICAgIHN0cmVhbS5lYXQoL0ovaSk7XG4gICAgICAvLyBUT0RPIC0gQ2FuIHlvdSBoYXZlIGltYWdpbmFyeSBsb25ncz9cbiAgICAgIGludExpdGVyYWwgPSB0cnVlO1xuICAgIH1cbiAgICAvLyBaZXJvIGJ5IGl0c2VsZiB3aXRoIG5vIG90aGVyIHBpZWNlIG9mIG51bWJlci5cbiAgICBlbHNlIGlmIChzdHJlYW0ubWF0Y2goL14wKD8hW1xcZHhdKS9pKSkge1xuICAgICAgaW50TGl0ZXJhbCA9IHRydWU7XG4gICAgfVxuICAgIGlmIChpbnRMaXRlcmFsKSB7XG4gICAgICAvLyBJbnRlZ2VyIGxpdGVyYWxzIG1heSBiZSBcImxvbmdcIlxuICAgICAgc3RyZWFtLmVhdCgvTC9pKTtcbiAgICAgIHJldHVybiAnbnVtYmVyJztcbiAgICB9XG4gIH1cblxuICAvLyBIYW5kbGUgU3RyaW5nc1xuICBpZiAoc3RyZWFtLm1hdGNoKHN0cmluZ1ByZWZpeGVzKSkge1xuICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5TdHJpbmdGYWN0b3J5KHN0cmVhbS5jdXJyZW50KCkpO1xuICAgIHJldHVybiBzdGF0ZS50b2tlbml6ZShzdHJlYW0sIHN0YXRlKTtcbiAgfVxuXG4gIC8vIEhhbmRsZSBvcGVyYXRvcnMgYW5kIERlbGltaXRlcnNcbiAgaWYgKHN0cmVhbS5tYXRjaCh0cmlwbGVEZWxpbWl0ZXJzKSB8fCBzdHJlYW0ubWF0Y2goZG91YmxlRGVsaW1pdGVycykpIHtcbiAgICByZXR1cm4gbnVsbDtcbiAgfVxuICBpZiAoc3RyZWFtLm1hdGNoKGRvdWJsZU9wZXJhdG9ycykgfHwgc3RyZWFtLm1hdGNoKHNpbmdsZU9wZXJhdG9ycykgfHwgc3RyZWFtLm1hdGNoKHdvcmRPcGVyYXRvcnMpKSB7XG4gICAgcmV0dXJuICdvcGVyYXRvcic7XG4gIH1cbiAgaWYgKHN0cmVhbS5tYXRjaChzaW5nbGVEZWxpbWl0ZXJzKSkge1xuICAgIHJldHVybiBudWxsO1xuICB9XG4gIGlmIChzdHJlYW0ubWF0Y2goZG9PcGVuaW5nKSkge1xuICAgIGluZGVudChzdHJlYW0sIHN0YXRlKTtcbiAgICBzdGF0ZS5kb0luQ3VycmVudExpbmUgPSB0cnVlO1xuICAgIHJldHVybiAna2V5d29yZCc7XG4gIH1cbiAgaWYgKHN0cmVhbS5tYXRjaChvcGVuaW5nKSkge1xuICAgIGlmICghc3RhdGUuZG9JbkN1cnJlbnRMaW5lKSBpbmRlbnQoc3RyZWFtLCBzdGF0ZSk7ZWxzZSBzdGF0ZS5kb0luQ3VycmVudExpbmUgPSBmYWxzZTtcbiAgICByZXR1cm4gJ2tleXdvcmQnO1xuICB9XG4gIGlmIChzdHJlYW0ubWF0Y2gobWlkZGxlKSkge1xuICAgIHJldHVybiAna2V5d29yZCc7XG4gIH1cbiAgaWYgKHN0cmVhbS5tYXRjaChkb3VibGVDbG9zaW5nKSkge1xuICAgIGRlZGVudChzdHJlYW0sIHN0YXRlKTtcbiAgICBkZWRlbnQoc3RyZWFtLCBzdGF0ZSk7XG4gICAgcmV0dXJuICdrZXl3b3JkJztcbiAgfVxuICBpZiAoc3RyZWFtLm1hdGNoKGNsb3NpbmcpKSB7XG4gICAgZGVkZW50KHN0cmVhbSwgc3RhdGUpO1xuICAgIHJldHVybiAna2V5d29yZCc7XG4gIH1cbiAgaWYgKHN0cmVhbS5tYXRjaCh0eXBlcykpIHtcbiAgICByZXR1cm4gJ2tleXdvcmQnO1xuICB9XG4gIGlmIChzdHJlYW0ubWF0Y2goa2V5d29yZHMpKSB7XG4gICAgcmV0dXJuICdrZXl3b3JkJztcbiAgfVxuICBpZiAoc3RyZWFtLm1hdGNoKGlkZW50aWZpZXJzKSkge1xuICAgIHJldHVybiAndmFyaWFibGUnO1xuICB9XG5cbiAgLy8gSGFuZGxlIG5vbi1kZXRlY3RlZCBpdGVtc1xuICBzdHJlYW0ubmV4dCgpO1xuICByZXR1cm4gRVJST1JDTEFTUztcbn1cbmZ1bmN0aW9uIHRva2VuU3RyaW5nRmFjdG9yeShkZWxpbWl0ZXIpIHtcbiAgdmFyIHNpbmdsZWxpbmUgPSBkZWxpbWl0ZXIubGVuZ3RoID09IDE7XG4gIHZhciBPVVRDTEFTUyA9ICdzdHJpbmcnO1xuICByZXR1cm4gZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICB3aGlsZSAoIXN0cmVhbS5lb2woKSkge1xuICAgICAgc3RyZWFtLmVhdFdoaWxlKC9bXidcIl0vKTtcbiAgICAgIGlmIChzdHJlYW0ubWF0Y2goZGVsaW1pdGVyKSkge1xuICAgICAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQmFzZTtcbiAgICAgICAgcmV0dXJuIE9VVENMQVNTO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgc3RyZWFtLmVhdCgvWydcIl0vKTtcbiAgICAgIH1cbiAgICB9XG4gICAgaWYgKHNpbmdsZWxpbmUpIHtcbiAgICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlO1xuICAgIH1cbiAgICByZXR1cm4gT1VUQ0xBU1M7XG4gIH07XG59XG5mdW5jdGlvbiB0b2tlbkxleGVyKHN0cmVhbSwgc3RhdGUpIHtcbiAgdmFyIHN0eWxlID0gc3RhdGUudG9rZW5pemUoc3RyZWFtLCBzdGF0ZSk7XG4gIHZhciBjdXJyZW50ID0gc3RyZWFtLmN1cnJlbnQoKTtcblxuICAvLyBIYW5kbGUgJy4nIGNvbm5lY3RlZCBpZGVudGlmaWVyc1xuICBpZiAoY3VycmVudCA9PT0gJy4nKSB7XG4gICAgc3R5bGUgPSBzdGF0ZS50b2tlbml6ZShzdHJlYW0sIHN0YXRlKTtcbiAgICBpZiAoc3R5bGUgPT09ICd2YXJpYWJsZScpIHtcbiAgICAgIHJldHVybiAndmFyaWFibGUnO1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gRVJST1JDTEFTUztcbiAgICB9XG4gIH1cbiAgdmFyIGRlbGltaXRlcl9pbmRleCA9ICdbKHsnLmluZGV4T2YoY3VycmVudCk7XG4gIGlmIChkZWxpbWl0ZXJfaW5kZXggIT09IC0xKSB7XG4gICAgaW5kZW50KHN0cmVhbSwgc3RhdGUpO1xuICB9XG4gIGlmIChpbmRlbnRJbmZvID09PSAnZGVkZW50Jykge1xuICAgIGlmIChkZWRlbnQoc3RyZWFtLCBzdGF0ZSkpIHtcbiAgICAgIHJldHVybiBFUlJPUkNMQVNTO1xuICAgIH1cbiAgfVxuICBkZWxpbWl0ZXJfaW5kZXggPSAnXSl9Jy5pbmRleE9mKGN1cnJlbnQpO1xuICBpZiAoZGVsaW1pdGVyX2luZGV4ICE9PSAtMSkge1xuICAgIGlmIChkZWRlbnQoc3RyZWFtLCBzdGF0ZSkpIHtcbiAgICAgIHJldHVybiBFUlJPUkNMQVNTO1xuICAgIH1cbiAgfVxuICByZXR1cm4gc3R5bGU7XG59XG5leHBvcnQgY29uc3QgdmIgPSB7XG4gIG5hbWU6IFwidmJcIixcbiAgc3RhcnRTdGF0ZTogZnVuY3Rpb24gKCkge1xuICAgIHJldHVybiB7XG4gICAgICB0b2tlbml6ZTogdG9rZW5CYXNlLFxuICAgICAgbGFzdFRva2VuOiBudWxsLFxuICAgICAgY3VycmVudEluZGVudDogMCxcbiAgICAgIG5leHRMaW5lSW5kZW50OiAwLFxuICAgICAgZG9JbkN1cnJlbnRMaW5lOiBmYWxzZVxuICAgIH07XG4gIH0sXG4gIHRva2VuOiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIGlmIChzdHJlYW0uc29sKCkpIHtcbiAgICAgIHN0YXRlLmN1cnJlbnRJbmRlbnQgKz0gc3RhdGUubmV4dExpbmVJbmRlbnQ7XG4gICAgICBzdGF0ZS5uZXh0TGluZUluZGVudCA9IDA7XG4gICAgICBzdGF0ZS5kb0luQ3VycmVudExpbmUgPSAwO1xuICAgIH1cbiAgICB2YXIgc3R5bGUgPSB0b2tlbkxleGVyKHN0cmVhbSwgc3RhdGUpO1xuICAgIHN0YXRlLmxhc3RUb2tlbiA9IHtcbiAgICAgIHN0eWxlOiBzdHlsZSxcbiAgICAgIGNvbnRlbnQ6IHN0cmVhbS5jdXJyZW50KClcbiAgICB9O1xuICAgIHJldHVybiBzdHlsZTtcbiAgfSxcbiAgaW5kZW50OiBmdW5jdGlvbiAoc3RhdGUsIHRleHRBZnRlciwgY3gpIHtcbiAgICB2YXIgdHJ1ZVRleHQgPSB0ZXh0QWZ0ZXIucmVwbGFjZSgvXlxccyt8XFxzKyQvZywgJycpO1xuICAgIGlmICh0cnVlVGV4dC5tYXRjaChjbG9zaW5nKSB8fCB0cnVlVGV4dC5tYXRjaChkb3VibGVDbG9zaW5nKSB8fCB0cnVlVGV4dC5tYXRjaChtaWRkbGUpKSByZXR1cm4gY3gudW5pdCAqIChzdGF0ZS5jdXJyZW50SW5kZW50IC0gMSk7XG4gICAgaWYgKHN0YXRlLmN1cnJlbnRJbmRlbnQgPCAwKSByZXR1cm4gMDtcbiAgICByZXR1cm4gc3RhdGUuY3VycmVudEluZGVudCAqIGN4LnVuaXQ7XG4gIH0sXG4gIGxhbmd1YWdlRGF0YToge1xuICAgIGNsb3NlQnJhY2tldHM6IHtcbiAgICAgIGJyYWNrZXRzOiBbXCIoXCIsIFwiW1wiLCBcIntcIiwgJ1wiJ11cbiAgICB9LFxuICAgIGNvbW1lbnRUb2tlbnM6IHtcbiAgICAgIGxpbmU6IFwiJ1wiXG4gICAgfSxcbiAgICBhdXRvY29tcGxldGU6IG9wZW5pbmdLZXl3b3Jkcy5jb25jYXQobWlkZGxlS2V5d29yZHMpLmNvbmNhdChlbmRLZXl3b3JkcykuY29uY2F0KG9wZXJhdG9yS2V5d29yZHMpLmNvbmNhdChjb21tb25LZXl3b3JkcykuY29uY2F0KGNvbW1vbnR5cGVzKVxuICB9XG59OyJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==