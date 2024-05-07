"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[5749],{

/***/ 85749:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "velocity": () => (/* binding */ velocity)
/* harmony export */ });
function parseWords(str) {
  var obj = {},
    words = str.split(" ");
  for (var i = 0; i < words.length; ++i) obj[words[i]] = true;
  return obj;
}
var keywords = parseWords("#end #else #break #stop #[[ #]] " + "#{end} #{else} #{break} #{stop}");
var functions = parseWords("#if #elseif #foreach #set #include #parse #macro #define #evaluate " + "#{if} #{elseif} #{foreach} #{set} #{include} #{parse} #{macro} #{define} #{evaluate}");
var specials = parseWords("$foreach.count $foreach.hasNext $foreach.first $foreach.last $foreach.topmost $foreach.parent.count $foreach.parent.hasNext $foreach.parent.first $foreach.parent.last $foreach.parent $velocityCount $!bodyContent $bodyContent");
var isOperatorChar = /[+\-*&%=<>!?:\/|]/;
function chain(stream, state, f) {
  state.tokenize = f;
  return f(stream, state);
}
function tokenBase(stream, state) {
  var beforeParams = state.beforeParams;
  state.beforeParams = false;
  var ch = stream.next();
  // start of unparsed string?
  if (ch == "'" && !state.inString && state.inParams) {
    state.lastTokenWasBuiltin = false;
    return chain(stream, state, tokenString(ch));
  }
  // start of parsed string?
  else if (ch == '"') {
    state.lastTokenWasBuiltin = false;
    if (state.inString) {
      state.inString = false;
      return "string";
    } else if (state.inParams) return chain(stream, state, tokenString(ch));
  }
  // is it one of the special signs []{}().,;? Separator?
  else if (/[\[\]{}\(\),;\.]/.test(ch)) {
    if (ch == "(" && beforeParams) state.inParams = true;else if (ch == ")") {
      state.inParams = false;
      state.lastTokenWasBuiltin = true;
    }
    return null;
  }
  // start of a number value?
  else if (/\d/.test(ch)) {
    state.lastTokenWasBuiltin = false;
    stream.eatWhile(/[\w\.]/);
    return "number";
  }
  // multi line comment?
  else if (ch == "#" && stream.eat("*")) {
    state.lastTokenWasBuiltin = false;
    return chain(stream, state, tokenComment);
  }
  // unparsed content?
  else if (ch == "#" && stream.match(/ *\[ *\[/)) {
    state.lastTokenWasBuiltin = false;
    return chain(stream, state, tokenUnparsed);
  }
  // single line comment?
  else if (ch == "#" && stream.eat("#")) {
    state.lastTokenWasBuiltin = false;
    stream.skipToEnd();
    return "comment";
  }
  // variable?
  else if (ch == "$") {
    stream.eat("!");
    stream.eatWhile(/[\w\d\$_\.{}-]/);
    // is it one of the specials?
    if (specials && specials.propertyIsEnumerable(stream.current())) {
      return "keyword";
    } else {
      state.lastTokenWasBuiltin = true;
      state.beforeParams = true;
      return "builtin";
    }
  }
  // is it a operator?
  else if (isOperatorChar.test(ch)) {
    state.lastTokenWasBuiltin = false;
    stream.eatWhile(isOperatorChar);
    return "operator";
  } else {
    // get the whole word
    stream.eatWhile(/[\w\$_{}@]/);
    var word = stream.current();
    // is it one of the listed keywords?
    if (keywords && keywords.propertyIsEnumerable(word)) return "keyword";
    // is it one of the listed functions?
    if (functions && functions.propertyIsEnumerable(word) || stream.current().match(/^#@?[a-z0-9_]+ *$/i) && stream.peek() == "(" && !(functions && functions.propertyIsEnumerable(word.toLowerCase()))) {
      state.beforeParams = true;
      state.lastTokenWasBuiltin = false;
      return "keyword";
    }
    if (state.inString) {
      state.lastTokenWasBuiltin = false;
      return "string";
    }
    if (stream.pos > word.length && stream.string.charAt(stream.pos - word.length - 1) == "." && state.lastTokenWasBuiltin) return "builtin";
    // default: just a "word"
    state.lastTokenWasBuiltin = false;
    return null;
  }
}
function tokenString(quote) {
  return function (stream, state) {
    var escaped = false,
      next,
      end = false;
    while ((next = stream.next()) != null) {
      if (next == quote && !escaped) {
        end = true;
        break;
      }
      if (quote == '"' && stream.peek() == '$' && !escaped) {
        state.inString = true;
        end = true;
        break;
      }
      escaped = !escaped && next == "\\";
    }
    if (end) state.tokenize = tokenBase;
    return "string";
  };
}
function tokenComment(stream, state) {
  var maybeEnd = false,
    ch;
  while (ch = stream.next()) {
    if (ch == "#" && maybeEnd) {
      state.tokenize = tokenBase;
      break;
    }
    maybeEnd = ch == "*";
  }
  return "comment";
}
function tokenUnparsed(stream, state) {
  var maybeEnd = 0,
    ch;
  while (ch = stream.next()) {
    if (ch == "#" && maybeEnd == 2) {
      state.tokenize = tokenBase;
      break;
    }
    if (ch == "]") maybeEnd++;else if (ch != " ") maybeEnd = 0;
  }
  return "meta";
}
// Interface

const velocity = {
  name: "velocity",
  startState: function () {
    return {
      tokenize: tokenBase,
      beforeParams: false,
      inParams: false,
      inString: false,
      lastTokenWasBuiltin: false
    };
  },
  token: function (stream, state) {
    if (stream.eatSpace()) return null;
    return state.tokenize(stream, state);
  },
  languageData: {
    commentTokens: {
      line: "##",
      block: {
        open: "#*",
        close: "*#"
      }
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNTc0OS5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGNvZGVtaXJyb3IvbGVnYWN5LW1vZGVzL21vZGUvdmVsb2NpdHkuanMiXSwic291cmNlc0NvbnRlbnQiOlsiZnVuY3Rpb24gcGFyc2VXb3JkcyhzdHIpIHtcbiAgdmFyIG9iaiA9IHt9LFxuICAgIHdvcmRzID0gc3RyLnNwbGl0KFwiIFwiKTtcbiAgZm9yICh2YXIgaSA9IDA7IGkgPCB3b3Jkcy5sZW5ndGg7ICsraSkgb2JqW3dvcmRzW2ldXSA9IHRydWU7XG4gIHJldHVybiBvYmo7XG59XG52YXIga2V5d29yZHMgPSBwYXJzZVdvcmRzKFwiI2VuZCAjZWxzZSAjYnJlYWsgI3N0b3AgI1tbICNdXSBcIiArIFwiI3tlbmR9ICN7ZWxzZX0gI3ticmVha30gI3tzdG9wfVwiKTtcbnZhciBmdW5jdGlvbnMgPSBwYXJzZVdvcmRzKFwiI2lmICNlbHNlaWYgI2ZvcmVhY2ggI3NldCAjaW5jbHVkZSAjcGFyc2UgI21hY3JvICNkZWZpbmUgI2V2YWx1YXRlIFwiICsgXCIje2lmfSAje2Vsc2VpZn0gI3tmb3JlYWNofSAje3NldH0gI3tpbmNsdWRlfSAje3BhcnNlfSAje21hY3JvfSAje2RlZmluZX0gI3tldmFsdWF0ZX1cIik7XG52YXIgc3BlY2lhbHMgPSBwYXJzZVdvcmRzKFwiJGZvcmVhY2guY291bnQgJGZvcmVhY2guaGFzTmV4dCAkZm9yZWFjaC5maXJzdCAkZm9yZWFjaC5sYXN0ICRmb3JlYWNoLnRvcG1vc3QgJGZvcmVhY2gucGFyZW50LmNvdW50ICRmb3JlYWNoLnBhcmVudC5oYXNOZXh0ICRmb3JlYWNoLnBhcmVudC5maXJzdCAkZm9yZWFjaC5wYXJlbnQubGFzdCAkZm9yZWFjaC5wYXJlbnQgJHZlbG9jaXR5Q291bnQgJCFib2R5Q29udGVudCAkYm9keUNvbnRlbnRcIik7XG52YXIgaXNPcGVyYXRvckNoYXIgPSAvWytcXC0qJiU9PD4hPzpcXC98XS87XG5mdW5jdGlvbiBjaGFpbihzdHJlYW0sIHN0YXRlLCBmKSB7XG4gIHN0YXRlLnRva2VuaXplID0gZjtcbiAgcmV0dXJuIGYoc3RyZWFtLCBzdGF0ZSk7XG59XG5mdW5jdGlvbiB0b2tlbkJhc2Uoc3RyZWFtLCBzdGF0ZSkge1xuICB2YXIgYmVmb3JlUGFyYW1zID0gc3RhdGUuYmVmb3JlUGFyYW1zO1xuICBzdGF0ZS5iZWZvcmVQYXJhbXMgPSBmYWxzZTtcbiAgdmFyIGNoID0gc3RyZWFtLm5leHQoKTtcbiAgLy8gc3RhcnQgb2YgdW5wYXJzZWQgc3RyaW5nP1xuICBpZiAoY2ggPT0gXCInXCIgJiYgIXN0YXRlLmluU3RyaW5nICYmIHN0YXRlLmluUGFyYW1zKSB7XG4gICAgc3RhdGUubGFzdFRva2VuV2FzQnVpbHRpbiA9IGZhbHNlO1xuICAgIHJldHVybiBjaGFpbihzdHJlYW0sIHN0YXRlLCB0b2tlblN0cmluZyhjaCkpO1xuICB9XG4gIC8vIHN0YXJ0IG9mIHBhcnNlZCBzdHJpbmc/XG4gIGVsc2UgaWYgKGNoID09ICdcIicpIHtcbiAgICBzdGF0ZS5sYXN0VG9rZW5XYXNCdWlsdGluID0gZmFsc2U7XG4gICAgaWYgKHN0YXRlLmluU3RyaW5nKSB7XG4gICAgICBzdGF0ZS5pblN0cmluZyA9IGZhbHNlO1xuICAgICAgcmV0dXJuIFwic3RyaW5nXCI7XG4gICAgfSBlbHNlIGlmIChzdGF0ZS5pblBhcmFtcykgcmV0dXJuIGNoYWluKHN0cmVhbSwgc3RhdGUsIHRva2VuU3RyaW5nKGNoKSk7XG4gIH1cbiAgLy8gaXMgaXQgb25lIG9mIHRoZSBzcGVjaWFsIHNpZ25zIFtde30oKS4sOz8gU2VwYXJhdG9yP1xuICBlbHNlIGlmICgvW1xcW1xcXXt9XFwoXFwpLDtcXC5dLy50ZXN0KGNoKSkge1xuICAgIGlmIChjaCA9PSBcIihcIiAmJiBiZWZvcmVQYXJhbXMpIHN0YXRlLmluUGFyYW1zID0gdHJ1ZTtlbHNlIGlmIChjaCA9PSBcIilcIikge1xuICAgICAgc3RhdGUuaW5QYXJhbXMgPSBmYWxzZTtcbiAgICAgIHN0YXRlLmxhc3RUb2tlbldhc0J1aWx0aW4gPSB0cnVlO1xuICAgIH1cbiAgICByZXR1cm4gbnVsbDtcbiAgfVxuICAvLyBzdGFydCBvZiBhIG51bWJlciB2YWx1ZT9cbiAgZWxzZSBpZiAoL1xcZC8udGVzdChjaCkpIHtcbiAgICBzdGF0ZS5sYXN0VG9rZW5XYXNCdWlsdGluID0gZmFsc2U7XG4gICAgc3RyZWFtLmVhdFdoaWxlKC9bXFx3XFwuXS8pO1xuICAgIHJldHVybiBcIm51bWJlclwiO1xuICB9XG4gIC8vIG11bHRpIGxpbmUgY29tbWVudD9cbiAgZWxzZSBpZiAoY2ggPT0gXCIjXCIgJiYgc3RyZWFtLmVhdChcIipcIikpIHtcbiAgICBzdGF0ZS5sYXN0VG9rZW5XYXNCdWlsdGluID0gZmFsc2U7XG4gICAgcmV0dXJuIGNoYWluKHN0cmVhbSwgc3RhdGUsIHRva2VuQ29tbWVudCk7XG4gIH1cbiAgLy8gdW5wYXJzZWQgY29udGVudD9cbiAgZWxzZSBpZiAoY2ggPT0gXCIjXCIgJiYgc3RyZWFtLm1hdGNoKC8gKlxcWyAqXFxbLykpIHtcbiAgICBzdGF0ZS5sYXN0VG9rZW5XYXNCdWlsdGluID0gZmFsc2U7XG4gICAgcmV0dXJuIGNoYWluKHN0cmVhbSwgc3RhdGUsIHRva2VuVW5wYXJzZWQpO1xuICB9XG4gIC8vIHNpbmdsZSBsaW5lIGNvbW1lbnQ/XG4gIGVsc2UgaWYgKGNoID09IFwiI1wiICYmIHN0cmVhbS5lYXQoXCIjXCIpKSB7XG4gICAgc3RhdGUubGFzdFRva2VuV2FzQnVpbHRpbiA9IGZhbHNlO1xuICAgIHN0cmVhbS5za2lwVG9FbmQoKTtcbiAgICByZXR1cm4gXCJjb21tZW50XCI7XG4gIH1cbiAgLy8gdmFyaWFibGU/XG4gIGVsc2UgaWYgKGNoID09IFwiJFwiKSB7XG4gICAgc3RyZWFtLmVhdChcIiFcIik7XG4gICAgc3RyZWFtLmVhdFdoaWxlKC9bXFx3XFxkXFwkX1xcLnt9LV0vKTtcbiAgICAvLyBpcyBpdCBvbmUgb2YgdGhlIHNwZWNpYWxzP1xuICAgIGlmIChzcGVjaWFscyAmJiBzcGVjaWFscy5wcm9wZXJ0eUlzRW51bWVyYWJsZShzdHJlYW0uY3VycmVudCgpKSkge1xuICAgICAgcmV0dXJuIFwia2V5d29yZFwiO1xuICAgIH0gZWxzZSB7XG4gICAgICBzdGF0ZS5sYXN0VG9rZW5XYXNCdWlsdGluID0gdHJ1ZTtcbiAgICAgIHN0YXRlLmJlZm9yZVBhcmFtcyA9IHRydWU7XG4gICAgICByZXR1cm4gXCJidWlsdGluXCI7XG4gICAgfVxuICB9XG4gIC8vIGlzIGl0IGEgb3BlcmF0b3I/XG4gIGVsc2UgaWYgKGlzT3BlcmF0b3JDaGFyLnRlc3QoY2gpKSB7XG4gICAgc3RhdGUubGFzdFRva2VuV2FzQnVpbHRpbiA9IGZhbHNlO1xuICAgIHN0cmVhbS5lYXRXaGlsZShpc09wZXJhdG9yQ2hhcik7XG4gICAgcmV0dXJuIFwib3BlcmF0b3JcIjtcbiAgfSBlbHNlIHtcbiAgICAvLyBnZXQgdGhlIHdob2xlIHdvcmRcbiAgICBzdHJlYW0uZWF0V2hpbGUoL1tcXHdcXCRfe31AXS8pO1xuICAgIHZhciB3b3JkID0gc3RyZWFtLmN1cnJlbnQoKTtcbiAgICAvLyBpcyBpdCBvbmUgb2YgdGhlIGxpc3RlZCBrZXl3b3Jkcz9cbiAgICBpZiAoa2V5d29yZHMgJiYga2V5d29yZHMucHJvcGVydHlJc0VudW1lcmFibGUod29yZCkpIHJldHVybiBcImtleXdvcmRcIjtcbiAgICAvLyBpcyBpdCBvbmUgb2YgdGhlIGxpc3RlZCBmdW5jdGlvbnM/XG4gICAgaWYgKGZ1bmN0aW9ucyAmJiBmdW5jdGlvbnMucHJvcGVydHlJc0VudW1lcmFibGUod29yZCkgfHwgc3RyZWFtLmN1cnJlbnQoKS5tYXRjaCgvXiNAP1thLXowLTlfXSsgKiQvaSkgJiYgc3RyZWFtLnBlZWsoKSA9PSBcIihcIiAmJiAhKGZ1bmN0aW9ucyAmJiBmdW5jdGlvbnMucHJvcGVydHlJc0VudW1lcmFibGUod29yZC50b0xvd2VyQ2FzZSgpKSkpIHtcbiAgICAgIHN0YXRlLmJlZm9yZVBhcmFtcyA9IHRydWU7XG4gICAgICBzdGF0ZS5sYXN0VG9rZW5XYXNCdWlsdGluID0gZmFsc2U7XG4gICAgICByZXR1cm4gXCJrZXl3b3JkXCI7XG4gICAgfVxuICAgIGlmIChzdGF0ZS5pblN0cmluZykge1xuICAgICAgc3RhdGUubGFzdFRva2VuV2FzQnVpbHRpbiA9IGZhbHNlO1xuICAgICAgcmV0dXJuIFwic3RyaW5nXCI7XG4gICAgfVxuICAgIGlmIChzdHJlYW0ucG9zID4gd29yZC5sZW5ndGggJiYgc3RyZWFtLnN0cmluZy5jaGFyQXQoc3RyZWFtLnBvcyAtIHdvcmQubGVuZ3RoIC0gMSkgPT0gXCIuXCIgJiYgc3RhdGUubGFzdFRva2VuV2FzQnVpbHRpbikgcmV0dXJuIFwiYnVpbHRpblwiO1xuICAgIC8vIGRlZmF1bHQ6IGp1c3QgYSBcIndvcmRcIlxuICAgIHN0YXRlLmxhc3RUb2tlbldhc0J1aWx0aW4gPSBmYWxzZTtcbiAgICByZXR1cm4gbnVsbDtcbiAgfVxufVxuZnVuY3Rpb24gdG9rZW5TdHJpbmcocXVvdGUpIHtcbiAgcmV0dXJuIGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgdmFyIGVzY2FwZWQgPSBmYWxzZSxcbiAgICAgIG5leHQsXG4gICAgICBlbmQgPSBmYWxzZTtcbiAgICB3aGlsZSAoKG5leHQgPSBzdHJlYW0ubmV4dCgpKSAhPSBudWxsKSB7XG4gICAgICBpZiAobmV4dCA9PSBxdW90ZSAmJiAhZXNjYXBlZCkge1xuICAgICAgICBlbmQgPSB0cnVlO1xuICAgICAgICBicmVhaztcbiAgICAgIH1cbiAgICAgIGlmIChxdW90ZSA9PSAnXCInICYmIHN0cmVhbS5wZWVrKCkgPT0gJyQnICYmICFlc2NhcGVkKSB7XG4gICAgICAgIHN0YXRlLmluU3RyaW5nID0gdHJ1ZTtcbiAgICAgICAgZW5kID0gdHJ1ZTtcbiAgICAgICAgYnJlYWs7XG4gICAgICB9XG4gICAgICBlc2NhcGVkID0gIWVzY2FwZWQgJiYgbmV4dCA9PSBcIlxcXFxcIjtcbiAgICB9XG4gICAgaWYgKGVuZCkgc3RhdGUudG9rZW5pemUgPSB0b2tlbkJhc2U7XG4gICAgcmV0dXJuIFwic3RyaW5nXCI7XG4gIH07XG59XG5mdW5jdGlvbiB0b2tlbkNvbW1lbnQoc3RyZWFtLCBzdGF0ZSkge1xuICB2YXIgbWF5YmVFbmQgPSBmYWxzZSxcbiAgICBjaDtcbiAgd2hpbGUgKGNoID0gc3RyZWFtLm5leHQoKSkge1xuICAgIGlmIChjaCA9PSBcIiNcIiAmJiBtYXliZUVuZCkge1xuICAgICAgc3RhdGUudG9rZW5pemUgPSB0b2tlbkJhc2U7XG4gICAgICBicmVhaztcbiAgICB9XG4gICAgbWF5YmVFbmQgPSBjaCA9PSBcIipcIjtcbiAgfVxuICByZXR1cm4gXCJjb21tZW50XCI7XG59XG5mdW5jdGlvbiB0b2tlblVucGFyc2VkKHN0cmVhbSwgc3RhdGUpIHtcbiAgdmFyIG1heWJlRW5kID0gMCxcbiAgICBjaDtcbiAgd2hpbGUgKGNoID0gc3RyZWFtLm5leHQoKSkge1xuICAgIGlmIChjaCA9PSBcIiNcIiAmJiBtYXliZUVuZCA9PSAyKSB7XG4gICAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQmFzZTtcbiAgICAgIGJyZWFrO1xuICAgIH1cbiAgICBpZiAoY2ggPT0gXCJdXCIpIG1heWJlRW5kKys7ZWxzZSBpZiAoY2ggIT0gXCIgXCIpIG1heWJlRW5kID0gMDtcbiAgfVxuICByZXR1cm4gXCJtZXRhXCI7XG59XG4vLyBJbnRlcmZhY2VcblxuZXhwb3J0IGNvbnN0IHZlbG9jaXR5ID0ge1xuICBuYW1lOiBcInZlbG9jaXR5XCIsXG4gIHN0YXJ0U3RhdGU6IGZ1bmN0aW9uICgpIHtcbiAgICByZXR1cm4ge1xuICAgICAgdG9rZW5pemU6IHRva2VuQmFzZSxcbiAgICAgIGJlZm9yZVBhcmFtczogZmFsc2UsXG4gICAgICBpblBhcmFtczogZmFsc2UsXG4gICAgICBpblN0cmluZzogZmFsc2UsXG4gICAgICBsYXN0VG9rZW5XYXNCdWlsdGluOiBmYWxzZVxuICAgIH07XG4gIH0sXG4gIHRva2VuOiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIGlmIChzdHJlYW0uZWF0U3BhY2UoKSkgcmV0dXJuIG51bGw7XG4gICAgcmV0dXJuIHN0YXRlLnRva2VuaXplKHN0cmVhbSwgc3RhdGUpO1xuICB9LFxuICBsYW5ndWFnZURhdGE6IHtcbiAgICBjb21tZW50VG9rZW5zOiB7XG4gICAgICBsaW5lOiBcIiMjXCIsXG4gICAgICBibG9jazoge1xuICAgICAgICBvcGVuOiBcIiMqXCIsXG4gICAgICAgIGNsb3NlOiBcIiojXCJcbiAgICAgIH1cbiAgICB9XG4gIH1cbn07Il0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9