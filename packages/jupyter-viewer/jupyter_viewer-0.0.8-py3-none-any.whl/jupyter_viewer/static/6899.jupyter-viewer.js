"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[6899],{

/***/ 36899:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "vbScript": () => (/* binding */ vbScript),
/* harmony export */   "vbScriptASP": () => (/* binding */ vbScriptASP)
/* harmony export */ });
function mkVBScript(parserConf) {
  var ERRORCLASS = 'error';
  function wordRegexp(words) {
    return new RegExp("^((" + words.join(")|(") + "))\\b", "i");
  }
  var singleOperators = new RegExp("^[\\+\\-\\*/&\\\\\\^<>=]");
  var doubleOperators = new RegExp("^((<>)|(<=)|(>=))");
  var singleDelimiters = new RegExp('^[\\.,]');
  var brackets = new RegExp('^[\\(\\)]');
  var identifiers = new RegExp("^[A-Za-z][_A-Za-z0-9]*");
  var openingKeywords = ['class', 'sub', 'select', 'while', 'if', 'function', 'property', 'with', 'for'];
  var middleKeywords = ['else', 'elseif', 'case'];
  var endKeywords = ['next', 'loop', 'wend'];
  var wordOperators = wordRegexp(['and', 'or', 'not', 'xor', 'is', 'mod', 'eqv', 'imp']);
  var commonkeywords = ['dim', 'redim', 'then', 'until', 'randomize', 'byval', 'byref', 'new', 'property', 'exit', 'in', 'const', 'private', 'public', 'get', 'set', 'let', 'stop', 'on error resume next', 'on error goto 0', 'option explicit', 'call', 'me'];

  //This list was from: http://msdn.microsoft.com/en-us/library/f8tbc79x(v=vs.84).aspx
  var atomWords = ['true', 'false', 'nothing', 'empty', 'null'];
  //This list was from: http://msdn.microsoft.com/en-us/library/3ca8tfek(v=vs.84).aspx
  var builtinFuncsWords = ['abs', 'array', 'asc', 'atn', 'cbool', 'cbyte', 'ccur', 'cdate', 'cdbl', 'chr', 'cint', 'clng', 'cos', 'csng', 'cstr', 'date', 'dateadd', 'datediff', 'datepart', 'dateserial', 'datevalue', 'day', 'escape', 'eval', 'execute', 'exp', 'filter', 'formatcurrency', 'formatdatetime', 'formatnumber', 'formatpercent', 'getlocale', 'getobject', 'getref', 'hex', 'hour', 'inputbox', 'instr', 'instrrev', 'int', 'fix', 'isarray', 'isdate', 'isempty', 'isnull', 'isnumeric', 'isobject', 'join', 'lbound', 'lcase', 'left', 'len', 'loadpicture', 'log', 'ltrim', 'rtrim', 'trim', 'maths', 'mid', 'minute', 'month', 'monthname', 'msgbox', 'now', 'oct', 'replace', 'rgb', 'right', 'rnd', 'round', 'scriptengine', 'scriptenginebuildversion', 'scriptenginemajorversion', 'scriptengineminorversion', 'second', 'setlocale', 'sgn', 'sin', 'space', 'split', 'sqr', 'strcomp', 'string', 'strreverse', 'tan', 'time', 'timer', 'timeserial', 'timevalue', 'typename', 'ubound', 'ucase', 'unescape', 'vartype', 'weekday', 'weekdayname', 'year'];

  //This list was from: http://msdn.microsoft.com/en-us/library/ydz4cfk3(v=vs.84).aspx
  var builtinConsts = ['vbBlack', 'vbRed', 'vbGreen', 'vbYellow', 'vbBlue', 'vbMagenta', 'vbCyan', 'vbWhite', 'vbBinaryCompare', 'vbTextCompare', 'vbSunday', 'vbMonday', 'vbTuesday', 'vbWednesday', 'vbThursday', 'vbFriday', 'vbSaturday', 'vbUseSystemDayOfWeek', 'vbFirstJan1', 'vbFirstFourDays', 'vbFirstFullWeek', 'vbGeneralDate', 'vbLongDate', 'vbShortDate', 'vbLongTime', 'vbShortTime', 'vbObjectError', 'vbOKOnly', 'vbOKCancel', 'vbAbortRetryIgnore', 'vbYesNoCancel', 'vbYesNo', 'vbRetryCancel', 'vbCritical', 'vbQuestion', 'vbExclamation', 'vbInformation', 'vbDefaultButton1', 'vbDefaultButton2', 'vbDefaultButton3', 'vbDefaultButton4', 'vbApplicationModal', 'vbSystemModal', 'vbOK', 'vbCancel', 'vbAbort', 'vbRetry', 'vbIgnore', 'vbYes', 'vbNo', 'vbCr', 'VbCrLf', 'vbFormFeed', 'vbLf', 'vbNewLine', 'vbNullChar', 'vbNullString', 'vbTab', 'vbVerticalTab', 'vbUseDefault', 'vbTrue', 'vbFalse', 'vbEmpty', 'vbNull', 'vbInteger', 'vbLong', 'vbSingle', 'vbDouble', 'vbCurrency', 'vbDate', 'vbString', 'vbObject', 'vbError', 'vbBoolean', 'vbVariant', 'vbDataObject', 'vbDecimal', 'vbByte', 'vbArray'];
  //This list was from: http://msdn.microsoft.com/en-us/library/hkc375ea(v=vs.84).aspx
  var builtinObjsWords = ['WScript', 'err', 'debug', 'RegExp'];
  var knownProperties = ['description', 'firstindex', 'global', 'helpcontext', 'helpfile', 'ignorecase', 'length', 'number', 'pattern', 'source', 'value', 'count'];
  var knownMethods = ['clear', 'execute', 'raise', 'replace', 'test', 'write', 'writeline', 'close', 'open', 'state', 'eof', 'update', 'addnew', 'end', 'createobject', 'quit'];
  var aspBuiltinObjsWords = ['server', 'response', 'request', 'session', 'application'];
  var aspKnownProperties = ['buffer', 'cachecontrol', 'charset', 'contenttype', 'expires', 'expiresabsolute', 'isclientconnected', 'pics', 'status',
  //response
  'clientcertificate', 'cookies', 'form', 'querystring', 'servervariables', 'totalbytes',
  //request
  'contents', 'staticobjects',
  //application
  'codepage', 'lcid', 'sessionid', 'timeout',
  //session
  'scripttimeout']; //server
  var aspKnownMethods = ['addheader', 'appendtolog', 'binarywrite', 'end', 'flush', 'redirect',
  //response
  'binaryread',
  //request
  'remove', 'removeall', 'lock', 'unlock',
  //application
  'abandon',
  //session
  'getlasterror', 'htmlencode', 'mappath', 'transfer', 'urlencode']; //server

  var knownWords = knownMethods.concat(knownProperties);
  builtinObjsWords = builtinObjsWords.concat(builtinConsts);
  if (parserConf.isASP) {
    builtinObjsWords = builtinObjsWords.concat(aspBuiltinObjsWords);
    knownWords = knownWords.concat(aspKnownMethods, aspKnownProperties);
  }
  ;
  var keywords = wordRegexp(commonkeywords);
  var atoms = wordRegexp(atomWords);
  var builtinFuncs = wordRegexp(builtinFuncsWords);
  var builtinObjs = wordRegexp(builtinObjsWords);
  var known = wordRegexp(knownWords);
  var stringPrefixes = '"';
  var opening = wordRegexp(openingKeywords);
  var middle = wordRegexp(middleKeywords);
  var closing = wordRegexp(endKeywords);
  var doubleClosing = wordRegexp(['end']);
  var doOpening = wordRegexp(['do']);
  var noIndentWords = wordRegexp(['on error resume next', 'exit']);
  var comment = wordRegexp(['rem']);
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
      //return null;
    }
    var ch = stream.peek();

    // Handle Comments
    if (ch === "'") {
      stream.skipToEnd();
      return 'comment';
    }
    if (stream.match(comment)) {
      stream.skipToEnd();
      return 'comment';
    }

    // Handle Number Literals
    if (stream.match(/^((&H)|(&O))?[0-9\.]/i, false) && !stream.match(/^((&H)|(&O))?[0-9\.]+[a-z_]/i, false)) {
      var floatLiteral = false;
      // Floats
      if (stream.match(/^\d*\.\d+/i)) {
        floatLiteral = true;
      } else if (stream.match(/^\d+\.\d*/)) {
        floatLiteral = true;
      } else if (stream.match(/^\.\d+/)) {
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
    if (stream.match(doubleOperators) || stream.match(singleOperators) || stream.match(wordOperators)) {
      return 'operator';
    }
    if (stream.match(singleDelimiters)) {
      return null;
    }
    if (stream.match(brackets)) {
      return "bracket";
    }
    if (stream.match(noIndentWords)) {
      state.doInCurrentLine = true;
      return 'keyword';
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
      if (!state.doInCurrentLine) dedent(stream, state);else state.doInCurrentLine = false;
      return 'keyword';
    }
    if (stream.match(keywords)) {
      return 'keyword';
    }
    if (stream.match(atoms)) {
      return 'atom';
    }
    if (stream.match(known)) {
      return 'variableName.special';
    }
    if (stream.match(builtinFuncs)) {
      return 'builtin';
    }
    if (stream.match(builtinObjs)) {
      return 'builtin';
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
      current = stream.current();
      if (style && (style.substr(0, 8) === 'variable' || style === 'builtin' || style === 'keyword')) {
        //|| knownWords.indexOf(current.substring(1)) > -1) {
        if (style === 'builtin' || style === 'keyword') style = 'variable';
        if (knownWords.indexOf(current.substr(1)) > -1) style = 'keyword';
        return style;
      } else {
        return ERRORCLASS;
      }
    }
    return style;
  }
  return {
    name: "vbscript",
    startState: function () {
      return {
        tokenize: tokenBase,
        lastToken: null,
        currentIndent: 0,
        nextLineIndent: 0,
        doInCurrentLine: false,
        ignoreKeyword: false
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
      if (style === null) style = null;
      return style;
    },
    indent: function (state, textAfter, cx) {
      var trueText = textAfter.replace(/^\s+|\s+$/g, '');
      if (trueText.match(closing) || trueText.match(doubleClosing) || trueText.match(middle)) return cx.unit * (state.currentIndent - 1);
      if (state.currentIndent < 0) return 0;
      return state.currentIndent * cx.unit;
    }
  };
}
;
const vbScript = mkVBScript({});
const vbScriptASP = mkVBScript({
  isASP: true
});

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNjg5OS5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGNvZGVtaXJyb3IvbGVnYWN5LW1vZGVzL21vZGUvdmJzY3JpcHQuanMiXSwic291cmNlc0NvbnRlbnQiOlsiZnVuY3Rpb24gbWtWQlNjcmlwdChwYXJzZXJDb25mKSB7XG4gIHZhciBFUlJPUkNMQVNTID0gJ2Vycm9yJztcbiAgZnVuY3Rpb24gd29yZFJlZ2V4cCh3b3Jkcykge1xuICAgIHJldHVybiBuZXcgUmVnRXhwKFwiXigoXCIgKyB3b3Jkcy5qb2luKFwiKXwoXCIpICsgXCIpKVxcXFxiXCIsIFwiaVwiKTtcbiAgfVxuICB2YXIgc2luZ2xlT3BlcmF0b3JzID0gbmV3IFJlZ0V4cChcIl5bXFxcXCtcXFxcLVxcXFwqLyZcXFxcXFxcXFxcXFxePD49XVwiKTtcbiAgdmFyIGRvdWJsZU9wZXJhdG9ycyA9IG5ldyBSZWdFeHAoXCJeKCg8Pil8KDw9KXwoPj0pKVwiKTtcbiAgdmFyIHNpbmdsZURlbGltaXRlcnMgPSBuZXcgUmVnRXhwKCdeW1xcXFwuLF0nKTtcbiAgdmFyIGJyYWNrZXRzID0gbmV3IFJlZ0V4cCgnXltcXFxcKFxcXFwpXScpO1xuICB2YXIgaWRlbnRpZmllcnMgPSBuZXcgUmVnRXhwKFwiXltBLVphLXpdW19BLVphLXowLTldKlwiKTtcbiAgdmFyIG9wZW5pbmdLZXl3b3JkcyA9IFsnY2xhc3MnLCAnc3ViJywgJ3NlbGVjdCcsICd3aGlsZScsICdpZicsICdmdW5jdGlvbicsICdwcm9wZXJ0eScsICd3aXRoJywgJ2ZvciddO1xuICB2YXIgbWlkZGxlS2V5d29yZHMgPSBbJ2Vsc2UnLCAnZWxzZWlmJywgJ2Nhc2UnXTtcbiAgdmFyIGVuZEtleXdvcmRzID0gWyduZXh0JywgJ2xvb3AnLCAnd2VuZCddO1xuICB2YXIgd29yZE9wZXJhdG9ycyA9IHdvcmRSZWdleHAoWydhbmQnLCAnb3InLCAnbm90JywgJ3hvcicsICdpcycsICdtb2QnLCAnZXF2JywgJ2ltcCddKTtcbiAgdmFyIGNvbW1vbmtleXdvcmRzID0gWydkaW0nLCAncmVkaW0nLCAndGhlbicsICd1bnRpbCcsICdyYW5kb21pemUnLCAnYnl2YWwnLCAnYnlyZWYnLCAnbmV3JywgJ3Byb3BlcnR5JywgJ2V4aXQnLCAnaW4nLCAnY29uc3QnLCAncHJpdmF0ZScsICdwdWJsaWMnLCAnZ2V0JywgJ3NldCcsICdsZXQnLCAnc3RvcCcsICdvbiBlcnJvciByZXN1bWUgbmV4dCcsICdvbiBlcnJvciBnb3RvIDAnLCAnb3B0aW9uIGV4cGxpY2l0JywgJ2NhbGwnLCAnbWUnXTtcblxuICAvL1RoaXMgbGlzdCB3YXMgZnJvbTogaHR0cDovL21zZG4ubWljcm9zb2Z0LmNvbS9lbi11cy9saWJyYXJ5L2Y4dGJjNzl4KHY9dnMuODQpLmFzcHhcbiAgdmFyIGF0b21Xb3JkcyA9IFsndHJ1ZScsICdmYWxzZScsICdub3RoaW5nJywgJ2VtcHR5JywgJ251bGwnXTtcbiAgLy9UaGlzIGxpc3Qgd2FzIGZyb206IGh0dHA6Ly9tc2RuLm1pY3Jvc29mdC5jb20vZW4tdXMvbGlicmFyeS8zY2E4dGZlayh2PXZzLjg0KS5hc3B4XG4gIHZhciBidWlsdGluRnVuY3NXb3JkcyA9IFsnYWJzJywgJ2FycmF5JywgJ2FzYycsICdhdG4nLCAnY2Jvb2wnLCAnY2J5dGUnLCAnY2N1cicsICdjZGF0ZScsICdjZGJsJywgJ2NocicsICdjaW50JywgJ2NsbmcnLCAnY29zJywgJ2NzbmcnLCAnY3N0cicsICdkYXRlJywgJ2RhdGVhZGQnLCAnZGF0ZWRpZmYnLCAnZGF0ZXBhcnQnLCAnZGF0ZXNlcmlhbCcsICdkYXRldmFsdWUnLCAnZGF5JywgJ2VzY2FwZScsICdldmFsJywgJ2V4ZWN1dGUnLCAnZXhwJywgJ2ZpbHRlcicsICdmb3JtYXRjdXJyZW5jeScsICdmb3JtYXRkYXRldGltZScsICdmb3JtYXRudW1iZXInLCAnZm9ybWF0cGVyY2VudCcsICdnZXRsb2NhbGUnLCAnZ2V0b2JqZWN0JywgJ2dldHJlZicsICdoZXgnLCAnaG91cicsICdpbnB1dGJveCcsICdpbnN0cicsICdpbnN0cnJldicsICdpbnQnLCAnZml4JywgJ2lzYXJyYXknLCAnaXNkYXRlJywgJ2lzZW1wdHknLCAnaXNudWxsJywgJ2lzbnVtZXJpYycsICdpc29iamVjdCcsICdqb2luJywgJ2xib3VuZCcsICdsY2FzZScsICdsZWZ0JywgJ2xlbicsICdsb2FkcGljdHVyZScsICdsb2cnLCAnbHRyaW0nLCAncnRyaW0nLCAndHJpbScsICdtYXRocycsICdtaWQnLCAnbWludXRlJywgJ21vbnRoJywgJ21vbnRobmFtZScsICdtc2dib3gnLCAnbm93JywgJ29jdCcsICdyZXBsYWNlJywgJ3JnYicsICdyaWdodCcsICdybmQnLCAncm91bmQnLCAnc2NyaXB0ZW5naW5lJywgJ3NjcmlwdGVuZ2luZWJ1aWxkdmVyc2lvbicsICdzY3JpcHRlbmdpbmVtYWpvcnZlcnNpb24nLCAnc2NyaXB0ZW5naW5lbWlub3J2ZXJzaW9uJywgJ3NlY29uZCcsICdzZXRsb2NhbGUnLCAnc2duJywgJ3NpbicsICdzcGFjZScsICdzcGxpdCcsICdzcXInLCAnc3RyY29tcCcsICdzdHJpbmcnLCAnc3RycmV2ZXJzZScsICd0YW4nLCAndGltZScsICd0aW1lcicsICd0aW1lc2VyaWFsJywgJ3RpbWV2YWx1ZScsICd0eXBlbmFtZScsICd1Ym91bmQnLCAndWNhc2UnLCAndW5lc2NhcGUnLCAndmFydHlwZScsICd3ZWVrZGF5JywgJ3dlZWtkYXluYW1lJywgJ3llYXInXTtcblxuICAvL1RoaXMgbGlzdCB3YXMgZnJvbTogaHR0cDovL21zZG4ubWljcm9zb2Z0LmNvbS9lbi11cy9saWJyYXJ5L3lkejRjZmszKHY9dnMuODQpLmFzcHhcbiAgdmFyIGJ1aWx0aW5Db25zdHMgPSBbJ3ZiQmxhY2snLCAndmJSZWQnLCAndmJHcmVlbicsICd2YlllbGxvdycsICd2YkJsdWUnLCAndmJNYWdlbnRhJywgJ3ZiQ3lhbicsICd2YldoaXRlJywgJ3ZiQmluYXJ5Q29tcGFyZScsICd2YlRleHRDb21wYXJlJywgJ3ZiU3VuZGF5JywgJ3ZiTW9uZGF5JywgJ3ZiVHVlc2RheScsICd2YldlZG5lc2RheScsICd2YlRodXJzZGF5JywgJ3ZiRnJpZGF5JywgJ3ZiU2F0dXJkYXknLCAndmJVc2VTeXN0ZW1EYXlPZldlZWsnLCAndmJGaXJzdEphbjEnLCAndmJGaXJzdEZvdXJEYXlzJywgJ3ZiRmlyc3RGdWxsV2VlaycsICd2YkdlbmVyYWxEYXRlJywgJ3ZiTG9uZ0RhdGUnLCAndmJTaG9ydERhdGUnLCAndmJMb25nVGltZScsICd2YlNob3J0VGltZScsICd2Yk9iamVjdEVycm9yJywgJ3ZiT0tPbmx5JywgJ3ZiT0tDYW5jZWwnLCAndmJBYm9ydFJldHJ5SWdub3JlJywgJ3ZiWWVzTm9DYW5jZWwnLCAndmJZZXNObycsICd2YlJldHJ5Q2FuY2VsJywgJ3ZiQ3JpdGljYWwnLCAndmJRdWVzdGlvbicsICd2YkV4Y2xhbWF0aW9uJywgJ3ZiSW5mb3JtYXRpb24nLCAndmJEZWZhdWx0QnV0dG9uMScsICd2YkRlZmF1bHRCdXR0b24yJywgJ3ZiRGVmYXVsdEJ1dHRvbjMnLCAndmJEZWZhdWx0QnV0dG9uNCcsICd2YkFwcGxpY2F0aW9uTW9kYWwnLCAndmJTeXN0ZW1Nb2RhbCcsICd2Yk9LJywgJ3ZiQ2FuY2VsJywgJ3ZiQWJvcnQnLCAndmJSZXRyeScsICd2Yklnbm9yZScsICd2YlllcycsICd2Yk5vJywgJ3ZiQ3InLCAnVmJDckxmJywgJ3ZiRm9ybUZlZWQnLCAndmJMZicsICd2Yk5ld0xpbmUnLCAndmJOdWxsQ2hhcicsICd2Yk51bGxTdHJpbmcnLCAndmJUYWInLCAndmJWZXJ0aWNhbFRhYicsICd2YlVzZURlZmF1bHQnLCAndmJUcnVlJywgJ3ZiRmFsc2UnLCAndmJFbXB0eScsICd2Yk51bGwnLCAndmJJbnRlZ2VyJywgJ3ZiTG9uZycsICd2YlNpbmdsZScsICd2YkRvdWJsZScsICd2YkN1cnJlbmN5JywgJ3ZiRGF0ZScsICd2YlN0cmluZycsICd2Yk9iamVjdCcsICd2YkVycm9yJywgJ3ZiQm9vbGVhbicsICd2YlZhcmlhbnQnLCAndmJEYXRhT2JqZWN0JywgJ3ZiRGVjaW1hbCcsICd2YkJ5dGUnLCAndmJBcnJheSddO1xuICAvL1RoaXMgbGlzdCB3YXMgZnJvbTogaHR0cDovL21zZG4ubWljcm9zb2Z0LmNvbS9lbi11cy9saWJyYXJ5L2hrYzM3NWVhKHY9dnMuODQpLmFzcHhcbiAgdmFyIGJ1aWx0aW5PYmpzV29yZHMgPSBbJ1dTY3JpcHQnLCAnZXJyJywgJ2RlYnVnJywgJ1JlZ0V4cCddO1xuICB2YXIga25vd25Qcm9wZXJ0aWVzID0gWydkZXNjcmlwdGlvbicsICdmaXJzdGluZGV4JywgJ2dsb2JhbCcsICdoZWxwY29udGV4dCcsICdoZWxwZmlsZScsICdpZ25vcmVjYXNlJywgJ2xlbmd0aCcsICdudW1iZXInLCAncGF0dGVybicsICdzb3VyY2UnLCAndmFsdWUnLCAnY291bnQnXTtcbiAgdmFyIGtub3duTWV0aG9kcyA9IFsnY2xlYXInLCAnZXhlY3V0ZScsICdyYWlzZScsICdyZXBsYWNlJywgJ3Rlc3QnLCAnd3JpdGUnLCAnd3JpdGVsaW5lJywgJ2Nsb3NlJywgJ29wZW4nLCAnc3RhdGUnLCAnZW9mJywgJ3VwZGF0ZScsICdhZGRuZXcnLCAnZW5kJywgJ2NyZWF0ZW9iamVjdCcsICdxdWl0J107XG4gIHZhciBhc3BCdWlsdGluT2Jqc1dvcmRzID0gWydzZXJ2ZXInLCAncmVzcG9uc2UnLCAncmVxdWVzdCcsICdzZXNzaW9uJywgJ2FwcGxpY2F0aW9uJ107XG4gIHZhciBhc3BLbm93blByb3BlcnRpZXMgPSBbJ2J1ZmZlcicsICdjYWNoZWNvbnRyb2wnLCAnY2hhcnNldCcsICdjb250ZW50dHlwZScsICdleHBpcmVzJywgJ2V4cGlyZXNhYnNvbHV0ZScsICdpc2NsaWVudGNvbm5lY3RlZCcsICdwaWNzJywgJ3N0YXR1cycsXG4gIC8vcmVzcG9uc2VcbiAgJ2NsaWVudGNlcnRpZmljYXRlJywgJ2Nvb2tpZXMnLCAnZm9ybScsICdxdWVyeXN0cmluZycsICdzZXJ2ZXJ2YXJpYWJsZXMnLCAndG90YWxieXRlcycsXG4gIC8vcmVxdWVzdFxuICAnY29udGVudHMnLCAnc3RhdGljb2JqZWN0cycsXG4gIC8vYXBwbGljYXRpb25cbiAgJ2NvZGVwYWdlJywgJ2xjaWQnLCAnc2Vzc2lvbmlkJywgJ3RpbWVvdXQnLFxuICAvL3Nlc3Npb25cbiAgJ3NjcmlwdHRpbWVvdXQnXTsgLy9zZXJ2ZXJcbiAgdmFyIGFzcEtub3duTWV0aG9kcyA9IFsnYWRkaGVhZGVyJywgJ2FwcGVuZHRvbG9nJywgJ2JpbmFyeXdyaXRlJywgJ2VuZCcsICdmbHVzaCcsICdyZWRpcmVjdCcsXG4gIC8vcmVzcG9uc2VcbiAgJ2JpbmFyeXJlYWQnLFxuICAvL3JlcXVlc3RcbiAgJ3JlbW92ZScsICdyZW1vdmVhbGwnLCAnbG9jaycsICd1bmxvY2snLFxuICAvL2FwcGxpY2F0aW9uXG4gICdhYmFuZG9uJyxcbiAgLy9zZXNzaW9uXG4gICdnZXRsYXN0ZXJyb3InLCAnaHRtbGVuY29kZScsICdtYXBwYXRoJywgJ3RyYW5zZmVyJywgJ3VybGVuY29kZSddOyAvL3NlcnZlclxuXG4gIHZhciBrbm93bldvcmRzID0ga25vd25NZXRob2RzLmNvbmNhdChrbm93blByb3BlcnRpZXMpO1xuICBidWlsdGluT2Jqc1dvcmRzID0gYnVpbHRpbk9ianNXb3Jkcy5jb25jYXQoYnVpbHRpbkNvbnN0cyk7XG4gIGlmIChwYXJzZXJDb25mLmlzQVNQKSB7XG4gICAgYnVpbHRpbk9ianNXb3JkcyA9IGJ1aWx0aW5PYmpzV29yZHMuY29uY2F0KGFzcEJ1aWx0aW5PYmpzV29yZHMpO1xuICAgIGtub3duV29yZHMgPSBrbm93bldvcmRzLmNvbmNhdChhc3BLbm93bk1ldGhvZHMsIGFzcEtub3duUHJvcGVydGllcyk7XG4gIH1cbiAgO1xuICB2YXIga2V5d29yZHMgPSB3b3JkUmVnZXhwKGNvbW1vbmtleXdvcmRzKTtcbiAgdmFyIGF0b21zID0gd29yZFJlZ2V4cChhdG9tV29yZHMpO1xuICB2YXIgYnVpbHRpbkZ1bmNzID0gd29yZFJlZ2V4cChidWlsdGluRnVuY3NXb3Jkcyk7XG4gIHZhciBidWlsdGluT2JqcyA9IHdvcmRSZWdleHAoYnVpbHRpbk9ianNXb3Jkcyk7XG4gIHZhciBrbm93biA9IHdvcmRSZWdleHAoa25vd25Xb3Jkcyk7XG4gIHZhciBzdHJpbmdQcmVmaXhlcyA9ICdcIic7XG4gIHZhciBvcGVuaW5nID0gd29yZFJlZ2V4cChvcGVuaW5nS2V5d29yZHMpO1xuICB2YXIgbWlkZGxlID0gd29yZFJlZ2V4cChtaWRkbGVLZXl3b3Jkcyk7XG4gIHZhciBjbG9zaW5nID0gd29yZFJlZ2V4cChlbmRLZXl3b3Jkcyk7XG4gIHZhciBkb3VibGVDbG9zaW5nID0gd29yZFJlZ2V4cChbJ2VuZCddKTtcbiAgdmFyIGRvT3BlbmluZyA9IHdvcmRSZWdleHAoWydkbyddKTtcbiAgdmFyIG5vSW5kZW50V29yZHMgPSB3b3JkUmVnZXhwKFsnb24gZXJyb3IgcmVzdW1lIG5leHQnLCAnZXhpdCddKTtcbiAgdmFyIGNvbW1lbnQgPSB3b3JkUmVnZXhwKFsncmVtJ10pO1xuICBmdW5jdGlvbiBpbmRlbnQoX3N0cmVhbSwgc3RhdGUpIHtcbiAgICBzdGF0ZS5jdXJyZW50SW5kZW50Kys7XG4gIH1cbiAgZnVuY3Rpb24gZGVkZW50KF9zdHJlYW0sIHN0YXRlKSB7XG4gICAgc3RhdGUuY3VycmVudEluZGVudC0tO1xuICB9XG4gIC8vIHRva2VuaXplcnNcbiAgZnVuY3Rpb24gdG9rZW5CYXNlKHN0cmVhbSwgc3RhdGUpIHtcbiAgICBpZiAoc3RyZWFtLmVhdFNwYWNlKCkpIHtcbiAgICAgIHJldHVybiBudWxsO1xuICAgICAgLy9yZXR1cm4gbnVsbDtcbiAgICB9XG4gICAgdmFyIGNoID0gc3RyZWFtLnBlZWsoKTtcblxuICAgIC8vIEhhbmRsZSBDb21tZW50c1xuICAgIGlmIChjaCA9PT0gXCInXCIpIHtcbiAgICAgIHN0cmVhbS5za2lwVG9FbmQoKTtcbiAgICAgIHJldHVybiAnY29tbWVudCc7XG4gICAgfVxuICAgIGlmIChzdHJlYW0ubWF0Y2goY29tbWVudCkpIHtcbiAgICAgIHN0cmVhbS5za2lwVG9FbmQoKTtcbiAgICAgIHJldHVybiAnY29tbWVudCc7XG4gICAgfVxuXG4gICAgLy8gSGFuZGxlIE51bWJlciBMaXRlcmFsc1xuICAgIGlmIChzdHJlYW0ubWF0Y2goL14oKCZIKXwoJk8pKT9bMC05XFwuXS9pLCBmYWxzZSkgJiYgIXN0cmVhbS5tYXRjaCgvXigoJkgpfCgmTykpP1swLTlcXC5dK1thLXpfXS9pLCBmYWxzZSkpIHtcbiAgICAgIHZhciBmbG9hdExpdGVyYWwgPSBmYWxzZTtcbiAgICAgIC8vIEZsb2F0c1xuICAgICAgaWYgKHN0cmVhbS5tYXRjaCgvXlxcZCpcXC5cXGQrL2kpKSB7XG4gICAgICAgIGZsb2F0TGl0ZXJhbCA9IHRydWU7XG4gICAgICB9IGVsc2UgaWYgKHN0cmVhbS5tYXRjaCgvXlxcZCtcXC5cXGQqLykpIHtcbiAgICAgICAgZmxvYXRMaXRlcmFsID0gdHJ1ZTtcbiAgICAgIH0gZWxzZSBpZiAoc3RyZWFtLm1hdGNoKC9eXFwuXFxkKy8pKSB7XG4gICAgICAgIGZsb2F0TGl0ZXJhbCA9IHRydWU7XG4gICAgICB9XG4gICAgICBpZiAoZmxvYXRMaXRlcmFsKSB7XG4gICAgICAgIC8vIEZsb2F0IGxpdGVyYWxzIG1heSBiZSBcImltYWdpbmFyeVwiXG4gICAgICAgIHN0cmVhbS5lYXQoL0ovaSk7XG4gICAgICAgIHJldHVybiAnbnVtYmVyJztcbiAgICAgIH1cbiAgICAgIC8vIEludGVnZXJzXG4gICAgICB2YXIgaW50TGl0ZXJhbCA9IGZhbHNlO1xuICAgICAgLy8gSGV4XG4gICAgICBpZiAoc3RyZWFtLm1hdGNoKC9eJkhbMC05YS1mXSsvaSkpIHtcbiAgICAgICAgaW50TGl0ZXJhbCA9IHRydWU7XG4gICAgICB9XG4gICAgICAvLyBPY3RhbFxuICAgICAgZWxzZSBpZiAoc3RyZWFtLm1hdGNoKC9eJk9bMC03XSsvaSkpIHtcbiAgICAgICAgaW50TGl0ZXJhbCA9IHRydWU7XG4gICAgICB9XG4gICAgICAvLyBEZWNpbWFsXG4gICAgICBlbHNlIGlmIChzdHJlYW0ubWF0Y2goL15bMS05XVxcZCpGPy8pKSB7XG4gICAgICAgIC8vIERlY2ltYWwgbGl0ZXJhbHMgbWF5IGJlIFwiaW1hZ2luYXJ5XCJcbiAgICAgICAgc3RyZWFtLmVhdCgvSi9pKTtcbiAgICAgICAgLy8gVE9ETyAtIENhbiB5b3UgaGF2ZSBpbWFnaW5hcnkgbG9uZ3M/XG4gICAgICAgIGludExpdGVyYWwgPSB0cnVlO1xuICAgICAgfVxuICAgICAgLy8gWmVybyBieSBpdHNlbGYgd2l0aCBubyBvdGhlciBwaWVjZSBvZiBudW1iZXIuXG4gICAgICBlbHNlIGlmIChzdHJlYW0ubWF0Y2goL14wKD8hW1xcZHhdKS9pKSkge1xuICAgICAgICBpbnRMaXRlcmFsID0gdHJ1ZTtcbiAgICAgIH1cbiAgICAgIGlmIChpbnRMaXRlcmFsKSB7XG4gICAgICAgIC8vIEludGVnZXIgbGl0ZXJhbHMgbWF5IGJlIFwibG9uZ1wiXG4gICAgICAgIHN0cmVhbS5lYXQoL0wvaSk7XG4gICAgICAgIHJldHVybiAnbnVtYmVyJztcbiAgICAgIH1cbiAgICB9XG5cbiAgICAvLyBIYW5kbGUgU3RyaW5nc1xuICAgIGlmIChzdHJlYW0ubWF0Y2goc3RyaW5nUHJlZml4ZXMpKSB7XG4gICAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuU3RyaW5nRmFjdG9yeShzdHJlYW0uY3VycmVudCgpKTtcbiAgICAgIHJldHVybiBzdGF0ZS50b2tlbml6ZShzdHJlYW0sIHN0YXRlKTtcbiAgICB9XG5cbiAgICAvLyBIYW5kbGUgb3BlcmF0b3JzIGFuZCBEZWxpbWl0ZXJzXG4gICAgaWYgKHN0cmVhbS5tYXRjaChkb3VibGVPcGVyYXRvcnMpIHx8IHN0cmVhbS5tYXRjaChzaW5nbGVPcGVyYXRvcnMpIHx8IHN0cmVhbS5tYXRjaCh3b3JkT3BlcmF0b3JzKSkge1xuICAgICAgcmV0dXJuICdvcGVyYXRvcic7XG4gICAgfVxuICAgIGlmIChzdHJlYW0ubWF0Y2goc2luZ2xlRGVsaW1pdGVycykpIHtcbiAgICAgIHJldHVybiBudWxsO1xuICAgIH1cbiAgICBpZiAoc3RyZWFtLm1hdGNoKGJyYWNrZXRzKSkge1xuICAgICAgcmV0dXJuIFwiYnJhY2tldFwiO1xuICAgIH1cbiAgICBpZiAoc3RyZWFtLm1hdGNoKG5vSW5kZW50V29yZHMpKSB7XG4gICAgICBzdGF0ZS5kb0luQ3VycmVudExpbmUgPSB0cnVlO1xuICAgICAgcmV0dXJuICdrZXl3b3JkJztcbiAgICB9XG4gICAgaWYgKHN0cmVhbS5tYXRjaChkb09wZW5pbmcpKSB7XG4gICAgICBpbmRlbnQoc3RyZWFtLCBzdGF0ZSk7XG4gICAgICBzdGF0ZS5kb0luQ3VycmVudExpbmUgPSB0cnVlO1xuICAgICAgcmV0dXJuICdrZXl3b3JkJztcbiAgICB9XG4gICAgaWYgKHN0cmVhbS5tYXRjaChvcGVuaW5nKSkge1xuICAgICAgaWYgKCFzdGF0ZS5kb0luQ3VycmVudExpbmUpIGluZGVudChzdHJlYW0sIHN0YXRlKTtlbHNlIHN0YXRlLmRvSW5DdXJyZW50TGluZSA9IGZhbHNlO1xuICAgICAgcmV0dXJuICdrZXl3b3JkJztcbiAgICB9XG4gICAgaWYgKHN0cmVhbS5tYXRjaChtaWRkbGUpKSB7XG4gICAgICByZXR1cm4gJ2tleXdvcmQnO1xuICAgIH1cbiAgICBpZiAoc3RyZWFtLm1hdGNoKGRvdWJsZUNsb3NpbmcpKSB7XG4gICAgICBkZWRlbnQoc3RyZWFtLCBzdGF0ZSk7XG4gICAgICBkZWRlbnQoc3RyZWFtLCBzdGF0ZSk7XG4gICAgICByZXR1cm4gJ2tleXdvcmQnO1xuICAgIH1cbiAgICBpZiAoc3RyZWFtLm1hdGNoKGNsb3NpbmcpKSB7XG4gICAgICBpZiAoIXN0YXRlLmRvSW5DdXJyZW50TGluZSkgZGVkZW50KHN0cmVhbSwgc3RhdGUpO2Vsc2Ugc3RhdGUuZG9JbkN1cnJlbnRMaW5lID0gZmFsc2U7XG4gICAgICByZXR1cm4gJ2tleXdvcmQnO1xuICAgIH1cbiAgICBpZiAoc3RyZWFtLm1hdGNoKGtleXdvcmRzKSkge1xuICAgICAgcmV0dXJuICdrZXl3b3JkJztcbiAgICB9XG4gICAgaWYgKHN0cmVhbS5tYXRjaChhdG9tcykpIHtcbiAgICAgIHJldHVybiAnYXRvbSc7XG4gICAgfVxuICAgIGlmIChzdHJlYW0ubWF0Y2goa25vd24pKSB7XG4gICAgICByZXR1cm4gJ3ZhcmlhYmxlTmFtZS5zcGVjaWFsJztcbiAgICB9XG4gICAgaWYgKHN0cmVhbS5tYXRjaChidWlsdGluRnVuY3MpKSB7XG4gICAgICByZXR1cm4gJ2J1aWx0aW4nO1xuICAgIH1cbiAgICBpZiAoc3RyZWFtLm1hdGNoKGJ1aWx0aW5PYmpzKSkge1xuICAgICAgcmV0dXJuICdidWlsdGluJztcbiAgICB9XG4gICAgaWYgKHN0cmVhbS5tYXRjaChpZGVudGlmaWVycykpIHtcbiAgICAgIHJldHVybiAndmFyaWFibGUnO1xuICAgIH1cblxuICAgIC8vIEhhbmRsZSBub24tZGV0ZWN0ZWQgaXRlbXNcbiAgICBzdHJlYW0ubmV4dCgpO1xuICAgIHJldHVybiBFUlJPUkNMQVNTO1xuICB9XG4gIGZ1bmN0aW9uIHRva2VuU3RyaW5nRmFjdG9yeShkZWxpbWl0ZXIpIHtcbiAgICB2YXIgc2luZ2xlbGluZSA9IGRlbGltaXRlci5sZW5ndGggPT0gMTtcbiAgICB2YXIgT1VUQ0xBU1MgPSAnc3RyaW5nJztcbiAgICByZXR1cm4gZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICAgIHdoaWxlICghc3RyZWFtLmVvbCgpKSB7XG4gICAgICAgIHN0cmVhbS5lYXRXaGlsZSgvW14nXCJdLyk7XG4gICAgICAgIGlmIChzdHJlYW0ubWF0Y2goZGVsaW1pdGVyKSkge1xuICAgICAgICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlO1xuICAgICAgICAgIHJldHVybiBPVVRDTEFTUztcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICBzdHJlYW0uZWF0KC9bJ1wiXS8pO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgICBpZiAoc2luZ2xlbGluZSkge1xuICAgICAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQmFzZTtcbiAgICAgIH1cbiAgICAgIHJldHVybiBPVVRDTEFTUztcbiAgICB9O1xuICB9XG4gIGZ1bmN0aW9uIHRva2VuTGV4ZXIoc3RyZWFtLCBzdGF0ZSkge1xuICAgIHZhciBzdHlsZSA9IHN0YXRlLnRva2VuaXplKHN0cmVhbSwgc3RhdGUpO1xuICAgIHZhciBjdXJyZW50ID0gc3RyZWFtLmN1cnJlbnQoKTtcblxuICAgIC8vIEhhbmRsZSAnLicgY29ubmVjdGVkIGlkZW50aWZpZXJzXG4gICAgaWYgKGN1cnJlbnQgPT09ICcuJykge1xuICAgICAgc3R5bGUgPSBzdGF0ZS50b2tlbml6ZShzdHJlYW0sIHN0YXRlKTtcbiAgICAgIGN1cnJlbnQgPSBzdHJlYW0uY3VycmVudCgpO1xuICAgICAgaWYgKHN0eWxlICYmIChzdHlsZS5zdWJzdHIoMCwgOCkgPT09ICd2YXJpYWJsZScgfHwgc3R5bGUgPT09ICdidWlsdGluJyB8fCBzdHlsZSA9PT0gJ2tleXdvcmQnKSkge1xuICAgICAgICAvL3x8IGtub3duV29yZHMuaW5kZXhPZihjdXJyZW50LnN1YnN0cmluZygxKSkgPiAtMSkge1xuICAgICAgICBpZiAoc3R5bGUgPT09ICdidWlsdGluJyB8fCBzdHlsZSA9PT0gJ2tleXdvcmQnKSBzdHlsZSA9ICd2YXJpYWJsZSc7XG4gICAgICAgIGlmIChrbm93bldvcmRzLmluZGV4T2YoY3VycmVudC5zdWJzdHIoMSkpID4gLTEpIHN0eWxlID0gJ2tleXdvcmQnO1xuICAgICAgICByZXR1cm4gc3R5bGU7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICByZXR1cm4gRVJST1JDTEFTUztcbiAgICAgIH1cbiAgICB9XG4gICAgcmV0dXJuIHN0eWxlO1xuICB9XG4gIHJldHVybiB7XG4gICAgbmFtZTogXCJ2YnNjcmlwdFwiLFxuICAgIHN0YXJ0U3RhdGU6IGZ1bmN0aW9uICgpIHtcbiAgICAgIHJldHVybiB7XG4gICAgICAgIHRva2VuaXplOiB0b2tlbkJhc2UsXG4gICAgICAgIGxhc3RUb2tlbjogbnVsbCxcbiAgICAgICAgY3VycmVudEluZGVudDogMCxcbiAgICAgICAgbmV4dExpbmVJbmRlbnQ6IDAsXG4gICAgICAgIGRvSW5DdXJyZW50TGluZTogZmFsc2UsXG4gICAgICAgIGlnbm9yZUtleXdvcmQ6IGZhbHNlXG4gICAgICB9O1xuICAgIH0sXG4gICAgdG9rZW46IGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgICBpZiAoc3RyZWFtLnNvbCgpKSB7XG4gICAgICAgIHN0YXRlLmN1cnJlbnRJbmRlbnQgKz0gc3RhdGUubmV4dExpbmVJbmRlbnQ7XG4gICAgICAgIHN0YXRlLm5leHRMaW5lSW5kZW50ID0gMDtcbiAgICAgICAgc3RhdGUuZG9JbkN1cnJlbnRMaW5lID0gMDtcbiAgICAgIH1cbiAgICAgIHZhciBzdHlsZSA9IHRva2VuTGV4ZXIoc3RyZWFtLCBzdGF0ZSk7XG4gICAgICBzdGF0ZS5sYXN0VG9rZW4gPSB7XG4gICAgICAgIHN0eWxlOiBzdHlsZSxcbiAgICAgICAgY29udGVudDogc3RyZWFtLmN1cnJlbnQoKVxuICAgICAgfTtcbiAgICAgIGlmIChzdHlsZSA9PT0gbnVsbCkgc3R5bGUgPSBudWxsO1xuICAgICAgcmV0dXJuIHN0eWxlO1xuICAgIH0sXG4gICAgaW5kZW50OiBmdW5jdGlvbiAoc3RhdGUsIHRleHRBZnRlciwgY3gpIHtcbiAgICAgIHZhciB0cnVlVGV4dCA9IHRleHRBZnRlci5yZXBsYWNlKC9eXFxzK3xcXHMrJC9nLCAnJyk7XG4gICAgICBpZiAodHJ1ZVRleHQubWF0Y2goY2xvc2luZykgfHwgdHJ1ZVRleHQubWF0Y2goZG91YmxlQ2xvc2luZykgfHwgdHJ1ZVRleHQubWF0Y2gobWlkZGxlKSkgcmV0dXJuIGN4LnVuaXQgKiAoc3RhdGUuY3VycmVudEluZGVudCAtIDEpO1xuICAgICAgaWYgKHN0YXRlLmN1cnJlbnRJbmRlbnQgPCAwKSByZXR1cm4gMDtcbiAgICAgIHJldHVybiBzdGF0ZS5jdXJyZW50SW5kZW50ICogY3gudW5pdDtcbiAgICB9XG4gIH07XG59XG47XG5leHBvcnQgY29uc3QgdmJTY3JpcHQgPSBta1ZCU2NyaXB0KHt9KTtcbmV4cG9ydCBjb25zdCB2YlNjcmlwdEFTUCA9IG1rVkJTY3JpcHQoe1xuICBpc0FTUDogdHJ1ZVxufSk7Il0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9