"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[6041],{

/***/ 16041:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "haskell": () => (/* binding */ haskell)
/* harmony export */ });
function switchState(source, setState, f) {
  setState(f);
  return f(source, setState);
}

// These should all be Unicode extended, as per the Haskell 2010 report
var smallRE = /[a-z_]/;
var largeRE = /[A-Z]/;
var digitRE = /\d/;
var hexitRE = /[0-9A-Fa-f]/;
var octitRE = /[0-7]/;
var idRE = /[a-z_A-Z0-9'\xa1-\uffff]/;
var symbolRE = /[-!#$%&*+.\/<=>?@\\^|~:]/;
var specialRE = /[(),;[\]`{}]/;
var whiteCharRE = /[ \t\v\f]/; // newlines are handled in tokenizer

function normal(source, setState) {
  if (source.eatWhile(whiteCharRE)) {
    return null;
  }
  var ch = source.next();
  if (specialRE.test(ch)) {
    if (ch == '{' && source.eat('-')) {
      var t = "comment";
      if (source.eat('#')) {
        t = "meta";
      }
      return switchState(source, setState, ncomment(t, 1));
    }
    return null;
  }
  if (ch == '\'') {
    if (source.eat('\\')) {
      source.next(); // should handle other escapes here
    } else {
      source.next();
    }
    if (source.eat('\'')) {
      return "string";
    }
    return "error";
  }
  if (ch == '"') {
    return switchState(source, setState, stringLiteral);
  }
  if (largeRE.test(ch)) {
    source.eatWhile(idRE);
    if (source.eat('.')) {
      return "qualifier";
    }
    return "type";
  }
  if (smallRE.test(ch)) {
    source.eatWhile(idRE);
    return "variable";
  }
  if (digitRE.test(ch)) {
    if (ch == '0') {
      if (source.eat(/[xX]/)) {
        source.eatWhile(hexitRE); // should require at least 1
        return "integer";
      }
      if (source.eat(/[oO]/)) {
        source.eatWhile(octitRE); // should require at least 1
        return "number";
      }
    }
    source.eatWhile(digitRE);
    var t = "number";
    if (source.match(/^\.\d+/)) {
      t = "number";
    }
    if (source.eat(/[eE]/)) {
      t = "number";
      source.eat(/[-+]/);
      source.eatWhile(digitRE); // should require at least 1
    }
    return t;
  }
  if (ch == "." && source.eat(".")) return "keyword";
  if (symbolRE.test(ch)) {
    if (ch == '-' && source.eat(/-/)) {
      source.eatWhile(/-/);
      if (!source.eat(symbolRE)) {
        source.skipToEnd();
        return "comment";
      }
    }
    source.eatWhile(symbolRE);
    return "variable";
  }
  return "error";
}
function ncomment(type, nest) {
  if (nest == 0) {
    return normal;
  }
  return function (source, setState) {
    var currNest = nest;
    while (!source.eol()) {
      var ch = source.next();
      if (ch == '{' && source.eat('-')) {
        ++currNest;
      } else if (ch == '-' && source.eat('}')) {
        --currNest;
        if (currNest == 0) {
          setState(normal);
          return type;
        }
      }
    }
    setState(ncomment(type, currNest));
    return type;
  };
}
function stringLiteral(source, setState) {
  while (!source.eol()) {
    var ch = source.next();
    if (ch == '"') {
      setState(normal);
      return "string";
    }
    if (ch == '\\') {
      if (source.eol() || source.eat(whiteCharRE)) {
        setState(stringGap);
        return "string";
      }
      if (source.eat('&')) {} else {
        source.next(); // should handle other escapes here
      }
    }
  }
  setState(normal);
  return "error";
}
function stringGap(source, setState) {
  if (source.eat('\\')) {
    return switchState(source, setState, stringLiteral);
  }
  source.next();
  setState(normal);
  return "error";
}
var wellKnownWords = function () {
  var wkw = {};
  function setType(t) {
    return function () {
      for (var i = 0; i < arguments.length; i++) wkw[arguments[i]] = t;
    };
  }
  setType("keyword")("case", "class", "data", "default", "deriving", "do", "else", "foreign", "if", "import", "in", "infix", "infixl", "infixr", "instance", "let", "module", "newtype", "of", "then", "type", "where", "_");
  setType("keyword")("\.\.", ":", "::", "=", "\\", "<-", "->", "@", "~", "=>");
  setType("builtin")("!!", "$!", "$", "&&", "+", "++", "-", ".", "/", "/=", "<", "<*", "<=", "<$>", "<*>", "=<<", "==", ">", ">=", ">>", ">>=", "^", "^^", "||", "*", "*>", "**");
  setType("builtin")("Applicative", "Bool", "Bounded", "Char", "Double", "EQ", "Either", "Enum", "Eq", "False", "FilePath", "Float", "Floating", "Fractional", "Functor", "GT", "IO", "IOError", "Int", "Integer", "Integral", "Just", "LT", "Left", "Maybe", "Monad", "Nothing", "Num", "Ord", "Ordering", "Rational", "Read", "ReadS", "Real", "RealFloat", "RealFrac", "Right", "Show", "ShowS", "String", "True");
  setType("builtin")("abs", "acos", "acosh", "all", "and", "any", "appendFile", "asTypeOf", "asin", "asinh", "atan", "atan2", "atanh", "break", "catch", "ceiling", "compare", "concat", "concatMap", "const", "cos", "cosh", "curry", "cycle", "decodeFloat", "div", "divMod", "drop", "dropWhile", "either", "elem", "encodeFloat", "enumFrom", "enumFromThen", "enumFromThenTo", "enumFromTo", "error", "even", "exp", "exponent", "fail", "filter", "flip", "floatDigits", "floatRadix", "floatRange", "floor", "fmap", "foldl", "foldl1", "foldr", "foldr1", "fromEnum", "fromInteger", "fromIntegral", "fromRational", "fst", "gcd", "getChar", "getContents", "getLine", "head", "id", "init", "interact", "ioError", "isDenormalized", "isIEEE", "isInfinite", "isNaN", "isNegativeZero", "iterate", "last", "lcm", "length", "lex", "lines", "log", "logBase", "lookup", "map", "mapM", "mapM_", "max", "maxBound", "maximum", "maybe", "min", "minBound", "minimum", "mod", "negate", "not", "notElem", "null", "odd", "or", "otherwise", "pi", "pred", "print", "product", "properFraction", "pure", "putChar", "putStr", "putStrLn", "quot", "quotRem", "read", "readFile", "readIO", "readList", "readLn", "readParen", "reads", "readsPrec", "realToFrac", "recip", "rem", "repeat", "replicate", "return", "reverse", "round", "scaleFloat", "scanl", "scanl1", "scanr", "scanr1", "seq", "sequence", "sequence_", "show", "showChar", "showList", "showParen", "showString", "shows", "showsPrec", "significand", "signum", "sin", "sinh", "snd", "span", "splitAt", "sqrt", "subtract", "succ", "sum", "tail", "take", "takeWhile", "tan", "tanh", "toEnum", "toInteger", "toRational", "truncate", "uncurry", "undefined", "unlines", "until", "unwords", "unzip", "unzip3", "userError", "words", "writeFile", "zip", "zip3", "zipWith", "zipWith3");
  return wkw;
}();
const haskell = {
  name: "haskell",
  startState: function () {
    return {
      f: normal
    };
  },
  copyState: function (s) {
    return {
      f: s.f
    };
  },
  token: function (stream, state) {
    var t = state.f(stream, function (s) {
      state.f = s;
    });
    var w = stream.current();
    return wellKnownWords.hasOwnProperty(w) ? wellKnownWords[w] : t;
  },
  languageData: {
    commentTokens: {
      line: "--",
      block: {
        open: "{-",
        close: "-}"
      }
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNjA0MS5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9AY29kZW1pcnJvci9sZWdhY3ktbW9kZXMvbW9kZS9oYXNrZWxsLmpzIl0sInNvdXJjZXNDb250ZW50IjpbImZ1bmN0aW9uIHN3aXRjaFN0YXRlKHNvdXJjZSwgc2V0U3RhdGUsIGYpIHtcbiAgc2V0U3RhdGUoZik7XG4gIHJldHVybiBmKHNvdXJjZSwgc2V0U3RhdGUpO1xufVxuXG4vLyBUaGVzZSBzaG91bGQgYWxsIGJlIFVuaWNvZGUgZXh0ZW5kZWQsIGFzIHBlciB0aGUgSGFza2VsbCAyMDEwIHJlcG9ydFxudmFyIHNtYWxsUkUgPSAvW2Etel9dLztcbnZhciBsYXJnZVJFID0gL1tBLVpdLztcbnZhciBkaWdpdFJFID0gL1xcZC87XG52YXIgaGV4aXRSRSA9IC9bMC05QS1GYS1mXS87XG52YXIgb2N0aXRSRSA9IC9bMC03XS87XG52YXIgaWRSRSA9IC9bYS16X0EtWjAtOSdcXHhhMS1cXHVmZmZmXS87XG52YXIgc3ltYm9sUkUgPSAvWy0hIyQlJiorLlxcLzw9Pj9AXFxcXF58fjpdLztcbnZhciBzcGVjaWFsUkUgPSAvWygpLDtbXFxdYHt9XS87XG52YXIgd2hpdGVDaGFyUkUgPSAvWyBcXHRcXHZcXGZdLzsgLy8gbmV3bGluZXMgYXJlIGhhbmRsZWQgaW4gdG9rZW5pemVyXG5cbmZ1bmN0aW9uIG5vcm1hbChzb3VyY2UsIHNldFN0YXRlKSB7XG4gIGlmIChzb3VyY2UuZWF0V2hpbGUod2hpdGVDaGFyUkUpKSB7XG4gICAgcmV0dXJuIG51bGw7XG4gIH1cbiAgdmFyIGNoID0gc291cmNlLm5leHQoKTtcbiAgaWYgKHNwZWNpYWxSRS50ZXN0KGNoKSkge1xuICAgIGlmIChjaCA9PSAneycgJiYgc291cmNlLmVhdCgnLScpKSB7XG4gICAgICB2YXIgdCA9IFwiY29tbWVudFwiO1xuICAgICAgaWYgKHNvdXJjZS5lYXQoJyMnKSkge1xuICAgICAgICB0ID0gXCJtZXRhXCI7XG4gICAgICB9XG4gICAgICByZXR1cm4gc3dpdGNoU3RhdGUoc291cmNlLCBzZXRTdGF0ZSwgbmNvbW1lbnQodCwgMSkpO1xuICAgIH1cbiAgICByZXR1cm4gbnVsbDtcbiAgfVxuICBpZiAoY2ggPT0gJ1xcJycpIHtcbiAgICBpZiAoc291cmNlLmVhdCgnXFxcXCcpKSB7XG4gICAgICBzb3VyY2UubmV4dCgpOyAvLyBzaG91bGQgaGFuZGxlIG90aGVyIGVzY2FwZXMgaGVyZVxuICAgIH0gZWxzZSB7XG4gICAgICBzb3VyY2UubmV4dCgpO1xuICAgIH1cbiAgICBpZiAoc291cmNlLmVhdCgnXFwnJykpIHtcbiAgICAgIHJldHVybiBcInN0cmluZ1wiO1xuICAgIH1cbiAgICByZXR1cm4gXCJlcnJvclwiO1xuICB9XG4gIGlmIChjaCA9PSAnXCInKSB7XG4gICAgcmV0dXJuIHN3aXRjaFN0YXRlKHNvdXJjZSwgc2V0U3RhdGUsIHN0cmluZ0xpdGVyYWwpO1xuICB9XG4gIGlmIChsYXJnZVJFLnRlc3QoY2gpKSB7XG4gICAgc291cmNlLmVhdFdoaWxlKGlkUkUpO1xuICAgIGlmIChzb3VyY2UuZWF0KCcuJykpIHtcbiAgICAgIHJldHVybiBcInF1YWxpZmllclwiO1xuICAgIH1cbiAgICByZXR1cm4gXCJ0eXBlXCI7XG4gIH1cbiAgaWYgKHNtYWxsUkUudGVzdChjaCkpIHtcbiAgICBzb3VyY2UuZWF0V2hpbGUoaWRSRSk7XG4gICAgcmV0dXJuIFwidmFyaWFibGVcIjtcbiAgfVxuICBpZiAoZGlnaXRSRS50ZXN0KGNoKSkge1xuICAgIGlmIChjaCA9PSAnMCcpIHtcbiAgICAgIGlmIChzb3VyY2UuZWF0KC9beFhdLykpIHtcbiAgICAgICAgc291cmNlLmVhdFdoaWxlKGhleGl0UkUpOyAvLyBzaG91bGQgcmVxdWlyZSBhdCBsZWFzdCAxXG4gICAgICAgIHJldHVybiBcImludGVnZXJcIjtcbiAgICAgIH1cbiAgICAgIGlmIChzb3VyY2UuZWF0KC9bb09dLykpIHtcbiAgICAgICAgc291cmNlLmVhdFdoaWxlKG9jdGl0UkUpOyAvLyBzaG91bGQgcmVxdWlyZSBhdCBsZWFzdCAxXG4gICAgICAgIHJldHVybiBcIm51bWJlclwiO1xuICAgICAgfVxuICAgIH1cbiAgICBzb3VyY2UuZWF0V2hpbGUoZGlnaXRSRSk7XG4gICAgdmFyIHQgPSBcIm51bWJlclwiO1xuICAgIGlmIChzb3VyY2UubWF0Y2goL15cXC5cXGQrLykpIHtcbiAgICAgIHQgPSBcIm51bWJlclwiO1xuICAgIH1cbiAgICBpZiAoc291cmNlLmVhdCgvW2VFXS8pKSB7XG4gICAgICB0ID0gXCJudW1iZXJcIjtcbiAgICAgIHNvdXJjZS5lYXQoL1stK10vKTtcbiAgICAgIHNvdXJjZS5lYXRXaGlsZShkaWdpdFJFKTsgLy8gc2hvdWxkIHJlcXVpcmUgYXQgbGVhc3QgMVxuICAgIH1cbiAgICByZXR1cm4gdDtcbiAgfVxuICBpZiAoY2ggPT0gXCIuXCIgJiYgc291cmNlLmVhdChcIi5cIikpIHJldHVybiBcImtleXdvcmRcIjtcbiAgaWYgKHN5bWJvbFJFLnRlc3QoY2gpKSB7XG4gICAgaWYgKGNoID09ICctJyAmJiBzb3VyY2UuZWF0KC8tLykpIHtcbiAgICAgIHNvdXJjZS5lYXRXaGlsZSgvLS8pO1xuICAgICAgaWYgKCFzb3VyY2UuZWF0KHN5bWJvbFJFKSkge1xuICAgICAgICBzb3VyY2Uuc2tpcFRvRW5kKCk7XG4gICAgICAgIHJldHVybiBcImNvbW1lbnRcIjtcbiAgICAgIH1cbiAgICB9XG4gICAgc291cmNlLmVhdFdoaWxlKHN5bWJvbFJFKTtcbiAgICByZXR1cm4gXCJ2YXJpYWJsZVwiO1xuICB9XG4gIHJldHVybiBcImVycm9yXCI7XG59XG5mdW5jdGlvbiBuY29tbWVudCh0eXBlLCBuZXN0KSB7XG4gIGlmIChuZXN0ID09IDApIHtcbiAgICByZXR1cm4gbm9ybWFsO1xuICB9XG4gIHJldHVybiBmdW5jdGlvbiAoc291cmNlLCBzZXRTdGF0ZSkge1xuICAgIHZhciBjdXJyTmVzdCA9IG5lc3Q7XG4gICAgd2hpbGUgKCFzb3VyY2UuZW9sKCkpIHtcbiAgICAgIHZhciBjaCA9IHNvdXJjZS5uZXh0KCk7XG4gICAgICBpZiAoY2ggPT0gJ3snICYmIHNvdXJjZS5lYXQoJy0nKSkge1xuICAgICAgICArK2N1cnJOZXN0O1xuICAgICAgfSBlbHNlIGlmIChjaCA9PSAnLScgJiYgc291cmNlLmVhdCgnfScpKSB7XG4gICAgICAgIC0tY3Vyck5lc3Q7XG4gICAgICAgIGlmIChjdXJyTmVzdCA9PSAwKSB7XG4gICAgICAgICAgc2V0U3RhdGUobm9ybWFsKTtcbiAgICAgICAgICByZXR1cm4gdHlwZTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH1cbiAgICBzZXRTdGF0ZShuY29tbWVudCh0eXBlLCBjdXJyTmVzdCkpO1xuICAgIHJldHVybiB0eXBlO1xuICB9O1xufVxuZnVuY3Rpb24gc3RyaW5nTGl0ZXJhbChzb3VyY2UsIHNldFN0YXRlKSB7XG4gIHdoaWxlICghc291cmNlLmVvbCgpKSB7XG4gICAgdmFyIGNoID0gc291cmNlLm5leHQoKTtcbiAgICBpZiAoY2ggPT0gJ1wiJykge1xuICAgICAgc2V0U3RhdGUobm9ybWFsKTtcbiAgICAgIHJldHVybiBcInN0cmluZ1wiO1xuICAgIH1cbiAgICBpZiAoY2ggPT0gJ1xcXFwnKSB7XG4gICAgICBpZiAoc291cmNlLmVvbCgpIHx8IHNvdXJjZS5lYXQod2hpdGVDaGFyUkUpKSB7XG4gICAgICAgIHNldFN0YXRlKHN0cmluZ0dhcCk7XG4gICAgICAgIHJldHVybiBcInN0cmluZ1wiO1xuICAgICAgfVxuICAgICAgaWYgKHNvdXJjZS5lYXQoJyYnKSkge30gZWxzZSB7XG4gICAgICAgIHNvdXJjZS5uZXh0KCk7IC8vIHNob3VsZCBoYW5kbGUgb3RoZXIgZXNjYXBlcyBoZXJlXG4gICAgICB9XG4gICAgfVxuICB9XG4gIHNldFN0YXRlKG5vcm1hbCk7XG4gIHJldHVybiBcImVycm9yXCI7XG59XG5mdW5jdGlvbiBzdHJpbmdHYXAoc291cmNlLCBzZXRTdGF0ZSkge1xuICBpZiAoc291cmNlLmVhdCgnXFxcXCcpKSB7XG4gICAgcmV0dXJuIHN3aXRjaFN0YXRlKHNvdXJjZSwgc2V0U3RhdGUsIHN0cmluZ0xpdGVyYWwpO1xuICB9XG4gIHNvdXJjZS5uZXh0KCk7XG4gIHNldFN0YXRlKG5vcm1hbCk7XG4gIHJldHVybiBcImVycm9yXCI7XG59XG52YXIgd2VsbEtub3duV29yZHMgPSBmdW5jdGlvbiAoKSB7XG4gIHZhciB3a3cgPSB7fTtcbiAgZnVuY3Rpb24gc2V0VHlwZSh0KSB7XG4gICAgcmV0dXJuIGZ1bmN0aW9uICgpIHtcbiAgICAgIGZvciAodmFyIGkgPSAwOyBpIDwgYXJndW1lbnRzLmxlbmd0aDsgaSsrKSB3a3dbYXJndW1lbnRzW2ldXSA9IHQ7XG4gICAgfTtcbiAgfVxuICBzZXRUeXBlKFwia2V5d29yZFwiKShcImNhc2VcIiwgXCJjbGFzc1wiLCBcImRhdGFcIiwgXCJkZWZhdWx0XCIsIFwiZGVyaXZpbmdcIiwgXCJkb1wiLCBcImVsc2VcIiwgXCJmb3JlaWduXCIsIFwiaWZcIiwgXCJpbXBvcnRcIiwgXCJpblwiLCBcImluZml4XCIsIFwiaW5maXhsXCIsIFwiaW5maXhyXCIsIFwiaW5zdGFuY2VcIiwgXCJsZXRcIiwgXCJtb2R1bGVcIiwgXCJuZXd0eXBlXCIsIFwib2ZcIiwgXCJ0aGVuXCIsIFwidHlwZVwiLCBcIndoZXJlXCIsIFwiX1wiKTtcbiAgc2V0VHlwZShcImtleXdvcmRcIikoXCJcXC5cXC5cIiwgXCI6XCIsIFwiOjpcIiwgXCI9XCIsIFwiXFxcXFwiLCBcIjwtXCIsIFwiLT5cIiwgXCJAXCIsIFwiflwiLCBcIj0+XCIpO1xuICBzZXRUeXBlKFwiYnVpbHRpblwiKShcIiEhXCIsIFwiJCFcIiwgXCIkXCIsIFwiJiZcIiwgXCIrXCIsIFwiKytcIiwgXCItXCIsIFwiLlwiLCBcIi9cIiwgXCIvPVwiLCBcIjxcIiwgXCI8KlwiLCBcIjw9XCIsIFwiPCQ+XCIsIFwiPCo+XCIsIFwiPTw8XCIsIFwiPT1cIiwgXCI+XCIsIFwiPj1cIiwgXCI+PlwiLCBcIj4+PVwiLCBcIl5cIiwgXCJeXlwiLCBcInx8XCIsIFwiKlwiLCBcIio+XCIsIFwiKipcIik7XG4gIHNldFR5cGUoXCJidWlsdGluXCIpKFwiQXBwbGljYXRpdmVcIiwgXCJCb29sXCIsIFwiQm91bmRlZFwiLCBcIkNoYXJcIiwgXCJEb3VibGVcIiwgXCJFUVwiLCBcIkVpdGhlclwiLCBcIkVudW1cIiwgXCJFcVwiLCBcIkZhbHNlXCIsIFwiRmlsZVBhdGhcIiwgXCJGbG9hdFwiLCBcIkZsb2F0aW5nXCIsIFwiRnJhY3Rpb25hbFwiLCBcIkZ1bmN0b3JcIiwgXCJHVFwiLCBcIklPXCIsIFwiSU9FcnJvclwiLCBcIkludFwiLCBcIkludGVnZXJcIiwgXCJJbnRlZ3JhbFwiLCBcIkp1c3RcIiwgXCJMVFwiLCBcIkxlZnRcIiwgXCJNYXliZVwiLCBcIk1vbmFkXCIsIFwiTm90aGluZ1wiLCBcIk51bVwiLCBcIk9yZFwiLCBcIk9yZGVyaW5nXCIsIFwiUmF0aW9uYWxcIiwgXCJSZWFkXCIsIFwiUmVhZFNcIiwgXCJSZWFsXCIsIFwiUmVhbEZsb2F0XCIsIFwiUmVhbEZyYWNcIiwgXCJSaWdodFwiLCBcIlNob3dcIiwgXCJTaG93U1wiLCBcIlN0cmluZ1wiLCBcIlRydWVcIik7XG4gIHNldFR5cGUoXCJidWlsdGluXCIpKFwiYWJzXCIsIFwiYWNvc1wiLCBcImFjb3NoXCIsIFwiYWxsXCIsIFwiYW5kXCIsIFwiYW55XCIsIFwiYXBwZW5kRmlsZVwiLCBcImFzVHlwZU9mXCIsIFwiYXNpblwiLCBcImFzaW5oXCIsIFwiYXRhblwiLCBcImF0YW4yXCIsIFwiYXRhbmhcIiwgXCJicmVha1wiLCBcImNhdGNoXCIsIFwiY2VpbGluZ1wiLCBcImNvbXBhcmVcIiwgXCJjb25jYXRcIiwgXCJjb25jYXRNYXBcIiwgXCJjb25zdFwiLCBcImNvc1wiLCBcImNvc2hcIiwgXCJjdXJyeVwiLCBcImN5Y2xlXCIsIFwiZGVjb2RlRmxvYXRcIiwgXCJkaXZcIiwgXCJkaXZNb2RcIiwgXCJkcm9wXCIsIFwiZHJvcFdoaWxlXCIsIFwiZWl0aGVyXCIsIFwiZWxlbVwiLCBcImVuY29kZUZsb2F0XCIsIFwiZW51bUZyb21cIiwgXCJlbnVtRnJvbVRoZW5cIiwgXCJlbnVtRnJvbVRoZW5Ub1wiLCBcImVudW1Gcm9tVG9cIiwgXCJlcnJvclwiLCBcImV2ZW5cIiwgXCJleHBcIiwgXCJleHBvbmVudFwiLCBcImZhaWxcIiwgXCJmaWx0ZXJcIiwgXCJmbGlwXCIsIFwiZmxvYXREaWdpdHNcIiwgXCJmbG9hdFJhZGl4XCIsIFwiZmxvYXRSYW5nZVwiLCBcImZsb29yXCIsIFwiZm1hcFwiLCBcImZvbGRsXCIsIFwiZm9sZGwxXCIsIFwiZm9sZHJcIiwgXCJmb2xkcjFcIiwgXCJmcm9tRW51bVwiLCBcImZyb21JbnRlZ2VyXCIsIFwiZnJvbUludGVncmFsXCIsIFwiZnJvbVJhdGlvbmFsXCIsIFwiZnN0XCIsIFwiZ2NkXCIsIFwiZ2V0Q2hhclwiLCBcImdldENvbnRlbnRzXCIsIFwiZ2V0TGluZVwiLCBcImhlYWRcIiwgXCJpZFwiLCBcImluaXRcIiwgXCJpbnRlcmFjdFwiLCBcImlvRXJyb3JcIiwgXCJpc0Rlbm9ybWFsaXplZFwiLCBcImlzSUVFRVwiLCBcImlzSW5maW5pdGVcIiwgXCJpc05hTlwiLCBcImlzTmVnYXRpdmVaZXJvXCIsIFwiaXRlcmF0ZVwiLCBcImxhc3RcIiwgXCJsY21cIiwgXCJsZW5ndGhcIiwgXCJsZXhcIiwgXCJsaW5lc1wiLCBcImxvZ1wiLCBcImxvZ0Jhc2VcIiwgXCJsb29rdXBcIiwgXCJtYXBcIiwgXCJtYXBNXCIsIFwibWFwTV9cIiwgXCJtYXhcIiwgXCJtYXhCb3VuZFwiLCBcIm1heGltdW1cIiwgXCJtYXliZVwiLCBcIm1pblwiLCBcIm1pbkJvdW5kXCIsIFwibWluaW11bVwiLCBcIm1vZFwiLCBcIm5lZ2F0ZVwiLCBcIm5vdFwiLCBcIm5vdEVsZW1cIiwgXCJudWxsXCIsIFwib2RkXCIsIFwib3JcIiwgXCJvdGhlcndpc2VcIiwgXCJwaVwiLCBcInByZWRcIiwgXCJwcmludFwiLCBcInByb2R1Y3RcIiwgXCJwcm9wZXJGcmFjdGlvblwiLCBcInB1cmVcIiwgXCJwdXRDaGFyXCIsIFwicHV0U3RyXCIsIFwicHV0U3RyTG5cIiwgXCJxdW90XCIsIFwicXVvdFJlbVwiLCBcInJlYWRcIiwgXCJyZWFkRmlsZVwiLCBcInJlYWRJT1wiLCBcInJlYWRMaXN0XCIsIFwicmVhZExuXCIsIFwicmVhZFBhcmVuXCIsIFwicmVhZHNcIiwgXCJyZWFkc1ByZWNcIiwgXCJyZWFsVG9GcmFjXCIsIFwicmVjaXBcIiwgXCJyZW1cIiwgXCJyZXBlYXRcIiwgXCJyZXBsaWNhdGVcIiwgXCJyZXR1cm5cIiwgXCJyZXZlcnNlXCIsIFwicm91bmRcIiwgXCJzY2FsZUZsb2F0XCIsIFwic2NhbmxcIiwgXCJzY2FubDFcIiwgXCJzY2FuclwiLCBcInNjYW5yMVwiLCBcInNlcVwiLCBcInNlcXVlbmNlXCIsIFwic2VxdWVuY2VfXCIsIFwic2hvd1wiLCBcInNob3dDaGFyXCIsIFwic2hvd0xpc3RcIiwgXCJzaG93UGFyZW5cIiwgXCJzaG93U3RyaW5nXCIsIFwic2hvd3NcIiwgXCJzaG93c1ByZWNcIiwgXCJzaWduaWZpY2FuZFwiLCBcInNpZ251bVwiLCBcInNpblwiLCBcInNpbmhcIiwgXCJzbmRcIiwgXCJzcGFuXCIsIFwic3BsaXRBdFwiLCBcInNxcnRcIiwgXCJzdWJ0cmFjdFwiLCBcInN1Y2NcIiwgXCJzdW1cIiwgXCJ0YWlsXCIsIFwidGFrZVwiLCBcInRha2VXaGlsZVwiLCBcInRhblwiLCBcInRhbmhcIiwgXCJ0b0VudW1cIiwgXCJ0b0ludGVnZXJcIiwgXCJ0b1JhdGlvbmFsXCIsIFwidHJ1bmNhdGVcIiwgXCJ1bmN1cnJ5XCIsIFwidW5kZWZpbmVkXCIsIFwidW5saW5lc1wiLCBcInVudGlsXCIsIFwidW53b3Jkc1wiLCBcInVuemlwXCIsIFwidW56aXAzXCIsIFwidXNlckVycm9yXCIsIFwid29yZHNcIiwgXCJ3cml0ZUZpbGVcIiwgXCJ6aXBcIiwgXCJ6aXAzXCIsIFwiemlwV2l0aFwiLCBcInppcFdpdGgzXCIpO1xuICByZXR1cm4gd2t3O1xufSgpO1xuZXhwb3J0IGNvbnN0IGhhc2tlbGwgPSB7XG4gIG5hbWU6IFwiaGFza2VsbFwiLFxuICBzdGFydFN0YXRlOiBmdW5jdGlvbiAoKSB7XG4gICAgcmV0dXJuIHtcbiAgICAgIGY6IG5vcm1hbFxuICAgIH07XG4gIH0sXG4gIGNvcHlTdGF0ZTogZnVuY3Rpb24gKHMpIHtcbiAgICByZXR1cm4ge1xuICAgICAgZjogcy5mXG4gICAgfTtcbiAgfSxcbiAgdG9rZW46IGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgdmFyIHQgPSBzdGF0ZS5mKHN0cmVhbSwgZnVuY3Rpb24gKHMpIHtcbiAgICAgIHN0YXRlLmYgPSBzO1xuICAgIH0pO1xuICAgIHZhciB3ID0gc3RyZWFtLmN1cnJlbnQoKTtcbiAgICByZXR1cm4gd2VsbEtub3duV29yZHMuaGFzT3duUHJvcGVydHkodykgPyB3ZWxsS25vd25Xb3Jkc1t3XSA6IHQ7XG4gIH0sXG4gIGxhbmd1YWdlRGF0YToge1xuICAgIGNvbW1lbnRUb2tlbnM6IHtcbiAgICAgIGxpbmU6IFwiLS1cIixcbiAgICAgIGJsb2NrOiB7XG4gICAgICAgIG9wZW46IFwiey1cIixcbiAgICAgICAgY2xvc2U6IFwiLX1cIlxuICAgICAgfVxuICAgIH1cbiAgfVxufTsiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=