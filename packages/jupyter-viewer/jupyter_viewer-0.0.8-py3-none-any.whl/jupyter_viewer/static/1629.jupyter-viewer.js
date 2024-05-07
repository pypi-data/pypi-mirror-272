"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[1629],{

/***/ 61629:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ttcnCfg": () => (/* binding */ ttcnCfg)
/* harmony export */ });
function words(str) {
  var obj = {},
    words = str.split(" ");
  for (var i = 0; i < words.length; ++i) obj[words[i]] = true;
  return obj;
}
const parserConfig = {
  name: "ttcn-cfg",
  keywords: words("Yes No LogFile FileMask ConsoleMask AppendFile" + " TimeStampFormat LogEventTypes SourceInfoFormat" + " LogEntityName LogSourceInfo DiskFullAction" + " LogFileNumber LogFileSize MatchingHints Detailed" + " Compact SubCategories Stack Single None Seconds" + " DateTime Time Stop Error Retry Delete TCPPort KillTimer" + " NumHCs UnixSocketsEnabled LocalAddress"),
  fileNCtrlMaskOptions: words("TTCN_EXECUTOR TTCN_ERROR TTCN_WARNING" + " TTCN_PORTEVENT TTCN_TIMEROP TTCN_VERDICTOP" + " TTCN_DEFAULTOP TTCN_TESTCASE TTCN_ACTION" + " TTCN_USER TTCN_FUNCTION TTCN_STATISTICS" + " TTCN_PARALLEL TTCN_MATCHING TTCN_DEBUG" + " EXECUTOR ERROR WARNING PORTEVENT TIMEROP" + " VERDICTOP DEFAULTOP TESTCASE ACTION USER" + " FUNCTION STATISTICS PARALLEL MATCHING DEBUG" + " LOG_ALL LOG_NOTHING ACTION_UNQUALIFIED" + " DEBUG_ENCDEC DEBUG_TESTPORT" + " DEBUG_UNQUALIFIED DEFAULTOP_ACTIVATE" + " DEFAULTOP_DEACTIVATE DEFAULTOP_EXIT" + " DEFAULTOP_UNQUALIFIED ERROR_UNQUALIFIED" + " EXECUTOR_COMPONENT EXECUTOR_CONFIGDATA" + " EXECUTOR_EXTCOMMAND EXECUTOR_LOGOPTIONS" + " EXECUTOR_RUNTIME EXECUTOR_UNQUALIFIED" + " FUNCTION_RND FUNCTION_UNQUALIFIED" + " MATCHING_DONE MATCHING_MCSUCCESS" + " MATCHING_MCUNSUCC MATCHING_MMSUCCESS" + " MATCHING_MMUNSUCC MATCHING_PCSUCCESS" + " MATCHING_PCUNSUCC MATCHING_PMSUCCESS" + " MATCHING_PMUNSUCC MATCHING_PROBLEM" + " MATCHING_TIMEOUT MATCHING_UNQUALIFIED" + " PARALLEL_PORTCONN PARALLEL_PORTMAP" + " PARALLEL_PTC PARALLEL_UNQUALIFIED" + " PORTEVENT_DUALRECV PORTEVENT_DUALSEND" + " PORTEVENT_MCRECV PORTEVENT_MCSEND" + " PORTEVENT_MMRECV PORTEVENT_MMSEND" + " PORTEVENT_MQUEUE PORTEVENT_PCIN" + " PORTEVENT_PCOUT PORTEVENT_PMIN" + " PORTEVENT_PMOUT PORTEVENT_PQUEUE" + " PORTEVENT_STATE PORTEVENT_UNQUALIFIED" + " STATISTICS_UNQUALIFIED STATISTICS_VERDICT" + " TESTCASE_FINISH TESTCASE_START" + " TESTCASE_UNQUALIFIED TIMEROP_GUARD" + " TIMEROP_READ TIMEROP_START TIMEROP_STOP" + " TIMEROP_TIMEOUT TIMEROP_UNQUALIFIED" + " USER_UNQUALIFIED VERDICTOP_FINAL" + " VERDICTOP_GETVERDICT VERDICTOP_SETVERDICT" + " VERDICTOP_UNQUALIFIED WARNING_UNQUALIFIED"),
  externalCommands: words("BeginControlPart EndControlPart BeginTestCase" + " EndTestCase"),
  multiLineStrings: true
};
var keywords = parserConfig.keywords,
  fileNCtrlMaskOptions = parserConfig.fileNCtrlMaskOptions,
  externalCommands = parserConfig.externalCommands,
  multiLineStrings = parserConfig.multiLineStrings,
  indentStatements = parserConfig.indentStatements !== false;
