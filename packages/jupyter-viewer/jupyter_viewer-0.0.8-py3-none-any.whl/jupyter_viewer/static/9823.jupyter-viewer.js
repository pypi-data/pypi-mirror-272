"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[9823],{

/***/ 19823:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "puppet": () => (/* binding */ puppet)
/* harmony export */ });
// Stores the words from the define method
var words = {};
// Taken, mostly, from the Puppet official variable standards regex
var variable_regex = /({)?([a-z][a-z0-9_]*)?((::[a-z][a-z0-9_]*)*::)?[a-zA-Z0-9_]+(})?/;

// Takes a string of words separated by spaces and adds them as
// keys with the value of the first argument 'style'
function define(style, string) {
  var split = string.split(' ');
  for (var i = 0; i < split.length; i++) {
    words[split[i]] = style;
  }
}

// Takes commonly known puppet types/words and classifies them to a style
define('keyword', 'class define site node include import inherits');
define('keyword', 'case if else in and elsif default or');
define('atom', 'false true running present absent file directory undef');
define('builtin', 'action augeas burst chain computer cron destination dport exec ' + 'file filebucket group host icmp iniface interface jump k5login limit log_level ' + 'log_prefix macauthorization mailalias maillist mcx mount nagios_command ' + 'nagios_contact nagios_contactgroup nagios_host nagios_hostdependency ' + 'nagios_hostescalation nagios_hostextinfo nagios_hostgroup nagios_service ' + 'nagios_servicedependency nagios_serviceescalation nagios_serviceextinfo ' + 'nagios_servicegroup nagios_timeperiod name notify outiface package proto reject ' + 'resources router schedule scheduled_task selboolean selmodule service source ' + 'sport ssh_authorized_key sshkey stage state table tidy todest toports tosource ' + 'user vlan yumrepo zfs zone zpool');

// After finding a start of a string ('|") this function attempts to find the end;
// If a variable is encountered along the way, we display it differently when it
// is encapsulated in a double-quoted string.
function tokenString(stream, state) {
  var current,
    prev,
    found_var = false;
  while (!stream.eol() && (current = stream.next()) != state.pending) {
    if (current === '$' && prev != '\\' && state.pending == '"') {
      found_var = true;
      break;
    }
    prev = current;
  }
  if (found_var) {
    stream.backUp(1);
  }
  if (current == state.pending) {
    state.continueString = false;
  } else {
    state.continueString = true;
  }
  return "string";
}

