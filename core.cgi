#!/usr/local/bin/perl

#------------------------------------------------------------------------------#
# 'Marldia' Chat System
# - Main Script -
#
# $Revision: 1.2 $
# "This file is written in euc-jp, CRLF." 空
# Scripted by NARUSE Yui.
#------------------------------------------------------------------------------#
# $cvsid = q$Id: core.cgi,v 1.2 2001-12-21 09:06:47 naruse Exp $;
require 5.004;
#use lib './lib';
use Fcntl qw(:DEFAULT :flock);
use strict;
use vars qw(%CF %IN %CK %IC);
$|=1;

MAIN:{
  &getfm;
  
  (" $IN{'name'} "=~m/ $CF{'denyname'} /o)&&(&locate($CF{'home'}));
#  (" $ENV{'REMOT_ADDR'} "=~m/ $CF{'denyra'} /o)&&(&locate($CF{'home'}));
#  (" $ENV{'REMOT_HOST'} "=~m/ $CF{'denyrh'} /o)&&(&locate($CF{'home'}));
  
  if('frame'eq$IN{'mode'}){
    &frame;
  }elsif('north'eq$IN{'mode'}){
    &north;
  }else{
    &south;
  }
  exit;
}

#-------------------------------------------------
# Frame
sub frame{
  print<<"_HTML_";
Content-type: text/html; charset=euc-jp
Content-Language: ja

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN""http://www.w3.org/TR/html4/frameset.dtd">
<html lang="ja">
<head>
<meta http-equiv="Content-type" content="text/html; charset=euc-jp">
<meta http-equiv="Content-Script-Type" content="text/javascript">
<meta http-equiv="Content-Style-Type" content="text/css">
<link rel="start" href="$CF{'home'}">
<link rel="index" href="$CF{'index'}">
<link rel="help" href="$CF{'help'}">
<title>$CF{'title'}</title>
</head>
<frameset rows="80,*" title="MarldiaFrameset">
  <frame frameborder="0" name="North" src="index.cgi?north">
  <frame frameborder="0" name="South" src="index.cgi?south">
  <noframes>
  <pre>
  このページはMicrosoft Internet Explorer 6.0 向けに作られています
  MSIE5.01やNetscape6、Mozilla0.9以上でもそこそこに見ることが出来ると思います
  Netscape4.xでは表示の一部が崩れる可能性があります
  テーブルやフレームに対応していないブラウザでは、表示の大部分が崩れてしまうため、
  実質的に閲覧することができません
  Mozilla4以上互換のブラウザでまた来てください
  </pre>
  </noframes>
</frameset>
_HTML_
  exit;
}

