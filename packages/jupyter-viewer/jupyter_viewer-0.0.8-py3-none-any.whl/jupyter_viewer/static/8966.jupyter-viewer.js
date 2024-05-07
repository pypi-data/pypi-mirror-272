"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[8966],{

/***/ 88966:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "fSharp": () => (/* binding */ fSharp),
/* harmony export */   "oCaml": () => (/* binding */ oCaml),
/* harmony export */   "sml": () => (/* binding */ sml)
/* harmony export */ });
function mlLike(parserConfig) {
  var words = {
    'as': 'keyword',
    'do': 'keyword',
    'else': 'keyword',
    'end': 'keyword',
    'exception': 'keyword',
    'fun': 'keyword',
    'functor': 'keyword',
    'if': 'keyword',
    'in': 'keyword',
    'include': 'keyword',
    'let': 'keyword',
    'of': 'keyword',
    'open': 'keyword',
    'rec': 'keyword',
    'struct': 'keyword',
    'then': 'keyword',
    'type': 'keyword',
    'val': 'keyword',
    'while': 'keyword',
    'with': 'keyword'
  };
  var extraWords = parserConfig.extraWords || {};
  for (var prop in extraWords) {
    if (extraWords.hasOwnProperty(prop)) {
      words[prop] = parserConfig.extraWords[prop];
    }
  }
  var hintWords = [];
  for (var k in words) {
    hintWords.push(k);
  }
  function tokenBase(stream, state) {
    var ch = stream.next();
    if (ch === '"') {
      state.tokenize = tokenString;
      return state.tokenize(stream, state);
    }
    if (ch === '{') {
      if (stream.eat('|')) {
        state.longString = true;
        state.tokenize = tokenLongString;
        return state.tokenize(stream, state);
      }
    }
    if (ch === '(') {
      if (stream.match(/^\*(?!\))/)) {
        state.commentLevel++;
        state.tokenize = tokenComment;
        return state.tokenize(stream, state);
      }
    }
    if (ch === '~' || ch === '?') {
      stream.eatWhile(/\w/);
      return 'variableName.special';
    }
    if (ch === '`') {
      stream.eatWhile(/\w/);
      return 'quote';
    }
    if (ch === '/' && parserConfig.slashComments && stream.eat('/')) {
      stream.skipToEnd();
      return 'comment';
    }
    if (/\d/.test(ch)) {
      if (ch === '0' && stream.eat(/[bB]/)) {
        stream.eatWhile(/[01]/);
      }
      if (ch === '0' && stream.eat(/[xX]/)) {
        stream.eatWhile(/[0-9a-fA-F]/);
      }
      if (ch === '0' && stream.eat(/[oO]/)) {
        stream.eatWhile(/[0-7]/);
      } else {
        stream.eatWhile(/[\d_]/);
        if (stream.eat('.')) {
          stream.eatWhile(/[\d]/);
        }
        if (stream.eat(/[eE]/)) {
          stream.eatWhile(/[\d\-+]/);
        }
      }
      return 'number';
    }
    if (/[+\-*&%=<>!?|@\.~:]/.test(ch)) {
      return 'operator';
    }
    if (/[\w\xa1-\uffff]/.test(ch)) {
      stream.eatWhile(/[\w\xa1-\uffff]/);
      var cur = stream.current();
      return words.hasOwnProperty(cur) ? words[cur] : 'variable';
    }
    return null;
  }
  function tokenString(stream, state) {
    var next,
      end = false,
      escaped = false;
    while ((next = stream.next()) != null) {
      if (next === '"' && !escaped) {
        end = true;
        break;
      }
      escaped = !escaped && next === '\\';
    }
    if (end && !escaped) {
      state.tokenize = tokenBase;
    }
    return 'string';
  }
  ;
  function tokenComment(stream, state) {
    var prev, next;
    while (state.commentLevel > 0 && (next = stream.next()) != null) {
      if (prev === '(' && next === '*') state.commentLevel++;
      if (prev === '*' && next === ')') state.commentLevel--;
      prev = next;
    }
    if (state.commentLevel <= 0) {
      state.tokenize = tokenBase;
    }
    return 'comment';
  }
  function tokenLongString(stream, state) {
    var prev, next;
    while (state.longString && (next = stream.next()) != null) {
      if (prev === '|' && next === '}') state.longString = false;
      prev = next;
    }
    if (!state.longString) {
      state.tokenize = tokenBase;
    }
    return 'string';
  }
  return {
    startState: function () {
      return {
        tokenize: tokenBase,
        commentLevel: 0,
        longString: false
      };
    },
    token: function (stream, state) {
      if (stream.eatSpace()) return null;
      return state.tokenize(stream, state);
    },
    languageData: {
      autocomplete: hintWords,
      commentTokens: {
        line: parserConfig.slashComments ? "//" : undefined,
        block: {
          open: "(*",
          close: "*)"
        }
      }
    }
  };
}
;
const oCaml = mlLike({
  name: "ocaml",
  extraWords: {
    'and': 'keyword',
    'assert': 'keyword',
    'begin': 'keyword',
    'class': 'keyword',
    'constraint': 'keyword',
    'done': 'keyword',
    'downto': 'keyword',
    'external': 'keyword',
    'function': 'keyword',
    'initializer': 'keyword',
    'lazy': 'keyword',
    'match': 'keyword',
    'method': 'keyword',
    'module': 'keyword',
    'mutable': 'keyword',
    'new': 'keyword',
    'nonrec': 'keyword',
    'object': 'keyword',
    'private': 'keyword',
    'sig': 'keyword',
    'to': 'keyword',
    'try': 'keyword',
    'value': 'keyword',
    'virtual': 'keyword',
    'when': 'keyword',
    // builtins
    'raise': 'builtin',
    'failwith': 'builtin',
    'true': 'builtin',
    'false': 'builtin',
    // Pervasives builtins
    'asr': 'builtin',
    'land': 'builtin',
    'lor': 'builtin',
    'lsl': 'builtin',
    'lsr': 'builtin',
    'lxor': 'builtin',
    'mod': 'builtin',
    'or': 'builtin',
    // More Pervasives
    'raise_notrace': 'builtin',
    'trace': 'builtin',
    'exit': 'builtin',
    'print_string': 'builtin',
    'print_endline': 'builtin',
    'int': 'type',
    'float': 'type',
    'bool': 'type',
    'char': 'type',
    'string': 'type',
    'unit': 'type',
    // Modules
    'List': 'builtin'
  }
});
const fSharp = mlLike({
  name: "fsharp",
  extraWords: {
    'abstract': 'keyword',
    'assert': 'keyword',
    'base': 'keyword',
    'begin': 'keyword',
    'class': 'keyword',
    'default': 'keyword',
    'delegate': 'keyword',
    'do!': 'keyword',
    'done': 'keyword',
    'downcast': 'keyword',
    'downto': 'keyword',
    'elif': 'keyword',
    'extern': 'keyword',
    'finally': 'keyword',
    'for': 'keyword',
    'function': 'keyword',
    'global': 'keyword',
    'inherit': 'keyword',
    'inline': 'keyword',
    'interface': 'keyword',
    'internal': 'keyword',
    'lazy': 'keyword',
    'let!': 'keyword',
    'match': 'keyword',
    'member': 'keyword',
    'module': 'keyword',
    'mutable': 'keyword',
    'namespace': 'keyword',
    'new': 'keyword',
    'null': 'keyword',
    'override': 'keyword',
    'private': 'keyword',
    'public': 'keyword',
    'return!': 'keyword',
    'return': 'keyword',
    'select': 'keyword',
    'static': 'keyword',
    'to': 'keyword',
    'try': 'keyword',
    'upcast': 'keyword',
    'use!': 'keyword',
    'use': 'keyword',
    'void': 'keyword',
    'when': 'keyword',
    'yield!': 'keyword',
    'yield': 'keyword',
    // Reserved words
    'atomic': 'keyword',
    'break': 'keyword',
    'checked': 'keyword',
    'component': 'keyword',
    'const': 'keyword',
    'constraint': 'keyword',
    'constructor': 'keyword',
    'continue': 'keyword',
    'eager': 'keyword',
    'event': 'keyword',
    'external': 'keyword',
    'fixed': 'keyword',
    'method': 'keyword',
    'mixin': 'keyword',
    'object': 'keyword',
    'parallel': 'keyword',
    'process': 'keyword',
    'protected': 'keyword',
    'pure': 'keyword',
    'sealed': 'keyword',
    'tailcall': 'keyword',
    'trait': 'keyword',
    'virtual': 'keyword',
    'volatile': 'keyword',
    // builtins
    'List': 'builtin',
    'Seq': 'builtin',
    'Map': 'builtin',
    'Set': 'builtin',
    'Option': 'builtin',
    'int': 'builtin',
    'string': 'builtin',
    'not': 'builtin',
    'true': 'builtin',
    'false': 'builtin',
    'raise': 'builtin',
    'failwith': 'builtin'
  },
  slashComments: true
});
const sml = mlLike({
  name: "sml",
  extraWords: {
    'abstype': 'keyword',
    'and': 'keyword',
    'andalso': 'keyword',
    'case': 'keyword',
    'datatype': 'keyword',
    'fn': 'keyword',
    'handle': 'keyword',
    'infix': 'keyword',
    'infixr': 'keyword',
    'local': 'keyword',
    'nonfix': 'keyword',
    'op': 'keyword',
    'orelse': 'keyword',
    'raise': 'keyword',
    'withtype': 'keyword',
    'eqtype': 'keyword',
    'sharing': 'keyword',
    'sig': 'keyword',
    'signature': 'keyword',
    'structure': 'keyword',
    'where': 'keyword',
    'true': 'keyword',
    'false': 'keyword',
    // types
    'int': 'builtin',
    'real': 'builtin',
    'string': 'builtin',
    'char': 'builtin',
    'bool': 'builtin'
  },
  slashComments: true
});

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiODk2Ni5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7QUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGNvZGVtaXJyb3IvbGVnYWN5LW1vZGVzL21vZGUvbWxsaWtlLmpzIl0sInNvdXJjZXNDb250ZW50IjpbImZ1bmN0aW9uIG1sTGlrZShwYXJzZXJDb25maWcpIHtcbiAgdmFyIHdvcmRzID0ge1xuICAgICdhcyc6ICdrZXl3b3JkJyxcbiAgICAnZG8nOiAna2V5d29yZCcsXG4gICAgJ2Vsc2UnOiAna2V5d29yZCcsXG4gICAgJ2VuZCc6ICdrZXl3b3JkJyxcbiAgICAnZXhjZXB0aW9uJzogJ2tleXdvcmQnLFxuICAgICdmdW4nOiAna2V5d29yZCcsXG4gICAgJ2Z1bmN0b3InOiAna2V5d29yZCcsXG4gICAgJ2lmJzogJ2tleXdvcmQnLFxuICAgICdpbic6ICdrZXl3b3JkJyxcbiAgICAnaW5jbHVkZSc6ICdrZXl3b3JkJyxcbiAgICAnbGV0JzogJ2tleXdvcmQnLFxuICAgICdvZic6ICdrZXl3b3JkJyxcbiAgICAnb3Blbic6ICdrZXl3b3JkJyxcbiAgICAncmVjJzogJ2tleXdvcmQnLFxuICAgICdzdHJ1Y3QnOiAna2V5d29yZCcsXG4gICAgJ3RoZW4nOiAna2V5d29yZCcsXG4gICAgJ3R5cGUnOiAna2V5d29yZCcsXG4gICAgJ3ZhbCc6ICdrZXl3b3JkJyxcbiAgICAnd2hpbGUnOiAna2V5d29yZCcsXG4gICAgJ3dpdGgnOiAna2V5d29yZCdcbiAgfTtcbiAgdmFyIGV4dHJhV29yZHMgPSBwYXJzZXJDb25maWcuZXh0cmFXb3JkcyB8fCB7fTtcbiAgZm9yICh2YXIgcHJvcCBpbiBleHRyYVdvcmRzKSB7XG4gICAgaWYgKGV4dHJhV29yZHMuaGFzT3duUHJvcGVydHkocHJvcCkpIHtcbiAgICAgIHdvcmRzW3Byb3BdID0gcGFyc2VyQ29uZmlnLmV4dHJhV29yZHNbcHJvcF07XG4gICAgfVxuICB9XG4gIHZhciBoaW50V29yZHMgPSBbXTtcbiAgZm9yICh2YXIgayBpbiB3b3Jkcykge1xuICAgIGhpbnRXb3Jkcy5wdXNoKGspO1xuICB9XG4gIGZ1bmN0aW9uIHRva2VuQmFzZShzdHJlYW0sIHN0YXRlKSB7XG4gICAgdmFyIGNoID0gc3RyZWFtLm5leHQoKTtcbiAgICBpZiAoY2ggPT09ICdcIicpIHtcbiAgICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5TdHJpbmc7XG4gICAgICByZXR1cm4gc3RhdGUudG9rZW5pemUoc3RyZWFtLCBzdGF0ZSk7XG4gICAgfVxuICAgIGlmIChjaCA9PT0gJ3snKSB7XG4gICAgICBpZiAoc3RyZWFtLmVhdCgnfCcpKSB7XG4gICAgICAgIHN0YXRlLmxvbmdTdHJpbmcgPSB0cnVlO1xuICAgICAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuTG9uZ1N0cmluZztcbiAgICAgICAgcmV0dXJuIHN0YXRlLnRva2VuaXplKHN0cmVhbSwgc3RhdGUpO1xuICAgICAgfVxuICAgIH1cbiAgICBpZiAoY2ggPT09ICcoJykge1xuICAgICAgaWYgKHN0cmVhbS5tYXRjaCgvXlxcKig/IVxcKSkvKSkge1xuICAgICAgICBzdGF0ZS5jb21tZW50TGV2ZWwrKztcbiAgICAgICAgc3RhdGUudG9rZW5pemUgPSB0b2tlbkNvbW1lbnQ7XG4gICAgICAgIHJldHVybiBzdGF0ZS50b2tlbml6ZShzdHJlYW0sIHN0YXRlKTtcbiAgICAgIH1cbiAgICB9XG4gICAgaWYgKGNoID09PSAnficgfHwgY2ggPT09ICc/Jykge1xuICAgICAgc3RyZWFtLmVhdFdoaWxlKC9cXHcvKTtcbiAgICAgIHJldHVybiAndmFyaWFibGVOYW1lLnNwZWNpYWwnO1xuICAgIH1cbiAgICBpZiAoY2ggPT09ICdgJykge1xuICAgICAgc3RyZWFtLmVhdFdoaWxlKC9cXHcvKTtcbiAgICAgIHJldHVybiAncXVvdGUnO1xuICAgIH1cbiAgICBpZiAoY2ggPT09ICcvJyAmJiBwYXJzZXJDb25maWcuc2xhc2hDb21tZW50cyAmJiBzdHJlYW0uZWF0KCcvJykpIHtcbiAgICAgIHN0cmVhbS5za2lwVG9FbmQoKTtcbiAgICAgIHJldHVybiAnY29tbWVudCc7XG4gICAgfVxuICAgIGlmICgvXFxkLy50ZXN0KGNoKSkge1xuICAgICAgaWYgKGNoID09PSAnMCcgJiYgc3RyZWFtLmVhdCgvW2JCXS8pKSB7XG4gICAgICAgIHN0cmVhbS5lYXRXaGlsZSgvWzAxXS8pO1xuICAgICAgfVxuICAgICAgaWYgKGNoID09PSAnMCcgJiYgc3RyZWFtLmVhdCgvW3hYXS8pKSB7XG4gICAgICAgIHN0cmVhbS5lYXRXaGlsZSgvWzAtOWEtZkEtRl0vKTtcbiAgICAgIH1cbiAgICAgIGlmIChjaCA9PT0gJzAnICYmIHN0cmVhbS5lYXQoL1tvT10vKSkge1xuICAgICAgICBzdHJlYW0uZWF0V2hpbGUoL1swLTddLyk7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBzdHJlYW0uZWF0V2hpbGUoL1tcXGRfXS8pO1xuICAgICAgICBpZiAoc3RyZWFtLmVhdCgnLicpKSB7XG4gICAgICAgICAgc3RyZWFtLmVhdFdoaWxlKC9bXFxkXS8pO1xuICAgICAgICB9XG4gICAgICAgIGlmIChzdHJlYW0uZWF0KC9bZUVdLykpIHtcbiAgICAgICAgICBzdHJlYW0uZWF0V2hpbGUoL1tcXGRcXC0rXS8pO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgICByZXR1cm4gJ251bWJlcic7XG4gICAgfVxuICAgIGlmICgvWytcXC0qJiU9PD4hP3xAXFwufjpdLy50ZXN0KGNoKSkge1xuICAgICAgcmV0dXJuICdvcGVyYXRvcic7XG4gICAgfVxuICAgIGlmICgvW1xcd1xceGExLVxcdWZmZmZdLy50ZXN0KGNoKSkge1xuICAgICAgc3RyZWFtLmVhdFdoaWxlKC9bXFx3XFx4YTEtXFx1ZmZmZl0vKTtcbiAgICAgIHZhciBjdXIgPSBzdHJlYW0uY3VycmVudCgpO1xuICAgICAgcmV0dXJuIHdvcmRzLmhhc093blByb3BlcnR5KGN1cikgPyB3b3Jkc1tjdXJdIDogJ3ZhcmlhYmxlJztcbiAgICB9XG4gICAgcmV0dXJuIG51bGw7XG4gIH1cbiAgZnVuY3Rpb24gdG9rZW5TdHJpbmcoc3RyZWFtLCBzdGF0ZSkge1xuICAgIHZhciBuZXh0LFxuICAgICAgZW5kID0gZmFsc2UsXG4gICAgICBlc2NhcGVkID0gZmFsc2U7XG4gICAgd2hpbGUgKChuZXh0ID0gc3RyZWFtLm5leHQoKSkgIT0gbnVsbCkge1xuICAgICAgaWYgKG5leHQgPT09ICdcIicgJiYgIWVzY2FwZWQpIHtcbiAgICAgICAgZW5kID0gdHJ1ZTtcbiAgICAgICAgYnJlYWs7XG4gICAgICB9XG4gICAgICBlc2NhcGVkID0gIWVzY2FwZWQgJiYgbmV4dCA9PT0gJ1xcXFwnO1xuICAgIH1cbiAgICBpZiAoZW5kICYmICFlc2NhcGVkKSB7XG4gICAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQmFzZTtcbiAgICB9XG4gICAgcmV0dXJuICdzdHJpbmcnO1xuICB9XG4gIDtcbiAgZnVuY3Rpb24gdG9rZW5Db21tZW50KHN0cmVhbSwgc3RhdGUpIHtcbiAgICB2YXIgcHJldiwgbmV4dDtcbiAgICB3aGlsZSAoc3RhdGUuY29tbWVudExldmVsID4gMCAmJiAobmV4dCA9IHN0cmVhbS5uZXh0KCkpICE9IG51bGwpIHtcbiAgICAgIGlmIChwcmV2ID09PSAnKCcgJiYgbmV4dCA9PT0gJyonKSBzdGF0ZS5jb21tZW50TGV2ZWwrKztcbiAgICAgIGlmIChwcmV2ID09PSAnKicgJiYgbmV4dCA9PT0gJyknKSBzdGF0ZS5jb21tZW50TGV2ZWwtLTtcbiAgICAgIHByZXYgPSBuZXh0O1xuICAgIH1cbiAgICBpZiAoc3RhdGUuY29tbWVudExldmVsIDw9IDApIHtcbiAgICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlO1xuICAgIH1cbiAgICByZXR1cm4gJ2NvbW1lbnQnO1xuICB9XG4gIGZ1bmN0aW9uIHRva2VuTG9uZ1N0cmluZyhzdHJlYW0sIHN0YXRlKSB7XG4gICAgdmFyIHByZXYsIG5leHQ7XG4gICAgd2hpbGUgKHN0YXRlLmxvbmdTdHJpbmcgJiYgKG5leHQgPSBzdHJlYW0ubmV4dCgpKSAhPSBudWxsKSB7XG4gICAgICBpZiAocHJldiA9PT0gJ3wnICYmIG5leHQgPT09ICd9Jykgc3RhdGUubG9uZ1N0cmluZyA9IGZhbHNlO1xuICAgICAgcHJldiA9IG5leHQ7XG4gICAgfVxuICAgIGlmICghc3RhdGUubG9uZ1N0cmluZykge1xuICAgICAgc3RhdGUudG9rZW5pemUgPSB0b2tlbkJhc2U7XG4gICAgfVxuICAgIHJldHVybiAnc3RyaW5nJztcbiAgfVxuICByZXR1cm4ge1xuICAgIHN0YXJ0U3RhdGU6IGZ1bmN0aW9uICgpIHtcbiAgICAgIHJldHVybiB7XG4gICAgICAgIHRva2VuaXplOiB0b2tlbkJhc2UsXG4gICAgICAgIGNvbW1lbnRMZXZlbDogMCxcbiAgICAgICAgbG9uZ1N0cmluZzogZmFsc2VcbiAgICAgIH07XG4gICAgfSxcbiAgICB0b2tlbjogZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICAgIGlmIChzdHJlYW0uZWF0U3BhY2UoKSkgcmV0dXJuIG51bGw7XG4gICAgICByZXR1cm4gc3RhdGUudG9rZW5pemUoc3RyZWFtLCBzdGF0ZSk7XG4gICAgfSxcbiAgICBsYW5ndWFnZURhdGE6IHtcbiAgICAgIGF1dG9jb21wbGV0ZTogaGludFdvcmRzLFxuICAgICAgY29tbWVudFRva2Vuczoge1xuICAgICAgICBsaW5lOiBwYXJzZXJDb25maWcuc2xhc2hDb21tZW50cyA/IFwiLy9cIiA6IHVuZGVmaW5lZCxcbiAgICAgICAgYmxvY2s6IHtcbiAgICAgICAgICBvcGVuOiBcIigqXCIsXG4gICAgICAgICAgY2xvc2U6IFwiKilcIlxuICAgICAgICB9XG4gICAgICB9XG4gICAgfVxuICB9O1xufVxuO1xuZXhwb3J0IGNvbnN0IG9DYW1sID0gbWxMaWtlKHtcbiAgbmFtZTogXCJvY2FtbFwiLFxuICBleHRyYVdvcmRzOiB7XG4gICAgJ2FuZCc6ICdrZXl3b3JkJyxcbiAgICAnYXNzZXJ0JzogJ2tleXdvcmQnLFxuICAgICdiZWdpbic6ICdrZXl3b3JkJyxcbiAgICAnY2xhc3MnOiAna2V5d29yZCcsXG4gICAgJ2NvbnN0cmFpbnQnOiAna2V5d29yZCcsXG4gICAgJ2RvbmUnOiAna2V5d29yZCcsXG4gICAgJ2Rvd250byc6ICdrZXl3b3JkJyxcbiAgICAnZXh0ZXJuYWwnOiAna2V5d29yZCcsXG4gICAgJ2Z1bmN0aW9uJzogJ2tleXdvcmQnLFxuICAgICdpbml0aWFsaXplcic6ICdrZXl3b3JkJyxcbiAgICAnbGF6eSc6ICdrZXl3b3JkJyxcbiAgICAnbWF0Y2gnOiAna2V5d29yZCcsXG4gICAgJ21ldGhvZCc6ICdrZXl3b3JkJyxcbiAgICAnbW9kdWxlJzogJ2tleXdvcmQnLFxuICAgICdtdXRhYmxlJzogJ2tleXdvcmQnLFxuICAgICduZXcnOiAna2V5d29yZCcsXG4gICAgJ25vbnJlYyc6ICdrZXl3b3JkJyxcbiAgICAnb2JqZWN0JzogJ2tleXdvcmQnLFxuICAgICdwcml2YXRlJzogJ2tleXdvcmQnLFxuICAgICdzaWcnOiAna2V5d29yZCcsXG4gICAgJ3RvJzogJ2tleXdvcmQnLFxuICAgICd0cnknOiAna2V5d29yZCcsXG4gICAgJ3ZhbHVlJzogJ2tleXdvcmQnLFxuICAgICd2aXJ0dWFsJzogJ2tleXdvcmQnLFxuICAgICd3aGVuJzogJ2tleXdvcmQnLFxuICAgIC8vIGJ1aWx0aW5zXG4gICAgJ3JhaXNlJzogJ2J1aWx0aW4nLFxuICAgICdmYWlsd2l0aCc6ICdidWlsdGluJyxcbiAgICAndHJ1ZSc6ICdidWlsdGluJyxcbiAgICAnZmFsc2UnOiAnYnVpbHRpbicsXG4gICAgLy8gUGVydmFzaXZlcyBidWlsdGluc1xuICAgICdhc3InOiAnYnVpbHRpbicsXG4gICAgJ2xhbmQnOiAnYnVpbHRpbicsXG4gICAgJ2xvcic6ICdidWlsdGluJyxcbiAgICAnbHNsJzogJ2J1aWx0aW4nLFxuICAgICdsc3InOiAnYnVpbHRpbicsXG4gICAgJ2x4b3InOiAnYnVpbHRpbicsXG4gICAgJ21vZCc6ICdidWlsdGluJyxcbiAgICAnb3InOiAnYnVpbHRpbicsXG4gICAgLy8gTW9yZSBQZXJ2YXNpdmVzXG4gICAgJ3JhaXNlX25vdHJhY2UnOiAnYnVpbHRpbicsXG4gICAgJ3RyYWNlJzogJ2J1aWx0aW4nLFxuICAgICdleGl0JzogJ2J1aWx0aW4nLFxuICAgICdwcmludF9zdHJpbmcnOiAnYnVpbHRpbicsXG4gICAgJ3ByaW50X2VuZGxpbmUnOiAnYnVpbHRpbicsXG4gICAgJ2ludCc6ICd0eXBlJyxcbiAgICAnZmxvYXQnOiAndHlwZScsXG4gICAgJ2Jvb2wnOiAndHlwZScsXG4gICAgJ2NoYXInOiAndHlwZScsXG4gICAgJ3N0cmluZyc6ICd0eXBlJyxcbiAgICAndW5pdCc6ICd0eXBlJyxcbiAgICAvLyBNb2R1bGVzXG4gICAgJ0xpc3QnOiAnYnVpbHRpbidcbiAgfVxufSk7XG5leHBvcnQgY29uc3QgZlNoYXJwID0gbWxMaWtlKHtcbiAgbmFtZTogXCJmc2hhcnBcIixcbiAgZXh0cmFXb3Jkczoge1xuICAgICdhYnN0cmFjdCc6ICdrZXl3b3JkJyxcbiAgICAnYXNzZXJ0JzogJ2tleXdvcmQnLFxuICAgICdiYXNlJzogJ2tleXdvcmQnLFxuICAgICdiZWdpbic6ICdrZXl3b3JkJyxcbiAgICAnY2xhc3MnOiAna2V5d29yZCcsXG4gICAgJ2RlZmF1bHQnOiAna2V5d29yZCcsXG4gICAgJ2RlbGVnYXRlJzogJ2tleXdvcmQnLFxuICAgICdkbyEnOiAna2V5d29yZCcsXG4gICAgJ2RvbmUnOiAna2V5d29yZCcsXG4gICAgJ2Rvd25jYXN0JzogJ2tleXdvcmQnLFxuICAgICdkb3dudG8nOiAna2V5d29yZCcsXG4gICAgJ2VsaWYnOiAna2V5d29yZCcsXG4gICAgJ2V4dGVybic6ICdrZXl3b3JkJyxcbiAgICAnZmluYWxseSc6ICdrZXl3b3JkJyxcbiAgICAnZm9yJzogJ2tleXdvcmQnLFxuICAgICdmdW5jdGlvbic6ICdrZXl3b3JkJyxcbiAgICAnZ2xvYmFsJzogJ2tleXdvcmQnLFxuICAgICdpbmhlcml0JzogJ2tleXdvcmQnLFxuICAgICdpbmxpbmUnOiAna2V5d29yZCcsXG4gICAgJ2ludGVyZmFjZSc6ICdrZXl3b3JkJyxcbiAgICAnaW50ZXJuYWwnOiAna2V5d29yZCcsXG4gICAgJ2xhenknOiAna2V5d29yZCcsXG4gICAgJ2xldCEnOiAna2V5d29yZCcsXG4gICAgJ21hdGNoJzogJ2tleXdvcmQnLFxuICAgICdtZW1iZXInOiAna2V5d29yZCcsXG4gICAgJ21vZHVsZSc6ICdrZXl3b3JkJyxcbiAgICAnbXV0YWJsZSc6ICdrZXl3b3JkJyxcbiAgICAnbmFtZXNwYWNlJzogJ2tleXdvcmQnLFxuICAgICduZXcnOiAna2V5d29yZCcsXG4gICAgJ251bGwnOiAna2V5d29yZCcsXG4gICAgJ292ZXJyaWRlJzogJ2tleXdvcmQnLFxuICAgICdwcml2YXRlJzogJ2tleXdvcmQnLFxuICAgICdwdWJsaWMnOiAna2V5d29yZCcsXG4gICAgJ3JldHVybiEnOiAna2V5d29yZCcsXG4gICAgJ3JldHVybic6ICdrZXl3b3JkJyxcbiAgICAnc2VsZWN0JzogJ2tleXdvcmQnLFxuICAgICdzdGF0aWMnOiAna2V5d29yZCcsXG4gICAgJ3RvJzogJ2tleXdvcmQnLFxuICAgICd0cnknOiAna2V5d29yZCcsXG4gICAgJ3VwY2FzdCc6ICdrZXl3b3JkJyxcbiAgICAndXNlISc6ICdrZXl3b3JkJyxcbiAgICAndXNlJzogJ2tleXdvcmQnLFxuICAgICd2b2lkJzogJ2tleXdvcmQnLFxuICAgICd3aGVuJzogJ2tleXdvcmQnLFxuICAgICd5aWVsZCEnOiAna2V5d29yZCcsXG4gICAgJ3lpZWxkJzogJ2tleXdvcmQnLFxuICAgIC8vIFJlc2VydmVkIHdvcmRzXG4gICAgJ2F0b21pYyc6ICdrZXl3b3JkJyxcbiAgICAnYnJlYWsnOiAna2V5d29yZCcsXG4gICAgJ2NoZWNrZWQnOiAna2V5d29yZCcsXG4gICAgJ2NvbXBvbmVudCc6ICdrZXl3b3JkJyxcbiAgICAnY29uc3QnOiAna2V5d29yZCcsXG4gICAgJ2NvbnN0cmFpbnQnOiAna2V5d29yZCcsXG4gICAgJ2NvbnN0cnVjdG9yJzogJ2tleXdvcmQnLFxuICAgICdjb250aW51ZSc6ICdrZXl3b3JkJyxcbiAgICAnZWFnZXInOiAna2V5d29yZCcsXG4gICAgJ2V2ZW50JzogJ2tleXdvcmQnLFxuICAgICdleHRlcm5hbCc6ICdrZXl3b3JkJyxcbiAgICAnZml4ZWQnOiAna2V5d29yZCcsXG4gICAgJ21ldGhvZCc6ICdrZXl3b3JkJyxcbiAgICAnbWl4aW4nOiAna2V5d29yZCcsXG4gICAgJ29iamVjdCc6ICdrZXl3b3JkJyxcbiAgICAncGFyYWxsZWwnOiAna2V5d29yZCcsXG4gICAgJ3Byb2Nlc3MnOiAna2V5d29yZCcsXG4gICAgJ3Byb3RlY3RlZCc6ICdrZXl3b3JkJyxcbiAgICAncHVyZSc6ICdrZXl3b3JkJyxcbiAgICAnc2VhbGVkJzogJ2tleXdvcmQnLFxuICAgICd0YWlsY2FsbCc6ICdrZXl3b3JkJyxcbiAgICAndHJhaXQnOiAna2V5d29yZCcsXG4gICAgJ3ZpcnR1YWwnOiAna2V5d29yZCcsXG4gICAgJ3ZvbGF0aWxlJzogJ2tleXdvcmQnLFxuICAgIC8vIGJ1aWx0aW5zXG4gICAgJ0xpc3QnOiAnYnVpbHRpbicsXG4gICAgJ1NlcSc6ICdidWlsdGluJyxcbiAgICAnTWFwJzogJ2J1aWx0aW4nLFxuICAgICdTZXQnOiAnYnVpbHRpbicsXG4gICAgJ09wdGlvbic6ICdidWlsdGluJyxcbiAgICAnaW50JzogJ2J1aWx0aW4nLFxuICAgICdzdHJpbmcnOiAnYnVpbHRpbicsXG4gICAgJ25vdCc6ICdidWlsdGluJyxcbiAgICAndHJ1ZSc6ICdidWlsdGluJyxcbiAgICAnZmFsc2UnOiAnYnVpbHRpbicsXG4gICAgJ3JhaXNlJzogJ2J1aWx0aW4nLFxuICAgICdmYWlsd2l0aCc6ICdidWlsdGluJ1xuICB9LFxuICBzbGFzaENvbW1lbnRzOiB0cnVlXG59KTtcbmV4cG9ydCBjb25zdCBzbWwgPSBtbExpa2Uoe1xuICBuYW1lOiBcInNtbFwiLFxuICBleHRyYVdvcmRzOiB7XG4gICAgJ2Fic3R5cGUnOiAna2V5d29yZCcsXG4gICAgJ2FuZCc6ICdrZXl3b3JkJyxcbiAgICAnYW5kYWxzbyc6ICdrZXl3b3JkJyxcbiAgICAnY2FzZSc6ICdrZXl3b3JkJyxcbiAgICAnZGF0YXR5cGUnOiAna2V5d29yZCcsXG4gICAgJ2ZuJzogJ2tleXdvcmQnLFxuICAgICdoYW5kbGUnOiAna2V5d29yZCcsXG4gICAgJ2luZml4JzogJ2tleXdvcmQnLFxuICAgICdpbmZpeHInOiAna2V5d29yZCcsXG4gICAgJ2xvY2FsJzogJ2tleXdvcmQnLFxuICAgICdub25maXgnOiAna2V5d29yZCcsXG4gICAgJ29wJzogJ2tleXdvcmQnLFxuICAgICdvcmVsc2UnOiAna2V5d29yZCcsXG4gICAgJ3JhaXNlJzogJ2tleXdvcmQnLFxuICAgICd3aXRodHlwZSc6ICdrZXl3b3JkJyxcbiAgICAnZXF0eXBlJzogJ2tleXdvcmQnLFxuICAgICdzaGFyaW5nJzogJ2tleXdvcmQnLFxuICAgICdzaWcnOiAna2V5d29yZCcsXG4gICAgJ3NpZ25hdHVyZSc6ICdrZXl3b3JkJyxcbiAgICAnc3RydWN0dXJlJzogJ2tleXdvcmQnLFxuICAgICd3aGVyZSc6ICdrZXl3b3JkJyxcbiAgICAndHJ1ZSc6ICdrZXl3b3JkJyxcbiAgICAnZmFsc2UnOiAna2V5d29yZCcsXG4gICAgLy8gdHlwZXNcbiAgICAnaW50JzogJ2J1aWx0aW4nLFxuICAgICdyZWFsJzogJ2J1aWx0aW4nLFxuICAgICdzdHJpbmcnOiAnYnVpbHRpbicsXG4gICAgJ2NoYXInOiAnYnVpbHRpbicsXG4gICAgJ2Jvb2wnOiAnYnVpbHRpbidcbiAgfSxcbiAgc2xhc2hDb21tZW50czogdHJ1ZVxufSk7Il0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9