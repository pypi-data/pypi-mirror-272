"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[8984],{

/***/ 38984:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "rpmChanges": () => (/* binding */ rpmChanges),
/* harmony export */   "rpmSpec": () => (/* binding */ rpmSpec)
/* harmony export */ });
var headerSeparator = /^-+$/;
var headerLine = /^(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)  ?\d{1,2} \d{2}:\d{2}(:\d{2})? [A-Z]{3,4} \d{4} - /;
var simpleEmail = /^[\w+.-]+@[\w.-]+/;
const rpmChanges = {
  name: "rpmchanges",
  token: function (stream) {
    if (stream.sol()) {
      if (stream.match(headerSeparator)) {
        return 'tag';
      }
      if (stream.match(headerLine)) {
        return 'tag';
      }
    }
    if (stream.match(simpleEmail)) {
      return 'string';
    }
    stream.next();
    return null;
  }
};

// Quick and dirty spec file highlighting

var arch = /^(i386|i586|i686|x86_64|ppc64le|ppc64|ppc|ia64|s390x|s390|sparc64|sparcv9|sparc|noarch|alphaev6|alpha|hppa|mipsel)/;
var preamble = /^[a-zA-Z0-9()]+:/;
var section = /^%(debug_package|package|description|prep|build|install|files|clean|changelog|preinstall|preun|postinstall|postun|pretrans|posttrans|pre|post|triggerin|triggerun|verifyscript|check|triggerpostun|triggerprein|trigger)/;
var control_flow_complex = /^%(ifnarch|ifarch|if)/; // rpm control flow macros
var control_flow_simple = /^%(else|endif)/; // rpm control flow macros
var operators = /^(\!|\?|\<\=|\<|\>\=|\>|\=\=|\&\&|\|\|)/; // operators in control flow macros