#-------------------------------------------------
# North
sub north{
  &getck;
  (%CK)||(%CK=%IN);
  &header;
  &iptico($CK{'icon'},'icon','tabindex="12"');
  print<<"_HTML_";
<script type="text/javascript" defer="defer">
<!--
window.onload=autoreset;
function autoreset(){
  if(self.document.north.cook){
    if(document.cookie){
      self.document.north.cook.checked=false;
    }else if(self.document.north.cook.checked==true){
      self.document.north.cook.checked=true;
    }
  }
  if(self.document.north.mes){
    self.document.north.mes.value="";
    self.document.north.mes.focus();
  }
}
function IconPreview(arg){
  if(document.images["Preview"]){
    document.images["Preview"].src="$CF{'icon'}"+arg;
  }
}
//-->
</script>
<form name="north" id="north" method="post" action="index.cgi" target="South" onsubmit="setTimeout(autoreset,20)">
<table style="margin:0 auto;width:780px" summary="主要項目">
<col style="width:100px">
<col style="width:80px">
<col style="width:160px">
<col style="width:80px">
<col style="width:110px">
<col style="width:90px">
<col style="width:40px">
<col style="width:120px">
<col>
<tr>
<th style="font-size:15px;text-align:center">: Marldia :
<input type="hidden" name="home" value="$CK{'home'}">
</th>
<th><label accesskey="n" for="name">名前(<span class="ak">N</span>)</label>:</th>
<td><input type="text" name="name" id="name" maxlength="20" size="20"
 style="ime-mode:active;width:100px" value="$CK{'name'}" tabindex="11"></td>
<th><label accesskey="c" for="color">名前色(<span class="ak">C</span>)</label>:</th>
<td>@{[&iptcol($CK{'color'},'color','tabindex="21"')]}</td>
<th><label accesskey="g" for="line">ログ行数(<span class="ak">G</span>)</label>:</th>
<td><input type="text" name="line" id="line" maxlength="4" size="4"
 style="ime-mode:disabled;width:32px" value="$CK{'line'}行" tabindex="31"></td>
<td><input type="submit" accesskey="s" class="submit" value="OK" tabindex="41"></td>
<td></td>
</tr>
<tr>
<td rowspan="2" style="text-align:center">
<img name="Preview" id="Preview" alt="Preview" src="$CF{'icon'}$CK{'icon'}"$CF{'icsz'}></td>
<th><label accesskey="i" for="icon">アイコン(<span class="ak">I</span>)</label>:</th>
<td>@{[&iptico($CK{'icon'},'icon','tabindex="12"')]}</td>
<th><label accesskey="b" for="bcolo">文章色(<span class="ak">B</span>)</label>:</th>
<td>@{[&iptcol($CK{'bcolo'},'bcolo','tabindex="22"')]}</td>
<th><label accesskey="r" for="reload">更新間隔(<span class="ak">R</span>)</label>:</th>
<td><input type="text" name="reload" id="reload" maxlength="4" size="4"
 style="ime-mode:disabled;width:32px" value="$CK{'reload'}秒" tabindex="32"></td>
<td><input type="reset" class="reset" value="キャンセル" tabindex="42"></td>
</tr>
<tr>
<th><label accesskey="m" for="mes">内容(<span class="ak">M</span>)</label>:</th>
<td colspan="5"><input type="text" name="mes" id="mes" accesskey="m" maxlength="300" size="100"
 style="ime-mode:active;width:460px" tabindex="1"></td>
<td><label accesskey="k" for="cook"><input type="checkbox" name="cook" id="cook"
 class="check" tabindex="51" checked="checked">クッキ保存(<span class="ak">K</span>)</label></td>
</tr>
<tr>
<td rowspan="2" style="text-align:center">[ <a href="$ENV{'SCRIPT_NAME'}?north" accesskey="q" tabindex="52">再読込(<span class="ak">Q</span>)</a> ]</td>
<th><label accesskey="u" for="id">登録名(<span class="ak">U</span>)</label>:</th>
<td><input type="text" name="id" id="id" maxlength="20" size="20"
 style="ime-mode:active;width:100px" value="$CK{'id'}" tabindex="101"></td>
<th><label accesskey="l" for="email">E-Mai<span class="ak">l</span></label>:</th>
<td colspan="3"><input type="text" name="email" id="email" maxlength="200" size="40"
 style="ime-mode:inactive;width:200px" value="$CK{'email'}" tabindex="111"></td>
</tr>
<tr>
<th><label accesskey="x" for="cmd">E<span class="ak">X</span>Icon</label>:</th>
<td><input type="text" name="cmd" id="cmd" maxlength="200" style="ime-mode:inactive;width:100px"
 onchange="IconPreview(&#34;$CF{'icon'}&#34;+this.value)" value="$CK{'cmd'}" tabindex="102"></td>
<th><label accesskey="o" for="home">H<span class="ak">o</span>me</label>:</th>
<td colspan="3"><input type="text" name="home" id="home" maxlength="200" size="40"
 style="ime-mode:inactive;width:200px" value="$CK{'home'}" tabindex="112"></td>
</tr>
</table>
</form>
_HTML_
  exit;
}


