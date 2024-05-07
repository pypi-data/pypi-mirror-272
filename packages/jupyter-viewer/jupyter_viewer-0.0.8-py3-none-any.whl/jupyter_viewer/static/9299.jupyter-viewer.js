"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[9299],{

/***/ 42464:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "asterisk": () => (/* binding */ asterisk)
/* harmony export */ });
var atoms = ["exten", "same", "include", "ignorepat", "switch"],
  dpcmd = ["#include", "#exec"],
  apps = ["addqueuemember", "adsiprog", "aelsub", "agentlogin", "agentmonitoroutgoing", "agi", "alarmreceiver", "amd", "answer", "authenticate", "background", "backgrounddetect", "bridge", "busy", "callcompletioncancel", "callcompletionrequest", "celgenuserevent", "changemonitor", "chanisavail", "channelredirect", "chanspy", "clearhash", "confbridge", "congestion", "continuewhile", "controlplayback", "dahdiacceptr2call", "dahdibarge", "dahdiras", "dahdiscan", "dahdisendcallreroutingfacility", "dahdisendkeypadfacility", "datetime", "dbdel", "dbdeltree", "deadagi", "dial", "dictate", "directory", "disa", "dumpchan", "eagi", "echo", "endwhile", "exec", "execif", "execiftime", "exitwhile", "extenspy", "externalivr", "festival", "flash", "followme", "forkcdr", "getcpeid", "gosub", "gosubif", "goto", "gotoif", "gotoiftime", "hangup", "iax2provision", "ices", "importvar", "incomplete", "ivrdemo", "jabberjoin", "jabberleave", "jabbersend", "jabbersendgroup", "jabberstatus", "jack", "log", "macro", "macroexclusive", "macroexit", "macroif", "mailboxexists", "meetme", "meetmeadmin", "meetmechanneladmin", "meetmecount", "milliwatt", "minivmaccmess", "minivmdelete", "minivmgreet", "minivmmwi", "minivmnotify", "minivmrecord", "mixmonitor", "monitor", "morsecode", "mp3player", "mset", "musiconhold", "nbscat", "nocdr", "noop", "odbc", "odbc", "odbcfinish", "originate", "ospauth", "ospfinish", "osplookup", "ospnext", "page", "park", "parkandannounce", "parkedcall", "pausemonitor", "pausequeuemember", "pickup", "pickupchan", "playback", "playtones", "privacymanager", "proceeding", "progress", "queue", "queuelog", "raiseexception", "read", "readexten", "readfile", "receivefax", "receivefax", "receivefax", "record", "removequeuemember", "resetcdr", "retrydial", "return", "ringing", "sayalpha", "saycountedadj", "saycountednoun", "saycountpl", "saydigits", "saynumber", "sayphonetic", "sayunixtime", "senddtmf", "sendfax", "sendfax", "sendfax", "sendimage", "sendtext", "sendurl", "set", "setamaflags", "setcallerpres", "setmusiconhold", "sipaddheader", "sipdtmfmode", "sipremoveheader", "skel", "slastation", "slatrunk", "sms", "softhangup", "speechactivategrammar", "speechbackground", "speechcreate", "speechdeactivategrammar", "speechdestroy", "speechloadgrammar", "speechprocessingsound", "speechstart", "speechunloadgrammar", "stackpop", "startmusiconhold", "stopmixmonitor", "stopmonitor", "stopmusiconhold", "stopplaytones", "system", "testclient", "testserver", "transfer", "tryexec", "trysystem", "unpausemonitor", "unpausequeuemember", "userevent", "verbose", "vmauthenticate", "vmsayname", "voicemail", "voicemailmain", "wait", "waitexten", "waitfornoise", "waitforring", "waitforsilence", "waitmusiconhold", "waituntil", "while", "zapateller"];
