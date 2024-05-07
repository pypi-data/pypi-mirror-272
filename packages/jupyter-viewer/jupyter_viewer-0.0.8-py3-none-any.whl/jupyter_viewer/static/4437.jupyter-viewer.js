"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[4437],{

/***/ 94637:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "liveScript": () => (/* binding */ liveScript)
/* harmony export */ });
var tokenBase = function (stream, state) {
  var next_rule = state.next || "start";
  if (next_rule) {
    state.next = state.next;
    var nr = Rules[next_rule];
    if (nr.splice) {
      for (var i$ = 0; i$ < nr.length; ++i$) {
        var r = nr[i$];
        if (r.regex && stream.match(r.regex)) {
          state.next = r.next || state.next;
          return r.token;
        }
      }
      stream.next();
      return 'error';
    }
    if (stream.match(r = Rules[next_rule])) {
      if (r.regex && stream.match(r.regex)) {
        state.next = r.next;
        return r.token;
      } else {
        stream.next();
        return 'error';
      }
    }
  }
  stream.next();
  return 'error';
};
var identifier = '(?![\\d\\s])[$\\w\\xAA-\\uFFDC](?:(?!\\s)[$\\w\\xAA-\\uFFDC]|-[A-Za-z])*';
var indenter = RegExp('(?:[({[=:]|[-~]>|\\b(?:e(?:lse|xport)|d(?:o|efault)|t(?:ry|hen)|finally|import(?:\\s*all)?|const|var|let|new|catch(?:\\s*' + identifier + ')?))\\s*$');
var keywordend = '(?![$\\w]|-[A-Za-z]|\\s*:(?![:=]))';
var stringfill = {
  token: 'string',
  regex: '.+'
};
var Rules = {
  start: [{
    token: 'docComment',
    regex: '/\\*',
    next: 'comment'
  }, {
    token: 'comment',
    regex: '#.*'
  }, {
    token: 'keyword',
    regex: '(?:t(?:h(?:is|row|en)|ry|ypeof!?)|c(?:on(?:tinue|st)|a(?:se|tch)|lass)|i(?:n(?:stanceof)?|mp(?:ort(?:\\s+all)?|lements)|[fs])|d(?:e(?:fault|lete|bugger)|o)|f(?:or(?:\\s+own)?|inally|unction)|s(?:uper|witch)|e(?:lse|x(?:tends|port)|val)|a(?:nd|rguments)|n(?:ew|ot)|un(?:less|til)|w(?:hile|ith)|o[fr]|return|break|let|var|loop)' + keywordend
  }, {
    token: 'atom',
    regex: '(?:true|false|yes|no|on|off|null|void|undefined)' + keywordend
  }, {
    token: 'invalid',
    regex: '(?:p(?:ackage|r(?:ivate|otected)|ublic)|i(?:mplements|nterface)|enum|static|yield)' + keywordend
  }, {
    token: 'className.standard',
    regex: '(?:R(?:e(?:gExp|ferenceError)|angeError)|S(?:tring|yntaxError)|E(?:rror|valError)|Array|Boolean|Date|Function|Number|Object|TypeError|URIError)' + keywordend
  }, {
    token: 'variableName.function.standard',
    regex: '(?:is(?:NaN|Finite)|parse(?:Int|Float)|Math|JSON|(?:en|de)codeURI(?:Component)?)' + keywordend
  }, {
    token: 'variableName.standard',
    regex: '(?:t(?:hat|il|o)|f(?:rom|allthrough)|it|by|e)' + keywordend
  }, {
    token: 'variableName',
    regex: identifier + '\\s*:(?![:=])'
  }, {
    token: 'variableName',
    regex: identifier
  }, {
    token: 'operatorKeyword',
    regex: '(?:\\.{3}|\\s+\\?)'
  }, {
    token: 'keyword',
    regex: '(?:@+|::|\\.\\.)',
    next: 'key'
  }, {
    token: 'operatorKeyword',
    regex: '\\.\\s*',
    next: 'key'
  }, {
    token: 'string',
    regex: '\\\\\\S[^\\s,;)}\\]]*'
  }, {
    token: 'docString',
    regex: '\'\'\'',
    next: 'qdoc'
  }, {
    token: 'docString',
    regex: '"""',
    next: 'qqdoc'
  }, {
    token: 'string',
    regex: '\'',
    next: 'qstring'
  }, {
    token: 'string',
    regex: '"',
    next: 'qqstring'
  }, {
    token: 'string',
    regex: '`',
    next: 'js'
  }, {
    token: 'string',
    regex: '<\\[',
    next: 'words'
  }, {
    token: 'regexp',
    regex: '//',
    next: 'heregex'
  }, {
    token: 'regexp',
    regex: '\\/(?:[^[\\/\\n\\\\]*(?:(?:\\\\.|\\[[^\\]\\n\\\\]*(?:\\\\.[^\\]\\n\\\\]*)*\\])[^[\\/\\n\\\\]*)*)\\/[gimy$]{0,4}',
    next: 'key'
  }, {
    token: 'number',
    regex: '(?:0x[\\da-fA-F][\\da-fA-F_]*|(?:[2-9]|[12]\\d|3[0-6])r[\\da-zA-Z][\\da-zA-Z_]*|(?:\\d[\\d_]*(?:\\.\\d[\\d_]*)?|\\.\\d[\\d_]*)(?:e[+-]?\\d[\\d_]*)?[\\w$]*)'
  }, {
    token: 'paren',
    regex: '[({[]'
  }, {
    token: 'paren',
    regex: '[)}\\]]',
    next: 'key'
  }, {
    token: 'operatorKeyword',
    regex: '\\S+'
  }, {
    token: 'content',
    regex: '\\s+'
  }],
  heregex: [{
    token: 'regexp',
    regex: '.*?//[gimy$?]{0,4}',
    next: 'start'
  }, {
    token: 'regexp',
    regex: '\\s*#{'
  }, {
    token: 'comment',
    regex: '\\s+(?:#.*)?'
  }, {
    token: 'regexp',
    regex: '\\S+'
  }],
  key: [{
    token: 'operatorKeyword',
    regex: '[.?@!]+'
  }, {
    token: 'variableName',
    regex: identifier,
    next: 'start'
  }, {
    token: 'content',
    regex: '',
    next: 'start'
  }],
  comment: [{
    token: 'docComment',
    regex: '.*?\\*/',
    next: 'start'
  }, {
    token: 'docComment',
    regex: '.+'
  }],
  qdoc: [{
    token: 'string',
    regex: ".*?'''",
    next: 'key'
  }, stringfill],
  qqdoc: [{
    token: 'string',
    regex: '.*?"""',
    next: 'key'
  }, stringfill],
  qstring: [{
    token: 'string',
    regex: '[^\\\\\']*(?:\\\\.[^\\\\\']*)*\'',
    next: 'key'
  }, stringfill],
  qqstring: [{
    token: 'string',
    regex: '[^\\\\"]*(?:\\\\.[^\\\\"]*)*"',
    next: 'key'
  }, stringfill],
  js: [{
    token: 'string',
    regex: '[^\\\\`]*(?:\\\\.[^\\\\`]*)*`',
    next: 'key'
  }, stringfill],
  words: [{
    token: 'string',
    regex: '.*?\\]>',
    next: 'key'
  }, stringfill]
};
for (var idx in Rules) {
  var r = Rules[idx];
  if (r.splice) {
    for (var i = 0, len = r.length; i < len; ++i) {
      var rr = r[i];
      if (typeof rr.regex === 'string') {
        Rules[idx][i].regex = new RegExp('^' + rr.regex);
      }
    }
  } else if (typeof rr.regex === 'string') {
    Rules[idx].regex = new RegExp('^' + r.regex);
  }
}
const liveScript = {
  name: "livescript",
  startState: function () {
    return {
      next: 'start',
      lastToken: {
        style: null,
        indent: 0,
        content: ""
      }
    };
  },
  token: function (stream, state) {
    while (stream.pos == stream.start) var style = tokenBase(stream, state);
    state.lastToken = {
      style: style,
      indent: stream.indentation(),
      content: stream.current()
    };
    return style.replace(/\./g, ' ');
  },
  indent: function (state) {
    var indentation = state.lastToken.indent;
    if (state.lastToken.content.match(indenter)) {
      indentation += 2;
    }
    return indentation;
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNDQzNy5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL0Bjb2RlbWlycm9yL2xlZ2FjeS1tb2Rlcy9tb2RlL2xpdmVzY3JpcHQuanMiXSwic291cmNlc0NvbnRlbnQiOlsidmFyIHRva2VuQmFzZSA9IGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gIHZhciBuZXh0X3J1bGUgPSBzdGF0ZS5uZXh0IHx8IFwic3RhcnRcIjtcbiAgaWYgKG5leHRfcnVsZSkge1xuICAgIHN0YXRlLm5leHQgPSBzdGF0ZS5uZXh0O1xuICAgIHZhciBuciA9IFJ1bGVzW25leHRfcnVsZV07XG4gICAgaWYgKG5yLnNwbGljZSkge1xuICAgICAgZm9yICh2YXIgaSQgPSAwOyBpJCA8IG5yLmxlbmd0aDsgKytpJCkge1xuICAgICAgICB2YXIgciA9IG5yW2kkXTtcbiAgICAgICAgaWYgKHIucmVnZXggJiYgc3RyZWFtLm1hdGNoKHIucmVnZXgpKSB7XG4gICAgICAgICAgc3RhdGUubmV4dCA9IHIubmV4dCB8fCBzdGF0ZS5uZXh0O1xuICAgICAgICAgIHJldHVybiByLnRva2VuO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgICBzdHJlYW0ubmV4dCgpO1xuICAgICAgcmV0dXJuICdlcnJvcic7XG4gICAgfVxuICAgIGlmIChzdHJlYW0ubWF0Y2gociA9IFJ1bGVzW25leHRfcnVsZV0pKSB7XG4gICAgICBpZiAoci5yZWdleCAmJiBzdHJlYW0ubWF0Y2goci5yZWdleCkpIHtcbiAgICAgICAgc3RhdGUubmV4dCA9IHIubmV4dDtcbiAgICAgICAgcmV0dXJuIHIudG9rZW47XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBzdHJlYW0ubmV4dCgpO1xuICAgICAgICByZXR1cm4gJ2Vycm9yJztcbiAgICAgIH1cbiAgICB9XG4gIH1cbiAgc3RyZWFtLm5leHQoKTtcbiAgcmV0dXJuICdlcnJvcic7XG59O1xudmFyIGlkZW50aWZpZXIgPSAnKD8hW1xcXFxkXFxcXHNdKVskXFxcXHdcXFxceEFBLVxcXFx1RkZEQ10oPzooPyFcXFxccylbJFxcXFx3XFxcXHhBQS1cXFxcdUZGRENdfC1bQS1aYS16XSkqJztcbnZhciBpbmRlbnRlciA9IFJlZ0V4cCgnKD86Wyh7Wz06XXxbLX5dPnxcXFxcYig/OmUoPzpsc2V8eHBvcnQpfGQoPzpvfGVmYXVsdCl8dCg/OnJ5fGhlbil8ZmluYWxseXxpbXBvcnQoPzpcXFxccyphbGwpP3xjb25zdHx2YXJ8bGV0fG5ld3xjYXRjaCg/OlxcXFxzKicgKyBpZGVudGlmaWVyICsgJyk/KSlcXFxccyokJyk7XG52YXIga2V5d29yZGVuZCA9ICcoPyFbJFxcXFx3XXwtW0EtWmEtel18XFxcXHMqOig/IVs6PV0pKSc7XG52YXIgc3RyaW5nZmlsbCA9IHtcbiAgdG9rZW46ICdzdHJpbmcnLFxuICByZWdleDogJy4rJ1xufTtcbnZhciBSdWxlcyA9IHtcbiAgc3RhcnQ6IFt7XG4gICAgdG9rZW46ICdkb2NDb21tZW50JyxcbiAgICByZWdleDogJy9cXFxcKicsXG4gICAgbmV4dDogJ2NvbW1lbnQnXG4gIH0sIHtcbiAgICB0b2tlbjogJ2NvbW1lbnQnLFxuICAgIHJlZ2V4OiAnIy4qJ1xuICB9LCB7XG4gICAgdG9rZW46ICdrZXl3b3JkJyxcbiAgICByZWdleDogJyg/OnQoPzpoKD86aXN8cm93fGVuKXxyeXx5cGVvZiE/KXxjKD86b24oPzp0aW51ZXxzdCl8YSg/OnNlfHRjaCl8bGFzcyl8aSg/Om4oPzpzdGFuY2VvZik/fG1wKD86b3J0KD86XFxcXHMrYWxsKT98bGVtZW50cyl8W2ZzXSl8ZCg/OmUoPzpmYXVsdHxsZXRlfGJ1Z2dlcil8byl8Zig/Om9yKD86XFxcXHMrb3duKT98aW5hbGx5fHVuY3Rpb24pfHMoPzp1cGVyfHdpdGNoKXxlKD86bHNlfHgoPzp0ZW5kc3xwb3J0KXx2YWwpfGEoPzpuZHxyZ3VtZW50cyl8big/OmV3fG90KXx1big/Omxlc3N8dGlsKXx3KD86aGlsZXxpdGgpfG9bZnJdfHJldHVybnxicmVha3xsZXR8dmFyfGxvb3ApJyArIGtleXdvcmRlbmRcbiAgfSwge1xuICAgIHRva2VuOiAnYXRvbScsXG4gICAgcmVnZXg6ICcoPzp0cnVlfGZhbHNlfHllc3xub3xvbnxvZmZ8bnVsbHx2b2lkfHVuZGVmaW5lZCknICsga2V5d29yZGVuZFxuICB9LCB7XG4gICAgdG9rZW46ICdpbnZhbGlkJyxcbiAgICByZWdleDogJyg/OnAoPzphY2thZ2V8cig/Oml2YXRlfG90ZWN0ZWQpfHVibGljKXxpKD86bXBsZW1lbnRzfG50ZXJmYWNlKXxlbnVtfHN0YXRpY3x5aWVsZCknICsga2V5d29yZGVuZFxuICB9LCB7XG4gICAgdG9rZW46ICdjbGFzc05hbWUuc3RhbmRhcmQnLFxuICAgIHJlZ2V4OiAnKD86Uig/OmUoPzpnRXhwfGZlcmVuY2VFcnJvcil8YW5nZUVycm9yKXxTKD86dHJpbmd8eW50YXhFcnJvcil8RSg/OnJyb3J8dmFsRXJyb3IpfEFycmF5fEJvb2xlYW58RGF0ZXxGdW5jdGlvbnxOdW1iZXJ8T2JqZWN0fFR5cGVFcnJvcnxVUklFcnJvciknICsga2V5d29yZGVuZFxuICB9LCB7XG4gICAgdG9rZW46ICd2YXJpYWJsZU5hbWUuZnVuY3Rpb24uc3RhbmRhcmQnLFxuICAgIHJlZ2V4OiAnKD86aXMoPzpOYU58RmluaXRlKXxwYXJzZSg/OkludHxGbG9hdCl8TWF0aHxKU09OfCg/OmVufGRlKWNvZGVVUkkoPzpDb21wb25lbnQpPyknICsga2V5d29yZGVuZFxuICB9LCB7XG4gICAgdG9rZW46ICd2YXJpYWJsZU5hbWUuc3RhbmRhcmQnLFxuICAgIHJlZ2V4OiAnKD86dCg/OmhhdHxpbHxvKXxmKD86cm9tfGFsbHRocm91Z2gpfGl0fGJ5fGUpJyArIGtleXdvcmRlbmRcbiAgfSwge1xuICAgIHRva2VuOiAndmFyaWFibGVOYW1lJyxcbiAgICByZWdleDogaWRlbnRpZmllciArICdcXFxccyo6KD8hWzo9XSknXG4gIH0sIHtcbiAgICB0b2tlbjogJ3ZhcmlhYmxlTmFtZScsXG4gICAgcmVnZXg6IGlkZW50aWZpZXJcbiAgfSwge1xuICAgIHRva2VuOiAnb3BlcmF0b3JLZXl3b3JkJyxcbiAgICByZWdleDogJyg/OlxcXFwuezN9fFxcXFxzK1xcXFw/KSdcbiAgfSwge1xuICAgIHRva2VuOiAna2V5d29yZCcsXG4gICAgcmVnZXg6ICcoPzpAK3w6OnxcXFxcLlxcXFwuKScsXG4gICAgbmV4dDogJ2tleSdcbiAgfSwge1xuICAgIHRva2VuOiAnb3BlcmF0b3JLZXl3b3JkJyxcbiAgICByZWdleDogJ1xcXFwuXFxcXHMqJyxcbiAgICBuZXh0OiAna2V5J1xuICB9LCB7XG4gICAgdG9rZW46ICdzdHJpbmcnLFxuICAgIHJlZ2V4OiAnXFxcXFxcXFxcXFxcU1teXFxcXHMsOyl9XFxcXF1dKidcbiAgfSwge1xuICAgIHRva2VuOiAnZG9jU3RyaW5nJyxcbiAgICByZWdleDogJ1xcJ1xcJ1xcJycsXG4gICAgbmV4dDogJ3Fkb2MnXG4gIH0sIHtcbiAgICB0b2tlbjogJ2RvY1N0cmluZycsXG4gICAgcmVnZXg6ICdcIlwiXCInLFxuICAgIG5leHQ6ICdxcWRvYydcbiAgfSwge1xuICAgIHRva2VuOiAnc3RyaW5nJyxcbiAgICByZWdleDogJ1xcJycsXG4gICAgbmV4dDogJ3FzdHJpbmcnXG4gIH0sIHtcbiAgICB0b2tlbjogJ3N0cmluZycsXG4gICAgcmVnZXg6ICdcIicsXG4gICAgbmV4dDogJ3Fxc3RyaW5nJ1xuICB9LCB7XG4gICAgdG9rZW46ICdzdHJpbmcnLFxuICAgIHJlZ2V4OiAnYCcsXG4gICAgbmV4dDogJ2pzJ1xuICB9LCB7XG4gICAgdG9rZW46ICdzdHJpbmcnLFxuICAgIHJlZ2V4OiAnPFxcXFxbJyxcbiAgICBuZXh0OiAnd29yZHMnXG4gIH0sIHtcbiAgICB0b2tlbjogJ3JlZ2V4cCcsXG4gICAgcmVnZXg6ICcvLycsXG4gICAgbmV4dDogJ2hlcmVnZXgnXG4gIH0sIHtcbiAgICB0b2tlbjogJ3JlZ2V4cCcsXG4gICAgcmVnZXg6ICdcXFxcLyg/OlteW1xcXFwvXFxcXG5cXFxcXFxcXF0qKD86KD86XFxcXFxcXFwufFxcXFxbW15cXFxcXVxcXFxuXFxcXFxcXFxdKig/OlxcXFxcXFxcLlteXFxcXF1cXFxcblxcXFxcXFxcXSopKlxcXFxdKVteW1xcXFwvXFxcXG5cXFxcXFxcXF0qKSopXFxcXC9bZ2lteSRdezAsNH0nLFxuICAgIG5leHQ6ICdrZXknXG4gIH0sIHtcbiAgICB0b2tlbjogJ251bWJlcicsXG4gICAgcmVnZXg6ICcoPzoweFtcXFxcZGEtZkEtRl1bXFxcXGRhLWZBLUZfXSp8KD86WzItOV18WzEyXVxcXFxkfDNbMC02XSlyW1xcXFxkYS16QS1aXVtcXFxcZGEtekEtWl9dKnwoPzpcXFxcZFtcXFxcZF9dKig/OlxcXFwuXFxcXGRbXFxcXGRfXSopP3xcXFxcLlxcXFxkW1xcXFxkX10qKSg/OmVbKy1dP1xcXFxkW1xcXFxkX10qKT9bXFxcXHckXSopJ1xuICB9LCB7XG4gICAgdG9rZW46ICdwYXJlbicsXG4gICAgcmVnZXg6ICdbKHtbXSdcbiAgfSwge1xuICAgIHRva2VuOiAncGFyZW4nLFxuICAgIHJlZ2V4OiAnWyl9XFxcXF1dJyxcbiAgICBuZXh0OiAna2V5J1xuICB9LCB7XG4gICAgdG9rZW46ICdvcGVyYXRvcktleXdvcmQnLFxuICAgIHJlZ2V4OiAnXFxcXFMrJ1xuICB9LCB7XG4gICAgdG9rZW46ICdjb250ZW50JyxcbiAgICByZWdleDogJ1xcXFxzKydcbiAgfV0sXG4gIGhlcmVnZXg6IFt7XG4gICAgdG9rZW46ICdyZWdleHAnLFxuICAgIHJlZ2V4OiAnLio/Ly9bZ2lteSQ/XXswLDR9JyxcbiAgICBuZXh0OiAnc3RhcnQnXG4gIH0sIHtcbiAgICB0b2tlbjogJ3JlZ2V4cCcsXG4gICAgcmVnZXg6ICdcXFxccyojeydcbiAgfSwge1xuICAgIHRva2VuOiAnY29tbWVudCcsXG4gICAgcmVnZXg6ICdcXFxccysoPzojLiopPydcbiAgfSwge1xuICAgIHRva2VuOiAncmVnZXhwJyxcbiAgICByZWdleDogJ1xcXFxTKydcbiAgfV0sXG4gIGtleTogW3tcbiAgICB0b2tlbjogJ29wZXJhdG9yS2V5d29yZCcsXG4gICAgcmVnZXg6ICdbLj9AIV0rJ1xuICB9LCB7XG4gICAgdG9rZW46ICd2YXJpYWJsZU5hbWUnLFxuICAgIHJlZ2V4OiBpZGVudGlmaWVyLFxuICAgIG5leHQ6ICdzdGFydCdcbiAgfSwge1xuICAgIHRva2VuOiAnY29udGVudCcsXG4gICAgcmVnZXg6ICcnLFxuICAgIG5leHQ6ICdzdGFydCdcbiAgfV0sXG4gIGNvbW1lbnQ6IFt7XG4gICAgdG9rZW46ICdkb2NDb21tZW50JyxcbiAgICByZWdleDogJy4qP1xcXFwqLycsXG4gICAgbmV4dDogJ3N0YXJ0J1xuICB9LCB7XG4gICAgdG9rZW46ICdkb2NDb21tZW50JyxcbiAgICByZWdleDogJy4rJ1xuICB9XSxcbiAgcWRvYzogW3tcbiAgICB0b2tlbjogJ3N0cmluZycsXG4gICAgcmVnZXg6IFwiLio/JycnXCIsXG4gICAgbmV4dDogJ2tleSdcbiAgfSwgc3RyaW5nZmlsbF0sXG4gIHFxZG9jOiBbe1xuICAgIHRva2VuOiAnc3RyaW5nJyxcbiAgICByZWdleDogJy4qP1wiXCJcIicsXG4gICAgbmV4dDogJ2tleSdcbiAgfSwgc3RyaW5nZmlsbF0sXG4gIHFzdHJpbmc6IFt7XG4gICAgdG9rZW46ICdzdHJpbmcnLFxuICAgIHJlZ2V4OiAnW15cXFxcXFxcXFxcJ10qKD86XFxcXFxcXFwuW15cXFxcXFxcXFxcJ10qKSpcXCcnLFxuICAgIG5leHQ6ICdrZXknXG4gIH0sIHN0cmluZ2ZpbGxdLFxuICBxcXN0cmluZzogW3tcbiAgICB0b2tlbjogJ3N0cmluZycsXG4gICAgcmVnZXg6ICdbXlxcXFxcXFxcXCJdKig/OlxcXFxcXFxcLlteXFxcXFxcXFxcIl0qKSpcIicsXG4gICAgbmV4dDogJ2tleSdcbiAgfSwgc3RyaW5nZmlsbF0sXG4gIGpzOiBbe1xuICAgIHRva2VuOiAnc3RyaW5nJyxcbiAgICByZWdleDogJ1teXFxcXFxcXFxgXSooPzpcXFxcXFxcXC5bXlxcXFxcXFxcYF0qKSpgJyxcbiAgICBuZXh0OiAna2V5J1xuICB9LCBzdHJpbmdmaWxsXSxcbiAgd29yZHM6IFt7XG4gICAgdG9rZW46ICdzdHJpbmcnLFxuICAgIHJlZ2V4OiAnLio/XFxcXF0+JyxcbiAgICBuZXh0OiAna2V5J1xuICB9LCBzdHJpbmdmaWxsXVxufTtcbmZvciAodmFyIGlkeCBpbiBSdWxlcykge1xuICB2YXIgciA9IFJ1bGVzW2lkeF07XG4gIGlmIChyLnNwbGljZSkge1xuICAgIGZvciAodmFyIGkgPSAwLCBsZW4gPSByLmxlbmd0aDsgaSA8IGxlbjsgKytpKSB7XG4gICAgICB2YXIgcnIgPSByW2ldO1xuICAgICAgaWYgKHR5cGVvZiByci5yZWdleCA9PT0gJ3N0cmluZycpIHtcbiAgICAgICAgUnVsZXNbaWR4XVtpXS5yZWdleCA9IG5ldyBSZWdFeHAoJ14nICsgcnIucmVnZXgpO1xuICAgICAgfVxuICAgIH1cbiAgfSBlbHNlIGlmICh0eXBlb2YgcnIucmVnZXggPT09ICdzdHJpbmcnKSB7XG4gICAgUnVsZXNbaWR4XS5yZWdleCA9IG5ldyBSZWdFeHAoJ14nICsgci5yZWdleCk7XG4gIH1cbn1cbmV4cG9ydCBjb25zdCBsaXZlU2NyaXB0ID0ge1xuICBuYW1lOiBcImxpdmVzY3JpcHRcIixcbiAgc3RhcnRTdGF0ZTogZnVuY3Rpb24gKCkge1xuICAgIHJldHVybiB7XG4gICAgICBuZXh0OiAnc3RhcnQnLFxuICAgICAgbGFzdFRva2VuOiB7XG4gICAgICAgIHN0eWxlOiBudWxsLFxuICAgICAgICBpbmRlbnQ6IDAsXG4gICAgICAgIGNvbnRlbnQ6IFwiXCJcbiAgICAgIH1cbiAgICB9O1xuICB9LFxuICB0b2tlbjogZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICB3aGlsZSAoc3RyZWFtLnBvcyA9PSBzdHJlYW0uc3RhcnQpIHZhciBzdHlsZSA9IHRva2VuQmFzZShzdHJlYW0sIHN0YXRlKTtcbiAgICBzdGF0ZS5sYXN0VG9rZW4gPSB7XG4gICAgICBzdHlsZTogc3R5bGUsXG4gICAgICBpbmRlbnQ6IHN0cmVhbS5pbmRlbnRhdGlvbigpLFxuICAgICAgY29udGVudDogc3RyZWFtLmN1cnJlbnQoKVxuICAgIH07XG4gICAgcmV0dXJuIHN0eWxlLnJlcGxhY2UoL1xcLi9nLCAnICcpO1xuICB9LFxuICBpbmRlbnQ6IGZ1bmN0aW9uIChzdGF0ZSkge1xuICAgIHZhciBpbmRlbnRhdGlvbiA9IHN0YXRlLmxhc3RUb2tlbi5pbmRlbnQ7XG4gICAgaWYgKHN0YXRlLmxhc3RUb2tlbi5jb250ZW50Lm1hdGNoKGluZGVudGVyKSkge1xuICAgICAgaW5kZW50YXRpb24gKz0gMjtcbiAgICB9XG4gICAgcmV0dXJuIGluZGVudGF0aW9uO1xuICB9XG59OyJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==