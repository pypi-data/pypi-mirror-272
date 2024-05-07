"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[1146],{

/***/ 91146:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "asn1": () => (/* binding */ asn1)
/* harmony export */ });
function words(str) {
  var obj = {},
    words = str.split(" ");
  for (var i = 0; i < words.length; ++i) obj[words[i]] = true;
  return obj;
}
const defaults = {
  keywords: words("DEFINITIONS OBJECTS IF DERIVED INFORMATION ACTION" + " REPLY ANY NAMED CHARACTERIZED BEHAVIOUR REGISTERED" + " WITH AS IDENTIFIED CONSTRAINED BY PRESENT BEGIN" + " IMPORTS FROM UNITS SYNTAX MIN-ACCESS MAX-ACCESS" + " MINACCESS MAXACCESS REVISION STATUS DESCRIPTION" + " SEQUENCE SET COMPONENTS OF CHOICE DistinguishedName" + " ENUMERATED SIZE MODULE END INDEX AUGMENTS EXTENSIBILITY" + " IMPLIED EXPORTS"),
  cmipVerbs: words("ACTIONS ADD GET NOTIFICATIONS REPLACE REMOVE"),
  compareTypes: words("OPTIONAL DEFAULT MANAGED MODULE-TYPE MODULE_IDENTITY" + " MODULE-COMPLIANCE OBJECT-TYPE OBJECT-IDENTITY" + " OBJECT-COMPLIANCE MODE CONFIRMED CONDITIONAL" + " SUBORDINATE SUPERIOR CLASS TRUE FALSE NULL" + " TEXTUAL-CONVENTION"),
  status: words("current deprecated mandatory obsolete"),
  tags: words("APPLICATION AUTOMATIC EXPLICIT IMPLICIT PRIVATE TAGS" + " UNIVERSAL"),
  storage: words("BOOLEAN INTEGER OBJECT IDENTIFIER BIT OCTET STRING" + " UTCTime InterfaceIndex IANAifType CMIP-Attribute" + " REAL PACKAGE PACKAGES IpAddress PhysAddress" + " NetworkAddress BITS BMPString TimeStamp TimeTicks" + " TruthValue RowStatus DisplayString GeneralString" + " GraphicString IA5String NumericString" + " PrintableString SnmpAdminString TeletexString" + " UTF8String VideotexString VisibleString StringStore" + " ISO646String T61String UniversalString Unsigned32" + " Integer32 Gauge Gauge32 Counter Counter32 Counter64"),
  modifier: words("ATTRIBUTE ATTRIBUTES MANDATORY-GROUP MANDATORY-GROUPS" + " GROUP GROUPS ELEMENTS EQUALITY ORDERING SUBSTRINGS" + " DEFINED"),
  accessTypes: words("not-accessible accessible-for-notify read-only" + " read-create read-write"),
  multiLineStrings: true
};
function asn1(parserConfig) {
  var keywords = parserConfig.keywords || defaults.keywords,
    cmipVerbs = parserConfig.cmipVerbs || defaults.cmipVerbs,
    compareTypes = parserConfig.compareTypes || defaults.compareTypes,
    status = parserConfig.status || defaults.status,
    tags = parserConfig.tags || defaults.tags,
    storage = parserConfig.storage || defaults.storage,
    modifier = parserConfig.modifier || defaults.modifier,
    accessTypes = parserConfig.accessTypes || defaults.accessTypes,
    multiLineStrings = parserConfig.multiLineStrings || defaults.multiLineStrings,
    indentStatements = parserConfig.indentStatements !== false;
  var isOperatorChar = /[\|\^]/;
  var curPunc;
  function tokenBase(stream, state) {
    var ch = stream.next();
    if (ch == '"' || ch == "'") {
      state.tokenize = tokenString(ch);
      return state.tokenize(stream, state);
    }
    if (/[\[\]\(\){}:=,;]/.test(ch)) {
      curPunc = ch;
      return "punctuation";
    }
    if (ch == "-") {
      if (stream.eat("-")) {
        stream.skipToEnd();
        return "comment";
      }
    }
    if (/\d/.test(ch)) {
      stream.eatWhile(/[\w\.]/);
      return "number";
    }
    if (isOperatorChar.test(ch)) {
      stream.eatWhile(isOperatorChar);
      return "operator";
    }
    stream.eatWhile(/[\w\-]/);
    var cur = stream.current();
    if (keywords.propertyIsEnumerable(cur)) return "keyword";
    if (cmipVerbs.propertyIsEnumerable(cur)) return "variableName";
    if (compareTypes.propertyIsEnumerable(cur)) return "atom";
    if (status.propertyIsEnumerable(cur)) return "comment";
    if (tags.propertyIsEnumerable(cur)) return "typeName";
    if (storage.propertyIsEnumerable(cur)) return "modifier";
    if (modifier.propertyIsEnumerable(cur)) return "modifier";
    if (accessTypes.propertyIsEnumerable(cur)) return "modifier";
    return "variableName";
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
  return {
    name: "asn1",
    startState: function () {
      return {
        tokenize: null,
        context: new Context(-2, 0, "top", false),
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
        line: "--"
      }
    }
  };
}
;

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiMTE0Ni5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL0Bjb2RlbWlycm9yL2xlZ2FjeS1tb2Rlcy9tb2RlL2FzbjEuanMiXSwic291cmNlc0NvbnRlbnQiOlsiZnVuY3Rpb24gd29yZHMoc3RyKSB7XG4gIHZhciBvYmogPSB7fSxcbiAgICB3b3JkcyA9IHN0ci5zcGxpdChcIiBcIik7XG4gIGZvciAodmFyIGkgPSAwOyBpIDwgd29yZHMubGVuZ3RoOyArK2kpIG9ialt3b3Jkc1tpXV0gPSB0cnVlO1xuICByZXR1cm4gb2JqO1xufVxuY29uc3QgZGVmYXVsdHMgPSB7XG4gIGtleXdvcmRzOiB3b3JkcyhcIkRFRklOSVRJT05TIE9CSkVDVFMgSUYgREVSSVZFRCBJTkZPUk1BVElPTiBBQ1RJT05cIiArIFwiIFJFUExZIEFOWSBOQU1FRCBDSEFSQUNURVJJWkVEIEJFSEFWSU9VUiBSRUdJU1RFUkVEXCIgKyBcIiBXSVRIIEFTIElERU5USUZJRUQgQ09OU1RSQUlORUQgQlkgUFJFU0VOVCBCRUdJTlwiICsgXCIgSU1QT1JUUyBGUk9NIFVOSVRTIFNZTlRBWCBNSU4tQUNDRVNTIE1BWC1BQ0NFU1NcIiArIFwiIE1JTkFDQ0VTUyBNQVhBQ0NFU1MgUkVWSVNJT04gU1RBVFVTIERFU0NSSVBUSU9OXCIgKyBcIiBTRVFVRU5DRSBTRVQgQ09NUE9ORU5UUyBPRiBDSE9JQ0UgRGlzdGluZ3Vpc2hlZE5hbWVcIiArIFwiIEVOVU1FUkFURUQgU0laRSBNT0RVTEUgRU5EIElOREVYIEFVR01FTlRTIEVYVEVOU0lCSUxJVFlcIiArIFwiIElNUExJRUQgRVhQT1JUU1wiKSxcbiAgY21pcFZlcmJzOiB3b3JkcyhcIkFDVElPTlMgQUREIEdFVCBOT1RJRklDQVRJT05TIFJFUExBQ0UgUkVNT1ZFXCIpLFxuICBjb21wYXJlVHlwZXM6IHdvcmRzKFwiT1BUSU9OQUwgREVGQVVMVCBNQU5BR0VEIE1PRFVMRS1UWVBFIE1PRFVMRV9JREVOVElUWVwiICsgXCIgTU9EVUxFLUNPTVBMSUFOQ0UgT0JKRUNULVRZUEUgT0JKRUNULUlERU5USVRZXCIgKyBcIiBPQkpFQ1QtQ09NUExJQU5DRSBNT0RFIENPTkZJUk1FRCBDT05ESVRJT05BTFwiICsgXCIgU1VCT1JESU5BVEUgU1VQRVJJT1IgQ0xBU1MgVFJVRSBGQUxTRSBOVUxMXCIgKyBcIiBURVhUVUFMLUNPTlZFTlRJT05cIiksXG4gIHN0YXR1czogd29yZHMoXCJjdXJyZW50IGRlcHJlY2F0ZWQgbWFuZGF0b3J5IG9ic29sZXRlXCIpLFxuICB0YWdzOiB3b3JkcyhcIkFQUExJQ0FUSU9OIEFVVE9NQVRJQyBFWFBMSUNJVCBJTVBMSUNJVCBQUklWQVRFIFRBR1NcIiArIFwiIFVOSVZFUlNBTFwiKSxcbiAgc3RvcmFnZTogd29yZHMoXCJCT09MRUFOIElOVEVHRVIgT0JKRUNUIElERU5USUZJRVIgQklUIE9DVEVUIFNUUklOR1wiICsgXCIgVVRDVGltZSBJbnRlcmZhY2VJbmRleCBJQU5BaWZUeXBlIENNSVAtQXR0cmlidXRlXCIgKyBcIiBSRUFMIFBBQ0tBR0UgUEFDS0FHRVMgSXBBZGRyZXNzIFBoeXNBZGRyZXNzXCIgKyBcIiBOZXR3b3JrQWRkcmVzcyBCSVRTIEJNUFN0cmluZyBUaW1lU3RhbXAgVGltZVRpY2tzXCIgKyBcIiBUcnV0aFZhbHVlIFJvd1N0YXR1cyBEaXNwbGF5U3RyaW5nIEdlbmVyYWxTdHJpbmdcIiArIFwiIEdyYXBoaWNTdHJpbmcgSUE1U3RyaW5nIE51bWVyaWNTdHJpbmdcIiArIFwiIFByaW50YWJsZVN0cmluZyBTbm1wQWRtaW5TdHJpbmcgVGVsZXRleFN0cmluZ1wiICsgXCIgVVRGOFN0cmluZyBWaWRlb3RleFN0cmluZyBWaXNpYmxlU3RyaW5nIFN0cmluZ1N0b3JlXCIgKyBcIiBJU082NDZTdHJpbmcgVDYxU3RyaW5nIFVuaXZlcnNhbFN0cmluZyBVbnNpZ25lZDMyXCIgKyBcIiBJbnRlZ2VyMzIgR2F1Z2UgR2F1Z2UzMiBDb3VudGVyIENvdW50ZXIzMiBDb3VudGVyNjRcIiksXG4gIG1vZGlmaWVyOiB3b3JkcyhcIkFUVFJJQlVURSBBVFRSSUJVVEVTIE1BTkRBVE9SWS1HUk9VUCBNQU5EQVRPUlktR1JPVVBTXCIgKyBcIiBHUk9VUCBHUk9VUFMgRUxFTUVOVFMgRVFVQUxJVFkgT1JERVJJTkcgU1VCU1RSSU5HU1wiICsgXCIgREVGSU5FRFwiKSxcbiAgYWNjZXNzVHlwZXM6IHdvcmRzKFwibm90LWFjY2Vzc2libGUgYWNjZXNzaWJsZS1mb3Itbm90aWZ5IHJlYWQtb25seVwiICsgXCIgcmVhZC1jcmVhdGUgcmVhZC13cml0ZVwiKSxcbiAgbXVsdGlMaW5lU3RyaW5nczogdHJ1ZVxufTtcbmV4cG9ydCBmdW5jdGlvbiBhc24xKHBhcnNlckNvbmZpZykge1xuICB2YXIga2V5d29yZHMgPSBwYXJzZXJDb25maWcua2V5d29yZHMgfHwgZGVmYXVsdHMua2V5d29yZHMsXG4gICAgY21pcFZlcmJzID0gcGFyc2VyQ29uZmlnLmNtaXBWZXJicyB8fCBkZWZhdWx0cy5jbWlwVmVyYnMsXG4gICAgY29tcGFyZVR5cGVzID0gcGFyc2VyQ29uZmlnLmNvbXBhcmVUeXBlcyB8fCBkZWZhdWx0cy5jb21wYXJlVHlwZXMsXG4gICAgc3RhdHVzID0gcGFyc2VyQ29uZmlnLnN0YXR1cyB8fCBkZWZhdWx0cy5zdGF0dXMsXG4gICAgdGFncyA9IHBhcnNlckNvbmZpZy50YWdzIHx8IGRlZmF1bHRzLnRhZ3MsXG4gICAgc3RvcmFnZSA9IHBhcnNlckNvbmZpZy5zdG9yYWdlIHx8IGRlZmF1bHRzLnN0b3JhZ2UsXG4gICAgbW9kaWZpZXIgPSBwYXJzZXJDb25maWcubW9kaWZpZXIgfHwgZGVmYXVsdHMubW9kaWZpZXIsXG4gICAgYWNjZXNzVHlwZXMgPSBwYXJzZXJDb25maWcuYWNjZXNzVHlwZXMgfHwgZGVmYXVsdHMuYWNjZXNzVHlwZXMsXG4gICAgbXVsdGlMaW5lU3RyaW5ncyA9IHBhcnNlckNvbmZpZy5tdWx0aUxpbmVTdHJpbmdzIHx8IGRlZmF1bHRzLm11bHRpTGluZVN0cmluZ3MsXG4gICAgaW5kZW50U3RhdGVtZW50cyA9IHBhcnNlckNvbmZpZy5pbmRlbnRTdGF0ZW1lbnRzICE9PSBmYWxzZTtcbiAgdmFyIGlzT3BlcmF0b3JDaGFyID0gL1tcXHxcXF5dLztcbiAgdmFyIGN1clB1bmM7XG4gIGZ1bmN0aW9uIHRva2VuQmFzZShzdHJlYW0sIHN0YXRlKSB7XG4gICAgdmFyIGNoID0gc3RyZWFtLm5leHQoKTtcbiAgICBpZiAoY2ggPT0gJ1wiJyB8fCBjaCA9PSBcIidcIikge1xuICAgICAgc3RhdGUudG9rZW5pemUgPSB0b2tlblN0cmluZyhjaCk7XG4gICAgICByZXR1cm4gc3RhdGUudG9rZW5pemUoc3RyZWFtLCBzdGF0ZSk7XG4gICAgfVxuICAgIGlmICgvW1xcW1xcXVxcKFxcKXt9Oj0sO10vLnRlc3QoY2gpKSB7XG4gICAgICBjdXJQdW5jID0gY2g7XG4gICAgICByZXR1cm4gXCJwdW5jdHVhdGlvblwiO1xuICAgIH1cbiAgICBpZiAoY2ggPT0gXCItXCIpIHtcbiAgICAgIGlmIChzdHJlYW0uZWF0KFwiLVwiKSkge1xuICAgICAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgICAgIHJldHVybiBcImNvbW1lbnRcIjtcbiAgICAgIH1cbiAgICB9XG4gICAgaWYgKC9cXGQvLnRlc3QoY2gpKSB7XG4gICAgICBzdHJlYW0uZWF0V2hpbGUoL1tcXHdcXC5dLyk7XG4gICAgICByZXR1cm4gXCJudW1iZXJcIjtcbiAgICB9XG4gICAgaWYgKGlzT3BlcmF0b3JDaGFyLnRlc3QoY2gpKSB7XG4gICAgICBzdHJlYW0uZWF0V2hpbGUoaXNPcGVyYXRvckNoYXIpO1xuICAgICAgcmV0dXJuIFwib3BlcmF0b3JcIjtcbiAgICB9XG4gICAgc3RyZWFtLmVhdFdoaWxlKC9bXFx3XFwtXS8pO1xuICAgIHZhciBjdXIgPSBzdHJlYW0uY3VycmVudCgpO1xuICAgIGlmIChrZXl3b3Jkcy5wcm9wZXJ0eUlzRW51bWVyYWJsZShjdXIpKSByZXR1cm4gXCJrZXl3b3JkXCI7XG4gICAgaWYgKGNtaXBWZXJicy5wcm9wZXJ0eUlzRW51bWVyYWJsZShjdXIpKSByZXR1cm4gXCJ2YXJpYWJsZU5hbWVcIjtcbiAgICBpZiAoY29tcGFyZVR5cGVzLnByb3BlcnR5SXNFbnVtZXJhYmxlKGN1cikpIHJldHVybiBcImF0b21cIjtcbiAgICBpZiAoc3RhdHVzLnByb3BlcnR5SXNFbnVtZXJhYmxlKGN1cikpIHJldHVybiBcImNvbW1lbnRcIjtcbiAgICBpZiAodGFncy5wcm9wZXJ0eUlzRW51bWVyYWJsZShjdXIpKSByZXR1cm4gXCJ0eXBlTmFtZVwiO1xuICAgIGlmIChzdG9yYWdlLnByb3BlcnR5SXNFbnVtZXJhYmxlKGN1cikpIHJldHVybiBcIm1vZGlmaWVyXCI7XG4gICAgaWYgKG1vZGlmaWVyLnByb3BlcnR5SXNFbnVtZXJhYmxlKGN1cikpIHJldHVybiBcIm1vZGlmaWVyXCI7XG4gICAgaWYgKGFjY2Vzc1R5cGVzLnByb3BlcnR5SXNFbnVtZXJhYmxlKGN1cikpIHJldHVybiBcIm1vZGlmaWVyXCI7XG4gICAgcmV0dXJuIFwidmFyaWFibGVOYW1lXCI7XG4gIH1cbiAgZnVuY3Rpb24gdG9rZW5TdHJpbmcocXVvdGUpIHtcbiAgICByZXR1cm4gZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICAgIHZhciBlc2NhcGVkID0gZmFsc2UsXG4gICAgICAgIG5leHQsXG4gICAgICAgIGVuZCA9IGZhbHNlO1xuICAgICAgd2hpbGUgKChuZXh0ID0gc3RyZWFtLm5leHQoKSkgIT0gbnVsbCkge1xuICAgICAgICBpZiAobmV4dCA9PSBxdW90ZSAmJiAhZXNjYXBlZCkge1xuICAgICAgICAgIHZhciBhZnRlck5leHQgPSBzdHJlYW0ucGVlaygpO1xuICAgICAgICAgIC8vbG9vayBpZiB0aGUgY2hhcmFjdGVyIGlmIHRoZSBxdW90ZSBpcyBsaWtlIHRoZSBCIGluICcxMDEwMDAxMCdCXG4gICAgICAgICAgaWYgKGFmdGVyTmV4dCkge1xuICAgICAgICAgICAgYWZ0ZXJOZXh0ID0gYWZ0ZXJOZXh0LnRvTG93ZXJDYXNlKCk7XG4gICAgICAgICAgICBpZiAoYWZ0ZXJOZXh0ID09IFwiYlwiIHx8IGFmdGVyTmV4dCA9PSBcImhcIiB8fCBhZnRlck5leHQgPT0gXCJvXCIpIHN0cmVhbS5uZXh0KCk7XG4gICAgICAgICAgfVxuICAgICAgICAgIGVuZCA9IHRydWU7XG4gICAgICAgICAgYnJlYWs7XG4gICAgICAgIH1cbiAgICAgICAgZXNjYXBlZCA9ICFlc2NhcGVkICYmIG5leHQgPT0gXCJcXFxcXCI7XG4gICAgICB9XG4gICAgICBpZiAoZW5kIHx8ICEoZXNjYXBlZCB8fCBtdWx0aUxpbmVTdHJpbmdzKSkgc3RhdGUudG9rZW5pemUgPSBudWxsO1xuICAgICAgcmV0dXJuIFwic3RyaW5nXCI7XG4gICAgfTtcbiAgfVxuICBmdW5jdGlvbiBDb250ZXh0KGluZGVudGVkLCBjb2x1bW4sIHR5cGUsIGFsaWduLCBwcmV2KSB7XG4gICAgdGhpcy5pbmRlbnRlZCA9IGluZGVudGVkO1xuICAgIHRoaXMuY29sdW1uID0gY29sdW1uO1xuICAgIHRoaXMudHlwZSA9IHR5cGU7XG4gICAgdGhpcy5hbGlnbiA9IGFsaWduO1xuICAgIHRoaXMucHJldiA9IHByZXY7XG4gIH1cbiAgZnVuY3Rpb24gcHVzaENvbnRleHQoc3RhdGUsIGNvbCwgdHlwZSkge1xuICAgIHZhciBpbmRlbnQgPSBzdGF0ZS5pbmRlbnRlZDtcbiAgICBpZiAoc3RhdGUuY29udGV4dCAmJiBzdGF0ZS5jb250ZXh0LnR5cGUgPT0gXCJzdGF0ZW1lbnRcIikgaW5kZW50ID0gc3RhdGUuY29udGV4dC5pbmRlbnRlZDtcbiAgICByZXR1cm4gc3RhdGUuY29udGV4dCA9IG5ldyBDb250ZXh0KGluZGVudCwgY29sLCB0eXBlLCBudWxsLCBzdGF0ZS5jb250ZXh0KTtcbiAgfVxuICBmdW5jdGlvbiBwb3BDb250ZXh0KHN0YXRlKSB7XG4gICAgdmFyIHQgPSBzdGF0ZS5jb250ZXh0LnR5cGU7XG4gICAgaWYgKHQgPT0gXCIpXCIgfHwgdCA9PSBcIl1cIiB8fCB0ID09IFwifVwiKSBzdGF0ZS5pbmRlbnRlZCA9IHN0YXRlLmNvbnRleHQuaW5kZW50ZWQ7XG4gICAgcmV0dXJuIHN0YXRlLmNvbnRleHQgPSBzdGF0ZS5jb250ZXh0LnByZXY7XG4gIH1cblxuICAvL0ludGVyZmFjZVxuICByZXR1cm4ge1xuICAgIG5hbWU6IFwiYXNuMVwiLFxuICAgIHN0YXJ0U3RhdGU6IGZ1bmN0aW9uICgpIHtcbiAgICAgIHJldHVybiB7XG4gICAgICAgIHRva2VuaXplOiBudWxsLFxuICAgICAgICBjb250ZXh0OiBuZXcgQ29udGV4dCgtMiwgMCwgXCJ0b3BcIiwgZmFsc2UpLFxuICAgICAgICBpbmRlbnRlZDogMCxcbiAgICAgICAgc3RhcnRPZkxpbmU6IHRydWVcbiAgICAgIH07XG4gICAgfSxcbiAgICB0b2tlbjogZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICAgIHZhciBjdHggPSBzdGF0ZS5jb250ZXh0O1xuICAgICAgaWYgKHN0cmVhbS5zb2woKSkge1xuICAgICAgICBpZiAoY3R4LmFsaWduID09IG51bGwpIGN0eC5hbGlnbiA9IGZhbHNlO1xuICAgICAgICBzdGF0ZS5pbmRlbnRlZCA9IHN0cmVhbS5pbmRlbnRhdGlvbigpO1xuICAgICAgICBzdGF0ZS5zdGFydE9mTGluZSA9IHRydWU7XG4gICAgICB9XG4gICAgICBpZiAoc3RyZWFtLmVhdFNwYWNlKCkpIHJldHVybiBudWxsO1xuICAgICAgY3VyUHVuYyA9IG51bGw7XG4gICAgICB2YXIgc3R5bGUgPSAoc3RhdGUudG9rZW5pemUgfHwgdG9rZW5CYXNlKShzdHJlYW0sIHN0YXRlKTtcbiAgICAgIGlmIChzdHlsZSA9PSBcImNvbW1lbnRcIikgcmV0dXJuIHN0eWxlO1xuICAgICAgaWYgKGN0eC5hbGlnbiA9PSBudWxsKSBjdHguYWxpZ24gPSB0cnVlO1xuICAgICAgaWYgKChjdXJQdW5jID09IFwiO1wiIHx8IGN1clB1bmMgPT0gXCI6XCIgfHwgY3VyUHVuYyA9PSBcIixcIikgJiYgY3R4LnR5cGUgPT0gXCJzdGF0ZW1lbnRcIikge1xuICAgICAgICBwb3BDb250ZXh0KHN0YXRlKTtcbiAgICAgIH0gZWxzZSBpZiAoY3VyUHVuYyA9PSBcIntcIikgcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbS5jb2x1bW4oKSwgXCJ9XCIpO2Vsc2UgaWYgKGN1clB1bmMgPT0gXCJbXCIpIHB1c2hDb250ZXh0KHN0YXRlLCBzdHJlYW0uY29sdW1uKCksIFwiXVwiKTtlbHNlIGlmIChjdXJQdW5jID09IFwiKFwiKSBwdXNoQ29udGV4dChzdGF0ZSwgc3RyZWFtLmNvbHVtbigpLCBcIilcIik7ZWxzZSBpZiAoY3VyUHVuYyA9PSBcIn1cIikge1xuICAgICAgICB3aGlsZSAoY3R4LnR5cGUgPT0gXCJzdGF0ZW1lbnRcIikgY3R4ID0gcG9wQ29udGV4dChzdGF0ZSk7XG4gICAgICAgIGlmIChjdHgudHlwZSA9PSBcIn1cIikgY3R4ID0gcG9wQ29udGV4dChzdGF0ZSk7XG4gICAgICAgIHdoaWxlIChjdHgudHlwZSA9PSBcInN0YXRlbWVudFwiKSBjdHggPSBwb3BDb250ZXh0KHN0YXRlKTtcbiAgICAgIH0gZWxzZSBpZiAoY3VyUHVuYyA9PSBjdHgudHlwZSkgcG9wQ29udGV4dChzdGF0ZSk7ZWxzZSBpZiAoaW5kZW50U3RhdGVtZW50cyAmJiAoKGN0eC50eXBlID09IFwifVwiIHx8IGN0eC50eXBlID09IFwidG9wXCIpICYmIGN1clB1bmMgIT0gJzsnIHx8IGN0eC50eXBlID09IFwic3RhdGVtZW50XCIgJiYgY3VyUHVuYyA9PSBcIm5ld3N0YXRlbWVudFwiKSkgcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbS5jb2x1bW4oKSwgXCJzdGF0ZW1lbnRcIik7XG4gICAgICBzdGF0ZS5zdGFydE9mTGluZSA9IGZhbHNlO1xuICAgICAgcmV0dXJuIHN0eWxlO1xuICAgIH0sXG4gICAgbGFuZ3VhZ2VEYXRhOiB7XG4gICAgICBpbmRlbnRPbklucHV0OiAvXlxccypbe31dJC8sXG4gICAgICBjb21tZW50VG9rZW5zOiB7XG4gICAgICAgIGxpbmU6IFwiLS1cIlxuICAgICAgfVxuICAgIH1cbiAgfTtcbn1cbjsiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=