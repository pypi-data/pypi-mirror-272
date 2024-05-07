"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[9018],{

/***/ 69018:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "mbox": () => (/* binding */ mbox)
/* harmony export */ });
var rfc2822 = ["From", "Sender", "Reply-To", "To", "Cc", "Bcc", "Message-ID", "In-Reply-To", "References", "Resent-From", "Resent-Sender", "Resent-To", "Resent-Cc", "Resent-Bcc", "Resent-Message-ID", "Return-Path", "Received"];
var rfc2822NoEmail = ["Date", "Subject", "Comments", "Keywords", "Resent-Date"];
var whitespace = /^[ \t]/;
var separator = /^From /; // See RFC 4155
var rfc2822Header = new RegExp("^(" + rfc2822.join("|") + "): ");
var rfc2822HeaderNoEmail = new RegExp("^(" + rfc2822NoEmail.join("|") + "): ");
var header = /^[^:]+:/; // Optional fields defined in RFC 2822
var email = /^[^ ]+@[^ ]+/;
var untilEmail = /^.*?(?=[^ ]+?@[^ ]+)/;
var bracketedEmail = /^<.*?>/;
var untilBracketedEmail = /^.*?(?=<.*>)/;
function styleForHeader(header) {
  if (header === "Subject") return "header";
  return "string";
}
function readToken(stream, state) {
  if (stream.sol()) {
    // From last line
    state.inSeparator = false;
    if (state.inHeader && stream.match(whitespace)) {
      // Header folding
      return null;
    } else {
      state.inHeader = false;
      state.header = null;
    }
    if (stream.match(separator)) {
      state.inHeaders = true;
      state.inSeparator = true;
      return "atom";
    }
    var match;
    var emailPermitted = false;
    if ((match = stream.match(rfc2822HeaderNoEmail)) || (emailPermitted = true) && (match = stream.match(rfc2822Header))) {
      state.inHeaders = true;
      state.inHeader = true;
      state.emailPermitted = emailPermitted;
      state.header = match[1];
      return "atom";
    }

    // Use vim's heuristics: recognize custom headers only if the line is in a
    // block of legitimate headers.
    if (state.inHeaders && (match = stream.match(header))) {
      state.inHeader = true;
      state.emailPermitted = true;
      state.header = match[1];
      return "atom";
    }
    state.inHeaders = false;
    stream.skipToEnd();
    return null;
  }
  if (state.inSeparator) {
    if (stream.match(email)) return "link";
    if (stream.match(untilEmail)) return "atom";
    stream.skipToEnd();
    return "atom";
  }
  if (state.inHeader) {
    var style = styleForHeader(state.header);
    if (state.emailPermitted) {
      if (stream.match(bracketedEmail)) return style + " link";
      if (stream.match(untilBracketedEmail)) return style;
    }
    stream.skipToEnd();
    return style;
  }
  stream.skipToEnd();
  return null;
}
;
const mbox = {
  name: "mbox",
  startState: function () {
    return {
      // Is in a mbox separator
      inSeparator: false,
      // Is in a mail header
      inHeader: false,
      // If bracketed email is permitted. Only applicable when inHeader
      emailPermitted: false,
      // Name of current header
      header: null,
      // Is in a region of mail headers
      inHeaders: false
    };
  },
  token: readToken,
  blankLine: function (state) {
    state.inHeaders = state.inSeparator = state.inHeader = false;
  },
  languageData: {
    autocomplete: rfc2822.concat(rfc2822NoEmail)
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiOTAxOC5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9AY29kZW1pcnJvci9sZWdhY3ktbW9kZXMvbW9kZS9tYm94LmpzIl0sInNvdXJjZXNDb250ZW50IjpbInZhciByZmMyODIyID0gW1wiRnJvbVwiLCBcIlNlbmRlclwiLCBcIlJlcGx5LVRvXCIsIFwiVG9cIiwgXCJDY1wiLCBcIkJjY1wiLCBcIk1lc3NhZ2UtSURcIiwgXCJJbi1SZXBseS1Ub1wiLCBcIlJlZmVyZW5jZXNcIiwgXCJSZXNlbnQtRnJvbVwiLCBcIlJlc2VudC1TZW5kZXJcIiwgXCJSZXNlbnQtVG9cIiwgXCJSZXNlbnQtQ2NcIiwgXCJSZXNlbnQtQmNjXCIsIFwiUmVzZW50LU1lc3NhZ2UtSURcIiwgXCJSZXR1cm4tUGF0aFwiLCBcIlJlY2VpdmVkXCJdO1xudmFyIHJmYzI4MjJOb0VtYWlsID0gW1wiRGF0ZVwiLCBcIlN1YmplY3RcIiwgXCJDb21tZW50c1wiLCBcIktleXdvcmRzXCIsIFwiUmVzZW50LURhdGVcIl07XG52YXIgd2hpdGVzcGFjZSA9IC9eWyBcXHRdLztcbnZhciBzZXBhcmF0b3IgPSAvXkZyb20gLzsgLy8gU2VlIFJGQyA0MTU1XG52YXIgcmZjMjgyMkhlYWRlciA9IG5ldyBSZWdFeHAoXCJeKFwiICsgcmZjMjgyMi5qb2luKFwifFwiKSArIFwiKTogXCIpO1xudmFyIHJmYzI4MjJIZWFkZXJOb0VtYWlsID0gbmV3IFJlZ0V4cChcIl4oXCIgKyByZmMyODIyTm9FbWFpbC5qb2luKFwifFwiKSArIFwiKTogXCIpO1xudmFyIGhlYWRlciA9IC9eW146XSs6LzsgLy8gT3B0aW9uYWwgZmllbGRzIGRlZmluZWQgaW4gUkZDIDI4MjJcbnZhciBlbWFpbCA9IC9eW14gXStAW14gXSsvO1xudmFyIHVudGlsRW1haWwgPSAvXi4qPyg/PVteIF0rP0BbXiBdKykvO1xudmFyIGJyYWNrZXRlZEVtYWlsID0gL148Lio/Pi87XG52YXIgdW50aWxCcmFja2V0ZWRFbWFpbCA9IC9eLio/KD89PC4qPikvO1xuZnVuY3Rpb24gc3R5bGVGb3JIZWFkZXIoaGVhZGVyKSB7XG4gIGlmIChoZWFkZXIgPT09IFwiU3ViamVjdFwiKSByZXR1cm4gXCJoZWFkZXJcIjtcbiAgcmV0dXJuIFwic3RyaW5nXCI7XG59XG5mdW5jdGlvbiByZWFkVG9rZW4oc3RyZWFtLCBzdGF0ZSkge1xuICBpZiAoc3RyZWFtLnNvbCgpKSB7XG4gICAgLy8gRnJvbSBsYXN0IGxpbmVcbiAgICBzdGF0ZS5pblNlcGFyYXRvciA9IGZhbHNlO1xuICAgIGlmIChzdGF0ZS5pbkhlYWRlciAmJiBzdHJlYW0ubWF0Y2god2hpdGVzcGFjZSkpIHtcbiAgICAgIC8vIEhlYWRlciBmb2xkaW5nXG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9IGVsc2Uge1xuICAgICAgc3RhdGUuaW5IZWFkZXIgPSBmYWxzZTtcbiAgICAgIHN0YXRlLmhlYWRlciA9IG51bGw7XG4gICAgfVxuICAgIGlmIChzdHJlYW0ubWF0Y2goc2VwYXJhdG9yKSkge1xuICAgICAgc3RhdGUuaW5IZWFkZXJzID0gdHJ1ZTtcbiAgICAgIHN0YXRlLmluU2VwYXJhdG9yID0gdHJ1ZTtcbiAgICAgIHJldHVybiBcImF0b21cIjtcbiAgICB9XG4gICAgdmFyIG1hdGNoO1xuICAgIHZhciBlbWFpbFBlcm1pdHRlZCA9IGZhbHNlO1xuICAgIGlmICgobWF0Y2ggPSBzdHJlYW0ubWF0Y2gocmZjMjgyMkhlYWRlck5vRW1haWwpKSB8fCAoZW1haWxQZXJtaXR0ZWQgPSB0cnVlKSAmJiAobWF0Y2ggPSBzdHJlYW0ubWF0Y2gocmZjMjgyMkhlYWRlcikpKSB7XG4gICAgICBzdGF0ZS5pbkhlYWRlcnMgPSB0cnVlO1xuICAgICAgc3RhdGUuaW5IZWFkZXIgPSB0cnVlO1xuICAgICAgc3RhdGUuZW1haWxQZXJtaXR0ZWQgPSBlbWFpbFBlcm1pdHRlZDtcbiAgICAgIHN0YXRlLmhlYWRlciA9IG1hdGNoWzFdO1xuICAgICAgcmV0dXJuIFwiYXRvbVwiO1xuICAgIH1cblxuICAgIC8vIFVzZSB2aW0ncyBoZXVyaXN0aWNzOiByZWNvZ25pemUgY3VzdG9tIGhlYWRlcnMgb25seSBpZiB0aGUgbGluZSBpcyBpbiBhXG4gICAgLy8gYmxvY2sgb2YgbGVnaXRpbWF0ZSBoZWFkZXJzLlxuICAgIGlmIChzdGF0ZS5pbkhlYWRlcnMgJiYgKG1hdGNoID0gc3RyZWFtLm1hdGNoKGhlYWRlcikpKSB7XG4gICAgICBzdGF0ZS5pbkhlYWRlciA9IHRydWU7XG4gICAgICBzdGF0ZS5lbWFpbFBlcm1pdHRlZCA9IHRydWU7XG4gICAgICBzdGF0ZS5oZWFkZXIgPSBtYXRjaFsxXTtcbiAgICAgIHJldHVybiBcImF0b21cIjtcbiAgICB9XG4gICAgc3RhdGUuaW5IZWFkZXJzID0gZmFsc2U7XG4gICAgc3RyZWFtLnNraXBUb0VuZCgpO1xuICAgIHJldHVybiBudWxsO1xuICB9XG4gIGlmIChzdGF0ZS5pblNlcGFyYXRvcikge1xuICAgIGlmIChzdHJlYW0ubWF0Y2goZW1haWwpKSByZXR1cm4gXCJsaW5rXCI7XG4gICAgaWYgKHN0cmVhbS5tYXRjaCh1bnRpbEVtYWlsKSkgcmV0dXJuIFwiYXRvbVwiO1xuICAgIHN0cmVhbS5za2lwVG9FbmQoKTtcbiAgICByZXR1cm4gXCJhdG9tXCI7XG4gIH1cbiAgaWYgKHN0YXRlLmluSGVhZGVyKSB7XG4gICAgdmFyIHN0eWxlID0gc3R5bGVGb3JIZWFkZXIoc3RhdGUuaGVhZGVyKTtcbiAgICBpZiAoc3RhdGUuZW1haWxQZXJtaXR0ZWQpIHtcbiAgICAgIGlmIChzdHJlYW0ubWF0Y2goYnJhY2tldGVkRW1haWwpKSByZXR1cm4gc3R5bGUgKyBcIiBsaW5rXCI7XG4gICAgICBpZiAoc3RyZWFtLm1hdGNoKHVudGlsQnJhY2tldGVkRW1haWwpKSByZXR1cm4gc3R5bGU7XG4gICAgfVxuICAgIHN0cmVhbS5za2lwVG9FbmQoKTtcbiAgICByZXR1cm4gc3R5bGU7XG4gIH1cbiAgc3RyZWFtLnNraXBUb0VuZCgpO1xuICByZXR1cm4gbnVsbDtcbn1cbjtcbmV4cG9ydCBjb25zdCBtYm94ID0ge1xuICBuYW1lOiBcIm1ib3hcIixcbiAgc3RhcnRTdGF0ZTogZnVuY3Rpb24gKCkge1xuICAgIHJldHVybiB7XG4gICAgICAvLyBJcyBpbiBhIG1ib3ggc2VwYXJhdG9yXG4gICAgICBpblNlcGFyYXRvcjogZmFsc2UsXG4gICAgICAvLyBJcyBpbiBhIG1haWwgaGVhZGVyXG4gICAgICBpbkhlYWRlcjogZmFsc2UsXG4gICAgICAvLyBJZiBicmFja2V0ZWQgZW1haWwgaXMgcGVybWl0dGVkLiBPbmx5IGFwcGxpY2FibGUgd2hlbiBpbkhlYWRlclxuICAgICAgZW1haWxQZXJtaXR0ZWQ6IGZhbHNlLFxuICAgICAgLy8gTmFtZSBvZiBjdXJyZW50IGhlYWRlclxuICAgICAgaGVhZGVyOiBudWxsLFxuICAgICAgLy8gSXMgaW4gYSByZWdpb24gb2YgbWFpbCBoZWFkZXJzXG4gICAgICBpbkhlYWRlcnM6IGZhbHNlXG4gICAgfTtcbiAgfSxcbiAgdG9rZW46IHJlYWRUb2tlbixcbiAgYmxhbmtMaW5lOiBmdW5jdGlvbiAoc3RhdGUpIHtcbiAgICBzdGF0ZS5pbkhlYWRlcnMgPSBzdGF0ZS5pblNlcGFyYXRvciA9IHN0YXRlLmluSGVhZGVyID0gZmFsc2U7XG4gIH0sXG4gIGxhbmd1YWdlRGF0YToge1xuICAgIGF1dG9jb21wbGV0ZTogcmZjMjgyMi5jb25jYXQocmZjMjgyMk5vRW1haWwpXG4gIH1cbn07Il0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9