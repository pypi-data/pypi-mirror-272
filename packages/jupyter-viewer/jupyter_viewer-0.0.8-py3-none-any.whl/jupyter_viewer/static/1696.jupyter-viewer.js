"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[1696],{

/***/ 31696:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ecl": () => (/* binding */ ecl)
/* harmony export */ });
function words(str) {
  var obj = {},
    words = str.split(" ");
  for (var i = 0; i < words.length; ++i) obj[words[i]] = true;
  return obj;
}
function metaHook(stream, state) {
  if (!state.startOfLine) return false;
  stream.skipToEnd();
  return "meta";
}
var keyword = words("abs acos allnodes ascii asin asstring atan atan2 ave case choose choosen choosesets clustersize combine correlation cos cosh count covariance cron dataset dedup define denormalize distribute distributed distribution ebcdic enth error evaluate event eventextra eventname exists exp failcode failmessage fetch fromunicode getisvalid global graph group hash hash32 hash64 hashcrc hashmd5 having if index intformat isvalid iterate join keyunicode length library limit ln local log loop map matched matchlength matchposition matchtext matchunicode max merge mergejoin min nolocal nonempty normalize parse pipe power preload process project pull random range rank ranked realformat recordof regexfind regexreplace regroup rejected rollup round roundup row rowdiff sample set sin sinh sizeof soapcall sort sorted sqrt stepped stored sum table tan tanh thisnode topn tounicode transfer trim truncate typeof ungroup unicodeorder variance which workunit xmldecode xmlencode xmltext xmlunicode");
var variable = words("apply assert build buildindex evaluate fail keydiff keypatch loadxml nothor notify output parallel sequential soapcall wait");
var variable_2 = words("__compressed__ all and any as atmost before beginc++ best between case const counter csv descend encrypt end endc++ endmacro except exclusive expire export extend false few first flat from full function group header heading hole ifblock import in interface joined keep keyed last left limit load local locale lookup macro many maxcount maxlength min skew module named nocase noroot noscan nosort not of only opt or outer overwrite packed partition penalty physicallength pipe quote record relationship repeat return right scan self separator service shared skew skip sql store terminator thor threshold token transform trim true type unicodeorder unsorted validate virtual whole wild within xml xpath");
var variable_3 = words("ascii big_endian boolean data decimal ebcdic integer pattern qstring real record rule set of string token udecimal unicode unsigned varstring varunicode");
var builtin = words("checkpoint deprecated failcode failmessage failure global independent onwarning persist priority recovery stored success wait when");
var blockKeywords = words("catch class do else finally for if switch try while");
var atoms = words("true false null");
var hooks = {
  "#": metaHook
};
var isOperatorChar = /[+\-*&%=<>!?|\/]/;
var curPunc;
function tokenBase(stream, state) {
  var ch = stream.next();
  if (hooks[ch]) {
    var result = hooks[ch](stream, state);
    if (result !== false) return result;
  }
  if (ch == '"' || ch == "'") {
    state.tokenize = tokenString(ch);
    return state.tokenize(stream, state);
  }
  if (/[\[\]{}\(\),;\:\.]/.test(ch)) {
    curPunc = ch;
    return null;
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
    stream.eatWhile(isOperatorChar);
    return "operator";
  }
  stream.eatWhile(/[\w\$_]/);
  var cur = stream.current().toLowerCase();
  if (keyword.propertyIsEnumerable(cur)) {
    if (blockKeywords.propertyIsEnumerable(cur)) curPunc = "newstatement";
    return "keyword";
  } else if (variable.propertyIsEnumerable(cur)) {
    if (blockKeywords.propertyIsEnumerable(cur)) curPunc = "newstatement";
    return "variable";
  } else if (variable_2.propertyIsEnumerable(cur)) {
    if (blockKeywords.propertyIsEnumerable(cur)) curPunc = "newstatement";
    return "modifier";
  } else if (variable_3.propertyIsEnumerable(cur)) {
    if (blockKeywords.propertyIsEnumerable(cur)) curPunc = "newstatement";
    return "type";
  } else if (builtin.propertyIsEnumerable(cur)) {
    if (blockKeywords.propertyIsEnumerable(cur)) curPunc = "newstatement";
    return "builtin";
  } else {
    //Data types are of from KEYWORD##
    var i = cur.length - 1;
    while (i >= 0 && (!isNaN(cur[i]) || cur[i] == '_')) --i;
    if (i > 0) {
      var cur2 = cur.substr(0, i + 1);
      if (variable_3.propertyIsEnumerable(cur2)) {
        if (blockKeywords.propertyIsEnumerable(cur2)) curPunc = "newstatement";
        return "type";
      }
    }
  }
  if (atoms.propertyIsEnumerable(cur)) return "atom";
  return null;
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
    if (end || !escaped) state.tokenize = tokenBase;
    return "string";
  };
}
function tokenComment(stream, state) {
  var maybeEnd = false,
    ch;
  while (ch = stream.next()) {
    if (ch == "/" && maybeEnd) {
      state.tokenize = tokenBase;
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
  return state.context = new Context(state.indented, col, type, null, state.context);
}
function popContext(state) {
  var t = state.context.type;
  if (t == ")" || t == "]" || t == "}") state.indented = state.context.indented;
  return state.context = state.context.prev;
}

// Interface

const ecl = {
  name: "ecl",
  startState: function (indentUnit) {
    return {
      tokenize: null,
      context: new Context(-indentUnit, 0, "top", false),
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
    if (style == "comment" || style == "meta") return style;
    if (ctx.align == null) ctx.align = true;
    if ((curPunc == ";" || curPunc == ":") && ctx.type == "statement") popContext(state);else if (curPunc == "{") pushContext(state, stream.column(), "}");else if (curPunc == "[") pushContext(state, stream.column(), "]");else if (curPunc == "(") pushContext(state, stream.column(), ")");else if (curPunc == "}") {
      while (ctx.type == "statement") ctx = popContext(state);
      if (ctx.type == "}") ctx = popContext(state);
      while (ctx.type == "statement") ctx = popContext(state);
    } else if (curPunc == ctx.type) popContext(state);else if (ctx.type == "}" || ctx.type == "top" || ctx.type == "statement" && curPunc == "newstatement") pushContext(state, stream.column(), "statement");
    state.startOfLine = false;
    return style;
  },
  indent: function (state, textAfter, cx) {
    if (state.tokenize != tokenBase && state.tokenize != null) return 0;
    var ctx = state.context,
      firstChar = textAfter && textAfter.charAt(0);
    if (ctx.type == "statement" && firstChar == "}") ctx = ctx.prev;
    var closing = firstChar == ctx.type;
    if (ctx.type == "statement") return ctx.indented + (firstChar == "{" ? 0 : cx.unit);else if (ctx.align) return ctx.column + (closing ? 0 : 1);else return ctx.indented + (closing ? 0 : cx.unit);
  },
  languageData: {
    indentOnInput: /^\s*[{}]$/
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiMTY5Ni5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL0Bjb2RlbWlycm9yL2xlZ2FjeS1tb2Rlcy9tb2RlL2VjbC5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyJmdW5jdGlvbiB3b3JkcyhzdHIpIHtcbiAgdmFyIG9iaiA9IHt9LFxuICAgIHdvcmRzID0gc3RyLnNwbGl0KFwiIFwiKTtcbiAgZm9yICh2YXIgaSA9IDA7IGkgPCB3b3Jkcy5sZW5ndGg7ICsraSkgb2JqW3dvcmRzW2ldXSA9IHRydWU7XG4gIHJldHVybiBvYmo7XG59XG5mdW5jdGlvbiBtZXRhSG9vayhzdHJlYW0sIHN0YXRlKSB7XG4gIGlmICghc3RhdGUuc3RhcnRPZkxpbmUpIHJldHVybiBmYWxzZTtcbiAgc3RyZWFtLnNraXBUb0VuZCgpO1xuICByZXR1cm4gXCJtZXRhXCI7XG59XG52YXIga2V5d29yZCA9IHdvcmRzKFwiYWJzIGFjb3MgYWxsbm9kZXMgYXNjaWkgYXNpbiBhc3N0cmluZyBhdGFuIGF0YW4yIGF2ZSBjYXNlIGNob29zZSBjaG9vc2VuIGNob29zZXNldHMgY2x1c3RlcnNpemUgY29tYmluZSBjb3JyZWxhdGlvbiBjb3MgY29zaCBjb3VudCBjb3ZhcmlhbmNlIGNyb24gZGF0YXNldCBkZWR1cCBkZWZpbmUgZGVub3JtYWxpemUgZGlzdHJpYnV0ZSBkaXN0cmlidXRlZCBkaXN0cmlidXRpb24gZWJjZGljIGVudGggZXJyb3IgZXZhbHVhdGUgZXZlbnQgZXZlbnRleHRyYSBldmVudG5hbWUgZXhpc3RzIGV4cCBmYWlsY29kZSBmYWlsbWVzc2FnZSBmZXRjaCBmcm9tdW5pY29kZSBnZXRpc3ZhbGlkIGdsb2JhbCBncmFwaCBncm91cCBoYXNoIGhhc2gzMiBoYXNoNjQgaGFzaGNyYyBoYXNobWQ1IGhhdmluZyBpZiBpbmRleCBpbnRmb3JtYXQgaXN2YWxpZCBpdGVyYXRlIGpvaW4ga2V5dW5pY29kZSBsZW5ndGggbGlicmFyeSBsaW1pdCBsbiBsb2NhbCBsb2cgbG9vcCBtYXAgbWF0Y2hlZCBtYXRjaGxlbmd0aCBtYXRjaHBvc2l0aW9uIG1hdGNodGV4dCBtYXRjaHVuaWNvZGUgbWF4IG1lcmdlIG1lcmdlam9pbiBtaW4gbm9sb2NhbCBub25lbXB0eSBub3JtYWxpemUgcGFyc2UgcGlwZSBwb3dlciBwcmVsb2FkIHByb2Nlc3MgcHJvamVjdCBwdWxsIHJhbmRvbSByYW5nZSByYW5rIHJhbmtlZCByZWFsZm9ybWF0IHJlY29yZG9mIHJlZ2V4ZmluZCByZWdleHJlcGxhY2UgcmVncm91cCByZWplY3RlZCByb2xsdXAgcm91bmQgcm91bmR1cCByb3cgcm93ZGlmZiBzYW1wbGUgc2V0IHNpbiBzaW5oIHNpemVvZiBzb2FwY2FsbCBzb3J0IHNvcnRlZCBzcXJ0IHN0ZXBwZWQgc3RvcmVkIHN1bSB0YWJsZSB0YW4gdGFuaCB0aGlzbm9kZSB0b3BuIHRvdW5pY29kZSB0cmFuc2ZlciB0cmltIHRydW5jYXRlIHR5cGVvZiB1bmdyb3VwIHVuaWNvZGVvcmRlciB2YXJpYW5jZSB3aGljaCB3b3JrdW5pdCB4bWxkZWNvZGUgeG1sZW5jb2RlIHhtbHRleHQgeG1sdW5pY29kZVwiKTtcbnZhciB2YXJpYWJsZSA9IHdvcmRzKFwiYXBwbHkgYXNzZXJ0IGJ1aWxkIGJ1aWxkaW5kZXggZXZhbHVhdGUgZmFpbCBrZXlkaWZmIGtleXBhdGNoIGxvYWR4bWwgbm90aG9yIG5vdGlmeSBvdXRwdXQgcGFyYWxsZWwgc2VxdWVudGlhbCBzb2FwY2FsbCB3YWl0XCIpO1xudmFyIHZhcmlhYmxlXzIgPSB3b3JkcyhcIl9fY29tcHJlc3NlZF9fIGFsbCBhbmQgYW55IGFzIGF0bW9zdCBiZWZvcmUgYmVnaW5jKysgYmVzdCBiZXR3ZWVuIGNhc2UgY29uc3QgY291bnRlciBjc3YgZGVzY2VuZCBlbmNyeXB0IGVuZCBlbmRjKysgZW5kbWFjcm8gZXhjZXB0IGV4Y2x1c2l2ZSBleHBpcmUgZXhwb3J0IGV4dGVuZCBmYWxzZSBmZXcgZmlyc3QgZmxhdCBmcm9tIGZ1bGwgZnVuY3Rpb24gZ3JvdXAgaGVhZGVyIGhlYWRpbmcgaG9sZSBpZmJsb2NrIGltcG9ydCBpbiBpbnRlcmZhY2Ugam9pbmVkIGtlZXAga2V5ZWQgbGFzdCBsZWZ0IGxpbWl0IGxvYWQgbG9jYWwgbG9jYWxlIGxvb2t1cCBtYWNybyBtYW55IG1heGNvdW50IG1heGxlbmd0aCBtaW4gc2tldyBtb2R1bGUgbmFtZWQgbm9jYXNlIG5vcm9vdCBub3NjYW4gbm9zb3J0IG5vdCBvZiBvbmx5IG9wdCBvciBvdXRlciBvdmVyd3JpdGUgcGFja2VkIHBhcnRpdGlvbiBwZW5hbHR5IHBoeXNpY2FsbGVuZ3RoIHBpcGUgcXVvdGUgcmVjb3JkIHJlbGF0aW9uc2hpcCByZXBlYXQgcmV0dXJuIHJpZ2h0IHNjYW4gc2VsZiBzZXBhcmF0b3Igc2VydmljZSBzaGFyZWQgc2tldyBza2lwIHNxbCBzdG9yZSB0ZXJtaW5hdG9yIHRob3IgdGhyZXNob2xkIHRva2VuIHRyYW5zZm9ybSB0cmltIHRydWUgdHlwZSB1bmljb2Rlb3JkZXIgdW5zb3J0ZWQgdmFsaWRhdGUgdmlydHVhbCB3aG9sZSB3aWxkIHdpdGhpbiB4bWwgeHBhdGhcIik7XG52YXIgdmFyaWFibGVfMyA9IHdvcmRzKFwiYXNjaWkgYmlnX2VuZGlhbiBib29sZWFuIGRhdGEgZGVjaW1hbCBlYmNkaWMgaW50ZWdlciBwYXR0ZXJuIHFzdHJpbmcgcmVhbCByZWNvcmQgcnVsZSBzZXQgb2Ygc3RyaW5nIHRva2VuIHVkZWNpbWFsIHVuaWNvZGUgdW5zaWduZWQgdmFyc3RyaW5nIHZhcnVuaWNvZGVcIik7XG52YXIgYnVpbHRpbiA9IHdvcmRzKFwiY2hlY2twb2ludCBkZXByZWNhdGVkIGZhaWxjb2RlIGZhaWxtZXNzYWdlIGZhaWx1cmUgZ2xvYmFsIGluZGVwZW5kZW50IG9ud2FybmluZyBwZXJzaXN0IHByaW9yaXR5IHJlY292ZXJ5IHN0b3JlZCBzdWNjZXNzIHdhaXQgd2hlblwiKTtcbnZhciBibG9ja0tleXdvcmRzID0gd29yZHMoXCJjYXRjaCBjbGFzcyBkbyBlbHNlIGZpbmFsbHkgZm9yIGlmIHN3aXRjaCB0cnkgd2hpbGVcIik7XG52YXIgYXRvbXMgPSB3b3JkcyhcInRydWUgZmFsc2UgbnVsbFwiKTtcbnZhciBob29rcyA9IHtcbiAgXCIjXCI6IG1ldGFIb29rXG59O1xudmFyIGlzT3BlcmF0b3JDaGFyID0gL1srXFwtKiYlPTw+IT98XFwvXS87XG52YXIgY3VyUHVuYztcbmZ1bmN0aW9uIHRva2VuQmFzZShzdHJlYW0sIHN0YXRlKSB7XG4gIHZhciBjaCA9IHN0cmVhbS5uZXh0KCk7XG4gIGlmIChob29rc1tjaF0pIHtcbiAgICB2YXIgcmVzdWx0ID0gaG9va3NbY2hdKHN0cmVhbSwgc3RhdGUpO1xuICAgIGlmIChyZXN1bHQgIT09IGZhbHNlKSByZXR1cm4gcmVzdWx0O1xuICB9XG4gIGlmIChjaCA9PSAnXCInIHx8IGNoID09IFwiJ1wiKSB7XG4gICAgc3RhdGUudG9rZW5pemUgPSB0b2tlblN0cmluZyhjaCk7XG4gICAgcmV0dXJuIHN0YXRlLnRva2VuaXplKHN0cmVhbSwgc3RhdGUpO1xuICB9XG4gIGlmICgvW1xcW1xcXXt9XFwoXFwpLDtcXDpcXC5dLy50ZXN0KGNoKSkge1xuICAgIGN1clB1bmMgPSBjaDtcbiAgICByZXR1cm4gbnVsbDtcbiAgfVxuICBpZiAoL1xcZC8udGVzdChjaCkpIHtcbiAgICBzdHJlYW0uZWF0V2hpbGUoL1tcXHdcXC5dLyk7XG4gICAgcmV0dXJuIFwibnVtYmVyXCI7XG4gIH1cbiAgaWYgKGNoID09IFwiL1wiKSB7XG4gICAgaWYgKHN0cmVhbS5lYXQoXCIqXCIpKSB7XG4gICAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQ29tbWVudDtcbiAgICAgIHJldHVybiB0b2tlbkNvbW1lbnQoc3RyZWFtLCBzdGF0ZSk7XG4gICAgfVxuICAgIGlmIChzdHJlYW0uZWF0KFwiL1wiKSkge1xuICAgICAgc3RyZWFtLnNraXBUb0VuZCgpO1xuICAgICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICAgIH1cbiAgfVxuICBpZiAoaXNPcGVyYXRvckNoYXIudGVzdChjaCkpIHtcbiAgICBzdHJlYW0uZWF0V2hpbGUoaXNPcGVyYXRvckNoYXIpO1xuICAgIHJldHVybiBcIm9wZXJhdG9yXCI7XG4gIH1cbiAgc3RyZWFtLmVhdFdoaWxlKC9bXFx3XFwkX10vKTtcbiAgdmFyIGN1ciA9IHN0cmVhbS5jdXJyZW50KCkudG9Mb3dlckNhc2UoKTtcbiAgaWYgKGtleXdvcmQucHJvcGVydHlJc0VudW1lcmFibGUoY3VyKSkge1xuICAgIGlmIChibG9ja0tleXdvcmRzLnByb3BlcnR5SXNFbnVtZXJhYmxlKGN1cikpIGN1clB1bmMgPSBcIm5ld3N0YXRlbWVudFwiO1xuICAgIHJldHVybiBcImtleXdvcmRcIjtcbiAgfSBlbHNlIGlmICh2YXJpYWJsZS5wcm9wZXJ0eUlzRW51bWVyYWJsZShjdXIpKSB7XG4gICAgaWYgKGJsb2NrS2V5d29yZHMucHJvcGVydHlJc0VudW1lcmFibGUoY3VyKSkgY3VyUHVuYyA9IFwibmV3c3RhdGVtZW50XCI7XG4gICAgcmV0dXJuIFwidmFyaWFibGVcIjtcbiAgfSBlbHNlIGlmICh2YXJpYWJsZV8yLnByb3BlcnR5SXNFbnVtZXJhYmxlKGN1cikpIHtcbiAgICBpZiAoYmxvY2tLZXl3b3Jkcy5wcm9wZXJ0eUlzRW51bWVyYWJsZShjdXIpKSBjdXJQdW5jID0gXCJuZXdzdGF0ZW1lbnRcIjtcbiAgICByZXR1cm4gXCJtb2RpZmllclwiO1xuICB9IGVsc2UgaWYgKHZhcmlhYmxlXzMucHJvcGVydHlJc0VudW1lcmFibGUoY3VyKSkge1xuICAgIGlmIChibG9ja0tleXdvcmRzLnByb3BlcnR5SXNFbnVtZXJhYmxlKGN1cikpIGN1clB1bmMgPSBcIm5ld3N0YXRlbWVudFwiO1xuICAgIHJldHVybiBcInR5cGVcIjtcbiAgfSBlbHNlIGlmIChidWlsdGluLnByb3BlcnR5SXNFbnVtZXJhYmxlKGN1cikpIHtcbiAgICBpZiAoYmxvY2tLZXl3b3Jkcy5wcm9wZXJ0eUlzRW51bWVyYWJsZShjdXIpKSBjdXJQdW5jID0gXCJuZXdzdGF0ZW1lbnRcIjtcbiAgICByZXR1cm4gXCJidWlsdGluXCI7XG4gIH0gZWxzZSB7XG4gICAgLy9EYXRhIHR5cGVzIGFyZSBvZiBmcm9tIEtFWVdPUkQjI1xuICAgIHZhciBpID0gY3VyLmxlbmd0aCAtIDE7XG4gICAgd2hpbGUgKGkgPj0gMCAmJiAoIWlzTmFOKGN1cltpXSkgfHwgY3VyW2ldID09ICdfJykpIC0taTtcbiAgICBpZiAoaSA+IDApIHtcbiAgICAgIHZhciBjdXIyID0gY3VyLnN1YnN0cigwLCBpICsgMSk7XG4gICAgICBpZiAodmFyaWFibGVfMy5wcm9wZXJ0eUlzRW51bWVyYWJsZShjdXIyKSkge1xuICAgICAgICBpZiAoYmxvY2tLZXl3b3Jkcy5wcm9wZXJ0eUlzRW51bWVyYWJsZShjdXIyKSkgY3VyUHVuYyA9IFwibmV3c3RhdGVtZW50XCI7XG4gICAgICAgIHJldHVybiBcInR5cGVcIjtcbiAgICAgIH1cbiAgICB9XG4gIH1cbiAgaWYgKGF0b21zLnByb3BlcnR5SXNFbnVtZXJhYmxlKGN1cikpIHJldHVybiBcImF0b21cIjtcbiAgcmV0dXJuIG51bGw7XG59XG5mdW5jdGlvbiB0b2tlblN0cmluZyhxdW90ZSkge1xuICByZXR1cm4gZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICB2YXIgZXNjYXBlZCA9IGZhbHNlLFxuICAgICAgbmV4dCxcbiAgICAgIGVuZCA9IGZhbHNlO1xuICAgIHdoaWxlICgobmV4dCA9IHN0cmVhbS5uZXh0KCkpICE9IG51bGwpIHtcbiAgICAgIGlmIChuZXh0ID09IHF1b3RlICYmICFlc2NhcGVkKSB7XG4gICAgICAgIGVuZCA9IHRydWU7XG4gICAgICAgIGJyZWFrO1xuICAgICAgfVxuICAgICAgZXNjYXBlZCA9ICFlc2NhcGVkICYmIG5leHQgPT0gXCJcXFxcXCI7XG4gICAgfVxuICAgIGlmIChlbmQgfHwgIWVzY2FwZWQpIHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlO1xuICAgIHJldHVybiBcInN0cmluZ1wiO1xuICB9O1xufVxuZnVuY3Rpb24gdG9rZW5Db21tZW50KHN0cmVhbSwgc3RhdGUpIHtcbiAgdmFyIG1heWJlRW5kID0gZmFsc2UsXG4gICAgY2g7XG4gIHdoaWxlIChjaCA9IHN0cmVhbS5uZXh0KCkpIHtcbiAgICBpZiAoY2ggPT0gXCIvXCIgJiYgbWF5YmVFbmQpIHtcbiAgICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlO1xuICAgICAgYnJlYWs7XG4gICAgfVxuICAgIG1heWJlRW5kID0gY2ggPT0gXCIqXCI7XG4gIH1cbiAgcmV0dXJuIFwiY29tbWVudFwiO1xufVxuZnVuY3Rpb24gQ29udGV4dChpbmRlbnRlZCwgY29sdW1uLCB0eXBlLCBhbGlnbiwgcHJldikge1xuICB0aGlzLmluZGVudGVkID0gaW5kZW50ZWQ7XG4gIHRoaXMuY29sdW1uID0gY29sdW1uO1xuICB0aGlzLnR5cGUgPSB0eXBlO1xuICB0aGlzLmFsaWduID0gYWxpZ247XG4gIHRoaXMucHJldiA9IHByZXY7XG59XG5mdW5jdGlvbiBwdXNoQ29udGV4dChzdGF0ZSwgY29sLCB0eXBlKSB7XG4gIHJldHVybiBzdGF0ZS5jb250ZXh0ID0gbmV3IENvbnRleHQoc3RhdGUuaW5kZW50ZWQsIGNvbCwgdHlwZSwgbnVsbCwgc3RhdGUuY29udGV4dCk7XG59XG5mdW5jdGlvbiBwb3BDb250ZXh0KHN0YXRlKSB7XG4gIHZhciB0ID0gc3RhdGUuY29udGV4dC50eXBlO1xuICBpZiAodCA9PSBcIilcIiB8fCB0ID09IFwiXVwiIHx8IHQgPT0gXCJ9XCIpIHN0YXRlLmluZGVudGVkID0gc3RhdGUuY29udGV4dC5pbmRlbnRlZDtcbiAgcmV0dXJuIHN0YXRlLmNvbnRleHQgPSBzdGF0ZS5jb250ZXh0LnByZXY7XG59XG5cbi8vIEludGVyZmFjZVxuXG5leHBvcnQgY29uc3QgZWNsID0ge1xuICBuYW1lOiBcImVjbFwiLFxuICBzdGFydFN0YXRlOiBmdW5jdGlvbiAoaW5kZW50VW5pdCkge1xuICAgIHJldHVybiB7XG4gICAgICB0b2tlbml6ZTogbnVsbCxcbiAgICAgIGNvbnRleHQ6IG5ldyBDb250ZXh0KC1pbmRlbnRVbml0LCAwLCBcInRvcFwiLCBmYWxzZSksXG4gICAgICBpbmRlbnRlZDogMCxcbiAgICAgIHN0YXJ0T2ZMaW5lOiB0cnVlXG4gICAgfTtcbiAgfSxcbiAgdG9rZW46IGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgdmFyIGN0eCA9IHN0YXRlLmNvbnRleHQ7XG4gICAgaWYgKHN0cmVhbS5zb2woKSkge1xuICAgICAgaWYgKGN0eC5hbGlnbiA9PSBudWxsKSBjdHguYWxpZ24gPSBmYWxzZTtcbiAgICAgIHN0YXRlLmluZGVudGVkID0gc3RyZWFtLmluZGVudGF0aW9uKCk7XG4gICAgICBzdGF0ZS5zdGFydE9mTGluZSA9IHRydWU7XG4gICAgfVxuICAgIGlmIChzdHJlYW0uZWF0U3BhY2UoKSkgcmV0dXJuIG51bGw7XG4gICAgY3VyUHVuYyA9IG51bGw7XG4gICAgdmFyIHN0eWxlID0gKHN0YXRlLnRva2VuaXplIHx8IHRva2VuQmFzZSkoc3RyZWFtLCBzdGF0ZSk7XG4gICAgaWYgKHN0eWxlID09IFwiY29tbWVudFwiIHx8IHN0eWxlID09IFwibWV0YVwiKSByZXR1cm4gc3R5bGU7XG4gICAgaWYgKGN0eC5hbGlnbiA9PSBudWxsKSBjdHguYWxpZ24gPSB0cnVlO1xuICAgIGlmICgoY3VyUHVuYyA9PSBcIjtcIiB8fCBjdXJQdW5jID09IFwiOlwiKSAmJiBjdHgudHlwZSA9PSBcInN0YXRlbWVudFwiKSBwb3BDb250ZXh0KHN0YXRlKTtlbHNlIGlmIChjdXJQdW5jID09IFwie1wiKSBwdXNoQ29udGV4dChzdGF0ZSwgc3RyZWFtLmNvbHVtbigpLCBcIn1cIik7ZWxzZSBpZiAoY3VyUHVuYyA9PSBcIltcIikgcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbS5jb2x1bW4oKSwgXCJdXCIpO2Vsc2UgaWYgKGN1clB1bmMgPT0gXCIoXCIpIHB1c2hDb250ZXh0KHN0YXRlLCBzdHJlYW0uY29sdW1uKCksIFwiKVwiKTtlbHNlIGlmIChjdXJQdW5jID09IFwifVwiKSB7XG4gICAgICB3aGlsZSAoY3R4LnR5cGUgPT0gXCJzdGF0ZW1lbnRcIikgY3R4ID0gcG9wQ29udGV4dChzdGF0ZSk7XG4gICAgICBpZiAoY3R4LnR5cGUgPT0gXCJ9XCIpIGN0eCA9IHBvcENvbnRleHQoc3RhdGUpO1xuICAgICAgd2hpbGUgKGN0eC50eXBlID09IFwic3RhdGVtZW50XCIpIGN0eCA9IHBvcENvbnRleHQoc3RhdGUpO1xuICAgIH0gZWxzZSBpZiAoY3VyUHVuYyA9PSBjdHgudHlwZSkgcG9wQ29udGV4dChzdGF0ZSk7ZWxzZSBpZiAoY3R4LnR5cGUgPT0gXCJ9XCIgfHwgY3R4LnR5cGUgPT0gXCJ0b3BcIiB8fCBjdHgudHlwZSA9PSBcInN0YXRlbWVudFwiICYmIGN1clB1bmMgPT0gXCJuZXdzdGF0ZW1lbnRcIikgcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbS5jb2x1bW4oKSwgXCJzdGF0ZW1lbnRcIik7XG4gICAgc3RhdGUuc3RhcnRPZkxpbmUgPSBmYWxzZTtcbiAgICByZXR1cm4gc3R5bGU7XG4gIH0sXG4gIGluZGVudDogZnVuY3Rpb24gKHN0YXRlLCB0ZXh0QWZ0ZXIsIGN4KSB7XG4gICAgaWYgKHN0YXRlLnRva2VuaXplICE9IHRva2VuQmFzZSAmJiBzdGF0ZS50b2tlbml6ZSAhPSBudWxsKSByZXR1cm4gMDtcbiAgICB2YXIgY3R4ID0gc3RhdGUuY29udGV4dCxcbiAgICAgIGZpcnN0Q2hhciA9IHRleHRBZnRlciAmJiB0ZXh0QWZ0ZXIuY2hhckF0KDApO1xuICAgIGlmIChjdHgudHlwZSA9PSBcInN0YXRlbWVudFwiICYmIGZpcnN0Q2hhciA9PSBcIn1cIikgY3R4ID0gY3R4LnByZXY7XG4gICAgdmFyIGNsb3NpbmcgPSBmaXJzdENoYXIgPT0gY3R4LnR5cGU7XG4gICAgaWYgKGN0eC50eXBlID09IFwic3RhdGVtZW50XCIpIHJldHVybiBjdHguaW5kZW50ZWQgKyAoZmlyc3RDaGFyID09IFwie1wiID8gMCA6IGN4LnVuaXQpO2Vsc2UgaWYgKGN0eC5hbGlnbikgcmV0dXJuIGN0eC5jb2x1bW4gKyAoY2xvc2luZyA/IDAgOiAxKTtlbHNlIHJldHVybiBjdHguaW5kZW50ZWQgKyAoY2xvc2luZyA/IDAgOiBjeC51bml0KTtcbiAgfSxcbiAgbGFuZ3VhZ2VEYXRhOiB7XG4gICAgaW5kZW50T25JbnB1dDogL15cXHMqW3t9XSQvXG4gIH1cbn07Il0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9