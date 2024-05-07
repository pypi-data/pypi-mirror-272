"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[6049],{

/***/ 66049:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "webIDL": () => (/* binding */ webIDL)
/* harmony export */ });
function wordRegexp(words) {
  return new RegExp("^((" + words.join(")|(") + "))\\b");
}
;
var builtinArray = ["Clamp", "Constructor", "EnforceRange", "Exposed", "ImplicitThis", "Global", "PrimaryGlobal", "LegacyArrayClass", "LegacyUnenumerableNamedProperties", "LenientThis", "NamedConstructor", "NewObject", "NoInterfaceObject", "OverrideBuiltins", "PutForwards", "Replaceable", "SameObject", "TreatNonObjectAsNull", "TreatNullAs", "EmptyString", "Unforgeable", "Unscopeable"];
var builtins = wordRegexp(builtinArray);
var typeArray = ["unsigned", "short", "long",
// UnsignedIntegerType
"unrestricted", "float", "double",
// UnrestrictedFloatType
"boolean", "byte", "octet",
// Rest of PrimitiveType
"Promise",
// PromiseType
"ArrayBuffer", "DataView", "Int8Array", "Int16Array", "Int32Array", "Uint8Array", "Uint16Array", "Uint32Array", "Uint8ClampedArray", "Float32Array", "Float64Array",
// BufferRelatedType
"ByteString", "DOMString", "USVString", "sequence", "object", "RegExp", "Error", "DOMException", "FrozenArray",
// Rest of NonAnyType
"any",
// Rest of SingleType
"void" // Rest of ReturnType
];
var types = wordRegexp(typeArray);
var keywordArray = ["attribute", "callback", "const", "deleter", "dictionary", "enum", "getter", "implements", "inherit", "interface", "iterable", "legacycaller", "maplike", "partial", "required", "serializer", "setlike", "setter", "static", "stringifier", "typedef",
// ArgumentNameKeyword except
// "unrestricted"
"optional", "readonly", "or"];
var keywords = wordRegexp(keywordArray);
var atomArray = ["true", "false",
// BooleanLiteral
"Infinity", "NaN",
// FloatLiteral
"null" // Rest of ConstValue
];
var atoms = wordRegexp(atomArray);
var startDefArray = ["callback", "dictionary", "enum", "interface"];
var startDefs = wordRegexp(startDefArray);
var endDefArray = ["typedef"];
var endDefs = wordRegexp(endDefArray);
var singleOperators = /^[:<=>?]/;
var integers = /^-?([1-9][0-9]*|0[Xx][0-9A-Fa-f]+|0[0-7]*)/;
var floats = /^-?(([0-9]+\.[0-9]*|[0-9]*\.[0-9]+)([Ee][+-]?[0-9]+)?|[0-9]+[Ee][+-]?[0-9]+)/;
var identifiers = /^_?[A-Za-z][0-9A-Z_a-z-]*/;
var identifiersEnd = /^_?[A-Za-z][0-9A-Z_a-z-]*(?=\s*;)/;
var strings = /^"[^"]*"/;
var multilineComments = /^\/\*.*?\*\//;
var multilineCommentsStart = /^\/\*.*/;
var multilineCommentsEnd = /^.*?\*\//;
function readToken(stream, state) {
  // whitespace
  if (stream.eatSpace()) return null;

  // comment
  if (state.inComment) {
    if (stream.match(multilineCommentsEnd)) {
      state.inComment = false;
      return "comment";
    }
    stream.skipToEnd();
    return "comment";
  }
  if (stream.match("//")) {
    stream.skipToEnd();
    return "comment";
  }
  if (stream.match(multilineComments)) return "comment";
  if (stream.match(multilineCommentsStart)) {
    state.inComment = true;
    return "comment";
  }

  // integer and float
  if (stream.match(/^-?[0-9\.]/, false)) {
    if (stream.match(integers) || stream.match(floats)) return "number";
  }

  // string
  if (stream.match(strings)) return "string";

  // identifier
  if (state.startDef && stream.match(identifiers)) return "def";
  if (state.endDef && stream.match(identifiersEnd)) {
    state.endDef = false;
    return "def";
  }
  if (stream.match(keywords)) return "keyword";
  if (stream.match(types)) {
    var lastToken = state.lastToken;
    var nextToken = (stream.match(/^\s*(.+?)\b/, false) || [])[1];
    if (lastToken === ":" || lastToken === "implements" || nextToken === "implements" || nextToken === "=") {
      // Used as identifier
      return "builtin";
    } else {
      // Used as type
      return "type";
    }
  }
  if (stream.match(builtins)) return "builtin";
  if (stream.match(atoms)) return "atom";
  if (stream.match(identifiers)) return "variable";

  // other
  if (stream.match(singleOperators)) return "operator";

  // unrecognized
  stream.next();
  return null;
}
;
const webIDL = {
  name: "webidl",
  startState: function () {
    return {
      // Is in multiline comment
      inComment: false,
      // Last non-whitespace, matched token
      lastToken: "",
      // Next token is a definition
      startDef: false,
      // Last token of the statement is a definition
      endDef: false
    };
  },
  token: function (stream, state) {
    var style = readToken(stream, state);
    if (style) {
      var cur = stream.current();
      state.lastToken = cur;
      if (style === "keyword") {
        state.startDef = startDefs.test(cur);
        state.endDef = state.endDef || endDefs.test(cur);
      } else {
        state.startDef = false;
      }
    }
    return style;
  },
  languageData: {
    autocomplete: builtinArray.concat(typeArray).concat(keywordArray).concat(atomArray)
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNjA0OS5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9AY29kZW1pcnJvci9sZWdhY3ktbW9kZXMvbW9kZS93ZWJpZGwuanMiXSwic291cmNlc0NvbnRlbnQiOlsiZnVuY3Rpb24gd29yZFJlZ2V4cCh3b3Jkcykge1xuICByZXR1cm4gbmV3IFJlZ0V4cChcIl4oKFwiICsgd29yZHMuam9pbihcIil8KFwiKSArIFwiKSlcXFxcYlwiKTtcbn1cbjtcbnZhciBidWlsdGluQXJyYXkgPSBbXCJDbGFtcFwiLCBcIkNvbnN0cnVjdG9yXCIsIFwiRW5mb3JjZVJhbmdlXCIsIFwiRXhwb3NlZFwiLCBcIkltcGxpY2l0VGhpc1wiLCBcIkdsb2JhbFwiLCBcIlByaW1hcnlHbG9iYWxcIiwgXCJMZWdhY3lBcnJheUNsYXNzXCIsIFwiTGVnYWN5VW5lbnVtZXJhYmxlTmFtZWRQcm9wZXJ0aWVzXCIsIFwiTGVuaWVudFRoaXNcIiwgXCJOYW1lZENvbnN0cnVjdG9yXCIsIFwiTmV3T2JqZWN0XCIsIFwiTm9JbnRlcmZhY2VPYmplY3RcIiwgXCJPdmVycmlkZUJ1aWx0aW5zXCIsIFwiUHV0Rm9yd2FyZHNcIiwgXCJSZXBsYWNlYWJsZVwiLCBcIlNhbWVPYmplY3RcIiwgXCJUcmVhdE5vbk9iamVjdEFzTnVsbFwiLCBcIlRyZWF0TnVsbEFzXCIsIFwiRW1wdHlTdHJpbmdcIiwgXCJVbmZvcmdlYWJsZVwiLCBcIlVuc2NvcGVhYmxlXCJdO1xudmFyIGJ1aWx0aW5zID0gd29yZFJlZ2V4cChidWlsdGluQXJyYXkpO1xudmFyIHR5cGVBcnJheSA9IFtcInVuc2lnbmVkXCIsIFwic2hvcnRcIiwgXCJsb25nXCIsXG4vLyBVbnNpZ25lZEludGVnZXJUeXBlXG5cInVucmVzdHJpY3RlZFwiLCBcImZsb2F0XCIsIFwiZG91YmxlXCIsXG4vLyBVbnJlc3RyaWN0ZWRGbG9hdFR5cGVcblwiYm9vbGVhblwiLCBcImJ5dGVcIiwgXCJvY3RldFwiLFxuLy8gUmVzdCBvZiBQcmltaXRpdmVUeXBlXG5cIlByb21pc2VcIixcbi8vIFByb21pc2VUeXBlXG5cIkFycmF5QnVmZmVyXCIsIFwiRGF0YVZpZXdcIiwgXCJJbnQ4QXJyYXlcIiwgXCJJbnQxNkFycmF5XCIsIFwiSW50MzJBcnJheVwiLCBcIlVpbnQ4QXJyYXlcIiwgXCJVaW50MTZBcnJheVwiLCBcIlVpbnQzMkFycmF5XCIsIFwiVWludDhDbGFtcGVkQXJyYXlcIiwgXCJGbG9hdDMyQXJyYXlcIiwgXCJGbG9hdDY0QXJyYXlcIixcbi8vIEJ1ZmZlclJlbGF0ZWRUeXBlXG5cIkJ5dGVTdHJpbmdcIiwgXCJET01TdHJpbmdcIiwgXCJVU1ZTdHJpbmdcIiwgXCJzZXF1ZW5jZVwiLCBcIm9iamVjdFwiLCBcIlJlZ0V4cFwiLCBcIkVycm9yXCIsIFwiRE9NRXhjZXB0aW9uXCIsIFwiRnJvemVuQXJyYXlcIixcbi8vIFJlc3Qgb2YgTm9uQW55VHlwZVxuXCJhbnlcIixcbi8vIFJlc3Qgb2YgU2luZ2xlVHlwZVxuXCJ2b2lkXCIgLy8gUmVzdCBvZiBSZXR1cm5UeXBlXG5dO1xudmFyIHR5cGVzID0gd29yZFJlZ2V4cCh0eXBlQXJyYXkpO1xudmFyIGtleXdvcmRBcnJheSA9IFtcImF0dHJpYnV0ZVwiLCBcImNhbGxiYWNrXCIsIFwiY29uc3RcIiwgXCJkZWxldGVyXCIsIFwiZGljdGlvbmFyeVwiLCBcImVudW1cIiwgXCJnZXR0ZXJcIiwgXCJpbXBsZW1lbnRzXCIsIFwiaW5oZXJpdFwiLCBcImludGVyZmFjZVwiLCBcIml0ZXJhYmxlXCIsIFwibGVnYWN5Y2FsbGVyXCIsIFwibWFwbGlrZVwiLCBcInBhcnRpYWxcIiwgXCJyZXF1aXJlZFwiLCBcInNlcmlhbGl6ZXJcIiwgXCJzZXRsaWtlXCIsIFwic2V0dGVyXCIsIFwic3RhdGljXCIsIFwic3RyaW5naWZpZXJcIiwgXCJ0eXBlZGVmXCIsXG4vLyBBcmd1bWVudE5hbWVLZXl3b3JkIGV4Y2VwdFxuLy8gXCJ1bnJlc3RyaWN0ZWRcIlxuXCJvcHRpb25hbFwiLCBcInJlYWRvbmx5XCIsIFwib3JcIl07XG52YXIga2V5d29yZHMgPSB3b3JkUmVnZXhwKGtleXdvcmRBcnJheSk7XG52YXIgYXRvbUFycmF5ID0gW1widHJ1ZVwiLCBcImZhbHNlXCIsXG4vLyBCb29sZWFuTGl0ZXJhbFxuXCJJbmZpbml0eVwiLCBcIk5hTlwiLFxuLy8gRmxvYXRMaXRlcmFsXG5cIm51bGxcIiAvLyBSZXN0IG9mIENvbnN0VmFsdWVcbl07XG52YXIgYXRvbXMgPSB3b3JkUmVnZXhwKGF0b21BcnJheSk7XG52YXIgc3RhcnREZWZBcnJheSA9IFtcImNhbGxiYWNrXCIsIFwiZGljdGlvbmFyeVwiLCBcImVudW1cIiwgXCJpbnRlcmZhY2VcIl07XG52YXIgc3RhcnREZWZzID0gd29yZFJlZ2V4cChzdGFydERlZkFycmF5KTtcbnZhciBlbmREZWZBcnJheSA9IFtcInR5cGVkZWZcIl07XG52YXIgZW5kRGVmcyA9IHdvcmRSZWdleHAoZW5kRGVmQXJyYXkpO1xudmFyIHNpbmdsZU9wZXJhdG9ycyA9IC9eWzo8PT4/XS87XG52YXIgaW50ZWdlcnMgPSAvXi0/KFsxLTldWzAtOV0qfDBbWHhdWzAtOUEtRmEtZl0rfDBbMC03XSopLztcbnZhciBmbG9hdHMgPSAvXi0/KChbMC05XStcXC5bMC05XSp8WzAtOV0qXFwuWzAtOV0rKShbRWVdWystXT9bMC05XSspP3xbMC05XStbRWVdWystXT9bMC05XSspLztcbnZhciBpZGVudGlmaWVycyA9IC9eXz9bQS1aYS16XVswLTlBLVpfYS16LV0qLztcbnZhciBpZGVudGlmaWVyc0VuZCA9IC9eXz9bQS1aYS16XVswLTlBLVpfYS16LV0qKD89XFxzKjspLztcbnZhciBzdHJpbmdzID0gL15cIlteXCJdKlwiLztcbnZhciBtdWx0aWxpbmVDb21tZW50cyA9IC9eXFwvXFwqLio/XFwqXFwvLztcbnZhciBtdWx0aWxpbmVDb21tZW50c1N0YXJ0ID0gL15cXC9cXCouKi87XG52YXIgbXVsdGlsaW5lQ29tbWVudHNFbmQgPSAvXi4qP1xcKlxcLy87XG5mdW5jdGlvbiByZWFkVG9rZW4oc3RyZWFtLCBzdGF0ZSkge1xuICAvLyB3aGl0ZXNwYWNlXG4gIGlmIChzdHJlYW0uZWF0U3BhY2UoKSkgcmV0dXJuIG51bGw7XG5cbiAgLy8gY29tbWVudFxuICBpZiAoc3RhdGUuaW5Db21tZW50KSB7XG4gICAgaWYgKHN0cmVhbS5tYXRjaChtdWx0aWxpbmVDb21tZW50c0VuZCkpIHtcbiAgICAgIHN0YXRlLmluQ29tbWVudCA9IGZhbHNlO1xuICAgICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICAgIH1cbiAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICB9XG4gIGlmIChzdHJlYW0ubWF0Y2goXCIvL1wiKSkge1xuICAgIHN0cmVhbS5za2lwVG9FbmQoKTtcbiAgICByZXR1cm4gXCJjb21tZW50XCI7XG4gIH1cbiAgaWYgKHN0cmVhbS5tYXRjaChtdWx0aWxpbmVDb21tZW50cykpIHJldHVybiBcImNvbW1lbnRcIjtcbiAgaWYgKHN0cmVhbS5tYXRjaChtdWx0aWxpbmVDb21tZW50c1N0YXJ0KSkge1xuICAgIHN0YXRlLmluQ29tbWVudCA9IHRydWU7XG4gICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICB9XG5cbiAgLy8gaW50ZWdlciBhbmQgZmxvYXRcbiAgaWYgKHN0cmVhbS5tYXRjaCgvXi0/WzAtOVxcLl0vLCBmYWxzZSkpIHtcbiAgICBpZiAoc3RyZWFtLm1hdGNoKGludGVnZXJzKSB8fCBzdHJlYW0ubWF0Y2goZmxvYXRzKSkgcmV0dXJuIFwibnVtYmVyXCI7XG4gIH1cblxuICAvLyBzdHJpbmdcbiAgaWYgKHN0cmVhbS5tYXRjaChzdHJpbmdzKSkgcmV0dXJuIFwic3RyaW5nXCI7XG5cbiAgLy8gaWRlbnRpZmllclxuICBpZiAoc3RhdGUuc3RhcnREZWYgJiYgc3RyZWFtLm1hdGNoKGlkZW50aWZpZXJzKSkgcmV0dXJuIFwiZGVmXCI7XG4gIGlmIChzdGF0ZS5lbmREZWYgJiYgc3RyZWFtLm1hdGNoKGlkZW50aWZpZXJzRW5kKSkge1xuICAgIHN0YXRlLmVuZERlZiA9IGZhbHNlO1xuICAgIHJldHVybiBcImRlZlwiO1xuICB9XG4gIGlmIChzdHJlYW0ubWF0Y2goa2V5d29yZHMpKSByZXR1cm4gXCJrZXl3b3JkXCI7XG4gIGlmIChzdHJlYW0ubWF0Y2godHlwZXMpKSB7XG4gICAgdmFyIGxhc3RUb2tlbiA9IHN0YXRlLmxhc3RUb2tlbjtcbiAgICB2YXIgbmV4dFRva2VuID0gKHN0cmVhbS5tYXRjaCgvXlxccyooLis/KVxcYi8sIGZhbHNlKSB8fCBbXSlbMV07XG4gICAgaWYgKGxhc3RUb2tlbiA9PT0gXCI6XCIgfHwgbGFzdFRva2VuID09PSBcImltcGxlbWVudHNcIiB8fCBuZXh0VG9rZW4gPT09IFwiaW1wbGVtZW50c1wiIHx8IG5leHRUb2tlbiA9PT0gXCI9XCIpIHtcbiAgICAgIC8vIFVzZWQgYXMgaWRlbnRpZmllclxuICAgICAgcmV0dXJuIFwiYnVpbHRpblwiO1xuICAgIH0gZWxzZSB7XG4gICAgICAvLyBVc2VkIGFzIHR5cGVcbiAgICAgIHJldHVybiBcInR5cGVcIjtcbiAgICB9XG4gIH1cbiAgaWYgKHN0cmVhbS5tYXRjaChidWlsdGlucykpIHJldHVybiBcImJ1aWx0aW5cIjtcbiAgaWYgKHN0cmVhbS5tYXRjaChhdG9tcykpIHJldHVybiBcImF0b21cIjtcbiAgaWYgKHN0cmVhbS5tYXRjaChpZGVudGlmaWVycykpIHJldHVybiBcInZhcmlhYmxlXCI7XG5cbiAgLy8gb3RoZXJcbiAgaWYgKHN0cmVhbS5tYXRjaChzaW5nbGVPcGVyYXRvcnMpKSByZXR1cm4gXCJvcGVyYXRvclwiO1xuXG4gIC8vIHVucmVjb2duaXplZFxuICBzdHJlYW0ubmV4dCgpO1xuICByZXR1cm4gbnVsbDtcbn1cbjtcbmV4cG9ydCBjb25zdCB3ZWJJREwgPSB7XG4gIG5hbWU6IFwid2ViaWRsXCIsXG4gIHN0YXJ0U3RhdGU6IGZ1bmN0aW9uICgpIHtcbiAgICByZXR1cm4ge1xuICAgICAgLy8gSXMgaW4gbXVsdGlsaW5lIGNvbW1lbnRcbiAgICAgIGluQ29tbWVudDogZmFsc2UsXG4gICAgICAvLyBMYXN0IG5vbi13aGl0ZXNwYWNlLCBtYXRjaGVkIHRva2VuXG4gICAgICBsYXN0VG9rZW46IFwiXCIsXG4gICAgICAvLyBOZXh0IHRva2VuIGlzIGEgZGVmaW5pdGlvblxuICAgICAgc3RhcnREZWY6IGZhbHNlLFxuICAgICAgLy8gTGFzdCB0b2tlbiBvZiB0aGUgc3RhdGVtZW50IGlzIGEgZGVmaW5pdGlvblxuICAgICAgZW5kRGVmOiBmYWxzZVxuICAgIH07XG4gIH0sXG4gIHRva2VuOiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIHZhciBzdHlsZSA9IHJlYWRUb2tlbihzdHJlYW0sIHN0YXRlKTtcbiAgICBpZiAoc3R5bGUpIHtcbiAgICAgIHZhciBjdXIgPSBzdHJlYW0uY3VycmVudCgpO1xuICAgICAgc3RhdGUubGFzdFRva2VuID0gY3VyO1xuICAgICAgaWYgKHN0eWxlID09PSBcImtleXdvcmRcIikge1xuICAgICAgICBzdGF0ZS5zdGFydERlZiA9IHN0YXJ0RGVmcy50ZXN0KGN1cik7XG4gICAgICAgIHN0YXRlLmVuZERlZiA9IHN0YXRlLmVuZERlZiB8fCBlbmREZWZzLnRlc3QoY3VyKTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHN0YXRlLnN0YXJ0RGVmID0gZmFsc2U7XG4gICAgICB9XG4gICAgfVxuICAgIHJldHVybiBzdHlsZTtcbiAgfSxcbiAgbGFuZ3VhZ2VEYXRhOiB7XG4gICAgYXV0b2NvbXBsZXRlOiBidWlsdGluQXJyYXkuY29uY2F0KHR5cGVBcnJheSkuY29uY2F0KGtleXdvcmRBcnJheSkuY29uY2F0KGF0b21BcnJheSlcbiAgfVxufTsiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=