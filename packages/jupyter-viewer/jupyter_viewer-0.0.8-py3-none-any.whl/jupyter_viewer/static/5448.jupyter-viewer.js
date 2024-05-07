"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[5448],{

/***/ 75448:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "tcl": () => (/* binding */ tcl)
/* harmony export */ });
function parseWords(str) {
  var obj = {},
    words = str.split(" ");
  for (var i = 0; i < words.length; ++i) obj[words[i]] = true;
  return obj;
}
var keywords = parseWords("Tcl safe after append array auto_execok auto_import auto_load " + "auto_mkindex auto_mkindex_old auto_qualify auto_reset bgerror " + "binary break catch cd close concat continue dde eof encoding error " + "eval exec exit expr fblocked fconfigure fcopy file fileevent filename " + "filename flush for foreach format gets glob global history http if " + "incr info interp join lappend lindex linsert list llength load lrange " + "lreplace lsearch lset lsort memory msgcat namespace open package parray " + "pid pkg::create pkg_mkIndex proc puts pwd re_syntax read regex regexp " + "registry regsub rename resource return scan seek set socket source split " + "string subst switch tcl_endOfWord tcl_findLibrary tcl_startOfNextWord " + "tcl_wordBreakAfter tcl_startOfPreviousWord tcl_wordBreakBefore tcltest " + "tclvars tell time trace unknown unset update uplevel upvar variable " + "vwait");
var functions = parseWords("if elseif else and not or eq ne in ni for foreach while switch");
var isOperatorChar = /[+\-*&%=<>!?^\/\|]/;
function chain(stream, state, f) {
  state.tokenize = f;
  return f(stream, state);
}
function tokenBase(stream, state) {
  var beforeParams = state.beforeParams;
  state.beforeParams = false;
  var ch = stream.next();
  if ((ch == '"' || ch == "'") && state.inParams) {
    return chain(stream, state, tokenString(ch));
  } else if (/[\[\]{}\(\),;\.]/.test(ch)) {
    if (ch == "(" && beforeParams) state.inParams = true;else if (ch == ")") state.inParams = false;
    return null;
  } else if (/\d/.test(ch)) {
    stream.eatWhile(/[\w\.]/);
    return "number";
  } else if (ch == "#") {
    if (stream.eat("*")) return chain(stream, state, tokenComment);
    if (ch == "#" && stream.match(/ *\[ *\[/)) return chain(stream, state, tokenUnparsed);
    stream.skipToEnd();
    return "comment";
  } else if (ch == '"') {
    stream.skipTo(/"/);
    return "comment";
  } else if (ch == "$") {
    stream.eatWhile(/[$_a-z0-9A-Z\.{:]/);
    stream.eatWhile(/}/);
    state.beforeParams = true;
    return "builtin";
  } else if (isOperatorChar.test(ch)) {
    stream.eatWhile(isOperatorChar);
    return "comment";
  } else {
    stream.eatWhile(/[\w\$_{}\xa1-\uffff]/);
    var word = stream.current().toLowerCase();
    if (keywords && keywords.propertyIsEnumerable(word)) return "keyword";
    if (functions && functions.propertyIsEnumerable(word)) {
      state.beforeParams = true;
      return "keyword";
    }
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
const tcl = {
  name: "tcl",
  startState: function () {
    return {
      tokenize: tokenBase,
      beforeParams: false,
      inParams: false
    };
  },
  token: function (stream, state) {
    if (stream.eatSpace()) return null;
    return state.tokenize(stream, state);
  },
  languageData: {
    commentTokens: {
      line: "#"
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNTQ0OC5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9AY29kZW1pcnJvci9sZWdhY3ktbW9kZXMvbW9kZS90Y2wuanMiXSwic291cmNlc0NvbnRlbnQiOlsiZnVuY3Rpb24gcGFyc2VXb3JkcyhzdHIpIHtcbiAgdmFyIG9iaiA9IHt9LFxuICAgIHdvcmRzID0gc3RyLnNwbGl0KFwiIFwiKTtcbiAgZm9yICh2YXIgaSA9IDA7IGkgPCB3b3Jkcy5sZW5ndGg7ICsraSkgb2JqW3dvcmRzW2ldXSA9IHRydWU7XG4gIHJldHVybiBvYmo7XG59XG52YXIga2V5d29yZHMgPSBwYXJzZVdvcmRzKFwiVGNsIHNhZmUgYWZ0ZXIgYXBwZW5kIGFycmF5IGF1dG9fZXhlY29rIGF1dG9faW1wb3J0IGF1dG9fbG9hZCBcIiArIFwiYXV0b19ta2luZGV4IGF1dG9fbWtpbmRleF9vbGQgYXV0b19xdWFsaWZ5IGF1dG9fcmVzZXQgYmdlcnJvciBcIiArIFwiYmluYXJ5IGJyZWFrIGNhdGNoIGNkIGNsb3NlIGNvbmNhdCBjb250aW51ZSBkZGUgZW9mIGVuY29kaW5nIGVycm9yIFwiICsgXCJldmFsIGV4ZWMgZXhpdCBleHByIGZibG9ja2VkIGZjb25maWd1cmUgZmNvcHkgZmlsZSBmaWxlZXZlbnQgZmlsZW5hbWUgXCIgKyBcImZpbGVuYW1lIGZsdXNoIGZvciBmb3JlYWNoIGZvcm1hdCBnZXRzIGdsb2IgZ2xvYmFsIGhpc3RvcnkgaHR0cCBpZiBcIiArIFwiaW5jciBpbmZvIGludGVycCBqb2luIGxhcHBlbmQgbGluZGV4IGxpbnNlcnQgbGlzdCBsbGVuZ3RoIGxvYWQgbHJhbmdlIFwiICsgXCJscmVwbGFjZSBsc2VhcmNoIGxzZXQgbHNvcnQgbWVtb3J5IG1zZ2NhdCBuYW1lc3BhY2Ugb3BlbiBwYWNrYWdlIHBhcnJheSBcIiArIFwicGlkIHBrZzo6Y3JlYXRlIHBrZ19ta0luZGV4IHByb2MgcHV0cyBwd2QgcmVfc3ludGF4IHJlYWQgcmVnZXggcmVnZXhwIFwiICsgXCJyZWdpc3RyeSByZWdzdWIgcmVuYW1lIHJlc291cmNlIHJldHVybiBzY2FuIHNlZWsgc2V0IHNvY2tldCBzb3VyY2Ugc3BsaXQgXCIgKyBcInN0cmluZyBzdWJzdCBzd2l0Y2ggdGNsX2VuZE9mV29yZCB0Y2xfZmluZExpYnJhcnkgdGNsX3N0YXJ0T2ZOZXh0V29yZCBcIiArIFwidGNsX3dvcmRCcmVha0FmdGVyIHRjbF9zdGFydE9mUHJldmlvdXNXb3JkIHRjbF93b3JkQnJlYWtCZWZvcmUgdGNsdGVzdCBcIiArIFwidGNsdmFycyB0ZWxsIHRpbWUgdHJhY2UgdW5rbm93biB1bnNldCB1cGRhdGUgdXBsZXZlbCB1cHZhciB2YXJpYWJsZSBcIiArIFwidndhaXRcIik7XG52YXIgZnVuY3Rpb25zID0gcGFyc2VXb3JkcyhcImlmIGVsc2VpZiBlbHNlIGFuZCBub3Qgb3IgZXEgbmUgaW4gbmkgZm9yIGZvcmVhY2ggd2hpbGUgc3dpdGNoXCIpO1xudmFyIGlzT3BlcmF0b3JDaGFyID0gL1srXFwtKiYlPTw+IT9eXFwvXFx8XS87XG5mdW5jdGlvbiBjaGFpbihzdHJlYW0sIHN0YXRlLCBmKSB7XG4gIHN0YXRlLnRva2VuaXplID0gZjtcbiAgcmV0dXJuIGYoc3RyZWFtLCBzdGF0ZSk7XG59XG5mdW5jdGlvbiB0b2tlbkJhc2Uoc3RyZWFtLCBzdGF0ZSkge1xuICB2YXIgYmVmb3JlUGFyYW1zID0gc3RhdGUuYmVmb3JlUGFyYW1zO1xuICBzdGF0ZS5iZWZvcmVQYXJhbXMgPSBmYWxzZTtcbiAgdmFyIGNoID0gc3RyZWFtLm5leHQoKTtcbiAgaWYgKChjaCA9PSAnXCInIHx8IGNoID09IFwiJ1wiKSAmJiBzdGF0ZS5pblBhcmFtcykge1xuICAgIHJldHVybiBjaGFpbihzdHJlYW0sIHN0YXRlLCB0b2tlblN0cmluZyhjaCkpO1xuICB9IGVsc2UgaWYgKC9bXFxbXFxde31cXChcXCksO1xcLl0vLnRlc3QoY2gpKSB7XG4gICAgaWYgKGNoID09IFwiKFwiICYmIGJlZm9yZVBhcmFtcykgc3RhdGUuaW5QYXJhbXMgPSB0cnVlO2Vsc2UgaWYgKGNoID09IFwiKVwiKSBzdGF0ZS5pblBhcmFtcyA9IGZhbHNlO1xuICAgIHJldHVybiBudWxsO1xuICB9IGVsc2UgaWYgKC9cXGQvLnRlc3QoY2gpKSB7XG4gICAgc3RyZWFtLmVhdFdoaWxlKC9bXFx3XFwuXS8pO1xuICAgIHJldHVybiBcIm51bWJlclwiO1xuICB9IGVsc2UgaWYgKGNoID09IFwiI1wiKSB7XG4gICAgaWYgKHN0cmVhbS5lYXQoXCIqXCIpKSByZXR1cm4gY2hhaW4oc3RyZWFtLCBzdGF0ZSwgdG9rZW5Db21tZW50KTtcbiAgICBpZiAoY2ggPT0gXCIjXCIgJiYgc3RyZWFtLm1hdGNoKC8gKlxcWyAqXFxbLykpIHJldHVybiBjaGFpbihzdHJlYW0sIHN0YXRlLCB0b2tlblVucGFyc2VkKTtcbiAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICB9IGVsc2UgaWYgKGNoID09ICdcIicpIHtcbiAgICBzdHJlYW0uc2tpcFRvKC9cIi8pO1xuICAgIHJldHVybiBcImNvbW1lbnRcIjtcbiAgfSBlbHNlIGlmIChjaCA9PSBcIiRcIikge1xuICAgIHN0cmVhbS5lYXRXaGlsZSgvWyRfYS16MC05QS1aXFwuezpdLyk7XG4gICAgc3RyZWFtLmVhdFdoaWxlKC99Lyk7XG4gICAgc3RhdGUuYmVmb3JlUGFyYW1zID0gdHJ1ZTtcbiAgICByZXR1cm4gXCJidWlsdGluXCI7XG4gIH0gZWxzZSBpZiAoaXNPcGVyYXRvckNoYXIudGVzdChjaCkpIHtcbiAgICBzdHJlYW0uZWF0V2hpbGUoaXNPcGVyYXRvckNoYXIpO1xuICAgIHJldHVybiBcImNvbW1lbnRcIjtcbiAgfSBlbHNlIHtcbiAgICBzdHJlYW0uZWF0V2hpbGUoL1tcXHdcXCRfe31cXHhhMS1cXHVmZmZmXS8pO1xuICAgIHZhciB3b3JkID0gc3RyZWFtLmN1cnJlbnQoKS50b0xvd2VyQ2FzZSgpO1xuICAgIGlmIChrZXl3b3JkcyAmJiBrZXl3b3Jkcy5wcm9wZXJ0eUlzRW51bWVyYWJsZSh3b3JkKSkgcmV0dXJuIFwia2V5d29yZFwiO1xuICAgIGlmIChmdW5jdGlvbnMgJiYgZnVuY3Rpb25zLnByb3BlcnR5SXNFbnVtZXJhYmxlKHdvcmQpKSB7XG4gICAgICBzdGF0ZS5iZWZvcmVQYXJhbXMgPSB0cnVlO1xuICAgICAgcmV0dXJuIFwia2V5d29yZFwiO1xuICAgIH1cbiAgICByZXR1cm4gbnVsbDtcbiAgfVxufVxuZnVuY3Rpb24gdG9rZW5TdHJpbmcocXVvdGUpIHtcbiAgcmV0dXJuIGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgdmFyIGVzY2FwZWQgPSBmYWxzZSxcbiAgICAgIG5leHQsXG4gICAgICBlbmQgPSBmYWxzZTtcbiAgICB3aGlsZSAoKG5leHQgPSBzdHJlYW0ubmV4dCgpKSAhPSBudWxsKSB7XG4gICAgICBpZiAobmV4dCA9PSBxdW90ZSAmJiAhZXNjYXBlZCkge1xuICAgICAgICBlbmQgPSB0cnVlO1xuICAgICAgICBicmVhaztcbiAgICAgIH1cbiAgICAgIGVzY2FwZWQgPSAhZXNjYXBlZCAmJiBuZXh0ID09IFwiXFxcXFwiO1xuICAgIH1cbiAgICBpZiAoZW5kKSBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQmFzZTtcbiAgICByZXR1cm4gXCJzdHJpbmdcIjtcbiAgfTtcbn1cbmZ1bmN0aW9uIHRva2VuQ29tbWVudChzdHJlYW0sIHN0YXRlKSB7XG4gIHZhciBtYXliZUVuZCA9IGZhbHNlLFxuICAgIGNoO1xuICB3aGlsZSAoY2ggPSBzdHJlYW0ubmV4dCgpKSB7XG4gICAgaWYgKGNoID09IFwiI1wiICYmIG1heWJlRW5kKSB7XG4gICAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQmFzZTtcbiAgICAgIGJyZWFrO1xuICAgIH1cbiAgICBtYXliZUVuZCA9IGNoID09IFwiKlwiO1xuICB9XG4gIHJldHVybiBcImNvbW1lbnRcIjtcbn1cbmZ1bmN0aW9uIHRva2VuVW5wYXJzZWQoc3RyZWFtLCBzdGF0ZSkge1xuICB2YXIgbWF5YmVFbmQgPSAwLFxuICAgIGNoO1xuICB3aGlsZSAoY2ggPSBzdHJlYW0ubmV4dCgpKSB7XG4gICAgaWYgKGNoID09IFwiI1wiICYmIG1heWJlRW5kID09IDIpIHtcbiAgICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlO1xuICAgICAgYnJlYWs7XG4gICAgfVxuICAgIGlmIChjaCA9PSBcIl1cIikgbWF5YmVFbmQrKztlbHNlIGlmIChjaCAhPSBcIiBcIikgbWF5YmVFbmQgPSAwO1xuICB9XG4gIHJldHVybiBcIm1ldGFcIjtcbn1cbmV4cG9ydCBjb25zdCB0Y2wgPSB7XG4gIG5hbWU6IFwidGNsXCIsXG4gIHN0YXJ0U3RhdGU6IGZ1bmN0aW9uICgpIHtcbiAgICByZXR1cm4ge1xuICAgICAgdG9rZW5pemU6IHRva2VuQmFzZSxcbiAgICAgIGJlZm9yZVBhcmFtczogZmFsc2UsXG4gICAgICBpblBhcmFtczogZmFsc2VcbiAgICB9O1xuICB9LFxuICB0b2tlbjogZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICBpZiAoc3RyZWFtLmVhdFNwYWNlKCkpIHJldHVybiBudWxsO1xuICAgIHJldHVybiBzdGF0ZS50b2tlbml6ZShzdHJlYW0sIHN0YXRlKTtcbiAgfSxcbiAgbGFuZ3VhZ2VEYXRhOiB7XG4gICAgY29tbWVudFRva2Vuczoge1xuICAgICAgbGluZTogXCIjXCJcbiAgICB9XG4gIH1cbn07Il0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9