#-------------------------------------------------
# South
sub south{

  #補助スイッチ
  if($IN{'mes'}eq '#rank'){
    #ランキング
    &rank;
  }
#=item
  elsif($IN{'mes'}eq '#mem'){
    #参加者詳細
    &mem;
  }
#=cut

  my@log=();
  my%RK;
  my%MB;

  #専用アイコン
  if($IN{'cmd'}){
#    my%CM=($IN{'cmd'}=~m/([^\t]*)=\t([^\t]*);\t/go);
#    ($CM{'icon'})&&($IN{'icon'}=$CM{'icon'});
    $IN{'icon'}=$IN{'cmd'};
  }

  #クッキー書き込み
  if($IN{'cook'}){
    my$cook="id\t$IN{'id'}\tname\t$IN{'name'}\tcolor\t$IN{'color'}\tbcolo\t$IN{'bcolo'}"
    ."\tline\t$IN{'line'}\treload\t$IN{'reload'}\ticon\t$IN{'icon'}"
    ."\temail\t$IN{'email'}\thome\t$IN{'home'}";
    #0-9A-Za-z\-\.\_
    $cook=~s{(\W)}{'%'.unpack('H2',$1)}ego;
    my$gmt=&date(($^T+20000000),'gmt');
    print"Set-Cookie: Marldia=$cook; expires=$gmt\n";
  }

  if(length$IN{'mes'}){
    #ランキング加点
    sysopen(RANK,$CF{'rank'},O_CREAT|O_RDWR)||die"Can't write rank.";
    flock(RANK,LOCK_EX);
    my($key,$val,@tmp)=map{$_=~/(.*)/o}('','',<RANK>);
    while(($key,$val)=splice(@tmp,0,2)){
      $RK{"$key"}="$val";
    }
    ($RK{"$IN{'id'}"}=~s/\tpoint=\t(\d+);\t/\tpoint=\t@{[$1+1]};\t/o)
     ||($RK{"$IN{'id'}"}="\tpoint=\t1;\t");
    $IN{'point'}=($1)?$1+1:1;
    delete$RK{''};
    truncate(RANK,0);
    seek(RANK,0,'SEEK_SET');
    for(keys%RK){
      print RANK "$_\n$RK{$_}\n";
    }
    close RANK;

    # 発言処理
    my$data="Mar1=\t;\tname=\t$IN{'name'};\tcolor=\t$IN{'color'};\tbcolo=\t$IN{'bcolo'};\t"
    ."mes=\t$IN{'mes'};\ticon=\t$IN{'icon'};\thome=\t$IN{'home'};\temail=\t$IN{'email'};\t"
    ."point=\t$IN{'point'};\tua=\t$IN{'hua'};\taddr=\t$IN{'ra'};\ttime=\t$^T;\t\n";
    
    sysopen(LOG,$CF{'log'},O_CREAT|O_RDWR)||die"Can't write file.";
    flock(LOG,LOCK_EX);
    @log=<LOG>;
    splice(@log,$CF{'max'}-1);
    unshift(@log,$data);
    truncate(LOG,0);
    seek(LOG,0,'SEEK_SET');
    print LOG join('',@log);
    close(LOG);
    
  }else{
    sysopen(LOG,$CF{'log'},O_CREAT|O_RDONLY)||die"Can't open file.";
    flock(LOG,LOCK_SH);
    @log=<LOG>;
    close(LOG);
  }

  #参加者読み込み
  sysopen(MEM,$CF{'mem'},O_CREAT|O_RDWR)||die"Can't write mem.";
  flock(MEM,LOCK_EX);
  my($key,$val,@tmp)=map{$_=~/(.*)/o}('','',<MEM>);
  while(($key,$val)=splice(@tmp,0,2)){
    $MB{"$key"}="$val";
  }
  delete$MB{''};
  if($IN{'name'}&&$ENV{'CONTENT_LENGTH'}){
    delete$MB{"$IN{'ra'}"};
    $MB{"$IN{'id'}"}="name=\t$IN{'name'};\tcolor=\t$IN{'color'};\treload=\t$IN{'reload'};\taddr=\t$IN{'ra'};\ttime=\t$^T;\texpire=\t$^T;\t";
  }elsif($IN{'name'}){
    delete$MB{"$IN{'ra'}"};
    $MB{"$IN{'id'}"}=~m/\texpire=\t(\d+);\t/;
    $MB{"$IN{'id'}"}="name=\t$IN{'name'};\tcolor=\t$IN{'color'};\treload=\t$IN{'reload'};\taddr=\t$IN{'ra'};\ttime=\t$^T;\texpire=\t$1;\t";
  }else{
    $MB{"$IN{'ra'}"}="reload=\t$IN{'reload'};\taddr=\t$IN{'ra'};\ttime=\t$^T;\t";
  }
  #参加者処理
  my@mb=();
  for(keys%MB){
    my%DT=($MB{"$_"}=~m/([^\t]*)=\t([^\t]*);\t/go);
    ($DT{'reload'}<20)&&($DT{'reload'}=20);
    (($DT{'time'}+($DT{'reload'}*6))<$^T)&&(delete$MB{$_},next);#TimeOver
    (exists$DT{'color'})||(next);#ROM
    $DT{'expire'}=$^T-$DT{'expire'};
    push(@mb,qq[<a style="color:$DT{'color'}" title="$DT{'expire'}秒">$DT{'name'}</a>☆]);
  }
  truncate(MEM,0);
  seek(MEM,0,'SEEK_SET');
  for(keys%MB){
    print MEM "$_\n$MB{$_}\n";
  }
  close MEM;
  
  my$visitor=scalar(keys%MB);
  my$entrant=$#mb+1;
  my$audience=$visitor-$entrant;

  my$query='south';
  if($IN{'id'}){
    my%DT=%IN;
    for(keys%IN){
      $DT{$_}=~s{(\W)}{'%'.unpack('H2',$1)}ego;
      $_="$_=$DT{$_}";
    }
    $query='';
    for(qw(name id line reload color)){
      $query.="$_=$DT{$_}&amp;";
    }
  }
  
  if($IN{'reload'}){
    &header(qq(<meta http-equiv="refresh" content="$IN{'reload'};url=index.cgi?$query">));
  }else{
    &header;
  }
  print<<"_HTML_";
<div style="text-align:left"><span>[ <a href="index.cgi?$query">Reload</a> ]</span>
<span>[合計:$visitor人 参加者:$entrant人 観客:$audience人] [ @mb ] </span></div>
_HTML_
  
  #ログ表示
  @log=splice(@log,0,$IN{'line'});
  for(@log){
    my%DT=($_=~m/([^\t]*)=\t([^\t]*);\t/go);
    $DT{'date'}=&date($DT{'time'});
    
    #名前・メールアドレス・名前色
    if($DT{'email'}&&$DT{'color'}){
      $DT{'name'}=qq[<a href="mailto:$DT{'email'}" style="color:$DT{'color'}" title="$DT{'email'}">$DT{'name'}</a>];
    }elsif($DT{'email'}){
      $DT{'name'}=qq[<a href="mailto:$DT{'email'}" title="$DT{'email'}">$DT{'name'}</a>];
    }elsif($DT{'color'}){
      $DT{'name'}=qq[<a style="color:$DT{'color'}">$DT{'name'}</a>];
    }
    
    #
    if($DT{'home'}){
      $DT{'home'}=qq[<a href="$DT{'home'}" target="_blank" title="$DT{'home'}">≫</a>];
    }else{
      $DT{'home'}="≫";
    }
    srand($DT{'point'});
    $DT{'level'}=1+int(rand(sqrt$DT{'point'}*2));
    
    print<<"_HTML_";
<table cellspacing="0" class="message" summary="message">
<tr>
<th class="mesicon"><img src="$CF{'icon'}$DT{'icon'}" alt="$DT{'icon'}"$CF{'icsz'}></th>
<th class="mesname">$DT{'name'}&nbsp;$DT{'home'}</th>
<td class="mesbody" style="color:$DT{'bcolo'}">$DT{'mes'}</td>
<td class="mesinfo"><span class="level">Exp.$DT{'point'}/Lv.$DT{'level'}</span>
<span class="date">$DT{'date'}</span></td>
</tr>
</table>
_HTML_
  }
  
    print<<"_HTML_";
<div class="AiremixCopy">- <a href="http://airemix.site.ne.jp/" target="_blank" title="Airemix - Mireille -">Airemix Marldia</a>
<var>$CF{'correv'}</var> -</div>
</body>
</html>
_HTML_
  exit;
}


