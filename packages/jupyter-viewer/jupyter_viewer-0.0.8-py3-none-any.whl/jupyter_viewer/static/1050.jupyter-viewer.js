"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[1050],{

/***/ 51050:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ntriples": () => (/* binding */ ntriples)
/* harmony export */ });
var Location = {
  PRE_SUBJECT: 0,
  WRITING_SUB_URI: 1,
  WRITING_BNODE_URI: 2,
  PRE_PRED: 3,
  WRITING_PRED_URI: 4,
  PRE_OBJ: 5,
  WRITING_OBJ_URI: 6,
  WRITING_OBJ_BNODE: 7,
  WRITING_OBJ_LITERAL: 8,
  WRITING_LIT_LANG: 9,
  WRITING_LIT_TYPE: 10,
  POST_OBJ: 11,
  ERROR: 12
};
function transitState(currState, c) {
  var currLocation = currState.location;
  var ret;

  // Opening.
  if (currLocation == Location.PRE_SUBJECT && c == '<') ret = Location.WRITING_SUB_URI;else if (currLocation == Location.PRE_SUBJECT && c == '_') ret = Location.WRITING_BNODE_URI;else if (currLocation == Location.PRE_PRED && c == '<') ret = Location.WRITING_PRED_URI;else if (currLocation == Location.PRE_OBJ && c == '<') ret = Location.WRITING_OBJ_URI;else if (currLocation == Location.PRE_OBJ && c == '_') ret = Location.WRITING_OBJ_BNODE;else if (currLocation == Location.PRE_OBJ && c == '"') ret = Location.WRITING_OBJ_LITERAL;

  // Closing.
  else if (currLocation == Location.WRITING_SUB_URI && c == '>') ret = Location.PRE_PRED;else if (currLocation == Location.WRITING_BNODE_URI && c == ' ') ret = Location.PRE_PRED;else if (currLocation == Location.WRITING_PRED_URI && c == '>') ret = Location.PRE_OBJ;else if (currLocation == Location.WRITING_OBJ_URI && c == '>') ret = Location.POST_OBJ;else if (currLocation == Location.WRITING_OBJ_BNODE && c == ' ') ret = Location.POST_OBJ;else if (currLocation == Location.WRITING_OBJ_LITERAL && c == '"') ret = Location.POST_OBJ;else if (currLocation == Location.WRITING_LIT_LANG && c == ' ') ret = Location.POST_OBJ;else if (currLocation == Location.WRITING_LIT_TYPE && c == '>') ret = Location.POST_OBJ;

  // Closing typed and language literal.
  else if (currLocation == Location.WRITING_OBJ_LITERAL && c == '@') ret = Location.WRITING_LIT_LANG;else if (currLocation == Location.WRITING_OBJ_LITERAL && c == '^') ret = Location.WRITING_LIT_TYPE;

  // Spaces.
  else if (c == ' ' && (currLocation == Location.PRE_SUBJECT || currLocation == Location.PRE_PRED || currLocation == Location.PRE_OBJ || currLocation == Location.POST_OBJ)) ret = currLocation;

  // Reset.
  else if (currLocation == Location.POST_OBJ && c == '.') ret = Location.PRE_SUBJECT;

  // Error
  else ret = Location.ERROR;
  currState.location = ret;
}
const ntriples = {
  name: "ntriples",
  startState: function () {
    return {
      location: Location.PRE_SUBJECT,
      uris: [],
      anchors: [],
      bnodes: [],
      langs: [],
      types: []
    };
  },
  token: function (stream, state) {
    var ch = stream.next();
    if (ch == '<') {
      transitState(state, ch);
      var parsedURI = '';
      stream.eatWhile(function (c) {
        if (c != '#' && c != '>') {
          parsedURI += c;
          return true;
        }
        return false;
      });
      state.uris.push(parsedURI);
      if (stream.match('#', false)) return 'variable';
      stream.next();
      transitState(state, '>');
      return 'variable';
    }
    if (ch == '#') {
      var parsedAnchor = '';
      stream.eatWhile(function (c) {
        if (c != '>' && c != ' ') {
          parsedAnchor += c;
          return true;
        }
        return false;
      });
      state.anchors.push(parsedAnchor);
      return 'url';
    }
    if (ch == '>') {
      transitState(state, '>');
      return 'variable';
    }
    if (ch == '_') {
      transitState(state, ch);
      var parsedBNode = '';
      stream.eatWhile(function (c) {
        if (c != ' ') {
          parsedBNode += c;
          return true;
        }
        return false;
      });
      state.bnodes.push(parsedBNode);
      stream.next();
      transitState(state, ' ');
      return 'builtin';
    }
    if (ch == '"') {
      transitState(state, ch);
      stream.eatWhile(function (c) {
        return c != '"';
      });
      stream.next();
      if (stream.peek() != '@' && stream.peek() != '^') {
        transitState(state, '"');
      }
      return 'string';
    }
    if (ch == '@') {
      transitState(state, '@');
      var parsedLang = '';
      stream.eatWhile(function (c) {
        if (c != ' ') {
          parsedLang += c;
          return true;
        }
        return false;
      });
      state.langs.push(parsedLang);
      stream.next();
      transitState(state, ' ');
      return 'string.special';
    }
    if (ch == '^') {
      stream.next();
      transitState(state, '^');
      var parsedType = '';
      stream.eatWhile(function (c) {
        if (c != '>') {
          parsedType += c;
          return true;
        }
        return false;
      });
      state.types.push(parsedType);
      stream.next();
      transitState(state, '>');
      return 'variable';
    }
    if (ch == ' ') {
      transitState(state, ch);
    }
    if (ch == '.') {
      transitState(state, ch);
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiMTA1MC5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGNvZGVtaXJyb3IvbGVnYWN5LW1vZGVzL21vZGUvbnRyaXBsZXMuanMiXSwic291cmNlc0NvbnRlbnQiOlsidmFyIExvY2F0aW9uID0ge1xuICBQUkVfU1VCSkVDVDogMCxcbiAgV1JJVElOR19TVUJfVVJJOiAxLFxuICBXUklUSU5HX0JOT0RFX1VSSTogMixcbiAgUFJFX1BSRUQ6IDMsXG4gIFdSSVRJTkdfUFJFRF9VUkk6IDQsXG4gIFBSRV9PQko6IDUsXG4gIFdSSVRJTkdfT0JKX1VSSTogNixcbiAgV1JJVElOR19PQkpfQk5PREU6IDcsXG4gIFdSSVRJTkdfT0JKX0xJVEVSQUw6IDgsXG4gIFdSSVRJTkdfTElUX0xBTkc6IDksXG4gIFdSSVRJTkdfTElUX1RZUEU6IDEwLFxuICBQT1NUX09CSjogMTEsXG4gIEVSUk9SOiAxMlxufTtcbmZ1bmN0aW9uIHRyYW5zaXRTdGF0ZShjdXJyU3RhdGUsIGMpIHtcbiAgdmFyIGN1cnJMb2NhdGlvbiA9IGN1cnJTdGF0ZS5sb2NhdGlvbjtcbiAgdmFyIHJldDtcblxuICAvLyBPcGVuaW5nLlxuICBpZiAoY3VyckxvY2F0aW9uID09IExvY2F0aW9uLlBSRV9TVUJKRUNUICYmIGMgPT0gJzwnKSByZXQgPSBMb2NhdGlvbi5XUklUSU5HX1NVQl9VUkk7ZWxzZSBpZiAoY3VyckxvY2F0aW9uID09IExvY2F0aW9uLlBSRV9TVUJKRUNUICYmIGMgPT0gJ18nKSByZXQgPSBMb2NhdGlvbi5XUklUSU5HX0JOT0RFX1VSSTtlbHNlIGlmIChjdXJyTG9jYXRpb24gPT0gTG9jYXRpb24uUFJFX1BSRUQgJiYgYyA9PSAnPCcpIHJldCA9IExvY2F0aW9uLldSSVRJTkdfUFJFRF9VUkk7ZWxzZSBpZiAoY3VyckxvY2F0aW9uID09IExvY2F0aW9uLlBSRV9PQkogJiYgYyA9PSAnPCcpIHJldCA9IExvY2F0aW9uLldSSVRJTkdfT0JKX1VSSTtlbHNlIGlmIChjdXJyTG9jYXRpb24gPT0gTG9jYXRpb24uUFJFX09CSiAmJiBjID09ICdfJykgcmV0ID0gTG9jYXRpb24uV1JJVElOR19PQkpfQk5PREU7ZWxzZSBpZiAoY3VyckxvY2F0aW9uID09IExvY2F0aW9uLlBSRV9PQkogJiYgYyA9PSAnXCInKSByZXQgPSBMb2NhdGlvbi5XUklUSU5HX09CSl9MSVRFUkFMO1xuXG4gIC8vIENsb3NpbmcuXG4gIGVsc2UgaWYgKGN1cnJMb2NhdGlvbiA9PSBMb2NhdGlvbi5XUklUSU5HX1NVQl9VUkkgJiYgYyA9PSAnPicpIHJldCA9IExvY2F0aW9uLlBSRV9QUkVEO2Vsc2UgaWYgKGN1cnJMb2NhdGlvbiA9PSBMb2NhdGlvbi5XUklUSU5HX0JOT0RFX1VSSSAmJiBjID09ICcgJykgcmV0ID0gTG9jYXRpb24uUFJFX1BSRUQ7ZWxzZSBpZiAoY3VyckxvY2F0aW9uID09IExvY2F0aW9uLldSSVRJTkdfUFJFRF9VUkkgJiYgYyA9PSAnPicpIHJldCA9IExvY2F0aW9uLlBSRV9PQko7ZWxzZSBpZiAoY3VyckxvY2F0aW9uID09IExvY2F0aW9uLldSSVRJTkdfT0JKX1VSSSAmJiBjID09ICc+JykgcmV0ID0gTG9jYXRpb24uUE9TVF9PQko7ZWxzZSBpZiAoY3VyckxvY2F0aW9uID09IExvY2F0aW9uLldSSVRJTkdfT0JKX0JOT0RFICYmIGMgPT0gJyAnKSByZXQgPSBMb2NhdGlvbi5QT1NUX09CSjtlbHNlIGlmIChjdXJyTG9jYXRpb24gPT0gTG9jYXRpb24uV1JJVElOR19PQkpfTElURVJBTCAmJiBjID09ICdcIicpIHJldCA9IExvY2F0aW9uLlBPU1RfT0JKO2Vsc2UgaWYgKGN1cnJMb2NhdGlvbiA9PSBMb2NhdGlvbi5XUklUSU5HX0xJVF9MQU5HICYmIGMgPT0gJyAnKSByZXQgPSBMb2NhdGlvbi5QT1NUX09CSjtlbHNlIGlmIChjdXJyTG9jYXRpb24gPT0gTG9jYXRpb24uV1JJVElOR19MSVRfVFlQRSAmJiBjID09ICc+JykgcmV0ID0gTG9jYXRpb24uUE9TVF9PQko7XG5cbiAgLy8gQ2xvc2luZyB0eXBlZCBhbmQgbGFuZ3VhZ2UgbGl0ZXJhbC5cbiAgZWxzZSBpZiAoY3VyckxvY2F0aW9uID09IExvY2F0aW9uLldSSVRJTkdfT0JKX0xJVEVSQUwgJiYgYyA9PSAnQCcpIHJldCA9IExvY2F0aW9uLldSSVRJTkdfTElUX0xBTkc7ZWxzZSBpZiAoY3VyckxvY2F0aW9uID09IExvY2F0aW9uLldSSVRJTkdfT0JKX0xJVEVSQUwgJiYgYyA9PSAnXicpIHJldCA9IExvY2F0aW9uLldSSVRJTkdfTElUX1RZUEU7XG5cbiAgLy8gU3BhY2VzLlxuICBlbHNlIGlmIChjID09ICcgJyAmJiAoY3VyckxvY2F0aW9uID09IExvY2F0aW9uLlBSRV9TVUJKRUNUIHx8IGN1cnJMb2NhdGlvbiA9PSBMb2NhdGlvbi5QUkVfUFJFRCB8fCBjdXJyTG9jYXRpb24gPT0gTG9jYXRpb24uUFJFX09CSiB8fCBjdXJyTG9jYXRpb24gPT0gTG9jYXRpb24uUE9TVF9PQkopKSByZXQgPSBjdXJyTG9jYXRpb247XG5cbiAgLy8gUmVzZXQuXG4gIGVsc2UgaWYgKGN1cnJMb2NhdGlvbiA9PSBMb2NhdGlvbi5QT1NUX09CSiAmJiBjID09ICcuJykgcmV0ID0gTG9jYXRpb24uUFJFX1NVQkpFQ1Q7XG5cbiAgLy8gRXJyb3JcbiAgZWxzZSByZXQgPSBMb2NhdGlvbi5FUlJPUjtcbiAgY3VyclN0YXRlLmxvY2F0aW9uID0gcmV0O1xufVxuZXhwb3J0IGNvbnN0IG50cmlwbGVzID0ge1xuICBuYW1lOiBcIm50cmlwbGVzXCIsXG4gIHN0YXJ0U3RhdGU6IGZ1bmN0aW9uICgpIHtcbiAgICByZXR1cm4ge1xuICAgICAgbG9jYXRpb246IExvY2F0aW9uLlBSRV9TVUJKRUNULFxuICAgICAgdXJpczogW10sXG4gICAgICBhbmNob3JzOiBbXSxcbiAgICAgIGJub2RlczogW10sXG4gICAgICBsYW5nczogW10sXG4gICAgICB0eXBlczogW11cbiAgICB9O1xuICB9LFxuICB0b2tlbjogZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICB2YXIgY2ggPSBzdHJlYW0ubmV4dCgpO1xuICAgIGlmIChjaCA9PSAnPCcpIHtcbiAgICAgIHRyYW5zaXRTdGF0ZShzdGF0ZSwgY2gpO1xuICAgICAgdmFyIHBhcnNlZFVSSSA9ICcnO1xuICAgICAgc3RyZWFtLmVhdFdoaWxlKGZ1bmN0aW9uIChjKSB7XG4gICAgICAgIGlmIChjICE9ICcjJyAmJiBjICE9ICc+Jykge1xuICAgICAgICAgIHBhcnNlZFVSSSArPSBjO1xuICAgICAgICAgIHJldHVybiB0cnVlO1xuICAgICAgICB9XG4gICAgICAgIHJldHVybiBmYWxzZTtcbiAgICAgIH0pO1xuICAgICAgc3RhdGUudXJpcy5wdXNoKHBhcnNlZFVSSSk7XG4gICAgICBpZiAoc3RyZWFtLm1hdGNoKCcjJywgZmFsc2UpKSByZXR1cm4gJ3ZhcmlhYmxlJztcbiAgICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgICB0cmFuc2l0U3RhdGUoc3RhdGUsICc+Jyk7XG4gICAgICByZXR1cm4gJ3ZhcmlhYmxlJztcbiAgICB9XG4gICAgaWYgKGNoID09ICcjJykge1xuICAgICAgdmFyIHBhcnNlZEFuY2hvciA9ICcnO1xuICAgICAgc3RyZWFtLmVhdFdoaWxlKGZ1bmN0aW9uIChjKSB7XG4gICAgICAgIGlmIChjICE9ICc+JyAmJiBjICE9ICcgJykge1xuICAgICAgICAgIHBhcnNlZEFuY2hvciArPSBjO1xuICAgICAgICAgIHJldHVybiB0cnVlO1xuICAgICAgICB9XG4gICAgICAgIHJldHVybiBmYWxzZTtcbiAgICAgIH0pO1xuICAgICAgc3RhdGUuYW5jaG9ycy5wdXNoKHBhcnNlZEFuY2hvcik7XG4gICAgICByZXR1cm4gJ3VybCc7XG4gICAgfVxuICAgIGlmIChjaCA9PSAnPicpIHtcbiAgICAgIHRyYW5zaXRTdGF0ZShzdGF0ZSwgJz4nKTtcbiAgICAgIHJldHVybiAndmFyaWFibGUnO1xuICAgIH1cbiAgICBpZiAoY2ggPT0gJ18nKSB7XG4gICAgICB0cmFuc2l0U3RhdGUoc3RhdGUsIGNoKTtcbiAgICAgIHZhciBwYXJzZWRCTm9kZSA9ICcnO1xuICAgICAgc3RyZWFtLmVhdFdoaWxlKGZ1bmN0aW9uIChjKSB7XG4gICAgICAgIGlmIChjICE9ICcgJykge1xuICAgICAgICAgIHBhcnNlZEJOb2RlICs9IGM7XG4gICAgICAgICAgcmV0dXJuIHRydWU7XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIGZhbHNlO1xuICAgICAgfSk7XG4gICAgICBzdGF0ZS5ibm9kZXMucHVzaChwYXJzZWRCTm9kZSk7XG4gICAgICBzdHJlYW0ubmV4dCgpO1xuICAgICAgdHJhbnNpdFN0YXRlKHN0YXRlLCAnICcpO1xuICAgICAgcmV0dXJuICdidWlsdGluJztcbiAgICB9XG4gICAgaWYgKGNoID09ICdcIicpIHtcbiAgICAgIHRyYW5zaXRTdGF0ZShzdGF0ZSwgY2gpO1xuICAgICAgc3RyZWFtLmVhdFdoaWxlKGZ1bmN0aW9uIChjKSB7XG4gICAgICAgIHJldHVybiBjICE9ICdcIic7XG4gICAgICB9KTtcbiAgICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgICBpZiAoc3RyZWFtLnBlZWsoKSAhPSAnQCcgJiYgc3RyZWFtLnBlZWsoKSAhPSAnXicpIHtcbiAgICAgICAgdHJhbnNpdFN0YXRlKHN0YXRlLCAnXCInKTtcbiAgICAgIH1cbiAgICAgIHJldHVybiAnc3RyaW5nJztcbiAgICB9XG4gICAgaWYgKGNoID09ICdAJykge1xuICAgICAgdHJhbnNpdFN0YXRlKHN0YXRlLCAnQCcpO1xuICAgICAgdmFyIHBhcnNlZExhbmcgPSAnJztcbiAgICAgIHN0cmVhbS5lYXRXaGlsZShmdW5jdGlvbiAoYykge1xuICAgICAgICBpZiAoYyAhPSAnICcpIHtcbiAgICAgICAgICBwYXJzZWRMYW5nICs9IGM7XG4gICAgICAgICAgcmV0dXJuIHRydWU7XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIGZhbHNlO1xuICAgICAgfSk7XG4gICAgICBzdGF0ZS5sYW5ncy5wdXNoKHBhcnNlZExhbmcpO1xuICAgICAgc3RyZWFtLm5leHQoKTtcbiAgICAgIHRyYW5zaXRTdGF0ZShzdGF0ZSwgJyAnKTtcbiAgICAgIHJldHVybiAnc3RyaW5nLnNwZWNpYWwnO1xuICAgIH1cbiAgICBpZiAoY2ggPT0gJ14nKSB7XG4gICAgICBzdHJlYW0ubmV4dCgpO1xuICAgICAgdHJhbnNpdFN0YXRlKHN0YXRlLCAnXicpO1xuICAgICAgdmFyIHBhcnNlZFR5cGUgPSAnJztcbiAgICAgIHN0cmVhbS5lYXRXaGlsZShmdW5jdGlvbiAoYykge1xuICAgICAgICBpZiAoYyAhPSAnPicpIHtcbiAgICAgICAgICBwYXJzZWRUeXBlICs9IGM7XG4gICAgICAgICAgcmV0dXJuIHRydWU7XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIGZhbHNlO1xuICAgICAgfSk7XG4gICAgICBzdGF0ZS50eXBlcy5wdXNoKHBhcnNlZFR5cGUpO1xuICAgICAgc3RyZWFtLm5leHQoKTtcbiAgICAgIHRyYW5zaXRTdGF0ZShzdGF0ZSwgJz4nKTtcbiAgICAgIHJldHVybiAndmFyaWFibGUnO1xuICAgIH1cbiAgICBpZiAoY2ggPT0gJyAnKSB7XG4gICAgICB0cmFuc2l0U3RhdGUoc3RhdGUsIGNoKTtcbiAgICB9XG4gICAgaWYgKGNoID09ICcuJykge1xuICAgICAgdHJhbnNpdFN0YXRlKHN0YXRlLCBjaCk7XG4gICAgfVxuICB9XG59OyJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==