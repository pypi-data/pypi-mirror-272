"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[8486],{

/***/ 8486:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "xQuery": () => (/* binding */ xQuery)
/* harmony export */ });
// The keywords object is set to the result of this self executing
// function. Each keyword is a property of the keywords object whose
// value is {type: atype, style: astyle}
var keywords = function () {
  // convenience functions used to build keywords object
  function kw(type) {
    return {
      type: type,
      style: "keyword"
    };
  }
  var operator = kw("operator"),
    atom = {
      type: "atom",
      style: "atom"
    },
    punctuation = {
      type: "punctuation",
      style: null
    },
    qualifier = {
      type: "axis_specifier",
      style: "qualifier"
    };

  // kwObj is what is return from this function at the end
  var kwObj = {
    ',': punctuation
  };

  // a list of 'basic' keywords. For each add a property to kwObj with the value of
  // {type: basic[i], style: "keyword"} e.g. 'after' --> {type: "after", style: "keyword"}
  var basic = ['after', 'all', 'allowing', 'ancestor', 'ancestor-or-self', 'any', 'array', 'as', 'ascending', 'at', 'attribute', 'base-uri', 'before', 'boundary-space', 'by', 'case', 'cast', 'castable', 'catch', 'child', 'collation', 'comment', 'construction', 'contains', 'content', 'context', 'copy', 'copy-namespaces', 'count', 'decimal-format', 'declare', 'default', 'delete', 'descendant', 'descendant-or-self', 'descending', 'diacritics', 'different', 'distance', 'document', 'document-node', 'element', 'else', 'empty', 'empty-sequence', 'encoding', 'end', 'entire', 'every', 'exactly', 'except', 'external', 'first', 'following', 'following-sibling', 'for', 'from', 'ftand', 'ftnot', 'ft-option', 'ftor', 'function', 'fuzzy', 'greatest', 'group', 'if', 'import', 'in', 'inherit', 'insensitive', 'insert', 'instance', 'intersect', 'into', 'invoke', 'is', 'item', 'language', 'last', 'lax', 'least', 'let', 'levels', 'lowercase', 'map', 'modify', 'module', 'most', 'namespace', 'next', 'no', 'node', 'nodes', 'no-inherit', 'no-preserve', 'not', 'occurs', 'of', 'only', 'option', 'order', 'ordered', 'ordering', 'paragraph', 'paragraphs', 'parent', 'phrase', 'preceding', 'preceding-sibling', 'preserve', 'previous', 'processing-instruction', 'relationship', 'rename', 'replace', 'return', 'revalidation', 'same', 'satisfies', 'schema', 'schema-attribute', 'schema-element', 'score', 'self', 'sensitive', 'sentence', 'sentences', 'sequence', 'skip', 'sliding', 'some', 'stable', 'start', 'stemming', 'stop', 'strict', 'strip', 'switch', 'text', 'then', 'thesaurus', 'times', 'to', 'transform', 'treat', 'try', 'tumbling', 'type', 'typeswitch', 'union', 'unordered', 'update', 'updating', 'uppercase', 'using', 'validate', 'value', 'variable', 'version', 'weight', 'when', 'where', 'wildcards', 'window', 'with', 'without', 'word', 'words', 'xquery'];
  for (var i = 0, l = basic.length; i < l; i++) {
    kwObj[basic[i]] = kw(basic[i]);
  }
  ;

  // a list of types. For each add a property to kwObj with the value of
  // {type: "atom", style: "atom"}
  var types = ['xs:anyAtomicType', 'xs:anySimpleType', 'xs:anyType', 'xs:anyURI', 'xs:base64Binary', 'xs:boolean', 'xs:byte', 'xs:date', 'xs:dateTime', 'xs:dateTimeStamp', 'xs:dayTimeDuration', 'xs:decimal', 'xs:double', 'xs:duration', 'xs:ENTITIES', 'xs:ENTITY', 'xs:float', 'xs:gDay', 'xs:gMonth', 'xs:gMonthDay', 'xs:gYear', 'xs:gYearMonth', 'xs:hexBinary', 'xs:ID', 'xs:IDREF', 'xs:IDREFS', 'xs:int', 'xs:integer', 'xs:item', 'xs:java', 'xs:language', 'xs:long', 'xs:Name', 'xs:NCName', 'xs:negativeInteger', 'xs:NMTOKEN', 'xs:NMTOKENS', 'xs:nonNegativeInteger', 'xs:nonPositiveInteger', 'xs:normalizedString', 'xs:NOTATION', 'xs:numeric', 'xs:positiveInteger', 'xs:precisionDecimal', 'xs:QName', 'xs:short', 'xs:string', 'xs:time', 'xs:token', 'xs:unsignedByte', 'xs:unsignedInt', 'xs:unsignedLong', 'xs:unsignedShort', 'xs:untyped', 'xs:untypedAtomic', 'xs:yearMonthDuration'];
  for (var i = 0, l = types.length; i < l; i++) {
    kwObj[types[i]] = atom;
  }
  ;

  // each operator will add a property to kwObj with value of {type: "operator", style: "keyword"}
  var operators = ['eq', 'ne', 'lt', 'le', 'gt', 'ge', ':=', '=', '>', '>=', '<', '<=', '.', '|', '?', 'and', 'or', 'div', 'idiv', 'mod', '*', '/', '+', '-'];
  for (var i = 0, l = operators.length; i < l; i++) {
    kwObj[operators[i]] = operator;
  }
  ;

  // each axis_specifiers will add a property to kwObj with value of {type: "axis_specifier", style: "qualifier"}
  var axis_specifiers = ["self::", "attribute::", "child::", "descendant::", "descendant-or-self::", "parent::", "ancestor::", "ancestor-or-self::", "following::", "preceding::", "following-sibling::", "preceding-sibling::"];
  for (var i = 0, l = axis_specifiers.length; i < l; i++) {
    kwObj[axis_specifiers[i]] = qualifier;
  }
  ;
  return kwObj;
}();
function chain(stream, state, f) {
  state.tokenize = f;
  return f(stream, state);
}

