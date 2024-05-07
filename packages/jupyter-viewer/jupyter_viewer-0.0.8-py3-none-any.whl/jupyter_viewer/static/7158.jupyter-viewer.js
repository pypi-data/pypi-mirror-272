"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[7158],{

/***/ 57158:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "tiddlyWiki": () => (/* binding */ tiddlyWiki)
/* harmony export */ });
// Tokenizer
var textwords = {};
var keywords = {
  "allTags": true,
  "closeAll": true,
  "list": true,
  "newJournal": true,
  "newTiddler": true,
  "permaview": true,
  "saveChanges": true,
  "search": true,
  "slider": true,
  "tabs": true,
  "tag": true,
  "tagging": true,
  "tags": true,
  "tiddler": true,
  "timeline": true,
  "today": true,
  "version": true,
  "option": true,
  "with": true,
  "filter": true
};
var isSpaceName = /[\w_\-]/i,
  reHR = /^\-\-\-\-+$/,
  // <hr>
  reWikiCommentStart = /^\/\*\*\*$/,
  // /***
  reWikiCommentStop = /^\*\*\*\/$/,
  // ***/
  reBlockQuote = /^<<<$/,
  reJsCodeStart = /^\/\/\{\{\{$/,
  // //{{{ js block start
  reJsCodeStop = /^\/\/\}\}\}$/,
  // //}}} js stop
  reXmlCodeStart = /^<!--\{\{\{-->$/,
  // xml block start
  reXmlCodeStop = /^<!--\}\}\}-->$/,
  // xml stop

  reCodeBlockStart = /^\{\{\{$/,
  // {{{ TW text div block start
  reCodeBlockStop = /^\}\}\}$/,
  // }}} TW text stop

  reUntilCodeStop = /.*?\}\}\}/;
