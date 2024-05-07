"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[5914],{

/***/ 15914:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "sas": () => (/* binding */ sas)
/* harmony export */ });
var words = {};
var isDoubleOperatorSym = {
  eq: 'operator',
  lt: 'operator',
  le: 'operator',
  gt: 'operator',
  ge: 'operator',
  "in": 'operator',
  ne: 'operator',
  or: 'operator'
};
var isDoubleOperatorChar = /(<=|>=|!=|<>)/;
var isSingleOperatorChar = /[=\(:\),{}.*<>+\-\/^\[\]]/;

// Takes a string of words separated by spaces and adds them as
// keys with the value of the first argument 'style'
function define(style, string, context) {
  if (context) {
    var split = string.split(' ');
    for (var i = 0; i < split.length; i++) {
      words[split[i]] = {
        style: style,
        state: context
      };
    }
  }
}
//datastep
define('def', 'stack pgm view source debug nesting nolist', ['inDataStep']);
define('def', 'if while until for do do; end end; then else cancel', ['inDataStep']);
define('def', 'label format _n_ _error_', ['inDataStep']);
define('def', 'ALTER BUFNO BUFSIZE CNTLLEV COMPRESS DLDMGACTION ENCRYPT ENCRYPTKEY EXTENDOBSCOUNTER GENMAX GENNUM INDEX LABEL OBSBUF OUTREP PW PWREQ READ REPEMPTY REPLACE REUSE ROLE SORTEDBY SPILL TOBSNO TYPE WRITE FILECLOSE FIRSTOBS IN OBS POINTOBS WHERE WHEREUP IDXNAME IDXWHERE DROP KEEP RENAME', ['inDataStep']);
define('def', 'filevar finfo finv fipname fipnamel fipstate first firstobs floor', ['inDataStep']);
define('def', 'varfmt varinfmt varlabel varlen varname varnum varray varrayx vartype verify vformat vformatd vformatdx vformatn vformatnx vformatw vformatwx vformatx vinarray vinarrayx vinformat vinformatd vinformatdx vinformatn vinformatnx vinformatw vinformatwx vinformatx vlabel vlabelx vlength vlengthx vname vnamex vnferr vtype vtypex weekday', ['inDataStep']);
define('def', 'zipfips zipname zipnamel zipstate', ['inDataStep']);
define('def', 'put putc putn', ['inDataStep']);
define('builtin', 'data run', ['inDataStep']);

//proc
define('def', 'data', ['inProc']);

// flow control for macros
define('def', '%if %end %end; %else %else; %do %do; %then', ['inMacro']);

//everywhere
define('builtin', 'proc run; quit; libname filename %macro %mend option options', ['ALL']);
define('def', 'footnote title libname ods', ['ALL']);
define('def', '%let %put %global %sysfunc %eval ', ['ALL']);
// automatic macro variables http://support.sas.com/documentation/cdl/en/mcrolref/61885/HTML/default/viewer.htm#a003167023.htm
define('variable', '&sysbuffr &syscc &syscharwidth &syscmd &sysdate &sysdate9 &sysday &sysdevic &sysdmg &sysdsn &sysencoding &sysenv &syserr &syserrortext &sysfilrc &syshostname &sysindex &sysinfo &sysjobid &syslast &syslckrc &syslibrc &syslogapplname &sysmacroname &sysmenv &sysmsg &sysncpu &sysodspath &sysparm &syspbuff &sysprocessid &sysprocessname &sysprocname &sysrc &sysscp &sysscpl &sysscpl &syssite &sysstartid &sysstartname &systcpiphostname &systime &sysuserid &sysver &sysvlong &sysvlong4 &syswarningtext', ['ALL']);

//footnote[1-9]? title[1-9]?

//options statement
define('def', 'source2 nosource2 page pageno pagesize', ['ALL']);

//proc and datastep
define('def', '_all_ _character_ _cmd_ _freq_ _i_ _infile_ _last_ _msg_ _null_ _numeric_ _temporary_ _type_ abort abs addr adjrsq airy alpha alter altlog altprint and arcos array arsin as atan attrc attrib attrn authserver autoexec awscontrol awsdef awsmenu awsmenumerge awstitle backward band base betainv between blocksize blshift bnot bor brshift bufno bufsize bxor by byerr byline byte calculated call cards cards4 catcache cbufno cdf ceil center cexist change chisq cinv class cleanup close cnonct cntllev coalesce codegen col collate collin column comamid comaux1 comaux2 comdef compbl compound compress config continue convert cos cosh cpuid create cross crosstab css curobs cv daccdb daccdbsl daccsl daccsyd dacctab dairy datalines datalines4 datejul datepart datetime day dbcslang dbcstype dclose ddfm ddm delete delimiter depdb depdbsl depsl depsyd deptab dequote descending descript design= device dflang dhms dif digamma dim dinfo display distinct dkricond dkrocond dlm dnum do dopen doptname doptnum dread drop dropnote dsname dsnferr echo else emaildlg emailid emailpw emailserver emailsys encrypt end endsas engine eof eov erf erfc error errorcheck errors exist exp fappend fclose fcol fdelete feedback fetch fetchobs fexist fget file fileclose fileexist filefmt filename fileref  fmterr fmtsearch fnonct fnote font fontalias  fopen foptname foptnum force formatted formchar formdelim formdlim forward fpoint fpos fput fread frewind frlen from fsep fuzz fwrite gaminv gamma getoption getvarc getvarn go goto group gwindow hbar hbound helpenv helploc hms honorappearance hosthelp hostprint hour hpct html hvar ibessel ibr id if index indexc indexw initcmd initstmt inner input inputc inputn inr insert int intck intnx into intrr invaliddata irr is jbessel join juldate keep kentb kurtosis label lag last lbound leave left length levels lgamma lib  library libref line linesize link list log log10 log2 logpdf logpmf logsdf lostcard lowcase lrecl ls macro macrogen maps mautosource max maxdec maxr mdy mean measures median memtype merge merror min minute missing missover mlogic mod mode model modify month mopen mort mprint mrecall msglevel msymtabmax mvarsize myy n nest netpv new news nmiss no nobatch nobs nocaps nocardimage nocenter nocharcode nocmdmac nocol nocum nodate nodbcs nodetails nodmr nodms nodmsbatch nodup nodupkey noduplicates noechoauto noequals noerrorabend noexitwindows nofullstimer noicon noimplmac noint nolist noloadlist nomiss nomlogic nomprint nomrecall nomsgcase nomstored nomultenvappl nonotes nonumber noobs noovp nopad nopercent noprint noprintinit normal norow norsasuser nosetinit  nosplash nosymbolgen note notes notitle notitles notsorted noverbose noxsync noxwait npv null number numkeys nummousekeys nway obs  on open     order ordinal otherwise out outer outp= output over ovp p(1 5 10 25 50 75 90 95 99) pad pad2  paired parm parmcards path pathdll pathname pdf peek peekc pfkey pmf point poisson poke position printer probbeta probbnml probchi probf probgam probhypr probit probnegb probnorm probsig probt procleave prt ps  pw pwreq qtr quote r ranbin rancau random ranexp rangam range ranks rannor ranpoi rantbl rantri ranuni rcorr read recfm register regr remote remove rename repeat repeated replace resolve retain return reuse reverse rewind right round rsquare rtf rtrace rtraceloc s s2 samploc sasautos sascontrol sasfrscr sasmsg sasmstore sasscript sasuser saving scan sdf second select selection separated seq serror set setcomm setot sign simple sin sinh siteinfo skewness skip sle sls sortedby sortpgm sortseq sortsize soundex  spedis splashlocation split spool sqrt start std stderr stdin stfips stimer stname stnamel stop stopover sub subgroup subpopn substr sum sumwgt symbol symbolgen symget symput sysget sysin sysleave sysmsg sysparm sysprint sysprintfont sysprod sysrc system t table tables tan tanh tapeclose tbufsize terminal test then timepart tinv  tnonct to today tol tooldef totper transformout translate trantab tranwrd trigamma trim trimn trunc truncover type unformatted uniform union until upcase update user usericon uss validate value var  weight when where while wincharset window work workinit workterm write wsum xsync xwait yearcutoff yes yyq  min max', ['inDataStep', 'inProc']);
define('operator', 'and not ', ['inDataStep', 'inProc']);

