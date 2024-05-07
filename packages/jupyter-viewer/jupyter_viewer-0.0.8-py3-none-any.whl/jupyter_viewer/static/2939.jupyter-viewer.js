"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[2939],{

/***/ 2939:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "mumps": () => (/* binding */ mumps)
/* harmony export */ });
function wordRegexp(words) {
  return new RegExp("^((" + words.join(")|(") + "))\\b", "i");
}
var singleOperators = new RegExp("^[\\+\\-\\*/&#!_?\\\\<>=\\'\\[\\]]");
var doubleOperators = new RegExp("^(('=)|(<=)|(>=)|('>)|('<)|([[)|(]])|(^$))");
var singleDelimiters = new RegExp("^[\\.,:]");
var brackets = new RegExp("[()]");
var identifiers = new RegExp("^[%A-Za-z][A-Za-z0-9]*");
var commandKeywords = ["break", "close", "do", "else", "for", "goto", "halt", "hang", "if", "job", "kill", "lock", "merge", "new", "open", "quit", "read", "set", "tcommit", "trollback", "tstart", "use", "view", "write", "xecute", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "q", "r", "s", "tc", "tro", "ts", "u", "v", "w", "x"];
// The following list includes intrinsic functions _and_ special variables
var intrinsicFuncsWords = ["\\$ascii", "\\$char", "\\$data", "\\$ecode", "\\$estack", "\\$etrap", "\\$extract", "\\$find", "\\$fnumber", "\\$get", "\\$horolog", "\\$io", "\\$increment", "\\$job", "\\$justify", "\\$length", "\\$name", "\\$next", "\\$order", "\\$piece", "\\$qlength", "\\$qsubscript", "\\$query", "\\$quit", "\\$random", "\\$reverse", "\\$select", "\\$stack", "\\$test", "\\$text", "\\$translate", "\\$view", "\\$x", "\\$y", "\\$a", "\\$c", "\\$d", "\\$e", "\\$ec", "\\$es", "\\$et", "\\$f", "\\$fn", "\\$g", "\\$h", "\\$i", "\\$j", "\\$l", "\\$n", "\\$na", "\\$o", "\\$p", "\\$q", "\\$ql", "\\$qs", "\\$r", "\\$re", "\\$s", "\\$st", "\\$t", "\\$tr", "\\$v", "\\$z"];
var intrinsicFuncs = wordRegexp(intrinsicFuncsWords);
var command = wordRegexp(commandKeywords);
function tokenBase(stream, state) {
  if (stream.sol()) {
    state.label = true;
    state.commandMode = 0;
  }

  // The <space> character has meaning in MUMPS. Ignoring consecutive
  // spaces would interfere with interpreting whether the next non-space
  // character belongs to the command or argument context.

  // Examine each character and update a mode variable whose interpretation is:
  //   >0 => command    0 => argument    <0 => command post-conditional
  var ch = stream.peek();
  if (ch == " " || ch == "\t") {
    // Pre-process <space>
    state.label = false;
    if (state.commandMode == 0) state.commandMode = 1;else if (state.commandMode < 0 || state.commandMode == 2) state.commandMode = 0;
  } else if (ch != "." && state.commandMode > 0) {
    if (ch == ":") state.commandMode = -1; // SIS - Command post-conditional
    else state.commandMode = 2;
  }

  // Do not color parameter list as line tag
  if (ch === "(" || ch === "\u0009") state.label = false;

  // MUMPS comment starts with ";"
  if (ch === ";") {
    stream.skipToEnd();
    return "comment";
  }

  // Number Literals // SIS/RLM - MUMPS permits canonic number followed by concatenate operator
  if (stream.match(/^[-+]?\d+(\.\d+)?([eE][-+]?\d+)?/)) return "number";

  // Handle Strings
  if (ch == '"') {
    if (stream.skipTo('"')) {
      stream.next();
      return "string";
    } else {
      stream.skipToEnd();
      return "error";
    }
  }

  // Handle operators and Delimiters
  if (stream.match(doubleOperators) || stream.match(singleOperators)) return "operator";

  // Prevents leading "." in DO block from falling through to error
  if (stream.match(singleDelimiters)) return null;
  if (brackets.test(ch)) {
    stream.next();
    return "bracket";
  }
  if (state.commandMode > 0 && stream.match(command)) return "controlKeyword";
  if (stream.match(intrinsicFuncs)) return "builtin";
  if (stream.match(identifiers)) return "variable";

  // Detect dollar-sign when not a documented intrinsic function
  // "^" may introduce a GVN or SSVN - Color same as function
  if (ch === "$" || ch === "^") {
    stream.next();
    return "builtin";
  }

  // MUMPS Indirection
  if (ch === "@") {
    stream.next();
    return "string.special";
  }
  if (/[\w%]/.test(ch)) {
    stream.eatWhile(/[\w%]/);
    return "variable";
  }

  // Handle non-detected items
  stream.next();
  return "error";
}
const mumps = {
  name: "mumps",
  startState: function () {
    return {
      label: false,
      commandMode: 0
    };
  },
  token: function (stream, state) {
    var style = tokenBase(stream, state);
    if (state.label) return "tag";
    return style;
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiMjkzOS5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL0Bjb2RlbWlycm9yL2xlZ2FjeS1tb2Rlcy9tb2RlL211bXBzLmpzIl0sInNvdXJjZXNDb250ZW50IjpbImZ1bmN0aW9uIHdvcmRSZWdleHAod29yZHMpIHtcbiAgcmV0dXJuIG5ldyBSZWdFeHAoXCJeKChcIiArIHdvcmRzLmpvaW4oXCIpfChcIikgKyBcIikpXFxcXGJcIiwgXCJpXCIpO1xufVxudmFyIHNpbmdsZU9wZXJhdG9ycyA9IG5ldyBSZWdFeHAoXCJeW1xcXFwrXFxcXC1cXFxcKi8mIyFfP1xcXFxcXFxcPD49XFxcXCdcXFxcW1xcXFxdXVwiKTtcbnZhciBkb3VibGVPcGVyYXRvcnMgPSBuZXcgUmVnRXhwKFwiXigoJz0pfCg8PSl8KD49KXwoJz4pfCgnPCl8KFtbKXwoXV0pfCheJCkpXCIpO1xudmFyIHNpbmdsZURlbGltaXRlcnMgPSBuZXcgUmVnRXhwKFwiXltcXFxcLiw6XVwiKTtcbnZhciBicmFja2V0cyA9IG5ldyBSZWdFeHAoXCJbKCldXCIpO1xudmFyIGlkZW50aWZpZXJzID0gbmV3IFJlZ0V4cChcIl5bJUEtWmEtel1bQS1aYS16MC05XSpcIik7XG52YXIgY29tbWFuZEtleXdvcmRzID0gW1wiYnJlYWtcIiwgXCJjbG9zZVwiLCBcImRvXCIsIFwiZWxzZVwiLCBcImZvclwiLCBcImdvdG9cIiwgXCJoYWx0XCIsIFwiaGFuZ1wiLCBcImlmXCIsIFwiam9iXCIsIFwia2lsbFwiLCBcImxvY2tcIiwgXCJtZXJnZVwiLCBcIm5ld1wiLCBcIm9wZW5cIiwgXCJxdWl0XCIsIFwicmVhZFwiLCBcInNldFwiLCBcInRjb21taXRcIiwgXCJ0cm9sbGJhY2tcIiwgXCJ0c3RhcnRcIiwgXCJ1c2VcIiwgXCJ2aWV3XCIsIFwid3JpdGVcIiwgXCJ4ZWN1dGVcIiwgXCJiXCIsIFwiY1wiLCBcImRcIiwgXCJlXCIsIFwiZlwiLCBcImdcIiwgXCJoXCIsIFwiaVwiLCBcImpcIiwgXCJrXCIsIFwibFwiLCBcIm1cIiwgXCJuXCIsIFwib1wiLCBcInFcIiwgXCJyXCIsIFwic1wiLCBcInRjXCIsIFwidHJvXCIsIFwidHNcIiwgXCJ1XCIsIFwidlwiLCBcIndcIiwgXCJ4XCJdO1xuLy8gVGhlIGZvbGxvd2luZyBsaXN0IGluY2x1ZGVzIGludHJpbnNpYyBmdW5jdGlvbnMgX2FuZF8gc3BlY2lhbCB2YXJpYWJsZXNcbnZhciBpbnRyaW5zaWNGdW5jc1dvcmRzID0gW1wiXFxcXCRhc2NpaVwiLCBcIlxcXFwkY2hhclwiLCBcIlxcXFwkZGF0YVwiLCBcIlxcXFwkZWNvZGVcIiwgXCJcXFxcJGVzdGFja1wiLCBcIlxcXFwkZXRyYXBcIiwgXCJcXFxcJGV4dHJhY3RcIiwgXCJcXFxcJGZpbmRcIiwgXCJcXFxcJGZudW1iZXJcIiwgXCJcXFxcJGdldFwiLCBcIlxcXFwkaG9yb2xvZ1wiLCBcIlxcXFwkaW9cIiwgXCJcXFxcJGluY3JlbWVudFwiLCBcIlxcXFwkam9iXCIsIFwiXFxcXCRqdXN0aWZ5XCIsIFwiXFxcXCRsZW5ndGhcIiwgXCJcXFxcJG5hbWVcIiwgXCJcXFxcJG5leHRcIiwgXCJcXFxcJG9yZGVyXCIsIFwiXFxcXCRwaWVjZVwiLCBcIlxcXFwkcWxlbmd0aFwiLCBcIlxcXFwkcXN1YnNjcmlwdFwiLCBcIlxcXFwkcXVlcnlcIiwgXCJcXFxcJHF1aXRcIiwgXCJcXFxcJHJhbmRvbVwiLCBcIlxcXFwkcmV2ZXJzZVwiLCBcIlxcXFwkc2VsZWN0XCIsIFwiXFxcXCRzdGFja1wiLCBcIlxcXFwkdGVzdFwiLCBcIlxcXFwkdGV4dFwiLCBcIlxcXFwkdHJhbnNsYXRlXCIsIFwiXFxcXCR2aWV3XCIsIFwiXFxcXCR4XCIsIFwiXFxcXCR5XCIsIFwiXFxcXCRhXCIsIFwiXFxcXCRjXCIsIFwiXFxcXCRkXCIsIFwiXFxcXCRlXCIsIFwiXFxcXCRlY1wiLCBcIlxcXFwkZXNcIiwgXCJcXFxcJGV0XCIsIFwiXFxcXCRmXCIsIFwiXFxcXCRmblwiLCBcIlxcXFwkZ1wiLCBcIlxcXFwkaFwiLCBcIlxcXFwkaVwiLCBcIlxcXFwkalwiLCBcIlxcXFwkbFwiLCBcIlxcXFwkblwiLCBcIlxcXFwkbmFcIiwgXCJcXFxcJG9cIiwgXCJcXFxcJHBcIiwgXCJcXFxcJHFcIiwgXCJcXFxcJHFsXCIsIFwiXFxcXCRxc1wiLCBcIlxcXFwkclwiLCBcIlxcXFwkcmVcIiwgXCJcXFxcJHNcIiwgXCJcXFxcJHN0XCIsIFwiXFxcXCR0XCIsIFwiXFxcXCR0clwiLCBcIlxcXFwkdlwiLCBcIlxcXFwkelwiXTtcbnZhciBpbnRyaW5zaWNGdW5jcyA9IHdvcmRSZWdleHAoaW50cmluc2ljRnVuY3NXb3Jkcyk7XG52YXIgY29tbWFuZCA9IHdvcmRSZWdleHAoY29tbWFuZEtleXdvcmRzKTtcbmZ1bmN0aW9uIHRva2VuQmFzZShzdHJlYW0sIHN0YXRlKSB7XG4gIGlmIChzdHJlYW0uc29sKCkpIHtcbiAgICBzdGF0ZS5sYWJlbCA9IHRydWU7XG4gICAgc3RhdGUuY29tbWFuZE1vZGUgPSAwO1xuICB9XG5cbiAgLy8gVGhlIDxzcGFjZT4gY2hhcmFjdGVyIGhhcyBtZWFuaW5nIGluIE1VTVBTLiBJZ25vcmluZyBjb25zZWN1dGl2ZVxuICAvLyBzcGFjZXMgd291bGQgaW50ZXJmZXJlIHdpdGggaW50ZXJwcmV0aW5nIHdoZXRoZXIgdGhlIG5leHQgbm9uLXNwYWNlXG4gIC8vIGNoYXJhY3RlciBiZWxvbmdzIHRvIHRoZSBjb21tYW5kIG9yIGFyZ3VtZW50IGNvbnRleHQuXG5cbiAgLy8gRXhhbWluZSBlYWNoIGNoYXJhY3RlciBhbmQgdXBkYXRlIGEgbW9kZSB2YXJpYWJsZSB3aG9zZSBpbnRlcnByZXRhdGlvbiBpczpcbiAgLy8gICA+MCA9PiBjb21tYW5kICAgIDAgPT4gYXJndW1lbnQgICAgPDAgPT4gY29tbWFuZCBwb3N0LWNvbmRpdGlvbmFsXG4gIHZhciBjaCA9IHN0cmVhbS5wZWVrKCk7XG4gIGlmIChjaCA9PSBcIiBcIiB8fCBjaCA9PSBcIlxcdFwiKSB7XG4gICAgLy8gUHJlLXByb2Nlc3MgPHNwYWNlPlxuICAgIHN0YXRlLmxhYmVsID0gZmFsc2U7XG4gICAgaWYgKHN0YXRlLmNvbW1hbmRNb2RlID09IDApIHN0YXRlLmNvbW1hbmRNb2RlID0gMTtlbHNlIGlmIChzdGF0ZS5jb21tYW5kTW9kZSA8IDAgfHwgc3RhdGUuY29tbWFuZE1vZGUgPT0gMikgc3RhdGUuY29tbWFuZE1vZGUgPSAwO1xuICB9IGVsc2UgaWYgKGNoICE9IFwiLlwiICYmIHN0YXRlLmNvbW1hbmRNb2RlID4gMCkge1xuICAgIGlmIChjaCA9PSBcIjpcIikgc3RhdGUuY29tbWFuZE1vZGUgPSAtMTsgLy8gU0lTIC0gQ29tbWFuZCBwb3N0LWNvbmRpdGlvbmFsXG4gICAgZWxzZSBzdGF0ZS5jb21tYW5kTW9kZSA9IDI7XG4gIH1cblxuICAvLyBEbyBub3QgY29sb3IgcGFyYW1ldGVyIGxpc3QgYXMgbGluZSB0YWdcbiAgaWYgKGNoID09PSBcIihcIiB8fCBjaCA9PT0gXCJcXHUwMDA5XCIpIHN0YXRlLmxhYmVsID0gZmFsc2U7XG5cbiAgLy8gTVVNUFMgY29tbWVudCBzdGFydHMgd2l0aCBcIjtcIlxuICBpZiAoY2ggPT09IFwiO1wiKSB7XG4gICAgc3RyZWFtLnNraXBUb0VuZCgpO1xuICAgIHJldHVybiBcImNvbW1lbnRcIjtcbiAgfVxuXG4gIC8vIE51bWJlciBMaXRlcmFscyAvLyBTSVMvUkxNIC0gTVVNUFMgcGVybWl0cyBjYW5vbmljIG51bWJlciBmb2xsb3dlZCBieSBjb25jYXRlbmF0ZSBvcGVyYXRvclxuICBpZiAoc3RyZWFtLm1hdGNoKC9eWy0rXT9cXGQrKFxcLlxcZCspPyhbZUVdWy0rXT9cXGQrKT8vKSkgcmV0dXJuIFwibnVtYmVyXCI7XG5cbiAgLy8gSGFuZGxlIFN0cmluZ3NcbiAgaWYgKGNoID09ICdcIicpIHtcbiAgICBpZiAoc3RyZWFtLnNraXBUbygnXCInKSkge1xuICAgICAgc3RyZWFtLm5leHQoKTtcbiAgICAgIHJldHVybiBcInN0cmluZ1wiO1xuICAgIH0gZWxzZSB7XG4gICAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgICByZXR1cm4gXCJlcnJvclwiO1xuICAgIH1cbiAgfVxuXG4gIC8vIEhhbmRsZSBvcGVyYXRvcnMgYW5kIERlbGltaXRlcnNcbiAgaWYgKHN0cmVhbS5tYXRjaChkb3VibGVPcGVyYXRvcnMpIHx8IHN0cmVhbS5tYXRjaChzaW5nbGVPcGVyYXRvcnMpKSByZXR1cm4gXCJvcGVyYXRvclwiO1xuXG4gIC8vIFByZXZlbnRzIGxlYWRpbmcgXCIuXCIgaW4gRE8gYmxvY2sgZnJvbSBmYWxsaW5nIHRocm91Z2ggdG8gZXJyb3JcbiAgaWYgKHN0cmVhbS5tYXRjaChzaW5nbGVEZWxpbWl0ZXJzKSkgcmV0dXJuIG51bGw7XG4gIGlmIChicmFja2V0cy50ZXN0KGNoKSkge1xuICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgcmV0dXJuIFwiYnJhY2tldFwiO1xuICB9XG4gIGlmIChzdGF0ZS5jb21tYW5kTW9kZSA+IDAgJiYgc3RyZWFtLm1hdGNoKGNvbW1hbmQpKSByZXR1cm4gXCJjb250cm9sS2V5d29yZFwiO1xuICBpZiAoc3RyZWFtLm1hdGNoKGludHJpbnNpY0Z1bmNzKSkgcmV0dXJuIFwiYnVpbHRpblwiO1xuICBpZiAoc3RyZWFtLm1hdGNoKGlkZW50aWZpZXJzKSkgcmV0dXJuIFwidmFyaWFibGVcIjtcblxuICAvLyBEZXRlY3QgZG9sbGFyLXNpZ24gd2hlbiBub3QgYSBkb2N1bWVudGVkIGludHJpbnNpYyBmdW5jdGlvblxuICAvLyBcIl5cIiBtYXkgaW50cm9kdWNlIGEgR1ZOIG9yIFNTVk4gLSBDb2xvciBzYW1lIGFzIGZ1bmN0aW9uXG4gIGlmIChjaCA9PT0gXCIkXCIgfHwgY2ggPT09IFwiXlwiKSB7XG4gICAgc3RyZWFtLm5leHQoKTtcbiAgICByZXR1cm4gXCJidWlsdGluXCI7XG4gIH1cblxuICAvLyBNVU1QUyBJbmRpcmVjdGlvblxuICBpZiAoY2ggPT09IFwiQFwiKSB7XG4gICAgc3RyZWFtLm5leHQoKTtcbiAgICByZXR1cm4gXCJzdHJpbmcuc3BlY2lhbFwiO1xuICB9XG4gIGlmICgvW1xcdyVdLy50ZXN0KGNoKSkge1xuICAgIHN0cmVhbS5lYXRXaGlsZSgvW1xcdyVdLyk7XG4gICAgcmV0dXJuIFwidmFyaWFibGVcIjtcbiAgfVxuXG4gIC8vIEhhbmRsZSBub24tZGV0ZWN0ZWQgaXRlbXNcbiAgc3RyZWFtLm5leHQoKTtcbiAgcmV0dXJuIFwiZXJyb3JcIjtcbn1cbmV4cG9ydCBjb25zdCBtdW1wcyA9IHtcbiAgbmFtZTogXCJtdW1wc1wiLFxuICBzdGFydFN0YXRlOiBmdW5jdGlvbiAoKSB7XG4gICAgcmV0dXJuIHtcbiAgICAgIGxhYmVsOiBmYWxzZSxcbiAgICAgIGNvbW1hbmRNb2RlOiAwXG4gICAgfTtcbiAgfSxcbiAgdG9rZW46IGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgdmFyIHN0eWxlID0gdG9rZW5CYXNlKHN0cmVhbSwgc3RhdGUpO1xuICAgIGlmIChzdGF0ZS5sYWJlbCkgcmV0dXJuIFwidGFnXCI7XG4gICAgcmV0dXJuIHN0eWxlO1xuICB9XG59OyJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==