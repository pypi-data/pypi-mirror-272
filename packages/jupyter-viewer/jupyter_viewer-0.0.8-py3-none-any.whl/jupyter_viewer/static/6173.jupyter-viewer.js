"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[6173],{

/***/ 86173:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "perl": () => (/* binding */ perl)
/* harmony export */ });
// it's like "peek", but need for look-ahead or look-behind if index < 0
function look(stream, c) {
  return stream.string.charAt(stream.pos + (c || 0));
}

// return a part of prefix of current stream from current position
function prefix(stream, c) {
  if (c) {
    var x = stream.pos - c;
    return stream.string.substr(x >= 0 ? x : 0, c);
  } else {
    return stream.string.substr(0, stream.pos - 1);
  }
}

// return a part of suffix of current stream from current position
function suffix(stream, c) {
  var y = stream.string.length;
  var x = y - stream.pos + 1;
  return stream.string.substr(stream.pos, c && c < y ? c : x);
}

// eating and vomiting a part of stream from current position
function eatSuffix(stream, c) {
  var x = stream.pos + c;
  var y;
  if (x <= 0) stream.pos = 0;else if (x >= (y = stream.string.length - 1)) stream.pos = y;else stream.pos = x;
}

// http://perldoc.perl.org
var PERL = {
  //   null - magic touch
  //   1 - keyword
  //   2 - def
  //   3 - atom
  //   4 - operator
  //   5 - builtin (predefined)
  //   [x,y] - x=1,2,3; y=must be defined if x{...}
  //      PERL operators
  '->': 4,
  '++': 4,
  '--': 4,
  '**': 4,
  //   ! ~ \ and unary + and -
  '=~': 4,
  '!~': 4,
  '*': 4,
  '/': 4,
  '%': 4,
  'x': 4,
  '+': 4,
  '-': 4,
  '.': 4,
  '<<': 4,
  '>>': 4,
  //   named unary operators
  '<': 4,
  '>': 4,
  '<=': 4,
  '>=': 4,
  'lt': 4,
  'gt': 4,
  'le': 4,
  'ge': 4,
  '==': 4,
  '!=': 4,
  '<=>': 4,
  'eq': 4,
  'ne': 4,
  'cmp': 4,
  '~~': 4,
  '&': 4,
  '|': 4,
  '^': 4,
  '&&': 4,
  '||': 4,
  '//': 4,
  '..': 4,
  '...': 4,
  '?': 4,
  ':': 4,
  '=': 4,
  '+=': 4,
  '-=': 4,
  '*=': 4,
  //   etc. ???
  ',': 4,
  '=>': 4,
  '::': 4,
  //   list operators (rightward)
  'not': 4,
  'and': 4,
  'or': 4,
  'xor': 4,
  //      PERL predefined variables (I know, what this is a paranoid idea, but may be needed for people, who learn PERL, and for me as well, ...and may be for you?;)
  'BEGIN': [5, 1],
  'END': [5, 1],
  'PRINT': [5, 1],
  'PRINTF': [5, 1],
  'GETC': [5, 1],
  'READ': [5, 1],
  'READLINE': [5, 1],
  'DESTROY': [5, 1],
  'TIE': [5, 1],
  'TIEHANDLE': [5, 1],
  'UNTIE': [5, 1],
  'STDIN': 5,
  'STDIN_TOP': 5,
  'STDOUT': 5,
  'STDOUT_TOP': 5,
  'STDERR': 5,
  'STDERR_TOP': 5,
  '$ARG': 5,
  '$_': 5,
  '@ARG': 5,
  '@_': 5,
  '$LIST_SEPARATOR': 5,
  '$"': 5,
  '$PROCESS_ID': 5,
  '$PID': 5,
  '$$': 5,
  '$REAL_GROUP_ID': 5,
  '$GID': 5,
  '$(': 5,
  '$EFFECTIVE_GROUP_ID': 5,
  '$EGID': 5,
  '$)': 5,
  '$PROGRAM_NAME': 5,
  '$0': 5,
  '$SUBSCRIPT_SEPARATOR': 5,
  '$SUBSEP': 5,
  '$;': 5,
  '$REAL_USER_ID': 5,
  '$UID': 5,
  '$<': 5,
  '$EFFECTIVE_USER_ID': 5,
  '$EUID': 5,
  '$>': 5,
  '$a': 5,
  '$b': 5,
  '$COMPILING': 5,
  '$^C': 5,
  '$DEBUGGING': 5,
  '$^D': 5,
  '${^ENCODING}': 5,
  '$ENV': 5,
  '%ENV': 5,
  '$SYSTEM_FD_MAX': 5,
  '$^F': 5,
  '@F': 5,
  '${^GLOBAL_PHASE}': 5,
  '$^H': 5,
  '%^H': 5,
  '@INC': 5,
  '%INC': 5,
  '$INPLACE_EDIT': 5,
  '$^I': 5,
  '$^M': 5,
  '$OSNAME': 5,
  '$^O': 5,
  '${^OPEN}': 5,
  '$PERLDB': 5,
  '$^P': 5,
  '$SIG': 5,
  '%SIG': 5,
  '$BASETIME': 5,
  '$^T': 5,
  '${^TAINT}': 5,
  '${^UNICODE}': 5,
  '${^UTF8CACHE}': 5,
  '${^UTF8LOCALE}': 5,
  '$PERL_VERSION': 5,
  '$^V': 5,
  '${^WIN32_SLOPPY_STAT}': 5,
  '$EXECUTABLE_NAME': 5,
  '$^X': 5,
  '$1': 5,
  // - regexp $1, $2...
  '$MATCH': 5,
  '$&': 5,
  '${^MATCH}': 5,
  '$PREMATCH': 5,
  '$`': 5,
  '${^PREMATCH}': 5,
  '$POSTMATCH': 5,
  "$'": 5,
  '${^POSTMATCH}': 5,
  '$LAST_PAREN_MATCH': 5,
  '$+': 5,
  '$LAST_SUBMATCH_RESULT': 5,
  '$^N': 5,
  '@LAST_MATCH_END': 5,
  '@+': 5,
  '%LAST_PAREN_MATCH': 5,
  '%+': 5,
  '@LAST_MATCH_START': 5,
  '@-': 5,
  '%LAST_MATCH_START': 5,
  '%-': 5,
  '$LAST_REGEXP_CODE_RESULT': 5,
  '$^R': 5,
  '${^RE_DEBUG_FLAGS}': 5,
  '${^RE_TRIE_MAXBUF}': 5,
  '$ARGV': 5,
  '@ARGV': 5,
  'ARGV': 5,
  'ARGVOUT': 5,
  '$OUTPUT_FIELD_SEPARATOR': 5,
  '$OFS': 5,
  '$,': 5,
  '$INPUT_LINE_NUMBER': 5,
  '$NR': 5,
  '$.': 5,
  '$INPUT_RECORD_SEPARATOR': 5,
  '$RS': 5,
  '$/': 5,
  '$OUTPUT_RECORD_SEPARATOR': 5,
  '$ORS': 5,
  '$\\': 5,
  '$OUTPUT_AUTOFLUSH': 5,
  '$|': 5,
  '$ACCUMULATOR': 5,
  '$^A': 5,
  '$FORMAT_FORMFEED': 5,
  '$^L': 5,
  '$FORMAT_PAGE_NUMBER': 5,
  '$%': 5,
  '$FORMAT_LINES_LEFT': 5,
  '$-': 5,
  '$FORMAT_LINE_BREAK_CHARACTERS': 5,
  '$:': 5,
  '$FORMAT_LINES_PER_PAGE': 5,
  '$=': 5,
  '$FORMAT_TOP_NAME': 5,
  '$^': 5,
  '$FORMAT_NAME': 5,
  '$~': 5,
  '${^CHILD_ERROR_NATIVE}': 5,
  '$EXTENDED_OS_ERROR': 5,
  '$^E': 5,
  '$EXCEPTIONS_BEING_CAUGHT': 5,
  '$^S': 5,
  '$WARNING': 5,
  '$^W': 5,
  '${^WARNING_BITS}': 5,
  '$OS_ERROR': 5,
  '$ERRNO': 5,
  '$!': 5,
  '%OS_ERROR': 5,
  '%ERRNO': 5,
  '%!': 5,
  '$CHILD_ERROR': 5,
  '$?': 5,
  '$EVAL_ERROR': 5,
  '$@': 5,
  '$OFMT': 5,
  '$#': 5,
  '$*': 5,
  '$ARRAY_BASE': 5,
  '$[': 5,
  '$OLD_PERL_VERSION': 5,
  '$]': 5,
  //      PERL blocks
  'if': [1, 1],
  elsif: [1, 1],
  'else': [1, 1],
  'while': [1, 1],
  unless: [1, 1],
  'for': [1, 1],
  foreach: [1, 1],
  //      PERL functions
  'abs': 1,
  // - absolute value function
  accept: 1,
  // - accept an incoming socket connect
  alarm: 1,
  // - schedule a SIGALRM
  'atan2': 1,
  // - arctangent of Y/X in the range -PI to PI
  bind: 1,
  // - binds an address to a socket
  binmode: 1,
  // - prepare binary files for I/O
  bless: 1,
  // - create an object
  bootstrap: 1,
  //
  'break': 1,
  // - break out of a "given" block
  caller: 1,
  // - get context of the current subroutine call
  chdir: 1,
  // - change your current working directory
  chmod: 1,
  // - changes the permissions on a list of files
  chomp: 1,
  // - remove a trailing record separator from a string
  chop: 1,
  // - remove the last character from a string
  chown: 1,
  // - change the ownership on a list of files
  chr: 1,
  // - get character this number represents
  chroot: 1,
  // - make directory new root for path lookups
  close: 1,
  // - close file (or pipe or socket) handle
  closedir: 1,
  // - close directory handle
  connect: 1,
  // - connect to a remote socket
  'continue': [1, 1],
  // - optional trailing block in a while or foreach
  'cos': 1,
  // - cosine function
  crypt: 1,
  // - one-way passwd-style encryption
  dbmclose: 1,
  // - breaks binding on a tied dbm file
  dbmopen: 1,
  // - create binding on a tied dbm file
  'default': 1,
  //
  defined: 1,
  // - test whether a value, variable, or function is defined
  'delete': 1,
  // - deletes a value from a hash
  die: 1,
  // - raise an exception or bail out
  'do': 1,
  // - turn a BLOCK into a TERM
  dump: 1,
  // - create an immediate core dump
  each: 1,
  // - retrieve the next key/value pair from a hash
  endgrent: 1,
  // - be done using group file
  endhostent: 1,
  // - be done using hosts file
  endnetent: 1,
  // - be done using networks file
  endprotoent: 1,
  // - be done using protocols file
  endpwent: 1,
  // - be done using passwd file
  endservent: 1,
  // - be done using services file
  eof: 1,
  // - test a filehandle for its end
  'eval': 1,
  // - catch exceptions or compile and run code
  'exec': 1,
  // - abandon this program to run another
  exists: 1,
  // - test whether a hash key is present
  exit: 1,
  // - terminate this program
  'exp': 1,
  // - raise I to a power
  fcntl: 1,
  // - file control system call
  fileno: 1,
  // - return file descriptor from filehandle
  flock: 1,
  // - lock an entire file with an advisory lock
  fork: 1,
  // - create a new process just like this one
  format: 1,
  // - declare a picture format with use by the write() function
  formline: 1,
  // - internal function used for formats
  getc: 1,
  // - get the next character from the filehandle
  getgrent: 1,
  // - get next group record
  getgrgid: 1,
  // - get group record given group user ID
  getgrnam: 1,
  // - get group record given group name
  gethostbyaddr: 1,
  // - get host record given its address
  gethostbyname: 1,
  // - get host record given name
  gethostent: 1,
  // - get next hosts record
  getlogin: 1,
  // - return who logged in at this tty
  getnetbyaddr: 1,
  // - get network record given its address
  getnetbyname: 1,
  // - get networks record given name
  getnetent: 1,
  // - get next networks record
  getpeername: 1,
  // - find the other end of a socket connection
  getpgrp: 1,
  // - get process group
  getppid: 1,
  // - get parent process ID
  getpriority: 1,
  // - get current nice value
  getprotobyname: 1,
  // - get protocol record given name
  getprotobynumber: 1,
  // - get protocol record numeric protocol
  getprotoent: 1,
  // - get next protocols record
  getpwent: 1,
  // - get next passwd record
  getpwnam: 1,
  // - get passwd record given user login name
  getpwuid: 1,
  // - get passwd record given user ID
  getservbyname: 1,
  // - get services record given its name
  getservbyport: 1,
  // - get services record given numeric port
  getservent: 1,
  // - get next services record
  getsockname: 1,
  // - retrieve the sockaddr for a given socket
  getsockopt: 1,
  // - get socket options on a given socket
  given: 1,
  //
  glob: 1,
  // - expand filenames using wildcards
  gmtime: 1,
  // - convert UNIX time into record or string using Greenwich time
  'goto': 1,
  // - create spaghetti code
  grep: 1,
  // - locate elements in a list test true against a given criterion
  hex: 1,
  // - convert a string to a hexadecimal number
  'import': 1,
  // - patch a module's namespace into your own
  index: 1,
  // - find a substring within a string
  'int': 1,
  // - get the integer portion of a number
  ioctl: 1,
  // - system-dependent device control system call
  'join': 1,
  // - join a list into a string using a separator
  keys: 1,
  // - retrieve list of indices from a hash
  kill: 1,
  // - send a signal to a process or process group
  last: 1,
  // - exit a block prematurely
  lc: 1,
  // - return lower-case version of a string
  lcfirst: 1,
  // - return a string with just the next letter in lower case
  length: 1,
  // - return the number of bytes in a string
  'link': 1,
  // - create a hard link in the filesystem
  listen: 1,
  // - register your socket as a server
  local: 2,
  // - create a temporary value for a global variable (dynamic scoping)
  localtime: 1,
  // - convert UNIX time into record or string using local time
  lock: 1,
  // - get a thread lock on a variable, subroutine, or method
  'log': 1,
  // - retrieve the natural logarithm for a number
  lstat: 1,
  // - stat a symbolic link
  m: null,
  // - match a string with a regular expression pattern
  map: 1,
  // - apply a change to a list to get back a new list with the changes
  mkdir: 1,
  // - create a directory
  msgctl: 1,
  // - SysV IPC message control operations
  msgget: 1,
  // - get SysV IPC message queue
  msgrcv: 1,
  // - receive a SysV IPC message from a message queue
  msgsnd: 1,
  // - send a SysV IPC message to a message queue
  my: 2,
  // - declare and assign a local variable (lexical scoping)
  'new': 1,
  //
  next: 1,
  // - iterate a block prematurely
  no: 1,
  // - unimport some module symbols or semantics at compile time
  oct: 1,
  // - convert a string to an octal number
  open: 1,
  // - open a file, pipe, or descriptor
  opendir: 1,
  // - open a directory
  ord: 1,
  // - find a character's numeric representation
  our: 2,
  // - declare and assign a package variable (lexical scoping)
  pack: 1,
  // - convert a list into a binary representation
  'package': 1,
  // - declare a separate global namespace
  pipe: 1,
  // - open a pair of connected filehandles
  pop: 1,
  // - remove the last element from an array and return it
  pos: 1,
  // - find or set the offset for the last/next m//g search
  print: 1,
  // - output a list to a filehandle
  printf: 1,
  // - output a formatted list to a filehandle
  prototype: 1,
  // - get the prototype (if any) of a subroutine
  push: 1,
  // - append one or more elements to an array
  q: null,
  // - singly quote a string
  qq: null,
  // - doubly quote a string
  qr: null,
  // - Compile pattern
  quotemeta: null,
  // - quote regular expression magic characters
  qw: null,
  // - quote a list of words
  qx: null,
  // - backquote quote a string
  rand: 1,
  // - retrieve the next pseudorandom number
  read: 1,
  // - fixed-length buffered input from a filehandle
  readdir: 1,
  // - get a directory from a directory handle
  readline: 1,
  // - fetch a record from a file
  readlink: 1,
  // - determine where a symbolic link is pointing
  readpipe: 1,
  // - execute a system command and collect standard output
  recv: 1,
  // - receive a message over a Socket
  redo: 1,
  // - start this loop iteration over again
  ref: 1,
  // - find out the type of thing being referenced
  rename: 1,
  // - change a filename
  require: 1,
  // - load in external functions from a library at runtime
  reset: 1,
  // - clear all variables of a given name
  'return': 1,
  // - get out of a function early
  reverse: 1,
  // - flip a string or a list
  rewinddir: 1,
  // - reset directory handle
  rindex: 1,
  // - right-to-left substring search
  rmdir: 1,
  // - remove a directory
  s: null,
  // - replace a pattern with a string
  say: 1,
  // - print with newline
  scalar: 1,
  // - force a scalar context
  seek: 1,
  // - reposition file pointer for random-access I/O
  seekdir: 1,
  // - reposition directory pointer
  select: 1,
  // - reset default output or do I/O multiplexing
  semctl: 1,
  // - SysV semaphore control operations
  semget: 1,
  // - get set of SysV semaphores
  semop: 1,
  // - SysV semaphore operations
  send: 1,
  // - send a message over a socket
  setgrent: 1,
  // - prepare group file for use
  sethostent: 1,
  // - prepare hosts file for use
  setnetent: 1,
  // - prepare networks file for use
  setpgrp: 1,
  // - set the process group of a process
  setpriority: 1,
  // - set a process's nice value
  setprotoent: 1,
  // - prepare protocols file for use
  setpwent: 1,
  // - prepare passwd file for use
  setservent: 1,
  // - prepare services file for use
  setsockopt: 1,
  // - set some socket options
  shift: 1,
  // - remove the first element of an array, and return it
  shmctl: 1,
  // - SysV shared memory operations
  shmget: 1,
  // - get SysV shared memory segment identifier
  shmread: 1,
  // - read SysV shared memory
  shmwrite: 1,
  // - write SysV shared memory
  shutdown: 1,
  // - close down just half of a socket connection
  'sin': 1,
  // - return the sine of a number
  sleep: 1,
  // - block for some number of seconds
  socket: 1,
  // - create a socket
  socketpair: 1,
  // - create a pair of sockets
  'sort': 1,
  // - sort a list of values
  splice: 1,
  // - add or remove elements anywhere in an array
  'split': 1,
  // - split up a string using a regexp delimiter
  sprintf: 1,
  // - formatted print into a string
  'sqrt': 1,
  // - square root function
  srand: 1,
  // - seed the random number generator
  stat: 1,
  // - get a file's status information
  state: 1,
  // - declare and assign a state variable (persistent lexical scoping)
  study: 1,
  // - optimize input data for repeated searches
  'sub': 1,
  // - declare a subroutine, possibly anonymously
  'substr': 1,
  // - get or alter a portion of a string
  symlink: 1,
  // - create a symbolic link to a file
  syscall: 1,
  // - execute an arbitrary system call
  sysopen: 1,
  // - open a file, pipe, or descriptor
  sysread: 1,
  // - fixed-length unbuffered input from a filehandle
  sysseek: 1,
  // - position I/O pointer on handle used with sysread and syswrite
  system: 1,
  // - run a separate program
  syswrite: 1,
  // - fixed-length unbuffered output to a filehandle
  tell: 1,
  // - get current seekpointer on a filehandle
  telldir: 1,
  // - get current seekpointer on a directory handle
  tie: 1,
  // - bind a variable to an object class
  tied: 1,
  // - get a reference to the object underlying a tied variable
  time: 1,
  // - return number of seconds since 1970
  times: 1,
  // - return elapsed time for self and child processes
  tr: null,
  // - transliterate a string
  truncate: 1,
  // - shorten a file
  uc: 1,
  // - return upper-case version of a string
  ucfirst: 1,
  // - return a string with just the next letter in upper case
  umask: 1,
  // - set file creation mode mask
  undef: 1,
  // - remove a variable or function definition
  unlink: 1,
  // - remove one link to a file
  unpack: 1,
  // - convert binary structure into normal perl variables
  unshift: 1,
  // - prepend more elements to the beginning of a list
  untie: 1,
  // - break a tie binding to a variable
  use: 1,
  // - load in a module at compile time
  utime: 1,
  // - set a file's last access and modify times
  values: 1,
  // - return a list of the values in a hash
  vec: 1,
  // - test or set particular bits in a string
  wait: 1,
  // - wait for any child process to die
  waitpid: 1,
  // - wait for a particular child process to die
  wantarray: 1,
  // - get void vs scalar vs list context of current subroutine call
  warn: 1,
  // - print debugging info
  when: 1,
  //
  write: 1,
  // - print a picture record
  y: null
}; // - transliterate a string

