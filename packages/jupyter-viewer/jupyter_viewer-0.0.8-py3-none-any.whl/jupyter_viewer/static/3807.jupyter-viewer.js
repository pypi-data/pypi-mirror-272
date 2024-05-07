"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[3807],{

/***/ 13807:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "nsis": () => (/* binding */ nsis)
/* harmony export */ });
/* harmony import */ var _simple_mode_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(58053);

const nsis = (0,_simple_mode_js__WEBPACK_IMPORTED_MODULE_0__/* .simpleMode */ .Q)({
  start: [
  // Numbers
  {
    regex: /(?:[+-]?)(?:0x[\d,a-f]+)|(?:0o[0-7]+)|(?:0b[0,1]+)|(?:\d+.?\d*)/,
    token: "number"
  },
  // Strings
  {
    regex: /"(?:[^\\"]|\\.)*"?/,
    token: "string"
  }, {
    regex: /'(?:[^\\']|\\.)*'?/,
    token: "string"
  }, {
    regex: /`(?:[^\\`]|\\.)*`?/,
    token: "string"
  },
  // Compile Time Commands
  {
    regex: /^\s*(?:\!(addincludedir|addplugindir|appendfile|assert|cd|define|delfile|echo|error|execute|finalize|getdllversion|gettlbversion|include|insertmacro|macro|macroend|makensis|packhdr|pragma|searchparse|searchreplace|system|tempfile|undef|uninstfinalize|verbose|warning))\b/i,
    token: "keyword"
  },
  // Conditional Compilation
  {
    regex: /^\s*(?:\!(if(?:n?def)?|ifmacron?def|macro))\b/i,
    token: "keyword",
    indent: true
  }, {
    regex: /^\s*(?:\!(else|endif|macroend))\b/i,
    token: "keyword",
    dedent: true
  },
  // Runtime Commands
  {
    regex: /^\s*(?:Abort|AddBrandingImage|AddSize|AllowRootDirInstall|AllowSkipFiles|AutoCloseWindow|BGFont|BGGradient|BrandingText|BringToFront|Call|CallInstDLL|Caption|ChangeUI|CheckBitmap|ClearErrors|CompletedText|ComponentText|CopyFiles|CRCCheck|CreateDirectory|CreateFont|CreateShortCut|Delete|DeleteINISec|DeleteINIStr|DeleteRegKey|DeleteRegValue|DetailPrint|DetailsButtonText|DirText|DirVar|DirVerify|EnableWindow|EnumRegKey|EnumRegValue|Exch|Exec|ExecShell|ExecShellWait|ExecWait|ExpandEnvStrings|File|FileBufSize|FileClose|FileErrorText|FileOpen|FileRead|FileReadByte|FileReadUTF16LE|FileReadWord|FileWriteUTF16LE|FileSeek|FileWrite|FileWriteByte|FileWriteWord|FindClose|FindFirst|FindNext|FindWindow|FlushINI|GetCurInstType|GetCurrentAddress|GetDlgItem|GetDLLVersion|GetDLLVersionLocal|GetErrorLevel|GetFileTime|GetFileTimeLocal|GetFullPathName|GetFunctionAddress|GetInstDirError|GetKnownFolderPath|GetLabelAddress|GetTempFileName|GetWinVer|Goto|HideWindow|Icon|IfAbort|IfErrors|IfFileExists|IfRebootFlag|IfRtlLanguage|IfShellVarContextAll|IfSilent|InitPluginsDir|InstallButtonText|InstallColors|InstallDir|InstallDirRegKey|InstProgressFlags|InstType|InstTypeGetText|InstTypeSetText|Int64Cmp|Int64CmpU|Int64Fmt|IntCmp|IntCmpU|IntFmt|IntOp|IntPtrCmp|IntPtrCmpU|IntPtrOp|IsWindow|LangString|LicenseBkColor|LicenseData|LicenseForceSelection|LicenseLangString|LicenseText|LoadAndSetImage|LoadLanguageFile|LockWindow|LogSet|LogText|ManifestDPIAware|ManifestLongPathAware|ManifestMaxVersionTested|ManifestSupportedOS|MessageBox|MiscButtonText|Name|Nop|OutFile|Page|PageCallbacks|PEAddResource|PEDllCharacteristics|PERemoveResource|PESubsysVer|Pop|Push|Quit|ReadEnvStr|ReadINIStr|ReadRegDWORD|ReadRegStr|Reboot|RegDLL|Rename|RequestExecutionLevel|ReserveFile|Return|RMDir|SearchPath|SectionGetFlags|SectionGetInstTypes|SectionGetSize|SectionGetText|SectionIn|SectionSetFlags|SectionSetInstTypes|SectionSetSize|SectionSetText|SendMessage|SetAutoClose|SetBrandingImage|SetCompress|SetCompressor|SetCompressorDictSize|SetCtlColors|SetCurInstType|SetDatablockOptimize|SetDateSave|SetDetailsPrint|SetDetailsView|SetErrorLevel|SetErrors|SetFileAttributes|SetFont|SetOutPath|SetOverwrite|SetRebootFlag|SetRegView|SetShellVarContext|SetSilent|ShowInstDetails|ShowUninstDetails|ShowWindow|SilentInstall|SilentUnInstall|Sleep|SpaceTexts|StrCmp|StrCmpS|StrCpy|StrLen|SubCaption|Target|Unicode|UninstallButtonText|UninstallCaption|UninstallIcon|UninstallSubCaption|UninstallText|UninstPage|UnRegDLL|Var|VIAddVersionKey|VIFileVersion|VIProductVersion|WindowIcon|WriteINIStr|WriteRegBin|WriteRegDWORD|WriteRegExpandStr|WriteRegMultiStr|WriteRegNone|WriteRegStr|WriteUninstaller|XPStyle)\b/i,
    token: "keyword"
  }, {
    regex: /^\s*(?:Function|PageEx|Section(?:Group)?)\b/i,
    token: "keyword",
    indent: true
  }, {
    regex: /^\s*(?:(Function|PageEx|Section(?:Group)?)End)\b/i,
    token: "keyword",
    dedent: true
  },
  // Command Options
  {
    regex: /\b(?:ARCHIVE|FILE_ATTRIBUTE_ARCHIVE|FILE_ATTRIBUTE_HIDDEN|FILE_ATTRIBUTE_NORMAL|FILE_ATTRIBUTE_OFFLINE|FILE_ATTRIBUTE_READONLY|FILE_ATTRIBUTE_SYSTEM|FILE_ATTRIBUTE_TEMPORARY|HIDDEN|HKCC|HKCR(32|64)?|HKCU(32|64)?|HKDD|HKEY_CLASSES_ROOT|HKEY_CURRENT_CONFIG|HKEY_CURRENT_USER|HKEY_DYN_DATA|HKEY_LOCAL_MACHINE|HKEY_PERFORMANCE_DATA|HKEY_USERS|HKLM(32|64)?|HKPD|HKU|IDABORT|IDCANCEL|IDD_DIR|IDD_INST|IDD_INSTFILES|IDD_LICENSE|IDD_SELCOM|IDD_UNINST|IDD_VERIFY|IDIGNORE|IDNO|IDOK|IDRETRY|IDYES|MB_ABORTRETRYIGNORE|MB_DEFBUTTON1|MB_DEFBUTTON2|MB_DEFBUTTON3|MB_DEFBUTTON4|MB_ICONEXCLAMATION|MB_ICONINFORMATION|MB_ICONQUESTION|MB_ICONSTOP|MB_OK|MB_OKCANCEL|MB_RETRYCANCEL|MB_RIGHT|MB_RTLREADING|MB_SETFOREGROUND|MB_TOPMOST|MB_USERICON|MB_YESNO|MB_YESNOCANCEL|NORMAL|OFFLINE|READONLY|SHCTX|SHELL_CONTEXT|SW_HIDE|SW_SHOWDEFAULT|SW_SHOWMAXIMIZED|SW_SHOWMINIMIZED|SW_SHOWNORMAL|SYSTEM|TEMPORARY)\b/i,
    token: "atom"
  }, {
    regex: /\b(?:admin|all|amd64-unicode|auto|both|bottom|bzip2|components|current|custom|directory|false|force|hide|highest|ifdiff|ifnewer|instfiles|lastused|leave|left|license|listonly|lzma|nevershow|none|normal|notset|off|on|right|show|silent|silentlog|textonly|top|true|try|un\.components|un\.custom|un\.directory|un\.instfiles|un\.license|uninstConfirm|user|Win10|Win7|Win8|WinVista|x-86-(ansi|unicode)|zlib)\b/i,
    token: "builtin"
  },
  // LogicLib.nsh
  {
    regex: /\$\{(?:And(?:If(?:Not)?|Unless)|Break|Case(?:2|3|4|5|Else)?|Continue|Default|Do(?:Until|While)?|Else(?:If(?:Not)?|Unless)?|End(?:If|Select|Switch)|Exit(?:Do|For|While)|For(?:Each)?|If(?:Cmd|Not(?:Then)?|Then)?|Loop(?:Until|While)?|Or(?:If(?:Not)?|Unless)|Select|Switch|Unless|While)\}/i,
    token: "variable-2",
    indent: true
  },
  // FileFunc.nsh
  {
    regex: /\$\{(?:BannerTrimPath|DirState|DriveSpace|Get(BaseName|Drives|ExeName|ExePath|FileAttributes|FileExt|FileName|FileVersion|Options|OptionsS|Parameters|Parent|Root|Size|Time)|Locate|RefreshShellIcons)\}/i,
    token: "variable-2",
    dedent: true
  },
  // Memento.nsh
  {
    regex: /\$\{(?:Memento(?:Section(?:Done|End|Restore|Save)?|UnselectedSection))\}/i,
    token: "variable-2",
    dedent: true
  },
  // TextFunc.nsh
  {
    regex: /\$\{(?:Config(?:Read|ReadS|Write|WriteS)|File(?:Join|ReadFromEnd|Recode)|Line(?:Find|Read|Sum)|Text(?:Compare|CompareS)|TrimNewLines)\}/i,
    token: "variable-2",
    dedent: true
  },
  // WinVer.nsh
  {
    regex: /\$\{(?:(?:At(?:Least|Most)|Is)(?:ServicePack|Win(?:7|8|10|95|98|200(?:0|3|8(?:R2)?)|ME|NT4|Vista|XP))|Is(?:NT|Server))\}/i,
    token: "variable",
    dedent: true
  },
  // WordFunc.nsh
  {
    regex: /\$\{(?:StrFilterS?|Version(?:Compare|Convert)|Word(?:AddS?|Find(?:(?:2|3)X)?S?|InsertS?|ReplaceS?))\}/i,
    token: "keyword",
    dedent: true
  },
  // x64.nsh
  {
    regex: /\$\{(?:RunningX64)\}/i,
    token: "variable",
    dedent: true
  }, {
    regex: /\$\{(?:Disable|Enable)X64FSRedirection\}/i,
    token: "keyword",
    dedent: true
  },
  // Line Comment
  {
    regex: /(#|;).*/,
    token: "comment"
  },
  // Block Comment
  {
    regex: /\/\*/,
    token: "comment",
    next: "comment"
  },
  // Operator
  {
    regex: /[-+\/*=<>!]+/,
    token: "operator"
  },
  // Variable
  {
    regex: /\$\w[\w\.]*/,
    token: "variable"
  },
  // Constant
  {
    regex: /\${[\!\w\.:-]+}/,
    token: "variableName.constant"
  },
  // Language String
  {
    regex: /\$\([\!\w\.:-]+\)/,
    token: "atom"
  }],
  comment: [{
    regex: /.*?\*\//,
    token: "comment",
    next: "start"
  }, {
    regex: /.*/,
    token: "comment"
  }],
  languageData: {
    name: "nsis",
    indentOnInput: /^\s*((Function|PageEx|Section|Section(Group)?)End|(\!(endif|macroend))|\$\{(End(If|Unless|While)|Loop(Until)|Next)\})$/i,
    commentTokens: {
      line: "#",
      block: {
        open: "/*",
        close: "*/"
      }
    }
  }
});

/***/ }),

/***/ 58053:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Q": () => (/* binding */ simpleMode)
/* harmony export */ });
function simpleMode(states) {
  ensureState(states, "start");
  var states_ = {},
    meta = states.languageData || {},
    hasIndentation = false;
  for (var state in states) if (state != meta && states.hasOwnProperty(state)) {
    var list = states_[state] = [],
      orig = states[state];
    for (var i = 0; i < orig.length; i++) {
      var data = orig[i];
      list.push(new Rule(data, states));
      if (data.indent || data.dedent) hasIndentation = true;
    }
  }
  return {
    name: meta.name,
    startState: function () {
      return {
        state: "start",
        pending: null,
        indent: hasIndentation ? [] : null
      };
    },
    copyState: function (state) {
      var s = {
        state: state.state,
        pending: state.pending,
        indent: state.indent && state.indent.slice(0)
      };
      if (state.stack) s.stack = state.stack.slice(0);
      return s;
    },
    token: tokenFunction(states_),
    indent: indentFunction(states_, meta),
    languageData: meta
  };
}
;
function ensureState(states, name) {
  if (!states.hasOwnProperty(name)) throw new Error("Undefined state " + name + " in simple mode");
}
function toRegex(val, caret) {
  if (!val) return /(?:)/;
  var flags = "";
  if (val instanceof RegExp) {
    if (val.ignoreCase) flags = "i";
    val = val.source;
  } else {
    val = String(val);
  }
  return new RegExp((caret === false ? "" : "^") + "(?:" + val + ")", flags);
}
function asToken(val) {
  if (!val) return null;
  if (val.apply) return val;
  if (typeof val == "string") return val.replace(/\./g, " ");
  var result = [];
  for (var i = 0; i < val.length; i++) result.push(val[i] && val[i].replace(/\./g, " "));
  return result;
}
function Rule(data, states) {
  if (data.next || data.push) ensureState(states, data.next || data.push);
  this.regex = toRegex(data.regex);
  this.token = asToken(data.token);
  this.data = data;
}
function tokenFunction(states) {
  return function (stream, state) {
    if (state.pending) {
      var pend = state.pending.shift();
      if (state.pending.length == 0) state.pending = null;
      stream.pos += pend.text.length;
      return pend.token;
    }
    var curState = states[state.state];
    for (var i = 0; i < curState.length; i++) {
      var rule = curState[i];
      var matches = (!rule.data.sol || stream.sol()) && stream.match(rule.regex);
      if (matches) {
        if (rule.data.next) {
          state.state = rule.data.next;
        } else if (rule.data.push) {
          (state.stack || (state.stack = [])).push(state.state);
          state.state = rule.data.push;
        } else if (rule.data.pop && state.stack && state.stack.length) {
          state.state = state.stack.pop();
        }
        if (rule.data.indent) state.indent.push(stream.indentation() + stream.indentUnit);
        if (rule.data.dedent) state.indent.pop();
        var token = rule.token;
        if (token && token.apply) token = token(matches);
        if (matches.length > 2 && rule.token && typeof rule.token != "string") {
          state.pending = [];
          for (var j = 2; j < matches.length; j++) if (matches[j]) state.pending.push({
            text: matches[j],
            token: rule.token[j - 1]
          });
          stream.backUp(matches[0].length - (matches[1] ? matches[1].length : 0));
          return token[0];
        } else if (token && token.join) {
          return token[0];
        } else {
          return token;
        }
      }
    }
    stream.next();
    return null;
  };
}
function indentFunction(states, meta) {
  return function (state, textAfter) {
    if (state.indent == null || meta.dontIndentStates && meta.doneIndentState.indexOf(state.state) > -1) return null;
    var pos = state.indent.length - 1,
      rules = states[state.state];
    scan: for (;;) {
      for (var i = 0; i < rules.length; i++) {
        var rule = rules[i];
        if (rule.data.dedent && rule.data.dedentIfLineStart !== false) {
          var m = rule.regex.exec(textAfter);
          if (m && m[0]) {
            pos--;
            if (rule.next || rule.push) rules = states[rule.next || rule.push];
            textAfter = textAfter.slice(m[0].length);
            continue scan;
          }
        }
      }
      break;
    }
    return pos < 0 ? 0 : state.indent[pos];
  };
}

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiMzgwNy5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7Ozs7Ozs7Ozs7QUN2SkE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL0Bjb2RlbWlycm9yL2xlZ2FjeS1tb2Rlcy9tb2RlL25zaXMuanMiLCJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9AY29kZW1pcnJvci9sZWdhY3ktbW9kZXMvbW9kZS9zaW1wbGUtbW9kZS5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgeyBzaW1wbGVNb2RlIH0gZnJvbSBcIi4vc2ltcGxlLW1vZGUuanNcIjtcbmV4cG9ydCBjb25zdCBuc2lzID0gc2ltcGxlTW9kZSh7XG4gIHN0YXJ0OiBbXG4gIC8vIE51bWJlcnNcbiAge1xuICAgIHJlZ2V4OiAvKD86WystXT8pKD86MHhbXFxkLGEtZl0rKXwoPzowb1swLTddKyl8KD86MGJbMCwxXSspfCg/OlxcZCsuP1xcZCopLyxcbiAgICB0b2tlbjogXCJudW1iZXJcIlxuICB9LFxuICAvLyBTdHJpbmdzXG4gIHtcbiAgICByZWdleDogL1wiKD86W15cXFxcXCJdfFxcXFwuKSpcIj8vLFxuICAgIHRva2VuOiBcInN0cmluZ1wiXG4gIH0sIHtcbiAgICByZWdleDogLycoPzpbXlxcXFwnXXxcXFxcLikqJz8vLFxuICAgIHRva2VuOiBcInN0cmluZ1wiXG4gIH0sIHtcbiAgICByZWdleDogL2AoPzpbXlxcXFxgXXxcXFxcLikqYD8vLFxuICAgIHRva2VuOiBcInN0cmluZ1wiXG4gIH0sXG4gIC8vIENvbXBpbGUgVGltZSBDb21tYW5kc1xuICB7XG4gICAgcmVnZXg6IC9eXFxzKig/OlxcIShhZGRpbmNsdWRlZGlyfGFkZHBsdWdpbmRpcnxhcHBlbmRmaWxlfGFzc2VydHxjZHxkZWZpbmV8ZGVsZmlsZXxlY2hvfGVycm9yfGV4ZWN1dGV8ZmluYWxpemV8Z2V0ZGxsdmVyc2lvbnxnZXR0bGJ2ZXJzaW9ufGluY2x1ZGV8aW5zZXJ0bWFjcm98bWFjcm98bWFjcm9lbmR8bWFrZW5zaXN8cGFja2hkcnxwcmFnbWF8c2VhcmNocGFyc2V8c2VhcmNocmVwbGFjZXxzeXN0ZW18dGVtcGZpbGV8dW5kZWZ8dW5pbnN0ZmluYWxpemV8dmVyYm9zZXx3YXJuaW5nKSlcXGIvaSxcbiAgICB0b2tlbjogXCJrZXl3b3JkXCJcbiAgfSxcbiAgLy8gQ29uZGl0aW9uYWwgQ29tcGlsYXRpb25cbiAge1xuICAgIHJlZ2V4OiAvXlxccyooPzpcXCEoaWYoPzpuP2RlZik/fGlmbWFjcm9uP2RlZnxtYWNybykpXFxiL2ksXG4gICAgdG9rZW46IFwia2V5d29yZFwiLFxuICAgIGluZGVudDogdHJ1ZVxuICB9LCB7XG4gICAgcmVnZXg6IC9eXFxzKig/OlxcIShlbHNlfGVuZGlmfG1hY3JvZW5kKSlcXGIvaSxcbiAgICB0b2tlbjogXCJrZXl3b3JkXCIsXG4gICAgZGVkZW50OiB0cnVlXG4gIH0sXG4gIC8vIFJ1bnRpbWUgQ29tbWFuZHNcbiAge1xuICAgIHJlZ2V4OiAvXlxccyooPzpBYm9ydHxBZGRCcmFuZGluZ0ltYWdlfEFkZFNpemV8QWxsb3dSb290RGlySW5zdGFsbHxBbGxvd1NraXBGaWxlc3xBdXRvQ2xvc2VXaW5kb3d8QkdGb250fEJHR3JhZGllbnR8QnJhbmRpbmdUZXh0fEJyaW5nVG9Gcm9udHxDYWxsfENhbGxJbnN0RExMfENhcHRpb258Q2hhbmdlVUl8Q2hlY2tCaXRtYXB8Q2xlYXJFcnJvcnN8Q29tcGxldGVkVGV4dHxDb21wb25lbnRUZXh0fENvcHlGaWxlc3xDUkNDaGVja3xDcmVhdGVEaXJlY3Rvcnl8Q3JlYXRlRm9udHxDcmVhdGVTaG9ydEN1dHxEZWxldGV8RGVsZXRlSU5JU2VjfERlbGV0ZUlOSVN0cnxEZWxldGVSZWdLZXl8RGVsZXRlUmVnVmFsdWV8RGV0YWlsUHJpbnR8RGV0YWlsc0J1dHRvblRleHR8RGlyVGV4dHxEaXJWYXJ8RGlyVmVyaWZ5fEVuYWJsZVdpbmRvd3xFbnVtUmVnS2V5fEVudW1SZWdWYWx1ZXxFeGNofEV4ZWN8RXhlY1NoZWxsfEV4ZWNTaGVsbFdhaXR8RXhlY1dhaXR8RXhwYW5kRW52U3RyaW5nc3xGaWxlfEZpbGVCdWZTaXplfEZpbGVDbG9zZXxGaWxlRXJyb3JUZXh0fEZpbGVPcGVufEZpbGVSZWFkfEZpbGVSZWFkQnl0ZXxGaWxlUmVhZFVURjE2TEV8RmlsZVJlYWRXb3JkfEZpbGVXcml0ZVVURjE2TEV8RmlsZVNlZWt8RmlsZVdyaXRlfEZpbGVXcml0ZUJ5dGV8RmlsZVdyaXRlV29yZHxGaW5kQ2xvc2V8RmluZEZpcnN0fEZpbmROZXh0fEZpbmRXaW5kb3d8Rmx1c2hJTkl8R2V0Q3VySW5zdFR5cGV8R2V0Q3VycmVudEFkZHJlc3N8R2V0RGxnSXRlbXxHZXRETExWZXJzaW9ufEdldERMTFZlcnNpb25Mb2NhbHxHZXRFcnJvckxldmVsfEdldEZpbGVUaW1lfEdldEZpbGVUaW1lTG9jYWx8R2V0RnVsbFBhdGhOYW1lfEdldEZ1bmN0aW9uQWRkcmVzc3xHZXRJbnN0RGlyRXJyb3J8R2V0S25vd25Gb2xkZXJQYXRofEdldExhYmVsQWRkcmVzc3xHZXRUZW1wRmlsZU5hbWV8R2V0V2luVmVyfEdvdG98SGlkZVdpbmRvd3xJY29ufElmQWJvcnR8SWZFcnJvcnN8SWZGaWxlRXhpc3RzfElmUmVib290RmxhZ3xJZlJ0bExhbmd1YWdlfElmU2hlbGxWYXJDb250ZXh0QWxsfElmU2lsZW50fEluaXRQbHVnaW5zRGlyfEluc3RhbGxCdXR0b25UZXh0fEluc3RhbGxDb2xvcnN8SW5zdGFsbERpcnxJbnN0YWxsRGlyUmVnS2V5fEluc3RQcm9ncmVzc0ZsYWdzfEluc3RUeXBlfEluc3RUeXBlR2V0VGV4dHxJbnN0VHlwZVNldFRleHR8SW50NjRDbXB8SW50NjRDbXBVfEludDY0Rm10fEludENtcHxJbnRDbXBVfEludEZtdHxJbnRPcHxJbnRQdHJDbXB8SW50UHRyQ21wVXxJbnRQdHJPcHxJc1dpbmRvd3xMYW5nU3RyaW5nfExpY2Vuc2VCa0NvbG9yfExpY2Vuc2VEYXRhfExpY2Vuc2VGb3JjZVNlbGVjdGlvbnxMaWNlbnNlTGFuZ1N0cmluZ3xMaWNlbnNlVGV4dHxMb2FkQW5kU2V0SW1hZ2V8TG9hZExhbmd1YWdlRmlsZXxMb2NrV2luZG93fExvZ1NldHxMb2dUZXh0fE1hbmlmZXN0RFBJQXdhcmV8TWFuaWZlc3RMb25nUGF0aEF3YXJlfE1hbmlmZXN0TWF4VmVyc2lvblRlc3RlZHxNYW5pZmVzdFN1cHBvcnRlZE9TfE1lc3NhZ2VCb3h8TWlzY0J1dHRvblRleHR8TmFtZXxOb3B8T3V0RmlsZXxQYWdlfFBhZ2VDYWxsYmFja3N8UEVBZGRSZXNvdXJjZXxQRURsbENoYXJhY3RlcmlzdGljc3xQRVJlbW92ZVJlc291cmNlfFBFU3Vic3lzVmVyfFBvcHxQdXNofFF1aXR8UmVhZEVudlN0cnxSZWFkSU5JU3RyfFJlYWRSZWdEV09SRHxSZWFkUmVnU3RyfFJlYm9vdHxSZWdETEx8UmVuYW1lfFJlcXVlc3RFeGVjdXRpb25MZXZlbHxSZXNlcnZlRmlsZXxSZXR1cm58Uk1EaXJ8U2VhcmNoUGF0aHxTZWN0aW9uR2V0RmxhZ3N8U2VjdGlvbkdldEluc3RUeXBlc3xTZWN0aW9uR2V0U2l6ZXxTZWN0aW9uR2V0VGV4dHxTZWN0aW9uSW58U2VjdGlvblNldEZsYWdzfFNlY3Rpb25TZXRJbnN0VHlwZXN8U2VjdGlvblNldFNpemV8U2VjdGlvblNldFRleHR8U2VuZE1lc3NhZ2V8U2V0QXV0b0Nsb3NlfFNldEJyYW5kaW5nSW1hZ2V8U2V0Q29tcHJlc3N8U2V0Q29tcHJlc3NvcnxTZXRDb21wcmVzc29yRGljdFNpemV8U2V0Q3RsQ29sb3JzfFNldEN1ckluc3RUeXBlfFNldERhdGFibG9ja09wdGltaXplfFNldERhdGVTYXZlfFNldERldGFpbHNQcmludHxTZXREZXRhaWxzVmlld3xTZXRFcnJvckxldmVsfFNldEVycm9yc3xTZXRGaWxlQXR0cmlidXRlc3xTZXRGb250fFNldE91dFBhdGh8U2V0T3ZlcndyaXRlfFNldFJlYm9vdEZsYWd8U2V0UmVnVmlld3xTZXRTaGVsbFZhckNvbnRleHR8U2V0U2lsZW50fFNob3dJbnN0RGV0YWlsc3xTaG93VW5pbnN0RGV0YWlsc3xTaG93V2luZG93fFNpbGVudEluc3RhbGx8U2lsZW50VW5JbnN0YWxsfFNsZWVwfFNwYWNlVGV4dHN8U3RyQ21wfFN0ckNtcFN8U3RyQ3B5fFN0ckxlbnxTdWJDYXB0aW9ufFRhcmdldHxVbmljb2RlfFVuaW5zdGFsbEJ1dHRvblRleHR8VW5pbnN0YWxsQ2FwdGlvbnxVbmluc3RhbGxJY29ufFVuaW5zdGFsbFN1YkNhcHRpb258VW5pbnN0YWxsVGV4dHxVbmluc3RQYWdlfFVuUmVnRExMfFZhcnxWSUFkZFZlcnNpb25LZXl8VklGaWxlVmVyc2lvbnxWSVByb2R1Y3RWZXJzaW9ufFdpbmRvd0ljb258V3JpdGVJTklTdHJ8V3JpdGVSZWdCaW58V3JpdGVSZWdEV09SRHxXcml0ZVJlZ0V4cGFuZFN0cnxXcml0ZVJlZ011bHRpU3RyfFdyaXRlUmVnTm9uZXxXcml0ZVJlZ1N0cnxXcml0ZVVuaW5zdGFsbGVyfFhQU3R5bGUpXFxiL2ksXG4gICAgdG9rZW46IFwia2V5d29yZFwiXG4gIH0sIHtcbiAgICByZWdleDogL15cXHMqKD86RnVuY3Rpb258UGFnZUV4fFNlY3Rpb24oPzpHcm91cCk/KVxcYi9pLFxuICAgIHRva2VuOiBcImtleXdvcmRcIixcbiAgICBpbmRlbnQ6IHRydWVcbiAgfSwge1xuICAgIHJlZ2V4OiAvXlxccyooPzooRnVuY3Rpb258UGFnZUV4fFNlY3Rpb24oPzpHcm91cCk/KUVuZClcXGIvaSxcbiAgICB0b2tlbjogXCJrZXl3b3JkXCIsXG4gICAgZGVkZW50OiB0cnVlXG4gIH0sXG4gIC8vIENvbW1hbmQgT3B0aW9uc1xuICB7XG4gICAgcmVnZXg6IC9cXGIoPzpBUkNISVZFfEZJTEVfQVRUUklCVVRFX0FSQ0hJVkV8RklMRV9BVFRSSUJVVEVfSElEREVOfEZJTEVfQVRUUklCVVRFX05PUk1BTHxGSUxFX0FUVFJJQlVURV9PRkZMSU5FfEZJTEVfQVRUUklCVVRFX1JFQURPTkxZfEZJTEVfQVRUUklCVVRFX1NZU1RFTXxGSUxFX0FUVFJJQlVURV9URU1QT1JBUll8SElEREVOfEhLQ0N8SEtDUigzMnw2NCk/fEhLQ1UoMzJ8NjQpP3xIS0REfEhLRVlfQ0xBU1NFU19ST09UfEhLRVlfQ1VSUkVOVF9DT05GSUd8SEtFWV9DVVJSRU5UX1VTRVJ8SEtFWV9EWU5fREFUQXxIS0VZX0xPQ0FMX01BQ0hJTkV8SEtFWV9QRVJGT1JNQU5DRV9EQVRBfEhLRVlfVVNFUlN8SEtMTSgzMnw2NCk/fEhLUER8SEtVfElEQUJPUlR8SURDQU5DRUx8SUREX0RJUnxJRERfSU5TVHxJRERfSU5TVEZJTEVTfElERF9MSUNFTlNFfElERF9TRUxDT018SUREX1VOSU5TVHxJRERfVkVSSUZZfElESUdOT1JFfElETk98SURPS3xJRFJFVFJZfElEWUVTfE1CX0FCT1JUUkVUUllJR05PUkV8TUJfREVGQlVUVE9OMXxNQl9ERUZCVVRUT04yfE1CX0RFRkJVVFRPTjN8TUJfREVGQlVUVE9ONHxNQl9JQ09ORVhDTEFNQVRJT058TUJfSUNPTklORk9STUFUSU9OfE1CX0lDT05RVUVTVElPTnxNQl9JQ09OU1RPUHxNQl9PS3xNQl9PS0NBTkNFTHxNQl9SRVRSWUNBTkNFTHxNQl9SSUdIVHxNQl9SVExSRUFESU5HfE1CX1NFVEZPUkVHUk9VTkR8TUJfVE9QTU9TVHxNQl9VU0VSSUNPTnxNQl9ZRVNOT3xNQl9ZRVNOT0NBTkNFTHxOT1JNQUx8T0ZGTElORXxSRUFET05MWXxTSENUWHxTSEVMTF9DT05URVhUfFNXX0hJREV8U1dfU0hPV0RFRkFVTFR8U1dfU0hPV01BWElNSVpFRHxTV19TSE9XTUlOSU1JWkVEfFNXX1NIT1dOT1JNQUx8U1lTVEVNfFRFTVBPUkFSWSlcXGIvaSxcbiAgICB0b2tlbjogXCJhdG9tXCJcbiAgfSwge1xuICAgIHJlZ2V4OiAvXFxiKD86YWRtaW58YWxsfGFtZDY0LXVuaWNvZGV8YXV0b3xib3RofGJvdHRvbXxiemlwMnxjb21wb25lbnRzfGN1cnJlbnR8Y3VzdG9tfGRpcmVjdG9yeXxmYWxzZXxmb3JjZXxoaWRlfGhpZ2hlc3R8aWZkaWZmfGlmbmV3ZXJ8aW5zdGZpbGVzfGxhc3R1c2VkfGxlYXZlfGxlZnR8bGljZW5zZXxsaXN0b25seXxsem1hfG5ldmVyc2hvd3xub25lfG5vcm1hbHxub3RzZXR8b2ZmfG9ufHJpZ2h0fHNob3d8c2lsZW50fHNpbGVudGxvZ3x0ZXh0b25seXx0b3B8dHJ1ZXx0cnl8dW5cXC5jb21wb25lbnRzfHVuXFwuY3VzdG9tfHVuXFwuZGlyZWN0b3J5fHVuXFwuaW5zdGZpbGVzfHVuXFwubGljZW5zZXx1bmluc3RDb25maXJtfHVzZXJ8V2luMTB8V2luN3xXaW44fFdpblZpc3RhfHgtODYtKGFuc2l8dW5pY29kZSl8emxpYilcXGIvaSxcbiAgICB0b2tlbjogXCJidWlsdGluXCJcbiAgfSxcbiAgLy8gTG9naWNMaWIubnNoXG4gIHtcbiAgICByZWdleDogL1xcJFxceyg/OkFuZCg/OklmKD86Tm90KT98VW5sZXNzKXxCcmVha3xDYXNlKD86MnwzfDR8NXxFbHNlKT98Q29udGludWV8RGVmYXVsdHxEbyg/OlVudGlsfFdoaWxlKT98RWxzZSg/OklmKD86Tm90KT98VW5sZXNzKT98RW5kKD86SWZ8U2VsZWN0fFN3aXRjaCl8RXhpdCg/OkRvfEZvcnxXaGlsZSl8Rm9yKD86RWFjaCk/fElmKD86Q21kfE5vdCg/OlRoZW4pP3xUaGVuKT98TG9vcCg/OlVudGlsfFdoaWxlKT98T3IoPzpJZig/Ok5vdCk/fFVubGVzcyl8U2VsZWN0fFN3aXRjaHxVbmxlc3N8V2hpbGUpXFx9L2ksXG4gICAgdG9rZW46IFwidmFyaWFibGUtMlwiLFxuICAgIGluZGVudDogdHJ1ZVxuICB9LFxuICAvLyBGaWxlRnVuYy5uc2hcbiAge1xuICAgIHJlZ2V4OiAvXFwkXFx7KD86QmFubmVyVHJpbVBhdGh8RGlyU3RhdGV8RHJpdmVTcGFjZXxHZXQoQmFzZU5hbWV8RHJpdmVzfEV4ZU5hbWV8RXhlUGF0aHxGaWxlQXR0cmlidXRlc3xGaWxlRXh0fEZpbGVOYW1lfEZpbGVWZXJzaW9ufE9wdGlvbnN8T3B0aW9uc1N8UGFyYW1ldGVyc3xQYXJlbnR8Um9vdHxTaXplfFRpbWUpfExvY2F0ZXxSZWZyZXNoU2hlbGxJY29ucylcXH0vaSxcbiAgICB0b2tlbjogXCJ2YXJpYWJsZS0yXCIsXG4gICAgZGVkZW50OiB0cnVlXG4gIH0sXG4gIC8vIE1lbWVudG8ubnNoXG4gIHtcbiAgICByZWdleDogL1xcJFxceyg/Ok1lbWVudG8oPzpTZWN0aW9uKD86RG9uZXxFbmR8UmVzdG9yZXxTYXZlKT98VW5zZWxlY3RlZFNlY3Rpb24pKVxcfS9pLFxuICAgIHRva2VuOiBcInZhcmlhYmxlLTJcIixcbiAgICBkZWRlbnQ6IHRydWVcbiAgfSxcbiAgLy8gVGV4dEZ1bmMubnNoXG4gIHtcbiAgICByZWdleDogL1xcJFxceyg/OkNvbmZpZyg/OlJlYWR8UmVhZFN8V3JpdGV8V3JpdGVTKXxGaWxlKD86Sm9pbnxSZWFkRnJvbUVuZHxSZWNvZGUpfExpbmUoPzpGaW5kfFJlYWR8U3VtKXxUZXh0KD86Q29tcGFyZXxDb21wYXJlUyl8VHJpbU5ld0xpbmVzKVxcfS9pLFxuICAgIHRva2VuOiBcInZhcmlhYmxlLTJcIixcbiAgICBkZWRlbnQ6IHRydWVcbiAgfSxcbiAgLy8gV2luVmVyLm5zaFxuICB7XG4gICAgcmVnZXg6IC9cXCRcXHsoPzooPzpBdCg/OkxlYXN0fE1vc3QpfElzKSg/OlNlcnZpY2VQYWNrfFdpbig/Ojd8OHwxMHw5NXw5OHwyMDAoPzowfDN8OCg/OlIyKT8pfE1FfE5UNHxWaXN0YXxYUCkpfElzKD86TlR8U2VydmVyKSlcXH0vaSxcbiAgICB0b2tlbjogXCJ2YXJpYWJsZVwiLFxuICAgIGRlZGVudDogdHJ1ZVxuICB9LFxuICAvLyBXb3JkRnVuYy5uc2hcbiAge1xuICAgIHJlZ2V4OiAvXFwkXFx7KD86U3RyRmlsdGVyUz98VmVyc2lvbig/OkNvbXBhcmV8Q29udmVydCl8V29yZCg/OkFkZFM/fEZpbmQoPzooPzoyfDMpWCk/Uz98SW5zZXJ0Uz98UmVwbGFjZVM/KSlcXH0vaSxcbiAgICB0b2tlbjogXCJrZXl3b3JkXCIsXG4gICAgZGVkZW50OiB0cnVlXG4gIH0sXG4gIC8vIHg2NC5uc2hcbiAge1xuICAgIHJlZ2V4OiAvXFwkXFx7KD86UnVubmluZ1g2NClcXH0vaSxcbiAgICB0b2tlbjogXCJ2YXJpYWJsZVwiLFxuICAgIGRlZGVudDogdHJ1ZVxuICB9LCB7XG4gICAgcmVnZXg6IC9cXCRcXHsoPzpEaXNhYmxlfEVuYWJsZSlYNjRGU1JlZGlyZWN0aW9uXFx9L2ksXG4gICAgdG9rZW46IFwia2V5d29yZFwiLFxuICAgIGRlZGVudDogdHJ1ZVxuICB9LFxuICAvLyBMaW5lIENvbW1lbnRcbiAge1xuICAgIHJlZ2V4OiAvKCN8OykuKi8sXG4gICAgdG9rZW46IFwiY29tbWVudFwiXG4gIH0sXG4gIC8vIEJsb2NrIENvbW1lbnRcbiAge1xuICAgIHJlZ2V4OiAvXFwvXFwqLyxcbiAgICB0b2tlbjogXCJjb21tZW50XCIsXG4gICAgbmV4dDogXCJjb21tZW50XCJcbiAgfSxcbiAgLy8gT3BlcmF0b3JcbiAge1xuICAgIHJlZ2V4OiAvWy0rXFwvKj08PiFdKy8sXG4gICAgdG9rZW46IFwib3BlcmF0b3JcIlxuICB9LFxuICAvLyBWYXJpYWJsZVxuICB7XG4gICAgcmVnZXg6IC9cXCRcXHdbXFx3XFwuXSovLFxuICAgIHRva2VuOiBcInZhcmlhYmxlXCJcbiAgfSxcbiAgLy8gQ29uc3RhbnRcbiAge1xuICAgIHJlZ2V4OiAvXFwke1tcXCFcXHdcXC46LV0rfS8sXG4gICAgdG9rZW46IFwidmFyaWFibGVOYW1lLmNvbnN0YW50XCJcbiAgfSxcbiAgLy8gTGFuZ3VhZ2UgU3RyaW5nXG4gIHtcbiAgICByZWdleDogL1xcJFxcKFtcXCFcXHdcXC46LV0rXFwpLyxcbiAgICB0b2tlbjogXCJhdG9tXCJcbiAgfV0sXG4gIGNvbW1lbnQ6IFt7XG4gICAgcmVnZXg6IC8uKj9cXCpcXC8vLFxuICAgIHRva2VuOiBcImNvbW1lbnRcIixcbiAgICBuZXh0OiBcInN0YXJ0XCJcbiAgfSwge1xuICAgIHJlZ2V4OiAvLiovLFxuICAgIHRva2VuOiBcImNvbW1lbnRcIlxuICB9XSxcbiAgbGFuZ3VhZ2VEYXRhOiB7XG4gICAgbmFtZTogXCJuc2lzXCIsXG4gICAgaW5kZW50T25JbnB1dDogL15cXHMqKChGdW5jdGlvbnxQYWdlRXh8U2VjdGlvbnxTZWN0aW9uKEdyb3VwKT8pRW5kfChcXCEoZW5kaWZ8bWFjcm9lbmQpKXxcXCRcXHsoRW5kKElmfFVubGVzc3xXaGlsZSl8TG9vcChVbnRpbCl8TmV4dClcXH0pJC9pLFxuICAgIGNvbW1lbnRUb2tlbnM6IHtcbiAgICAgIGxpbmU6IFwiI1wiLFxuICAgICAgYmxvY2s6IHtcbiAgICAgICAgb3BlbjogXCIvKlwiLFxuICAgICAgICBjbG9zZTogXCIqL1wiXG4gICAgICB9XG4gICAgfVxuICB9XG59KTsiLCJleHBvcnQgZnVuY3Rpb24gc2ltcGxlTW9kZShzdGF0ZXMpIHtcbiAgZW5zdXJlU3RhdGUoc3RhdGVzLCBcInN0YXJ0XCIpO1xuICB2YXIgc3RhdGVzXyA9IHt9LFxuICAgIG1ldGEgPSBzdGF0ZXMubGFuZ3VhZ2VEYXRhIHx8IHt9LFxuICAgIGhhc0luZGVudGF0aW9uID0gZmFsc2U7XG4gIGZvciAodmFyIHN0YXRlIGluIHN0YXRlcykgaWYgKHN0YXRlICE9IG1ldGEgJiYgc3RhdGVzLmhhc093blByb3BlcnR5KHN0YXRlKSkge1xuICAgIHZhciBsaXN0ID0gc3RhdGVzX1tzdGF0ZV0gPSBbXSxcbiAgICAgIG9yaWcgPSBzdGF0ZXNbc3RhdGVdO1xuICAgIGZvciAodmFyIGkgPSAwOyBpIDwgb3JpZy5sZW5ndGg7IGkrKykge1xuICAgICAgdmFyIGRhdGEgPSBvcmlnW2ldO1xuICAgICAgbGlzdC5wdXNoKG5ldyBSdWxlKGRhdGEsIHN0YXRlcykpO1xuICAgICAgaWYgKGRhdGEuaW5kZW50IHx8IGRhdGEuZGVkZW50KSBoYXNJbmRlbnRhdGlvbiA9IHRydWU7XG4gICAgfVxuICB9XG4gIHJldHVybiB7XG4gICAgbmFtZTogbWV0YS5uYW1lLFxuICAgIHN0YXJ0U3RhdGU6IGZ1bmN0aW9uICgpIHtcbiAgICAgIHJldHVybiB7XG4gICAgICAgIHN0YXRlOiBcInN0YXJ0XCIsXG4gICAgICAgIHBlbmRpbmc6IG51bGwsXG4gICAgICAgIGluZGVudDogaGFzSW5kZW50YXRpb24gPyBbXSA6IG51bGxcbiAgICAgIH07XG4gICAgfSxcbiAgICBjb3B5U3RhdGU6IGZ1bmN0aW9uIChzdGF0ZSkge1xuICAgICAgdmFyIHMgPSB7XG4gICAgICAgIHN0YXRlOiBzdGF0ZS5zdGF0ZSxcbiAgICAgICAgcGVuZGluZzogc3RhdGUucGVuZGluZyxcbiAgICAgICAgaW5kZW50OiBzdGF0ZS5pbmRlbnQgJiYgc3RhdGUuaW5kZW50LnNsaWNlKDApXG4gICAgICB9O1xuICAgICAgaWYgKHN0YXRlLnN0YWNrKSBzLnN0YWNrID0gc3RhdGUuc3RhY2suc2xpY2UoMCk7XG4gICAgICByZXR1cm4gcztcbiAgICB9LFxuICAgIHRva2VuOiB0b2tlbkZ1bmN0aW9uKHN0YXRlc18pLFxuICAgIGluZGVudDogaW5kZW50RnVuY3Rpb24oc3RhdGVzXywgbWV0YSksXG4gICAgbGFuZ3VhZ2VEYXRhOiBtZXRhXG4gIH07XG59XG47XG5mdW5jdGlvbiBlbnN1cmVTdGF0ZShzdGF0ZXMsIG5hbWUpIHtcbiAgaWYgKCFzdGF0ZXMuaGFzT3duUHJvcGVydHkobmFtZSkpIHRocm93IG5ldyBFcnJvcihcIlVuZGVmaW5lZCBzdGF0ZSBcIiArIG5hbWUgKyBcIiBpbiBzaW1wbGUgbW9kZVwiKTtcbn1cbmZ1bmN0aW9uIHRvUmVnZXgodmFsLCBjYXJldCkge1xuICBpZiAoIXZhbCkgcmV0dXJuIC8oPzopLztcbiAgdmFyIGZsYWdzID0gXCJcIjtcbiAgaWYgKHZhbCBpbnN0YW5jZW9mIFJlZ0V4cCkge1xuICAgIGlmICh2YWwuaWdub3JlQ2FzZSkgZmxhZ3MgPSBcImlcIjtcbiAgICB2YWwgPSB2YWwuc291cmNlO1xuICB9IGVsc2Uge1xuICAgIHZhbCA9IFN0cmluZyh2YWwpO1xuICB9XG4gIHJldHVybiBuZXcgUmVnRXhwKChjYXJldCA9PT0gZmFsc2UgPyBcIlwiIDogXCJeXCIpICsgXCIoPzpcIiArIHZhbCArIFwiKVwiLCBmbGFncyk7XG59XG5mdW5jdGlvbiBhc1Rva2VuKHZhbCkge1xuICBpZiAoIXZhbCkgcmV0dXJuIG51bGw7XG4gIGlmICh2YWwuYXBwbHkpIHJldHVybiB2YWw7XG4gIGlmICh0eXBlb2YgdmFsID09IFwic3RyaW5nXCIpIHJldHVybiB2YWwucmVwbGFjZSgvXFwuL2csIFwiIFwiKTtcbiAgdmFyIHJlc3VsdCA9IFtdO1xuICBmb3IgKHZhciBpID0gMDsgaSA8IHZhbC5sZW5ndGg7IGkrKykgcmVzdWx0LnB1c2godmFsW2ldICYmIHZhbFtpXS5yZXBsYWNlKC9cXC4vZywgXCIgXCIpKTtcbiAgcmV0dXJuIHJlc3VsdDtcbn1cbmZ1bmN0aW9uIFJ1bGUoZGF0YSwgc3RhdGVzKSB7XG4gIGlmIChkYXRhLm5leHQgfHwgZGF0YS5wdXNoKSBlbnN1cmVTdGF0ZShzdGF0ZXMsIGRhdGEubmV4dCB8fCBkYXRhLnB1c2gpO1xuICB0aGlzLnJlZ2V4ID0gdG9SZWdleChkYXRhLnJlZ2V4KTtcbiAgdGhpcy50b2tlbiA9IGFzVG9rZW4oZGF0YS50b2tlbik7XG4gIHRoaXMuZGF0YSA9IGRhdGE7XG59XG5mdW5jdGlvbiB0b2tlbkZ1bmN0aW9uKHN0YXRlcykge1xuICByZXR1cm4gZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICBpZiAoc3RhdGUucGVuZGluZykge1xuICAgICAgdmFyIHBlbmQgPSBzdGF0ZS5wZW5kaW5nLnNoaWZ0KCk7XG4gICAgICBpZiAoc3RhdGUucGVuZGluZy5sZW5ndGggPT0gMCkgc3RhdGUucGVuZGluZyA9IG51bGw7XG4gICAgICBzdHJlYW0ucG9zICs9IHBlbmQudGV4dC5sZW5ndGg7XG4gICAgICByZXR1cm4gcGVuZC50b2tlbjtcbiAgICB9XG4gICAgdmFyIGN1clN0YXRlID0gc3RhdGVzW3N0YXRlLnN0YXRlXTtcbiAgICBmb3IgKHZhciBpID0gMDsgaSA8IGN1clN0YXRlLmxlbmd0aDsgaSsrKSB7XG4gICAgICB2YXIgcnVsZSA9IGN1clN0YXRlW2ldO1xuICAgICAgdmFyIG1hdGNoZXMgPSAoIXJ1bGUuZGF0YS5zb2wgfHwgc3RyZWFtLnNvbCgpKSAmJiBzdHJlYW0ubWF0Y2gocnVsZS5yZWdleCk7XG4gICAgICBpZiAobWF0Y2hlcykge1xuICAgICAgICBpZiAocnVsZS5kYXRhLm5leHQpIHtcbiAgICAgICAgICBzdGF0ZS5zdGF0ZSA9IHJ1bGUuZGF0YS5uZXh0O1xuICAgICAgICB9IGVsc2UgaWYgKHJ1bGUuZGF0YS5wdXNoKSB7XG4gICAgICAgICAgKHN0YXRlLnN0YWNrIHx8IChzdGF0ZS5zdGFjayA9IFtdKSkucHVzaChzdGF0ZS5zdGF0ZSk7XG4gICAgICAgICAgc3RhdGUuc3RhdGUgPSBydWxlLmRhdGEucHVzaDtcbiAgICAgICAgfSBlbHNlIGlmIChydWxlLmRhdGEucG9wICYmIHN0YXRlLnN0YWNrICYmIHN0YXRlLnN0YWNrLmxlbmd0aCkge1xuICAgICAgICAgIHN0YXRlLnN0YXRlID0gc3RhdGUuc3RhY2sucG9wKCk7XG4gICAgICAgIH1cbiAgICAgICAgaWYgKHJ1bGUuZGF0YS5pbmRlbnQpIHN0YXRlLmluZGVudC5wdXNoKHN0cmVhbS5pbmRlbnRhdGlvbigpICsgc3RyZWFtLmluZGVudFVuaXQpO1xuICAgICAgICBpZiAocnVsZS5kYXRhLmRlZGVudCkgc3RhdGUuaW5kZW50LnBvcCgpO1xuICAgICAgICB2YXIgdG9rZW4gPSBydWxlLnRva2VuO1xuICAgICAgICBpZiAodG9rZW4gJiYgdG9rZW4uYXBwbHkpIHRva2VuID0gdG9rZW4obWF0Y2hlcyk7XG4gICAgICAgIGlmIChtYXRjaGVzLmxlbmd0aCA+IDIgJiYgcnVsZS50b2tlbiAmJiB0eXBlb2YgcnVsZS50b2tlbiAhPSBcInN0cmluZ1wiKSB7XG4gICAgICAgICAgc3RhdGUucGVuZGluZyA9IFtdO1xuICAgICAgICAgIGZvciAodmFyIGogPSAyOyBqIDwgbWF0Y2hlcy5sZW5ndGg7IGorKykgaWYgKG1hdGNoZXNbal0pIHN0YXRlLnBlbmRpbmcucHVzaCh7XG4gICAgICAgICAgICB0ZXh0OiBtYXRjaGVzW2pdLFxuICAgICAgICAgICAgdG9rZW46IHJ1bGUudG9rZW5baiAtIDFdXG4gICAgICAgICAgfSk7XG4gICAgICAgICAgc3RyZWFtLmJhY2tVcChtYXRjaGVzWzBdLmxlbmd0aCAtIChtYXRjaGVzWzFdID8gbWF0Y2hlc1sxXS5sZW5ndGggOiAwKSk7XG4gICAgICAgICAgcmV0dXJuIHRva2VuWzBdO1xuICAgICAgICB9IGVsc2UgaWYgKHRva2VuICYmIHRva2VuLmpvaW4pIHtcbiAgICAgICAgICByZXR1cm4gdG9rZW5bMF07XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgcmV0dXJuIHRva2VuO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfVxuICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgcmV0dXJuIG51bGw7XG4gIH07XG59XG5mdW5jdGlvbiBpbmRlbnRGdW5jdGlvbihzdGF0ZXMsIG1ldGEpIHtcbiAgcmV0dXJuIGZ1bmN0aW9uIChzdGF0ZSwgdGV4dEFmdGVyKSB7XG4gICAgaWYgKHN0YXRlLmluZGVudCA9PSBudWxsIHx8IG1ldGEuZG9udEluZGVudFN0YXRlcyAmJiBtZXRhLmRvbmVJbmRlbnRTdGF0ZS5pbmRleE9mKHN0YXRlLnN0YXRlKSA+IC0xKSByZXR1cm4gbnVsbDtcbiAgICB2YXIgcG9zID0gc3RhdGUuaW5kZW50Lmxlbmd0aCAtIDEsXG4gICAgICBydWxlcyA9IHN0YXRlc1tzdGF0ZS5zdGF0ZV07XG4gICAgc2NhbjogZm9yICg7Oykge1xuICAgICAgZm9yICh2YXIgaSA9IDA7IGkgPCBydWxlcy5sZW5ndGg7IGkrKykge1xuICAgICAgICB2YXIgcnVsZSA9IHJ1bGVzW2ldO1xuICAgICAgICBpZiAocnVsZS5kYXRhLmRlZGVudCAmJiBydWxlLmRhdGEuZGVkZW50SWZMaW5lU3RhcnQgIT09IGZhbHNlKSB7XG4gICAgICAgICAgdmFyIG0gPSBydWxlLnJlZ2V4LmV4ZWModGV4dEFmdGVyKTtcbiAgICAgICAgICBpZiAobSAmJiBtWzBdKSB7XG4gICAgICAgICAgICBwb3MtLTtcbiAgICAgICAgICAgIGlmIChydWxlLm5leHQgfHwgcnVsZS5wdXNoKSBydWxlcyA9IHN0YXRlc1tydWxlLm5leHQgfHwgcnVsZS5wdXNoXTtcbiAgICAgICAgICAgIHRleHRBZnRlciA9IHRleHRBZnRlci5zbGljZShtWzBdLmxlbmd0aCk7XG4gICAgICAgICAgICBjb250aW51ZSBzY2FuO1xuICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgfVxuICAgICAgYnJlYWs7XG4gICAgfVxuICAgIHJldHVybiBwb3MgPCAwID8gMCA6IHN0YXRlLmluZGVudFtwb3NdO1xuICB9O1xufSJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==