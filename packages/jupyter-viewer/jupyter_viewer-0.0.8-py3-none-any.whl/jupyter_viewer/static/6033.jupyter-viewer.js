"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[6033],{

/***/ 6033:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "vhdl": () => (/* binding */ vhdl)
/* harmony export */ });
function words(str) {
  var obj = {},
    words = str.split(",");
  for (var i = 0; i < words.length; ++i) {
    var allCaps = words[i].toUpperCase();
    var firstCap = words[i].charAt(0).toUpperCase() + words[i].slice(1);
    obj[words[i]] = true;
    obj[allCaps] = true;
    obj[firstCap] = true;
  }
  return obj;
}
function metaHook(stream) {
  stream.eatWhile(/[\w\$_]/);
  return "meta";
}
var atoms = words("null"),
  hooks = {
    "`": metaHook,
    "$": metaHook
  },
  multiLineStrings = false;
var keywords = words("abs,access,after,alias,all,and,architecture,array,assert,attribute,begin,block," + "body,buffer,bus,case,component,configuration,constant,disconnect,downto,else,elsif,end,end block,end case," + "end component,end for,end generate,end if,end loop,end process,end record,end units,entity,exit,file,for," + "function,generate,generic,generic map,group,guarded,if,impure,in,inertial,inout,is,label,library,linkage," + "literal,loop,map,mod,nand,new,next,nor,null,of,on,open,or,others,out,package,package body,port,port map," + "postponed,procedure,process,pure,range,record,register,reject,rem,report,return,rol,ror,select,severity,signal," + "sla,sll,sra,srl,subtype,then,to,transport,type,unaffected,units,until,use,variable,wait,when,while,with,xnor,xor");
var blockKeywords = words("architecture,entity,begin,case,port,else,elsif,end,for,function,if");
var isOperatorChar = /[&|~><!\)\(*#%@+\/=?\:;}{,\.\^\-\[\]]/;
var curPunc;
function tokenBase(stream, state) {
  var ch = stream.next();
  if (hooks[ch]) {
    var result = hooks[ch](stream, state);
    if (result !== false) return result;
  }
  if (ch == '"') {
    state.tokenize = tokenString2(ch);
    return state.tokenize(stream, state);
  }
  if (ch == "'") {
    state.tokenize = tokenString(ch);
    return state.tokenize(stream, state);
  }
  if (/[\[\]{}\(\),;\:\.]/.test(ch)) {
    curPunc = ch;
    return null;
  }
  if (/[\d']/.test(ch)) {
    stream.eatWhile(/[\w\.']/);
    return "number";
  }
  if (ch == "-") {
    if (stream.eat("-")) {
      stream.skipToEnd();
      return "comment";
    }
  }
  if (isOperatorChar.test(ch)) {
    stream.eatWhile(isOperatorChar);
    return "operator";
  }
  stream.eatWhile(/[\w\$_]/);
  var cur = stream.current();
  if (keywords.propertyIsEnumerable(cur.toLowerCase())) {
    if (blockKeywords.propertyIsEnumerable(cur)) curPunc = "newstatement";
    return "keyword";
  }
  if (atoms.propertyIsEnumerable(cur)) return "atom";
  return "variable";
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
      escaped = !escaped && next == "--";
    }
    if (end || !(escaped || multiLineStrings)) state.tokenize = tokenBase;
    return "string";
  };
}
function tokenString2(quote) {
  return function (stream, state) {
    var escaped = false,
      next,
      end = false;
    while ((next = stream.next()) != null) {
      if (next == quote && !escaped) {
        end = true;
        break;
      }
      escaped = !escaped && next == "--";
    }
    if (end || !(escaped || multiLineStrings)) state.tokenize = tokenBase;
    return "string.special";
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
  return state.context = new Context(state.indented, col, type, null, state.context);
}
function popContext(state) {
  var t = state.context.type;
  if (t == ")" || t == "]" || t == "}") state.indented = state.context.indented;
  return state.context = state.context.prev;
}

// Interface
const vhdl = {
  name: "vhdl",
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
    var firstChar = textAfter && textAfter.charAt(0),
      ctx = state.context,
      closing = firstChar == ctx.type;
    if (ctx.type == "statement") return ctx.indented + (firstChar == "{" ? 0 : cx.unit);else if (ctx.align) return ctx.column + (closing ? 0 : 1);else return ctx.indented + (closing ? 0 : cx.unit);
  },
  languageData: {
    indentOnInput: /^\s*[{}]$/,
    commentTokens: {
      line: "--"
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNjAzMy5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL0Bjb2RlbWlycm9yL2xlZ2FjeS1tb2Rlcy9tb2RlL3ZoZGwuanMiXSwic291cmNlc0NvbnRlbnQiOlsiZnVuY3Rpb24gd29yZHMoc3RyKSB7XG4gIHZhciBvYmogPSB7fSxcbiAgICB3b3JkcyA9IHN0ci5zcGxpdChcIixcIik7XG4gIGZvciAodmFyIGkgPSAwOyBpIDwgd29yZHMubGVuZ3RoOyArK2kpIHtcbiAgICB2YXIgYWxsQ2FwcyA9IHdvcmRzW2ldLnRvVXBwZXJDYXNlKCk7XG4gICAgdmFyIGZpcnN0Q2FwID0gd29yZHNbaV0uY2hhckF0KDApLnRvVXBwZXJDYXNlKCkgKyB3b3Jkc1tpXS5zbGljZSgxKTtcbiAgICBvYmpbd29yZHNbaV1dID0gdHJ1ZTtcbiAgICBvYmpbYWxsQ2Fwc10gPSB0cnVlO1xuICAgIG9ialtmaXJzdENhcF0gPSB0cnVlO1xuICB9XG4gIHJldHVybiBvYmo7XG59XG5mdW5jdGlvbiBtZXRhSG9vayhzdHJlYW0pIHtcbiAgc3RyZWFtLmVhdFdoaWxlKC9bXFx3XFwkX10vKTtcbiAgcmV0dXJuIFwibWV0YVwiO1xufVxudmFyIGF0b21zID0gd29yZHMoXCJudWxsXCIpLFxuICBob29rcyA9IHtcbiAgICBcImBcIjogbWV0YUhvb2ssXG4gICAgXCIkXCI6IG1ldGFIb29rXG4gIH0sXG4gIG11bHRpTGluZVN0cmluZ3MgPSBmYWxzZTtcbnZhciBrZXl3b3JkcyA9IHdvcmRzKFwiYWJzLGFjY2VzcyxhZnRlcixhbGlhcyxhbGwsYW5kLGFyY2hpdGVjdHVyZSxhcnJheSxhc3NlcnQsYXR0cmlidXRlLGJlZ2luLGJsb2NrLFwiICsgXCJib2R5LGJ1ZmZlcixidXMsY2FzZSxjb21wb25lbnQsY29uZmlndXJhdGlvbixjb25zdGFudCxkaXNjb25uZWN0LGRvd250byxlbHNlLGVsc2lmLGVuZCxlbmQgYmxvY2ssZW5kIGNhc2UsXCIgKyBcImVuZCBjb21wb25lbnQsZW5kIGZvcixlbmQgZ2VuZXJhdGUsZW5kIGlmLGVuZCBsb29wLGVuZCBwcm9jZXNzLGVuZCByZWNvcmQsZW5kIHVuaXRzLGVudGl0eSxleGl0LGZpbGUsZm9yLFwiICsgXCJmdW5jdGlvbixnZW5lcmF0ZSxnZW5lcmljLGdlbmVyaWMgbWFwLGdyb3VwLGd1YXJkZWQsaWYsaW1wdXJlLGluLGluZXJ0aWFsLGlub3V0LGlzLGxhYmVsLGxpYnJhcnksbGlua2FnZSxcIiArIFwibGl0ZXJhbCxsb29wLG1hcCxtb2QsbmFuZCxuZXcsbmV4dCxub3IsbnVsbCxvZixvbixvcGVuLG9yLG90aGVycyxvdXQscGFja2FnZSxwYWNrYWdlIGJvZHkscG9ydCxwb3J0IG1hcCxcIiArIFwicG9zdHBvbmVkLHByb2NlZHVyZSxwcm9jZXNzLHB1cmUscmFuZ2UscmVjb3JkLHJlZ2lzdGVyLHJlamVjdCxyZW0scmVwb3J0LHJldHVybixyb2wscm9yLHNlbGVjdCxzZXZlcml0eSxzaWduYWwsXCIgKyBcInNsYSxzbGwsc3JhLHNybCxzdWJ0eXBlLHRoZW4sdG8sdHJhbnNwb3J0LHR5cGUsdW5hZmZlY3RlZCx1bml0cyx1bnRpbCx1c2UsdmFyaWFibGUsd2FpdCx3aGVuLHdoaWxlLHdpdGgseG5vcix4b3JcIik7XG52YXIgYmxvY2tLZXl3b3JkcyA9IHdvcmRzKFwiYXJjaGl0ZWN0dXJlLGVudGl0eSxiZWdpbixjYXNlLHBvcnQsZWxzZSxlbHNpZixlbmQsZm9yLGZ1bmN0aW9uLGlmXCIpO1xudmFyIGlzT3BlcmF0b3JDaGFyID0gL1smfH4+PCFcXClcXCgqIyVAK1xcLz0/XFw6O317LFxcLlxcXlxcLVxcW1xcXV0vO1xudmFyIGN1clB1bmM7XG5mdW5jdGlvbiB0b2tlbkJhc2Uoc3RyZWFtLCBzdGF0ZSkge1xuICB2YXIgY2ggPSBzdHJlYW0ubmV4dCgpO1xuICBpZiAoaG9va3NbY2hdKSB7XG4gICAgdmFyIHJlc3VsdCA9IGhvb2tzW2NoXShzdHJlYW0sIHN0YXRlKTtcbiAgICBpZiAocmVzdWx0ICE9PSBmYWxzZSkgcmV0dXJuIHJlc3VsdDtcbiAgfVxuICBpZiAoY2ggPT0gJ1wiJykge1xuICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5TdHJpbmcyKGNoKTtcbiAgICByZXR1cm4gc3RhdGUudG9rZW5pemUoc3RyZWFtLCBzdGF0ZSk7XG4gIH1cbiAgaWYgKGNoID09IFwiJ1wiKSB7XG4gICAgc3RhdGUudG9rZW5pemUgPSB0b2tlblN0cmluZyhjaCk7XG4gICAgcmV0dXJuIHN0YXRlLnRva2VuaXplKHN0cmVhbSwgc3RhdGUpO1xuICB9XG4gIGlmICgvW1xcW1xcXXt9XFwoXFwpLDtcXDpcXC5dLy50ZXN0KGNoKSkge1xuICAgIGN1clB1bmMgPSBjaDtcbiAgICByZXR1cm4gbnVsbDtcbiAgfVxuICBpZiAoL1tcXGQnXS8udGVzdChjaCkpIHtcbiAgICBzdHJlYW0uZWF0V2hpbGUoL1tcXHdcXC4nXS8pO1xuICAgIHJldHVybiBcIm51bWJlclwiO1xuICB9XG4gIGlmIChjaCA9PSBcIi1cIikge1xuICAgIGlmIChzdHJlYW0uZWF0KFwiLVwiKSkge1xuICAgICAgc3RyZWFtLnNraXBUb0VuZCgpO1xuICAgICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICAgIH1cbiAgfVxuICBpZiAoaXNPcGVyYXRvckNoYXIudGVzdChjaCkpIHtcbiAgICBzdHJlYW0uZWF0V2hpbGUoaXNPcGVyYXRvckNoYXIpO1xuICAgIHJldHVybiBcIm9wZXJhdG9yXCI7XG4gIH1cbiAgc3RyZWFtLmVhdFdoaWxlKC9bXFx3XFwkX10vKTtcbiAgdmFyIGN1ciA9IHN0cmVhbS5jdXJyZW50KCk7XG4gIGlmIChrZXl3b3Jkcy5wcm9wZXJ0eUlzRW51bWVyYWJsZShjdXIudG9Mb3dlckNhc2UoKSkpIHtcbiAgICBpZiAoYmxvY2tLZXl3b3Jkcy5wcm9wZXJ0eUlzRW51bWVyYWJsZShjdXIpKSBjdXJQdW5jID0gXCJuZXdzdGF0ZW1lbnRcIjtcbiAgICByZXR1cm4gXCJrZXl3b3JkXCI7XG4gIH1cbiAgaWYgKGF0b21zLnByb3BlcnR5SXNFbnVtZXJhYmxlKGN1cikpIHJldHVybiBcImF0b21cIjtcbiAgcmV0dXJuIFwidmFyaWFibGVcIjtcbn1cbmZ1bmN0aW9uIHRva2VuU3RyaW5nKHF1b3RlKSB7XG4gIHJldHVybiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIHZhciBlc2NhcGVkID0gZmFsc2UsXG4gICAgICBuZXh0LFxuICAgICAgZW5kID0gZmFsc2U7XG4gICAgd2hpbGUgKChuZXh0ID0gc3RyZWFtLm5leHQoKSkgIT0gbnVsbCkge1xuICAgICAgaWYgKG5leHQgPT0gcXVvdGUgJiYgIWVzY2FwZWQpIHtcbiAgICAgICAgZW5kID0gdHJ1ZTtcbiAgICAgICAgYnJlYWs7XG4gICAgICB9XG4gICAgICBlc2NhcGVkID0gIWVzY2FwZWQgJiYgbmV4dCA9PSBcIi0tXCI7XG4gICAgfVxuICAgIGlmIChlbmQgfHwgIShlc2NhcGVkIHx8IG11bHRpTGluZVN0cmluZ3MpKSBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQmFzZTtcbiAgICByZXR1cm4gXCJzdHJpbmdcIjtcbiAgfTtcbn1cbmZ1bmN0aW9uIHRva2VuU3RyaW5nMihxdW90ZSkge1xuICByZXR1cm4gZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICB2YXIgZXNjYXBlZCA9IGZhbHNlLFxuICAgICAgbmV4dCxcbiAgICAgIGVuZCA9IGZhbHNlO1xuICAgIHdoaWxlICgobmV4dCA9IHN0cmVhbS5uZXh0KCkpICE9IG51bGwpIHtcbiAgICAgIGlmIChuZXh0ID09IHF1b3RlICYmICFlc2NhcGVkKSB7XG4gICAgICAgIGVuZCA9IHRydWU7XG4gICAgICAgIGJyZWFrO1xuICAgICAgfVxuICAgICAgZXNjYXBlZCA9ICFlc2NhcGVkICYmIG5leHQgPT0gXCItLVwiO1xuICAgIH1cbiAgICBpZiAoZW5kIHx8ICEoZXNjYXBlZCB8fCBtdWx0aUxpbmVTdHJpbmdzKSkgc3RhdGUudG9rZW5pemUgPSB0b2tlbkJhc2U7XG4gICAgcmV0dXJuIFwic3RyaW5nLnNwZWNpYWxcIjtcbiAgfTtcbn1cbmZ1bmN0aW9uIENvbnRleHQoaW5kZW50ZWQsIGNvbHVtbiwgdHlwZSwgYWxpZ24sIHByZXYpIHtcbiAgdGhpcy5pbmRlbnRlZCA9IGluZGVudGVkO1xuICB0aGlzLmNvbHVtbiA9IGNvbHVtbjtcbiAgdGhpcy50eXBlID0gdHlwZTtcbiAgdGhpcy5hbGlnbiA9IGFsaWduO1xuICB0aGlzLnByZXYgPSBwcmV2O1xufVxuZnVuY3Rpb24gcHVzaENvbnRleHQoc3RhdGUsIGNvbCwgdHlwZSkge1xuICByZXR1cm4gc3RhdGUuY29udGV4dCA9IG5ldyBDb250ZXh0KHN0YXRlLmluZGVudGVkLCBjb2wsIHR5cGUsIG51bGwsIHN0YXRlLmNvbnRleHQpO1xufVxuZnVuY3Rpb24gcG9wQ29udGV4dChzdGF0ZSkge1xuICB2YXIgdCA9IHN0YXRlLmNvbnRleHQudHlwZTtcbiAgaWYgKHQgPT0gXCIpXCIgfHwgdCA9PSBcIl1cIiB8fCB0ID09IFwifVwiKSBzdGF0ZS5pbmRlbnRlZCA9IHN0YXRlLmNvbnRleHQuaW5kZW50ZWQ7XG4gIHJldHVybiBzdGF0ZS5jb250ZXh0ID0gc3RhdGUuY29udGV4dC5wcmV2O1xufVxuXG4vLyBJbnRlcmZhY2VcbmV4cG9ydCBjb25zdCB2aGRsID0ge1xuICBuYW1lOiBcInZoZGxcIixcbiAgc3RhcnRTdGF0ZTogZnVuY3Rpb24gKGluZGVudFVuaXQpIHtcbiAgICByZXR1cm4ge1xuICAgICAgdG9rZW5pemU6IG51bGwsXG4gICAgICBjb250ZXh0OiBuZXcgQ29udGV4dCgtaW5kZW50VW5pdCwgMCwgXCJ0b3BcIiwgZmFsc2UpLFxuICAgICAgaW5kZW50ZWQ6IDAsXG4gICAgICBzdGFydE9mTGluZTogdHJ1ZVxuICAgIH07XG4gIH0sXG4gIHRva2VuOiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIHZhciBjdHggPSBzdGF0ZS5jb250ZXh0O1xuICAgIGlmIChzdHJlYW0uc29sKCkpIHtcbiAgICAgIGlmIChjdHguYWxpZ24gPT0gbnVsbCkgY3R4LmFsaWduID0gZmFsc2U7XG4gICAgICBzdGF0ZS5pbmRlbnRlZCA9IHN0cmVhbS5pbmRlbnRhdGlvbigpO1xuICAgICAgc3RhdGUuc3RhcnRPZkxpbmUgPSB0cnVlO1xuICAgIH1cbiAgICBpZiAoc3RyZWFtLmVhdFNwYWNlKCkpIHJldHVybiBudWxsO1xuICAgIGN1clB1bmMgPSBudWxsO1xuICAgIHZhciBzdHlsZSA9IChzdGF0ZS50b2tlbml6ZSB8fCB0b2tlbkJhc2UpKHN0cmVhbSwgc3RhdGUpO1xuICAgIGlmIChzdHlsZSA9PSBcImNvbW1lbnRcIiB8fCBzdHlsZSA9PSBcIm1ldGFcIikgcmV0dXJuIHN0eWxlO1xuICAgIGlmIChjdHguYWxpZ24gPT0gbnVsbCkgY3R4LmFsaWduID0gdHJ1ZTtcbiAgICBpZiAoKGN1clB1bmMgPT0gXCI7XCIgfHwgY3VyUHVuYyA9PSBcIjpcIikgJiYgY3R4LnR5cGUgPT0gXCJzdGF0ZW1lbnRcIikgcG9wQ29udGV4dChzdGF0ZSk7ZWxzZSBpZiAoY3VyUHVuYyA9PSBcIntcIikgcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbS5jb2x1bW4oKSwgXCJ9XCIpO2Vsc2UgaWYgKGN1clB1bmMgPT0gXCJbXCIpIHB1c2hDb250ZXh0KHN0YXRlLCBzdHJlYW0uY29sdW1uKCksIFwiXVwiKTtlbHNlIGlmIChjdXJQdW5jID09IFwiKFwiKSBwdXNoQ29udGV4dChzdGF0ZSwgc3RyZWFtLmNvbHVtbigpLCBcIilcIik7ZWxzZSBpZiAoY3VyUHVuYyA9PSBcIn1cIikge1xuICAgICAgd2hpbGUgKGN0eC50eXBlID09IFwic3RhdGVtZW50XCIpIGN0eCA9IHBvcENvbnRleHQoc3RhdGUpO1xuICAgICAgaWYgKGN0eC50eXBlID09IFwifVwiKSBjdHggPSBwb3BDb250ZXh0KHN0YXRlKTtcbiAgICAgIHdoaWxlIChjdHgudHlwZSA9PSBcInN0YXRlbWVudFwiKSBjdHggPSBwb3BDb250ZXh0KHN0YXRlKTtcbiAgICB9IGVsc2UgaWYgKGN1clB1bmMgPT0gY3R4LnR5cGUpIHBvcENvbnRleHQoc3RhdGUpO2Vsc2UgaWYgKGN0eC50eXBlID09IFwifVwiIHx8IGN0eC50eXBlID09IFwidG9wXCIgfHwgY3R4LnR5cGUgPT0gXCJzdGF0ZW1lbnRcIiAmJiBjdXJQdW5jID09IFwibmV3c3RhdGVtZW50XCIpIHB1c2hDb250ZXh0KHN0YXRlLCBzdHJlYW0uY29sdW1uKCksIFwic3RhdGVtZW50XCIpO1xuICAgIHN0YXRlLnN0YXJ0T2ZMaW5lID0gZmFsc2U7XG4gICAgcmV0dXJuIHN0eWxlO1xuICB9LFxuICBpbmRlbnQ6IGZ1bmN0aW9uIChzdGF0ZSwgdGV4dEFmdGVyLCBjeCkge1xuICAgIGlmIChzdGF0ZS50b2tlbml6ZSAhPSB0b2tlbkJhc2UgJiYgc3RhdGUudG9rZW5pemUgIT0gbnVsbCkgcmV0dXJuIDA7XG4gICAgdmFyIGZpcnN0Q2hhciA9IHRleHRBZnRlciAmJiB0ZXh0QWZ0ZXIuY2hhckF0KDApLFxuICAgICAgY3R4ID0gc3RhdGUuY29udGV4dCxcbiAgICAgIGNsb3NpbmcgPSBmaXJzdENoYXIgPT0gY3R4LnR5cGU7XG4gICAgaWYgKGN0eC50eXBlID09IFwic3RhdGVtZW50XCIpIHJldHVybiBjdHguaW5kZW50ZWQgKyAoZmlyc3RDaGFyID09IFwie1wiID8gMCA6IGN4LnVuaXQpO2Vsc2UgaWYgKGN0eC5hbGlnbikgcmV0dXJuIGN0eC5jb2x1bW4gKyAoY2xvc2luZyA/IDAgOiAxKTtlbHNlIHJldHVybiBjdHguaW5kZW50ZWQgKyAoY2xvc2luZyA/IDAgOiBjeC51bml0KTtcbiAgfSxcbiAgbGFuZ3VhZ2VEYXRhOiB7XG4gICAgaW5kZW50T25JbnB1dDogL15cXHMqW3t9XSQvLFxuICAgIGNvbW1lbnRUb2tlbnM6IHtcbiAgICAgIGxpbmU6IFwiLS1cIlxuICAgIH1cbiAgfVxufTsiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=