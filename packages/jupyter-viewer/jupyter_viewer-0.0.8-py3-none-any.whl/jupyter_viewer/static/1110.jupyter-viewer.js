"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[1110],{

/***/ 81110:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "mscgen": () => (/* binding */ mscgen),
/* harmony export */   "msgenny": () => (/* binding */ msgenny),
/* harmony export */   "xu": () => (/* binding */ xu)
/* harmony export */ });
function mkParser(lang) {
  return {
    name: "mscgen",
    startState: startStateFn,
    copyState: copyStateFn,
    token: produceTokenFunction(lang),
    languageData: {
      commentTokens: {
        line: "#",
        block: {
          open: "/*",
          close: "*/"
        }
      }
    }
  };
}
const mscgen = mkParser({
  "keywords": ["msc"],
  "options": ["hscale", "width", "arcgradient", "wordwraparcs"],
  "constants": ["true", "false", "on", "off"],
  "attributes": ["label", "idurl", "id", "url", "linecolor", "linecolour", "textcolor", "textcolour", "textbgcolor", "textbgcolour", "arclinecolor", "arclinecolour", "arctextcolor", "arctextcolour", "arctextbgcolor", "arctextbgcolour", "arcskip"],
  "brackets": ["\\{", "\\}"],
  // [ and  ] are brackets too, but these get handled in with lists
  "arcsWords": ["note", "abox", "rbox", "box"],
  "arcsOthers": ["\\|\\|\\|", "\\.\\.\\.", "---", "--", "<->", "==", "<<=>>", "<=>", "\\.\\.", "<<>>", "::", "<:>", "->", "=>>", "=>", ">>", ":>", "<-", "<<=", "<=", "<<", "<:", "x-", "-x"],
  "singlecomment": ["//", "#"],
  "operators": ["="]
});
const msgenny = mkParser({
  "keywords": null,
  "options": ["hscale", "width", "arcgradient", "wordwraparcs", "wordwrapentities", "watermark"],
  "constants": ["true", "false", "on", "off", "auto"],
  "attributes": null,
  "brackets": ["\\{", "\\}"],
  "arcsWords": ["note", "abox", "rbox", "box", "alt", "else", "opt", "break", "par", "seq", "strict", "neg", "critical", "ignore", "consider", "assert", "loop", "ref", "exc"],
  "arcsOthers": ["\\|\\|\\|", "\\.\\.\\.", "---", "--", "<->", "==", "<<=>>", "<=>", "\\.\\.", "<<>>", "::", "<:>", "->", "=>>", "=>", ">>", ":>", "<-", "<<=", "<=", "<<", "<:", "x-", "-x"],
  "singlecomment": ["//", "#"],
  "operators": ["="]
});
const xu = mkParser({
  "keywords": ["msc", "xu"],
  "options": ["hscale", "width", "arcgradient", "wordwraparcs", "wordwrapentities", "watermark"],
  "constants": ["true", "false", "on", "off", "auto"],
  "attributes": ["label", "idurl", "id", "url", "linecolor", "linecolour", "textcolor", "textcolour", "textbgcolor", "textbgcolour", "arclinecolor", "arclinecolour", "arctextcolor", "arctextcolour", "arctextbgcolor", "arctextbgcolour", "arcskip", "title", "deactivate", "activate", "activation"],
  "brackets": ["\\{", "\\}"],
  // [ and  ] are brackets too, but these get handled in with lists
  "arcsWords": ["note", "abox", "rbox", "box", "alt", "else", "opt", "break", "par", "seq", "strict", "neg", "critical", "ignore", "consider", "assert", "loop", "ref", "exc"],
  "arcsOthers": ["\\|\\|\\|", "\\.\\.\\.", "---", "--", "<->", "==", "<<=>>", "<=>", "\\.\\.", "<<>>", "::", "<:>", "->", "=>>", "=>", ">>", ":>", "<-", "<<=", "<=", "<<", "<:", "x-", "-x"],
  "singlecomment": ["//", "#"],
  "operators": ["="]
});
function wordRegexpBoundary(pWords) {
  return new RegExp("^\\b(" + pWords.join("|") + ")\\b", "i");
}
function wordRegexp(pWords) {
  return new RegExp("^(?:" + pWords.join("|") + ")", "i");
}
function startStateFn() {
  return {
    inComment: false,
    inString: false,
    inAttributeList: false,
    inScript: false
  };
}
function copyStateFn(pState) {
  return {
    inComment: pState.inComment,
    inString: pState.inString,
    inAttributeList: pState.inAttributeList,
    inScript: pState.inScript
  };
}
function produceTokenFunction(pConfig) {
  return function (pStream, pState) {
    if (pStream.match(wordRegexp(pConfig.brackets), true, true)) {
      return "bracket";
    }
    /* comments */
    if (!pState.inComment) {
      if (pStream.match(/\/\*[^\*\/]*/, true, true)) {
        pState.inComment = true;
        return "comment";
      }
      if (pStream.match(wordRegexp(pConfig.singlecomment), true, true)) {
        pStream.skipToEnd();
        return "comment";
      }
    }
    if (pState.inComment) {
      if (pStream.match(/[^\*\/]*\*\//, true, true)) pState.inComment = false;else pStream.skipToEnd();
      return "comment";
    }
    /* strings */
    if (!pState.inString && pStream.match(/\"(\\\"|[^\"])*/, true, true)) {
      pState.inString = true;
      return "string";
    }
    if (pState.inString) {
      if (pStream.match(/[^\"]*\"/, true, true)) pState.inString = false;else pStream.skipToEnd();
      return "string";
    }
    /* keywords & operators */
    if (!!pConfig.keywords && pStream.match(wordRegexpBoundary(pConfig.keywords), true, true)) return "keyword";
    if (pStream.match(wordRegexpBoundary(pConfig.options), true, true)) return "keyword";
    if (pStream.match(wordRegexpBoundary(pConfig.arcsWords), true, true)) return "keyword";
    if (pStream.match(wordRegexp(pConfig.arcsOthers), true, true)) return "keyword";
    if (!!pConfig.operators && pStream.match(wordRegexp(pConfig.operators), true, true)) return "operator";
    if (!!pConfig.constants && pStream.match(wordRegexp(pConfig.constants), true, true)) return "variable";

    /* attribute lists */
    if (!pConfig.inAttributeList && !!pConfig.attributes && pStream.match('[', true, true)) {
      pConfig.inAttributeList = true;
      return "bracket";
    }
    if (pConfig.inAttributeList) {
      if (pConfig.attributes !== null && pStream.match(wordRegexpBoundary(pConfig.attributes), true, true)) {
        return "attribute";
      }
      if (pStream.match(']', true, true)) {
        pConfig.inAttributeList = false;
        return "bracket";
      }
    }
    pStream.next();
    return null;
  };
}

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiMTExMC5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL0Bjb2RlbWlycm9yL2xlZ2FjeS1tb2Rlcy9tb2RlL21zY2dlbi5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyJmdW5jdGlvbiBta1BhcnNlcihsYW5nKSB7XG4gIHJldHVybiB7XG4gICAgbmFtZTogXCJtc2NnZW5cIixcbiAgICBzdGFydFN0YXRlOiBzdGFydFN0YXRlRm4sXG4gICAgY29weVN0YXRlOiBjb3B5U3RhdGVGbixcbiAgICB0b2tlbjogcHJvZHVjZVRva2VuRnVuY3Rpb24obGFuZyksXG4gICAgbGFuZ3VhZ2VEYXRhOiB7XG4gICAgICBjb21tZW50VG9rZW5zOiB7XG4gICAgICAgIGxpbmU6IFwiI1wiLFxuICAgICAgICBibG9jazoge1xuICAgICAgICAgIG9wZW46IFwiLypcIixcbiAgICAgICAgICBjbG9zZTogXCIqL1wiXG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9XG4gIH07XG59XG5leHBvcnQgY29uc3QgbXNjZ2VuID0gbWtQYXJzZXIoe1xuICBcImtleXdvcmRzXCI6IFtcIm1zY1wiXSxcbiAgXCJvcHRpb25zXCI6IFtcImhzY2FsZVwiLCBcIndpZHRoXCIsIFwiYXJjZ3JhZGllbnRcIiwgXCJ3b3Jkd3JhcGFyY3NcIl0sXG4gIFwiY29uc3RhbnRzXCI6IFtcInRydWVcIiwgXCJmYWxzZVwiLCBcIm9uXCIsIFwib2ZmXCJdLFxuICBcImF0dHJpYnV0ZXNcIjogW1wibGFiZWxcIiwgXCJpZHVybFwiLCBcImlkXCIsIFwidXJsXCIsIFwibGluZWNvbG9yXCIsIFwibGluZWNvbG91clwiLCBcInRleHRjb2xvclwiLCBcInRleHRjb2xvdXJcIiwgXCJ0ZXh0Ymdjb2xvclwiLCBcInRleHRiZ2NvbG91clwiLCBcImFyY2xpbmVjb2xvclwiLCBcImFyY2xpbmVjb2xvdXJcIiwgXCJhcmN0ZXh0Y29sb3JcIiwgXCJhcmN0ZXh0Y29sb3VyXCIsIFwiYXJjdGV4dGJnY29sb3JcIiwgXCJhcmN0ZXh0Ymdjb2xvdXJcIiwgXCJhcmNza2lwXCJdLFxuICBcImJyYWNrZXRzXCI6IFtcIlxcXFx7XCIsIFwiXFxcXH1cIl0sXG4gIC8vIFsgYW5kICBdIGFyZSBicmFja2V0cyB0b28sIGJ1dCB0aGVzZSBnZXQgaGFuZGxlZCBpbiB3aXRoIGxpc3RzXG4gIFwiYXJjc1dvcmRzXCI6IFtcIm5vdGVcIiwgXCJhYm94XCIsIFwicmJveFwiLCBcImJveFwiXSxcbiAgXCJhcmNzT3RoZXJzXCI6IFtcIlxcXFx8XFxcXHxcXFxcfFwiLCBcIlxcXFwuXFxcXC5cXFxcLlwiLCBcIi0tLVwiLCBcIi0tXCIsIFwiPC0+XCIsIFwiPT1cIiwgXCI8PD0+PlwiLCBcIjw9PlwiLCBcIlxcXFwuXFxcXC5cIiwgXCI8PD4+XCIsIFwiOjpcIiwgXCI8Oj5cIiwgXCItPlwiLCBcIj0+PlwiLCBcIj0+XCIsIFwiPj5cIiwgXCI6PlwiLCBcIjwtXCIsIFwiPDw9XCIsIFwiPD1cIiwgXCI8PFwiLCBcIjw6XCIsIFwieC1cIiwgXCIteFwiXSxcbiAgXCJzaW5nbGVjb21tZW50XCI6IFtcIi8vXCIsIFwiI1wiXSxcbiAgXCJvcGVyYXRvcnNcIjogW1wiPVwiXVxufSk7XG5leHBvcnQgY29uc3QgbXNnZW5ueSA9IG1rUGFyc2VyKHtcbiAgXCJrZXl3b3Jkc1wiOiBudWxsLFxuICBcIm9wdGlvbnNcIjogW1wiaHNjYWxlXCIsIFwid2lkdGhcIiwgXCJhcmNncmFkaWVudFwiLCBcIndvcmR3cmFwYXJjc1wiLCBcIndvcmR3cmFwZW50aXRpZXNcIiwgXCJ3YXRlcm1hcmtcIl0sXG4gIFwiY29uc3RhbnRzXCI6IFtcInRydWVcIiwgXCJmYWxzZVwiLCBcIm9uXCIsIFwib2ZmXCIsIFwiYXV0b1wiXSxcbiAgXCJhdHRyaWJ1dGVzXCI6IG51bGwsXG4gIFwiYnJhY2tldHNcIjogW1wiXFxcXHtcIiwgXCJcXFxcfVwiXSxcbiAgXCJhcmNzV29yZHNcIjogW1wibm90ZVwiLCBcImFib3hcIiwgXCJyYm94XCIsIFwiYm94XCIsIFwiYWx0XCIsIFwiZWxzZVwiLCBcIm9wdFwiLCBcImJyZWFrXCIsIFwicGFyXCIsIFwic2VxXCIsIFwic3RyaWN0XCIsIFwibmVnXCIsIFwiY3JpdGljYWxcIiwgXCJpZ25vcmVcIiwgXCJjb25zaWRlclwiLCBcImFzc2VydFwiLCBcImxvb3BcIiwgXCJyZWZcIiwgXCJleGNcIl0sXG4gIFwiYXJjc090aGVyc1wiOiBbXCJcXFxcfFxcXFx8XFxcXHxcIiwgXCJcXFxcLlxcXFwuXFxcXC5cIiwgXCItLS1cIiwgXCItLVwiLCBcIjwtPlwiLCBcIj09XCIsIFwiPDw9Pj5cIiwgXCI8PT5cIiwgXCJcXFxcLlxcXFwuXCIsIFwiPDw+PlwiLCBcIjo6XCIsIFwiPDo+XCIsIFwiLT5cIiwgXCI9Pj5cIiwgXCI9PlwiLCBcIj4+XCIsIFwiOj5cIiwgXCI8LVwiLCBcIjw8PVwiLCBcIjw9XCIsIFwiPDxcIiwgXCI8OlwiLCBcIngtXCIsIFwiLXhcIl0sXG4gIFwic2luZ2xlY29tbWVudFwiOiBbXCIvL1wiLCBcIiNcIl0sXG4gIFwib3BlcmF0b3JzXCI6IFtcIj1cIl1cbn0pO1xuZXhwb3J0IGNvbnN0IHh1ID0gbWtQYXJzZXIoe1xuICBcImtleXdvcmRzXCI6IFtcIm1zY1wiLCBcInh1XCJdLFxuICBcIm9wdGlvbnNcIjogW1wiaHNjYWxlXCIsIFwid2lkdGhcIiwgXCJhcmNncmFkaWVudFwiLCBcIndvcmR3cmFwYXJjc1wiLCBcIndvcmR3cmFwZW50aXRpZXNcIiwgXCJ3YXRlcm1hcmtcIl0sXG4gIFwiY29uc3RhbnRzXCI6IFtcInRydWVcIiwgXCJmYWxzZVwiLCBcIm9uXCIsIFwib2ZmXCIsIFwiYXV0b1wiXSxcbiAgXCJhdHRyaWJ1dGVzXCI6IFtcImxhYmVsXCIsIFwiaWR1cmxcIiwgXCJpZFwiLCBcInVybFwiLCBcImxpbmVjb2xvclwiLCBcImxpbmVjb2xvdXJcIiwgXCJ0ZXh0Y29sb3JcIiwgXCJ0ZXh0Y29sb3VyXCIsIFwidGV4dGJnY29sb3JcIiwgXCJ0ZXh0Ymdjb2xvdXJcIiwgXCJhcmNsaW5lY29sb3JcIiwgXCJhcmNsaW5lY29sb3VyXCIsIFwiYXJjdGV4dGNvbG9yXCIsIFwiYXJjdGV4dGNvbG91clwiLCBcImFyY3RleHRiZ2NvbG9yXCIsIFwiYXJjdGV4dGJnY29sb3VyXCIsIFwiYXJjc2tpcFwiLCBcInRpdGxlXCIsIFwiZGVhY3RpdmF0ZVwiLCBcImFjdGl2YXRlXCIsIFwiYWN0aXZhdGlvblwiXSxcbiAgXCJicmFja2V0c1wiOiBbXCJcXFxce1wiLCBcIlxcXFx9XCJdLFxuICAvLyBbIGFuZCAgXSBhcmUgYnJhY2tldHMgdG9vLCBidXQgdGhlc2UgZ2V0IGhhbmRsZWQgaW4gd2l0aCBsaXN0c1xuICBcImFyY3NXb3Jkc1wiOiBbXCJub3RlXCIsIFwiYWJveFwiLCBcInJib3hcIiwgXCJib3hcIiwgXCJhbHRcIiwgXCJlbHNlXCIsIFwib3B0XCIsIFwiYnJlYWtcIiwgXCJwYXJcIiwgXCJzZXFcIiwgXCJzdHJpY3RcIiwgXCJuZWdcIiwgXCJjcml0aWNhbFwiLCBcImlnbm9yZVwiLCBcImNvbnNpZGVyXCIsIFwiYXNzZXJ0XCIsIFwibG9vcFwiLCBcInJlZlwiLCBcImV4Y1wiXSxcbiAgXCJhcmNzT3RoZXJzXCI6IFtcIlxcXFx8XFxcXHxcXFxcfFwiLCBcIlxcXFwuXFxcXC5cXFxcLlwiLCBcIi0tLVwiLCBcIi0tXCIsIFwiPC0+XCIsIFwiPT1cIiwgXCI8PD0+PlwiLCBcIjw9PlwiLCBcIlxcXFwuXFxcXC5cIiwgXCI8PD4+XCIsIFwiOjpcIiwgXCI8Oj5cIiwgXCItPlwiLCBcIj0+PlwiLCBcIj0+XCIsIFwiPj5cIiwgXCI6PlwiLCBcIjwtXCIsIFwiPDw9XCIsIFwiPD1cIiwgXCI8PFwiLCBcIjw6XCIsIFwieC1cIiwgXCIteFwiXSxcbiAgXCJzaW5nbGVjb21tZW50XCI6IFtcIi8vXCIsIFwiI1wiXSxcbiAgXCJvcGVyYXRvcnNcIjogW1wiPVwiXVxufSk7XG5mdW5jdGlvbiB3b3JkUmVnZXhwQm91bmRhcnkocFdvcmRzKSB7XG4gIHJldHVybiBuZXcgUmVnRXhwKFwiXlxcXFxiKFwiICsgcFdvcmRzLmpvaW4oXCJ8XCIpICsgXCIpXFxcXGJcIiwgXCJpXCIpO1xufVxuZnVuY3Rpb24gd29yZFJlZ2V4cChwV29yZHMpIHtcbiAgcmV0dXJuIG5ldyBSZWdFeHAoXCJeKD86XCIgKyBwV29yZHMuam9pbihcInxcIikgKyBcIilcIiwgXCJpXCIpO1xufVxuZnVuY3Rpb24gc3RhcnRTdGF0ZUZuKCkge1xuICByZXR1cm4ge1xuICAgIGluQ29tbWVudDogZmFsc2UsXG4gICAgaW5TdHJpbmc6IGZhbHNlLFxuICAgIGluQXR0cmlidXRlTGlzdDogZmFsc2UsXG4gICAgaW5TY3JpcHQ6IGZhbHNlXG4gIH07XG59XG5mdW5jdGlvbiBjb3B5U3RhdGVGbihwU3RhdGUpIHtcbiAgcmV0dXJuIHtcbiAgICBpbkNvbW1lbnQ6IHBTdGF0ZS5pbkNvbW1lbnQsXG4gICAgaW5TdHJpbmc6IHBTdGF0ZS5pblN0cmluZyxcbiAgICBpbkF0dHJpYnV0ZUxpc3Q6IHBTdGF0ZS5pbkF0dHJpYnV0ZUxpc3QsXG4gICAgaW5TY3JpcHQ6IHBTdGF0ZS5pblNjcmlwdFxuICB9O1xufVxuZnVuY3Rpb24gcHJvZHVjZVRva2VuRnVuY3Rpb24ocENvbmZpZykge1xuICByZXR1cm4gZnVuY3Rpb24gKHBTdHJlYW0sIHBTdGF0ZSkge1xuICAgIGlmIChwU3RyZWFtLm1hdGNoKHdvcmRSZWdleHAocENvbmZpZy5icmFja2V0cyksIHRydWUsIHRydWUpKSB7XG4gICAgICByZXR1cm4gXCJicmFja2V0XCI7XG4gICAgfVxuICAgIC8qIGNvbW1lbnRzICovXG4gICAgaWYgKCFwU3RhdGUuaW5Db21tZW50KSB7XG4gICAgICBpZiAocFN0cmVhbS5tYXRjaCgvXFwvXFwqW15cXCpcXC9dKi8sIHRydWUsIHRydWUpKSB7XG4gICAgICAgIHBTdGF0ZS5pbkNvbW1lbnQgPSB0cnVlO1xuICAgICAgICByZXR1cm4gXCJjb21tZW50XCI7XG4gICAgICB9XG4gICAgICBpZiAocFN0cmVhbS5tYXRjaCh3b3JkUmVnZXhwKHBDb25maWcuc2luZ2xlY29tbWVudCksIHRydWUsIHRydWUpKSB7XG4gICAgICAgIHBTdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgICAgIHJldHVybiBcImNvbW1lbnRcIjtcbiAgICAgIH1cbiAgICB9XG4gICAgaWYgKHBTdGF0ZS5pbkNvbW1lbnQpIHtcbiAgICAgIGlmIChwU3RyZWFtLm1hdGNoKC9bXlxcKlxcL10qXFwqXFwvLywgdHJ1ZSwgdHJ1ZSkpIHBTdGF0ZS5pbkNvbW1lbnQgPSBmYWxzZTtlbHNlIHBTdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgICByZXR1cm4gXCJjb21tZW50XCI7XG4gICAgfVxuICAgIC8qIHN0cmluZ3MgKi9cbiAgICBpZiAoIXBTdGF0ZS5pblN0cmluZyAmJiBwU3RyZWFtLm1hdGNoKC9cXFwiKFxcXFxcXFwifFteXFxcIl0pKi8sIHRydWUsIHRydWUpKSB7XG4gICAgICBwU3RhdGUuaW5TdHJpbmcgPSB0cnVlO1xuICAgICAgcmV0dXJuIFwic3RyaW5nXCI7XG4gICAgfVxuICAgIGlmIChwU3RhdGUuaW5TdHJpbmcpIHtcbiAgICAgIGlmIChwU3RyZWFtLm1hdGNoKC9bXlxcXCJdKlxcXCIvLCB0cnVlLCB0cnVlKSkgcFN0YXRlLmluU3RyaW5nID0gZmFsc2U7ZWxzZSBwU3RyZWFtLnNraXBUb0VuZCgpO1xuICAgICAgcmV0dXJuIFwic3RyaW5nXCI7XG4gICAgfVxuICAgIC8qIGtleXdvcmRzICYgb3BlcmF0b3JzICovXG4gICAgaWYgKCEhcENvbmZpZy5rZXl3b3JkcyAmJiBwU3RyZWFtLm1hdGNoKHdvcmRSZWdleHBCb3VuZGFyeShwQ29uZmlnLmtleXdvcmRzKSwgdHJ1ZSwgdHJ1ZSkpIHJldHVybiBcImtleXdvcmRcIjtcbiAgICBpZiAocFN0cmVhbS5tYXRjaCh3b3JkUmVnZXhwQm91bmRhcnkocENvbmZpZy5vcHRpb25zKSwgdHJ1ZSwgdHJ1ZSkpIHJldHVybiBcImtleXdvcmRcIjtcbiAgICBpZiAocFN0cmVhbS5tYXRjaCh3b3JkUmVnZXhwQm91bmRhcnkocENvbmZpZy5hcmNzV29yZHMpLCB0cnVlLCB0cnVlKSkgcmV0dXJuIFwia2V5d29yZFwiO1xuICAgIGlmIChwU3RyZWFtLm1hdGNoKHdvcmRSZWdleHAocENvbmZpZy5hcmNzT3RoZXJzKSwgdHJ1ZSwgdHJ1ZSkpIHJldHVybiBcImtleXdvcmRcIjtcbiAgICBpZiAoISFwQ29uZmlnLm9wZXJhdG9ycyAmJiBwU3RyZWFtLm1hdGNoKHdvcmRSZWdleHAocENvbmZpZy5vcGVyYXRvcnMpLCB0cnVlLCB0cnVlKSkgcmV0dXJuIFwib3BlcmF0b3JcIjtcbiAgICBpZiAoISFwQ29uZmlnLmNvbnN0YW50cyAmJiBwU3RyZWFtLm1hdGNoKHdvcmRSZWdleHAocENvbmZpZy5jb25zdGFudHMpLCB0cnVlLCB0cnVlKSkgcmV0dXJuIFwidmFyaWFibGVcIjtcblxuICAgIC8qIGF0dHJpYnV0ZSBsaXN0cyAqL1xuICAgIGlmICghcENvbmZpZy5pbkF0dHJpYnV0ZUxpc3QgJiYgISFwQ29uZmlnLmF0dHJpYnV0ZXMgJiYgcFN0cmVhbS5tYXRjaCgnWycsIHRydWUsIHRydWUpKSB7XG4gICAgICBwQ29uZmlnLmluQXR0cmlidXRlTGlzdCA9IHRydWU7XG4gICAgICByZXR1cm4gXCJicmFja2V0XCI7XG4gICAgfVxuICAgIGlmIChwQ29uZmlnLmluQXR0cmlidXRlTGlzdCkge1xuICAgICAgaWYgKHBDb25maWcuYXR0cmlidXRlcyAhPT0gbnVsbCAmJiBwU3RyZWFtLm1hdGNoKHdvcmRSZWdleHBCb3VuZGFyeShwQ29uZmlnLmF0dHJpYnV0ZXMpLCB0cnVlLCB0cnVlKSkge1xuICAgICAgICByZXR1cm4gXCJhdHRyaWJ1dGVcIjtcbiAgICAgIH1cbiAgICAgIGlmIChwU3RyZWFtLm1hdGNoKCddJywgdHJ1ZSwgdHJ1ZSkpIHtcbiAgICAgICAgcENvbmZpZy5pbkF0dHJpYnV0ZUxpc3QgPSBmYWxzZTtcbiAgICAgICAgcmV0dXJuIFwiYnJhY2tldFwiO1xuICAgICAgfVxuICAgIH1cbiAgICBwU3RyZWFtLm5leHQoKTtcbiAgICByZXR1cm4gbnVsbDtcbiAgfTtcbn0iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=