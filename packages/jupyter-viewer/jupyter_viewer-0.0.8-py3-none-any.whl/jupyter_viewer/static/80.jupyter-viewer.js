"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[80],{

/***/ 80:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "fortran": () => (/* binding */ fortran)
/* harmony export */ });
function words(array) {
  var keys = {};
  for (var i = 0; i < array.length; ++i) {
    keys[array[i]] = true;
  }
  return keys;
}
var keywords = words(["abstract", "accept", "allocatable", "allocate", "array", "assign", "asynchronous", "backspace", "bind", "block", "byte", "call", "case", "class", "close", "common", "contains", "continue", "cycle", "data", "deallocate", "decode", "deferred", "dimension", "do", "elemental", "else", "encode", "end", "endif", "entry", "enumerator", "equivalence", "exit", "external", "extrinsic", "final", "forall", "format", "function", "generic", "go", "goto", "if", "implicit", "import", "include", "inquire", "intent", "interface", "intrinsic", "module", "namelist", "non_intrinsic", "non_overridable", "none", "nopass", "nullify", "open", "optional", "options", "parameter", "pass", "pause", "pointer", "print", "private", "program", "protected", "public", "pure", "read", "recursive", "result", "return", "rewind", "save", "select", "sequence", "stop", "subroutine", "target", "then", "to", "type", "use", "value", "volatile", "where", "while", "write"]);
var builtins = words(["abort", "abs", "access", "achar", "acos", "adjustl", "adjustr", "aimag", "aint", "alarm", "all", "allocated", "alog", "amax", "amin", "amod", "and", "anint", "any", "asin", "associated", "atan", "besj", "besjn", "besy", "besyn", "bit_size", "btest", "cabs", "ccos", "ceiling", "cexp", "char", "chdir", "chmod", "clog", "cmplx", "command_argument_count", "complex", "conjg", "cos", "cosh", "count", "cpu_time", "cshift", "csin", "csqrt", "ctime", "c_funloc", "c_loc", "c_associated", "c_null_ptr", "c_null_funptr", "c_f_pointer", "c_null_char", "c_alert", "c_backspace", "c_form_feed", "c_new_line", "c_carriage_return", "c_horizontal_tab", "c_vertical_tab", "dabs", "dacos", "dasin", "datan", "date_and_time", "dbesj", "dbesj", "dbesjn", "dbesy", "dbesy", "dbesyn", "dble", "dcos", "dcosh", "ddim", "derf", "derfc", "dexp", "digits", "dim", "dint", "dlog", "dlog", "dmax", "dmin", "dmod", "dnint", "dot_product", "dprod", "dsign", "dsinh", "dsin", "dsqrt", "dtanh", "dtan", "dtime", "eoshift", "epsilon", "erf", "erfc", "etime", "exit", "exp", "exponent", "extends_type_of", "fdate", "fget", "fgetc", "float", "floor", "flush", "fnum", "fputc", "fput", "fraction", "fseek", "fstat", "ftell", "gerror", "getarg", "get_command", "get_command_argument", "get_environment_variable", "getcwd", "getenv", "getgid", "getlog", "getpid", "getuid", "gmtime", "hostnm", "huge", "iabs", "iachar", "iand", "iargc", "ibclr", "ibits", "ibset", "ichar", "idate", "idim", "idint", "idnint", "ieor", "ierrno", "ifix", "imag", "imagpart", "index", "int", "ior", "irand", "isatty", "ishft", "ishftc", "isign", "iso_c_binding", "is_iostat_end", "is_iostat_eor", "itime", "kill", "kind", "lbound", "len", "len_trim", "lge", "lgt", "link", "lle", "llt", "lnblnk", "loc", "log", "logical", "long", "lshift", "lstat", "ltime", "matmul", "max", "maxexponent", "maxloc", "maxval", "mclock", "merge", "move_alloc", "min", "minexponent", "minloc", "minval", "mod", "modulo", "mvbits", "nearest", "new_line", "nint", "not", "or", "pack", "perror", "precision", "present", "product", "radix", "rand", "random_number", "random_seed", "range", "real", "realpart", "rename", "repeat", "reshape", "rrspacing", "rshift", "same_type_as", "scale", "scan", "second", "selected_int_kind", "selected_real_kind", "set_exponent", "shape", "short", "sign", "signal", "sinh", "sin", "sleep", "sngl", "spacing", "spread", "sqrt", "srand", "stat", "sum", "symlnk", "system", "system_clock", "tan", "tanh", "time", "tiny", "transfer", "transpose", "trim", "ttynam", "ubound", "umask", "unlink", "unpack", "verify", "xor", "zabs", "zcos", "zexp", "zlog", "zsin", "zsqrt"]);
var dataTypes = words(["c_bool", "c_char", "c_double", "c_double_complex", "c_float", "c_float_complex", "c_funptr", "c_int", "c_int16_t", "c_int32_t", "c_int64_t", "c_int8_t", "c_int_fast16_t", "c_int_fast32_t", "c_int_fast64_t", "c_int_fast8_t", "c_int_least16_t", "c_int_least32_t", "c_int_least64_t", "c_int_least8_t", "c_intmax_t", "c_intptr_t", "c_long", "c_long_double", "c_long_double_complex", "c_long_long", "c_ptr", "c_short", "c_signed_char", "c_size_t", "character", "complex", "double", "integer", "logical", "real"]);
var isOperatorChar = /[+\-*&=<>\/\:]/;
var litOperator = /^\.(and|or|eq|lt|le|gt|ge|ne|not|eqv|neqv)\./i;
function tokenBase(stream, state) {
  if (stream.match(litOperator)) {
    return 'operator';
  }
  var ch = stream.next();
  if (ch == "!") {
    stream.skipToEnd();
    return "comment";
  }
  if (ch == '"' || ch == "'") {
    state.tokenize = tokenString(ch);
    return state.tokenize(stream, state);
  }
  if (/[\[\]\(\),]/.test(ch)) {
    return null;
  }
  if (/\d/.test(ch)) {
    stream.eatWhile(/[\w\.]/);
    return "number";
  }
  if (isOperatorChar.test(ch)) {
    stream.eatWhile(isOperatorChar);
    return "operator";
  }
  stream.eatWhile(/[\w\$_]/);
  var word = stream.current().toLowerCase();
  if (keywords.hasOwnProperty(word)) {
    return 'keyword';
  }
  if (builtins.hasOwnProperty(word) || dataTypes.hasOwnProperty(word)) {
    return 'builtin';
  }
  return "variable";
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
    if (end || !escaped) state.tokenize = null;
    return "string";
  };
}

