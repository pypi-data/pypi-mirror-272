"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[3510],{

/***/ 13510:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ttcn": () => (/* binding */ ttcn)
/* harmony export */ });
function words(str) {
  var obj = {},
    words = str.split(" ");
  for (var i = 0; i < words.length; ++i) obj[words[i]] = true;
  return obj;
}
const parserConfig = {
  name: "ttcn",
  keywords: words("activate address alive all alt altstep and and4b any" + " break case component const continue control deactivate" + " display do else encode enumerated except exception" + " execute extends extension external for from function" + " goto group if import in infinity inout interleave" + " label language length log match message mixed mod" + " modifies module modulepar mtc noblock not not4b nowait" + " of on optional or or4b out override param pattern port" + " procedure record recursive rem repeat return runs select" + " self sender set signature system template testcase to" + " type union value valueof var variant while with xor xor4b"),
  builtin: words("bit2hex bit2int bit2oct bit2str char2int char2oct encvalue" + " decomp decvalue float2int float2str hex2bit hex2int" + " hex2oct hex2str int2bit int2char int2float int2hex" + " int2oct int2str int2unichar isbound ischosen ispresent" + " isvalue lengthof log2str oct2bit oct2char oct2hex oct2int" + " oct2str regexp replace rnd sizeof str2bit str2float" + " str2hex str2int str2oct substr unichar2int unichar2char" + " enum2int"),
  types: words("anytype bitstring boolean char charstring default float" + " hexstring integer objid octetstring universal verdicttype timer"),
  timerOps: words("read running start stop timeout"),
  portOps: words("call catch check clear getcall getreply halt raise receive" + " reply send trigger"),
  configOps: words("create connect disconnect done kill killed map unmap"),
  verdictOps: words("getverdict setverdict"),
  sutOps: words("action"),
  functionOps: words("apply derefers refers"),
  verdictConsts: words("error fail inconc none pass"),
  booleanConsts: words("true false"),
  otherConsts: words("null NULL omit"),
  visibilityModifiers: words("private public friend"),
  templateMatch: words("complement ifpresent subset superset permutation"),
  multiLineStrings: true
};
var wordList = [];
function add(obj) {
  if (obj) for (var prop in obj) if (obj.hasOwnProperty(prop)) wordList.push(prop);
}
add(parserConfig.keywords);
add(parserConfig.builtin);
add(parserConfig.timerOps);
add(parserConfig.portOps);
var keywords = parserConfig.keywords || {},
  builtin = parserConfig.builtin || {},
  timerOps = parserConfig.timerOps || {},
  portOps = parserConfig.portOps || {},
  configOps = parserConfig.configOps || {},
  verdictOps = parserConfig.verdictOps || {},
  sutOps = parserConfig.sutOps || {},
  functionOps = parserConfig.functionOps || {},
  verdictConsts = parserConfig.verdictConsts || {},
  booleanConsts = parserConfig.booleanConsts || {},
  otherConsts = parserConfig.otherConsts || {},
  types = parserConfig.types || {},
  visibilityModifiers = parserConfig.visibilityModifiers || {},
  templateMatch = parserConfig.templateMatch || {},
  multiLineStrings = parserConfig.multiLineStrings,
  indentStatements = parserConfig.indentStatements !== false;
