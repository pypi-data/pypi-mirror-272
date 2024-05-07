"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[5853],{

/***/ 25853:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "properties": () => (/* binding */ properties)
/* harmony export */ });
const properties = {
  name: "properties",
  token: function (stream, state) {
    var sol = stream.sol() || state.afterSection;
    var eol = stream.eol();
    state.afterSection = false;
    if (sol) {
      if (state.nextMultiline) {
        state.inMultiline = true;
        state.nextMultiline = false;
      } else {
        state.position = "def";
      }
    }
    if (eol && !state.nextMultiline) {
      state.inMultiline = false;
      state.position = "def";
    }
    if (sol) {
      while (stream.eatSpace()) {}
    }
    var ch = stream.next();
    if (sol && (ch === "#" || ch === "!" || ch === ";")) {
      state.position = "comment";
      stream.skipToEnd();
      return "comment";
    } else if (sol && ch === "[") {
      state.afterSection = true;
      stream.skipTo("]");
      stream.eat("]");
      return "header";
    } else if (ch === "=" || ch === ":") {
      state.position = "quote";
      return null;
    } else if (ch === "\\" && state.position === "quote") {
      if (stream.eol()) {
        // end of line?
        // Multiline value
        state.nextMultiline = true;
      }
    }
    return state.position;
  },
  startState: function () {
    return {
      position: "def",
      // Current position, "def", "quote" or "comment"
      nextMultiline: false,
      // Is the next line multiline value
      inMultiline: false,
      // Is the current line a multiline value
      afterSection: false // Did we just open a section
    };
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNTg1My5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL0Bjb2RlbWlycm9yL2xlZ2FjeS1tb2Rlcy9tb2RlL3Byb3BlcnRpZXMuanMiXSwic291cmNlc0NvbnRlbnQiOlsiZXhwb3J0IGNvbnN0IHByb3BlcnRpZXMgPSB7XG4gIG5hbWU6IFwicHJvcGVydGllc1wiLFxuICB0b2tlbjogZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICB2YXIgc29sID0gc3RyZWFtLnNvbCgpIHx8IHN0YXRlLmFmdGVyU2VjdGlvbjtcbiAgICB2YXIgZW9sID0gc3RyZWFtLmVvbCgpO1xuICAgIHN0YXRlLmFmdGVyU2VjdGlvbiA9IGZhbHNlO1xuICAgIGlmIChzb2wpIHtcbiAgICAgIGlmIChzdGF0ZS5uZXh0TXVsdGlsaW5lKSB7XG4gICAgICAgIHN0YXRlLmluTXVsdGlsaW5lID0gdHJ1ZTtcbiAgICAgICAgc3RhdGUubmV4dE11bHRpbGluZSA9IGZhbHNlO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgc3RhdGUucG9zaXRpb24gPSBcImRlZlwiO1xuICAgICAgfVxuICAgIH1cbiAgICBpZiAoZW9sICYmICFzdGF0ZS5uZXh0TXVsdGlsaW5lKSB7XG4gICAgICBzdGF0ZS5pbk11bHRpbGluZSA9IGZhbHNlO1xuICAgICAgc3RhdGUucG9zaXRpb24gPSBcImRlZlwiO1xuICAgIH1cbiAgICBpZiAoc29sKSB7XG4gICAgICB3aGlsZSAoc3RyZWFtLmVhdFNwYWNlKCkpIHt9XG4gICAgfVxuICAgIHZhciBjaCA9IHN0cmVhbS5uZXh0KCk7XG4gICAgaWYgKHNvbCAmJiAoY2ggPT09IFwiI1wiIHx8IGNoID09PSBcIiFcIiB8fCBjaCA9PT0gXCI7XCIpKSB7XG4gICAgICBzdGF0ZS5wb3NpdGlvbiA9IFwiY29tbWVudFwiO1xuICAgICAgc3RyZWFtLnNraXBUb0VuZCgpO1xuICAgICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICAgIH0gZWxzZSBpZiAoc29sICYmIGNoID09PSBcIltcIikge1xuICAgICAgc3RhdGUuYWZ0ZXJTZWN0aW9uID0gdHJ1ZTtcbiAgICAgIHN0cmVhbS5za2lwVG8oXCJdXCIpO1xuICAgICAgc3RyZWFtLmVhdChcIl1cIik7XG4gICAgICByZXR1cm4gXCJoZWFkZXJcIjtcbiAgICB9IGVsc2UgaWYgKGNoID09PSBcIj1cIiB8fCBjaCA9PT0gXCI6XCIpIHtcbiAgICAgIHN0YXRlLnBvc2l0aW9uID0gXCJxdW90ZVwiO1xuICAgICAgcmV0dXJuIG51bGw7XG4gICAgfSBlbHNlIGlmIChjaCA9PT0gXCJcXFxcXCIgJiYgc3RhdGUucG9zaXRpb24gPT09IFwicXVvdGVcIikge1xuICAgICAgaWYgKHN0cmVhbS5lb2woKSkge1xuICAgICAgICAvLyBlbmQgb2YgbGluZT9cbiAgICAgICAgLy8gTXVsdGlsaW5lIHZhbHVlXG4gICAgICAgIHN0YXRlLm5leHRNdWx0aWxpbmUgPSB0cnVlO1xuICAgICAgfVxuICAgIH1cbiAgICByZXR1cm4gc3RhdGUucG9zaXRpb247XG4gIH0sXG4gIHN0YXJ0U3RhdGU6IGZ1bmN0aW9uICgpIHtcbiAgICByZXR1cm4ge1xuICAgICAgcG9zaXRpb246IFwiZGVmXCIsXG4gICAgICAvLyBDdXJyZW50IHBvc2l0aW9uLCBcImRlZlwiLCBcInF1b3RlXCIgb3IgXCJjb21tZW50XCJcbiAgICAgIG5leHRNdWx0aWxpbmU6IGZhbHNlLFxuICAgICAgLy8gSXMgdGhlIG5leHQgbGluZSBtdWx0aWxpbmUgdmFsdWVcbiAgICAgIGluTXVsdGlsaW5lOiBmYWxzZSxcbiAgICAgIC8vIElzIHRoZSBjdXJyZW50IGxpbmUgYSBtdWx0aWxpbmUgdmFsdWVcbiAgICAgIGFmdGVyU2VjdGlvbjogZmFsc2UgLy8gRGlkIHdlIGp1c3Qgb3BlbiBhIHNlY3Rpb25cbiAgICB9O1xuICB9XG59OyJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==