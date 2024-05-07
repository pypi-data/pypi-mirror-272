"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[5058],{

/***/ 25058:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "tlv": () => (/* binding */ tlv),
/* harmony export */   "verilog": () => (/* binding */ verilog)
/* harmony export */ });
function mkVerilog(parserConfig) {
  var statementIndentUnit = parserConfig.statementIndentUnit,
    dontAlignCalls = parserConfig.dontAlignCalls,
    noIndentKeywords = parserConfig.noIndentKeywords || [],
    multiLineStrings = parserConfig.multiLineStrings,
    hooks = parserConfig.hooks || {};
  function words(str) {
    var obj = {},
      words = str.split(" ");
    for (var i = 0; i < words.length; ++i) obj[words[i]] = true;
    return obj;
  }

  /**
   * Keywords from IEEE 1800-2012
   */
  var keywords = words("accept_on alias always always_comb always_ff always_latch and assert assign assume automatic before begin bind " + "bins binsof bit break buf bufif0 bufif1 byte case casex casez cell chandle checker class clocking cmos config " + "const constraint context continue cover covergroup coverpoint cross deassign default defparam design disable " + "dist do edge else end endcase endchecker endclass endclocking endconfig endfunction endgenerate endgroup " + "endinterface endmodule endpackage endprimitive endprogram endproperty endspecify endsequence endtable endtask " + "enum event eventually expect export extends extern final first_match for force foreach forever fork forkjoin " + "function generate genvar global highz0 highz1 if iff ifnone ignore_bins illegal_bins implements implies import " + "incdir include initial inout input inside instance int integer interconnect interface intersect join join_any " + "join_none large let liblist library local localparam logic longint macromodule matches medium modport module " + "nand negedge nettype new nexttime nmos nor noshowcancelled not notif0 notif1 null or output package packed " + "parameter pmos posedge primitive priority program property protected pull0 pull1 pulldown pullup " + "pulsestyle_ondetect pulsestyle_onevent pure rand randc randcase randsequence rcmos real realtime ref reg " + "reject_on release repeat restrict return rnmos rpmos rtran rtranif0 rtranif1 s_always s_eventually s_nexttime " + "s_until s_until_with scalared sequence shortint shortreal showcancelled signed small soft solve specify " + "specparam static string strong strong0 strong1 struct super supply0 supply1 sync_accept_on sync_reject_on " + "table tagged task this throughout time timeprecision timeunit tran tranif0 tranif1 tri tri0 tri1 triand trior " + "trireg type typedef union unique unique0 unsigned until until_with untyped use uwire var vectored virtual void " + "wait wait_order wand weak weak0 weak1 while wildcard wire with within wor xnor xor");

  /** Operators from IEEE 1800-2012
      unary_operator ::=
      + | - | ! | ~ | & | ~& | | | ~| | ^ | ~^ | ^~
      binary_operator ::=
      + | - | * | / | % | == | != | === | !== | ==? | !=? | && | || | **
      | < | <= | > | >= | & | | | ^ | ^~ | ~^ | >> | << | >>> | <<<
      | -> | <->
      inc_or_dec_operator ::= ++ | --
      unary_module_path_operator ::=
      ! | ~ | & | ~& | | | ~| | ^ | ~^ | ^~
      binary_module_path_operator ::=
      == | != | && | || | & | | | ^ | ^~ | ~^
  */
  var isOperatorChar = /[\+\-\*\/!~&|^%=?:]/;
  var isBracketChar = /[\[\]{}()]/;
  var unsignedNumber = /\d[0-9_]*/;
  var decimalLiteral = /\d*\s*'s?d\s*\d[0-9_]*/i;
  var binaryLiteral = /\d*\s*'s?b\s*[xz01][xz01_]*/i;
  var octLiteral = /\d*\s*'s?o\s*[xz0-7][xz0-7_]*/i;
  var hexLiteral = /\d*\s*'s?h\s*[0-9a-fxz?][0-9a-fxz?_]*/i;
  var realLiteral = /(\d[\d_]*(\.\d[\d_]*)?E-?[\d_]+)|(\d[\d_]*\.\d[\d_]*)/i;
  var closingBracketOrWord = /^((\w+)|[)}\]])/;
  var closingBracket = /[)}\]]/;
  var curPunc;
  var curKeyword;

  // Block openings which are closed by a matching keyword in the form of ("end" + keyword)
  // E.g. "task" => "endtask"
  var blockKeywords = words("case checker class clocking config function generate interface module package " + "primitive program property specify sequence table task");

  // Opening/closing pairs
  var openClose = {};
  for (var keyword in blockKeywords) {
    openClose[keyword] = "end" + keyword;
  }
  openClose["begin"] = "end";
  openClose["casex"] = "endcase";
  openClose["casez"] = "endcase";
  openClose["do"] = "while";
  openClose["fork"] = "join;join_any;join_none";
  openClose["covergroup"] = "endgroup";
  for (var i in noIndentKeywords) {
    var keyword = noIndentKeywords[i];
    if (openClose[keyword]) {
      openClose[keyword] = undefined;
    }
  }

  // Keywords which open statements that are ended with a semi-colon
  var statementKeywords = words("always always_comb always_ff always_latch assert assign assume else export for foreach forever if import initial repeat while");
  function tokenBase(stream, state) {
    var ch = stream.peek(),
      style;
    if (hooks[ch] && (style = hooks[ch](stream, state)) != false) return style;
    if (hooks.tokenBase && (style = hooks.tokenBase(stream, state)) != false) return style;
    if (/[,;:\.]/.test(ch)) {
      curPunc = stream.next();
      return null;
    }
    if (isBracketChar.test(ch)) {
      curPunc = stream.next();
      return "bracket";
    }
    // Macros (tick-defines)
    if (ch == '`') {
      stream.next();
      if (stream.eatWhile(/[\w\$_]/)) {
        return "def";
      } else {
        return null;
      }
    }
    // System calls
    if (ch == '$') {
      stream.next();
      if (stream.eatWhile(/[\w\$_]/)) {
        return "meta";
      } else {
        return null;
      }
    }
    // Time literals
    if (ch == '#') {
      stream.next();
      stream.eatWhile(/[\d_.]/);
      return "def";
    }
    // Strings
    if (ch == '"') {
      stream.next();
      state.tokenize = tokenString(ch);
      return state.tokenize(stream, state);
    }
    // Comments
    if (ch == "/") {
      stream.next();
      if (stream.eat("*")) {
        state.tokenize = tokenComment;
        return tokenComment(stream, state);
      }
      if (stream.eat("/")) {
        stream.skipToEnd();
        return "comment";
      }
      stream.backUp(1);
    }

    // Numeric literals
    if (stream.match(realLiteral) || stream.match(decimalLiteral) || stream.match(binaryLiteral) || stream.match(octLiteral) || stream.match(hexLiteral) || stream.match(unsignedNumber) || stream.match(realLiteral)) {
      return "number";
    }

    // Operators
    if (stream.eatWhile(isOperatorChar)) {
      return "meta";
    }

    // Keywords / plain variables
    if (stream.eatWhile(/[\w\$_]/)) {
      var cur = stream.current();
      if (keywords[cur]) {
        if (openClose[cur]) {
          curPunc = "newblock";
        }
        if (statementKeywords[cur]) {
          curPunc = "newstatement";
        }
        curKeyword = cur;
        return "keyword";
      }
      return "variable";
    }
    stream.next();
    return null;
  }
  function tokenString(quote) {
    return function (stream, state) {
      var escaped = false,
        next,
        end = false;
      while ((next = stream.next()) != null) {
        if (next == quote && !escaped) {
          end = true;
          break;
        }
        escaped = !escaped && next == "\\";
      }
      if (end || !(escaped || multiLineStrings)) state.tokenize = tokenBase;
      return "string";
    };
  }
  function tokenComment(stream, state) {
    var maybeEnd = false,
      ch;
    while (ch = stream.next()) {
      if (ch == "/" && maybeEnd) {
        state.tokenize = tokenBase;
        break;
      }
      maybeEnd = ch == "*";
    }
    return "comment";
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
    var c = new Context(indent, col, type, null, state.context);
    return state.context = c;
  }
  function popContext(state) {
    var t = state.context.type;
    if (t == ")" || t == "]" || t == "}") {
      state.indented = state.context.indented;
    }
    return state.context = state.context.prev;
  }
  function isClosing(text, contextClosing) {
    if (text == contextClosing) {
      return true;
    } else {
      // contextClosing may be multiple keywords separated by ;
      var closingKeywords = contextClosing.split(";");
      for (var i in closingKeywords) {
        if (text == closingKeywords[i]) {
          return true;
        }
      }
      return false;
    }
  }
  function buildElectricInputRegEx() {
    // Reindentation should occur on any bracket char: {}()[]
    // or on a match of any of the block closing keywords, at
    // the end of a line
    var allClosings = [];
    for (var i in openClose) {
      if (openClose[i]) {
        var closings = openClose[i].split(";");
        for (var j in closings) {
          allClosings.push(closings[j]);
        }
      }
    }
    var re = new RegExp("[{}()\\[\\]]|(" + allClosings.join("|") + ")$");
    return re;
  }

  // Interface
  return {
    name: "verilog",
    startState: function (indentUnit) {
      var state = {
        tokenize: null,
        context: new Context(-indentUnit, 0, "top", false),
        indented: 0,
        startOfLine: true
      };
      if (hooks.startState) hooks.startState(state);
      return state;
    },
    token: function (stream, state) {
      var ctx = state.context;
      if (stream.sol()) {
        if (ctx.align == null) ctx.align = false;
        state.indented = stream.indentation();
        state.startOfLine = true;
      }
      if (hooks.token) {
        // Call hook, with an optional return value of a style to override verilog styling.
        var style = hooks.token(stream, state);
        if (style !== undefined) {
          return style;
        }
      }
      if (stream.eatSpace()) return null;
      curPunc = null;
      curKeyword = null;
      var style = (state.tokenize || tokenBase)(stream, state);
      if (style == "comment" || style == "meta" || style == "variable") return style;
      if (ctx.align == null) ctx.align = true;
      if (curPunc == ctx.type) {
        popContext(state);
      } else if (curPunc == ";" && ctx.type == "statement" || ctx.type && isClosing(curKeyword, ctx.type)) {
        ctx = popContext(state);
        while (ctx && ctx.type == "statement") ctx = popContext(state);
      } else if (curPunc == "{") {
        pushContext(state, stream.column(), "}");
      } else if (curPunc == "[") {
        pushContext(state, stream.column(), "]");
      } else if (curPunc == "(") {
        pushContext(state, stream.column(), ")");
      } else if (ctx && ctx.type == "endcase" && curPunc == ":") {
        pushContext(state, stream.column(), "statement");
      } else if (curPunc == "newstatement") {
        pushContext(state, stream.column(), "statement");
      } else if (curPunc == "newblock") {
        if (curKeyword == "function" && ctx && (ctx.type == "statement" || ctx.type == "endgroup")) {
          // The 'function' keyword can appear in some other contexts where it actually does not
          // indicate a function (import/export DPI and covergroup definitions).
          // Do nothing in this case
        } else if (curKeyword == "task" && ctx && ctx.type == "statement") {
          // Same thing for task
        } else {
          var close = openClose[curKeyword];
          pushContext(state, stream.column(), close);
        }
      }
      state.startOfLine = false;
      return style;
    },
    indent: function (state, textAfter, cx) {
      if (state.tokenize != tokenBase && state.tokenize != null) return null;
      if (hooks.indent) {
        var fromHook = hooks.indent(state);
        if (fromHook >= 0) return fromHook;
      }
      var ctx = state.context,
        firstChar = textAfter && textAfter.charAt(0);
      if (ctx.type == "statement" && firstChar == "}") ctx = ctx.prev;
      var closing = false;
      var possibleClosing = textAfter.match(closingBracketOrWord);
      if (possibleClosing) closing = isClosing(possibleClosing[0], ctx.type);
      if (ctx.type == "statement") return ctx.indented + (firstChar == "{" ? 0 : statementIndentUnit || cx.unit);else if (closingBracket.test(ctx.type) && ctx.align && !dontAlignCalls) return ctx.column + (closing ? 0 : 1);else if (ctx.type == ")" && !closing) return ctx.indented + (statementIndentUnit || cx.unit);else return ctx.indented + (closing ? 0 : cx.unit);
    },
    languageData: {
      indentOnInput: buildElectricInputRegEx(),
      commentTokens: {
        line: "//",
        block: {
          open: "/*",
          close: "*/"
        }
      }
    }
  };
}
;
const verilog = mkVerilog({});

