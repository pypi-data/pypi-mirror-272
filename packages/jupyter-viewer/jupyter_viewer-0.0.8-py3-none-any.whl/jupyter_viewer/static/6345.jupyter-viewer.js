"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[6345],{

/***/ 76345:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "stylus": () => (/* binding */ stylus)
/* harmony export */ });
// developer.mozilla.org/en-US/docs/Web/HTML/Element
var tagKeywords_ = ["a", "abbr", "address", "area", "article", "aside", "audio", "b", "base", "bdi", "bdo", "bgsound", "blockquote", "body", "br", "button", "canvas", "caption", "cite", "code", "col", "colgroup", "data", "datalist", "dd", "del", "details", "dfn", "div", "dl", "dt", "em", "embed", "fieldset", "figcaption", "figure", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "head", "header", "hgroup", "hr", "html", "i", "iframe", "img", "input", "ins", "kbd", "keygen", "label", "legend", "li", "link", "main", "map", "mark", "marquee", "menu", "menuitem", "meta", "meter", "nav", "nobr", "noframes", "noscript", "object", "ol", "optgroup", "option", "output", "p", "param", "pre", "progress", "q", "rp", "rt", "ruby", "s", "samp", "script", "section", "select", "small", "source", "span", "strong", "style", "sub", "summary", "sup", "table", "tbody", "td", "textarea", "tfoot", "th", "thead", "time", "tr", "track", "u", "ul", "var", "video"];

// github.com/codemirror/CodeMirror/blob/master/mode/css/css.js
// Note, "url-prefix" should precede "url" in order to match correctly in documentTypesRegexp
var documentTypes_ = ["domain", "regexp", "url-prefix", "url"];
var mediaTypes_ = ["all", "aural", "braille", "handheld", "print", "projection", "screen", "tty", "tv", "embossed"];
var mediaFeatures_ = ["width", "min-width", "max-width", "height", "min-height", "max-height", "device-width", "min-device-width", "max-device-width", "device-height", "min-device-height", "max-device-height", "aspect-ratio", "min-aspect-ratio", "max-aspect-ratio", "device-aspect-ratio", "min-device-aspect-ratio", "max-device-aspect-ratio", "color", "min-color", "max-color", "color-index", "min-color-index", "max-color-index", "monochrome", "min-monochrome", "max-monochrome", "resolution", "min-resolution", "max-resolution", "scan", "grid", "dynamic-range", "video-dynamic-range"];
var propertyKeywords_ = ["align-content", "align-items", "align-self", "alignment-adjust", "alignment-baseline", "anchor-point", "animation", "animation-delay", "animation-direction", "animation-duration", "animation-fill-mode", "animation-iteration-count", "animation-name", "animation-play-state", "animation-timing-function", "appearance", "azimuth", "backface-visibility", "background", "background-attachment", "background-clip", "background-color", "background-image", "background-origin", "background-position", "background-repeat", "background-size", "baseline-shift", "binding", "bleed", "bookmark-label", "bookmark-level", "bookmark-state", "bookmark-target", "border", "border-bottom", "border-bottom-color", "border-bottom-left-radius", "border-bottom-right-radius", "border-bottom-style", "border-bottom-width", "border-collapse", "border-color", "border-image", "border-image-outset", "border-image-repeat", "border-image-slice", "border-image-source", "border-image-width", "border-left", "border-left-color", "border-left-style", "border-left-width", "border-radius", "border-right", "border-right-color", "border-right-style", "border-right-width", "border-spacing", "border-style", "border-top", "border-top-color", "border-top-left-radius", "border-top-right-radius", "border-top-style", "border-top-width", "border-width", "bottom", "box-decoration-break", "box-shadow", "box-sizing", "break-after", "break-before", "break-inside", "caption-side", "clear", "clip", "color", "color-profile", "column-count", "column-fill", "column-gap", "column-rule", "column-rule-color", "column-rule-style", "column-rule-width", "column-span", "column-width", "columns", "content", "counter-increment", "counter-reset", "crop", "cue", "cue-after", "cue-before", "cursor", "direction", "display", "dominant-baseline", "drop-initial-after-adjust", "drop-initial-after-align", "drop-initial-before-adjust", "drop-initial-before-align", "drop-initial-size", "drop-initial-value", "elevation", "empty-cells", "fit", "fit-position", "flex", "flex-basis", "flex-direction", "flex-flow", "flex-grow", "flex-shrink", "flex-wrap", "float", "float-offset", "flow-from", "flow-into", "font", "font-feature-settings", "font-family", "font-kerning", "font-language-override", "font-size", "font-size-adjust", "font-stretch", "font-style", "font-synthesis", "font-variant", "font-variant-alternates", "font-variant-caps", "font-variant-east-asian", "font-variant-ligatures", "font-variant-numeric", "font-variant-position", "font-weight", "grid", "grid-area", "grid-auto-columns", "grid-auto-flow", "grid-auto-position", "grid-auto-rows", "grid-column", "grid-column-end", "grid-column-start", "grid-row", "grid-row-end", "grid-row-start", "grid-template", "grid-template-areas", "grid-template-columns", "grid-template-rows", "hanging-punctuation", "height", "hyphens", "icon", "image-orientation", "image-rendering", "image-resolution", "inline-box-align", "justify-content", "left", "letter-spacing", "line-break", "line-height", "line-stacking", "line-stacking-ruby", "line-stacking-shift", "line-stacking-strategy", "list-style", "list-style-image", "list-style-position", "list-style-type", "margin", "margin-bottom", "margin-left", "margin-right", "margin-top", "marker-offset", "marks", "marquee-direction", "marquee-loop", "marquee-play-count", "marquee-speed", "marquee-style", "max-height", "max-width", "min-height", "min-width", "move-to", "nav-down", "nav-index", "nav-left", "nav-right", "nav-up", "object-fit", "object-position", "opacity", "order", "orphans", "outline", "outline-color", "outline-offset", "outline-style", "outline-width", "overflow", "overflow-style", "overflow-wrap", "overflow-x", "overflow-y", "padding", "padding-bottom", "padding-left", "padding-right", "padding-top", "page", "page-break-after", "page-break-before", "page-break-inside", "page-policy", "pause", "pause-after", "pause-before", "perspective", "perspective-origin", "pitch", "pitch-range", "play-during", "position", "presentation-level", "punctuation-trim", "quotes", "region-break-after", "region-break-before", "region-break-inside", "region-fragment", "rendering-intent", "resize", "rest", "rest-after", "rest-before", "richness", "right", "rotation", "rotation-point", "ruby-align", "ruby-overhang", "ruby-position", "ruby-span", "shape-image-threshold", "shape-inside", "shape-margin", "shape-outside", "size", "speak", "speak-as", "speak-header", "speak-numeral", "speak-punctuation", "speech-rate", "stress", "string-set", "tab-size", "table-layout", "target", "target-name", "target-new", "target-position", "text-align", "text-align-last", "text-decoration", "text-decoration-color", "text-decoration-line", "text-decoration-skip", "text-decoration-style", "text-emphasis", "text-emphasis-color", "text-emphasis-position", "text-emphasis-style", "text-height", "text-indent", "text-justify", "text-outline", "text-overflow", "text-shadow", "text-size-adjust", "text-space-collapse", "text-transform", "text-underline-position", "text-wrap", "top", "transform", "transform-origin", "transform-style", "transition", "transition-delay", "transition-duration", "transition-property", "transition-timing-function", "unicode-bidi", "vertical-align", "visibility", "voice-balance", "voice-duration", "voice-family", "voice-pitch", "voice-range", "voice-rate", "voice-stress", "voice-volume", "volume", "white-space", "widows", "width", "will-change", "word-break", "word-spacing", "word-wrap", "z-index", "clip-path", "clip-rule", "mask", "enable-background", "filter", "flood-color", "flood-opacity", "lighting-color", "stop-color", "stop-opacity", "pointer-events", "color-interpolation", "color-interpolation-filters", "color-rendering", "fill", "fill-opacity", "fill-rule", "image-rendering", "marker", "marker-end", "marker-mid", "marker-start", "shape-rendering", "stroke", "stroke-dasharray", "stroke-dashoffset", "stroke-linecap", "stroke-linejoin", "stroke-miterlimit", "stroke-opacity", "stroke-width", "text-rendering", "baseline-shift", "dominant-baseline", "glyph-orientation-horizontal", "glyph-orientation-vertical", "text-anchor", "writing-mode", "font-smoothing", "osx-font-smoothing"];
var nonStandardPropertyKeywords_ = ["scrollbar-arrow-color", "scrollbar-base-color", "scrollbar-dark-shadow-color", "scrollbar-face-color", "scrollbar-highlight-color", "scrollbar-shadow-color", "scrollbar-3d-light-color", "scrollbar-track-color", "shape-inside", "searchfield-cancel-button", "searchfield-decoration", "searchfield-results-button", "searchfield-results-decoration", "zoom"];
var fontProperties_ = ["font-family", "src", "unicode-range", "font-variant", "font-feature-settings", "font-stretch", "font-weight", "font-style"];
var colorKeywords_ = ["aliceblue", "antiquewhite", "aqua", "aquamarine", "azure", "beige", "bisque", "black", "blanchedalmond", "blue", "blueviolet", "brown", "burlywood", "cadetblue", "chartreuse", "chocolate", "coral", "cornflowerblue", "cornsilk", "crimson", "cyan", "darkblue", "darkcyan", "darkgoldenrod", "darkgray", "darkgreen", "darkkhaki", "darkmagenta", "darkolivegreen", "darkorange", "darkorchid", "darkred", "darksalmon", "darkseagreen", "darkslateblue", "darkslategray", "darkturquoise", "darkviolet", "deeppink", "deepskyblue", "dimgray", "dodgerblue", "firebrick", "floralwhite", "forestgreen", "fuchsia", "gainsboro", "ghostwhite", "gold", "goldenrod", "gray", "grey", "green", "greenyellow", "honeydew", "hotpink", "indianred", "indigo", "ivory", "khaki", "lavender", "lavenderblush", "lawngreen", "lemonchiffon", "lightblue", "lightcoral", "lightcyan", "lightgoldenrodyellow", "lightgray", "lightgreen", "lightpink", "lightsalmon", "lightseagreen", "lightskyblue", "lightslategray", "lightsteelblue", "lightyellow", "lime", "limegreen", "linen", "magenta", "maroon", "mediumaquamarine", "mediumblue", "mediumorchid", "mediumpurple", "mediumseagreen", "mediumslateblue", "mediumspringgreen", "mediumturquoise", "mediumvioletred", "midnightblue", "mintcream", "mistyrose", "moccasin", "navajowhite", "navy", "oldlace", "olive", "olivedrab", "orange", "orangered", "orchid", "palegoldenrod", "palegreen", "paleturquoise", "palevioletred", "papayawhip", "peachpuff", "peru", "pink", "plum", "powderblue", "purple", "rebeccapurple", "red", "rosybrown", "royalblue", "saddlebrown", "salmon", "sandybrown", "seagreen", "seashell", "sienna", "silver", "skyblue", "slateblue", "slategray", "snow", "springgreen", "steelblue", "tan", "teal", "thistle", "tomato", "turquoise", "violet", "wheat", "white", "whitesmoke", "yellow", "yellowgreen"];
var valueKeywords_ = ["above", "absolute", "activeborder", "additive", "activecaption", "afar", "after-white-space", "ahead", "alias", "all", "all-scroll", "alphabetic", "alternate", "always", "amharic", "amharic-abegede", "antialiased", "appworkspace", "arabic-indic", "armenian", "asterisks", "attr", "auto", "avoid", "avoid-column", "avoid-page", "avoid-region", "background", "backwards", "baseline", "below", "bidi-override", "binary", "bengali", "blink", "block", "block-axis", "bold", "bolder", "border", "border-box", "both", "bottom", "break", "break-all", "break-word", "bullets", "button", "buttonface", "buttonhighlight", "buttonshadow", "buttontext", "calc", "cambodian", "capitalize", "caps-lock-indicator", "caption", "captiontext", "caret", "cell", "center", "checkbox", "circle", "cjk-decimal", "cjk-earthly-branch", "cjk-heavenly-stem", "cjk-ideographic", "clear", "clip", "close-quote", "col-resize", "collapse", "column", "compact", "condensed", "conic-gradient", "contain", "content", "contents", "content-box", "context-menu", "continuous", "copy", "counter", "counters", "cover", "crop", "cross", "crosshair", "currentcolor", "cursive", "cyclic", "dashed", "decimal", "decimal-leading-zero", "default", "default-button", "destination-atop", "destination-in", "destination-out", "destination-over", "devanagari", "disc", "discard", "disclosure-closed", "disclosure-open", "document", "dot-dash", "dot-dot-dash", "dotted", "double", "down", "e-resize", "ease", "ease-in", "ease-in-out", "ease-out", "element", "ellipse", "ellipsis", "embed", "end", "ethiopic", "ethiopic-abegede", "ethiopic-abegede-am-et", "ethiopic-abegede-gez", "ethiopic-abegede-ti-er", "ethiopic-abegede-ti-et", "ethiopic-halehame-aa-er", "ethiopic-halehame-aa-et", "ethiopic-halehame-am-et", "ethiopic-halehame-gez", "ethiopic-halehame-om-et", "ethiopic-halehame-sid-et", "ethiopic-halehame-so-et", "ethiopic-halehame-ti-er", "ethiopic-halehame-ti-et", "ethiopic-halehame-tig", "ethiopic-numeric", "ew-resize", "expanded", "extends", "extra-condensed", "extra-expanded", "fantasy", "fast", "fill", "fixed", "flat", "flex", "footnotes", "forwards", "from", "geometricPrecision", "georgian", "graytext", "groove", "gujarati", "gurmukhi", "hand", "hangul", "hangul-consonant", "hebrew", "help", "hidden", "hide", "high", "higher", "highlight", "highlighttext", "hiragana", "hiragana-iroha", "horizontal", "hsl", "hsla", "icon", "ignore", "inactiveborder", "inactivecaption", "inactivecaptiontext", "infinite", "infobackground", "infotext", "inherit", "initial", "inline", "inline-axis", "inline-block", "inline-flex", "inline-table", "inset", "inside", "intrinsic", "invert", "italic", "japanese-formal", "japanese-informal", "justify", "kannada", "katakana", "katakana-iroha", "keep-all", "khmer", "korean-hangul-formal", "korean-hanja-formal", "korean-hanja-informal", "landscape", "lao", "large", "larger", "left", "level", "lighter", "line-through", "linear", "linear-gradient", "lines", "list-item", "listbox", "listitem", "local", "logical", "loud", "lower", "lower-alpha", "lower-armenian", "lower-greek", "lower-hexadecimal", "lower-latin", "lower-norwegian", "lower-roman", "lowercase", "ltr", "malayalam", "match", "matrix", "matrix3d", "media-play-button", "media-slider", "media-sliderthumb", "media-volume-slider", "media-volume-sliderthumb", "medium", "menu", "menulist", "menulist-button", "menutext", "message-box", "middle", "min-intrinsic", "mix", "mongolian", "monospace", "move", "multiple", "myanmar", "n-resize", "narrower", "ne-resize", "nesw-resize", "no-close-quote", "no-drop", "no-open-quote", "no-repeat", "none", "normal", "not-allowed", "nowrap", "ns-resize", "numbers", "numeric", "nw-resize", "nwse-resize", "oblique", "octal", "open-quote", "optimizeLegibility", "optimizeSpeed", "oriya", "oromo", "outset", "outside", "outside-shape", "overlay", "overline", "padding", "padding-box", "painted", "page", "paused", "persian", "perspective", "plus-darker", "plus-lighter", "pointer", "polygon", "portrait", "pre", "pre-line", "pre-wrap", "preserve-3d", "progress", "push-button", "radial-gradient", "radio", "read-only", "read-write", "read-write-plaintext-only", "rectangle", "region", "relative", "repeat", "repeating-linear-gradient", "repeating-radial-gradient", "repeating-conic-gradient", "repeat-x", "repeat-y", "reset", "reverse", "rgb", "rgba", "ridge", "right", "rotate", "rotate3d", "rotateX", "rotateY", "rotateZ", "round", "row-resize", "rtl", "run-in", "running", "s-resize", "sans-serif", "scale", "scale3d", "scaleX", "scaleY", "scaleZ", "scroll", "scrollbar", "scroll-position", "se-resize", "searchfield", "searchfield-cancel-button", "searchfield-decoration", "searchfield-results-button", "searchfield-results-decoration", "semi-condensed", "semi-expanded", "separate", "serif", "show", "sidama", "simp-chinese-formal", "simp-chinese-informal", "single", "skew", "skewX", "skewY", "skip-white-space", "slide", "slider-horizontal", "slider-vertical", "sliderthumb-horizontal", "sliderthumb-vertical", "slow", "small", "small-caps", "small-caption", "smaller", "solid", "somali", "source-atop", "source-in", "source-out", "source-over", "space", "spell-out", "square", "square-button", "standard", "start", "static", "status-bar", "stretch", "stroke", "sub", "subpixel-antialiased", "super", "sw-resize", "symbolic", "symbols", "table", "table-caption", "table-cell", "table-column", "table-column-group", "table-footer-group", "table-header-group", "table-row", "table-row-group", "tamil", "telugu", "text", "text-bottom", "text-top", "textarea", "textfield", "thai", "thick", "thin", "threeddarkshadow", "threedface", "threedhighlight", "threedlightshadow", "threedshadow", "tibetan", "tigre", "tigrinya-er", "tigrinya-er-abegede", "tigrinya-et", "tigrinya-et-abegede", "to", "top", "trad-chinese-formal", "trad-chinese-informal", "translate", "translate3d", "translateX", "translateY", "translateZ", "transparent", "ultra-condensed", "ultra-expanded", "underline", "up", "upper-alpha", "upper-armenian", "upper-greek", "upper-hexadecimal", "upper-latin", "upper-norwegian", "upper-roman", "uppercase", "urdu", "url", "var", "vertical", "vertical-text", "visible", "visibleFill", "visiblePainted", "visibleStroke", "visual", "w-resize", "wait", "wave", "wider", "window", "windowframe", "windowtext", "words", "x-large", "x-small", "xor", "xx-large", "xx-small", "bicubic", "optimizespeed", "grayscale", "row", "row-reverse", "wrap", "wrap-reverse", "column-reverse", "flex-start", "flex-end", "space-between", "space-around", "unset"];
var wordOperatorKeywords_ = ["in", "and", "or", "not", "is not", "is a", "is", "isnt", "defined", "if unless"],
  blockKeywords_ = ["for", "if", "else", "unless", "from", "to"],
  commonAtoms_ = ["null", "true", "false", "href", "title", "type", "not-allowed", "readonly", "disabled"],
  commonDef_ = ["@font-face", "@keyframes", "@media", "@viewport", "@page", "@host", "@supports", "@block", "@css"];
var hintWords = tagKeywords_.concat(documentTypes_, mediaTypes_, mediaFeatures_, propertyKeywords_, nonStandardPropertyKeywords_, colorKeywords_, valueKeywords_, fontProperties_, wordOperatorKeywords_, blockKeywords_, commonAtoms_, commonDef_);
function wordRegexp(words) {
  words = words.sort(function (a, b) {
    return b > a;
  });
  return new RegExp("^((" + words.join(")|(") + "))\\b");
}
function keySet(array) {
  var keys = {};
  for (var i = 0; i < array.length; ++i) keys[array[i]] = true;
  return keys;
}
function escapeRegExp(text) {
  return text.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, "\\$&");
}
var tagKeywords = keySet(tagKeywords_),
  tagVariablesRegexp = /^(a|b|i|s|col|em)$/i,
  propertyKeywords = keySet(propertyKeywords_),
  nonStandardPropertyKeywords = keySet(nonStandardPropertyKeywords_),
  valueKeywords = keySet(valueKeywords_),
  colorKeywords = keySet(colorKeywords_),
  documentTypes = keySet(documentTypes_),
  documentTypesRegexp = wordRegexp(documentTypes_),
  mediaFeatures = keySet(mediaFeatures_),
  mediaTypes = keySet(mediaTypes_),
  fontProperties = keySet(fontProperties_),
  operatorsRegexp = /^\s*([.]{2,3}|&&|\|\||\*\*|[?!=:]?=|[-+*\/%<>]=?|\?:|\~)/,
  wordOperatorKeywordsRegexp = wordRegexp(wordOperatorKeywords_),
  blockKeywords = keySet(blockKeywords_),
  vendorPrefixesRegexp = new RegExp(/^\-(moz|ms|o|webkit)-/i),
  commonAtoms = keySet(commonAtoms_),
  firstWordMatch = "",
  states = {},
  ch,
  style,
  type,
  override;

/**
 * Tokenizers
 */
