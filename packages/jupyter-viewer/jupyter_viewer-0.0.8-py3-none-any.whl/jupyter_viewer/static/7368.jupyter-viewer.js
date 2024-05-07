"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[7368],{

/***/ 17368:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "powerShell": () => (/* binding */ powerShell)
/* harmony export */ });
function buildRegexp(patterns, options) {
  options = options || {};
  var prefix = options.prefix !== undefined ? options.prefix : '^';
  var suffix = options.suffix !== undefined ? options.suffix : '\\b';
  for (var i = 0; i < patterns.length; i++) {
    if (patterns[i] instanceof RegExp) {
      patterns[i] = patterns[i].source;
    } else {
      patterns[i] = patterns[i].replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
    }
  }
  return new RegExp(prefix + '(' + patterns.join('|') + ')' + suffix, 'i');
}
var notCharacterOrDash = '(?=[^A-Za-z\\d\\-_]|$)';
var varNames = /[\w\-:]/;
var keywords = buildRegexp([/begin|break|catch|continue|data|default|do|dynamicparam/, /else|elseif|end|exit|filter|finally|for|foreach|from|function|if|in/, /param|process|return|switch|throw|trap|try|until|where|while/], {
  suffix: notCharacterOrDash
});
var punctuation = /[\[\]{},;`\\\.]|@[({]/;
var wordOperators = buildRegexp(['f', /b?not/, /[ic]?split/, 'join', /is(not)?/, 'as', /[ic]?(eq|ne|[gl][te])/, /[ic]?(not)?(like|match|contains)/, /[ic]?replace/, /b?(and|or|xor)/], {
  prefix: '-'
});
var symbolOperators = /[+\-*\/%]=|\+\+|--|\.\.|[+\-*&^%:=!|\/]|<(?!#)|(?!#)>/;
var operators = buildRegexp([wordOperators, symbolOperators], {
  suffix: ''
});
var numbers = /^((0x[\da-f]+)|((\d+\.\d+|\d\.|\.\d+|\d+)(e[\+\-]?\d+)?))[ld]?([kmgtp]b)?/i;
var identifiers = /^[A-Za-z\_][A-Za-z\-\_\d]*\b/;
var symbolBuiltins = /[A-Z]:|%|\?/i;
var namedBuiltins = buildRegexp([/Add-(Computer|Content|History|Member|PSSnapin|Type)/, /Checkpoint-Computer/, /Clear-(Content|EventLog|History|Host|Item(Property)?|Variable)/, /Compare-Object/, /Complete-Transaction/, /Connect-PSSession/, /ConvertFrom-(Csv|Json|SecureString|StringData)/, /Convert-Path/, /ConvertTo-(Csv|Html|Json|SecureString|Xml)/, /Copy-Item(Property)?/, /Debug-Process/, /Disable-(ComputerRestore|PSBreakpoint|PSRemoting|PSSessionConfiguration)/, /Disconnect-PSSession/, /Enable-(ComputerRestore|PSBreakpoint|PSRemoting|PSSessionConfiguration)/, /(Enter|Exit)-PSSession/, /Export-(Alias|Clixml|Console|Counter|Csv|FormatData|ModuleMember|PSSession)/, /ForEach-Object/, /Format-(Custom|List|Table|Wide)/, new RegExp('Get-(Acl|Alias|AuthenticodeSignature|ChildItem|Command|ComputerRestorePoint|Content|ControlPanelItem|Counter|Credential' + '|Culture|Date|Event|EventLog|EventSubscriber|ExecutionPolicy|FormatData|Help|History|Host|HotFix|Item|ItemProperty|Job' + '|Location|Member|Module|PfxCertificate|Process|PSBreakpoint|PSCallStack|PSDrive|PSProvider|PSSession|PSSessionConfiguration' + '|PSSnapin|Random|Service|TraceSource|Transaction|TypeData|UICulture|Unique|Variable|Verb|WinEvent|WmiObject)'), /Group-Object/, /Import-(Alias|Clixml|Counter|Csv|LocalizedData|Module|PSSession)/, /ImportSystemModules/, /Invoke-(Command|Expression|History|Item|RestMethod|WebRequest|WmiMethod)/, /Join-Path/, /Limit-EventLog/, /Measure-(Command|Object)/, /Move-Item(Property)?/, new RegExp('New-(Alias|Event|EventLog|Item(Property)?|Module|ModuleManifest|Object|PSDrive|PSSession|PSSessionConfigurationFile' + '|PSSessionOption|PSTransportOption|Service|TimeSpan|Variable|WebServiceProxy|WinEvent)'), /Out-(Default|File|GridView|Host|Null|Printer|String)/, /Pause/, /(Pop|Push)-Location/, /Read-Host/, /Receive-(Job|PSSession)/, /Register-(EngineEvent|ObjectEvent|PSSessionConfiguration|WmiEvent)/, /Remove-(Computer|Event|EventLog|Item(Property)?|Job|Module|PSBreakpoint|PSDrive|PSSession|PSSnapin|TypeData|Variable|WmiObject)/, /Rename-(Computer|Item(Property)?)/, /Reset-ComputerMachinePassword/, /Resolve-Path/, /Restart-(Computer|Service)/, /Restore-Computer/, /Resume-(Job|Service)/, /Save-Help/, /Select-(Object|String|Xml)/, /Send-MailMessage/, new RegExp('Set-(Acl|Alias|AuthenticodeSignature|Content|Date|ExecutionPolicy|Item(Property)?|Location|PSBreakpoint|PSDebug' + '|PSSessionConfiguration|Service|StrictMode|TraceSource|Variable|WmiInstance)'), /Show-(Command|ControlPanelItem|EventLog)/, /Sort-Object/, /Split-Path/, /Start-(Job|Process|Service|Sleep|Transaction|Transcript)/, /Stop-(Computer|Job|Process|Service|Transcript)/, /Suspend-(Job|Service)/, /TabExpansion2/, /Tee-Object/, /Test-(ComputerSecureChannel|Connection|ModuleManifest|Path|PSSessionConfigurationFile)/, /Trace-Command/, /Unblock-File/, /Undo-Transaction/, /Unregister-(Event|PSSessionConfiguration)/, /Update-(FormatData|Help|List|TypeData)/, /Use-Transaction/, /Wait-(Event|Job|Process)/, /Where-Object/, /Write-(Debug|Error|EventLog|Host|Output|Progress|Verbose|Warning)/, /cd|help|mkdir|more|oss|prompt/, /ac|asnp|cat|cd|chdir|clc|clear|clhy|cli|clp|cls|clv|cnsn|compare|copy|cp|cpi|cpp|cvpa|dbp|del|diff|dir|dnsn|ebp/, /echo|epal|epcsv|epsn|erase|etsn|exsn|fc|fl|foreach|ft|fw|gal|gbp|gc|gci|gcm|gcs|gdr|ghy|gi|gjb|gl|gm|gmo|gp|gps/, /group|gsn|gsnp|gsv|gu|gv|gwmi|h|history|icm|iex|ihy|ii|ipal|ipcsv|ipmo|ipsn|irm|ise|iwmi|iwr|kill|lp|ls|man|md/, /measure|mi|mount|move|mp|mv|nal|ndr|ni|nmo|npssc|nsn|nv|ogv|oh|popd|ps|pushd|pwd|r|rbp|rcjb|rcsn|rd|rdr|ren|ri/, /rjb|rm|rmdir|rmo|rni|rnp|rp|rsn|rsnp|rujb|rv|rvpa|rwmi|sajb|sal|saps|sasv|sbp|sc|select|set|shcm|si|sl|sleep|sls/, /sort|sp|spjb|spps|spsv|start|sujb|sv|swmi|tee|trcm|type|where|wjb|write/], {
  prefix: '',
  suffix: ''
});
var variableBuiltins = buildRegexp([/[$?^_]|Args|ConfirmPreference|ConsoleFileName|DebugPreference|Error|ErrorActionPreference|ErrorView|ExecutionContext/, /FormatEnumerationLimit|Home|Host|Input|MaximumAliasCount|MaximumDriveCount|MaximumErrorCount|MaximumFunctionCount/, /MaximumHistoryCount|MaximumVariableCount|MyInvocation|NestedPromptLevel|OutputEncoding|Pid|Profile|ProgressPreference/, /PSBoundParameters|PSCommandPath|PSCulture|PSDefaultParameterValues|PSEmailServer|PSHome|PSScriptRoot|PSSessionApplicationName/, /PSSessionConfigurationName|PSSessionOption|PSUICulture|PSVersionTable|Pwd|ShellId|StackTrace|VerbosePreference/, /WarningPreference|WhatIfPreference/, /Event|EventArgs|EventSubscriber|Sender/, /Matches|Ofs|ForEach|LastExitCode|PSCmdlet|PSItem|PSSenderInfo|This/, /true|false|null/], {
  prefix: '\\$',
  suffix: ''
});
var builtins = buildRegexp([symbolBuiltins, namedBuiltins, variableBuiltins], {
  suffix: notCharacterOrDash
});
var grammar = {
  keyword: keywords,
  number: numbers,
  operator: operators,
  builtin: builtins,
  punctuation: punctuation,
  variable: identifiers
};

// tokenizers
function tokenBase(stream, state) {
  // Handle Comments
  //var ch = stream.peek();

  var parent = state.returnStack[state.returnStack.length - 1];
  if (parent && parent.shouldReturnFrom(state)) {
    state.tokenize = parent.tokenize;
    state.returnStack.pop();
    return state.tokenize(stream, state);
  }
  if (stream.eatSpace()) {
    return null;
  }
  if (stream.eat('(')) {
    state.bracketNesting += 1;
    return 'punctuation';
  }
  if (stream.eat(')')) {
    state.bracketNesting -= 1;
    return 'punctuation';
  }
  for (var key in grammar) {
    if (stream.match(grammar[key])) {
      return key;
    }
  }
  var ch = stream.next();

  // single-quote string
  if (ch === "'") {
    return tokenSingleQuoteString(stream, state);
  }
  if (ch === '$') {
    return tokenVariable(stream, state);
  }

  // double-quote string
  if (ch === '"') {
    return tokenDoubleQuoteString(stream, state);
  }
  if (ch === '<' && stream.eat('#')) {
    state.tokenize = tokenComment;
    return tokenComment(stream, state);
  }
  if (ch === '#') {
    stream.skipToEnd();
    return 'comment';
  }
  if (ch === '@') {
    var quoteMatch = stream.eat(/["']/);
    if (quoteMatch && stream.eol()) {
      state.tokenize = tokenMultiString;
      state.startQuote = quoteMatch[0];
      return tokenMultiString(stream, state);
    } else if (stream.eol()) {
      return 'error';
    } else if (stream.peek().match(/[({]/)) {
      return 'punctuation';
    } else if (stream.peek().match(varNames)) {
      // splatted variable
      return tokenVariable(stream, state);
    }
  }
  return 'error';
}
function tokenSingleQuoteString(stream, state) {
  var ch;
  while ((ch = stream.peek()) != null) {
    stream.next();
    if (ch === "'" && !stream.eat("'")) {
      state.tokenize = tokenBase;
      return 'string';
    }
  }
  return 'error';
}
function tokenDoubleQuoteString(stream, state) {
  var ch;
  while ((ch = stream.peek()) != null) {
    if (ch === '$') {
      state.tokenize = tokenStringInterpolation;
      return 'string';
    }
    stream.next();
    if (ch === '`') {
      stream.next();
      continue;
    }
    if (ch === '"' && !stream.eat('"')) {
      state.tokenize = tokenBase;
      return 'string';
    }
  }
  return 'error';
}
function tokenStringInterpolation(stream, state) {
  return tokenInterpolation(stream, state, tokenDoubleQuoteString);
}
function tokenMultiStringReturn(stream, state) {
  state.tokenize = tokenMultiString;
  state.startQuote = '"';
  return tokenMultiString(stream, state);
}
function tokenHereStringInterpolation(stream, state) {
  return tokenInterpolation(stream, state, tokenMultiStringReturn);
}
function tokenInterpolation(stream, state, parentTokenize) {
  if (stream.match('$(')) {
    var savedBracketNesting = state.bracketNesting;
    state.returnStack.push({
      /*jshint loopfunc:true */
      shouldReturnFrom: function (state) {
        return state.bracketNesting === savedBracketNesting;
      },
      tokenize: parentTokenize
    });
    state.tokenize = tokenBase;
    state.bracketNesting += 1;
    return 'punctuation';
  } else {
    stream.next();
    state.returnStack.push({
      shouldReturnFrom: function () {
        return true;
      },
      tokenize: parentTokenize
    });
    state.tokenize = tokenVariable;
    return state.tokenize(stream, state);
  }
}
function tokenComment(stream, state) {
  var maybeEnd = false,
    ch;
  while ((ch = stream.next()) != null) {
    if (maybeEnd && ch == '>') {
      state.tokenize = tokenBase;
      break;
    }
    maybeEnd = ch === '#';
  }
  return 'comment';
}
function tokenVariable(stream, state) {
  var ch = stream.peek();
  if (stream.eat('{')) {
    state.tokenize = tokenVariableWithBraces;
    return tokenVariableWithBraces(stream, state);
  } else if (ch != undefined && ch.match(varNames)) {
    stream.eatWhile(varNames);
    state.tokenize = tokenBase;
    return 'variable';
  } else {
    state.tokenize = tokenBase;
    return 'error';
  }
}
function tokenVariableWithBraces(stream, state) {
  var ch;
  while ((ch = stream.next()) != null) {
    if (ch === '}') {
      state.tokenize = tokenBase;
      break;
    }
  }
  return 'variable';
}
function tokenMultiString(stream, state) {
  var quote = state.startQuote;
  if (stream.sol() && stream.match(new RegExp(quote + '@'))) {
    state.tokenize = tokenBase;
  } else if (quote === '"') {
    while (!stream.eol()) {
      var ch = stream.peek();
      if (ch === '$') {
        state.tokenize = tokenHereStringInterpolation;
        return 'string';
      }
      stream.next();
      if (ch === '`') {
        stream.next();
      }
    }
  } else {
    stream.skipToEnd();
  }
  return 'string';
}
const powerShell = {
  name: "powershell",
  startState: function () {
    return {
      returnStack: [],
      bracketNesting: 0,
      tokenize: tokenBase
    };
  },
  token: function (stream, state) {
    return state.tokenize(stream, state);
  },
  languageData: {
    commentTokens: {
      line: "#",
      block: {
        open: "<#",
        close: "#>"
      }
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNzM2OC5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGNvZGVtaXJyb3IvbGVnYWN5LW1vZGVzL21vZGUvcG93ZXJzaGVsbC5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyJmdW5jdGlvbiBidWlsZFJlZ2V4cChwYXR0ZXJucywgb3B0aW9ucykge1xuICBvcHRpb25zID0gb3B0aW9ucyB8fCB7fTtcbiAgdmFyIHByZWZpeCA9IG9wdGlvbnMucHJlZml4ICE9PSB1bmRlZmluZWQgPyBvcHRpb25zLnByZWZpeCA6ICdeJztcbiAgdmFyIHN1ZmZpeCA9IG9wdGlvbnMuc3VmZml4ICE9PSB1bmRlZmluZWQgPyBvcHRpb25zLnN1ZmZpeCA6ICdcXFxcYic7XG4gIGZvciAodmFyIGkgPSAwOyBpIDwgcGF0dGVybnMubGVuZ3RoOyBpKyspIHtcbiAgICBpZiAocGF0dGVybnNbaV0gaW5zdGFuY2VvZiBSZWdFeHApIHtcbiAgICAgIHBhdHRlcm5zW2ldID0gcGF0dGVybnNbaV0uc291cmNlO1xuICAgIH0gZWxzZSB7XG4gICAgICBwYXR0ZXJuc1tpXSA9IHBhdHRlcm5zW2ldLnJlcGxhY2UoL1stXFwvXFxcXF4kKis/LigpfFtcXF17fV0vZywgJ1xcXFwkJicpO1xuICAgIH1cbiAgfVxuICByZXR1cm4gbmV3IFJlZ0V4cChwcmVmaXggKyAnKCcgKyBwYXR0ZXJucy5qb2luKCd8JykgKyAnKScgKyBzdWZmaXgsICdpJyk7XG59XG52YXIgbm90Q2hhcmFjdGVyT3JEYXNoID0gJyg/PVteQS1aYS16XFxcXGRcXFxcLV9dfCQpJztcbnZhciB2YXJOYW1lcyA9IC9bXFx3XFwtOl0vO1xudmFyIGtleXdvcmRzID0gYnVpbGRSZWdleHAoWy9iZWdpbnxicmVha3xjYXRjaHxjb250aW51ZXxkYXRhfGRlZmF1bHR8ZG98ZHluYW1pY3BhcmFtLywgL2Vsc2V8ZWxzZWlmfGVuZHxleGl0fGZpbHRlcnxmaW5hbGx5fGZvcnxmb3JlYWNofGZyb218ZnVuY3Rpb258aWZ8aW4vLCAvcGFyYW18cHJvY2Vzc3xyZXR1cm58c3dpdGNofHRocm93fHRyYXB8dHJ5fHVudGlsfHdoZXJlfHdoaWxlL10sIHtcbiAgc3VmZml4OiBub3RDaGFyYWN0ZXJPckRhc2hcbn0pO1xudmFyIHB1bmN0dWF0aW9uID0gL1tcXFtcXF17fSw7YFxcXFxcXC5dfEBbKHtdLztcbnZhciB3b3JkT3BlcmF0b3JzID0gYnVpbGRSZWdleHAoWydmJywgL2I/bm90LywgL1tpY10/c3BsaXQvLCAnam9pbicsIC9pcyhub3QpPy8sICdhcycsIC9baWNdPyhlcXxuZXxbZ2xdW3RlXSkvLCAvW2ljXT8obm90KT8obGlrZXxtYXRjaHxjb250YWlucykvLCAvW2ljXT9yZXBsYWNlLywgL2I/KGFuZHxvcnx4b3IpL10sIHtcbiAgcHJlZml4OiAnLSdcbn0pO1xudmFyIHN5bWJvbE9wZXJhdG9ycyA9IC9bK1xcLSpcXC8lXT18XFwrXFwrfC0tfFxcLlxcLnxbK1xcLSomXiU6PSF8XFwvXXw8KD8hIyl8KD8hIyk+LztcbnZhciBvcGVyYXRvcnMgPSBidWlsZFJlZ2V4cChbd29yZE9wZXJhdG9ycywgc3ltYm9sT3BlcmF0b3JzXSwge1xuICBzdWZmaXg6ICcnXG59KTtcbnZhciBudW1iZXJzID0gL14oKDB4W1xcZGEtZl0rKXwoKFxcZCtcXC5cXGQrfFxcZFxcLnxcXC5cXGQrfFxcZCspKGVbXFwrXFwtXT9cXGQrKT8pKVtsZF0/KFtrbWd0cF1iKT8vaTtcbnZhciBpZGVudGlmaWVycyA9IC9eW0EtWmEtelxcX11bQS1aYS16XFwtXFxfXFxkXSpcXGIvO1xudmFyIHN5bWJvbEJ1aWx0aW5zID0gL1tBLVpdOnwlfFxcPy9pO1xudmFyIG5hbWVkQnVpbHRpbnMgPSBidWlsZFJlZ2V4cChbL0FkZC0oQ29tcHV0ZXJ8Q29udGVudHxIaXN0b3J5fE1lbWJlcnxQU1NuYXBpbnxUeXBlKS8sIC9DaGVja3BvaW50LUNvbXB1dGVyLywgL0NsZWFyLShDb250ZW50fEV2ZW50TG9nfEhpc3Rvcnl8SG9zdHxJdGVtKFByb3BlcnR5KT98VmFyaWFibGUpLywgL0NvbXBhcmUtT2JqZWN0LywgL0NvbXBsZXRlLVRyYW5zYWN0aW9uLywgL0Nvbm5lY3QtUFNTZXNzaW9uLywgL0NvbnZlcnRGcm9tLShDc3Z8SnNvbnxTZWN1cmVTdHJpbmd8U3RyaW5nRGF0YSkvLCAvQ29udmVydC1QYXRoLywgL0NvbnZlcnRUby0oQ3N2fEh0bWx8SnNvbnxTZWN1cmVTdHJpbmd8WG1sKS8sIC9Db3B5LUl0ZW0oUHJvcGVydHkpPy8sIC9EZWJ1Zy1Qcm9jZXNzLywgL0Rpc2FibGUtKENvbXB1dGVyUmVzdG9yZXxQU0JyZWFrcG9pbnR8UFNSZW1vdGluZ3xQU1Nlc3Npb25Db25maWd1cmF0aW9uKS8sIC9EaXNjb25uZWN0LVBTU2Vzc2lvbi8sIC9FbmFibGUtKENvbXB1dGVyUmVzdG9yZXxQU0JyZWFrcG9pbnR8UFNSZW1vdGluZ3xQU1Nlc3Npb25Db25maWd1cmF0aW9uKS8sIC8oRW50ZXJ8RXhpdCktUFNTZXNzaW9uLywgL0V4cG9ydC0oQWxpYXN8Q2xpeG1sfENvbnNvbGV8Q291bnRlcnxDc3Z8Rm9ybWF0RGF0YXxNb2R1bGVNZW1iZXJ8UFNTZXNzaW9uKS8sIC9Gb3JFYWNoLU9iamVjdC8sIC9Gb3JtYXQtKEN1c3RvbXxMaXN0fFRhYmxlfFdpZGUpLywgbmV3IFJlZ0V4cCgnR2V0LShBY2x8QWxpYXN8QXV0aGVudGljb2RlU2lnbmF0dXJlfENoaWxkSXRlbXxDb21tYW5kfENvbXB1dGVyUmVzdG9yZVBvaW50fENvbnRlbnR8Q29udHJvbFBhbmVsSXRlbXxDb3VudGVyfENyZWRlbnRpYWwnICsgJ3xDdWx0dXJlfERhdGV8RXZlbnR8RXZlbnRMb2d8RXZlbnRTdWJzY3JpYmVyfEV4ZWN1dGlvblBvbGljeXxGb3JtYXREYXRhfEhlbHB8SGlzdG9yeXxIb3N0fEhvdEZpeHxJdGVtfEl0ZW1Qcm9wZXJ0eXxKb2InICsgJ3xMb2NhdGlvbnxNZW1iZXJ8TW9kdWxlfFBmeENlcnRpZmljYXRlfFByb2Nlc3N8UFNCcmVha3BvaW50fFBTQ2FsbFN0YWNrfFBTRHJpdmV8UFNQcm92aWRlcnxQU1Nlc3Npb258UFNTZXNzaW9uQ29uZmlndXJhdGlvbicgKyAnfFBTU25hcGlufFJhbmRvbXxTZXJ2aWNlfFRyYWNlU291cmNlfFRyYW5zYWN0aW9ufFR5cGVEYXRhfFVJQ3VsdHVyZXxVbmlxdWV8VmFyaWFibGV8VmVyYnxXaW5FdmVudHxXbWlPYmplY3QpJyksIC9Hcm91cC1PYmplY3QvLCAvSW1wb3J0LShBbGlhc3xDbGl4bWx8Q291bnRlcnxDc3Z8TG9jYWxpemVkRGF0YXxNb2R1bGV8UFNTZXNzaW9uKS8sIC9JbXBvcnRTeXN0ZW1Nb2R1bGVzLywgL0ludm9rZS0oQ29tbWFuZHxFeHByZXNzaW9ufEhpc3Rvcnl8SXRlbXxSZXN0TWV0aG9kfFdlYlJlcXVlc3R8V21pTWV0aG9kKS8sIC9Kb2luLVBhdGgvLCAvTGltaXQtRXZlbnRMb2cvLCAvTWVhc3VyZS0oQ29tbWFuZHxPYmplY3QpLywgL01vdmUtSXRlbShQcm9wZXJ0eSk/LywgbmV3IFJlZ0V4cCgnTmV3LShBbGlhc3xFdmVudHxFdmVudExvZ3xJdGVtKFByb3BlcnR5KT98TW9kdWxlfE1vZHVsZU1hbmlmZXN0fE9iamVjdHxQU0RyaXZlfFBTU2Vzc2lvbnxQU1Nlc3Npb25Db25maWd1cmF0aW9uRmlsZScgKyAnfFBTU2Vzc2lvbk9wdGlvbnxQU1RyYW5zcG9ydE9wdGlvbnxTZXJ2aWNlfFRpbWVTcGFufFZhcmlhYmxlfFdlYlNlcnZpY2VQcm94eXxXaW5FdmVudCknKSwgL091dC0oRGVmYXVsdHxGaWxlfEdyaWRWaWV3fEhvc3R8TnVsbHxQcmludGVyfFN0cmluZykvLCAvUGF1c2UvLCAvKFBvcHxQdXNoKS1Mb2NhdGlvbi8sIC9SZWFkLUhvc3QvLCAvUmVjZWl2ZS0oSm9ifFBTU2Vzc2lvbikvLCAvUmVnaXN0ZXItKEVuZ2luZUV2ZW50fE9iamVjdEV2ZW50fFBTU2Vzc2lvbkNvbmZpZ3VyYXRpb258V21pRXZlbnQpLywgL1JlbW92ZS0oQ29tcHV0ZXJ8RXZlbnR8RXZlbnRMb2d8SXRlbShQcm9wZXJ0eSk/fEpvYnxNb2R1bGV8UFNCcmVha3BvaW50fFBTRHJpdmV8UFNTZXNzaW9ufFBTU25hcGlufFR5cGVEYXRhfFZhcmlhYmxlfFdtaU9iamVjdCkvLCAvUmVuYW1lLShDb21wdXRlcnxJdGVtKFByb3BlcnR5KT8pLywgL1Jlc2V0LUNvbXB1dGVyTWFjaGluZVBhc3N3b3JkLywgL1Jlc29sdmUtUGF0aC8sIC9SZXN0YXJ0LShDb21wdXRlcnxTZXJ2aWNlKS8sIC9SZXN0b3JlLUNvbXB1dGVyLywgL1Jlc3VtZS0oSm9ifFNlcnZpY2UpLywgL1NhdmUtSGVscC8sIC9TZWxlY3QtKE9iamVjdHxTdHJpbmd8WG1sKS8sIC9TZW5kLU1haWxNZXNzYWdlLywgbmV3IFJlZ0V4cCgnU2V0LShBY2x8QWxpYXN8QXV0aGVudGljb2RlU2lnbmF0dXJlfENvbnRlbnR8RGF0ZXxFeGVjdXRpb25Qb2xpY3l8SXRlbShQcm9wZXJ0eSk/fExvY2F0aW9ufFBTQnJlYWtwb2ludHxQU0RlYnVnJyArICd8UFNTZXNzaW9uQ29uZmlndXJhdGlvbnxTZXJ2aWNlfFN0cmljdE1vZGV8VHJhY2VTb3VyY2V8VmFyaWFibGV8V21pSW5zdGFuY2UpJyksIC9TaG93LShDb21tYW5kfENvbnRyb2xQYW5lbEl0ZW18RXZlbnRMb2cpLywgL1NvcnQtT2JqZWN0LywgL1NwbGl0LVBhdGgvLCAvU3RhcnQtKEpvYnxQcm9jZXNzfFNlcnZpY2V8U2xlZXB8VHJhbnNhY3Rpb258VHJhbnNjcmlwdCkvLCAvU3RvcC0oQ29tcHV0ZXJ8Sm9ifFByb2Nlc3N8U2VydmljZXxUcmFuc2NyaXB0KS8sIC9TdXNwZW5kLShKb2J8U2VydmljZSkvLCAvVGFiRXhwYW5zaW9uMi8sIC9UZWUtT2JqZWN0LywgL1Rlc3QtKENvbXB1dGVyU2VjdXJlQ2hhbm5lbHxDb25uZWN0aW9ufE1vZHVsZU1hbmlmZXN0fFBhdGh8UFNTZXNzaW9uQ29uZmlndXJhdGlvbkZpbGUpLywgL1RyYWNlLUNvbW1hbmQvLCAvVW5ibG9jay1GaWxlLywgL1VuZG8tVHJhbnNhY3Rpb24vLCAvVW5yZWdpc3Rlci0oRXZlbnR8UFNTZXNzaW9uQ29uZmlndXJhdGlvbikvLCAvVXBkYXRlLShGb3JtYXREYXRhfEhlbHB8TGlzdHxUeXBlRGF0YSkvLCAvVXNlLVRyYW5zYWN0aW9uLywgL1dhaXQtKEV2ZW50fEpvYnxQcm9jZXNzKS8sIC9XaGVyZS1PYmplY3QvLCAvV3JpdGUtKERlYnVnfEVycm9yfEV2ZW50TG9nfEhvc3R8T3V0cHV0fFByb2dyZXNzfFZlcmJvc2V8V2FybmluZykvLCAvY2R8aGVscHxta2Rpcnxtb3JlfG9zc3xwcm9tcHQvLCAvYWN8YXNucHxjYXR8Y2R8Y2hkaXJ8Y2xjfGNsZWFyfGNsaHl8Y2xpfGNscHxjbHN8Y2x2fGNuc258Y29tcGFyZXxjb3B5fGNwfGNwaXxjcHB8Y3ZwYXxkYnB8ZGVsfGRpZmZ8ZGlyfGRuc258ZWJwLywgL2VjaG98ZXBhbHxlcGNzdnxlcHNufGVyYXNlfGV0c258ZXhzbnxmY3xmbHxmb3JlYWNofGZ0fGZ3fGdhbHxnYnB8Z2N8Z2NpfGdjbXxnY3N8Z2RyfGdoeXxnaXxnamJ8Z2x8Z218Z21vfGdwfGdwcy8sIC9ncm91cHxnc258Z3NucHxnc3Z8Z3V8Z3Z8Z3dtaXxofGhpc3Rvcnl8aWNtfGlleHxpaHl8aWl8aXBhbHxpcGNzdnxpcG1vfGlwc258aXJtfGlzZXxpd21pfGl3cnxraWxsfGxwfGxzfG1hbnxtZC8sIC9tZWFzdXJlfG1pfG1vdW50fG1vdmV8bXB8bXZ8bmFsfG5kcnxuaXxubW98bnBzc2N8bnNufG52fG9ndnxvaHxwb3BkfHBzfHB1c2hkfHB3ZHxyfHJicHxyY2pifHJjc258cmR8cmRyfHJlbnxyaS8sIC9yamJ8cm18cm1kaXJ8cm1vfHJuaXxybnB8cnB8cnNufHJzbnB8cnVqYnxydnxydnBhfHJ3bWl8c2FqYnxzYWx8c2Fwc3xzYXN2fHNicHxzY3xzZWxlY3R8c2V0fHNoY218c2l8c2x8c2xlZXB8c2xzLywgL3NvcnR8c3B8c3BqYnxzcHBzfHNwc3Z8c3RhcnR8c3VqYnxzdnxzd21pfHRlZXx0cmNtfHR5cGV8d2hlcmV8d2pifHdyaXRlL10sIHtcbiAgcHJlZml4OiAnJyxcbiAgc3VmZml4OiAnJ1xufSk7XG52YXIgdmFyaWFibGVCdWlsdGlucyA9IGJ1aWxkUmVnZXhwKFsvWyQ/Xl9dfEFyZ3N8Q29uZmlybVByZWZlcmVuY2V8Q29uc29sZUZpbGVOYW1lfERlYnVnUHJlZmVyZW5jZXxFcnJvcnxFcnJvckFjdGlvblByZWZlcmVuY2V8RXJyb3JWaWV3fEV4ZWN1dGlvbkNvbnRleHQvLCAvRm9ybWF0RW51bWVyYXRpb25MaW1pdHxIb21lfEhvc3R8SW5wdXR8TWF4aW11bUFsaWFzQ291bnR8TWF4aW11bURyaXZlQ291bnR8TWF4aW11bUVycm9yQ291bnR8TWF4aW11bUZ1bmN0aW9uQ291bnQvLCAvTWF4aW11bUhpc3RvcnlDb3VudHxNYXhpbXVtVmFyaWFibGVDb3VudHxNeUludm9jYXRpb258TmVzdGVkUHJvbXB0TGV2ZWx8T3V0cHV0RW5jb2Rpbmd8UGlkfFByb2ZpbGV8UHJvZ3Jlc3NQcmVmZXJlbmNlLywgL1BTQm91bmRQYXJhbWV0ZXJzfFBTQ29tbWFuZFBhdGh8UFNDdWx0dXJlfFBTRGVmYXVsdFBhcmFtZXRlclZhbHVlc3xQU0VtYWlsU2VydmVyfFBTSG9tZXxQU1NjcmlwdFJvb3R8UFNTZXNzaW9uQXBwbGljYXRpb25OYW1lLywgL1BTU2Vzc2lvbkNvbmZpZ3VyYXRpb25OYW1lfFBTU2Vzc2lvbk9wdGlvbnxQU1VJQ3VsdHVyZXxQU1ZlcnNpb25UYWJsZXxQd2R8U2hlbGxJZHxTdGFja1RyYWNlfFZlcmJvc2VQcmVmZXJlbmNlLywgL1dhcm5pbmdQcmVmZXJlbmNlfFdoYXRJZlByZWZlcmVuY2UvLCAvRXZlbnR8RXZlbnRBcmdzfEV2ZW50U3Vic2NyaWJlcnxTZW5kZXIvLCAvTWF0Y2hlc3xPZnN8Rm9yRWFjaHxMYXN0RXhpdENvZGV8UFNDbWRsZXR8UFNJdGVtfFBTU2VuZGVySW5mb3xUaGlzLywgL3RydWV8ZmFsc2V8bnVsbC9dLCB7XG4gIHByZWZpeDogJ1xcXFwkJyxcbiAgc3VmZml4OiAnJ1xufSk7XG52YXIgYnVpbHRpbnMgPSBidWlsZFJlZ2V4cChbc3ltYm9sQnVpbHRpbnMsIG5hbWVkQnVpbHRpbnMsIHZhcmlhYmxlQnVpbHRpbnNdLCB7XG4gIHN1ZmZpeDogbm90Q2hhcmFjdGVyT3JEYXNoXG59KTtcbnZhciBncmFtbWFyID0ge1xuICBrZXl3b3JkOiBrZXl3b3JkcyxcbiAgbnVtYmVyOiBudW1iZXJzLFxuICBvcGVyYXRvcjogb3BlcmF0b3JzLFxuICBidWlsdGluOiBidWlsdGlucyxcbiAgcHVuY3R1YXRpb246IHB1bmN0dWF0aW9uLFxuICB2YXJpYWJsZTogaWRlbnRpZmllcnNcbn07XG5cbi8vIHRva2VuaXplcnNcbmZ1bmN0aW9uIHRva2VuQmFzZShzdHJlYW0sIHN0YXRlKSB7XG4gIC8vIEhhbmRsZSBDb21tZW50c1xuICAvL3ZhciBjaCA9IHN0cmVhbS5wZWVrKCk7XG5cbiAgdmFyIHBhcmVudCA9IHN0YXRlLnJldHVyblN0YWNrW3N0YXRlLnJldHVyblN0YWNrLmxlbmd0aCAtIDFdO1xuICBpZiAocGFyZW50ICYmIHBhcmVudC5zaG91bGRSZXR1cm5Gcm9tKHN0YXRlKSkge1xuICAgIHN0YXRlLnRva2VuaXplID0gcGFyZW50LnRva2VuaXplO1xuICAgIHN0YXRlLnJldHVyblN0YWNrLnBvcCgpO1xuICAgIHJldHVybiBzdGF0ZS50b2tlbml6ZShzdHJlYW0sIHN0YXRlKTtcbiAgfVxuICBpZiAoc3RyZWFtLmVhdFNwYWNlKCkpIHtcbiAgICByZXR1cm4gbnVsbDtcbiAgfVxuICBpZiAoc3RyZWFtLmVhdCgnKCcpKSB7XG4gICAgc3RhdGUuYnJhY2tldE5lc3RpbmcgKz0gMTtcbiAgICByZXR1cm4gJ3B1bmN0dWF0aW9uJztcbiAgfVxuICBpZiAoc3RyZWFtLmVhdCgnKScpKSB7XG4gICAgc3RhdGUuYnJhY2tldE5lc3RpbmcgLT0gMTtcbiAgICByZXR1cm4gJ3B1bmN0dWF0aW9uJztcbiAgfVxuICBmb3IgKHZhciBrZXkgaW4gZ3JhbW1hcikge1xuICAgIGlmIChzdHJlYW0ubWF0Y2goZ3JhbW1hcltrZXldKSkge1xuICAgICAgcmV0dXJuIGtleTtcbiAgICB9XG4gIH1cbiAgdmFyIGNoID0gc3RyZWFtLm5leHQoKTtcblxuICAvLyBzaW5nbGUtcXVvdGUgc3RyaW5nXG4gIGlmIChjaCA9PT0gXCInXCIpIHtcbiAgICByZXR1cm4gdG9rZW5TaW5nbGVRdW90ZVN0cmluZyhzdHJlYW0sIHN0YXRlKTtcbiAgfVxuICBpZiAoY2ggPT09ICckJykge1xuICAgIHJldHVybiB0b2tlblZhcmlhYmxlKHN0cmVhbSwgc3RhdGUpO1xuICB9XG5cbiAgLy8gZG91YmxlLXF1b3RlIHN0cmluZ1xuICBpZiAoY2ggPT09ICdcIicpIHtcbiAgICByZXR1cm4gdG9rZW5Eb3VibGVRdW90ZVN0cmluZyhzdHJlYW0sIHN0YXRlKTtcbiAgfVxuICBpZiAoY2ggPT09ICc8JyAmJiBzdHJlYW0uZWF0KCcjJykpIHtcbiAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQ29tbWVudDtcbiAgICByZXR1cm4gdG9rZW5Db21tZW50KHN0cmVhbSwgc3RhdGUpO1xuICB9XG4gIGlmIChjaCA9PT0gJyMnKSB7XG4gICAgc3RyZWFtLnNraXBUb0VuZCgpO1xuICAgIHJldHVybiAnY29tbWVudCc7XG4gIH1cbiAgaWYgKGNoID09PSAnQCcpIHtcbiAgICB2YXIgcXVvdGVNYXRjaCA9IHN0cmVhbS5lYXQoL1tcIiddLyk7XG4gICAgaWYgKHF1b3RlTWF0Y2ggJiYgc3RyZWFtLmVvbCgpKSB7XG4gICAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuTXVsdGlTdHJpbmc7XG4gICAgICBzdGF0ZS5zdGFydFF1b3RlID0gcXVvdGVNYXRjaFswXTtcbiAgICAgIHJldHVybiB0b2tlbk11bHRpU3RyaW5nKHN0cmVhbSwgc3RhdGUpO1xuICAgIH0gZWxzZSBpZiAoc3RyZWFtLmVvbCgpKSB7XG4gICAgICByZXR1cm4gJ2Vycm9yJztcbiAgICB9IGVsc2UgaWYgKHN0cmVhbS5wZWVrKCkubWF0Y2goL1soe10vKSkge1xuICAgICAgcmV0dXJuICdwdW5jdHVhdGlvbic7XG4gICAgfSBlbHNlIGlmIChzdHJlYW0ucGVlaygpLm1hdGNoKHZhck5hbWVzKSkge1xuICAgICAgLy8gc3BsYXR0ZWQgdmFyaWFibGVcbiAgICAgIHJldHVybiB0b2tlblZhcmlhYmxlKHN0cmVhbSwgc3RhdGUpO1xuICAgIH1cbiAgfVxuICByZXR1cm4gJ2Vycm9yJztcbn1cbmZ1bmN0aW9uIHRva2VuU2luZ2xlUXVvdGVTdHJpbmcoc3RyZWFtLCBzdGF0ZSkge1xuICB2YXIgY2g7XG4gIHdoaWxlICgoY2ggPSBzdHJlYW0ucGVlaygpKSAhPSBudWxsKSB7XG4gICAgc3RyZWFtLm5leHQoKTtcbiAgICBpZiAoY2ggPT09IFwiJ1wiICYmICFzdHJlYW0uZWF0KFwiJ1wiKSkge1xuICAgICAgc3RhdGUudG9rZW5pemUgPSB0b2tlbkJhc2U7XG4gICAgICByZXR1cm4gJ3N0cmluZyc7XG4gICAgfVxuICB9XG4gIHJldHVybiAnZXJyb3InO1xufVxuZnVuY3Rpb24gdG9rZW5Eb3VibGVRdW90ZVN0cmluZyhzdHJlYW0sIHN0YXRlKSB7XG4gIHZhciBjaDtcbiAgd2hpbGUgKChjaCA9IHN0cmVhbS5wZWVrKCkpICE9IG51bGwpIHtcbiAgICBpZiAoY2ggPT09ICckJykge1xuICAgICAgc3RhdGUudG9rZW5pemUgPSB0b2tlblN0cmluZ0ludGVycG9sYXRpb247XG4gICAgICByZXR1cm4gJ3N0cmluZyc7XG4gICAgfVxuICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgaWYgKGNoID09PSAnYCcpIHtcbiAgICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgICBjb250aW51ZTtcbiAgICB9XG4gICAgaWYgKGNoID09PSAnXCInICYmICFzdHJlYW0uZWF0KCdcIicpKSB7XG4gICAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQmFzZTtcbiAgICAgIHJldHVybiAnc3RyaW5nJztcbiAgICB9XG4gIH1cbiAgcmV0dXJuICdlcnJvcic7XG59XG5mdW5jdGlvbiB0b2tlblN0cmluZ0ludGVycG9sYXRpb24oc3RyZWFtLCBzdGF0ZSkge1xuICByZXR1cm4gdG9rZW5JbnRlcnBvbGF0aW9uKHN0cmVhbSwgc3RhdGUsIHRva2VuRG91YmxlUXVvdGVTdHJpbmcpO1xufVxuZnVuY3Rpb24gdG9rZW5NdWx0aVN0cmluZ1JldHVybihzdHJlYW0sIHN0YXRlKSB7XG4gIHN0YXRlLnRva2VuaXplID0gdG9rZW5NdWx0aVN0cmluZztcbiAgc3RhdGUuc3RhcnRRdW90ZSA9ICdcIic7XG4gIHJldHVybiB0b2tlbk11bHRpU3RyaW5nKHN0cmVhbSwgc3RhdGUpO1xufVxuZnVuY3Rpb24gdG9rZW5IZXJlU3RyaW5nSW50ZXJwb2xhdGlvbihzdHJlYW0sIHN0YXRlKSB7XG4gIHJldHVybiB0b2tlbkludGVycG9sYXRpb24oc3RyZWFtLCBzdGF0ZSwgdG9rZW5NdWx0aVN0cmluZ1JldHVybik7XG59XG5mdW5jdGlvbiB0b2tlbkludGVycG9sYXRpb24oc3RyZWFtLCBzdGF0ZSwgcGFyZW50VG9rZW5pemUpIHtcbiAgaWYgKHN0cmVhbS5tYXRjaCgnJCgnKSkge1xuICAgIHZhciBzYXZlZEJyYWNrZXROZXN0aW5nID0gc3RhdGUuYnJhY2tldE5lc3Rpbmc7XG4gICAgc3RhdGUucmV0dXJuU3RhY2sucHVzaCh7XG4gICAgICAvKmpzaGludCBsb29wZnVuYzp0cnVlICovXG4gICAgICBzaG91bGRSZXR1cm5Gcm9tOiBmdW5jdGlvbiAoc3RhdGUpIHtcbiAgICAgICAgcmV0dXJuIHN0YXRlLmJyYWNrZXROZXN0aW5nID09PSBzYXZlZEJyYWNrZXROZXN0aW5nO1xuICAgICAgfSxcbiAgICAgIHRva2VuaXplOiBwYXJlbnRUb2tlbml6ZVxuICAgIH0pO1xuICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlO1xuICAgIHN0YXRlLmJyYWNrZXROZXN0aW5nICs9IDE7XG4gICAgcmV0dXJuICdwdW5jdHVhdGlvbic7XG4gIH0gZWxzZSB7XG4gICAgc3RyZWFtLm5leHQoKTtcbiAgICBzdGF0ZS5yZXR1cm5TdGFjay5wdXNoKHtcbiAgICAgIHNob3VsZFJldHVybkZyb206IGZ1bmN0aW9uICgpIHtcbiAgICAgICAgcmV0dXJuIHRydWU7XG4gICAgICB9LFxuICAgICAgdG9rZW5pemU6IHBhcmVudFRva2VuaXplXG4gICAgfSk7XG4gICAgc3RhdGUudG9rZW5pemUgPSB0b2tlblZhcmlhYmxlO1xuICAgIHJldHVybiBzdGF0ZS50b2tlbml6ZShzdHJlYW0sIHN0YXRlKTtcbiAgfVxufVxuZnVuY3Rpb24gdG9rZW5Db21tZW50KHN0cmVhbSwgc3RhdGUpIHtcbiAgdmFyIG1heWJlRW5kID0gZmFsc2UsXG4gICAgY2g7XG4gIHdoaWxlICgoY2ggPSBzdHJlYW0ubmV4dCgpKSAhPSBudWxsKSB7XG4gICAgaWYgKG1heWJlRW5kICYmIGNoID09ICc+Jykge1xuICAgICAgc3RhdGUudG9rZW5pemUgPSB0b2tlbkJhc2U7XG4gICAgICBicmVhaztcbiAgICB9XG4gICAgbWF5YmVFbmQgPSBjaCA9PT0gJyMnO1xuICB9XG4gIHJldHVybiAnY29tbWVudCc7XG59XG5mdW5jdGlvbiB0b2tlblZhcmlhYmxlKHN0cmVhbSwgc3RhdGUpIHtcbiAgdmFyIGNoID0gc3RyZWFtLnBlZWsoKTtcbiAgaWYgKHN0cmVhbS5lYXQoJ3snKSkge1xuICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5WYXJpYWJsZVdpdGhCcmFjZXM7XG4gICAgcmV0dXJuIHRva2VuVmFyaWFibGVXaXRoQnJhY2VzKHN0cmVhbSwgc3RhdGUpO1xuICB9IGVsc2UgaWYgKGNoICE9IHVuZGVmaW5lZCAmJiBjaC5tYXRjaCh2YXJOYW1lcykpIHtcbiAgICBzdHJlYW0uZWF0V2hpbGUodmFyTmFtZXMpO1xuICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlO1xuICAgIHJldHVybiAndmFyaWFibGUnO1xuICB9IGVsc2Uge1xuICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlO1xuICAgIHJldHVybiAnZXJyb3InO1xuICB9XG59XG5mdW5jdGlvbiB0b2tlblZhcmlhYmxlV2l0aEJyYWNlcyhzdHJlYW0sIHN0YXRlKSB7XG4gIHZhciBjaDtcbiAgd2hpbGUgKChjaCA9IHN0cmVhbS5uZXh0KCkpICE9IG51bGwpIHtcbiAgICBpZiAoY2ggPT09ICd9Jykge1xuICAgICAgc3RhdGUudG9rZW5pemUgPSB0b2tlbkJhc2U7XG4gICAgICBicmVhaztcbiAgICB9XG4gIH1cbiAgcmV0dXJuICd2YXJpYWJsZSc7XG59XG5mdW5jdGlvbiB0b2tlbk11bHRpU3RyaW5nKHN0cmVhbSwgc3RhdGUpIHtcbiAgdmFyIHF1b3RlID0gc3RhdGUuc3RhcnRRdW90ZTtcbiAgaWYgKHN0cmVhbS5zb2woKSAmJiBzdHJlYW0ubWF0Y2gobmV3IFJlZ0V4cChxdW90ZSArICdAJykpKSB7XG4gICAgc3RhdGUudG9rZW5pemUgPSB0b2tlbkJhc2U7XG4gIH0gZWxzZSBpZiAocXVvdGUgPT09ICdcIicpIHtcbiAgICB3aGlsZSAoIXN0cmVhbS5lb2woKSkge1xuICAgICAgdmFyIGNoID0gc3RyZWFtLnBlZWsoKTtcbiAgICAgIGlmIChjaCA9PT0gJyQnKSB7XG4gICAgICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5IZXJlU3RyaW5nSW50ZXJwb2xhdGlvbjtcbiAgICAgICAgcmV0dXJuICdzdHJpbmcnO1xuICAgICAgfVxuICAgICAgc3RyZWFtLm5leHQoKTtcbiAgICAgIGlmIChjaCA9PT0gJ2AnKSB7XG4gICAgICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgICB9XG4gICAgfVxuICB9IGVsc2Uge1xuICAgIHN0cmVhbS5za2lwVG9FbmQoKTtcbiAgfVxuICByZXR1cm4gJ3N0cmluZyc7XG59XG5leHBvcnQgY29uc3QgcG93ZXJTaGVsbCA9IHtcbiAgbmFtZTogXCJwb3dlcnNoZWxsXCIsXG4gIHN0YXJ0U3RhdGU6IGZ1bmN0aW9uICgpIHtcbiAgICByZXR1cm4ge1xuICAgICAgcmV0dXJuU3RhY2s6IFtdLFxuICAgICAgYnJhY2tldE5lc3Rpbmc6IDAsXG4gICAgICB0b2tlbml6ZTogdG9rZW5CYXNlXG4gICAgfTtcbiAgfSxcbiAgdG9rZW46IGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgcmV0dXJuIHN0YXRlLnRva2VuaXplKHN0cmVhbSwgc3RhdGUpO1xuICB9LFxuICBsYW5ndWFnZURhdGE6IHtcbiAgICBjb21tZW50VG9rZW5zOiB7XG4gICAgICBsaW5lOiBcIiNcIixcbiAgICAgIGJsb2NrOiB7XG4gICAgICAgIG9wZW46IFwiPCNcIixcbiAgICAgICAgY2xvc2U6IFwiIz5cIlxuICAgICAgfVxuICAgIH1cbiAgfVxufTsiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=