const rpmSpec = {
  name: "rpmspec",
  startState: function () {
    return {
      controlFlow: false,
      macroParameters: false,
      section: false
    };
  },
  token: function (stream, state) {
    var ch = stream.peek();
    if (ch == "#") {
      stream.skipToEnd();
      return "comment";
    }
    if (stream.sol()) {
      if (stream.match(preamble)) {
        return "header";
      }
      if (stream.match(section)) {
        return "atom";
      }
    }
    if (stream.match(/^\$\w+/)) {
      return "def";
    } // Variables like '$RPM_BUILD_ROOT'
    if (stream.match(/^\$\{\w+\}/)) {
      return "def";
    } // Variables like '${RPM_BUILD_ROOT}'

    if (stream.match(control_flow_simple)) {
      return "keyword";
    }
    if (stream.match(control_flow_complex)) {
      state.controlFlow = true;
      return "keyword";
    }
    if (state.controlFlow) {
      if (stream.match(operators)) {
        return "operator";
      }
      if (stream.match(/^(\d+)/)) {
        return "number";
      }
      if (stream.eol()) {
        state.controlFlow = false;
      }
    }
    if (stream.match(arch)) {
      if (stream.eol()) {
        state.controlFlow = false;
      }
      return "number";
    }

    // Macros like '%make_install' or '%attr(0775,root,root)'
    if (stream.match(/^%[\w]+/)) {
      if (stream.match('(')) {
        state.macroParameters = true;
      }
      return "keyword";
    }
    if (state.macroParameters) {
      if (stream.match(/^\d+/)) {
        return "number";
      }
      if (stream.match(')')) {
        state.macroParameters = false;
        return "keyword";
      }
    }

    // Macros like '%{defined fedora}'
    if (stream.match(/^%\{\??[\w \-\:\!]+\}/)) {
      if (stream.eol()) {
        state.controlFlow = false;
      }
      return "def";
    }
    stream.next();
    return null;
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiODk4NC5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGNvZGVtaXJyb3IvbGVnYWN5LW1vZGVzL21vZGUvcnBtLmpzIl0sInNvdXJjZXNDb250ZW50IjpbInZhciBoZWFkZXJTZXBhcmF0b3IgPSAvXi0rJC87XG52YXIgaGVhZGVyTGluZSA9IC9eKE1vbnxUdWV8V2VkfFRodXxGcml8U2F0fFN1bikgKEphbnxGZWJ8TWFyfEFwcnxNYXl8SnVufEp1bHxBdWd8U2VwfE9jdHxOb3Z8RGVjKSAgP1xcZHsxLDJ9IFxcZHsyfTpcXGR7Mn0oOlxcZHsyfSk/IFtBLVpdezMsNH0gXFxkezR9IC0gLztcbnZhciBzaW1wbGVFbWFpbCA9IC9eW1xcdysuLV0rQFtcXHcuLV0rLztcbmV4cG9ydCBjb25zdCBycG1DaGFuZ2VzID0ge1xuICBuYW1lOiBcInJwbWNoYW5nZXNcIixcbiAgdG9rZW46IGZ1bmN0aW9uIChzdHJlYW0pIHtcbiAgICBpZiAoc3RyZWFtLnNvbCgpKSB7XG4gICAgICBpZiAoc3RyZWFtLm1hdGNoKGhlYWRlclNlcGFyYXRvcikpIHtcbiAgICAgICAgcmV0dXJuICd0YWcnO1xuICAgICAgfVxuICAgICAgaWYgKHN0cmVhbS5tYXRjaChoZWFkZXJMaW5lKSkge1xuICAgICAgICByZXR1cm4gJ3RhZyc7XG4gICAgICB9XG4gICAgfVxuICAgIGlmIChzdHJlYW0ubWF0Y2goc2ltcGxlRW1haWwpKSB7XG4gICAgICByZXR1cm4gJ3N0cmluZyc7XG4gICAgfVxuICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgcmV0dXJuIG51bGw7XG4gIH1cbn07XG5cbi8vIFF1aWNrIGFuZCBkaXJ0eSBzcGVjIGZpbGUgaGlnaGxpZ2h0aW5nXG5cbnZhciBhcmNoID0gL14oaTM4NnxpNTg2fGk2ODZ8eDg2XzY0fHBwYzY0bGV8cHBjNjR8cHBjfGlhNjR8czM5MHh8czM5MHxzcGFyYzY0fHNwYXJjdjl8c3BhcmN8bm9hcmNofGFscGhhZXY2fGFscGhhfGhwcGF8bWlwc2VsKS87XG52YXIgcHJlYW1ibGUgPSAvXlthLXpBLVowLTkoKV0rOi87XG52YXIgc2VjdGlvbiA9IC9eJShkZWJ1Z19wYWNrYWdlfHBhY2thZ2V8ZGVzY3JpcHRpb258cHJlcHxidWlsZHxpbnN0YWxsfGZpbGVzfGNsZWFufGNoYW5nZWxvZ3xwcmVpbnN0YWxsfHByZXVufHBvc3RpbnN0YWxsfHBvc3R1bnxwcmV0cmFuc3xwb3N0dHJhbnN8cHJlfHBvc3R8dHJpZ2dlcmlufHRyaWdnZXJ1bnx2ZXJpZnlzY3JpcHR8Y2hlY2t8dHJpZ2dlcnBvc3R1bnx0cmlnZ2VycHJlaW58dHJpZ2dlcikvO1xudmFyIGNvbnRyb2xfZmxvd19jb21wbGV4ID0gL14lKGlmbmFyY2h8aWZhcmNofGlmKS87IC8vIHJwbSBjb250cm9sIGZsb3cgbWFjcm9zXG52YXIgY29udHJvbF9mbG93X3NpbXBsZSA9IC9eJShlbHNlfGVuZGlmKS87IC8vIHJwbSBjb250cm9sIGZsb3cgbWFjcm9zXG52YXIgb3BlcmF0b3JzID0gL14oXFwhfFxcP3xcXDxcXD18XFw8fFxcPlxcPXxcXD58XFw9XFw9fFxcJlxcJnxcXHxcXHwpLzsgLy8gb3BlcmF0b3JzIGluIGNvbnRyb2wgZmxvdyBtYWNyb3NcblxuZXhwb3J0IGNvbnN0IHJwbVNwZWMgPSB7XG4gIG5hbWU6IFwicnBtc3BlY1wiLFxuICBzdGFydFN0YXRlOiBmdW5jdGlvbiAoKSB7XG4gICAgcmV0dXJuIHtcbiAgICAgIGNvbnRyb2xGbG93OiBmYWxzZSxcbiAgICAgIG1hY3JvUGFyYW1ldGVyczogZmFsc2UsXG4gICAgICBzZWN0aW9uOiBmYWxzZVxuICAgIH07XG4gIH0sXG4gIHRva2VuOiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIHZhciBjaCA9IHN0cmVhbS5wZWVrKCk7XG4gICAgaWYgKGNoID09IFwiI1wiKSB7XG4gICAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgICByZXR1cm4gXCJjb21tZW50XCI7XG4gICAgfVxuICAgIGlmIChzdHJlYW0uc29sKCkpIHtcbiAgICAgIGlmIChzdHJlYW0ubWF0Y2gocHJlYW1ibGUpKSB7XG4gICAgICAgIHJldHVybiBcImhlYWRlclwiO1xuICAgICAgfVxuICAgICAgaWYgKHN0cmVhbS5tYXRjaChzZWN0aW9uKSkge1xuICAgICAgICByZXR1cm4gXCJhdG9tXCI7XG4gICAgICB9XG4gICAgfVxuICAgIGlmIChzdHJlYW0ubWF0Y2goL15cXCRcXHcrLykpIHtcbiAgICAgIHJldHVybiBcImRlZlwiO1xuICAgIH0gLy8gVmFyaWFibGVzIGxpa2UgJyRSUE1fQlVJTERfUk9PVCdcbiAgICBpZiAoc3RyZWFtLm1hdGNoKC9eXFwkXFx7XFx3K1xcfS8pKSB7XG4gICAgICByZXR1cm4gXCJkZWZcIjtcbiAgICB9IC8vIFZhcmlhYmxlcyBsaWtlICcke1JQTV9CVUlMRF9ST09UfSdcblxuICAgIGlmIChzdHJlYW0ubWF0Y2goY29udHJvbF9mbG93X3NpbXBsZSkpIHtcbiAgICAgIHJldHVybiBcImtleXdvcmRcIjtcbiAgICB9XG4gICAgaWYgKHN0cmVhbS5tYXRjaChjb250cm9sX2Zsb3dfY29tcGxleCkpIHtcbiAgICAgIHN0YXRlLmNvbnRyb2xGbG93ID0gdHJ1ZTtcbiAgICAgIHJldHVybiBcImtleXdvcmRcIjtcbiAgICB9XG4gICAgaWYgKHN0YXRlLmNvbnRyb2xGbG93KSB7XG4gICAgICBpZiAoc3RyZWFtLm1hdGNoKG9wZXJhdG9ycykpIHtcbiAgICAgICAgcmV0dXJuIFwib3BlcmF0b3JcIjtcbiAgICAgIH1cbiAgICAgIGlmIChzdHJlYW0ubWF0Y2goL14oXFxkKykvKSkge1xuICAgICAgICByZXR1cm4gXCJudW1iZXJcIjtcbiAgICAgIH1cbiAgICAgIGlmIChzdHJlYW0uZW9sKCkpIHtcbiAgICAgICAgc3RhdGUuY29udHJvbEZsb3cgPSBmYWxzZTtcbiAgICAgIH1cbiAgICB9XG4gICAgaWYgKHN0cmVhbS5tYXRjaChhcmNoKSkge1xuICAgICAgaWYgKHN0cmVhbS5lb2woKSkge1xuICAgICAgICBzdGF0ZS5jb250cm9sRmxvdyA9IGZhbHNlO1xuICAgICAgfVxuICAgICAgcmV0dXJuIFwibnVtYmVyXCI7XG4gICAgfVxuXG4gICAgLy8gTWFjcm9zIGxpa2UgJyVtYWtlX2luc3RhbGwnIG9yICclYXR0cigwNzc1LHJvb3Qscm9vdCknXG4gICAgaWYgKHN0cmVhbS5tYXRjaCgvXiVbXFx3XSsvKSkge1xuICAgICAgaWYgKHN0cmVhbS5tYXRjaCgnKCcpKSB7XG4gICAgICAgIHN0YXRlLm1hY3JvUGFyYW1ldGVycyA9IHRydWU7XG4gICAgICB9XG4gICAgICByZXR1cm4gXCJrZXl3b3JkXCI7XG4gICAgfVxuICAgIGlmIChzdGF0ZS5tYWNyb1BhcmFtZXRlcnMpIHtcbiAgICAgIGlmIChzdHJlYW0ubWF0Y2goL15cXGQrLykpIHtcbiAgICAgICAgcmV0dXJuIFwibnVtYmVyXCI7XG4gICAgICB9XG4gICAgICBpZiAoc3RyZWFtLm1hdGNoKCcpJykpIHtcbiAgICAgICAgc3RhdGUubWFjcm9QYXJhbWV0ZXJzID0gZmFsc2U7XG4gICAgICAgIHJldHVybiBcImtleXdvcmRcIjtcbiAgICAgIH1cbiAgICB9XG5cbiAgICAvLyBNYWNyb3MgbGlrZSAnJXtkZWZpbmVkIGZlZG9yYX0nXG4gICAgaWYgKHN0cmVhbS5tYXRjaCgvXiVcXHtcXD8/W1xcdyBcXC1cXDpcXCFdK1xcfS8pKSB7XG4gICAgICBpZiAoc3RyZWFtLmVvbCgpKSB7XG4gICAgICAgIHN0YXRlLmNvbnRyb2xGbG93ID0gZmFsc2U7XG4gICAgICB9XG4gICAgICByZXR1cm4gXCJkZWZcIjtcbiAgICB9XG4gICAgc3RyZWFtLm5leHQoKTtcbiAgICByZXR1cm4gbnVsbDtcbiAgfVxufTsiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=