// Main function
function tokenize(stream, state) {
  // Finally advance the stream
  var ch = stream.next();

  // BLOCKCOMMENT
  if (ch === '/' && stream.eat('*')) {
    state.continueComment = true;
    return "comment";
  } else if (state.continueComment === true) {
    // in comment block
    //comment ends at the beginning of the line
    if (ch === '*' && stream.peek() === '/') {
      stream.next();
      state.continueComment = false;
    } else if (stream.skipTo('*')) {
      //comment is potentially later in line
      stream.skipTo('*');
      stream.next();
      if (stream.eat('/')) state.continueComment = false;
    } else {
      stream.skipToEnd();
    }
    return "comment";
  }
  if (ch == "*" && stream.column() == stream.indentation()) {
    stream.skipToEnd();
    return "comment";
  }

  // DoubleOperator match
  var doubleOperator = ch + stream.peek();
  if ((ch === '"' || ch === "'") && !state.continueString) {
    state.continueString = ch;
    return "string";
  } else if (state.continueString) {
    if (state.continueString == ch) {
      state.continueString = null;
    } else if (stream.skipTo(state.continueString)) {
      // quote found on this line
      stream.next();
      state.continueString = null;
    } else {
      stream.skipToEnd();
    }
    return "string";
  } else if (state.continueString !== null && stream.eol()) {
    stream.skipTo(state.continueString) || stream.skipToEnd();
    return "string";
  } else if (/[\d\.]/.test(ch)) {
    //find numbers
    if (ch === ".") stream.match(/^[0-9]+([eE][\-+]?[0-9]+)?/);else if (ch === "0") stream.match(/^[xX][0-9a-fA-F]+/) || stream.match(/^0[0-7]+/);else stream.match(/^[0-9]*\.?[0-9]*([eE][\-+]?[0-9]+)?/);
    return "number";
  } else if (isDoubleOperatorChar.test(ch + stream.peek())) {
    // TWO SYMBOL TOKENS
    stream.next();
    return "operator";
  } else if (isDoubleOperatorSym.hasOwnProperty(doubleOperator)) {
    stream.next();
    if (stream.peek() === ' ') return isDoubleOperatorSym[doubleOperator.toLowerCase()];
  } else if (isSingleOperatorChar.test(ch)) {
    // SINGLE SYMBOL TOKENS
    return "operator";
  }

  // Matches one whole word -- even if the word is a character
  var word;
  if (stream.match(/[%&;\w]+/, false) != null) {
    word = ch + stream.match(/[%&;\w]+/, true);
    if (/&/.test(word)) return 'variable';
  } else {
    word = ch;
  }
  // the word after DATA PROC or MACRO
  if (state.nextword) {
    stream.match(/[\w]+/);
    // match memname.libname
    if (stream.peek() === '.') stream.skipTo(' ');
    state.nextword = false;
    return 'variableName.special';
  }
  word = word.toLowerCase();
  // Are we in a DATA Step?
  if (state.inDataStep) {
    if (word === 'run;' || stream.match(/run\s;/)) {
      state.inDataStep = false;
      return 'builtin';
    }
    // variable formats
    if (word && stream.next() === '.') {
      //either a format or libname.memname
      if (/\w/.test(stream.peek())) return 'variableName.special';else return 'variable';
    }
    // do we have a DATA Step keyword
    if (word && words.hasOwnProperty(word) && (words[word].state.indexOf("inDataStep") !== -1 || words[word].state.indexOf("ALL") !== -1)) {
      //backup to the start of the word
      if (stream.start < stream.pos) stream.backUp(stream.pos - stream.start);
      //advance the length of the word and return
      for (var i = 0; i < word.length; ++i) stream.next();
      return words[word].style;
    }
  }
  // Are we in an Proc statement?
  if (state.inProc) {
    if (word === 'run;' || word === 'quit;') {
      state.inProc = false;
      return 'builtin';
    }
    // do we have a proc keyword
    if (word && words.hasOwnProperty(word) && (words[word].state.indexOf("inProc") !== -1 || words[word].state.indexOf("ALL") !== -1)) {
      stream.match(/[\w]+/);
      return words[word].style;
    }
  }
  // Are we in a Macro statement?
  if (state.inMacro) {
    if (word === '%mend') {
      if (stream.peek() === ';') stream.next();
      state.inMacro = false;
      return 'builtin';
    }
    if (word && words.hasOwnProperty(word) && (words[word].state.indexOf("inMacro") !== -1 || words[word].state.indexOf("ALL") !== -1)) {
      stream.match(/[\w]+/);
      return words[word].style;
    }
    return 'atom';
  }
  // Do we have Keywords specific words?
  if (word && words.hasOwnProperty(word)) {
    // Negates the initial next()
    stream.backUp(1);
    // Actually move the stream
    stream.match(/[\w]+/);
    if (word === 'data' && /=/.test(stream.peek()) === false) {
      state.inDataStep = true;
      state.nextword = true;
      return 'builtin';
    }
    if (word === 'proc') {
      state.inProc = true;
      state.nextword = true;
      return 'builtin';
    }
    if (word === '%macro') {
      state.inMacro = true;
      state.nextword = true;
      return 'builtin';
    }
    if (/title[1-9]/.test(word)) return 'def';
    if (word === 'footnote') {
      stream.eat(/[1-9]/);
      return 'def';
    }

    // Returns their value as state in the prior define methods
    if (state.inDataStep === true && words[word].state.indexOf("inDataStep") !== -1) return words[word].style;
    if (state.inProc === true && words[word].state.indexOf("inProc") !== -1) return words[word].style;
    if (state.inMacro === true && words[word].state.indexOf("inMacro") !== -1) return words[word].style;
    if (words[word].state.indexOf("ALL") !== -1) return words[word].style;
    return null;
  }
  // Unrecognized syntax
  return null;
}
const sas = {
  name: "sas",
  startState: function () {
    return {
      inDataStep: false,
      inProc: false,
      inMacro: false,
      nextword: false,
      continueString: null,
      continueComment: false
    };
  },
  token: function (stream, state) {
    // Strip the spaces, but regex will account for them either way
    if (stream.eatSpace()) return null;
    // Go through the main process
    return tokenize(stream, state);
  },
  languageData: {
    commentTokens: {
      block: {
        open: "/*",
        close: "*/"
      }
    }
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNTkxNC5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGNvZGVtaXJyb3IvbGVnYWN5LW1vZGVzL21vZGUvc2FzLmpzIl0sInNvdXJjZXNDb250ZW50IjpbInZhciB3b3JkcyA9IHt9O1xudmFyIGlzRG91YmxlT3BlcmF0b3JTeW0gPSB7XG4gIGVxOiAnb3BlcmF0b3InLFxuICBsdDogJ29wZXJhdG9yJyxcbiAgbGU6ICdvcGVyYXRvcicsXG4gIGd0OiAnb3BlcmF0b3InLFxuICBnZTogJ29wZXJhdG9yJyxcbiAgXCJpblwiOiAnb3BlcmF0b3InLFxuICBuZTogJ29wZXJhdG9yJyxcbiAgb3I6ICdvcGVyYXRvcidcbn07XG52YXIgaXNEb3VibGVPcGVyYXRvckNoYXIgPSAvKDw9fD49fCE9fDw+KS87XG52YXIgaXNTaW5nbGVPcGVyYXRvckNoYXIgPSAvWz1cXCg6XFwpLHt9Lio8PitcXC1cXC9eXFxbXFxdXS87XG5cbi8vIFRha2VzIGEgc3RyaW5nIG9mIHdvcmRzIHNlcGFyYXRlZCBieSBzcGFjZXMgYW5kIGFkZHMgdGhlbSBhc1xuLy8ga2V5cyB3aXRoIHRoZSB2YWx1ZSBvZiB0aGUgZmlyc3QgYXJndW1lbnQgJ3N0eWxlJ1xuZnVuY3Rpb24gZGVmaW5lKHN0eWxlLCBzdHJpbmcsIGNvbnRleHQpIHtcbiAgaWYgKGNvbnRleHQpIHtcbiAgICB2YXIgc3BsaXQgPSBzdHJpbmcuc3BsaXQoJyAnKTtcbiAgICBmb3IgKHZhciBpID0gMDsgaSA8IHNwbGl0Lmxlbmd0aDsgaSsrKSB7XG4gICAgICB3b3Jkc1tzcGxpdFtpXV0gPSB7XG4gICAgICAgIHN0eWxlOiBzdHlsZSxcbiAgICAgICAgc3RhdGU6IGNvbnRleHRcbiAgICAgIH07XG4gICAgfVxuICB9XG59XG4vL2RhdGFzdGVwXG5kZWZpbmUoJ2RlZicsICdzdGFjayBwZ20gdmlldyBzb3VyY2UgZGVidWcgbmVzdGluZyBub2xpc3QnLCBbJ2luRGF0YVN0ZXAnXSk7XG5kZWZpbmUoJ2RlZicsICdpZiB3aGlsZSB1bnRpbCBmb3IgZG8gZG87IGVuZCBlbmQ7IHRoZW4gZWxzZSBjYW5jZWwnLCBbJ2luRGF0YVN0ZXAnXSk7XG5kZWZpbmUoJ2RlZicsICdsYWJlbCBmb3JtYXQgX25fIF9lcnJvcl8nLCBbJ2luRGF0YVN0ZXAnXSk7XG5kZWZpbmUoJ2RlZicsICdBTFRFUiBCVUZOTyBCVUZTSVpFIENOVExMRVYgQ09NUFJFU1MgRExETUdBQ1RJT04gRU5DUllQVCBFTkNSWVBUS0VZIEVYVEVORE9CU0NPVU5URVIgR0VOTUFYIEdFTk5VTSBJTkRFWCBMQUJFTCBPQlNCVUYgT1VUUkVQIFBXIFBXUkVRIFJFQUQgUkVQRU1QVFkgUkVQTEFDRSBSRVVTRSBST0xFIFNPUlRFREJZIFNQSUxMIFRPQlNOTyBUWVBFIFdSSVRFIEZJTEVDTE9TRSBGSVJTVE9CUyBJTiBPQlMgUE9JTlRPQlMgV0hFUkUgV0hFUkVVUCBJRFhOQU1FIElEWFdIRVJFIERST1AgS0VFUCBSRU5BTUUnLCBbJ2luRGF0YVN0ZXAnXSk7XG5kZWZpbmUoJ2RlZicsICdmaWxldmFyIGZpbmZvIGZpbnYgZmlwbmFtZSBmaXBuYW1lbCBmaXBzdGF0ZSBmaXJzdCBmaXJzdG9icyBmbG9vcicsIFsnaW5EYXRhU3RlcCddKTtcbmRlZmluZSgnZGVmJywgJ3ZhcmZtdCB2YXJpbmZtdCB2YXJsYWJlbCB2YXJsZW4gdmFybmFtZSB2YXJudW0gdmFycmF5IHZhcnJheXggdmFydHlwZSB2ZXJpZnkgdmZvcm1hdCB2Zm9ybWF0ZCB2Zm9ybWF0ZHggdmZvcm1hdG4gdmZvcm1hdG54IHZmb3JtYXR3IHZmb3JtYXR3eCB2Zm9ybWF0eCB2aW5hcnJheSB2aW5hcnJheXggdmluZm9ybWF0IHZpbmZvcm1hdGQgdmluZm9ybWF0ZHggdmluZm9ybWF0biB2aW5mb3JtYXRueCB2aW5mb3JtYXR3IHZpbmZvcm1hdHd4IHZpbmZvcm1hdHggdmxhYmVsIHZsYWJlbHggdmxlbmd0aCB2bGVuZ3RoeCB2bmFtZSB2bmFtZXggdm5mZXJyIHZ0eXBlIHZ0eXBleCB3ZWVrZGF5JywgWydpbkRhdGFTdGVwJ10pO1xuZGVmaW5lKCdkZWYnLCAnemlwZmlwcyB6aXBuYW1lIHppcG5hbWVsIHppcHN0YXRlJywgWydpbkRhdGFTdGVwJ10pO1xuZGVmaW5lKCdkZWYnLCAncHV0IHB1dGMgcHV0bicsIFsnaW5EYXRhU3RlcCddKTtcbmRlZmluZSgnYnVpbHRpbicsICdkYXRhIHJ1bicsIFsnaW5EYXRhU3RlcCddKTtcblxuLy9wcm9jXG5kZWZpbmUoJ2RlZicsICdkYXRhJywgWydpblByb2MnXSk7XG5cbi8vIGZsb3cgY29udHJvbCBmb3IgbWFjcm9zXG5kZWZpbmUoJ2RlZicsICclaWYgJWVuZCAlZW5kOyAlZWxzZSAlZWxzZTsgJWRvICVkbzsgJXRoZW4nLCBbJ2luTWFjcm8nXSk7XG5cbi8vZXZlcnl3aGVyZVxuZGVmaW5lKCdidWlsdGluJywgJ3Byb2MgcnVuOyBxdWl0OyBsaWJuYW1lIGZpbGVuYW1lICVtYWNybyAlbWVuZCBvcHRpb24gb3B0aW9ucycsIFsnQUxMJ10pO1xuZGVmaW5lKCdkZWYnLCAnZm9vdG5vdGUgdGl0bGUgbGlibmFtZSBvZHMnLCBbJ0FMTCddKTtcbmRlZmluZSgnZGVmJywgJyVsZXQgJXB1dCAlZ2xvYmFsICVzeXNmdW5jICVldmFsICcsIFsnQUxMJ10pO1xuLy8gYXV0b21hdGljIG1hY3JvIHZhcmlhYmxlcyBodHRwOi8vc3VwcG9ydC5zYXMuY29tL2RvY3VtZW50YXRpb24vY2RsL2VuL21jcm9scmVmLzYxODg1L0hUTUwvZGVmYXVsdC92aWV3ZXIuaHRtI2EwMDMxNjcwMjMuaHRtXG5kZWZpbmUoJ3ZhcmlhYmxlJywgJyZzeXNidWZmciAmc3lzY2MgJnN5c2NoYXJ3aWR0aCAmc3lzY21kICZzeXNkYXRlICZzeXNkYXRlOSAmc3lzZGF5ICZzeXNkZXZpYyAmc3lzZG1nICZzeXNkc24gJnN5c2VuY29kaW5nICZzeXNlbnYgJnN5c2VyciAmc3lzZXJyb3J0ZXh0ICZzeXNmaWxyYyAmc3lzaG9zdG5hbWUgJnN5c2luZGV4ICZzeXNpbmZvICZzeXNqb2JpZCAmc3lzbGFzdCAmc3lzbGNrcmMgJnN5c2xpYnJjICZzeXNsb2dhcHBsbmFtZSAmc3lzbWFjcm9uYW1lICZzeXNtZW52ICZzeXNtc2cgJnN5c25jcHUgJnN5c29kc3BhdGggJnN5c3Bhcm0gJnN5c3BidWZmICZzeXNwcm9jZXNzaWQgJnN5c3Byb2Nlc3NuYW1lICZzeXNwcm9jbmFtZSAmc3lzcmMgJnN5c3NjcCAmc3lzc2NwbCAmc3lzc2NwbCAmc3lzc2l0ZSAmc3lzc3RhcnRpZCAmc3lzc3RhcnRuYW1lICZzeXN0Y3BpcGhvc3RuYW1lICZzeXN0aW1lICZzeXN1c2VyaWQgJnN5c3ZlciAmc3lzdmxvbmcgJnN5c3Zsb25nNCAmc3lzd2FybmluZ3RleHQnLCBbJ0FMTCddKTtcblxuLy9mb290bm90ZVsxLTldPyB0aXRsZVsxLTldP1xuXG4vL29wdGlvbnMgc3RhdGVtZW50XG5kZWZpbmUoJ2RlZicsICdzb3VyY2UyIG5vc291cmNlMiBwYWdlIHBhZ2VubyBwYWdlc2l6ZScsIFsnQUxMJ10pO1xuXG4vL3Byb2MgYW5kIGRhdGFzdGVwXG5kZWZpbmUoJ2RlZicsICdfYWxsXyBfY2hhcmFjdGVyXyBfY21kXyBfZnJlcV8gX2lfIF9pbmZpbGVfIF9sYXN0XyBfbXNnXyBfbnVsbF8gX251bWVyaWNfIF90ZW1wb3JhcnlfIF90eXBlXyBhYm9ydCBhYnMgYWRkciBhZGpyc3EgYWlyeSBhbHBoYSBhbHRlciBhbHRsb2cgYWx0cHJpbnQgYW5kIGFyY29zIGFycmF5IGFyc2luIGFzIGF0YW4gYXR0cmMgYXR0cmliIGF0dHJuIGF1dGhzZXJ2ZXIgYXV0b2V4ZWMgYXdzY29udHJvbCBhd3NkZWYgYXdzbWVudSBhd3NtZW51bWVyZ2UgYXdzdGl0bGUgYmFja3dhcmQgYmFuZCBiYXNlIGJldGFpbnYgYmV0d2VlbiBibG9ja3NpemUgYmxzaGlmdCBibm90IGJvciBicnNoaWZ0IGJ1Zm5vIGJ1ZnNpemUgYnhvciBieSBieWVyciBieWxpbmUgYnl0ZSBjYWxjdWxhdGVkIGNhbGwgY2FyZHMgY2FyZHM0IGNhdGNhY2hlIGNidWZubyBjZGYgY2VpbCBjZW50ZXIgY2V4aXN0IGNoYW5nZSBjaGlzcSBjaW52IGNsYXNzIGNsZWFudXAgY2xvc2UgY25vbmN0IGNudGxsZXYgY29hbGVzY2UgY29kZWdlbiBjb2wgY29sbGF0ZSBjb2xsaW4gY29sdW1uIGNvbWFtaWQgY29tYXV4MSBjb21hdXgyIGNvbWRlZiBjb21wYmwgY29tcG91bmQgY29tcHJlc3MgY29uZmlnIGNvbnRpbnVlIGNvbnZlcnQgY29zIGNvc2ggY3B1aWQgY3JlYXRlIGNyb3NzIGNyb3NzdGFiIGNzcyBjdXJvYnMgY3YgZGFjY2RiIGRhY2NkYnNsIGRhY2NzbCBkYWNjc3lkIGRhY2N0YWIgZGFpcnkgZGF0YWxpbmVzIGRhdGFsaW5lczQgZGF0ZWp1bCBkYXRlcGFydCBkYXRldGltZSBkYXkgZGJjc2xhbmcgZGJjc3R5cGUgZGNsb3NlIGRkZm0gZGRtIGRlbGV0ZSBkZWxpbWl0ZXIgZGVwZGIgZGVwZGJzbCBkZXBzbCBkZXBzeWQgZGVwdGFiIGRlcXVvdGUgZGVzY2VuZGluZyBkZXNjcmlwdCBkZXNpZ249IGRldmljZSBkZmxhbmcgZGhtcyBkaWYgZGlnYW1tYSBkaW0gZGluZm8gZGlzcGxheSBkaXN0aW5jdCBka3JpY29uZCBka3JvY29uZCBkbG0gZG51bSBkbyBkb3BlbiBkb3B0bmFtZSBkb3B0bnVtIGRyZWFkIGRyb3AgZHJvcG5vdGUgZHNuYW1lIGRzbmZlcnIgZWNobyBlbHNlIGVtYWlsZGxnIGVtYWlsaWQgZW1haWxwdyBlbWFpbHNlcnZlciBlbWFpbHN5cyBlbmNyeXB0IGVuZCBlbmRzYXMgZW5naW5lIGVvZiBlb3YgZXJmIGVyZmMgZXJyb3IgZXJyb3JjaGVjayBlcnJvcnMgZXhpc3QgZXhwIGZhcHBlbmQgZmNsb3NlIGZjb2wgZmRlbGV0ZSBmZWVkYmFjayBmZXRjaCBmZXRjaG9icyBmZXhpc3QgZmdldCBmaWxlIGZpbGVjbG9zZSBmaWxlZXhpc3QgZmlsZWZtdCBmaWxlbmFtZSBmaWxlcmVmICBmbXRlcnIgZm10c2VhcmNoIGZub25jdCBmbm90ZSBmb250IGZvbnRhbGlhcyAgZm9wZW4gZm9wdG5hbWUgZm9wdG51bSBmb3JjZSBmb3JtYXR0ZWQgZm9ybWNoYXIgZm9ybWRlbGltIGZvcm1kbGltIGZvcndhcmQgZnBvaW50IGZwb3MgZnB1dCBmcmVhZCBmcmV3aW5kIGZybGVuIGZyb20gZnNlcCBmdXp6IGZ3cml0ZSBnYW1pbnYgZ2FtbWEgZ2V0b3B0aW9uIGdldHZhcmMgZ2V0dmFybiBnbyBnb3RvIGdyb3VwIGd3aW5kb3cgaGJhciBoYm91bmQgaGVscGVudiBoZWxwbG9jIGhtcyBob25vcmFwcGVhcmFuY2UgaG9zdGhlbHAgaG9zdHByaW50IGhvdXIgaHBjdCBodG1sIGh2YXIgaWJlc3NlbCBpYnIgaWQgaWYgaW5kZXggaW5kZXhjIGluZGV4dyBpbml0Y21kIGluaXRzdG10IGlubmVyIGlucHV0IGlucHV0YyBpbnB1dG4gaW5yIGluc2VydCBpbnQgaW50Y2sgaW50bnggaW50byBpbnRyciBpbnZhbGlkZGF0YSBpcnIgaXMgamJlc3NlbCBqb2luIGp1bGRhdGUga2VlcCBrZW50YiBrdXJ0b3NpcyBsYWJlbCBsYWcgbGFzdCBsYm91bmQgbGVhdmUgbGVmdCBsZW5ndGggbGV2ZWxzIGxnYW1tYSBsaWIgIGxpYnJhcnkgbGlicmVmIGxpbmUgbGluZXNpemUgbGluayBsaXN0IGxvZyBsb2cxMCBsb2cyIGxvZ3BkZiBsb2dwbWYgbG9nc2RmIGxvc3RjYXJkIGxvd2Nhc2UgbHJlY2wgbHMgbWFjcm8gbWFjcm9nZW4gbWFwcyBtYXV0b3NvdXJjZSBtYXggbWF4ZGVjIG1heHIgbWR5IG1lYW4gbWVhc3VyZXMgbWVkaWFuIG1lbXR5cGUgbWVyZ2UgbWVycm9yIG1pbiBtaW51dGUgbWlzc2luZyBtaXNzb3ZlciBtbG9naWMgbW9kIG1vZGUgbW9kZWwgbW9kaWZ5IG1vbnRoIG1vcGVuIG1vcnQgbXByaW50IG1yZWNhbGwgbXNnbGV2ZWwgbXN5bXRhYm1heCBtdmFyc2l6ZSBteXkgbiBuZXN0IG5ldHB2IG5ldyBuZXdzIG5taXNzIG5vIG5vYmF0Y2ggbm9icyBub2NhcHMgbm9jYXJkaW1hZ2Ugbm9jZW50ZXIgbm9jaGFyY29kZSBub2NtZG1hYyBub2NvbCBub2N1bSBub2RhdGUgbm9kYmNzIG5vZGV0YWlscyBub2RtciBub2RtcyBub2Rtc2JhdGNoIG5vZHVwIG5vZHVwa2V5IG5vZHVwbGljYXRlcyBub2VjaG9hdXRvIG5vZXF1YWxzIG5vZXJyb3JhYmVuZCBub2V4aXR3aW5kb3dzIG5vZnVsbHN0aW1lciBub2ljb24gbm9pbXBsbWFjIG5vaW50IG5vbGlzdCBub2xvYWRsaXN0IG5vbWlzcyBub21sb2dpYyBub21wcmludCBub21yZWNhbGwgbm9tc2djYXNlIG5vbXN0b3JlZCBub211bHRlbnZhcHBsIG5vbm90ZXMgbm9udW1iZXIgbm9vYnMgbm9vdnAgbm9wYWQgbm9wZXJjZW50IG5vcHJpbnQgbm9wcmludGluaXQgbm9ybWFsIG5vcm93IG5vcnNhc3VzZXIgbm9zZXRpbml0ICBub3NwbGFzaCBub3N5bWJvbGdlbiBub3RlIG5vdGVzIG5vdGl0bGUgbm90aXRsZXMgbm90c29ydGVkIG5vdmVyYm9zZSBub3hzeW5jIG5veHdhaXQgbnB2IG51bGwgbnVtYmVyIG51bWtleXMgbnVtbW91c2VrZXlzIG53YXkgb2JzICBvbiBvcGVuICAgICBvcmRlciBvcmRpbmFsIG90aGVyd2lzZSBvdXQgb3V0ZXIgb3V0cD0gb3V0cHV0IG92ZXIgb3ZwIHAoMSA1IDEwIDI1IDUwIDc1IDkwIDk1IDk5KSBwYWQgcGFkMiAgcGFpcmVkIHBhcm0gcGFybWNhcmRzIHBhdGggcGF0aGRsbCBwYXRobmFtZSBwZGYgcGVlayBwZWVrYyBwZmtleSBwbWYgcG9pbnQgcG9pc3NvbiBwb2tlIHBvc2l0aW9uIHByaW50ZXIgcHJvYmJldGEgcHJvYmJubWwgcHJvYmNoaSBwcm9iZiBwcm9iZ2FtIHByb2JoeXByIHByb2JpdCBwcm9ibmVnYiBwcm9ibm9ybSBwcm9ic2lnIHByb2J0IHByb2NsZWF2ZSBwcnQgcHMgIHB3IHB3cmVxIHF0ciBxdW90ZSByIHJhbmJpbiByYW5jYXUgcmFuZG9tIHJhbmV4cCByYW5nYW0gcmFuZ2UgcmFua3MgcmFubm9yIHJhbnBvaSByYW50YmwgcmFudHJpIHJhbnVuaSByY29yciByZWFkIHJlY2ZtIHJlZ2lzdGVyIHJlZ3IgcmVtb3RlIHJlbW92ZSByZW5hbWUgcmVwZWF0IHJlcGVhdGVkIHJlcGxhY2UgcmVzb2x2ZSByZXRhaW4gcmV0dXJuIHJldXNlIHJldmVyc2UgcmV3aW5kIHJpZ2h0IHJvdW5kIHJzcXVhcmUgcnRmIHJ0cmFjZSBydHJhY2Vsb2MgcyBzMiBzYW1wbG9jIHNhc2F1dG9zIHNhc2NvbnRyb2wgc2FzZnJzY3Igc2FzbXNnIHNhc21zdG9yZSBzYXNzY3JpcHQgc2FzdXNlciBzYXZpbmcgc2NhbiBzZGYgc2Vjb25kIHNlbGVjdCBzZWxlY3Rpb24gc2VwYXJhdGVkIHNlcSBzZXJyb3Igc2V0IHNldGNvbW0gc2V0b3Qgc2lnbiBzaW1wbGUgc2luIHNpbmggc2l0ZWluZm8gc2tld25lc3Mgc2tpcCBzbGUgc2xzIHNvcnRlZGJ5IHNvcnRwZ20gc29ydHNlcSBzb3J0c2l6ZSBzb3VuZGV4ICBzcGVkaXMgc3BsYXNobG9jYXRpb24gc3BsaXQgc3Bvb2wgc3FydCBzdGFydCBzdGQgc3RkZXJyIHN0ZGluIHN0ZmlwcyBzdGltZXIgc3RuYW1lIHN0bmFtZWwgc3RvcCBzdG9wb3ZlciBzdWIgc3ViZ3JvdXAgc3VicG9wbiBzdWJzdHIgc3VtIHN1bXdndCBzeW1ib2wgc3ltYm9sZ2VuIHN5bWdldCBzeW1wdXQgc3lzZ2V0IHN5c2luIHN5c2xlYXZlIHN5c21zZyBzeXNwYXJtIHN5c3ByaW50IHN5c3ByaW50Zm9udCBzeXNwcm9kIHN5c3JjIHN5c3RlbSB0IHRhYmxlIHRhYmxlcyB0YW4gdGFuaCB0YXBlY2xvc2UgdGJ1ZnNpemUgdGVybWluYWwgdGVzdCB0aGVuIHRpbWVwYXJ0IHRpbnYgIHRub25jdCB0byB0b2RheSB0b2wgdG9vbGRlZiB0b3RwZXIgdHJhbnNmb3Jtb3V0IHRyYW5zbGF0ZSB0cmFudGFiIHRyYW53cmQgdHJpZ2FtbWEgdHJpbSB0cmltbiB0cnVuYyB0cnVuY292ZXIgdHlwZSB1bmZvcm1hdHRlZCB1bmlmb3JtIHVuaW9uIHVudGlsIHVwY2FzZSB1cGRhdGUgdXNlciB1c2VyaWNvbiB1c3MgdmFsaWRhdGUgdmFsdWUgdmFyICB3ZWlnaHQgd2hlbiB3aGVyZSB3aGlsZSB3aW5jaGFyc2V0IHdpbmRvdyB3b3JrIHdvcmtpbml0IHdvcmt0ZXJtIHdyaXRlIHdzdW0geHN5bmMgeHdhaXQgeWVhcmN1dG9mZiB5ZXMgeXlxICBtaW4gbWF4JywgWydpbkRhdGFTdGVwJywgJ2luUHJvYyddKTtcbmRlZmluZSgnb3BlcmF0b3InLCAnYW5kIG5vdCAnLCBbJ2luRGF0YVN0ZXAnLCAnaW5Qcm9jJ10pO1xuXG4vLyBNYWluIGZ1bmN0aW9uXG5mdW5jdGlvbiB0b2tlbml6ZShzdHJlYW0sIHN0YXRlKSB7XG4gIC8vIEZpbmFsbHkgYWR2YW5jZSB0aGUgc3RyZWFtXG4gIHZhciBjaCA9IHN0cmVhbS5uZXh0KCk7XG5cbiAgLy8gQkxPQ0tDT01NRU5UXG4gIGlmIChjaCA9PT0gJy8nICYmIHN0cmVhbS5lYXQoJyonKSkge1xuICAgIHN0YXRlLmNvbnRpbnVlQ29tbWVudCA9IHRydWU7XG4gICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICB9IGVsc2UgaWYgKHN0YXRlLmNvbnRpbnVlQ29tbWVudCA9PT0gdHJ1ZSkge1xuICAgIC8vIGluIGNvbW1lbnQgYmxvY2tcbiAgICAvL2NvbW1lbnQgZW5kcyBhdCB0aGUgYmVnaW5uaW5nIG9mIHRoZSBsaW5lXG4gICAgaWYgKGNoID09PSAnKicgJiYgc3RyZWFtLnBlZWsoKSA9PT0gJy8nKSB7XG4gICAgICBzdHJlYW0ubmV4dCgpO1xuICAgICAgc3RhdGUuY29udGludWVDb21tZW50ID0gZmFsc2U7XG4gICAgfSBlbHNlIGlmIChzdHJlYW0uc2tpcFRvKCcqJykpIHtcbiAgICAgIC8vY29tbWVudCBpcyBwb3RlbnRpYWxseSBsYXRlciBpbiBsaW5lXG4gICAgICBzdHJlYW0uc2tpcFRvKCcqJyk7XG4gICAgICBzdHJlYW0ubmV4dCgpO1xuICAgICAgaWYgKHN0cmVhbS5lYXQoJy8nKSkgc3RhdGUuY29udGludWVDb21tZW50ID0gZmFsc2U7XG4gICAgfSBlbHNlIHtcbiAgICAgIHN0cmVhbS5za2lwVG9FbmQoKTtcbiAgICB9XG4gICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICB9XG4gIGlmIChjaCA9PSBcIipcIiAmJiBzdHJlYW0uY29sdW1uKCkgPT0gc3RyZWFtLmluZGVudGF0aW9uKCkpIHtcbiAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICB9XG5cbiAgLy8gRG91YmxlT3BlcmF0b3IgbWF0Y2hcbiAgdmFyIGRvdWJsZU9wZXJhdG9yID0gY2ggKyBzdHJlYW0ucGVlaygpO1xuICBpZiAoKGNoID09PSAnXCInIHx8IGNoID09PSBcIidcIikgJiYgIXN0YXRlLmNvbnRpbnVlU3RyaW5nKSB7XG4gICAgc3RhdGUuY29udGludWVTdHJpbmcgPSBjaDtcbiAgICByZXR1cm4gXCJzdHJpbmdcIjtcbiAgfSBlbHNlIGlmIChzdGF0ZS5jb250aW51ZVN0cmluZykge1xuICAgIGlmIChzdGF0ZS5jb250aW51ZVN0cmluZyA9PSBjaCkge1xuICAgICAgc3RhdGUuY29udGludWVTdHJpbmcgPSBudWxsO1xuICAgIH0gZWxzZSBpZiAoc3RyZWFtLnNraXBUbyhzdGF0ZS5jb250aW51ZVN0cmluZykpIHtcbiAgICAgIC8vIHF1b3RlIGZvdW5kIG9uIHRoaXMgbGluZVxuICAgICAgc3RyZWFtLm5leHQoKTtcbiAgICAgIHN0YXRlLmNvbnRpbnVlU3RyaW5nID0gbnVsbDtcbiAgICB9IGVsc2Uge1xuICAgICAgc3RyZWFtLnNraXBUb0VuZCgpO1xuICAgIH1cbiAgICByZXR1cm4gXCJzdHJpbmdcIjtcbiAgfSBlbHNlIGlmIChzdGF0ZS5jb250aW51ZVN0cmluZyAhPT0gbnVsbCAmJiBzdHJlYW0uZW9sKCkpIHtcbiAgICBzdHJlYW0uc2tpcFRvKHN0YXRlLmNvbnRpbnVlU3RyaW5nKSB8fCBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgcmV0dXJuIFwic3RyaW5nXCI7XG4gIH0gZWxzZSBpZiAoL1tcXGRcXC5dLy50ZXN0KGNoKSkge1xuICAgIC8vZmluZCBudW1iZXJzXG4gICAgaWYgKGNoID09PSBcIi5cIikgc3RyZWFtLm1hdGNoKC9eWzAtOV0rKFtlRV1bXFwtK10/WzAtOV0rKT8vKTtlbHNlIGlmIChjaCA9PT0gXCIwXCIpIHN0cmVhbS5tYXRjaCgvXlt4WF1bMC05YS1mQS1GXSsvKSB8fCBzdHJlYW0ubWF0Y2goL14wWzAtN10rLyk7ZWxzZSBzdHJlYW0ubWF0Y2goL15bMC05XSpcXC4/WzAtOV0qKFtlRV1bXFwtK10/WzAtOV0rKT8vKTtcbiAgICByZXR1cm4gXCJudW1iZXJcIjtcbiAgfSBlbHNlIGlmIChpc0RvdWJsZU9wZXJhdG9yQ2hhci50ZXN0KGNoICsgc3RyZWFtLnBlZWsoKSkpIHtcbiAgICAvLyBUV08gU1lNQk9MIFRPS0VOU1xuICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgcmV0dXJuIFwib3BlcmF0b3JcIjtcbiAgfSBlbHNlIGlmIChpc0RvdWJsZU9wZXJhdG9yU3ltLmhhc093blByb3BlcnR5KGRvdWJsZU9wZXJhdG9yKSkge1xuICAgIHN0cmVhbS5uZXh0KCk7XG4gICAgaWYgKHN0cmVhbS5wZWVrKCkgPT09ICcgJykgcmV0dXJuIGlzRG91YmxlT3BlcmF0b3JTeW1bZG91YmxlT3BlcmF0b3IudG9Mb3dlckNhc2UoKV07XG4gIH0gZWxzZSBpZiAoaXNTaW5nbGVPcGVyYXRvckNoYXIudGVzdChjaCkpIHtcbiAgICAvLyBTSU5HTEUgU1lNQk9MIFRPS0VOU1xuICAgIHJldHVybiBcIm9wZXJhdG9yXCI7XG4gIH1cblxuICAvLyBNYXRjaGVzIG9uZSB3aG9sZSB3b3JkIC0tIGV2ZW4gaWYgdGhlIHdvcmQgaXMgYSBjaGFyYWN0ZXJcbiAgdmFyIHdvcmQ7XG4gIGlmIChzdHJlYW0ubWF0Y2goL1slJjtcXHddKy8sIGZhbHNlKSAhPSBudWxsKSB7XG4gICAgd29yZCA9IGNoICsgc3RyZWFtLm1hdGNoKC9bJSY7XFx3XSsvLCB0cnVlKTtcbiAgICBpZiAoLyYvLnRlc3Qod29yZCkpIHJldHVybiAndmFyaWFibGUnO1xuICB9IGVsc2Uge1xuICAgIHdvcmQgPSBjaDtcbiAgfVxuICAvLyB0aGUgd29yZCBhZnRlciBEQVRBIFBST0Mgb3IgTUFDUk9cbiAgaWYgKHN0YXRlLm5leHR3b3JkKSB7XG4gICAgc3RyZWFtLm1hdGNoKC9bXFx3XSsvKTtcbiAgICAvLyBtYXRjaCBtZW1uYW1lLmxpYm5hbWVcbiAgICBpZiAoc3RyZWFtLnBlZWsoKSA9PT0gJy4nKSBzdHJlYW0uc2tpcFRvKCcgJyk7XG4gICAgc3RhdGUubmV4dHdvcmQgPSBmYWxzZTtcbiAgICByZXR1cm4gJ3ZhcmlhYmxlTmFtZS5zcGVjaWFsJztcbiAgfVxuICB3b3JkID0gd29yZC50b0xvd2VyQ2FzZSgpO1xuICAvLyBBcmUgd2UgaW4gYSBEQVRBIFN0ZXA/XG4gIGlmIChzdGF0ZS5pbkRhdGFTdGVwKSB7XG4gICAgaWYgKHdvcmQgPT09ICdydW47JyB8fCBzdHJlYW0ubWF0Y2goL3J1blxcczsvKSkge1xuICAgICAgc3RhdGUuaW5EYXRhU3RlcCA9IGZhbHNlO1xuICAgICAgcmV0dXJuICdidWlsdGluJztcbiAgICB9XG4gICAgLy8gdmFyaWFibGUgZm9ybWF0c1xuICAgIGlmICh3b3JkICYmIHN0cmVhbS5uZXh0KCkgPT09ICcuJykge1xuICAgICAgLy9laXRoZXIgYSBmb3JtYXQgb3IgbGlibmFtZS5tZW1uYW1lXG4gICAgICBpZiAoL1xcdy8udGVzdChzdHJlYW0ucGVlaygpKSkgcmV0dXJuICd2YXJpYWJsZU5hbWUuc3BlY2lhbCc7ZWxzZSByZXR1cm4gJ3ZhcmlhYmxlJztcbiAgICB9XG4gICAgLy8gZG8gd2UgaGF2ZSBhIERBVEEgU3RlcCBrZXl3b3JkXG4gICAgaWYgKHdvcmQgJiYgd29yZHMuaGFzT3duUHJvcGVydHkod29yZCkgJiYgKHdvcmRzW3dvcmRdLnN0YXRlLmluZGV4T2YoXCJpbkRhdGFTdGVwXCIpICE9PSAtMSB8fCB3b3Jkc1t3b3JkXS5zdGF0ZS5pbmRleE9mKFwiQUxMXCIpICE9PSAtMSkpIHtcbiAgICAgIC8vYmFja3VwIHRvIHRoZSBzdGFydCBvZiB0aGUgd29yZFxuICAgICAgaWYgKHN0cmVhbS5zdGFydCA8IHN0cmVhbS5wb3MpIHN0cmVhbS5iYWNrVXAoc3RyZWFtLnBvcyAtIHN0cmVhbS5zdGFydCk7XG4gICAgICAvL2FkdmFuY2UgdGhlIGxlbmd0aCBvZiB0aGUgd29yZCBhbmQgcmV0dXJuXG4gICAgICBmb3IgKHZhciBpID0gMDsgaSA8IHdvcmQubGVuZ3RoOyArK2kpIHN0cmVhbS5uZXh0KCk7XG4gICAgICByZXR1cm4gd29yZHNbd29yZF0uc3R5bGU7XG4gICAgfVxuICB9XG4gIC8vIEFyZSB3ZSBpbiBhbiBQcm9jIHN0YXRlbWVudD9cbiAgaWYgKHN0YXRlLmluUHJvYykge1xuICAgIGlmICh3b3JkID09PSAncnVuOycgfHwgd29yZCA9PT0gJ3F1aXQ7Jykge1xuICAgICAgc3RhdGUuaW5Qcm9jID0gZmFsc2U7XG4gICAgICByZXR1cm4gJ2J1aWx0aW4nO1xuICAgIH1cbiAgICAvLyBkbyB3ZSBoYXZlIGEgcHJvYyBrZXl3b3JkXG4gICAgaWYgKHdvcmQgJiYgd29yZHMuaGFzT3duUHJvcGVydHkod29yZCkgJiYgKHdvcmRzW3dvcmRdLnN0YXRlLmluZGV4T2YoXCJpblByb2NcIikgIT09IC0xIHx8IHdvcmRzW3dvcmRdLnN0YXRlLmluZGV4T2YoXCJBTExcIikgIT09IC0xKSkge1xuICAgICAgc3RyZWFtLm1hdGNoKC9bXFx3XSsvKTtcbiAgICAgIHJldHVybiB3b3Jkc1t3b3JkXS5zdHlsZTtcbiAgICB9XG4gIH1cbiAgLy8gQXJlIHdlIGluIGEgTWFjcm8gc3RhdGVtZW50P1xuICBpZiAoc3RhdGUuaW5NYWNybykge1xuICAgIGlmICh3b3JkID09PSAnJW1lbmQnKSB7XG4gICAgICBpZiAoc3RyZWFtLnBlZWsoKSA9PT0gJzsnKSBzdHJlYW0ubmV4dCgpO1xuICAgICAgc3RhdGUuaW5NYWNybyA9IGZhbHNlO1xuICAgICAgcmV0dXJuICdidWlsdGluJztcbiAgICB9XG4gICAgaWYgKHdvcmQgJiYgd29yZHMuaGFzT3duUHJvcGVydHkod29yZCkgJiYgKHdvcmRzW3dvcmRdLnN0YXRlLmluZGV4T2YoXCJpbk1hY3JvXCIpICE9PSAtMSB8fCB3b3Jkc1t3b3JkXS5zdGF0ZS5pbmRleE9mKFwiQUxMXCIpICE9PSAtMSkpIHtcbiAgICAgIHN0cmVhbS5tYXRjaCgvW1xcd10rLyk7XG4gICAgICByZXR1cm4gd29yZHNbd29yZF0uc3R5bGU7XG4gICAgfVxuICAgIHJldHVybiAnYXRvbSc7XG4gIH1cbiAgLy8gRG8gd2UgaGF2ZSBLZXl3b3JkcyBzcGVjaWZpYyB3b3Jkcz9cbiAgaWYgKHdvcmQgJiYgd29yZHMuaGFzT3duUHJvcGVydHkod29yZCkpIHtcbiAgICAvLyBOZWdhdGVzIHRoZSBpbml0aWFsIG5leHQoKVxuICAgIHN0cmVhbS5iYWNrVXAoMSk7XG4gICAgLy8gQWN0dWFsbHkgbW92ZSB0aGUgc3RyZWFtXG4gICAgc3RyZWFtLm1hdGNoKC9bXFx3XSsvKTtcbiAgICBpZiAod29yZCA9PT0gJ2RhdGEnICYmIC89Ly50ZXN0KHN0cmVhbS5wZWVrKCkpID09PSBmYWxzZSkge1xuICAgICAgc3RhdGUuaW5EYXRhU3RlcCA9IHRydWU7XG4gICAgICBzdGF0ZS5uZXh0d29yZCA9IHRydWU7XG4gICAgICByZXR1cm4gJ2J1aWx0aW4nO1xuICAgIH1cbiAgICBpZiAod29yZCA9PT0gJ3Byb2MnKSB7XG4gICAgICBzdGF0ZS5pblByb2MgPSB0cnVlO1xuICAgICAgc3RhdGUubmV4dHdvcmQgPSB0cnVlO1xuICAgICAgcmV0dXJuICdidWlsdGluJztcbiAgICB9XG4gICAgaWYgKHdvcmQgPT09ICclbWFjcm8nKSB7XG4gICAgICBzdGF0ZS5pbk1hY3JvID0gdHJ1ZTtcbiAgICAgIHN0YXRlLm5leHR3b3JkID0gdHJ1ZTtcbiAgICAgIHJldHVybiAnYnVpbHRpbic7XG4gICAgfVxuICAgIGlmICgvdGl0bGVbMS05XS8udGVzdCh3b3JkKSkgcmV0dXJuICdkZWYnO1xuICAgIGlmICh3b3JkID09PSAnZm9vdG5vdGUnKSB7XG4gICAgICBzdHJlYW0uZWF0KC9bMS05XS8pO1xuICAgICAgcmV0dXJuICdkZWYnO1xuICAgIH1cblxuICAgIC8vIFJldHVybnMgdGhlaXIgdmFsdWUgYXMgc3RhdGUgaW4gdGhlIHByaW9yIGRlZmluZSBtZXRob2RzXG4gICAgaWYgKHN0YXRlLmluRGF0YVN0ZXAgPT09IHRydWUgJiYgd29yZHNbd29yZF0uc3RhdGUuaW5kZXhPZihcImluRGF0YVN0ZXBcIikgIT09IC0xKSByZXR1cm4gd29yZHNbd29yZF0uc3R5bGU7XG4gICAgaWYgKHN0YXRlLmluUHJvYyA9PT0gdHJ1ZSAmJiB3b3Jkc1t3b3JkXS5zdGF0ZS5pbmRleE9mKFwiaW5Qcm9jXCIpICE9PSAtMSkgcmV0dXJuIHdvcmRzW3dvcmRdLnN0eWxlO1xuICAgIGlmIChzdGF0ZS5pbk1hY3JvID09PSB0cnVlICYmIHdvcmRzW3dvcmRdLnN0YXRlLmluZGV4T2YoXCJpbk1hY3JvXCIpICE9PSAtMSkgcmV0dXJuIHdvcmRzW3dvcmRdLnN0eWxlO1xuICAgIGlmICh3b3Jkc1t3b3JkXS5zdGF0ZS5pbmRleE9mKFwiQUxMXCIpICE9PSAtMSkgcmV0dXJuIHdvcmRzW3dvcmRdLnN0eWxlO1xuICAgIHJldHVybiBudWxsO1xuICB9XG4gIC8vIFVucmVjb2duaXplZCBzeW50YXhcbiAgcmV0dXJuIG51bGw7XG59XG5leHBvcnQgY29uc3Qgc2FzID0ge1xuICBuYW1lOiBcInNhc1wiLFxuICBzdGFydFN0YXRlOiBmdW5jdGlvbiAoKSB7XG4gICAgcmV0dXJuIHtcbiAgICAgIGluRGF0YVN0ZXA6IGZhbHNlLFxuICAgICAgaW5Qcm9jOiBmYWxzZSxcbiAgICAgIGluTWFjcm86IGZhbHNlLFxuICAgICAgbmV4dHdvcmQ6IGZhbHNlLFxuICAgICAgY29udGludWVTdHJpbmc6IG51bGwsXG4gICAgICBjb250aW51ZUNvbW1lbnQ6IGZhbHNlXG4gICAgfTtcbiAgfSxcbiAgdG9rZW46IGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgLy8gU3RyaXAgdGhlIHNwYWNlcywgYnV0IHJlZ2V4IHdpbGwgYWNjb3VudCBmb3IgdGhlbSBlaXRoZXIgd2F5XG4gICAgaWYgKHN0cmVhbS5lYXRTcGFjZSgpKSByZXR1cm4gbnVsbDtcbiAgICAvLyBHbyB0aHJvdWdoIHRoZSBtYWluIHByb2Nlc3NcbiAgICByZXR1cm4gdG9rZW5pemUoc3RyZWFtLCBzdGF0ZSk7XG4gIH0sXG4gIGxhbmd1YWdlRGF0YToge1xuICAgIGNvbW1lbnRUb2tlbnM6IHtcbiAgICAgIGJsb2NrOiB7XG4gICAgICAgIG9wZW46IFwiLypcIixcbiAgICAgICAgY2xvc2U6IFwiKi9cIlxuICAgICAgfVxuICAgIH1cbiAgfVxufTsiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=