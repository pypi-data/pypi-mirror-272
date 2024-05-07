"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[7094],{

/***/ 47094:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "scheme": () => (/* binding */ scheme)
/* harmony export */ });
var BUILTIN = "builtin",
  COMMENT = "comment",
  STRING = "string",
  SYMBOL = "symbol",
  ATOM = "atom",
  NUMBER = "number",
  BRACKET = "bracket";
var INDENT_WORD_SKIP = 2;
function makeKeywords(str) {
  var obj = {},
    words = str.split(" ");
  for (var i = 0; i < words.length; ++i) obj[words[i]] = true;
  return obj;
}
var keywords = makeKeywords("λ case-lambda call/cc class cond-expand define-class define-values exit-handler field import inherit init-field interface let*-values let-values let/ec mixin opt-lambda override protect provide public rename require require-for-syntax syntax syntax-case syntax-error unit/sig unless when with-syntax and begin call-with-current-continuation call-with-input-file call-with-output-file case cond define define-syntax define-macro defmacro delay do dynamic-wind else for-each if lambda let let* let-syntax letrec letrec-syntax map or syntax-rules abs acos angle append apply asin assoc assq assv atan boolean? caar cadr call-with-input-file call-with-output-file call-with-values car cdddar cddddr cdr ceiling char->integer char-alphabetic? char-ci<=? char-ci<? char-ci=? char-ci>=? char-ci>? char-downcase char-lower-case? char-numeric? char-ready? char-upcase char-upper-case? char-whitespace? char<=? char<? char=? char>=? char>? char? close-input-port close-output-port complex? cons cos current-input-port current-output-port denominator display eof-object? eq? equal? eqv? eval even? exact->inexact exact? exp expt #f floor force gcd imag-part inexact->exact inexact? input-port? integer->char integer? interaction-environment lcm length list list->string list->vector list-ref list-tail list? load log magnitude make-polar make-rectangular make-string make-vector max member memq memv min modulo negative? newline not null-environment null? number->string number? numerator odd? open-input-file open-output-file output-port? pair? peek-char port? positive? procedure? quasiquote quote quotient rational? rationalize read read-char real-part real? remainder reverse round scheme-report-environment set! set-car! set-cdr! sin sqrt string string->list string->number string->symbol string-append string-ci<=? string-ci<? string-ci=? string-ci>=? string-ci>? string-copy string-fill! string-length string-ref string-set! string<=? string<? string=? string>=? string>? string? substring symbol->string symbol? #t tan transcript-off transcript-on truncate values vector vector->list vector-fill! vector-length vector-ref vector-set! with-input-from-file with-output-to-file write write-char zero?");
var indentKeys = makeKeywords("define let letrec let* lambda define-macro defmacro let-syntax letrec-syntax let-values let*-values define-syntax syntax-rules define-values when unless");
function stateStack(indent, type, prev) {
  // represents a state stack object
  this.indent = indent;
  this.type = type;
  this.prev = prev;
}
function pushStack(state, indent, type) {
  state.indentStack = new stateStack(indent, type, state.indentStack);
}
function popStack(state) {
  state.indentStack = state.indentStack.prev;
}
var binaryMatcher = new RegExp(/^(?:[-+]i|[-+][01]+#*(?:\/[01]+#*)?i|[-+]?[01]+#*(?:\/[01]+#*)?@[-+]?[01]+#*(?:\/[01]+#*)?|[-+]?[01]+#*(?:\/[01]+#*)?[-+](?:[01]+#*(?:\/[01]+#*)?)?i|[-+]?[01]+#*(?:\/[01]+#*)?)(?=[()\s;"]|$)/i);
var octalMatcher = new RegExp(/^(?:[-+]i|[-+][0-7]+#*(?:\/[0-7]+#*)?i|[-+]?[0-7]+#*(?:\/[0-7]+#*)?@[-+]?[0-7]+#*(?:\/[0-7]+#*)?|[-+]?[0-7]+#*(?:\/[0-7]+#*)?[-+](?:[0-7]+#*(?:\/[0-7]+#*)?)?i|[-+]?[0-7]+#*(?:\/[0-7]+#*)?)(?=[()\s;"]|$)/i);
var hexMatcher = new RegExp(/^(?:[-+]i|[-+][\da-f]+#*(?:\/[\da-f]+#*)?i|[-+]?[\da-f]+#*(?:\/[\da-f]+#*)?@[-+]?[\da-f]+#*(?:\/[\da-f]+#*)?|[-+]?[\da-f]+#*(?:\/[\da-f]+#*)?[-+](?:[\da-f]+#*(?:\/[\da-f]+#*)?)?i|[-+]?[\da-f]+#*(?:\/[\da-f]+#*)?)(?=[()\s;"]|$)/i);
var decimalMatcher = new RegExp(/^(?:[-+]i|[-+](?:(?:(?:\d+#+\.?#*|\d+\.\d*#*|\.\d+#*|\d+)(?:[esfdl][-+]?\d+)?)|\d+#*\/\d+#*)i|[-+]?(?:(?:(?:\d+#+\.?#*|\d+\.\d*#*|\.\d+#*|\d+)(?:[esfdl][-+]?\d+)?)|\d+#*\/\d+#*)@[-+]?(?:(?:(?:\d+#+\.?#*|\d+\.\d*#*|\.\d+#*|\d+)(?:[esfdl][-+]?\d+)?)|\d+#*\/\d+#*)|[-+]?(?:(?:(?:\d+#+\.?#*|\d+\.\d*#*|\.\d+#*|\d+)(?:[esfdl][-+]?\d+)?)|\d+#*\/\d+#*)[-+](?:(?:(?:\d+#+\.?#*|\d+\.\d*#*|\.\d+#*|\d+)(?:[esfdl][-+]?\d+)?)|\d+#*\/\d+#*)?i|(?:(?:(?:\d+#+\.?#*|\d+\.\d*#*|\.\d+#*|\d+)(?:[esfdl][-+]?\d+)?)|\d+#*\/\d+#*))(?=[()\s;"]|$)/i);
function isBinaryNumber(stream) {
  return stream.match(binaryMatcher);
}
function isOctalNumber(stream) {
  return stream.match(octalMatcher);
}
function isDecimalNumber(stream, backup) {
  if (backup === true) {
    stream.backUp(1);
  }
  return stream.match(decimalMatcher);
}
function isHexNumber(stream) {
  return stream.match(hexMatcher);
}
function processEscapedSequence(stream, options) {
  var next,
    escaped = false;
  while ((next = stream.next()) != null) {
    if (next == options.token && !escaped) {
      options.state.mode = false;
      break;
    }
    escaped = !escaped && next == "\\";
  }
}
const scheme = {
  name: "scheme",
  startState: function () {
    return {
      indentStack: null,
      indentation: 0,
      mode: false,
      sExprComment: false,
      sExprQuote: false
    };
  },
  token: function (stream, state) {
    if (state.indentStack == null && stream.sol()) {
      // update indentation, but only if indentStack is empty
      state.indentation = stream.indentation();
    }

    // skip spaces
    if (stream.eatSpace()) {
      return null;
    }
    var returnType = null;
    switch (state.mode) {
      case "string":
        // multi-line string parsing mode
        processEscapedSequence(stream, {
          token: "\"",
          state: state
        });
        returnType = STRING; // continue on in scheme-string mode
        break;
      case "symbol":
        // escape symbol
        processEscapedSequence(stream, {
          token: "|",
          state: state
        });
        returnType = SYMBOL; // continue on in scheme-symbol mode
        break;
      case "comment":
        // comment parsing mode
        var next,
          maybeEnd = false;
        while ((next = stream.next()) != null) {
          if (next == "#" && maybeEnd) {
            state.mode = false;
            break;
          }
          maybeEnd = next == "|";
        }
        returnType = COMMENT;
        break;
      case "s-expr-comment":
        // s-expr commenting mode
        state.mode = false;
        if (stream.peek() == "(" || stream.peek() == "[") {
          // actually start scheme s-expr commenting mode
          state.sExprComment = 0;
        } else {
          // if not we just comment the entire of the next token
          stream.eatWhile(/[^\s\(\)\[\]]/); // eat symbol atom
          returnType = COMMENT;
          break;
        }
      default:
        // default parsing mode
        var ch = stream.next();
        if (ch == "\"") {
          state.mode = "string";
          returnType = STRING;
        } else if (ch == "'") {
          if (stream.peek() == "(" || stream.peek() == "[") {
            if (typeof state.sExprQuote != "number") {
              state.sExprQuote = 0;
            } // else already in a quoted expression
            returnType = ATOM;
          } else {
            stream.eatWhile(/[\w_\-!$%&*+\.\/:<=>?@\^~]/);
            returnType = ATOM;
          }
        } else if (ch == '|') {
          state.mode = "symbol";
          returnType = SYMBOL;
        } else if (ch == '#') {
          if (stream.eat("|")) {
            // Multi-line comment
            state.mode = "comment"; // toggle to comment mode
            returnType = COMMENT;
          } else if (stream.eat(/[tf]/i)) {
            // #t/#f (atom)
            returnType = ATOM;
          } else if (stream.eat(';')) {
            // S-Expr comment
            state.mode = "s-expr-comment";
            returnType = COMMENT;
          } else {
            var numTest = null,
              hasExactness = false,
              hasRadix = true;
            if (stream.eat(/[ei]/i)) {
              hasExactness = true;
            } else {
              stream.backUp(1); // must be radix specifier
            }
            if (stream.match(/^#b/i)) {
              numTest = isBinaryNumber;
            } else if (stream.match(/^#o/i)) {
              numTest = isOctalNumber;
            } else if (stream.match(/^#x/i)) {
              numTest = isHexNumber;
            } else if (stream.match(/^#d/i)) {
              numTest = isDecimalNumber;
            } else if (stream.match(/^[-+0-9.]/, false)) {
              hasRadix = false;
              numTest = isDecimalNumber;
              // re-consume the initial # if all matches failed
            } else if (!hasExactness) {
              stream.eat('#');
            }
            if (numTest != null) {
              if (hasRadix && !hasExactness) {
                // consume optional exactness after radix
                stream.match(/^#[ei]/i);
              }
              if (numTest(stream)) returnType = NUMBER;
            }
          }
        } else if (/^[-+0-9.]/.test(ch) && isDecimalNumber(stream, true)) {
          // match non-prefixed number, must be decimal
          returnType = NUMBER;
        } else if (ch == ";") {
          // comment
          stream.skipToEnd(); // rest of the line is a comment
          returnType = COMMENT;
        } else if (ch == "(" || ch == "[") {
          var keyWord = '';
          var indentTemp = stream.column(),
            letter;
          /**
             Either
             (indent-word ..
             (non-indent-word ..
             (;something else, bracket, etc.
          */

          while ((letter = stream.eat(/[^\s\(\[\;\)\]]/)) != null) {
            keyWord += letter;
          }
          if (keyWord.length > 0 && indentKeys.propertyIsEnumerable(keyWord)) {
            // indent-word

            pushStack(state, indentTemp + INDENT_WORD_SKIP, ch);
          } else {
            // non-indent word
            // we continue eating the spaces
            stream.eatSpace();
            if (stream.eol() || stream.peek() == ";") {
              // nothing significant after
              // we restart indentation 1 space after
              pushStack(state, indentTemp + 1, ch);
            } else {
              pushStack(state, indentTemp + stream.current().length, ch); // else we match
            }
          }
          stream.backUp(stream.current().length - 1); // undo all the eating

          if (typeof state.sExprComment == "number") state.sExprComment++;
          if (typeof state.sExprQuote == "number") state.sExprQuote++;
          returnType = BRACKET;
        } else if (ch == ")" || ch == "]") {
          returnType = BRACKET;
          if (state.indentStack != null && state.indentStack.type == (ch == ")" ? "(" : "[")) {
            popStack(state);
            if (typeof state.sExprComment == "number") {
              if (--state.sExprComment == 0) {
                returnType = COMMENT; // final closing bracket
                state.sExprComment = false; // turn off s-expr commenting mode
              }
            }
            if (typeof state.sExprQuote == "number") {
              if (--state.sExprQuote == 0) {
                returnType = ATOM; // final closing bracket
                state.sExprQuote = false; // turn off s-expr quote mode
              }
            }
          }
        } else {
          stream.eatWhile(/[\w_\-!$%&*+\.\/:<=>?@\^~]/);
          if (keywords && keywords.propertyIsEnumerable(stream.current())) {
            returnType = BUILTIN;
          } else returnType = "variable";
        }
    }
    return typeof state.sExprComment == "number" ? COMMENT : typeof state.sExprQuote == "number" ? ATOM : returnType;
  },
  indent: function (state) {
    if (state.indentStack == null) return state.indentation;
    return state.indentStack.indent;
  },
  languageData: {
    closeBrackets: {
      brackets: ["(", "[", "{", '"']
    },
    commentTokens: {
      line: ";;"
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNzA5NC5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGNvZGVtaXJyb3IvbGVnYWN5LW1vZGVzL21vZGUvc2NoZW1lLmpzIl0sInNvdXJjZXNDb250ZW50IjpbInZhciBCVUlMVElOID0gXCJidWlsdGluXCIsXG4gIENPTU1FTlQgPSBcImNvbW1lbnRcIixcbiAgU1RSSU5HID0gXCJzdHJpbmdcIixcbiAgU1lNQk9MID0gXCJzeW1ib2xcIixcbiAgQVRPTSA9IFwiYXRvbVwiLFxuICBOVU1CRVIgPSBcIm51bWJlclwiLFxuICBCUkFDS0VUID0gXCJicmFja2V0XCI7XG52YXIgSU5ERU5UX1dPUkRfU0tJUCA9IDI7XG5mdW5jdGlvbiBtYWtlS2V5d29yZHMoc3RyKSB7XG4gIHZhciBvYmogPSB7fSxcbiAgICB3b3JkcyA9IHN0ci5zcGxpdChcIiBcIik7XG4gIGZvciAodmFyIGkgPSAwOyBpIDwgd29yZHMubGVuZ3RoOyArK2kpIG9ialt3b3Jkc1tpXV0gPSB0cnVlO1xuICByZXR1cm4gb2JqO1xufVxudmFyIGtleXdvcmRzID0gbWFrZUtleXdvcmRzKFwizrsgY2FzZS1sYW1iZGEgY2FsbC9jYyBjbGFzcyBjb25kLWV4cGFuZCBkZWZpbmUtY2xhc3MgZGVmaW5lLXZhbHVlcyBleGl0LWhhbmRsZXIgZmllbGQgaW1wb3J0IGluaGVyaXQgaW5pdC1maWVsZCBpbnRlcmZhY2UgbGV0Ki12YWx1ZXMgbGV0LXZhbHVlcyBsZXQvZWMgbWl4aW4gb3B0LWxhbWJkYSBvdmVycmlkZSBwcm90ZWN0IHByb3ZpZGUgcHVibGljIHJlbmFtZSByZXF1aXJlIHJlcXVpcmUtZm9yLXN5bnRheCBzeW50YXggc3ludGF4LWNhc2Ugc3ludGF4LWVycm9yIHVuaXQvc2lnIHVubGVzcyB3aGVuIHdpdGgtc3ludGF4IGFuZCBiZWdpbiBjYWxsLXdpdGgtY3VycmVudC1jb250aW51YXRpb24gY2FsbC13aXRoLWlucHV0LWZpbGUgY2FsbC13aXRoLW91dHB1dC1maWxlIGNhc2UgY29uZCBkZWZpbmUgZGVmaW5lLXN5bnRheCBkZWZpbmUtbWFjcm8gZGVmbWFjcm8gZGVsYXkgZG8gZHluYW1pYy13aW5kIGVsc2UgZm9yLWVhY2ggaWYgbGFtYmRhIGxldCBsZXQqIGxldC1zeW50YXggbGV0cmVjIGxldHJlYy1zeW50YXggbWFwIG9yIHN5bnRheC1ydWxlcyBhYnMgYWNvcyBhbmdsZSBhcHBlbmQgYXBwbHkgYXNpbiBhc3NvYyBhc3NxIGFzc3YgYXRhbiBib29sZWFuPyBjYWFyIGNhZHIgY2FsbC13aXRoLWlucHV0LWZpbGUgY2FsbC13aXRoLW91dHB1dC1maWxlIGNhbGwtd2l0aC12YWx1ZXMgY2FyIGNkZGRhciBjZGRkZHIgY2RyIGNlaWxpbmcgY2hhci0+aW50ZWdlciBjaGFyLWFscGhhYmV0aWM/IGNoYXItY2k8PT8gY2hhci1jaTw/IGNoYXItY2k9PyBjaGFyLWNpPj0/IGNoYXItY2k+PyBjaGFyLWRvd25jYXNlIGNoYXItbG93ZXItY2FzZT8gY2hhci1udW1lcmljPyBjaGFyLXJlYWR5PyBjaGFyLXVwY2FzZSBjaGFyLXVwcGVyLWNhc2U/IGNoYXItd2hpdGVzcGFjZT8gY2hhcjw9PyBjaGFyPD8gY2hhcj0/IGNoYXI+PT8gY2hhcj4/IGNoYXI/IGNsb3NlLWlucHV0LXBvcnQgY2xvc2Utb3V0cHV0LXBvcnQgY29tcGxleD8gY29ucyBjb3MgY3VycmVudC1pbnB1dC1wb3J0IGN1cnJlbnQtb3V0cHV0LXBvcnQgZGVub21pbmF0b3IgZGlzcGxheSBlb2Ytb2JqZWN0PyBlcT8gZXF1YWw/IGVxdj8gZXZhbCBldmVuPyBleGFjdC0+aW5leGFjdCBleGFjdD8gZXhwIGV4cHQgI2YgZmxvb3IgZm9yY2UgZ2NkIGltYWctcGFydCBpbmV4YWN0LT5leGFjdCBpbmV4YWN0PyBpbnB1dC1wb3J0PyBpbnRlZ2VyLT5jaGFyIGludGVnZXI/IGludGVyYWN0aW9uLWVudmlyb25tZW50IGxjbSBsZW5ndGggbGlzdCBsaXN0LT5zdHJpbmcgbGlzdC0+dmVjdG9yIGxpc3QtcmVmIGxpc3QtdGFpbCBsaXN0PyBsb2FkIGxvZyBtYWduaXR1ZGUgbWFrZS1wb2xhciBtYWtlLXJlY3Rhbmd1bGFyIG1ha2Utc3RyaW5nIG1ha2UtdmVjdG9yIG1heCBtZW1iZXIgbWVtcSBtZW12IG1pbiBtb2R1bG8gbmVnYXRpdmU/IG5ld2xpbmUgbm90IG51bGwtZW52aXJvbm1lbnQgbnVsbD8gbnVtYmVyLT5zdHJpbmcgbnVtYmVyPyBudW1lcmF0b3Igb2RkPyBvcGVuLWlucHV0LWZpbGUgb3Blbi1vdXRwdXQtZmlsZSBvdXRwdXQtcG9ydD8gcGFpcj8gcGVlay1jaGFyIHBvcnQ/IHBvc2l0aXZlPyBwcm9jZWR1cmU/IHF1YXNpcXVvdGUgcXVvdGUgcXVvdGllbnQgcmF0aW9uYWw/IHJhdGlvbmFsaXplIHJlYWQgcmVhZC1jaGFyIHJlYWwtcGFydCByZWFsPyByZW1haW5kZXIgcmV2ZXJzZSByb3VuZCBzY2hlbWUtcmVwb3J0LWVudmlyb25tZW50IHNldCEgc2V0LWNhciEgc2V0LWNkciEgc2luIHNxcnQgc3RyaW5nIHN0cmluZy0+bGlzdCBzdHJpbmctPm51bWJlciBzdHJpbmctPnN5bWJvbCBzdHJpbmctYXBwZW5kIHN0cmluZy1jaTw9PyBzdHJpbmctY2k8PyBzdHJpbmctY2k9PyBzdHJpbmctY2k+PT8gc3RyaW5nLWNpPj8gc3RyaW5nLWNvcHkgc3RyaW5nLWZpbGwhIHN0cmluZy1sZW5ndGggc3RyaW5nLXJlZiBzdHJpbmctc2V0ISBzdHJpbmc8PT8gc3RyaW5nPD8gc3RyaW5nPT8gc3RyaW5nPj0/IHN0cmluZz4/IHN0cmluZz8gc3Vic3RyaW5nIHN5bWJvbC0+c3RyaW5nIHN5bWJvbD8gI3QgdGFuIHRyYW5zY3JpcHQtb2ZmIHRyYW5zY3JpcHQtb24gdHJ1bmNhdGUgdmFsdWVzIHZlY3RvciB2ZWN0b3ItPmxpc3QgdmVjdG9yLWZpbGwhIHZlY3Rvci1sZW5ndGggdmVjdG9yLXJlZiB2ZWN0b3Itc2V0ISB3aXRoLWlucHV0LWZyb20tZmlsZSB3aXRoLW91dHB1dC10by1maWxlIHdyaXRlIHdyaXRlLWNoYXIgemVybz9cIik7XG52YXIgaW5kZW50S2V5cyA9IG1ha2VLZXl3b3JkcyhcImRlZmluZSBsZXQgbGV0cmVjIGxldCogbGFtYmRhIGRlZmluZS1tYWNybyBkZWZtYWNybyBsZXQtc3ludGF4IGxldHJlYy1zeW50YXggbGV0LXZhbHVlcyBsZXQqLXZhbHVlcyBkZWZpbmUtc3ludGF4IHN5bnRheC1ydWxlcyBkZWZpbmUtdmFsdWVzIHdoZW4gdW5sZXNzXCIpO1xuZnVuY3Rpb24gc3RhdGVTdGFjayhpbmRlbnQsIHR5cGUsIHByZXYpIHtcbiAgLy8gcmVwcmVzZW50cyBhIHN0YXRlIHN0YWNrIG9iamVjdFxuICB0aGlzLmluZGVudCA9IGluZGVudDtcbiAgdGhpcy50eXBlID0gdHlwZTtcbiAgdGhpcy5wcmV2ID0gcHJldjtcbn1cbmZ1bmN0aW9uIHB1c2hTdGFjayhzdGF0ZSwgaW5kZW50LCB0eXBlKSB7XG4gIHN0YXRlLmluZGVudFN0YWNrID0gbmV3IHN0YXRlU3RhY2soaW5kZW50LCB0eXBlLCBzdGF0ZS5pbmRlbnRTdGFjayk7XG59XG5mdW5jdGlvbiBwb3BTdGFjayhzdGF0ZSkge1xuICBzdGF0ZS5pbmRlbnRTdGFjayA9IHN0YXRlLmluZGVudFN0YWNrLnByZXY7XG59XG52YXIgYmluYXJ5TWF0Y2hlciA9IG5ldyBSZWdFeHAoL14oPzpbLStdaXxbLStdWzAxXSsjKig/OlxcL1swMV0rIyopP2l8Wy0rXT9bMDFdKyMqKD86XFwvWzAxXSsjKik/QFstK10/WzAxXSsjKig/OlxcL1swMV0rIyopP3xbLStdP1swMV0rIyooPzpcXC9bMDFdKyMqKT9bLStdKD86WzAxXSsjKig/OlxcL1swMV0rIyopPyk/aXxbLStdP1swMV0rIyooPzpcXC9bMDFdKyMqKT8pKD89WygpXFxzO1wiXXwkKS9pKTtcbnZhciBvY3RhbE1hdGNoZXIgPSBuZXcgUmVnRXhwKC9eKD86Wy0rXWl8Wy0rXVswLTddKyMqKD86XFwvWzAtN10rIyopP2l8Wy0rXT9bMC03XSsjKig/OlxcL1swLTddKyMqKT9AWy0rXT9bMC03XSsjKig/OlxcL1swLTddKyMqKT98Wy0rXT9bMC03XSsjKig/OlxcL1swLTddKyMqKT9bLStdKD86WzAtN10rIyooPzpcXC9bMC03XSsjKik/KT9pfFstK10/WzAtN10rIyooPzpcXC9bMC03XSsjKik/KSg/PVsoKVxccztcIl18JCkvaSk7XG52YXIgaGV4TWF0Y2hlciA9IG5ldyBSZWdFeHAoL14oPzpbLStdaXxbLStdW1xcZGEtZl0rIyooPzpcXC9bXFxkYS1mXSsjKik/aXxbLStdP1tcXGRhLWZdKyMqKD86XFwvW1xcZGEtZl0rIyopP0BbLStdP1tcXGRhLWZdKyMqKD86XFwvW1xcZGEtZl0rIyopP3xbLStdP1tcXGRhLWZdKyMqKD86XFwvW1xcZGEtZl0rIyopP1stK10oPzpbXFxkYS1mXSsjKig/OlxcL1tcXGRhLWZdKyMqKT8pP2l8Wy0rXT9bXFxkYS1mXSsjKig/OlxcL1tcXGRhLWZdKyMqKT8pKD89WygpXFxzO1wiXXwkKS9pKTtcbnZhciBkZWNpbWFsTWF0Y2hlciA9IG5ldyBSZWdFeHAoL14oPzpbLStdaXxbLStdKD86KD86KD86XFxkKyMrXFwuPyMqfFxcZCtcXC5cXGQqIyp8XFwuXFxkKyMqfFxcZCspKD86W2VzZmRsXVstK10/XFxkKyk/KXxcXGQrIypcXC9cXGQrIyopaXxbLStdPyg/Oig/Oig/OlxcZCsjK1xcLj8jKnxcXGQrXFwuXFxkKiMqfFxcLlxcZCsjKnxcXGQrKSg/Oltlc2ZkbF1bLStdP1xcZCspPyl8XFxkKyMqXFwvXFxkKyMqKUBbLStdPyg/Oig/Oig/OlxcZCsjK1xcLj8jKnxcXGQrXFwuXFxkKiMqfFxcLlxcZCsjKnxcXGQrKSg/Oltlc2ZkbF1bLStdP1xcZCspPyl8XFxkKyMqXFwvXFxkKyMqKXxbLStdPyg/Oig/Oig/OlxcZCsjK1xcLj8jKnxcXGQrXFwuXFxkKiMqfFxcLlxcZCsjKnxcXGQrKSg/Oltlc2ZkbF1bLStdP1xcZCspPyl8XFxkKyMqXFwvXFxkKyMqKVstK10oPzooPzooPzpcXGQrIytcXC4/Iyp8XFxkK1xcLlxcZCojKnxcXC5cXGQrIyp8XFxkKykoPzpbZXNmZGxdWy0rXT9cXGQrKT8pfFxcZCsjKlxcL1xcZCsjKik/aXwoPzooPzooPzpcXGQrIytcXC4/Iyp8XFxkK1xcLlxcZCojKnxcXC5cXGQrIyp8XFxkKykoPzpbZXNmZGxdWy0rXT9cXGQrKT8pfFxcZCsjKlxcL1xcZCsjKikpKD89WygpXFxzO1wiXXwkKS9pKTtcbmZ1bmN0aW9uIGlzQmluYXJ5TnVtYmVyKHN0cmVhbSkge1xuICByZXR1cm4gc3RyZWFtLm1hdGNoKGJpbmFyeU1hdGNoZXIpO1xufVxuZnVuY3Rpb24gaXNPY3RhbE51bWJlcihzdHJlYW0pIHtcbiAgcmV0dXJuIHN0cmVhbS5tYXRjaChvY3RhbE1hdGNoZXIpO1xufVxuZnVuY3Rpb24gaXNEZWNpbWFsTnVtYmVyKHN0cmVhbSwgYmFja3VwKSB7XG4gIGlmIChiYWNrdXAgPT09IHRydWUpIHtcbiAgICBzdHJlYW0uYmFja1VwKDEpO1xuICB9XG4gIHJldHVybiBzdHJlYW0ubWF0Y2goZGVjaW1hbE1hdGNoZXIpO1xufVxuZnVuY3Rpb24gaXNIZXhOdW1iZXIoc3RyZWFtKSB7XG4gIHJldHVybiBzdHJlYW0ubWF0Y2goaGV4TWF0Y2hlcik7XG59XG5mdW5jdGlvbiBwcm9jZXNzRXNjYXBlZFNlcXVlbmNlKHN0cmVhbSwgb3B0aW9ucykge1xuICB2YXIgbmV4dCxcbiAgICBlc2NhcGVkID0gZmFsc2U7XG4gIHdoaWxlICgobmV4dCA9IHN0cmVhbS5uZXh0KCkpICE9IG51bGwpIHtcbiAgICBpZiAobmV4dCA9PSBvcHRpb25zLnRva2VuICYmICFlc2NhcGVkKSB7XG4gICAgICBvcHRpb25zLnN0YXRlLm1vZGUgPSBmYWxzZTtcbiAgICAgIGJyZWFrO1xuICAgIH1cbiAgICBlc2NhcGVkID0gIWVzY2FwZWQgJiYgbmV4dCA9PSBcIlxcXFxcIjtcbiAgfVxufVxuZXhwb3J0IGNvbnN0IHNjaGVtZSA9IHtcbiAgbmFtZTogXCJzY2hlbWVcIixcbiAgc3RhcnRTdGF0ZTogZnVuY3Rpb24gKCkge1xuICAgIHJldHVybiB7XG4gICAgICBpbmRlbnRTdGFjazogbnVsbCxcbiAgICAgIGluZGVudGF0aW9uOiAwLFxuICAgICAgbW9kZTogZmFsc2UsXG4gICAgICBzRXhwckNvbW1lbnQ6IGZhbHNlLFxuICAgICAgc0V4cHJRdW90ZTogZmFsc2VcbiAgICB9O1xuICB9LFxuICB0b2tlbjogZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICBpZiAoc3RhdGUuaW5kZW50U3RhY2sgPT0gbnVsbCAmJiBzdHJlYW0uc29sKCkpIHtcbiAgICAgIC8vIHVwZGF0ZSBpbmRlbnRhdGlvbiwgYnV0IG9ubHkgaWYgaW5kZW50U3RhY2sgaXMgZW1wdHlcbiAgICAgIHN0YXRlLmluZGVudGF0aW9uID0gc3RyZWFtLmluZGVudGF0aW9uKCk7XG4gICAgfVxuXG4gICAgLy8gc2tpcCBzcGFjZXNcbiAgICBpZiAoc3RyZWFtLmVhdFNwYWNlKCkpIHtcbiAgICAgIHJldHVybiBudWxsO1xuICAgIH1cbiAgICB2YXIgcmV0dXJuVHlwZSA9IG51bGw7XG4gICAgc3dpdGNoIChzdGF0ZS5tb2RlKSB7XG4gICAgICBjYXNlIFwic3RyaW5nXCI6XG4gICAgICAgIC8vIG11bHRpLWxpbmUgc3RyaW5nIHBhcnNpbmcgbW9kZVxuICAgICAgICBwcm9jZXNzRXNjYXBlZFNlcXVlbmNlKHN0cmVhbSwge1xuICAgICAgICAgIHRva2VuOiBcIlxcXCJcIixcbiAgICAgICAgICBzdGF0ZTogc3RhdGVcbiAgICAgICAgfSk7XG4gICAgICAgIHJldHVyblR5cGUgPSBTVFJJTkc7IC8vIGNvbnRpbnVlIG9uIGluIHNjaGVtZS1zdHJpbmcgbW9kZVxuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgXCJzeW1ib2xcIjpcbiAgICAgICAgLy8gZXNjYXBlIHN5bWJvbFxuICAgICAgICBwcm9jZXNzRXNjYXBlZFNlcXVlbmNlKHN0cmVhbSwge1xuICAgICAgICAgIHRva2VuOiBcInxcIixcbiAgICAgICAgICBzdGF0ZTogc3RhdGVcbiAgICAgICAgfSk7XG4gICAgICAgIHJldHVyblR5cGUgPSBTWU1CT0w7IC8vIGNvbnRpbnVlIG9uIGluIHNjaGVtZS1zeW1ib2wgbW9kZVxuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgXCJjb21tZW50XCI6XG4gICAgICAgIC8vIGNvbW1lbnQgcGFyc2luZyBtb2RlXG4gICAgICAgIHZhciBuZXh0LFxuICAgICAgICAgIG1heWJlRW5kID0gZmFsc2U7XG4gICAgICAgIHdoaWxlICgobmV4dCA9IHN0cmVhbS5uZXh0KCkpICE9IG51bGwpIHtcbiAgICAgICAgICBpZiAobmV4dCA9PSBcIiNcIiAmJiBtYXliZUVuZCkge1xuICAgICAgICAgICAgc3RhdGUubW9kZSA9IGZhbHNlO1xuICAgICAgICAgICAgYnJlYWs7XG4gICAgICAgICAgfVxuICAgICAgICAgIG1heWJlRW5kID0gbmV4dCA9PSBcInxcIjtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm5UeXBlID0gQ09NTUVOVDtcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlIFwicy1leHByLWNvbW1lbnRcIjpcbiAgICAgICAgLy8gcy1leHByIGNvbW1lbnRpbmcgbW9kZVxuICAgICAgICBzdGF0ZS5tb2RlID0gZmFsc2U7XG4gICAgICAgIGlmIChzdHJlYW0ucGVlaygpID09IFwiKFwiIHx8IHN0cmVhbS5wZWVrKCkgPT0gXCJbXCIpIHtcbiAgICAgICAgICAvLyBhY3R1YWxseSBzdGFydCBzY2hlbWUgcy1leHByIGNvbW1lbnRpbmcgbW9kZVxuICAgICAgICAgIHN0YXRlLnNFeHByQ29tbWVudCA9IDA7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgLy8gaWYgbm90IHdlIGp1c3QgY29tbWVudCB0aGUgZW50aXJlIG9mIHRoZSBuZXh0IHRva2VuXG4gICAgICAgICAgc3RyZWFtLmVhdFdoaWxlKC9bXlxcc1xcKFxcKVxcW1xcXV0vKTsgLy8gZWF0IHN5bWJvbCBhdG9tXG4gICAgICAgICAgcmV0dXJuVHlwZSA9IENPTU1FTlQ7XG4gICAgICAgICAgYnJlYWs7XG4gICAgICAgIH1cbiAgICAgIGRlZmF1bHQ6XG4gICAgICAgIC8vIGRlZmF1bHQgcGFyc2luZyBtb2RlXG4gICAgICAgIHZhciBjaCA9IHN0cmVhbS5uZXh0KCk7XG4gICAgICAgIGlmIChjaCA9PSBcIlxcXCJcIikge1xuICAgICAgICAgIHN0YXRlLm1vZGUgPSBcInN0cmluZ1wiO1xuICAgICAgICAgIHJldHVyblR5cGUgPSBTVFJJTkc7XG4gICAgICAgIH0gZWxzZSBpZiAoY2ggPT0gXCInXCIpIHtcbiAgICAgICAgICBpZiAoc3RyZWFtLnBlZWsoKSA9PSBcIihcIiB8fCBzdHJlYW0ucGVlaygpID09IFwiW1wiKSB7XG4gICAgICAgICAgICBpZiAodHlwZW9mIHN0YXRlLnNFeHByUXVvdGUgIT0gXCJudW1iZXJcIikge1xuICAgICAgICAgICAgICBzdGF0ZS5zRXhwclF1b3RlID0gMDtcbiAgICAgICAgICAgIH0gLy8gZWxzZSBhbHJlYWR5IGluIGEgcXVvdGVkIGV4cHJlc3Npb25cbiAgICAgICAgICAgIHJldHVyblR5cGUgPSBBVE9NO1xuICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICBzdHJlYW0uZWF0V2hpbGUoL1tcXHdfXFwtISQlJiorXFwuXFwvOjw9Pj9AXFxefl0vKTtcbiAgICAgICAgICAgIHJldHVyblR5cGUgPSBBVE9NO1xuICAgICAgICAgIH1cbiAgICAgICAgfSBlbHNlIGlmIChjaCA9PSAnfCcpIHtcbiAgICAgICAgICBzdGF0ZS5tb2RlID0gXCJzeW1ib2xcIjtcbiAgICAgICAgICByZXR1cm5UeXBlID0gU1lNQk9MO1xuICAgICAgICB9IGVsc2UgaWYgKGNoID09ICcjJykge1xuICAgICAgICAgIGlmIChzdHJlYW0uZWF0KFwifFwiKSkge1xuICAgICAgICAgICAgLy8gTXVsdGktbGluZSBjb21tZW50XG4gICAgICAgICAgICBzdGF0ZS5tb2RlID0gXCJjb21tZW50XCI7IC8vIHRvZ2dsZSB0byBjb21tZW50IG1vZGVcbiAgICAgICAgICAgIHJldHVyblR5cGUgPSBDT01NRU5UO1xuICAgICAgICAgIH0gZWxzZSBpZiAoc3RyZWFtLmVhdCgvW3RmXS9pKSkge1xuICAgICAgICAgICAgLy8gI3QvI2YgKGF0b20pXG4gICAgICAgICAgICByZXR1cm5UeXBlID0gQVRPTTtcbiAgICAgICAgICB9IGVsc2UgaWYgKHN0cmVhbS5lYXQoJzsnKSkge1xuICAgICAgICAgICAgLy8gUy1FeHByIGNvbW1lbnRcbiAgICAgICAgICAgIHN0YXRlLm1vZGUgPSBcInMtZXhwci1jb21tZW50XCI7XG4gICAgICAgICAgICByZXR1cm5UeXBlID0gQ09NTUVOVDtcbiAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgdmFyIG51bVRlc3QgPSBudWxsLFxuICAgICAgICAgICAgICBoYXNFeGFjdG5lc3MgPSBmYWxzZSxcbiAgICAgICAgICAgICAgaGFzUmFkaXggPSB0cnVlO1xuICAgICAgICAgICAgaWYgKHN0cmVhbS5lYXQoL1tlaV0vaSkpIHtcbiAgICAgICAgICAgICAgaGFzRXhhY3RuZXNzID0gdHJ1ZTtcbiAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgIHN0cmVhbS5iYWNrVXAoMSk7IC8vIG11c3QgYmUgcmFkaXggc3BlY2lmaWVyXG4gICAgICAgICAgICB9XG4gICAgICAgICAgICBpZiAoc3RyZWFtLm1hdGNoKC9eI2IvaSkpIHtcbiAgICAgICAgICAgICAgbnVtVGVzdCA9IGlzQmluYXJ5TnVtYmVyO1xuICAgICAgICAgICAgfSBlbHNlIGlmIChzdHJlYW0ubWF0Y2goL14jby9pKSkge1xuICAgICAgICAgICAgICBudW1UZXN0ID0gaXNPY3RhbE51bWJlcjtcbiAgICAgICAgICAgIH0gZWxzZSBpZiAoc3RyZWFtLm1hdGNoKC9eI3gvaSkpIHtcbiAgICAgICAgICAgICAgbnVtVGVzdCA9IGlzSGV4TnVtYmVyO1xuICAgICAgICAgICAgfSBlbHNlIGlmIChzdHJlYW0ubWF0Y2goL14jZC9pKSkge1xuICAgICAgICAgICAgICBudW1UZXN0ID0gaXNEZWNpbWFsTnVtYmVyO1xuICAgICAgICAgICAgfSBlbHNlIGlmIChzdHJlYW0ubWF0Y2goL15bLSswLTkuXS8sIGZhbHNlKSkge1xuICAgICAgICAgICAgICBoYXNSYWRpeCA9IGZhbHNlO1xuICAgICAgICAgICAgICBudW1UZXN0ID0gaXNEZWNpbWFsTnVtYmVyO1xuICAgICAgICAgICAgICAvLyByZS1jb25zdW1lIHRoZSBpbml0aWFsICMgaWYgYWxsIG1hdGNoZXMgZmFpbGVkXG4gICAgICAgICAgICB9IGVsc2UgaWYgKCFoYXNFeGFjdG5lc3MpIHtcbiAgICAgICAgICAgICAgc3RyZWFtLmVhdCgnIycpO1xuICAgICAgICAgICAgfVxuICAgICAgICAgICAgaWYgKG51bVRlc3QgIT0gbnVsbCkge1xuICAgICAgICAgICAgICBpZiAoaGFzUmFkaXggJiYgIWhhc0V4YWN0bmVzcykge1xuICAgICAgICAgICAgICAgIC8vIGNvbnN1bWUgb3B0aW9uYWwgZXhhY3RuZXNzIGFmdGVyIHJhZGl4XG4gICAgICAgICAgICAgICAgc3RyZWFtLm1hdGNoKC9eI1tlaV0vaSk7XG4gICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgaWYgKG51bVRlc3Qoc3RyZWFtKSkgcmV0dXJuVHlwZSA9IE5VTUJFUjtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICB9XG4gICAgICAgIH0gZWxzZSBpZiAoL15bLSswLTkuXS8udGVzdChjaCkgJiYgaXNEZWNpbWFsTnVtYmVyKHN0cmVhbSwgdHJ1ZSkpIHtcbiAgICAgICAgICAvLyBtYXRjaCBub24tcHJlZml4ZWQgbnVtYmVyLCBtdXN0IGJlIGRlY2ltYWxcbiAgICAgICAgICByZXR1cm5UeXBlID0gTlVNQkVSO1xuICAgICAgICB9IGVsc2UgaWYgKGNoID09IFwiO1wiKSB7XG4gICAgICAgICAgLy8gY29tbWVudFxuICAgICAgICAgIHN0cmVhbS5za2lwVG9FbmQoKTsgLy8gcmVzdCBvZiB0aGUgbGluZSBpcyBhIGNvbW1lbnRcbiAgICAgICAgICByZXR1cm5UeXBlID0gQ09NTUVOVDtcbiAgICAgICAgfSBlbHNlIGlmIChjaCA9PSBcIihcIiB8fCBjaCA9PSBcIltcIikge1xuICAgICAgICAgIHZhciBrZXlXb3JkID0gJyc7XG4gICAgICAgICAgdmFyIGluZGVudFRlbXAgPSBzdHJlYW0uY29sdW1uKCksXG4gICAgICAgICAgICBsZXR0ZXI7XG4gICAgICAgICAgLyoqXG4gICAgICAgICAgICAgRWl0aGVyXG4gICAgICAgICAgICAgKGluZGVudC13b3JkIC4uXG4gICAgICAgICAgICAgKG5vbi1pbmRlbnQtd29yZCAuLlxuICAgICAgICAgICAgICg7c29tZXRoaW5nIGVsc2UsIGJyYWNrZXQsIGV0Yy5cbiAgICAgICAgICAqL1xuXG4gICAgICAgICAgd2hpbGUgKChsZXR0ZXIgPSBzdHJlYW0uZWF0KC9bXlxcc1xcKFxcW1xcO1xcKVxcXV0vKSkgIT0gbnVsbCkge1xuICAgICAgICAgICAga2V5V29yZCArPSBsZXR0ZXI7XG4gICAgICAgICAgfVxuICAgICAgICAgIGlmIChrZXlXb3JkLmxlbmd0aCA+IDAgJiYgaW5kZW50S2V5cy5wcm9wZXJ0eUlzRW51bWVyYWJsZShrZXlXb3JkKSkge1xuICAgICAgICAgICAgLy8gaW5kZW50LXdvcmRcblxuICAgICAgICAgICAgcHVzaFN0YWNrKHN0YXRlLCBpbmRlbnRUZW1wICsgSU5ERU5UX1dPUkRfU0tJUCwgY2gpO1xuICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAvLyBub24taW5kZW50IHdvcmRcbiAgICAgICAgICAgIC8vIHdlIGNvbnRpbnVlIGVhdGluZyB0aGUgc3BhY2VzXG4gICAgICAgICAgICBzdHJlYW0uZWF0U3BhY2UoKTtcbiAgICAgICAgICAgIGlmIChzdHJlYW0uZW9sKCkgfHwgc3RyZWFtLnBlZWsoKSA9PSBcIjtcIikge1xuICAgICAgICAgICAgICAvLyBub3RoaW5nIHNpZ25pZmljYW50IGFmdGVyXG4gICAgICAgICAgICAgIC8vIHdlIHJlc3RhcnQgaW5kZW50YXRpb24gMSBzcGFjZSBhZnRlclxuICAgICAgICAgICAgICBwdXNoU3RhY2soc3RhdGUsIGluZGVudFRlbXAgKyAxLCBjaCk7XG4gICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICBwdXNoU3RhY2soc3RhdGUsIGluZGVudFRlbXAgKyBzdHJlYW0uY3VycmVudCgpLmxlbmd0aCwgY2gpOyAvLyBlbHNlIHdlIG1hdGNoXG4gICAgICAgICAgICB9XG4gICAgICAgICAgfVxuICAgICAgICAgIHN0cmVhbS5iYWNrVXAoc3RyZWFtLmN1cnJlbnQoKS5sZW5ndGggLSAxKTsgLy8gdW5kbyBhbGwgdGhlIGVhdGluZ1xuXG4gICAgICAgICAgaWYgKHR5cGVvZiBzdGF0ZS5zRXhwckNvbW1lbnQgPT0gXCJudW1iZXJcIikgc3RhdGUuc0V4cHJDb21tZW50Kys7XG4gICAgICAgICAgaWYgKHR5cGVvZiBzdGF0ZS5zRXhwclF1b3RlID09IFwibnVtYmVyXCIpIHN0YXRlLnNFeHByUXVvdGUrKztcbiAgICAgICAgICByZXR1cm5UeXBlID0gQlJBQ0tFVDtcbiAgICAgICAgfSBlbHNlIGlmIChjaCA9PSBcIilcIiB8fCBjaCA9PSBcIl1cIikge1xuICAgICAgICAgIHJldHVyblR5cGUgPSBCUkFDS0VUO1xuICAgICAgICAgIGlmIChzdGF0ZS5pbmRlbnRTdGFjayAhPSBudWxsICYmIHN0YXRlLmluZGVudFN0YWNrLnR5cGUgPT0gKGNoID09IFwiKVwiID8gXCIoXCIgOiBcIltcIikpIHtcbiAgICAgICAgICAgIHBvcFN0YWNrKHN0YXRlKTtcbiAgICAgICAgICAgIGlmICh0eXBlb2Ygc3RhdGUuc0V4cHJDb21tZW50ID09IFwibnVtYmVyXCIpIHtcbiAgICAgICAgICAgICAgaWYgKC0tc3RhdGUuc0V4cHJDb21tZW50ID09IDApIHtcbiAgICAgICAgICAgICAgICByZXR1cm5UeXBlID0gQ09NTUVOVDsgLy8gZmluYWwgY2xvc2luZyBicmFja2V0XG4gICAgICAgICAgICAgICAgc3RhdGUuc0V4cHJDb21tZW50ID0gZmFsc2U7IC8vIHR1cm4gb2ZmIHMtZXhwciBjb21tZW50aW5nIG1vZGVcbiAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfVxuICAgICAgICAgICAgaWYgKHR5cGVvZiBzdGF0ZS5zRXhwclF1b3RlID09IFwibnVtYmVyXCIpIHtcbiAgICAgICAgICAgICAgaWYgKC0tc3RhdGUuc0V4cHJRdW90ZSA9PSAwKSB7XG4gICAgICAgICAgICAgICAgcmV0dXJuVHlwZSA9IEFUT007IC8vIGZpbmFsIGNsb3NpbmcgYnJhY2tldFxuICAgICAgICAgICAgICAgIHN0YXRlLnNFeHByUXVvdGUgPSBmYWxzZTsgLy8gdHVybiBvZmYgcy1leHByIHF1b3RlIG1vZGVcbiAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfVxuICAgICAgICAgIH1cbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICBzdHJlYW0uZWF0V2hpbGUoL1tcXHdfXFwtISQlJiorXFwuXFwvOjw9Pj9AXFxefl0vKTtcbiAgICAgICAgICBpZiAoa2V5d29yZHMgJiYga2V5d29yZHMucHJvcGVydHlJc0VudW1lcmFibGUoc3RyZWFtLmN1cnJlbnQoKSkpIHtcbiAgICAgICAgICAgIHJldHVyblR5cGUgPSBCVUlMVElOO1xuICAgICAgICAgIH0gZWxzZSByZXR1cm5UeXBlID0gXCJ2YXJpYWJsZVwiO1xuICAgICAgICB9XG4gICAgfVxuICAgIHJldHVybiB0eXBlb2Ygc3RhdGUuc0V4cHJDb21tZW50ID09IFwibnVtYmVyXCIgPyBDT01NRU5UIDogdHlwZW9mIHN0YXRlLnNFeHByUXVvdGUgPT0gXCJudW1iZXJcIiA/IEFUT00gOiByZXR1cm5UeXBlO1xuICB9LFxuICBpbmRlbnQ6IGZ1bmN0aW9uIChzdGF0ZSkge1xuICAgIGlmIChzdGF0ZS5pbmRlbnRTdGFjayA9PSBudWxsKSByZXR1cm4gc3RhdGUuaW5kZW50YXRpb247XG4gICAgcmV0dXJuIHN0YXRlLmluZGVudFN0YWNrLmluZGVudDtcbiAgfSxcbiAgbGFuZ3VhZ2VEYXRhOiB7XG4gICAgY2xvc2VCcmFja2V0czoge1xuICAgICAgYnJhY2tldHM6IFtcIihcIiwgXCJbXCIsIFwie1wiLCAnXCInXVxuICAgIH0sXG4gICAgY29tbWVudFRva2Vuczoge1xuICAgICAgbGluZTogXCI7O1wiXG4gICAgfVxuICB9XG59OyJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==