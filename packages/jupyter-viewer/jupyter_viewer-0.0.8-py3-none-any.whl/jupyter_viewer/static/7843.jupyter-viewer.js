"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[7843],{

/***/ 37843:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "textile": () => (/* binding */ textile)
/* harmony export */ });
var TOKEN_STYLES = {
  addition: "inserted",
  attributes: "propertyName",
  bold: "strong",
  cite: "keyword",
  code: "monospace",
  definitionList: "list",
  deletion: "deleted",
  div: "punctuation",
  em: "emphasis",
  footnote: "variable",
  footCite: "qualifier",
  header: "heading",
  html: "comment",
  image: "atom",
  italic: "emphasis",
  link: "link",
  linkDefinition: "link",
  list1: "list",
  list2: "list.special",
  list3: "list",
  notextile: "string.special",
  pre: "operator",
  p: "content",
  quote: "bracket",
  span: "quote",
  specialChar: "character",
  strong: "strong",
  sub: "content.special",
  sup: "content.special",
  table: "variableName.special",
  tableHeading: "operator"
};
function startNewLine(stream, state) {
  state.mode = Modes.newLayout;
  state.tableHeading = false;
  if (state.layoutType === "definitionList" && state.spanningLayout && stream.match(RE("definitionListEnd"), false)) state.spanningLayout = false;
}
function handlePhraseModifier(stream, state, ch) {
  if (ch === "_") {
    if (stream.eat("_")) return togglePhraseModifier(stream, state, "italic", /__/, 2);else return togglePhraseModifier(stream, state, "em", /_/, 1);
  }
  if (ch === "*") {
    if (stream.eat("*")) {
      return togglePhraseModifier(stream, state, "bold", /\*\*/, 2);
    }
    return togglePhraseModifier(stream, state, "strong", /\*/, 1);
  }
  if (ch === "[") {
    if (stream.match(/\d+\]/)) state.footCite = true;
    return tokenStyles(state);
  }
  if (ch === "(") {
    var spec = stream.match(/^(r|tm|c)\)/);
    if (spec) return TOKEN_STYLES.specialChar;
  }
  if (ch === "<" && stream.match(/(\w+)[^>]+>[^<]+<\/\1>/)) return TOKEN_STYLES.html;
  if (ch === "?" && stream.eat("?")) return togglePhraseModifier(stream, state, "cite", /\?\?/, 2);
  if (ch === "=" && stream.eat("=")) return togglePhraseModifier(stream, state, "notextile", /==/, 2);
  if (ch === "-" && !stream.eat("-")) return togglePhraseModifier(stream, state, "deletion", /-/, 1);
  if (ch === "+") return togglePhraseModifier(stream, state, "addition", /\+/, 1);
  if (ch === "~") return togglePhraseModifier(stream, state, "sub", /~/, 1);
  if (ch === "^") return togglePhraseModifier(stream, state, "sup", /\^/, 1);
  if (ch === "%") return togglePhraseModifier(stream, state, "span", /%/, 1);
  if (ch === "@") return togglePhraseModifier(stream, state, "code", /@/, 1);
  if (ch === "!") {
    var type = togglePhraseModifier(stream, state, "image", /(?:\([^\)]+\))?!/, 1);
    stream.match(/^:\S+/); // optional Url portion
    return type;
  }
  return tokenStyles(state);
}
function togglePhraseModifier(stream, state, phraseModifier, closeRE, openSize) {
  var charBefore = stream.pos > openSize ? stream.string.charAt(stream.pos - openSize - 1) : null;
  var charAfter = stream.peek();
  if (state[phraseModifier]) {
    if ((!charAfter || /\W/.test(charAfter)) && charBefore && /\S/.test(charBefore)) {
      var type = tokenStyles(state);
      state[phraseModifier] = false;
      return type;
    }
  } else if ((!charBefore || /\W/.test(charBefore)) && charAfter && /\S/.test(charAfter) && stream.match(new RegExp("^.*\\S" + closeRE.source + "(?:\\W|$)"), false)) {
    state[phraseModifier] = true;
    state.mode = Modes.attributes;
  }
  return tokenStyles(state);
}
;
function tokenStyles(state) {
  var disabled = textileDisabled(state);
  if (disabled) return disabled;
  var styles = [];
  if (state.layoutType) styles.push(TOKEN_STYLES[state.layoutType]);
  styles = styles.concat(activeStyles(state, "addition", "bold", "cite", "code", "deletion", "em", "footCite", "image", "italic", "link", "span", "strong", "sub", "sup", "table", "tableHeading"));
  if (state.layoutType === "header") styles.push(TOKEN_STYLES.header + "-" + state.header);
  return styles.length ? styles.join(" ") : null;
}
function textileDisabled(state) {
  var type = state.layoutType;
  switch (type) {
    case "notextile":
    case "code":
    case "pre":
      return TOKEN_STYLES[type];
    default:
      if (state.notextile) return TOKEN_STYLES.notextile + (type ? " " + TOKEN_STYLES[type] : "");
      return null;
  }
}
function activeStyles(state) {
  var styles = [];
  for (var i = 1; i < arguments.length; ++i) {
    if (state[arguments[i]]) styles.push(TOKEN_STYLES[arguments[i]]);
  }
  return styles;
}
function blankLine(state) {
  var spanningLayout = state.spanningLayout,
    type = state.layoutType;
  for (var key in state) if (state.hasOwnProperty(key)) delete state[key];
  state.mode = Modes.newLayout;
  if (spanningLayout) {
    state.layoutType = type;
    state.spanningLayout = true;
  }
}
var REs = {
  cache: {},
  single: {
    bc: "bc",
    bq: "bq",
    definitionList: /- .*?:=+/,
    definitionListEnd: /.*=:\s*$/,
    div: "div",
    drawTable: /\|.*\|/,
    foot: /fn\d+/,
    header: /h[1-6]/,
    html: /\s*<(?:\/)?(\w+)(?:[^>]+)?>(?:[^<]+<\/\1>)?/,
    link: /[^"]+":\S/,
    linkDefinition: /\[[^\s\]]+\]\S+/,
    list: /(?:#+|\*+)/,
    notextile: "notextile",
    para: "p",
    pre: "pre",
    table: "table",
    tableCellAttributes: /[\/\\]\d+/,
    tableHeading: /\|_\./,
    tableText: /[^"_\*\[\(\?\+~\^%@|-]+/,
    text: /[^!"_=\*\[\(<\?\+~\^%@-]+/
  },
  attributes: {
    align: /(?:<>|<|>|=)/,
    selector: /\([^\(][^\)]+\)/,
    lang: /\[[^\[\]]+\]/,
    pad: /(?:\(+|\)+){1,2}/,
    css: /\{[^\}]+\}/
  },
  createRe: function (name) {
    switch (name) {
      case "drawTable":
        return REs.makeRe("^", REs.single.drawTable, "$");
      case "html":
        return REs.makeRe("^", REs.single.html, "(?:", REs.single.html, ")*", "$");
      case "linkDefinition":
        return REs.makeRe("^", REs.single.linkDefinition, "$");
      case "listLayout":
        return REs.makeRe("^", REs.single.list, RE("allAttributes"), "*\\s+");
      case "tableCellAttributes":
        return REs.makeRe("^", REs.choiceRe(REs.single.tableCellAttributes, RE("allAttributes")), "+\\.");
      case "type":
        return REs.makeRe("^", RE("allTypes"));
      case "typeLayout":
        return REs.makeRe("^", RE("allTypes"), RE("allAttributes"), "*\\.\\.?", "(\\s+|$)");
      case "attributes":
        return REs.makeRe("^", RE("allAttributes"), "+");
      case "allTypes":
        return REs.choiceRe(REs.single.div, REs.single.foot, REs.single.header, REs.single.bc, REs.single.bq, REs.single.notextile, REs.single.pre, REs.single.table, REs.single.para);
      case "allAttributes":
        return REs.choiceRe(REs.attributes.selector, REs.attributes.css, REs.attributes.lang, REs.attributes.align, REs.attributes.pad);
      default:
        return REs.makeRe("^", REs.single[name]);
    }
  },
  makeRe: function () {
    var pattern = "";
    for (var i = 0; i < arguments.length; ++i) {
      var arg = arguments[i];
      pattern += typeof arg === "string" ? arg : arg.source;
    }
    return new RegExp(pattern);
  },
  choiceRe: function () {
    var parts = [arguments[0]];
    for (var i = 1; i < arguments.length; ++i) {
      parts[i * 2 - 1] = "|";
      parts[i * 2] = arguments[i];
    }
    parts.unshift("(?:");
    parts.push(")");
    return REs.makeRe.apply(null, parts);
  }
};
function RE(name) {
  return REs.cache[name] || (REs.cache[name] = REs.createRe(name));
}
var Modes = {
  newLayout: function (stream, state) {
    if (stream.match(RE("typeLayout"), false)) {
      state.spanningLayout = false;
      return (state.mode = Modes.blockType)(stream, state);
    }
    var newMode;
    if (!textileDisabled(state)) {
      if (stream.match(RE("listLayout"), false)) newMode = Modes.list;else if (stream.match(RE("drawTable"), false)) newMode = Modes.table;else if (stream.match(RE("linkDefinition"), false)) newMode = Modes.linkDefinition;else if (stream.match(RE("definitionList"))) newMode = Modes.definitionList;else if (stream.match(RE("html"), false)) newMode = Modes.html;
    }
    return (state.mode = newMode || Modes.text)(stream, state);
  },
  blockType: function (stream, state) {
    var match, type;
    state.layoutType = null;
    if (match = stream.match(RE("type"))) type = match[0];else return (state.mode = Modes.text)(stream, state);
    if (match = type.match(RE("header"))) {
      state.layoutType = "header";
      state.header = parseInt(match[0][1]);
    } else if (type.match(RE("bq"))) {
      state.layoutType = "quote";
    } else if (type.match(RE("bc"))) {
      state.layoutType = "code";
    } else if (type.match(RE("foot"))) {
      state.layoutType = "footnote";
    } else if (type.match(RE("notextile"))) {
      state.layoutType = "notextile";
    } else if (type.match(RE("pre"))) {
      state.layoutType = "pre";
    } else if (type.match(RE("div"))) {
      state.layoutType = "div";
    } else if (type.match(RE("table"))) {
      state.layoutType = "table";
    }
    state.mode = Modes.attributes;
    return tokenStyles(state);
  },
  text: function (stream, state) {
    if (stream.match(RE("text"))) return tokenStyles(state);
    var ch = stream.next();
    if (ch === '"') return (state.mode = Modes.link)(stream, state);
    return handlePhraseModifier(stream, state, ch);
  },
  attributes: function (stream, state) {
    state.mode = Modes.layoutLength;
    if (stream.match(RE("attributes"))) return TOKEN_STYLES.attributes;else return tokenStyles(state);
  },
  layoutLength: function (stream, state) {
    if (stream.eat(".") && stream.eat(".")) state.spanningLayout = true;
    state.mode = Modes.text;
    return tokenStyles(state);
  },
  list: function (stream, state) {
    var match = stream.match(RE("list"));
    state.listDepth = match[0].length;
    var listMod = (state.listDepth - 1) % 3;
    if (!listMod) state.layoutType = "list1";else if (listMod === 1) state.layoutType = "list2";else state.layoutType = "list3";
    state.mode = Modes.attributes;
    return tokenStyles(state);
  },
  link: function (stream, state) {
    state.mode = Modes.text;
    if (stream.match(RE("link"))) {
      stream.match(/\S+/);
      return TOKEN_STYLES.link;
    }
    return tokenStyles(state);
  },
  linkDefinition: function (stream) {
    stream.skipToEnd();
    return TOKEN_STYLES.linkDefinition;
  },
  definitionList: function (stream, state) {
    stream.match(RE("definitionList"));
    state.layoutType = "definitionList";
    if (stream.match(/\s*$/)) state.spanningLayout = true;else state.mode = Modes.attributes;
    return tokenStyles(state);
  },
  html: function (stream) {
    stream.skipToEnd();
    return TOKEN_STYLES.html;
  },
  table: function (stream, state) {
    state.layoutType = "table";
    return (state.mode = Modes.tableCell)(stream, state);
  },
  tableCell: function (stream, state) {
    if (stream.match(RE("tableHeading"))) state.tableHeading = true;else stream.eat("|");
    state.mode = Modes.tableCellAttributes;
    return tokenStyles(state);
  },
  tableCellAttributes: function (stream, state) {
    state.mode = Modes.tableText;
    if (stream.match(RE("tableCellAttributes"))) return TOKEN_STYLES.attributes;else return tokenStyles(state);
  },
  tableText: function (stream, state) {
    if (stream.match(RE("tableText"))) return tokenStyles(state);
    if (stream.peek() === "|") {
      // end of cell
      state.mode = Modes.tableCell;
      return tokenStyles(state);
    }
    return handlePhraseModifier(stream, state, stream.next());
  }
};
const textile = {
  name: "textile",
  startState: function () {
    return {
      mode: Modes.newLayout
    };
  },
  token: function (stream, state) {
    if (stream.sol()) startNewLine(stream, state);
    return state.mode(stream, state);
  },
  blankLine: blankLine
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNzg0My5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGNvZGVtaXJyb3IvbGVnYWN5LW1vZGVzL21vZGUvdGV4dGlsZS5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyJ2YXIgVE9LRU5fU1RZTEVTID0ge1xuICBhZGRpdGlvbjogXCJpbnNlcnRlZFwiLFxuICBhdHRyaWJ1dGVzOiBcInByb3BlcnR5TmFtZVwiLFxuICBib2xkOiBcInN0cm9uZ1wiLFxuICBjaXRlOiBcImtleXdvcmRcIixcbiAgY29kZTogXCJtb25vc3BhY2VcIixcbiAgZGVmaW5pdGlvbkxpc3Q6IFwibGlzdFwiLFxuICBkZWxldGlvbjogXCJkZWxldGVkXCIsXG4gIGRpdjogXCJwdW5jdHVhdGlvblwiLFxuICBlbTogXCJlbXBoYXNpc1wiLFxuICBmb290bm90ZTogXCJ2YXJpYWJsZVwiLFxuICBmb290Q2l0ZTogXCJxdWFsaWZpZXJcIixcbiAgaGVhZGVyOiBcImhlYWRpbmdcIixcbiAgaHRtbDogXCJjb21tZW50XCIsXG4gIGltYWdlOiBcImF0b21cIixcbiAgaXRhbGljOiBcImVtcGhhc2lzXCIsXG4gIGxpbms6IFwibGlua1wiLFxuICBsaW5rRGVmaW5pdGlvbjogXCJsaW5rXCIsXG4gIGxpc3QxOiBcImxpc3RcIixcbiAgbGlzdDI6IFwibGlzdC5zcGVjaWFsXCIsXG4gIGxpc3QzOiBcImxpc3RcIixcbiAgbm90ZXh0aWxlOiBcInN0cmluZy5zcGVjaWFsXCIsXG4gIHByZTogXCJvcGVyYXRvclwiLFxuICBwOiBcImNvbnRlbnRcIixcbiAgcXVvdGU6IFwiYnJhY2tldFwiLFxuICBzcGFuOiBcInF1b3RlXCIsXG4gIHNwZWNpYWxDaGFyOiBcImNoYXJhY3RlclwiLFxuICBzdHJvbmc6IFwic3Ryb25nXCIsXG4gIHN1YjogXCJjb250ZW50LnNwZWNpYWxcIixcbiAgc3VwOiBcImNvbnRlbnQuc3BlY2lhbFwiLFxuICB0YWJsZTogXCJ2YXJpYWJsZU5hbWUuc3BlY2lhbFwiLFxuICB0YWJsZUhlYWRpbmc6IFwib3BlcmF0b3JcIlxufTtcbmZ1bmN0aW9uIHN0YXJ0TmV3TGluZShzdHJlYW0sIHN0YXRlKSB7XG4gIHN0YXRlLm1vZGUgPSBNb2Rlcy5uZXdMYXlvdXQ7XG4gIHN0YXRlLnRhYmxlSGVhZGluZyA9IGZhbHNlO1xuICBpZiAoc3RhdGUubGF5b3V0VHlwZSA9PT0gXCJkZWZpbml0aW9uTGlzdFwiICYmIHN0YXRlLnNwYW5uaW5nTGF5b3V0ICYmIHN0cmVhbS5tYXRjaChSRShcImRlZmluaXRpb25MaXN0RW5kXCIpLCBmYWxzZSkpIHN0YXRlLnNwYW5uaW5nTGF5b3V0ID0gZmFsc2U7XG59XG5mdW5jdGlvbiBoYW5kbGVQaHJhc2VNb2RpZmllcihzdHJlYW0sIHN0YXRlLCBjaCkge1xuICBpZiAoY2ggPT09IFwiX1wiKSB7XG4gICAgaWYgKHN0cmVhbS5lYXQoXCJfXCIpKSByZXR1cm4gdG9nZ2xlUGhyYXNlTW9kaWZpZXIoc3RyZWFtLCBzdGF0ZSwgXCJpdGFsaWNcIiwgL19fLywgMik7ZWxzZSByZXR1cm4gdG9nZ2xlUGhyYXNlTW9kaWZpZXIoc3RyZWFtLCBzdGF0ZSwgXCJlbVwiLCAvXy8sIDEpO1xuICB9XG4gIGlmIChjaCA9PT0gXCIqXCIpIHtcbiAgICBpZiAoc3RyZWFtLmVhdChcIipcIikpIHtcbiAgICAgIHJldHVybiB0b2dnbGVQaHJhc2VNb2RpZmllcihzdHJlYW0sIHN0YXRlLCBcImJvbGRcIiwgL1xcKlxcKi8sIDIpO1xuICAgIH1cbiAgICByZXR1cm4gdG9nZ2xlUGhyYXNlTW9kaWZpZXIoc3RyZWFtLCBzdGF0ZSwgXCJzdHJvbmdcIiwgL1xcKi8sIDEpO1xuICB9XG4gIGlmIChjaCA9PT0gXCJbXCIpIHtcbiAgICBpZiAoc3RyZWFtLm1hdGNoKC9cXGQrXFxdLykpIHN0YXRlLmZvb3RDaXRlID0gdHJ1ZTtcbiAgICByZXR1cm4gdG9rZW5TdHlsZXMoc3RhdGUpO1xuICB9XG4gIGlmIChjaCA9PT0gXCIoXCIpIHtcbiAgICB2YXIgc3BlYyA9IHN0cmVhbS5tYXRjaCgvXihyfHRtfGMpXFwpLyk7XG4gICAgaWYgKHNwZWMpIHJldHVybiBUT0tFTl9TVFlMRVMuc3BlY2lhbENoYXI7XG4gIH1cbiAgaWYgKGNoID09PSBcIjxcIiAmJiBzdHJlYW0ubWF0Y2goLyhcXHcrKVtePl0rPltePF0rPFxcL1xcMT4vKSkgcmV0dXJuIFRPS0VOX1NUWUxFUy5odG1sO1xuICBpZiAoY2ggPT09IFwiP1wiICYmIHN0cmVhbS5lYXQoXCI/XCIpKSByZXR1cm4gdG9nZ2xlUGhyYXNlTW9kaWZpZXIoc3RyZWFtLCBzdGF0ZSwgXCJjaXRlXCIsIC9cXD9cXD8vLCAyKTtcbiAgaWYgKGNoID09PSBcIj1cIiAmJiBzdHJlYW0uZWF0KFwiPVwiKSkgcmV0dXJuIHRvZ2dsZVBocmFzZU1vZGlmaWVyKHN0cmVhbSwgc3RhdGUsIFwibm90ZXh0aWxlXCIsIC89PS8sIDIpO1xuICBpZiAoY2ggPT09IFwiLVwiICYmICFzdHJlYW0uZWF0KFwiLVwiKSkgcmV0dXJuIHRvZ2dsZVBocmFzZU1vZGlmaWVyKHN0cmVhbSwgc3RhdGUsIFwiZGVsZXRpb25cIiwgLy0vLCAxKTtcbiAgaWYgKGNoID09PSBcIitcIikgcmV0dXJuIHRvZ2dsZVBocmFzZU1vZGlmaWVyKHN0cmVhbSwgc3RhdGUsIFwiYWRkaXRpb25cIiwgL1xcKy8sIDEpO1xuICBpZiAoY2ggPT09IFwiflwiKSByZXR1cm4gdG9nZ2xlUGhyYXNlTW9kaWZpZXIoc3RyZWFtLCBzdGF0ZSwgXCJzdWJcIiwgL34vLCAxKTtcbiAgaWYgKGNoID09PSBcIl5cIikgcmV0dXJuIHRvZ2dsZVBocmFzZU1vZGlmaWVyKHN0cmVhbSwgc3RhdGUsIFwic3VwXCIsIC9cXF4vLCAxKTtcbiAgaWYgKGNoID09PSBcIiVcIikgcmV0dXJuIHRvZ2dsZVBocmFzZU1vZGlmaWVyKHN0cmVhbSwgc3RhdGUsIFwic3BhblwiLCAvJS8sIDEpO1xuICBpZiAoY2ggPT09IFwiQFwiKSByZXR1cm4gdG9nZ2xlUGhyYXNlTW9kaWZpZXIoc3RyZWFtLCBzdGF0ZSwgXCJjb2RlXCIsIC9ALywgMSk7XG4gIGlmIChjaCA9PT0gXCIhXCIpIHtcbiAgICB2YXIgdHlwZSA9IHRvZ2dsZVBocmFzZU1vZGlmaWVyKHN0cmVhbSwgc3RhdGUsIFwiaW1hZ2VcIiwgLyg/OlxcKFteXFwpXStcXCkpPyEvLCAxKTtcbiAgICBzdHJlYW0ubWF0Y2goL146XFxTKy8pOyAvLyBvcHRpb25hbCBVcmwgcG9ydGlvblxuICAgIHJldHVybiB0eXBlO1xuICB9XG4gIHJldHVybiB0b2tlblN0eWxlcyhzdGF0ZSk7XG59XG5mdW5jdGlvbiB0b2dnbGVQaHJhc2VNb2RpZmllcihzdHJlYW0sIHN0YXRlLCBwaHJhc2VNb2RpZmllciwgY2xvc2VSRSwgb3BlblNpemUpIHtcbiAgdmFyIGNoYXJCZWZvcmUgPSBzdHJlYW0ucG9zID4gb3BlblNpemUgPyBzdHJlYW0uc3RyaW5nLmNoYXJBdChzdHJlYW0ucG9zIC0gb3BlblNpemUgLSAxKSA6IG51bGw7XG4gIHZhciBjaGFyQWZ0ZXIgPSBzdHJlYW0ucGVlaygpO1xuICBpZiAoc3RhdGVbcGhyYXNlTW9kaWZpZXJdKSB7XG4gICAgaWYgKCghY2hhckFmdGVyIHx8IC9cXFcvLnRlc3QoY2hhckFmdGVyKSkgJiYgY2hhckJlZm9yZSAmJiAvXFxTLy50ZXN0KGNoYXJCZWZvcmUpKSB7XG4gICAgICB2YXIgdHlwZSA9IHRva2VuU3R5bGVzKHN0YXRlKTtcbiAgICAgIHN0YXRlW3BocmFzZU1vZGlmaWVyXSA9IGZhbHNlO1xuICAgICAgcmV0dXJuIHR5cGU7XG4gICAgfVxuICB9IGVsc2UgaWYgKCghY2hhckJlZm9yZSB8fCAvXFxXLy50ZXN0KGNoYXJCZWZvcmUpKSAmJiBjaGFyQWZ0ZXIgJiYgL1xcUy8udGVzdChjaGFyQWZ0ZXIpICYmIHN0cmVhbS5tYXRjaChuZXcgUmVnRXhwKFwiXi4qXFxcXFNcIiArIGNsb3NlUkUuc291cmNlICsgXCIoPzpcXFxcV3wkKVwiKSwgZmFsc2UpKSB7XG4gICAgc3RhdGVbcGhyYXNlTW9kaWZpZXJdID0gdHJ1ZTtcbiAgICBzdGF0ZS5tb2RlID0gTW9kZXMuYXR0cmlidXRlcztcbiAgfVxuICByZXR1cm4gdG9rZW5TdHlsZXMoc3RhdGUpO1xufVxuO1xuZnVuY3Rpb24gdG9rZW5TdHlsZXMoc3RhdGUpIHtcbiAgdmFyIGRpc2FibGVkID0gdGV4dGlsZURpc2FibGVkKHN0YXRlKTtcbiAgaWYgKGRpc2FibGVkKSByZXR1cm4gZGlzYWJsZWQ7XG4gIHZhciBzdHlsZXMgPSBbXTtcbiAgaWYgKHN0YXRlLmxheW91dFR5cGUpIHN0eWxlcy5wdXNoKFRPS0VOX1NUWUxFU1tzdGF0ZS5sYXlvdXRUeXBlXSk7XG4gIHN0eWxlcyA9IHN0eWxlcy5jb25jYXQoYWN0aXZlU3R5bGVzKHN0YXRlLCBcImFkZGl0aW9uXCIsIFwiYm9sZFwiLCBcImNpdGVcIiwgXCJjb2RlXCIsIFwiZGVsZXRpb25cIiwgXCJlbVwiLCBcImZvb3RDaXRlXCIsIFwiaW1hZ2VcIiwgXCJpdGFsaWNcIiwgXCJsaW5rXCIsIFwic3BhblwiLCBcInN0cm9uZ1wiLCBcInN1YlwiLCBcInN1cFwiLCBcInRhYmxlXCIsIFwidGFibGVIZWFkaW5nXCIpKTtcbiAgaWYgKHN0YXRlLmxheW91dFR5cGUgPT09IFwiaGVhZGVyXCIpIHN0eWxlcy5wdXNoKFRPS0VOX1NUWUxFUy5oZWFkZXIgKyBcIi1cIiArIHN0YXRlLmhlYWRlcik7XG4gIHJldHVybiBzdHlsZXMubGVuZ3RoID8gc3R5bGVzLmpvaW4oXCIgXCIpIDogbnVsbDtcbn1cbmZ1bmN0aW9uIHRleHRpbGVEaXNhYmxlZChzdGF0ZSkge1xuICB2YXIgdHlwZSA9IHN0YXRlLmxheW91dFR5cGU7XG4gIHN3aXRjaCAodHlwZSkge1xuICAgIGNhc2UgXCJub3RleHRpbGVcIjpcbiAgICBjYXNlIFwiY29kZVwiOlxuICAgIGNhc2UgXCJwcmVcIjpcbiAgICAgIHJldHVybiBUT0tFTl9TVFlMRVNbdHlwZV07XG4gICAgZGVmYXVsdDpcbiAgICAgIGlmIChzdGF0ZS5ub3RleHRpbGUpIHJldHVybiBUT0tFTl9TVFlMRVMubm90ZXh0aWxlICsgKHR5cGUgPyBcIiBcIiArIFRPS0VOX1NUWUxFU1t0eXBlXSA6IFwiXCIpO1xuICAgICAgcmV0dXJuIG51bGw7XG4gIH1cbn1cbmZ1bmN0aW9uIGFjdGl2ZVN0eWxlcyhzdGF0ZSkge1xuICB2YXIgc3R5bGVzID0gW107XG4gIGZvciAodmFyIGkgPSAxOyBpIDwgYXJndW1lbnRzLmxlbmd0aDsgKytpKSB7XG4gICAgaWYgKHN0YXRlW2FyZ3VtZW50c1tpXV0pIHN0eWxlcy5wdXNoKFRPS0VOX1NUWUxFU1thcmd1bWVudHNbaV1dKTtcbiAgfVxuICByZXR1cm4gc3R5bGVzO1xufVxuZnVuY3Rpb24gYmxhbmtMaW5lKHN0YXRlKSB7XG4gIHZhciBzcGFubmluZ0xheW91dCA9IHN0YXRlLnNwYW5uaW5nTGF5b3V0LFxuICAgIHR5cGUgPSBzdGF0ZS5sYXlvdXRUeXBlO1xuICBmb3IgKHZhciBrZXkgaW4gc3RhdGUpIGlmIChzdGF0ZS5oYXNPd25Qcm9wZXJ0eShrZXkpKSBkZWxldGUgc3RhdGVba2V5XTtcbiAgc3RhdGUubW9kZSA9IE1vZGVzLm5ld0xheW91dDtcbiAgaWYgKHNwYW5uaW5nTGF5b3V0KSB7XG4gICAgc3RhdGUubGF5b3V0VHlwZSA9IHR5cGU7XG4gICAgc3RhdGUuc3Bhbm5pbmdMYXlvdXQgPSB0cnVlO1xuICB9XG59XG52YXIgUkVzID0ge1xuICBjYWNoZToge30sXG4gIHNpbmdsZToge1xuICAgIGJjOiBcImJjXCIsXG4gICAgYnE6IFwiYnFcIixcbiAgICBkZWZpbml0aW9uTGlzdDogLy0gLio/Oj0rLyxcbiAgICBkZWZpbml0aW9uTGlzdEVuZDogLy4qPTpcXHMqJC8sXG4gICAgZGl2OiBcImRpdlwiLFxuICAgIGRyYXdUYWJsZTogL1xcfC4qXFx8LyxcbiAgICBmb290OiAvZm5cXGQrLyxcbiAgICBoZWFkZXI6IC9oWzEtNl0vLFxuICAgIGh0bWw6IC9cXHMqPCg/OlxcLyk/KFxcdyspKD86W14+XSspPz4oPzpbXjxdKzxcXC9cXDE+KT8vLFxuICAgIGxpbms6IC9bXlwiXStcIjpcXFMvLFxuICAgIGxpbmtEZWZpbml0aW9uOiAvXFxbW15cXHNcXF1dK1xcXVxcUysvLFxuICAgIGxpc3Q6IC8oPzojK3xcXCorKS8sXG4gICAgbm90ZXh0aWxlOiBcIm5vdGV4dGlsZVwiLFxuICAgIHBhcmE6IFwicFwiLFxuICAgIHByZTogXCJwcmVcIixcbiAgICB0YWJsZTogXCJ0YWJsZVwiLFxuICAgIHRhYmxlQ2VsbEF0dHJpYnV0ZXM6IC9bXFwvXFxcXF1cXGQrLyxcbiAgICB0YWJsZUhlYWRpbmc6IC9cXHxfXFwuLyxcbiAgICB0YWJsZVRleHQ6IC9bXlwiX1xcKlxcW1xcKFxcP1xcK35cXF4lQHwtXSsvLFxuICAgIHRleHQ6IC9bXiFcIl89XFwqXFxbXFwoPFxcP1xcK35cXF4lQC1dKy9cbiAgfSxcbiAgYXR0cmlidXRlczoge1xuICAgIGFsaWduOiAvKD86PD58PHw+fD0pLyxcbiAgICBzZWxlY3RvcjogL1xcKFteXFwoXVteXFwpXStcXCkvLFxuICAgIGxhbmc6IC9cXFtbXlxcW1xcXV0rXFxdLyxcbiAgICBwYWQ6IC8oPzpcXCgrfFxcKSspezEsMn0vLFxuICAgIGNzczogL1xce1teXFx9XStcXH0vXG4gIH0sXG4gIGNyZWF0ZVJlOiBmdW5jdGlvbiAobmFtZSkge1xuICAgIHN3aXRjaCAobmFtZSkge1xuICAgICAgY2FzZSBcImRyYXdUYWJsZVwiOlxuICAgICAgICByZXR1cm4gUkVzLm1ha2VSZShcIl5cIiwgUkVzLnNpbmdsZS5kcmF3VGFibGUsIFwiJFwiKTtcbiAgICAgIGNhc2UgXCJodG1sXCI6XG4gICAgICAgIHJldHVybiBSRXMubWFrZVJlKFwiXlwiLCBSRXMuc2luZ2xlLmh0bWwsIFwiKD86XCIsIFJFcy5zaW5nbGUuaHRtbCwgXCIpKlwiLCBcIiRcIik7XG4gICAgICBjYXNlIFwibGlua0RlZmluaXRpb25cIjpcbiAgICAgICAgcmV0dXJuIFJFcy5tYWtlUmUoXCJeXCIsIFJFcy5zaW5nbGUubGlua0RlZmluaXRpb24sIFwiJFwiKTtcbiAgICAgIGNhc2UgXCJsaXN0TGF5b3V0XCI6XG4gICAgICAgIHJldHVybiBSRXMubWFrZVJlKFwiXlwiLCBSRXMuc2luZ2xlLmxpc3QsIFJFKFwiYWxsQXR0cmlidXRlc1wiKSwgXCIqXFxcXHMrXCIpO1xuICAgICAgY2FzZSBcInRhYmxlQ2VsbEF0dHJpYnV0ZXNcIjpcbiAgICAgICAgcmV0dXJuIFJFcy5tYWtlUmUoXCJeXCIsIFJFcy5jaG9pY2VSZShSRXMuc2luZ2xlLnRhYmxlQ2VsbEF0dHJpYnV0ZXMsIFJFKFwiYWxsQXR0cmlidXRlc1wiKSksIFwiK1xcXFwuXCIpO1xuICAgICAgY2FzZSBcInR5cGVcIjpcbiAgICAgICAgcmV0dXJuIFJFcy5tYWtlUmUoXCJeXCIsIFJFKFwiYWxsVHlwZXNcIikpO1xuICAgICAgY2FzZSBcInR5cGVMYXlvdXRcIjpcbiAgICAgICAgcmV0dXJuIFJFcy5tYWtlUmUoXCJeXCIsIFJFKFwiYWxsVHlwZXNcIiksIFJFKFwiYWxsQXR0cmlidXRlc1wiKSwgXCIqXFxcXC5cXFxcLj9cIiwgXCIoXFxcXHMrfCQpXCIpO1xuICAgICAgY2FzZSBcImF0dHJpYnV0ZXNcIjpcbiAgICAgICAgcmV0dXJuIFJFcy5tYWtlUmUoXCJeXCIsIFJFKFwiYWxsQXR0cmlidXRlc1wiKSwgXCIrXCIpO1xuICAgICAgY2FzZSBcImFsbFR5cGVzXCI6XG4gICAgICAgIHJldHVybiBSRXMuY2hvaWNlUmUoUkVzLnNpbmdsZS5kaXYsIFJFcy5zaW5nbGUuZm9vdCwgUkVzLnNpbmdsZS5oZWFkZXIsIFJFcy5zaW5nbGUuYmMsIFJFcy5zaW5nbGUuYnEsIFJFcy5zaW5nbGUubm90ZXh0aWxlLCBSRXMuc2luZ2xlLnByZSwgUkVzLnNpbmdsZS50YWJsZSwgUkVzLnNpbmdsZS5wYXJhKTtcbiAgICAgIGNhc2UgXCJhbGxBdHRyaWJ1dGVzXCI6XG4gICAgICAgIHJldHVybiBSRXMuY2hvaWNlUmUoUkVzLmF0dHJpYnV0ZXMuc2VsZWN0b3IsIFJFcy5hdHRyaWJ1dGVzLmNzcywgUkVzLmF0dHJpYnV0ZXMubGFuZywgUkVzLmF0dHJpYnV0ZXMuYWxpZ24sIFJFcy5hdHRyaWJ1dGVzLnBhZCk7XG4gICAgICBkZWZhdWx0OlxuICAgICAgICByZXR1cm4gUkVzLm1ha2VSZShcIl5cIiwgUkVzLnNpbmdsZVtuYW1lXSk7XG4gICAgfVxuICB9LFxuICBtYWtlUmU6IGZ1bmN0aW9uICgpIHtcbiAgICB2YXIgcGF0dGVybiA9IFwiXCI7XG4gICAgZm9yICh2YXIgaSA9IDA7IGkgPCBhcmd1bWVudHMubGVuZ3RoOyArK2kpIHtcbiAgICAgIHZhciBhcmcgPSBhcmd1bWVudHNbaV07XG4gICAgICBwYXR0ZXJuICs9IHR5cGVvZiBhcmcgPT09IFwic3RyaW5nXCIgPyBhcmcgOiBhcmcuc291cmNlO1xuICAgIH1cbiAgICByZXR1cm4gbmV3IFJlZ0V4cChwYXR0ZXJuKTtcbiAgfSxcbiAgY2hvaWNlUmU6IGZ1bmN0aW9uICgpIHtcbiAgICB2YXIgcGFydHMgPSBbYXJndW1lbnRzWzBdXTtcbiAgICBmb3IgKHZhciBpID0gMTsgaSA8IGFyZ3VtZW50cy5sZW5ndGg7ICsraSkge1xuICAgICAgcGFydHNbaSAqIDIgLSAxXSA9IFwifFwiO1xuICAgICAgcGFydHNbaSAqIDJdID0gYXJndW1lbnRzW2ldO1xuICAgIH1cbiAgICBwYXJ0cy51bnNoaWZ0KFwiKD86XCIpO1xuICAgIHBhcnRzLnB1c2goXCIpXCIpO1xuICAgIHJldHVybiBSRXMubWFrZVJlLmFwcGx5KG51bGwsIHBhcnRzKTtcbiAgfVxufTtcbmZ1bmN0aW9uIFJFKG5hbWUpIHtcbiAgcmV0dXJuIFJFcy5jYWNoZVtuYW1lXSB8fCAoUkVzLmNhY2hlW25hbWVdID0gUkVzLmNyZWF0ZVJlKG5hbWUpKTtcbn1cbnZhciBNb2RlcyA9IHtcbiAgbmV3TGF5b3V0OiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIGlmIChzdHJlYW0ubWF0Y2goUkUoXCJ0eXBlTGF5b3V0XCIpLCBmYWxzZSkpIHtcbiAgICAgIHN0YXRlLnNwYW5uaW5nTGF5b3V0ID0gZmFsc2U7XG4gICAgICByZXR1cm4gKHN0YXRlLm1vZGUgPSBNb2Rlcy5ibG9ja1R5cGUpKHN0cmVhbSwgc3RhdGUpO1xuICAgIH1cbiAgICB2YXIgbmV3TW9kZTtcbiAgICBpZiAoIXRleHRpbGVEaXNhYmxlZChzdGF0ZSkpIHtcbiAgICAgIGlmIChzdHJlYW0ubWF0Y2goUkUoXCJsaXN0TGF5b3V0XCIpLCBmYWxzZSkpIG5ld01vZGUgPSBNb2Rlcy5saXN0O2Vsc2UgaWYgKHN0cmVhbS5tYXRjaChSRShcImRyYXdUYWJsZVwiKSwgZmFsc2UpKSBuZXdNb2RlID0gTW9kZXMudGFibGU7ZWxzZSBpZiAoc3RyZWFtLm1hdGNoKFJFKFwibGlua0RlZmluaXRpb25cIiksIGZhbHNlKSkgbmV3TW9kZSA9IE1vZGVzLmxpbmtEZWZpbml0aW9uO2Vsc2UgaWYgKHN0cmVhbS5tYXRjaChSRShcImRlZmluaXRpb25MaXN0XCIpKSkgbmV3TW9kZSA9IE1vZGVzLmRlZmluaXRpb25MaXN0O2Vsc2UgaWYgKHN0cmVhbS5tYXRjaChSRShcImh0bWxcIiksIGZhbHNlKSkgbmV3TW9kZSA9IE1vZGVzLmh0bWw7XG4gICAgfVxuICAgIHJldHVybiAoc3RhdGUubW9kZSA9IG5ld01vZGUgfHwgTW9kZXMudGV4dCkoc3RyZWFtLCBzdGF0ZSk7XG4gIH0sXG4gIGJsb2NrVHlwZTogZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICB2YXIgbWF0Y2gsIHR5cGU7XG4gICAgc3RhdGUubGF5b3V0VHlwZSA9IG51bGw7XG4gICAgaWYgKG1hdGNoID0gc3RyZWFtLm1hdGNoKFJFKFwidHlwZVwiKSkpIHR5cGUgPSBtYXRjaFswXTtlbHNlIHJldHVybiAoc3RhdGUubW9kZSA9IE1vZGVzLnRleHQpKHN0cmVhbSwgc3RhdGUpO1xuICAgIGlmIChtYXRjaCA9IHR5cGUubWF0Y2goUkUoXCJoZWFkZXJcIikpKSB7XG4gICAgICBzdGF0ZS5sYXlvdXRUeXBlID0gXCJoZWFkZXJcIjtcbiAgICAgIHN0YXRlLmhlYWRlciA9IHBhcnNlSW50KG1hdGNoWzBdWzFdKTtcbiAgICB9IGVsc2UgaWYgKHR5cGUubWF0Y2goUkUoXCJicVwiKSkpIHtcbiAgICAgIHN0YXRlLmxheW91dFR5cGUgPSBcInF1b3RlXCI7XG4gICAgfSBlbHNlIGlmICh0eXBlLm1hdGNoKFJFKFwiYmNcIikpKSB7XG4gICAgICBzdGF0ZS5sYXlvdXRUeXBlID0gXCJjb2RlXCI7XG4gICAgfSBlbHNlIGlmICh0eXBlLm1hdGNoKFJFKFwiZm9vdFwiKSkpIHtcbiAgICAgIHN0YXRlLmxheW91dFR5cGUgPSBcImZvb3Rub3RlXCI7XG4gICAgfSBlbHNlIGlmICh0eXBlLm1hdGNoKFJFKFwibm90ZXh0aWxlXCIpKSkge1xuICAgICAgc3RhdGUubGF5b3V0VHlwZSA9IFwibm90ZXh0aWxlXCI7XG4gICAgfSBlbHNlIGlmICh0eXBlLm1hdGNoKFJFKFwicHJlXCIpKSkge1xuICAgICAgc3RhdGUubGF5b3V0VHlwZSA9IFwicHJlXCI7XG4gICAgfSBlbHNlIGlmICh0eXBlLm1hdGNoKFJFKFwiZGl2XCIpKSkge1xuICAgICAgc3RhdGUubGF5b3V0VHlwZSA9IFwiZGl2XCI7XG4gICAgfSBlbHNlIGlmICh0eXBlLm1hdGNoKFJFKFwidGFibGVcIikpKSB7XG4gICAgICBzdGF0ZS5sYXlvdXRUeXBlID0gXCJ0YWJsZVwiO1xuICAgIH1cbiAgICBzdGF0ZS5tb2RlID0gTW9kZXMuYXR0cmlidXRlcztcbiAgICByZXR1cm4gdG9rZW5TdHlsZXMoc3RhdGUpO1xuICB9LFxuICB0ZXh0OiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIGlmIChzdHJlYW0ubWF0Y2goUkUoXCJ0ZXh0XCIpKSkgcmV0dXJuIHRva2VuU3R5bGVzKHN0YXRlKTtcbiAgICB2YXIgY2ggPSBzdHJlYW0ubmV4dCgpO1xuICAgIGlmIChjaCA9PT0gJ1wiJykgcmV0dXJuIChzdGF0ZS5tb2RlID0gTW9kZXMubGluaykoc3RyZWFtLCBzdGF0ZSk7XG4gICAgcmV0dXJuIGhhbmRsZVBocmFzZU1vZGlmaWVyKHN0cmVhbSwgc3RhdGUsIGNoKTtcbiAgfSxcbiAgYXR0cmlidXRlczogZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICBzdGF0ZS5tb2RlID0gTW9kZXMubGF5b3V0TGVuZ3RoO1xuICAgIGlmIChzdHJlYW0ubWF0Y2goUkUoXCJhdHRyaWJ1dGVzXCIpKSkgcmV0dXJuIFRPS0VOX1NUWUxFUy5hdHRyaWJ1dGVzO2Vsc2UgcmV0dXJuIHRva2VuU3R5bGVzKHN0YXRlKTtcbiAgfSxcbiAgbGF5b3V0TGVuZ3RoOiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIGlmIChzdHJlYW0uZWF0KFwiLlwiKSAmJiBzdHJlYW0uZWF0KFwiLlwiKSkgc3RhdGUuc3Bhbm5pbmdMYXlvdXQgPSB0cnVlO1xuICAgIHN0YXRlLm1vZGUgPSBNb2Rlcy50ZXh0O1xuICAgIHJldHVybiB0b2tlblN0eWxlcyhzdGF0ZSk7XG4gIH0sXG4gIGxpc3Q6IGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgdmFyIG1hdGNoID0gc3RyZWFtLm1hdGNoKFJFKFwibGlzdFwiKSk7XG4gICAgc3RhdGUubGlzdERlcHRoID0gbWF0Y2hbMF0ubGVuZ3RoO1xuICAgIHZhciBsaXN0TW9kID0gKHN0YXRlLmxpc3REZXB0aCAtIDEpICUgMztcbiAgICBpZiAoIWxpc3RNb2QpIHN0YXRlLmxheW91dFR5cGUgPSBcImxpc3QxXCI7ZWxzZSBpZiAobGlzdE1vZCA9PT0gMSkgc3RhdGUubGF5b3V0VHlwZSA9IFwibGlzdDJcIjtlbHNlIHN0YXRlLmxheW91dFR5cGUgPSBcImxpc3QzXCI7XG4gICAgc3RhdGUubW9kZSA9IE1vZGVzLmF0dHJpYnV0ZXM7XG4gICAgcmV0dXJuIHRva2VuU3R5bGVzKHN0YXRlKTtcbiAgfSxcbiAgbGluazogZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICBzdGF0ZS5tb2RlID0gTW9kZXMudGV4dDtcbiAgICBpZiAoc3RyZWFtLm1hdGNoKFJFKFwibGlua1wiKSkpIHtcbiAgICAgIHN0cmVhbS5tYXRjaCgvXFxTKy8pO1xuICAgICAgcmV0dXJuIFRPS0VOX1NUWUxFUy5saW5rO1xuICAgIH1cbiAgICByZXR1cm4gdG9rZW5TdHlsZXMoc3RhdGUpO1xuICB9LFxuICBsaW5rRGVmaW5pdGlvbjogZnVuY3Rpb24gKHN0cmVhbSkge1xuICAgIHN0cmVhbS5za2lwVG9FbmQoKTtcbiAgICByZXR1cm4gVE9LRU5fU1RZTEVTLmxpbmtEZWZpbml0aW9uO1xuICB9LFxuICBkZWZpbml0aW9uTGlzdDogZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICBzdHJlYW0ubWF0Y2goUkUoXCJkZWZpbml0aW9uTGlzdFwiKSk7XG4gICAgc3RhdGUubGF5b3V0VHlwZSA9IFwiZGVmaW5pdGlvbkxpc3RcIjtcbiAgICBpZiAoc3RyZWFtLm1hdGNoKC9cXHMqJC8pKSBzdGF0ZS5zcGFubmluZ0xheW91dCA9IHRydWU7ZWxzZSBzdGF0ZS5tb2RlID0gTW9kZXMuYXR0cmlidXRlcztcbiAgICByZXR1cm4gdG9rZW5TdHlsZXMoc3RhdGUpO1xuICB9LFxuICBodG1sOiBmdW5jdGlvbiAoc3RyZWFtKSB7XG4gICAgc3RyZWFtLnNraXBUb0VuZCgpO1xuICAgIHJldHVybiBUT0tFTl9TVFlMRVMuaHRtbDtcbiAgfSxcbiAgdGFibGU6IGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgc3RhdGUubGF5b3V0VHlwZSA9IFwidGFibGVcIjtcbiAgICByZXR1cm4gKHN0YXRlLm1vZGUgPSBNb2Rlcy50YWJsZUNlbGwpKHN0cmVhbSwgc3RhdGUpO1xuICB9LFxuICB0YWJsZUNlbGw6IGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgaWYgKHN0cmVhbS5tYXRjaChSRShcInRhYmxlSGVhZGluZ1wiKSkpIHN0YXRlLnRhYmxlSGVhZGluZyA9IHRydWU7ZWxzZSBzdHJlYW0uZWF0KFwifFwiKTtcbiAgICBzdGF0ZS5tb2RlID0gTW9kZXMudGFibGVDZWxsQXR0cmlidXRlcztcbiAgICByZXR1cm4gdG9rZW5TdHlsZXMoc3RhdGUpO1xuICB9LFxuICB0YWJsZUNlbGxBdHRyaWJ1dGVzOiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIHN0YXRlLm1vZGUgPSBNb2Rlcy50YWJsZVRleHQ7XG4gICAgaWYgKHN0cmVhbS5tYXRjaChSRShcInRhYmxlQ2VsbEF0dHJpYnV0ZXNcIikpKSByZXR1cm4gVE9LRU5fU1RZTEVTLmF0dHJpYnV0ZXM7ZWxzZSByZXR1cm4gdG9rZW5TdHlsZXMoc3RhdGUpO1xuICB9LFxuICB0YWJsZVRleHQ6IGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgaWYgKHN0cmVhbS5tYXRjaChSRShcInRhYmxlVGV4dFwiKSkpIHJldHVybiB0b2tlblN0eWxlcyhzdGF0ZSk7XG4gICAgaWYgKHN0cmVhbS5wZWVrKCkgPT09IFwifFwiKSB7XG4gICAgICAvLyBlbmQgb2YgY2VsbFxuICAgICAgc3RhdGUubW9kZSA9IE1vZGVzLnRhYmxlQ2VsbDtcbiAgICAgIHJldHVybiB0b2tlblN0eWxlcyhzdGF0ZSk7XG4gICAgfVxuICAgIHJldHVybiBoYW5kbGVQaHJhc2VNb2RpZmllcihzdHJlYW0sIHN0YXRlLCBzdHJlYW0ubmV4dCgpKTtcbiAgfVxufTtcbmV4cG9ydCBjb25zdCB0ZXh0aWxlID0ge1xuICBuYW1lOiBcInRleHRpbGVcIixcbiAgc3RhcnRTdGF0ZTogZnVuY3Rpb24gKCkge1xuICAgIHJldHVybiB7XG4gICAgICBtb2RlOiBNb2Rlcy5uZXdMYXlvdXRcbiAgICB9O1xuICB9LFxuICB0b2tlbjogZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICBpZiAoc3RyZWFtLnNvbCgpKSBzdGFydE5ld0xpbmUoc3RyZWFtLCBzdGF0ZSk7XG4gICAgcmV0dXJuIHN0YXRlLm1vZGUoc3RyZWFtLCBzdGF0ZSk7XG4gIH0sXG4gIGJsYW5rTGluZTogYmxhbmtMaW5lXG59OyJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==