// TL-Verilog mode.
// See tl-x.org for language spec.
// See the mode in action at makerchip.com.
// Contact: steve.hoover@redwoodeda.com

// TLV Identifier prefixes.
// Note that sign is not treated separately, so "+/-" versions of numeric identifiers
// are included.
var tlvIdentifierStyle = {
  "|": "link",
  ">": "property",
  // Should condition this off for > TLV 1c.
  "$": "variable",
  "$$": "variable",
  "?$": "qualifier",
  "?*": "qualifier",
  "-": "contentSeparator",
  "/": "property",
  "/-": "property",
  "@": "variableName.special",
  "@-": "variableName.special",
  "@++": "variableName.special",
  "@+=": "variableName.special",
  "@+=-": "variableName.special",
  "@--": "variableName.special",
  "@-=": "variableName.special",
  "%+": "tag",
  "%-": "tag",
  "%": "tag",
  ">>": "tag",
  "<<": "tag",
  "<>": "tag",
  "#": "tag",
  // Need to choose a style for this.
  "^": "attribute",
  "^^": "attribute",
  "^!": "attribute",
  "*": "variable",
  "**": "variable",
  "\\": "keyword",
  "\"": "comment"
};

// Lines starting with these characters define scope (result in indentation).
var tlvScopePrefixChars = {
  "/": "beh-hier",
  ">": "beh-hier",
  "-": "phys-hier",
  "|": "pipe",
  "?": "when",
  "@": "stage",
  "\\": "keyword"
};
var tlvIndentUnit = 3;
var tlvTrackStatements = false;
var tlvIdentMatch = /^([~!@#\$%\^&\*-\+=\?\/\\\|'"<>]+)([\d\w_]*)/; // Matches an identifier.
// Note that ':' is excluded, because of it's use in [:].
var tlvLineIndentationMatch = /^[! ] */;
var tlvCommentMatch = /^\/[\/\*]/;
const tlv = mkVerilog({
  hooks: {
    electricInput: false,
    // Return undefined for verilog tokenizing, or style for TLV token (null not used).
    // Standard CM styles are used for most formatting, but some TL-Verilog-specific highlighting
    // can be enabled with the definition of cm-tlv-* styles, including highlighting for:
    //   - M4 tokens
    //   - TLV scope indentation
    //   - Statement delimitation (enabled by tlvTrackStatements)
    token: function (stream, state) {
      var style = undefined;
      var match; // Return value of pattern matches.

      // Set highlighting mode based on code region (TLV or SV).
      if (stream.sol() && !state.tlvInBlockComment) {
        // Process region.
        if (stream.peek() == '\\') {
          style = "def";
          stream.skipToEnd();
          if (stream.string.match(/\\SV/)) {
            state.tlvCodeActive = false;
          } else if (stream.string.match(/\\TLV/)) {
            state.tlvCodeActive = true;
          }
        }
        // Correct indentation in the face of a line prefix char.
        if (state.tlvCodeActive && stream.pos == 0 && state.indented == 0 && (match = stream.match(tlvLineIndentationMatch, false))) {
          state.indented = match[0].length;
        }

        // Compute indentation state:
        //   o Auto indentation on next line
        //   o Indentation scope styles
        var indented = state.indented;
        var depth = indented / tlvIndentUnit;
        if (depth <= state.tlvIndentationStyle.length) {
          // not deeper than current scope

          var blankline = stream.string.length == indented;
          var chPos = depth * tlvIndentUnit;
          if (chPos < stream.string.length) {
            var bodyString = stream.string.slice(chPos);
            var ch = bodyString[0];
            if (tlvScopePrefixChars[ch] && (match = bodyString.match(tlvIdentMatch)) && tlvIdentifierStyle[match[1]]) {
              // This line begins scope.
              // Next line gets indented one level.
              indented += tlvIndentUnit;
              // Style the next level of indentation (except non-region keyword identifiers,
              //   which are statements themselves)
              if (!(ch == "\\" && chPos > 0)) {
                state.tlvIndentationStyle[depth] = tlvScopePrefixChars[ch];
                if (tlvTrackStatements) {
                  state.statementComment = false;
                }
                depth++;
              }
            }
          }
          // Clear out deeper indentation levels unless line is blank.
          if (!blankline) {
            while (state.tlvIndentationStyle.length > depth) {
              state.tlvIndentationStyle.pop();
            }
          }
        }
        // Set next level of indentation.
        state.tlvNextIndent = indented;
      }
      if (state.tlvCodeActive) {
        // Highlight as TLV.

        var beginStatement = false;
        if (tlvTrackStatements) {
          // This starts a statement if the position is at the scope level
          // and we're not within a statement leading comment.
          beginStatement = stream.peek() != " " &&
          // not a space
          style === undefined &&
          // not a region identifier
          !state.tlvInBlockComment &&
          // not in block comment
          //!stream.match(tlvCommentMatch, false) && // not comment start
          stream.column() == state.tlvIndentationStyle.length * tlvIndentUnit; // at scope level
          if (beginStatement) {
            if (state.statementComment) {
              // statement already started by comment
              beginStatement = false;
            }
            state.statementComment = stream.match(tlvCommentMatch, false); // comment start
          }
        }
        var match;
        if (style !== undefined) {} else if (state.tlvInBlockComment) {
          // In a block comment.
          if (stream.match(/^.*?\*\//)) {
            // Exit block comment.
            state.tlvInBlockComment = false;
            if (tlvTrackStatements && !stream.eol()) {
              // Anything after comment is assumed to be real statement content.
              state.statementComment = false;
            }
          } else {
            stream.skipToEnd();
          }
          style = "comment";
        } else if ((match = stream.match(tlvCommentMatch)) && !state.tlvInBlockComment) {
          // Start comment.
          if (match[0] == "//") {
            // Line comment.
            stream.skipToEnd();
          } else {
            // Block comment.
            state.tlvInBlockComment = true;
          }
          style = "comment";
        } else if (match = stream.match(tlvIdentMatch)) {
          // looks like an identifier (or identifier prefix)
          var prefix = match[1];
          var mnemonic = match[2];
          if (
          // is identifier prefix
          tlvIdentifierStyle.hasOwnProperty(prefix) && (
          // has mnemonic or we're at the end of the line (maybe it hasn't been typed yet)
          mnemonic.length > 0 || stream.eol())) {
            style = tlvIdentifierStyle[prefix];
          } else {
            // Just swallow one character and try again.
            // This enables subsequent identifier match with preceding symbol character, which
            //   is legal within a statement.  (Eg, !$reset).  It also enables detection of
            //   comment start with preceding symbols.
            stream.backUp(stream.current().length - 1);
          }
        } else if (stream.match(/^\t+/)) {
          // Highlight tabs, which are illegal.
          style = "invalid";
        } else if (stream.match(/^[\[\]{}\(\);\:]+/)) {
          // [:], (), {}, ;.
          style = "meta";
        } else if (match = stream.match(/^[mM]4([\+_])?[\w\d_]*/)) {
          // m4 pre proc
          style = match[1] == "+" ? "keyword.special" : "keyword";
        } else if (stream.match(/^ +/)) {
          // Skip over spaces.
          if (stream.eol()) {
            // Trailing spaces.
            style = "error";
          }
        } else if (stream.match(/^[\w\d_]+/)) {
          // alpha-numeric token.
          style = "number";
        } else {
          // Eat the next char w/ no formatting.
          stream.next();
        }
      } else {
        if (stream.match(/^[mM]4([\w\d_]*)/)) {
          // m4 pre proc
          style = "keyword";
        }
      }
      return style;
    },
    indent: function (state) {
      return state.tlvCodeActive == true ? state.tlvNextIndent : -1;
    },
    startState: function (state) {
      state.tlvIndentationStyle = []; // Styles to use for each level of indentation.
      state.tlvCodeActive = true; // True when we're in a TLV region (and at beginning of file).
      state.tlvNextIndent = -1; // The number of spaces to autoindent the next line if tlvCodeActive.
      state.tlvInBlockComment = false; // True inside /**/ comment.
      if (tlvTrackStatements) {
        state.statementComment = false; // True inside a statement's header comment.
      }
    }
  }
});

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNTA1OC5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGNvZGVtaXJyb3IvbGVnYWN5LW1vZGVzL21vZGUvdmVyaWxvZy5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyJmdW5jdGlvbiBta1Zlcmlsb2cocGFyc2VyQ29uZmlnKSB7XG4gIHZhciBzdGF0ZW1lbnRJbmRlbnRVbml0ID0gcGFyc2VyQ29uZmlnLnN0YXRlbWVudEluZGVudFVuaXQsXG4gICAgZG9udEFsaWduQ2FsbHMgPSBwYXJzZXJDb25maWcuZG9udEFsaWduQ2FsbHMsXG4gICAgbm9JbmRlbnRLZXl3b3JkcyA9IHBhcnNlckNvbmZpZy5ub0luZGVudEtleXdvcmRzIHx8IFtdLFxuICAgIG11bHRpTGluZVN0cmluZ3MgPSBwYXJzZXJDb25maWcubXVsdGlMaW5lU3RyaW5ncyxcbiAgICBob29rcyA9IHBhcnNlckNvbmZpZy5ob29rcyB8fCB7fTtcbiAgZnVuY3Rpb24gd29yZHMoc3RyKSB7XG4gICAgdmFyIG9iaiA9IHt9LFxuICAgICAgd29yZHMgPSBzdHIuc3BsaXQoXCIgXCIpO1xuICAgIGZvciAodmFyIGkgPSAwOyBpIDwgd29yZHMubGVuZ3RoOyArK2kpIG9ialt3b3Jkc1tpXV0gPSB0cnVlO1xuICAgIHJldHVybiBvYmo7XG4gIH1cblxuICAvKipcbiAgICogS2V5d29yZHMgZnJvbSBJRUVFIDE4MDAtMjAxMlxuICAgKi9cbiAgdmFyIGtleXdvcmRzID0gd29yZHMoXCJhY2NlcHRfb24gYWxpYXMgYWx3YXlzIGFsd2F5c19jb21iIGFsd2F5c19mZiBhbHdheXNfbGF0Y2ggYW5kIGFzc2VydCBhc3NpZ24gYXNzdW1lIGF1dG9tYXRpYyBiZWZvcmUgYmVnaW4gYmluZCBcIiArIFwiYmlucyBiaW5zb2YgYml0IGJyZWFrIGJ1ZiBidWZpZjAgYnVmaWYxIGJ5dGUgY2FzZSBjYXNleCBjYXNleiBjZWxsIGNoYW5kbGUgY2hlY2tlciBjbGFzcyBjbG9ja2luZyBjbW9zIGNvbmZpZyBcIiArIFwiY29uc3QgY29uc3RyYWludCBjb250ZXh0IGNvbnRpbnVlIGNvdmVyIGNvdmVyZ3JvdXAgY292ZXJwb2ludCBjcm9zcyBkZWFzc2lnbiBkZWZhdWx0IGRlZnBhcmFtIGRlc2lnbiBkaXNhYmxlIFwiICsgXCJkaXN0IGRvIGVkZ2UgZWxzZSBlbmQgZW5kY2FzZSBlbmRjaGVja2VyIGVuZGNsYXNzIGVuZGNsb2NraW5nIGVuZGNvbmZpZyBlbmRmdW5jdGlvbiBlbmRnZW5lcmF0ZSBlbmRncm91cCBcIiArIFwiZW5kaW50ZXJmYWNlIGVuZG1vZHVsZSBlbmRwYWNrYWdlIGVuZHByaW1pdGl2ZSBlbmRwcm9ncmFtIGVuZHByb3BlcnR5IGVuZHNwZWNpZnkgZW5kc2VxdWVuY2UgZW5kdGFibGUgZW5kdGFzayBcIiArIFwiZW51bSBldmVudCBldmVudHVhbGx5IGV4cGVjdCBleHBvcnQgZXh0ZW5kcyBleHRlcm4gZmluYWwgZmlyc3RfbWF0Y2ggZm9yIGZvcmNlIGZvcmVhY2ggZm9yZXZlciBmb3JrIGZvcmtqb2luIFwiICsgXCJmdW5jdGlvbiBnZW5lcmF0ZSBnZW52YXIgZ2xvYmFsIGhpZ2h6MCBoaWdoejEgaWYgaWZmIGlmbm9uZSBpZ25vcmVfYmlucyBpbGxlZ2FsX2JpbnMgaW1wbGVtZW50cyBpbXBsaWVzIGltcG9ydCBcIiArIFwiaW5jZGlyIGluY2x1ZGUgaW5pdGlhbCBpbm91dCBpbnB1dCBpbnNpZGUgaW5zdGFuY2UgaW50IGludGVnZXIgaW50ZXJjb25uZWN0IGludGVyZmFjZSBpbnRlcnNlY3Qgam9pbiBqb2luX2FueSBcIiArIFwiam9pbl9ub25lIGxhcmdlIGxldCBsaWJsaXN0IGxpYnJhcnkgbG9jYWwgbG9jYWxwYXJhbSBsb2dpYyBsb25naW50IG1hY3JvbW9kdWxlIG1hdGNoZXMgbWVkaXVtIG1vZHBvcnQgbW9kdWxlIFwiICsgXCJuYW5kIG5lZ2VkZ2UgbmV0dHlwZSBuZXcgbmV4dHRpbWUgbm1vcyBub3Igbm9zaG93Y2FuY2VsbGVkIG5vdCBub3RpZjAgbm90aWYxIG51bGwgb3Igb3V0cHV0IHBhY2thZ2UgcGFja2VkIFwiICsgXCJwYXJhbWV0ZXIgcG1vcyBwb3NlZGdlIHByaW1pdGl2ZSBwcmlvcml0eSBwcm9ncmFtIHByb3BlcnR5IHByb3RlY3RlZCBwdWxsMCBwdWxsMSBwdWxsZG93biBwdWxsdXAgXCIgKyBcInB1bHNlc3R5bGVfb25kZXRlY3QgcHVsc2VzdHlsZV9vbmV2ZW50IHB1cmUgcmFuZCByYW5kYyByYW5kY2FzZSByYW5kc2VxdWVuY2UgcmNtb3MgcmVhbCByZWFsdGltZSByZWYgcmVnIFwiICsgXCJyZWplY3Rfb24gcmVsZWFzZSByZXBlYXQgcmVzdHJpY3QgcmV0dXJuIHJubW9zIHJwbW9zIHJ0cmFuIHJ0cmFuaWYwIHJ0cmFuaWYxIHNfYWx3YXlzIHNfZXZlbnR1YWxseSBzX25leHR0aW1lIFwiICsgXCJzX3VudGlsIHNfdW50aWxfd2l0aCBzY2FsYXJlZCBzZXF1ZW5jZSBzaG9ydGludCBzaG9ydHJlYWwgc2hvd2NhbmNlbGxlZCBzaWduZWQgc21hbGwgc29mdCBzb2x2ZSBzcGVjaWZ5IFwiICsgXCJzcGVjcGFyYW0gc3RhdGljIHN0cmluZyBzdHJvbmcgc3Ryb25nMCBzdHJvbmcxIHN0cnVjdCBzdXBlciBzdXBwbHkwIHN1cHBseTEgc3luY19hY2NlcHRfb24gc3luY19yZWplY3Rfb24gXCIgKyBcInRhYmxlIHRhZ2dlZCB0YXNrIHRoaXMgdGhyb3VnaG91dCB0aW1lIHRpbWVwcmVjaXNpb24gdGltZXVuaXQgdHJhbiB0cmFuaWYwIHRyYW5pZjEgdHJpIHRyaTAgdHJpMSB0cmlhbmQgdHJpb3IgXCIgKyBcInRyaXJlZyB0eXBlIHR5cGVkZWYgdW5pb24gdW5pcXVlIHVuaXF1ZTAgdW5zaWduZWQgdW50aWwgdW50aWxfd2l0aCB1bnR5cGVkIHVzZSB1d2lyZSB2YXIgdmVjdG9yZWQgdmlydHVhbCB2b2lkIFwiICsgXCJ3YWl0IHdhaXRfb3JkZXIgd2FuZCB3ZWFrIHdlYWswIHdlYWsxIHdoaWxlIHdpbGRjYXJkIHdpcmUgd2l0aCB3aXRoaW4gd29yIHhub3IgeG9yXCIpO1xuXG4gIC8qKiBPcGVyYXRvcnMgZnJvbSBJRUVFIDE4MDAtMjAxMlxuICAgICAgdW5hcnlfb3BlcmF0b3IgOjo9XG4gICAgICArIHwgLSB8ICEgfCB+IHwgJiB8IH4mIHwgfCB8IH58IHwgXiB8IH5eIHwgXn5cbiAgICAgIGJpbmFyeV9vcGVyYXRvciA6Oj1cbiAgICAgICsgfCAtIHwgKiB8IC8gfCAlIHwgPT0gfCAhPSB8ID09PSB8ICE9PSB8ID09PyB8ICE9PyB8ICYmIHwgfHwgfCAqKlxuICAgICAgfCA8IHwgPD0gfCA+IHwgPj0gfCAmIHwgfCB8IF4gfCBefiB8IH5eIHwgPj4gfCA8PCB8ID4+PiB8IDw8PFxuICAgICAgfCAtPiB8IDwtPlxuICAgICAgaW5jX29yX2RlY19vcGVyYXRvciA6Oj0gKysgfCAtLVxuICAgICAgdW5hcnlfbW9kdWxlX3BhdGhfb3BlcmF0b3IgOjo9XG4gICAgICAhIHwgfiB8ICYgfCB+JiB8IHwgfCB+fCB8IF4gfCB+XiB8IF5+XG4gICAgICBiaW5hcnlfbW9kdWxlX3BhdGhfb3BlcmF0b3IgOjo9XG4gICAgICA9PSB8ICE9IHwgJiYgfCB8fCB8ICYgfCB8IHwgXiB8IF5+IHwgfl5cbiAgKi9cbiAgdmFyIGlzT3BlcmF0b3JDaGFyID0gL1tcXCtcXC1cXCpcXC8hfiZ8XiU9PzpdLztcbiAgdmFyIGlzQnJhY2tldENoYXIgPSAvW1xcW1xcXXt9KCldLztcbiAgdmFyIHVuc2lnbmVkTnVtYmVyID0gL1xcZFswLTlfXSovO1xuICB2YXIgZGVjaW1hbExpdGVyYWwgPSAvXFxkKlxccyoncz9kXFxzKlxcZFswLTlfXSovaTtcbiAgdmFyIGJpbmFyeUxpdGVyYWwgPSAvXFxkKlxccyoncz9iXFxzKlt4ejAxXVt4ejAxX10qL2k7XG4gIHZhciBvY3RMaXRlcmFsID0gL1xcZCpcXHMqJ3M/b1xccypbeHowLTddW3h6MC03X10qL2k7XG4gIHZhciBoZXhMaXRlcmFsID0gL1xcZCpcXHMqJ3M/aFxccypbMC05YS1meHo/XVswLTlhLWZ4ej9fXSovaTtcbiAgdmFyIHJlYWxMaXRlcmFsID0gLyhcXGRbXFxkX10qKFxcLlxcZFtcXGRfXSopP0UtP1tcXGRfXSspfChcXGRbXFxkX10qXFwuXFxkW1xcZF9dKikvaTtcbiAgdmFyIGNsb3NpbmdCcmFja2V0T3JXb3JkID0gL14oKFxcdyspfFspfVxcXV0pLztcbiAgdmFyIGNsb3NpbmdCcmFja2V0ID0gL1spfVxcXV0vO1xuICB2YXIgY3VyUHVuYztcbiAgdmFyIGN1cktleXdvcmQ7XG5cbiAgLy8gQmxvY2sgb3BlbmluZ3Mgd2hpY2ggYXJlIGNsb3NlZCBieSBhIG1hdGNoaW5nIGtleXdvcmQgaW4gdGhlIGZvcm0gb2YgKFwiZW5kXCIgKyBrZXl3b3JkKVxuICAvLyBFLmcuIFwidGFza1wiID0+IFwiZW5kdGFza1wiXG4gIHZhciBibG9ja0tleXdvcmRzID0gd29yZHMoXCJjYXNlIGNoZWNrZXIgY2xhc3MgY2xvY2tpbmcgY29uZmlnIGZ1bmN0aW9uIGdlbmVyYXRlIGludGVyZmFjZSBtb2R1bGUgcGFja2FnZSBcIiArIFwicHJpbWl0aXZlIHByb2dyYW0gcHJvcGVydHkgc3BlY2lmeSBzZXF1ZW5jZSB0YWJsZSB0YXNrXCIpO1xuXG4gIC8vIE9wZW5pbmcvY2xvc2luZyBwYWlyc1xuICB2YXIgb3BlbkNsb3NlID0ge307XG4gIGZvciAodmFyIGtleXdvcmQgaW4gYmxvY2tLZXl3b3Jkcykge1xuICAgIG9wZW5DbG9zZVtrZXl3b3JkXSA9IFwiZW5kXCIgKyBrZXl3b3JkO1xuICB9XG4gIG9wZW5DbG9zZVtcImJlZ2luXCJdID0gXCJlbmRcIjtcbiAgb3BlbkNsb3NlW1wiY2FzZXhcIl0gPSBcImVuZGNhc2VcIjtcbiAgb3BlbkNsb3NlW1wiY2FzZXpcIl0gPSBcImVuZGNhc2VcIjtcbiAgb3BlbkNsb3NlW1wiZG9cIl0gPSBcIndoaWxlXCI7XG4gIG9wZW5DbG9zZVtcImZvcmtcIl0gPSBcImpvaW47am9pbl9hbnk7am9pbl9ub25lXCI7XG4gIG9wZW5DbG9zZVtcImNvdmVyZ3JvdXBcIl0gPSBcImVuZGdyb3VwXCI7XG4gIGZvciAodmFyIGkgaW4gbm9JbmRlbnRLZXl3b3Jkcykge1xuICAgIHZhciBrZXl3b3JkID0gbm9JbmRlbnRLZXl3b3Jkc1tpXTtcbiAgICBpZiAob3BlbkNsb3NlW2tleXdvcmRdKSB7XG4gICAgICBvcGVuQ2xvc2Vba2V5d29yZF0gPSB1bmRlZmluZWQ7XG4gICAgfVxuICB9XG5cbiAgLy8gS2V5d29yZHMgd2hpY2ggb3BlbiBzdGF0ZW1lbnRzIHRoYXQgYXJlIGVuZGVkIHdpdGggYSBzZW1pLWNvbG9uXG4gIHZhciBzdGF0ZW1lbnRLZXl3b3JkcyA9IHdvcmRzKFwiYWx3YXlzIGFsd2F5c19jb21iIGFsd2F5c19mZiBhbHdheXNfbGF0Y2ggYXNzZXJ0IGFzc2lnbiBhc3N1bWUgZWxzZSBleHBvcnQgZm9yIGZvcmVhY2ggZm9yZXZlciBpZiBpbXBvcnQgaW5pdGlhbCByZXBlYXQgd2hpbGVcIik7XG4gIGZ1bmN0aW9uIHRva2VuQmFzZShzdHJlYW0sIHN0YXRlKSB7XG4gICAgdmFyIGNoID0gc3RyZWFtLnBlZWsoKSxcbiAgICAgIHN0eWxlO1xuICAgIGlmIChob29rc1tjaF0gJiYgKHN0eWxlID0gaG9va3NbY2hdKHN0cmVhbSwgc3RhdGUpKSAhPSBmYWxzZSkgcmV0dXJuIHN0eWxlO1xuICAgIGlmIChob29rcy50b2tlbkJhc2UgJiYgKHN0eWxlID0gaG9va3MudG9rZW5CYXNlKHN0cmVhbSwgc3RhdGUpKSAhPSBmYWxzZSkgcmV0dXJuIHN0eWxlO1xuICAgIGlmICgvWyw7OlxcLl0vLnRlc3QoY2gpKSB7XG4gICAgICBjdXJQdW5jID0gc3RyZWFtLm5leHQoKTtcbiAgICAgIHJldHVybiBudWxsO1xuICAgIH1cbiAgICBpZiAoaXNCcmFja2V0Q2hhci50ZXN0KGNoKSkge1xuICAgICAgY3VyUHVuYyA9IHN0cmVhbS5uZXh0KCk7XG4gICAgICByZXR1cm4gXCJicmFja2V0XCI7XG4gICAgfVxuICAgIC8vIE1hY3JvcyAodGljay1kZWZpbmVzKVxuICAgIGlmIChjaCA9PSAnYCcpIHtcbiAgICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgICBpZiAoc3RyZWFtLmVhdFdoaWxlKC9bXFx3XFwkX10vKSkge1xuICAgICAgICByZXR1cm4gXCJkZWZcIjtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHJldHVybiBudWxsO1xuICAgICAgfVxuICAgIH1cbiAgICAvLyBTeXN0ZW0gY2FsbHNcbiAgICBpZiAoY2ggPT0gJyQnKSB7XG4gICAgICBzdHJlYW0ubmV4dCgpO1xuICAgICAgaWYgKHN0cmVhbS5lYXRXaGlsZSgvW1xcd1xcJF9dLykpIHtcbiAgICAgICAgcmV0dXJuIFwibWV0YVwiO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgcmV0dXJuIG51bGw7XG4gICAgICB9XG4gICAgfVxuICAgIC8vIFRpbWUgbGl0ZXJhbHNcbiAgICBpZiAoY2ggPT0gJyMnKSB7XG4gICAgICBzdHJlYW0ubmV4dCgpO1xuICAgICAgc3RyZWFtLmVhdFdoaWxlKC9bXFxkXy5dLyk7XG4gICAgICByZXR1cm4gXCJkZWZcIjtcbiAgICB9XG4gICAgLy8gU3RyaW5nc1xuICAgIGlmIChjaCA9PSAnXCInKSB7XG4gICAgICBzdHJlYW0ubmV4dCgpO1xuICAgICAgc3RhdGUudG9rZW5pemUgPSB0b2tlblN0cmluZyhjaCk7XG4gICAgICByZXR1cm4gc3RhdGUudG9rZW5pemUoc3RyZWFtLCBzdGF0ZSk7XG4gICAgfVxuICAgIC8vIENvbW1lbnRzXG4gICAgaWYgKGNoID09IFwiL1wiKSB7XG4gICAgICBzdHJlYW0ubmV4dCgpO1xuICAgICAgaWYgKHN0cmVhbS5lYXQoXCIqXCIpKSB7XG4gICAgICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5Db21tZW50O1xuICAgICAgICByZXR1cm4gdG9rZW5Db21tZW50KHN0cmVhbSwgc3RhdGUpO1xuICAgICAgfVxuICAgICAgaWYgKHN0cmVhbS5lYXQoXCIvXCIpKSB7XG4gICAgICAgIHN0cmVhbS5za2lwVG9FbmQoKTtcbiAgICAgICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICAgICAgfVxuICAgICAgc3RyZWFtLmJhY2tVcCgxKTtcbiAgICB9XG5cbiAgICAvLyBOdW1lcmljIGxpdGVyYWxzXG4gICAgaWYgKHN0cmVhbS5tYXRjaChyZWFsTGl0ZXJhbCkgfHwgc3RyZWFtLm1hdGNoKGRlY2ltYWxMaXRlcmFsKSB8fCBzdHJlYW0ubWF0Y2goYmluYXJ5TGl0ZXJhbCkgfHwgc3RyZWFtLm1hdGNoKG9jdExpdGVyYWwpIHx8IHN0cmVhbS5tYXRjaChoZXhMaXRlcmFsKSB8fCBzdHJlYW0ubWF0Y2godW5zaWduZWROdW1iZXIpIHx8IHN0cmVhbS5tYXRjaChyZWFsTGl0ZXJhbCkpIHtcbiAgICAgIHJldHVybiBcIm51bWJlclwiO1xuICAgIH1cblxuICAgIC8vIE9wZXJhdG9yc1xuICAgIGlmIChzdHJlYW0uZWF0V2hpbGUoaXNPcGVyYXRvckNoYXIpKSB7XG4gICAgICByZXR1cm4gXCJtZXRhXCI7XG4gICAgfVxuXG4gICAgLy8gS2V5d29yZHMgLyBwbGFpbiB2YXJpYWJsZXNcbiAgICBpZiAoc3RyZWFtLmVhdFdoaWxlKC9bXFx3XFwkX10vKSkge1xuICAgICAgdmFyIGN1ciA9IHN0cmVhbS5jdXJyZW50KCk7XG4gICAgICBpZiAoa2V5d29yZHNbY3VyXSkge1xuICAgICAgICBpZiAob3BlbkNsb3NlW2N1cl0pIHtcbiAgICAgICAgICBjdXJQdW5jID0gXCJuZXdibG9ja1wiO1xuICAgICAgICB9XG4gICAgICAgIGlmIChzdGF0ZW1lbnRLZXl3b3Jkc1tjdXJdKSB7XG4gICAgICAgICAgY3VyUHVuYyA9IFwibmV3c3RhdGVtZW50XCI7XG4gICAgICAgIH1cbiAgICAgICAgY3VyS2V5d29yZCA9IGN1cjtcbiAgICAgICAgcmV0dXJuIFwia2V5d29yZFwiO1xuICAgICAgfVxuICAgICAgcmV0dXJuIFwidmFyaWFibGVcIjtcbiAgICB9XG4gICAgc3RyZWFtLm5leHQoKTtcbiAgICByZXR1cm4gbnVsbDtcbiAgfVxuICBmdW5jdGlvbiB0b2tlblN0cmluZyhxdW90ZSkge1xuICAgIHJldHVybiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgICAgdmFyIGVzY2FwZWQgPSBmYWxzZSxcbiAgICAgICAgbmV4dCxcbiAgICAgICAgZW5kID0gZmFsc2U7XG4gICAgICB3aGlsZSAoKG5leHQgPSBzdHJlYW0ubmV4dCgpKSAhPSBudWxsKSB7XG4gICAgICAgIGlmIChuZXh0ID09IHF1b3RlICYmICFlc2NhcGVkKSB7XG4gICAgICAgICAgZW5kID0gdHJ1ZTtcbiAgICAgICAgICBicmVhaztcbiAgICAgICAgfVxuICAgICAgICBlc2NhcGVkID0gIWVzY2FwZWQgJiYgbmV4dCA9PSBcIlxcXFxcIjtcbiAgICAgIH1cbiAgICAgIGlmIChlbmQgfHwgIShlc2NhcGVkIHx8IG11bHRpTGluZVN0cmluZ3MpKSBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQmFzZTtcbiAgICAgIHJldHVybiBcInN0cmluZ1wiO1xuICAgIH07XG4gIH1cbiAgZnVuY3Rpb24gdG9rZW5Db21tZW50KHN0cmVhbSwgc3RhdGUpIHtcbiAgICB2YXIgbWF5YmVFbmQgPSBmYWxzZSxcbiAgICAgIGNoO1xuICAgIHdoaWxlIChjaCA9IHN0cmVhbS5uZXh0KCkpIHtcbiAgICAgIGlmIChjaCA9PSBcIi9cIiAmJiBtYXliZUVuZCkge1xuICAgICAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQmFzZTtcbiAgICAgICAgYnJlYWs7XG4gICAgICB9XG4gICAgICBtYXliZUVuZCA9IGNoID09IFwiKlwiO1xuICAgIH1cbiAgICByZXR1cm4gXCJjb21tZW50XCI7XG4gIH1cbiAgZnVuY3Rpb24gQ29udGV4dChpbmRlbnRlZCwgY29sdW1uLCB0eXBlLCBhbGlnbiwgcHJldikge1xuICAgIHRoaXMuaW5kZW50ZWQgPSBpbmRlbnRlZDtcbiAgICB0aGlzLmNvbHVtbiA9IGNvbHVtbjtcbiAgICB0aGlzLnR5cGUgPSB0eXBlO1xuICAgIHRoaXMuYWxpZ24gPSBhbGlnbjtcbiAgICB0aGlzLnByZXYgPSBwcmV2O1xuICB9XG4gIGZ1bmN0aW9uIHB1c2hDb250ZXh0KHN0YXRlLCBjb2wsIHR5cGUpIHtcbiAgICB2YXIgaW5kZW50ID0gc3RhdGUuaW5kZW50ZWQ7XG4gICAgdmFyIGMgPSBuZXcgQ29udGV4dChpbmRlbnQsIGNvbCwgdHlwZSwgbnVsbCwgc3RhdGUuY29udGV4dCk7XG4gICAgcmV0dXJuIHN0YXRlLmNvbnRleHQgPSBjO1xuICB9XG4gIGZ1bmN0aW9uIHBvcENvbnRleHQoc3RhdGUpIHtcbiAgICB2YXIgdCA9IHN0YXRlLmNvbnRleHQudHlwZTtcbiAgICBpZiAodCA9PSBcIilcIiB8fCB0ID09IFwiXVwiIHx8IHQgPT0gXCJ9XCIpIHtcbiAgICAgIHN0YXRlLmluZGVudGVkID0gc3RhdGUuY29udGV4dC5pbmRlbnRlZDtcbiAgICB9XG4gICAgcmV0dXJuIHN0YXRlLmNvbnRleHQgPSBzdGF0ZS5jb250ZXh0LnByZXY7XG4gIH1cbiAgZnVuY3Rpb24gaXNDbG9zaW5nKHRleHQsIGNvbnRleHRDbG9zaW5nKSB7XG4gICAgaWYgKHRleHQgPT0gY29udGV4dENsb3NpbmcpIHtcbiAgICAgIHJldHVybiB0cnVlO1xuICAgIH0gZWxzZSB7XG4gICAgICAvLyBjb250ZXh0Q2xvc2luZyBtYXkgYmUgbXVsdGlwbGUga2V5d29yZHMgc2VwYXJhdGVkIGJ5IDtcbiAgICAgIHZhciBjbG9zaW5nS2V5d29yZHMgPSBjb250ZXh0Q2xvc2luZy5zcGxpdChcIjtcIik7XG4gICAgICBmb3IgKHZhciBpIGluIGNsb3NpbmdLZXl3b3Jkcykge1xuICAgICAgICBpZiAodGV4dCA9PSBjbG9zaW5nS2V5d29yZHNbaV0pIHtcbiAgICAgICAgICByZXR1cm4gdHJ1ZTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgICAgcmV0dXJuIGZhbHNlO1xuICAgIH1cbiAgfVxuICBmdW5jdGlvbiBidWlsZEVsZWN0cmljSW5wdXRSZWdFeCgpIHtcbiAgICAvLyBSZWluZGVudGF0aW9uIHNob3VsZCBvY2N1ciBvbiBhbnkgYnJhY2tldCBjaGFyOiB7fSgpW11cbiAgICAvLyBvciBvbiBhIG1hdGNoIG9mIGFueSBvZiB0aGUgYmxvY2sgY2xvc2luZyBrZXl3b3JkcywgYXRcbiAgICAvLyB0aGUgZW5kIG9mIGEgbGluZVxuICAgIHZhciBhbGxDbG9zaW5ncyA9IFtdO1xuICAgIGZvciAodmFyIGkgaW4gb3BlbkNsb3NlKSB7XG4gICAgICBpZiAob3BlbkNsb3NlW2ldKSB7XG4gICAgICAgIHZhciBjbG9zaW5ncyA9IG9wZW5DbG9zZVtpXS5zcGxpdChcIjtcIik7XG4gICAgICAgIGZvciAodmFyIGogaW4gY2xvc2luZ3MpIHtcbiAgICAgICAgICBhbGxDbG9zaW5ncy5wdXNoKGNsb3NpbmdzW2pdKTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH1cbiAgICB2YXIgcmUgPSBuZXcgUmVnRXhwKFwiW3t9KClcXFxcW1xcXFxdXXwoXCIgKyBhbGxDbG9zaW5ncy5qb2luKFwifFwiKSArIFwiKSRcIik7XG4gICAgcmV0dXJuIHJlO1xuICB9XG5cbiAgLy8gSW50ZXJmYWNlXG4gIHJldHVybiB7XG4gICAgbmFtZTogXCJ2ZXJpbG9nXCIsXG4gICAgc3RhcnRTdGF0ZTogZnVuY3Rpb24gKGluZGVudFVuaXQpIHtcbiAgICAgIHZhciBzdGF0ZSA9IHtcbiAgICAgICAgdG9rZW5pemU6IG51bGwsXG4gICAgICAgIGNvbnRleHQ6IG5ldyBDb250ZXh0KC1pbmRlbnRVbml0LCAwLCBcInRvcFwiLCBmYWxzZSksXG4gICAgICAgIGluZGVudGVkOiAwLFxuICAgICAgICBzdGFydE9mTGluZTogdHJ1ZVxuICAgICAgfTtcbiAgICAgIGlmIChob29rcy5zdGFydFN0YXRlKSBob29rcy5zdGFydFN0YXRlKHN0YXRlKTtcbiAgICAgIHJldHVybiBzdGF0ZTtcbiAgICB9LFxuICAgIHRva2VuOiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgICAgdmFyIGN0eCA9IHN0YXRlLmNvbnRleHQ7XG4gICAgICBpZiAoc3RyZWFtLnNvbCgpKSB7XG4gICAgICAgIGlmIChjdHguYWxpZ24gPT0gbnVsbCkgY3R4LmFsaWduID0gZmFsc2U7XG4gICAgICAgIHN0YXRlLmluZGVudGVkID0gc3RyZWFtLmluZGVudGF0aW9uKCk7XG4gICAgICAgIHN0YXRlLnN0YXJ0T2ZMaW5lID0gdHJ1ZTtcbiAgICAgIH1cbiAgICAgIGlmIChob29rcy50b2tlbikge1xuICAgICAgICAvLyBDYWxsIGhvb2ssIHdpdGggYW4gb3B0aW9uYWwgcmV0dXJuIHZhbHVlIG9mIGEgc3R5bGUgdG8gb3ZlcnJpZGUgdmVyaWxvZyBzdHlsaW5nLlxuICAgICAgICB2YXIgc3R5bGUgPSBob29rcy50b2tlbihzdHJlYW0sIHN0YXRlKTtcbiAgICAgICAgaWYgKHN0eWxlICE9PSB1bmRlZmluZWQpIHtcbiAgICAgICAgICByZXR1cm4gc3R5bGU7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICAgIGlmIChzdHJlYW0uZWF0U3BhY2UoKSkgcmV0dXJuIG51bGw7XG4gICAgICBjdXJQdW5jID0gbnVsbDtcbiAgICAgIGN1cktleXdvcmQgPSBudWxsO1xuICAgICAgdmFyIHN0eWxlID0gKHN0YXRlLnRva2VuaXplIHx8IHRva2VuQmFzZSkoc3RyZWFtLCBzdGF0ZSk7XG4gICAgICBpZiAoc3R5bGUgPT0gXCJjb21tZW50XCIgfHwgc3R5bGUgPT0gXCJtZXRhXCIgfHwgc3R5bGUgPT0gXCJ2YXJpYWJsZVwiKSByZXR1cm4gc3R5bGU7XG4gICAgICBpZiAoY3R4LmFsaWduID09IG51bGwpIGN0eC5hbGlnbiA9IHRydWU7XG4gICAgICBpZiAoY3VyUHVuYyA9PSBjdHgudHlwZSkge1xuICAgICAgICBwb3BDb250ZXh0KHN0YXRlKTtcbiAgICAgIH0gZWxzZSBpZiAoY3VyUHVuYyA9PSBcIjtcIiAmJiBjdHgudHlwZSA9PSBcInN0YXRlbWVudFwiIHx8IGN0eC50eXBlICYmIGlzQ2xvc2luZyhjdXJLZXl3b3JkLCBjdHgudHlwZSkpIHtcbiAgICAgICAgY3R4ID0gcG9wQ29udGV4dChzdGF0ZSk7XG4gICAgICAgIHdoaWxlIChjdHggJiYgY3R4LnR5cGUgPT0gXCJzdGF0ZW1lbnRcIikgY3R4ID0gcG9wQ29udGV4dChzdGF0ZSk7XG4gICAgICB9IGVsc2UgaWYgKGN1clB1bmMgPT0gXCJ7XCIpIHtcbiAgICAgICAgcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbS5jb2x1bW4oKSwgXCJ9XCIpO1xuICAgICAgfSBlbHNlIGlmIChjdXJQdW5jID09IFwiW1wiKSB7XG4gICAgICAgIHB1c2hDb250ZXh0KHN0YXRlLCBzdHJlYW0uY29sdW1uKCksIFwiXVwiKTtcbiAgICAgIH0gZWxzZSBpZiAoY3VyUHVuYyA9PSBcIihcIikge1xuICAgICAgICBwdXNoQ29udGV4dChzdGF0ZSwgc3RyZWFtLmNvbHVtbigpLCBcIilcIik7XG4gICAgICB9IGVsc2UgaWYgKGN0eCAmJiBjdHgudHlwZSA9PSBcImVuZGNhc2VcIiAmJiBjdXJQdW5jID09IFwiOlwiKSB7XG4gICAgICAgIHB1c2hDb250ZXh0KHN0YXRlLCBzdHJlYW0uY29sdW1uKCksIFwic3RhdGVtZW50XCIpO1xuICAgICAgfSBlbHNlIGlmIChjdXJQdW5jID09IFwibmV3c3RhdGVtZW50XCIpIHtcbiAgICAgICAgcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbS5jb2x1bW4oKSwgXCJzdGF0ZW1lbnRcIik7XG4gICAgICB9IGVsc2UgaWYgKGN1clB1bmMgPT0gXCJuZXdibG9ja1wiKSB7XG4gICAgICAgIGlmIChjdXJLZXl3b3JkID09IFwiZnVuY3Rpb25cIiAmJiBjdHggJiYgKGN0eC50eXBlID09IFwic3RhdGVtZW50XCIgfHwgY3R4LnR5cGUgPT0gXCJlbmRncm91cFwiKSkge1xuICAgICAgICAgIC8vIFRoZSAnZnVuY3Rpb24nIGtleXdvcmQgY2FuIGFwcGVhciBpbiBzb21lIG90aGVyIGNvbnRleHRzIHdoZXJlIGl0IGFjdHVhbGx5IGRvZXMgbm90XG4gICAgICAgICAgLy8gaW5kaWNhdGUgYSBmdW5jdGlvbiAoaW1wb3J0L2V4cG9ydCBEUEkgYW5kIGNvdmVyZ3JvdXAgZGVmaW5pdGlvbnMpLlxuICAgICAgICAgIC8vIERvIG5vdGhpbmcgaW4gdGhpcyBjYXNlXG4gICAgICAgIH0gZWxzZSBpZiAoY3VyS2V5d29yZCA9PSBcInRhc2tcIiAmJiBjdHggJiYgY3R4LnR5cGUgPT0gXCJzdGF0ZW1lbnRcIikge1xuICAgICAgICAgIC8vIFNhbWUgdGhpbmcgZm9yIHRhc2tcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICB2YXIgY2xvc2UgPSBvcGVuQ2xvc2VbY3VyS2V5d29yZF07XG4gICAgICAgICAgcHVzaENvbnRleHQoc3RhdGUsIHN0cmVhbS5jb2x1bW4oKSwgY2xvc2UpO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgICBzdGF0ZS5zdGFydE9mTGluZSA9IGZhbHNlO1xuICAgICAgcmV0dXJuIHN0eWxlO1xuICAgIH0sXG4gICAgaW5kZW50OiBmdW5jdGlvbiAoc3RhdGUsIHRleHRBZnRlciwgY3gpIHtcbiAgICAgIGlmIChzdGF0ZS50b2tlbml6ZSAhPSB0b2tlbkJhc2UgJiYgc3RhdGUudG9rZW5pemUgIT0gbnVsbCkgcmV0dXJuIG51bGw7XG4gICAgICBpZiAoaG9va3MuaW5kZW50KSB7XG4gICAgICAgIHZhciBmcm9tSG9vayA9IGhvb2tzLmluZGVudChzdGF0ZSk7XG4gICAgICAgIGlmIChmcm9tSG9vayA+PSAwKSByZXR1cm4gZnJvbUhvb2s7XG4gICAgICB9XG4gICAgICB2YXIgY3R4ID0gc3RhdGUuY29udGV4dCxcbiAgICAgICAgZmlyc3RDaGFyID0gdGV4dEFmdGVyICYmIHRleHRBZnRlci5jaGFyQXQoMCk7XG4gICAgICBpZiAoY3R4LnR5cGUgPT0gXCJzdGF0ZW1lbnRcIiAmJiBmaXJzdENoYXIgPT0gXCJ9XCIpIGN0eCA9IGN0eC5wcmV2O1xuICAgICAgdmFyIGNsb3NpbmcgPSBmYWxzZTtcbiAgICAgIHZhciBwb3NzaWJsZUNsb3NpbmcgPSB0ZXh0QWZ0ZXIubWF0Y2goY2xvc2luZ0JyYWNrZXRPcldvcmQpO1xuICAgICAgaWYgKHBvc3NpYmxlQ2xvc2luZykgY2xvc2luZyA9IGlzQ2xvc2luZyhwb3NzaWJsZUNsb3NpbmdbMF0sIGN0eC50eXBlKTtcbiAgICAgIGlmIChjdHgudHlwZSA9PSBcInN0YXRlbWVudFwiKSByZXR1cm4gY3R4LmluZGVudGVkICsgKGZpcnN0Q2hhciA9PSBcIntcIiA/IDAgOiBzdGF0ZW1lbnRJbmRlbnRVbml0IHx8IGN4LnVuaXQpO2Vsc2UgaWYgKGNsb3NpbmdCcmFja2V0LnRlc3QoY3R4LnR5cGUpICYmIGN0eC5hbGlnbiAmJiAhZG9udEFsaWduQ2FsbHMpIHJldHVybiBjdHguY29sdW1uICsgKGNsb3NpbmcgPyAwIDogMSk7ZWxzZSBpZiAoY3R4LnR5cGUgPT0gXCIpXCIgJiYgIWNsb3NpbmcpIHJldHVybiBjdHguaW5kZW50ZWQgKyAoc3RhdGVtZW50SW5kZW50VW5pdCB8fCBjeC51bml0KTtlbHNlIHJldHVybiBjdHguaW5kZW50ZWQgKyAoY2xvc2luZyA/IDAgOiBjeC51bml0KTtcbiAgICB9LFxuICAgIGxhbmd1YWdlRGF0YToge1xuICAgICAgaW5kZW50T25JbnB1dDogYnVpbGRFbGVjdHJpY0lucHV0UmVnRXgoKSxcbiAgICAgIGNvbW1lbnRUb2tlbnM6IHtcbiAgICAgICAgbGluZTogXCIvL1wiLFxuICAgICAgICBibG9jazoge1xuICAgICAgICAgIG9wZW46IFwiLypcIixcbiAgICAgICAgICBjbG9zZTogXCIqL1wiXG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9XG4gIH07XG59XG47XG5leHBvcnQgY29uc3QgdmVyaWxvZyA9IG1rVmVyaWxvZyh7fSk7XG5cbi8vIFRMLVZlcmlsb2cgbW9kZS5cbi8vIFNlZSB0bC14Lm9yZyBmb3IgbGFuZ3VhZ2Ugc3BlYy5cbi8vIFNlZSB0aGUgbW9kZSBpbiBhY3Rpb24gYXQgbWFrZXJjaGlwLmNvbS5cbi8vIENvbnRhY3Q6IHN0ZXZlLmhvb3ZlckByZWR3b29kZWRhLmNvbVxuXG4vLyBUTFYgSWRlbnRpZmllciBwcmVmaXhlcy5cbi8vIE5vdGUgdGhhdCBzaWduIGlzIG5vdCB0cmVhdGVkIHNlcGFyYXRlbHksIHNvIFwiKy8tXCIgdmVyc2lvbnMgb2YgbnVtZXJpYyBpZGVudGlmaWVyc1xuLy8gYXJlIGluY2x1ZGVkLlxudmFyIHRsdklkZW50aWZpZXJTdHlsZSA9IHtcbiAgXCJ8XCI6IFwibGlua1wiLFxuICBcIj5cIjogXCJwcm9wZXJ0eVwiLFxuICAvLyBTaG91bGQgY29uZGl0aW9uIHRoaXMgb2ZmIGZvciA+IFRMViAxYy5cbiAgXCIkXCI6IFwidmFyaWFibGVcIixcbiAgXCIkJFwiOiBcInZhcmlhYmxlXCIsXG4gIFwiPyRcIjogXCJxdWFsaWZpZXJcIixcbiAgXCI/KlwiOiBcInF1YWxpZmllclwiLFxuICBcIi1cIjogXCJjb250ZW50U2VwYXJhdG9yXCIsXG4gIFwiL1wiOiBcInByb3BlcnR5XCIsXG4gIFwiLy1cIjogXCJwcm9wZXJ0eVwiLFxuICBcIkBcIjogXCJ2YXJpYWJsZU5hbWUuc3BlY2lhbFwiLFxuICBcIkAtXCI6IFwidmFyaWFibGVOYW1lLnNwZWNpYWxcIixcbiAgXCJAKytcIjogXCJ2YXJpYWJsZU5hbWUuc3BlY2lhbFwiLFxuICBcIkArPVwiOiBcInZhcmlhYmxlTmFtZS5zcGVjaWFsXCIsXG4gIFwiQCs9LVwiOiBcInZhcmlhYmxlTmFtZS5zcGVjaWFsXCIsXG4gIFwiQC0tXCI6IFwidmFyaWFibGVOYW1lLnNwZWNpYWxcIixcbiAgXCJALT1cIjogXCJ2YXJpYWJsZU5hbWUuc3BlY2lhbFwiLFxuICBcIiUrXCI6IFwidGFnXCIsXG4gIFwiJS1cIjogXCJ0YWdcIixcbiAgXCIlXCI6IFwidGFnXCIsXG4gIFwiPj5cIjogXCJ0YWdcIixcbiAgXCI8PFwiOiBcInRhZ1wiLFxuICBcIjw+XCI6IFwidGFnXCIsXG4gIFwiI1wiOiBcInRhZ1wiLFxuICAvLyBOZWVkIHRvIGNob29zZSBhIHN0eWxlIGZvciB0aGlzLlxuICBcIl5cIjogXCJhdHRyaWJ1dGVcIixcbiAgXCJeXlwiOiBcImF0dHJpYnV0ZVwiLFxuICBcIl4hXCI6IFwiYXR0cmlidXRlXCIsXG4gIFwiKlwiOiBcInZhcmlhYmxlXCIsXG4gIFwiKipcIjogXCJ2YXJpYWJsZVwiLFxuICBcIlxcXFxcIjogXCJrZXl3b3JkXCIsXG4gIFwiXFxcIlwiOiBcImNvbW1lbnRcIlxufTtcblxuLy8gTGluZXMgc3RhcnRpbmcgd2l0aCB0aGVzZSBjaGFyYWN0ZXJzIGRlZmluZSBzY29wZSAocmVzdWx0IGluIGluZGVudGF0aW9uKS5cbnZhciB0bHZTY29wZVByZWZpeENoYXJzID0ge1xuICBcIi9cIjogXCJiZWgtaGllclwiLFxuICBcIj5cIjogXCJiZWgtaGllclwiLFxuICBcIi1cIjogXCJwaHlzLWhpZXJcIixcbiAgXCJ8XCI6IFwicGlwZVwiLFxuICBcIj9cIjogXCJ3aGVuXCIsXG4gIFwiQFwiOiBcInN0YWdlXCIsXG4gIFwiXFxcXFwiOiBcImtleXdvcmRcIlxufTtcbnZhciB0bHZJbmRlbnRVbml0ID0gMztcbnZhciB0bHZUcmFja1N0YXRlbWVudHMgPSBmYWxzZTtcbnZhciB0bHZJZGVudE1hdGNoID0gL14oW34hQCNcXCQlXFxeJlxcKi1cXCs9XFw/XFwvXFxcXFxcfCdcIjw+XSspKFtcXGRcXHdfXSopLzsgLy8gTWF0Y2hlcyBhbiBpZGVudGlmaWVyLlxuLy8gTm90ZSB0aGF0ICc6JyBpcyBleGNsdWRlZCwgYmVjYXVzZSBvZiBpdCdzIHVzZSBpbiBbOl0uXG52YXIgdGx2TGluZUluZGVudGF0aW9uTWF0Y2ggPSAvXlshIF0gKi87XG52YXIgdGx2Q29tbWVudE1hdGNoID0gL15cXC9bXFwvXFwqXS87XG5leHBvcnQgY29uc3QgdGx2ID0gbWtWZXJpbG9nKHtcbiAgaG9va3M6IHtcbiAgICBlbGVjdHJpY0lucHV0OiBmYWxzZSxcbiAgICAvLyBSZXR1cm4gdW5kZWZpbmVkIGZvciB2ZXJpbG9nIHRva2VuaXppbmcsIG9yIHN0eWxlIGZvciBUTFYgdG9rZW4gKG51bGwgbm90IHVzZWQpLlxuICAgIC8vIFN0YW5kYXJkIENNIHN0eWxlcyBhcmUgdXNlZCBmb3IgbW9zdCBmb3JtYXR0aW5nLCBidXQgc29tZSBUTC1WZXJpbG9nLXNwZWNpZmljIGhpZ2hsaWdodGluZ1xuICAgIC8vIGNhbiBiZSBlbmFibGVkIHdpdGggdGhlIGRlZmluaXRpb24gb2YgY20tdGx2LSogc3R5bGVzLCBpbmNsdWRpbmcgaGlnaGxpZ2h0aW5nIGZvcjpcbiAgICAvLyAgIC0gTTQgdG9rZW5zXG4gICAgLy8gICAtIFRMViBzY29wZSBpbmRlbnRhdGlvblxuICAgIC8vICAgLSBTdGF0ZW1lbnQgZGVsaW1pdGF0aW9uIChlbmFibGVkIGJ5IHRsdlRyYWNrU3RhdGVtZW50cylcbiAgICB0b2tlbjogZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICAgIHZhciBzdHlsZSA9IHVuZGVmaW5lZDtcbiAgICAgIHZhciBtYXRjaDsgLy8gUmV0dXJuIHZhbHVlIG9mIHBhdHRlcm4gbWF0Y2hlcy5cblxuICAgICAgLy8gU2V0IGhpZ2hsaWdodGluZyBtb2RlIGJhc2VkIG9uIGNvZGUgcmVnaW9uIChUTFYgb3IgU1YpLlxuICAgICAgaWYgKHN0cmVhbS5zb2woKSAmJiAhc3RhdGUudGx2SW5CbG9ja0NvbW1lbnQpIHtcbiAgICAgICAgLy8gUHJvY2VzcyByZWdpb24uXG4gICAgICAgIGlmIChzdHJlYW0ucGVlaygpID09ICdcXFxcJykge1xuICAgICAgICAgIHN0eWxlID0gXCJkZWZcIjtcbiAgICAgICAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgICAgICAgaWYgKHN0cmVhbS5zdHJpbmcubWF0Y2goL1xcXFxTVi8pKSB7XG4gICAgICAgICAgICBzdGF0ZS50bHZDb2RlQWN0aXZlID0gZmFsc2U7XG4gICAgICAgICAgfSBlbHNlIGlmIChzdHJlYW0uc3RyaW5nLm1hdGNoKC9cXFxcVExWLykpIHtcbiAgICAgICAgICAgIHN0YXRlLnRsdkNvZGVBY3RpdmUgPSB0cnVlO1xuICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgICAvLyBDb3JyZWN0IGluZGVudGF0aW9uIGluIHRoZSBmYWNlIG9mIGEgbGluZSBwcmVmaXggY2hhci5cbiAgICAgICAgaWYgKHN0YXRlLnRsdkNvZGVBY3RpdmUgJiYgc3RyZWFtLnBvcyA9PSAwICYmIHN0YXRlLmluZGVudGVkID09IDAgJiYgKG1hdGNoID0gc3RyZWFtLm1hdGNoKHRsdkxpbmVJbmRlbnRhdGlvbk1hdGNoLCBmYWxzZSkpKSB7XG4gICAgICAgICAgc3RhdGUuaW5kZW50ZWQgPSBtYXRjaFswXS5sZW5ndGg7XG4gICAgICAgIH1cblxuICAgICAgICAvLyBDb21wdXRlIGluZGVudGF0aW9uIHN0YXRlOlxuICAgICAgICAvLyAgIG8gQXV0byBpbmRlbnRhdGlvbiBvbiBuZXh0IGxpbmVcbiAgICAgICAgLy8gICBvIEluZGVudGF0aW9uIHNjb3BlIHN0eWxlc1xuICAgICAgICB2YXIgaW5kZW50ZWQgPSBzdGF0ZS5pbmRlbnRlZDtcbiAgICAgICAgdmFyIGRlcHRoID0gaW5kZW50ZWQgLyB0bHZJbmRlbnRVbml0O1xuICAgICAgICBpZiAoZGVwdGggPD0gc3RhdGUudGx2SW5kZW50YXRpb25TdHlsZS5sZW5ndGgpIHtcbiAgICAgICAgICAvLyBub3QgZGVlcGVyIHRoYW4gY3VycmVudCBzY29wZVxuXG4gICAgICAgICAgdmFyIGJsYW5rbGluZSA9IHN0cmVhbS5zdHJpbmcubGVuZ3RoID09IGluZGVudGVkO1xuICAgICAgICAgIHZhciBjaFBvcyA9IGRlcHRoICogdGx2SW5kZW50VW5pdDtcbiAgICAgICAgICBpZiAoY2hQb3MgPCBzdHJlYW0uc3RyaW5nLmxlbmd0aCkge1xuICAgICAgICAgICAgdmFyIGJvZHlTdHJpbmcgPSBzdHJlYW0uc3RyaW5nLnNsaWNlKGNoUG9zKTtcbiAgICAgICAgICAgIHZhciBjaCA9IGJvZHlTdHJpbmdbMF07XG4gICAgICAgICAgICBpZiAodGx2U2NvcGVQcmVmaXhDaGFyc1tjaF0gJiYgKG1hdGNoID0gYm9keVN0cmluZy5tYXRjaCh0bHZJZGVudE1hdGNoKSkgJiYgdGx2SWRlbnRpZmllclN0eWxlW21hdGNoWzFdXSkge1xuICAgICAgICAgICAgICAvLyBUaGlzIGxpbmUgYmVnaW5zIHNjb3BlLlxuICAgICAgICAgICAgICAvLyBOZXh0IGxpbmUgZ2V0cyBpbmRlbnRlZCBvbmUgbGV2ZWwuXG4gICAgICAgICAgICAgIGluZGVudGVkICs9IHRsdkluZGVudFVuaXQ7XG4gICAgICAgICAgICAgIC8vIFN0eWxlIHRoZSBuZXh0IGxldmVsIG9mIGluZGVudGF0aW9uIChleGNlcHQgbm9uLXJlZ2lvbiBrZXl3b3JkIGlkZW50aWZpZXJzLFxuICAgICAgICAgICAgICAvLyAgIHdoaWNoIGFyZSBzdGF0ZW1lbnRzIHRoZW1zZWx2ZXMpXG4gICAgICAgICAgICAgIGlmICghKGNoID09IFwiXFxcXFwiICYmIGNoUG9zID4gMCkpIHtcbiAgICAgICAgICAgICAgICBzdGF0ZS50bHZJbmRlbnRhdGlvblN0eWxlW2RlcHRoXSA9IHRsdlNjb3BlUHJlZml4Q2hhcnNbY2hdO1xuICAgICAgICAgICAgICAgIGlmICh0bHZUcmFja1N0YXRlbWVudHMpIHtcbiAgICAgICAgICAgICAgICAgIHN0YXRlLnN0YXRlbWVudENvbW1lbnQgPSBmYWxzZTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgZGVwdGgrKztcbiAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfVxuICAgICAgICAgIH1cbiAgICAgICAgICAvLyBDbGVhciBvdXQgZGVlcGVyIGluZGVudGF0aW9uIGxldmVscyB1bmxlc3MgbGluZSBpcyBibGFuay5cbiAgICAgICAgICBpZiAoIWJsYW5rbGluZSkge1xuICAgICAgICAgICAgd2hpbGUgKHN0YXRlLnRsdkluZGVudGF0aW9uU3R5bGUubGVuZ3RoID4gZGVwdGgpIHtcbiAgICAgICAgICAgICAgc3RhdGUudGx2SW5kZW50YXRpb25TdHlsZS5wb3AoKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgICAgLy8gU2V0IG5leHQgbGV2ZWwgb2YgaW5kZW50YXRpb24uXG4gICAgICAgIHN0YXRlLnRsdk5leHRJbmRlbnQgPSBpbmRlbnRlZDtcbiAgICAgIH1cbiAgICAgIGlmIChzdGF0ZS50bHZDb2RlQWN0aXZlKSB7XG4gICAgICAgIC8vIEhpZ2hsaWdodCBhcyBUTFYuXG5cbiAgICAgICAgdmFyIGJlZ2luU3RhdGVtZW50ID0gZmFsc2U7XG4gICAgICAgIGlmICh0bHZUcmFja1N0YXRlbWVudHMpIHtcbiAgICAgICAgICAvLyBUaGlzIHN0YXJ0cyBhIHN0YXRlbWVudCBpZiB0aGUgcG9zaXRpb24gaXMgYXQgdGhlIHNjb3BlIGxldmVsXG4gICAgICAgICAgLy8gYW5kIHdlJ3JlIG5vdCB3aXRoaW4gYSBzdGF0ZW1lbnQgbGVhZGluZyBjb21tZW50LlxuICAgICAgICAgIGJlZ2luU3RhdGVtZW50ID0gc3RyZWFtLnBlZWsoKSAhPSBcIiBcIiAmJlxuICAgICAgICAgIC8vIG5vdCBhIHNwYWNlXG4gICAgICAgICAgc3R5bGUgPT09IHVuZGVmaW5lZCAmJlxuICAgICAgICAgIC8vIG5vdCBhIHJlZ2lvbiBpZGVudGlmaWVyXG4gICAgICAgICAgIXN0YXRlLnRsdkluQmxvY2tDb21tZW50ICYmXG4gICAgICAgICAgLy8gbm90IGluIGJsb2NrIGNvbW1lbnRcbiAgICAgICAgICAvLyFzdHJlYW0ubWF0Y2godGx2Q29tbWVudE1hdGNoLCBmYWxzZSkgJiYgLy8gbm90IGNvbW1lbnQgc3RhcnRcbiAgICAgICAgICBzdHJlYW0uY29sdW1uKCkgPT0gc3RhdGUudGx2SW5kZW50YXRpb25TdHlsZS5sZW5ndGggKiB0bHZJbmRlbnRVbml0OyAvLyBhdCBzY29wZSBsZXZlbFxuICAgICAgICAgIGlmIChiZWdpblN0YXRlbWVudCkge1xuICAgICAgICAgICAgaWYgKHN0YXRlLnN0YXRlbWVudENvbW1lbnQpIHtcbiAgICAgICAgICAgICAgLy8gc3RhdGVtZW50IGFscmVhZHkgc3RhcnRlZCBieSBjb21tZW50XG4gICAgICAgICAgICAgIGJlZ2luU3RhdGVtZW50ID0gZmFsc2U7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICBzdGF0ZS5zdGF0ZW1lbnRDb21tZW50ID0gc3RyZWFtLm1hdGNoKHRsdkNvbW1lbnRNYXRjaCwgZmFsc2UpOyAvLyBjb21tZW50IHN0YXJ0XG4gICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICAgIHZhciBtYXRjaDtcbiAgICAgICAgaWYgKHN0eWxlICE9PSB1bmRlZmluZWQpIHt9IGVsc2UgaWYgKHN0YXRlLnRsdkluQmxvY2tDb21tZW50KSB7XG4gICAgICAgICAgLy8gSW4gYSBibG9jayBjb21tZW50LlxuICAgICAgICAgIGlmIChzdHJlYW0ubWF0Y2goL14uKj9cXCpcXC8vKSkge1xuICAgICAgICAgICAgLy8gRXhpdCBibG9jayBjb21tZW50LlxuICAgICAgICAgICAgc3RhdGUudGx2SW5CbG9ja0NvbW1lbnQgPSBmYWxzZTtcbiAgICAgICAgICAgIGlmICh0bHZUcmFja1N0YXRlbWVudHMgJiYgIXN0cmVhbS5lb2woKSkge1xuICAgICAgICAgICAgICAvLyBBbnl0aGluZyBhZnRlciBjb21tZW50IGlzIGFzc3VtZWQgdG8gYmUgcmVhbCBzdGF0ZW1lbnQgY29udGVudC5cbiAgICAgICAgICAgICAgc3RhdGUuc3RhdGVtZW50Q29tbWVudCA9IGZhbHNlO1xuICAgICAgICAgICAgfVxuICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgICAgICAgfVxuICAgICAgICAgIHN0eWxlID0gXCJjb21tZW50XCI7XG4gICAgICAgIH0gZWxzZSBpZiAoKG1hdGNoID0gc3RyZWFtLm1hdGNoKHRsdkNvbW1lbnRNYXRjaCkpICYmICFzdGF0ZS50bHZJbkJsb2NrQ29tbWVudCkge1xuICAgICAgICAgIC8vIFN0YXJ0IGNvbW1lbnQuXG4gICAgICAgICAgaWYgKG1hdGNoWzBdID09IFwiLy9cIikge1xuICAgICAgICAgICAgLy8gTGluZSBjb21tZW50LlxuICAgICAgICAgICAgc3RyZWFtLnNraXBUb0VuZCgpO1xuICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAvLyBCbG9jayBjb21tZW50LlxuICAgICAgICAgICAgc3RhdGUudGx2SW5CbG9ja0NvbW1lbnQgPSB0cnVlO1xuICAgICAgICAgIH1cbiAgICAgICAgICBzdHlsZSA9IFwiY29tbWVudFwiO1xuICAgICAgICB9IGVsc2UgaWYgKG1hdGNoID0gc3RyZWFtLm1hdGNoKHRsdklkZW50TWF0Y2gpKSB7XG4gICAgICAgICAgLy8gbG9va3MgbGlrZSBhbiBpZGVudGlmaWVyIChvciBpZGVudGlmaWVyIHByZWZpeClcbiAgICAgICAgICB2YXIgcHJlZml4ID0gbWF0Y2hbMV07XG4gICAgICAgICAgdmFyIG1uZW1vbmljID0gbWF0Y2hbMl07XG4gICAgICAgICAgaWYgKFxuICAgICAgICAgIC8vIGlzIGlkZW50aWZpZXIgcHJlZml4XG4gICAgICAgICAgdGx2SWRlbnRpZmllclN0eWxlLmhhc093blByb3BlcnR5KHByZWZpeCkgJiYgKFxuICAgICAgICAgIC8vIGhhcyBtbmVtb25pYyBvciB3ZSdyZSBhdCB0aGUgZW5kIG9mIHRoZSBsaW5lIChtYXliZSBpdCBoYXNuJ3QgYmVlbiB0eXBlZCB5ZXQpXG4gICAgICAgICAgbW5lbW9uaWMubGVuZ3RoID4gMCB8fCBzdHJlYW0uZW9sKCkpKSB7XG4gICAgICAgICAgICBzdHlsZSA9IHRsdklkZW50aWZpZXJTdHlsZVtwcmVmaXhdO1xuICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAvLyBKdXN0IHN3YWxsb3cgb25lIGNoYXJhY3RlciBhbmQgdHJ5IGFnYWluLlxuICAgICAgICAgICAgLy8gVGhpcyBlbmFibGVzIHN1YnNlcXVlbnQgaWRlbnRpZmllciBtYXRjaCB3aXRoIHByZWNlZGluZyBzeW1ib2wgY2hhcmFjdGVyLCB3aGljaFxuICAgICAgICAgICAgLy8gICBpcyBsZWdhbCB3aXRoaW4gYSBzdGF0ZW1lbnQuICAoRWcsICEkcmVzZXQpLiAgSXQgYWxzbyBlbmFibGVzIGRldGVjdGlvbiBvZlxuICAgICAgICAgICAgLy8gICBjb21tZW50IHN0YXJ0IHdpdGggcHJlY2VkaW5nIHN5bWJvbHMuXG4gICAgICAgICAgICBzdHJlYW0uYmFja1VwKHN0cmVhbS5jdXJyZW50KCkubGVuZ3RoIC0gMSk7XG4gICAgICAgICAgfVxuICAgICAgICB9IGVsc2UgaWYgKHN0cmVhbS5tYXRjaCgvXlxcdCsvKSkge1xuICAgICAgICAgIC8vIEhpZ2hsaWdodCB0YWJzLCB3aGljaCBhcmUgaWxsZWdhbC5cbiAgICAgICAgICBzdHlsZSA9IFwiaW52YWxpZFwiO1xuICAgICAgICB9IGVsc2UgaWYgKHN0cmVhbS5tYXRjaCgvXltcXFtcXF17fVxcKFxcKTtcXDpdKy8pKSB7XG4gICAgICAgICAgLy8gWzpdLCAoKSwge30sIDsuXG4gICAgICAgICAgc3R5bGUgPSBcIm1ldGFcIjtcbiAgICAgICAgfSBlbHNlIGlmIChtYXRjaCA9IHN0cmVhbS5tYXRjaCgvXlttTV00KFtcXCtfXSk/W1xcd1xcZF9dKi8pKSB7XG4gICAgICAgICAgLy8gbTQgcHJlIHByb2NcbiAgICAgICAgICBzdHlsZSA9IG1hdGNoWzFdID09IFwiK1wiID8gXCJrZXl3b3JkLnNwZWNpYWxcIiA6IFwia2V5d29yZFwiO1xuICAgICAgICB9IGVsc2UgaWYgKHN0cmVhbS5tYXRjaCgvXiArLykpIHtcbiAgICAgICAgICAvLyBTa2lwIG92ZXIgc3BhY2VzLlxuICAgICAgICAgIGlmIChzdHJlYW0uZW9sKCkpIHtcbiAgICAgICAgICAgIC8vIFRyYWlsaW5nIHNwYWNlcy5cbiAgICAgICAgICAgIHN0eWxlID0gXCJlcnJvclwiO1xuICAgICAgICAgIH1cbiAgICAgICAgfSBlbHNlIGlmIChzdHJlYW0ubWF0Y2goL15bXFx3XFxkX10rLykpIHtcbiAgICAgICAgICAvLyBhbHBoYS1udW1lcmljIHRva2VuLlxuICAgICAgICAgIHN0eWxlID0gXCJudW1iZXJcIjtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAvLyBFYXQgdGhlIG5leHQgY2hhciB3LyBubyBmb3JtYXR0aW5nLlxuICAgICAgICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgICAgIH1cbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIGlmIChzdHJlYW0ubWF0Y2goL15bbU1dNChbXFx3XFxkX10qKS8pKSB7XG4gICAgICAgICAgLy8gbTQgcHJlIHByb2NcbiAgICAgICAgICBzdHlsZSA9IFwia2V5d29yZFwiO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgICByZXR1cm4gc3R5bGU7XG4gICAgfSxcbiAgICBpbmRlbnQ6IGZ1bmN0aW9uIChzdGF0ZSkge1xuICAgICAgcmV0dXJuIHN0YXRlLnRsdkNvZGVBY3RpdmUgPT0gdHJ1ZSA/IHN0YXRlLnRsdk5leHRJbmRlbnQgOiAtMTtcbiAgICB9LFxuICAgIHN0YXJ0U3RhdGU6IGZ1bmN0aW9uIChzdGF0ZSkge1xuICAgICAgc3RhdGUudGx2SW5kZW50YXRpb25TdHlsZSA9IFtdOyAvLyBTdHlsZXMgdG8gdXNlIGZvciBlYWNoIGxldmVsIG9mIGluZGVudGF0aW9uLlxuICAgICAgc3RhdGUudGx2Q29kZUFjdGl2ZSA9IHRydWU7IC8vIFRydWUgd2hlbiB3ZSdyZSBpbiBhIFRMViByZWdpb24gKGFuZCBhdCBiZWdpbm5pbmcgb2YgZmlsZSkuXG4gICAgICBzdGF0ZS50bHZOZXh0SW5kZW50ID0gLTE7IC8vIFRoZSBudW1iZXIgb2Ygc3BhY2VzIHRvIGF1dG9pbmRlbnQgdGhlIG5leHQgbGluZSBpZiB0bHZDb2RlQWN0aXZlLlxuICAgICAgc3RhdGUudGx2SW5CbG9ja0NvbW1lbnQgPSBmYWxzZTsgLy8gVHJ1ZSBpbnNpZGUgLyoqLyBjb21tZW50LlxuICAgICAgaWYgKHRsdlRyYWNrU3RhdGVtZW50cykge1xuICAgICAgICBzdGF0ZS5zdGF0ZW1lbnRDb21tZW50ID0gZmFsc2U7IC8vIFRydWUgaW5zaWRlIGEgc3RhdGVtZW50J3MgaGVhZGVyIGNvbW1lbnQuXG4gICAgICB9XG4gICAgfVxuICB9XG59KTsiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=