var isOperatorChar = /[\|]/;
var curPunc;
function tokenBase(stream, state) {
  var ch = stream.next();
  if (ch == '"' || ch == "'") {
    state.tokenize = tokenString(ch);
    return state.tokenize(stream, state);
  }
  if (/[:=]/.test(ch)) {
    curPunc = ch;
    return "punctuation";
  }
  if (ch == "#") {
    stream.skipToEnd();
    return "comment";
  }
  if (/\d/.test(ch)) {
    stream.eatWhile(/[\w\.]/);
    return "number";
  }
  if (isOperatorChar.test(ch)) {
    stream.eatWhile(isOperatorChar);
    return "operator";
  }
  if (ch == "[") {
    stream.eatWhile(/[\w_\]]/);
    return "number";
  }
  stream.eatWhile(/[\w\$_]/);
  var cur = stream.current();
  if (keywords.propertyIsEnumerable(cur)) return "keyword";
  if (fileNCtrlMaskOptions.propertyIsEnumerable(cur)) return "atom";
  if (externalCommands.propertyIsEnumerable(cur)) return "deleted";
  return "variable";
}
function tokenString(quote) {
  return function (stream, state) {
    var escaped = false,
      next,
      end = false;
    while ((next = stream.next()) != null) {
      if (next == quote && !escaped) {
        var afterNext = stream.peek();
        //look if the character if the quote is like the B in '10100010'B
        if (afterNext) {
          afterNext = afterNext.toLowerCase();
          if (afterNext == "b" || afterNext == "h" || afterNext == "o") stream.next();
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
const ttcnCfg = {
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
      line: "#"
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiMTYyOS5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL0Bjb2RlbWlycm9yL2xlZ2FjeS1tb2Rlcy9tb2RlL3R0Y24tY2ZnLmpzIl0sInNvdXJjZXNDb250ZW50IjpbImZ1bmN0aW9uIHdvcmRzKHN0cikge1xuICB2YXIgb2JqID0ge30sXG4gICAgd29yZHMgPSBzdHIuc3BsaXQoXCIgXCIpO1xuICBmb3IgKHZhciBpID0gMDsgaSA8IHdvcmRzLmxlbmd0aDsgKytpKSBvYmpbd29yZHNbaV1dID0gdHJ1ZTtcbiAgcmV0dXJuIG9iajtcbn1cbmNvbnN0IHBhcnNlckNvbmZpZyA9IHtcbiAgbmFtZTogXCJ0dGNuLWNmZ1wiLFxuICBrZXl3b3Jkczogd29yZHMoXCJZZXMgTm8gTG9nRmlsZSBGaWxlTWFzayBDb25zb2xlTWFzayBBcHBlbmRGaWxlXCIgKyBcIiBUaW1lU3RhbXBGb3JtYXQgTG9nRXZlbnRUeXBlcyBTb3VyY2VJbmZvRm9ybWF0XCIgKyBcIiBMb2dFbnRpdHlOYW1lIExvZ1NvdXJjZUluZm8gRGlza0Z1bGxBY3Rpb25cIiArIFwiIExvZ0ZpbGVOdW1iZXIgTG9nRmlsZVNpemUgTWF0Y2hpbmdIaW50cyBEZXRhaWxlZFwiICsgXCIgQ29tcGFjdCBTdWJDYXRlZ29yaWVzIFN0YWNrIFNpbmdsZSBOb25lIFNlY29uZHNcIiArIFwiIERhdGVUaW1lIFRpbWUgU3RvcCBFcnJvciBSZXRyeSBEZWxldGUgVENQUG9ydCBLaWxsVGltZXJcIiArIFwiIE51bUhDcyBVbml4U29ja2V0c0VuYWJsZWQgTG9jYWxBZGRyZXNzXCIpLFxuICBmaWxlTkN0cmxNYXNrT3B0aW9uczogd29yZHMoXCJUVENOX0VYRUNVVE9SIFRUQ05fRVJST1IgVFRDTl9XQVJOSU5HXCIgKyBcIiBUVENOX1BPUlRFVkVOVCBUVENOX1RJTUVST1AgVFRDTl9WRVJESUNUT1BcIiArIFwiIFRUQ05fREVGQVVMVE9QIFRUQ05fVEVTVENBU0UgVFRDTl9BQ1RJT05cIiArIFwiIFRUQ05fVVNFUiBUVENOX0ZVTkNUSU9OIFRUQ05fU1RBVElTVElDU1wiICsgXCIgVFRDTl9QQVJBTExFTCBUVENOX01BVENISU5HIFRUQ05fREVCVUdcIiArIFwiIEVYRUNVVE9SIEVSUk9SIFdBUk5JTkcgUE9SVEVWRU5UIFRJTUVST1BcIiArIFwiIFZFUkRJQ1RPUCBERUZBVUxUT1AgVEVTVENBU0UgQUNUSU9OIFVTRVJcIiArIFwiIEZVTkNUSU9OIFNUQVRJU1RJQ1MgUEFSQUxMRUwgTUFUQ0hJTkcgREVCVUdcIiArIFwiIExPR19BTEwgTE9HX05PVEhJTkcgQUNUSU9OX1VOUVVBTElGSUVEXCIgKyBcIiBERUJVR19FTkNERUMgREVCVUdfVEVTVFBPUlRcIiArIFwiIERFQlVHX1VOUVVBTElGSUVEIERFRkFVTFRPUF9BQ1RJVkFURVwiICsgXCIgREVGQVVMVE9QX0RFQUNUSVZBVEUgREVGQVVMVE9QX0VYSVRcIiArIFwiIERFRkFVTFRPUF9VTlFVQUxJRklFRCBFUlJPUl9VTlFVQUxJRklFRFwiICsgXCIgRVhFQ1VUT1JfQ09NUE9ORU5UIEVYRUNVVE9SX0NPTkZJR0RBVEFcIiArIFwiIEVYRUNVVE9SX0VYVENPTU1BTkQgRVhFQ1VUT1JfTE9HT1BUSU9OU1wiICsgXCIgRVhFQ1VUT1JfUlVOVElNRSBFWEVDVVRPUl9VTlFVQUxJRklFRFwiICsgXCIgRlVOQ1RJT05fUk5EIEZVTkNUSU9OX1VOUVVBTElGSUVEXCIgKyBcIiBNQVRDSElOR19ET05FIE1BVENISU5HX01DU1VDQ0VTU1wiICsgXCIgTUFUQ0hJTkdfTUNVTlNVQ0MgTUFUQ0hJTkdfTU1TVUNDRVNTXCIgKyBcIiBNQVRDSElOR19NTVVOU1VDQyBNQVRDSElOR19QQ1NVQ0NFU1NcIiArIFwiIE1BVENISU5HX1BDVU5TVUNDIE1BVENISU5HX1BNU1VDQ0VTU1wiICsgXCIgTUFUQ0hJTkdfUE1VTlNVQ0MgTUFUQ0hJTkdfUFJPQkxFTVwiICsgXCIgTUFUQ0hJTkdfVElNRU9VVCBNQVRDSElOR19VTlFVQUxJRklFRFwiICsgXCIgUEFSQUxMRUxfUE9SVENPTk4gUEFSQUxMRUxfUE9SVE1BUFwiICsgXCIgUEFSQUxMRUxfUFRDIFBBUkFMTEVMX1VOUVVBTElGSUVEXCIgKyBcIiBQT1JURVZFTlRfRFVBTFJFQ1YgUE9SVEVWRU5UX0RVQUxTRU5EXCIgKyBcIiBQT1JURVZFTlRfTUNSRUNWIFBPUlRFVkVOVF9NQ1NFTkRcIiArIFwiIFBPUlRFVkVOVF9NTVJFQ1YgUE9SVEVWRU5UX01NU0VORFwiICsgXCIgUE9SVEVWRU5UX01RVUVVRSBQT1JURVZFTlRfUENJTlwiICsgXCIgUE9SVEVWRU5UX1BDT1VUIFBPUlRFVkVOVF9QTUlOXCIgKyBcIiBQT1JURVZFTlRfUE1PVVQgUE9SVEVWRU5UX1BRVUVVRVwiICsgXCIgUE9SVEVWRU5UX1NUQVRFIFBPUlRFVkVOVF9VTlFVQUxJRklFRFwiICsgXCIgU1RBVElTVElDU19VTlFVQUxJRklFRCBTVEFUSVNUSUNTX1ZFUkRJQ1RcIiArIFwiIFRFU1RDQVNFX0ZJTklTSCBURVNUQ0FTRV9TVEFSVFwiICsgXCIgVEVTVENBU0VfVU5RVUFMSUZJRUQgVElNRVJPUF9HVUFSRFwiICsgXCIgVElNRVJPUF9SRUFEIFRJTUVST1BfU1RBUlQgVElNRVJPUF9TVE9QXCIgKyBcIiBUSU1FUk9QX1RJTUVPVVQgVElNRVJPUF9VTlFVQUxJRklFRFwiICsgXCIgVVNFUl9VTlFVQUxJRklFRCBWRVJESUNUT1BfRklOQUxcIiArIFwiIFZFUkRJQ1RPUF9HRVRWRVJESUNUIFZFUkRJQ1RPUF9TRVRWRVJESUNUXCIgKyBcIiBWRVJESUNUT1BfVU5RVUFMSUZJRUQgV0FSTklOR19VTlFVQUxJRklFRFwiKSxcbiAgZXh0ZXJuYWxDb21tYW5kczogd29yZHMoXCJCZWdpbkNvbnRyb2xQYXJ0IEVuZENvbnRyb2xQYXJ0IEJlZ2luVGVzdENhc2VcIiArIFwiIEVuZFRlc3RDYXNlXCIpLFxuICBtdWx0aUxpbmVTdHJpbmdzOiB0cnVlXG59O1xudmFyIGtleXdvcmRzID0gcGFyc2VyQ29uZmlnLmtleXdvcmRzLFxuICBmaWxlTkN0cmxNYXNrT3B0aW9ucyA9IHBhcnNlckNvbmZpZy5maWxlTkN0cmxNYXNrT3B0aW9ucyxcbiAgZXh0ZXJuYWxDb21tYW5kcyA9IHBhcnNlckNvbmZpZy5leHRlcm5hbENvbW1hbmRzLFxuICBtdWx0aUxpbmVTdHJpbmdzID0gcGFyc2VyQ29uZmlnLm11bHRpTGluZVN0cmluZ3MsXG4gIGluZGVudFN0YXRlbWVudHMgPSBwYXJzZXJDb25maWcuaW5kZW50U3RhdGVtZW50cyAhPT0gZmFsc2U7XG52YXIgaXNPcGVyYXRvckNoYXIgPSAvW1xcfF0vO1xudmFyIGN1clB1bmM7XG5mdW5jdGlvbiB0b2tlbkJhc2Uoc3RyZWFtLCBzdGF0ZSkge1xuICB2YXIgY2ggPSBzdHJlYW0ubmV4dCgpO1xuICBpZiAoY2ggPT0gJ1wiJyB8fCBjaCA9PSBcIidcIikge1xuICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5TdHJpbmcoY2gpO1xuICAgIHJldHVybiBzdGF0ZS50b2tlbml6ZShzdHJlYW0sIHN0YXRlKTtcbiAgfVxuICBpZiAoL1s6PV0vLnRlc3QoY2gpKSB7XG4gICAgY3VyUHVuYyA9IGNoO1xuICAgIHJldHVybiBcInB1bmN0dWF0aW9uXCI7XG4gIH1cbiAgaWYgKGNoID09IFwiI1wiKSB7XG4gICAgc3RyZWFtLnNraXBUb0VuZCgpO1xuICAgIHJldHVybiBcImNvbW1lbnRcIjtcbiAgfVxuICBpZiAoL1xcZC8udGVzdChjaCkpIHtcbiAgICBzdHJlYW0uZWF0V2hpbGUoL1tcXHdcXC5dLyk7XG4gICAgcmV0dXJuIFwibnVtYmVyXCI7XG4gIH1cbiAgaWYgKGlzT3BlcmF0b3JDaGFyLnRlc3QoY2gpKSB7XG4gICAgc3RyZWFtLmVhdFdoaWxlKGlzT3BlcmF0b3JDaGFyKTtcbiAgICByZXR1cm4gXCJvcGVyYXRvclwiO1xuICB9XG4gIGlmIChjaCA9PSBcIltcIikge1xuICAgIHN0cmVhbS5lYXRXaGlsZSgvW1xcd19cXF1dLyk7XG4gICAgcmV0dXJuIFwibnVtYmVyXCI7XG4gIH1cbiAgc3RyZWFtLmVhdFdoaWxlKC9bXFx3XFwkX10vKTtcbiAgdmFyIGN1ciA9IHN0cmVhbS5jdXJyZW50KCk7XG4gIGlmIChrZXl3b3Jkcy5wcm9wZXJ0eUlzRW51bWVyYWJsZShjdXIpKSByZXR1cm4gXCJrZXl3b3JkXCI7XG4gIGlmIChmaWxlTkN0cmxNYXNrT3B0aW9ucy5wcm9wZXJ0eUlzRW51bWVyYWJsZShjdXIpKSByZXR1cm4gXCJhdG9tXCI7XG4gIGlmIChleHRlcm5hbENvbW1hbmRzLnByb3BlcnR5SXNFbnVtZXJhYmxlKGN1cikpIHJldHVybiBcImRlbGV0ZWRcIjtcbiAgcmV0dXJuIFwidmFyaWFibGVcIjtcbn1cbmZ1bmN0aW9uIHRva2VuU3RyaW5nKHF1b3RlKSB7XG4gIHJldHVybiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIHZhciBlc2NhcGVkID0gZmFsc2UsXG4gICAgICBuZXh0LFxuICAgICAgZW5kID0gZmFsc2U7XG4gICAgd2hpbGUgKChuZXh0ID0gc3RyZWFtLm5leHQoKSkgIT0gbnVsbCkge1xuICAgICAgaWYgKG5leHQgPT0gcXVvdGUgJiYgIWVzY2FwZWQpIHtcbiAgICAgICAgdmFyIGFmdGVyTmV4dCA9IHN0cmVhbS5wZWVrKCk7XG4gICAgICAgIC8vbG9vayBpZiB0aGUgY2hhcmFjdGVyIGlmIHRoZSBxdW90ZSBpcyBsaWtlIHRoZSBCIGluICcxMDEwMDAxMCdCXG4gICAgICAgIGlmIChhZnRlck5leHQpIHtcbiAgICAgICAgICBhZnRlck5leHQgPSBhZnRlck5leHQudG9Mb3dlckNhc2UoKTtcbiAgICAgICAgICBpZiAoYWZ0ZXJOZXh0ID09IFwiYlwiIHx8IGFmdGVyTmV4dCA9PSBcImhcIiB8fCBhZnRlck5leHQgPT0gXCJvXCIpIHN0cmVhbS5uZXh0KCk7XG4gICAgICAgIH1cbiAgICAgICAgZW5kID0gdHJ1ZTtcbiAgICAgICAgYnJlYWs7XG4gICAgICB9XG4gICAgICBlc2NhcGVkID0gIWVzY2FwZWQgJiYgbmV4dCA9PSBcIlxcXFxcIjtcbiAgICB9XG4gICAgaWYgKGVuZCB8fCAhKGVzY2FwZWQgfHwgbXVsdGlMaW5lU3RyaW5ncykpIHN0YXRlLnRva2VuaXplID0gbnVsbDtcbiAgICByZXR1cm4gXCJzdHJpbmdcIjtcbiAgfTtcbn1cbmZ1bmN0aW9uIENvbnRleHQoaW5kZW50ZWQsIGNvbHVtbiwgdHlwZSwgYWxpZ24sIHByZXYpIHtcbiAgdGhpcy5pbmRlbnRlZCA9IGluZGVudGVkO1xuICB0aGlzLmNvbHVtbiA9IGNvbHVtbjtcbiAgdGhpcy50eXBlID0gdHlwZTtcbiAgdGhpcy5hbGlnbiA9IGFsaWduO1xuICB0aGlzLnByZXYgPSBwcmV2O1xufVxuZnVuY3Rpb24gcHVzaENvbnRleHQoc3RhdGUsIGNvbCwgdHlwZSkge1xuICB2YXIgaW5kZW50ID0gc3RhdGUuaW5kZW50ZWQ7XG4gIGlmIChzdGF0ZS5jb250ZXh0ICYmIHN0YXRlLmNvbnRleHQudHlwZSA9PSBcInN0YXRlbWVudFwiKSBpbmRlbnQgPSBzdGF0ZS5jb250ZXh0LmluZGVudGVkO1xuICByZXR1cm4gc3RhdGUuY29udGV4dCA9IG5ldyBDb250ZXh0KGluZGVudCwgY29sLCB0eXBlLCBudWxsLCBzdGF0ZS5jb250ZXh0KTtcbn1cbmZ1bmN0aW9uIHBvcENvbnRleHQoc3RhdGUpIHtcbiAgdmFyIHQgPSBzdGF0ZS5jb250ZXh0LnR5cGU7XG4gIGlmICh0ID09IFwiKVwiIHx8IHQgPT0gXCJdXCIgfHwgdCA9PSBcIn1cIikgc3RhdGUuaW5kZW50ZWQgPSBzdGF0ZS5jb250ZXh0LmluZGVudGVkO1xuICByZXR1cm4gc3RhdGUuY29udGV4dCA9IHN0YXRlLmNvbnRleHQucHJldjtcbn1cblxuLy9JbnRlcmZhY2VcbmV4cG9ydCBjb25zdCB0dGNuQ2ZnID0ge1xuICBuYW1lOiBcInR0Y25cIixcbiAgc3RhcnRTdGF0ZTogZnVuY3Rpb24gKCkge1xuICAgIHJldHVybiB7XG4gICAgICB0b2tlbml6ZTogbnVsbCxcbiAgICAgIGNvbnRleHQ6IG5ldyBDb250ZXh0KDAsIDAsIFwidG9wXCIsIGZhbHNlKSxcbiAgICAgIGluZGVudGVkOiAwLFxuICAgICAgc3RhcnRPZkxpbmU6IHRydWVcbiAgICB9O1xuICB9LFxuICB0b2tlbjogZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICB2YXIgY3R4ID0gc3RhdGUuY29udGV4dDtcbiAgICBpZiAoc3RyZWFtLnNvbCgpKSB7XG4gICAgICBpZiAoY3R4LmFsaWduID09IG51bGwpIGN0eC5hbGlnbiA9IGZhbHNlO1xuICAgICAgc3RhdGUuaW5kZW50ZWQgPSBzdHJlYW0uaW5kZW50YXRpb24oKTtcbiAgICAgIHN0YXRlLnN0YXJ0T2ZMaW5lID0gdHJ1ZTtcbiAgICB9XG4gICAgaWYgKHN0cmVhbS5lYXRTcGFjZSgpKSByZXR1cm4gbnVsbDtcbiAgICBjdXJQdW5jID0gbnVsbDtcbiAgICB2YXIgc3R5bGUgPSAoc3RhdGUudG9rZW5pemUgfHwgdG9rZW5CYXNlKShzdHJlYW0sIHN0YXRlKTtcbiAgICBpZiAoc3R5bGUgPT0gXCJjb21tZW50XCIpIHJldHVybiBzdHlsZTtcbiAgICBpZiAoY3R4LmFsaWduID09IG51bGwpIGN0eC5hbGlnbiA9IHRydWU7XG4gICAgaWYgKChjdXJQdW5jID09IFwiO1wiIHx8IGN1clB1bmMgPT0gXCI6XCIgfHwgY3VyUHVuYyA9PSBcIixcIikgJiYgY3R4LnR5cGUgPT0gXCJzdGF0ZW1lbnRcIikge1xuICAgICAgcG9wQ29udGV4dChzdGF0ZSk7XG4gICAgfSBlbHNlIGlmIChjdXJQdW5jID09IFwie1wiKSBwdXNoQ29udGV4dChzdGF0ZSwgc3RyZWFtLmNvbHVtbigpLCBcIn1cIik7ZWxzZSBpZiAoY3VyUHVuYyA9PSBcIltcIikgcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbS5jb2x1bW4oKSwgXCJdXCIpO2Vsc2UgaWYgKGN1clB1bmMgPT0gXCIoXCIpIHB1c2hDb250ZXh0KHN0YXRlLCBzdHJlYW0uY29sdW1uKCksIFwiKVwiKTtlbHNlIGlmIChjdXJQdW5jID09IFwifVwiKSB7XG4gICAgICB3aGlsZSAoY3R4LnR5cGUgPT0gXCJzdGF0ZW1lbnRcIikgY3R4ID0gcG9wQ29udGV4dChzdGF0ZSk7XG4gICAgICBpZiAoY3R4LnR5cGUgPT0gXCJ9XCIpIGN0eCA9IHBvcENvbnRleHQoc3RhdGUpO1xuICAgICAgd2hpbGUgKGN0eC50eXBlID09IFwic3RhdGVtZW50XCIpIGN0eCA9IHBvcENvbnRleHQoc3RhdGUpO1xuICAgIH0gZWxzZSBpZiAoY3VyUHVuYyA9PSBjdHgudHlwZSkgcG9wQ29udGV4dChzdGF0ZSk7ZWxzZSBpZiAoaW5kZW50U3RhdGVtZW50cyAmJiAoKGN0eC50eXBlID09IFwifVwiIHx8IGN0eC50eXBlID09IFwidG9wXCIpICYmIGN1clB1bmMgIT0gJzsnIHx8IGN0eC50eXBlID09IFwic3RhdGVtZW50XCIgJiYgY3VyUHVuYyA9PSBcIm5ld3N0YXRlbWVudFwiKSkgcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbS5jb2x1bW4oKSwgXCJzdGF0ZW1lbnRcIik7XG4gICAgc3RhdGUuc3RhcnRPZkxpbmUgPSBmYWxzZTtcbiAgICByZXR1cm4gc3R5bGU7XG4gIH0sXG4gIGxhbmd1YWdlRGF0YToge1xuICAgIGluZGVudE9uSW5wdXQ6IC9eXFxzKlt7fV0kLyxcbiAgICBjb21tZW50VG9rZW5zOiB7XG4gICAgICBsaW5lOiBcIiNcIlxuICAgIH1cbiAgfVxufTsiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=