var RXstyle = "string.special";
var RXmodifiers = /[goseximacplud]/; // NOTE: "m", "s", "y" and "tr" need to correct real modifiers for each regexp type

function tokenChain(stream, state, chain, style, tail) {
  // NOTE: chain.length > 2 is not working now (it's for s[...][...]geos;)
  state.chain = null; //                                                          12   3tail
  state.style = null;
  state.tail = null;
  state.tokenize = function (stream, state) {
    var e = false,
      c,
      i = 0;
    while (c = stream.next()) {
      if (c === chain[i] && !e) {
        if (chain[++i] !== undefined) {
          state.chain = chain[i];
          state.style = style;
          state.tail = tail;
        } else if (tail) stream.eatWhile(tail);
        state.tokenize = tokenPerl;
        return style;
      }
      e = !e && c == "\\";
    }
    return style;
  };
  return state.tokenize(stream, state);
}
function tokenSOMETHING(stream, state, string) {
  state.tokenize = function (stream, state) {
    if (stream.string == string) state.tokenize = tokenPerl;
    stream.skipToEnd();
    return "string";
  };
  return state.tokenize(stream, state);
}
function tokenPerl(stream, state) {
  if (stream.eatSpace()) return null;
  if (state.chain) return tokenChain(stream, state, state.chain, state.style, state.tail);
  if (stream.match(/^(\-?((\d[\d_]*)?\.\d+(e[+-]?\d+)?|\d+\.\d*)|0x[\da-fA-F_]+|0b[01_]+|\d[\d_]*(e[+-]?\d+)?)/)) return 'number';
  if (stream.match(/^<<(?=[_a-zA-Z])/)) {
    // NOTE: <<SOMETHING\n...\nSOMETHING\n
    stream.eatWhile(/\w/);
    return tokenSOMETHING(stream, state, stream.current().substr(2));
  }
  if (stream.sol() && stream.match(/^\=item(?!\w)/)) {
    // NOTE: \n=item...\n=cut\n
    return tokenSOMETHING(stream, state, '=cut');
  }
  var ch = stream.next();
  if (ch == '"' || ch == "'") {
    // NOTE: ' or " or <<'SOMETHING'\n...\nSOMETHING\n or <<"SOMETHING"\n...\nSOMETHING\n
    if (prefix(stream, 3) == "<<" + ch) {
      var p = stream.pos;
      stream.eatWhile(/\w/);
      var n = stream.current().substr(1);
      if (n && stream.eat(ch)) return tokenSOMETHING(stream, state, n);
      stream.pos = p;
    }
    return tokenChain(stream, state, [ch], "string");
  }
  if (ch == "q") {
    var c = look(stream, -2);
    if (!(c && /\w/.test(c))) {
      c = look(stream, 0);
      if (c == "x") {
        c = look(stream, 1);
        if (c == "(") {
          eatSuffix(stream, 2);
          return tokenChain(stream, state, [")"], RXstyle, RXmodifiers);
        }
        if (c == "[") {
          eatSuffix(stream, 2);
          return tokenChain(stream, state, ["]"], RXstyle, RXmodifiers);
        }
        if (c == "{") {
          eatSuffix(stream, 2);
          return tokenChain(stream, state, ["}"], RXstyle, RXmodifiers);
        }
        if (c == "<") {
          eatSuffix(stream, 2);
          return tokenChain(stream, state, [">"], RXstyle, RXmodifiers);
        }
        if (/[\^'"!~\/]/.test(c)) {
          eatSuffix(stream, 1);
          return tokenChain(stream, state, [stream.eat(c)], RXstyle, RXmodifiers);
        }
      } else if (c == "q") {
        c = look(stream, 1);
        if (c == "(") {
          eatSuffix(stream, 2);
          return tokenChain(stream, state, [")"], "string");
        }
        if (c == "[") {
          eatSuffix(stream, 2);
          return tokenChain(stream, state, ["]"], "string");
        }
        if (c == "{") {
          eatSuffix(stream, 2);
          return tokenChain(stream, state, ["}"], "string");
        }
        if (c == "<") {
          eatSuffix(stream, 2);
          return tokenChain(stream, state, [">"], "string");
        }
        if (/[\^'"!~\/]/.test(c)) {
          eatSuffix(stream, 1);
          return tokenChain(stream, state, [stream.eat(c)], "string");
        }
      } else if (c == "w") {
        c = look(stream, 1);
        if (c == "(") {
          eatSuffix(stream, 2);
          return tokenChain(stream, state, [")"], "bracket");
        }
        if (c == "[") {
          eatSuffix(stream, 2);
          return tokenChain(stream, state, ["]"], "bracket");
        }
        if (c == "{") {
          eatSuffix(stream, 2);
          return tokenChain(stream, state, ["}"], "bracket");
        }
        if (c == "<") {
          eatSuffix(stream, 2);
          return tokenChain(stream, state, [">"], "bracket");
        }
        if (/[\^'"!~\/]/.test(c)) {
          eatSuffix(stream, 1);
          return tokenChain(stream, state, [stream.eat(c)], "bracket");
        }
      } else if (c == "r") {
        c = look(stream, 1);
        if (c == "(") {
          eatSuffix(stream, 2);
          return tokenChain(stream, state, [")"], RXstyle, RXmodifiers);
        }
        if (c == "[") {
          eatSuffix(stream, 2);
          return tokenChain(stream, state, ["]"], RXstyle, RXmodifiers);
        }
        if (c == "{") {
          eatSuffix(stream, 2);
          return tokenChain(stream, state, ["}"], RXstyle, RXmodifiers);
        }
        if (c == "<") {
          eatSuffix(stream, 2);
          return tokenChain(stream, state, [">"], RXstyle, RXmodifiers);
        }
        if (/[\^'"!~\/]/.test(c)) {
          eatSuffix(stream, 1);
          return tokenChain(stream, state, [stream.eat(c)], RXstyle, RXmodifiers);
        }
      } else if (/[\^'"!~\/(\[{<]/.test(c)) {
        if (c == "(") {
          eatSuffix(stream, 1);
          return tokenChain(stream, state, [")"], "string");
        }
        if (c == "[") {
          eatSuffix(stream, 1);
          return tokenChain(stream, state, ["]"], "string");
        }
        if (c == "{") {
          eatSuffix(stream, 1);
          return tokenChain(stream, state, ["}"], "string");
        }
        if (c == "<") {
          eatSuffix(stream, 1);
          return tokenChain(stream, state, [">"], "string");
        }
        if (/[\^'"!~\/]/.test(c)) {
          return tokenChain(stream, state, [stream.eat(c)], "string");
        }
      }
    }
  }
  if (ch == "m") {
    var c = look(stream, -2);
    if (!(c && /\w/.test(c))) {
      c = stream.eat(/[(\[{<\^'"!~\/]/);
      if (c) {
        if (/[\^'"!~\/]/.test(c)) {
          return tokenChain(stream, state, [c], RXstyle, RXmodifiers);
        }
        if (c == "(") {
          return tokenChain(stream, state, [")"], RXstyle, RXmodifiers);
        }
        if (c == "[") {
          return tokenChain(stream, state, ["]"], RXstyle, RXmodifiers);
        }
        if (c == "{") {
          return tokenChain(stream, state, ["}"], RXstyle, RXmodifiers);
        }
        if (c == "<") {
          return tokenChain(stream, state, [">"], RXstyle, RXmodifiers);
        }
      }
    }
  }
  if (ch == "s") {
    var c = /[\/>\]})\w]/.test(look(stream, -2));
    if (!c) {
      c = stream.eat(/[(\[{<\^'"!~\/]/);
      if (c) {
        if (c == "[") return tokenChain(stream, state, ["]", "]"], RXstyle, RXmodifiers);
        if (c == "{") return tokenChain(stream, state, ["}", "}"], RXstyle, RXmodifiers);
        if (c == "<") return tokenChain(stream, state, [">", ">"], RXstyle, RXmodifiers);
        if (c == "(") return tokenChain(stream, state, [")", ")"], RXstyle, RXmodifiers);
        return tokenChain(stream, state, [c, c], RXstyle, RXmodifiers);
      }
    }
  }
  if (ch == "y") {
    var c = /[\/>\]})\w]/.test(look(stream, -2));
    if (!c) {
      c = stream.eat(/[(\[{<\^'"!~\/]/);
      if (c) {
        if (c == "[") return tokenChain(stream, state, ["]", "]"], RXstyle, RXmodifiers);
        if (c == "{") return tokenChain(stream, state, ["}", "}"], RXstyle, RXmodifiers);
        if (c == "<") return tokenChain(stream, state, [">", ">"], RXstyle, RXmodifiers);
        if (c == "(") return tokenChain(stream, state, [")", ")"], RXstyle, RXmodifiers);
        return tokenChain(stream, state, [c, c], RXstyle, RXmodifiers);
      }
    }
  }
  if (ch == "t") {
    var c = /[\/>\]})\w]/.test(look(stream, -2));
    if (!c) {
      c = stream.eat("r");
      if (c) {
        c = stream.eat(/[(\[{<\^'"!~\/]/);
        if (c) {
          if (c == "[") return tokenChain(stream, state, ["]", "]"], RXstyle, RXmodifiers);
          if (c == "{") return tokenChain(stream, state, ["}", "}"], RXstyle, RXmodifiers);
          if (c == "<") return tokenChain(stream, state, [">", ">"], RXstyle, RXmodifiers);
          if (c == "(") return tokenChain(stream, state, [")", ")"], RXstyle, RXmodifiers);
          return tokenChain(stream, state, [c, c], RXstyle, RXmodifiers);
        }
      }
    }
  }
  if (ch == "`") {
    return tokenChain(stream, state, [ch], "builtin");
  }
  if (ch == "/") {
    if (!/~\s*$/.test(prefix(stream))) return "operator";else return tokenChain(stream, state, [ch], RXstyle, RXmodifiers);
  }
  if (ch == "$") {
    var p = stream.pos;
    if (stream.eatWhile(/\d/) || stream.eat("{") && stream.eatWhile(/\d/) && stream.eat("}")) return "builtin";else stream.pos = p;
  }
  if (/[$@%]/.test(ch)) {
    var p = stream.pos;
    if (stream.eat("^") && stream.eat(/[A-Z]/) || !/[@$%&]/.test(look(stream, -2)) && stream.eat(/[=|\\\-#?@;:&`~\^!\[\]*'"$+.,\/<>()]/)) {
      var c = stream.current();
      if (PERL[c]) return "builtin";
    }
    stream.pos = p;
  }
  if (/[$@%&]/.test(ch)) {
    if (stream.eatWhile(/[\w$]/) || stream.eat("{") && stream.eatWhile(/[\w$]/) && stream.eat("}")) {
      var c = stream.current();
      if (PERL[c]) return "builtin";else return "variable";
    }
  }
  if (ch == "#") {
    if (look(stream, -2) != "$") {
      stream.skipToEnd();
      return "comment";
    }
  }
  if (/[:+\-\^*$&%@=<>!?|\/~\.]/.test(ch)) {
    var p = stream.pos;
    stream.eatWhile(/[:+\-\^*$&%@=<>!?|\/~\.]/);
    if (PERL[stream.current()]) return "operator";else stream.pos = p;
  }
  if (ch == "_") {
    if (stream.pos == 1) {
      if (suffix(stream, 6) == "_END__") {
        return tokenChain(stream, state, ['\0'], "comment");
      } else if (suffix(stream, 7) == "_DATA__") {
        return tokenChain(stream, state, ['\0'], "builtin");
      } else if (suffix(stream, 7) == "_C__") {
        return tokenChain(stream, state, ['\0'], "string");
      }
    }
  }
  if (/\w/.test(ch)) {
    var p = stream.pos;
    if (look(stream, -2) == "{" && (look(stream, 0) == "}" || stream.eatWhile(/\w/) && look(stream, 0) == "}")) return "string";else stream.pos = p;
  }
  if (/[A-Z]/.test(ch)) {
    var l = look(stream, -2);
    var p = stream.pos;
    stream.eatWhile(/[A-Z_]/);
    if (/[\da-z]/.test(look(stream, 0))) {
      stream.pos = p;
    } else {
      var c = PERL[stream.current()];
      if (!c) return "meta";
      if (c[1]) c = c[0];
      if (l != ":") {
        if (c == 1) return "keyword";else if (c == 2) return "def";else if (c == 3) return "atom";else if (c == 4) return "operator";else if (c == 5) return "builtin";else return "meta";
      } else return "meta";
    }
  }
  if (/[a-zA-Z_]/.test(ch)) {
    var l = look(stream, -2);
    stream.eatWhile(/\w/);
    var c = PERL[stream.current()];
    if (!c) return "meta";
    if (c[1]) c = c[0];
    if (l != ":") {
      if (c == 1) return "keyword";else if (c == 2) return "def";else if (c == 3) return "atom";else if (c == 4) return "operator";else if (c == 5) return "builtin";else return "meta";
    } else return "meta";
  }
  return null;
}
const perl = {
  name: "perl",
  startState: function () {
    return {
      tokenize: tokenPerl,
      chain: null,
      style: null,
      tail: null
    };
  },
  token: function (stream, state) {
    return (state.tokenize || tokenPerl)(stream, state);
  },
  languageData: {
    commentTokens: {
      line: "#"
    },
    wordChars: "$"
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNjE3My5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL0Bjb2RlbWlycm9yL2xlZ2FjeS1tb2Rlcy9tb2RlL3BlcmwuanMiXSwic291cmNlc0NvbnRlbnQiOlsiLy8gaXQncyBsaWtlIFwicGVla1wiLCBidXQgbmVlZCBmb3IgbG9vay1haGVhZCBvciBsb29rLWJlaGluZCBpZiBpbmRleCA8IDBcbmZ1bmN0aW9uIGxvb2soc3RyZWFtLCBjKSB7XG4gIHJldHVybiBzdHJlYW0uc3RyaW5nLmNoYXJBdChzdHJlYW0ucG9zICsgKGMgfHwgMCkpO1xufVxuXG4vLyByZXR1cm4gYSBwYXJ0IG9mIHByZWZpeCBvZiBjdXJyZW50IHN0cmVhbSBmcm9tIGN1cnJlbnQgcG9zaXRpb25cbmZ1bmN0aW9uIHByZWZpeChzdHJlYW0sIGMpIHtcbiAgaWYgKGMpIHtcbiAgICB2YXIgeCA9IHN0cmVhbS5wb3MgLSBjO1xuICAgIHJldHVybiBzdHJlYW0uc3RyaW5nLnN1YnN0cih4ID49IDAgPyB4IDogMCwgYyk7XG4gIH0gZWxzZSB7XG4gICAgcmV0dXJuIHN0cmVhbS5zdHJpbmcuc3Vic3RyKDAsIHN0cmVhbS5wb3MgLSAxKTtcbiAgfVxufVxuXG4vLyByZXR1cm4gYSBwYXJ0IG9mIHN1ZmZpeCBvZiBjdXJyZW50IHN0cmVhbSBmcm9tIGN1cnJlbnQgcG9zaXRpb25cbmZ1bmN0aW9uIHN1ZmZpeChzdHJlYW0sIGMpIHtcbiAgdmFyIHkgPSBzdHJlYW0uc3RyaW5nLmxlbmd0aDtcbiAgdmFyIHggPSB5IC0gc3RyZWFtLnBvcyArIDE7XG4gIHJldHVybiBzdHJlYW0uc3RyaW5nLnN1YnN0cihzdHJlYW0ucG9zLCBjICYmIGMgPCB5ID8gYyA6IHgpO1xufVxuXG4vLyBlYXRpbmcgYW5kIHZvbWl0aW5nIGEgcGFydCBvZiBzdHJlYW0gZnJvbSBjdXJyZW50IHBvc2l0aW9uXG5mdW5jdGlvbiBlYXRTdWZmaXgoc3RyZWFtLCBjKSB7XG4gIHZhciB4ID0gc3RyZWFtLnBvcyArIGM7XG4gIHZhciB5O1xuICBpZiAoeCA8PSAwKSBzdHJlYW0ucG9zID0gMDtlbHNlIGlmICh4ID49ICh5ID0gc3RyZWFtLnN0cmluZy5sZW5ndGggLSAxKSkgc3RyZWFtLnBvcyA9IHk7ZWxzZSBzdHJlYW0ucG9zID0geDtcbn1cblxuLy8gaHR0cDovL3Blcmxkb2MucGVybC5vcmdcbnZhciBQRVJMID0ge1xuICAvLyAgIG51bGwgLSBtYWdpYyB0b3VjaFxuICAvLyAgIDEgLSBrZXl3b3JkXG4gIC8vICAgMiAtIGRlZlxuICAvLyAgIDMgLSBhdG9tXG4gIC8vICAgNCAtIG9wZXJhdG9yXG4gIC8vICAgNSAtIGJ1aWx0aW4gKHByZWRlZmluZWQpXG4gIC8vICAgW3gseV0gLSB4PTEsMiwzOyB5PW11c3QgYmUgZGVmaW5lZCBpZiB4ey4uLn1cbiAgLy8gICAgICBQRVJMIG9wZXJhdG9yc1xuICAnLT4nOiA0LFxuICAnKysnOiA0LFxuICAnLS0nOiA0LFxuICAnKionOiA0LFxuICAvLyAgICEgfiBcXCBhbmQgdW5hcnkgKyBhbmQgLVxuICAnPX4nOiA0LFxuICAnIX4nOiA0LFxuICAnKic6IDQsXG4gICcvJzogNCxcbiAgJyUnOiA0LFxuICAneCc6IDQsXG4gICcrJzogNCxcbiAgJy0nOiA0LFxuICAnLic6IDQsXG4gICc8PCc6IDQsXG4gICc+Pic6IDQsXG4gIC8vICAgbmFtZWQgdW5hcnkgb3BlcmF0b3JzXG4gICc8JzogNCxcbiAgJz4nOiA0LFxuICAnPD0nOiA0LFxuICAnPj0nOiA0LFxuICAnbHQnOiA0LFxuICAnZ3QnOiA0LFxuICAnbGUnOiA0LFxuICAnZ2UnOiA0LFxuICAnPT0nOiA0LFxuICAnIT0nOiA0LFxuICAnPD0+JzogNCxcbiAgJ2VxJzogNCxcbiAgJ25lJzogNCxcbiAgJ2NtcCc6IDQsXG4gICd+fic6IDQsXG4gICcmJzogNCxcbiAgJ3wnOiA0LFxuICAnXic6IDQsXG4gICcmJic6IDQsXG4gICd8fCc6IDQsXG4gICcvLyc6IDQsXG4gICcuLic6IDQsXG4gICcuLi4nOiA0LFxuICAnPyc6IDQsXG4gICc6JzogNCxcbiAgJz0nOiA0LFxuICAnKz0nOiA0LFxuICAnLT0nOiA0LFxuICAnKj0nOiA0LFxuICAvLyAgIGV0Yy4gPz8/XG4gICcsJzogNCxcbiAgJz0+JzogNCxcbiAgJzo6JzogNCxcbiAgLy8gICBsaXN0IG9wZXJhdG9ycyAocmlnaHR3YXJkKVxuICAnbm90JzogNCxcbiAgJ2FuZCc6IDQsXG4gICdvcic6IDQsXG4gICd4b3InOiA0LFxuICAvLyAgICAgIFBFUkwgcHJlZGVmaW5lZCB2YXJpYWJsZXMgKEkga25vdywgd2hhdCB0aGlzIGlzIGEgcGFyYW5vaWQgaWRlYSwgYnV0IG1heSBiZSBuZWVkZWQgZm9yIHBlb3BsZSwgd2hvIGxlYXJuIFBFUkwsIGFuZCBmb3IgbWUgYXMgd2VsbCwgLi4uYW5kIG1heSBiZSBmb3IgeW91PzspXG4gICdCRUdJTic6IFs1LCAxXSxcbiAgJ0VORCc6IFs1LCAxXSxcbiAgJ1BSSU5UJzogWzUsIDFdLFxuICAnUFJJTlRGJzogWzUsIDFdLFxuICAnR0VUQyc6IFs1LCAxXSxcbiAgJ1JFQUQnOiBbNSwgMV0sXG4gICdSRUFETElORSc6IFs1LCAxXSxcbiAgJ0RFU1RST1knOiBbNSwgMV0sXG4gICdUSUUnOiBbNSwgMV0sXG4gICdUSUVIQU5ETEUnOiBbNSwgMV0sXG4gICdVTlRJRSc6IFs1LCAxXSxcbiAgJ1NURElOJzogNSxcbiAgJ1NURElOX1RPUCc6IDUsXG4gICdTVERPVVQnOiA1LFxuICAnU1RET1VUX1RPUCc6IDUsXG4gICdTVERFUlInOiA1LFxuICAnU1RERVJSX1RPUCc6IDUsXG4gICckQVJHJzogNSxcbiAgJyRfJzogNSxcbiAgJ0BBUkcnOiA1LFxuICAnQF8nOiA1LFxuICAnJExJU1RfU0VQQVJBVE9SJzogNSxcbiAgJyRcIic6IDUsXG4gICckUFJPQ0VTU19JRCc6IDUsXG4gICckUElEJzogNSxcbiAgJyQkJzogNSxcbiAgJyRSRUFMX0dST1VQX0lEJzogNSxcbiAgJyRHSUQnOiA1LFxuICAnJCgnOiA1LFxuICAnJEVGRkVDVElWRV9HUk9VUF9JRCc6IDUsXG4gICckRUdJRCc6IDUsXG4gICckKSc6IDUsXG4gICckUFJPR1JBTV9OQU1FJzogNSxcbiAgJyQwJzogNSxcbiAgJyRTVUJTQ1JJUFRfU0VQQVJBVE9SJzogNSxcbiAgJyRTVUJTRVAnOiA1LFxuICAnJDsnOiA1LFxuICAnJFJFQUxfVVNFUl9JRCc6IDUsXG4gICckVUlEJzogNSxcbiAgJyQ8JzogNSxcbiAgJyRFRkZFQ1RJVkVfVVNFUl9JRCc6IDUsXG4gICckRVVJRCc6IDUsXG4gICckPic6IDUsXG4gICckYSc6IDUsXG4gICckYic6IDUsXG4gICckQ09NUElMSU5HJzogNSxcbiAgJyReQyc6IDUsXG4gICckREVCVUdHSU5HJzogNSxcbiAgJyReRCc6IDUsXG4gICcke15FTkNPRElOR30nOiA1LFxuICAnJEVOVic6IDUsXG4gICclRU5WJzogNSxcbiAgJyRTWVNURU1fRkRfTUFYJzogNSxcbiAgJyReRic6IDUsXG4gICdARic6IDUsXG4gICcke15HTE9CQUxfUEhBU0V9JzogNSxcbiAgJyReSCc6IDUsXG4gICclXkgnOiA1LFxuICAnQElOQyc6IDUsXG4gICclSU5DJzogNSxcbiAgJyRJTlBMQUNFX0VESVQnOiA1LFxuICAnJF5JJzogNSxcbiAgJyReTSc6IDUsXG4gICckT1NOQU1FJzogNSxcbiAgJyReTyc6IDUsXG4gICcke15PUEVOfSc6IDUsXG4gICckUEVSTERCJzogNSxcbiAgJyReUCc6IDUsXG4gICckU0lHJzogNSxcbiAgJyVTSUcnOiA1LFxuICAnJEJBU0VUSU1FJzogNSxcbiAgJyReVCc6IDUsXG4gICcke15UQUlOVH0nOiA1LFxuICAnJHteVU5JQ09ERX0nOiA1LFxuICAnJHteVVRGOENBQ0hFfSc6IDUsXG4gICcke15VVEY4TE9DQUxFfSc6IDUsXG4gICckUEVSTF9WRVJTSU9OJzogNSxcbiAgJyReVic6IDUsXG4gICcke15XSU4zMl9TTE9QUFlfU1RBVH0nOiA1LFxuICAnJEVYRUNVVEFCTEVfTkFNRSc6IDUsXG4gICckXlgnOiA1LFxuICAnJDEnOiA1LFxuICAvLyAtIHJlZ2V4cCAkMSwgJDIuLi5cbiAgJyRNQVRDSCc6IDUsXG4gICckJic6IDUsXG4gICcke15NQVRDSH0nOiA1LFxuICAnJFBSRU1BVENIJzogNSxcbiAgJyRgJzogNSxcbiAgJyR7XlBSRU1BVENIfSc6IDUsXG4gICckUE9TVE1BVENIJzogNSxcbiAgXCIkJ1wiOiA1LFxuICAnJHteUE9TVE1BVENIfSc6IDUsXG4gICckTEFTVF9QQVJFTl9NQVRDSCc6IDUsXG4gICckKyc6IDUsXG4gICckTEFTVF9TVUJNQVRDSF9SRVNVTFQnOiA1LFxuICAnJF5OJzogNSxcbiAgJ0BMQVNUX01BVENIX0VORCc6IDUsXG4gICdAKyc6IDUsXG4gICclTEFTVF9QQVJFTl9NQVRDSCc6IDUsXG4gICclKyc6IDUsXG4gICdATEFTVF9NQVRDSF9TVEFSVCc6IDUsXG4gICdALSc6IDUsXG4gICclTEFTVF9NQVRDSF9TVEFSVCc6IDUsXG4gICclLSc6IDUsXG4gICckTEFTVF9SRUdFWFBfQ09ERV9SRVNVTFQnOiA1LFxuICAnJF5SJzogNSxcbiAgJyR7XlJFX0RFQlVHX0ZMQUdTfSc6IDUsXG4gICcke15SRV9UUklFX01BWEJVRn0nOiA1LFxuICAnJEFSR1YnOiA1LFxuICAnQEFSR1YnOiA1LFxuICAnQVJHVic6IDUsXG4gICdBUkdWT1VUJzogNSxcbiAgJyRPVVRQVVRfRklFTERfU0VQQVJBVE9SJzogNSxcbiAgJyRPRlMnOiA1LFxuICAnJCwnOiA1LFxuICAnJElOUFVUX0xJTkVfTlVNQkVSJzogNSxcbiAgJyROUic6IDUsXG4gICckLic6IDUsXG4gICckSU5QVVRfUkVDT1JEX1NFUEFSQVRPUic6IDUsXG4gICckUlMnOiA1LFxuICAnJC8nOiA1LFxuICAnJE9VVFBVVF9SRUNPUkRfU0VQQVJBVE9SJzogNSxcbiAgJyRPUlMnOiA1LFxuICAnJFxcXFwnOiA1LFxuICAnJE9VVFBVVF9BVVRPRkxVU0gnOiA1LFxuICAnJHwnOiA1LFxuICAnJEFDQ1VNVUxBVE9SJzogNSxcbiAgJyReQSc6IDUsXG4gICckRk9STUFUX0ZPUk1GRUVEJzogNSxcbiAgJyReTCc6IDUsXG4gICckRk9STUFUX1BBR0VfTlVNQkVSJzogNSxcbiAgJyQlJzogNSxcbiAgJyRGT1JNQVRfTElORVNfTEVGVCc6IDUsXG4gICckLSc6IDUsXG4gICckRk9STUFUX0xJTkVfQlJFQUtfQ0hBUkFDVEVSUyc6IDUsXG4gICckOic6IDUsXG4gICckRk9STUFUX0xJTkVTX1BFUl9QQUdFJzogNSxcbiAgJyQ9JzogNSxcbiAgJyRGT1JNQVRfVE9QX05BTUUnOiA1LFxuICAnJF4nOiA1LFxuICAnJEZPUk1BVF9OQU1FJzogNSxcbiAgJyR+JzogNSxcbiAgJyR7XkNISUxEX0VSUk9SX05BVElWRX0nOiA1LFxuICAnJEVYVEVOREVEX09TX0VSUk9SJzogNSxcbiAgJyReRSc6IDUsXG4gICckRVhDRVBUSU9OU19CRUlOR19DQVVHSFQnOiA1LFxuICAnJF5TJzogNSxcbiAgJyRXQVJOSU5HJzogNSxcbiAgJyReVyc6IDUsXG4gICcke15XQVJOSU5HX0JJVFN9JzogNSxcbiAgJyRPU19FUlJPUic6IDUsXG4gICckRVJSTk8nOiA1LFxuICAnJCEnOiA1LFxuICAnJU9TX0VSUk9SJzogNSxcbiAgJyVFUlJOTyc6IDUsXG4gICclISc6IDUsXG4gICckQ0hJTERfRVJST1InOiA1LFxuICAnJD8nOiA1LFxuICAnJEVWQUxfRVJST1InOiA1LFxuICAnJEAnOiA1LFxuICAnJE9GTVQnOiA1LFxuICAnJCMnOiA1LFxuICAnJConOiA1LFxuICAnJEFSUkFZX0JBU0UnOiA1LFxuICAnJFsnOiA1LFxuICAnJE9MRF9QRVJMX1ZFUlNJT04nOiA1LFxuICAnJF0nOiA1LFxuICAvLyAgICAgIFBFUkwgYmxvY2tzXG4gICdpZic6IFsxLCAxXSxcbiAgZWxzaWY6IFsxLCAxXSxcbiAgJ2Vsc2UnOiBbMSwgMV0sXG4gICd3aGlsZSc6IFsxLCAxXSxcbiAgdW5sZXNzOiBbMSwgMV0sXG4gICdmb3InOiBbMSwgMV0sXG4gIGZvcmVhY2g6IFsxLCAxXSxcbiAgLy8gICAgICBQRVJMIGZ1bmN0aW9uc1xuICAnYWJzJzogMSxcbiAgLy8gLSBhYnNvbHV0ZSB2YWx1ZSBmdW5jdGlvblxuICBhY2NlcHQ6IDEsXG4gIC8vIC0gYWNjZXB0IGFuIGluY29taW5nIHNvY2tldCBjb25uZWN0XG4gIGFsYXJtOiAxLFxuICAvLyAtIHNjaGVkdWxlIGEgU0lHQUxSTVxuICAnYXRhbjInOiAxLFxuICAvLyAtIGFyY3RhbmdlbnQgb2YgWS9YIGluIHRoZSByYW5nZSAtUEkgdG8gUElcbiAgYmluZDogMSxcbiAgLy8gLSBiaW5kcyBhbiBhZGRyZXNzIHRvIGEgc29ja2V0XG4gIGJpbm1vZGU6IDEsXG4gIC8vIC0gcHJlcGFyZSBiaW5hcnkgZmlsZXMgZm9yIEkvT1xuICBibGVzczogMSxcbiAgLy8gLSBjcmVhdGUgYW4gb2JqZWN0XG4gIGJvb3RzdHJhcDogMSxcbiAgLy9cbiAgJ2JyZWFrJzogMSxcbiAgLy8gLSBicmVhayBvdXQgb2YgYSBcImdpdmVuXCIgYmxvY2tcbiAgY2FsbGVyOiAxLFxuICAvLyAtIGdldCBjb250ZXh0IG9mIHRoZSBjdXJyZW50IHN1YnJvdXRpbmUgY2FsbFxuICBjaGRpcjogMSxcbiAgLy8gLSBjaGFuZ2UgeW91ciBjdXJyZW50IHdvcmtpbmcgZGlyZWN0b3J5XG4gIGNobW9kOiAxLFxuICAvLyAtIGNoYW5nZXMgdGhlIHBlcm1pc3Npb25zIG9uIGEgbGlzdCBvZiBmaWxlc1xuICBjaG9tcDogMSxcbiAgLy8gLSByZW1vdmUgYSB0cmFpbGluZyByZWNvcmQgc2VwYXJhdG9yIGZyb20gYSBzdHJpbmdcbiAgY2hvcDogMSxcbiAgLy8gLSByZW1vdmUgdGhlIGxhc3QgY2hhcmFjdGVyIGZyb20gYSBzdHJpbmdcbiAgY2hvd246IDEsXG4gIC8vIC0gY2hhbmdlIHRoZSBvd25lcnNoaXAgb24gYSBsaXN0IG9mIGZpbGVzXG4gIGNocjogMSxcbiAgLy8gLSBnZXQgY2hhcmFjdGVyIHRoaXMgbnVtYmVyIHJlcHJlc2VudHNcbiAgY2hyb290OiAxLFxuICAvLyAtIG1ha2UgZGlyZWN0b3J5IG5ldyByb290IGZvciBwYXRoIGxvb2t1cHNcbiAgY2xvc2U6IDEsXG4gIC8vIC0gY2xvc2UgZmlsZSAob3IgcGlwZSBvciBzb2NrZXQpIGhhbmRsZVxuICBjbG9zZWRpcjogMSxcbiAgLy8gLSBjbG9zZSBkaXJlY3RvcnkgaGFuZGxlXG4gIGNvbm5lY3Q6IDEsXG4gIC8vIC0gY29ubmVjdCB0byBhIHJlbW90ZSBzb2NrZXRcbiAgJ2NvbnRpbnVlJzogWzEsIDFdLFxuICAvLyAtIG9wdGlvbmFsIHRyYWlsaW5nIGJsb2NrIGluIGEgd2hpbGUgb3IgZm9yZWFjaFxuICAnY29zJzogMSxcbiAgLy8gLSBjb3NpbmUgZnVuY3Rpb25cbiAgY3J5cHQ6IDEsXG4gIC8vIC0gb25lLXdheSBwYXNzd2Qtc3R5bGUgZW5jcnlwdGlvblxuICBkYm1jbG9zZTogMSxcbiAgLy8gLSBicmVha3MgYmluZGluZyBvbiBhIHRpZWQgZGJtIGZpbGVcbiAgZGJtb3BlbjogMSxcbiAgLy8gLSBjcmVhdGUgYmluZGluZyBvbiBhIHRpZWQgZGJtIGZpbGVcbiAgJ2RlZmF1bHQnOiAxLFxuICAvL1xuICBkZWZpbmVkOiAxLFxuICAvLyAtIHRlc3Qgd2hldGhlciBhIHZhbHVlLCB2YXJpYWJsZSwgb3IgZnVuY3Rpb24gaXMgZGVmaW5lZFxuICAnZGVsZXRlJzogMSxcbiAgLy8gLSBkZWxldGVzIGEgdmFsdWUgZnJvbSBhIGhhc2hcbiAgZGllOiAxLFxuICAvLyAtIHJhaXNlIGFuIGV4Y2VwdGlvbiBvciBiYWlsIG91dFxuICAnZG8nOiAxLFxuICAvLyAtIHR1cm4gYSBCTE9DSyBpbnRvIGEgVEVSTVxuICBkdW1wOiAxLFxuICAvLyAtIGNyZWF0ZSBhbiBpbW1lZGlhdGUgY29yZSBkdW1wXG4gIGVhY2g6IDEsXG4gIC8vIC0gcmV0cmlldmUgdGhlIG5leHQga2V5L3ZhbHVlIHBhaXIgZnJvbSBhIGhhc2hcbiAgZW5kZ3JlbnQ6IDEsXG4gIC8vIC0gYmUgZG9uZSB1c2luZyBncm91cCBmaWxlXG4gIGVuZGhvc3RlbnQ6IDEsXG4gIC8vIC0gYmUgZG9uZSB1c2luZyBob3N0cyBmaWxlXG4gIGVuZG5ldGVudDogMSxcbiAgLy8gLSBiZSBkb25lIHVzaW5nIG5ldHdvcmtzIGZpbGVcbiAgZW5kcHJvdG9lbnQ6IDEsXG4gIC8vIC0gYmUgZG9uZSB1c2luZyBwcm90b2NvbHMgZmlsZVxuICBlbmRwd2VudDogMSxcbiAgLy8gLSBiZSBkb25lIHVzaW5nIHBhc3N3ZCBmaWxlXG4gIGVuZHNlcnZlbnQ6IDEsXG4gIC8vIC0gYmUgZG9uZSB1c2luZyBzZXJ2aWNlcyBmaWxlXG4gIGVvZjogMSxcbiAgLy8gLSB0ZXN0IGEgZmlsZWhhbmRsZSBmb3IgaXRzIGVuZFxuICAnZXZhbCc6IDEsXG4gIC8vIC0gY2F0Y2ggZXhjZXB0aW9ucyBvciBjb21waWxlIGFuZCBydW4gY29kZVxuICAnZXhlYyc6IDEsXG4gIC8vIC0gYWJhbmRvbiB0aGlzIHByb2dyYW0gdG8gcnVuIGFub3RoZXJcbiAgZXhpc3RzOiAxLFxuICAvLyAtIHRlc3Qgd2hldGhlciBhIGhhc2gga2V5IGlzIHByZXNlbnRcbiAgZXhpdDogMSxcbiAgLy8gLSB0ZXJtaW5hdGUgdGhpcyBwcm9ncmFtXG4gICdleHAnOiAxLFxuICAvLyAtIHJhaXNlIEkgdG8gYSBwb3dlclxuICBmY250bDogMSxcbiAgLy8gLSBmaWxlIGNvbnRyb2wgc3lzdGVtIGNhbGxcbiAgZmlsZW5vOiAxLFxuICAvLyAtIHJldHVybiBmaWxlIGRlc2NyaXB0b3IgZnJvbSBmaWxlaGFuZGxlXG4gIGZsb2NrOiAxLFxuICAvLyAtIGxvY2sgYW4gZW50aXJlIGZpbGUgd2l0aCBhbiBhZHZpc29yeSBsb2NrXG4gIGZvcms6IDEsXG4gIC8vIC0gY3JlYXRlIGEgbmV3IHByb2Nlc3MganVzdCBsaWtlIHRoaXMgb25lXG4gIGZvcm1hdDogMSxcbiAgLy8gLSBkZWNsYXJlIGEgcGljdHVyZSBmb3JtYXQgd2l0aCB1c2UgYnkgdGhlIHdyaXRlKCkgZnVuY3Rpb25cbiAgZm9ybWxpbmU6IDEsXG4gIC8vIC0gaW50ZXJuYWwgZnVuY3Rpb24gdXNlZCBmb3IgZm9ybWF0c1xuICBnZXRjOiAxLFxuICAvLyAtIGdldCB0aGUgbmV4dCBjaGFyYWN0ZXIgZnJvbSB0aGUgZmlsZWhhbmRsZVxuICBnZXRncmVudDogMSxcbiAgLy8gLSBnZXQgbmV4dCBncm91cCByZWNvcmRcbiAgZ2V0Z3JnaWQ6IDEsXG4gIC8vIC0gZ2V0IGdyb3VwIHJlY29yZCBnaXZlbiBncm91cCB1c2VyIElEXG4gIGdldGdybmFtOiAxLFxuICAvLyAtIGdldCBncm91cCByZWNvcmQgZ2l2ZW4gZ3JvdXAgbmFtZVxuICBnZXRob3N0YnlhZGRyOiAxLFxuICAvLyAtIGdldCBob3N0IHJlY29yZCBnaXZlbiBpdHMgYWRkcmVzc1xuICBnZXRob3N0YnluYW1lOiAxLFxuICAvLyAtIGdldCBob3N0IHJlY29yZCBnaXZlbiBuYW1lXG4gIGdldGhvc3RlbnQ6IDEsXG4gIC8vIC0gZ2V0IG5leHQgaG9zdHMgcmVjb3JkXG4gIGdldGxvZ2luOiAxLFxuICAvLyAtIHJldHVybiB3aG8gbG9nZ2VkIGluIGF0IHRoaXMgdHR5XG4gIGdldG5ldGJ5YWRkcjogMSxcbiAgLy8gLSBnZXQgbmV0d29yayByZWNvcmQgZ2l2ZW4gaXRzIGFkZHJlc3NcbiAgZ2V0bmV0YnluYW1lOiAxLFxuICAvLyAtIGdldCBuZXR3b3JrcyByZWNvcmQgZ2l2ZW4gbmFtZVxuICBnZXRuZXRlbnQ6IDEsXG4gIC8vIC0gZ2V0IG5leHQgbmV0d29ya3MgcmVjb3JkXG4gIGdldHBlZXJuYW1lOiAxLFxuICAvLyAtIGZpbmQgdGhlIG90aGVyIGVuZCBvZiBhIHNvY2tldCBjb25uZWN0aW9uXG4gIGdldHBncnA6IDEsXG4gIC8vIC0gZ2V0IHByb2Nlc3MgZ3JvdXBcbiAgZ2V0cHBpZDogMSxcbiAgLy8gLSBnZXQgcGFyZW50IHByb2Nlc3MgSURcbiAgZ2V0cHJpb3JpdHk6IDEsXG4gIC8vIC0gZ2V0IGN1cnJlbnQgbmljZSB2YWx1ZVxuICBnZXRwcm90b2J5bmFtZTogMSxcbiAgLy8gLSBnZXQgcHJvdG9jb2wgcmVjb3JkIGdpdmVuIG5hbWVcbiAgZ2V0cHJvdG9ieW51bWJlcjogMSxcbiAgLy8gLSBnZXQgcHJvdG9jb2wgcmVjb3JkIG51bWVyaWMgcHJvdG9jb2xcbiAgZ2V0cHJvdG9lbnQ6IDEsXG4gIC8vIC0gZ2V0IG5leHQgcHJvdG9jb2xzIHJlY29yZFxuICBnZXRwd2VudDogMSxcbiAgLy8gLSBnZXQgbmV4dCBwYXNzd2QgcmVjb3JkXG4gIGdldHB3bmFtOiAxLFxuICAvLyAtIGdldCBwYXNzd2QgcmVjb3JkIGdpdmVuIHVzZXIgbG9naW4gbmFtZVxuICBnZXRwd3VpZDogMSxcbiAgLy8gLSBnZXQgcGFzc3dkIHJlY29yZCBnaXZlbiB1c2VyIElEXG4gIGdldHNlcnZieW5hbWU6IDEsXG4gIC8vIC0gZ2V0IHNlcnZpY2VzIHJlY29yZCBnaXZlbiBpdHMgbmFtZVxuICBnZXRzZXJ2Ynlwb3J0OiAxLFxuICAvLyAtIGdldCBzZXJ2aWNlcyByZWNvcmQgZ2l2ZW4gbnVtZXJpYyBwb3J0XG4gIGdldHNlcnZlbnQ6IDEsXG4gIC8vIC0gZ2V0IG5leHQgc2VydmljZXMgcmVjb3JkXG4gIGdldHNvY2tuYW1lOiAxLFxuICAvLyAtIHJldHJpZXZlIHRoZSBzb2NrYWRkciBmb3IgYSBnaXZlbiBzb2NrZXRcbiAgZ2V0c29ja29wdDogMSxcbiAgLy8gLSBnZXQgc29ja2V0IG9wdGlvbnMgb24gYSBnaXZlbiBzb2NrZXRcbiAgZ2l2ZW46IDEsXG4gIC8vXG4gIGdsb2I6IDEsXG4gIC8vIC0gZXhwYW5kIGZpbGVuYW1lcyB1c2luZyB3aWxkY2FyZHNcbiAgZ210aW1lOiAxLFxuICAvLyAtIGNvbnZlcnQgVU5JWCB0aW1lIGludG8gcmVjb3JkIG9yIHN0cmluZyB1c2luZyBHcmVlbndpY2ggdGltZVxuICAnZ290byc6IDEsXG4gIC8vIC0gY3JlYXRlIHNwYWdoZXR0aSBjb2RlXG4gIGdyZXA6IDEsXG4gIC8vIC0gbG9jYXRlIGVsZW1lbnRzIGluIGEgbGlzdCB0ZXN0IHRydWUgYWdhaW5zdCBhIGdpdmVuIGNyaXRlcmlvblxuICBoZXg6IDEsXG4gIC8vIC0gY29udmVydCBhIHN0cmluZyB0byBhIGhleGFkZWNpbWFsIG51bWJlclxuICAnaW1wb3J0JzogMSxcbiAgLy8gLSBwYXRjaCBhIG1vZHVsZSdzIG5hbWVzcGFjZSBpbnRvIHlvdXIgb3duXG4gIGluZGV4OiAxLFxuICAvLyAtIGZpbmQgYSBzdWJzdHJpbmcgd2l0aGluIGEgc3RyaW5nXG4gICdpbnQnOiAxLFxuICAvLyAtIGdldCB0aGUgaW50ZWdlciBwb3J0aW9uIG9mIGEgbnVtYmVyXG4gIGlvY3RsOiAxLFxuICAvLyAtIHN5c3RlbS1kZXBlbmRlbnQgZGV2aWNlIGNvbnRyb2wgc3lzdGVtIGNhbGxcbiAgJ2pvaW4nOiAxLFxuICAvLyAtIGpvaW4gYSBsaXN0IGludG8gYSBzdHJpbmcgdXNpbmcgYSBzZXBhcmF0b3JcbiAga2V5czogMSxcbiAgLy8gLSByZXRyaWV2ZSBsaXN0IG9mIGluZGljZXMgZnJvbSBhIGhhc2hcbiAga2lsbDogMSxcbiAgLy8gLSBzZW5kIGEgc2lnbmFsIHRvIGEgcHJvY2VzcyBvciBwcm9jZXNzIGdyb3VwXG4gIGxhc3Q6IDEsXG4gIC8vIC0gZXhpdCBhIGJsb2NrIHByZW1hdHVyZWx5XG4gIGxjOiAxLFxuICAvLyAtIHJldHVybiBsb3dlci1jYXNlIHZlcnNpb24gb2YgYSBzdHJpbmdcbiAgbGNmaXJzdDogMSxcbiAgLy8gLSByZXR1cm4gYSBzdHJpbmcgd2l0aCBqdXN0IHRoZSBuZXh0IGxldHRlciBpbiBsb3dlciBjYXNlXG4gIGxlbmd0aDogMSxcbiAgLy8gLSByZXR1cm4gdGhlIG51bWJlciBvZiBieXRlcyBpbiBhIHN0cmluZ1xuICAnbGluayc6IDEsXG4gIC8vIC0gY3JlYXRlIGEgaGFyZCBsaW5rIGluIHRoZSBmaWxlc3lzdGVtXG4gIGxpc3RlbjogMSxcbiAgLy8gLSByZWdpc3RlciB5b3VyIHNvY2tldCBhcyBhIHNlcnZlclxuICBsb2NhbDogMixcbiAgLy8gLSBjcmVhdGUgYSB0ZW1wb3JhcnkgdmFsdWUgZm9yIGEgZ2xvYmFsIHZhcmlhYmxlIChkeW5hbWljIHNjb3BpbmcpXG4gIGxvY2FsdGltZTogMSxcbiAgLy8gLSBjb252ZXJ0IFVOSVggdGltZSBpbnRvIHJlY29yZCBvciBzdHJpbmcgdXNpbmcgbG9jYWwgdGltZVxuICBsb2NrOiAxLFxuICAvLyAtIGdldCBhIHRocmVhZCBsb2NrIG9uIGEgdmFyaWFibGUsIHN1YnJvdXRpbmUsIG9yIG1ldGhvZFxuICAnbG9nJzogMSxcbiAgLy8gLSByZXRyaWV2ZSB0aGUgbmF0dXJhbCBsb2dhcml0aG0gZm9yIGEgbnVtYmVyXG4gIGxzdGF0OiAxLFxuICAvLyAtIHN0YXQgYSBzeW1ib2xpYyBsaW5rXG4gIG06IG51bGwsXG4gIC8vIC0gbWF0Y2ggYSBzdHJpbmcgd2l0aCBhIHJlZ3VsYXIgZXhwcmVzc2lvbiBwYXR0ZXJuXG4gIG1hcDogMSxcbiAgLy8gLSBhcHBseSBhIGNoYW5nZSB0byBhIGxpc3QgdG8gZ2V0IGJhY2sgYSBuZXcgbGlzdCB3aXRoIHRoZSBjaGFuZ2VzXG4gIG1rZGlyOiAxLFxuICAvLyAtIGNyZWF0ZSBhIGRpcmVjdG9yeVxuICBtc2djdGw6IDEsXG4gIC8vIC0gU3lzViBJUEMgbWVzc2FnZSBjb250cm9sIG9wZXJhdGlvbnNcbiAgbXNnZ2V0OiAxLFxuICAvLyAtIGdldCBTeXNWIElQQyBtZXNzYWdlIHF1ZXVlXG4gIG1zZ3JjdjogMSxcbiAgLy8gLSByZWNlaXZlIGEgU3lzViBJUEMgbWVzc2FnZSBmcm9tIGEgbWVzc2FnZSBxdWV1ZVxuICBtc2dzbmQ6IDEsXG4gIC8vIC0gc2VuZCBhIFN5c1YgSVBDIG1lc3NhZ2UgdG8gYSBtZXNzYWdlIHF1ZXVlXG4gIG15OiAyLFxuICAvLyAtIGRlY2xhcmUgYW5kIGFzc2lnbiBhIGxvY2FsIHZhcmlhYmxlIChsZXhpY2FsIHNjb3BpbmcpXG4gICduZXcnOiAxLFxuICAvL1xuICBuZXh0OiAxLFxuICAvLyAtIGl0ZXJhdGUgYSBibG9jayBwcmVtYXR1cmVseVxuICBubzogMSxcbiAgLy8gLSB1bmltcG9ydCBzb21lIG1vZHVsZSBzeW1ib2xzIG9yIHNlbWFudGljcyBhdCBjb21waWxlIHRpbWVcbiAgb2N0OiAxLFxuICAvLyAtIGNvbnZlcnQgYSBzdHJpbmcgdG8gYW4gb2N0YWwgbnVtYmVyXG4gIG9wZW46IDEsXG4gIC8vIC0gb3BlbiBhIGZpbGUsIHBpcGUsIG9yIGRlc2NyaXB0b3JcbiAgb3BlbmRpcjogMSxcbiAgLy8gLSBvcGVuIGEgZGlyZWN0b3J5XG4gIG9yZDogMSxcbiAgLy8gLSBmaW5kIGEgY2hhcmFjdGVyJ3MgbnVtZXJpYyByZXByZXNlbnRhdGlvblxuICBvdXI6IDIsXG4gIC8vIC0gZGVjbGFyZSBhbmQgYXNzaWduIGEgcGFja2FnZSB2YXJpYWJsZSAobGV4aWNhbCBzY29waW5nKVxuICBwYWNrOiAxLFxuICAvLyAtIGNvbnZlcnQgYSBsaXN0IGludG8gYSBiaW5hcnkgcmVwcmVzZW50YXRpb25cbiAgJ3BhY2thZ2UnOiAxLFxuICAvLyAtIGRlY2xhcmUgYSBzZXBhcmF0ZSBnbG9iYWwgbmFtZXNwYWNlXG4gIHBpcGU6IDEsXG4gIC8vIC0gb3BlbiBhIHBhaXIgb2YgY29ubmVjdGVkIGZpbGVoYW5kbGVzXG4gIHBvcDogMSxcbiAgLy8gLSByZW1vdmUgdGhlIGxhc3QgZWxlbWVudCBmcm9tIGFuIGFycmF5IGFuZCByZXR1cm4gaXRcbiAgcG9zOiAxLFxuICAvLyAtIGZpbmQgb3Igc2V0IHRoZSBvZmZzZXQgZm9yIHRoZSBsYXN0L25leHQgbS8vZyBzZWFyY2hcbiAgcHJpbnQ6IDEsXG4gIC8vIC0gb3V0cHV0IGEgbGlzdCB0byBhIGZpbGVoYW5kbGVcbiAgcHJpbnRmOiAxLFxuICAvLyAtIG91dHB1dCBhIGZvcm1hdHRlZCBsaXN0IHRvIGEgZmlsZWhhbmRsZVxuICBwcm90b3R5cGU6IDEsXG4gIC8vIC0gZ2V0IHRoZSBwcm90b3R5cGUgKGlmIGFueSkgb2YgYSBzdWJyb3V0aW5lXG4gIHB1c2g6IDEsXG4gIC8vIC0gYXBwZW5kIG9uZSBvciBtb3JlIGVsZW1lbnRzIHRvIGFuIGFycmF5XG4gIHE6IG51bGwsXG4gIC8vIC0gc2luZ2x5IHF1b3RlIGEgc3RyaW5nXG4gIHFxOiBudWxsLFxuICAvLyAtIGRvdWJseSBxdW90ZSBhIHN0cmluZ1xuICBxcjogbnVsbCxcbiAgLy8gLSBDb21waWxlIHBhdHRlcm5cbiAgcXVvdGVtZXRhOiBudWxsLFxuICAvLyAtIHF1b3RlIHJlZ3VsYXIgZXhwcmVzc2lvbiBtYWdpYyBjaGFyYWN0ZXJzXG4gIHF3OiBudWxsLFxuICAvLyAtIHF1b3RlIGEgbGlzdCBvZiB3b3Jkc1xuICBxeDogbnVsbCxcbiAgLy8gLSBiYWNrcXVvdGUgcXVvdGUgYSBzdHJpbmdcbiAgcmFuZDogMSxcbiAgLy8gLSByZXRyaWV2ZSB0aGUgbmV4dCBwc2V1ZG9yYW5kb20gbnVtYmVyXG4gIHJlYWQ6IDEsXG4gIC8vIC0gZml4ZWQtbGVuZ3RoIGJ1ZmZlcmVkIGlucHV0IGZyb20gYSBmaWxlaGFuZGxlXG4gIHJlYWRkaXI6IDEsXG4gIC8vIC0gZ2V0IGEgZGlyZWN0b3J5IGZyb20gYSBkaXJlY3RvcnkgaGFuZGxlXG4gIHJlYWRsaW5lOiAxLFxuICAvLyAtIGZldGNoIGEgcmVjb3JkIGZyb20gYSBmaWxlXG4gIHJlYWRsaW5rOiAxLFxuICAvLyAtIGRldGVybWluZSB3aGVyZSBhIHN5bWJvbGljIGxpbmsgaXMgcG9pbnRpbmdcbiAgcmVhZHBpcGU6IDEsXG4gIC8vIC0gZXhlY3V0ZSBhIHN5c3RlbSBjb21tYW5kIGFuZCBjb2xsZWN0IHN0YW5kYXJkIG91dHB1dFxuICByZWN2OiAxLFxuICAvLyAtIHJlY2VpdmUgYSBtZXNzYWdlIG92ZXIgYSBTb2NrZXRcbiAgcmVkbzogMSxcbiAgLy8gLSBzdGFydCB0aGlzIGxvb3AgaXRlcmF0aW9uIG92ZXIgYWdhaW5cbiAgcmVmOiAxLFxuICAvLyAtIGZpbmQgb3V0IHRoZSB0eXBlIG9mIHRoaW5nIGJlaW5nIHJlZmVyZW5jZWRcbiAgcmVuYW1lOiAxLFxuICAvLyAtIGNoYW5nZSBhIGZpbGVuYW1lXG4gIHJlcXVpcmU6IDEsXG4gIC8vIC0gbG9hZCBpbiBleHRlcm5hbCBmdW5jdGlvbnMgZnJvbSBhIGxpYnJhcnkgYXQgcnVudGltZVxuICByZXNldDogMSxcbiAgLy8gLSBjbGVhciBhbGwgdmFyaWFibGVzIG9mIGEgZ2l2ZW4gbmFtZVxuICAncmV0dXJuJzogMSxcbiAgLy8gLSBnZXQgb3V0IG9mIGEgZnVuY3Rpb24gZWFybHlcbiAgcmV2ZXJzZTogMSxcbiAgLy8gLSBmbGlwIGEgc3RyaW5nIG9yIGEgbGlzdFxuICByZXdpbmRkaXI6IDEsXG4gIC8vIC0gcmVzZXQgZGlyZWN0b3J5IGhhbmRsZVxuICByaW5kZXg6IDEsXG4gIC8vIC0gcmlnaHQtdG8tbGVmdCBzdWJzdHJpbmcgc2VhcmNoXG4gIHJtZGlyOiAxLFxuICAvLyAtIHJlbW92ZSBhIGRpcmVjdG9yeVxuICBzOiBudWxsLFxuICAvLyAtIHJlcGxhY2UgYSBwYXR0ZXJuIHdpdGggYSBzdHJpbmdcbiAgc2F5OiAxLFxuICAvLyAtIHByaW50IHdpdGggbmV3bGluZVxuICBzY2FsYXI6IDEsXG4gIC8vIC0gZm9yY2UgYSBzY2FsYXIgY29udGV4dFxuICBzZWVrOiAxLFxuICAvLyAtIHJlcG9zaXRpb24gZmlsZSBwb2ludGVyIGZvciByYW5kb20tYWNjZXNzIEkvT1xuICBzZWVrZGlyOiAxLFxuICAvLyAtIHJlcG9zaXRpb24gZGlyZWN0b3J5IHBvaW50ZXJcbiAgc2VsZWN0OiAxLFxuICAvLyAtIHJlc2V0IGRlZmF1bHQgb3V0cHV0IG9yIGRvIEkvTyBtdWx0aXBsZXhpbmdcbiAgc2VtY3RsOiAxLFxuICAvLyAtIFN5c1Ygc2VtYXBob3JlIGNvbnRyb2wgb3BlcmF0aW9uc1xuICBzZW1nZXQ6IDEsXG4gIC8vIC0gZ2V0IHNldCBvZiBTeXNWIHNlbWFwaG9yZXNcbiAgc2Vtb3A6IDEsXG4gIC8vIC0gU3lzViBzZW1hcGhvcmUgb3BlcmF0aW9uc1xuICBzZW5kOiAxLFxuICAvLyAtIHNlbmQgYSBtZXNzYWdlIG92ZXIgYSBzb2NrZXRcbiAgc2V0Z3JlbnQ6IDEsXG4gIC8vIC0gcHJlcGFyZSBncm91cCBmaWxlIGZvciB1c2VcbiAgc2V0aG9zdGVudDogMSxcbiAgLy8gLSBwcmVwYXJlIGhvc3RzIGZpbGUgZm9yIHVzZVxuICBzZXRuZXRlbnQ6IDEsXG4gIC8vIC0gcHJlcGFyZSBuZXR3b3JrcyBmaWxlIGZvciB1c2VcbiAgc2V0cGdycDogMSxcbiAgLy8gLSBzZXQgdGhlIHByb2Nlc3MgZ3JvdXAgb2YgYSBwcm9jZXNzXG4gIHNldHByaW9yaXR5OiAxLFxuICAvLyAtIHNldCBhIHByb2Nlc3MncyBuaWNlIHZhbHVlXG4gIHNldHByb3RvZW50OiAxLFxuICAvLyAtIHByZXBhcmUgcHJvdG9jb2xzIGZpbGUgZm9yIHVzZVxuICBzZXRwd2VudDogMSxcbiAgLy8gLSBwcmVwYXJlIHBhc3N3ZCBmaWxlIGZvciB1c2VcbiAgc2V0c2VydmVudDogMSxcbiAgLy8gLSBwcmVwYXJlIHNlcnZpY2VzIGZpbGUgZm9yIHVzZVxuICBzZXRzb2Nrb3B0OiAxLFxuICAvLyAtIHNldCBzb21lIHNvY2tldCBvcHRpb25zXG4gIHNoaWZ0OiAxLFxuICAvLyAtIHJlbW92ZSB0aGUgZmlyc3QgZWxlbWVudCBvZiBhbiBhcnJheSwgYW5kIHJldHVybiBpdFxuICBzaG1jdGw6IDEsXG4gIC8vIC0gU3lzViBzaGFyZWQgbWVtb3J5IG9wZXJhdGlvbnNcbiAgc2htZ2V0OiAxLFxuICAvLyAtIGdldCBTeXNWIHNoYXJlZCBtZW1vcnkgc2VnbWVudCBpZGVudGlmaWVyXG4gIHNobXJlYWQ6IDEsXG4gIC8vIC0gcmVhZCBTeXNWIHNoYXJlZCBtZW1vcnlcbiAgc2htd3JpdGU6IDEsXG4gIC8vIC0gd3JpdGUgU3lzViBzaGFyZWQgbWVtb3J5XG4gIHNodXRkb3duOiAxLFxuICAvLyAtIGNsb3NlIGRvd24ganVzdCBoYWxmIG9mIGEgc29ja2V0IGNvbm5lY3Rpb25cbiAgJ3Npbic6IDEsXG4gIC8vIC0gcmV0dXJuIHRoZSBzaW5lIG9mIGEgbnVtYmVyXG4gIHNsZWVwOiAxLFxuICAvLyAtIGJsb2NrIGZvciBzb21lIG51bWJlciBvZiBzZWNvbmRzXG4gIHNvY2tldDogMSxcbiAgLy8gLSBjcmVhdGUgYSBzb2NrZXRcbiAgc29ja2V0cGFpcjogMSxcbiAgLy8gLSBjcmVhdGUgYSBwYWlyIG9mIHNvY2tldHNcbiAgJ3NvcnQnOiAxLFxuICAvLyAtIHNvcnQgYSBsaXN0IG9mIHZhbHVlc1xuICBzcGxpY2U6IDEsXG4gIC8vIC0gYWRkIG9yIHJlbW92ZSBlbGVtZW50cyBhbnl3aGVyZSBpbiBhbiBhcnJheVxuICAnc3BsaXQnOiAxLFxuICAvLyAtIHNwbGl0IHVwIGEgc3RyaW5nIHVzaW5nIGEgcmVnZXhwIGRlbGltaXRlclxuICBzcHJpbnRmOiAxLFxuICAvLyAtIGZvcm1hdHRlZCBwcmludCBpbnRvIGEgc3RyaW5nXG4gICdzcXJ0JzogMSxcbiAgLy8gLSBzcXVhcmUgcm9vdCBmdW5jdGlvblxuICBzcmFuZDogMSxcbiAgLy8gLSBzZWVkIHRoZSByYW5kb20gbnVtYmVyIGdlbmVyYXRvclxuICBzdGF0OiAxLFxuICAvLyAtIGdldCBhIGZpbGUncyBzdGF0dXMgaW5mb3JtYXRpb25cbiAgc3RhdGU6IDEsXG4gIC8vIC0gZGVjbGFyZSBhbmQgYXNzaWduIGEgc3RhdGUgdmFyaWFibGUgKHBlcnNpc3RlbnQgbGV4aWNhbCBzY29waW5nKVxuICBzdHVkeTogMSxcbiAgLy8gLSBvcHRpbWl6ZSBpbnB1dCBkYXRhIGZvciByZXBlYXRlZCBzZWFyY2hlc1xuICAnc3ViJzogMSxcbiAgLy8gLSBkZWNsYXJlIGEgc3Vicm91dGluZSwgcG9zc2libHkgYW5vbnltb3VzbHlcbiAgJ3N1YnN0cic6IDEsXG4gIC8vIC0gZ2V0IG9yIGFsdGVyIGEgcG9ydGlvbiBvZiBhIHN0cmluZ1xuICBzeW1saW5rOiAxLFxuICAvLyAtIGNyZWF0ZSBhIHN5bWJvbGljIGxpbmsgdG8gYSBmaWxlXG4gIHN5c2NhbGw6IDEsXG4gIC8vIC0gZXhlY3V0ZSBhbiBhcmJpdHJhcnkgc3lzdGVtIGNhbGxcbiAgc3lzb3BlbjogMSxcbiAgLy8gLSBvcGVuIGEgZmlsZSwgcGlwZSwgb3IgZGVzY3JpcHRvclxuICBzeXNyZWFkOiAxLFxuICAvLyAtIGZpeGVkLWxlbmd0aCB1bmJ1ZmZlcmVkIGlucHV0IGZyb20gYSBmaWxlaGFuZGxlXG4gIHN5c3NlZWs6IDEsXG4gIC8vIC0gcG9zaXRpb24gSS9PIHBvaW50ZXIgb24gaGFuZGxlIHVzZWQgd2l0aCBzeXNyZWFkIGFuZCBzeXN3cml0ZVxuICBzeXN0ZW06IDEsXG4gIC8vIC0gcnVuIGEgc2VwYXJhdGUgcHJvZ3JhbVxuICBzeXN3cml0ZTogMSxcbiAgLy8gLSBmaXhlZC1sZW5ndGggdW5idWZmZXJlZCBvdXRwdXQgdG8gYSBmaWxlaGFuZGxlXG4gIHRlbGw6IDEsXG4gIC8vIC0gZ2V0IGN1cnJlbnQgc2Vla3BvaW50ZXIgb24gYSBmaWxlaGFuZGxlXG4gIHRlbGxkaXI6IDEsXG4gIC8vIC0gZ2V0IGN1cnJlbnQgc2Vla3BvaW50ZXIgb24gYSBkaXJlY3RvcnkgaGFuZGxlXG4gIHRpZTogMSxcbiAgLy8gLSBiaW5kIGEgdmFyaWFibGUgdG8gYW4gb2JqZWN0IGNsYXNzXG4gIHRpZWQ6IDEsXG4gIC8vIC0gZ2V0IGEgcmVmZXJlbmNlIHRvIHRoZSBvYmplY3QgdW5kZXJseWluZyBhIHRpZWQgdmFyaWFibGVcbiAgdGltZTogMSxcbiAgLy8gLSByZXR1cm4gbnVtYmVyIG9mIHNlY29uZHMgc2luY2UgMTk3MFxuICB0aW1lczogMSxcbiAgLy8gLSByZXR1cm4gZWxhcHNlZCB0aW1lIGZvciBzZWxmIGFuZCBjaGlsZCBwcm9jZXNzZXNcbiAgdHI6IG51bGwsXG4gIC8vIC0gdHJhbnNsaXRlcmF0ZSBhIHN0cmluZ1xuICB0cnVuY2F0ZTogMSxcbiAgLy8gLSBzaG9ydGVuIGEgZmlsZVxuICB1YzogMSxcbiAgLy8gLSByZXR1cm4gdXBwZXItY2FzZSB2ZXJzaW9uIG9mIGEgc3RyaW5nXG4gIHVjZmlyc3Q6IDEsXG4gIC8vIC0gcmV0dXJuIGEgc3RyaW5nIHdpdGgganVzdCB0aGUgbmV4dCBsZXR0ZXIgaW4gdXBwZXIgY2FzZVxuICB1bWFzazogMSxcbiAgLy8gLSBzZXQgZmlsZSBjcmVhdGlvbiBtb2RlIG1hc2tcbiAgdW5kZWY6IDEsXG4gIC8vIC0gcmVtb3ZlIGEgdmFyaWFibGUgb3IgZnVuY3Rpb24gZGVmaW5pdGlvblxuICB1bmxpbms6IDEsXG4gIC8vIC0gcmVtb3ZlIG9uZSBsaW5rIHRvIGEgZmlsZVxuICB1bnBhY2s6IDEsXG4gIC8vIC0gY29udmVydCBiaW5hcnkgc3RydWN0dXJlIGludG8gbm9ybWFsIHBlcmwgdmFyaWFibGVzXG4gIHVuc2hpZnQ6IDEsXG4gIC8vIC0gcHJlcGVuZCBtb3JlIGVsZW1lbnRzIHRvIHRoZSBiZWdpbm5pbmcgb2YgYSBsaXN0XG4gIHVudGllOiAxLFxuICAvLyAtIGJyZWFrIGEgdGllIGJpbmRpbmcgdG8gYSB2YXJpYWJsZVxuICB1c2U6IDEsXG4gIC8vIC0gbG9hZCBpbiBhIG1vZHVsZSBhdCBjb21waWxlIHRpbWVcbiAgdXRpbWU6IDEsXG4gIC8vIC0gc2V0IGEgZmlsZSdzIGxhc3QgYWNjZXNzIGFuZCBtb2RpZnkgdGltZXNcbiAgdmFsdWVzOiAxLFxuICAvLyAtIHJldHVybiBhIGxpc3Qgb2YgdGhlIHZhbHVlcyBpbiBhIGhhc2hcbiAgdmVjOiAxLFxuICAvLyAtIHRlc3Qgb3Igc2V0IHBhcnRpY3VsYXIgYml0cyBpbiBhIHN0cmluZ1xuICB3YWl0OiAxLFxuICAvLyAtIHdhaXQgZm9yIGFueSBjaGlsZCBwcm9jZXNzIHRvIGRpZVxuICB3YWl0cGlkOiAxLFxuICAvLyAtIHdhaXQgZm9yIGEgcGFydGljdWxhciBjaGlsZCBwcm9jZXNzIHRvIGRpZVxuICB3YW50YXJyYXk6IDEsXG4gIC8vIC0gZ2V0IHZvaWQgdnMgc2NhbGFyIHZzIGxpc3QgY29udGV4dCBvZiBjdXJyZW50IHN1YnJvdXRpbmUgY2FsbFxuICB3YXJuOiAxLFxuICAvLyAtIHByaW50IGRlYnVnZ2luZyBpbmZvXG4gIHdoZW46IDEsXG4gIC8vXG4gIHdyaXRlOiAxLFxuICAvLyAtIHByaW50IGEgcGljdHVyZSByZWNvcmRcbiAgeTogbnVsbFxufTsgLy8gLSB0cmFuc2xpdGVyYXRlIGEgc3RyaW5nXG5cbnZhciBSWHN0eWxlID0gXCJzdHJpbmcuc3BlY2lhbFwiO1xudmFyIFJYbW9kaWZpZXJzID0gL1tnb3NleGltYWNwbHVkXS87IC8vIE5PVEU6IFwibVwiLCBcInNcIiwgXCJ5XCIgYW5kIFwidHJcIiBuZWVkIHRvIGNvcnJlY3QgcmVhbCBtb2RpZmllcnMgZm9yIGVhY2ggcmVnZXhwIHR5cGVcblxuZnVuY3Rpb24gdG9rZW5DaGFpbihzdHJlYW0sIHN0YXRlLCBjaGFpbiwgc3R5bGUsIHRhaWwpIHtcbiAgLy8gTk9URTogY2hhaW4ubGVuZ3RoID4gMiBpcyBub3Qgd29ya2luZyBub3cgKGl0J3MgZm9yIHNbLi4uXVsuLi5dZ2VvczspXG4gIHN0YXRlLmNoYWluID0gbnVsbDsgLy8gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgMTIgICAzdGFpbFxuICBzdGF0ZS5zdHlsZSA9IG51bGw7XG4gIHN0YXRlLnRhaWwgPSBudWxsO1xuICBzdGF0ZS50b2tlbml6ZSA9IGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgdmFyIGUgPSBmYWxzZSxcbiAgICAgIGMsXG4gICAgICBpID0gMDtcbiAgICB3aGlsZSAoYyA9IHN0cmVhbS5uZXh0KCkpIHtcbiAgICAgIGlmIChjID09PSBjaGFpbltpXSAmJiAhZSkge1xuICAgICAgICBpZiAoY2hhaW5bKytpXSAhPT0gdW5kZWZpbmVkKSB7XG4gICAgICAgICAgc3RhdGUuY2hhaW4gPSBjaGFpbltpXTtcbiAgICAgICAgICBzdGF0ZS5zdHlsZSA9IHN0eWxlO1xuICAgICAgICAgIHN0YXRlLnRhaWwgPSB0YWlsO1xuICAgICAgICB9IGVsc2UgaWYgKHRhaWwpIHN0cmVhbS5lYXRXaGlsZSh0YWlsKTtcbiAgICAgICAgc3RhdGUudG9rZW5pemUgPSB0b2tlblBlcmw7XG4gICAgICAgIHJldHVybiBzdHlsZTtcbiAgICAgIH1cbiAgICAgIGUgPSAhZSAmJiBjID09IFwiXFxcXFwiO1xuICAgIH1cbiAgICByZXR1cm4gc3R5bGU7XG4gIH07XG4gIHJldHVybiBzdGF0ZS50b2tlbml6ZShzdHJlYW0sIHN0YXRlKTtcbn1cbmZ1bmN0aW9uIHRva2VuU09NRVRISU5HKHN0cmVhbSwgc3RhdGUsIHN0cmluZykge1xuICBzdGF0ZS50b2tlbml6ZSA9IGZ1bmN0aW9uIChzdHJlYW0sIHN0YXRlKSB7XG4gICAgaWYgKHN0cmVhbS5zdHJpbmcgPT0gc3RyaW5nKSBzdGF0ZS50b2tlbml6ZSA9IHRva2VuUGVybDtcbiAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgcmV0dXJuIFwic3RyaW5nXCI7XG4gIH07XG4gIHJldHVybiBzdGF0ZS50b2tlbml6ZShzdHJlYW0sIHN0YXRlKTtcbn1cbmZ1bmN0aW9uIHRva2VuUGVybChzdHJlYW0sIHN0YXRlKSB7XG4gIGlmIChzdHJlYW0uZWF0U3BhY2UoKSkgcmV0dXJuIG51bGw7XG4gIGlmIChzdGF0ZS5jaGFpbikgcmV0dXJuIHRva2VuQ2hhaW4oc3RyZWFtLCBzdGF0ZSwgc3RhdGUuY2hhaW4sIHN0YXRlLnN0eWxlLCBzdGF0ZS50YWlsKTtcbiAgaWYgKHN0cmVhbS5tYXRjaCgvXihcXC0/KChcXGRbXFxkX10qKT9cXC5cXGQrKGVbKy1dP1xcZCspP3xcXGQrXFwuXFxkKil8MHhbXFxkYS1mQS1GX10rfDBiWzAxX10rfFxcZFtcXGRfXSooZVsrLV0/XFxkKyk/KS8pKSByZXR1cm4gJ251bWJlcic7XG4gIGlmIChzdHJlYW0ubWF0Y2goL148PCg/PVtfYS16QS1aXSkvKSkge1xuICAgIC8vIE5PVEU6IDw8U09NRVRISU5HXFxuLi4uXFxuU09NRVRISU5HXFxuXG4gICAgc3RyZWFtLmVhdFdoaWxlKC9cXHcvKTtcbiAgICByZXR1cm4gdG9rZW5TT01FVEhJTkcoc3RyZWFtLCBzdGF0ZSwgc3RyZWFtLmN1cnJlbnQoKS5zdWJzdHIoMikpO1xuICB9XG4gIGlmIChzdHJlYW0uc29sKCkgJiYgc3RyZWFtLm1hdGNoKC9eXFw9aXRlbSg/IVxcdykvKSkge1xuICAgIC8vIE5PVEU6IFxcbj1pdGVtLi4uXFxuPWN1dFxcblxuICAgIHJldHVybiB0b2tlblNPTUVUSElORyhzdHJlYW0sIHN0YXRlLCAnPWN1dCcpO1xuICB9XG4gIHZhciBjaCA9IHN0cmVhbS5uZXh0KCk7XG4gIGlmIChjaCA9PSAnXCInIHx8IGNoID09IFwiJ1wiKSB7XG4gICAgLy8gTk9URTogJyBvciBcIiBvciA8PCdTT01FVEhJTkcnXFxuLi4uXFxuU09NRVRISU5HXFxuIG9yIDw8XCJTT01FVEhJTkdcIlxcbi4uLlxcblNPTUVUSElOR1xcblxuICAgIGlmIChwcmVmaXgoc3RyZWFtLCAzKSA9PSBcIjw8XCIgKyBjaCkge1xuICAgICAgdmFyIHAgPSBzdHJlYW0ucG9zO1xuICAgICAgc3RyZWFtLmVhdFdoaWxlKC9cXHcvKTtcbiAgICAgIHZhciBuID0gc3RyZWFtLmN1cnJlbnQoKS5zdWJzdHIoMSk7XG4gICAgICBpZiAobiAmJiBzdHJlYW0uZWF0KGNoKSkgcmV0dXJuIHRva2VuU09NRVRISU5HKHN0cmVhbSwgc3RhdGUsIG4pO1xuICAgICAgc3RyZWFtLnBvcyA9IHA7XG4gICAgfVxuICAgIHJldHVybiB0b2tlbkNoYWluKHN0cmVhbSwgc3RhdGUsIFtjaF0sIFwic3RyaW5nXCIpO1xuICB9XG4gIGlmIChjaCA9PSBcInFcIikge1xuICAgIHZhciBjID0gbG9vayhzdHJlYW0sIC0yKTtcbiAgICBpZiAoIShjICYmIC9cXHcvLnRlc3QoYykpKSB7XG4gICAgICBjID0gbG9vayhzdHJlYW0sIDApO1xuICAgICAgaWYgKGMgPT0gXCJ4XCIpIHtcbiAgICAgICAgYyA9IGxvb2soc3RyZWFtLCAxKTtcbiAgICAgICAgaWYgKGMgPT0gXCIoXCIpIHtcbiAgICAgICAgICBlYXRTdWZmaXgoc3RyZWFtLCAyKTtcbiAgICAgICAgICByZXR1cm4gdG9rZW5DaGFpbihzdHJlYW0sIHN0YXRlLCBbXCIpXCJdLCBSWHN0eWxlLCBSWG1vZGlmaWVycyk7XG4gICAgICAgIH1cbiAgICAgICAgaWYgKGMgPT0gXCJbXCIpIHtcbiAgICAgICAgICBlYXRTdWZmaXgoc3RyZWFtLCAyKTtcbiAgICAgICAgICByZXR1cm4gdG9rZW5DaGFpbihzdHJlYW0sIHN0YXRlLCBbXCJdXCJdLCBSWHN0eWxlLCBSWG1vZGlmaWVycyk7XG4gICAgICAgIH1cbiAgICAgICAgaWYgKGMgPT0gXCJ7XCIpIHtcbiAgICAgICAgICBlYXRTdWZmaXgoc3RyZWFtLCAyKTtcbiAgICAgICAgICByZXR1cm4gdG9rZW5DaGFpbihzdHJlYW0sIHN0YXRlLCBbXCJ9XCJdLCBSWHN0eWxlLCBSWG1vZGlmaWVycyk7XG4gICAgICAgIH1cbiAgICAgICAgaWYgKGMgPT0gXCI8XCIpIHtcbiAgICAgICAgICBlYXRTdWZmaXgoc3RyZWFtLCAyKTtcbiAgICAgICAgICByZXR1cm4gdG9rZW5DaGFpbihzdHJlYW0sIHN0YXRlLCBbXCI+XCJdLCBSWHN0eWxlLCBSWG1vZGlmaWVycyk7XG4gICAgICAgIH1cbiAgICAgICAgaWYgKC9bXFxeJ1wiIX5cXC9dLy50ZXN0KGMpKSB7XG4gICAgICAgICAgZWF0U3VmZml4KHN0cmVhbSwgMSk7XG4gICAgICAgICAgcmV0dXJuIHRva2VuQ2hhaW4oc3RyZWFtLCBzdGF0ZSwgW3N0cmVhbS5lYXQoYyldLCBSWHN0eWxlLCBSWG1vZGlmaWVycyk7XG4gICAgICAgIH1cbiAgICAgIH0gZWxzZSBpZiAoYyA9PSBcInFcIikge1xuICAgICAgICBjID0gbG9vayhzdHJlYW0sIDEpO1xuICAgICAgICBpZiAoYyA9PSBcIihcIikge1xuICAgICAgICAgIGVhdFN1ZmZpeChzdHJlYW0sIDIpO1xuICAgICAgICAgIHJldHVybiB0b2tlbkNoYWluKHN0cmVhbSwgc3RhdGUsIFtcIilcIl0sIFwic3RyaW5nXCIpO1xuICAgICAgICB9XG4gICAgICAgIGlmIChjID09IFwiW1wiKSB7XG4gICAgICAgICAgZWF0U3VmZml4KHN0cmVhbSwgMik7XG4gICAgICAgICAgcmV0dXJuIHRva2VuQ2hhaW4oc3RyZWFtLCBzdGF0ZSwgW1wiXVwiXSwgXCJzdHJpbmdcIik7XG4gICAgICAgIH1cbiAgICAgICAgaWYgKGMgPT0gXCJ7XCIpIHtcbiAgICAgICAgICBlYXRTdWZmaXgoc3RyZWFtLCAyKTtcbiAgICAgICAgICByZXR1cm4gdG9rZW5DaGFpbihzdHJlYW0sIHN0YXRlLCBbXCJ9XCJdLCBcInN0cmluZ1wiKTtcbiAgICAgICAgfVxuICAgICAgICBpZiAoYyA9PSBcIjxcIikge1xuICAgICAgICAgIGVhdFN1ZmZpeChzdHJlYW0sIDIpO1xuICAgICAgICAgIHJldHVybiB0b2tlbkNoYWluKHN0cmVhbSwgc3RhdGUsIFtcIj5cIl0sIFwic3RyaW5nXCIpO1xuICAgICAgICB9XG4gICAgICAgIGlmICgvW1xcXidcIiF+XFwvXS8udGVzdChjKSkge1xuICAgICAgICAgIGVhdFN1ZmZpeChzdHJlYW0sIDEpO1xuICAgICAgICAgIHJldHVybiB0b2tlbkNoYWluKHN0cmVhbSwgc3RhdGUsIFtzdHJlYW0uZWF0KGMpXSwgXCJzdHJpbmdcIik7XG4gICAgICAgIH1cbiAgICAgIH0gZWxzZSBpZiAoYyA9PSBcIndcIikge1xuICAgICAgICBjID0gbG9vayhzdHJlYW0sIDEpO1xuICAgICAgICBpZiAoYyA9PSBcIihcIikge1xuICAgICAgICAgIGVhdFN1ZmZpeChzdHJlYW0sIDIpO1xuICAgICAgICAgIHJldHVybiB0b2tlbkNoYWluKHN0cmVhbSwgc3RhdGUsIFtcIilcIl0sIFwiYnJhY2tldFwiKTtcbiAgICAgICAgfVxuICAgICAgICBpZiAoYyA9PSBcIltcIikge1xuICAgICAgICAgIGVhdFN1ZmZpeChzdHJlYW0sIDIpO1xuICAgICAgICAgIHJldHVybiB0b2tlbkNoYWluKHN0cmVhbSwgc3RhdGUsIFtcIl1cIl0sIFwiYnJhY2tldFwiKTtcbiAgICAgICAgfVxuICAgICAgICBpZiAoYyA9PSBcIntcIikge1xuICAgICAgICAgIGVhdFN1ZmZpeChzdHJlYW0sIDIpO1xuICAgICAgICAgIHJldHVybiB0b2tlbkNoYWluKHN0cmVhbSwgc3RhdGUsIFtcIn1cIl0sIFwiYnJhY2tldFwiKTtcbiAgICAgICAgfVxuICAgICAgICBpZiAoYyA9PSBcIjxcIikge1xuICAgICAgICAgIGVhdFN1ZmZpeChzdHJlYW0sIDIpO1xuICAgICAgICAgIHJldHVybiB0b2tlbkNoYWluKHN0cmVhbSwgc3RhdGUsIFtcIj5cIl0sIFwiYnJhY2tldFwiKTtcbiAgICAgICAgfVxuICAgICAgICBpZiAoL1tcXF4nXCIhflxcL10vLnRlc3QoYykpIHtcbiAgICAgICAgICBlYXRTdWZmaXgoc3RyZWFtLCAxKTtcbiAgICAgICAgICByZXR1cm4gdG9rZW5DaGFpbihzdHJlYW0sIHN0YXRlLCBbc3RyZWFtLmVhdChjKV0sIFwiYnJhY2tldFwiKTtcbiAgICAgICAgfVxuICAgICAgfSBlbHNlIGlmIChjID09IFwiclwiKSB7XG4gICAgICAgIGMgPSBsb29rKHN0cmVhbSwgMSk7XG4gICAgICAgIGlmIChjID09IFwiKFwiKSB7XG4gICAgICAgICAgZWF0U3VmZml4KHN0cmVhbSwgMik7XG4gICAgICAgICAgcmV0dXJuIHRva2VuQ2hhaW4oc3RyZWFtLCBzdGF0ZSwgW1wiKVwiXSwgUlhzdHlsZSwgUlhtb2RpZmllcnMpO1xuICAgICAgICB9XG4gICAgICAgIGlmIChjID09IFwiW1wiKSB7XG4gICAgICAgICAgZWF0U3VmZml4KHN0cmVhbSwgMik7XG4gICAgICAgICAgcmV0dXJuIHRva2VuQ2hhaW4oc3RyZWFtLCBzdGF0ZSwgW1wiXVwiXSwgUlhzdHlsZSwgUlhtb2RpZmllcnMpO1xuICAgICAgICB9XG4gICAgICAgIGlmIChjID09IFwie1wiKSB7XG4gICAgICAgICAgZWF0U3VmZml4KHN0cmVhbSwgMik7XG4gICAgICAgICAgcmV0dXJuIHRva2VuQ2hhaW4oc3RyZWFtLCBzdGF0ZSwgW1wifVwiXSwgUlhzdHlsZSwgUlhtb2RpZmllcnMpO1xuICAgICAgICB9XG4gICAgICAgIGlmIChjID09IFwiPFwiKSB7XG4gICAgICAgICAgZWF0U3VmZml4KHN0cmVhbSwgMik7XG4gICAgICAgICAgcmV0dXJuIHRva2VuQ2hhaW4oc3RyZWFtLCBzdGF0ZSwgW1wiPlwiXSwgUlhzdHlsZSwgUlhtb2RpZmllcnMpO1xuICAgICAgICB9XG4gICAgICAgIGlmICgvW1xcXidcIiF+XFwvXS8udGVzdChjKSkge1xuICAgICAgICAgIGVhdFN1ZmZpeChzdHJlYW0sIDEpO1xuICAgICAgICAgIHJldHVybiB0b2tlbkNoYWluKHN0cmVhbSwgc3RhdGUsIFtzdHJlYW0uZWF0KGMpXSwgUlhzdHlsZSwgUlhtb2RpZmllcnMpO1xuICAgICAgICB9XG4gICAgICB9IGVsc2UgaWYgKC9bXFxeJ1wiIX5cXC8oXFxbezxdLy50ZXN0KGMpKSB7XG4gICAgICAgIGlmIChjID09IFwiKFwiKSB7XG4gICAgICAgICAgZWF0U3VmZml4KHN0cmVhbSwgMSk7XG4gICAgICAgICAgcmV0dXJuIHRva2VuQ2hhaW4oc3RyZWFtLCBzdGF0ZSwgW1wiKVwiXSwgXCJzdHJpbmdcIik7XG4gICAgICAgIH1cbiAgICAgICAgaWYgKGMgPT0gXCJbXCIpIHtcbiAgICAgICAgICBlYXRTdWZmaXgoc3RyZWFtLCAxKTtcbiAgICAgICAgICByZXR1cm4gdG9rZW5DaGFpbihzdHJlYW0sIHN0YXRlLCBbXCJdXCJdLCBcInN0cmluZ1wiKTtcbiAgICAgICAgfVxuICAgICAgICBpZiAoYyA9PSBcIntcIikge1xuICAgICAgICAgIGVhdFN1ZmZpeChzdHJlYW0sIDEpO1xuICAgICAgICAgIHJldHVybiB0b2tlbkNoYWluKHN0cmVhbSwgc3RhdGUsIFtcIn1cIl0sIFwic3RyaW5nXCIpO1xuICAgICAgICB9XG4gICAgICAgIGlmIChjID09IFwiPFwiKSB7XG4gICAgICAgICAgZWF0U3VmZml4KHN0cmVhbSwgMSk7XG4gICAgICAgICAgcmV0dXJuIHRva2VuQ2hhaW4oc3RyZWFtLCBzdGF0ZSwgW1wiPlwiXSwgXCJzdHJpbmdcIik7XG4gICAgICAgIH1cbiAgICAgICAgaWYgKC9bXFxeJ1wiIX5cXC9dLy50ZXN0KGMpKSB7XG4gICAgICAgICAgcmV0dXJuIHRva2VuQ2hhaW4oc3RyZWFtLCBzdGF0ZSwgW3N0cmVhbS5lYXQoYyldLCBcInN0cmluZ1wiKTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH1cbiAgfVxuICBpZiAoY2ggPT0gXCJtXCIpIHtcbiAgICB2YXIgYyA9IGxvb2soc3RyZWFtLCAtMik7XG4gICAgaWYgKCEoYyAmJiAvXFx3Ly50ZXN0KGMpKSkge1xuICAgICAgYyA9IHN0cmVhbS5lYXQoL1soXFxbezxcXF4nXCIhflxcL10vKTtcbiAgICAgIGlmIChjKSB7XG4gICAgICAgIGlmICgvW1xcXidcIiF+XFwvXS8udGVzdChjKSkge1xuICAgICAgICAgIHJldHVybiB0b2tlbkNoYWluKHN0cmVhbSwgc3RhdGUsIFtjXSwgUlhzdHlsZSwgUlhtb2RpZmllcnMpO1xuICAgICAgICB9XG4gICAgICAgIGlmIChjID09IFwiKFwiKSB7XG4gICAgICAgICAgcmV0dXJuIHRva2VuQ2hhaW4oc3RyZWFtLCBzdGF0ZSwgW1wiKVwiXSwgUlhzdHlsZSwgUlhtb2RpZmllcnMpO1xuICAgICAgICB9XG4gICAgICAgIGlmIChjID09IFwiW1wiKSB7XG4gICAgICAgICAgcmV0dXJuIHRva2VuQ2hhaW4oc3RyZWFtLCBzdGF0ZSwgW1wiXVwiXSwgUlhzdHlsZSwgUlhtb2RpZmllcnMpO1xuICAgICAgICB9XG4gICAgICAgIGlmIChjID09IFwie1wiKSB7XG4gICAgICAgICAgcmV0dXJuIHRva2VuQ2hhaW4oc3RyZWFtLCBzdGF0ZSwgW1wifVwiXSwgUlhzdHlsZSwgUlhtb2RpZmllcnMpO1xuICAgICAgICB9XG4gICAgICAgIGlmIChjID09IFwiPFwiKSB7XG4gICAgICAgICAgcmV0dXJuIHRva2VuQ2hhaW4oc3RyZWFtLCBzdGF0ZSwgW1wiPlwiXSwgUlhzdHlsZSwgUlhtb2RpZmllcnMpO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfVxuICB9XG4gIGlmIChjaCA9PSBcInNcIikge1xuICAgIHZhciBjID0gL1tcXC8+XFxdfSlcXHddLy50ZXN0KGxvb2soc3RyZWFtLCAtMikpO1xuICAgIGlmICghYykge1xuICAgICAgYyA9IHN0cmVhbS5lYXQoL1soXFxbezxcXF4nXCIhflxcL10vKTtcbiAgICAgIGlmIChjKSB7XG4gICAgICAgIGlmIChjID09IFwiW1wiKSByZXR1cm4gdG9rZW5DaGFpbihzdHJlYW0sIHN0YXRlLCBbXCJdXCIsIFwiXVwiXSwgUlhzdHlsZSwgUlhtb2RpZmllcnMpO1xuICAgICAgICBpZiAoYyA9PSBcIntcIikgcmV0dXJuIHRva2VuQ2hhaW4oc3RyZWFtLCBzdGF0ZSwgW1wifVwiLCBcIn1cIl0sIFJYc3R5bGUsIFJYbW9kaWZpZXJzKTtcbiAgICAgICAgaWYgKGMgPT0gXCI8XCIpIHJldHVybiB0b2tlbkNoYWluKHN0cmVhbSwgc3RhdGUsIFtcIj5cIiwgXCI+XCJdLCBSWHN0eWxlLCBSWG1vZGlmaWVycyk7XG4gICAgICAgIGlmIChjID09IFwiKFwiKSByZXR1cm4gdG9rZW5DaGFpbihzdHJlYW0sIHN0YXRlLCBbXCIpXCIsIFwiKVwiXSwgUlhzdHlsZSwgUlhtb2RpZmllcnMpO1xuICAgICAgICByZXR1cm4gdG9rZW5DaGFpbihzdHJlYW0sIHN0YXRlLCBbYywgY10sIFJYc3R5bGUsIFJYbW9kaWZpZXJzKTtcbiAgICAgIH1cbiAgICB9XG4gIH1cbiAgaWYgKGNoID09IFwieVwiKSB7XG4gICAgdmFyIGMgPSAvW1xcLz5cXF19KVxcd10vLnRlc3QobG9vayhzdHJlYW0sIC0yKSk7XG4gICAgaWYgKCFjKSB7XG4gICAgICBjID0gc3RyZWFtLmVhdCgvWyhcXFt7PFxcXidcIiF+XFwvXS8pO1xuICAgICAgaWYgKGMpIHtcbiAgICAgICAgaWYgKGMgPT0gXCJbXCIpIHJldHVybiB0b2tlbkNoYWluKHN0cmVhbSwgc3RhdGUsIFtcIl1cIiwgXCJdXCJdLCBSWHN0eWxlLCBSWG1vZGlmaWVycyk7XG4gICAgICAgIGlmIChjID09IFwie1wiKSByZXR1cm4gdG9rZW5DaGFpbihzdHJlYW0sIHN0YXRlLCBbXCJ9XCIsIFwifVwiXSwgUlhzdHlsZSwgUlhtb2RpZmllcnMpO1xuICAgICAgICBpZiAoYyA9PSBcIjxcIikgcmV0dXJuIHRva2VuQ2hhaW4oc3RyZWFtLCBzdGF0ZSwgW1wiPlwiLCBcIj5cIl0sIFJYc3R5bGUsIFJYbW9kaWZpZXJzKTtcbiAgICAgICAgaWYgKGMgPT0gXCIoXCIpIHJldHVybiB0b2tlbkNoYWluKHN0cmVhbSwgc3RhdGUsIFtcIilcIiwgXCIpXCJdLCBSWHN0eWxlLCBSWG1vZGlmaWVycyk7XG4gICAgICAgIHJldHVybiB0b2tlbkNoYWluKHN0cmVhbSwgc3RhdGUsIFtjLCBjXSwgUlhzdHlsZSwgUlhtb2RpZmllcnMpO1xuICAgICAgfVxuICAgIH1cbiAgfVxuICBpZiAoY2ggPT0gXCJ0XCIpIHtcbiAgICB2YXIgYyA9IC9bXFwvPlxcXX0pXFx3XS8udGVzdChsb29rKHN0cmVhbSwgLTIpKTtcbiAgICBpZiAoIWMpIHtcbiAgICAgIGMgPSBzdHJlYW0uZWF0KFwiclwiKTtcbiAgICAgIGlmIChjKSB7XG4gICAgICAgIGMgPSBzdHJlYW0uZWF0KC9bKFxcW3s8XFxeJ1wiIX5cXC9dLyk7XG4gICAgICAgIGlmIChjKSB7XG4gICAgICAgICAgaWYgKGMgPT0gXCJbXCIpIHJldHVybiB0b2tlbkNoYWluKHN0cmVhbSwgc3RhdGUsIFtcIl1cIiwgXCJdXCJdLCBSWHN0eWxlLCBSWG1vZGlmaWVycyk7XG4gICAgICAgICAgaWYgKGMgPT0gXCJ7XCIpIHJldHVybiB0b2tlbkNoYWluKHN0cmVhbSwgc3RhdGUsIFtcIn1cIiwgXCJ9XCJdLCBSWHN0eWxlLCBSWG1vZGlmaWVycyk7XG4gICAgICAgICAgaWYgKGMgPT0gXCI8XCIpIHJldHVybiB0b2tlbkNoYWluKHN0cmVhbSwgc3RhdGUsIFtcIj5cIiwgXCI+XCJdLCBSWHN0eWxlLCBSWG1vZGlmaWVycyk7XG4gICAgICAgICAgaWYgKGMgPT0gXCIoXCIpIHJldHVybiB0b2tlbkNoYWluKHN0cmVhbSwgc3RhdGUsIFtcIilcIiwgXCIpXCJdLCBSWHN0eWxlLCBSWG1vZGlmaWVycyk7XG4gICAgICAgICAgcmV0dXJuIHRva2VuQ2hhaW4oc3RyZWFtLCBzdGF0ZSwgW2MsIGNdLCBSWHN0eWxlLCBSWG1vZGlmaWVycyk7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9XG4gIH1cbiAgaWYgKGNoID09IFwiYFwiKSB7XG4gICAgcmV0dXJuIHRva2VuQ2hhaW4oc3RyZWFtLCBzdGF0ZSwgW2NoXSwgXCJidWlsdGluXCIpO1xuICB9XG4gIGlmIChjaCA9PSBcIi9cIikge1xuICAgIGlmICghL35cXHMqJC8udGVzdChwcmVmaXgoc3RyZWFtKSkpIHJldHVybiBcIm9wZXJhdG9yXCI7ZWxzZSByZXR1cm4gdG9rZW5DaGFpbihzdHJlYW0sIHN0YXRlLCBbY2hdLCBSWHN0eWxlLCBSWG1vZGlmaWVycyk7XG4gIH1cbiAgaWYgKGNoID09IFwiJFwiKSB7XG4gICAgdmFyIHAgPSBzdHJlYW0ucG9zO1xuICAgIGlmIChzdHJlYW0uZWF0V2hpbGUoL1xcZC8pIHx8IHN0cmVhbS5lYXQoXCJ7XCIpICYmIHN0cmVhbS5lYXRXaGlsZSgvXFxkLykgJiYgc3RyZWFtLmVhdChcIn1cIikpIHJldHVybiBcImJ1aWx0aW5cIjtlbHNlIHN0cmVhbS5wb3MgPSBwO1xuICB9XG4gIGlmICgvWyRAJV0vLnRlc3QoY2gpKSB7XG4gICAgdmFyIHAgPSBzdHJlYW0ucG9zO1xuICAgIGlmIChzdHJlYW0uZWF0KFwiXlwiKSAmJiBzdHJlYW0uZWF0KC9bQS1aXS8pIHx8ICEvW0AkJSZdLy50ZXN0KGxvb2soc3RyZWFtLCAtMikpICYmIHN0cmVhbS5lYXQoL1s9fFxcXFxcXC0jP0A7OiZgflxcXiFcXFtcXF0qJ1wiJCsuLFxcLzw+KCldLykpIHtcbiAgICAgIHZhciBjID0gc3RyZWFtLmN1cnJlbnQoKTtcbiAgICAgIGlmIChQRVJMW2NdKSByZXR1cm4gXCJidWlsdGluXCI7XG4gICAgfVxuICAgIHN0cmVhbS5wb3MgPSBwO1xuICB9XG4gIGlmICgvWyRAJSZdLy50ZXN0KGNoKSkge1xuICAgIGlmIChzdHJlYW0uZWF0V2hpbGUoL1tcXHckXS8pIHx8IHN0cmVhbS5lYXQoXCJ7XCIpICYmIHN0cmVhbS5lYXRXaGlsZSgvW1xcdyRdLykgJiYgc3RyZWFtLmVhdChcIn1cIikpIHtcbiAgICAgIHZhciBjID0gc3RyZWFtLmN1cnJlbnQoKTtcbiAgICAgIGlmIChQRVJMW2NdKSByZXR1cm4gXCJidWlsdGluXCI7ZWxzZSByZXR1cm4gXCJ2YXJpYWJsZVwiO1xuICAgIH1cbiAgfVxuICBpZiAoY2ggPT0gXCIjXCIpIHtcbiAgICBpZiAobG9vayhzdHJlYW0sIC0yKSAhPSBcIiRcIikge1xuICAgICAgc3RyZWFtLnNraXBUb0VuZCgpO1xuICAgICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICAgIH1cbiAgfVxuICBpZiAoL1s6K1xcLVxcXiokJiVAPTw+IT98XFwvflxcLl0vLnRlc3QoY2gpKSB7XG4gICAgdmFyIHAgPSBzdHJlYW0ucG9zO1xuICAgIHN0cmVhbS5lYXRXaGlsZSgvWzorXFwtXFxeKiQmJUA9PD4hP3xcXC9+XFwuXS8pO1xuICAgIGlmIChQRVJMW3N0cmVhbS5jdXJyZW50KCldKSByZXR1cm4gXCJvcGVyYXRvclwiO2Vsc2Ugc3RyZWFtLnBvcyA9IHA7XG4gIH1cbiAgaWYgKGNoID09IFwiX1wiKSB7XG4gICAgaWYgKHN0cmVhbS5wb3MgPT0gMSkge1xuICAgICAgaWYgKHN1ZmZpeChzdHJlYW0sIDYpID09IFwiX0VORF9fXCIpIHtcbiAgICAgICAgcmV0dXJuIHRva2VuQ2hhaW4oc3RyZWFtLCBzdGF0ZSwgWydcXDAnXSwgXCJjb21tZW50XCIpO1xuICAgICAgfSBlbHNlIGlmIChzdWZmaXgoc3RyZWFtLCA3KSA9PSBcIl9EQVRBX19cIikge1xuICAgICAgICByZXR1cm4gdG9rZW5DaGFpbihzdHJlYW0sIHN0YXRlLCBbJ1xcMCddLCBcImJ1aWx0aW5cIik7XG4gICAgICB9IGVsc2UgaWYgKHN1ZmZpeChzdHJlYW0sIDcpID09IFwiX0NfX1wiKSB7XG4gICAgICAgIHJldHVybiB0b2tlbkNoYWluKHN0cmVhbSwgc3RhdGUsIFsnXFwwJ10sIFwic3RyaW5nXCIpO1xuICAgICAgfVxuICAgIH1cbiAgfVxuICBpZiAoL1xcdy8udGVzdChjaCkpIHtcbiAgICB2YXIgcCA9IHN0cmVhbS5wb3M7XG4gICAgaWYgKGxvb2soc3RyZWFtLCAtMikgPT0gXCJ7XCIgJiYgKGxvb2soc3RyZWFtLCAwKSA9PSBcIn1cIiB8fCBzdHJlYW0uZWF0V2hpbGUoL1xcdy8pICYmIGxvb2soc3RyZWFtLCAwKSA9PSBcIn1cIikpIHJldHVybiBcInN0cmluZ1wiO2Vsc2Ugc3RyZWFtLnBvcyA9IHA7XG4gIH1cbiAgaWYgKC9bQS1aXS8udGVzdChjaCkpIHtcbiAgICB2YXIgbCA9IGxvb2soc3RyZWFtLCAtMik7XG4gICAgdmFyIHAgPSBzdHJlYW0ucG9zO1xuICAgIHN0cmVhbS5lYXRXaGlsZSgvW0EtWl9dLyk7XG4gICAgaWYgKC9bXFxkYS16XS8udGVzdChsb29rKHN0cmVhbSwgMCkpKSB7XG4gICAgICBzdHJlYW0ucG9zID0gcDtcbiAgICB9IGVsc2Uge1xuICAgICAgdmFyIGMgPSBQRVJMW3N0cmVhbS5jdXJyZW50KCldO1xuICAgICAgaWYgKCFjKSByZXR1cm4gXCJtZXRhXCI7XG4gICAgICBpZiAoY1sxXSkgYyA9IGNbMF07XG4gICAgICBpZiAobCAhPSBcIjpcIikge1xuICAgICAgICBpZiAoYyA9PSAxKSByZXR1cm4gXCJrZXl3b3JkXCI7ZWxzZSBpZiAoYyA9PSAyKSByZXR1cm4gXCJkZWZcIjtlbHNlIGlmIChjID09IDMpIHJldHVybiBcImF0b21cIjtlbHNlIGlmIChjID09IDQpIHJldHVybiBcIm9wZXJhdG9yXCI7ZWxzZSBpZiAoYyA9PSA1KSByZXR1cm4gXCJidWlsdGluXCI7ZWxzZSByZXR1cm4gXCJtZXRhXCI7XG4gICAgICB9IGVsc2UgcmV0dXJuIFwibWV0YVwiO1xuICAgIH1cbiAgfVxuICBpZiAoL1thLXpBLVpfXS8udGVzdChjaCkpIHtcbiAgICB2YXIgbCA9IGxvb2soc3RyZWFtLCAtMik7XG4gICAgc3RyZWFtLmVhdFdoaWxlKC9cXHcvKTtcbiAgICB2YXIgYyA9IFBFUkxbc3RyZWFtLmN1cnJlbnQoKV07XG4gICAgaWYgKCFjKSByZXR1cm4gXCJtZXRhXCI7XG4gICAgaWYgKGNbMV0pIGMgPSBjWzBdO1xuICAgIGlmIChsICE9IFwiOlwiKSB7XG4gICAgICBpZiAoYyA9PSAxKSByZXR1cm4gXCJrZXl3b3JkXCI7ZWxzZSBpZiAoYyA9PSAyKSByZXR1cm4gXCJkZWZcIjtlbHNlIGlmIChjID09IDMpIHJldHVybiBcImF0b21cIjtlbHNlIGlmIChjID09IDQpIHJldHVybiBcIm9wZXJhdG9yXCI7ZWxzZSBpZiAoYyA9PSA1KSByZXR1cm4gXCJidWlsdGluXCI7ZWxzZSByZXR1cm4gXCJtZXRhXCI7XG4gICAgfSBlbHNlIHJldHVybiBcIm1ldGFcIjtcbiAgfVxuICByZXR1cm4gbnVsbDtcbn1cbmV4cG9ydCBjb25zdCBwZXJsID0ge1xuICBuYW1lOiBcInBlcmxcIixcbiAgc3RhcnRTdGF0ZTogZnVuY3Rpb24gKCkge1xuICAgIHJldHVybiB7XG4gICAgICB0b2tlbml6ZTogdG9rZW5QZXJsLFxuICAgICAgY2hhaW46IG51bGwsXG4gICAgICBzdHlsZTogbnVsbCxcbiAgICAgIHRhaWw6IG51bGxcbiAgICB9O1xuICB9LFxuICB0b2tlbjogZnVuY3Rpb24gKHN0cmVhbSwgc3RhdGUpIHtcbiAgICByZXR1cm4gKHN0YXRlLnRva2VuaXplIHx8IHRva2VuUGVybCkoc3RyZWFtLCBzdGF0ZSk7XG4gIH0sXG4gIGxhbmd1YWdlRGF0YToge1xuICAgIGNvbW1lbnRUb2tlbnM6IHtcbiAgICAgIGxpbmU6IFwiI1wiXG4gICAgfSxcbiAgICB3b3JkQ2hhcnM6IFwiJFwiXG4gIH1cbn07Il0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9