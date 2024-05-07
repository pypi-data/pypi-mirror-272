"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[3415],{

/***/ 73415:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "erlang": () => (/* binding */ erlang)
/* harmony export */ });
/////////////////////////////////////////////////////////////////////////////
// constants

var typeWords = ["-type", "-spec", "-export_type", "-opaque"];
var keywordWords = ["after", "begin", "catch", "case", "cond", "end", "fun", "if", "let", "of", "query", "receive", "try", "when"];
var separatorRE = /[\->,;]/;
var separatorWords = ["->", ";", ","];
var operatorAtomWords = ["and", "andalso", "band", "bnot", "bor", "bsl", "bsr", "bxor", "div", "not", "or", "orelse", "rem", "xor"];
var operatorSymbolRE = /[\+\-\*\/<>=\|:!]/;
var operatorSymbolWords = ["=", "+", "-", "*", "/", ">", ">=", "<", "=<", "=:=", "==", "=/=", "/=", "||", "<-", "!"];
var openParenRE = /[<\(\[\{]/;
var openParenWords = ["<<", "(", "[", "{"];
var closeParenRE = /[>\)\]\}]/;
var closeParenWords = ["}", "]", ")", ">>"];
var guardWords = ["is_atom", "is_binary", "is_bitstring", "is_boolean", "is_float", "is_function", "is_integer", "is_list", "is_number", "is_pid", "is_port", "is_record", "is_reference", "is_tuple", "atom", "binary", "bitstring", "boolean", "function", "integer", "list", "number", "pid", "port", "record", "reference", "tuple"];
var bifWords = ["abs", "adler32", "adler32_combine", "alive", "apply", "atom_to_binary", "atom_to_list", "binary_to_atom", "binary_to_existing_atom", "binary_to_list", "binary_to_term", "bit_size", "bitstring_to_list", "byte_size", "check_process_code", "contact_binary", "crc32", "crc32_combine", "date", "decode_packet", "delete_module", "disconnect_node", "element", "erase", "exit", "float", "float_to_list", "garbage_collect", "get", "get_keys", "group_leader", "halt", "hd", "integer_to_list", "internal_bif", "iolist_size", "iolist_to_binary", "is_alive", "is_atom", "is_binary", "is_bitstring", "is_boolean", "is_float", "is_function", "is_integer", "is_list", "is_number", "is_pid", "is_port", "is_process_alive", "is_record", "is_reference", "is_tuple", "length", "link", "list_to_atom", "list_to_binary", "list_to_bitstring", "list_to_existing_atom", "list_to_float", "list_to_integer", "list_to_pid", "list_to_tuple", "load_module", "make_ref", "module_loaded", "monitor_node", "node", "node_link", "node_unlink", "nodes", "notalive", "now", "open_port", "pid_to_list", "port_close", "port_command", "port_connect", "port_control", "pre_loaded", "process_flag", "process_info", "processes", "purge_module", "put", "register", "registered", "round", "self", "setelement", "size", "spawn", "spawn_link", "spawn_monitor", "spawn_opt", "split_binary", "statistics", "term_to_binary", "time", "throw", "tl", "trunc", "tuple_size", "tuple_to_list", "unlink", "unregister", "whereis"];