var isOperatorChar = /[+\-*&@=<>!\/]/;
var curPunc;
function tokenBase(stream, state) {
  var ch = stream.next();
  if (ch == '"' || ch == "'") {
    state.tokenize = tokenString(ch);
    return state.tokenize(stream, state);
  }
  if (/[\[\]{}\(\),;\\:\?\.]/.test(ch)) {
    curPunc = ch;
    return "punctuation";
  }
  if (ch == "#") {
    stream.skipToEnd();
    return "atom";
  }
  if (ch == "%") {
    stream.eatWhile(/\b/);
    return "atom";
  }
  if (/\d/.test(ch)) {
    stream.eatWhile(/[\w\.]/);
    return "number";
  }
  if (ch == "/") {
    if (stream.eat("*")) {
      state.tokenize = tokenComment;
      return tokenComment(stream, state);
    }
    if (stream.eat("/")) {
      stream.skipToEnd();
      return "comment";
    }
  }
  if (isOperatorChar.test(ch)) {
    if (ch == "@") {
      if (stream.match("try") || stream.match("catch") || stream.match("lazy")) {
        return "keyword";
      }
    }
    stream.eatWhile(isOperatorChar);
    return "operator";
  }
  stream.eatWhile(/[\w\$_\xa1-\uffff]/);
  var cur = stream.current();
  if (keywords.propertyIsEnumerable(cur)) return "keyword";
  if (builtin.propertyIsEnumerable(cur)) return "builtin";
  if (timerOps.propertyIsEnumerable(cur)) return "def";
  if (configOps.propertyIsEnumerable(cur)) return "def";
  if (verdictOps.propertyIsEnumerable(cur)) return "def";
  if (portOps.propertyIsEnumerable(cur)) return "def";
  if (sutOps.propertyIsEnumerable(cur)) return "def";
  if (functionOps.propertyIsEnumerable(cur)) return "def";
  if (verdictConsts.propertyIsEnumerable(cur)) return "string";
  if (booleanConsts.propertyIsEnumerable(cur)) return "string";
  if (otherConsts.propertyIsEnumerable(cur)) return "string";
  if (types.propertyIsEnumerable(cur)) return "typeName.standard";
  if (visibilityModifiers.propertyIsEnumerable(cur)) return "modifier";
  if (templateMatch.propertyIsEnumerable(cur)) return "atom";
  return "variable";
}
function tokenString(quote) {
  return function (stream, state) {
    var escaped = false,
      next,
      end = false;
    while ((next = stream.next()) != null) {
      if (next == quote && !escaped) {
        var afterQuote = stream.peek();
        //look if the character after the quote is like the B in '10100010'B
        if (afterQuote) {
          afterQuote = afterQuote.toLowerCase();
          if (afterQuote == "b" || afterQuote == "h" || afterQuote == "o") stream.next();
        }
        end = true;
        break;
      }
      escaped = !escaped && next == "\\";
    }
    if (end || !(escaped || multiLineStrings)) state.tokenize = null;
    return "string";
  };
}
function tokenComment(stream, state) {
  var maybeEnd = false,
    ch;
  while (ch = stream.next()) {
    if (ch == "/" && maybeEnd) {
      state.tokenize = null;
      break;
    }
    maybeEnd = ch == "*";
  }
  return "comment";
}
function Context(indented, column, type, align, prev) {
  this.indented = indented;
  this.column = column;
  this.type = type;
  this.align = align;
  this.prev = prev;
}
function pushContext(state, col, type) {
  var indent = state.indented;
  if (state.context && state.context.type == "statement") indent = state.context.indented;
  return state.context = new Context(indent, col, type, null, state.context);
}
function popContext(state) {
  var t = state.context.type;
  if (t == ")" || t == "]" || t == "}") state.indented = state.context.indented;
  return state.context = state.context.prev;
}