function chain(stream, state, f) {
  state.tokenize = f;
  return f(stream, state);
}
function tokenBase(stream, state) {
  var sol = stream.sol(),
    ch = stream.peek();
  state.block = false; // indicates the start of a code block.

  // check start of  blocks
  if (sol && /[<\/\*{}\-]/.test(ch)) {
    if (stream.match(reCodeBlockStart)) {
      state.block = true;
      return chain(stream, state, twTokenCode);
    }
    if (stream.match(reBlockQuote)) return 'quote';
    if (stream.match(reWikiCommentStart) || stream.match(reWikiCommentStop)) return 'comment';
    if (stream.match(reJsCodeStart) || stream.match(reJsCodeStop) || stream.match(reXmlCodeStart) || stream.match(reXmlCodeStop)) return 'comment';
    if (stream.match(reHR)) return 'contentSeparator';
  }
  stream.next();
  if (sol && /[\/\*!#;:>|]/.test(ch)) {
    if (ch == "!") {
      // tw header
      stream.skipToEnd();
      return "header";
    }
    if (ch == "*") {
      // tw list
      stream.eatWhile('*');
      return "comment";
    }
    if (ch == "#") {
      // tw numbered list
      stream.eatWhile('#');
      return "comment";
    }
    if (ch == ";") {
      // definition list, term
      stream.eatWhile(';');
      return "comment";
    }
    if (ch == ":") {
      // definition list, description
      stream.eatWhile(':');
      return "comment";
    }
    if (ch == ">") {
      // single line quote
      stream.eatWhile(">");
      return "quote";
    }
    if (ch == '|') return 'header';
  }
  if (ch == '{' && stream.match('{{')) return chain(stream, state, twTokenCode);

  // rudimentary html:// file:// link matching. TW knows much more ...
  if (/[hf]/i.test(ch) && /[ti]/i.test(stream.peek()) && stream.match(/\b(ttps?|tp|ile):\/\/[\-A-Z0-9+&@#\/%?=~_|$!:,.;]*[A-Z0-9+&@#\/%=~_|$]/i)) return "link";

  // just a little string indicator, don't want to have the whole string covered
  if (ch == '"') return 'string';
  if (ch == '~')
    // _no_ CamelCase indicator should be bold
    return 'brace';
  if (/[\[\]]/.test(ch) && stream.match(ch))
    // check for [[..]]
    return 'brace';
  if (ch == "@") {
    // check for space link. TODO fix @@...@@ highlighting
    stream.eatWhile(isSpaceName);
    return "link";
  }
  if (/\d/.test(ch)) {
    // numbers
    stream.eatWhile(/\d/);
    return "number";
  }
  if (ch == "/") {
    // tw invisible comment
    if (stream.eat("%")) {
      return chain(stream, state, twTokenComment);
    } else if (stream.eat("/")) {
      //
      return chain(stream, state, twTokenEm);
    }
  }
  if (ch == "_" && stream.eat("_"))
    // tw underline
    return chain(stream, state, twTokenUnderline);

  // strikethrough and mdash handling
  if (ch == "-" && stream.eat("-")) {
    // if strikethrough looks ugly, change CSS.
    if (stream.peek() != ' ') return chain(stream, state, twTokenStrike);
    // mdash
    if (stream.peek() == ' ') return 'brace';
  }
  if (ch == "'" && stream.eat("'"))
    // tw bold
    return chain(stream, state, twTokenStrong);
  if (ch == "<" && stream.eat("<"))
    // tw macro
    return chain(stream, state, twTokenMacro);

  // core macro handling
  stream.eatWhile(/[\w\$_]/);
  return textwords.propertyIsEnumerable(stream.current()) ? "keyword" : null;
}

// tw invisible comment
function twTokenComment(stream, state) {
  var maybeEnd = false,
    ch;
  while (ch = stream.next()) {
    if (ch == "/" && maybeEnd) {
      state.tokenize = tokenBase;
      break;
    }
    maybeEnd = ch == "%";
  }
  return "comment";
}

// tw strong / bold
function twTokenStrong(stream, state) {
  var maybeEnd = false,
    ch;
  while (ch = stream.next()) {
    if (ch == "'" && maybeEnd) {
      state.tokenize = tokenBase;
      break;
    }
    maybeEnd = ch == "'";
  }
  return "strong";
}

// tw code
function twTokenCode(stream, state) {
  var sb = state.block;
  if (sb && stream.current()) {
    return "comment";
  }
  if (!sb && stream.match(reUntilCodeStop)) {
    state.tokenize = tokenBase;
    return "comment";
  }
  if (sb && stream.sol() && stream.match(reCodeBlockStop)) {
    state.tokenize = tokenBase;
    return "comment";
  }
  stream.next();
  return "comment";
}

// tw em / italic
function twTokenEm(stream, state) {
  var maybeEnd = false,
    ch;
  while (ch = stream.next()) {
    if (ch == "/" && maybeEnd) {
      state.tokenize = tokenBase;
      break;
    }
    maybeEnd = ch == "/";
  }
  return "emphasis";
}

// tw underlined text
function twTokenUnderline(stream, state) {
  var maybeEnd = false,
    ch;
  while (ch = stream.next()) {
    if (ch == "_" && maybeEnd) {
      state.tokenize = tokenBase;
      break;
    }
    maybeEnd = ch == "_";
  }
  return "link";
}

// tw strike through text looks ugly
// change CSS if needed
function twTokenStrike(stream, state) {
  var maybeEnd = false,
    ch;
  while (ch = stream.next()) {
    if (ch == "-" && maybeEnd) {
      state.tokenize = tokenBase;
      break;
    }
    maybeEnd = ch == "-";
  }
  return "deleted";
}

// macro
function twTokenMacro(stream, state) {
  if (stream.current() == '<<') {
    return 'meta';
  }
  var ch = stream.next();
  if (!ch) {
    state.tokenize = tokenBase;
    return null;
  }
  if (ch == ">") {
    if (stream.peek() == '>') {
      stream.next();
      state.tokenize = tokenBase;
      return "meta";
    }
  }
  stream.eatWhile(/[\w\$_]/);
  return keywords.propertyIsEnumerable(stream.current()) ? "keyword" : null;
}

// Interface
const tiddlyWiki = {
  name: "tiddlywiki",
  startState: function () {
    return {
      tokenize: tokenBase
    };
  },
  token: function (stream, state) {
    if (stream.eatSpace()) return null;
    var style = state.tokenize(stream, state);
    return style;
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNzE1OC5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL0Bjb2RlbWlycm9yL2xlZ2FjeS1tb2Rlcy9tb2RlL3RpZGRseXdpa2kuanMiXSwic291cmNlc0NvbnRlbnQiOlsiLy8gVG9rZW5pemVyXG52YXIgdGV4dHdvcmRzID0ge307XG52YXIga2V5d29yZHMgPSB7XG4gIFwiYWxsVGFnc1wiOiB0cnVlLFxuICBcImNsb3NlQWxsXCI6IHRydWUsXG4gIFwibGlzdFwiOiB0cnVlLFxuICBcIm5ld0pvdXJuYWxcIjogdHJ1ZSxcbiAgXCJuZXdUaWRkbGVyXCI6IHRydWUsXG4gIFwicGVybWF2aWV3XCI6IHRydWUsXG4gIFwic2F2ZUNoYW5nZXNcIjogdHJ1ZSxcbiAgXCJzZWFyY2hcIjogdHJ1ZSxcbiAgXCJzbGlkZXJcIjogdHJ1ZSxcbiAgXCJ0YWJzXCI6IHRydWUsXG4gIFwidGFnXCI6IHRydWUsXG4gIFwidGFnZ2luZ1wiOiB0cnVlLFxuICBcInRhZ3NcIjogdHJ1ZSxcbiAgXCJ0aWRkbGVyXCI6IHRydWUsXG4gIFwidGltZWxpbmVcIjogdHJ1ZSxcbiAgXCJ0b2RheVwiOiB0cnVlLFxuICBcInZlcnNpb25cIjogdHJ1ZSxcbiAgXCJvcHRpb25cIjogdHJ1ZSxcbiAgXCJ3aXRoXCI6IHRydWUsXG4gIFwiZmlsdGVyXCI6IHRydWVcbn07XG52YXIgaXNTcGFjZU5hbWUgPSAvW1xcd19cXC1dL2ksXG4gIHJlSFIgPSAvXlxcLVxcLVxcLVxcLSskLyxcbiAgLy8gPGhyPlxuICByZVdpa2lDb21tZW50U3RhcnQgPSAvXlxcL1xcKlxcKlxcKiQvLFxuICAvLyAvKioqXG4gIHJlV2lraUNvbW1lbnRTdG9wID0gL15cXCpcXCpcXCpcXC8kLyxcbiAgLy8gKioqL1xuICByZUJsb2NrUXVvdGUgPSAvXjw8PCQvLFxuICByZUpzQ29kZVN0YXJ0ID0gL15cXC9cXC9cXHtcXHtcXHskLyxcbiAgLy8gLy97e3sganMgYmxvY2sgc3RhcnRcbiAgcmVKc0NvZGVTdG9wID0gL15cXC9cXC9cXH1cXH1cXH0kLyxcbiAgLy8gLy99fX0ganMgc3RvcFxuICByZVhtbENvZGVTdGFydCA9IC9ePCEtLVxce1xce1xcey0tPiQvLFxuICAvLyB4bWwgYmxvY2sgc3RhcnRcbiAgcmVYbWxDb2RlU3RvcCA9IC9ePCEtLVxcfVxcfVxcfS0tPiQvLFxuICAvLyB4bWwgc3RvcFxuXG4gIHJlQ29kZUJsb2NrU3RhcnQgPSAvXlxce1xce1xceyQvLFxuICAvLyB7e3sgVFcgdGV4dCBkaXYgYmxvY2sgc3RhcnRcbiAgcmVDb2RlQmxvY2tTdG9wID0gL15cXH1cXH1cXH0kLyxcbiAgLy8gfX19IFRXIHRleHQgc3RvcFxuXG4gIHJlVW50aWxDb2RlU3RvcCA9IC8uKj9cXH1cXH1cXH0vO1xuZnVuY3Rpb24gY2hhaW4oc3RyZWFtLCBzdGF0ZSwgZikge1xuICBzdGF0ZS50b2tlbml6ZSA9IGY7XG4gIHJldHVybiBmKHN0cmVhbSwgc3RhdGUpO1xufVxuZnVuY3Rpb24gdG9rZW5CYXNlKHN0cmVhbSwgc3RhdGUpIHtcbiAgdmFyIHNvbCA9IHN0cmVhbS5zb2woKSxcbiAgICBjaCA9IHN0cmVhbS5wZWVrKCk7XG4gIHN0YXRlLmJsb2NrID0gZmFsc2U7IC8vIGluZGljYXRlcyB0aGUgc3RhcnQgb2YgYSBjb2RlIGJsb2NrLlxuXG4gIC8vIGNoZWNrIHN0YXJ0IG9mICBibG9ja3NcbiAgaWYgKHNvbCAmJiAvWzxcXC9cXCp7fVxcLV0vLnRlc3QoY2gpKSB7XG4gICAgaWYgKHN0cmVhbS5tYXRjaChyZUNvZGVCbG9ja1N0YXJ0KSkge1xuICAgICAgc3RhdGUuYmxvY2sgPSB0cnVlO1xuICAgICAgcmV0dXJuIGNoYWluKHN0cmVhbSwgc3RhdGUsIHR3VG9rZW5Db2RlKTtcbiAgICB9XG4gICAgaWYgKHN0cmVhbS5tYXRjaChyZUJsb2NrUXVvdGUpKSByZXR1cm4gJ3F1b3RlJztcbiAgICBpZiAoc3RyZWFtLm1hdGNoKHJlV2lraUNvbW1lbnRTdGFydCkgfHwgc3RyZWFtLm1hdGNoKHJlV2lraUNvbW1lbnRTdG9wKSkgcmV0dXJuICdjb21tZW50JztcbiAgICBpZiAoc3RyZWFtLm1hdGNoKHJlSnNDb2RlU3RhcnQpIHx8IHN0cmVhbS5tYXRjaChyZUpzQ29kZVN0b3ApIHx8IHN0cmVhbS5tYXRjaChyZVhtbENvZGVTdGFydCkgfHwgc3RyZWFtLm1hdGNoKHJlWG1sQ29kZVN0b3ApKSByZXR1cm4gJ2NvbW1lbnQnO1xuICAgIGlmIChzdHJlYW0ubWF0Y2gocmVIUikpIHJldHVybiAnY29udGVudFNlcGFyYXRvcic7XG4gIH1cbiAgc3RyZWFtLm5leHQoKTtcbiAgaWYgKHNvbCAmJiAvW1xcL1xcKiEjOzo+fF0vLnRlc3QoY2gpKSB7XG4gICAgaWYgKGNoID09IFwiIVwiKSB7XG4gICAgICAvLyB0dyBoZWFkZXJcbiAgICAgIHN0cmVhbS5za2lwVG9FbmQoKTtcbiAgICAgIHJldHVybiBcImhlYWRlclwiO1xuICAgIH1cbiAgICBpZiAoY2ggPT0gXCIqXCIpIHtcbiAgICAgIC8vIHR3IGxpc3RcbiAgICAgIHN0cmVhbS5lYXRXaGlsZSgnKicpO1xuICAgICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICAgIH1cbiAgICBpZiAoY2ggPT0gXCIjXCIpIHtcbiAgICAgIC8vIHR3IG51bWJlcmVkIGxpc3RcbiAgICAgIHN0cmVhbS5lYXRXaGlsZSgnIycpO1xuICAgICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICAgIH1cbiAgICBpZiAoY2ggPT0gXCI7XCIpIHtcbiAgICAgIC8vIGRlZmluaXRpb24gbGlzdCwgdGVybVxuICAgICAgc3RyZWFtLmVhdFdoaWxlKCc7Jyk7XG4gICAgICByZXR1cm4gXCJjb21tZW50XCI7XG4gICAgfVxuICAgIGlmIChjaCA9PSBcIjpcIikge1xuICAgICAgLy8gZGVmaW5pdGlvbiBsaXN0LCBkZXNjcmlwdGlvblxuICAgICAgc3RyZWFtLmVhdFdoaWxlKCc6Jyk7XG4gICAgICByZXR1cm4gXCJjb21tZW50XCI7XG4gICAgfVxuICAgIGlmIChjaCA9PSBcIj5cIikge1xuICAgICAgLy8gc2luZ2xlIGxpbmUgcXVvdGVcbiAgICAgIHN0cmVhbS5lYXRXaGlsZShcIj5cIik7XG4gICAgICByZXR1cm4gXCJxdW90ZVwiO1xuICAgIH1cbiAgICBpZiAoY2ggPT0gJ3wnKSByZXR1cm4gJ2hlYWRlcic7XG4gIH1cbiAgaWYgKGNoID09ICd7JyAmJiBzdHJlYW0ubWF0Y2goJ3t7JykpIHJldHVybiBjaGFpbihzdHJlYW0sIHN0YXRlLCB0d1Rva2VuQ29kZSk7XG5cbiAgLy8gcnVkaW1lbnRhcnkgaHRtbDovLyBmaWxlOi8vIGxpbmsgbWF0Y2hpbmcuIFRXIGtub3dzIG11Y2ggbW9yZSAuLi5cbiAgaWYgKC9baGZdL2kudGVzdChjaCkgJiYgL1t0aV0vaS50ZXN0KHN0cmVhbS5wZWVrKCkpICYmIHN0cmVhbS5tYXRjaCgvXFxiKHR0cHM/fHRwfGlsZSk6XFwvXFwvW1xcLUEtWjAtOSsmQCNcXC8lPz1+X3wkITosLjtdKltBLVowLTkrJkAjXFwvJT1+X3wkXS9pKSkgcmV0dXJuIFwibGlua1wiO1xuXG4gIC8vIGp1c3QgYSBsaXR0bGUgc3RyaW5nIGluZGljYXRvciwgZG9uJ3Qgd2FudCB0byBoYXZlIHRoZSB3aG9sZSBzdHJpbmcgY292ZXJlZFxuICBpZiAoY2ggPT0gJ1wiJykgcmV0dXJuICdzdHJpbmcnO1xuICBpZiAoY2ggPT0gJ34nKVxuICAgIC8vIF9ub18gQ2FtZWxDYXNlIGluZGljYXRvciBzaG91bGQgYmUgYm9sZFxuICAgIHJldHVybiAnYnJhY2UnO1xuICBpZiAoL1tcXFtcXF1dLy50ZXN0KGNoKSAmJiBzdHJlYW0ubWF0Y2goY2gpKVxuICAgIC8vIGNoZWNrIGZvciBbWy4uXV1cbiAgICByZXR1cm4gJ2JyYWNlJztcbiAgaWYgKGNoID09IFwiQFwiKSB7XG4gICAgLy8gY2hlY2sgZm9yIHNwYWNlIGxpbmsuIFRPRE8gZml4IEBALi4uQEAgaGlnaGxpZ2h0aW5nXG4gICAgc3RyZWFtLmVhdFdoaWxlKGlzU3BhY2VOYW1lKTtcbiAgICByZXR1cm4gXCJsaW5rXCI7XG4gIH1cbiAgaWYgKC9cXGQvLnRlc3QoY2gpKSB7XG4gICAgLy8gbnVtYmVyc1xuICAgIHN0cmVhbS5lYXRXaGlsZSgvXFxkLyk7XG4gICAgcmV0dXJuIFwibnVtYmVyXCI7XG4gIH1cbiAgaWYgKGNoID09IFwiL1wiKSB7XG4gICAgLy8gdHcgaW52aXNpYmxlIGNvbW1lbnRcbiAgICBpZiAoc3RyZWFtLmVhdChcIiVcIikpIHtcbiAgICAgIHJldHVybiBjaGFpbihzdHJlYW0sIHN0YXRlLCB0d1Rva2VuQ29tbWVudCk7XG4gICAgfSBlbHNlIGlmIChzdHJlYW0uZWF0KFwiL1wiKSkge1xuICAgICAgLy9cbiAgICAgIHJldHVybiBjaGFpbihzdHJlYW0sIHN0YXRlLCB0d1Rva2VuRW0pO1xuICAgIH1cbiAgfVxuICBpZiAoY2ggPT0gXCJfXCIgJiYgc3RyZWFtLmVhdChcIl9cIikpXG4gICAgLy8gdHcgdW5kZXJsaW5lXG4gICAgcmV0dXJuIGNoYWluKHN0cmVhbSwgc3RhdGUsIHR3VG9rZW5VbmRlcmxpbmUpO1xuXG4gIC8vIHN0cmlrZXRocm91Z2ggYW5kIG1kYXNoIGhhbmRsaW5nXG4gIGlmIChjaCA9PSBcIi1cIiAmJiBzdHJlYW0uZWF0KFwiLVwiKSkge1xuICAgIC8vIGlmIHN0cmlrZXRocm91Z2ggbG9va3MgdWdseSwgY2hhbmdlIENTUy5cbiAgICBpZiAoc3RyZWFtLnBlZWsoKSAhPSAnICcpIHJldHVybiBjaGFpbihzdHJlYW0sIHN0YXRlLCB0d1Rva2VuU3RyaWtlKTtcbiAgICAvLyBtZGFzaFxuICAgIGlmIChzdHJlYW0ucGVlaygpID09ICcgJykgcmV0dXJuICdicmFjZSc7XG4gIH1cbiAgaWYgKGNoID09IFwiJ1wiICYmIHN0cmVhbS5lYXQoXCInXCIpKVxuICAgIC8vIHR3IGJvbGRcbiAgICByZXR1cm4gY2hhaW4oc3RyZWFtLCBzdGF0ZSwgdHdUb2tlblN0cm9uZyk7XG4gIGlmIChjaCA9PSBcIjxcIiAmJiBzdHJlYW0uZWF0KFwiPFwiKSlcbiAgICAvLyB0dyBtYWNyb1xuICAgIHJldHVybiBjaGFpbihzdHJlYW0sIHN0YXRlLCB0d1Rva2VuTWFjcm8pO1xuXG4gIC8vIGNvcmUgbWFjcm8gaGFuZGxpbmdcbiAgc3RyZWFtLmVhdFdoaWxlKC9bXFx3XFwkX10vKTtcbiAgcmV0dXJuIHRleHR3b3Jkcy5wcm9wZXJ0eUlzRW51bWVyYWJsZShzdHJlYW0uY3VycmVudCgpKSA/IFwia2V5d29yZFwiIDogbnVsbDtcbn1cblxuLy8gdHcgaW52aXNpYmxlIGNvbW1lbnRcbmZ1bmN0aW9uIHR3VG9rZW5Db21tZW50KHN0cmVhbSwgc3RhdGUpIHtcbiAgdmFyIG1heWJlRW5kID0gZmFsc2UsXG4gICAgY2g7XG4gIHdoaWxlIChjaCA9IHN0cmVhbS5uZXh0KCkpIHtcbiAgICBpZiAoY2ggPT0gXCIvXCIgJiYgbWF5YmVFbmQpIHtcbiAgICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlO1xuICAgICAgYnJlYWs7XG4gICAgfVxuICAgIG1heWJlRW5kID0gY2ggPT0gXCIlXCI7XG4gIH1cbiAgcmV0dXJuIFwiY29tbWVudFwiO1xufVxuXG4vLyB0dyBzdHJvbmcgLyBib2xkXG5mdW5jdGlvbiB0d1Rva2VuU3Ryb25nKHN0cmVhbSwgc3RhdGUpIHtcbiAgdmFyIG1heWJlRW5kID0gZmFsc2UsXG4gICAgY2g7XG4gIHdoaWxlIChjaCA9IHN0cmVhbS5uZXh0KCkpIHtcbiAgICBpZiAoY2ggPT0gXCInXCIgJiYgbWF5YmVFbmQpIHtcbiAgICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlO1xuICAgICAgYnJlYWs7XG4gICAgfVxuICAgIG1heWJlRW5kID0gY2ggPT0gXCInXCI7XG4gIH1cbiAgcmV0dXJuIFwic3Ryb25nXCI7XG59XG5cbi8vIHR3IGNvZGVcbmZ1bmN0aW9uIHR3VG9rZW5Db2RlKHN0cmVhbSwgc3RhdGUpIHtcbiAgdmFyIHNiID0gc3RhdGUuYmxvY2s7XG4gIGlmIChzYiAmJiBzdHJlYW0uY3VycmVudCgpKSB7XG4gICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICB9XG4gIGlmICghc2IgJiYgc3RyZWFtLm1hdGNoKHJlVW50aWxDb2RlU3RvcCkpIHtcbiAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQmFzZTtcbiAgICByZXR1cm4gXCJjb21tZW50XCI7XG4gIH1cbiAgaWYgKHNiICYmIHN0cmVhbS5zb2woKSAmJiBzdHJlYW0ubWF0Y2gocmVDb2RlQmxvY2tTdG9wKSkge1xuICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlO1xuICAgIHJldHVybiBcImNvbW1lbnRcIjtcbiAgfVxuICBzdHJlYW0ubmV4dCgpO1xuICByZXR1cm4gXCJjb21tZW50XCI7XG59XG5cbi8vIHR3IGVtIC8gaXRhbGljXG5mdW5jdGlvbiB0d1Rva2VuRW0oc3RyZWFtLCBzdGF0ZSkge1xuICB2YXIgbWF5YmVFbmQgPSBmYWxzZSxcbiAgICBjaDtcbiAgd2hpbGUgKGNoID0gc3RyZWFtLm5leHQoKSkge1xuICAgIGlmIChjaCA9PSBcIi9cIiAmJiBtYXliZUVuZCkge1xuICAgICAgc3RhdGUudG9rZW5pemUgPSB0b2tlbkJhc2U7XG4gICAgICBicmVhaztcbiAgICB9XG4gICAgbWF5YmVFbmQgPSBjaCA9PSBcIi9cIjtcbiAgfVxuICByZXR1cm4gXCJlbXBoYXNpc1wiO1xufVxuXG4vLyB0dyB1bmRlcmxpbmVkIHRleHRcbmZ1bmN0aW9uIHR3VG9rZW5VbmRlcmxpbmUoc3RyZWFtLCBzdGF0ZSkge1xuICB2YXIgbWF5YmVFbmQgPSBmYWxzZSxcbiAgICBjaDtcbiAgd2hpbGUgKGNoID0gc3RyZWFtLm5leHQoKSkge1xuICAgIGlmIChjaCA9PSBcIl9cIiAmJiBtYXliZUVuZCkge1xuICAgICAgc3RhdGUudG9rZW5pemUgPSB0b2tlbkJhc2U7XG4gICAgICBicmVhaztcbiAgICB9XG4gICAgbWF5YmVFbmQgPSBjaCA9PSBcIl9cIjtcbiAgfVxuICByZXR1cm4gXCJsaW5rXCI7XG59XG5cbi8vIHR3IHN0cmlrZSB0aHJvdWdoIHRleHQgbG9va3MgdWdseVxuLy8gY2hhbmdlIENTUyBpZiBuZWVkZWRcbmZ1bmN0aW9uIHR3VG9rZW5TdHJpa2Uoc3RyZWFtLCBzdGF0ZSkge1xuICB2YXIgbWF5YmVFbmQgPSBmYWxzZSxcbiAgICBjaDtcbiAgd2hpbGUgKGNoID0gc3RyZWFtLm5leHQoKSkge1xuICAgIGlmIChjaCA9PSBcIi1cIiAmJiBtYXliZUVuZCkge1xuICAgICAgc3RhdGUudG9rZW5pemUgPSB0b2tlbkJhc2U7XG4gICAgICBicmVhaztcbiAgICB9XG4gICAgbWF5YmVFbmQgPSBjaCA9PSBcIi1cIjtcbiAgfVxuICByZXR1cm4gXCJkZWxldGVkXCI7XG59XG5cbi8vIG1hY3JvXG5mdW5jdGlvbiB0d1Rva2VuTWFjcm8oc3RyZWFtLCBzdGF0ZSkge1xuICBpZiAoc3RyZWFtLmN1cnJlbnQoKSA9PSAnPDwnKSB7XG4gICAgcmV0dXJuICdtZXRhJztcbiAgfVxuICB2YXIgY2ggPSBzdHJlYW0ubmV4dCgpO1xuICBpZiAoIWNoKSB7XG4gICAgc3RhdGUudG9rZW5pemUgPSB0b2tlbkJhc2U7XG4gICAgcmV0dXJuIG51bGw7XG4gIH1cbiAgaWYgKGNoID09IFwiPlwiKSB7XG4gICAgaWYgKHN0cmVhbS5wZWVrKCkgPT0gJz4nKSB7XG4gICAgICBzdHJlYW0ubmV4dCgpO1xuICAgICAgc3RhdGUudG9rZW5pemUgPSB0b2tlbkJhc2U7XG4gICAgICByZXR1cm4gXCJtZXRhXCI7XG4gICAgfVxuICB9XG4gIHN0cmVhbS5lYXRXaGlsZSgvW1xcd1xcJF9dLyk7XG4gIHJldHVybiBrZXl3b3Jkcy5wcm9wZXJ0eUlzRW51bWVyYWJsZShzdHJlYW0uY3VycmVudCgpKSA/IFwia2V5d29yZFwiIDogbnVsbDtcbn1cblxuLy8gSW50ZXJmYWNlXG5leHBvcnQgY29uc3QgdGlkZGx5V2lraSA9IHtcbiAgbmFtZTogXCJ0aWRkbHl3aWtpXCIsXG4gIHN0YXJ0U3RhdGU6IGZ1bmN0aW9uICgpIHtcbiAgICByZXR1cm4ge1xuICAgICAgdG9rZW5pemU6IHRva2VuQmFzZVxuICAgIH07XG4gIH0sXG4gIHRva2VuOiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIGlmIChzdHJlYW0uZWF0U3BhY2UoKSkgcmV0dXJuIG51bGw7XG4gICAgdmFyIHN0eWxlID0gc3RhdGUudG9rZW5pemUoc3RyZWFtLCBzdGF0ZSk7XG4gICAgcmV0dXJuIHN0eWxlO1xuICB9XG59OyJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==