// upper case: [A-Z] [Ø-Þ] [À-Ö]
// lower case: [a-z] [ß-ö] [ø-ÿ]
var anumRE = /[\w@Ø-ÞÀ-Öß-öø-ÿ]/;
var escapesRE = /[0-7]{1,3}|[bdefnrstv\\"']|\^[a-zA-Z]|x[0-9a-zA-Z]{2}|x{[0-9a-zA-Z]+}/;

/////////////////////////////////////////////////////////////////////////////
// tokenizer

function tokenizer(stream, state) {
  // in multi-line string
  if (state.in_string) {
    state.in_string = !doubleQuote(stream);
    return rval(state, stream, "string");
  }

  // in multi-line atom
  if (state.in_atom) {
    state.in_atom = !singleQuote(stream);
    return rval(state, stream, "atom");
  }

  // whitespace
  if (stream.eatSpace()) {
    return rval(state, stream, "whitespace");
  }

  // attributes and type specs
  if (!peekToken(state) && stream.match(/-\s*[a-zß-öø-ÿ][\wØ-ÞÀ-Öß-öø-ÿ]*/)) {
    if (is_member(stream.current(), typeWords)) {
      return rval(state, stream, "type");
    } else {
      return rval(state, stream, "attribute");
    }
  }
  var ch = stream.next();

  // comment
  if (ch == '%') {
    stream.skipToEnd();
    return rval(state, stream, "comment");
  }

  // colon
  if (ch == ":") {
    return rval(state, stream, "colon");
  }

  // macro
  if (ch == '?') {
    stream.eatSpace();
    stream.eatWhile(anumRE);
    return rval(state, stream, "macro");
  }

  // record
  if (ch == "#") {
    stream.eatSpace();
    stream.eatWhile(anumRE);
    return rval(state, stream, "record");
  }

  // dollar escape
  if (ch == "$") {
    if (stream.next() == "\\" && !stream.match(escapesRE)) {
      return rval(state, stream, "error");
    }
    return rval(state, stream, "number");
  }

  // dot
  if (ch == ".") {
    return rval(state, stream, "dot");
  }

  // quoted atom
  if (ch == '\'') {
    if (!(state.in_atom = !singleQuote(stream))) {
      if (stream.match(/\s*\/\s*[0-9]/, false)) {
        stream.match(/\s*\/\s*[0-9]/, true);
        return rval(state, stream, "fun"); // 'f'/0 style fun
      }
      if (stream.match(/\s*\(/, false) || stream.match(/\s*:/, false)) {
        return rval(state, stream, "function");
      }
    }
    return rval(state, stream, "atom");
  }

  // string
  if (ch == '"') {
    state.in_string = !doubleQuote(stream);
    return rval(state, stream, "string");
  }

  // variable
  if (/[A-Z_Ø-ÞÀ-Ö]/.test(ch)) {
    stream.eatWhile(anumRE);
    return rval(state, stream, "variable");
  }

  // atom/keyword/BIF/function
  if (/[a-z_ß-öø-ÿ]/.test(ch)) {
    stream.eatWhile(anumRE);
    if (stream.match(/\s*\/\s*[0-9]/, false)) {
      stream.match(/\s*\/\s*[0-9]/, true);
      return rval(state, stream, "fun"); // f/0 style fun
    }
    var w = stream.current();
    if (is_member(w, keywordWords)) {
      return rval(state, stream, "keyword");
    } else if (is_member(w, operatorAtomWords)) {
      return rval(state, stream, "operator");
    } else if (stream.match(/\s*\(/, false)) {
      // 'put' and 'erlang:put' are bifs, 'foo:put' is not
      if (is_member(w, bifWords) && (peekToken(state).token != ":" || peekToken(state, 2).token == "erlang")) {
        return rval(state, stream, "builtin");
      } else if (is_member(w, guardWords)) {
        return rval(state, stream, "guard");
      } else {
        return rval(state, stream, "function");
      }
    } else if (lookahead(stream) == ":") {
      if (w == "erlang") {
        return rval(state, stream, "builtin");
      } else {
        return rval(state, stream, "function");
      }
    } else if (is_member(w, ["true", "false"])) {
      return rval(state, stream, "boolean");
    } else {
      return rval(state, stream, "atom");
    }
  }

  // number
  var digitRE = /[0-9]/;
  var radixRE = /[0-9a-zA-Z]/; // 36#zZ style int
  if (digitRE.test(ch)) {
    stream.eatWhile(digitRE);
    if (stream.eat('#')) {
      // 36#aZ  style integer
      if (!stream.eatWhile(radixRE)) {
        stream.backUp(1); //"36#" - syntax error
      }
    } else if (stream.eat('.')) {
      // float
      if (!stream.eatWhile(digitRE)) {
        stream.backUp(1); // "3." - probably end of function
      } else {
        if (stream.eat(/[eE]/)) {
          // float with exponent
          if (stream.eat(/[-+]/)) {
            if (!stream.eatWhile(digitRE)) {
              stream.backUp(2); // "2e-" - syntax error
            }
          } else {
            if (!stream.eatWhile(digitRE)) {
              stream.backUp(1); // "2e" - syntax error
            }
          }
        }
      }
    }
    return rval(state, stream, "number"); // normal integer
  }

  // open parens
  if (nongreedy(stream, openParenRE, openParenWords)) {
    return rval(state, stream, "open_paren");
  }

  // close parens
  if (nongreedy(stream, closeParenRE, closeParenWords)) {
    return rval(state, stream, "close_paren");
  }

  // separators
  if (greedy(stream, separatorRE, separatorWords)) {
    return rval(state, stream, "separator");
  }

  // operators
  if (greedy(stream, operatorSymbolRE, operatorSymbolWords)) {
    return rval(state, stream, "operator");
  }
  return rval(state, stream, null);
}

/////////////////////////////////////////////////////////////////////////////
// utilities
function nongreedy(stream, re, words) {
  if (stream.current().length == 1 && re.test(stream.current())) {
    stream.backUp(1);
    while (re.test(stream.peek())) {
      stream.next();
      if (is_member(stream.current(), words)) {
        return true;
      }
    }
    stream.backUp(stream.current().length - 1);
  }
  return false;
}
function greedy(stream, re, words) {
  if (stream.current().length == 1 && re.test(stream.current())) {
    while (re.test(stream.peek())) {
      stream.next();
    }
    while (0 < stream.current().length) {
      if (is_member(stream.current(), words)) {
        return true;
      } else {
        stream.backUp(1);
      }
    }
    stream.next();
  }
  return false;
}
function doubleQuote(stream) {
  return quote(stream, '"', '\\');
}
function singleQuote(stream) {
  return quote(stream, '\'', '\\');
}
function quote(stream, quoteChar, escapeChar) {
  while (!stream.eol()) {
    var ch = stream.next();
    if (ch == quoteChar) {
      return true;
    } else if (ch == escapeChar) {
      stream.next();
    }
  }
  return false;
}
function lookahead(stream) {
  var m = stream.match(/^\s*([^\s%])/, false);
  return m ? m[1] : "";
}
function is_member(element, list) {
  return -1 < list.indexOf(element);
}
function rval(state, stream, type) {
  // parse stack
  pushToken(state, realToken(type, stream));

  // map erlang token type to CodeMirror style class
  //     erlang             -> CodeMirror tag
  switch (type) {
    case "atom":
      return "atom";
    case "attribute":
      return "attribute";
    case "boolean":
      return "atom";
    case "builtin":
      return "builtin";
    case "close_paren":
      return null;
    case "colon":
      return null;
    case "comment":
      return "comment";
    case "dot":
      return null;
    case "error":
      return "error";
    case "fun":
      return "meta";
    case "function":
      return "tag";
    case "guard":
      return "property";
    case "keyword":
      return "keyword";
    case "macro":
      return "macroName";
    case "number":
      return "number";
    case "open_paren":
      return null;
    case "operator":
      return "operator";
    case "record":
      return "bracket";
    case "separator":
      return null;
    case "string":
      return "string";
    case "type":
      return "def";
    case "variable":
      return "variable";
    default:
      return null;
  }
}
function aToken(tok, col, ind, typ) {
  return {
    token: tok,
    column: col,
    indent: ind,
    type: typ
  };
}
function realToken(type, stream) {
  return aToken(stream.current(), stream.column(), stream.indentation(), type);
}
function fakeToken(type) {
  return aToken(type, 0, 0, type);
}
function peekToken(state, depth) {
  var len = state.tokenStack.length;
  var dep = depth ? depth : 1;
  if (len < dep) {
    return false;
  } else {
    return state.tokenStack[len - dep];
  }
}
function pushToken(state, token) {
  if (!(token.type == "comment" || token.type == "whitespace")) {
    state.tokenStack = maybe_drop_pre(state.tokenStack, token);
    state.tokenStack = maybe_drop_post(state.tokenStack);
  }
}
function maybe_drop_pre(s, token) {
  var last = s.length - 1;
  if (0 < last && s[last].type === "record" && token.type === "dot") {
    s.pop();
  } else if (0 < last && s[last].type === "group") {
    s.pop();
    s.push(token);
  } else {
    s.push(token);
  }
  return s;
}
function maybe_drop_post(s) {
  if (!s.length) return s;
  var last = s.length - 1;
  if (s[last].type === "dot") {
    return [];
  }
  if (last > 1 && s[last].type === "fun" && s[last - 1].token === "fun") {
    return s.slice(0, last - 1);
  }
  switch (s[last].token) {
    case "}":
      return d(s, {
        g: ["{"]
      });
    case "]":
      return d(s, {
        i: ["["]
      });
    case ")":
      return d(s, {
        i: ["("]
      });
    case ">>":
      return d(s, {
        i: ["<<"]
      });
    case "end":
      return d(s, {
        i: ["begin", "case", "fun", "if", "receive", "try"]
      });
    case ",":
      return d(s, {
        e: ["begin", "try", "when", "->", ",", "(", "[", "{", "<<"]
      });
    case "->":
      return d(s, {
        r: ["when"],
        m: ["try", "if", "case", "receive"]
      });
    case ";":
      return d(s, {
        E: ["case", "fun", "if", "receive", "try", "when"]
      });
    case "catch":
      return d(s, {
        e: ["try"]
      });
    case "of":
      return d(s, {
        e: ["case"]
      });
    case "after":
      return d(s, {
        e: ["receive", "try"]
      });
    default:
      return s;
  }
}
function d(stack, tt) {
  // stack is a stack of Token objects.
  // tt is an object; {type:tokens}
  // type is a char, tokens is a list of token strings.
  // The function returns (possibly truncated) stack.
  // It will descend the stack, looking for a Token such that Token.token
  //  is a member of tokens. If it does not find that, it will normally (but
  //  see "E" below) return stack. If it does find a match, it will remove
  //  all the Tokens between the top and the matched Token.
  // If type is "m", that is all it does.
  // If type is "i", it will also remove the matched Token and the top Token.
  // If type is "g", like "i", but add a fake "group" token at the top.
  // If type is "r", it will remove the matched Token, but not the top Token.
  // If type is "e", it will keep the matched Token but not the top Token.
  // If type is "E", it behaves as for type "e", except if there is no match,
  //  in which case it will return an empty stack.

  for (var type in tt) {
    var len = stack.length - 1;
    var tokens = tt[type];
    for (var i = len - 1; -1 < i; i--) {
      if (is_member(stack[i].token, tokens)) {
        var ss = stack.slice(0, i);
        switch (type) {
          case "m":
            return ss.concat(stack[i]).concat(stack[len]);
          case "r":
            return ss.concat(stack[len]);
          case "i":
            return ss;
          case "g":
            return ss.concat(fakeToken("group"));
          case "E":
            return ss.concat(stack[i]);
          case "e":
            return ss.concat(stack[i]);
        }
      }
    }
  }
  return type == "E" ? [] : stack;
}

/////////////////////////////////////////////////////////////////////////////
// indenter

function indenter(state, textAfter, cx) {
  var t;
  var wordAfter = wordafter(textAfter);
  var currT = peekToken(state, 1);
  var prevT = peekToken(state, 2);
  if (state.in_string || state.in_atom) {
    return null;
  } else if (!prevT) {
    return 0;
  } else if (currT.token == "when") {
    return currT.column + cx.unit;
  } else if (wordAfter === "when" && prevT.type === "function") {
    return prevT.indent + cx.unit;
  } else if (wordAfter === "(" && currT.token === "fun") {
    return currT.column + 3;
  } else if (wordAfter === "catch" && (t = getToken(state, ["try"]))) {
    return t.column;
  } else if (is_member(wordAfter, ["end", "after", "of"])) {
    t = getToken(state, ["begin", "case", "fun", "if", "receive", "try"]);
    return t ? t.column : null;
  } else if (is_member(wordAfter, closeParenWords)) {
    t = getToken(state, openParenWords);
    return t ? t.column : null;
  } else if (is_member(currT.token, [",", "|", "||"]) || is_member(wordAfter, [",", "|", "||"])) {
    t = postcommaToken(state);
    return t ? t.column + t.token.length : cx.unit;
  } else if (currT.token == "->") {
    if (is_member(prevT.token, ["receive", "case", "if", "try"])) {
      return prevT.column + cx.unit + cx.unit;
    } else {
      return prevT.column + cx.unit;
    }
  } else if (is_member(currT.token, openParenWords)) {
    return currT.column + currT.token.length;
  } else {
    t = defaultToken(state);
    return truthy(t) ? t.column + cx.unit : 0;
  }
}
function wordafter(str) {
  var m = str.match(/,|[a-z]+|\}|\]|\)|>>|\|+|\(/);
  return truthy(m) && m.index === 0 ? m[0] : "";
}
function postcommaToken(state) {
  var objs = state.tokenStack.slice(0, -1);
  var i = getTokenIndex(objs, "type", ["open_paren"]);
  return truthy(objs[i]) ? objs[i] : false;
}
function defaultToken(state) {
  var objs = state.tokenStack;
  var stop = getTokenIndex(objs, "type", ["open_paren", "separator", "keyword"]);
  var oper = getTokenIndex(objs, "type", ["operator"]);
  if (truthy(stop) && truthy(oper) && stop < oper) {
    return objs[stop + 1];
  } else if (truthy(stop)) {
    return objs[stop];
  } else {
    return false;
  }
}
function getToken(state, tokens) {
  var objs = state.tokenStack;
  var i = getTokenIndex(objs, "token", tokens);
  return truthy(objs[i]) ? objs[i] : false;
}
function getTokenIndex(objs, propname, propvals) {
  for (var i = objs.length - 1; -1 < i; i--) {
    if (is_member(objs[i][propname], propvals)) {
      return i;
    }
  }
  return false;
}
function truthy(x) {
  return x !== false && x != null;
}

/////////////////////////////////////////////////////////////////////////////
// this object defines the mode

const erlang = {
  name: "erlang",
  startState() {
    return {
      tokenStack: [],
      in_string: false,
      in_atom: false
    };
  },
  token: tokenizer,
  indent: indenter,
  languageData: {
    commentTokens: {
      line: "%"
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiMzQxNS5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9AY29kZW1pcnJvci9sZWdhY3ktbW9kZXMvbW9kZS9lcmxhbmcuanMiXSwic291cmNlc0NvbnRlbnQiOlsiLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy9cbi8vIGNvbnN0YW50c1xuXG52YXIgdHlwZVdvcmRzID0gW1wiLXR5cGVcIiwgXCItc3BlY1wiLCBcIi1leHBvcnRfdHlwZVwiLCBcIi1vcGFxdWVcIl07XG52YXIga2V5d29yZFdvcmRzID0gW1wiYWZ0ZXJcIiwgXCJiZWdpblwiLCBcImNhdGNoXCIsIFwiY2FzZVwiLCBcImNvbmRcIiwgXCJlbmRcIiwgXCJmdW5cIiwgXCJpZlwiLCBcImxldFwiLCBcIm9mXCIsIFwicXVlcnlcIiwgXCJyZWNlaXZlXCIsIFwidHJ5XCIsIFwid2hlblwiXTtcbnZhciBzZXBhcmF0b3JSRSA9IC9bXFwtPiw7XS87XG52YXIgc2VwYXJhdG9yV29yZHMgPSBbXCItPlwiLCBcIjtcIiwgXCIsXCJdO1xudmFyIG9wZXJhdG9yQXRvbVdvcmRzID0gW1wiYW5kXCIsIFwiYW5kYWxzb1wiLCBcImJhbmRcIiwgXCJibm90XCIsIFwiYm9yXCIsIFwiYnNsXCIsIFwiYnNyXCIsIFwiYnhvclwiLCBcImRpdlwiLCBcIm5vdFwiLCBcIm9yXCIsIFwib3JlbHNlXCIsIFwicmVtXCIsIFwieG9yXCJdO1xudmFyIG9wZXJhdG9yU3ltYm9sUkUgPSAvW1xcK1xcLVxcKlxcLzw+PVxcfDohXS87XG52YXIgb3BlcmF0b3JTeW1ib2xXb3JkcyA9IFtcIj1cIiwgXCIrXCIsIFwiLVwiLCBcIipcIiwgXCIvXCIsIFwiPlwiLCBcIj49XCIsIFwiPFwiLCBcIj08XCIsIFwiPTo9XCIsIFwiPT1cIiwgXCI9Lz1cIiwgXCIvPVwiLCBcInx8XCIsIFwiPC1cIiwgXCIhXCJdO1xudmFyIG9wZW5QYXJlblJFID0gL1s8XFwoXFxbXFx7XS87XG52YXIgb3BlblBhcmVuV29yZHMgPSBbXCI8PFwiLCBcIihcIiwgXCJbXCIsIFwie1wiXTtcbnZhciBjbG9zZVBhcmVuUkUgPSAvWz5cXClcXF1cXH1dLztcbnZhciBjbG9zZVBhcmVuV29yZHMgPSBbXCJ9XCIsIFwiXVwiLCBcIilcIiwgXCI+PlwiXTtcbnZhciBndWFyZFdvcmRzID0gW1wiaXNfYXRvbVwiLCBcImlzX2JpbmFyeVwiLCBcImlzX2JpdHN0cmluZ1wiLCBcImlzX2Jvb2xlYW5cIiwgXCJpc19mbG9hdFwiLCBcImlzX2Z1bmN0aW9uXCIsIFwiaXNfaW50ZWdlclwiLCBcImlzX2xpc3RcIiwgXCJpc19udW1iZXJcIiwgXCJpc19waWRcIiwgXCJpc19wb3J0XCIsIFwiaXNfcmVjb3JkXCIsIFwiaXNfcmVmZXJlbmNlXCIsIFwiaXNfdHVwbGVcIiwgXCJhdG9tXCIsIFwiYmluYXJ5XCIsIFwiYml0c3RyaW5nXCIsIFwiYm9vbGVhblwiLCBcImZ1bmN0aW9uXCIsIFwiaW50ZWdlclwiLCBcImxpc3RcIiwgXCJudW1iZXJcIiwgXCJwaWRcIiwgXCJwb3J0XCIsIFwicmVjb3JkXCIsIFwicmVmZXJlbmNlXCIsIFwidHVwbGVcIl07XG52YXIgYmlmV29yZHMgPSBbXCJhYnNcIiwgXCJhZGxlcjMyXCIsIFwiYWRsZXIzMl9jb21iaW5lXCIsIFwiYWxpdmVcIiwgXCJhcHBseVwiLCBcImF0b21fdG9fYmluYXJ5XCIsIFwiYXRvbV90b19saXN0XCIsIFwiYmluYXJ5X3RvX2F0b21cIiwgXCJiaW5hcnlfdG9fZXhpc3RpbmdfYXRvbVwiLCBcImJpbmFyeV90b19saXN0XCIsIFwiYmluYXJ5X3RvX3Rlcm1cIiwgXCJiaXRfc2l6ZVwiLCBcImJpdHN0cmluZ190b19saXN0XCIsIFwiYnl0ZV9zaXplXCIsIFwiY2hlY2tfcHJvY2Vzc19jb2RlXCIsIFwiY29udGFjdF9iaW5hcnlcIiwgXCJjcmMzMlwiLCBcImNyYzMyX2NvbWJpbmVcIiwgXCJkYXRlXCIsIFwiZGVjb2RlX3BhY2tldFwiLCBcImRlbGV0ZV9tb2R1bGVcIiwgXCJkaXNjb25uZWN0X25vZGVcIiwgXCJlbGVtZW50XCIsIFwiZXJhc2VcIiwgXCJleGl0XCIsIFwiZmxvYXRcIiwgXCJmbG9hdF90b19saXN0XCIsIFwiZ2FyYmFnZV9jb2xsZWN0XCIsIFwiZ2V0XCIsIFwiZ2V0X2tleXNcIiwgXCJncm91cF9sZWFkZXJcIiwgXCJoYWx0XCIsIFwiaGRcIiwgXCJpbnRlZ2VyX3RvX2xpc3RcIiwgXCJpbnRlcm5hbF9iaWZcIiwgXCJpb2xpc3Rfc2l6ZVwiLCBcImlvbGlzdF90b19iaW5hcnlcIiwgXCJpc19hbGl2ZVwiLCBcImlzX2F0b21cIiwgXCJpc19iaW5hcnlcIiwgXCJpc19iaXRzdHJpbmdcIiwgXCJpc19ib29sZWFuXCIsIFwiaXNfZmxvYXRcIiwgXCJpc19mdW5jdGlvblwiLCBcImlzX2ludGVnZXJcIiwgXCJpc19saXN0XCIsIFwiaXNfbnVtYmVyXCIsIFwiaXNfcGlkXCIsIFwiaXNfcG9ydFwiLCBcImlzX3Byb2Nlc3NfYWxpdmVcIiwgXCJpc19yZWNvcmRcIiwgXCJpc19yZWZlcmVuY2VcIiwgXCJpc190dXBsZVwiLCBcImxlbmd0aFwiLCBcImxpbmtcIiwgXCJsaXN0X3RvX2F0b21cIiwgXCJsaXN0X3RvX2JpbmFyeVwiLCBcImxpc3RfdG9fYml0c3RyaW5nXCIsIFwibGlzdF90b19leGlzdGluZ19hdG9tXCIsIFwibGlzdF90b19mbG9hdFwiLCBcImxpc3RfdG9faW50ZWdlclwiLCBcImxpc3RfdG9fcGlkXCIsIFwibGlzdF90b190dXBsZVwiLCBcImxvYWRfbW9kdWxlXCIsIFwibWFrZV9yZWZcIiwgXCJtb2R1bGVfbG9hZGVkXCIsIFwibW9uaXRvcl9ub2RlXCIsIFwibm9kZVwiLCBcIm5vZGVfbGlua1wiLCBcIm5vZGVfdW5saW5rXCIsIFwibm9kZXNcIiwgXCJub3RhbGl2ZVwiLCBcIm5vd1wiLCBcIm9wZW5fcG9ydFwiLCBcInBpZF90b19saXN0XCIsIFwicG9ydF9jbG9zZVwiLCBcInBvcnRfY29tbWFuZFwiLCBcInBvcnRfY29ubmVjdFwiLCBcInBvcnRfY29udHJvbFwiLCBcInByZV9sb2FkZWRcIiwgXCJwcm9jZXNzX2ZsYWdcIiwgXCJwcm9jZXNzX2luZm9cIiwgXCJwcm9jZXNzZXNcIiwgXCJwdXJnZV9tb2R1bGVcIiwgXCJwdXRcIiwgXCJyZWdpc3RlclwiLCBcInJlZ2lzdGVyZWRcIiwgXCJyb3VuZFwiLCBcInNlbGZcIiwgXCJzZXRlbGVtZW50XCIsIFwic2l6ZVwiLCBcInNwYXduXCIsIFwic3Bhd25fbGlua1wiLCBcInNwYXduX21vbml0b3JcIiwgXCJzcGF3bl9vcHRcIiwgXCJzcGxpdF9iaW5hcnlcIiwgXCJzdGF0aXN0aWNzXCIsIFwidGVybV90b19iaW5hcnlcIiwgXCJ0aW1lXCIsIFwidGhyb3dcIiwgXCJ0bFwiLCBcInRydW5jXCIsIFwidHVwbGVfc2l6ZVwiLCBcInR1cGxlX3RvX2xpc3RcIiwgXCJ1bmxpbmtcIiwgXCJ1bnJlZ2lzdGVyXCIsIFwid2hlcmVpc1wiXTtcblxuLy8gdXBwZXIgY2FzZTogW0EtWl0gW8OYLcOeXSBbw4Atw5ZdXG4vLyBsb3dlciBjYXNlOiBbYS16XSBbw58tw7ZdIFvDuC3Dv11cbnZhciBhbnVtUkUgPSAvW1xcd0DDmC3DnsOALcOWw58tw7bDuC3Dv10vO1xudmFyIGVzY2FwZXNSRSA9IC9bMC03XXsxLDN9fFtiZGVmbnJzdHZcXFxcXCInXXxcXF5bYS16QS1aXXx4WzAtOWEtekEtWl17Mn18eHtbMC05YS16QS1aXSt9LztcblxuLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy9cbi8vIHRva2VuaXplclxuXG5mdW5jdGlvbiB0b2tlbml6ZXIoc3RyZWFtLCBzdGF0ZSkge1xuICAvLyBpbiBtdWx0aS1saW5lIHN0cmluZ1xuICBpZiAoc3RhdGUuaW5fc3RyaW5nKSB7XG4gICAgc3RhdGUuaW5fc3RyaW5nID0gIWRvdWJsZVF1b3RlKHN0cmVhbSk7XG4gICAgcmV0dXJuIHJ2YWwoc3RhdGUsIHN0cmVhbSwgXCJzdHJpbmdcIik7XG4gIH1cblxuICAvLyBpbiBtdWx0aS1saW5lIGF0b21cbiAgaWYgKHN0YXRlLmluX2F0b20pIHtcbiAgICBzdGF0ZS5pbl9hdG9tID0gIXNpbmdsZVF1b3RlKHN0cmVhbSk7XG4gICAgcmV0dXJuIHJ2YWwoc3RhdGUsIHN0cmVhbSwgXCJhdG9tXCIpO1xuICB9XG5cbiAgLy8gd2hpdGVzcGFjZVxuICBpZiAoc3RyZWFtLmVhdFNwYWNlKCkpIHtcbiAgICByZXR1cm4gcnZhbChzdGF0ZSwgc3RyZWFtLCBcIndoaXRlc3BhY2VcIik7XG4gIH1cblxuICAvLyBhdHRyaWJ1dGVzIGFuZCB0eXBlIHNwZWNzXG4gIGlmICghcGVla1Rva2VuKHN0YXRlKSAmJiBzdHJlYW0ubWF0Y2goLy1cXHMqW2EtesOfLcO2w7gtw79dW1xcd8OYLcOew4Atw5bDny3DtsO4LcO/XSovKSkge1xuICAgIGlmIChpc19tZW1iZXIoc3RyZWFtLmN1cnJlbnQoKSwgdHlwZVdvcmRzKSkge1xuICAgICAgcmV0dXJuIHJ2YWwoc3RhdGUsIHN0cmVhbSwgXCJ0eXBlXCIpO1xuICAgIH0gZWxzZSB7XG4gICAgICByZXR1cm4gcnZhbChzdGF0ZSwgc3RyZWFtLCBcImF0dHJpYnV0ZVwiKTtcbiAgICB9XG4gIH1cbiAgdmFyIGNoID0gc3RyZWFtLm5leHQoKTtcblxuICAvLyBjb21tZW50XG4gIGlmIChjaCA9PSAnJScpIHtcbiAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgcmV0dXJuIHJ2YWwoc3RhdGUsIHN0cmVhbSwgXCJjb21tZW50XCIpO1xuICB9XG5cbiAgLy8gY29sb25cbiAgaWYgKGNoID09IFwiOlwiKSB7XG4gICAgcmV0dXJuIHJ2YWwoc3RhdGUsIHN0cmVhbSwgXCJjb2xvblwiKTtcbiAgfVxuXG4gIC8vIG1hY3JvXG4gIGlmIChjaCA9PSAnPycpIHtcbiAgICBzdHJlYW0uZWF0U3BhY2UoKTtcbiAgICBzdHJlYW0uZWF0V2hpbGUoYW51bVJFKTtcbiAgICByZXR1cm4gcnZhbChzdGF0ZSwgc3RyZWFtLCBcIm1hY3JvXCIpO1xuICB9XG5cbiAgLy8gcmVjb3JkXG4gIGlmIChjaCA9PSBcIiNcIikge1xuICAgIHN0cmVhbS5lYXRTcGFjZSgpO1xuICAgIHN0cmVhbS5lYXRXaGlsZShhbnVtUkUpO1xuICAgIHJldHVybiBydmFsKHN0YXRlLCBzdHJlYW0sIFwicmVjb3JkXCIpO1xuICB9XG5cbiAgLy8gZG9sbGFyIGVzY2FwZVxuICBpZiAoY2ggPT0gXCIkXCIpIHtcbiAgICBpZiAoc3RyZWFtLm5leHQoKSA9PSBcIlxcXFxcIiAmJiAhc3RyZWFtLm1hdGNoKGVzY2FwZXNSRSkpIHtcbiAgICAgIHJldHVybiBydmFsKHN0YXRlLCBzdHJlYW0sIFwiZXJyb3JcIik7XG4gICAgfVxuICAgIHJldHVybiBydmFsKHN0YXRlLCBzdHJlYW0sIFwibnVtYmVyXCIpO1xuICB9XG5cbiAgLy8gZG90XG4gIGlmIChjaCA9PSBcIi5cIikge1xuICAgIHJldHVybiBydmFsKHN0YXRlLCBzdHJlYW0sIFwiZG90XCIpO1xuICB9XG5cbiAgLy8gcXVvdGVkIGF0b21cbiAgaWYgKGNoID09ICdcXCcnKSB7XG4gICAgaWYgKCEoc3RhdGUuaW5fYXRvbSA9ICFzaW5nbGVRdW90ZShzdHJlYW0pKSkge1xuICAgICAgaWYgKHN0cmVhbS5tYXRjaCgvXFxzKlxcL1xccypbMC05XS8sIGZhbHNlKSkge1xuICAgICAgICBzdHJlYW0ubWF0Y2goL1xccypcXC9cXHMqWzAtOV0vLCB0cnVlKTtcbiAgICAgICAgcmV0dXJuIHJ2YWwoc3RhdGUsIHN0cmVhbSwgXCJmdW5cIik7IC8vICdmJy8wIHN0eWxlIGZ1blxuICAgICAgfVxuICAgICAgaWYgKHN0cmVhbS5tYXRjaCgvXFxzKlxcKC8sIGZhbHNlKSB8fCBzdHJlYW0ubWF0Y2goL1xccyo6LywgZmFsc2UpKSB7XG4gICAgICAgIHJldHVybiBydmFsKHN0YXRlLCBzdHJlYW0sIFwiZnVuY3Rpb25cIik7XG4gICAgICB9XG4gICAgfVxuICAgIHJldHVybiBydmFsKHN0YXRlLCBzdHJlYW0sIFwiYXRvbVwiKTtcbiAgfVxuXG4gIC8vIHN0cmluZ1xuICBpZiAoY2ggPT0gJ1wiJykge1xuICAgIHN0YXRlLmluX3N0cmluZyA9ICFkb3VibGVRdW90ZShzdHJlYW0pO1xuICAgIHJldHVybiBydmFsKHN0YXRlLCBzdHJlYW0sIFwic3RyaW5nXCIpO1xuICB9XG5cbiAgLy8gdmFyaWFibGVcbiAgaWYgKC9bQS1aX8OYLcOew4Atw5ZdLy50ZXN0KGNoKSkge1xuICAgIHN0cmVhbS5lYXRXaGlsZShhbnVtUkUpO1xuICAgIHJldHVybiBydmFsKHN0YXRlLCBzdHJlYW0sIFwidmFyaWFibGVcIik7XG4gIH1cblxuICAvLyBhdG9tL2tleXdvcmQvQklGL2Z1bmN0aW9uXG4gIGlmICgvW2Etel/Dny3DtsO4LcO/XS8udGVzdChjaCkpIHtcbiAgICBzdHJlYW0uZWF0V2hpbGUoYW51bVJFKTtcbiAgICBpZiAoc3RyZWFtLm1hdGNoKC9cXHMqXFwvXFxzKlswLTldLywgZmFsc2UpKSB7XG4gICAgICBzdHJlYW0ubWF0Y2goL1xccypcXC9cXHMqWzAtOV0vLCB0cnVlKTtcbiAgICAgIHJldHVybiBydmFsKHN0YXRlLCBzdHJlYW0sIFwiZnVuXCIpOyAvLyBmLzAgc3R5bGUgZnVuXG4gICAgfVxuICAgIHZhciB3ID0gc3RyZWFtLmN1cnJlbnQoKTtcbiAgICBpZiAoaXNfbWVtYmVyKHcsIGtleXdvcmRXb3JkcykpIHtcbiAgICAgIHJldHVybiBydmFsKHN0YXRlLCBzdHJlYW0sIFwia2V5d29yZFwiKTtcbiAgICB9IGVsc2UgaWYgKGlzX21lbWJlcih3LCBvcGVyYXRvckF0b21Xb3JkcykpIHtcbiAgICAgIHJldHVybiBydmFsKHN0YXRlLCBzdHJlYW0sIFwib3BlcmF0b3JcIik7XG4gICAgfSBlbHNlIGlmIChzdHJlYW0ubWF0Y2goL1xccypcXCgvLCBmYWxzZSkpIHtcbiAgICAgIC8vICdwdXQnIGFuZCAnZXJsYW5nOnB1dCcgYXJlIGJpZnMsICdmb286cHV0JyBpcyBub3RcbiAgICAgIGlmIChpc19tZW1iZXIodywgYmlmV29yZHMpICYmIChwZWVrVG9rZW4oc3RhdGUpLnRva2VuICE9IFwiOlwiIHx8IHBlZWtUb2tlbihzdGF0ZSwgMikudG9rZW4gPT0gXCJlcmxhbmdcIikpIHtcbiAgICAgICAgcmV0dXJuIHJ2YWwoc3RhdGUsIHN0cmVhbSwgXCJidWlsdGluXCIpO1xuICAgICAgfSBlbHNlIGlmIChpc19tZW1iZXIodywgZ3VhcmRXb3JkcykpIHtcbiAgICAgICAgcmV0dXJuIHJ2YWwoc3RhdGUsIHN0cmVhbSwgXCJndWFyZFwiKTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHJldHVybiBydmFsKHN0YXRlLCBzdHJlYW0sIFwiZnVuY3Rpb25cIik7XG4gICAgICB9XG4gICAgfSBlbHNlIGlmIChsb29rYWhlYWQoc3RyZWFtKSA9PSBcIjpcIikge1xuICAgICAgaWYgKHcgPT0gXCJlcmxhbmdcIikge1xuICAgICAgICByZXR1cm4gcnZhbChzdGF0ZSwgc3RyZWFtLCBcImJ1aWx0aW5cIik7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICByZXR1cm4gcnZhbChzdGF0ZSwgc3RyZWFtLCBcImZ1bmN0aW9uXCIpO1xuICAgICAgfVxuICAgIH0gZWxzZSBpZiAoaXNfbWVtYmVyKHcsIFtcInRydWVcIiwgXCJmYWxzZVwiXSkpIHtcbiAgICAgIHJldHVybiBydmFsKHN0YXRlLCBzdHJlYW0sIFwiYm9vbGVhblwiKTtcbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIHJ2YWwoc3RhdGUsIHN0cmVhbSwgXCJhdG9tXCIpO1xuICAgIH1cbiAgfVxuXG4gIC8vIG51bWJlclxuICB2YXIgZGlnaXRSRSA9IC9bMC05XS87XG4gIHZhciByYWRpeFJFID0gL1swLTlhLXpBLVpdLzsgLy8gMzYjelogc3R5bGUgaW50XG4gIGlmIChkaWdpdFJFLnRlc3QoY2gpKSB7XG4gICAgc3RyZWFtLmVhdFdoaWxlKGRpZ2l0UkUpO1xuICAgIGlmIChzdHJlYW0uZWF0KCcjJykpIHtcbiAgICAgIC8vIDM2I2FaICBzdHlsZSBpbnRlZ2VyXG4gICAgICBpZiAoIXN0cmVhbS5lYXRXaGlsZShyYWRpeFJFKSkge1xuICAgICAgICBzdHJlYW0uYmFja1VwKDEpOyAvL1wiMzYjXCIgLSBzeW50YXggZXJyb3JcbiAgICAgIH1cbiAgICB9IGVsc2UgaWYgKHN0cmVhbS5lYXQoJy4nKSkge1xuICAgICAgLy8gZmxvYXRcbiAgICAgIGlmICghc3RyZWFtLmVhdFdoaWxlKGRpZ2l0UkUpKSB7XG4gICAgICAgIHN0cmVhbS5iYWNrVXAoMSk7IC8vIFwiMy5cIiAtIHByb2JhYmx5IGVuZCBvZiBmdW5jdGlvblxuICAgICAgfSBlbHNlIHtcbiAgICAgICAgaWYgKHN0cmVhbS5lYXQoL1tlRV0vKSkge1xuICAgICAgICAgIC8vIGZsb2F0IHdpdGggZXhwb25lbnRcbiAgICAgICAgICBpZiAoc3RyZWFtLmVhdCgvWy0rXS8pKSB7XG4gICAgICAgICAgICBpZiAoIXN0cmVhbS5lYXRXaGlsZShkaWdpdFJFKSkge1xuICAgICAgICAgICAgICBzdHJlYW0uYmFja1VwKDIpOyAvLyBcIjJlLVwiIC0gc3ludGF4IGVycm9yXG4gICAgICAgICAgICB9XG4gICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIGlmICghc3RyZWFtLmVhdFdoaWxlKGRpZ2l0UkUpKSB7XG4gICAgICAgICAgICAgIHN0cmVhbS5iYWNrVXAoMSk7IC8vIFwiMmVcIiAtIHN5bnRheCBlcnJvclxuICAgICAgICAgICAgfVxuICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgfVxuICAgIH1cbiAgICByZXR1cm4gcnZhbChzdGF0ZSwgc3RyZWFtLCBcIm51bWJlclwiKTsgLy8gbm9ybWFsIGludGVnZXJcbiAgfVxuXG4gIC8vIG9wZW4gcGFyZW5zXG4gIGlmIChub25ncmVlZHkoc3RyZWFtLCBvcGVuUGFyZW5SRSwgb3BlblBhcmVuV29yZHMpKSB7XG4gICAgcmV0dXJuIHJ2YWwoc3RhdGUsIHN0cmVhbSwgXCJvcGVuX3BhcmVuXCIpO1xuICB9XG5cbiAgLy8gY2xvc2UgcGFyZW5zXG4gIGlmIChub25ncmVlZHkoc3RyZWFtLCBjbG9zZVBhcmVuUkUsIGNsb3NlUGFyZW5Xb3JkcykpIHtcbiAgICByZXR1cm4gcnZhbChzdGF0ZSwgc3RyZWFtLCBcImNsb3NlX3BhcmVuXCIpO1xuICB9XG5cbiAgLy8gc2VwYXJhdG9yc1xuICBpZiAoZ3JlZWR5KHN0cmVhbSwgc2VwYXJhdG9yUkUsIHNlcGFyYXRvcldvcmRzKSkge1xuICAgIHJldHVybiBydmFsKHN0YXRlLCBzdHJlYW0sIFwic2VwYXJhdG9yXCIpO1xuICB9XG5cbiAgLy8gb3BlcmF0b3JzXG4gIGlmIChncmVlZHkoc3RyZWFtLCBvcGVyYXRvclN5bWJvbFJFLCBvcGVyYXRvclN5bWJvbFdvcmRzKSkge1xuICAgIHJldHVybiBydmFsKHN0YXRlLCBzdHJlYW0sIFwib3BlcmF0b3JcIik7XG4gIH1cbiAgcmV0dXJuIHJ2YWwoc3RhdGUsIHN0cmVhbSwgbnVsbCk7XG59XG5cbi8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vXG4vLyB1dGlsaXRpZXNcbmZ1bmN0aW9uIG5vbmdyZWVkeShzdHJlYW0sIHJlLCB3b3Jkcykge1xuICBpZiAoc3RyZWFtLmN1cnJlbnQoKS5sZW5ndGggPT0gMSAmJiByZS50ZXN0KHN0cmVhbS5jdXJyZW50KCkpKSB7XG4gICAgc3RyZWFtLmJhY2tVcCgxKTtcbiAgICB3aGlsZSAocmUudGVzdChzdHJlYW0ucGVlaygpKSkge1xuICAgICAgc3RyZWFtLm5leHQoKTtcbiAgICAgIGlmIChpc19tZW1iZXIoc3RyZWFtLmN1cnJlbnQoKSwgd29yZHMpKSB7XG4gICAgICAgIHJldHVybiB0cnVlO1xuICAgICAgfVxuICAgIH1cbiAgICBzdHJlYW0uYmFja1VwKHN0cmVhbS5jdXJyZW50KCkubGVuZ3RoIC0gMSk7XG4gIH1cbiAgcmV0dXJuIGZhbHNlO1xufVxuZnVuY3Rpb24gZ3JlZWR5KHN0cmVhbSwgcmUsIHdvcmRzKSB7XG4gIGlmIChzdHJlYW0uY3VycmVudCgpLmxlbmd0aCA9PSAxICYmIHJlLnRlc3Qoc3RyZWFtLmN1cnJlbnQoKSkpIHtcbiAgICB3aGlsZSAocmUudGVzdChzdHJlYW0ucGVlaygpKSkge1xuICAgICAgc3RyZWFtLm5leHQoKTtcbiAgICB9XG4gICAgd2hpbGUgKDAgPCBzdHJlYW0uY3VycmVudCgpLmxlbmd0aCkge1xuICAgICAgaWYgKGlzX21lbWJlcihzdHJlYW0uY3VycmVudCgpLCB3b3JkcykpIHtcbiAgICAgICAgcmV0dXJuIHRydWU7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBzdHJlYW0uYmFja1VwKDEpO1xuICAgICAgfVxuICAgIH1cbiAgICBzdHJlYW0ubmV4dCgpO1xuICB9XG4gIHJldHVybiBmYWxzZTtcbn1cbmZ1bmN0aW9uIGRvdWJsZVF1b3RlKHN0cmVhbSkge1xuICByZXR1cm4gcXVvdGUoc3RyZWFtLCAnXCInLCAnXFxcXCcpO1xufVxuZnVuY3Rpb24gc2luZ2xlUXVvdGUoc3RyZWFtKSB7XG4gIHJldHVybiBxdW90ZShzdHJlYW0sICdcXCcnLCAnXFxcXCcpO1xufVxuZnVuY3Rpb24gcXVvdGUoc3RyZWFtLCBxdW90ZUNoYXIsIGVzY2FwZUNoYXIpIHtcbiAgd2hpbGUgKCFzdHJlYW0uZW9sKCkpIHtcbiAgICB2YXIgY2ggPSBzdHJlYW0ubmV4dCgpO1xuICAgIGlmIChjaCA9PSBxdW90ZUNoYXIpIHtcbiAgICAgIHJldHVybiB0cnVlO1xuICAgIH0gZWxzZSBpZiAoY2ggPT0gZXNjYXBlQ2hhcikge1xuICAgICAgc3RyZWFtLm5leHQoKTtcbiAgICB9XG4gIH1cbiAgcmV0dXJuIGZhbHNlO1xufVxuZnVuY3Rpb24gbG9va2FoZWFkKHN0cmVhbSkge1xuICB2YXIgbSA9IHN0cmVhbS5tYXRjaCgvXlxccyooW15cXHMlXSkvLCBmYWxzZSk7XG4gIHJldHVybiBtID8gbVsxXSA6IFwiXCI7XG59XG5mdW5jdGlvbiBpc19tZW1iZXIoZWxlbWVudCwgbGlzdCkge1xuICByZXR1cm4gLTEgPCBsaXN0LmluZGV4T2YoZWxlbWVudCk7XG59XG5mdW5jdGlvbiBydmFsKHN0YXRlLCBzdHJlYW0sIHR5cGUpIHtcbiAgLy8gcGFyc2Ugc3RhY2tcbiAgcHVzaFRva2VuKHN0YXRlLCByZWFsVG9rZW4odHlwZSwgc3RyZWFtKSk7XG5cbiAgLy8gbWFwIGVybGFuZyB0b2tlbiB0eXBlIHRvIENvZGVNaXJyb3Igc3R5bGUgY2xhc3NcbiAgLy8gICAgIGVybGFuZyAgICAgICAgICAgICAtPiBDb2RlTWlycm9yIHRhZ1xuICBzd2l0Y2ggKHR5cGUpIHtcbiAgICBjYXNlIFwiYXRvbVwiOlxuICAgICAgcmV0dXJuIFwiYXRvbVwiO1xuICAgIGNhc2UgXCJhdHRyaWJ1dGVcIjpcbiAgICAgIHJldHVybiBcImF0dHJpYnV0ZVwiO1xuICAgIGNhc2UgXCJib29sZWFuXCI6XG4gICAgICByZXR1cm4gXCJhdG9tXCI7XG4gICAgY2FzZSBcImJ1aWx0aW5cIjpcbiAgICAgIHJldHVybiBcImJ1aWx0aW5cIjtcbiAgICBjYXNlIFwiY2xvc2VfcGFyZW5cIjpcbiAgICAgIHJldHVybiBudWxsO1xuICAgIGNhc2UgXCJjb2xvblwiOlxuICAgICAgcmV0dXJuIG51bGw7XG4gICAgY2FzZSBcImNvbW1lbnRcIjpcbiAgICAgIHJldHVybiBcImNvbW1lbnRcIjtcbiAgICBjYXNlIFwiZG90XCI6XG4gICAgICByZXR1cm4gbnVsbDtcbiAgICBjYXNlIFwiZXJyb3JcIjpcbiAgICAgIHJldHVybiBcImVycm9yXCI7XG4gICAgY2FzZSBcImZ1blwiOlxuICAgICAgcmV0dXJuIFwibWV0YVwiO1xuICAgIGNhc2UgXCJmdW5jdGlvblwiOlxuICAgICAgcmV0dXJuIFwidGFnXCI7XG4gICAgY2FzZSBcImd1YXJkXCI6XG4gICAgICByZXR1cm4gXCJwcm9wZXJ0eVwiO1xuICAgIGNhc2UgXCJrZXl3b3JkXCI6XG4gICAgICByZXR1cm4gXCJrZXl3b3JkXCI7XG4gICAgY2FzZSBcIm1hY3JvXCI6XG4gICAgICByZXR1cm4gXCJtYWNyb05hbWVcIjtcbiAgICBjYXNlIFwibnVtYmVyXCI6XG4gICAgICByZXR1cm4gXCJudW1iZXJcIjtcbiAgICBjYXNlIFwib3Blbl9wYXJlblwiOlxuICAgICAgcmV0dXJuIG51bGw7XG4gICAgY2FzZSBcIm9wZXJhdG9yXCI6XG4gICAgICByZXR1cm4gXCJvcGVyYXRvclwiO1xuICAgIGNhc2UgXCJyZWNvcmRcIjpcbiAgICAgIHJldHVybiBcImJyYWNrZXRcIjtcbiAgICBjYXNlIFwic2VwYXJhdG9yXCI6XG4gICAgICByZXR1cm4gbnVsbDtcbiAgICBjYXNlIFwic3RyaW5nXCI6XG4gICAgICByZXR1cm4gXCJzdHJpbmdcIjtcbiAgICBjYXNlIFwidHlwZVwiOlxuICAgICAgcmV0dXJuIFwiZGVmXCI7XG4gICAgY2FzZSBcInZhcmlhYmxlXCI6XG4gICAgICByZXR1cm4gXCJ2YXJpYWJsZVwiO1xuICAgIGRlZmF1bHQ6XG4gICAgICByZXR1cm4gbnVsbDtcbiAgfVxufVxuZnVuY3Rpb24gYVRva2VuKHRvaywgY29sLCBpbmQsIHR5cCkge1xuICByZXR1cm4ge1xuICAgIHRva2VuOiB0b2ssXG4gICAgY29sdW1uOiBjb2wsXG4gICAgaW5kZW50OiBpbmQsXG4gICAgdHlwZTogdHlwXG4gIH07XG59XG5mdW5jdGlvbiByZWFsVG9rZW4odHlwZSwgc3RyZWFtKSB7XG4gIHJldHVybiBhVG9rZW4oc3RyZWFtLmN1cnJlbnQoKSwgc3RyZWFtLmNvbHVtbigpLCBzdHJlYW0uaW5kZW50YXRpb24oKSwgdHlwZSk7XG59XG5mdW5jdGlvbiBmYWtlVG9rZW4odHlwZSkge1xuICByZXR1cm4gYVRva2VuKHR5cGUsIDAsIDAsIHR5cGUpO1xufVxuZnVuY3Rpb24gcGVla1Rva2VuKHN0YXRlLCBkZXB0aCkge1xuICB2YXIgbGVuID0gc3RhdGUudG9rZW5TdGFjay5sZW5ndGg7XG4gIHZhciBkZXAgPSBkZXB0aCA/IGRlcHRoIDogMTtcbiAgaWYgKGxlbiA8IGRlcCkge1xuICAgIHJldHVybiBmYWxzZTtcbiAgfSBlbHNlIHtcbiAgICByZXR1cm4gc3RhdGUudG9rZW5TdGFja1tsZW4gLSBkZXBdO1xuICB9XG59XG5mdW5jdGlvbiBwdXNoVG9rZW4oc3RhdGUsIHRva2VuKSB7XG4gIGlmICghKHRva2VuLnR5cGUgPT0gXCJjb21tZW50XCIgfHwgdG9rZW4udHlwZSA9PSBcIndoaXRlc3BhY2VcIikpIHtcbiAgICBzdGF0ZS50b2tlblN0YWNrID0gbWF5YmVfZHJvcF9wcmUoc3RhdGUudG9rZW5TdGFjaywgdG9rZW4pO1xuICAgIHN0YXRlLnRva2VuU3RhY2sgPSBtYXliZV9kcm9wX3Bvc3Qoc3RhdGUudG9rZW5TdGFjayk7XG4gIH1cbn1cbmZ1bmN0aW9uIG1heWJlX2Ryb3BfcHJlKHMsIHRva2VuKSB7XG4gIHZhciBsYXN0ID0gcy5sZW5ndGggLSAxO1xuICBpZiAoMCA8IGxhc3QgJiYgc1tsYXN0XS50eXBlID09PSBcInJlY29yZFwiICYmIHRva2VuLnR5cGUgPT09IFwiZG90XCIpIHtcbiAgICBzLnBvcCgpO1xuICB9IGVsc2UgaWYgKDAgPCBsYXN0ICYmIHNbbGFzdF0udHlwZSA9PT0gXCJncm91cFwiKSB7XG4gICAgcy5wb3AoKTtcbiAgICBzLnB1c2godG9rZW4pO1xuICB9IGVsc2Uge1xuICAgIHMucHVzaCh0b2tlbik7XG4gIH1cbiAgcmV0dXJuIHM7XG59XG5mdW5jdGlvbiBtYXliZV9kcm9wX3Bvc3Qocykge1xuICBpZiAoIXMubGVuZ3RoKSByZXR1cm4gcztcbiAgdmFyIGxhc3QgPSBzLmxlbmd0aCAtIDE7XG4gIGlmIChzW2xhc3RdLnR5cGUgPT09IFwiZG90XCIpIHtcbiAgICByZXR1cm4gW107XG4gIH1cbiAgaWYgKGxhc3QgPiAxICYmIHNbbGFzdF0udHlwZSA9PT0gXCJmdW5cIiAmJiBzW2xhc3QgLSAxXS50b2tlbiA9PT0gXCJmdW5cIikge1xuICAgIHJldHVybiBzLnNsaWNlKDAsIGxhc3QgLSAxKTtcbiAgfVxuICBzd2l0Y2ggKHNbbGFzdF0udG9rZW4pIHtcbiAgICBjYXNlIFwifVwiOlxuICAgICAgcmV0dXJuIGQocywge1xuICAgICAgICBnOiBbXCJ7XCJdXG4gICAgICB9KTtcbiAgICBjYXNlIFwiXVwiOlxuICAgICAgcmV0dXJuIGQocywge1xuICAgICAgICBpOiBbXCJbXCJdXG4gICAgICB9KTtcbiAgICBjYXNlIFwiKVwiOlxuICAgICAgcmV0dXJuIGQocywge1xuICAgICAgICBpOiBbXCIoXCJdXG4gICAgICB9KTtcbiAgICBjYXNlIFwiPj5cIjpcbiAgICAgIHJldHVybiBkKHMsIHtcbiAgICAgICAgaTogW1wiPDxcIl1cbiAgICAgIH0pO1xuICAgIGNhc2UgXCJlbmRcIjpcbiAgICAgIHJldHVybiBkKHMsIHtcbiAgICAgICAgaTogW1wiYmVnaW5cIiwgXCJjYXNlXCIsIFwiZnVuXCIsIFwiaWZcIiwgXCJyZWNlaXZlXCIsIFwidHJ5XCJdXG4gICAgICB9KTtcbiAgICBjYXNlIFwiLFwiOlxuICAgICAgcmV0dXJuIGQocywge1xuICAgICAgICBlOiBbXCJiZWdpblwiLCBcInRyeVwiLCBcIndoZW5cIiwgXCItPlwiLCBcIixcIiwgXCIoXCIsIFwiW1wiLCBcIntcIiwgXCI8PFwiXVxuICAgICAgfSk7XG4gICAgY2FzZSBcIi0+XCI6XG4gICAgICByZXR1cm4gZChzLCB7XG4gICAgICAgIHI6IFtcIndoZW5cIl0sXG4gICAgICAgIG06IFtcInRyeVwiLCBcImlmXCIsIFwiY2FzZVwiLCBcInJlY2VpdmVcIl1cbiAgICAgIH0pO1xuICAgIGNhc2UgXCI7XCI6XG4gICAgICByZXR1cm4gZChzLCB7XG4gICAgICAgIEU6IFtcImNhc2VcIiwgXCJmdW5cIiwgXCJpZlwiLCBcInJlY2VpdmVcIiwgXCJ0cnlcIiwgXCJ3aGVuXCJdXG4gICAgICB9KTtcbiAgICBjYXNlIFwiY2F0Y2hcIjpcbiAgICAgIHJldHVybiBkKHMsIHtcbiAgICAgICAgZTogW1widHJ5XCJdXG4gICAgICB9KTtcbiAgICBjYXNlIFwib2ZcIjpcbiAgICAgIHJldHVybiBkKHMsIHtcbiAgICAgICAgZTogW1wiY2FzZVwiXVxuICAgICAgfSk7XG4gICAgY2FzZSBcImFmdGVyXCI6XG4gICAgICByZXR1cm4gZChzLCB7XG4gICAgICAgIGU6IFtcInJlY2VpdmVcIiwgXCJ0cnlcIl1cbiAgICAgIH0pO1xuICAgIGRlZmF1bHQ6XG4gICAgICByZXR1cm4gcztcbiAgfVxufVxuZnVuY3Rpb24gZChzdGFjaywgdHQpIHtcbiAgLy8gc3RhY2sgaXMgYSBzdGFjayBvZiBUb2tlbiBvYmplY3RzLlxuICAvLyB0dCBpcyBhbiBvYmplY3Q7IHt0eXBlOnRva2Vuc31cbiAgLy8gdHlwZSBpcyBhIGNoYXIsIHRva2VucyBpcyBhIGxpc3Qgb2YgdG9rZW4gc3RyaW5ncy5cbiAgLy8gVGhlIGZ1bmN0aW9uIHJldHVybnMgKHBvc3NpYmx5IHRydW5jYXRlZCkgc3RhY2suXG4gIC8vIEl0IHdpbGwgZGVzY2VuZCB0aGUgc3RhY2ssIGxvb2tpbmcgZm9yIGEgVG9rZW4gc3VjaCB0aGF0IFRva2VuLnRva2VuXG4gIC8vICBpcyBhIG1lbWJlciBvZiB0b2tlbnMuIElmIGl0IGRvZXMgbm90IGZpbmQgdGhhdCwgaXQgd2lsbCBub3JtYWxseSAoYnV0XG4gIC8vICBzZWUgXCJFXCIgYmVsb3cpIHJldHVybiBzdGFjay4gSWYgaXQgZG9lcyBmaW5kIGEgbWF0Y2gsIGl0IHdpbGwgcmVtb3ZlXG4gIC8vICBhbGwgdGhlIFRva2VucyBiZXR3ZWVuIHRoZSB0b3AgYW5kIHRoZSBtYXRjaGVkIFRva2VuLlxuICAvLyBJZiB0eXBlIGlzIFwibVwiLCB0aGF0IGlzIGFsbCBpdCBkb2VzLlxuICAvLyBJZiB0eXBlIGlzIFwiaVwiLCBpdCB3aWxsIGFsc28gcmVtb3ZlIHRoZSBtYXRjaGVkIFRva2VuIGFuZCB0aGUgdG9wIFRva2VuLlxuICAvLyBJZiB0eXBlIGlzIFwiZ1wiLCBsaWtlIFwiaVwiLCBidXQgYWRkIGEgZmFrZSBcImdyb3VwXCIgdG9rZW4gYXQgdGhlIHRvcC5cbiAgLy8gSWYgdHlwZSBpcyBcInJcIiwgaXQgd2lsbCByZW1vdmUgdGhlIG1hdGNoZWQgVG9rZW4sIGJ1dCBub3QgdGhlIHRvcCBUb2tlbi5cbiAgLy8gSWYgdHlwZSBpcyBcImVcIiwgaXQgd2lsbCBrZWVwIHRoZSBtYXRjaGVkIFRva2VuIGJ1dCBub3QgdGhlIHRvcCBUb2tlbi5cbiAgLy8gSWYgdHlwZSBpcyBcIkVcIiwgaXQgYmVoYXZlcyBhcyBmb3IgdHlwZSBcImVcIiwgZXhjZXB0IGlmIHRoZXJlIGlzIG5vIG1hdGNoLFxuICAvLyAgaW4gd2hpY2ggY2FzZSBpdCB3aWxsIHJldHVybiBhbiBlbXB0eSBzdGFjay5cblxuICBmb3IgKHZhciB0eXBlIGluIHR0KSB7XG4gICAgdmFyIGxlbiA9IHN0YWNrLmxlbmd0aCAtIDE7XG4gICAgdmFyIHRva2VucyA9IHR0W3R5cGVdO1xuICAgIGZvciAodmFyIGkgPSBsZW4gLSAxOyAtMSA8IGk7IGktLSkge1xuICAgICAgaWYgKGlzX21lbWJlcihzdGFja1tpXS50b2tlbiwgdG9rZW5zKSkge1xuICAgICAgICB2YXIgc3MgPSBzdGFjay5zbGljZSgwLCBpKTtcbiAgICAgICAgc3dpdGNoICh0eXBlKSB7XG4gICAgICAgICAgY2FzZSBcIm1cIjpcbiAgICAgICAgICAgIHJldHVybiBzcy5jb25jYXQoc3RhY2tbaV0pLmNvbmNhdChzdGFja1tsZW5dKTtcbiAgICAgICAgICBjYXNlIFwiclwiOlxuICAgICAgICAgICAgcmV0dXJuIHNzLmNvbmNhdChzdGFja1tsZW5dKTtcbiAgICAgICAgICBjYXNlIFwiaVwiOlxuICAgICAgICAgICAgcmV0dXJuIHNzO1xuICAgICAgICAgIGNhc2UgXCJnXCI6XG4gICAgICAgICAgICByZXR1cm4gc3MuY29uY2F0KGZha2VUb2tlbihcImdyb3VwXCIpKTtcbiAgICAgICAgICBjYXNlIFwiRVwiOlxuICAgICAgICAgICAgcmV0dXJuIHNzLmNvbmNhdChzdGFja1tpXSk7XG4gICAgICAgICAgY2FzZSBcImVcIjpcbiAgICAgICAgICAgIHJldHVybiBzcy5jb25jYXQoc3RhY2tbaV0pO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfVxuICB9XG4gIHJldHVybiB0eXBlID09IFwiRVwiID8gW10gOiBzdGFjaztcbn1cblxuLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy9cbi8vIGluZGVudGVyXG5cbmZ1bmN0aW9uIGluZGVudGVyKHN0YXRlLCB0ZXh0QWZ0ZXIsIGN4KSB7XG4gIHZhciB0O1xuICB2YXIgd29yZEFmdGVyID0gd29yZGFmdGVyKHRleHRBZnRlcik7XG4gIHZhciBjdXJyVCA9IHBlZWtUb2tlbihzdGF0ZSwgMSk7XG4gIHZhciBwcmV2VCA9IHBlZWtUb2tlbihzdGF0ZSwgMik7XG4gIGlmIChzdGF0ZS5pbl9zdHJpbmcgfHwgc3RhdGUuaW5fYXRvbSkge1xuICAgIHJldHVybiBudWxsO1xuICB9IGVsc2UgaWYgKCFwcmV2VCkge1xuICAgIHJldHVybiAwO1xuICB9IGVsc2UgaWYgKGN1cnJULnRva2VuID09IFwid2hlblwiKSB7XG4gICAgcmV0dXJuIGN1cnJULmNvbHVtbiArIGN4LnVuaXQ7XG4gIH0gZWxzZSBpZiAod29yZEFmdGVyID09PSBcIndoZW5cIiAmJiBwcmV2VC50eXBlID09PSBcImZ1bmN0aW9uXCIpIHtcbiAgICByZXR1cm4gcHJldlQuaW5kZW50ICsgY3gudW5pdDtcbiAgfSBlbHNlIGlmICh3b3JkQWZ0ZXIgPT09IFwiKFwiICYmIGN1cnJULnRva2VuID09PSBcImZ1blwiKSB7XG4gICAgcmV0dXJuIGN1cnJULmNvbHVtbiArIDM7XG4gIH0gZWxzZSBpZiAod29yZEFmdGVyID09PSBcImNhdGNoXCIgJiYgKHQgPSBnZXRUb2tlbihzdGF0ZSwgW1widHJ5XCJdKSkpIHtcbiAgICByZXR1cm4gdC5jb2x1bW47XG4gIH0gZWxzZSBpZiAoaXNfbWVtYmVyKHdvcmRBZnRlciwgW1wiZW5kXCIsIFwiYWZ0ZXJcIiwgXCJvZlwiXSkpIHtcbiAgICB0ID0gZ2V0VG9rZW4oc3RhdGUsIFtcImJlZ2luXCIsIFwiY2FzZVwiLCBcImZ1blwiLCBcImlmXCIsIFwicmVjZWl2ZVwiLCBcInRyeVwiXSk7XG4gICAgcmV0dXJuIHQgPyB0LmNvbHVtbiA6IG51bGw7XG4gIH0gZWxzZSBpZiAoaXNfbWVtYmVyKHdvcmRBZnRlciwgY2xvc2VQYXJlbldvcmRzKSkge1xuICAgIHQgPSBnZXRUb2tlbihzdGF0ZSwgb3BlblBhcmVuV29yZHMpO1xuICAgIHJldHVybiB0ID8gdC5jb2x1bW4gOiBudWxsO1xuICB9IGVsc2UgaWYgKGlzX21lbWJlcihjdXJyVC50b2tlbiwgW1wiLFwiLCBcInxcIiwgXCJ8fFwiXSkgfHwgaXNfbWVtYmVyKHdvcmRBZnRlciwgW1wiLFwiLCBcInxcIiwgXCJ8fFwiXSkpIHtcbiAgICB0ID0gcG9zdGNvbW1hVG9rZW4oc3RhdGUpO1xuICAgIHJldHVybiB0ID8gdC5jb2x1bW4gKyB0LnRva2VuLmxlbmd0aCA6IGN4LnVuaXQ7XG4gIH0gZWxzZSBpZiAoY3VyclQudG9rZW4gPT0gXCItPlwiKSB7XG4gICAgaWYgKGlzX21lbWJlcihwcmV2VC50b2tlbiwgW1wicmVjZWl2ZVwiLCBcImNhc2VcIiwgXCJpZlwiLCBcInRyeVwiXSkpIHtcbiAgICAgIHJldHVybiBwcmV2VC5jb2x1bW4gKyBjeC51bml0ICsgY3gudW5pdDtcbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIHByZXZULmNvbHVtbiArIGN4LnVuaXQ7XG4gICAgfVxuICB9IGVsc2UgaWYgKGlzX21lbWJlcihjdXJyVC50b2tlbiwgb3BlblBhcmVuV29yZHMpKSB7XG4gICAgcmV0dXJuIGN1cnJULmNvbHVtbiArIGN1cnJULnRva2VuLmxlbmd0aDtcbiAgfSBlbHNlIHtcbiAgICB0ID0gZGVmYXVsdFRva2VuKHN0YXRlKTtcbiAgICByZXR1cm4gdHJ1dGh5KHQpID8gdC5jb2x1bW4gKyBjeC51bml0IDogMDtcbiAgfVxufVxuZnVuY3Rpb24gd29yZGFmdGVyKHN0cikge1xuICB2YXIgbSA9IHN0ci5tYXRjaCgvLHxbYS16XSt8XFx9fFxcXXxcXCl8Pj58XFx8K3xcXCgvKTtcbiAgcmV0dXJuIHRydXRoeShtKSAmJiBtLmluZGV4ID09PSAwID8gbVswXSA6IFwiXCI7XG59XG5mdW5jdGlvbiBwb3N0Y29tbWFUb2tlbihzdGF0ZSkge1xuICB2YXIgb2JqcyA9IHN0YXRlLnRva2VuU3RhY2suc2xpY2UoMCwgLTEpO1xuICB2YXIgaSA9IGdldFRva2VuSW5kZXgob2JqcywgXCJ0eXBlXCIsIFtcIm9wZW5fcGFyZW5cIl0pO1xuICByZXR1cm4gdHJ1dGh5KG9ianNbaV0pID8gb2Jqc1tpXSA6IGZhbHNlO1xufVxuZnVuY3Rpb24gZGVmYXVsdFRva2VuKHN0YXRlKSB7XG4gIHZhciBvYmpzID0gc3RhdGUudG9rZW5TdGFjaztcbiAgdmFyIHN0b3AgPSBnZXRUb2tlbkluZGV4KG9ianMsIFwidHlwZVwiLCBbXCJvcGVuX3BhcmVuXCIsIFwic2VwYXJhdG9yXCIsIFwia2V5d29yZFwiXSk7XG4gIHZhciBvcGVyID0gZ2V0VG9rZW5JbmRleChvYmpzLCBcInR5cGVcIiwgW1wib3BlcmF0b3JcIl0pO1xuICBpZiAodHJ1dGh5KHN0b3ApICYmIHRydXRoeShvcGVyKSAmJiBzdG9wIDwgb3Blcikge1xuICAgIHJldHVybiBvYmpzW3N0b3AgKyAxXTtcbiAgfSBlbHNlIGlmICh0cnV0aHkoc3RvcCkpIHtcbiAgICByZXR1cm4gb2Jqc1tzdG9wXTtcbiAgfSBlbHNlIHtcbiAgICByZXR1cm4gZmFsc2U7XG4gIH1cbn1cbmZ1bmN0aW9uIGdldFRva2VuKHN0YXRlLCB0b2tlbnMpIHtcbiAgdmFyIG9ianMgPSBzdGF0ZS50b2tlblN0YWNrO1xuICB2YXIgaSA9IGdldFRva2VuSW5kZXgob2JqcywgXCJ0b2tlblwiLCB0b2tlbnMpO1xuICByZXR1cm4gdHJ1dGh5KG9ianNbaV0pID8gb2Jqc1tpXSA6IGZhbHNlO1xufVxuZnVuY3Rpb24gZ2V0VG9rZW5JbmRleChvYmpzLCBwcm9wbmFtZSwgcHJvcHZhbHMpIHtcbiAgZm9yICh2YXIgaSA9IG9ianMubGVuZ3RoIC0gMTsgLTEgPCBpOyBpLS0pIHtcbiAgICBpZiAoaXNfbWVtYmVyKG9ianNbaV1bcHJvcG5hbWVdLCBwcm9wdmFscykpIHtcbiAgICAgIHJldHVybiBpO1xuICAgIH1cbiAgfVxuICByZXR1cm4gZmFsc2U7XG59XG5mdW5jdGlvbiB0cnV0aHkoeCkge1xuICByZXR1cm4geCAhPT0gZmFsc2UgJiYgeCAhPSBudWxsO1xufVxuXG4vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vLy8vL1xuLy8gdGhpcyBvYmplY3QgZGVmaW5lcyB0aGUgbW9kZVxuXG5leHBvcnQgY29uc3QgZXJsYW5nID0ge1xuICBuYW1lOiBcImVybGFuZ1wiLFxuICBzdGFydFN0YXRlKCkge1xuICAgIHJldHVybiB7XG4gICAgICB0b2tlblN0YWNrOiBbXSxcbiAgICAgIGluX3N0cmluZzogZmFsc2UsXG4gICAgICBpbl9hdG9tOiBmYWxzZVxuICAgIH07XG4gIH0sXG4gIHRva2VuOiB0b2tlbml6ZXIsXG4gIGluZGVudDogaW5kZW50ZXIsXG4gIGxhbmd1YWdlRGF0YToge1xuICAgIGNvbW1lbnRUb2tlbnM6IHtcbiAgICAgIGxpbmU6IFwiJVwiXG4gICAgfVxuICB9XG59OyJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==