function tokenBase(stream, state) {
  firstWordMatch = stream.string.match(/(^[\w-]+\s*=\s*$)|(^\s*[\w-]+\s*=\s*[\w-])|(^\s*(\.|#|@|\$|\&|\[|\d|\+|::?|\{|\>|~|\/)?\s*[\w-]*([a-z0-9-]|\*|\/\*)(\(|,)?)/);
  state.context.line.firstWord = firstWordMatch ? firstWordMatch[0].replace(/^\s*/, "") : "";
  state.context.line.indent = stream.indentation();
  ch = stream.peek();

  // Line comment
  if (stream.match("//")) {
    stream.skipToEnd();
    return ["comment", "comment"];
  }
  // Block comment
  if (stream.match("/*")) {
    state.tokenize = tokenCComment;
    return tokenCComment(stream, state);
  }
  // String
  if (ch == "\"" || ch == "'") {
    stream.next();
    state.tokenize = tokenString(ch);
    return state.tokenize(stream, state);
  }
  // Def
  if (ch == "@") {
    stream.next();
    stream.eatWhile(/[\w\\-]/);
    return ["def", stream.current()];
  }
  // ID selector or Hex color
  if (ch == "#") {
    stream.next();
    // Hex color
    if (stream.match(/^[0-9a-f]{3}([0-9a-f]([0-9a-f]{2}){0,2})?\b(?!-)/i)) {
      return ["atom", "atom"];
    }
    // ID selector
    if (stream.match(/^[a-z][\w-]*/i)) {
      return ["builtin", "hash"];
    }
  }
  // Vendor prefixes
  if (stream.match(vendorPrefixesRegexp)) {
    return ["meta", "vendor-prefixes"];
  }
  // Numbers
  if (stream.match(/^-?[0-9]?\.?[0-9]/)) {
    stream.eatWhile(/[a-z%]/i);
    return ["number", "unit"];
  }
  // !important|optional
  if (ch == "!") {
    stream.next();
    return [stream.match(/^(important|optional)/i) ? "keyword" : "operator", "important"];
  }
  // Class
  if (ch == "." && stream.match(/^\.[a-z][\w-]*/i)) {
    return ["qualifier", "qualifier"];
  }
  // url url-prefix domain regexp
  if (stream.match(documentTypesRegexp)) {
    if (stream.peek() == "(") state.tokenize = tokenParenthesized;
    return ["property", "word"];
  }
  // Mixins / Functions
  if (stream.match(/^[a-z][\w-]*\(/i)) {
    stream.backUp(1);
    return ["keyword", "mixin"];
  }
  // Block mixins
  if (stream.match(/^(\+|-)[a-z][\w-]*\(/i)) {
    stream.backUp(1);
    return ["keyword", "block-mixin"];
  }
  // Parent Reference BEM naming
  if (stream.string.match(/^\s*&/) && stream.match(/^[-_]+[a-z][\w-]*/)) {
    return ["qualifier", "qualifier"];
  }
  // / Root Reference & Parent Reference
  if (stream.match(/^(\/|&)(-|_|:|\.|#|[a-z])/)) {
    stream.backUp(1);
    return ["variableName.special", "reference"];
  }
  if (stream.match(/^&{1}\s*$/)) {
    return ["variableName.special", "reference"];
  }
  // Word operator
  if (stream.match(wordOperatorKeywordsRegexp)) {
    return ["operator", "operator"];
  }
  // Word
  if (stream.match(/^\$?[-_]*[a-z0-9]+[\w-]*/i)) {
    // Variable
    if (stream.match(/^(\.|\[)[\w-\'\"\]]+/i, false)) {
      if (!wordIsTag(stream.current())) {
        stream.match('.');
        return ["variable", "variable-name"];
      }
    }
    return ["variable", "word"];
  }
  // Operators
  if (stream.match(operatorsRegexp)) {
    return ["operator", stream.current()];
  }
  // Delimiters
  if (/[:;,{}\[\]\(\)]/.test(ch)) {
    stream.next();
    return [null, ch];
  }
  // Non-detected items
  stream.next();
  return [null, null];
}

/**
 * Token comment
 */
function tokenCComment(stream, state) {
  var maybeEnd = false,
    ch;
  while ((ch = stream.next()) != null) {
    if (maybeEnd && ch == "/") {
      state.tokenize = null;
      break;
    }
    maybeEnd = ch == "*";
  }
  return ["comment", "comment"];
}

/**
 * Token string
 */
function tokenString(quote) {
  return function (stream, state) {
    var escaped = false,
      ch;
    while ((ch = stream.next()) != null) {
      if (ch == quote && !escaped) {
        if (quote == ")") stream.backUp(1);
        break;
      }
      escaped = !escaped && ch == "\\";
    }
    if (ch == quote || !escaped && quote != ")") state.tokenize = null;
    return ["string", "string"];
  };
}

/**
 * Token parenthesized
 */
function tokenParenthesized(stream, state) {
  stream.next(); // Must be "("
  if (!stream.match(/\s*[\"\')]/, false)) state.tokenize = tokenString(")");else state.tokenize = null;
  return [null, "("];
}

/**
 * Context management
 */
function Context(type, indent, prev, line) {
  this.type = type;
  this.indent = indent;
  this.prev = prev;
  this.line = line || {
    firstWord: "",
    indent: 0
  };
}
function pushContext(state, stream, type, indent) {
  indent = indent >= 0 ? indent : stream.indentUnit;
  state.context = new Context(type, stream.indentation() + indent, state.context);
  return type;
}
function popContext(state, stream, currentIndent) {
  var contextIndent = state.context.indent - stream.indentUnit;
  currentIndent = currentIndent || false;
  state.context = state.context.prev;
  if (currentIndent) state.context.indent = contextIndent;
  return state.context.type;
}
function pass(type, stream, state) {
  return states[state.context.type](type, stream, state);
}
function popAndPass(type, stream, state, n) {
  for (var i = n || 1; i > 0; i--) state.context = state.context.prev;
  return pass(type, stream, state);
}

/**
 * Parser
 */
function wordIsTag(word) {
  return word.toLowerCase() in tagKeywords;
}
function wordIsProperty(word) {
  word = word.toLowerCase();
  return word in propertyKeywords || word in fontProperties;
}
function wordIsBlock(word) {
  return word.toLowerCase() in blockKeywords;
}
function wordIsVendorPrefix(word) {
  return word.toLowerCase().match(vendorPrefixesRegexp);
}
function wordAsValue(word) {
  var wordLC = word.toLowerCase();
  var override = "variable";
  if (wordIsTag(word)) override = "tag";else if (wordIsBlock(word)) override = "block-keyword";else if (wordIsProperty(word)) override = "property";else if (wordLC in valueKeywords || wordLC in commonAtoms) override = "atom";else if (wordLC == "return" || wordLC in colorKeywords) override = "keyword";

  // Font family
  else if (word.match(/^[A-Z]/)) override = "string";
  return override;
}
function typeIsBlock(type, stream) {
  return endOfLine(stream) && (type == "{" || type == "]" || type == "hash" || type == "qualifier") || type == "block-mixin";
}
function typeIsInterpolation(type, stream) {
  return type == "{" && stream.match(/^\s*\$?[\w-]+/i, false);
}
function typeIsPseudo(type, stream) {
  return type == ":" && stream.match(/^[a-z-]+/, false);
}
function startOfLine(stream) {
  return stream.sol() || stream.string.match(new RegExp("^\\s*" + escapeRegExp(stream.current())));
}
function endOfLine(stream) {
  return stream.eol() || stream.match(/^\s*$/, false);
}
function firstWordOfLine(line) {
  var re = /^\s*[-_]*[a-z0-9]+[\w-]*/i;
  var result = typeof line == "string" ? line.match(re) : line.string.match(re);
  return result ? result[0].replace(/^\s*/, "") : "";
}

/**
 * Block
 */
states.block = function (type, stream, state) {
  if (type == "comment" && startOfLine(stream) || type == "," && endOfLine(stream) || type == "mixin") {
    return pushContext(state, stream, "block", 0);
  }
  if (typeIsInterpolation(type, stream)) {
    return pushContext(state, stream, "interpolation");
  }
  if (endOfLine(stream) && type == "]") {
    if (!/^\s*(\.|#|:|\[|\*|&)/.test(stream.string) && !wordIsTag(firstWordOfLine(stream))) {
      return pushContext(state, stream, "block", 0);
    }
  }
  if (typeIsBlock(type, stream)) {
    return pushContext(state, stream, "block");
  }
  if (type == "}" && endOfLine(stream)) {
    return pushContext(state, stream, "block", 0);
  }
  if (type == "variable-name") {
    if (stream.string.match(/^\s?\$[\w-\.\[\]\'\"]+$/) || wordIsBlock(firstWordOfLine(stream))) {
      return pushContext(state, stream, "variableName");
    } else {
      return pushContext(state, stream, "variableName", 0);
    }
  }
  if (type == "=") {
    if (!endOfLine(stream) && !wordIsBlock(firstWordOfLine(stream))) {
      return pushContext(state, stream, "block", 0);
    }
    return pushContext(state, stream, "block");
  }
  if (type == "*") {
    if (endOfLine(stream) || stream.match(/\s*(,|\.|#|\[|:|{)/, false)) {
      override = "tag";
      return pushContext(state, stream, "block");
    }
  }
  if (typeIsPseudo(type, stream)) {
    return pushContext(state, stream, "pseudo");
  }
  if (/@(font-face|media|supports|(-moz-)?document)/.test(type)) {
    return pushContext(state, stream, endOfLine(stream) ? "block" : "atBlock");
  }
  if (/@(-(moz|ms|o|webkit)-)?keyframes$/.test(type)) {
    return pushContext(state, stream, "keyframes");
  }
  if (/@extends?/.test(type)) {
    return pushContext(state, stream, "extend", 0);
  }
  if (type && type.charAt(0) == "@") {
    // Property Lookup
    if (stream.indentation() > 0 && wordIsProperty(stream.current().slice(1))) {
      override = "variable";
      return "block";
    }
    if (/(@import|@require|@charset)/.test(type)) {
      return pushContext(state, stream, "block", 0);
    }
    return pushContext(state, stream, "block");
  }
  if (type == "reference" && endOfLine(stream)) {
    return pushContext(state, stream, "block");
  }
  if (type == "(") {
    return pushContext(state, stream, "parens");
  }
  if (type == "vendor-prefixes") {
    return pushContext(state, stream, "vendorPrefixes");
  }
  if (type == "word") {
    var word = stream.current();
    override = wordAsValue(word);
    if (override == "property") {
      if (startOfLine(stream)) {
        return pushContext(state, stream, "block", 0);
      } else {
        override = "atom";
        return "block";
      }
    }
    if (override == "tag") {
      // tag is a css value
      if (/embed|menu|pre|progress|sub|table/.test(word)) {
        if (wordIsProperty(firstWordOfLine(stream))) {
          override = "atom";
          return "block";
        }
      }

      // tag is an attribute
      if (stream.string.match(new RegExp("\\[\\s*" + word + "|" + word + "\\s*\\]"))) {
        override = "atom";
        return "block";
      }

      // tag is a variable
      if (tagVariablesRegexp.test(word)) {
        if (startOfLine(stream) && stream.string.match(/=/) || !startOfLine(stream) && !stream.string.match(/^(\s*\.|#|\&|\[|\/|>|\*)/) && !wordIsTag(firstWordOfLine(stream))) {
          override = "variable";
          if (wordIsBlock(firstWordOfLine(stream))) return "block";
          return pushContext(state, stream, "block", 0);
        }
      }
      if (endOfLine(stream)) return pushContext(state, stream, "block");
    }
    if (override == "block-keyword") {
      override = "keyword";

      // Postfix conditionals
      if (stream.current(/(if|unless)/) && !startOfLine(stream)) {
        return "block";
      }
      return pushContext(state, stream, "block");
    }
    if (word == "return") return pushContext(state, stream, "block", 0);

    // Placeholder selector
    if (override == "variable" && stream.string.match(/^\s?\$[\w-\.\[\]\'\"]+$/)) {
      return pushContext(state, stream, "block");
    }
  }
  return state.context.type;
};

/**
 * Parens
 */
states.parens = function (type, stream, state) {
  if (type == "(") return pushContext(state, stream, "parens");
  if (type == ")") {
    if (state.context.prev.type == "parens") {
      return popContext(state, stream);
    }
    if (stream.string.match(/^[a-z][\w-]*\(/i) && endOfLine(stream) || wordIsBlock(firstWordOfLine(stream)) || /(\.|#|:|\[|\*|&|>|~|\+|\/)/.test(firstWordOfLine(stream)) || !stream.string.match(/^-?[a-z][\w-\.\[\]\'\"]*\s*=/) && wordIsTag(firstWordOfLine(stream))) {
      return pushContext(state, stream, "block");
    }
    if (stream.string.match(/^[\$-]?[a-z][\w-\.\[\]\'\"]*\s*=/) || stream.string.match(/^\s*(\(|\)|[0-9])/) || stream.string.match(/^\s+[a-z][\w-]*\(/i) || stream.string.match(/^\s+[\$-]?[a-z]/i)) {
      return pushContext(state, stream, "block", 0);
    }
    if (endOfLine(stream)) return pushContext(state, stream, "block");else return pushContext(state, stream, "block", 0);
  }
  if (type && type.charAt(0) == "@" && wordIsProperty(stream.current().slice(1))) {
    override = "variable";
  }
  if (type == "word") {
    var word = stream.current();
    override = wordAsValue(word);
    if (override == "tag" && tagVariablesRegexp.test(word)) {
      override = "variable";
    }
    if (override == "property" || word == "to") override = "atom";
  }
  if (type == "variable-name") {
    return pushContext(state, stream, "variableName");
  }
  if (typeIsPseudo(type, stream)) {
    return pushContext(state, stream, "pseudo");
  }
  return state.context.type;
};

/**
 * Vendor prefixes
 */
states.vendorPrefixes = function (type, stream, state) {
  if (type == "word") {
    override = "property";
    return pushContext(state, stream, "block", 0);
  }
  return popContext(state, stream);
};

/**
 * Pseudo
 */
states.pseudo = function (type, stream, state) {
  if (!wordIsProperty(firstWordOfLine(stream.string))) {
    stream.match(/^[a-z-]+/);
    override = "variableName.special";
    if (endOfLine(stream)) return pushContext(state, stream, "block");
    return popContext(state, stream);
  }
  return popAndPass(type, stream, state);
};

/**
 * atBlock
 */
states.atBlock = function (type, stream, state) {
  if (type == "(") return pushContext(state, stream, "atBlock_parens");
  if (typeIsBlock(type, stream)) {
    return pushContext(state, stream, "block");
  }
  if (typeIsInterpolation(type, stream)) {
    return pushContext(state, stream, "interpolation");
  }
  if (type == "word") {
    var word = stream.current().toLowerCase();
    if (/^(only|not|and|or)$/.test(word)) override = "keyword";else if (documentTypes.hasOwnProperty(word)) override = "tag";else if (mediaTypes.hasOwnProperty(word)) override = "attribute";else if (mediaFeatures.hasOwnProperty(word)) override = "property";else if (nonStandardPropertyKeywords.hasOwnProperty(word)) override = "string.special";else override = wordAsValue(stream.current());
    if (override == "tag" && endOfLine(stream)) {
      return pushContext(state, stream, "block");
    }
  }
  if (type == "operator" && /^(not|and|or)$/.test(stream.current())) {
    override = "keyword";
  }
  return state.context.type;
};
states.atBlock_parens = function (type, stream, state) {
  if (type == "{" || type == "}") return state.context.type;
  if (type == ")") {
    if (endOfLine(stream)) return pushContext(state, stream, "block");else return pushContext(state, stream, "atBlock");
  }
  if (type == "word") {
    var word = stream.current().toLowerCase();
    override = wordAsValue(word);
    if (/^(max|min)/.test(word)) override = "property";
    if (override == "tag") {
      tagVariablesRegexp.test(word) ? override = "variable" : override = "atom";
    }
    return state.context.type;
  }
  return states.atBlock(type, stream, state);
};

/**
 * Keyframes
 */
states.keyframes = function (type, stream, state) {
  if (stream.indentation() == "0" && (type == "}" && startOfLine(stream) || type == "]" || type == "hash" || type == "qualifier" || wordIsTag(stream.current()))) {
    return popAndPass(type, stream, state);
  }
  if (type == "{") return pushContext(state, stream, "keyframes");
  if (type == "}") {
    if (startOfLine(stream)) return popContext(state, stream, true);else return pushContext(state, stream, "keyframes");
  }
  if (type == "unit" && /^[0-9]+\%$/.test(stream.current())) {
    return pushContext(state, stream, "keyframes");
  }
  if (type == "word") {
    override = wordAsValue(stream.current());
    if (override == "block-keyword") {
      override = "keyword";
      return pushContext(state, stream, "keyframes");
    }
  }
  if (/@(font-face|media|supports|(-moz-)?document)/.test(type)) {
    return pushContext(state, stream, endOfLine(stream) ? "block" : "atBlock");
  }
  if (type == "mixin") {
    return pushContext(state, stream, "block", 0);
  }
  return state.context.type;
};

/**
 * Interpolation
 */
states.interpolation = function (type, stream, state) {
  if (type == "{") popContext(state, stream) && pushContext(state, stream, "block");
  if (type == "}") {
    if (stream.string.match(/^\s*(\.|#|:|\[|\*|&|>|~|\+|\/)/i) || stream.string.match(/^\s*[a-z]/i) && wordIsTag(firstWordOfLine(stream))) {
      return pushContext(state, stream, "block");
    }
    if (!stream.string.match(/^(\{|\s*\&)/) || stream.match(/\s*[\w-]/, false)) {
      return pushContext(state, stream, "block", 0);
    }
    return pushContext(state, stream, "block");
  }
  if (type == "variable-name") {
    return pushContext(state, stream, "variableName", 0);
  }
  if (type == "word") {
    override = wordAsValue(stream.current());
    if (override == "tag") override = "atom";
  }
  return state.context.type;
};

/**
 * Extend/s
 */
states.extend = function (type, stream, state) {
  if (type == "[" || type == "=") return "extend";
  if (type == "]") return popContext(state, stream);
  if (type == "word") {
    override = wordAsValue(stream.current());
    return "extend";
  }
  return popContext(state, stream);
};

/**
 * Variable name
 */
states.variableName = function (type, stream, state) {
  if (type == "string" || type == "[" || type == "]" || stream.current().match(/^(\.|\$)/)) {
    if (stream.current().match(/^\.[\w-]+/i)) override = "variable";
    return "variableName";
  }
  return popAndPass(type, stream, state);
};
const stylus = {
  name: "stylus",
  startState: function () {
    return {
      tokenize: null,
      state: "block",
      context: new Context("block", 0, null)
    };
  },
  token: function (stream, state) {
    if (!state.tokenize && stream.eatSpace()) return null;
    style = (state.tokenize || tokenBase)(stream, state);
    if (style && typeof style == "object") {
      type = style[1];
      style = style[0];
    }
    override = style;
    state.state = states[state.state](type, stream, state);
    return override;
  },
  indent: function (state, textAfter, iCx) {
    var cx = state.context,
      ch = textAfter && textAfter.charAt(0),
      indent = cx.indent,
      lineFirstWord = firstWordOfLine(textAfter),
      lineIndent = iCx.lineIndent(iCx.pos),
      prevLineFirstWord = state.context.prev ? state.context.prev.line.firstWord : "",
      prevLineIndent = state.context.prev ? state.context.prev.line.indent : lineIndent;
    if (cx.prev && (ch == "}" && (cx.type == "block" || cx.type == "atBlock" || cx.type == "keyframes") || ch == ")" && (cx.type == "parens" || cx.type == "atBlock_parens") || ch == "{" && cx.type == "at")) {
      indent = cx.indent - iCx.unit;
    } else if (!/(\})/.test(ch)) {
      if (/@|\$|\d/.test(ch) || /^\{/.test(textAfter) || /^\s*\/(\/|\*)/.test(textAfter) || /^\s*\/\*/.test(prevLineFirstWord) || /^\s*[\w-\.\[\]\'\"]+\s*(\?|:|\+)?=/i.test(textAfter) || /^(\+|-)?[a-z][\w-]*\(/i.test(textAfter) || /^return/.test(textAfter) || wordIsBlock(lineFirstWord)) {
        indent = lineIndent;
      } else if (/(\.|#|:|\[|\*|&|>|~|\+|\/)/.test(ch) || wordIsTag(lineFirstWord)) {
        if (/\,\s*$/.test(prevLineFirstWord)) {
          indent = prevLineIndent;
        } else if (!state.sol() && (/(\.|#|:|\[|\*|&|>|~|\+|\/)/.test(prevLineFirstWord) || wordIsTag(prevLineFirstWord))) {
          indent = lineIndent <= prevLineIndent ? prevLineIndent : prevLineIndent + iCx.unit;
        } else {
          indent = lineIndent;
        }
      } else if (!/,\s*$/.test(textAfter) && (wordIsVendorPrefix(lineFirstWord) || wordIsProperty(lineFirstWord))) {
        if (wordIsBlock(prevLineFirstWord)) {
          indent = lineIndent <= prevLineIndent ? prevLineIndent : prevLineIndent + iCx.unit;
        } else if (/^\{/.test(prevLineFirstWord)) {
          indent = lineIndent <= prevLineIndent ? lineIndent : prevLineIndent + iCx.unit;
        } else if (wordIsVendorPrefix(prevLineFirstWord) || wordIsProperty(prevLineFirstWord)) {
          indent = lineIndent >= prevLineIndent ? prevLineIndent : lineIndent;
        } else if (/^(\.|#|:|\[|\*|&|@|\+|\-|>|~|\/)/.test(prevLineFirstWord) || /=\s*$/.test(prevLineFirstWord) || wordIsTag(prevLineFirstWord) || /^\$[\w-\.\[\]\'\"]/.test(prevLineFirstWord)) {
          indent = prevLineIndent + iCx.unit;
        } else {
          indent = lineIndent;
        }
      }
    }
    return indent;
  },
  languageData: {
    indentOnInput: /^\s*\}$/,
    commentTokens: {
      line: "//",
      block: {
        open: "/*",
        close: "*/"
      }
    },
    autocomplete: hintWords
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNjM0NS5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGNvZGVtaXJyb3IvbGVnYWN5LW1vZGVzL21vZGUvc3R5bHVzLmpzIl0sInNvdXJjZXNDb250ZW50IjpbIi8vIGRldmVsb3Blci5tb3ppbGxhLm9yZy9lbi1VUy9kb2NzL1dlYi9IVE1ML0VsZW1lbnRcbnZhciB0YWdLZXl3b3Jkc18gPSBbXCJhXCIsIFwiYWJiclwiLCBcImFkZHJlc3NcIiwgXCJhcmVhXCIsIFwiYXJ0aWNsZVwiLCBcImFzaWRlXCIsIFwiYXVkaW9cIiwgXCJiXCIsIFwiYmFzZVwiLCBcImJkaVwiLCBcImJkb1wiLCBcImJnc291bmRcIiwgXCJibG9ja3F1b3RlXCIsIFwiYm9keVwiLCBcImJyXCIsIFwiYnV0dG9uXCIsIFwiY2FudmFzXCIsIFwiY2FwdGlvblwiLCBcImNpdGVcIiwgXCJjb2RlXCIsIFwiY29sXCIsIFwiY29sZ3JvdXBcIiwgXCJkYXRhXCIsIFwiZGF0YWxpc3RcIiwgXCJkZFwiLCBcImRlbFwiLCBcImRldGFpbHNcIiwgXCJkZm5cIiwgXCJkaXZcIiwgXCJkbFwiLCBcImR0XCIsIFwiZW1cIiwgXCJlbWJlZFwiLCBcImZpZWxkc2V0XCIsIFwiZmlnY2FwdGlvblwiLCBcImZpZ3VyZVwiLCBcImZvb3RlclwiLCBcImZvcm1cIiwgXCJoMVwiLCBcImgyXCIsIFwiaDNcIiwgXCJoNFwiLCBcImg1XCIsIFwiaDZcIiwgXCJoZWFkXCIsIFwiaGVhZGVyXCIsIFwiaGdyb3VwXCIsIFwiaHJcIiwgXCJodG1sXCIsIFwiaVwiLCBcImlmcmFtZVwiLCBcImltZ1wiLCBcImlucHV0XCIsIFwiaW5zXCIsIFwia2JkXCIsIFwia2V5Z2VuXCIsIFwibGFiZWxcIiwgXCJsZWdlbmRcIiwgXCJsaVwiLCBcImxpbmtcIiwgXCJtYWluXCIsIFwibWFwXCIsIFwibWFya1wiLCBcIm1hcnF1ZWVcIiwgXCJtZW51XCIsIFwibWVudWl0ZW1cIiwgXCJtZXRhXCIsIFwibWV0ZXJcIiwgXCJuYXZcIiwgXCJub2JyXCIsIFwibm9mcmFtZXNcIiwgXCJub3NjcmlwdFwiLCBcIm9iamVjdFwiLCBcIm9sXCIsIFwib3B0Z3JvdXBcIiwgXCJvcHRpb25cIiwgXCJvdXRwdXRcIiwgXCJwXCIsIFwicGFyYW1cIiwgXCJwcmVcIiwgXCJwcm9ncmVzc1wiLCBcInFcIiwgXCJycFwiLCBcInJ0XCIsIFwicnVieVwiLCBcInNcIiwgXCJzYW1wXCIsIFwic2NyaXB0XCIsIFwic2VjdGlvblwiLCBcInNlbGVjdFwiLCBcInNtYWxsXCIsIFwic291cmNlXCIsIFwic3BhblwiLCBcInN0cm9uZ1wiLCBcInN0eWxlXCIsIFwic3ViXCIsIFwic3VtbWFyeVwiLCBcInN1cFwiLCBcInRhYmxlXCIsIFwidGJvZHlcIiwgXCJ0ZFwiLCBcInRleHRhcmVhXCIsIFwidGZvb3RcIiwgXCJ0aFwiLCBcInRoZWFkXCIsIFwidGltZVwiLCBcInRyXCIsIFwidHJhY2tcIiwgXCJ1XCIsIFwidWxcIiwgXCJ2YXJcIiwgXCJ2aWRlb1wiXTtcblxuLy8gZ2l0aHViLmNvbS9jb2RlbWlycm9yL0NvZGVNaXJyb3IvYmxvYi9tYXN0ZXIvbW9kZS9jc3MvY3NzLmpzXG4vLyBOb3RlLCBcInVybC1wcmVmaXhcIiBzaG91bGQgcHJlY2VkZSBcInVybFwiIGluIG9yZGVyIHRvIG1hdGNoIGNvcnJlY3RseSBpbiBkb2N1bWVudFR5cGVzUmVnZXhwXG52YXIgZG9jdW1lbnRUeXBlc18gPSBbXCJkb21haW5cIiwgXCJyZWdleHBcIiwgXCJ1cmwtcHJlZml4XCIsIFwidXJsXCJdO1xudmFyIG1lZGlhVHlwZXNfID0gW1wiYWxsXCIsIFwiYXVyYWxcIiwgXCJicmFpbGxlXCIsIFwiaGFuZGhlbGRcIiwgXCJwcmludFwiLCBcInByb2plY3Rpb25cIiwgXCJzY3JlZW5cIiwgXCJ0dHlcIiwgXCJ0dlwiLCBcImVtYm9zc2VkXCJdO1xudmFyIG1lZGlhRmVhdHVyZXNfID0gW1wid2lkdGhcIiwgXCJtaW4td2lkdGhcIiwgXCJtYXgtd2lkdGhcIiwgXCJoZWlnaHRcIiwgXCJtaW4taGVpZ2h0XCIsIFwibWF4LWhlaWdodFwiLCBcImRldmljZS13aWR0aFwiLCBcIm1pbi1kZXZpY2Utd2lkdGhcIiwgXCJtYXgtZGV2aWNlLXdpZHRoXCIsIFwiZGV2aWNlLWhlaWdodFwiLCBcIm1pbi1kZXZpY2UtaGVpZ2h0XCIsIFwibWF4LWRldmljZS1oZWlnaHRcIiwgXCJhc3BlY3QtcmF0aW9cIiwgXCJtaW4tYXNwZWN0LXJhdGlvXCIsIFwibWF4LWFzcGVjdC1yYXRpb1wiLCBcImRldmljZS1hc3BlY3QtcmF0aW9cIiwgXCJtaW4tZGV2aWNlLWFzcGVjdC1yYXRpb1wiLCBcIm1heC1kZXZpY2UtYXNwZWN0LXJhdGlvXCIsIFwiY29sb3JcIiwgXCJtaW4tY29sb3JcIiwgXCJtYXgtY29sb3JcIiwgXCJjb2xvci1pbmRleFwiLCBcIm1pbi1jb2xvci1pbmRleFwiLCBcIm1heC1jb2xvci1pbmRleFwiLCBcIm1vbm9jaHJvbWVcIiwgXCJtaW4tbW9ub2Nocm9tZVwiLCBcIm1heC1tb25vY2hyb21lXCIsIFwicmVzb2x1dGlvblwiLCBcIm1pbi1yZXNvbHV0aW9uXCIsIFwibWF4LXJlc29sdXRpb25cIiwgXCJzY2FuXCIsIFwiZ3JpZFwiLCBcImR5bmFtaWMtcmFuZ2VcIiwgXCJ2aWRlby1keW5hbWljLXJhbmdlXCJdO1xudmFyIHByb3BlcnR5S2V5d29yZHNfID0gW1wiYWxpZ24tY29udGVudFwiLCBcImFsaWduLWl0ZW1zXCIsIFwiYWxpZ24tc2VsZlwiLCBcImFsaWdubWVudC1hZGp1c3RcIiwgXCJhbGlnbm1lbnQtYmFzZWxpbmVcIiwgXCJhbmNob3ItcG9pbnRcIiwgXCJhbmltYXRpb25cIiwgXCJhbmltYXRpb24tZGVsYXlcIiwgXCJhbmltYXRpb24tZGlyZWN0aW9uXCIsIFwiYW5pbWF0aW9uLWR1cmF0aW9uXCIsIFwiYW5pbWF0aW9uLWZpbGwtbW9kZVwiLCBcImFuaW1hdGlvbi1pdGVyYXRpb24tY291bnRcIiwgXCJhbmltYXRpb24tbmFtZVwiLCBcImFuaW1hdGlvbi1wbGF5LXN0YXRlXCIsIFwiYW5pbWF0aW9uLXRpbWluZy1mdW5jdGlvblwiLCBcImFwcGVhcmFuY2VcIiwgXCJhemltdXRoXCIsIFwiYmFja2ZhY2UtdmlzaWJpbGl0eVwiLCBcImJhY2tncm91bmRcIiwgXCJiYWNrZ3JvdW5kLWF0dGFjaG1lbnRcIiwgXCJiYWNrZ3JvdW5kLWNsaXBcIiwgXCJiYWNrZ3JvdW5kLWNvbG9yXCIsIFwiYmFja2dyb3VuZC1pbWFnZVwiLCBcImJhY2tncm91bmQtb3JpZ2luXCIsIFwiYmFja2dyb3VuZC1wb3NpdGlvblwiLCBcImJhY2tncm91bmQtcmVwZWF0XCIsIFwiYmFja2dyb3VuZC1zaXplXCIsIFwiYmFzZWxpbmUtc2hpZnRcIiwgXCJiaW5kaW5nXCIsIFwiYmxlZWRcIiwgXCJib29rbWFyay1sYWJlbFwiLCBcImJvb2ttYXJrLWxldmVsXCIsIFwiYm9va21hcmstc3RhdGVcIiwgXCJib29rbWFyay10YXJnZXRcIiwgXCJib3JkZXJcIiwgXCJib3JkZXItYm90dG9tXCIsIFwiYm9yZGVyLWJvdHRvbS1jb2xvclwiLCBcImJvcmRlci1ib3R0b20tbGVmdC1yYWRpdXNcIiwgXCJib3JkZXItYm90dG9tLXJpZ2h0LXJhZGl1c1wiLCBcImJvcmRlci1ib3R0b20tc3R5bGVcIiwgXCJib3JkZXItYm90dG9tLXdpZHRoXCIsIFwiYm9yZGVyLWNvbGxhcHNlXCIsIFwiYm9yZGVyLWNvbG9yXCIsIFwiYm9yZGVyLWltYWdlXCIsIFwiYm9yZGVyLWltYWdlLW91dHNldFwiLCBcImJvcmRlci1pbWFnZS1yZXBlYXRcIiwgXCJib3JkZXItaW1hZ2Utc2xpY2VcIiwgXCJib3JkZXItaW1hZ2Utc291cmNlXCIsIFwiYm9yZGVyLWltYWdlLXdpZHRoXCIsIFwiYm9yZGVyLWxlZnRcIiwgXCJib3JkZXItbGVmdC1jb2xvclwiLCBcImJvcmRlci1sZWZ0LXN0eWxlXCIsIFwiYm9yZGVyLWxlZnQtd2lkdGhcIiwgXCJib3JkZXItcmFkaXVzXCIsIFwiYm9yZGVyLXJpZ2h0XCIsIFwiYm9yZGVyLXJpZ2h0LWNvbG9yXCIsIFwiYm9yZGVyLXJpZ2h0LXN0eWxlXCIsIFwiYm9yZGVyLXJpZ2h0LXdpZHRoXCIsIFwiYm9yZGVyLXNwYWNpbmdcIiwgXCJib3JkZXItc3R5bGVcIiwgXCJib3JkZXItdG9wXCIsIFwiYm9yZGVyLXRvcC1jb2xvclwiLCBcImJvcmRlci10b3AtbGVmdC1yYWRpdXNcIiwgXCJib3JkZXItdG9wLXJpZ2h0LXJhZGl1c1wiLCBcImJvcmRlci10b3Atc3R5bGVcIiwgXCJib3JkZXItdG9wLXdpZHRoXCIsIFwiYm9yZGVyLXdpZHRoXCIsIFwiYm90dG9tXCIsIFwiYm94LWRlY29yYXRpb24tYnJlYWtcIiwgXCJib3gtc2hhZG93XCIsIFwiYm94LXNpemluZ1wiLCBcImJyZWFrLWFmdGVyXCIsIFwiYnJlYWstYmVmb3JlXCIsIFwiYnJlYWstaW5zaWRlXCIsIFwiY2FwdGlvbi1zaWRlXCIsIFwiY2xlYXJcIiwgXCJjbGlwXCIsIFwiY29sb3JcIiwgXCJjb2xvci1wcm9maWxlXCIsIFwiY29sdW1uLWNvdW50XCIsIFwiY29sdW1uLWZpbGxcIiwgXCJjb2x1bW4tZ2FwXCIsIFwiY29sdW1uLXJ1bGVcIiwgXCJjb2x1bW4tcnVsZS1jb2xvclwiLCBcImNvbHVtbi1ydWxlLXN0eWxlXCIsIFwiY29sdW1uLXJ1bGUtd2lkdGhcIiwgXCJjb2x1bW4tc3BhblwiLCBcImNvbHVtbi13aWR0aFwiLCBcImNvbHVtbnNcIiwgXCJjb250ZW50XCIsIFwiY291bnRlci1pbmNyZW1lbnRcIiwgXCJjb3VudGVyLXJlc2V0XCIsIFwiY3JvcFwiLCBcImN1ZVwiLCBcImN1ZS1hZnRlclwiLCBcImN1ZS1iZWZvcmVcIiwgXCJjdXJzb3JcIiwgXCJkaXJlY3Rpb25cIiwgXCJkaXNwbGF5XCIsIFwiZG9taW5hbnQtYmFzZWxpbmVcIiwgXCJkcm9wLWluaXRpYWwtYWZ0ZXItYWRqdXN0XCIsIFwiZHJvcC1pbml0aWFsLWFmdGVyLWFsaWduXCIsIFwiZHJvcC1pbml0aWFsLWJlZm9yZS1hZGp1c3RcIiwgXCJkcm9wLWluaXRpYWwtYmVmb3JlLWFsaWduXCIsIFwiZHJvcC1pbml0aWFsLXNpemVcIiwgXCJkcm9wLWluaXRpYWwtdmFsdWVcIiwgXCJlbGV2YXRpb25cIiwgXCJlbXB0eS1jZWxsc1wiLCBcImZpdFwiLCBcImZpdC1wb3NpdGlvblwiLCBcImZsZXhcIiwgXCJmbGV4LWJhc2lzXCIsIFwiZmxleC1kaXJlY3Rpb25cIiwgXCJmbGV4LWZsb3dcIiwgXCJmbGV4LWdyb3dcIiwgXCJmbGV4LXNocmlua1wiLCBcImZsZXgtd3JhcFwiLCBcImZsb2F0XCIsIFwiZmxvYXQtb2Zmc2V0XCIsIFwiZmxvdy1mcm9tXCIsIFwiZmxvdy1pbnRvXCIsIFwiZm9udFwiLCBcImZvbnQtZmVhdHVyZS1zZXR0aW5nc1wiLCBcImZvbnQtZmFtaWx5XCIsIFwiZm9udC1rZXJuaW5nXCIsIFwiZm9udC1sYW5ndWFnZS1vdmVycmlkZVwiLCBcImZvbnQtc2l6ZVwiLCBcImZvbnQtc2l6ZS1hZGp1c3RcIiwgXCJmb250LXN0cmV0Y2hcIiwgXCJmb250LXN0eWxlXCIsIFwiZm9udC1zeW50aGVzaXNcIiwgXCJmb250LXZhcmlhbnRcIiwgXCJmb250LXZhcmlhbnQtYWx0ZXJuYXRlc1wiLCBcImZvbnQtdmFyaWFudC1jYXBzXCIsIFwiZm9udC12YXJpYW50LWVhc3QtYXNpYW5cIiwgXCJmb250LXZhcmlhbnQtbGlnYXR1cmVzXCIsIFwiZm9udC12YXJpYW50LW51bWVyaWNcIiwgXCJmb250LXZhcmlhbnQtcG9zaXRpb25cIiwgXCJmb250LXdlaWdodFwiLCBcImdyaWRcIiwgXCJncmlkLWFyZWFcIiwgXCJncmlkLWF1dG8tY29sdW1uc1wiLCBcImdyaWQtYXV0by1mbG93XCIsIFwiZ3JpZC1hdXRvLXBvc2l0aW9uXCIsIFwiZ3JpZC1hdXRvLXJvd3NcIiwgXCJncmlkLWNvbHVtblwiLCBcImdyaWQtY29sdW1uLWVuZFwiLCBcImdyaWQtY29sdW1uLXN0YXJ0XCIsIFwiZ3JpZC1yb3dcIiwgXCJncmlkLXJvdy1lbmRcIiwgXCJncmlkLXJvdy1zdGFydFwiLCBcImdyaWQtdGVtcGxhdGVcIiwgXCJncmlkLXRlbXBsYXRlLWFyZWFzXCIsIFwiZ3JpZC10ZW1wbGF0ZS1jb2x1bW5zXCIsIFwiZ3JpZC10ZW1wbGF0ZS1yb3dzXCIsIFwiaGFuZ2luZy1wdW5jdHVhdGlvblwiLCBcImhlaWdodFwiLCBcImh5cGhlbnNcIiwgXCJpY29uXCIsIFwiaW1hZ2Utb3JpZW50YXRpb25cIiwgXCJpbWFnZS1yZW5kZXJpbmdcIiwgXCJpbWFnZS1yZXNvbHV0aW9uXCIsIFwiaW5saW5lLWJveC1hbGlnblwiLCBcImp1c3RpZnktY29udGVudFwiLCBcImxlZnRcIiwgXCJsZXR0ZXItc3BhY2luZ1wiLCBcImxpbmUtYnJlYWtcIiwgXCJsaW5lLWhlaWdodFwiLCBcImxpbmUtc3RhY2tpbmdcIiwgXCJsaW5lLXN0YWNraW5nLXJ1YnlcIiwgXCJsaW5lLXN0YWNraW5nLXNoaWZ0XCIsIFwibGluZS1zdGFja2luZy1zdHJhdGVneVwiLCBcImxpc3Qtc3R5bGVcIiwgXCJsaXN0LXN0eWxlLWltYWdlXCIsIFwibGlzdC1zdHlsZS1wb3NpdGlvblwiLCBcImxpc3Qtc3R5bGUtdHlwZVwiLCBcIm1hcmdpblwiLCBcIm1hcmdpbi1ib3R0b21cIiwgXCJtYXJnaW4tbGVmdFwiLCBcIm1hcmdpbi1yaWdodFwiLCBcIm1hcmdpbi10b3BcIiwgXCJtYXJrZXItb2Zmc2V0XCIsIFwibWFya3NcIiwgXCJtYXJxdWVlLWRpcmVjdGlvblwiLCBcIm1hcnF1ZWUtbG9vcFwiLCBcIm1hcnF1ZWUtcGxheS1jb3VudFwiLCBcIm1hcnF1ZWUtc3BlZWRcIiwgXCJtYXJxdWVlLXN0eWxlXCIsIFwibWF4LWhlaWdodFwiLCBcIm1heC13aWR0aFwiLCBcIm1pbi1oZWlnaHRcIiwgXCJtaW4td2lkdGhcIiwgXCJtb3ZlLXRvXCIsIFwibmF2LWRvd25cIiwgXCJuYXYtaW5kZXhcIiwgXCJuYXYtbGVmdFwiLCBcIm5hdi1yaWdodFwiLCBcIm5hdi11cFwiLCBcIm9iamVjdC1maXRcIiwgXCJvYmplY3QtcG9zaXRpb25cIiwgXCJvcGFjaXR5XCIsIFwib3JkZXJcIiwgXCJvcnBoYW5zXCIsIFwib3V0bGluZVwiLCBcIm91dGxpbmUtY29sb3JcIiwgXCJvdXRsaW5lLW9mZnNldFwiLCBcIm91dGxpbmUtc3R5bGVcIiwgXCJvdXRsaW5lLXdpZHRoXCIsIFwib3ZlcmZsb3dcIiwgXCJvdmVyZmxvdy1zdHlsZVwiLCBcIm92ZXJmbG93LXdyYXBcIiwgXCJvdmVyZmxvdy14XCIsIFwib3ZlcmZsb3cteVwiLCBcInBhZGRpbmdcIiwgXCJwYWRkaW5nLWJvdHRvbVwiLCBcInBhZGRpbmctbGVmdFwiLCBcInBhZGRpbmctcmlnaHRcIiwgXCJwYWRkaW5nLXRvcFwiLCBcInBhZ2VcIiwgXCJwYWdlLWJyZWFrLWFmdGVyXCIsIFwicGFnZS1icmVhay1iZWZvcmVcIiwgXCJwYWdlLWJyZWFrLWluc2lkZVwiLCBcInBhZ2UtcG9saWN5XCIsIFwicGF1c2VcIiwgXCJwYXVzZS1hZnRlclwiLCBcInBhdXNlLWJlZm9yZVwiLCBcInBlcnNwZWN0aXZlXCIsIFwicGVyc3BlY3RpdmUtb3JpZ2luXCIsIFwicGl0Y2hcIiwgXCJwaXRjaC1yYW5nZVwiLCBcInBsYXktZHVyaW5nXCIsIFwicG9zaXRpb25cIiwgXCJwcmVzZW50YXRpb24tbGV2ZWxcIiwgXCJwdW5jdHVhdGlvbi10cmltXCIsIFwicXVvdGVzXCIsIFwicmVnaW9uLWJyZWFrLWFmdGVyXCIsIFwicmVnaW9uLWJyZWFrLWJlZm9yZVwiLCBcInJlZ2lvbi1icmVhay1pbnNpZGVcIiwgXCJyZWdpb24tZnJhZ21lbnRcIiwgXCJyZW5kZXJpbmctaW50ZW50XCIsIFwicmVzaXplXCIsIFwicmVzdFwiLCBcInJlc3QtYWZ0ZXJcIiwgXCJyZXN0LWJlZm9yZVwiLCBcInJpY2huZXNzXCIsIFwicmlnaHRcIiwgXCJyb3RhdGlvblwiLCBcInJvdGF0aW9uLXBvaW50XCIsIFwicnVieS1hbGlnblwiLCBcInJ1Ynktb3ZlcmhhbmdcIiwgXCJydWJ5LXBvc2l0aW9uXCIsIFwicnVieS1zcGFuXCIsIFwic2hhcGUtaW1hZ2UtdGhyZXNob2xkXCIsIFwic2hhcGUtaW5zaWRlXCIsIFwic2hhcGUtbWFyZ2luXCIsIFwic2hhcGUtb3V0c2lkZVwiLCBcInNpemVcIiwgXCJzcGVha1wiLCBcInNwZWFrLWFzXCIsIFwic3BlYWstaGVhZGVyXCIsIFwic3BlYWstbnVtZXJhbFwiLCBcInNwZWFrLXB1bmN0dWF0aW9uXCIsIFwic3BlZWNoLXJhdGVcIiwgXCJzdHJlc3NcIiwgXCJzdHJpbmctc2V0XCIsIFwidGFiLXNpemVcIiwgXCJ0YWJsZS1sYXlvdXRcIiwgXCJ0YXJnZXRcIiwgXCJ0YXJnZXQtbmFtZVwiLCBcInRhcmdldC1uZXdcIiwgXCJ0YXJnZXQtcG9zaXRpb25cIiwgXCJ0ZXh0LWFsaWduXCIsIFwidGV4dC1hbGlnbi1sYXN0XCIsIFwidGV4dC1kZWNvcmF0aW9uXCIsIFwidGV4dC1kZWNvcmF0aW9uLWNvbG9yXCIsIFwidGV4dC1kZWNvcmF0aW9uLWxpbmVcIiwgXCJ0ZXh0LWRlY29yYXRpb24tc2tpcFwiLCBcInRleHQtZGVjb3JhdGlvbi1zdHlsZVwiLCBcInRleHQtZW1waGFzaXNcIiwgXCJ0ZXh0LWVtcGhhc2lzLWNvbG9yXCIsIFwidGV4dC1lbXBoYXNpcy1wb3NpdGlvblwiLCBcInRleHQtZW1waGFzaXMtc3R5bGVcIiwgXCJ0ZXh0LWhlaWdodFwiLCBcInRleHQtaW5kZW50XCIsIFwidGV4dC1qdXN0aWZ5XCIsIFwidGV4dC1vdXRsaW5lXCIsIFwidGV4dC1vdmVyZmxvd1wiLCBcInRleHQtc2hhZG93XCIsIFwidGV4dC1zaXplLWFkanVzdFwiLCBcInRleHQtc3BhY2UtY29sbGFwc2VcIiwgXCJ0ZXh0LXRyYW5zZm9ybVwiLCBcInRleHQtdW5kZXJsaW5lLXBvc2l0aW9uXCIsIFwidGV4dC13cmFwXCIsIFwidG9wXCIsIFwidHJhbnNmb3JtXCIsIFwidHJhbnNmb3JtLW9yaWdpblwiLCBcInRyYW5zZm9ybS1zdHlsZVwiLCBcInRyYW5zaXRpb25cIiwgXCJ0cmFuc2l0aW9uLWRlbGF5XCIsIFwidHJhbnNpdGlvbi1kdXJhdGlvblwiLCBcInRyYW5zaXRpb24tcHJvcGVydHlcIiwgXCJ0cmFuc2l0aW9uLXRpbWluZy1mdW5jdGlvblwiLCBcInVuaWNvZGUtYmlkaVwiLCBcInZlcnRpY2FsLWFsaWduXCIsIFwidmlzaWJpbGl0eVwiLCBcInZvaWNlLWJhbGFuY2VcIiwgXCJ2b2ljZS1kdXJhdGlvblwiLCBcInZvaWNlLWZhbWlseVwiLCBcInZvaWNlLXBpdGNoXCIsIFwidm9pY2UtcmFuZ2VcIiwgXCJ2b2ljZS1yYXRlXCIsIFwidm9pY2Utc3RyZXNzXCIsIFwidm9pY2Utdm9sdW1lXCIsIFwidm9sdW1lXCIsIFwid2hpdGUtc3BhY2VcIiwgXCJ3aWRvd3NcIiwgXCJ3aWR0aFwiLCBcIndpbGwtY2hhbmdlXCIsIFwid29yZC1icmVha1wiLCBcIndvcmQtc3BhY2luZ1wiLCBcIndvcmQtd3JhcFwiLCBcInotaW5kZXhcIiwgXCJjbGlwLXBhdGhcIiwgXCJjbGlwLXJ1bGVcIiwgXCJtYXNrXCIsIFwiZW5hYmxlLWJhY2tncm91bmRcIiwgXCJmaWx0ZXJcIiwgXCJmbG9vZC1jb2xvclwiLCBcImZsb29kLW9wYWNpdHlcIiwgXCJsaWdodGluZy1jb2xvclwiLCBcInN0b3AtY29sb3JcIiwgXCJzdG9wLW9wYWNpdHlcIiwgXCJwb2ludGVyLWV2ZW50c1wiLCBcImNvbG9yLWludGVycG9sYXRpb25cIiwgXCJjb2xvci1pbnRlcnBvbGF0aW9uLWZpbHRlcnNcIiwgXCJjb2xvci1yZW5kZXJpbmdcIiwgXCJmaWxsXCIsIFwiZmlsbC1vcGFjaXR5XCIsIFwiZmlsbC1ydWxlXCIsIFwiaW1hZ2UtcmVuZGVyaW5nXCIsIFwibWFya2VyXCIsIFwibWFya2VyLWVuZFwiLCBcIm1hcmtlci1taWRcIiwgXCJtYXJrZXItc3RhcnRcIiwgXCJzaGFwZS1yZW5kZXJpbmdcIiwgXCJzdHJva2VcIiwgXCJzdHJva2UtZGFzaGFycmF5XCIsIFwic3Ryb2tlLWRhc2hvZmZzZXRcIiwgXCJzdHJva2UtbGluZWNhcFwiLCBcInN0cm9rZS1saW5lam9pblwiLCBcInN0cm9rZS1taXRlcmxpbWl0XCIsIFwic3Ryb2tlLW9wYWNpdHlcIiwgXCJzdHJva2Utd2lkdGhcIiwgXCJ0ZXh0LXJlbmRlcmluZ1wiLCBcImJhc2VsaW5lLXNoaWZ0XCIsIFwiZG9taW5hbnQtYmFzZWxpbmVcIiwgXCJnbHlwaC1vcmllbnRhdGlvbi1ob3Jpem9udGFsXCIsIFwiZ2x5cGgtb3JpZW50YXRpb24tdmVydGljYWxcIiwgXCJ0ZXh0LWFuY2hvclwiLCBcIndyaXRpbmctbW9kZVwiLCBcImZvbnQtc21vb3RoaW5nXCIsIFwib3N4LWZvbnQtc21vb3RoaW5nXCJdO1xudmFyIG5vblN0YW5kYXJkUHJvcGVydHlLZXl3b3Jkc18gPSBbXCJzY3JvbGxiYXItYXJyb3ctY29sb3JcIiwgXCJzY3JvbGxiYXItYmFzZS1jb2xvclwiLCBcInNjcm9sbGJhci1kYXJrLXNoYWRvdy1jb2xvclwiLCBcInNjcm9sbGJhci1mYWNlLWNvbG9yXCIsIFwic2Nyb2xsYmFyLWhpZ2hsaWdodC1jb2xvclwiLCBcInNjcm9sbGJhci1zaGFkb3ctY29sb3JcIiwgXCJzY3JvbGxiYXItM2QtbGlnaHQtY29sb3JcIiwgXCJzY3JvbGxiYXItdHJhY2stY29sb3JcIiwgXCJzaGFwZS1pbnNpZGVcIiwgXCJzZWFyY2hmaWVsZC1jYW5jZWwtYnV0dG9uXCIsIFwic2VhcmNoZmllbGQtZGVjb3JhdGlvblwiLCBcInNlYXJjaGZpZWxkLXJlc3VsdHMtYnV0dG9uXCIsIFwic2VhcmNoZmllbGQtcmVzdWx0cy1kZWNvcmF0aW9uXCIsIFwiem9vbVwiXTtcbnZhciBmb250UHJvcGVydGllc18gPSBbXCJmb250LWZhbWlseVwiLCBcInNyY1wiLCBcInVuaWNvZGUtcmFuZ2VcIiwgXCJmb250LXZhcmlhbnRcIiwgXCJmb250LWZlYXR1cmUtc2V0dGluZ3NcIiwgXCJmb250LXN0cmV0Y2hcIiwgXCJmb250LXdlaWdodFwiLCBcImZvbnQtc3R5bGVcIl07XG52YXIgY29sb3JLZXl3b3Jkc18gPSBbXCJhbGljZWJsdWVcIiwgXCJhbnRpcXVld2hpdGVcIiwgXCJhcXVhXCIsIFwiYXF1YW1hcmluZVwiLCBcImF6dXJlXCIsIFwiYmVpZ2VcIiwgXCJiaXNxdWVcIiwgXCJibGFja1wiLCBcImJsYW5jaGVkYWxtb25kXCIsIFwiYmx1ZVwiLCBcImJsdWV2aW9sZXRcIiwgXCJicm93blwiLCBcImJ1cmx5d29vZFwiLCBcImNhZGV0Ymx1ZVwiLCBcImNoYXJ0cmV1c2VcIiwgXCJjaG9jb2xhdGVcIiwgXCJjb3JhbFwiLCBcImNvcm5mbG93ZXJibHVlXCIsIFwiY29ybnNpbGtcIiwgXCJjcmltc29uXCIsIFwiY3lhblwiLCBcImRhcmtibHVlXCIsIFwiZGFya2N5YW5cIiwgXCJkYXJrZ29sZGVucm9kXCIsIFwiZGFya2dyYXlcIiwgXCJkYXJrZ3JlZW5cIiwgXCJkYXJra2hha2lcIiwgXCJkYXJrbWFnZW50YVwiLCBcImRhcmtvbGl2ZWdyZWVuXCIsIFwiZGFya29yYW5nZVwiLCBcImRhcmtvcmNoaWRcIiwgXCJkYXJrcmVkXCIsIFwiZGFya3NhbG1vblwiLCBcImRhcmtzZWFncmVlblwiLCBcImRhcmtzbGF0ZWJsdWVcIiwgXCJkYXJrc2xhdGVncmF5XCIsIFwiZGFya3R1cnF1b2lzZVwiLCBcImRhcmt2aW9sZXRcIiwgXCJkZWVwcGlua1wiLCBcImRlZXBza3libHVlXCIsIFwiZGltZ3JheVwiLCBcImRvZGdlcmJsdWVcIiwgXCJmaXJlYnJpY2tcIiwgXCJmbG9yYWx3aGl0ZVwiLCBcImZvcmVzdGdyZWVuXCIsIFwiZnVjaHNpYVwiLCBcImdhaW5zYm9yb1wiLCBcImdob3N0d2hpdGVcIiwgXCJnb2xkXCIsIFwiZ29sZGVucm9kXCIsIFwiZ3JheVwiLCBcImdyZXlcIiwgXCJncmVlblwiLCBcImdyZWVueWVsbG93XCIsIFwiaG9uZXlkZXdcIiwgXCJob3RwaW5rXCIsIFwiaW5kaWFucmVkXCIsIFwiaW5kaWdvXCIsIFwiaXZvcnlcIiwgXCJraGFraVwiLCBcImxhdmVuZGVyXCIsIFwibGF2ZW5kZXJibHVzaFwiLCBcImxhd25ncmVlblwiLCBcImxlbW9uY2hpZmZvblwiLCBcImxpZ2h0Ymx1ZVwiLCBcImxpZ2h0Y29yYWxcIiwgXCJsaWdodGN5YW5cIiwgXCJsaWdodGdvbGRlbnJvZHllbGxvd1wiLCBcImxpZ2h0Z3JheVwiLCBcImxpZ2h0Z3JlZW5cIiwgXCJsaWdodHBpbmtcIiwgXCJsaWdodHNhbG1vblwiLCBcImxpZ2h0c2VhZ3JlZW5cIiwgXCJsaWdodHNreWJsdWVcIiwgXCJsaWdodHNsYXRlZ3JheVwiLCBcImxpZ2h0c3RlZWxibHVlXCIsIFwibGlnaHR5ZWxsb3dcIiwgXCJsaW1lXCIsIFwibGltZWdyZWVuXCIsIFwibGluZW5cIiwgXCJtYWdlbnRhXCIsIFwibWFyb29uXCIsIFwibWVkaXVtYXF1YW1hcmluZVwiLCBcIm1lZGl1bWJsdWVcIiwgXCJtZWRpdW1vcmNoaWRcIiwgXCJtZWRpdW1wdXJwbGVcIiwgXCJtZWRpdW1zZWFncmVlblwiLCBcIm1lZGl1bXNsYXRlYmx1ZVwiLCBcIm1lZGl1bXNwcmluZ2dyZWVuXCIsIFwibWVkaXVtdHVycXVvaXNlXCIsIFwibWVkaXVtdmlvbGV0cmVkXCIsIFwibWlkbmlnaHRibHVlXCIsIFwibWludGNyZWFtXCIsIFwibWlzdHlyb3NlXCIsIFwibW9jY2FzaW5cIiwgXCJuYXZham93aGl0ZVwiLCBcIm5hdnlcIiwgXCJvbGRsYWNlXCIsIFwib2xpdmVcIiwgXCJvbGl2ZWRyYWJcIiwgXCJvcmFuZ2VcIiwgXCJvcmFuZ2VyZWRcIiwgXCJvcmNoaWRcIiwgXCJwYWxlZ29sZGVucm9kXCIsIFwicGFsZWdyZWVuXCIsIFwicGFsZXR1cnF1b2lzZVwiLCBcInBhbGV2aW9sZXRyZWRcIiwgXCJwYXBheWF3aGlwXCIsIFwicGVhY2hwdWZmXCIsIFwicGVydVwiLCBcInBpbmtcIiwgXCJwbHVtXCIsIFwicG93ZGVyYmx1ZVwiLCBcInB1cnBsZVwiLCBcInJlYmVjY2FwdXJwbGVcIiwgXCJyZWRcIiwgXCJyb3N5YnJvd25cIiwgXCJyb3lhbGJsdWVcIiwgXCJzYWRkbGVicm93blwiLCBcInNhbG1vblwiLCBcInNhbmR5YnJvd25cIiwgXCJzZWFncmVlblwiLCBcInNlYXNoZWxsXCIsIFwic2llbm5hXCIsIFwic2lsdmVyXCIsIFwic2t5Ymx1ZVwiLCBcInNsYXRlYmx1ZVwiLCBcInNsYXRlZ3JheVwiLCBcInNub3dcIiwgXCJzcHJpbmdncmVlblwiLCBcInN0ZWVsYmx1ZVwiLCBcInRhblwiLCBcInRlYWxcIiwgXCJ0aGlzdGxlXCIsIFwidG9tYXRvXCIsIFwidHVycXVvaXNlXCIsIFwidmlvbGV0XCIsIFwid2hlYXRcIiwgXCJ3aGl0ZVwiLCBcIndoaXRlc21va2VcIiwgXCJ5ZWxsb3dcIiwgXCJ5ZWxsb3dncmVlblwiXTtcbnZhciB2YWx1ZUtleXdvcmRzXyA9IFtcImFib3ZlXCIsIFwiYWJzb2x1dGVcIiwgXCJhY3RpdmVib3JkZXJcIiwgXCJhZGRpdGl2ZVwiLCBcImFjdGl2ZWNhcHRpb25cIiwgXCJhZmFyXCIsIFwiYWZ0ZXItd2hpdGUtc3BhY2VcIiwgXCJhaGVhZFwiLCBcImFsaWFzXCIsIFwiYWxsXCIsIFwiYWxsLXNjcm9sbFwiLCBcImFscGhhYmV0aWNcIiwgXCJhbHRlcm5hdGVcIiwgXCJhbHdheXNcIiwgXCJhbWhhcmljXCIsIFwiYW1oYXJpYy1hYmVnZWRlXCIsIFwiYW50aWFsaWFzZWRcIiwgXCJhcHB3b3Jrc3BhY2VcIiwgXCJhcmFiaWMtaW5kaWNcIiwgXCJhcm1lbmlhblwiLCBcImFzdGVyaXNrc1wiLCBcImF0dHJcIiwgXCJhdXRvXCIsIFwiYXZvaWRcIiwgXCJhdm9pZC1jb2x1bW5cIiwgXCJhdm9pZC1wYWdlXCIsIFwiYXZvaWQtcmVnaW9uXCIsIFwiYmFja2dyb3VuZFwiLCBcImJhY2t3YXJkc1wiLCBcImJhc2VsaW5lXCIsIFwiYmVsb3dcIiwgXCJiaWRpLW92ZXJyaWRlXCIsIFwiYmluYXJ5XCIsIFwiYmVuZ2FsaVwiLCBcImJsaW5rXCIsIFwiYmxvY2tcIiwgXCJibG9jay1heGlzXCIsIFwiYm9sZFwiLCBcImJvbGRlclwiLCBcImJvcmRlclwiLCBcImJvcmRlci1ib3hcIiwgXCJib3RoXCIsIFwiYm90dG9tXCIsIFwiYnJlYWtcIiwgXCJicmVhay1hbGxcIiwgXCJicmVhay13b3JkXCIsIFwiYnVsbGV0c1wiLCBcImJ1dHRvblwiLCBcImJ1dHRvbmZhY2VcIiwgXCJidXR0b25oaWdobGlnaHRcIiwgXCJidXR0b25zaGFkb3dcIiwgXCJidXR0b250ZXh0XCIsIFwiY2FsY1wiLCBcImNhbWJvZGlhblwiLCBcImNhcGl0YWxpemVcIiwgXCJjYXBzLWxvY2staW5kaWNhdG9yXCIsIFwiY2FwdGlvblwiLCBcImNhcHRpb250ZXh0XCIsIFwiY2FyZXRcIiwgXCJjZWxsXCIsIFwiY2VudGVyXCIsIFwiY2hlY2tib3hcIiwgXCJjaXJjbGVcIiwgXCJjamstZGVjaW1hbFwiLCBcImNqay1lYXJ0aGx5LWJyYW5jaFwiLCBcImNqay1oZWF2ZW5seS1zdGVtXCIsIFwiY2prLWlkZW9ncmFwaGljXCIsIFwiY2xlYXJcIiwgXCJjbGlwXCIsIFwiY2xvc2UtcXVvdGVcIiwgXCJjb2wtcmVzaXplXCIsIFwiY29sbGFwc2VcIiwgXCJjb2x1bW5cIiwgXCJjb21wYWN0XCIsIFwiY29uZGVuc2VkXCIsIFwiY29uaWMtZ3JhZGllbnRcIiwgXCJjb250YWluXCIsIFwiY29udGVudFwiLCBcImNvbnRlbnRzXCIsIFwiY29udGVudC1ib3hcIiwgXCJjb250ZXh0LW1lbnVcIiwgXCJjb250aW51b3VzXCIsIFwiY29weVwiLCBcImNvdW50ZXJcIiwgXCJjb3VudGVyc1wiLCBcImNvdmVyXCIsIFwiY3JvcFwiLCBcImNyb3NzXCIsIFwiY3Jvc3NoYWlyXCIsIFwiY3VycmVudGNvbG9yXCIsIFwiY3Vyc2l2ZVwiLCBcImN5Y2xpY1wiLCBcImRhc2hlZFwiLCBcImRlY2ltYWxcIiwgXCJkZWNpbWFsLWxlYWRpbmctemVyb1wiLCBcImRlZmF1bHRcIiwgXCJkZWZhdWx0LWJ1dHRvblwiLCBcImRlc3RpbmF0aW9uLWF0b3BcIiwgXCJkZXN0aW5hdGlvbi1pblwiLCBcImRlc3RpbmF0aW9uLW91dFwiLCBcImRlc3RpbmF0aW9uLW92ZXJcIiwgXCJkZXZhbmFnYXJpXCIsIFwiZGlzY1wiLCBcImRpc2NhcmRcIiwgXCJkaXNjbG9zdXJlLWNsb3NlZFwiLCBcImRpc2Nsb3N1cmUtb3BlblwiLCBcImRvY3VtZW50XCIsIFwiZG90LWRhc2hcIiwgXCJkb3QtZG90LWRhc2hcIiwgXCJkb3R0ZWRcIiwgXCJkb3VibGVcIiwgXCJkb3duXCIsIFwiZS1yZXNpemVcIiwgXCJlYXNlXCIsIFwiZWFzZS1pblwiLCBcImVhc2UtaW4tb3V0XCIsIFwiZWFzZS1vdXRcIiwgXCJlbGVtZW50XCIsIFwiZWxsaXBzZVwiLCBcImVsbGlwc2lzXCIsIFwiZW1iZWRcIiwgXCJlbmRcIiwgXCJldGhpb3BpY1wiLCBcImV0aGlvcGljLWFiZWdlZGVcIiwgXCJldGhpb3BpYy1hYmVnZWRlLWFtLWV0XCIsIFwiZXRoaW9waWMtYWJlZ2VkZS1nZXpcIiwgXCJldGhpb3BpYy1hYmVnZWRlLXRpLWVyXCIsIFwiZXRoaW9waWMtYWJlZ2VkZS10aS1ldFwiLCBcImV0aGlvcGljLWhhbGVoYW1lLWFhLWVyXCIsIFwiZXRoaW9waWMtaGFsZWhhbWUtYWEtZXRcIiwgXCJldGhpb3BpYy1oYWxlaGFtZS1hbS1ldFwiLCBcImV0aGlvcGljLWhhbGVoYW1lLWdlelwiLCBcImV0aGlvcGljLWhhbGVoYW1lLW9tLWV0XCIsIFwiZXRoaW9waWMtaGFsZWhhbWUtc2lkLWV0XCIsIFwiZXRoaW9waWMtaGFsZWhhbWUtc28tZXRcIiwgXCJldGhpb3BpYy1oYWxlaGFtZS10aS1lclwiLCBcImV0aGlvcGljLWhhbGVoYW1lLXRpLWV0XCIsIFwiZXRoaW9waWMtaGFsZWhhbWUtdGlnXCIsIFwiZXRoaW9waWMtbnVtZXJpY1wiLCBcImV3LXJlc2l6ZVwiLCBcImV4cGFuZGVkXCIsIFwiZXh0ZW5kc1wiLCBcImV4dHJhLWNvbmRlbnNlZFwiLCBcImV4dHJhLWV4cGFuZGVkXCIsIFwiZmFudGFzeVwiLCBcImZhc3RcIiwgXCJmaWxsXCIsIFwiZml4ZWRcIiwgXCJmbGF0XCIsIFwiZmxleFwiLCBcImZvb3Rub3Rlc1wiLCBcImZvcndhcmRzXCIsIFwiZnJvbVwiLCBcImdlb21ldHJpY1ByZWNpc2lvblwiLCBcImdlb3JnaWFuXCIsIFwiZ3JheXRleHRcIiwgXCJncm9vdmVcIiwgXCJndWphcmF0aVwiLCBcImd1cm11a2hpXCIsIFwiaGFuZFwiLCBcImhhbmd1bFwiLCBcImhhbmd1bC1jb25zb25hbnRcIiwgXCJoZWJyZXdcIiwgXCJoZWxwXCIsIFwiaGlkZGVuXCIsIFwiaGlkZVwiLCBcImhpZ2hcIiwgXCJoaWdoZXJcIiwgXCJoaWdobGlnaHRcIiwgXCJoaWdobGlnaHR0ZXh0XCIsIFwiaGlyYWdhbmFcIiwgXCJoaXJhZ2FuYS1pcm9oYVwiLCBcImhvcml6b250YWxcIiwgXCJoc2xcIiwgXCJoc2xhXCIsIFwiaWNvblwiLCBcImlnbm9yZVwiLCBcImluYWN0aXZlYm9yZGVyXCIsIFwiaW5hY3RpdmVjYXB0aW9uXCIsIFwiaW5hY3RpdmVjYXB0aW9udGV4dFwiLCBcImluZmluaXRlXCIsIFwiaW5mb2JhY2tncm91bmRcIiwgXCJpbmZvdGV4dFwiLCBcImluaGVyaXRcIiwgXCJpbml0aWFsXCIsIFwiaW5saW5lXCIsIFwiaW5saW5lLWF4aXNcIiwgXCJpbmxpbmUtYmxvY2tcIiwgXCJpbmxpbmUtZmxleFwiLCBcImlubGluZS10YWJsZVwiLCBcImluc2V0XCIsIFwiaW5zaWRlXCIsIFwiaW50cmluc2ljXCIsIFwiaW52ZXJ0XCIsIFwiaXRhbGljXCIsIFwiamFwYW5lc2UtZm9ybWFsXCIsIFwiamFwYW5lc2UtaW5mb3JtYWxcIiwgXCJqdXN0aWZ5XCIsIFwia2FubmFkYVwiLCBcImthdGFrYW5hXCIsIFwia2F0YWthbmEtaXJvaGFcIiwgXCJrZWVwLWFsbFwiLCBcImtobWVyXCIsIFwia29yZWFuLWhhbmd1bC1mb3JtYWxcIiwgXCJrb3JlYW4taGFuamEtZm9ybWFsXCIsIFwia29yZWFuLWhhbmphLWluZm9ybWFsXCIsIFwibGFuZHNjYXBlXCIsIFwibGFvXCIsIFwibGFyZ2VcIiwgXCJsYXJnZXJcIiwgXCJsZWZ0XCIsIFwibGV2ZWxcIiwgXCJsaWdodGVyXCIsIFwibGluZS10aHJvdWdoXCIsIFwibGluZWFyXCIsIFwibGluZWFyLWdyYWRpZW50XCIsIFwibGluZXNcIiwgXCJsaXN0LWl0ZW1cIiwgXCJsaXN0Ym94XCIsIFwibGlzdGl0ZW1cIiwgXCJsb2NhbFwiLCBcImxvZ2ljYWxcIiwgXCJsb3VkXCIsIFwibG93ZXJcIiwgXCJsb3dlci1hbHBoYVwiLCBcImxvd2VyLWFybWVuaWFuXCIsIFwibG93ZXItZ3JlZWtcIiwgXCJsb3dlci1oZXhhZGVjaW1hbFwiLCBcImxvd2VyLWxhdGluXCIsIFwibG93ZXItbm9yd2VnaWFuXCIsIFwibG93ZXItcm9tYW5cIiwgXCJsb3dlcmNhc2VcIiwgXCJsdHJcIiwgXCJtYWxheWFsYW1cIiwgXCJtYXRjaFwiLCBcIm1hdHJpeFwiLCBcIm1hdHJpeDNkXCIsIFwibWVkaWEtcGxheS1idXR0b25cIiwgXCJtZWRpYS1zbGlkZXJcIiwgXCJtZWRpYS1zbGlkZXJ0aHVtYlwiLCBcIm1lZGlhLXZvbHVtZS1zbGlkZXJcIiwgXCJtZWRpYS12b2x1bWUtc2xpZGVydGh1bWJcIiwgXCJtZWRpdW1cIiwgXCJtZW51XCIsIFwibWVudWxpc3RcIiwgXCJtZW51bGlzdC1idXR0b25cIiwgXCJtZW51dGV4dFwiLCBcIm1lc3NhZ2UtYm94XCIsIFwibWlkZGxlXCIsIFwibWluLWludHJpbnNpY1wiLCBcIm1peFwiLCBcIm1vbmdvbGlhblwiLCBcIm1vbm9zcGFjZVwiLCBcIm1vdmVcIiwgXCJtdWx0aXBsZVwiLCBcIm15YW5tYXJcIiwgXCJuLXJlc2l6ZVwiLCBcIm5hcnJvd2VyXCIsIFwibmUtcmVzaXplXCIsIFwibmVzdy1yZXNpemVcIiwgXCJuby1jbG9zZS1xdW90ZVwiLCBcIm5vLWRyb3BcIiwgXCJuby1vcGVuLXF1b3RlXCIsIFwibm8tcmVwZWF0XCIsIFwibm9uZVwiLCBcIm5vcm1hbFwiLCBcIm5vdC1hbGxvd2VkXCIsIFwibm93cmFwXCIsIFwibnMtcmVzaXplXCIsIFwibnVtYmVyc1wiLCBcIm51bWVyaWNcIiwgXCJudy1yZXNpemVcIiwgXCJud3NlLXJlc2l6ZVwiLCBcIm9ibGlxdWVcIiwgXCJvY3RhbFwiLCBcIm9wZW4tcXVvdGVcIiwgXCJvcHRpbWl6ZUxlZ2liaWxpdHlcIiwgXCJvcHRpbWl6ZVNwZWVkXCIsIFwib3JpeWFcIiwgXCJvcm9tb1wiLCBcIm91dHNldFwiLCBcIm91dHNpZGVcIiwgXCJvdXRzaWRlLXNoYXBlXCIsIFwib3ZlcmxheVwiLCBcIm92ZXJsaW5lXCIsIFwicGFkZGluZ1wiLCBcInBhZGRpbmctYm94XCIsIFwicGFpbnRlZFwiLCBcInBhZ2VcIiwgXCJwYXVzZWRcIiwgXCJwZXJzaWFuXCIsIFwicGVyc3BlY3RpdmVcIiwgXCJwbHVzLWRhcmtlclwiLCBcInBsdXMtbGlnaHRlclwiLCBcInBvaW50ZXJcIiwgXCJwb2x5Z29uXCIsIFwicG9ydHJhaXRcIiwgXCJwcmVcIiwgXCJwcmUtbGluZVwiLCBcInByZS13cmFwXCIsIFwicHJlc2VydmUtM2RcIiwgXCJwcm9ncmVzc1wiLCBcInB1c2gtYnV0dG9uXCIsIFwicmFkaWFsLWdyYWRpZW50XCIsIFwicmFkaW9cIiwgXCJyZWFkLW9ubHlcIiwgXCJyZWFkLXdyaXRlXCIsIFwicmVhZC13cml0ZS1wbGFpbnRleHQtb25seVwiLCBcInJlY3RhbmdsZVwiLCBcInJlZ2lvblwiLCBcInJlbGF0aXZlXCIsIFwicmVwZWF0XCIsIFwicmVwZWF0aW5nLWxpbmVhci1ncmFkaWVudFwiLCBcInJlcGVhdGluZy1yYWRpYWwtZ3JhZGllbnRcIiwgXCJyZXBlYXRpbmctY29uaWMtZ3JhZGllbnRcIiwgXCJyZXBlYXQteFwiLCBcInJlcGVhdC15XCIsIFwicmVzZXRcIiwgXCJyZXZlcnNlXCIsIFwicmdiXCIsIFwicmdiYVwiLCBcInJpZGdlXCIsIFwicmlnaHRcIiwgXCJyb3RhdGVcIiwgXCJyb3RhdGUzZFwiLCBcInJvdGF0ZVhcIiwgXCJyb3RhdGVZXCIsIFwicm90YXRlWlwiLCBcInJvdW5kXCIsIFwicm93LXJlc2l6ZVwiLCBcInJ0bFwiLCBcInJ1bi1pblwiLCBcInJ1bm5pbmdcIiwgXCJzLXJlc2l6ZVwiLCBcInNhbnMtc2VyaWZcIiwgXCJzY2FsZVwiLCBcInNjYWxlM2RcIiwgXCJzY2FsZVhcIiwgXCJzY2FsZVlcIiwgXCJzY2FsZVpcIiwgXCJzY3JvbGxcIiwgXCJzY3JvbGxiYXJcIiwgXCJzY3JvbGwtcG9zaXRpb25cIiwgXCJzZS1yZXNpemVcIiwgXCJzZWFyY2hmaWVsZFwiLCBcInNlYXJjaGZpZWxkLWNhbmNlbC1idXR0b25cIiwgXCJzZWFyY2hmaWVsZC1kZWNvcmF0aW9uXCIsIFwic2VhcmNoZmllbGQtcmVzdWx0cy1idXR0b25cIiwgXCJzZWFyY2hmaWVsZC1yZXN1bHRzLWRlY29yYXRpb25cIiwgXCJzZW1pLWNvbmRlbnNlZFwiLCBcInNlbWktZXhwYW5kZWRcIiwgXCJzZXBhcmF0ZVwiLCBcInNlcmlmXCIsIFwic2hvd1wiLCBcInNpZGFtYVwiLCBcInNpbXAtY2hpbmVzZS1mb3JtYWxcIiwgXCJzaW1wLWNoaW5lc2UtaW5mb3JtYWxcIiwgXCJzaW5nbGVcIiwgXCJza2V3XCIsIFwic2tld1hcIiwgXCJza2V3WVwiLCBcInNraXAtd2hpdGUtc3BhY2VcIiwgXCJzbGlkZVwiLCBcInNsaWRlci1ob3Jpem9udGFsXCIsIFwic2xpZGVyLXZlcnRpY2FsXCIsIFwic2xpZGVydGh1bWItaG9yaXpvbnRhbFwiLCBcInNsaWRlcnRodW1iLXZlcnRpY2FsXCIsIFwic2xvd1wiLCBcInNtYWxsXCIsIFwic21hbGwtY2Fwc1wiLCBcInNtYWxsLWNhcHRpb25cIiwgXCJzbWFsbGVyXCIsIFwic29saWRcIiwgXCJzb21hbGlcIiwgXCJzb3VyY2UtYXRvcFwiLCBcInNvdXJjZS1pblwiLCBcInNvdXJjZS1vdXRcIiwgXCJzb3VyY2Utb3ZlclwiLCBcInNwYWNlXCIsIFwic3BlbGwtb3V0XCIsIFwic3F1YXJlXCIsIFwic3F1YXJlLWJ1dHRvblwiLCBcInN0YW5kYXJkXCIsIFwic3RhcnRcIiwgXCJzdGF0aWNcIiwgXCJzdGF0dXMtYmFyXCIsIFwic3RyZXRjaFwiLCBcInN0cm9rZVwiLCBcInN1YlwiLCBcInN1YnBpeGVsLWFudGlhbGlhc2VkXCIsIFwic3VwZXJcIiwgXCJzdy1yZXNpemVcIiwgXCJzeW1ib2xpY1wiLCBcInN5bWJvbHNcIiwgXCJ0YWJsZVwiLCBcInRhYmxlLWNhcHRpb25cIiwgXCJ0YWJsZS1jZWxsXCIsIFwidGFibGUtY29sdW1uXCIsIFwidGFibGUtY29sdW1uLWdyb3VwXCIsIFwidGFibGUtZm9vdGVyLWdyb3VwXCIsIFwidGFibGUtaGVhZGVyLWdyb3VwXCIsIFwidGFibGUtcm93XCIsIFwidGFibGUtcm93LWdyb3VwXCIsIFwidGFtaWxcIiwgXCJ0ZWx1Z3VcIiwgXCJ0ZXh0XCIsIFwidGV4dC1ib3R0b21cIiwgXCJ0ZXh0LXRvcFwiLCBcInRleHRhcmVhXCIsIFwidGV4dGZpZWxkXCIsIFwidGhhaVwiLCBcInRoaWNrXCIsIFwidGhpblwiLCBcInRocmVlZGRhcmtzaGFkb3dcIiwgXCJ0aHJlZWRmYWNlXCIsIFwidGhyZWVkaGlnaGxpZ2h0XCIsIFwidGhyZWVkbGlnaHRzaGFkb3dcIiwgXCJ0aHJlZWRzaGFkb3dcIiwgXCJ0aWJldGFuXCIsIFwidGlncmVcIiwgXCJ0aWdyaW55YS1lclwiLCBcInRpZ3JpbnlhLWVyLWFiZWdlZGVcIiwgXCJ0aWdyaW55YS1ldFwiLCBcInRpZ3JpbnlhLWV0LWFiZWdlZGVcIiwgXCJ0b1wiLCBcInRvcFwiLCBcInRyYWQtY2hpbmVzZS1mb3JtYWxcIiwgXCJ0cmFkLWNoaW5lc2UtaW5mb3JtYWxcIiwgXCJ0cmFuc2xhdGVcIiwgXCJ0cmFuc2xhdGUzZFwiLCBcInRyYW5zbGF0ZVhcIiwgXCJ0cmFuc2xhdGVZXCIsIFwidHJhbnNsYXRlWlwiLCBcInRyYW5zcGFyZW50XCIsIFwidWx0cmEtY29uZGVuc2VkXCIsIFwidWx0cmEtZXhwYW5kZWRcIiwgXCJ1bmRlcmxpbmVcIiwgXCJ1cFwiLCBcInVwcGVyLWFscGhhXCIsIFwidXBwZXItYXJtZW5pYW5cIiwgXCJ1cHBlci1ncmVla1wiLCBcInVwcGVyLWhleGFkZWNpbWFsXCIsIFwidXBwZXItbGF0aW5cIiwgXCJ1cHBlci1ub3J3ZWdpYW5cIiwgXCJ1cHBlci1yb21hblwiLCBcInVwcGVyY2FzZVwiLCBcInVyZHVcIiwgXCJ1cmxcIiwgXCJ2YXJcIiwgXCJ2ZXJ0aWNhbFwiLCBcInZlcnRpY2FsLXRleHRcIiwgXCJ2aXNpYmxlXCIsIFwidmlzaWJsZUZpbGxcIiwgXCJ2aXNpYmxlUGFpbnRlZFwiLCBcInZpc2libGVTdHJva2VcIiwgXCJ2aXN1YWxcIiwgXCJ3LXJlc2l6ZVwiLCBcIndhaXRcIiwgXCJ3YXZlXCIsIFwid2lkZXJcIiwgXCJ3aW5kb3dcIiwgXCJ3aW5kb3dmcmFtZVwiLCBcIndpbmRvd3RleHRcIiwgXCJ3b3Jkc1wiLCBcIngtbGFyZ2VcIiwgXCJ4LXNtYWxsXCIsIFwieG9yXCIsIFwieHgtbGFyZ2VcIiwgXCJ4eC1zbWFsbFwiLCBcImJpY3ViaWNcIiwgXCJvcHRpbWl6ZXNwZWVkXCIsIFwiZ3JheXNjYWxlXCIsIFwicm93XCIsIFwicm93LXJldmVyc2VcIiwgXCJ3cmFwXCIsIFwid3JhcC1yZXZlcnNlXCIsIFwiY29sdW1uLXJldmVyc2VcIiwgXCJmbGV4LXN0YXJ0XCIsIFwiZmxleC1lbmRcIiwgXCJzcGFjZS1iZXR3ZWVuXCIsIFwic3BhY2UtYXJvdW5kXCIsIFwidW5zZXRcIl07XG52YXIgd29yZE9wZXJhdG9yS2V5d29yZHNfID0gW1wiaW5cIiwgXCJhbmRcIiwgXCJvclwiLCBcIm5vdFwiLCBcImlzIG5vdFwiLCBcImlzIGFcIiwgXCJpc1wiLCBcImlzbnRcIiwgXCJkZWZpbmVkXCIsIFwiaWYgdW5sZXNzXCJdLFxuICBibG9ja0tleXdvcmRzXyA9IFtcImZvclwiLCBcImlmXCIsIFwiZWxzZVwiLCBcInVubGVzc1wiLCBcImZyb21cIiwgXCJ0b1wiXSxcbiAgY29tbW9uQXRvbXNfID0gW1wibnVsbFwiLCBcInRydWVcIiwgXCJmYWxzZVwiLCBcImhyZWZcIiwgXCJ0aXRsZVwiLCBcInR5cGVcIiwgXCJub3QtYWxsb3dlZFwiLCBcInJlYWRvbmx5XCIsIFwiZGlzYWJsZWRcIl0sXG4gIGNvbW1vbkRlZl8gPSBbXCJAZm9udC1mYWNlXCIsIFwiQGtleWZyYW1lc1wiLCBcIkBtZWRpYVwiLCBcIkB2aWV3cG9ydFwiLCBcIkBwYWdlXCIsIFwiQGhvc3RcIiwgXCJAc3VwcG9ydHNcIiwgXCJAYmxvY2tcIiwgXCJAY3NzXCJdO1xudmFyIGhpbnRXb3JkcyA9IHRhZ0tleXdvcmRzXy5jb25jYXQoZG9jdW1lbnRUeXBlc18sIG1lZGlhVHlwZXNfLCBtZWRpYUZlYXR1cmVzXywgcHJvcGVydHlLZXl3b3Jkc18sIG5vblN0YW5kYXJkUHJvcGVydHlLZXl3b3Jkc18sIGNvbG9yS2V5d29yZHNfLCB2YWx1ZUtleXdvcmRzXywgZm9udFByb3BlcnRpZXNfLCB3b3JkT3BlcmF0b3JLZXl3b3Jkc18sIGJsb2NrS2V5d29yZHNfLCBjb21tb25BdG9tc18sIGNvbW1vbkRlZl8pO1xuZnVuY3Rpb24gd29yZFJlZ2V4cCh3b3Jkcykge1xuICB3b3JkcyA9IHdvcmRzLnNvcnQoZnVuY3Rpb24gKGEsIGIpIHtcbiAgICByZXR1cm4gYiA+IGE7XG4gIH0pO1xuICByZXR1cm4gbmV3IFJlZ0V4cChcIl4oKFwiICsgd29yZHMuam9pbihcIil8KFwiKSArIFwiKSlcXFxcYlwiKTtcbn1cbmZ1bmN0aW9uIGtleVNldChhcnJheSkge1xuICB2YXIga2V5cyA9IHt9O1xuICBmb3IgKHZhciBpID0gMDsgaSA8IGFycmF5Lmxlbmd0aDsgKytpKSBrZXlzW2FycmF5W2ldXSA9IHRydWU7XG4gIHJldHVybiBrZXlzO1xufVxuZnVuY3Rpb24gZXNjYXBlUmVnRXhwKHRleHQpIHtcbiAgcmV0dXJuIHRleHQucmVwbGFjZSgvWy1bXFxde30oKSorPy4sXFxcXF4kfCNcXHNdL2csIFwiXFxcXCQmXCIpO1xufVxudmFyIHRhZ0tleXdvcmRzID0ga2V5U2V0KHRhZ0tleXdvcmRzXyksXG4gIHRhZ1ZhcmlhYmxlc1JlZ2V4cCA9IC9eKGF8YnxpfHN8Y29sfGVtKSQvaSxcbiAgcHJvcGVydHlLZXl3b3JkcyA9IGtleVNldChwcm9wZXJ0eUtleXdvcmRzXyksXG4gIG5vblN0YW5kYXJkUHJvcGVydHlLZXl3b3JkcyA9IGtleVNldChub25TdGFuZGFyZFByb3BlcnR5S2V5d29yZHNfKSxcbiAgdmFsdWVLZXl3b3JkcyA9IGtleVNldCh2YWx1ZUtleXdvcmRzXyksXG4gIGNvbG9yS2V5d29yZHMgPSBrZXlTZXQoY29sb3JLZXl3b3Jkc18pLFxuICBkb2N1bWVudFR5cGVzID0ga2V5U2V0KGRvY3VtZW50VHlwZXNfKSxcbiAgZG9jdW1lbnRUeXBlc1JlZ2V4cCA9IHdvcmRSZWdleHAoZG9jdW1lbnRUeXBlc18pLFxuICBtZWRpYUZlYXR1cmVzID0ga2V5U2V0KG1lZGlhRmVhdHVyZXNfKSxcbiAgbWVkaWFUeXBlcyA9IGtleVNldChtZWRpYVR5cGVzXyksXG4gIGZvbnRQcm9wZXJ0aWVzID0ga2V5U2V0KGZvbnRQcm9wZXJ0aWVzXyksXG4gIG9wZXJhdG9yc1JlZ2V4cCA9IC9eXFxzKihbLl17MiwzfXwmJnxcXHxcXHx8XFwqXFwqfFs/IT06XT89fFstKypcXC8lPD5dPT98XFw/OnxcXH4pLyxcbiAgd29yZE9wZXJhdG9yS2V5d29yZHNSZWdleHAgPSB3b3JkUmVnZXhwKHdvcmRPcGVyYXRvcktleXdvcmRzXyksXG4gIGJsb2NrS2V5d29yZHMgPSBrZXlTZXQoYmxvY2tLZXl3b3Jkc18pLFxuICB2ZW5kb3JQcmVmaXhlc1JlZ2V4cCA9IG5ldyBSZWdFeHAoL15cXC0obW96fG1zfG98d2Via2l0KS0vaSksXG4gIGNvbW1vbkF0b21zID0ga2V5U2V0KGNvbW1vbkF0b21zXyksXG4gIGZpcnN0V29yZE1hdGNoID0gXCJcIixcbiAgc3RhdGVzID0ge30sXG4gIGNoLFxuICBzdHlsZSxcbiAgdHlwZSxcbiAgb3ZlcnJpZGU7XG5cbi8qKlxuICogVG9rZW5pemVyc1xuICovXG5mdW5jdGlvbiB0b2tlbkJhc2Uoc3RyZWFtLCBzdGF0ZSkge1xuICBmaXJzdFdvcmRNYXRjaCA9IHN0cmVhbS5zdHJpbmcubWF0Y2goLyheW1xcdy1dK1xccyo9XFxzKiQpfCheXFxzKltcXHctXStcXHMqPVxccypbXFx3LV0pfCheXFxzKihcXC58I3xAfFxcJHxcXCZ8XFxbfFxcZHxcXCt8Ojo/fFxce3xcXD58fnxcXC8pP1xccypbXFx3LV0qKFthLXowLTktXXxcXCp8XFwvXFwqKShcXCh8LCk/KS8pO1xuICBzdGF0ZS5jb250ZXh0LmxpbmUuZmlyc3RXb3JkID0gZmlyc3RXb3JkTWF0Y2ggPyBmaXJzdFdvcmRNYXRjaFswXS5yZXBsYWNlKC9eXFxzKi8sIFwiXCIpIDogXCJcIjtcbiAgc3RhdGUuY29udGV4dC5saW5lLmluZGVudCA9IHN0cmVhbS5pbmRlbnRhdGlvbigpO1xuICBjaCA9IHN0cmVhbS5wZWVrKCk7XG5cbiAgLy8gTGluZSBjb21tZW50XG4gIGlmIChzdHJlYW0ubWF0Y2goXCIvL1wiKSkge1xuICAgIHN0cmVhbS5za2lwVG9FbmQoKTtcbiAgICByZXR1cm4gW1wiY29tbWVudFwiLCBcImNvbW1lbnRcIl07XG4gIH1cbiAgLy8gQmxvY2sgY29tbWVudFxuICBpZiAoc3RyZWFtLm1hdGNoKFwiLypcIikpIHtcbiAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQ0NvbW1lbnQ7XG4gICAgcmV0dXJuIHRva2VuQ0NvbW1lbnQoc3RyZWFtLCBzdGF0ZSk7XG4gIH1cbiAgLy8gU3RyaW5nXG4gIGlmIChjaCA9PSBcIlxcXCJcIiB8fCBjaCA9PSBcIidcIikge1xuICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgc3RhdGUudG9rZW5pemUgPSB0b2tlblN0cmluZyhjaCk7XG4gICAgcmV0dXJuIHN0YXRlLnRva2VuaXplKHN0cmVhbSwgc3RhdGUpO1xuICB9XG4gIC8vIERlZlxuICBpZiAoY2ggPT0gXCJAXCIpIHtcbiAgICBzdHJlYW0ubmV4dCgpO1xuICAgIHN0cmVhbS5lYXRXaGlsZSgvW1xcd1xcXFwtXS8pO1xuICAgIHJldHVybiBbXCJkZWZcIiwgc3RyZWFtLmN1cnJlbnQoKV07XG4gIH1cbiAgLy8gSUQgc2VsZWN0b3Igb3IgSGV4IGNvbG9yXG4gIGlmIChjaCA9PSBcIiNcIikge1xuICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgLy8gSGV4IGNvbG9yXG4gICAgaWYgKHN0cmVhbS5tYXRjaCgvXlswLTlhLWZdezN9KFswLTlhLWZdKFswLTlhLWZdezJ9KXswLDJ9KT9cXGIoPyEtKS9pKSkge1xuICAgICAgcmV0dXJuIFtcImF0b21cIiwgXCJhdG9tXCJdO1xuICAgIH1cbiAgICAvLyBJRCBzZWxlY3RvclxuICAgIGlmIChzdHJlYW0ubWF0Y2goL15bYS16XVtcXHctXSovaSkpIHtcbiAgICAgIHJldHVybiBbXCJidWlsdGluXCIsIFwiaGFzaFwiXTtcbiAgICB9XG4gIH1cbiAgLy8gVmVuZG9yIHByZWZpeGVzXG4gIGlmIChzdHJlYW0ubWF0Y2godmVuZG9yUHJlZml4ZXNSZWdleHApKSB7XG4gICAgcmV0dXJuIFtcIm1ldGFcIiwgXCJ2ZW5kb3ItcHJlZml4ZXNcIl07XG4gIH1cbiAgLy8gTnVtYmVyc1xuICBpZiAoc3RyZWFtLm1hdGNoKC9eLT9bMC05XT9cXC4/WzAtOV0vKSkge1xuICAgIHN0cmVhbS5lYXRXaGlsZSgvW2EteiVdL2kpO1xuICAgIHJldHVybiBbXCJudW1iZXJcIiwgXCJ1bml0XCJdO1xuICB9XG4gIC8vICFpbXBvcnRhbnR8b3B0aW9uYWxcbiAgaWYgKGNoID09IFwiIVwiKSB7XG4gICAgc3RyZWFtLm5leHQoKTtcbiAgICByZXR1cm4gW3N0cmVhbS5tYXRjaCgvXihpbXBvcnRhbnR8b3B0aW9uYWwpL2kpID8gXCJrZXl3b3JkXCIgOiBcIm9wZXJhdG9yXCIsIFwiaW1wb3J0YW50XCJdO1xuICB9XG4gIC8vIENsYXNzXG4gIGlmIChjaCA9PSBcIi5cIiAmJiBzdHJlYW0ubWF0Y2goL15cXC5bYS16XVtcXHctXSovaSkpIHtcbiAgICByZXR1cm4gW1wicXVhbGlmaWVyXCIsIFwicXVhbGlmaWVyXCJdO1xuICB9XG4gIC8vIHVybCB1cmwtcHJlZml4IGRvbWFpbiByZWdleHBcbiAgaWYgKHN0cmVhbS5tYXRjaChkb2N1bWVudFR5cGVzUmVnZXhwKSkge1xuICAgIGlmIChzdHJlYW0ucGVlaygpID09IFwiKFwiKSBzdGF0ZS50b2tlbml6ZSA9IHRva2VuUGFyZW50aGVzaXplZDtcbiAgICByZXR1cm4gW1wicHJvcGVydHlcIiwgXCJ3b3JkXCJdO1xuICB9XG4gIC8vIE1peGlucyAvIEZ1bmN0aW9uc1xuICBpZiAoc3RyZWFtLm1hdGNoKC9eW2Etel1bXFx3LV0qXFwoL2kpKSB7XG4gICAgc3RyZWFtLmJhY2tVcCgxKTtcbiAgICByZXR1cm4gW1wia2V5d29yZFwiLCBcIm1peGluXCJdO1xuICB9XG4gIC8vIEJsb2NrIG1peGluc1xuICBpZiAoc3RyZWFtLm1hdGNoKC9eKFxcK3wtKVthLXpdW1xcdy1dKlxcKC9pKSkge1xuICAgIHN0cmVhbS5iYWNrVXAoMSk7XG4gICAgcmV0dXJuIFtcImtleXdvcmRcIiwgXCJibG9jay1taXhpblwiXTtcbiAgfVxuICAvLyBQYXJlbnQgUmVmZXJlbmNlIEJFTSBuYW1pbmdcbiAgaWYgKHN0cmVhbS5zdHJpbmcubWF0Y2goL15cXHMqJi8pICYmIHN0cmVhbS5tYXRjaCgvXlstX10rW2Etel1bXFx3LV0qLykpIHtcbiAgICByZXR1cm4gW1wicXVhbGlmaWVyXCIsIFwicXVhbGlmaWVyXCJdO1xuICB9XG4gIC8vIC8gUm9vdCBSZWZlcmVuY2UgJiBQYXJlbnQgUmVmZXJlbmNlXG4gIGlmIChzdHJlYW0ubWF0Y2goL14oXFwvfCYpKC18X3w6fFxcLnwjfFthLXpdKS8pKSB7XG4gICAgc3RyZWFtLmJhY2tVcCgxKTtcbiAgICByZXR1cm4gW1widmFyaWFibGVOYW1lLnNwZWNpYWxcIiwgXCJyZWZlcmVuY2VcIl07XG4gIH1cbiAgaWYgKHN0cmVhbS5tYXRjaCgvXiZ7MX1cXHMqJC8pKSB7XG4gICAgcmV0dXJuIFtcInZhcmlhYmxlTmFtZS5zcGVjaWFsXCIsIFwicmVmZXJlbmNlXCJdO1xuICB9XG4gIC8vIFdvcmQgb3BlcmF0b3JcbiAgaWYgKHN0cmVhbS5tYXRjaCh3b3JkT3BlcmF0b3JLZXl3b3Jkc1JlZ2V4cCkpIHtcbiAgICByZXR1cm4gW1wib3BlcmF0b3JcIiwgXCJvcGVyYXRvclwiXTtcbiAgfVxuICAvLyBXb3JkXG4gIGlmIChzdHJlYW0ubWF0Y2goL15cXCQ/Wy1fXSpbYS16MC05XStbXFx3LV0qL2kpKSB7XG4gICAgLy8gVmFyaWFibGVcbiAgICBpZiAoc3RyZWFtLm1hdGNoKC9eKFxcLnxcXFspW1xcdy1cXCdcXFwiXFxdXSsvaSwgZmFsc2UpKSB7XG4gICAgICBpZiAoIXdvcmRJc1RhZyhzdHJlYW0uY3VycmVudCgpKSkge1xuICAgICAgICBzdHJlYW0ubWF0Y2goJy4nKTtcbiAgICAgICAgcmV0dXJuIFtcInZhcmlhYmxlXCIsIFwidmFyaWFibGUtbmFtZVwiXTtcbiAgICAgIH1cbiAgICB9XG4gICAgcmV0dXJuIFtcInZhcmlhYmxlXCIsIFwid29yZFwiXTtcbiAgfVxuICAvLyBPcGVyYXRvcnNcbiAgaWYgKHN0cmVhbS5tYXRjaChvcGVyYXRvcnNSZWdleHApKSB7XG4gICAgcmV0dXJuIFtcIm9wZXJhdG9yXCIsIHN0cmVhbS5jdXJyZW50KCldO1xuICB9XG4gIC8vIERlbGltaXRlcnNcbiAgaWYgKC9bOjsse31cXFtcXF1cXChcXCldLy50ZXN0KGNoKSkge1xuICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgcmV0dXJuIFtudWxsLCBjaF07XG4gIH1cbiAgLy8gTm9uLWRldGVjdGVkIGl0ZW1zXG4gIHN0cmVhbS5uZXh0KCk7XG4gIHJldHVybiBbbnVsbCwgbnVsbF07XG59XG5cbi8qKlxuICogVG9rZW4gY29tbWVudFxuICovXG5mdW5jdGlvbiB0b2tlbkNDb21tZW50KHN0cmVhbSwgc3RhdGUpIHtcbiAgdmFyIG1heWJlRW5kID0gZmFsc2UsXG4gICAgY2g7XG4gIHdoaWxlICgoY2ggPSBzdHJlYW0ubmV4dCgpKSAhPSBudWxsKSB7XG4gICAgaWYgKG1heWJlRW5kICYmIGNoID09IFwiL1wiKSB7XG4gICAgICBzdGF0ZS50b2tlbml6ZSA9IG51bGw7XG4gICAgICBicmVhaztcbiAgICB9XG4gICAgbWF5YmVFbmQgPSBjaCA9PSBcIipcIjtcbiAgfVxuICByZXR1cm4gW1wiY29tbWVudFwiLCBcImNvbW1lbnRcIl07XG59XG5cbi8qKlxuICogVG9rZW4gc3RyaW5nXG4gKi9cbmZ1bmN0aW9uIHRva2VuU3RyaW5nKHF1b3RlKSB7XG4gIHJldHVybiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIHZhciBlc2NhcGVkID0gZmFsc2UsXG4gICAgICBjaDtcbiAgICB3aGlsZSAoKGNoID0gc3RyZWFtLm5leHQoKSkgIT0gbnVsbCkge1xuICAgICAgaWYgKGNoID09IHF1b3RlICYmICFlc2NhcGVkKSB7XG4gICAgICAgIGlmIChxdW90ZSA9PSBcIilcIikgc3RyZWFtLmJhY2tVcCgxKTtcbiAgICAgICAgYnJlYWs7XG4gICAgICB9XG4gICAgICBlc2NhcGVkID0gIWVzY2FwZWQgJiYgY2ggPT0gXCJcXFxcXCI7XG4gICAgfVxuICAgIGlmIChjaCA9PSBxdW90ZSB8fCAhZXNjYXBlZCAmJiBxdW90ZSAhPSBcIilcIikgc3RhdGUudG9rZW5pemUgPSBudWxsO1xuICAgIHJldHVybiBbXCJzdHJpbmdcIiwgXCJzdHJpbmdcIl07XG4gIH07XG59XG5cbi8qKlxuICogVG9rZW4gcGFyZW50aGVzaXplZFxuICovXG5mdW5jdGlvbiB0b2tlblBhcmVudGhlc2l6ZWQoc3RyZWFtLCBzdGF0ZSkge1xuICBzdHJlYW0ubmV4dCgpOyAvLyBNdXN0IGJlIFwiKFwiXG4gIGlmICghc3RyZWFtLm1hdGNoKC9cXHMqW1xcXCJcXCcpXS8sIGZhbHNlKSkgc3RhdGUudG9rZW5pemUgPSB0b2tlblN0cmluZyhcIilcIik7ZWxzZSBzdGF0ZS50b2tlbml6ZSA9IG51bGw7XG4gIHJldHVybiBbbnVsbCwgXCIoXCJdO1xufVxuXG4vKipcbiAqIENvbnRleHQgbWFuYWdlbWVudFxuICovXG5mdW5jdGlvbiBDb250ZXh0KHR5cGUsIGluZGVudCwgcHJldiwgbGluZSkge1xuICB0aGlzLnR5cGUgPSB0eXBlO1xuICB0aGlzLmluZGVudCA9IGluZGVudDtcbiAgdGhpcy5wcmV2ID0gcHJldjtcbiAgdGhpcy5saW5lID0gbGluZSB8fCB7XG4gICAgZmlyc3RXb3JkOiBcIlwiLFxuICAgIGluZGVudDogMFxuICB9O1xufVxuZnVuY3Rpb24gcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbSwgdHlwZSwgaW5kZW50KSB7XG4gIGluZGVudCA9IGluZGVudCA+PSAwID8gaW5kZW50IDogc3RyZWFtLmluZGVudFVuaXQ7XG4gIHN0YXRlLmNvbnRleHQgPSBuZXcgQ29udGV4dCh0eXBlLCBzdHJlYW0uaW5kZW50YXRpb24oKSArIGluZGVudCwgc3RhdGUuY29udGV4dCk7XG4gIHJldHVybiB0eXBlO1xufVxuZnVuY3Rpb24gcG9wQ29udGV4dChzdGF0ZSwgc3RyZWFtLCBjdXJyZW50SW5kZW50KSB7XG4gIHZhciBjb250ZXh0SW5kZW50ID0gc3RhdGUuY29udGV4dC5pbmRlbnQgLSBzdHJlYW0uaW5kZW50VW5pdDtcbiAgY3VycmVudEluZGVudCA9IGN1cnJlbnRJbmRlbnQgfHwgZmFsc2U7XG4gIHN0YXRlLmNvbnRleHQgPSBzdGF0ZS5jb250ZXh0LnByZXY7XG4gIGlmIChjdXJyZW50SW5kZW50KSBzdGF0ZS5jb250ZXh0LmluZGVudCA9IGNvbnRleHRJbmRlbnQ7XG4gIHJldHVybiBzdGF0ZS5jb250ZXh0LnR5cGU7XG59XG5mdW5jdGlvbiBwYXNzKHR5cGUsIHN0cmVhbSwgc3RhdGUpIHtcbiAgcmV0dXJuIHN0YXRlc1tzdGF0ZS5jb250ZXh0LnR5cGVdKHR5cGUsIHN0cmVhbSwgc3RhdGUpO1xufVxuZnVuY3Rpb24gcG9wQW5kUGFzcyh0eXBlLCBzdHJlYW0sIHN0YXRlLCBuKSB7XG4gIGZvciAodmFyIGkgPSBuIHx8IDE7IGkgPiAwOyBpLS0pIHN0YXRlLmNvbnRleHQgPSBzdGF0ZS5jb250ZXh0LnByZXY7XG4gIHJldHVybiBwYXNzKHR5cGUsIHN0cmVhbSwgc3RhdGUpO1xufVxuXG4vKipcbiAqIFBhcnNlclxuICovXG5mdW5jdGlvbiB3b3JkSXNUYWcod29yZCkge1xuICByZXR1cm4gd29yZC50b0xvd2VyQ2FzZSgpIGluIHRhZ0tleXdvcmRzO1xufVxuZnVuY3Rpb24gd29yZElzUHJvcGVydHkod29yZCkge1xuICB3b3JkID0gd29yZC50b0xvd2VyQ2FzZSgpO1xuICByZXR1cm4gd29yZCBpbiBwcm9wZXJ0eUtleXdvcmRzIHx8IHdvcmQgaW4gZm9udFByb3BlcnRpZXM7XG59XG5mdW5jdGlvbiB3b3JkSXNCbG9jayh3b3JkKSB7XG4gIHJldHVybiB3b3JkLnRvTG93ZXJDYXNlKCkgaW4gYmxvY2tLZXl3b3Jkcztcbn1cbmZ1bmN0aW9uIHdvcmRJc1ZlbmRvclByZWZpeCh3b3JkKSB7XG4gIHJldHVybiB3b3JkLnRvTG93ZXJDYXNlKCkubWF0Y2godmVuZG9yUHJlZml4ZXNSZWdleHApO1xufVxuZnVuY3Rpb24gd29yZEFzVmFsdWUod29yZCkge1xuICB2YXIgd29yZExDID0gd29yZC50b0xvd2VyQ2FzZSgpO1xuICB2YXIgb3ZlcnJpZGUgPSBcInZhcmlhYmxlXCI7XG4gIGlmICh3b3JkSXNUYWcod29yZCkpIG92ZXJyaWRlID0gXCJ0YWdcIjtlbHNlIGlmICh3b3JkSXNCbG9jayh3b3JkKSkgb3ZlcnJpZGUgPSBcImJsb2NrLWtleXdvcmRcIjtlbHNlIGlmICh3b3JkSXNQcm9wZXJ0eSh3b3JkKSkgb3ZlcnJpZGUgPSBcInByb3BlcnR5XCI7ZWxzZSBpZiAod29yZExDIGluIHZhbHVlS2V5d29yZHMgfHwgd29yZExDIGluIGNvbW1vbkF0b21zKSBvdmVycmlkZSA9IFwiYXRvbVwiO2Vsc2UgaWYgKHdvcmRMQyA9PSBcInJldHVyblwiIHx8IHdvcmRMQyBpbiBjb2xvcktleXdvcmRzKSBvdmVycmlkZSA9IFwia2V5d29yZFwiO1xuXG4gIC8vIEZvbnQgZmFtaWx5XG4gIGVsc2UgaWYgKHdvcmQubWF0Y2goL15bQS1aXS8pKSBvdmVycmlkZSA9IFwic3RyaW5nXCI7XG4gIHJldHVybiBvdmVycmlkZTtcbn1cbmZ1bmN0aW9uIHR5cGVJc0Jsb2NrKHR5cGUsIHN0cmVhbSkge1xuICByZXR1cm4gZW5kT2ZMaW5lKHN0cmVhbSkgJiYgKHR5cGUgPT0gXCJ7XCIgfHwgdHlwZSA9PSBcIl1cIiB8fCB0eXBlID09IFwiaGFzaFwiIHx8IHR5cGUgPT0gXCJxdWFsaWZpZXJcIikgfHwgdHlwZSA9PSBcImJsb2NrLW1peGluXCI7XG59XG5mdW5jdGlvbiB0eXBlSXNJbnRlcnBvbGF0aW9uKHR5cGUsIHN0cmVhbSkge1xuICByZXR1cm4gdHlwZSA9PSBcIntcIiAmJiBzdHJlYW0ubWF0Y2goL15cXHMqXFwkP1tcXHctXSsvaSwgZmFsc2UpO1xufVxuZnVuY3Rpb24gdHlwZUlzUHNldWRvKHR5cGUsIHN0cmVhbSkge1xuICByZXR1cm4gdHlwZSA9PSBcIjpcIiAmJiBzdHJlYW0ubWF0Y2goL15bYS16LV0rLywgZmFsc2UpO1xufVxuZnVuY3Rpb24gc3RhcnRPZkxpbmUoc3RyZWFtKSB7XG4gIHJldHVybiBzdHJlYW0uc29sKCkgfHwgc3RyZWFtLnN0cmluZy5tYXRjaChuZXcgUmVnRXhwKFwiXlxcXFxzKlwiICsgZXNjYXBlUmVnRXhwKHN0cmVhbS5jdXJyZW50KCkpKSk7XG59XG5mdW5jdGlvbiBlbmRPZkxpbmUoc3RyZWFtKSB7XG4gIHJldHVybiBzdHJlYW0uZW9sKCkgfHwgc3RyZWFtLm1hdGNoKC9eXFxzKiQvLCBmYWxzZSk7XG59XG5mdW5jdGlvbiBmaXJzdFdvcmRPZkxpbmUobGluZSkge1xuICB2YXIgcmUgPSAvXlxccypbLV9dKlthLXowLTldK1tcXHctXSovaTtcbiAgdmFyIHJlc3VsdCA9IHR5cGVvZiBsaW5lID09IFwic3RyaW5nXCIgPyBsaW5lLm1hdGNoKHJlKSA6IGxpbmUuc3RyaW5nLm1hdGNoKHJlKTtcbiAgcmV0dXJuIHJlc3VsdCA/IHJlc3VsdFswXS5yZXBsYWNlKC9eXFxzKi8sIFwiXCIpIDogXCJcIjtcbn1cblxuLyoqXG4gKiBCbG9ja1xuICovXG5zdGF0ZXMuYmxvY2sgPSBmdW5jdGlvbiAodHlwZSwgc3RyZWFtLCBzdGF0ZSkge1xuICBpZiAodHlwZSA9PSBcImNvbW1lbnRcIiAmJiBzdGFydE9mTGluZShzdHJlYW0pIHx8IHR5cGUgPT0gXCIsXCIgJiYgZW5kT2ZMaW5lKHN0cmVhbSkgfHwgdHlwZSA9PSBcIm1peGluXCIpIHtcbiAgICByZXR1cm4gcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbSwgXCJibG9ja1wiLCAwKTtcbiAgfVxuICBpZiAodHlwZUlzSW50ZXJwb2xhdGlvbih0eXBlLCBzdHJlYW0pKSB7XG4gICAgcmV0dXJuIHB1c2hDb250ZXh0KHN0YXRlLCBzdHJlYW0sIFwiaW50ZXJwb2xhdGlvblwiKTtcbiAgfVxuICBpZiAoZW5kT2ZMaW5lKHN0cmVhbSkgJiYgdHlwZSA9PSBcIl1cIikge1xuICAgIGlmICghL15cXHMqKFxcLnwjfDp8XFxbfFxcKnwmKS8udGVzdChzdHJlYW0uc3RyaW5nKSAmJiAhd29yZElzVGFnKGZpcnN0V29yZE9mTGluZShzdHJlYW0pKSkge1xuICAgICAgcmV0dXJuIHB1c2hDb250ZXh0KHN0YXRlLCBzdHJlYW0sIFwiYmxvY2tcIiwgMCk7XG4gICAgfVxuICB9XG4gIGlmICh0eXBlSXNCbG9jayh0eXBlLCBzdHJlYW0pKSB7XG4gICAgcmV0dXJuIHB1c2hDb250ZXh0KHN0YXRlLCBzdHJlYW0sIFwiYmxvY2tcIik7XG4gIH1cbiAgaWYgKHR5cGUgPT0gXCJ9XCIgJiYgZW5kT2ZMaW5lKHN0cmVhbSkpIHtcbiAgICByZXR1cm4gcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbSwgXCJibG9ja1wiLCAwKTtcbiAgfVxuICBpZiAodHlwZSA9PSBcInZhcmlhYmxlLW5hbWVcIikge1xuICAgIGlmIChzdHJlYW0uc3RyaW5nLm1hdGNoKC9eXFxzP1xcJFtcXHctXFwuXFxbXFxdXFwnXFxcIl0rJC8pIHx8IHdvcmRJc0Jsb2NrKGZpcnN0V29yZE9mTGluZShzdHJlYW0pKSkge1xuICAgICAgcmV0dXJuIHB1c2hDb250ZXh0KHN0YXRlLCBzdHJlYW0sIFwidmFyaWFibGVOYW1lXCIpO1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbSwgXCJ2YXJpYWJsZU5hbWVcIiwgMCk7XG4gICAgfVxuICB9XG4gIGlmICh0eXBlID09IFwiPVwiKSB7XG4gICAgaWYgKCFlbmRPZkxpbmUoc3RyZWFtKSAmJiAhd29yZElzQmxvY2soZmlyc3RXb3JkT2ZMaW5lKHN0cmVhbSkpKSB7XG4gICAgICByZXR1cm4gcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbSwgXCJibG9ja1wiLCAwKTtcbiAgICB9XG4gICAgcmV0dXJuIHB1c2hDb250ZXh0KHN0YXRlLCBzdHJlYW0sIFwiYmxvY2tcIik7XG4gIH1cbiAgaWYgKHR5cGUgPT0gXCIqXCIpIHtcbiAgICBpZiAoZW5kT2ZMaW5lKHN0cmVhbSkgfHwgc3RyZWFtLm1hdGNoKC9cXHMqKCx8XFwufCN8XFxbfDp8eykvLCBmYWxzZSkpIHtcbiAgICAgIG92ZXJyaWRlID0gXCJ0YWdcIjtcbiAgICAgIHJldHVybiBwdXNoQ29udGV4dChzdGF0ZSwgc3RyZWFtLCBcImJsb2NrXCIpO1xuICAgIH1cbiAgfVxuICBpZiAodHlwZUlzUHNldWRvKHR5cGUsIHN0cmVhbSkpIHtcbiAgICByZXR1cm4gcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbSwgXCJwc2V1ZG9cIik7XG4gIH1cbiAgaWYgKC9AKGZvbnQtZmFjZXxtZWRpYXxzdXBwb3J0c3woLW1vei0pP2RvY3VtZW50KS8udGVzdCh0eXBlKSkge1xuICAgIHJldHVybiBwdXNoQ29udGV4dChzdGF0ZSwgc3RyZWFtLCBlbmRPZkxpbmUoc3RyZWFtKSA/IFwiYmxvY2tcIiA6IFwiYXRCbG9ja1wiKTtcbiAgfVxuICBpZiAoL0AoLShtb3p8bXN8b3x3ZWJraXQpLSk/a2V5ZnJhbWVzJC8udGVzdCh0eXBlKSkge1xuICAgIHJldHVybiBwdXNoQ29udGV4dChzdGF0ZSwgc3RyZWFtLCBcImtleWZyYW1lc1wiKTtcbiAgfVxuICBpZiAoL0BleHRlbmRzPy8udGVzdCh0eXBlKSkge1xuICAgIHJldHVybiBwdXNoQ29udGV4dChzdGF0ZSwgc3RyZWFtLCBcImV4dGVuZFwiLCAwKTtcbiAgfVxuICBpZiAodHlwZSAmJiB0eXBlLmNoYXJBdCgwKSA9PSBcIkBcIikge1xuICAgIC8vIFByb3BlcnR5IExvb2t1cFxuICAgIGlmIChzdHJlYW0uaW5kZW50YXRpb24oKSA+IDAgJiYgd29yZElzUHJvcGVydHkoc3RyZWFtLmN1cnJlbnQoKS5zbGljZSgxKSkpIHtcbiAgICAgIG92ZXJyaWRlID0gXCJ2YXJpYWJsZVwiO1xuICAgICAgcmV0dXJuIFwiYmxvY2tcIjtcbiAgICB9XG4gICAgaWYgKC8oQGltcG9ydHxAcmVxdWlyZXxAY2hhcnNldCkvLnRlc3QodHlwZSkpIHtcbiAgICAgIHJldHVybiBwdXNoQ29udGV4dChzdGF0ZSwgc3RyZWFtLCBcImJsb2NrXCIsIDApO1xuICAgIH1cbiAgICByZXR1cm4gcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbSwgXCJibG9ja1wiKTtcbiAgfVxuICBpZiAodHlwZSA9PSBcInJlZmVyZW5jZVwiICYmIGVuZE9mTGluZShzdHJlYW0pKSB7XG4gICAgcmV0dXJuIHB1c2hDb250ZXh0KHN0YXRlLCBzdHJlYW0sIFwiYmxvY2tcIik7XG4gIH1cbiAgaWYgKHR5cGUgPT0gXCIoXCIpIHtcbiAgICByZXR1cm4gcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbSwgXCJwYXJlbnNcIik7XG4gIH1cbiAgaWYgKHR5cGUgPT0gXCJ2ZW5kb3ItcHJlZml4ZXNcIikge1xuICAgIHJldHVybiBwdXNoQ29udGV4dChzdGF0ZSwgc3RyZWFtLCBcInZlbmRvclByZWZpeGVzXCIpO1xuICB9XG4gIGlmICh0eXBlID09IFwid29yZFwiKSB7XG4gICAgdmFyIHdvcmQgPSBzdHJlYW0uY3VycmVudCgpO1xuICAgIG92ZXJyaWRlID0gd29yZEFzVmFsdWUod29yZCk7XG4gICAgaWYgKG92ZXJyaWRlID09IFwicHJvcGVydHlcIikge1xuICAgICAgaWYgKHN0YXJ0T2ZMaW5lKHN0cmVhbSkpIHtcbiAgICAgICAgcmV0dXJuIHB1c2hDb250ZXh0KHN0YXRlLCBzdHJlYW0sIFwiYmxvY2tcIiwgMCk7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBvdmVycmlkZSA9IFwiYXRvbVwiO1xuICAgICAgICByZXR1cm4gXCJibG9ja1wiO1xuICAgICAgfVxuICAgIH1cbiAgICBpZiAob3ZlcnJpZGUgPT0gXCJ0YWdcIikge1xuICAgICAgLy8gdGFnIGlzIGEgY3NzIHZhbHVlXG4gICAgICBpZiAoL2VtYmVkfG1lbnV8cHJlfHByb2dyZXNzfHN1Ynx0YWJsZS8udGVzdCh3b3JkKSkge1xuICAgICAgICBpZiAod29yZElzUHJvcGVydHkoZmlyc3RXb3JkT2ZMaW5lKHN0cmVhbSkpKSB7XG4gICAgICAgICAgb3ZlcnJpZGUgPSBcImF0b21cIjtcbiAgICAgICAgICByZXR1cm4gXCJibG9ja1wiO1xuICAgICAgICB9XG4gICAgICB9XG5cbiAgICAgIC8vIHRhZyBpcyBhbiBhdHRyaWJ1dGVcbiAgICAgIGlmIChzdHJlYW0uc3RyaW5nLm1hdGNoKG5ldyBSZWdFeHAoXCJcXFxcW1xcXFxzKlwiICsgd29yZCArIFwifFwiICsgd29yZCArIFwiXFxcXHMqXFxcXF1cIikpKSB7XG4gICAgICAgIG92ZXJyaWRlID0gXCJhdG9tXCI7XG4gICAgICAgIHJldHVybiBcImJsb2NrXCI7XG4gICAgICB9XG5cbiAgICAgIC8vIHRhZyBpcyBhIHZhcmlhYmxlXG4gICAgICBpZiAodGFnVmFyaWFibGVzUmVnZXhwLnRlc3Qod29yZCkpIHtcbiAgICAgICAgaWYgKHN0YXJ0T2ZMaW5lKHN0cmVhbSkgJiYgc3RyZWFtLnN0cmluZy5tYXRjaCgvPS8pIHx8ICFzdGFydE9mTGluZShzdHJlYW0pICYmICFzdHJlYW0uc3RyaW5nLm1hdGNoKC9eKFxccypcXC58I3xcXCZ8XFxbfFxcL3w+fFxcKikvKSAmJiAhd29yZElzVGFnKGZpcnN0V29yZE9mTGluZShzdHJlYW0pKSkge1xuICAgICAgICAgIG92ZXJyaWRlID0gXCJ2YXJpYWJsZVwiO1xuICAgICAgICAgIGlmICh3b3JkSXNCbG9jayhmaXJzdFdvcmRPZkxpbmUoc3RyZWFtKSkpIHJldHVybiBcImJsb2NrXCI7XG4gICAgICAgICAgcmV0dXJuIHB1c2hDb250ZXh0KHN0YXRlLCBzdHJlYW0sIFwiYmxvY2tcIiwgMCk7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICAgIGlmIChlbmRPZkxpbmUoc3RyZWFtKSkgcmV0dXJuIHB1c2hDb250ZXh0KHN0YXRlLCBzdHJlYW0sIFwiYmxvY2tcIik7XG4gICAgfVxuICAgIGlmIChvdmVycmlkZSA9PSBcImJsb2NrLWtleXdvcmRcIikge1xuICAgICAgb3ZlcnJpZGUgPSBcImtleXdvcmRcIjtcblxuICAgICAgLy8gUG9zdGZpeCBjb25kaXRpb25hbHNcbiAgICAgIGlmIChzdHJlYW0uY3VycmVudCgvKGlmfHVubGVzcykvKSAmJiAhc3RhcnRPZkxpbmUoc3RyZWFtKSkge1xuICAgICAgICByZXR1cm4gXCJibG9ja1wiO1xuICAgICAgfVxuICAgICAgcmV0dXJuIHB1c2hDb250ZXh0KHN0YXRlLCBzdHJlYW0sIFwiYmxvY2tcIik7XG4gICAgfVxuICAgIGlmICh3b3JkID09IFwicmV0dXJuXCIpIHJldHVybiBwdXNoQ29udGV4dChzdGF0ZSwgc3RyZWFtLCBcImJsb2NrXCIsIDApO1xuXG4gICAgLy8gUGxhY2Vob2xkZXIgc2VsZWN0b3JcbiAgICBpZiAob3ZlcnJpZGUgPT0gXCJ2YXJpYWJsZVwiICYmIHN0cmVhbS5zdHJpbmcubWF0Y2goL15cXHM/XFwkW1xcdy1cXC5cXFtcXF1cXCdcXFwiXSskLykpIHtcbiAgICAgIHJldHVybiBwdXNoQ29udGV4dChzdGF0ZSwgc3RyZWFtLCBcImJsb2NrXCIpO1xuICAgIH1cbiAgfVxuICByZXR1cm4gc3RhdGUuY29udGV4dC50eXBlO1xufTtcblxuLyoqXG4gKiBQYXJlbnNcbiAqL1xuc3RhdGVzLnBhcmVucyA9IGZ1bmN0aW9uICh0eXBlLCBzdHJlYW0sIHN0YXRlKSB7XG4gIGlmICh0eXBlID09IFwiKFwiKSByZXR1cm4gcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbSwgXCJwYXJlbnNcIik7XG4gIGlmICh0eXBlID09IFwiKVwiKSB7XG4gICAgaWYgKHN0YXRlLmNvbnRleHQucHJldi50eXBlID09IFwicGFyZW5zXCIpIHtcbiAgICAgIHJldHVybiBwb3BDb250ZXh0KHN0YXRlLCBzdHJlYW0pO1xuICAgIH1cbiAgICBpZiAoc3RyZWFtLnN0cmluZy5tYXRjaCgvXlthLXpdW1xcdy1dKlxcKC9pKSAmJiBlbmRPZkxpbmUoc3RyZWFtKSB8fCB3b3JkSXNCbG9jayhmaXJzdFdvcmRPZkxpbmUoc3RyZWFtKSkgfHwgLyhcXC58I3w6fFxcW3xcXCp8Jnw+fH58XFwrfFxcLykvLnRlc3QoZmlyc3RXb3JkT2ZMaW5lKHN0cmVhbSkpIHx8ICFzdHJlYW0uc3RyaW5nLm1hdGNoKC9eLT9bYS16XVtcXHctXFwuXFxbXFxdXFwnXFxcIl0qXFxzKj0vKSAmJiB3b3JkSXNUYWcoZmlyc3RXb3JkT2ZMaW5lKHN0cmVhbSkpKSB7XG4gICAgICByZXR1cm4gcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbSwgXCJibG9ja1wiKTtcbiAgICB9XG4gICAgaWYgKHN0cmVhbS5zdHJpbmcubWF0Y2goL15bXFwkLV0/W2Etel1bXFx3LVxcLlxcW1xcXVxcJ1xcXCJdKlxccyo9LykgfHwgc3RyZWFtLnN0cmluZy5tYXRjaCgvXlxccyooXFwofFxcKXxbMC05XSkvKSB8fCBzdHJlYW0uc3RyaW5nLm1hdGNoKC9eXFxzK1thLXpdW1xcdy1dKlxcKC9pKSB8fCBzdHJlYW0uc3RyaW5nLm1hdGNoKC9eXFxzK1tcXCQtXT9bYS16XS9pKSkge1xuICAgICAgcmV0dXJuIHB1c2hDb250ZXh0KHN0YXRlLCBzdHJlYW0sIFwiYmxvY2tcIiwgMCk7XG4gICAgfVxuICAgIGlmIChlbmRPZkxpbmUoc3RyZWFtKSkgcmV0dXJuIHB1c2hDb250ZXh0KHN0YXRlLCBzdHJlYW0sIFwiYmxvY2tcIik7ZWxzZSByZXR1cm4gcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbSwgXCJibG9ja1wiLCAwKTtcbiAgfVxuICBpZiAodHlwZSAmJiB0eXBlLmNoYXJBdCgwKSA9PSBcIkBcIiAmJiB3b3JkSXNQcm9wZXJ0eShzdHJlYW0uY3VycmVudCgpLnNsaWNlKDEpKSkge1xuICAgIG92ZXJyaWRlID0gXCJ2YXJpYWJsZVwiO1xuICB9XG4gIGlmICh0eXBlID09IFwid29yZFwiKSB7XG4gICAgdmFyIHdvcmQgPSBzdHJlYW0uY3VycmVudCgpO1xuICAgIG92ZXJyaWRlID0gd29yZEFzVmFsdWUod29yZCk7XG4gICAgaWYgKG92ZXJyaWRlID09IFwidGFnXCIgJiYgdGFnVmFyaWFibGVzUmVnZXhwLnRlc3Qod29yZCkpIHtcbiAgICAgIG92ZXJyaWRlID0gXCJ2YXJpYWJsZVwiO1xuICAgIH1cbiAgICBpZiAob3ZlcnJpZGUgPT0gXCJwcm9wZXJ0eVwiIHx8IHdvcmQgPT0gXCJ0b1wiKSBvdmVycmlkZSA9IFwiYXRvbVwiO1xuICB9XG4gIGlmICh0eXBlID09IFwidmFyaWFibGUtbmFtZVwiKSB7XG4gICAgcmV0dXJuIHB1c2hDb250ZXh0KHN0YXRlLCBzdHJlYW0sIFwidmFyaWFibGVOYW1lXCIpO1xuICB9XG4gIGlmICh0eXBlSXNQc2V1ZG8odHlwZSwgc3RyZWFtKSkge1xuICAgIHJldHVybiBwdXNoQ29udGV4dChzdGF0ZSwgc3RyZWFtLCBcInBzZXVkb1wiKTtcbiAgfVxuICByZXR1cm4gc3RhdGUuY29udGV4dC50eXBlO1xufTtcblxuLyoqXG4gKiBWZW5kb3IgcHJlZml4ZXNcbiAqL1xuc3RhdGVzLnZlbmRvclByZWZpeGVzID0gZnVuY3Rpb24gKHR5cGUsIHN0cmVhbSwgc3RhdGUpIHtcbiAgaWYgKHR5cGUgPT0gXCJ3b3JkXCIpIHtcbiAgICBvdmVycmlkZSA9IFwicHJvcGVydHlcIjtcbiAgICByZXR1cm4gcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbSwgXCJibG9ja1wiLCAwKTtcbiAgfVxuICByZXR1cm4gcG9wQ29udGV4dChzdGF0ZSwgc3RyZWFtKTtcbn07XG5cbi8qKlxuICogUHNldWRvXG4gKi9cbnN0YXRlcy5wc2V1ZG8gPSBmdW5jdGlvbiAodHlwZSwgc3RyZWFtLCBzdGF0ZSkge1xuICBpZiAoIXdvcmRJc1Byb3BlcnR5KGZpcnN0V29yZE9mTGluZShzdHJlYW0uc3RyaW5nKSkpIHtcbiAgICBzdHJlYW0ubWF0Y2goL15bYS16LV0rLyk7XG4gICAgb3ZlcnJpZGUgPSBcInZhcmlhYmxlTmFtZS5zcGVjaWFsXCI7XG4gICAgaWYgKGVuZE9mTGluZShzdHJlYW0pKSByZXR1cm4gcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbSwgXCJibG9ja1wiKTtcbiAgICByZXR1cm4gcG9wQ29udGV4dChzdGF0ZSwgc3RyZWFtKTtcbiAgfVxuICByZXR1cm4gcG9wQW5kUGFzcyh0eXBlLCBzdHJlYW0sIHN0YXRlKTtcbn07XG5cbi8qKlxuICogYXRCbG9ja1xuICovXG5zdGF0ZXMuYXRCbG9jayA9IGZ1bmN0aW9uICh0eXBlLCBzdHJlYW0sIHN0YXRlKSB7XG4gIGlmICh0eXBlID09IFwiKFwiKSByZXR1cm4gcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbSwgXCJhdEJsb2NrX3BhcmVuc1wiKTtcbiAgaWYgKHR5cGVJc0Jsb2NrKHR5cGUsIHN0cmVhbSkpIHtcbiAgICByZXR1cm4gcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbSwgXCJibG9ja1wiKTtcbiAgfVxuICBpZiAodHlwZUlzSW50ZXJwb2xhdGlvbih0eXBlLCBzdHJlYW0pKSB7XG4gICAgcmV0dXJuIHB1c2hDb250ZXh0KHN0YXRlLCBzdHJlYW0sIFwiaW50ZXJwb2xhdGlvblwiKTtcbiAgfVxuICBpZiAodHlwZSA9PSBcIndvcmRcIikge1xuICAgIHZhciB3b3JkID0gc3RyZWFtLmN1cnJlbnQoKS50b0xvd2VyQ2FzZSgpO1xuICAgIGlmICgvXihvbmx5fG5vdHxhbmR8b3IpJC8udGVzdCh3b3JkKSkgb3ZlcnJpZGUgPSBcImtleXdvcmRcIjtlbHNlIGlmIChkb2N1bWVudFR5cGVzLmhhc093blByb3BlcnR5KHdvcmQpKSBvdmVycmlkZSA9IFwidGFnXCI7ZWxzZSBpZiAobWVkaWFUeXBlcy5oYXNPd25Qcm9wZXJ0eSh3b3JkKSkgb3ZlcnJpZGUgPSBcImF0dHJpYnV0ZVwiO2Vsc2UgaWYgKG1lZGlhRmVhdHVyZXMuaGFzT3duUHJvcGVydHkod29yZCkpIG92ZXJyaWRlID0gXCJwcm9wZXJ0eVwiO2Vsc2UgaWYgKG5vblN0YW5kYXJkUHJvcGVydHlLZXl3b3Jkcy5oYXNPd25Qcm9wZXJ0eSh3b3JkKSkgb3ZlcnJpZGUgPSBcInN0cmluZy5zcGVjaWFsXCI7ZWxzZSBvdmVycmlkZSA9IHdvcmRBc1ZhbHVlKHN0cmVhbS5jdXJyZW50KCkpO1xuICAgIGlmIChvdmVycmlkZSA9PSBcInRhZ1wiICYmIGVuZE9mTGluZShzdHJlYW0pKSB7XG4gICAgICByZXR1cm4gcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbSwgXCJibG9ja1wiKTtcbiAgICB9XG4gIH1cbiAgaWYgKHR5cGUgPT0gXCJvcGVyYXRvclwiICYmIC9eKG5vdHxhbmR8b3IpJC8udGVzdChzdHJlYW0uY3VycmVudCgpKSkge1xuICAgIG92ZXJyaWRlID0gXCJrZXl3b3JkXCI7XG4gIH1cbiAgcmV0dXJuIHN0YXRlLmNvbnRleHQudHlwZTtcbn07XG5zdGF0ZXMuYXRCbG9ja19wYXJlbnMgPSBmdW5jdGlvbiAodHlwZSwgc3RyZWFtLCBzdGF0ZSkge1xuICBpZiAodHlwZSA9PSBcIntcIiB8fCB0eXBlID09IFwifVwiKSByZXR1cm4gc3RhdGUuY29udGV4dC50eXBlO1xuICBpZiAodHlwZSA9PSBcIilcIikge1xuICAgIGlmIChlbmRPZkxpbmUoc3RyZWFtKSkgcmV0dXJuIHB1c2hDb250ZXh0KHN0YXRlLCBzdHJlYW0sIFwiYmxvY2tcIik7ZWxzZSByZXR1cm4gcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbSwgXCJhdEJsb2NrXCIpO1xuICB9XG4gIGlmICh0eXBlID09IFwid29yZFwiKSB7XG4gICAgdmFyIHdvcmQgPSBzdHJlYW0uY3VycmVudCgpLnRvTG93ZXJDYXNlKCk7XG4gICAgb3ZlcnJpZGUgPSB3b3JkQXNWYWx1ZSh3b3JkKTtcbiAgICBpZiAoL14obWF4fG1pbikvLnRlc3Qod29yZCkpIG92ZXJyaWRlID0gXCJwcm9wZXJ0eVwiO1xuICAgIGlmIChvdmVycmlkZSA9PSBcInRhZ1wiKSB7XG4gICAgICB0YWdWYXJpYWJsZXNSZWdleHAudGVzdCh3b3JkKSA/IG92ZXJyaWRlID0gXCJ2YXJpYWJsZVwiIDogb3ZlcnJpZGUgPSBcImF0b21cIjtcbiAgICB9XG4gICAgcmV0dXJuIHN0YXRlLmNvbnRleHQudHlwZTtcbiAgfVxuICByZXR1cm4gc3RhdGVzLmF0QmxvY2sodHlwZSwgc3RyZWFtLCBzdGF0ZSk7XG59O1xuXG4vKipcbiAqIEtleWZyYW1lc1xuICovXG5zdGF0ZXMua2V5ZnJhbWVzID0gZnVuY3Rpb24gKHR5cGUsIHN0cmVhbSwgc3RhdGUpIHtcbiAgaWYgKHN0cmVhbS5pbmRlbnRhdGlvbigpID09IFwiMFwiICYmICh0eXBlID09IFwifVwiICYmIHN0YXJ0T2ZMaW5lKHN0cmVhbSkgfHwgdHlwZSA9PSBcIl1cIiB8fCB0eXBlID09IFwiaGFzaFwiIHx8IHR5cGUgPT0gXCJxdWFsaWZpZXJcIiB8fCB3b3JkSXNUYWcoc3RyZWFtLmN1cnJlbnQoKSkpKSB7XG4gICAgcmV0dXJuIHBvcEFuZFBhc3ModHlwZSwgc3RyZWFtLCBzdGF0ZSk7XG4gIH1cbiAgaWYgKHR5cGUgPT0gXCJ7XCIpIHJldHVybiBwdXNoQ29udGV4dChzdGF0ZSwgc3RyZWFtLCBcImtleWZyYW1lc1wiKTtcbiAgaWYgKHR5cGUgPT0gXCJ9XCIpIHtcbiAgICBpZiAoc3RhcnRPZkxpbmUoc3RyZWFtKSkgcmV0dXJuIHBvcENvbnRleHQoc3RhdGUsIHN0cmVhbSwgdHJ1ZSk7ZWxzZSByZXR1cm4gcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbSwgXCJrZXlmcmFtZXNcIik7XG4gIH1cbiAgaWYgKHR5cGUgPT0gXCJ1bml0XCIgJiYgL15bMC05XStcXCUkLy50ZXN0KHN0cmVhbS5jdXJyZW50KCkpKSB7XG4gICAgcmV0dXJuIHB1c2hDb250ZXh0KHN0YXRlLCBzdHJlYW0sIFwia2V5ZnJhbWVzXCIpO1xuICB9XG4gIGlmICh0eXBlID09IFwid29yZFwiKSB7XG4gICAgb3ZlcnJpZGUgPSB3b3JkQXNWYWx1ZShzdHJlYW0uY3VycmVudCgpKTtcbiAgICBpZiAob3ZlcnJpZGUgPT0gXCJibG9jay1rZXl3b3JkXCIpIHtcbiAgICAgIG92ZXJyaWRlID0gXCJrZXl3b3JkXCI7XG4gICAgICByZXR1cm4gcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbSwgXCJrZXlmcmFtZXNcIik7XG4gICAgfVxuICB9XG4gIGlmICgvQChmb250LWZhY2V8bWVkaWF8c3VwcG9ydHN8KC1tb3otKT9kb2N1bWVudCkvLnRlc3QodHlwZSkpIHtcbiAgICByZXR1cm4gcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbSwgZW5kT2ZMaW5lKHN0cmVhbSkgPyBcImJsb2NrXCIgOiBcImF0QmxvY2tcIik7XG4gIH1cbiAgaWYgKHR5cGUgPT0gXCJtaXhpblwiKSB7XG4gICAgcmV0dXJuIHB1c2hDb250ZXh0KHN0YXRlLCBzdHJlYW0sIFwiYmxvY2tcIiwgMCk7XG4gIH1cbiAgcmV0dXJuIHN0YXRlLmNvbnRleHQudHlwZTtcbn07XG5cbi8qKlxuICogSW50ZXJwb2xhdGlvblxuICovXG5zdGF0ZXMuaW50ZXJwb2xhdGlvbiA9IGZ1bmN0aW9uICh0eXBlLCBzdHJlYW0sIHN0YXRlKSB7XG4gIGlmICh0eXBlID09IFwie1wiKSBwb3BDb250ZXh0KHN0YXRlLCBzdHJlYW0pICYmIHB1c2hDb250ZXh0KHN0YXRlLCBzdHJlYW0sIFwiYmxvY2tcIik7XG4gIGlmICh0eXBlID09IFwifVwiKSB7XG4gICAgaWYgKHN0cmVhbS5zdHJpbmcubWF0Y2goL15cXHMqKFxcLnwjfDp8XFxbfFxcKnwmfD58fnxcXCt8XFwvKS9pKSB8fCBzdHJlYW0uc3RyaW5nLm1hdGNoKC9eXFxzKlthLXpdL2kpICYmIHdvcmRJc1RhZyhmaXJzdFdvcmRPZkxpbmUoc3RyZWFtKSkpIHtcbiAgICAgIHJldHVybiBwdXNoQ29udGV4dChzdGF0ZSwgc3RyZWFtLCBcImJsb2NrXCIpO1xuICAgIH1cbiAgICBpZiAoIXN0cmVhbS5zdHJpbmcubWF0Y2goL14oXFx7fFxccypcXCYpLykgfHwgc3RyZWFtLm1hdGNoKC9cXHMqW1xcdy1dLywgZmFsc2UpKSB7XG4gICAgICByZXR1cm4gcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbSwgXCJibG9ja1wiLCAwKTtcbiAgICB9XG4gICAgcmV0dXJuIHB1c2hDb250ZXh0KHN0YXRlLCBzdHJlYW0sIFwiYmxvY2tcIik7XG4gIH1cbiAgaWYgKHR5cGUgPT0gXCJ2YXJpYWJsZS1uYW1lXCIpIHtcbiAgICByZXR1cm4gcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbSwgXCJ2YXJpYWJsZU5hbWVcIiwgMCk7XG4gIH1cbiAgaWYgKHR5cGUgPT0gXCJ3b3JkXCIpIHtcbiAgICBvdmVycmlkZSA9IHdvcmRBc1ZhbHVlKHN0cmVhbS5jdXJyZW50KCkpO1xuICAgIGlmIChvdmVycmlkZSA9PSBcInRhZ1wiKSBvdmVycmlkZSA9IFwiYXRvbVwiO1xuICB9XG4gIHJldHVybiBzdGF0ZS5jb250ZXh0LnR5cGU7XG59O1xuXG4vKipcbiAqIEV4dGVuZC9zXG4gKi9cbnN0YXRlcy5leHRlbmQgPSBmdW5jdGlvbiAodHlwZSwgc3RyZWFtLCBzdGF0ZSkge1xuICBpZiAodHlwZSA9PSBcIltcIiB8fCB0eXBlID09IFwiPVwiKSByZXR1cm4gXCJleHRlbmRcIjtcbiAgaWYgKHR5cGUgPT0gXCJdXCIpIHJldHVybiBwb3BDb250ZXh0KHN0YXRlLCBzdHJlYW0pO1xuICBpZiAodHlwZSA9PSBcIndvcmRcIikge1xuICAgIG92ZXJyaWRlID0gd29yZEFzVmFsdWUoc3RyZWFtLmN1cnJlbnQoKSk7XG4gICAgcmV0dXJuIFwiZXh0ZW5kXCI7XG4gIH1cbiAgcmV0dXJuIHBvcENvbnRleHQoc3RhdGUsIHN0cmVhbSk7XG59O1xuXG4vKipcbiAqIFZhcmlhYmxlIG5hbWVcbiAqL1xuc3RhdGVzLnZhcmlhYmxlTmFtZSA9IGZ1bmN0aW9uICh0eXBlLCBzdHJlYW0sIHN0YXRlKSB7XG4gIGlmICh0eXBlID09IFwic3RyaW5nXCIgfHwgdHlwZSA9PSBcIltcIiB8fCB0eXBlID09IFwiXVwiIHx8IHN0cmVhbS5jdXJyZW50KCkubWF0Y2goL14oXFwufFxcJCkvKSkge1xuICAgIGlmIChzdHJlYW0uY3VycmVudCgpLm1hdGNoKC9eXFwuW1xcdy1dKy9pKSkgb3ZlcnJpZGUgPSBcInZhcmlhYmxlXCI7XG4gICAgcmV0dXJuIFwidmFyaWFibGVOYW1lXCI7XG4gIH1cbiAgcmV0dXJuIHBvcEFuZFBhc3ModHlwZSwgc3RyZWFtLCBzdGF0ZSk7XG59O1xuZXhwb3J0IGNvbnN0IHN0eWx1cyA9IHtcbiAgbmFtZTogXCJzdHlsdXNcIixcbiAgc3RhcnRTdGF0ZTogZnVuY3Rpb24gKCkge1xuICAgIHJldHVybiB7XG4gICAgICB0b2tlbml6ZTogbnVsbCxcbiAgICAgIHN0YXRlOiBcImJsb2NrXCIsXG4gICAgICBjb250ZXh0OiBuZXcgQ29udGV4dChcImJsb2NrXCIsIDAsIG51bGwpXG4gICAgfTtcbiAgfSxcbiAgdG9rZW46IGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgaWYgKCFzdGF0ZS50b2tlbml6ZSAmJiBzdHJlYW0uZWF0U3BhY2UoKSkgcmV0dXJuIG51bGw7XG4gICAgc3R5bGUgPSAoc3RhdGUudG9rZW5pemUgfHwgdG9rZW5CYXNlKShzdHJlYW0sIHN0YXRlKTtcbiAgICBpZiAoc3R5bGUgJiYgdHlwZW9mIHN0eWxlID09IFwib2JqZWN0XCIpIHtcbiAgICAgIHR5cGUgPSBzdHlsZVsxXTtcbiAgICAgIHN0eWxlID0gc3R5bGVbMF07XG4gICAgfVxuICAgIG92ZXJyaWRlID0gc3R5bGU7XG4gICAgc3RhdGUuc3RhdGUgPSBzdGF0ZXNbc3RhdGUuc3RhdGVdKHR5cGUsIHN0cmVhbSwgc3RhdGUpO1xuICAgIHJldHVybiBvdmVycmlkZTtcbiAgfSxcbiAgaW5kZW50OiBmdW5jdGlvbiAoc3RhdGUsIHRleHRBZnRlciwgaUN4KSB7XG4gICAgdmFyIGN4ID0gc3RhdGUuY29udGV4dCxcbiAgICAgIGNoID0gdGV4dEFmdGVyICYmIHRleHRBZnRlci5jaGFyQXQoMCksXG4gICAgICBpbmRlbnQgPSBjeC5pbmRlbnQsXG4gICAgICBsaW5lRmlyc3RXb3JkID0gZmlyc3RXb3JkT2ZMaW5lKHRleHRBZnRlciksXG4gICAgICBsaW5lSW5kZW50ID0gaUN4LmxpbmVJbmRlbnQoaUN4LnBvcyksXG4gICAgICBwcmV2TGluZUZpcnN0V29yZCA9IHN0YXRlLmNvbnRleHQucHJldiA/IHN0YXRlLmNvbnRleHQucHJldi5saW5lLmZpcnN0V29yZCA6IFwiXCIsXG4gICAgICBwcmV2TGluZUluZGVudCA9IHN0YXRlLmNvbnRleHQucHJldiA/IHN0YXRlLmNvbnRleHQucHJldi5saW5lLmluZGVudCA6IGxpbmVJbmRlbnQ7XG4gICAgaWYgKGN4LnByZXYgJiYgKGNoID09IFwifVwiICYmIChjeC50eXBlID09IFwiYmxvY2tcIiB8fCBjeC50eXBlID09IFwiYXRCbG9ja1wiIHx8IGN4LnR5cGUgPT0gXCJrZXlmcmFtZXNcIikgfHwgY2ggPT0gXCIpXCIgJiYgKGN4LnR5cGUgPT0gXCJwYXJlbnNcIiB8fCBjeC50eXBlID09IFwiYXRCbG9ja19wYXJlbnNcIikgfHwgY2ggPT0gXCJ7XCIgJiYgY3gudHlwZSA9PSBcImF0XCIpKSB7XG4gICAgICBpbmRlbnQgPSBjeC5pbmRlbnQgLSBpQ3gudW5pdDtcbiAgICB9IGVsc2UgaWYgKCEvKFxcfSkvLnRlc3QoY2gpKSB7XG4gICAgICBpZiAoL0B8XFwkfFxcZC8udGVzdChjaCkgfHwgL15cXHsvLnRlc3QodGV4dEFmdGVyKSB8fCAvXlxccypcXC8oXFwvfFxcKikvLnRlc3QodGV4dEFmdGVyKSB8fCAvXlxccypcXC9cXCovLnRlc3QocHJldkxpbmVGaXJzdFdvcmQpIHx8IC9eXFxzKltcXHctXFwuXFxbXFxdXFwnXFxcIl0rXFxzKihcXD98OnxcXCspPz0vaS50ZXN0KHRleHRBZnRlcikgfHwgL14oXFwrfC0pP1thLXpdW1xcdy1dKlxcKC9pLnRlc3QodGV4dEFmdGVyKSB8fCAvXnJldHVybi8udGVzdCh0ZXh0QWZ0ZXIpIHx8IHdvcmRJc0Jsb2NrKGxpbmVGaXJzdFdvcmQpKSB7XG4gICAgICAgIGluZGVudCA9IGxpbmVJbmRlbnQ7XG4gICAgICB9IGVsc2UgaWYgKC8oXFwufCN8OnxcXFt8XFwqfCZ8Pnx+fFxcK3xcXC8pLy50ZXN0KGNoKSB8fCB3b3JkSXNUYWcobGluZUZpcnN0V29yZCkpIHtcbiAgICAgICAgaWYgKC9cXCxcXHMqJC8udGVzdChwcmV2TGluZUZpcnN0V29yZCkpIHtcbiAgICAgICAgICBpbmRlbnQgPSBwcmV2TGluZUluZGVudDtcbiAgICAgICAgfSBlbHNlIGlmICghc3RhdGUuc29sKCkgJiYgKC8oXFwufCN8OnxcXFt8XFwqfCZ8Pnx+fFxcK3xcXC8pLy50ZXN0KHByZXZMaW5lRmlyc3RXb3JkKSB8fCB3b3JkSXNUYWcocHJldkxpbmVGaXJzdFdvcmQpKSkge1xuICAgICAgICAgIGluZGVudCA9IGxpbmVJbmRlbnQgPD0gcHJldkxpbmVJbmRlbnQgPyBwcmV2TGluZUluZGVudCA6IHByZXZMaW5lSW5kZW50ICsgaUN4LnVuaXQ7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgaW5kZW50ID0gbGluZUluZGVudDtcbiAgICAgICAgfVxuICAgICAgfSBlbHNlIGlmICghLyxcXHMqJC8udGVzdCh0ZXh0QWZ0ZXIpICYmICh3b3JkSXNWZW5kb3JQcmVmaXgobGluZUZpcnN0V29yZCkgfHwgd29yZElzUHJvcGVydHkobGluZUZpcnN0V29yZCkpKSB7XG4gICAgICAgIGlmICh3b3JkSXNCbG9jayhwcmV2TGluZUZpcnN0V29yZCkpIHtcbiAgICAgICAgICBpbmRlbnQgPSBsaW5lSW5kZW50IDw9IHByZXZMaW5lSW5kZW50ID8gcHJldkxpbmVJbmRlbnQgOiBwcmV2TGluZUluZGVudCArIGlDeC51bml0O1xuICAgICAgICB9IGVsc2UgaWYgKC9eXFx7Ly50ZXN0KHByZXZMaW5lRmlyc3RXb3JkKSkge1xuICAgICAgICAgIGluZGVudCA9IGxpbmVJbmRlbnQgPD0gcHJldkxpbmVJbmRlbnQgPyBsaW5lSW5kZW50IDogcHJldkxpbmVJbmRlbnQgKyBpQ3gudW5pdDtcbiAgICAgICAgfSBlbHNlIGlmICh3b3JkSXNWZW5kb3JQcmVmaXgocHJldkxpbmVGaXJzdFdvcmQpIHx8IHdvcmRJc1Byb3BlcnR5KHByZXZMaW5lRmlyc3RXb3JkKSkge1xuICAgICAgICAgIGluZGVudCA9IGxpbmVJbmRlbnQgPj0gcHJldkxpbmVJbmRlbnQgPyBwcmV2TGluZUluZGVudCA6IGxpbmVJbmRlbnQ7XG4gICAgICAgIH0gZWxzZSBpZiAoL14oXFwufCN8OnxcXFt8XFwqfCZ8QHxcXCt8XFwtfD58fnxcXC8pLy50ZXN0KHByZXZMaW5lRmlyc3RXb3JkKSB8fCAvPVxccyokLy50ZXN0KHByZXZMaW5lRmlyc3RXb3JkKSB8fCB3b3JkSXNUYWcocHJldkxpbmVGaXJzdFdvcmQpIHx8IC9eXFwkW1xcdy1cXC5cXFtcXF1cXCdcXFwiXS8udGVzdChwcmV2TGluZUZpcnN0V29yZCkpIHtcbiAgICAgICAgICBpbmRlbnQgPSBwcmV2TGluZUluZGVudCArIGlDeC51bml0O1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgIGluZGVudCA9IGxpbmVJbmRlbnQ7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9XG4gICAgcmV0dXJuIGluZGVudDtcbiAgfSxcbiAgbGFuZ3VhZ2VEYXRhOiB7XG4gICAgaW5kZW50T25JbnB1dDogL15cXHMqXFx9JC8sXG4gICAgY29tbWVudFRva2Vuczoge1xuICAgICAgbGluZTogXCIvL1wiLFxuICAgICAgYmxvY2s6IHtcbiAgICAgICAgb3BlbjogXCIvKlwiLFxuICAgICAgICBjbG9zZTogXCIqL1wiXG4gICAgICB9XG4gICAgfSxcbiAgICBhdXRvY29tcGxldGU6IGhpbnRXb3Jkc1xuICB9XG59OyJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==