// Main function
function tokenize(stream, state) {
  // Matches one whole word
  var word = stream.match(/[\w]+/, false);
  // Matches attributes (i.e. ensure => present ; 'ensure' would be matched)
  var attribute = stream.match(/(\s+)?\w+\s+=>.*/, false);
  // Matches non-builtin resource declarations
  // (i.e. "apache::vhost {" or "mycustomclasss {" would be matched)
  var resource = stream.match(/(\s+)?[\w:_]+(\s+)?{/, false);
  // Matches virtual and exported resources (i.e. @@user { ; and the like)
  var special_resource = stream.match(/(\s+)?[@]{1,2}[\w:_]+(\s+)?{/, false);

  // Finally advance the stream
  var ch = stream.next();

  // Have we found a variable?
  if (ch === '$') {
    if (stream.match(variable_regex)) {
      // If so, and its in a string, assign it a different color
      return state.continueString ? 'variableName.special' : 'variable';
    }
    // Otherwise return an invalid variable
    return "error";
  }
  // Should we still be looking for the end of a string?
  if (state.continueString) {
    // If so, go through the loop again
    stream.backUp(1);
    return tokenString(stream, state);
  }
  // Are we in a definition (class, node, define)?
  if (state.inDefinition) {
    // If so, return def (i.e. for 'class myclass {' ; 'myclass' would be matched)
    if (stream.match(/(\s+)?[\w:_]+(\s+)?/)) {
      return 'def';
    }
    // Match the rest it the next time around
    stream.match(/\s+{/);
    state.inDefinition = false;
  }
  // Are we in an 'include' statement?
  if (state.inInclude) {
    // Match and return the included class
    stream.match(/(\s+)?\S+(\s+)?/);
    state.inInclude = false;
    return 'def';
  }
  // Do we just have a function on our hands?
  // In 'ensure_resource("myclass")', 'ensure_resource' is matched
  if (stream.match(/(\s+)?\w+\(/)) {
    stream.backUp(1);
    return 'def';
  }
  // Have we matched the prior attribute regex?
  if (attribute) {
    stream.match(/(\s+)?\w+/);
    return 'tag';
  }
  // Do we have Puppet specific words?
  if (word && words.hasOwnProperty(word)) {
    // Negates the initial next()
    stream.backUp(1);
    // rs move the stream
    stream.match(/[\w]+/);
    // We want to process these words differently
    // do to the importance they have in Puppet
    if (stream.match(/\s+\S+\s+{/, false)) {
      state.inDefinition = true;
    }
    if (word == 'include') {
      state.inInclude = true;
    }
    // Returns their value as state in the prior define methods
    return words[word];
  }
  // Is there a match on a reference?
  if (/(^|\s+)[A-Z][\w:_]+/.test(word)) {
    // Negate the next()
    stream.backUp(1);
    // Match the full reference
    stream.match(/(^|\s+)[A-Z][\w:_]+/);
    return 'def';
  }
  // Have we matched the prior resource regex?
  if (resource) {
    stream.match(/(\s+)?[\w:_]+/);
    return 'def';
  }
  // Have we matched the prior special_resource regex?
  if (special_resource) {
    stream.match(/(\s+)?[@]{1,2}/);
    return 'atom';
  }
  // Match all the comments. All of them.
  if (ch == "#") {
    stream.skipToEnd();
    return "comment";
  }
  // Have we found a string?
  if (ch == "'" || ch == '"') {
    // Store the type (single or double)
    state.pending = ch;
    // Perform the looping function to find the end
    return tokenString(stream, state);
  }
  // Match all the brackets
  if (ch == '{' || ch == '}') {
    return 'bracket';
  }
  // Match characters that we are going to assume
  // are trying to be regex
  if (ch == '/') {
    stream.match(/^[^\/]*\//);
    return 'string.special';
  }
  // Match all the numbers
  if (ch.match(/[0-9]/)) {
    stream.eatWhile(/[0-9]+/);
    return 'number';
  }
  // Match the '=' and '=>' operators
  if (ch == '=') {
    if (stream.peek() == '>') {
      stream.next();
    }
    return "operator";
  }
  // Keep advancing through all the rest
  stream.eatWhile(/[\w-]/);
  // Return a blank line for everything else
  return null;
}
// Start it all
const puppet = {
  name: "puppet",
  startState: function () {
    var state = {};
    state.inDefinition = false;
    state.inInclude = false;
    state.continueString = false;
    state.pending = false;
    return state;
  },
  token: function (stream, state) {
    // Strip the spaces, but regex will account for them eitherway
    if (stream.eatSpace()) return null;
    // Go through the main process
    return tokenize(stream, state);
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiOTgyMy5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9AY29kZW1pcnJvci9sZWdhY3ktbW9kZXMvbW9kZS9wdXBwZXQuanMiXSwic291cmNlc0NvbnRlbnQiOlsiLy8gU3RvcmVzIHRoZSB3b3JkcyBmcm9tIHRoZSBkZWZpbmUgbWV0aG9kXG52YXIgd29yZHMgPSB7fTtcbi8vIFRha2VuLCBtb3N0bHksIGZyb20gdGhlIFB1cHBldCBvZmZpY2lhbCB2YXJpYWJsZSBzdGFuZGFyZHMgcmVnZXhcbnZhciB2YXJpYWJsZV9yZWdleCA9IC8oeyk/KFthLXpdW2EtejAtOV9dKik/KCg6OlthLXpdW2EtejAtOV9dKikqOjopP1thLXpBLVowLTlfXSsofSk/LztcblxuLy8gVGFrZXMgYSBzdHJpbmcgb2Ygd29yZHMgc2VwYXJhdGVkIGJ5IHNwYWNlcyBhbmQgYWRkcyB0aGVtIGFzXG4vLyBrZXlzIHdpdGggdGhlIHZhbHVlIG9mIHRoZSBmaXJzdCBhcmd1bWVudCAnc3R5bGUnXG5mdW5jdGlvbiBkZWZpbmUoc3R5bGUsIHN0cmluZykge1xuICB2YXIgc3BsaXQgPSBzdHJpbmcuc3BsaXQoJyAnKTtcbiAgZm9yICh2YXIgaSA9IDA7IGkgPCBzcGxpdC5sZW5ndGg7IGkrKykge1xuICAgIHdvcmRzW3NwbGl0W2ldXSA9IHN0eWxlO1xuICB9XG59XG5cbi8vIFRha2VzIGNvbW1vbmx5IGtub3duIHB1cHBldCB0eXBlcy93b3JkcyBhbmQgY2xhc3NpZmllcyB0aGVtIHRvIGEgc3R5bGVcbmRlZmluZSgna2V5d29yZCcsICdjbGFzcyBkZWZpbmUgc2l0ZSBub2RlIGluY2x1ZGUgaW1wb3J0IGluaGVyaXRzJyk7XG5kZWZpbmUoJ2tleXdvcmQnLCAnY2FzZSBpZiBlbHNlIGluIGFuZCBlbHNpZiBkZWZhdWx0IG9yJyk7XG5kZWZpbmUoJ2F0b20nLCAnZmFsc2UgdHJ1ZSBydW5uaW5nIHByZXNlbnQgYWJzZW50IGZpbGUgZGlyZWN0b3J5IHVuZGVmJyk7XG5kZWZpbmUoJ2J1aWx0aW4nLCAnYWN0aW9uIGF1Z2VhcyBidXJzdCBjaGFpbiBjb21wdXRlciBjcm9uIGRlc3RpbmF0aW9uIGRwb3J0IGV4ZWMgJyArICdmaWxlIGZpbGVidWNrZXQgZ3JvdXAgaG9zdCBpY21wIGluaWZhY2UgaW50ZXJmYWNlIGp1bXAgazVsb2dpbiBsaW1pdCBsb2dfbGV2ZWwgJyArICdsb2dfcHJlZml4IG1hY2F1dGhvcml6YXRpb24gbWFpbGFsaWFzIG1haWxsaXN0IG1jeCBtb3VudCBuYWdpb3NfY29tbWFuZCAnICsgJ25hZ2lvc19jb250YWN0IG5hZ2lvc19jb250YWN0Z3JvdXAgbmFnaW9zX2hvc3QgbmFnaW9zX2hvc3RkZXBlbmRlbmN5ICcgKyAnbmFnaW9zX2hvc3Rlc2NhbGF0aW9uIG5hZ2lvc19ob3N0ZXh0aW5mbyBuYWdpb3NfaG9zdGdyb3VwIG5hZ2lvc19zZXJ2aWNlICcgKyAnbmFnaW9zX3NlcnZpY2VkZXBlbmRlbmN5IG5hZ2lvc19zZXJ2aWNlZXNjYWxhdGlvbiBuYWdpb3Nfc2VydmljZWV4dGluZm8gJyArICduYWdpb3Nfc2VydmljZWdyb3VwIG5hZ2lvc190aW1lcGVyaW9kIG5hbWUgbm90aWZ5IG91dGlmYWNlIHBhY2thZ2UgcHJvdG8gcmVqZWN0ICcgKyAncmVzb3VyY2VzIHJvdXRlciBzY2hlZHVsZSBzY2hlZHVsZWRfdGFzayBzZWxib29sZWFuIHNlbG1vZHVsZSBzZXJ2aWNlIHNvdXJjZSAnICsgJ3Nwb3J0IHNzaF9hdXRob3JpemVkX2tleSBzc2hrZXkgc3RhZ2Ugc3RhdGUgdGFibGUgdGlkeSB0b2Rlc3QgdG9wb3J0cyB0b3NvdXJjZSAnICsgJ3VzZXIgdmxhbiB5dW1yZXBvIHpmcyB6b25lIHpwb29sJyk7XG5cbi8vIEFmdGVyIGZpbmRpbmcgYSBzdGFydCBvZiBhIHN0cmluZyAoJ3xcIikgdGhpcyBmdW5jdGlvbiBhdHRlbXB0cyB0byBmaW5kIHRoZSBlbmQ7XG4vLyBJZiBhIHZhcmlhYmxlIGlzIGVuY291bnRlcmVkIGFsb25nIHRoZSB3YXksIHdlIGRpc3BsYXkgaXQgZGlmZmVyZW50bHkgd2hlbiBpdFxuLy8gaXMgZW5jYXBzdWxhdGVkIGluIGEgZG91YmxlLXF1b3RlZCBzdHJpbmcuXG5mdW5jdGlvbiB0b2tlblN0cmluZyhzdHJlYW0sIHN0YXRlKSB7XG4gIHZhciBjdXJyZW50LFxuICAgIHByZXYsXG4gICAgZm91bmRfdmFyID0gZmFsc2U7XG4gIHdoaWxlICghc3RyZWFtLmVvbCgpICYmIChjdXJyZW50ID0gc3RyZWFtLm5leHQoKSkgIT0gc3RhdGUucGVuZGluZykge1xuICAgIGlmIChjdXJyZW50ID09PSAnJCcgJiYgcHJldiAhPSAnXFxcXCcgJiYgc3RhdGUucGVuZGluZyA9PSAnXCInKSB7XG4gICAgICBmb3VuZF92YXIgPSB0cnVlO1xuICAgICAgYnJlYWs7XG4gICAgfVxuICAgIHByZXYgPSBjdXJyZW50O1xuICB9XG4gIGlmIChmb3VuZF92YXIpIHtcbiAgICBzdHJlYW0uYmFja1VwKDEpO1xuICB9XG4gIGlmIChjdXJyZW50ID09IHN0YXRlLnBlbmRpbmcpIHtcbiAgICBzdGF0ZS5jb250aW51ZVN0cmluZyA9IGZhbHNlO1xuICB9IGVsc2Uge1xuICAgIHN0YXRlLmNvbnRpbnVlU3RyaW5nID0gdHJ1ZTtcbiAgfVxuICByZXR1cm4gXCJzdHJpbmdcIjtcbn1cblxuLy8gTWFpbiBmdW5jdGlvblxuZnVuY3Rpb24gdG9rZW5pemUoc3RyZWFtLCBzdGF0ZSkge1xuICAvLyBNYXRjaGVzIG9uZSB3aG9sZSB3b3JkXG4gIHZhciB3b3JkID0gc3RyZWFtLm1hdGNoKC9bXFx3XSsvLCBmYWxzZSk7XG4gIC8vIE1hdGNoZXMgYXR0cmlidXRlcyAoaS5lLiBlbnN1cmUgPT4gcHJlc2VudCA7ICdlbnN1cmUnIHdvdWxkIGJlIG1hdGNoZWQpXG4gIHZhciBhdHRyaWJ1dGUgPSBzdHJlYW0ubWF0Y2goLyhcXHMrKT9cXHcrXFxzKz0+LiovLCBmYWxzZSk7XG4gIC8vIE1hdGNoZXMgbm9uLWJ1aWx0aW4gcmVzb3VyY2UgZGVjbGFyYXRpb25zXG4gIC8vIChpLmUuIFwiYXBhY2hlOjp2aG9zdCB7XCIgb3IgXCJteWN1c3RvbWNsYXNzcyB7XCIgd291bGQgYmUgbWF0Y2hlZClcbiAgdmFyIHJlc291cmNlID0gc3RyZWFtLm1hdGNoKC8oXFxzKyk/W1xcdzpfXSsoXFxzKyk/ey8sIGZhbHNlKTtcbiAgLy8gTWF0Y2hlcyB2aXJ0dWFsIGFuZCBleHBvcnRlZCByZXNvdXJjZXMgKGkuZS4gQEB1c2VyIHsgOyBhbmQgdGhlIGxpa2UpXG4gIHZhciBzcGVjaWFsX3Jlc291cmNlID0gc3RyZWFtLm1hdGNoKC8oXFxzKyk/W0BdezEsMn1bXFx3Ol9dKyhcXHMrKT97LywgZmFsc2UpO1xuXG4gIC8vIEZpbmFsbHkgYWR2YW5jZSB0aGUgc3RyZWFtXG4gIHZhciBjaCA9IHN0cmVhbS5uZXh0KCk7XG5cbiAgLy8gSGF2ZSB3ZSBmb3VuZCBhIHZhcmlhYmxlP1xuICBpZiAoY2ggPT09ICckJykge1xuICAgIGlmIChzdHJlYW0ubWF0Y2godmFyaWFibGVfcmVnZXgpKSB7XG4gICAgICAvLyBJZiBzbywgYW5kIGl0cyBpbiBhIHN0cmluZywgYXNzaWduIGl0IGEgZGlmZmVyZW50IGNvbG9yXG4gICAgICByZXR1cm4gc3RhdGUuY29udGludWVTdHJpbmcgPyAndmFyaWFibGVOYW1lLnNwZWNpYWwnIDogJ3ZhcmlhYmxlJztcbiAgICB9XG4gICAgLy8gT3RoZXJ3aXNlIHJldHVybiBhbiBpbnZhbGlkIHZhcmlhYmxlXG4gICAgcmV0dXJuIFwiZXJyb3JcIjtcbiAgfVxuICAvLyBTaG91bGQgd2Ugc3RpbGwgYmUgbG9va2luZyBmb3IgdGhlIGVuZCBvZiBhIHN0cmluZz9cbiAgaWYgKHN0YXRlLmNvbnRpbnVlU3RyaW5nKSB7XG4gICAgLy8gSWYgc28sIGdvIHRocm91Z2ggdGhlIGxvb3AgYWdhaW5cbiAgICBzdHJlYW0uYmFja1VwKDEpO1xuICAgIHJldHVybiB0b2tlblN0cmluZyhzdHJlYW0sIHN0YXRlKTtcbiAgfVxuICAvLyBBcmUgd2UgaW4gYSBkZWZpbml0aW9uIChjbGFzcywgbm9kZSwgZGVmaW5lKT9cbiAgaWYgKHN0YXRlLmluRGVmaW5pdGlvbikge1xuICAgIC8vIElmIHNvLCByZXR1cm4gZGVmIChpLmUuIGZvciAnY2xhc3MgbXljbGFzcyB7JyA7ICdteWNsYXNzJyB3b3VsZCBiZSBtYXRjaGVkKVxuICAgIGlmIChzdHJlYW0ubWF0Y2goLyhcXHMrKT9bXFx3Ol9dKyhcXHMrKT8vKSkge1xuICAgICAgcmV0dXJuICdkZWYnO1xuICAgIH1cbiAgICAvLyBNYXRjaCB0aGUgcmVzdCBpdCB0aGUgbmV4dCB0aW1lIGFyb3VuZFxuICAgIHN0cmVhbS5tYXRjaCgvXFxzK3svKTtcbiAgICBzdGF0ZS5pbkRlZmluaXRpb24gPSBmYWxzZTtcbiAgfVxuICAvLyBBcmUgd2UgaW4gYW4gJ2luY2x1ZGUnIHN0YXRlbWVudD9cbiAgaWYgKHN0YXRlLmluSW5jbHVkZSkge1xuICAgIC8vIE1hdGNoIGFuZCByZXR1cm4gdGhlIGluY2x1ZGVkIGNsYXNzXG4gICAgc3RyZWFtLm1hdGNoKC8oXFxzKyk/XFxTKyhcXHMrKT8vKTtcbiAgICBzdGF0ZS5pbkluY2x1ZGUgPSBmYWxzZTtcbiAgICByZXR1cm4gJ2RlZic7XG4gIH1cbiAgLy8gRG8gd2UganVzdCBoYXZlIGEgZnVuY3Rpb24gb24gb3VyIGhhbmRzP1xuICAvLyBJbiAnZW5zdXJlX3Jlc291cmNlKFwibXljbGFzc1wiKScsICdlbnN1cmVfcmVzb3VyY2UnIGlzIG1hdGNoZWRcbiAgaWYgKHN0cmVhbS5tYXRjaCgvKFxccyspP1xcdytcXCgvKSkge1xuICAgIHN0cmVhbS5iYWNrVXAoMSk7XG4gICAgcmV0dXJuICdkZWYnO1xuICB9XG4gIC8vIEhhdmUgd2UgbWF0Y2hlZCB0aGUgcHJpb3IgYXR0cmlidXRlIHJlZ2V4P1xuICBpZiAoYXR0cmlidXRlKSB7XG4gICAgc3RyZWFtLm1hdGNoKC8oXFxzKyk/XFx3Ky8pO1xuICAgIHJldHVybiAndGFnJztcbiAgfVxuICAvLyBEbyB3ZSBoYXZlIFB1cHBldCBzcGVjaWZpYyB3b3Jkcz9cbiAgaWYgKHdvcmQgJiYgd29yZHMuaGFzT3duUHJvcGVydHkod29yZCkpIHtcbiAgICAvLyBOZWdhdGVzIHRoZSBpbml0aWFsIG5leHQoKVxuICAgIHN0cmVhbS5iYWNrVXAoMSk7XG4gICAgLy8gcnMgbW92ZSB0aGUgc3RyZWFtXG4gICAgc3RyZWFtLm1hdGNoKC9bXFx3XSsvKTtcbiAgICAvLyBXZSB3YW50IHRvIHByb2Nlc3MgdGhlc2Ugd29yZHMgZGlmZmVyZW50bHlcbiAgICAvLyBkbyB0byB0aGUgaW1wb3J0YW5jZSB0aGV5IGhhdmUgaW4gUHVwcGV0XG4gICAgaWYgKHN0cmVhbS5tYXRjaCgvXFxzK1xcUytcXHMrey8sIGZhbHNlKSkge1xuICAgICAgc3RhdGUuaW5EZWZpbml0aW9uID0gdHJ1ZTtcbiAgICB9XG4gICAgaWYgKHdvcmQgPT0gJ2luY2x1ZGUnKSB7XG4gICAgICBzdGF0ZS5pbkluY2x1ZGUgPSB0cnVlO1xuICAgIH1cbiAgICAvLyBSZXR1cm5zIHRoZWlyIHZhbHVlIGFzIHN0YXRlIGluIHRoZSBwcmlvciBkZWZpbmUgbWV0aG9kc1xuICAgIHJldHVybiB3b3Jkc1t3b3JkXTtcbiAgfVxuICAvLyBJcyB0aGVyZSBhIG1hdGNoIG9uIGEgcmVmZXJlbmNlP1xuICBpZiAoLyhefFxccyspW0EtWl1bXFx3Ol9dKy8udGVzdCh3b3JkKSkge1xuICAgIC8vIE5lZ2F0ZSB0aGUgbmV4dCgpXG4gICAgc3RyZWFtLmJhY2tVcCgxKTtcbiAgICAvLyBNYXRjaCB0aGUgZnVsbCByZWZlcmVuY2VcbiAgICBzdHJlYW0ubWF0Y2goLyhefFxccyspW0EtWl1bXFx3Ol9dKy8pO1xuICAgIHJldHVybiAnZGVmJztcbiAgfVxuICAvLyBIYXZlIHdlIG1hdGNoZWQgdGhlIHByaW9yIHJlc291cmNlIHJlZ2V4P1xuICBpZiAocmVzb3VyY2UpIHtcbiAgICBzdHJlYW0ubWF0Y2goLyhcXHMrKT9bXFx3Ol9dKy8pO1xuICAgIHJldHVybiAnZGVmJztcbiAgfVxuICAvLyBIYXZlIHdlIG1hdGNoZWQgdGhlIHByaW9yIHNwZWNpYWxfcmVzb3VyY2UgcmVnZXg/XG4gIGlmIChzcGVjaWFsX3Jlc291cmNlKSB7XG4gICAgc3RyZWFtLm1hdGNoKC8oXFxzKyk/W0BdezEsMn0vKTtcbiAgICByZXR1cm4gJ2F0b20nO1xuICB9XG4gIC8vIE1hdGNoIGFsbCB0aGUgY29tbWVudHMuIEFsbCBvZiB0aGVtLlxuICBpZiAoY2ggPT0gXCIjXCIpIHtcbiAgICBzdHJlYW0uc2tpcFRvRW5kKCk7XG4gICAgcmV0dXJuIFwiY29tbWVudFwiO1xuICB9XG4gIC8vIEhhdmUgd2UgZm91bmQgYSBzdHJpbmc/XG4gIGlmIChjaCA9PSBcIidcIiB8fCBjaCA9PSAnXCInKSB7XG4gICAgLy8gU3RvcmUgdGhlIHR5cGUgKHNpbmdsZSBvciBkb3VibGUpXG4gICAgc3RhdGUucGVuZGluZyA9IGNoO1xuICAgIC8vIFBlcmZvcm0gdGhlIGxvb3BpbmcgZnVuY3Rpb24gdG8gZmluZCB0aGUgZW5kXG4gICAgcmV0dXJuIHRva2VuU3RyaW5nKHN0cmVhbSwgc3RhdGUpO1xuICB9XG4gIC8vIE1hdGNoIGFsbCB0aGUgYnJhY2tldHNcbiAgaWYgKGNoID09ICd7JyB8fCBjaCA9PSAnfScpIHtcbiAgICByZXR1cm4gJ2JyYWNrZXQnO1xuICB9XG4gIC8vIE1hdGNoIGNoYXJhY3RlcnMgdGhhdCB3ZSBhcmUgZ29pbmcgdG8gYXNzdW1lXG4gIC8vIGFyZSB0cnlpbmcgdG8gYmUgcmVnZXhcbiAgaWYgKGNoID09ICcvJykge1xuICAgIHN0cmVhbS5tYXRjaCgvXlteXFwvXSpcXC8vKTtcbiAgICByZXR1cm4gJ3N0cmluZy5zcGVjaWFsJztcbiAgfVxuICAvLyBNYXRjaCBhbGwgdGhlIG51bWJlcnNcbiAgaWYgKGNoLm1hdGNoKC9bMC05XS8pKSB7XG4gICAgc3RyZWFtLmVhdFdoaWxlKC9bMC05XSsvKTtcbiAgICByZXR1cm4gJ251bWJlcic7XG4gIH1cbiAgLy8gTWF0Y2ggdGhlICc9JyBhbmQgJz0+JyBvcGVyYXRvcnNcbiAgaWYgKGNoID09ICc9Jykge1xuICAgIGlmIChzdHJlYW0ucGVlaygpID09ICc+Jykge1xuICAgICAgc3RyZWFtLm5leHQoKTtcbiAgICB9XG4gICAgcmV0dXJuIFwib3BlcmF0b3JcIjtcbiAgfVxuICAvLyBLZWVwIGFkdmFuY2luZyB0aHJvdWdoIGFsbCB0aGUgcmVzdFxuICBzdHJlYW0uZWF0V2hpbGUoL1tcXHctXS8pO1xuICAvLyBSZXR1cm4gYSBibGFuayBsaW5lIGZvciBldmVyeXRoaW5nIGVsc2VcbiAgcmV0dXJuIG51bGw7XG59XG4vLyBTdGFydCBpdCBhbGxcbmV4cG9ydCBjb25zdCBwdXBwZXQgPSB7XG4gIG5hbWU6IFwicHVwcGV0XCIsXG4gIHN0YXJ0U3RhdGU6IGZ1bmN0aW9uICgpIHtcbiAgICB2YXIgc3RhdGUgPSB7fTtcbiAgICBzdGF0ZS5pbkRlZmluaXRpb24gPSBmYWxzZTtcbiAgICBzdGF0ZS5pbkluY2x1ZGUgPSBmYWxzZTtcbiAgICBzdGF0ZS5jb250aW51ZVN0cmluZyA9IGZhbHNlO1xuICAgIHN0YXRlLnBlbmRpbmcgPSBmYWxzZTtcbiAgICByZXR1cm4gc3RhdGU7XG4gIH0sXG4gIHRva2VuOiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIC8vIFN0cmlwIHRoZSBzcGFjZXMsIGJ1dCByZWdleCB3aWxsIGFjY291bnQgZm9yIHRoZW0gZWl0aGVyd2F5XG4gICAgaWYgKHN0cmVhbS5lYXRTcGFjZSgpKSByZXR1cm4gbnVsbDtcbiAgICAvLyBHbyB0aHJvdWdoIHRoZSBtYWluIHByb2Nlc3NcbiAgICByZXR1cm4gdG9rZW5pemUoc3RyZWFtLCBzdGF0ZSk7XG4gIH1cbn07Il0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9