#-------------------------------------------------
# 発言ランキング
sub rank{
  &header;
  print<<"_HTML_";
<table summary="Ranking">
<caption>発言ランキング</caption>
_HTML_
  sysopen(RANK,$CF{'rank'},O_CREAT|O_RDONLY)||die"Can't read rank.";
  flock(LOG,LOCK_SH);
  my($key,$val,@tmp)=map{$_=~/(.*)/o}('','',<RANK>);
  while(($key,$val)=splice(@tmp,0,2)){
    print"<tr><th>$key</th><td>$val</td></tr>";
  }
  close RANK;
  print<<"_HTML_";
</table>
</body>
</html>
_HTML_
  exit;
}

#-------------------------------------------------
# 見物人一覧
sub mem{
  &header;
  print<<"_HTML_";
<table summary="roms">
<caption>見物人一覧</caption>
_HTML_
  #参加者読み込み
  sysopen(MEM,$CF{'mem'},O_CREAT|O_RDONLY)||die"Can't write rank.";
  flock(LOG,LOCK_SH);
  my($key,$val,@tmp)=map{$_=~/(.*)/o}('','',<MEM>);
  while(($key,$val)=splice(@tmp,0,2)){
    print"<tr><th>$key</th><td>$val</td></tr>";
  }
  close MEM;
  print<<"_HTML_";
</table>
</body>
</html>
_HTML_
  exit;
}


#-------------------------------------------------
# Form内容取得
#