//Interface
const ttcn = {
  name: "ttcn",
  startState: function () {
    return {
      tokenize: null,
      context: new Context(0, 0, "top", false),
      indented: 0,
      startOfLine: true
    };
  },
  token: function (stream, state) {
    var ctx = state.context;
    if (stream.sol()) {
      if (ctx.align == null) ctx.align = false;
      state.indented = stream.indentation();
      state.startOfLine = true;
    }
    if (stream.eatSpace()) return null;
    curPunc = null;
    var style = (state.tokenize || tokenBase)(stream, state);
    if (style == "comment") return style;
    if (ctx.align == null) ctx.align = true;
    if ((curPunc == ";" || curPunc == ":" || curPunc == ",") && ctx.type == "statement") {
      popContext(state);
    } else if (curPunc == "{") pushContext(state, stream.column(), "}");else if (curPunc == "[") pushContext(state, stream.column(), "]");else if (curPunc == "(") pushContext(state, stream.column(), ")");else if (curPunc == "}") {
      while (ctx.type == "statement") ctx = popContext(state);
      if (ctx.type == "}") ctx = popContext(state);
      while (ctx.type == "statement") ctx = popContext(state);
    } else if (curPunc == ctx.type) popContext(state);else if (indentStatements && ((ctx.type == "}" || ctx.type == "top") && curPunc != ';' || ctx.type == "statement" && curPunc == "newstatement")) pushContext(state, stream.column(), "statement");
    state.startOfLine = false;
    return style;
  },
  languageData: {
    indentOnInput: /^\s*[{}]$/,
    commentTokens: {
      line: "//",
      block: {
        open: "/*",
        close: "*/"
      }
    },
    autocomplete: wordList
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiMzUxMC5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGNvZGVtaXJyb3IvbGVnYWN5LW1vZGVzL21vZGUvdHRjbi5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyJmdW5jdGlvbiB3b3JkcyhzdHIpIHtcbiAgdmFyIG9iaiA9IHt9LFxuICAgIHdvcmRzID0gc3RyLnNwbGl0KFwiIFwiKTtcbiAgZm9yICh2YXIgaSA9IDA7IGkgPCB3b3Jkcy5sZW5ndGg7ICsraSkgb2JqW3dvcmRzW2ldXSA9IHRydWU7XG4gIHJldHVybiBvYmo7XG59XG5jb25zdCBwYXJzZXJDb25maWcgPSB7XG4gIG5hbWU6IFwidHRjblwiLFxuICBrZXl3b3Jkczogd29yZHMoXCJhY3RpdmF0ZSBhZGRyZXNzIGFsaXZlIGFsbCBhbHQgYWx0c3RlcCBhbmQgYW5kNGIgYW55XCIgKyBcIiBicmVhayBjYXNlIGNvbXBvbmVudCBjb25zdCBjb250aW51ZSBjb250cm9sIGRlYWN0aXZhdGVcIiArIFwiIGRpc3BsYXkgZG8gZWxzZSBlbmNvZGUgZW51bWVyYXRlZCBleGNlcHQgZXhjZXB0aW9uXCIgKyBcIiBleGVjdXRlIGV4dGVuZHMgZXh0ZW5zaW9uIGV4dGVybmFsIGZvciBmcm9tIGZ1bmN0aW9uXCIgKyBcIiBnb3RvIGdyb3VwIGlmIGltcG9ydCBpbiBpbmZpbml0eSBpbm91dCBpbnRlcmxlYXZlXCIgKyBcIiBsYWJlbCBsYW5ndWFnZSBsZW5ndGggbG9nIG1hdGNoIG1lc3NhZ2UgbWl4ZWQgbW9kXCIgKyBcIiBtb2RpZmllcyBtb2R1bGUgbW9kdWxlcGFyIG10YyBub2Jsb2NrIG5vdCBub3Q0YiBub3dhaXRcIiArIFwiIG9mIG9uIG9wdGlvbmFsIG9yIG9yNGIgb3V0IG92ZXJyaWRlIHBhcmFtIHBhdHRlcm4gcG9ydFwiICsgXCIgcHJvY2VkdXJlIHJlY29yZCByZWN1cnNpdmUgcmVtIHJlcGVhdCByZXR1cm4gcnVucyBzZWxlY3RcIiArIFwiIHNlbGYgc2VuZGVyIHNldCBzaWduYXR1cmUgc3lzdGVtIHRlbXBsYXRlIHRlc3RjYXNlIHRvXCIgKyBcIiB0eXBlIHVuaW9uIHZhbHVlIHZhbHVlb2YgdmFyIHZhcmlhbnQgd2hpbGUgd2l0aCB4b3IgeG9yNGJcIiksXG4gIGJ1aWx0aW46IHdvcmRzKFwiYml0MmhleCBiaXQyaW50IGJpdDJvY3QgYml0MnN0ciBjaGFyMmludCBjaGFyMm9jdCBlbmN2YWx1ZVwiICsgXCIgZGVjb21wIGRlY3ZhbHVlIGZsb2F0MmludCBmbG9hdDJzdHIgaGV4MmJpdCBoZXgyaW50XCIgKyBcIiBoZXgyb2N0IGhleDJzdHIgaW50MmJpdCBpbnQyY2hhciBpbnQyZmxvYXQgaW50MmhleFwiICsgXCIgaW50Mm9jdCBpbnQyc3RyIGludDJ1bmljaGFyIGlzYm91bmQgaXNjaG9zZW4gaXNwcmVzZW50XCIgKyBcIiBpc3ZhbHVlIGxlbmd0aG9mIGxvZzJzdHIgb2N0MmJpdCBvY3QyY2hhciBvY3QyaGV4IG9jdDJpbnRcIiArIFwiIG9jdDJzdHIgcmVnZXhwIHJlcGxhY2Ugcm5kIHNpemVvZiBzdHIyYml0IHN0cjJmbG9hdFwiICsgXCIgc3RyMmhleCBzdHIyaW50IHN0cjJvY3Qgc3Vic3RyIHVuaWNoYXIyaW50IHVuaWNoYXIyY2hhclwiICsgXCIgZW51bTJpbnRcIiksXG4gIHR5cGVzOiB3b3JkcyhcImFueXR5cGUgYml0c3RyaW5nIGJvb2xlYW4gY2hhciBjaGFyc3RyaW5nIGRlZmF1bHQgZmxvYXRcIiArIFwiIGhleHN0cmluZyBpbnRlZ2VyIG9iamlkIG9jdGV0c3RyaW5nIHVuaXZlcnNhbCB2ZXJkaWN0dHlwZSB0aW1lclwiKSxcbiAgdGltZXJPcHM6IHdvcmRzKFwicmVhZCBydW5uaW5nIHN0YXJ0IHN0b3AgdGltZW91dFwiKSxcbiAgcG9ydE9wczogd29yZHMoXCJjYWxsIGNhdGNoIGNoZWNrIGNsZWFyIGdldGNhbGwgZ2V0cmVwbHkgaGFsdCByYWlzZSByZWNlaXZlXCIgKyBcIiByZXBseSBzZW5kIHRyaWdnZXJcIiksXG4gIGNvbmZpZ09wczogd29yZHMoXCJjcmVhdGUgY29ubmVjdCBkaXNjb25uZWN0IGRvbmUga2lsbCBraWxsZWQgbWFwIHVubWFwXCIpLFxuICB2ZXJkaWN0T3BzOiB3b3JkcyhcImdldHZlcmRpY3Qgc2V0dmVyZGljdFwiKSxcbiAgc3V0T3BzOiB3b3JkcyhcImFjdGlvblwiKSxcbiAgZnVuY3Rpb25PcHM6IHdvcmRzKFwiYXBwbHkgZGVyZWZlcnMgcmVmZXJzXCIpLFxuICB2ZXJkaWN0Q29uc3RzOiB3b3JkcyhcImVycm9yIGZhaWwgaW5jb25jIG5vbmUgcGFzc1wiKSxcbiAgYm9vbGVhbkNvbnN0czogd29yZHMoXCJ0cnVlIGZhbHNlXCIpLFxuICBvdGhlckNvbnN0czogd29yZHMoXCJudWxsIE5VTEwgb21pdFwiKSxcbiAgdmlzaWJpbGl0eU1vZGlmaWVyczogd29yZHMoXCJwcml2YXRlIHB1YmxpYyBmcmllbmRcIiksXG4gIHRlbXBsYXRlTWF0Y2g6IHdvcmRzKFwiY29tcGxlbWVudCBpZnByZXNlbnQgc3Vic2V0IHN1cGVyc2V0IHBlcm11dGF0aW9uXCIpLFxuICBtdWx0aUxpbmVTdHJpbmdzOiB0cnVlXG59O1xudmFyIHdvcmRMaXN0ID0gW107XG5mdW5jdGlvbiBhZGQob2JqKSB7XG4gIGlmIChvYmopIGZvciAodmFyIHByb3AgaW4gb2JqKSBpZiAob2JqLmhhc093blByb3BlcnR5KHByb3ApKSB3b3JkTGlzdC5wdXNoKHByb3ApO1xufVxuYWRkKHBhcnNlckNvbmZpZy5rZXl3b3Jkcyk7XG5hZGQocGFyc2VyQ29uZmlnLmJ1aWx0aW4pO1xuYWRkKHBhcnNlckNvbmZpZy50aW1lck9wcyk7XG5hZGQocGFyc2VyQ29uZmlnLnBvcnRPcHMpO1xudmFyIGtleXdvcmRzID0gcGFyc2VyQ29uZmlnLmtleXdvcmRzIHx8IHt9LFxuICBidWlsdGluID0gcGFyc2VyQ29uZmlnLmJ1aWx0aW4gfHwge30sXG4gIHRpbWVyT3BzID0gcGFyc2VyQ29uZmlnLnRpbWVyT3BzIHx8IHt9LFxuICBwb3J0T3BzID0gcGFyc2VyQ29uZmlnLnBvcnRPcHMgfHwge30sXG4gIGNvbmZpZ09wcyA9IHBhcnNlckNvbmZpZy5jb25maWdPcHMgfHwge30sXG4gIHZlcmRpY3RPcHMgPSBwYXJzZXJDb25maWcudmVyZGljdE9wcyB8fCB7fSxcbiAgc3V0T3BzID0gcGFyc2VyQ29uZmlnLnN1dE9wcyB8fCB7fSxcbiAgZnVuY3Rpb25PcHMgPSBwYXJzZXJDb25maWcuZnVuY3Rpb25PcHMgfHwge30sXG4gIHZlcmRpY3RDb25zdHMgPSBwYXJzZXJDb25maWcudmVyZGljdENvbnN0cyB8fCB7fSxcbiAgYm9vbGVhbkNvbnN0cyA9IHBhcnNlckNvbmZpZy5ib29sZWFuQ29uc3RzIHx8IHt9LFxuICBvdGhlckNvbnN0cyA9IHBhcnNlckNvbmZpZy5vdGhlckNvbnN0cyB8fCB7fSxcbiAgdHlwZXMgPSBwYXJzZXJDb25maWcudHlwZXMgfHwge30sXG4gIHZpc2liaWxpdHlNb2RpZmllcnMgPSBwYXJzZXJDb25maWcudmlzaWJpbGl0eU1vZGlmaWVycyB8fCB7fSxcbiAgdGVtcGxhdGVNYXRjaCA9IHBhcnNlckNvbmZpZy50ZW1wbGF0ZU1hdGNoIHx8IHt9LFxuICBtdWx0aUxpbmVTdHJpbmdzID0gcGFyc2VyQ29uZmlnLm11bHRpTGluZVN0cmluZ3MsXG4gIGluZGVudFN0YXRlbWVudHMgPSBwYXJzZXJDb25maWcuaW5kZW50U3RhdGVtZW50cyAhPT0gZmFsc2U7XG52YXIgaXNPcGVyYXRvckNoYXIgPSAvWytcXC0qJkA9PD4hXFwvXS87XG52YXIgY3VyUHVuYztcbmZ1bmN0aW9uIHRva2VuQmFzZShzdHJlYW0sIHN0YXRlKSB7XG4gIHZhciBjaCA9IHN0cmVhbS5uZXh0KCk7XG4gIGlmIChjaCA9PSAnXCInIHx8IGNoID09IFwiJ1wiKSB7XG4gICAgc3RhdGUudG9rZW5pemUgPSB0b2tlblN0cmluZyhjaCk7XG4gICAgcmV0dXJuIHN0YXRlLnRva2VuaXplKHN0cmVhbSwgc3RhdGUpO1xuICB9XG4gIGlmICgvW1xcW1xcXXt9XFwoXFwpLDtcXFxcOlxcP1xcLl0vLnRlc3QoY2gpKSB7XG4gICAgY3VyUHVuYyA9IGNoO1xuICAgIHJldHVybiBcInB1bmN0dWF0aW9uXCI7XG4gIH1cbiAgaWYgKGNoID09IFwiI1wiKSB7XG4gICAgc3RyZWFtLnNraXBUb0VuZCgpO1xuICAgIHJldHVybiBcImF0b21cIjtcbiAgfVxuICBpZiAoY2ggPT0gXCIlXCIpIHtcbiAgICBzdHJlYW0uZWF0V2hpbGUoL1xcYi8pO1xuICAgIHJldHVybiBcImF0b21cIjtcbiAgfVxuICBpZiAoL1xcZC8udGVzdChjaCkpIHtcbiAgICBzdHJlYW0uZWF0V2hpbGUoL1tcXHdcXC5dLyk7XG4gICAgcmV0dXJuIFwibnVtYmVyXCI7XG4gIH1cbiAgaWYgKGNoID09IFwiL1wiKSB7XG4gICAgaWYgKHN0cmVhbS5lYXQoXCIqXCIpKSB7XG4gICAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQ29tbWVudDtcbiAgICAgIHJldHVybiB0b2tlbkNvbW1lbnQoc3RyZWFtLCBzdGF0ZSk7XG4gICAgfVxuICAgIGlmIChzdHJlYW0uZWF0KFwiL1wiKSkge1xuICAgICAgc3RyZWFtLnNraXBUb0VuZCgpO1xuICAgICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICAgIH1cbiAgfVxuICBpZiAoaXNPcGVyYXRvckNoYXIudGVzdChjaCkpIHtcbiAgICBpZiAoY2ggPT0gXCJAXCIpIHtcbiAgICAgIGlmIChzdHJlYW0ubWF0Y2goXCJ0cnlcIikgfHwgc3RyZWFtLm1hdGNoKFwiY2F0Y2hcIikgfHwgc3RyZWFtLm1hdGNoKFwibGF6eVwiKSkge1xuICAgICAgICByZXR1cm4gXCJrZXl3b3JkXCI7XG4gICAgICB9XG4gICAgfVxuICAgIHN0cmVhbS5lYXRXaGlsZShpc09wZXJhdG9yQ2hhcik7XG4gICAgcmV0dXJuIFwib3BlcmF0b3JcIjtcbiAgfVxuICBzdHJlYW0uZWF0V2hpbGUoL1tcXHdcXCRfXFx4YTEtXFx1ZmZmZl0vKTtcbiAgdmFyIGN1ciA9IHN0cmVhbS5jdXJyZW50KCk7XG4gIGlmIChrZXl3b3Jkcy5wcm9wZXJ0eUlzRW51bWVyYWJsZShjdXIpKSByZXR1cm4gXCJrZXl3b3JkXCI7XG4gIGlmIChidWlsdGluLnByb3BlcnR5SXNFbnVtZXJhYmxlKGN1cikpIHJldHVybiBcImJ1aWx0aW5cIjtcbiAgaWYgKHRpbWVyT3BzLnByb3BlcnR5SXNFbnVtZXJhYmxlKGN1cikpIHJldHVybiBcImRlZlwiO1xuICBpZiAoY29uZmlnT3BzLnByb3BlcnR5SXNFbnVtZXJhYmxlKGN1cikpIHJldHVybiBcImRlZlwiO1xuICBpZiAodmVyZGljdE9wcy5wcm9wZXJ0eUlzRW51bWVyYWJsZShjdXIpKSByZXR1cm4gXCJkZWZcIjtcbiAgaWYgKHBvcnRPcHMucHJvcGVydHlJc0VudW1lcmFibGUoY3VyKSkgcmV0dXJuIFwiZGVmXCI7XG4gIGlmIChzdXRPcHMucHJvcGVydHlJc0VudW1lcmFibGUoY3VyKSkgcmV0dXJuIFwiZGVmXCI7XG4gIGlmIChmdW5jdGlvbk9wcy5wcm9wZXJ0eUlzRW51bWVyYWJsZShjdXIpKSByZXR1cm4gXCJkZWZcIjtcbiAgaWYgKHZlcmRpY3RDb25zdHMucHJvcGVydHlJc0VudW1lcmFibGUoY3VyKSkgcmV0dXJuIFwic3RyaW5nXCI7XG4gIGlmIChib29sZWFuQ29uc3RzLnByb3BlcnR5SXNFbnVtZXJhYmxlKGN1cikpIHJldHVybiBcInN0cmluZ1wiO1xuICBpZiAob3RoZXJDb25zdHMucHJvcGVydHlJc0VudW1lcmFibGUoY3VyKSkgcmV0dXJuIFwic3RyaW5nXCI7XG4gIGlmICh0eXBlcy5wcm9wZXJ0eUlzRW51bWVyYWJsZShjdXIpKSByZXR1cm4gXCJ0eXBlTmFtZS5zdGFuZGFyZFwiO1xuICBpZiAodmlzaWJpbGl0eU1vZGlmaWVycy5wcm9wZXJ0eUlzRW51bWVyYWJsZShjdXIpKSByZXR1cm4gXCJtb2RpZmllclwiO1xuICBpZiAodGVtcGxhdGVNYXRjaC5wcm9wZXJ0eUlzRW51bWVyYWJsZShjdXIpKSByZXR1cm4gXCJhdG9tXCI7XG4gIHJldHVybiBcInZhcmlhYmxlXCI7XG59XG5mdW5jdGlvbiB0b2tlblN0cmluZyhxdW90ZSkge1xuICByZXR1cm4gZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICB2YXIgZXNjYXBlZCA9IGZhbHNlLFxuICAgICAgbmV4dCxcbiAgICAgIGVuZCA9IGZhbHNlO1xuICAgIHdoaWxlICgobmV4dCA9IHN0cmVhbS5uZXh0KCkpICE9IG51bGwpIHtcbiAgICAgIGlmIChuZXh0ID09IHF1b3RlICYmICFlc2NhcGVkKSB7XG4gICAgICAgIHZhciBhZnRlclF1b3RlID0gc3RyZWFtLnBlZWsoKTtcbiAgICAgICAgLy9sb29rIGlmIHRoZSBjaGFyYWN0ZXIgYWZ0ZXIgdGhlIHF1b3RlIGlzIGxpa2UgdGhlIEIgaW4gJzEwMTAwMDEwJ0JcbiAgICAgICAgaWYgKGFmdGVyUXVvdGUpIHtcbiAgICAgICAgICBhZnRlclF1b3RlID0gYWZ0ZXJRdW90ZS50b0xvd2VyQ2FzZSgpO1xuICAgICAgICAgIGlmIChhZnRlclF1b3RlID09IFwiYlwiIHx8IGFmdGVyUXVvdGUgPT0gXCJoXCIgfHwgYWZ0ZXJRdW90ZSA9PSBcIm9cIikgc3RyZWFtLm5leHQoKTtcbiAgICAgICAgfVxuICAgICAgICBlbmQgPSB0cnVlO1xuICAgICAgICBicmVhaztcbiAgICAgIH1cbiAgICAgIGVzY2FwZWQgPSAhZXNjYXBlZCAmJiBuZXh0ID09IFwiXFxcXFwiO1xuICAgIH1cbiAgICBpZiAoZW5kIHx8ICEoZXNjYXBlZCB8fCBtdWx0aUxpbmVTdHJpbmdzKSkgc3RhdGUudG9rZW5pemUgPSBudWxsO1xuICAgIHJldHVybiBcInN0cmluZ1wiO1xuICB9O1xufVxuZnVuY3Rpb24gdG9rZW5Db21tZW50KHN0cmVhbSwgc3RhdGUpIHtcbiAgdmFyIG1heWJlRW5kID0gZmFsc2UsXG4gICAgY2g7XG4gIHdoaWxlIChjaCA9IHN0cmVhbS5uZXh0KCkpIHtcbiAgICBpZiAoY2ggPT0gXCIvXCIgJiYgbWF5YmVFbmQpIHtcbiAgICAgIHN0YXRlLnRva2VuaXplID0gbnVsbDtcbiAgICAgIGJyZWFrO1xuICAgIH1cbiAgICBtYXliZUVuZCA9IGNoID09IFwiKlwiO1xuICB9XG4gIHJldHVybiBcImNvbW1lbnRcIjtcbn1cbmZ1bmN0aW9uIENvbnRleHQoaW5kZW50ZWQsIGNvbHVtbiwgdHlwZSwgYWxpZ24sIHByZXYpIHtcbiAgdGhpcy5pbmRlbnRlZCA9IGluZGVudGVkO1xuICB0aGlzLmNvbHVtbiA9IGNvbHVtbjtcbiAgdGhpcy50eXBlID0gdHlwZTtcbiAgdGhpcy5hbGlnbiA9IGFsaWduO1xuICB0aGlzLnByZXYgPSBwcmV2O1xufVxuZnVuY3Rpb24gcHVzaENvbnRleHQoc3RhdGUsIGNvbCwgdHlwZSkge1xuICB2YXIgaW5kZW50ID0gc3RhdGUuaW5kZW50ZWQ7XG4gIGlmIChzdGF0ZS5jb250ZXh0ICYmIHN0YXRlLmNvbnRleHQudHlwZSA9PSBcInN0YXRlbWVudFwiKSBpbmRlbnQgPSBzdGF0ZS5jb250ZXh0LmluZGVudGVkO1xuICByZXR1cm4gc3RhdGUuY29udGV4dCA9IG5ldyBDb250ZXh0KGluZGVudCwgY29sLCB0eXBlLCBudWxsLCBzdGF0ZS5jb250ZXh0KTtcbn1cbmZ1bmN0aW9uIHBvcENvbnRleHQoc3RhdGUpIHtcbiAgdmFyIHQgPSBzdGF0ZS5jb250ZXh0LnR5cGU7XG4gIGlmICh0ID09IFwiKVwiIHx8IHQgPT0gXCJdXCIgfHwgdCA9PSBcIn1cIikgc3RhdGUuaW5kZW50ZWQgPSBzdGF0ZS5jb250ZXh0LmluZGVudGVkO1xuICByZXR1cm4gc3RhdGUuY29udGV4dCA9IHN0YXRlLmNvbnRleHQucHJldjtcbn1cblxuLy9JbnRlcmZhY2VcbmV4cG9ydCBjb25zdCB0dGNuID0ge1xuICBuYW1lOiBcInR0Y25cIixcbiAgc3RhcnRTdGF0ZTogZnVuY3Rpb24gKCkge1xuICAgIHJldHVybiB7XG4gICAgICB0b2tlbml6ZTogbnVsbCxcbiAgICAgIGNvbnRleHQ6IG5ldyBDb250ZXh0KDAsIDAsIFwidG9wXCIsIGZhbHNlKSxcbiAgICAgIGluZGVudGVkOiAwLFxuICAgICAgc3RhcnRPZkxpbmU6IHRydWVcbiAgICB9O1xuICB9LFxuICB0b2tlbjogZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICB2YXIgY3R4ID0gc3RhdGUuY29udGV4dDtcbiAgICBpZiAoc3RyZWFtLnNvbCgpKSB7XG4gICAgICBpZiAoY3R4LmFsaWduID09IG51bGwpIGN0eC5hbGlnbiA9IGZhbHNlO1xuICAgICAgc3RhdGUuaW5kZW50ZWQgPSBzdHJlYW0uaW5kZW50YXRpb24oKTtcbiAgICAgIHN0YXRlLnN0YXJ0T2ZMaW5lID0gdHJ1ZTtcbiAgICB9XG4gICAgaWYgKHN0cmVhbS5lYXRTcGFjZSgpKSByZXR1cm4gbnVsbDtcbiAgICBjdXJQdW5jID0gbnVsbDtcbiAgICB2YXIgc3R5bGUgPSAoc3RhdGUudG9rZW5pemUgfHwgdG9rZW5CYXNlKShzdHJlYW0sIHN0YXRlKTtcbiAgICBpZiAoc3R5bGUgPT0gXCJjb21tZW50XCIpIHJldHVybiBzdHlsZTtcbiAgICBpZiAoY3R4LmFsaWduID09IG51bGwpIGN0eC5hbGlnbiA9IHRydWU7XG4gICAgaWYgKChjdXJQdW5jID09IFwiO1wiIHx8IGN1clB1bmMgPT0gXCI6XCIgfHwgY3VyUHVuYyA9PSBcIixcIikgJiYgY3R4LnR5cGUgPT0gXCJzdGF0ZW1lbnRcIikge1xuICAgICAgcG9wQ29udGV4dChzdGF0ZSk7XG4gICAgfSBlbHNlIGlmIChjdXJQdW5jID09IFwie1wiKSBwdXNoQ29udGV4dChzdGF0ZSwgc3RyZWFtLmNvbHVtbigpLCBcIn1cIik7ZWxzZSBpZiAoY3VyUHVuYyA9PSBcIltcIikgcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbS5jb2x1bW4oKSwgXCJdXCIpO2Vsc2UgaWYgKGN1clB1bmMgPT0gXCIoXCIpIHB1c2hDb250ZXh0KHN0YXRlLCBzdHJlYW0uY29sdW1uKCksIFwiKVwiKTtlbHNlIGlmIChjdXJQdW5jID09IFwifVwiKSB7XG4gICAgICB3aGlsZSAoY3R4LnR5cGUgPT0gXCJzdGF0ZW1lbnRcIikgY3R4ID0gcG9wQ29udGV4dChzdGF0ZSk7XG4gICAgICBpZiAoY3R4LnR5cGUgPT0gXCJ9XCIpIGN0eCA9IHBvcENvbnRleHQoc3RhdGUpO1xuICAgICAgd2hpbGUgKGN0eC50eXBlID09IFwic3RhdGVtZW50XCIpIGN0eCA9IHBvcENvbnRleHQoc3RhdGUpO1xuICAgIH0gZWxzZSBpZiAoY3VyUHVuYyA9PSBjdHgudHlwZSkgcG9wQ29udGV4dChzdGF0ZSk7ZWxzZSBpZiAoaW5kZW50U3RhdGVtZW50cyAmJiAoKGN0eC50eXBlID09IFwifVwiIHx8IGN0eC50eXBlID09IFwidG9wXCIpICYmIGN1clB1bmMgIT0gJzsnIHx8IGN0eC50eXBlID09IFwic3RhdGVtZW50XCIgJiYgY3VyUHVuYyA9PSBcIm5ld3N0YXRlbWVudFwiKSkgcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbS5jb2x1bW4oKSwgXCJzdGF0ZW1lbnRcIik7XG4gICAgc3RhdGUuc3RhcnRPZkxpbmUgPSBmYWxzZTtcbiAgICByZXR1cm4gc3R5bGU7XG4gIH0sXG4gIGxhbmd1YWdlRGF0YToge1xuICAgIGluZGVudE9uSW5wdXQ6IC9eXFxzKlt7fV0kLyxcbiAgICBjb21tZW50VG9rZW5zOiB7XG4gICAgICBsaW5lOiBcIi8vXCIsXG4gICAgICBibG9jazoge1xuICAgICAgICBvcGVuOiBcIi8qXCIsXG4gICAgICAgIGNsb3NlOiBcIiovXCJcbiAgICAgIH1cbiAgICB9LFxuICAgIGF1dG9jb21wbGV0ZTogd29yZExpc3RcbiAgfVxufTsiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=