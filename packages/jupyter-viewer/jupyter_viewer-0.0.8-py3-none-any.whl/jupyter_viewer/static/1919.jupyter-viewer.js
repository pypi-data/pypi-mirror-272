"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[1919],{

/***/ 21919:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "eiffel": () => (/* binding */ eiffel)
/* harmony export */ });
function wordObj(words) {
  var o = {};
  for (var i = 0, e = words.length; i < e; ++i) o[words[i]] = true;
  return o;
}
var keywords = wordObj(['note', 'across', 'when', 'variant', 'until', 'unique', 'undefine', 'then', 'strip', 'select', 'retry', 'rescue', 'require', 'rename', 'reference', 'redefine', 'prefix', 'once', 'old', 'obsolete', 'loop', 'local', 'like', 'is', 'inspect', 'infix', 'include', 'if', 'frozen', 'from', 'external', 'export', 'ensure', 'end', 'elseif', 'else', 'do', 'creation', 'create', 'check', 'alias', 'agent', 'separate', 'invariant', 'inherit', 'indexing', 'feature', 'expanded', 'deferred', 'class', 'Void', 'True', 'Result', 'Precursor', 'False', 'Current', 'create', 'attached', 'detachable', 'as', 'and', 'implies', 'not', 'or']);
var operators = wordObj([":=", "and then", "and", "or", "<<", ">>"]);
function chain(newtok, stream, state) {
  state.tokenize.push(newtok);
  return newtok(stream, state);
}
function tokenBase(stream, state) {
  if (stream.eatSpace()) return null;
  var ch = stream.next();
  if (ch == '"' || ch == "'") {
    return chain(readQuoted(ch, "string"), stream, state);
  } else if (ch == "-" && stream.eat("-")) {
    stream.skipToEnd();
    return "comment";
  } else if (ch == ":" && stream.eat("=")) {
    return "operator";
  } else if (/[0-9]/.test(ch)) {
    stream.eatWhile(/[xXbBCc0-9\.]/);
    stream.eat(/[\?\!]/);
    return "variable";
  } else if (/[a-zA-Z_0-9]/.test(ch)) {
    stream.eatWhile(/[a-zA-Z_0-9]/);
    stream.eat(/[\?\!]/);
    return "variable";
  } else if (/[=+\-\/*^%<>~]/.test(ch)) {
    stream.eatWhile(/[=+\-\/*^%<>~]/);
    return "operator";
  } else {
    return null;
  }
}
function readQuoted(quote, style, unescaped) {
  return function (stream, state) {
    var escaped = false,
      ch;
    while ((ch = stream.next()) != null) {
      if (ch == quote && (unescaped || !escaped)) {
        state.tokenize.pop();
        break;
      }
      escaped = !escaped && ch == "%";
    }
    return style;
  };
}
const eiffel = {
  name: "eiffel",
  startState: function () {
    return {
      tokenize: [tokenBase]
    };
  },
  token: function (stream, state) {
    var style = state.tokenize[state.tokenize.length - 1](stream, state);
    if (style == "variable") {
      var word = stream.current();
      style = keywords.propertyIsEnumerable(stream.current()) ? "keyword" : operators.propertyIsEnumerable(stream.current()) ? "operator" : /^[A-Z][A-Z_0-9]*$/g.test(word) ? "tag" : /^0[bB][0-1]+$/g.test(word) ? "number" : /^0[cC][0-7]+$/g.test(word) ? "number" : /^0[xX][a-fA-F0-9]+$/g.test(word) ? "number" : /^([0-9]+\.[0-9]*)|([0-9]*\.[0-9]+)$/g.test(word) ? "number" : /^[0-9]+$/g.test(word) ? "number" : "variable";
    }
    return style;
  },
  languageData: {
    commentTokens: {
      line: "--"
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiMTkxOS5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGNvZGVtaXJyb3IvbGVnYWN5LW1vZGVzL21vZGUvZWlmZmVsLmpzIl0sInNvdXJjZXNDb250ZW50IjpbImZ1bmN0aW9uIHdvcmRPYmood29yZHMpIHtcbiAgdmFyIG8gPSB7fTtcbiAgZm9yICh2YXIgaSA9IDAsIGUgPSB3b3Jkcy5sZW5ndGg7IGkgPCBlOyArK2kpIG9bd29yZHNbaV1dID0gdHJ1ZTtcbiAgcmV0dXJuIG87XG59XG52YXIga2V5d29yZHMgPSB3b3JkT2JqKFsnbm90ZScsICdhY3Jvc3MnLCAnd2hlbicsICd2YXJpYW50JywgJ3VudGlsJywgJ3VuaXF1ZScsICd1bmRlZmluZScsICd0aGVuJywgJ3N0cmlwJywgJ3NlbGVjdCcsICdyZXRyeScsICdyZXNjdWUnLCAncmVxdWlyZScsICdyZW5hbWUnLCAncmVmZXJlbmNlJywgJ3JlZGVmaW5lJywgJ3ByZWZpeCcsICdvbmNlJywgJ29sZCcsICdvYnNvbGV0ZScsICdsb29wJywgJ2xvY2FsJywgJ2xpa2UnLCAnaXMnLCAnaW5zcGVjdCcsICdpbmZpeCcsICdpbmNsdWRlJywgJ2lmJywgJ2Zyb3plbicsICdmcm9tJywgJ2V4dGVybmFsJywgJ2V4cG9ydCcsICdlbnN1cmUnLCAnZW5kJywgJ2Vsc2VpZicsICdlbHNlJywgJ2RvJywgJ2NyZWF0aW9uJywgJ2NyZWF0ZScsICdjaGVjaycsICdhbGlhcycsICdhZ2VudCcsICdzZXBhcmF0ZScsICdpbnZhcmlhbnQnLCAnaW5oZXJpdCcsICdpbmRleGluZycsICdmZWF0dXJlJywgJ2V4cGFuZGVkJywgJ2RlZmVycmVkJywgJ2NsYXNzJywgJ1ZvaWQnLCAnVHJ1ZScsICdSZXN1bHQnLCAnUHJlY3Vyc29yJywgJ0ZhbHNlJywgJ0N1cnJlbnQnLCAnY3JlYXRlJywgJ2F0dGFjaGVkJywgJ2RldGFjaGFibGUnLCAnYXMnLCAnYW5kJywgJ2ltcGxpZXMnLCAnbm90JywgJ29yJ10pO1xudmFyIG9wZXJhdG9ycyA9IHdvcmRPYmooW1wiOj1cIiwgXCJhbmQgdGhlblwiLCBcImFuZFwiLCBcIm9yXCIsIFwiPDxcIiwgXCI+PlwiXSk7XG5mdW5jdGlvbiBjaGFpbihuZXd0b2ssIHN0cmVhbSwgc3RhdGUpIHtcbiAgc3RhdGUudG9rZW5pemUucHVzaChuZXd0b2spO1xuICByZXR1cm4gbmV3dG9rKHN0cmVhbSwgc3RhdGUpO1xufVxuZnVuY3Rpb24gdG9rZW5CYXNlKHN0cmVhbSwgc3RhdGUpIHtcbiAgaWYgKHN0cmVhbS5lYXRTcGFjZSgpKSByZXR1cm4gbnVsbDtcbiAgdmFyIGNoID0gc3RyZWFtLm5leHQoKTtcbiAgaWYgKGNoID09ICdcIicgfHwgY2ggPT0gXCInXCIpIHtcbiAgICByZXR1cm4gY2hhaW4ocmVhZFF1b3RlZChjaCwgXCJzdHJpbmdcIiksIHN0cmVhbSwgc3RhdGUpO1xuICB9IGVsc2UgaWYgKGNoID09IFwiLVwiICYmIHN0cmVhbS5lYXQoXCItXCIpKSB7XG4gICAgc3RyZWFtLnNraXBUb0VuZCgpO1xuICAgIHJldHVybiBcImNvbW1lbnRcIjtcbiAgfSBlbHNlIGlmIChjaCA9PSBcIjpcIiAmJiBzdHJlYW0uZWF0KFwiPVwiKSkge1xuICAgIHJldHVybiBcIm9wZXJhdG9yXCI7XG4gIH0gZWxzZSBpZiAoL1swLTldLy50ZXN0KGNoKSkge1xuICAgIHN0cmVhbS5lYXRXaGlsZSgvW3hYYkJDYzAtOVxcLl0vKTtcbiAgICBzdHJlYW0uZWF0KC9bXFw/XFwhXS8pO1xuICAgIHJldHVybiBcInZhcmlhYmxlXCI7XG4gIH0gZWxzZSBpZiAoL1thLXpBLVpfMC05XS8udGVzdChjaCkpIHtcbiAgICBzdHJlYW0uZWF0V2hpbGUoL1thLXpBLVpfMC05XS8pO1xuICAgIHN0cmVhbS5lYXQoL1tcXD9cXCFdLyk7XG4gICAgcmV0dXJuIFwidmFyaWFibGVcIjtcbiAgfSBlbHNlIGlmICgvWz0rXFwtXFwvKl4lPD5+XS8udGVzdChjaCkpIHtcbiAgICBzdHJlYW0uZWF0V2hpbGUoL1s9K1xcLVxcLypeJTw+fl0vKTtcbiAgICByZXR1cm4gXCJvcGVyYXRvclwiO1xuICB9IGVsc2Uge1xuICAgIHJldHVybiBudWxsO1xuICB9XG59XG5mdW5jdGlvbiByZWFkUXVvdGVkKHF1b3RlLCBzdHlsZSwgdW5lc2NhcGVkKSB7XG4gIHJldHVybiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIHZhciBlc2NhcGVkID0gZmFsc2UsXG4gICAgICBjaDtcbiAgICB3aGlsZSAoKGNoID0gc3RyZWFtLm5leHQoKSkgIT0gbnVsbCkge1xuICAgICAgaWYgKGNoID09IHF1b3RlICYmICh1bmVzY2FwZWQgfHwgIWVzY2FwZWQpKSB7XG4gICAgICAgIHN0YXRlLnRva2VuaXplLnBvcCgpO1xuICAgICAgICBicmVhaztcbiAgICAgIH1cbiAgICAgIGVzY2FwZWQgPSAhZXNjYXBlZCAmJiBjaCA9PSBcIiVcIjtcbiAgICB9XG4gICAgcmV0dXJuIHN0eWxlO1xuICB9O1xufVxuZXhwb3J0IGNvbnN0IGVpZmZlbCA9IHtcbiAgbmFtZTogXCJlaWZmZWxcIixcbiAgc3RhcnRTdGF0ZTogZnVuY3Rpb24gKCkge1xuICAgIHJldHVybiB7XG4gICAgICB0b2tlbml6ZTogW3Rva2VuQmFzZV1cbiAgICB9O1xuICB9LFxuICB0b2tlbjogZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICB2YXIgc3R5bGUgPSBzdGF0ZS50b2tlbml6ZVtzdGF0ZS50b2tlbml6ZS5sZW5ndGggLSAxXShzdHJlYW0sIHN0YXRlKTtcbiAgICBpZiAoc3R5bGUgPT0gXCJ2YXJpYWJsZVwiKSB7XG4gICAgICB2YXIgd29yZCA9IHN0cmVhbS5jdXJyZW50KCk7XG4gICAgICBzdHlsZSA9IGtleXdvcmRzLnByb3BlcnR5SXNFbnVtZXJhYmxlKHN0cmVhbS5jdXJyZW50KCkpID8gXCJrZXl3b3JkXCIgOiBvcGVyYXRvcnMucHJvcGVydHlJc0VudW1lcmFibGUoc3RyZWFtLmN1cnJlbnQoKSkgPyBcIm9wZXJhdG9yXCIgOiAvXltBLVpdW0EtWl8wLTldKiQvZy50ZXN0KHdvcmQpID8gXCJ0YWdcIiA6IC9eMFtiQl1bMC0xXSskL2cudGVzdCh3b3JkKSA/IFwibnVtYmVyXCIgOiAvXjBbY0NdWzAtN10rJC9nLnRlc3Qod29yZCkgPyBcIm51bWJlclwiIDogL14wW3hYXVthLWZBLUYwLTldKyQvZy50ZXN0KHdvcmQpID8gXCJudW1iZXJcIiA6IC9eKFswLTldK1xcLlswLTldKil8KFswLTldKlxcLlswLTldKykkL2cudGVzdCh3b3JkKSA/IFwibnVtYmVyXCIgOiAvXlswLTldKyQvZy50ZXN0KHdvcmQpID8gXCJudW1iZXJcIiA6IFwidmFyaWFibGVcIjtcbiAgICB9XG4gICAgcmV0dXJuIHN0eWxlO1xuICB9LFxuICBsYW5ndWFnZURhdGE6IHtcbiAgICBjb21tZW50VG9rZW5zOiB7XG4gICAgICBsaW5lOiBcIi0tXCJcbiAgICB9XG4gIH1cbn07Il0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9