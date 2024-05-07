"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[9042],{

/***/ 69042:
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "mirc": () => (/* binding */ mirc)
/* harmony export */ });
function parseWords(str) {
  var obj = {},
    words = str.split(" ");
  for (var i = 0; i < words.length; ++i) obj[words[i]] = true;
  return obj;
}
var specials = parseWords("$! $$ $& $? $+ $abook $abs $active $activecid " + "$activewid $address $addtok $agent $agentname $agentstat $agentver " + "$alias $and $anick $ansi2mirc $aop $appactive $appstate $asc $asctime " + "$asin $atan $avoice $away $awaymsg $awaytime $banmask $base $bfind " + "$binoff $biton $bnick $bvar $bytes $calc $cb $cd $ceil $chan $chanmodes " + "$chantypes $chat $chr $cid $clevel $click $cmdbox $cmdline $cnick $color " + "$com $comcall $comchan $comerr $compact $compress $comval $cos $count " + "$cr $crc $creq $crlf $ctime $ctimer $ctrlenter $date $day $daylight " + "$dbuh $dbuw $dccignore $dccport $dde $ddename $debug $decode $decompress " + "$deltok $devent $dialog $did $didreg $didtok $didwm $disk $dlevel $dll " + "$dllcall $dname $dns $duration $ebeeps $editbox $emailaddr $encode $error " + "$eval $event $exist $feof $ferr $fgetc $file $filename $filtered $finddir " + "$finddirn $findfile $findfilen $findtok $fline $floor $fopen $fread $fserve " + "$fulladdress $fulldate $fullname $fullscreen $get $getdir $getdot $gettok $gmt " + "$group $halted $hash $height $hfind $hget $highlight $hnick $hotline " + "$hotlinepos $ial $ialchan $ibl $idle $iel $ifmatch $ignore $iif $iil " + "$inelipse $ini $inmidi $inpaste $inpoly $input $inrect $inroundrect " + "$insong $instok $int $inwave $ip $isalias $isbit $isdde $isdir $isfile " + "$isid $islower $istok $isupper $keychar $keyrpt $keyval $knick $lactive " + "$lactivecid $lactivewid $left $len $level $lf $line $lines $link $lock " + "$lock $locked $log $logstamp $logstampfmt $longfn $longip $lower $ltimer " + "$maddress $mask $matchkey $matchtok $md5 $me $menu $menubar $menucontext " + "$menutype $mid $middir $mircdir $mircexe $mircini $mklogfn $mnick $mode " + "$modefirst $modelast $modespl $mouse $msfile $network $newnick $nick $nofile " + "$nopath $noqt $not $notags $notify $null $numeric $numok $oline $onpoly " + "$opnick $or $ord $os $passivedcc $pic $play $pnick $port $portable $portfree " + "$pos $prefix $prop $protect $puttok $qt $query $rand $r $rawmsg $read $readomo " + "$readn $regex $regml $regsub $regsubex $remove $remtok $replace $replacex " + "$reptok $result $rgb $right $round $scid $scon $script $scriptdir $scriptline " + "$sdir $send $server $serverip $sfile $sha1 $shortfn $show $signal $sin " + "$site $sline $snick $snicks $snotify $sock $sockbr $sockerr $sockname " + "$sorttok $sound $sqrt $ssl $sreq $sslready $status $strip $str $stripped " + "$syle $submenu $switchbar $tan $target $ticks $time $timer $timestamp " + "$timestampfmt $timezone $tip $titlebar $toolbar $treebar $trust $ulevel " + "$ulist $upper $uptime $url $usermode $v1 $v2 $var $vcmd $vcmdstat $vcmdver " + "$version $vnick $vol $wid $width $wildsite $wildtok $window $wrap $xor");
var keywords = parseWords("abook ajinvite alias aline ame amsg anick aop auser autojoin avoice " + "away background ban bcopy beep bread break breplace bset btrunc bunset bwrite " + "channel clear clearall cline clipboard close cnick color comclose comopen " + "comreg continue copy creq ctcpreply ctcps dcc dccserver dde ddeserver " + "debug dec describe dialog did didtok disable disconnect dlevel dline dll " + "dns dqwindow drawcopy drawdot drawfill drawline drawpic drawrect drawreplace " + "drawrot drawsave drawscroll drawtext ebeeps echo editbox emailaddr enable " + "events exit fclose filter findtext finger firewall flash flist flood flush " + "flushini font fopen fseek fsend fserve fullname fwrite ghide gload gmove " + "gopts goto gplay gpoint gqreq groups gshow gsize gstop gtalk gunload hadd " + "halt haltdef hdec hdel help hfree hinc hload hmake hop hsave ial ialclear " + "ialmark identd if ignore iline inc invite iuser join kick linesep links list " + "load loadbuf localinfo log mdi me menubar mkdir mnick mode msg nick noop notice " + "notify omsg onotice part partall pdcc perform play playctrl pop protect pvoice " + "qme qmsg query queryn quit raw reload remini remote remove rename renwin " + "reseterror resetidle return rlevel rline rmdir run ruser save savebuf saveini " + "say scid scon server set showmirc signam sline sockaccept sockclose socklist " + "socklisten sockmark sockopen sockpause sockread sockrename sockudp sockwrite " + "sound speak splay sreq strip switchbar timer timestamp titlebar tnick tokenize " + "toolbar topic tray treebar ulist unload unset unsetall updatenl url uwho " + "var vcadd vcmd vcrem vol while whois window winhelp write writeint if isalnum " + "isalpha isaop isavoice isban ischan ishop isignore isin isincs isletter islower " + "isnotify isnum ison isop isprotect isreg isupper isvoice iswm iswmcs " + "elseif else goto menu nicklist status title icon size option text edit " + "button check radio box scroll list combo link tab item");
var functions = parseWords("if elseif else and not or eq ne in ni for foreach while switch");
var isOperatorChar = /[+\-*&%=<>!?^\/\|]/;
function chain(stream, state, f) {
  state.tokenize = f;
  return f(stream, state);
}
function tokenBase(stream, state) {
  var beforeParams = state.beforeParams;
  state.beforeParams = false;
  var ch = stream.next();
  if (/[\[\]{}\(\),\.]/.test(ch)) {
    if (ch == "(" && beforeParams) state.inParams = true;else if (ch == ")") state.inParams = false;
    return null;
  } else if (/\d/.test(ch)) {
    stream.eatWhile(/[\w\.]/);
    return "number";
  } else if (ch == "\\") {
    stream.eat("\\");
    stream.eat(/./);
    return "number";
  } else if (ch == "/" && stream.eat("*")) {
    return chain(stream, state, tokenComment);
  } else if (ch == ";" && stream.match(/ *\( *\(/)) {
    return chain(stream, state, tokenUnparsed);
  } else if (ch == ";" && !state.inParams) {
    stream.skipToEnd();
    return "comment";
  } else if (ch == '"') {
    stream.eat(/"/);
    return "keyword";
  } else if (ch == "$") {
    stream.eatWhile(/[$_a-z0-9A-Z\.:]/);
    if (specials && specials.propertyIsEnumerable(stream.current().toLowerCase())) {
      return "keyword";
    } else {
      state.beforeParams = true;
      return "builtin";
    }
  } else if (ch == "%") {
    stream.eatWhile(/[^,\s()]/);
    state.beforeParams = true;
    return "string";
  } else if (isOperatorChar.test(ch)) {
    stream.eatWhile(isOperatorChar);
    return "operator";
  } else {
    stream.eatWhile(/[\w\$_{}]/);
    var word = stream.current().toLowerCase();
    if (keywords && keywords.propertyIsEnumerable(word)) return "keyword";
    if (functions && functions.propertyIsEnumerable(word)) {
      state.beforeParams = true;
      return "keyword";
    }
    return null;
  }
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
function tokenUnparsed(stream, state) {
  var maybeEnd = 0,
    ch;
  while (ch = stream.next()) {
    if (ch == ";" && maybeEnd == 2) {
      state.tokenize = tokenBase;
      break;
    }
    if (ch == ")") maybeEnd++;else if (ch != " ") maybeEnd = 0;
  }
  return "meta";
}
const mirc = {
  name: "mirc",
  startState: function () {
    return {
      tokenize: tokenBase,
      beforeParams: false,
      inParams: false
    };
  },
  token: function (stream, state) {
    if (stream.eatSpace()) return null;
    return state.tokenize(stream, state);
  }
};

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiOTA0Mi5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGRhdGFsYXllci9qdXB5dGVyLXZpZXdlci8uL25vZGVfbW9kdWxlcy9AY29kZW1pcnJvci9sZWdhY3ktbW9kZXMvbW9kZS9taXJjLmpzIl0sInNvdXJjZXNDb250ZW50IjpbImZ1bmN0aW9uIHBhcnNlV29yZHMoc3RyKSB7XG4gIHZhciBvYmogPSB7fSxcbiAgICB3b3JkcyA9IHN0ci5zcGxpdChcIiBcIik7XG4gIGZvciAodmFyIGkgPSAwOyBpIDwgd29yZHMubGVuZ3RoOyArK2kpIG9ialt3b3Jkc1tpXV0gPSB0cnVlO1xuICByZXR1cm4gb2JqO1xufVxudmFyIHNwZWNpYWxzID0gcGFyc2VXb3JkcyhcIiQhICQkICQmICQ/ICQrICRhYm9vayAkYWJzICRhY3RpdmUgJGFjdGl2ZWNpZCBcIiArIFwiJGFjdGl2ZXdpZCAkYWRkcmVzcyAkYWRkdG9rICRhZ2VudCAkYWdlbnRuYW1lICRhZ2VudHN0YXQgJGFnZW50dmVyIFwiICsgXCIkYWxpYXMgJGFuZCAkYW5pY2sgJGFuc2kybWlyYyAkYW9wICRhcHBhY3RpdmUgJGFwcHN0YXRlICRhc2MgJGFzY3RpbWUgXCIgKyBcIiRhc2luICRhdGFuICRhdm9pY2UgJGF3YXkgJGF3YXltc2cgJGF3YXl0aW1lICRiYW5tYXNrICRiYXNlICRiZmluZCBcIiArIFwiJGJpbm9mZiAkYml0b24gJGJuaWNrICRidmFyICRieXRlcyAkY2FsYyAkY2IgJGNkICRjZWlsICRjaGFuICRjaGFubW9kZXMgXCIgKyBcIiRjaGFudHlwZXMgJGNoYXQgJGNociAkY2lkICRjbGV2ZWwgJGNsaWNrICRjbWRib3ggJGNtZGxpbmUgJGNuaWNrICRjb2xvciBcIiArIFwiJGNvbSAkY29tY2FsbCAkY29tY2hhbiAkY29tZXJyICRjb21wYWN0ICRjb21wcmVzcyAkY29tdmFsICRjb3MgJGNvdW50IFwiICsgXCIkY3IgJGNyYyAkY3JlcSAkY3JsZiAkY3RpbWUgJGN0aW1lciAkY3RybGVudGVyICRkYXRlICRkYXkgJGRheWxpZ2h0IFwiICsgXCIkZGJ1aCAkZGJ1dyAkZGNjaWdub3JlICRkY2Nwb3J0ICRkZGUgJGRkZW5hbWUgJGRlYnVnICRkZWNvZGUgJGRlY29tcHJlc3MgXCIgKyBcIiRkZWx0b2sgJGRldmVudCAkZGlhbG9nICRkaWQgJGRpZHJlZyAkZGlkdG9rICRkaWR3bSAkZGlzayAkZGxldmVsICRkbGwgXCIgKyBcIiRkbGxjYWxsICRkbmFtZSAkZG5zICRkdXJhdGlvbiAkZWJlZXBzICRlZGl0Ym94ICRlbWFpbGFkZHIgJGVuY29kZSAkZXJyb3IgXCIgKyBcIiRldmFsICRldmVudCAkZXhpc3QgJGZlb2YgJGZlcnIgJGZnZXRjICRmaWxlICRmaWxlbmFtZSAkZmlsdGVyZWQgJGZpbmRkaXIgXCIgKyBcIiRmaW5kZGlybiAkZmluZGZpbGUgJGZpbmRmaWxlbiAkZmluZHRvayAkZmxpbmUgJGZsb29yICRmb3BlbiAkZnJlYWQgJGZzZXJ2ZSBcIiArIFwiJGZ1bGxhZGRyZXNzICRmdWxsZGF0ZSAkZnVsbG5hbWUgJGZ1bGxzY3JlZW4gJGdldCAkZ2V0ZGlyICRnZXRkb3QgJGdldHRvayAkZ210IFwiICsgXCIkZ3JvdXAgJGhhbHRlZCAkaGFzaCAkaGVpZ2h0ICRoZmluZCAkaGdldCAkaGlnaGxpZ2h0ICRobmljayAkaG90bGluZSBcIiArIFwiJGhvdGxpbmVwb3MgJGlhbCAkaWFsY2hhbiAkaWJsICRpZGxlICRpZWwgJGlmbWF0Y2ggJGlnbm9yZSAkaWlmICRpaWwgXCIgKyBcIiRpbmVsaXBzZSAkaW5pICRpbm1pZGkgJGlucGFzdGUgJGlucG9seSAkaW5wdXQgJGlucmVjdCAkaW5yb3VuZHJlY3QgXCIgKyBcIiRpbnNvbmcgJGluc3RvayAkaW50ICRpbndhdmUgJGlwICRpc2FsaWFzICRpc2JpdCAkaXNkZGUgJGlzZGlyICRpc2ZpbGUgXCIgKyBcIiRpc2lkICRpc2xvd2VyICRpc3RvayAkaXN1cHBlciAka2V5Y2hhciAka2V5cnB0ICRrZXl2YWwgJGtuaWNrICRsYWN0aXZlIFwiICsgXCIkbGFjdGl2ZWNpZCAkbGFjdGl2ZXdpZCAkbGVmdCAkbGVuICRsZXZlbCAkbGYgJGxpbmUgJGxpbmVzICRsaW5rICRsb2NrIFwiICsgXCIkbG9jayAkbG9ja2VkICRsb2cgJGxvZ3N0YW1wICRsb2dzdGFtcGZtdCAkbG9uZ2ZuICRsb25naXAgJGxvd2VyICRsdGltZXIgXCIgKyBcIiRtYWRkcmVzcyAkbWFzayAkbWF0Y2hrZXkgJG1hdGNodG9rICRtZDUgJG1lICRtZW51ICRtZW51YmFyICRtZW51Y29udGV4dCBcIiArIFwiJG1lbnV0eXBlICRtaWQgJG1pZGRpciAkbWlyY2RpciAkbWlyY2V4ZSAkbWlyY2luaSAkbWtsb2dmbiAkbW5pY2sgJG1vZGUgXCIgKyBcIiRtb2RlZmlyc3QgJG1vZGVsYXN0ICRtb2Rlc3BsICRtb3VzZSAkbXNmaWxlICRuZXR3b3JrICRuZXduaWNrICRuaWNrICRub2ZpbGUgXCIgKyBcIiRub3BhdGggJG5vcXQgJG5vdCAkbm90YWdzICRub3RpZnkgJG51bGwgJG51bWVyaWMgJG51bW9rICRvbGluZSAkb25wb2x5IFwiICsgXCIkb3BuaWNrICRvciAkb3JkICRvcyAkcGFzc2l2ZWRjYyAkcGljICRwbGF5ICRwbmljayAkcG9ydCAkcG9ydGFibGUgJHBvcnRmcmVlIFwiICsgXCIkcG9zICRwcmVmaXggJHByb3AgJHByb3RlY3QgJHB1dHRvayAkcXQgJHF1ZXJ5ICRyYW5kICRyICRyYXdtc2cgJHJlYWQgJHJlYWRvbW8gXCIgKyBcIiRyZWFkbiAkcmVnZXggJHJlZ21sICRyZWdzdWIgJHJlZ3N1YmV4ICRyZW1vdmUgJHJlbXRvayAkcmVwbGFjZSAkcmVwbGFjZXggXCIgKyBcIiRyZXB0b2sgJHJlc3VsdCAkcmdiICRyaWdodCAkcm91bmQgJHNjaWQgJHNjb24gJHNjcmlwdCAkc2NyaXB0ZGlyICRzY3JpcHRsaW5lIFwiICsgXCIkc2RpciAkc2VuZCAkc2VydmVyICRzZXJ2ZXJpcCAkc2ZpbGUgJHNoYTEgJHNob3J0Zm4gJHNob3cgJHNpZ25hbCAkc2luIFwiICsgXCIkc2l0ZSAkc2xpbmUgJHNuaWNrICRzbmlja3MgJHNub3RpZnkgJHNvY2sgJHNvY2ticiAkc29ja2VyciAkc29ja25hbWUgXCIgKyBcIiRzb3J0dG9rICRzb3VuZCAkc3FydCAkc3NsICRzcmVxICRzc2xyZWFkeSAkc3RhdHVzICRzdHJpcCAkc3RyICRzdHJpcHBlZCBcIiArIFwiJHN5bGUgJHN1Ym1lbnUgJHN3aXRjaGJhciAkdGFuICR0YXJnZXQgJHRpY2tzICR0aW1lICR0aW1lciAkdGltZXN0YW1wIFwiICsgXCIkdGltZXN0YW1wZm10ICR0aW1lem9uZSAkdGlwICR0aXRsZWJhciAkdG9vbGJhciAkdHJlZWJhciAkdHJ1c3QgJHVsZXZlbCBcIiArIFwiJHVsaXN0ICR1cHBlciAkdXB0aW1lICR1cmwgJHVzZXJtb2RlICR2MSAkdjIgJHZhciAkdmNtZCAkdmNtZHN0YXQgJHZjbWR2ZXIgXCIgKyBcIiR2ZXJzaW9uICR2bmljayAkdm9sICR3aWQgJHdpZHRoICR3aWxkc2l0ZSAkd2lsZHRvayAkd2luZG93ICR3cmFwICR4b3JcIik7XG52YXIga2V5d29yZHMgPSBwYXJzZVdvcmRzKFwiYWJvb2sgYWppbnZpdGUgYWxpYXMgYWxpbmUgYW1lIGFtc2cgYW5pY2sgYW9wIGF1c2VyIGF1dG9qb2luIGF2b2ljZSBcIiArIFwiYXdheSBiYWNrZ3JvdW5kIGJhbiBiY29weSBiZWVwIGJyZWFkIGJyZWFrIGJyZXBsYWNlIGJzZXQgYnRydW5jIGJ1bnNldCBid3JpdGUgXCIgKyBcImNoYW5uZWwgY2xlYXIgY2xlYXJhbGwgY2xpbmUgY2xpcGJvYXJkIGNsb3NlIGNuaWNrIGNvbG9yIGNvbWNsb3NlIGNvbW9wZW4gXCIgKyBcImNvbXJlZyBjb250aW51ZSBjb3B5IGNyZXEgY3RjcHJlcGx5IGN0Y3BzIGRjYyBkY2NzZXJ2ZXIgZGRlIGRkZXNlcnZlciBcIiArIFwiZGVidWcgZGVjIGRlc2NyaWJlIGRpYWxvZyBkaWQgZGlkdG9rIGRpc2FibGUgZGlzY29ubmVjdCBkbGV2ZWwgZGxpbmUgZGxsIFwiICsgXCJkbnMgZHF3aW5kb3cgZHJhd2NvcHkgZHJhd2RvdCBkcmF3ZmlsbCBkcmF3bGluZSBkcmF3cGljIGRyYXdyZWN0IGRyYXdyZXBsYWNlIFwiICsgXCJkcmF3cm90IGRyYXdzYXZlIGRyYXdzY3JvbGwgZHJhd3RleHQgZWJlZXBzIGVjaG8gZWRpdGJveCBlbWFpbGFkZHIgZW5hYmxlIFwiICsgXCJldmVudHMgZXhpdCBmY2xvc2UgZmlsdGVyIGZpbmR0ZXh0IGZpbmdlciBmaXJld2FsbCBmbGFzaCBmbGlzdCBmbG9vZCBmbHVzaCBcIiArIFwiZmx1c2hpbmkgZm9udCBmb3BlbiBmc2VlayBmc2VuZCBmc2VydmUgZnVsbG5hbWUgZndyaXRlIGdoaWRlIGdsb2FkIGdtb3ZlIFwiICsgXCJnb3B0cyBnb3RvIGdwbGF5IGdwb2ludCBncXJlcSBncm91cHMgZ3Nob3cgZ3NpemUgZ3N0b3AgZ3RhbGsgZ3VubG9hZCBoYWRkIFwiICsgXCJoYWx0IGhhbHRkZWYgaGRlYyBoZGVsIGhlbHAgaGZyZWUgaGluYyBobG9hZCBobWFrZSBob3AgaHNhdmUgaWFsIGlhbGNsZWFyIFwiICsgXCJpYWxtYXJrIGlkZW50ZCBpZiBpZ25vcmUgaWxpbmUgaW5jIGludml0ZSBpdXNlciBqb2luIGtpY2sgbGluZXNlcCBsaW5rcyBsaXN0IFwiICsgXCJsb2FkIGxvYWRidWYgbG9jYWxpbmZvIGxvZyBtZGkgbWUgbWVudWJhciBta2RpciBtbmljayBtb2RlIG1zZyBuaWNrIG5vb3Agbm90aWNlIFwiICsgXCJub3RpZnkgb21zZyBvbm90aWNlIHBhcnQgcGFydGFsbCBwZGNjIHBlcmZvcm0gcGxheSBwbGF5Y3RybCBwb3AgcHJvdGVjdCBwdm9pY2UgXCIgKyBcInFtZSBxbXNnIHF1ZXJ5IHF1ZXJ5biBxdWl0IHJhdyByZWxvYWQgcmVtaW5pIHJlbW90ZSByZW1vdmUgcmVuYW1lIHJlbndpbiBcIiArIFwicmVzZXRlcnJvciByZXNldGlkbGUgcmV0dXJuIHJsZXZlbCBybGluZSBybWRpciBydW4gcnVzZXIgc2F2ZSBzYXZlYnVmIHNhdmVpbmkgXCIgKyBcInNheSBzY2lkIHNjb24gc2VydmVyIHNldCBzaG93bWlyYyBzaWduYW0gc2xpbmUgc29ja2FjY2VwdCBzb2NrY2xvc2Ugc29ja2xpc3QgXCIgKyBcInNvY2tsaXN0ZW4gc29ja21hcmsgc29ja29wZW4gc29ja3BhdXNlIHNvY2tyZWFkIHNvY2tyZW5hbWUgc29ja3VkcCBzb2Nrd3JpdGUgXCIgKyBcInNvdW5kIHNwZWFrIHNwbGF5IHNyZXEgc3RyaXAgc3dpdGNoYmFyIHRpbWVyIHRpbWVzdGFtcCB0aXRsZWJhciB0bmljayB0b2tlbml6ZSBcIiArIFwidG9vbGJhciB0b3BpYyB0cmF5IHRyZWViYXIgdWxpc3QgdW5sb2FkIHVuc2V0IHVuc2V0YWxsIHVwZGF0ZW5sIHVybCB1d2hvIFwiICsgXCJ2YXIgdmNhZGQgdmNtZCB2Y3JlbSB2b2wgd2hpbGUgd2hvaXMgd2luZG93IHdpbmhlbHAgd3JpdGUgd3JpdGVpbnQgaWYgaXNhbG51bSBcIiArIFwiaXNhbHBoYSBpc2FvcCBpc2F2b2ljZSBpc2JhbiBpc2NoYW4gaXNob3AgaXNpZ25vcmUgaXNpbiBpc2luY3MgaXNsZXR0ZXIgaXNsb3dlciBcIiArIFwiaXNub3RpZnkgaXNudW0gaXNvbiBpc29wIGlzcHJvdGVjdCBpc3JlZyBpc3VwcGVyIGlzdm9pY2UgaXN3bSBpc3dtY3MgXCIgKyBcImVsc2VpZiBlbHNlIGdvdG8gbWVudSBuaWNrbGlzdCBzdGF0dXMgdGl0bGUgaWNvbiBzaXplIG9wdGlvbiB0ZXh0IGVkaXQgXCIgKyBcImJ1dHRvbiBjaGVjayByYWRpbyBib3ggc2Nyb2xsIGxpc3QgY29tYm8gbGluayB0YWIgaXRlbVwiKTtcbnZhciBmdW5jdGlvbnMgPSBwYXJzZVdvcmRzKFwiaWYgZWxzZWlmIGVsc2UgYW5kIG5vdCBvciBlcSBuZSBpbiBuaSBmb3IgZm9yZWFjaCB3aGlsZSBzd2l0Y2hcIik7XG52YXIgaXNPcGVyYXRvckNoYXIgPSAvWytcXC0qJiU9PD4hP15cXC9cXHxdLztcbmZ1bmN0aW9uIGNoYWluKHN0cmVhbSwgc3RhdGUsIGYpIHtcbiAgc3RhdGUudG9rZW5pemUgPSBmO1xuICByZXR1cm4gZihzdHJlYW0sIHN0YXRlKTtcbn1cbmZ1bmN0aW9uIHRva2VuQmFzZShzdHJlYW0sIHN0YXRlKSB7XG4gIHZhciBiZWZvcmVQYXJhbXMgPSBzdGF0ZS5iZWZvcmVQYXJhbXM7XG4gIHN0YXRlLmJlZm9yZVBhcmFtcyA9IGZhbHNlO1xuICB2YXIgY2ggPSBzdHJlYW0ubmV4dCgpO1xuICBpZiAoL1tcXFtcXF17fVxcKFxcKSxcXC5dLy50ZXN0KGNoKSkge1xuICAgIGlmIChjaCA9PSBcIihcIiAmJiBiZWZvcmVQYXJhbXMpIHN0YXRlLmluUGFyYW1zID0gdHJ1ZTtlbHNlIGlmIChjaCA9PSBcIilcIikgc3RhdGUuaW5QYXJhbXMgPSBmYWxzZTtcbiAgICByZXR1cm4gbnVsbDtcbiAgfSBlbHNlIGlmICgvXFxkLy50ZXN0KGNoKSkge1xuICAgIHN0cmVhbS5lYXRXaGlsZSgvW1xcd1xcLl0vKTtcbiAgICByZXR1cm4gXCJudW1iZXJcIjtcbiAgfSBlbHNlIGlmIChjaCA9PSBcIlxcXFxcIikge1xuICAgIHN0cmVhbS5lYXQoXCJcXFxcXCIpO1xuICAgIHN0cmVhbS5lYXQoLy4vKTtcbiAgICByZXR1cm4gXCJudW1iZXJcIjtcbiAgfSBlbHNlIGlmIChjaCA9PSBcIi9cIiAmJiBzdHJlYW0uZWF0KFwiKlwiKSkge1xuICAgIHJldHVybiBjaGFpbihzdHJlYW0sIHN0YXRlLCB0b2tlbkNvbW1lbnQpO1xuICB9IGVsc2UgaWYgKGNoID09IFwiO1wiICYmIHN0cmVhbS5tYXRjaCgvICpcXCggKlxcKC8pKSB7XG4gICAgcmV0dXJuIGNoYWluKHN0cmVhbSwgc3RhdGUsIHRva2VuVW5wYXJzZWQpO1xuICB9IGVsc2UgaWYgKGNoID09IFwiO1wiICYmICFzdGF0ZS5pblBhcmFtcykge1xuICAgIHN0cmVhbS5za2lwVG9FbmQoKTtcbiAgICByZXR1cm4gXCJjb21tZW50XCI7XG4gIH0gZWxzZSBpZiAoY2ggPT0gJ1wiJykge1xuICAgIHN0cmVhbS5lYXQoL1wiLyk7XG4gICAgcmV0dXJuIFwia2V5d29yZFwiO1xuICB9IGVsc2UgaWYgKGNoID09IFwiJFwiKSB7XG4gICAgc3RyZWFtLmVhdFdoaWxlKC9bJF9hLXowLTlBLVpcXC46XS8pO1xuICAgIGlmIChzcGVjaWFscyAmJiBzcGVjaWFscy5wcm9wZXJ0eUlzRW51bWVyYWJsZShzdHJlYW0uY3VycmVudCgpLnRvTG93ZXJDYXNlKCkpKSB7XG4gICAgICByZXR1cm4gXCJrZXl3b3JkXCI7XG4gICAgfSBlbHNlIHtcbiAgICAgIHN0YXRlLmJlZm9yZVBhcmFtcyA9IHRydWU7XG4gICAgICByZXR1cm4gXCJidWlsdGluXCI7XG4gICAgfVxuICB9IGVsc2UgaWYgKGNoID09IFwiJVwiKSB7XG4gICAgc3RyZWFtLmVhdFdoaWxlKC9bXixcXHMoKV0vKTtcbiAgICBzdGF0ZS5iZWZvcmVQYXJhbXMgPSB0cnVlO1xuICAgIHJldHVybiBcInN0cmluZ1wiO1xuICB9IGVsc2UgaWYgKGlzT3BlcmF0b3JDaGFyLnRlc3QoY2gpKSB7XG4gICAgc3RyZWFtLmVhdFdoaWxlKGlzT3BlcmF0b3JDaGFyKTtcbiAgICByZXR1cm4gXCJvcGVyYXRvclwiO1xuICB9IGVsc2Uge1xuICAgIHN0cmVhbS5lYXRXaGlsZSgvW1xcd1xcJF97fV0vKTtcbiAgICB2YXIgd29yZCA9IHN0cmVhbS5jdXJyZW50KCkudG9Mb3dlckNhc2UoKTtcbiAgICBpZiAoa2V5d29yZHMgJiYga2V5d29yZHMucHJvcGVydHlJc0VudW1lcmFibGUod29yZCkpIHJldHVybiBcImtleXdvcmRcIjtcbiAgICBpZiAoZnVuY3Rpb25zICYmIGZ1bmN0aW9ucy5wcm9wZXJ0eUlzRW51bWVyYWJsZSh3b3JkKSkge1xuICAgICAgc3RhdGUuYmVmb3JlUGFyYW1zID0gdHJ1ZTtcbiAgICAgIHJldHVybiBcImtleXdvcmRcIjtcbiAgICB9XG4gICAgcmV0dXJuIG51bGw7XG4gIH1cbn1cbmZ1bmN0aW9uIHRva2VuQ29tbWVudChzdHJlYW0sIHN0YXRlKSB7XG4gIHZhciBtYXliZUVuZCA9IGZhbHNlLFxuICAgIGNoO1xuICB3aGlsZSAoY2ggPSBzdHJlYW0ubmV4dCgpKSB7XG4gICAgaWYgKGNoID09IFwiL1wiICYmIG1heWJlRW5kKSB7XG4gICAgICBzdGF0ZS50b2tlbml6ZSA9IHRva2VuQmFzZTtcbiAgICAgIGJyZWFrO1xuICAgIH1cbiAgICBtYXliZUVuZCA9IGNoID09IFwiKlwiO1xuICB9XG4gIHJldHVybiBcImNvbW1lbnRcIjtcbn1cbmZ1bmN0aW9uIHRva2VuVW5wYXJzZWQoc3RyZWFtLCBzdGF0ZSkge1xuICB2YXIgbWF5YmVFbmQgPSAwLFxuICAgIGNoO1xuICB3aGlsZSAoY2ggPSBzdHJlYW0ubmV4dCgpKSB7XG4gICAgaWYgKGNoID09IFwiO1wiICYmIG1heWJlRW5kID09IDIpIHtcbiAgICAgIHN0YXRlLnRva2VuaXplID0gdG9rZW5CYXNlO1xuICAgICAgYnJlYWs7XG4gICAgfVxuICAgIGlmIChjaCA9PSBcIilcIikgbWF5YmVFbmQrKztlbHNlIGlmIChjaCAhPSBcIiBcIikgbWF5YmVFbmQgPSAwO1xuICB9XG4gIHJldHVybiBcIm1ldGFcIjtcbn1cbmV4cG9ydCBjb25zdCBtaXJjID0ge1xuICBuYW1lOiBcIm1pcmNcIixcbiAgc3RhcnRTdGF0ZTogZnVuY3Rpb24gKCkge1xuICAgIHJldHVybiB7XG4gICAgICB0b2tlbml6ZTogdG9rZW5CYXNlLFxuICAgICAgYmVmb3JlUGFyYW1zOiBmYWxzZSxcbiAgICAgIGluUGFyYW1zOiBmYWxzZVxuICAgIH07XG4gIH0sXG4gIHRva2VuOiBmdW5jdGlvbiAoc3RyZWFtLCBzdGF0ZSkge1xuICAgIGlmIChzdHJlYW0uZWF0U3BhY2UoKSkgcmV0dXJuIG51bGw7XG4gICAgcmV0dXJuIHN0YXRlLnRva2VuaXplKHN0cmVhbSwgc3RhdGUpO1xuICB9XG59OyJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==