#MethodがHEADならばLastModifedを出力して、
#最後の投稿時刻を知らせる
sub getfm{
  my$i;my%DT;
  if($ENV{'REQUEST_METHOD'}eq'POST'){
    read(STDIN,$i,$ENV{'CONTENT_LENGTH'});
  }elsif($ENV{'REQUEST_METHOD'}eq'GET'){
    $i=$ENV{'QUERY_STRING'};
  }

  if(length$i>262114){
    #サイズ制限
    die"いくらなんでも量が多すぎます\n$i";
    exit;
  }elsif(length$i>0){
    #入力を展開してハッシュに入れる
    # EUC-JP文字
    my$ascii='[\x09\x0A\x0D\x20-\x7E]'; # 1バイト EUC-JP文字改
    my$twoBytes='(?:[\x8E\xA1-\xFE][\xA1-\xFE])'; # 2バイト EUC-JP文字
    my$threeBytes='(?:\x8F[\xA1-\xFE][\xA1-\xFE])'; # 3バイト EUC-JP文字
    for(split(/[&;]/o,$i)){
      my($i,$j)=split('=',$_,2);
      (defined$j)||($DT{$i}='',next);
      study$j;
      $j=~tr/+/\ /;
      $j=~s/%([0-9A-Fa-f]{2})/pack('H2',$1)/ego;
      $j=($j=~/((?:$ascii|$twoBytes|$threeBytes)*)/o)?"$1":'';
      $j=~s/\t/\ \ /go;
      $j=~s/"/&#34;/go;
      $j=~s/&(#?\w+;)?/($1)?"&$1":'&#38;'/ego;
      $j=~s/'/&#39;/go;
  
      if('mes'eq$i){
        #本文のみタグを使ってもいい設定にもできる
        $j=~s/</&#60;\t/go;
        $j=~s/>/&#62;\t/go;
        if($CF{'tags'}){
          $j=~s{&#60;\t(/?)(\w+)([^\t]*)&#62;\t}
          {my($a,$b,$c)=($1,$2,$3);($CF{'tags'}=~/\b$2\b/io)?"<$a$b>":"&#60;$a$b$c&#62;"}ego;
        }
        $j=~tr/\t//d;
      }else{
        $j=~s/</&#60;/go;
        $j=~s/>/&#62;/go;
      }
  
      $j=~s/\x0D\x0A/<br>/go;$j=~s/\x0D/<br>/go;$j=~s/\x0A/<br>/go;
      $j=~s/(<br>)+$//o;
      $DT{$i}=$j;
    }
  }

  
  if((!%DT)||('frame'eq$DT{'mode'})){
    $IN{'mode'}='frame';
  }elsif((defined$DT{'north'})||('north'eq$DT{'mode'})){
    $IN{'mode'}='north';
    $IN{'line'}=$CF{'defline'};
    $IN{'reload'}=$CF{'defreload'};
  }elsif($DT{'name'}){
    &getck;
    #HTTP URL 正規表現
    my$http_URL_regex =
   q{\b(?:https?|shttp)://(?:(?:[-_.!~*'()a-zA-Z0-9;:&=+$,]|%[0-9A-Fa-f}.
   q{][0-9A-Fa-f])*@)?(?:(?:[a-zA-Z0-9](?:[-a-zA-Z0-9]*[a-zA-Z0-9])?\.)}.
   q{*[a-zA-Z](?:[-a-zA-Z0-9]*[a-zA-Z0-9])?\.?|[0-9]+\.[0-9]+\.[0-9]+\.}.
   q{[0-9]+)(?::[0-9]*)?(?:/(?:[-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f]}.
   q{[0-9A-Fa-f])*(?:;(?:[-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f][0-9A-}.
   q{Fa-f])*)*(?:/(?:[-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f}.
   q{])*(?:;(?:[-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*)*)}.
   q{*)?(?:\?(?:[-_.!~*'()a-zA-Z0-9;/?:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])}.
   q{*)?(?:#(?:[-_.!~*'()a-zA-Z0-9;/?:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*}.
   q{)?};
    #FTP URL 正規表現
    my$ftp_URL_regex=
   q{\bftp://(?:(?:[-a-zA-Z0-9_.!*'();&=~]|%[0-9A-Fa-f][0-9A-Fa-f])*(?:}
   .q{:(?:[-a-zA-Z0-9_.!*'();&=~]|%[0-9A-Fa-f][0-9A-Fa-f])*)?@)?(?:(?:[a}
   .q{-zA-Z0-9](?:(?:[a-zA-Z0-9]|-)*[a-zA-Z0-9])?\.)*[a-zA-Z](?:(?:[a-zA}
   .q{-Z0-9]|-)*[a-zA-Z0-9])?|[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)(?::[0-9]*)}
   .q{?(?:/(?:[-a-zA-Z0-9_.!*'():@&=~]|%[0-9A-Fa-f][0-9A-Fa-f])*(?:/(?:[}
   .q{-a-zA-Z0-9_.!*'():@&=~]|%[0-9A-Fa-f][0-9A-Fa-f])*)?(?:;type=[AIDai}
   .q{d])?)?(?![-a-zA-Z0-9_.!*'():@&=~/])}; #'}
    #MAIL 正規表現
    my$mail_regex=
   q{(?:[^(\040)<>@,;:".\\\\\[\]\000-\037\x80-\xff]+(?![^(\040)<>@,;:".\\\\}
   .q{\[\]\000-\037\x80-\xff])|"[^\\\\\x80-\xff\n\015"]*(?:\\\\[^\x80-\xff][}
   .q{^\\\\\x80-\xff\n\015"]*)*")(?:\.(?:[^(\040)<>@,;:".\\\\\[\]\000-\037\x}
   .q{80-\xff]+(?![^(\040)<>@,;:".\\\\\[\]\000-\037\x80-\xff])|"[^\\\\\x80-}
   .q{\xff\n\015"]*(?:\\\\[^\x80-\xff][^\\\\\x80-\xff\n\015"]*)*"))*@(?:[^(}
   .q{\040)<>@,;:".\\\\\[\]\000-\037\x80-\xff]+(?![^(\040)<>@,;:".\\\\\[\]\0}
   .q{00-\037\x80-\xff])|\[(?:[^\\\\\x80-\xff\n\015\[\]]|\\\\[^\x80-\xff])*}
   .q{\])(?:\.(?:[^(\040)<>@,;:".\\\\\[\]\000-\037\x80-\xff]+(?![^(\040)<>@,}
   .q{;:".\\\\\[\]\000-\037\x80-\xff])|\[(?:[^\\\\\x80-\xff\n\015\[\]]|\\\\[}
   .q{^\x80-\xff])*\]))*};
    
    if(defined$DT{'mes'}){
      #外部入力の汚染除去
      $DT{'mes'}=~s{($http_URL_regex|$ftp_URL_regex|($mail_regex))}
      {my($org,$mail)=($1,$2);(my$tmp=$org)=~s/"/&#34;/g;
      '<a class="user" href="'.($mail ne''?'mailto:':'')."$tmp\" target=\"_blank\">$org</a>"}ego;
      $IN{'mes'}=($DT{'mes'}=~/(.+)/o)?"$1":'';
      $IN{'cook'}=($DT{'cook'}=~/(.)/o)?'on':'0';
    }
    $IN{'name'}=($DT{'name'}=~/(.{1,100})/o)?"$1":'';
    $IN{'id'}=($DT{'id'}=~/(.{1,100})/o)?"$1":($CK{'id'}?$CK{'id'}:$IN{'name'});
    $IN{'color'}=($DT{'color'}=~/([\#\w\(\)\,]{1,20})/o)?"$1":'';
    $IN{'bcolo'}=($DT{'bcolo'}=~/([\#\w\(\)\,]{1,20})/o)?"$1":'';
    $DT{'email'}=($DT{'email'}=~/(.{1,200})/o)?"$1":'';
    $IN{'email'}=($DT{'email'}=~/($mail_regex)/o)?"$1":'';
    $DT{'home'}=($DT{'home'}=~/(.{1,200})/o)?"$1":'';
    $IN{'home'}=($DT{'home'}=~/($http_URL_regex)/o)?"$1":'';
    $IN{'icon'}=($DT{'icon'}=~/([\w\.\~\-\%\/]+)/o)?"$1":'';
    $IN{'cmd'}=($DT{'cmd'}=~/(.+)/o)?"$1":undef;
    $IN{'line'}=(($DT{'line'}=~/(\d+)/o)&&(int$1))?int$1:$CF{'defline'};
    $IN{'reload'}=(($DT{'reload'}=~/(\d+)/o)&&(int$1))?int$1:$CF{'defreload'};
    $IN{'ra'}=($ENV{'REMOTE_ADDR'}=~/(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/)?"$1":'';
    $IN{'hua'}=($ENV{'HTTP_USER_AGENT'}=~/([^\t]+)/)?"$1":'';
  }elsif(defined$DT{'south'}){
    $IN{'line'}=$CF{'romline'};
    $IN{'reload'}=$CF{'romreload'};
  }
  return%IN;
}

#-------------------------------------------------
# Header with G-ZIP etc.
sub header{
  print<<'_HTML_';
Content-type: text/html; charset=euc-jp
Content-Language: ja
Pragma: no-cache
Cache-Control: no-cache
_HTML_
=gzip
  if((-x$CF{'gzip'})&&($ENV{'HTTP_ACCEPT_ENCODING'}=~/gzip/)){
    print"Content-encoding: gzip\n\n";
    open(STDOUT,"| $CF{'gzip'} -1 -c");
    print"<!-- gzip enable -->\n";
  }else{print"\n<!-- gzip disable -->\n";}
=cut
  print<<"_HTML_";

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html lang="ja">
<head>
<meta http-equiv="Content-type" content="text/html; charset=euc-jp">
<meta http-equiv="Content-Script-Type" content="text/javascript">
<meta http-equiv="Content-Style-Type" content="text/css">
_HTML_

($_[0])&&(print"$_[0]");

  #CSS Switch
  CSS:{
    if($ENV{'HTTP_USER_AGENT'}=~m/MSIE 3/o){
      #IE3はNG
      last CSS;
    }elsif($ENV{'HTTP_USER_AGENT'}=~m{Mozilla/4.*compatible}o){
      #Mozilla/4互換は通す
    }elsif($ENV{'HTTP_USER_AGENT'}=~m{Mozilla/4}o){
      #NetscapeNavogator4はダメ
      last CSS;
    }
    #それ以外には一応渡しておく
    print qq{<link rel="stylesheet" type="text/css" href="$CF{'style'}" media="screen" title="DefaultStyle">\n};
  }
  print<<"_HTML_";
<link rel="start" href="$CF{'home'}">
<link rel="index" href="$CF{'index'}">
<link rel="help" href="$CF{'help'}">
<link rev="made" href="mailto:naruse\@airemix.site.ne.jp">
<title>$CF{'title'}</title>
</head>
<body>
_HTML_
}

#-------------------------------------------------
# Cookieを取得する
#
sub getck{
  ($ENV{'HTTP_COOKIE'})||(return undef);
  my$ascii='[\x0A\x0D\x20-\x7E]'; # 1バイト EUC-JP文字改-\x09
  my$twoBytes='(?:[\x8E\xA1-\xFE][\xA1-\xFE])'; # 2バイト EUC-JP文字
  my$threeBytes='(?:\x8F[\xA1-\xFE][\xA1-\xFE])'; # 3バイト EUC-JP文字
  my$cook=($ENV{'HTTP_COOKIE'}=~/([^\t]+)/o)?"$1":'';
  for(split('; ',$cook)){
    my($i,$j)=split('=',$_,2);
    ('Marldia'ne$i)&&(next);
    $j=~s/%([0-9A-Fa-f]{2})/pack('H2',$1)/ego;
    %CK=($j=~/(\w+)\t((?:$ascii|$twoBytes|$threeBytes)*)/go);
    last;
  }
  return%CK;
}

#-------------------------------------------------
# フォーマットされた日付取得を返す
sub date{
  if($_[1]eq'gmt'){
   # Cookie用
    return sprintf("%s, %02d-%s-%d %s GMT",(split/\s+/,gmtime($_[0]))[0,2,1,4,3]);
  }elsif($_[1]eq'last'){
   # LastModified用
    return sprintf("%s, %02d %s %s %s GMT",(split/\s+/,gmtime($_[0]))[0,2,1,4,3]);
  }else{
   # 投稿日時表示用
    my($sec,$min,$hour,$mday,$mon,$year,$wday)=localtime($_[0]);
#    my@wdays=qw(Sun Mon Tue Wed Thu Fri Sat);
    my@wdays=qw(日 月 火 水 木 金 土);
    $wday="($wdays[$wday])";
    ($year<1900)&&($year+=1900);
#    return sprintf("%4d/%02d/%02d%s %02d:%02d",$year,$mon+1,$mday,$wday,$hour,$min);
    return sprintf("%4d年%02d月%02d日%s %02d時%02d分",$year,$mon+1,$mday,$wday,$hour,$min);
  }
}

#-------------------------------------------------
# アイコンリスト
#
sub iptico{

=item

$_[0]: $CK{'icon'}
$_[1]: 'icon'
$_[2]: 'tabindex=12'

=cut

  my$name='icon';
  my$opt='';
  ($_[1])&&($name=$_[1]);
  ($_[2])&&($opt=" $_[2]");
  #リスト読み込み
  sysopen(RD,"$CF{'icls'}",O_RDONLY);#||die"Can't open iconlist."; #わざわざエラー返さなくても
  flock(RD,LOCK_SH);
  my$list=join('',<RD>);
  close(RD);
  if($_[0]and$list=~s/(value="$_[0]")/$1 selected="selected"/io){
  }elsif($list=~s/value="([^"]*)"/value="$1" selected="selected"/io){
    $_[0]=$1;
  }
  return<<"_HTML_";
<select name="$name" id="$name" onchange="IconPreview(this.form['icon'][this.options.selectedIndex].value)"$opt>
$list</select>
_HTML_
}


#-------------------------------------------------
# カラーリスト読み込み
#
sub iptcol{

=item

$_[0]: $CK{'color'}
$_[1]: 'color'
$_[2]: 'tabindex=12'

=cut

  my$name='color';
  my$opt='';
  ($_[1])&&($name=$_[1]);
  ($_[2])&&($opt=" $_[2]");
  if('input'eq$CF{'colway'}){
    return<<"_HTML_";
<input type="text" name="$name" id="$name" class="blur" maxlength="20" style="ime-mode:disabled; width:90px;" onFocus="this.className='focus'" onBlur="this.className='blur'" value="$_[0]"$opt>
_HTML_
  }else{
    my$list=<<"_HTML_";
<option value="#000000" style="background-color: #000000;">Black</option>
<option value="#2f4f4f" style="background-color: #2f4f4f;">DarkSlateGray</option>
<option value="#696969" style="background-color: #696969;">DimGray</option>
<option value="#808080" style="background-color: #808080;">Gray</option>
<option value="#708090" style="background-color: #708090;">SlateGray</option>
<option value="#778899" style="background-color: #778899;">LightSlateGray</option>
<option value="#8b4513" style="background-color: #8b4513;">SaddleBrown</option>
<option value="#a0522d" style="background-color: #a0522d;">Sienna</option>
<option value="#d2691e" style="background-color: #d2691e;">Chocolate</option>
<option value="#cd5c5c" style="background-color: #cd5c5c;">IndianRed</option>
<option value="#a52a2a" style="background-color: #a52a2a;">Brown</option>
<option value="#8b0000" style="background-color: #8b0000;">DarkRed</option>
<option value="#800000" style="background-color: #800000;">Maroon</option>
<option value="#b22222" style="background-color: #b22222;">FireBrick</option>
<option value="#ff6347" style="background-color: #ff6347;">Tomato</option>
<option value="#ff4500" style="background-color: #ff4500;">OrangeRed</option>
<option value="#dc143c" style="background-color: #dc143c;">Crimson</option>
<option value="#c71585" style="background-color: #c71585;">MediumVioletRed</option>
<option value="#ff1493" style="background-color: #bb1493;">DeepPink</option>
<option value="#8b008b" style="background-color: #8b008b;">DarkMagenta</option>
<option value="#800080" style="background-color: #800080;">Purple</option>
<option value="#9932cc" style="background-color: #9932cc;">DarkOrchid</option>
<option value="#9400d3" style="background-color: #9400d3;">DarkViolet</option>
<option value="#8a2be2" style="background-color: #8a2be2;">BlueViolet</option>
<option value="#6a5acd" style="background-color: #6a5acd;">SlateBlue</option>
<option value="#4b0082" style="background-color: #4b0082;">Indigo</option>
<option value="#00008e" style="background-color: #00008e;">DarkBlue</option>
<option value="#000080" style="background-color: #000080;">Navy</option>
<option value="#191970" style="background-color: #191970;">MidnightBlue</option>
<option value="#483d8b" style="background-color: #483d8b;">DarkSlateBlue</option>
<option value="#0000cd" style="background-color: #0000cd;">MediumBlue</option>
<option value="#4169e1" style="background-color: #4169e1;">RoyalBlue</option>
<option value="#5f9ea0" style="background-color: #5f9ae0;">CadetBlue</option>
<option value="#4682b4" style="background-color: #4682b4;">SteelBlue</option>
<option value="#008080" style="background-color: #008080;">Teal</option>
<option value="#008b8b" style="background-color: #008b8b;">Darkcyan</option>
<option value="#2e8b57" style="background-color: #2e8b57;">SeaGreen</option>
<option value="#228b22" style="background-color: #228b22;">ForestGreen</option>
<option value="#006400" style="background-color: #006400;">DarkGreen</option>
<option value="#556b2f" style="background-color: #556b2f;">DarkOliveGreen</option>
<option value="#6b8e23" style="background-color: #6b8e23;">OliveDrab</option>
<option value="#808000" style="background-color: #808000;">Olive</option>
_HTML_
    if($_[0]&&$list=~s/(value="$_[0]")/$1 selected="selected"/io){
    }elsif($list=~s/value="([^"]*)"/value="$1" selected="selected"/io){
      $_[0]=$1;
    }
    return<<"_HTML_";
<select name="$name" id="$name"$opt>
$list</select>
_HTML_
  }
}


#-------------------------------------------------
# Locationで転送
sub locate{
  my$i;
  if($_[0]=~/^http:/){
    $i=$_[0];
  }elsif($_[0]=~/\?/){
    $i=sprintf('http://%s%s/',$ENV{'SERVER_NAME'},
    substr($ENV{'SCRIPT_NAME'},0,rindex($ENV{'SCRIPT_NAME'},'/')));
    $i.=sprintf('%s?%s',$_[0]);
  }elsif($_[0]eq'/'){
    $i='http://'.$ENV{'SERVER_NAME'}.'/';
  }elsif($_[0]){
    $i=sprintf('http://%s%s/',$ENV{'SERVER_NAME'},
    substr($ENV{'SCRIPT_NAME'},0,rindex($ENV{'SCRIPT_NAME'},'/')));
    $i.=$_[0];
  }
  print<<"_HTML_";
Location: $i
Content-Type: text/html
Pragma: no-cache
Cache-Control: no-cache

<!DOCTYPE html PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html>
<head>
<meta http-equiv="Refresh" content="0;URL=$i">
<title>301 Moved Permanently</title>
</head>
<body>
<h1>Writing is Complete!</h1>
<p>And, please go <a href="$i">here</A>.</p>
<p>Location: $i</p>
<p>Marldia <span class="red">$CF{'correv'}</span>.<br>
Copyright &copy;2001 <a href="http://airemix.site.ne.jp/" title="Airemix">Airemix</a>. All rights reserved.</p>
</body>
</html>
_HTML_
  exit;
}

#-------------------------------------------------
# 初期設定
BEGIN{
  # Revision Number
  $CF{'correv'}=qq$Revision: 1.2 $;
  #エラーが出たらエラー画面を表示するように
  if($0=~m/\bindex.cgi$/o){
    $SIG{'__DIE__'}=sub{
    print<<"_HTML_";
Content-Language: ja
Content-type: text/plain; charset=euc-jp

<pre>
       :: Marldia ::
   * Error Screen 1.0 (T_T;) *

ERROR: $_[0]
Index : $CF{'idxrev'}
Core  : $CF{'correv'}

PerlVer  : $]
PerlPath : $^X
BaseTime : $^T
OS Name  : $^O
FileName : $0

 = = ENV = =
CONTENT_LENGTH: $ENV{'CONTENT_LENGTH'}
QUERY_STRING  : $ENV{'QUERY_STRING'}
REQUEST_METHOD: $ENV{'REQUEST_METHOD'}

SERVER_NAME: $ENV{'SERVER_NAME'}
HTTP_PATH  : $ENV{'HTTP_HOST'} $ENV{'SCRIPT_NAME'}
ENV_OS     : $ENV{'OS'}
SERVER_SOFTWARE      : $ENV{'SERVER_SOFTWARE'}
PROCESSOR_IDENTIFIER : $ENV{'PROCESSOR_IDENTIFIER'}

+#       Airemix Marldia        #+
+#  http://airemix.site.ne.jp/  #+
_HTML_
    exit;
    };
  }
}
1;
__END__
