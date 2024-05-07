"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[8672],{

/***/ 8672:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "gas": () => (/* binding */ gas),
/* harmony export */   "gasArm": () => (/* binding */ gasArm)
/* harmony export */ });
function mkGas(arch) {
  // If an architecture is specified, its initialization function may
  // populate this array with custom parsing functions which will be
  // tried in the event that the standard functions do not find a match.
  var custom = [];

  // The symbol used to start a line comment changes based on the target
  // architecture.
  // If no architecture is pased in "parserConfig" then only multiline
  // comments will have syntax support.
  var lineCommentStartSymbol = "";

  // These directives are architecture independent.
  // Machine specific directives should go in their respective
  // architecture initialization function.
  // Reference:
  // http://sourceware.org/binutils/docs/as/Pseudo-Ops.html#Pseudo-Ops
  var directives = {
    ".abort": "builtin",
    ".align": "builtin",
    ".altmacro": "builtin",
    ".ascii": "builtin",
    ".asciz": "builtin",
    ".balign": "builtin",
    ".balignw": "builtin",
    ".balignl": "builtin",
    ".bundle_align_mode": "builtin",
    ".bundle_lock": "builtin",
    ".bundle_unlock": "builtin",
    ".byte": "builtin",
    ".cfi_startproc": "builtin",
    ".comm": "builtin",
    ".data": "builtin",
    ".def": "builtin",
    ".desc": "builtin",
    ".dim": "builtin",
    ".double": "builtin",
    ".eject": "builtin",
    ".else": "builtin",
    ".elseif": "builtin",
    ".end": "builtin",
    ".endef": "builtin",
    ".endfunc": "builtin",
    ".endif": "builtin",
    ".equ": "builtin",
    ".equiv": "builtin",
    ".eqv": "builtin",
    ".err": "builtin",
    ".error": "builtin",
    ".exitm": "builtin",
    ".extern": "builtin",
    ".fail": "builtin",
    ".file": "builtin",
    ".fill": "builtin",
    ".float": "builtin",
    ".func": "builtin",
    ".global": "builtin",
    ".gnu_attribute": "builtin",
    ".hidden": "builtin",
    ".hword": "builtin",
    ".ident": "builtin",
    ".if": "builtin",
    ".incbin": "builtin",
    ".include": "builtin",
    ".int": "builtin",
    ".internal": "builtin",
    ".irp": "builtin",
    ".irpc": "builtin",
    ".lcomm": "builtin",
    ".lflags": "builtin",
    ".line": "builtin",
    ".linkonce": "builtin",
    ".list": "builtin",
    ".ln": "builtin",
    ".loc": "builtin",
    ".loc_mark_labels": "builtin",
    ".local": "builtin",
    ".long": "builtin",
    ".macro": "builtin",
    ".mri": "builtin",
    ".noaltmacro": "builtin",
    ".nolist": "builtin",
    ".octa": "builtin",
    ".offset": "builtin",
    ".org": "builtin",
    ".p2align": "builtin",
    ".popsection": "builtin",
    ".previous": "builtin",
    ".print": "builtin",
    ".protected": "builtin",
    ".psize": "builtin",
    ".purgem": "builtin",
    ".pushsection": "builtin",
    ".quad": "builtin",
    ".reloc": "builtin",
    ".rept": "builtin",
    ".sbttl": "builtin",
    ".scl": "builtin",
    ".section": "builtin",
    ".set": "builtin",
    ".short": "builtin",
    ".single": "builtin",
    ".size": "builtin",
    ".skip": "builtin",
    ".sleb128": "builtin",
    ".space": "builtin",
    ".stab": "builtin",
    ".string": "builtin",
    ".struct": "builtin",
    ".subsection": "builtin",
    ".symver": "builtin",
    ".tag": "builtin",
    ".text": "builtin",
    ".title": "builtin",
    ".type": "builtin",
    ".uleb128": "builtin",
    ".val": "builtin",
    ".version": "builtin",
    ".vtable_entry": "builtin",
    ".vtable_inherit": "builtin",
    ".warning": "builtin",
    ".weak": "builtin",
    ".weakref": "builtin",
    ".word": "builtin"
  };
  var registers = {};
  function x86() {
    lineCommentStartSymbol = "#";
    registers.al = "variable";
    registers.ah = "variable";
    registers.ax = "variable";
    registers.eax = "variableName.special";
    registers.rax = "variableName.special";
    registers.bl = "variable";
    registers.bh = "variable";
    registers.bx = "variable";
    registers.ebx = "variableName.special";
    registers.rbx = "variableName.special";
    registers.cl = "variable";
    registers.ch = "variable";
    registers.cx = "variable";
    registers.ecx = "variableName.special";
    registers.rcx = "variableName.special";
    registers.dl = "variable";
    registers.dh = "variable";
    registers.dx = "variable";
    registers.edx = "variableName.special";
    registers.rdx = "variableName.special";
    registers.si = "variable";
    registers.esi = "variableName.special";
    registers.rsi = "variableName.special";
    registers.di = "variable";
    registers.edi = "variableName.special";
    registers.rdi = "variableName.special";
    registers.sp = "variable";
    registers.esp = "variableName.special";
    registers.rsp = "variableName.special";
    registers.bp = "variable";
    registers.ebp = "variableName.special";
    registers.rbp = "variableName.special";
    registers.ip = "variable";
    registers.eip = "variableName.special";
    registers.rip = "variableName.special";
    registers.cs = "keyword";
    registers.ds = "keyword";
    registers.ss = "keyword";
    registers.es = "keyword";
    registers.fs = "keyword";
    registers.gs = "keyword";
  }
  function armv6() {
    // Reference:
    // http://infocenter.arm.com/help/topic/com.arm.doc.qrc0001l/QRC0001_UAL.pdf
    // http://infocenter.arm.com/help/topic/com.arm.doc.ddi0301h/DDI0301H_arm1176jzfs_r0p7_trm.pdf
    lineCommentStartSymbol = "@";
    directives.syntax = "builtin";
    registers.r0 = "variable";
    registers.r1 = "variable";
    registers.r2 = "variable";
    registers.r3 = "variable";
    registers.r4 = "variable";
    registers.r5 = "variable";
    registers.r6 = "variable";
    registers.r7 = "variable";
    registers.r8 = "variable";
    registers.r9 = "variable";
    registers.r10 = "variable";
    registers.r11 = "variable";
    registers.r12 = "variable";
    registers.sp = "variableName.special";
    registers.lr = "variableName.special";
    registers.pc = "variableName.special";
    registers.r13 = registers.sp;
    registers.r14 = registers.lr;
    registers.r15 = registers.pc;
    custom.push(function (ch, stream) {
      if (ch === '#') {
        stream.eatWhile(/\w/);
        return "number";
      }
    });
  }
  if (arch === "x86") {
    x86();
  } else if (arch === "arm" || arch === "armv6") {
    armv6();
  }
  function nextUntilUnescaped(stream, end) {
    var escaped = false,
      next;
    while ((next = stream.next()) != null) {
      if (next === end && !escaped) {
        return false;
      }
      escaped = !escaped && next === "\\";
    }
    return escaped;
  }
  function clikeComment(stream, state) {
    var maybeEnd = false,
      ch;
    while ((ch = stream.next()) != null) {
      if (ch === "/" && maybeEnd) {
        state.tokenize = null;
        break;
      }
      maybeEnd = ch === "*";
    }
    return "comment";
  }
  return {
    name: "gas",
    startState: function () {
      return {
        tokenize: null
      };
    },
    token: function (stream, state) {
      if (state.tokenize) {
        return state.tokenize(stream, state);
      }
      if (stream.eatSpace()) {
        return null;
      }
      var style,
        cur,
        ch = stream.next();
      if (ch === "/") {
        if (stream.eat("*")) {
          state.tokenize = clikeComment;
          return clikeComment(stream, state);
        }
      }
      if (ch === lineCommentStartSymbol) {
        stream.skipToEnd();
        return "comment";
      }
      if (ch === '"') {
        nextUntilUnescaped(stream, '"');
        return "string";
      }
      if (ch === '.') {
        stream.eatWhile(/\w/);
        cur = stream.current().toLowerCase();
        style = directives[cur];
        return style || null;
      }
      if (ch === '=') {
        stream.eatWhile(/\w/);
        return "tag";
      }
      if (ch === '{') {
        return "bracket";
      }
      if (ch === '}') {
        return "bracket";
      }
      if (/\d/.test(ch)) {
        if (ch === "0" && stream.eat("x")) {
          stream.eatWhile(/[0-9a-fA-F]/);
          return "number";
        }
        stream.eatWhile(/\d/);
        return "number";
      }
      if (/\w/.test(ch)) {
        stream.eatWhile(/\w/);
        if (stream.eat(":")) {
          return 'tag';
        }
        cur = stream.current().toLowerCase();
        style = registers[cur];
        return style || null;
      }
      for (var i = 0; i < custom.length; i++) {
        style = custom[i](ch, stream, state);
        if (style) {
          return style;
        }
      }
    },
    languageData: {
      commentTokens: {
        line: lineCommentStartSymbol,
        block: {
          open: "/*",
          close: "*/"
        }
      }
    }
  };
}
;
const gas = mkGas("x86");
const gasArm = mkGas("arm");

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiODY3Mi5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGNvZGVtaXJyb3IvbGVnYWN5LW1vZGVzL21vZGUvZ2FzLmpzIl0sInNvdXJjZXNDb250ZW50IjpbImZ1bmN0aW9uIG1rR2FzKGFyY2gpIHtcbiAgLy8gSWYgYW4gYXJjaGl0ZWN0dXJlIGlzIHNwZWNpZmllZCwgaXRzIGluaXRpYWxpemF0aW9uIGZ1bmN0aW9uIG1heVxuICAvLyBwb3B1bGF0ZSB0aGlzIGFycmF5IHdpdGggY3VzdG9tIHBhcnNpbmcgZnVuY3Rpb25zIHdoaWNoIHdpbGwgYmVcbiAgLy8gdHJpZWQgaW4gdGhlIGV2ZW50IHRoYXQgdGhlIHN0YW5kYXJkIGZ1bmN0aW9ucyBkbyBub3QgZmluZCBhIG1hdGNoLlxuICB2YXIgY3VzdG9tID0gW107XG5cbiAgLy8gVGhlIHN5bWJvbCB1c2VkIHRvIHN0YXJ0IGEgbGluZSBjb21tZW50IGNoYW5nZXMgYmFzZWQgb24gdGhlIHRhcmdldFxuICAvLyBhcmNoaXRlY3R1cmUuXG4gIC8vIElmIG5vIGFyY2hpdGVjdHVyZSBpcyBwYXNlZCBpbiBcInBhcnNlckNvbmZpZ1wiIHRoZW4gb25seSBtdWx0aWxpbmVcbiAgLy8gY29tbWVudHMgd2lsbCBoYXZlIHN5bnRheCBzdXBwb3J0LlxuICB2YXIgbGluZUNvbW1lbnRTdGFydFN5bWJvbCA9IFwiXCI7XG5cbiAgLy8gVGhlc2UgZGlyZWN0aXZlcyBhcmUgYXJjaGl0ZWN0dXJlIGluZGVwZW5kZW50LlxuICAvLyBNYWNoaW5lIHNwZWNpZmljIGRpcmVjdGl2ZXMgc2hvdWxkIGdvIGluIHRoZWlyIHJlc3BlY3RpdmVcbiAgLy8gYXJjaGl0ZWN0dXJlIGluaXRpYWxpemF0aW9uIGZ1bmN0aW9uLlxuICAvLyBSZWZlcmVuY2U6XG4gIC8vIGh0dHA6Ly9zb3VyY2V3YXJlLm9yZy9iaW51dGlscy9kb2NzL2FzL1BzZXVkby1PcHMuaHRtbCNQc2V1ZG8tT3BzXG4gIHZhciBkaXJlY3RpdmVzID0ge1xuICAgIFwiLmFib3J0XCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLmFsaWduXCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLmFsdG1hY3JvXCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLmFzY2lpXCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLmFzY2l6XCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLmJhbGlnblwiOiBcImJ1aWx0aW5cIixcbiAgICBcIi5iYWxpZ253XCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLmJhbGlnbmxcIjogXCJidWlsdGluXCIsXG4gICAgXCIuYnVuZGxlX2FsaWduX21vZGVcIjogXCJidWlsdGluXCIsXG4gICAgXCIuYnVuZGxlX2xvY2tcIjogXCJidWlsdGluXCIsXG4gICAgXCIuYnVuZGxlX3VubG9ja1wiOiBcImJ1aWx0aW5cIixcbiAgICBcIi5ieXRlXCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLmNmaV9zdGFydHByb2NcIjogXCJidWlsdGluXCIsXG4gICAgXCIuY29tbVwiOiBcImJ1aWx0aW5cIixcbiAgICBcIi5kYXRhXCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLmRlZlwiOiBcImJ1aWx0aW5cIixcbiAgICBcIi5kZXNjXCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLmRpbVwiOiBcImJ1aWx0aW5cIixcbiAgICBcIi5kb3VibGVcIjogXCJidWlsdGluXCIsXG4gICAgXCIuZWplY3RcIjogXCJidWlsdGluXCIsXG4gICAgXCIuZWxzZVwiOiBcImJ1aWx0aW5cIixcbiAgICBcIi5lbHNlaWZcIjogXCJidWlsdGluXCIsXG4gICAgXCIuZW5kXCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLmVuZGVmXCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLmVuZGZ1bmNcIjogXCJidWlsdGluXCIsXG4gICAgXCIuZW5kaWZcIjogXCJidWlsdGluXCIsXG4gICAgXCIuZXF1XCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLmVxdWl2XCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLmVxdlwiOiBcImJ1aWx0aW5cIixcbiAgICBcIi5lcnJcIjogXCJidWlsdGluXCIsXG4gICAgXCIuZXJyb3JcIjogXCJidWlsdGluXCIsXG4gICAgXCIuZXhpdG1cIjogXCJidWlsdGluXCIsXG4gICAgXCIuZXh0ZXJuXCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLmZhaWxcIjogXCJidWlsdGluXCIsXG4gICAgXCIuZmlsZVwiOiBcImJ1aWx0aW5cIixcbiAgICBcIi5maWxsXCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLmZsb2F0XCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLmZ1bmNcIjogXCJidWlsdGluXCIsXG4gICAgXCIuZ2xvYmFsXCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLmdudV9hdHRyaWJ1dGVcIjogXCJidWlsdGluXCIsXG4gICAgXCIuaGlkZGVuXCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLmh3b3JkXCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLmlkZW50XCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLmlmXCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLmluY2JpblwiOiBcImJ1aWx0aW5cIixcbiAgICBcIi5pbmNsdWRlXCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLmludFwiOiBcImJ1aWx0aW5cIixcbiAgICBcIi5pbnRlcm5hbFwiOiBcImJ1aWx0aW5cIixcbiAgICBcIi5pcnBcIjogXCJidWlsdGluXCIsXG4gICAgXCIuaXJwY1wiOiBcImJ1aWx0aW5cIixcbiAgICBcIi5sY29tbVwiOiBcImJ1aWx0aW5cIixcbiAgICBcIi5sZmxhZ3NcIjogXCJidWlsdGluXCIsXG4gICAgXCIubGluZVwiOiBcImJ1aWx0aW5cIixcbiAgICBcIi5saW5rb25jZVwiOiBcImJ1aWx0aW5cIixcbiAgICBcIi5saXN0XCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLmxuXCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLmxvY1wiOiBcImJ1aWx0aW5cIixcbiAgICBcIi5sb2NfbWFya19sYWJlbHNcIjogXCJidWlsdGluXCIsXG4gICAgXCIubG9jYWxcIjogXCJidWlsdGluXCIsXG4gICAgXCIubG9uZ1wiOiBcImJ1aWx0aW5cIixcbiAgICBcIi5tYWNyb1wiOiBcImJ1aWx0aW5cIixcbiAgICBcIi5tcmlcIjogXCJidWlsdGluXCIsXG4gICAgXCIubm9hbHRtYWNyb1wiOiBcImJ1aWx0aW5cIixcbiAgICBcIi5ub2xpc3RcIjogXCJidWlsdGluXCIsXG4gICAgXCIub2N0YVwiOiBcImJ1aWx0aW5cIixcbiAgICBcIi5vZmZzZXRcIjogXCJidWlsdGluXCIsXG4gICAgXCIub3JnXCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLnAyYWxpZ25cIjogXCJidWlsdGluXCIsXG4gICAgXCIucG9wc2VjdGlvblwiOiBcImJ1aWx0aW5cIixcbiAgICBcIi5wcmV2aW91c1wiOiBcImJ1aWx0aW5cIixcbiAgICBcIi5wcmludFwiOiBcImJ1aWx0aW5cIixcbiAgICBcIi5wcm90ZWN0ZWRcIjogXCJidWlsdGluXCIsXG4gICAgXCIucHNpemVcIjogXCJidWlsdGluXCIsXG4gICAgXCIucHVyZ2VtXCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLnB1c2hzZWN0aW9uXCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLnF1YWRcIjogXCJidWlsdGluXCIsXG4gICAgXCIucmVsb2NcIjogXCJidWlsdGluXCIsXG4gICAgXCIucmVwdFwiOiBcImJ1aWx0aW5cIixcbiAgICBcIi5zYnR0bFwiOiBcImJ1aWx0aW5cIixcbiAgICBcIi5zY2xcIjogXCJidWlsdGluXCIsXG4gICAgXCIuc2VjdGlvblwiOiBcImJ1aWx0aW5cIixcbiAgICBcIi5zZXRcIjogXCJidWlsdGluXCIsXG4gICAgXCIuc2hvcnRcIjogXCJidWlsdGluXCIsXG4gICAgXCIuc2luZ2xlXCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLnNpemVcIjogXCJidWlsdGluXCIsXG4gICAgXCIuc2tpcFwiOiBcImJ1aWx0aW5cIixcbiAgICBcIi5zbGViMTI4XCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLnNwYWNlXCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLnN0YWJcIjogXCJidWlsdGluXCIsXG4gICAgXCIuc3RyaW5nXCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLnN0cnVjdFwiOiBcImJ1aWx0aW5cIixcbiAgICBcIi5zdWJzZWN0aW9uXCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLnN5bXZlclwiOiBcImJ1aWx0aW5cIixcbiAgICBcIi50YWdcIjogXCJidWlsdGluXCIsXG4gICAgXCIudGV4dFwiOiBcImJ1aWx0aW5cIixcbiAgICBcIi50aXRsZVwiOiBcImJ1aWx0aW5cIixcbiAgICBcIi50eXBlXCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLnVsZWIxMjhcIjogXCJidWlsdGluXCIsXG4gICAgXCIudmFsXCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLnZlcnNpb25cIjogXCJidWlsdGluXCIsXG4gICAgXCIudnRhYmxlX2VudHJ5XCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLnZ0YWJsZV9pbmhlcml0XCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLndhcm5pbmdcIjogXCJidWlsdGluXCIsXG4gICAgXCIud2Vha1wiOiBcImJ1aWx0aW5cIixcbiAgICBcIi53ZWFrcmVmXCI6IFwiYnVpbHRpblwiLFxuICAgIFwiLndvcmRcIjogXCJidWlsdGluXCJcbiAgfTtcbiAgdmFyIHJlZ2lzdGVycyA9IHt9O1xuICBmdW5jdGlvbiB4ODYoKSB7XG4gICAgbGluZUNvbW1lbnRTdGFydFN5bWJvbCA9IFwiI1wiO1xuICAgIHJlZ2lzdGVycy5hbCA9IFwidmFyaWFibGVcIjtcbiAgICByZWdpc3RlcnMuYWggPSBcInZhcmlhYmxlXCI7XG4gICAgcmVnaXN0ZXJzLmF4ID0gXCJ2YXJpYWJsZVwiO1xuICAgIHJlZ2lzdGVycy5lYXggPSBcInZhcmlhYmxlTmFtZS5zcGVjaWFsXCI7XG4gICAgcmVnaXN0ZXJzLnJheCA9IFwidmFyaWFibGVOYW1lLnNwZWNpYWxcIjtcbiAgICByZWdpc3RlcnMuYmwgPSBcInZhcmlhYmxlXCI7XG4gICAgcmVnaXN0ZXJzLmJoID0gXCJ2YXJpYWJsZVwiO1xuICAgIHJlZ2lzdGVycy5ieCA9IFwidmFyaWFibGVcIjtcbiAgICByZWdpc3RlcnMuZWJ4ID0gXCJ2YXJpYWJsZU5hbWUuc3BlY2lhbFwiO1xuICAgIHJlZ2lzdGVycy5yYnggPSBcInZhcmlhYmxlTmFtZS5zcGVjaWFsXCI7XG4gICAgcmVnaXN0ZXJzLmNsID0gXCJ2YXJpYWJsZVwiO1xuICAgIHJlZ2lzdGVycy5jaCA9IFwidmFyaWFibGVcIjtcbiAgICByZWdpc3RlcnMuY3ggPSBcInZhcmlhYmxlXCI7XG4gICAgcmVnaXN0ZXJzLmVjeCA9IFwidmFyaWFibGVOYW1lLnNwZWNpYWxcIjtcbiAgICByZWdpc3RlcnMucmN4ID0gXCJ2YXJpYWJsZU5hbWUuc3BlY2lhbFwiO1xuICAgIHJlZ2lzdGVycy5kbCA9IFwidmFyaWFibGVcIjtcbiAgICByZWdpc3RlcnMuZGggPSBcInZhcmlhYmxlXCI7XG4gICAgcmVnaXN0ZXJzLmR4ID0gXCJ2YXJpYWJsZVwiO1xuICAgIHJlZ2lzdGVycy5lZHggPSBcInZhcmlhYmxlTmFtZS5zcGVjaWFsXCI7XG4gICAgcmVnaXN0ZXJzLnJkeCA9IFwidmFyaWFibGVOYW1lLnNwZWNpYWxcIjtcbiAgICByZWdpc3RlcnMuc2kgPSBcInZhcmlhYmxlXCI7XG4gICAgcmVnaXN0ZXJzLmVzaSA9IFwidmFyaWFibGVOYW1lLnNwZWNpYWxcIjtcbiAgICByZWdpc3RlcnMucnNpID0gXCJ2YXJpYWJsZU5hbWUuc3BlY2lhbFwiO1xuICAgIHJlZ2lzdGVycy5kaSA9IFwidmFyaWFibGVcIjtcbiAgICByZWdpc3RlcnMuZWRpID0gXCJ2YXJpYWJsZU5hbWUuc3BlY2lhbFwiO1xuICAgIHJlZ2lzdGVycy5yZGkgPSBcInZhcmlhYmxlTmFtZS5zcGVjaWFsXCI7XG4gICAgcmVnaXN0ZXJzLnNwID0gXCJ2YXJpYWJsZVwiO1xuICAgIHJlZ2lzdGVycy5lc3AgPSBcInZhcmlhYmxlTmFtZS5zcGVjaWFsXCI7XG4gICAgcmVnaXN0ZXJzLnJzcCA9IFwidmFyaWFibGVOYW1lLnNwZWNpYWxcIjtcbiAgICByZWdpc3RlcnMuYnAgPSBcInZhcmlhYmxlXCI7XG4gICAgcmVnaXN0ZXJzLmVicCA9IFwidmFyaWFibGVOYW1lLnNwZWNpYWxcIjtcbiAgICByZWdpc3RlcnMucmJwID0gXCJ2YXJpYWJsZU5hbWUuc3BlY2lhbFwiO1xuICAgIHJlZ2lzdGVycy5pcCA9IFwidmFyaWFibGVcIjtcbiAgICByZWdpc3RlcnMuZWlwID0gXCJ2YXJpYWJsZU5hbWUuc3BlY2lhbFwiO1xuICAgIHJlZ2lzdGVycy5yaXAgPSBcInZhcmlhYmxlTmFtZS5zcGVjaWFsXCI7XG4gICAgcmVnaXN0ZXJzLmNzID0gXCJrZXl3b3JkXCI7XG4gICAgcmVnaXN0ZXJzLmRzID0gXCJrZXl3b3JkXCI7XG4gICAgcmVnaXN0ZXJzLnNzID0gXCJrZXl3b3JkXCI7XG4gICAgcmVnaXN0ZXJzLmVzID0gXCJrZXl3b3JkXCI7XG4gICAgcmVnaXN0ZXJzLmZzID0gXCJrZXl3b3JkXCI7XG4gICAgcmVnaXN0ZXJzLmdzID0gXCJrZXl3b3JkXCI7XG4gIH1cbiAgZnVuY3Rpb24gYXJtdjYoKSB7XG4gICAgLy8gUmVmZXJlbmNlOlxuICAgIC8vIGh0dHA6Ly9pbmZvY2VudGVyLmFybS5jb20vaGVscC90b3BpYy9jb20uYXJtLmRvYy5xcmMwMDAxbC9RUkMwMDAxX1VBTC5wZGZcbiAgICAvLyBodHRwOi8vaW5mb2NlbnRlci5hcm0uY29tL2hlbHAvdG9waWMvY29tLmFybS5kb2MuZGRpMDMwMWgvRERJMDMwMUhfYXJtMTE3Nmp6ZnNfcjBwN190cm0ucGRmXG4gICAgbGluZUNvbW1lbnRTdGFydFN5bWJvbCA9IFwiQFwiO1xuICAgIGRpcmVjdGl2ZXMuc3ludGF4ID0gXCJidWlsdGluXCI7XG4gICAgcmVnaXN0ZXJzLnIwID0gXCJ2YXJpYWJsZVwiO1xuICAgIHJlZ2lzdGVycy5yMSA9IFwidmFyaWFibGVcIjtcbiAgICByZWdpc3RlcnMucjIgPSBcInZhcmlhYmxlXCI7XG4gICAgcmVnaXN0ZXJzLnIzID0gXCJ2YXJpYWJsZVwiO1xuICAgIHJlZ2lzdGVycy5yNCA9IFwidmFyaWFibGVcIjtcbiAgICByZWdpc3RlcnMucjUgPSBcInZhcmlhYmxlXCI7XG4gICAgcmVnaXN0ZXJzLnI2ID0gXCJ2YXJpYWJsZVwiO1xuICAgIHJlZ2lzdGVycy5yNyA9IFwidmFyaWFibGVcIjtcbiAgICByZWdpc3RlcnMucjggPSBcInZhcmlhYmxlXCI7XG4gICAgcmVnaXN0ZXJzLnI5ID0gXCJ2YXJpYWJsZVwiO1xuICAgIHJlZ2lzdGVycy5yMTAgPSBcInZhcmlhYmxlXCI7XG4gICAgcmVnaXN0ZXJzLnIxMSA9IFwidmFyaWFibGVcIjtcbiAgICByZWdpc3RlcnMucjEyID0gXCJ2YXJpYWJsZVwiO1xuICAgIHJlZ2lzdGVycy5zcCA9IFwidmFyaWFibGVOYW1lLnNwZWNpYWxcIjtcbiAgICByZWdpc3RlcnMubHIgPSBcInZhcmlhYmxlTmFtZS5zcGVjaWFsXCI7XG4gICAgcmVnaXN0ZXJzLnBjID0gXCJ2YXJpYWJsZU5hbWUuc3BlY2lhbFwiO1xuICAgIHJlZ2lzdGVycy5yMTMgPSByZWdpc3RlcnMuc3A7XG4gICAgcmVnaXN0ZXJzLnIxNCA9IHJlZ2lzdGVycy5scjtcbiAgICByZWdpc3RlcnMucjE1ID0gcmVnaXN0ZXJzLnBjO1xuICAgIGN1c3RvbS5wdXNoKGZ1bmN0aW9uIChjaCwgc3RyZWFtKSB7XG4gICAgICBpZiAoY2ggPT09ICcjJykge1xuICAgICAgICBzdHJlYW0uZWF0V2hpbGUoL1xcdy8pO1xuICAgICAgICByZXR1cm4gXCJudW1iZXJcIjtcbiAgICAgIH1cbiAgICB9KTtcbiAgfVxuICBpZiAoYXJjaCA9PT0gXCJ4ODZcIikge1xuICAgIHg4NigpO1xuICB9IGVsc2UgaWYgKGFyY2ggPT09IFwiYXJtXCIgfHwgYXJjaCA9PT0gXCJhcm12NlwiKSB7XG4gICAgYXJtdjYoKTtcbiAgfVxuICBmdW5jdGlvbiBuZXh0VW50aWxVbmVzY2FwZWQoc3RyZWFtLCBlbmQpIHtcbiAgICB2YXIgZXNjYXBlZCA9IGZhbHNlLFxuICAgICAgbmV4dDtcbiAgICB3aGlsZSAoKG5leHQgPSBzdHJlYW0ubmV4dCgpKSAhPSBudWxsKSB7XG4gICAgICBpZiAobmV4dCA9PT0gZW5kICYmICFlc2NhcGVkKSB7XG4gICAgICAgIHJldHVybiBmYWxzZTtcbiAgICAgIH1cbiAgICAgIGVzY2FwZWQgPSAhZXNjYXBlZCAmJiBuZXh0ID09PSBcIlxcXFxcIjtcbiAgICB9XG4gICAgcmV0dXJuIGVzY2FwZWQ7XG4gIH1cbiAgZnVuY3Rpb24gY2xpa2VDb21tZW50KHN0cmVhbSwgc3RhdGUpIHtcbiAgICB2YXIgbWF5YmVFbmQgPSBmYWxzZSxcbiAgICAgIGNoO1xuICAgIHdoaWxlICgoY2ggPSBzdHJlYW0ubmV4dCgpKSAhPSBudWxsKSB7XG4gICAgICBpZiAoY2ggPT09IFwiL1wiICYmIG1heWJlRW5kKSB7XG4gICAgICAgIHN0YXRlLnRva2VuaXplID0gbnVsbDtcbiAgICAgICAgYnJlYWs7XG4gICAgICB9XG4gICAgICBtYXliZUVuZCA9IGNoID09PSBcIipcIjtcbiAgICB9XG4gICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICB9XG4gIHJldHVybiB7XG4gICAgbmFtZTogXCJnYXNcIixcbiAgICBzdGFydFN0YXRlOiBmdW5jdGlvbiAoKSB7XG4gICAgICByZXR1cm4ge1xuICAgICAgICB0b2tlbml6ZTogbnVsbFxuICAgICAgfTtcbiAgICB9LFxuICAgIHRva2VuOiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgICAgaWYgKHN0YXRlLnRva2VuaXplKSB7XG4gICAgICAgIHJldHVybiBzdGF0ZS50b2tlbml6ZShzdHJlYW0sIHN0YXRlKTtcbiAgICAgIH1cbiAgICAgIGlmIChzdHJlYW0uZWF0U3BhY2UoKSkge1xuICAgICAgICByZXR1cm4gbnVsbDtcbiAgICAgIH1cbiAgICAgIHZhciBzdHlsZSxcbiAgICAgICAgY3VyLFxuICAgICAgICBjaCA9IHN0cmVhbS5uZXh0KCk7XG4gICAgICBpZiAoY2ggPT09IFwiL1wiKSB7XG4gICAgICAgIGlmIChzdHJlYW0uZWF0KFwiKlwiKSkge1xuICAgICAgICAgIHN0YXRlLnRva2VuaXplID0gY2xpa2VDb21tZW50O1xuICAgICAgICAgIHJldHVybiBjbGlrZUNvbW1lbnQoc3RyZWFtLCBzdGF0ZSk7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICAgIGlmIChjaCA9PT0gbGluZUNvbW1lbnRTdGFydFN5bWJvbCkge1xuICAgICAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgICAgIHJldHVybiBcImNvbW1lbnRcIjtcbiAgICAgIH1cbiAgICAgIGlmIChjaCA9PT0gJ1wiJykge1xuICAgICAgICBuZXh0VW50aWxVbmVzY2FwZWQoc3RyZWFtLCAnXCInKTtcbiAgICAgICAgcmV0dXJuIFwic3RyaW5nXCI7XG4gICAgICB9XG4gICAgICBpZiAoY2ggPT09ICcuJykge1xuICAgICAgICBzdHJlYW0uZWF0V2hpbGUoL1xcdy8pO1xuICAgICAgICBjdXIgPSBzdHJlYW0uY3VycmVudCgpLnRvTG93ZXJDYXNlKCk7XG4gICAgICAgIHN0eWxlID0gZGlyZWN0aXZlc1tjdXJdO1xuICAgICAgICByZXR1cm4gc3R5bGUgfHwgbnVsbDtcbiAgICAgIH1cbiAgICAgIGlmIChjaCA9PT0gJz0nKSB7XG4gICAgICAgIHN0cmVhbS5lYXRXaGlsZSgvXFx3Lyk7XG4gICAgICAgIHJldHVybiBcInRhZ1wiO1xuICAgICAgfVxuICAgICAgaWYgKGNoID09PSAneycpIHtcbiAgICAgICAgcmV0dXJuIFwiYnJhY2tldFwiO1xuICAgICAgfVxuICAgICAgaWYgKGNoID09PSAnfScpIHtcbiAgICAgICAgcmV0dXJuIFwiYnJhY2tldFwiO1xuICAgICAgfVxuICAgICAgaWYgKC9cXGQvLnRlc3QoY2gpKSB7XG4gICAgICAgIGlmIChjaCA9PT0gXCIwXCIgJiYgc3RyZWFtLmVhdChcInhcIikpIHtcbiAgICAgICAgICBzdHJlYW0uZWF0V2hpbGUoL1swLTlhLWZBLUZdLyk7XG4gICAgICAgICAgcmV0dXJuIFwibnVtYmVyXCI7XG4gICAgICAgIH1cbiAgICAgICAgc3RyZWFtLmVhdFdoaWxlKC9cXGQvKTtcbiAgICAgICAgcmV0dXJuIFwibnVtYmVyXCI7XG4gICAgICB9XG4gICAgICBpZiAoL1xcdy8udGVzdChjaCkpIHtcbiAgICAgICAgc3RyZWFtLmVhdFdoaWxlKC9cXHcvKTtcbiAgICAgICAgaWYgKHN0cmVhbS5lYXQoXCI6XCIpKSB7XG4gICAgICAgICAgcmV0dXJuICd0YWcnO1xuICAgICAgICB9XG4gICAgICAgIGN1ciA9IHN0cmVhbS5jdXJyZW50KCkudG9Mb3dlckNhc2UoKTtcbiAgICAgICAgc3R5bGUgPSByZWdpc3RlcnNbY3VyXTtcbiAgICAgICAgcmV0dXJuIHN0eWxlIHx8IG51bGw7XG4gICAgICB9XG4gICAgICBmb3IgKHZhciBpID0gMDsgaSA8IGN1c3RvbS5sZW5ndGg7IGkrKykge1xuICAgICAgICBzdHlsZSA9IGN1c3RvbVtpXShjaCwgc3RyZWFtLCBzdGF0ZSk7XG4gICAgICAgIGlmIChzdHlsZSkge1xuICAgICAgICAgIHJldHVybiBzdHlsZTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH0sXG4gICAgbGFuZ3VhZ2VEYXRhOiB7XG4gICAgICBjb21tZW50VG9rZW5zOiB7XG4gICAgICAgIGxpbmU6IGxpbmVDb21tZW50U3RhcnRTeW1ib2wsXG4gICAgICAgIGJsb2NrOiB7XG4gICAgICAgICAgb3BlbjogXCIvKlwiLFxuICAgICAgICAgIGNsb3NlOiBcIiovXCJcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH1cbiAgfTtcbn1cbjtcbmV4cG9ydCBjb25zdCBnYXMgPSBta0dhcyhcIng4NlwiKTtcbmV4cG9ydCBjb25zdCBnYXNBcm0gPSBta0dhcyhcImFybVwiKTsiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=