function basicToken(stream, state) {
  var cur = '';
  var ch = stream.next();
  // comment
  if (state.blockComment) {
    if (ch == "-" && stream.match("-;", true)) {
      state.blockComment = false;
    } else if (stream.skipTo("--;")) {
      stream.next();
      stream.next();
      stream.next();
      state.blockComment = false;
    } else {
      stream.skipToEnd();
    }
    return "comment";
  }
  if (ch == ";") {
    if (stream.match("--", true)) {
      if (!stream.match("-", false)) {
        // Except ;--- is not a block comment
        state.blockComment = true;
        return "comment";
      }
    }
    stream.skipToEnd();
    return "comment";
  }
  // context
  if (ch == '[') {
    stream.skipTo(']');
    stream.eat(']');
    return "header";
  }
  // string
  if (ch == '"') {
    stream.skipTo('"');
    return "string";
  }
  if (ch == "'") {
    stream.skipTo("'");
    return "string.special";
  }
  // dialplan commands
  if (ch == '#') {
    stream.eatWhile(/\w/);
    cur = stream.current();
    if (dpcmd.indexOf(cur) !== -1) {
      stream.skipToEnd();
      return "strong";
    }
  }
  // application args
  if (ch == '$') {
    var ch1 = stream.peek();
    if (ch1 == '{') {
      stream.skipTo('}');
      stream.eat('}');
      return "variableName.special";
    }
  }
  // extension
  stream.eatWhile(/\w/);
  cur = stream.current();
  if (atoms.indexOf(cur) !== -1) {
    state.extenStart = true;
    switch (cur) {
      case 'same':
        state.extenSame = true;
        break;
      case 'include':
      case 'switch':
      case 'ignorepat':
        state.extenInclude = true;
        break;
      default:
        break;
    }
    return "atom";
  }
}
const asterisk = {
  name: "asterisk",
  startState: function () {
    return {
      blockComment: false,
      extenStart: false,
      extenSame: false,
      extenInclude: false,
      extenExten: false,
      extenPriority: false,
      extenApplication: false
    };
  },
  token: function (stream, state) {
    var cur = '';
    if (stream.eatSpace()) return null;
    // extension started
    if (state.extenStart) {
      stream.eatWhile(/[^\s]/);
      cur = stream.current();
      if (/^=>?$/.test(cur)) {
        state.extenExten = true;
        state.extenStart = false;
        return "strong";
      } else {
        state.extenStart = false;
        stream.skipToEnd();
        return "error";
      }
    } else if (state.extenExten) {
      // set exten and priority
      state.extenExten = false;
      state.extenPriority = true;
      stream.eatWhile(/[^,]/);
      if (state.extenInclude) {
        stream.skipToEnd();
        state.extenPriority = false;
        state.extenInclude = false;
      }
      if (state.extenSame) {
        state.extenPriority = false;
        state.extenSame = false;
        state.extenApplication = true;
      }
      return "tag";
    } else if (state.extenPriority) {
      state.extenPriority = false;
      state.extenApplication = true;
      stream.next(); // get comma
      if (state.extenSame) return null;
      stream.eatWhile(/[^,]/);
      return "number";
    } else if (state.extenApplication) {
      stream.eatWhile(/,/);
      cur = stream.current();
      if (cur === ',') return null;
      stream.eatWhile(/\w/);
      cur = stream.current().toLowerCase();
      state.extenApplication = false;
      if (apps.indexOf(cur) !== -1) {
        return "def";
      }
    } else {
      return basicToken(stream, state);
    }
    return null;
  },
  languageData: {
    commentTokens: {
      line: ";",
      block: {
        open: ";--",
        close: "--;"
      }
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiOTI5OS5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGNvZGVtaXJyb3IvbGVnYWN5LW1vZGVzL21vZGUvYXN0ZXJpc2suanMiXSwic291cmNlc0NvbnRlbnQiOlsidmFyIGF0b21zID0gW1wiZXh0ZW5cIiwgXCJzYW1lXCIsIFwiaW5jbHVkZVwiLCBcImlnbm9yZXBhdFwiLCBcInN3aXRjaFwiXSxcbiAgZHBjbWQgPSBbXCIjaW5jbHVkZVwiLCBcIiNleGVjXCJdLFxuICBhcHBzID0gW1wiYWRkcXVldWVtZW1iZXJcIiwgXCJhZHNpcHJvZ1wiLCBcImFlbHN1YlwiLCBcImFnZW50bG9naW5cIiwgXCJhZ2VudG1vbml0b3JvdXRnb2luZ1wiLCBcImFnaVwiLCBcImFsYXJtcmVjZWl2ZXJcIiwgXCJhbWRcIiwgXCJhbnN3ZXJcIiwgXCJhdXRoZW50aWNhdGVcIiwgXCJiYWNrZ3JvdW5kXCIsIFwiYmFja2dyb3VuZGRldGVjdFwiLCBcImJyaWRnZVwiLCBcImJ1c3lcIiwgXCJjYWxsY29tcGxldGlvbmNhbmNlbFwiLCBcImNhbGxjb21wbGV0aW9ucmVxdWVzdFwiLCBcImNlbGdlbnVzZXJldmVudFwiLCBcImNoYW5nZW1vbml0b3JcIiwgXCJjaGFuaXNhdmFpbFwiLCBcImNoYW5uZWxyZWRpcmVjdFwiLCBcImNoYW5zcHlcIiwgXCJjbGVhcmhhc2hcIiwgXCJjb25mYnJpZGdlXCIsIFwiY29uZ2VzdGlvblwiLCBcImNvbnRpbnVld2hpbGVcIiwgXCJjb250cm9scGxheWJhY2tcIiwgXCJkYWhkaWFjY2VwdHIyY2FsbFwiLCBcImRhaGRpYmFyZ2VcIiwgXCJkYWhkaXJhc1wiLCBcImRhaGRpc2NhblwiLCBcImRhaGRpc2VuZGNhbGxyZXJvdXRpbmdmYWNpbGl0eVwiLCBcImRhaGRpc2VuZGtleXBhZGZhY2lsaXR5XCIsIFwiZGF0ZXRpbWVcIiwgXCJkYmRlbFwiLCBcImRiZGVsdHJlZVwiLCBcImRlYWRhZ2lcIiwgXCJkaWFsXCIsIFwiZGljdGF0ZVwiLCBcImRpcmVjdG9yeVwiLCBcImRpc2FcIiwgXCJkdW1wY2hhblwiLCBcImVhZ2lcIiwgXCJlY2hvXCIsIFwiZW5kd2hpbGVcIiwgXCJleGVjXCIsIFwiZXhlY2lmXCIsIFwiZXhlY2lmdGltZVwiLCBcImV4aXR3aGlsZVwiLCBcImV4dGVuc3B5XCIsIFwiZXh0ZXJuYWxpdnJcIiwgXCJmZXN0aXZhbFwiLCBcImZsYXNoXCIsIFwiZm9sbG93bWVcIiwgXCJmb3JrY2RyXCIsIFwiZ2V0Y3BlaWRcIiwgXCJnb3N1YlwiLCBcImdvc3ViaWZcIiwgXCJnb3RvXCIsIFwiZ290b2lmXCIsIFwiZ290b2lmdGltZVwiLCBcImhhbmd1cFwiLCBcImlheDJwcm92aXNpb25cIiwgXCJpY2VzXCIsIFwiaW1wb3J0dmFyXCIsIFwiaW5jb21wbGV0ZVwiLCBcIml2cmRlbW9cIiwgXCJqYWJiZXJqb2luXCIsIFwiamFiYmVybGVhdmVcIiwgXCJqYWJiZXJzZW5kXCIsIFwiamFiYmVyc2VuZGdyb3VwXCIsIFwiamFiYmVyc3RhdHVzXCIsIFwiamFja1wiLCBcImxvZ1wiLCBcIm1hY3JvXCIsIFwibWFjcm9leGNsdXNpdmVcIiwgXCJtYWNyb2V4aXRcIiwgXCJtYWNyb2lmXCIsIFwibWFpbGJveGV4aXN0c1wiLCBcIm1lZXRtZVwiLCBcIm1lZXRtZWFkbWluXCIsIFwibWVldG1lY2hhbm5lbGFkbWluXCIsIFwibWVldG1lY291bnRcIiwgXCJtaWxsaXdhdHRcIiwgXCJtaW5pdm1hY2NtZXNzXCIsIFwibWluaXZtZGVsZXRlXCIsIFwibWluaXZtZ3JlZXRcIiwgXCJtaW5pdm1td2lcIiwgXCJtaW5pdm1ub3RpZnlcIiwgXCJtaW5pdm1yZWNvcmRcIiwgXCJtaXhtb25pdG9yXCIsIFwibW9uaXRvclwiLCBcIm1vcnNlY29kZVwiLCBcIm1wM3BsYXllclwiLCBcIm1zZXRcIiwgXCJtdXNpY29uaG9sZFwiLCBcIm5ic2NhdFwiLCBcIm5vY2RyXCIsIFwibm9vcFwiLCBcIm9kYmNcIiwgXCJvZGJjXCIsIFwib2RiY2ZpbmlzaFwiLCBcIm9yaWdpbmF0ZVwiLCBcIm9zcGF1dGhcIiwgXCJvc3BmaW5pc2hcIiwgXCJvc3Bsb29rdXBcIiwgXCJvc3BuZXh0XCIsIFwicGFnZVwiLCBcInBhcmtcIiwgXCJwYXJrYW5kYW5ub3VuY2VcIiwgXCJwYXJrZWRjYWxsXCIsIFwicGF1c2Vtb25pdG9yXCIsIFwicGF1c2VxdWV1ZW1lbWJlclwiLCBcInBpY2t1cFwiLCBcInBpY2t1cGNoYW5cIiwgXCJwbGF5YmFja1wiLCBcInBsYXl0b25lc1wiLCBcInByaXZhY3ltYW5hZ2VyXCIsIFwicHJvY2VlZGluZ1wiLCBcInByb2dyZXNzXCIsIFwicXVldWVcIiwgXCJxdWV1ZWxvZ1wiLCBcInJhaXNlZXhjZXB0aW9uXCIsIFwicmVhZFwiLCBcInJlYWRleHRlblwiLCBcInJlYWRmaWxlXCIsIFwicmVjZWl2ZWZheFwiLCBcInJlY2VpdmVmYXhcIiwgXCJyZWNlaXZlZmF4XCIsIFwicmVjb3JkXCIsIFwicmVtb3ZlcXVldWVtZW1iZXJcIiwgXCJyZXNldGNkclwiLCBcInJldHJ5ZGlhbFwiLCBcInJldHVyblwiLCBcInJpbmdpbmdcIiwgXCJzYXlhbHBoYVwiLCBcInNheWNvdW50ZWRhZGpcIiwgXCJzYXljb3VudGVkbm91blwiLCBcInNheWNvdW50cGxcIiwgXCJzYXlkaWdpdHNcIiwgXCJzYXludW1iZXJcIiwgXCJzYXlwaG9uZXRpY1wiLCBcInNheXVuaXh0aW1lXCIsIFwic2VuZGR0bWZcIiwgXCJzZW5kZmF4XCIsIFwic2VuZGZheFwiLCBcInNlbmRmYXhcIiwgXCJzZW5kaW1hZ2VcIiwgXCJzZW5kdGV4dFwiLCBcInNlbmR1cmxcIiwgXCJzZXRcIiwgXCJzZXRhbWFmbGFnc1wiLCBcInNldGNhbGxlcnByZXNcIiwgXCJzZXRtdXNpY29uaG9sZFwiLCBcInNpcGFkZGhlYWRlclwiLCBcInNpcGR0bWZtb2RlXCIsIFwic2lwcmVtb3ZlaGVhZGVyXCIsIFwic2tlbFwiLCBcInNsYXN0YXRpb25cIiwgXCJzbGF0cnVua1wiLCBcInNtc1wiLCBcInNvZnRoYW5ndXBcIiwgXCJzcGVlY2hhY3RpdmF0ZWdyYW1tYXJcIiwgXCJzcGVlY2hiYWNrZ3JvdW5kXCIsIFwic3BlZWNoY3JlYXRlXCIsIFwic3BlZWNoZGVhY3RpdmF0ZWdyYW1tYXJcIiwgXCJzcGVlY2hkZXN0cm95XCIsIFwic3BlZWNobG9hZGdyYW1tYXJcIiwgXCJzcGVlY2hwcm9jZXNzaW5nc291bmRcIiwgXCJzcGVlY2hzdGFydFwiLCBcInNwZWVjaHVubG9hZGdyYW1tYXJcIiwgXCJzdGFja3BvcFwiLCBcInN0YXJ0bXVzaWNvbmhvbGRcIiwgXCJzdG9wbWl4bW9uaXRvclwiLCBcInN0b3Btb25pdG9yXCIsIFwic3RvcG11c2ljb25ob2xkXCIsIFwic3RvcHBsYXl0b25lc1wiLCBcInN5c3RlbVwiLCBcInRlc3RjbGllbnRcIiwgXCJ0ZXN0c2VydmVyXCIsIFwidHJhbnNmZXJcIiwgXCJ0cnlleGVjXCIsIFwidHJ5c3lzdGVtXCIsIFwidW5wYXVzZW1vbml0b3JcIiwgXCJ1bnBhdXNlcXVldWVtZW1iZXJcIiwgXCJ1c2VyZXZlbnRcIiwgXCJ2ZXJib3NlXCIsIFwidm1hdXRoZW50aWNhdGVcIiwgXCJ2bXNheW5hbWVcIiwgXCJ2b2ljZW1haWxcIiwgXCJ2b2ljZW1haWxtYWluXCIsIFwid2FpdFwiLCBcIndhaXRleHRlblwiLCBcIndhaXRmb3Jub2lzZVwiLCBcIndhaXRmb3JyaW5nXCIsIFwid2FpdGZvcnNpbGVuY2VcIiwgXCJ3YWl0bXVzaWNvbmhvbGRcIiwgXCJ3YWl0dW50aWxcIiwgXCJ3aGlsZVwiLCBcInphcGF0ZWxsZXJcIl07XG5mdW5jdGlvbiBiYXNpY1Rva2VuKHN0cmVhbSwgc3RhdGUpIHtcbiAgdmFyIGN1ciA9ICcnO1xuICB2YXIgY2ggPSBzdHJlYW0ubmV4dCgpO1xuICAvLyBjb21tZW50XG4gIGlmIChzdGF0ZS5ibG9ja0NvbW1lbnQpIHtcbiAgICBpZiAoY2ggPT0gXCItXCIgJiYgc3RyZWFtLm1hdGNoKFwiLTtcIiwgdHJ1ZSkpIHtcbiAgICAgIHN0YXRlLmJsb2NrQ29tbWVudCA9IGZhbHNlO1xuICAgIH0gZWxzZSBpZiAoc3RyZWFtLnNraXBUbyhcIi0tO1wiKSkge1xuICAgICAgc3RyZWFtLm5leHQoKTtcbiAgICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgICBzdHJlYW0ubmV4dCgpO1xuICAgICAgc3RhdGUuYmxvY2tDb21tZW50ID0gZmFsc2U7XG4gICAgfSBlbHNlIHtcbiAgICAgIHN0cmVhbS5za2lwVG9FbmQoKTtcbiAgICB9XG4gICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICB9XG4gIGlmIChjaCA9PSBcIjtcIikge1xuICAgIGlmIChzdHJlYW0ubWF0Y2goXCItLVwiLCB0cnVlKSkge1xuICAgICAgaWYgKCFzdHJlYW0ubWF0Y2goXCItXCIsIGZhbHNlKSkge1xuICAgICAgICAvLyBFeGNlcHQgOy0tLSBpcyBub3QgYSBibG9jayBjb21tZW50XG4gICAgICAgIHN0YXRlLmJsb2NrQ29tbWVudCA9IHRydWU7XG4gICAgICAgIHJldHVybiBcImNvbW1lbnRcIjtcbiAgICAgIH1cbiAgICB9XG4gICAgc3RyZWFtLnNraXBUb0VuZCgpO1xuICAgIHJldHVybiBcImNvbW1lbnRcIjtcbiAgfVxuICAvLyBjb250ZXh0XG4gIGlmIChjaCA9PSAnWycpIHtcbiAgICBzdHJlYW0uc2tpcFRvKCddJyk7XG4gICAgc3RyZWFtLmVhdCgnXScpO1xuICAgIHJldHVybiBcImhlYWRlclwiO1xuICB9XG4gIC8vIHN0cmluZ1xuICBpZiAoY2ggPT0gJ1wiJykge1xuICAgIHN0cmVhbS5za2lwVG8oJ1wiJyk7XG4gICAgcmV0dXJuIFwic3RyaW5nXCI7XG4gIH1cbiAgaWYgKGNoID09IFwiJ1wiKSB7XG4gICAgc3RyZWFtLnNraXBUbyhcIidcIik7XG4gICAgcmV0dXJuIFwic3RyaW5nLnNwZWNpYWxcIjtcbiAgfVxuICAvLyBkaWFscGxhbiBjb21tYW5kc1xuICBpZiAoY2ggPT0gJyMnKSB7XG4gICAgc3RyZWFtLmVhdFdoaWxlKC9cXHcvKTtcbiAgICBjdXIgPSBzdHJlYW0uY3VycmVudCgpO1xuICAgIGlmIChkcGNtZC5pbmRleE9mKGN1cikgIT09IC0xKSB7XG4gICAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgICByZXR1cm4gXCJzdHJvbmdcIjtcbiAgICB9XG4gIH1cbiAgLy8gYXBwbGljYXRpb24gYXJnc1xuICBpZiAoY2ggPT0gJyQnKSB7XG4gICAgdmFyIGNoMSA9IHN0cmVhbS5wZWVrKCk7XG4gICAgaWYgKGNoMSA9PSAneycpIHtcbiAgICAgIHN0cmVhbS5za2lwVG8oJ30nKTtcbiAgICAgIHN0cmVhbS5lYXQoJ30nKTtcbiAgICAgIHJldHVybiBcInZhcmlhYmxlTmFtZS5zcGVjaWFsXCI7XG4gICAgfVxuICB9XG4gIC8vIGV4dGVuc2lvblxuICBzdHJlYW0uZWF0V2hpbGUoL1xcdy8pO1xuICBjdXIgPSBzdHJlYW0uY3VycmVudCgpO1xuICBpZiAoYXRvbXMuaW5kZXhPZihjdXIpICE9PSAtMSkge1xuICAgIHN0YXRlLmV4dGVuU3RhcnQgPSB0cnVlO1xuICAgIHN3aXRjaCAoY3VyKSB7XG4gICAgICBjYXNlICdzYW1lJzpcbiAgICAgICAgc3RhdGUuZXh0ZW5TYW1lID0gdHJ1ZTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdpbmNsdWRlJzpcbiAgICAgIGNhc2UgJ3N3aXRjaCc6XG4gICAgICBjYXNlICdpZ25vcmVwYXQnOlxuICAgICAgICBzdGF0ZS5leHRlbkluY2x1ZGUgPSB0cnVlO1xuICAgICAgICBicmVhaztcbiAgICAgIGRlZmF1bHQ6XG4gICAgICAgIGJyZWFrO1xuICAgIH1cbiAgICByZXR1cm4gXCJhdG9tXCI7XG4gIH1cbn1cbmV4cG9ydCBjb25zdCBhc3RlcmlzayA9IHtcbiAgbmFtZTogXCJhc3Rlcmlza1wiLFxuICBzdGFydFN0YXRlOiBmdW5jdGlvbiAoKSB7XG4gICAgcmV0dXJuIHtcbiAgICAgIGJsb2NrQ29tbWVudDogZmFsc2UsXG4gICAgICBleHRlblN0YXJ0OiBmYWxzZSxcbiAgICAgIGV4dGVuU2FtZTogZmFsc2UsXG4gICAgICBleHRlbkluY2x1ZGU6IGZhbHNlLFxuICAgICAgZXh0ZW5FeHRlbjogZmFsc2UsXG4gICAgICBleHRlblByaW9yaXR5OiBmYWxzZSxcbiAgICAgIGV4dGVuQXBwbGljYXRpb246IGZhbHNlXG4gICAgfTtcbiAgfSxcbiAgdG9rZW46IGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgdmFyIGN1ciA9ICcnO1xuICAgIGlmIChzdHJlYW0uZWF0U3BhY2UoKSkgcmV0dXJuIG51bGw7XG4gICAgLy8gZXh0ZW5zaW9uIHN0YXJ0ZWRcbiAgICBpZiAoc3RhdGUuZXh0ZW5TdGFydCkge1xuICAgICAgc3RyZWFtLmVhdFdoaWxlKC9bXlxcc10vKTtcbiAgICAgIGN1ciA9IHN0cmVhbS5jdXJyZW50KCk7XG4gICAgICBpZiAoL149Pj8kLy50ZXN0KGN1cikpIHtcbiAgICAgICAgc3RhdGUuZXh0ZW5FeHRlbiA9IHRydWU7XG4gICAgICAgIHN0YXRlLmV4dGVuU3RhcnQgPSBmYWxzZTtcbiAgICAgICAgcmV0dXJuIFwic3Ryb25nXCI7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBzdGF0ZS5leHRlblN0YXJ0ID0gZmFsc2U7XG4gICAgICAgIHN0cmVhbS5za2lwVG9FbmQoKTtcbiAgICAgICAgcmV0dXJuIFwiZXJyb3JcIjtcbiAgICAgIH1cbiAgICB9IGVsc2UgaWYgKHN0YXRlLmV4dGVuRXh0ZW4pIHtcbiAgICAgIC8vIHNldCBleHRlbiBhbmQgcHJpb3JpdHlcbiAgICAgIHN0YXRlLmV4dGVuRXh0ZW4gPSBmYWxzZTtcbiAgICAgIHN0YXRlLmV4dGVuUHJpb3JpdHkgPSB0cnVlO1xuICAgICAgc3RyZWFtLmVhdFdoaWxlKC9bXixdLyk7XG4gICAgICBpZiAoc3RhdGUuZXh0ZW5JbmNsdWRlKSB7XG4gICAgICAgIHN0cmVhbS5za2lwVG9FbmQoKTtcbiAgICAgICAgc3RhdGUuZXh0ZW5Qcmlvcml0eSA9IGZhbHNlO1xuICAgICAgICBzdGF0ZS5leHRlbkluY2x1ZGUgPSBmYWxzZTtcbiAgICAgIH1cbiAgICAgIGlmIChzdGF0ZS5leHRlblNhbWUpIHtcbiAgICAgICAgc3RhdGUuZXh0ZW5Qcmlvcml0eSA9IGZhbHNlO1xuICAgICAgICBzdGF0ZS5leHRlblNhbWUgPSBmYWxzZTtcbiAgICAgICAgc3RhdGUuZXh0ZW5BcHBsaWNhdGlvbiA9IHRydWU7XG4gICAgICB9XG4gICAgICByZXR1cm4gXCJ0YWdcIjtcbiAgICB9IGVsc2UgaWYgKHN0YXRlLmV4dGVuUHJpb3JpdHkpIHtcbiAgICAgIHN0YXRlLmV4dGVuUHJpb3JpdHkgPSBmYWxzZTtcbiAgICAgIHN0YXRlLmV4dGVuQXBwbGljYXRpb24gPSB0cnVlO1xuICAgICAgc3RyZWFtLm5leHQoKTsgLy8gZ2V0IGNvbW1hXG4gICAgICBpZiAoc3RhdGUuZXh0ZW5TYW1lKSByZXR1cm4gbnVsbDtcbiAgICAgIHN0cmVhbS5lYXRXaGlsZSgvW14sXS8pO1xuICAgICAgcmV0dXJuIFwibnVtYmVyXCI7XG4gICAgfSBlbHNlIGlmIChzdGF0ZS5leHRlbkFwcGxpY2F0aW9uKSB7XG4gICAgICBzdHJlYW0uZWF0V2hpbGUoLywvKTtcbiAgICAgIGN1ciA9IHN0cmVhbS5jdXJyZW50KCk7XG4gICAgICBpZiAoY3VyID09PSAnLCcpIHJldHVybiBudWxsO1xuICAgICAgc3RyZWFtLmVhdFdoaWxlKC9cXHcvKTtcbiAgICAgIGN1ciA9IHN0cmVhbS5jdXJyZW50KCkudG9Mb3dlckNhc2UoKTtcbiAgICAgIHN0YXRlLmV4dGVuQXBwbGljYXRpb24gPSBmYWxzZTtcbiAgICAgIGlmIChhcHBzLmluZGV4T2YoY3VyKSAhPT0gLTEpIHtcbiAgICAgICAgcmV0dXJuIFwiZGVmXCI7XG4gICAgICB9XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiBiYXNpY1Rva2VuKHN0cmVhbSwgc3RhdGUpO1xuICAgIH1cbiAgICByZXR1cm4gbnVsbDtcbiAgfSxcbiAgbGFuZ3VhZ2VEYXRhOiB7XG4gICAgY29tbWVudFRva2Vuczoge1xuICAgICAgbGluZTogXCI7XCIsXG4gICAgICBibG9jazoge1xuICAgICAgICBvcGVuOiBcIjstLVwiLFxuICAgICAgICBjbG9zZTogXCItLTtcIlxuICAgICAgfVxuICAgIH1cbiAgfVxufTsiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=