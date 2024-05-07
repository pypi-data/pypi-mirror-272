"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[6249],{

/***/ 26249:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "apl": () => (/* binding */ apl)
/* harmony export */ });
var builtInFuncs = {
  "+": ["conjugate", "add"],
  "−": ["negate", "subtract"],
  "×": ["signOf", "multiply"],
  "÷": ["reciprocal", "divide"],
  "⌈": ["ceiling", "greaterOf"],
  "⌊": ["floor", "lesserOf"],
  "∣": ["absolute", "residue"],
  "⍳": ["indexGenerate", "indexOf"],
  "?": ["roll", "deal"],
  "⋆": ["exponentiate", "toThePowerOf"],
  "⍟": ["naturalLog", "logToTheBase"],
  "○": ["piTimes", "circularFuncs"],
  "!": ["factorial", "binomial"],
  "⌹": ["matrixInverse", "matrixDivide"],
  "<": [null, "lessThan"],
  "≤": [null, "lessThanOrEqual"],
  "=": [null, "equals"],
  ">": [null, "greaterThan"],
  "≥": [null, "greaterThanOrEqual"],
  "≠": [null, "notEqual"],
  "≡": ["depth", "match"],
  "≢": [null, "notMatch"],
  "∈": ["enlist", "membership"],
  "⍷": [null, "find"],
  "∪": ["unique", "union"],
  "∩": [null, "intersection"],
  "∼": ["not", "without"],
  "∨": [null, "or"],
  "∧": [null, "and"],
  "⍱": [null, "nor"],
  "⍲": [null, "nand"],
  "⍴": ["shapeOf", "reshape"],
  ",": ["ravel", "catenate"],
  "⍪": [null, "firstAxisCatenate"],
  "⌽": ["reverse", "rotate"],
  "⊖": ["axis1Reverse", "axis1Rotate"],
  "⍉": ["transpose", null],
  "↑": ["first", "take"],
  "↓": [null, "drop"],
  "⊂": ["enclose", "partitionWithAxis"],
  "⊃": ["diclose", "pick"],
  "⌷": [null, "index"],
  "⍋": ["gradeUp", null],
  "⍒": ["gradeDown", null],
  "⊤": ["encode", null],
  "⊥": ["decode", null],
  "⍕": ["format", "formatByExample"],
  "⍎": ["execute", null],
  "⊣": ["stop", "left"],
  "⊢": ["pass", "right"]
};
var isOperator = /[\.\/⌿⍀¨⍣]/;
var isNiladic = /⍬/;
var isFunction = /[\+−×÷⌈⌊∣⍳\?⋆⍟○!⌹<≤=>≥≠≡≢∈⍷∪∩∼∨∧⍱⍲⍴,⍪⌽⊖⍉↑↓⊂⊃⌷⍋⍒⊤⊥⍕⍎⊣⊢]/;
var isArrow = /←/;
var isComment = /[⍝#].*$/;
var stringEater = function (type) {
  var prev;
  prev = false;
  return function (c) {
    prev = c;
    if (c === type) {
      return prev === "\\";
    }
    return true;
  };
};
const apl = {
  name: "apl",
  startState: function () {
    return {
      prev: false,
      func: false,
      op: false,
      string: false,
      escape: false
    };
  },
  token: function (stream, state) {
    var ch;
    if (stream.eatSpace()) {
      return null;
    }
    ch = stream.next();
    if (ch === '"' || ch === "'") {
      stream.eatWhile(stringEater(ch));
      stream.next();
      state.prev = true;
      return "string";
    }
    if (/[\[{\(]/.test(ch)) {
      state.prev = false;
      return null;
    }
    if (/[\]}\)]/.test(ch)) {
      state.prev = true;
      return null;
    }
    if (isNiladic.test(ch)) {
      state.prev = false;
      return "atom";
    }
    if (/[¯\d]/.test(ch)) {
      if (state.func) {
        state.func = false;
        state.prev = false;
      } else {
        state.prev = true;
      }
      stream.eatWhile(/[\w\.]/);
      return "number";
    }
    if (isOperator.test(ch)) {
      return "operator";
    }
    if (isArrow.test(ch)) {
      return "operator";
    }
    if (isFunction.test(ch)) {
      state.func = true;
      state.prev = false;
      return builtInFuncs[ch] ? "variableName.function.standard" : "variableName.function";
    }
    if (isComment.test(ch)) {
      stream.skipToEnd();
      return "comment";
    }
    if (ch === "∘" && stream.peek() === ".") {
      stream.next();
      return "variableName.function";
    }
    stream.eatWhile(/[\w\$_]/);
    state.prev = true;
    return "keyword";
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNjI0OS5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGNvZGVtaXJyb3IvbGVnYWN5LW1vZGVzL21vZGUvYXBsLmpzIl0sInNvdXJjZXNDb250ZW50IjpbInZhciBidWlsdEluRnVuY3MgPSB7XG4gIFwiK1wiOiBbXCJjb25qdWdhdGVcIiwgXCJhZGRcIl0sXG4gIFwi4oiSXCI6IFtcIm5lZ2F0ZVwiLCBcInN1YnRyYWN0XCJdLFxuICBcIsOXXCI6IFtcInNpZ25PZlwiLCBcIm11bHRpcGx5XCJdLFxuICBcIsO3XCI6IFtcInJlY2lwcm9jYWxcIiwgXCJkaXZpZGVcIl0sXG4gIFwi4oyIXCI6IFtcImNlaWxpbmdcIiwgXCJncmVhdGVyT2ZcIl0sXG4gIFwi4oyKXCI6IFtcImZsb29yXCIsIFwibGVzc2VyT2ZcIl0sXG4gIFwi4oijXCI6IFtcImFic29sdXRlXCIsIFwicmVzaWR1ZVwiXSxcbiAgXCLijbNcIjogW1wiaW5kZXhHZW5lcmF0ZVwiLCBcImluZGV4T2ZcIl0sXG4gIFwiP1wiOiBbXCJyb2xsXCIsIFwiZGVhbFwiXSxcbiAgXCLii4ZcIjogW1wiZXhwb25lbnRpYXRlXCIsIFwidG9UaGVQb3dlck9mXCJdLFxuICBcIuKNn1wiOiBbXCJuYXR1cmFsTG9nXCIsIFwibG9nVG9UaGVCYXNlXCJdLFxuICBcIuKXi1wiOiBbXCJwaVRpbWVzXCIsIFwiY2lyY3VsYXJGdW5jc1wiXSxcbiAgXCIhXCI6IFtcImZhY3RvcmlhbFwiLCBcImJpbm9taWFsXCJdLFxuICBcIuKMuVwiOiBbXCJtYXRyaXhJbnZlcnNlXCIsIFwibWF0cml4RGl2aWRlXCJdLFxuICBcIjxcIjogW251bGwsIFwibGVzc1RoYW5cIl0sXG4gIFwi4omkXCI6IFtudWxsLCBcImxlc3NUaGFuT3JFcXVhbFwiXSxcbiAgXCI9XCI6IFtudWxsLCBcImVxdWFsc1wiXSxcbiAgXCI+XCI6IFtudWxsLCBcImdyZWF0ZXJUaGFuXCJdLFxuICBcIuKJpVwiOiBbbnVsbCwgXCJncmVhdGVyVGhhbk9yRXF1YWxcIl0sXG4gIFwi4omgXCI6IFtudWxsLCBcIm5vdEVxdWFsXCJdLFxuICBcIuKJoVwiOiBbXCJkZXB0aFwiLCBcIm1hdGNoXCJdLFxuICBcIuKJolwiOiBbbnVsbCwgXCJub3RNYXRjaFwiXSxcbiAgXCLiiIhcIjogW1wiZW5saXN0XCIsIFwibWVtYmVyc2hpcFwiXSxcbiAgXCLijbdcIjogW251bGwsIFwiZmluZFwiXSxcbiAgXCLiiKpcIjogW1widW5pcXVlXCIsIFwidW5pb25cIl0sXG4gIFwi4oipXCI6IFtudWxsLCBcImludGVyc2VjdGlvblwiXSxcbiAgXCLiiLxcIjogW1wibm90XCIsIFwid2l0aG91dFwiXSxcbiAgXCLiiKhcIjogW251bGwsIFwib3JcIl0sXG4gIFwi4oinXCI6IFtudWxsLCBcImFuZFwiXSxcbiAgXCLijbFcIjogW251bGwsIFwibm9yXCJdLFxuICBcIuKNslwiOiBbbnVsbCwgXCJuYW5kXCJdLFxuICBcIuKNtFwiOiBbXCJzaGFwZU9mXCIsIFwicmVzaGFwZVwiXSxcbiAgXCIsXCI6IFtcInJhdmVsXCIsIFwiY2F0ZW5hdGVcIl0sXG4gIFwi4o2qXCI6IFtudWxsLCBcImZpcnN0QXhpc0NhdGVuYXRlXCJdLFxuICBcIuKMvVwiOiBbXCJyZXZlcnNlXCIsIFwicm90YXRlXCJdLFxuICBcIuKKllwiOiBbXCJheGlzMVJldmVyc2VcIiwgXCJheGlzMVJvdGF0ZVwiXSxcbiAgXCLijYlcIjogW1widHJhbnNwb3NlXCIsIG51bGxdLFxuICBcIuKGkVwiOiBbXCJmaXJzdFwiLCBcInRha2VcIl0sXG4gIFwi4oaTXCI6IFtudWxsLCBcImRyb3BcIl0sXG4gIFwi4oqCXCI6IFtcImVuY2xvc2VcIiwgXCJwYXJ0aXRpb25XaXRoQXhpc1wiXSxcbiAgXCLiioNcIjogW1wiZGljbG9zZVwiLCBcInBpY2tcIl0sXG4gIFwi4oy3XCI6IFtudWxsLCBcImluZGV4XCJdLFxuICBcIuKNi1wiOiBbXCJncmFkZVVwXCIsIG51bGxdLFxuICBcIuKNklwiOiBbXCJncmFkZURvd25cIiwgbnVsbF0sXG4gIFwi4oqkXCI6IFtcImVuY29kZVwiLCBudWxsXSxcbiAgXCLiiqVcIjogW1wiZGVjb2RlXCIsIG51bGxdLFxuICBcIuKNlVwiOiBbXCJmb3JtYXRcIiwgXCJmb3JtYXRCeUV4YW1wbGVcIl0sXG4gIFwi4o2OXCI6IFtcImV4ZWN1dGVcIiwgbnVsbF0sXG4gIFwi4oqjXCI6IFtcInN0b3BcIiwgXCJsZWZ0XCJdLFxuICBcIuKKolwiOiBbXCJwYXNzXCIsIFwicmlnaHRcIl1cbn07XG52YXIgaXNPcGVyYXRvciA9IC9bXFwuXFwv4oy/4o2AwqjijaNdLztcbnZhciBpc05pbGFkaWMgPSAv4o2sLztcbnZhciBpc0Z1bmN0aW9uID0gL1tcXCviiJLDl8O34oyI4oyK4oij4o2zXFw/4ouG4o2f4peLIeKMuTziiaQ9PuKJpeKJoOKJoeKJouKIiOKNt+KIquKIqeKIvOKIqOKIp+KNseKNsuKNtCzijarijL3iipbijYnihpHihpPiioLiioPijLfijYvijZLiiqTiiqXijZXijY7iiqPiiqJdLztcbnZhciBpc0Fycm93ID0gL+KGkC87XG52YXIgaXNDb21tZW50ID0gL1vijZ0jXS4qJC87XG52YXIgc3RyaW5nRWF0ZXIgPSBmdW5jdGlvbiAodHlwZSkge1xuICB2YXIgcHJldjtcbiAgcHJldiA9IGZhbHNlO1xuICByZXR1cm4gZnVuY3Rpb24gKGMpIHtcbiAgICBwcmV2ID0gYztcbiAgICBpZiAoYyA9PT0gdHlwZSkge1xuICAgICAgcmV0dXJuIHByZXYgPT09IFwiXFxcXFwiO1xuICAgIH1cbiAgICByZXR1cm4gdHJ1ZTtcbiAgfTtcbn07XG5leHBvcnQgY29uc3QgYXBsID0ge1xuICBuYW1lOiBcImFwbFwiLFxuICBzdGFydFN0YXRlOiBmdW5jdGlvbiAoKSB7XG4gICAgcmV0dXJuIHtcbiAgICAgIHByZXY6IGZhbHNlLFxuICAgICAgZnVuYzogZmFsc2UsXG4gICAgICBvcDogZmFsc2UsXG4gICAgICBzdHJpbmc6IGZhbHNlLFxuICAgICAgZXNjYXBlOiBmYWxzZVxuICAgIH07XG4gIH0sXG4gIHRva2VuOiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIHZhciBjaDtcbiAgICBpZiAoc3RyZWFtLmVhdFNwYWNlKCkpIHtcbiAgICAgIHJldHVybiBudWxsO1xuICAgIH1cbiAgICBjaCA9IHN0cmVhbS5uZXh0KCk7XG4gICAgaWYgKGNoID09PSAnXCInIHx8IGNoID09PSBcIidcIikge1xuICAgICAgc3RyZWFtLmVhdFdoaWxlKHN0cmluZ0VhdGVyKGNoKSk7XG4gICAgICBzdHJlYW0ubmV4dCgpO1xuICAgICAgc3RhdGUucHJldiA9IHRydWU7XG4gICAgICByZXR1cm4gXCJzdHJpbmdcIjtcbiAgICB9XG4gICAgaWYgKC9bXFxbe1xcKF0vLnRlc3QoY2gpKSB7XG4gICAgICBzdGF0ZS5wcmV2ID0gZmFsc2U7XG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9XG4gICAgaWYgKC9bXFxdfVxcKV0vLnRlc3QoY2gpKSB7XG4gICAgICBzdGF0ZS5wcmV2ID0gdHJ1ZTtcbiAgICAgIHJldHVybiBudWxsO1xuICAgIH1cbiAgICBpZiAoaXNOaWxhZGljLnRlc3QoY2gpKSB7XG4gICAgICBzdGF0ZS5wcmV2ID0gZmFsc2U7XG4gICAgICByZXR1cm4gXCJhdG9tXCI7XG4gICAgfVxuICAgIGlmICgvW8KvXFxkXS8udGVzdChjaCkpIHtcbiAgICAgIGlmIChzdGF0ZS5mdW5jKSB7XG4gICAgICAgIHN0YXRlLmZ1bmMgPSBmYWxzZTtcbiAgICAgICAgc3RhdGUucHJldiA9IGZhbHNlO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgc3RhdGUucHJldiA9IHRydWU7XG4gICAgICB9XG4gICAgICBzdHJlYW0uZWF0V2hpbGUoL1tcXHdcXC5dLyk7XG4gICAgICByZXR1cm4gXCJudW1iZXJcIjtcbiAgICB9XG4gICAgaWYgKGlzT3BlcmF0b3IudGVzdChjaCkpIHtcbiAgICAgIHJldHVybiBcIm9wZXJhdG9yXCI7XG4gICAgfVxuICAgIGlmIChpc0Fycm93LnRlc3QoY2gpKSB7XG4gICAgICByZXR1cm4gXCJvcGVyYXRvclwiO1xuICAgIH1cbiAgICBpZiAoaXNGdW5jdGlvbi50ZXN0KGNoKSkge1xuICAgICAgc3RhdGUuZnVuYyA9IHRydWU7XG4gICAgICBzdGF0ZS5wcmV2ID0gZmFsc2U7XG4gICAgICByZXR1cm4gYnVpbHRJbkZ1bmNzW2NoXSA/IFwidmFyaWFibGVOYW1lLmZ1bmN0aW9uLnN0YW5kYXJkXCIgOiBcInZhcmlhYmxlTmFtZS5mdW5jdGlvblwiO1xuICAgIH1cbiAgICBpZiAoaXNDb21tZW50LnRlc3QoY2gpKSB7XG4gICAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgICByZXR1cm4gXCJjb21tZW50XCI7XG4gICAgfVxuICAgIGlmIChjaCA9PT0gXCLiiJhcIiAmJiBzdHJlYW0ucGVlaygpID09PSBcIi5cIikge1xuICAgICAgc3RyZWFtLm5leHQoKTtcbiAgICAgIHJldHVybiBcInZhcmlhYmxlTmFtZS5mdW5jdGlvblwiO1xuICAgIH1cbiAgICBzdHJlYW0uZWF0V2hpbGUoL1tcXHdcXCRfXS8pO1xuICAgIHN0YXRlLnByZXYgPSB0cnVlO1xuICAgIHJldHVybiBcImtleXdvcmRcIjtcbiAgfVxufTsiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=