// the primary mode tokenizer
function tokenBase(stream, state) {
  var ch = stream.next(),
    mightBeFunction = false,
    isEQName = isEQNameAhead(stream);

  // an XML tag (if not in some sub, chained tokenizer)
  if (ch == "<") {
    if (stream.match("!--", true)) return chain(stream, state, tokenXMLComment);
    if (stream.match("![CDATA", false)) {
      state.tokenize = tokenCDATA;
      return "tag";
    }
    if (stream.match("?", false)) {
      return chain(stream, state, tokenPreProcessing);
    }
    var isclose = stream.eat("/");
    stream.eatSpace();
    var tagName = "",
      c;
    while (c = stream.eat(/[^\s\u00a0=<>\"\'\/?]/)) tagName += c;
    return chain(stream, state, tokenTag(tagName, isclose));
  }
  // start code block
  else if (ch == "{") {
    pushStateStack(state, {
      type: "codeblock"
    });
    return null;
  }
  // end code block
  else if (ch == "}") {
    popStateStack(state);
    return null;
  }
  // if we're in an XML block
  else if (isInXmlBlock(state)) {
    if (ch == ">") return "tag";else if (ch == "/" && stream.eat(">")) {
      popStateStack(state);
      return "tag";
    } else return "variable";
  }
  // if a number
  else if (/\d/.test(ch)) {
    stream.match(/^\d*(?:\.\d*)?(?:E[+\-]?\d+)?/);
    return "atom";
  }
  // comment start
  else if (ch === "(" && stream.eat(":")) {
    pushStateStack(state, {
      type: "comment"
    });
    return chain(stream, state, tokenComment);
  }
  // quoted string
  else if (!isEQName && (ch === '"' || ch === "'")) return chain(stream, state, tokenString(ch));
  // variable
  else if (ch === "$") {
    return chain(stream, state, tokenVariable);
  }
  // assignment
  else if (ch === ":" && stream.eat("=")) {
    return "keyword";
  }
  // open paren
  else if (ch === "(") {
    pushStateStack(state, {
      type: "paren"
    });
    return null;
  }
  // close paren
  else if (ch === ")") {
    popStateStack(state);
    return null;
  }
  // open paren
  else if (ch === "[") {
    pushStateStack(state, {
      type: "bracket"
    });
    return null;
  }
  // close paren
  else if (ch === "]") {
    popStateStack(state);
    return null;
  } else {
    var known = keywords.propertyIsEnumerable(ch) && keywords[ch];

    // if there's a EQName ahead, consume the rest of the string portion, it's likely a function
    if (isEQName && ch === '\"') while (stream.next() !== '"') {}
    if (isEQName && ch === '\'') while (stream.next() !== '\'') {}

    // gobble up a word if the character is not known
    if (!known) stream.eatWhile(/[\w\$_-]/);

    // gobble a colon in the case that is a lib func type call fn:doc
    var foundColon = stream.eat(":");

    // if there's not a second colon, gobble another word. Otherwise, it's probably an axis specifier
    // which should get matched as a keyword
    if (!stream.eat(":") && foundColon) {
      stream.eatWhile(/[\w\$_-]/);
    }
    // if the next non whitespace character is an open paren, this is probably a function (if not a keyword of other sort)
    if (stream.match(/^[ \t]*\(/, false)) {
      mightBeFunction = true;
    }
    // is the word a keyword?
    var word = stream.current();
    known = keywords.propertyIsEnumerable(word) && keywords[word];

    // if we think it's a function call but not yet known,
    // set style to variable for now for lack of something better
    if (mightBeFunction && !known) known = {
      type: "function_call",
      style: "def"
    };

    // if the previous word was element, attribute, axis specifier, this word should be the name of that
    if (isInXmlConstructor(state)) {
      popStateStack(state);
      return "variable";
    }
    // as previously checked, if the word is element,attribute, axis specifier, call it an "xmlconstructor" and
    // push the stack so we know to look for it on the next word
    if (word == "element" || word == "attribute" || known.type == "axis_specifier") pushStateStack(state, {
      type: "xmlconstructor"
    });

    // if the word is known, return the details of that else just call this a generic 'word'
    return known ? known.style : "variable";
  }
}

// handle comments, including nested
function tokenComment(stream, state) {
  var maybeEnd = false,
    maybeNested = false,
    nestedCount = 0,
    ch;
  while (ch = stream.next()) {
    if (ch == ")" && maybeEnd) {
      if (nestedCount > 0) nestedCount--;else {
        popStateStack(state);
        break;
      }
    } else if (ch == ":" && maybeNested) {
      nestedCount++;
    }
    maybeEnd = ch == ":";
    maybeNested = ch == "(";
  }
  return "comment";
}

// tokenizer for string literals
// optionally pass a tokenizer function to set state.tokenize back to when finished
function tokenString(quote, f) {
  return function (stream, state) {
    var ch;
    if (isInString(state) && stream.current() == quote) {
      popStateStack(state);
      if (f) state.tokenize = f;
      return "string";
    }
    pushStateStack(state, {
      type: "string",
      name: quote,
      tokenize: tokenString(quote, f)
    });

    // if we're in a string and in an XML block, allow an embedded code block
    if (stream.match("{", false) && isInXmlAttributeBlock(state)) {
      state.tokenize = tokenBase;
      return "string";
    }
    while (ch = stream.next()) {
      if (ch == quote) {
        popStateStack(state);
        if (f) state.tokenize = f;
        break;
      } else {
        // if we're in a string and in an XML block, allow an embedded code block in an attribute
        if (stream.match("{", false) && isInXmlAttributeBlock(state)) {
          state.tokenize = tokenBase;
          return "string";
        }
      }
    }
    return "string";
  };
}

// tokenizer for variables
function tokenVariable(stream, state) {
  var isVariableChar = /[\w\$_-]/;

  // a variable may start with a quoted EQName so if the next character is quote, consume to the next quote
  if (stream.eat("\"")) {
    while (stream.next() !== '\"') {}
    ;
    stream.eat(":");
  } else {
    stream.eatWhile(isVariableChar);
    if (!stream.match(":=", false)) stream.eat(":");
  }
  stream.eatWhile(isVariableChar);
  state.tokenize = tokenBase;
  return "variable";
}

// tokenizer for XML tags
function tokenTag(name, isclose) {
  return function (stream, state) {
    stream.eatSpace();
    if (isclose && stream.eat(">")) {
      popStateStack(state);
      state.tokenize = tokenBase;
      return "tag";
    }
    // self closing tag without attributes?
    if (!stream.eat("/")) pushStateStack(state, {
      type: "tag",
      name: name,
      tokenize: tokenBase
    });
    if (!stream.eat(">")) {
      state.tokenize = tokenAttribute;
      return "tag";
    } else {
      state.tokenize = tokenBase;
    }
    return "tag";
  };
}

// tokenizer for XML attributes
function tokenAttribute(stream, state) {
  var ch = stream.next();
  if (ch == "/" && stream.eat(">")) {
    if (isInXmlAttributeBlock(state)) popStateStack(state);
    if (isInXmlBlock(state)) popStateStack(state);
    return "tag";
  }
  if (ch == ">") {
    if (isInXmlAttributeBlock(state)) popStateStack(state);
    return "tag";
  }
  if (ch == "=") return null;
  // quoted string
  if (ch == '"' || ch == "'") return chain(stream, state, tokenString(ch, tokenAttribute));
  if (!isInXmlAttributeBlock(state)) pushStateStack(state, {
    type: "attribute",
    tokenize: tokenAttribute
  });
  stream.eat(/[a-zA-Z_:]/);
  stream.eatWhile(/[-a-zA-Z0-9_:.]/);
  stream.eatSpace();

  // the case where the attribute has not value and the tag was closed
  if (stream.match(">", false) || stream.match("/", false)) {
    popStateStack(state);
    state.tokenize = tokenBase;
  }
  return "attribute";
}

// handle comments, including nested
function tokenXMLComment(stream, state) {
  var ch;
  while (ch = stream.next()) {
    if (ch == "-" && stream.match("->", true)) {
      state.tokenize = tokenBase;
      return "comment";
    }
  }
}

// handle CDATA
function tokenCDATA(stream, state) {
  var ch;
  while (ch = stream.next()) {
    if (ch == "]" && stream.match("]", true)) {
      state.tokenize = tokenBase;
      return "comment";
    }
  }
}

// handle preprocessing instructions
function tokenPreProcessing(stream, state) {
  var ch;
  while (ch = stream.next()) {
    if (ch == "?" && stream.match(">", true)) {
      state.tokenize = tokenBase;
      return "processingInstruction";
    }
  }
}

// functions to test the current context of the state
function isInXmlBlock(state) {
  return isIn(state, "tag");
}
function isInXmlAttributeBlock(state) {
  return isIn(state, "attribute");
}
function isInXmlConstructor(state) {
  return isIn(state, "xmlconstructor");
}
function isInString(state) {
  return isIn(state, "string");
}
function isEQNameAhead(stream) {
  // assume we've already eaten a quote (")
  if (stream.current() === '"') return stream.match(/^[^\"]+\"\:/, false);else if (stream.current() === '\'') return stream.match(/^[^\"]+\'\:/, false);else return false;
}
function isIn(state, type) {
  return state.stack.length && state.stack[state.stack.length - 1].type == type;
}
function pushStateStack(state, newState) {
  state.stack.push(newState);
}
function popStateStack(state) {
  state.stack.pop();
  var reinstateTokenize = state.stack.length && state.stack[state.stack.length - 1].tokenize;
  state.tokenize = reinstateTokenize || tokenBase;
}

// the interface for the mode API
const xQuery = {
  name: "xquery",
  startState: function () {
    return {
      tokenize: tokenBase,
      cc: [],
      stack: []
    };
  },
  token: function (stream, state) {
    if (stream.eatSpace()) return null;
    var style = state.tokenize(stream, state);
    return style;
  },
  languageData: {
    commentTokens: {
      block: {
        open: "(:",
        close: ":)"
      }
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiODQ4Ni5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL0Bjb2RlbWlycm9yL2xlZ2FjeS1tb2Rlcy9tb2RlL3hxdWVyeS5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyIvLyBUaGUga2V5d29yZHMgb2JqZWN0IGlzIHNldCB0byB0aGUgcmVzdWx0IG9mIHRoaXMgc2VsZiBleGVjdXRpbmdcbi8vIGZ1bmN0aW9uLiBFYWNoIGtleXdvcmQgaXMgYSBwcm9wZXJ0eSBvZiB0aGUga2V5d29yZHMgb2JqZWN0IHdob3NlXG4vLyB2YWx1ZSBpcyB7dHlwZTogYXR5cGUsIHN0eWxlOiBhc3R5bGV9XG52YXIga2V5d29yZHMgPSBmdW5jdGlvbiAoKSB7XG4gIC8vIGNvbnZlbmllbmNlIGZ1bmN0aW9ucyB1c2VkIHRvIGJ1aWxkIGtleXdvcmRzIG9iamVjdFxuICBmdW5jdGlvbiBrdyh0eXBlKSB7XG4gICAgcmV0dXJuIHtcbiAgICAgIHR5cGU6IHR5cGUsXG4gICAgICBzdHlsZTogXCJrZXl3b3JkXCJcbiAgICB9O1xuICB9XG4gIHZhciBvcGVyYXRvciA9IGt3KFwib3BlcmF0b3JcIiksXG4gICAgYXRvbSA9IHtcbiAgICAgIHR5cGU6IFwiYXRvbVwiLFxuICAgICAgc3R5bGU6IFwiYXRvbVwiXG4gICAgfSxcbiAgICBwdW5jdHVhdGlvbiA9IHtcbiAgICAgIHR5cGU6IFwicHVuY3R1YXRpb25cIixcbiAgICAgIHN0eWxlOiBudWxsXG4gICAgfSxcbiAgICBxdWFsaWZpZXIgPSB7XG4gICAgICB0eXBlOiBcImF4aXNfc3BlY2lmaWVyXCIsXG4gICAgICBzdHlsZTogXCJxdWFsaWZpZXJcIlxuICAgIH07XG5cbiAgLy8ga3dPYmogaXMgd2hhdCBpcyByZXR1cm4gZnJvbSB0aGlzIGZ1bmN0aW9uIGF0IHRoZSBlbmRcbiAgdmFyIGt3T2JqID0ge1xuICAgICcsJzogcHVuY3R1YXRpb25cbiAgfTtcblxuICAvLyBhIGxpc3Qgb2YgJ2Jhc2ljJyBrZXl3b3Jkcy4gRm9yIGVhY2ggYWRkIGEgcHJvcGVydHkgdG8ga3dPYmogd2l0aCB0aGUgdmFsdWUgb2ZcbiAgLy8ge3R5cGU6IGJhc2ljW2ldLCBzdHlsZTogXCJrZXl3b3JkXCJ9IGUuZy4gJ2FmdGVyJyAtLT4ge3R5cGU6IFwiYWZ0ZXJcIiwgc3R5bGU6IFwia2V5d29yZFwifVxuICB2YXIgYmFzaWMgPSBbJ2FmdGVyJywgJ2FsbCcsICdhbGxvd2luZycsICdhbmNlc3RvcicsICdhbmNlc3Rvci1vci1zZWxmJywgJ2FueScsICdhcnJheScsICdhcycsICdhc2NlbmRpbmcnLCAnYXQnLCAnYXR0cmlidXRlJywgJ2Jhc2UtdXJpJywgJ2JlZm9yZScsICdib3VuZGFyeS1zcGFjZScsICdieScsICdjYXNlJywgJ2Nhc3QnLCAnY2FzdGFibGUnLCAnY2F0Y2gnLCAnY2hpbGQnLCAnY29sbGF0aW9uJywgJ2NvbW1lbnQnLCAnY29uc3RydWN0aW9uJywgJ2NvbnRhaW5zJywgJ2NvbnRlbnQnLCAnY29udGV4dCcsICdjb3B5JywgJ2NvcHktbmFtZXNwYWNlcycsICdjb3VudCcsICdkZWNpbWFsLWZvcm1hdCcsICdkZWNsYXJlJywgJ2RlZmF1bHQnLCAnZGVsZXRlJywgJ2Rlc2NlbmRhbnQnLCAnZGVzY2VuZGFudC1vci1zZWxmJywgJ2Rlc2NlbmRpbmcnLCAnZGlhY3JpdGljcycsICdkaWZmZXJlbnQnLCAnZGlzdGFuY2UnLCAnZG9jdW1lbnQnLCAnZG9jdW1lbnQtbm9kZScsICdlbGVtZW50JywgJ2Vsc2UnLCAnZW1wdHknLCAnZW1wdHktc2VxdWVuY2UnLCAnZW5jb2RpbmcnLCAnZW5kJywgJ2VudGlyZScsICdldmVyeScsICdleGFjdGx5JywgJ2V4Y2VwdCcsICdleHRlcm5hbCcsICdmaXJzdCcsICdmb2xsb3dpbmcnLCAnZm9sbG93aW5nLXNpYmxpbmcnLCAnZm9yJywgJ2Zyb20nLCAnZnRhbmQnLCAnZnRub3QnLCAnZnQtb3B0aW9uJywgJ2Z0b3InLCAnZnVuY3Rpb24nLCAnZnV6enknLCAnZ3JlYXRlc3QnLCAnZ3JvdXAnLCAnaWYnLCAnaW1wb3J0JywgJ2luJywgJ2luaGVyaXQnLCAnaW5zZW5zaXRpdmUnLCAnaW5zZXJ0JywgJ2luc3RhbmNlJywgJ2ludGVyc2VjdCcsICdpbnRvJywgJ2ludm9rZScsICdpcycsICdpdGVtJywgJ2xhbmd1YWdlJywgJ2xhc3QnLCAnbGF4JywgJ2xlYXN0JywgJ2xldCcsICdsZXZlbHMnLCAnbG93ZXJjYXNlJywgJ21hcCcsICdtb2RpZnknLCAnbW9kdWxlJywgJ21vc3QnLCAnbmFtZXNwYWNlJywgJ25leHQnLCAnbm8nLCAnbm9kZScsICdub2RlcycsICduby1pbmhlcml0JywgJ25vLXByZXNlcnZlJywgJ25vdCcsICdvY2N1cnMnLCAnb2YnLCAnb25seScsICdvcHRpb24nLCAnb3JkZXInLCAnb3JkZXJlZCcsICdvcmRlcmluZycsICdwYXJhZ3JhcGgnLCAncGFyYWdyYXBocycsICdwYXJlbnQnLCAncGhyYXNlJywgJ3ByZWNlZGluZycsICdwcmVjZWRpbmctc2libGluZycsICdwcmVzZXJ2ZScsICdwcmV2aW91cycsICdwcm9jZXNzaW5nLWluc3RydWN0aW9uJywgJ3JlbGF0aW9uc2hpcCcsICdyZW5hbWUnLCAncmVwbGFjZScsICdyZXR1cm4nLCAncmV2YWxpZGF0aW9uJywgJ3NhbWUnLCAnc2F0aXNmaWVzJywgJ3NjaGVtYScsICdzY2hlbWEtYXR0cmlidXRlJywgJ3NjaGVtYS1lbGVtZW50JywgJ3Njb3JlJywgJ3NlbGYnLCAnc2Vuc2l0aXZlJywgJ3NlbnRlbmNlJywgJ3NlbnRlbmNlcycsICdzZXF1ZW5jZScsICdza2lwJywgJ3NsaWRpbmcnLCAnc29tZScsICdzdGFibGUnLCAnc3RhcnQnLCAnc3RlbW1pbmcnLCAnc3RvcCcsICdzdHJpY3QnLCAnc3RyaXAnLCAnc3dpdGNoJywgJ3RleHQnLCAndGhlbicsICd0aGVzYXVydXMnLCAndGltZXMnLCAndG8nLCAndHJhbnNmb3JtJywgJ3RyZWF0JywgJ3RyeScsICd0dW1ibGluZycsICd0eXBlJywgJ3R5cGVzd2l0Y2gnLCAndW5pb24nLCAndW5vcmRlcmVkJywgJ3VwZGF0ZScsICd1cGRhdGluZycsICd1cHBlcmNhc2UnLCAndXNpbmcnLCAndmFsaWRhdGUnLCAndmFsdWUnLCAndmFyaWFibGUnLCAndmVyc2lvbicsICd3ZWlnaHQnLCAnd2hlbicsICd3aGVyZScsICd3aWxkY2FyZHMnLCAnd2luZG93JywgJ3dpdGgnLCAnd2l0aG91dCcsICd3b3JkJywgJ3dvcmRzJywgJ3hxdWVyeSddO1xuICBmb3IgKHZhciBpID0gMCwgbCA9IGJhc2ljLmxlbmd0aDsgaSA8IGw7IGkrKykge1xuICAgIGt3T2JqW2Jhc2ljW2ldXSA9IGt3KGJhc2ljW2ldKTtcbiAgfVxuICA7XG5cbiAgLy8gYSBsaXN0IG9mIHR5cGVzLiBGb3IgZWFjaCBhZGQgYSBwcm9wZXJ0eSB0byBrd09iaiB3aXRoIHRoZSB2YWx1ZSBvZlxuICAvLyB7dHlwZTogXCJhdG9tXCIsIHN0eWxlOiBcImF0b21cIn1cbiAgdmFyIHR5cGVzID0gWyd4czphbnlBdG9taWNUeXBlJywgJ3hzOmFueVNpbXBsZVR5cGUnLCAneHM6YW55VHlwZScsICd4czphbnlVUkknLCAneHM6YmFzZTY0QmluYXJ5JywgJ3hzOmJvb2xlYW4nLCAneHM6Ynl0ZScsICd4czpkYXRlJywgJ3hzOmRhdGVUaW1lJywgJ3hzOmRhdGVUaW1lU3RhbXAnLCAneHM6ZGF5VGltZUR1cmF0aW9uJywgJ3hzOmRlY2ltYWwnLCAneHM6ZG91YmxlJywgJ3hzOmR1cmF0aW9uJywgJ3hzOkVOVElUSUVTJywgJ3hzOkVOVElUWScsICd4czpmbG9hdCcsICd4czpnRGF5JywgJ3hzOmdNb250aCcsICd4czpnTW9udGhEYXknLCAneHM6Z1llYXInLCAneHM6Z1llYXJNb250aCcsICd4czpoZXhCaW5hcnknLCAneHM6SUQnLCAneHM6SURSRUYnLCAneHM6SURSRUZTJywgJ3hzOmludCcsICd4czppbnRlZ2VyJywgJ3hzOml0ZW0nLCAneHM6amF2YScsICd4czpsYW5ndWFnZScsICd4czpsb25nJywgJ3hzOk5hbWUnLCAneHM6TkNOYW1lJywgJ3hzOm5lZ2F0aXZlSW50ZWdlcicsICd4czpOTVRPS0VOJywgJ3hzOk5NVE9LRU5TJywgJ3hzOm5vbk5lZ2F0aXZlSW50ZWdlcicsICd4czpub25Qb3NpdGl2ZUludGVnZXInLCAneHM6bm9ybWFsaXplZFN0cmluZycsICd4czpOT1RBVElPTicsICd4czpudW1lcmljJywgJ3hzOnBvc2l0aXZlSW50ZWdlcicsICd4czpwcmVjaXNpb25EZWNpbWFsJywgJ3hzOlFOYW1lJywgJ3hzOnNob3J0JywgJ3hzOnN0cmluZycsICd4czp0aW1lJywgJ3hzOnRva2VuJywgJ3hzOnVuc2lnbmVkQnl0ZScsICd4czp1bnNpZ25lZEludCcsICd4czp1bnNpZ25lZExvbmcnLCAneHM6dW5zaWduZWRTaG9ydCcsICd4czp1bnR5cGVkJywgJ3hzOnVudHlwZWRBdG9taWMnLCAneHM6eWVhck1vbnRoRHVyYXRpb24nXTtcbiAgZm9yICh2YXIgaSA9IDAsIGwgPSB0eXBlcy5sZW5ndGg7IGkgPCBsOyBpKyspIHtcbiAgICBrd09ialt0eXBlc1tpXV0gPSBhdG9tO1xuICB9XG4gIDtcblxuICAvLyBlYWNoIG9wZXJhdG9yIHdpbGwgYWRkIGEgcHJvcGVydHkgdG8ga3dPYmogd2l0aCB2YWx1ZSBvZiB7dHlwZTogXCJvcGVyYXRvclwiLCBzdHlsZTogXCJrZXl3b3JkXCJ9XG4gIHZhciBvcGVyYXRvcnMgPSBbJ2VxJywgJ25lJywgJ2x0JywgJ2xlJywgJ2d0JywgJ2dlJywgJzo9JywgJz0nLCAnPicsICc+PScsICc8JywgJzw9JywgJy4nLCAnfCcsICc/JywgJ2FuZCcsICdvcicsICdkaXYnLCAnaWRpdicsICdtb2QnLCAnKicsICcvJywgJysnLCAnLSddO1xuICBmb3IgKHZhciBpID0gMCwgbCA9IG9wZXJhdG9ycy5sZW5ndGg7IGkgPCBsOyBpKyspIHtcbiAgICBrd09ialtvcGVyYXRvcnNbaV1dID0gb3BlcmF0b3I7XG4gIH1cbiAgO1xuXG4gIC8vIGVhY2ggYXhpc19zcGVjaWZpZXJzIHdpbGwgYWRkIGEgcHJvcGVydHkgdG8ga3dPYmogd2l0aCB2YWx1ZSBvZiB7dHlwZTogXCJheGlzX3NwZWNpZmllclwiLCBzdHlsZTogXCJxdWFsaWZpZXJcIn1cbiAgdmFyIGF4aXNfc3BlY2lmaWVycyA9IFtcInNlbGY6OlwiLCBcImF0dHJpYnV0ZTo6XCIsIFwiY2hpbGQ6OlwiLCBcImRlc2NlbmRhbnQ6OlwiLCBcImRlc2NlbmRhbnQtb3Itc2VsZjo6XCIsIFwicGFyZW50OjpcIiwgXCJhbmNlc3Rvcjo6XCIsIFwiYW5jZXN0b3Itb3Itc2VsZjo6XCIsIFwiZm9sbG93aW5nOjpcIiwgXCJwcmVjZWRpbmc6OlwiLCBcImZvbGxvd2luZy1zaWJsaW5nOjpcIiwgXCJwcmVjZWRpbmctc2libGluZzo6XCJdO1xuICBmb3IgKHZhciBpID0gMCwgbCA9IGF4aXNfc3BlY2lmaWVycy5sZW5ndGg7IGkgPCBsOyBpKyspIHtcbiAgICBrd09ialtheGlzX3NwZWNpZmllcnNbaV1dID0gcXVhbGlmaWVyO1xuICB9XG4gIDtcbiAgcmV0dXJuIGt3T2JqO1xufSgpO1xuZnVuY3Rpb24gY2hhaW4oc3RyZWFtLCBzdGF0ZSwgZikge1xuICBzdGF0ZS50b2tlbml6ZSA9IGY7XG4gIHJldHVybiBmKHN0cmVhbSwgc3RhdGUpO1xufVxuXG4vLyB0aGUgcHJpbWFyeSBtb2RlIHRva2VuaXplclxuZnVuY3Rpb24gdG9rZW5CYXNlKHN0cmVhbSwgc3RhdGUpIHtcbiAgdmFyIGNoID0gc3RyZWFtLm5leHQoKSxcbiAgICBtaWdodEJlRnVuY3Rpb24gPSBmYWxzZSxcbiAgICBpc0VRTmFtZSA9IGlzRVFOYW1lQWhlYWQoc3RyZWFtKTtcblxuICAvLyBhbiBYTUwgdGFnIChpZiBub3QgaW4gc29tZSBzdWIsIGNoYWluZWQgdG9rZW5pemVyKVxuICBpZiAoY2ggPT0gXCI8XCIpIHtcbiAgICBpZiAoc3RyZWFtLm1hdGNoKFwiIS0tXCIsIHRydWUpKSByZXR1cm4gY2hhaW4oc3RyZWFtLCBzdGF0ZSwgdG9rZW5YTUxDb21tZW50KTtcbiAgICBpZiAoc3RyZWFtLm1hdGNoKFwiIVtDREFUQVwiLCBmYWxzZSkpIHtcbiAgICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5DREFUQTtcbiAgICAgIHJldHVybiBcInRhZ1wiO1xuICAgIH1cbiAgICBpZiAoc3RyZWFtLm1hdGNoKFwiP1wiLCBmYWxzZSkpIHtcbiAgICAgIHJldHVybiBjaGFpbihzdHJlYW0sIHN0YXRlLCB0b2tlblByZVByb2Nlc3NpbmcpO1xuICAgIH1cbiAgICB2YXIgaXNjbG9zZSA9IHN0cmVhbS5lYXQoXCIvXCIpO1xuICAgIHN0cmVhbS5lYXRTcGFjZSgpO1xuICAgIHZhciB0YWdOYW1lID0gXCJcIixcbiAgICAgIGM7XG4gICAgd2hpbGUgKGMgPSBzdHJlYW0uZWF0KC9bXlxcc1xcdTAwYTA9PD5cXFwiXFwnXFwvP10vKSkgdGFnTmFtZSArPSBjO1xuICAgIHJldHVybiBjaGFpbihzdHJlYW0sIHN0YXRlLCB0b2tlblRhZyh0YWdOYW1lLCBpc2Nsb3NlKSk7XG4gIH1cbiAgLy8gc3RhcnQgY29kZSBibG9ja1xuICBlbHNlIGlmIChjaCA9PSBcIntcIikge1xuICAgIHB1c2hTdGF0ZVN0YWNrKHN0YXRlLCB7XG4gICAgICB0eXBlOiBcImNvZGVibG9ja1wiXG4gICAgfSk7XG4gICAgcmV0dXJuIG51bGw7XG4gIH1cbiAgLy8gZW5kIGNvZGUgYmxvY2tcbiAgZWxzZSBpZiAoY2ggPT0gXCJ9XCIpIHtcbiAgICBwb3BTdGF0ZVN0YWNrKHN0YXRlKTtcbiAgICByZXR1cm4gbnVsbDtcbiAgfVxuICAvLyBpZiB3ZSdyZSBpbiBhbiBYTUwgYmxvY2tcbiAgZWxzZSBpZiAoaXNJblhtbEJsb2NrKHN0YXRlKSkge1xuICAgIGlmIChjaCA9PSBcIj5cIikgcmV0dXJuIFwidGFnXCI7ZWxzZSBpZiAoY2ggPT0gXCIvXCIgJiYgc3RyZWFtLmVhdChcIj5cIikpIHtcbiAgICAgIHBvcFN0YXRlU3RhY2soc3RhdGUpO1xuICAgICAgcmV0dXJuIFwidGFnXCI7XG4gICAgfSBlbHNlIHJldHVybiBcInZhcmlhYmxlXCI7XG4gIH1cbiAgLy8gaWYgYSBudW1iZXJcbiAgZWxzZSBpZiAoL1xcZC8udGVzdChjaCkpIHtcbiAgICBzdHJlYW0ubWF0Y2goL15cXGQqKD86XFwuXFxkKik/KD86RVsrXFwtXT9cXGQrKT8vKTtcbiAgICByZXR1cm4gXCJhdG9tXCI7XG4gIH1cbiAgLy8gY29tbWVudCBzdGFydFxuICBlbHNlIGlmIChjaCA9PT0gXCIoXCIgJiYgc3RyZWFtLmVhdChcIjpcIikpIHtcbiAgICBwdXNoU3RhdGVTdGFjayhzdGF0ZSwge1xuICAgICAgdHlwZTogXCJjb21tZW50XCJcbiAgICB9KTtcbiAgICByZXR1cm4gY2hhaW4oc3RyZWFtLCBzdGF0ZSwgdG9rZW5Db21tZW50KTtcbiAgfVxuICAvLyBxdW90ZWQgc3RyaW5nXG4gIGVsc2UgaWYgKCFpc0VRTmFtZSAmJiAoY2ggPT09ICdcIicgfHwgY2ggPT09IFwiJ1wiKSkgcmV0dXJuIGNoYWluKHN0cmVhbSwgc3RhdGUsIHRva2VuU3RyaW5nKGNoKSk7XG4gIC8vIHZhcmlhYmxlXG4gIGVsc2UgaWYgKGNoID09PSBcIiRcIikge1xuICAgIHJldHVybiBjaGFpbihzdHJlYW0sIHN0YXRlLCB0b2tlblZhcmlhYmxlKTtcbiAgfVxuICAvLyBhc3NpZ25tZW50XG4gIGVsc2UgaWYgKGNoID09PSBcIjpcIiAmJiBzdHJlYW0uZWF0KFwiPVwiKSkge1xuICAgIHJldHVybiBcImtleXdvcmRcIjtcbiAgfVxuICAvLyBvcGVuIHBhcmVuXG4gIGVsc2UgaWYgKGNoID09PSBcIihcIikge1xuICAgIHB1c2hTdGF0ZVN0YWNrKHN0YXRlLCB7XG4gICAgICB0eXBlOiBcInBhcmVuXCJcbiAgICB9KTtcbiAgICByZXR1cm4gbnVsbDtcbiAgfVxuICAvLyBjbG9zZSBwYXJlblxuICBlbHNlIGlmIChjaCA9PT0gXCIpXCIpIHtcbiAgICBwb3BTdGF0ZVN0YWNrKHN0YXRlKTtcbiAgICByZXR1cm4gbnVsbDtcbiAgfVxuICAvLyBvcGVuIHBhcmVuXG4gIGVsc2UgaWYgKGNoID09PSBcIltcIikge1xuICAgIHB1c2hTdGF0ZVN0YWNrKHN0YXRlLCB7XG4gICAgICB0eXBlOiBcImJyYWNrZXRcIlxuICAgIH0pO1xuICAgIHJldHVybiBudWxsO1xuICB9XG4gIC8vIGNsb3NlIHBhcmVuXG4gIGVsc2UgaWYgKGNoID09PSBcIl1cIikge1xuICAgIHBvcFN0YXRlU3RhY2soc3RhdGUpO1xuICAgIHJldHVybiBudWxsO1xuICB9IGVsc2Uge1xuICAgIHZhciBrbm93biA9IGtleXdvcmRzLnByb3BlcnR5SXNFbnVtZXJhYmxlKGNoKSAmJiBrZXl3b3Jkc1tjaF07XG5cbiAgICAvLyBpZiB0aGVyZSdzIGEgRVFOYW1lIGFoZWFkLCBjb25zdW1lIHRoZSByZXN0IG9mIHRoZSBzdHJpbmcgcG9ydGlvbiwgaXQncyBsaWtlbHkgYSBmdW5jdGlvblxuICAgIGlmIChpc0VRTmFtZSAmJiBjaCA9PT0gJ1xcXCInKSB3aGlsZSAoc3RyZWFtLm5leHQoKSAhPT0gJ1wiJykge31cbiAgICBpZiAoaXNFUU5hbWUgJiYgY2ggPT09ICdcXCcnKSB3aGlsZSAoc3RyZWFtLm5leHQoKSAhPT0gJ1xcJycpIHt9XG5cbiAgICAvLyBnb2JibGUgdXAgYSB3b3JkIGlmIHRoZSBjaGFyYWN0ZXIgaXMgbm90IGtub3duXG4gICAgaWYgKCFrbm93bikgc3RyZWFtLmVhdFdoaWxlKC9bXFx3XFwkXy1dLyk7XG5cbiAgICAvLyBnb2JibGUgYSBjb2xvbiBpbiB0aGUgY2FzZSB0aGF0IGlzIGEgbGliIGZ1bmMgdHlwZSBjYWxsIGZuOmRvY1xuICAgIHZhciBmb3VuZENvbG9uID0gc3RyZWFtLmVhdChcIjpcIik7XG5cbiAgICAvLyBpZiB0aGVyZSdzIG5vdCBhIHNlY29uZCBjb2xvbiwgZ29iYmxlIGFub3RoZXIgd29yZC4gT3RoZXJ3aXNlLCBpdCdzIHByb2JhYmx5IGFuIGF4aXMgc3BlY2lmaWVyXG4gICAgLy8gd2hpY2ggc2hvdWxkIGdldCBtYXRjaGVkIGFzIGEga2V5d29yZFxuICAgIGlmICghc3RyZWFtLmVhdChcIjpcIikgJiYgZm91bmRDb2xvbikge1xuICAgICAgc3RyZWFtLmVhdFdoaWxlKC9bXFx3XFwkXy1dLyk7XG4gICAgfVxuICAgIC8vIGlmIHRoZSBuZXh0IG5vbiB3aGl0ZXNwYWNlIGNoYXJhY3RlciBpcyBhbiBvcGVuIHBhcmVuLCB0aGlzIGlzIHByb2JhYmx5IGEgZnVuY3Rpb24gKGlmIG5vdCBhIGtleXdvcmQgb2Ygb3RoZXIgc29ydClcbiAgICBpZiAoc3RyZWFtLm1hdGNoKC9eWyBcXHRdKlxcKC8sIGZhbHNlKSkge1xuICAgICAgbWlnaHRCZUZ1bmN0aW9uID0gdHJ1ZTtcbiAgICB9XG4gICAgLy8gaXMgdGhlIHdvcmQgYSBrZXl3b3JkP1xuICAgIHZhciB3b3JkID0gc3RyZWFtLmN1cnJlbnQoKTtcbiAgICBrbm93biA9IGtleXdvcmRzLnByb3BlcnR5SXNFbnVtZXJhYmxlKHdvcmQpICYmIGtleXdvcmRzW3dvcmRdO1xuXG4gICAgLy8gaWYgd2UgdGhpbmsgaXQncyBhIGZ1bmN0aW9uIGNhbGwgYnV0IG5vdCB5ZXQga25vd24sXG4gICAgLy8gc2V0IHN0eWxlIHRvIHZhcmlhYmxlIGZvciBub3cgZm9yIGxhY2sgb2Ygc29tZXRoaW5nIGJldHRlclxuICAgIGlmIChtaWdodEJlRnVuY3Rpb24gJiYgIWtub3duKSBrbm93biA9IHtcbiAgICAgIHR5cGU6IFwiZnVuY3Rpb25fY2FsbFwiLFxuICAgICAgc3R5bGU6IFwiZGVmXCJcbiAgICB9O1xuXG4gICAgLy8gaWYgdGhlIHByZXZpb3VzIHdvcmQgd2FzIGVsZW1lbnQsIGF0dHJpYnV0ZSwgYXhpcyBzcGVjaWZpZXIsIHRoaXMgd29yZCBzaG91bGQgYmUgdGhlIG5hbWUgb2YgdGhhdFxuICAgIGlmIChpc0luWG1sQ29uc3RydWN0b3Ioc3RhdGUpKSB7XG4gICAgICBwb3BTdGF0ZVN0YWNrKHN0YXRlKTtcbiAgICAgIHJldHVybiBcInZhcmlhYmxlXCI7XG4gICAgfVxuICAgIC8vIGFzIHByZXZpb3VzbHkgY2hlY2tlZCwgaWYgdGhlIHdvcmQgaXMgZWxlbWVudCxhdHRyaWJ1dGUsIGF4aXMgc3BlY2lmaWVyLCBjYWxsIGl0IGFuIFwieG1sY29uc3RydWN0b3JcIiBhbmRcbiAgICAvLyBwdXNoIHRoZSBzdGFjayBzbyB3ZSBrbm93IHRvIGxvb2sgZm9yIGl0IG9uIHRoZSBuZXh0IHdvcmRcbiAgICBpZiAod29yZCA9PSBcImVsZW1lbnRcIiB8fCB3b3JkID09IFwiYXR0cmlidXRlXCIgfHwga25vd24udHlwZSA9PSBcImF4aXNfc3BlY2lmaWVyXCIpIHB1c2hTdGF0ZVN0YWNrKHN0YXRlLCB7XG4gICAgICB0eXBlOiBcInhtbGNvbnN0cnVjdG9yXCJcbiAgICB9KTtcblxuICAgIC8vIGlmIHRoZSB3b3JkIGlzIGtub3duLCByZXR1cm4gdGhlIGRldGFpbHMgb2YgdGhhdCBlbHNlIGp1c3QgY2FsbCB0aGlzIGEgZ2VuZXJpYyAnd29yZCdcbiAgICByZXR1cm4ga25vd24gPyBrbm93bi5zdHlsZSA6IFwidmFyaWFibGVcIjtcbiAgfVxufVxuXG4vLyBoYW5kbGUgY29tbWVudHMsIGluY2x1ZGluZyBuZXN0ZWRcbmZ1bmN0aW9uIHRva2VuQ29tbWVudChzdHJlYW0sIHN0YXRlKSB7XG4gIHZhciBtYXliZUVuZCA9IGZhbHNlLFxuICAgIG1heWJlTmVzdGVkID0gZmFsc2UsXG4gICAgbmVzdGVkQ291bnQgPSAwLFxuICAgIGNoO1xuICB3aGlsZSAoY2ggPSBzdHJlYW0ubmV4dCgpKSB7XG4gICAgaWYgKGNoID09IFwiKVwiICYmIG1heWJlRW5kKSB7XG4gICAgICBpZiAobmVzdGVkQ291bnQgPiAwKSBuZXN0ZWRDb3VudC0tO2Vsc2Uge1xuICAgICAgICBwb3BTdGF0ZVN0YWNrKHN0YXRlKTtcbiAgICAgICAgYnJlYWs7XG4gICAgICB9XG4gICAgfSBlbHNlIGlmIChjaCA9PSBcIjpcIiAmJiBtYXliZU5lc3RlZCkge1xuICAgICAgbmVzdGVkQ291bnQrKztcbiAgICB9XG4gICAgbWF5YmVFbmQgPSBjaCA9PSBcIjpcIjtcbiAgICBtYXliZU5lc3RlZCA9IGNoID09IFwiKFwiO1xuICB9XG4gIHJldHVybiBcImNvbW1lbnRcIjtcbn1cblxuLy8gdG9rZW5pemVyIGZvciBzdHJpbmcgbGl0ZXJhbHNcbi8vIG9wdGlvbmFsbHkgcGFzcyBhIHRva2VuaXplciBmdW5jdGlvbiB0byBzZXQgc3RhdGUudG9rZW5pemUgYmFjayB0byB3aGVuIGZpbmlzaGVkXG5mdW5jdGlvbiB0b2tlblN0cmluZyhxdW90ZSwgZikge1xuICByZXR1cm4gZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICB2YXIgY2g7XG4gICAgaWYgKGlzSW5TdHJpbmcoc3RhdGUpICYmIHN0cmVhbS5jdXJyZW50KCkgPT0gcXVvdGUpIHtcbiAgICAgIHBvcFN0YXRlU3RhY2soc3RhdGUpO1xuICAgICAgaWYgKGYpIHN0YXRlLnRva2VuaXplID0gZjtcbiAgICAgIHJldHVybiBcInN0cmluZ1wiO1xuICAgIH1cbiAgICBwdXNoU3RhdGVTdGFjayhzdGF0ZSwge1xuICAgICAgdHlwZTogXCJzdHJpbmdcIixcbiAgICAgIG5hbWU6IHF1b3RlLFxuICAgICAgdG9rZW5pemU6IHRva2VuU3RyaW5nKHF1b3RlLCBmKVxuICAgIH0pO1xuXG4gICAgLy8gaWYgd2UncmUgaW4gYSBzdHJpbmcgYW5kIGluIGFuIFhNTCBibG9jaywgYWxsb3cgYW4gZW1iZWRkZWQgY29kZSBibG9ja1xuICAgIGlmIChzdHJlYW0ubWF0Y2goXCJ7XCIsIGZhbHNlKSAmJiBpc0luWG1sQXR0cmlidXRlQmxvY2soc3RhdGUpKSB7XG4gICAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQmFzZTtcbiAgICAgIHJldHVybiBcInN0cmluZ1wiO1xuICAgIH1cbiAgICB3aGlsZSAoY2ggPSBzdHJlYW0ubmV4dCgpKSB7XG4gICAgICBpZiAoY2ggPT0gcXVvdGUpIHtcbiAgICAgICAgcG9wU3RhdGVTdGFjayhzdGF0ZSk7XG4gICAgICAgIGlmIChmKSBzdGF0ZS50b2tlbml6ZSA9IGY7XG4gICAgICAgIGJyZWFrO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgLy8gaWYgd2UncmUgaW4gYSBzdHJpbmcgYW5kIGluIGFuIFhNTCBibG9jaywgYWxsb3cgYW4gZW1iZWRkZWQgY29kZSBibG9jayBpbiBhbiBhdHRyaWJ1dGVcbiAgICAgICAgaWYgKHN0cmVhbS5tYXRjaChcIntcIiwgZmFsc2UpICYmIGlzSW5YbWxBdHRyaWJ1dGVCbG9jayhzdGF0ZSkpIHtcbiAgICAgICAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQmFzZTtcbiAgICAgICAgICByZXR1cm4gXCJzdHJpbmdcIjtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH1cbiAgICByZXR1cm4gXCJzdHJpbmdcIjtcbiAgfTtcbn1cblxuLy8gdG9rZW5pemVyIGZvciB2YXJpYWJsZXNcbmZ1bmN0aW9uIHRva2VuVmFyaWFibGUoc3RyZWFtLCBzdGF0ZSkge1xuICB2YXIgaXNWYXJpYWJsZUNoYXIgPSAvW1xcd1xcJF8tXS87XG5cbiAgLy8gYSB2YXJpYWJsZSBtYXkgc3RhcnQgd2l0aCBhIHF1b3RlZCBFUU5hbWUgc28gaWYgdGhlIG5leHQgY2hhcmFjdGVyIGlzIHF1b3RlLCBjb25zdW1lIHRvIHRoZSBuZXh0IHF1b3RlXG4gIGlmIChzdHJlYW0uZWF0KFwiXFxcIlwiKSkge1xuICAgIHdoaWxlIChzdHJlYW0ubmV4dCgpICE9PSAnXFxcIicpIHt9XG4gICAgO1xuICAgIHN0cmVhbS5lYXQoXCI6XCIpO1xuICB9IGVsc2Uge1xuICAgIHN0cmVhbS5lYXRXaGlsZShpc1ZhcmlhYmxlQ2hhcik7XG4gICAgaWYgKCFzdHJlYW0ubWF0Y2goXCI6PVwiLCBmYWxzZSkpIHN0cmVhbS5lYXQoXCI6XCIpO1xuICB9XG4gIHN0cmVhbS5lYXRXaGlsZShpc1ZhcmlhYmxlQ2hhcik7XG4gIHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlO1xuICByZXR1cm4gXCJ2YXJpYWJsZVwiO1xufVxuXG4vLyB0b2tlbml6ZXIgZm9yIFhNTCB0YWdzXG5mdW5jdGlvbiB0b2tlblRhZyhuYW1lLCBpc2Nsb3NlKSB7XG4gIHJldHVybiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIHN0cmVhbS5lYXRTcGFjZSgpO1xuICAgIGlmIChpc2Nsb3NlICYmIHN0cmVhbS5lYXQoXCI+XCIpKSB7XG4gICAgICBwb3BTdGF0ZVN0YWNrKHN0YXRlKTtcbiAgICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlO1xuICAgICAgcmV0dXJuIFwidGFnXCI7XG4gICAgfVxuICAgIC8vIHNlbGYgY2xvc2luZyB0YWcgd2l0aG91dCBhdHRyaWJ1dGVzP1xuICAgIGlmICghc3RyZWFtLmVhdChcIi9cIikpIHB1c2hTdGF0ZVN0YWNrKHN0YXRlLCB7XG4gICAgICB0eXBlOiBcInRhZ1wiLFxuICAgICAgbmFtZTogbmFtZSxcbiAgICAgIHRva2VuaXplOiB0b2tlbkJhc2VcbiAgICB9KTtcbiAgICBpZiAoIXN0cmVhbS5lYXQoXCI+XCIpKSB7XG4gICAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQXR0cmlidXRlO1xuICAgICAgcmV0dXJuIFwidGFnXCI7XG4gICAgfSBlbHNlIHtcbiAgICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlO1xuICAgIH1cbiAgICByZXR1cm4gXCJ0YWdcIjtcbiAgfTtcbn1cblxuLy8gdG9rZW5pemVyIGZvciBYTUwgYXR0cmlidXRlc1xuZnVuY3Rpb24gdG9rZW5BdHRyaWJ1dGUoc3RyZWFtLCBzdGF0ZSkge1xuICB2YXIgY2ggPSBzdHJlYW0ubmV4dCgpO1xuICBpZiAoY2ggPT0gXCIvXCIgJiYgc3RyZWFtLmVhdChcIj5cIikpIHtcbiAgICBpZiAoaXNJblhtbEF0dHJpYnV0ZUJsb2NrKHN0YXRlKSkgcG9wU3RhdGVTdGFjayhzdGF0ZSk7XG4gICAgaWYgKGlzSW5YbWxCbG9jayhzdGF0ZSkpIHBvcFN0YXRlU3RhY2soc3RhdGUpO1xuICAgIHJldHVybiBcInRhZ1wiO1xuICB9XG4gIGlmIChjaCA9PSBcIj5cIikge1xuICAgIGlmIChpc0luWG1sQXR0cmlidXRlQmxvY2soc3RhdGUpKSBwb3BTdGF0ZVN0YWNrKHN0YXRlKTtcbiAgICByZXR1cm4gXCJ0YWdcIjtcbiAgfVxuICBpZiAoY2ggPT0gXCI9XCIpIHJldHVybiBudWxsO1xuICAvLyBxdW90ZWQgc3RyaW5nXG4gIGlmIChjaCA9PSAnXCInIHx8IGNoID09IFwiJ1wiKSByZXR1cm4gY2hhaW4oc3RyZWFtLCBzdGF0ZSwgdG9rZW5TdHJpbmcoY2gsIHRva2VuQXR0cmlidXRlKSk7XG4gIGlmICghaXNJblhtbEF0dHJpYnV0ZUJsb2NrKHN0YXRlKSkgcHVzaFN0YXRlU3RhY2soc3RhdGUsIHtcbiAgICB0eXBlOiBcImF0dHJpYnV0ZVwiLFxuICAgIHRva2VuaXplOiB0b2tlbkF0dHJpYnV0ZVxuICB9KTtcbiAgc3RyZWFtLmVhdCgvW2EtekEtWl86XS8pO1xuICBzdHJlYW0uZWF0V2hpbGUoL1stYS16QS1aMC05XzouXS8pO1xuICBzdHJlYW0uZWF0U3BhY2UoKTtcblxuICAvLyB0aGUgY2FzZSB3aGVyZSB0aGUgYXR0cmlidXRlIGhhcyBub3QgdmFsdWUgYW5kIHRoZSB0YWcgd2FzIGNsb3NlZFxuICBpZiAoc3RyZWFtLm1hdGNoKFwiPlwiLCBmYWxzZSkgfHwgc3RyZWFtLm1hdGNoKFwiL1wiLCBmYWxzZSkpIHtcbiAgICBwb3BTdGF0ZVN0YWNrKHN0YXRlKTtcbiAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQmFzZTtcbiAgfVxuICByZXR1cm4gXCJhdHRyaWJ1dGVcIjtcbn1cblxuLy8gaGFuZGxlIGNvbW1lbnRzLCBpbmNsdWRpbmcgbmVzdGVkXG5mdW5jdGlvbiB0b2tlblhNTENvbW1lbnQoc3RyZWFtLCBzdGF0ZSkge1xuICB2YXIgY2g7XG4gIHdoaWxlIChjaCA9IHN0cmVhbS5uZXh0KCkpIHtcbiAgICBpZiAoY2ggPT0gXCItXCIgJiYgc3RyZWFtLm1hdGNoKFwiLT5cIiwgdHJ1ZSkpIHtcbiAgICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlO1xuICAgICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICAgIH1cbiAgfVxufVxuXG4vLyBoYW5kbGUgQ0RBVEFcbmZ1bmN0aW9uIHRva2VuQ0RBVEEoc3RyZWFtLCBzdGF0ZSkge1xuICB2YXIgY2g7XG4gIHdoaWxlIChjaCA9IHN0cmVhbS5uZXh0KCkpIHtcbiAgICBpZiAoY2ggPT0gXCJdXCIgJiYgc3RyZWFtLm1hdGNoKFwiXVwiLCB0cnVlKSkge1xuICAgICAgc3RhdGUudG9rZW5pemUgPSB0b2tlbkJhc2U7XG4gICAgICByZXR1cm4gXCJjb21tZW50XCI7XG4gICAgfVxuICB9XG59XG5cbi8vIGhhbmRsZSBwcmVwcm9jZXNzaW5nIGluc3RydWN0aW9uc1xuZnVuY3Rpb24gdG9rZW5QcmVQcm9jZXNzaW5nKHN0cmVhbSwgc3RhdGUpIHtcbiAgdmFyIGNoO1xuICB3aGlsZSAoY2ggPSBzdHJlYW0ubmV4dCgpKSB7XG4gICAgaWYgKGNoID09IFwiP1wiICYmIHN0cmVhbS5tYXRjaChcIj5cIiwgdHJ1ZSkpIHtcbiAgICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlO1xuICAgICAgcmV0dXJuIFwicHJvY2Vzc2luZ0luc3RydWN0aW9uXCI7XG4gICAgfVxuICB9XG59XG5cbi8vIGZ1bmN0aW9ucyB0byB0ZXN0IHRoZSBjdXJyZW50IGNvbnRleHQgb2YgdGhlIHN0YXRlXG5mdW5jdGlvbiBpc0luWG1sQmxvY2soc3RhdGUpIHtcbiAgcmV0dXJuIGlzSW4oc3RhdGUsIFwidGFnXCIpO1xufVxuZnVuY3Rpb24gaXNJblhtbEF0dHJpYnV0ZUJsb2NrKHN0YXRlKSB7XG4gIHJldHVybiBpc0luKHN0YXRlLCBcImF0dHJpYnV0ZVwiKTtcbn1cbmZ1bmN0aW9uIGlzSW5YbWxDb25zdHJ1Y3RvcihzdGF0ZSkge1xuICByZXR1cm4gaXNJbihzdGF0ZSwgXCJ4bWxjb25zdHJ1Y3RvclwiKTtcbn1cbmZ1bmN0aW9uIGlzSW5TdHJpbmcoc3RhdGUpIHtcbiAgcmV0dXJuIGlzSW4oc3RhdGUsIFwic3RyaW5nXCIpO1xufVxuZnVuY3Rpb24gaXNFUU5hbWVBaGVhZChzdHJlYW0pIHtcbiAgLy8gYXNzdW1lIHdlJ3ZlIGFscmVhZHkgZWF0ZW4gYSBxdW90ZSAoXCIpXG4gIGlmIChzdHJlYW0uY3VycmVudCgpID09PSAnXCInKSByZXR1cm4gc3RyZWFtLm1hdGNoKC9eW15cXFwiXStcXFwiXFw6LywgZmFsc2UpO2Vsc2UgaWYgKHN0cmVhbS5jdXJyZW50KCkgPT09ICdcXCcnKSByZXR1cm4gc3RyZWFtLm1hdGNoKC9eW15cXFwiXStcXCdcXDovLCBmYWxzZSk7ZWxzZSByZXR1cm4gZmFsc2U7XG59XG5mdW5jdGlvbiBpc0luKHN0YXRlLCB0eXBlKSB7XG4gIHJldHVybiBzdGF0ZS5zdGFjay5sZW5ndGggJiYgc3RhdGUuc3RhY2tbc3RhdGUuc3RhY2subGVuZ3RoIC0gMV0udHlwZSA9PSB0eXBlO1xufVxuZnVuY3Rpb24gcHVzaFN0YXRlU3RhY2soc3RhdGUsIG5ld1N0YXRlKSB7XG4gIHN0YXRlLnN0YWNrLnB1c2gobmV3U3RhdGUpO1xufVxuZnVuY3Rpb24gcG9wU3RhdGVTdGFjayhzdGF0ZSkge1xuICBzdGF0ZS5zdGFjay5wb3AoKTtcbiAgdmFyIHJlaW5zdGF0ZVRva2VuaXplID0gc3RhdGUuc3RhY2subGVuZ3RoICYmIHN0YXRlLnN0YWNrW3N0YXRlLnN0YWNrLmxlbmd0aCAtIDFdLnRva2VuaXplO1xuICBzdGF0ZS50b2tlbml6ZSA9IHJlaW5zdGF0ZVRva2VuaXplIHx8IHRva2VuQmFzZTtcbn1cblxuLy8gdGhlIGludGVyZmFjZSBmb3IgdGhlIG1vZGUgQVBJXG5leHBvcnQgY29uc3QgeFF1ZXJ5ID0ge1xuICBuYW1lOiBcInhxdWVyeVwiLFxuICBzdGFydFN0YXRlOiBmdW5jdGlvbiAoKSB7XG4gICAgcmV0dXJuIHtcbiAgICAgIHRva2VuaXplOiB0b2tlbkJhc2UsXG4gICAgICBjYzogW10sXG4gICAgICBzdGFjazogW11cbiAgICB9O1xuICB9LFxuICB0b2tlbjogZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICBpZiAoc3RyZWFtLmVhdFNwYWNlKCkpIHJldHVybiBudWxsO1xuICAgIHZhciBzdHlsZSA9IHN0YXRlLnRva2VuaXplKHN0cmVhbSwgc3RhdGUpO1xuICAgIHJldHVybiBzdHlsZTtcbiAgfSxcbiAgbGFuZ3VhZ2VEYXRhOiB7XG4gICAgY29tbWVudFRva2Vuczoge1xuICAgICAgYmxvY2s6IHtcbiAgICAgICAgb3BlbjogXCIoOlwiLFxuICAgICAgICBjbG9zZTogXCI6KVwiXG4gICAgICB9XG4gICAgfVxuICB9XG59OyJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==