// Interface

const fortran = {
  name: "fortran",
  startState: function () {
    return {
      tokenize: null
    };
  },
  token: function (stream, state) {
    if (stream.eatSpace()) return null;
    var style = (state.tokenize || tokenBase)(stream, state);
    if (style == "comment" || style == "meta") return style;
    return style;
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiODAuanVweXRlci12aWV3ZXIuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9AY29kZW1pcnJvci9sZWdhY3ktbW9kZXMvbW9kZS9mb3J0cmFuLmpzIl0sInNvdXJjZXNDb250ZW50IjpbImZ1bmN0aW9uIHdvcmRzKGFycmF5KSB7XG4gIHZhciBrZXlzID0ge307XG4gIGZvciAodmFyIGkgPSAwOyBpIDwgYXJyYXkubGVuZ3RoOyArK2kpIHtcbiAgICBrZXlzW2FycmF5W2ldXSA9IHRydWU7XG4gIH1cbiAgcmV0dXJuIGtleXM7XG59XG52YXIga2V5d29yZHMgPSB3b3JkcyhbXCJhYnN0cmFjdFwiLCBcImFjY2VwdFwiLCBcImFsbG9jYXRhYmxlXCIsIFwiYWxsb2NhdGVcIiwgXCJhcnJheVwiLCBcImFzc2lnblwiLCBcImFzeW5jaHJvbm91c1wiLCBcImJhY2tzcGFjZVwiLCBcImJpbmRcIiwgXCJibG9ja1wiLCBcImJ5dGVcIiwgXCJjYWxsXCIsIFwiY2FzZVwiLCBcImNsYXNzXCIsIFwiY2xvc2VcIiwgXCJjb21tb25cIiwgXCJjb250YWluc1wiLCBcImNvbnRpbnVlXCIsIFwiY3ljbGVcIiwgXCJkYXRhXCIsIFwiZGVhbGxvY2F0ZVwiLCBcImRlY29kZVwiLCBcImRlZmVycmVkXCIsIFwiZGltZW5zaW9uXCIsIFwiZG9cIiwgXCJlbGVtZW50YWxcIiwgXCJlbHNlXCIsIFwiZW5jb2RlXCIsIFwiZW5kXCIsIFwiZW5kaWZcIiwgXCJlbnRyeVwiLCBcImVudW1lcmF0b3JcIiwgXCJlcXVpdmFsZW5jZVwiLCBcImV4aXRcIiwgXCJleHRlcm5hbFwiLCBcImV4dHJpbnNpY1wiLCBcImZpbmFsXCIsIFwiZm9yYWxsXCIsIFwiZm9ybWF0XCIsIFwiZnVuY3Rpb25cIiwgXCJnZW5lcmljXCIsIFwiZ29cIiwgXCJnb3RvXCIsIFwiaWZcIiwgXCJpbXBsaWNpdFwiLCBcImltcG9ydFwiLCBcImluY2x1ZGVcIiwgXCJpbnF1aXJlXCIsIFwiaW50ZW50XCIsIFwiaW50ZXJmYWNlXCIsIFwiaW50cmluc2ljXCIsIFwibW9kdWxlXCIsIFwibmFtZWxpc3RcIiwgXCJub25faW50cmluc2ljXCIsIFwibm9uX292ZXJyaWRhYmxlXCIsIFwibm9uZVwiLCBcIm5vcGFzc1wiLCBcIm51bGxpZnlcIiwgXCJvcGVuXCIsIFwib3B0aW9uYWxcIiwgXCJvcHRpb25zXCIsIFwicGFyYW1ldGVyXCIsIFwicGFzc1wiLCBcInBhdXNlXCIsIFwicG9pbnRlclwiLCBcInByaW50XCIsIFwicHJpdmF0ZVwiLCBcInByb2dyYW1cIiwgXCJwcm90ZWN0ZWRcIiwgXCJwdWJsaWNcIiwgXCJwdXJlXCIsIFwicmVhZFwiLCBcInJlY3Vyc2l2ZVwiLCBcInJlc3VsdFwiLCBcInJldHVyblwiLCBcInJld2luZFwiLCBcInNhdmVcIiwgXCJzZWxlY3RcIiwgXCJzZXF1ZW5jZVwiLCBcInN0b3BcIiwgXCJzdWJyb3V0aW5lXCIsIFwidGFyZ2V0XCIsIFwidGhlblwiLCBcInRvXCIsIFwidHlwZVwiLCBcInVzZVwiLCBcInZhbHVlXCIsIFwidm9sYXRpbGVcIiwgXCJ3aGVyZVwiLCBcIndoaWxlXCIsIFwid3JpdGVcIl0pO1xudmFyIGJ1aWx0aW5zID0gd29yZHMoW1wiYWJvcnRcIiwgXCJhYnNcIiwgXCJhY2Nlc3NcIiwgXCJhY2hhclwiLCBcImFjb3NcIiwgXCJhZGp1c3RsXCIsIFwiYWRqdXN0clwiLCBcImFpbWFnXCIsIFwiYWludFwiLCBcImFsYXJtXCIsIFwiYWxsXCIsIFwiYWxsb2NhdGVkXCIsIFwiYWxvZ1wiLCBcImFtYXhcIiwgXCJhbWluXCIsIFwiYW1vZFwiLCBcImFuZFwiLCBcImFuaW50XCIsIFwiYW55XCIsIFwiYXNpblwiLCBcImFzc29jaWF0ZWRcIiwgXCJhdGFuXCIsIFwiYmVzalwiLCBcImJlc2puXCIsIFwiYmVzeVwiLCBcImJlc3luXCIsIFwiYml0X3NpemVcIiwgXCJidGVzdFwiLCBcImNhYnNcIiwgXCJjY29zXCIsIFwiY2VpbGluZ1wiLCBcImNleHBcIiwgXCJjaGFyXCIsIFwiY2hkaXJcIiwgXCJjaG1vZFwiLCBcImNsb2dcIiwgXCJjbXBseFwiLCBcImNvbW1hbmRfYXJndW1lbnRfY291bnRcIiwgXCJjb21wbGV4XCIsIFwiY29uamdcIiwgXCJjb3NcIiwgXCJjb3NoXCIsIFwiY291bnRcIiwgXCJjcHVfdGltZVwiLCBcImNzaGlmdFwiLCBcImNzaW5cIiwgXCJjc3FydFwiLCBcImN0aW1lXCIsIFwiY19mdW5sb2NcIiwgXCJjX2xvY1wiLCBcImNfYXNzb2NpYXRlZFwiLCBcImNfbnVsbF9wdHJcIiwgXCJjX251bGxfZnVucHRyXCIsIFwiY19mX3BvaW50ZXJcIiwgXCJjX251bGxfY2hhclwiLCBcImNfYWxlcnRcIiwgXCJjX2JhY2tzcGFjZVwiLCBcImNfZm9ybV9mZWVkXCIsIFwiY19uZXdfbGluZVwiLCBcImNfY2FycmlhZ2VfcmV0dXJuXCIsIFwiY19ob3Jpem9udGFsX3RhYlwiLCBcImNfdmVydGljYWxfdGFiXCIsIFwiZGFic1wiLCBcImRhY29zXCIsIFwiZGFzaW5cIiwgXCJkYXRhblwiLCBcImRhdGVfYW5kX3RpbWVcIiwgXCJkYmVzalwiLCBcImRiZXNqXCIsIFwiZGJlc2puXCIsIFwiZGJlc3lcIiwgXCJkYmVzeVwiLCBcImRiZXN5blwiLCBcImRibGVcIiwgXCJkY29zXCIsIFwiZGNvc2hcIiwgXCJkZGltXCIsIFwiZGVyZlwiLCBcImRlcmZjXCIsIFwiZGV4cFwiLCBcImRpZ2l0c1wiLCBcImRpbVwiLCBcImRpbnRcIiwgXCJkbG9nXCIsIFwiZGxvZ1wiLCBcImRtYXhcIiwgXCJkbWluXCIsIFwiZG1vZFwiLCBcImRuaW50XCIsIFwiZG90X3Byb2R1Y3RcIiwgXCJkcHJvZFwiLCBcImRzaWduXCIsIFwiZHNpbmhcIiwgXCJkc2luXCIsIFwiZHNxcnRcIiwgXCJkdGFuaFwiLCBcImR0YW5cIiwgXCJkdGltZVwiLCBcImVvc2hpZnRcIiwgXCJlcHNpbG9uXCIsIFwiZXJmXCIsIFwiZXJmY1wiLCBcImV0aW1lXCIsIFwiZXhpdFwiLCBcImV4cFwiLCBcImV4cG9uZW50XCIsIFwiZXh0ZW5kc190eXBlX29mXCIsIFwiZmRhdGVcIiwgXCJmZ2V0XCIsIFwiZmdldGNcIiwgXCJmbG9hdFwiLCBcImZsb29yXCIsIFwiZmx1c2hcIiwgXCJmbnVtXCIsIFwiZnB1dGNcIiwgXCJmcHV0XCIsIFwiZnJhY3Rpb25cIiwgXCJmc2Vla1wiLCBcImZzdGF0XCIsIFwiZnRlbGxcIiwgXCJnZXJyb3JcIiwgXCJnZXRhcmdcIiwgXCJnZXRfY29tbWFuZFwiLCBcImdldF9jb21tYW5kX2FyZ3VtZW50XCIsIFwiZ2V0X2Vudmlyb25tZW50X3ZhcmlhYmxlXCIsIFwiZ2V0Y3dkXCIsIFwiZ2V0ZW52XCIsIFwiZ2V0Z2lkXCIsIFwiZ2V0bG9nXCIsIFwiZ2V0cGlkXCIsIFwiZ2V0dWlkXCIsIFwiZ210aW1lXCIsIFwiaG9zdG5tXCIsIFwiaHVnZVwiLCBcImlhYnNcIiwgXCJpYWNoYXJcIiwgXCJpYW5kXCIsIFwiaWFyZ2NcIiwgXCJpYmNsclwiLCBcImliaXRzXCIsIFwiaWJzZXRcIiwgXCJpY2hhclwiLCBcImlkYXRlXCIsIFwiaWRpbVwiLCBcImlkaW50XCIsIFwiaWRuaW50XCIsIFwiaWVvclwiLCBcImllcnJub1wiLCBcImlmaXhcIiwgXCJpbWFnXCIsIFwiaW1hZ3BhcnRcIiwgXCJpbmRleFwiLCBcImludFwiLCBcImlvclwiLCBcImlyYW5kXCIsIFwiaXNhdHR5XCIsIFwiaXNoZnRcIiwgXCJpc2hmdGNcIiwgXCJpc2lnblwiLCBcImlzb19jX2JpbmRpbmdcIiwgXCJpc19pb3N0YXRfZW5kXCIsIFwiaXNfaW9zdGF0X2VvclwiLCBcIml0aW1lXCIsIFwia2lsbFwiLCBcImtpbmRcIiwgXCJsYm91bmRcIiwgXCJsZW5cIiwgXCJsZW5fdHJpbVwiLCBcImxnZVwiLCBcImxndFwiLCBcImxpbmtcIiwgXCJsbGVcIiwgXCJsbHRcIiwgXCJsbmJsbmtcIiwgXCJsb2NcIiwgXCJsb2dcIiwgXCJsb2dpY2FsXCIsIFwibG9uZ1wiLCBcImxzaGlmdFwiLCBcImxzdGF0XCIsIFwibHRpbWVcIiwgXCJtYXRtdWxcIiwgXCJtYXhcIiwgXCJtYXhleHBvbmVudFwiLCBcIm1heGxvY1wiLCBcIm1heHZhbFwiLCBcIm1jbG9ja1wiLCBcIm1lcmdlXCIsIFwibW92ZV9hbGxvY1wiLCBcIm1pblwiLCBcIm1pbmV4cG9uZW50XCIsIFwibWlubG9jXCIsIFwibWludmFsXCIsIFwibW9kXCIsIFwibW9kdWxvXCIsIFwibXZiaXRzXCIsIFwibmVhcmVzdFwiLCBcIm5ld19saW5lXCIsIFwibmludFwiLCBcIm5vdFwiLCBcIm9yXCIsIFwicGFja1wiLCBcInBlcnJvclwiLCBcInByZWNpc2lvblwiLCBcInByZXNlbnRcIiwgXCJwcm9kdWN0XCIsIFwicmFkaXhcIiwgXCJyYW5kXCIsIFwicmFuZG9tX251bWJlclwiLCBcInJhbmRvbV9zZWVkXCIsIFwicmFuZ2VcIiwgXCJyZWFsXCIsIFwicmVhbHBhcnRcIiwgXCJyZW5hbWVcIiwgXCJyZXBlYXRcIiwgXCJyZXNoYXBlXCIsIFwicnJzcGFjaW5nXCIsIFwicnNoaWZ0XCIsIFwic2FtZV90eXBlX2FzXCIsIFwic2NhbGVcIiwgXCJzY2FuXCIsIFwic2Vjb25kXCIsIFwic2VsZWN0ZWRfaW50X2tpbmRcIiwgXCJzZWxlY3RlZF9yZWFsX2tpbmRcIiwgXCJzZXRfZXhwb25lbnRcIiwgXCJzaGFwZVwiLCBcInNob3J0XCIsIFwic2lnblwiLCBcInNpZ25hbFwiLCBcInNpbmhcIiwgXCJzaW5cIiwgXCJzbGVlcFwiLCBcInNuZ2xcIiwgXCJzcGFjaW5nXCIsIFwic3ByZWFkXCIsIFwic3FydFwiLCBcInNyYW5kXCIsIFwic3RhdFwiLCBcInN1bVwiLCBcInN5bWxua1wiLCBcInN5c3RlbVwiLCBcInN5c3RlbV9jbG9ja1wiLCBcInRhblwiLCBcInRhbmhcIiwgXCJ0aW1lXCIsIFwidGlueVwiLCBcInRyYW5zZmVyXCIsIFwidHJhbnNwb3NlXCIsIFwidHJpbVwiLCBcInR0eW5hbVwiLCBcInVib3VuZFwiLCBcInVtYXNrXCIsIFwidW5saW5rXCIsIFwidW5wYWNrXCIsIFwidmVyaWZ5XCIsIFwieG9yXCIsIFwiemFic1wiLCBcInpjb3NcIiwgXCJ6ZXhwXCIsIFwiemxvZ1wiLCBcInpzaW5cIiwgXCJ6c3FydFwiXSk7XG52YXIgZGF0YVR5cGVzID0gd29yZHMoW1wiY19ib29sXCIsIFwiY19jaGFyXCIsIFwiY19kb3VibGVcIiwgXCJjX2RvdWJsZV9jb21wbGV4XCIsIFwiY19mbG9hdFwiLCBcImNfZmxvYXRfY29tcGxleFwiLCBcImNfZnVucHRyXCIsIFwiY19pbnRcIiwgXCJjX2ludDE2X3RcIiwgXCJjX2ludDMyX3RcIiwgXCJjX2ludDY0X3RcIiwgXCJjX2ludDhfdFwiLCBcImNfaW50X2Zhc3QxNl90XCIsIFwiY19pbnRfZmFzdDMyX3RcIiwgXCJjX2ludF9mYXN0NjRfdFwiLCBcImNfaW50X2Zhc3Q4X3RcIiwgXCJjX2ludF9sZWFzdDE2X3RcIiwgXCJjX2ludF9sZWFzdDMyX3RcIiwgXCJjX2ludF9sZWFzdDY0X3RcIiwgXCJjX2ludF9sZWFzdDhfdFwiLCBcImNfaW50bWF4X3RcIiwgXCJjX2ludHB0cl90XCIsIFwiY19sb25nXCIsIFwiY19sb25nX2RvdWJsZVwiLCBcImNfbG9uZ19kb3VibGVfY29tcGxleFwiLCBcImNfbG9uZ19sb25nXCIsIFwiY19wdHJcIiwgXCJjX3Nob3J0XCIsIFwiY19zaWduZWRfY2hhclwiLCBcImNfc2l6ZV90XCIsIFwiY2hhcmFjdGVyXCIsIFwiY29tcGxleFwiLCBcImRvdWJsZVwiLCBcImludGVnZXJcIiwgXCJsb2dpY2FsXCIsIFwicmVhbFwiXSk7XG52YXIgaXNPcGVyYXRvckNoYXIgPSAvWytcXC0qJj08PlxcL1xcOl0vO1xudmFyIGxpdE9wZXJhdG9yID0gL15cXC4oYW5kfG9yfGVxfGx0fGxlfGd0fGdlfG5lfG5vdHxlcXZ8bmVxdilcXC4vaTtcbmZ1bmN0aW9uIHRva2VuQmFzZShzdHJlYW0sIHN0YXRlKSB7XG4gIGlmIChzdHJlYW0ubWF0Y2gobGl0T3BlcmF0b3IpKSB7XG4gICAgcmV0dXJuICdvcGVyYXRvcic7XG4gIH1cbiAgdmFyIGNoID0gc3RyZWFtLm5leHQoKTtcbiAgaWYgKGNoID09IFwiIVwiKSB7XG4gICAgc3RyZWFtLnNraXBUb0VuZCgpO1xuICAgIHJldHVybiBcImNvbW1lbnRcIjtcbiAgfVxuICBpZiAoY2ggPT0gJ1wiJyB8fCBjaCA9PSBcIidcIikge1xuICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5TdHJpbmcoY2gpO1xuICAgIHJldHVybiBzdGF0ZS50b2tlbml6ZShzdHJlYW0sIHN0YXRlKTtcbiAgfVxuICBpZiAoL1tcXFtcXF1cXChcXCksXS8udGVzdChjaCkpIHtcbiAgICByZXR1cm4gbnVsbDtcbiAgfVxuICBpZiAoL1xcZC8udGVzdChjaCkpIHtcbiAgICBzdHJlYW0uZWF0V2hpbGUoL1tcXHdcXC5dLyk7XG4gICAgcmV0dXJuIFwibnVtYmVyXCI7XG4gIH1cbiAgaWYgKGlzT3BlcmF0b3JDaGFyLnRlc3QoY2gpKSB7XG4gICAgc3RyZWFtLmVhdFdoaWxlKGlzT3BlcmF0b3JDaGFyKTtcbiAgICByZXR1cm4gXCJvcGVyYXRvclwiO1xuICB9XG4gIHN0cmVhbS5lYXRXaGlsZSgvW1xcd1xcJF9dLyk7XG4gIHZhciB3b3JkID0gc3RyZWFtLmN1cnJlbnQoKS50b0xvd2VyQ2FzZSgpO1xuICBpZiAoa2V5d29yZHMuaGFzT3duUHJvcGVydHkod29yZCkpIHtcbiAgICByZXR1cm4gJ2tleXdvcmQnO1xuICB9XG4gIGlmIChidWlsdGlucy5oYXNPd25Qcm9wZXJ0eSh3b3JkKSB8fCBkYXRhVHlwZXMuaGFzT3duUHJvcGVydHkod29yZCkpIHtcbiAgICByZXR1cm4gJ2J1aWx0aW4nO1xuICB9XG4gIHJldHVybiBcInZhcmlhYmxlXCI7XG59XG5mdW5jdGlvbiB0b2tlblN0cmluZyhxdW90ZSkge1xuICByZXR1cm4gZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICB2YXIgZXNjYXBlZCA9IGZhbHNlLFxuICAgICAgbmV4dCxcbiAgICAgIGVuZCA9IGZhbHNlO1xuICAgIHdoaWxlICgobmV4dCA9IHN0cmVhbS5uZXh0KCkpICE9IG51bGwpIHtcbiAgICAgIGlmIChuZXh0ID09IHF1b3RlICYmICFlc2NhcGVkKSB7XG4gICAgICAgIGVuZCA9IHRydWU7XG4gICAgICAgIGJyZWFrO1xuICAgICAgfVxuICAgICAgZXNjYXBlZCA9ICFlc2NhcGVkICYmIG5leHQgPT0gXCJcXFxcXCI7XG4gICAgfVxuICAgIGlmIChlbmQgfHwgIWVzY2FwZWQpIHN0YXRlLnRva2VuaXplID0gbnVsbDtcbiAgICByZXR1cm4gXCJzdHJpbmdcIjtcbiAgfTtcbn1cblxuLy8gSW50ZXJmYWNlXG5cbmV4cG9ydCBjb25zdCBmb3J0cmFuID0ge1xuICBuYW1lOiBcImZvcnRyYW5cIixcbiAgc3RhcnRTdGF0ZTogZnVuY3Rpb24gKCkge1xuICAgIHJldHVybiB7XG4gICAgICB0b2tlbml6ZTogbnVsbFxuICAgIH07XG4gIH0sXG4gIHRva2VuOiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIGlmIChzdHJlYW0uZWF0U3BhY2UoKSkgcmV0dXJuIG51bGw7XG4gICAgdmFyIHN0eWxlID0gKHN0YXRlLnRva2VuaXplIHx8IHRva2VuQmFzZSkoc3RyZWFtLCBzdGF0ZSk7XG4gICAgaWYgKHN0eWxlID09IFwiY29tbWVudFwiIHx8IHN0eWxlID09IFwibWV0YVwiKSByZXR1cm4gc3R5bGU7XG4gICAgcmV0dXJuIHN0eWxlO1xuICB9XG59OyJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==