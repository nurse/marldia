#!/usr/local/bin/perl

#------------------------------------------------------------------------------#
# 'Marldia' Chat System
# - Main Script -
#
# $Revision: 1.7 $
# "This file is written in euc-jp, CRLF." 空
# Scripted by NARUSE Yui.
#------------------------------------------------------------------------------#
# $cvsid = q$Id: core.cgi,v 1.7 2002-05-04 18:10:30 naruse Exp $;
require 5.004;
#use lib './lib';
use Fcntl qw(:DEFAULT :flock);
use strict;
use vars qw(%CF %IN %CK %IC);
$|=1;

#-------------------------------------------------
# MAIN SWITCH
#
sub main{
  &getform;
  (" $IN{'name'} "=~m/ $CF{'denyname'} /o)&&(&locate($CF{'sitehome'}));
#  (" $ENV{'REMOT_ADDR'} "=~m/ $CF{'denyra'} /o)&&(&locate($CF{'sitehome'}));
#  (" $ENV{'REMOT_HOST'} "=~m/ $CF{'denyrh'} /o)&&(&locate($CF{'sitehome'}));
  
  if('south'eq$IN{'mode'}){
  }elsif('frame'eq$IN{'mode'}){
    &frame;
  }elsif('north'eq$IN{'mode'}){
    &north;
  }elsif('manage'eq$IN{'mode'}){
    &manage;
  }
  &south;
  exit;
}


#------------------------------------------------------------------------------#
# MARD ROUTINS
#
# main直下のサブルーチン群

#-------------------------------------------------
# Frame
#
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
<link rel="start" href="$CF{'sitehome'}">
<link rel="index" href="$CF{'index'}">
<link rel="help" href="$CF{'help'}">
<title>$CF{'title'}</title>
</head>
<frameset rows="120,*">
  <frame frameborder="0" name="north" src="index.cgi?north">
  <frame frameborder="0" name="south" src="index.cgi?south">
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
#
sub north{
  &getck;
  (%CK)||(%CK=%IN);
  &header;
  &iptico($CK{'icon'},'tabindex="12"');
  print<<'_HTML_';
<script type="text/javascript" defer>
<!--
//--------------------------------------
// 初期化
window.onload=autoreset;
var cook,body,preview,surface;
_HTML_
  print qq(var icondir='$CF{'icondir'}';\n);
  print<<'_HTML_';
function autoreset(){
  if(document.all){
    cook=document.all('cook');
    body=document.all('body');
    preview=document.all('Preview');
    surface=document.all('surface');
  }else if(document.getElementById){
    cook=document.getElementById('cook');
    body=document.getElementById('body');
    preview=document.getElementById('Preview');
    surface=document.getElementById('surface');
  }else{return}

  if(cook){
    cook.checked=(document.cookie)?false:true;
  }
  if(body){
    body.value="";
    body.focus();
  }
}

//--------------------------------------
// アイコンプレビュー
function iconPreview(arg){
  if(!preview&&!arg){return;}
  arg=icondir+arg;
  preview.src=arg;
}

//--------------------------------------
// アイコンを変えたら
function iconChange(arg){
  if(!surface&&!arg){return;}
  iconPreview(arg);
  if(!arg.match(/^(([^\/#]*\/)*([^\/#.]*\.)*[^\/#.]+)(\.[^\/#.]*)#(\d+)$/)){
    surface.length=1;
    surface.options[0].text='-';
    surface.options[0].value=arg;
    return;
  }
  var url=RegExp.$1;
  var ext=RegExp.$4;
  var len=parseInt(RegExp.$5)+1;
  surface.length=len+1;
  surface.options[0].text='-';
  surface.options[0].value=url+ext;
  for(i=0;i<len;i++){
    surface.options[i+1].text=i;
    surface.options[i+1].value=url+i+ext;
  }
}


//--------------------------------------
// 表情アイコン見本
function surfaceSample(){
  if(!window.createPopup){return;}
  var popup=window.createPopup();
  var wid=200;
  var hei=250;
  var str=
    '<button type="button" id="surface0" style="margin:0;padding:0;width:50px"'
    +' onclick="top.north.document.all(\'surface\').selectedIndex=0;document.all(\'surfaceS\').selectedIndex=0'
    +';top.north.document.all(\'preview\').src=\''+icondir+surface.options[0].value+'\'">'
    +'<img src="'+icondir+surface.options[0].value+'" alt="-"></button>';

  for(i=1;i<surface.length;i++){
    str+=
    '<button type="button" id="surface'+i+'" style="margin:0;padding:0;width:50px"'
    +' onclick="top.north.document.all(\'surface\').selectedIndex='+i+';document.all(\'surfaceS\').selectedIndex='+i
    +';top.north.document.all(\'preview\').src=\''+icondir+surface.options[i].value+'\'">'
    +'<img src="'+icondir+surface.options[i].value+'" alt="'+(i-1)+'"></button>';
    if(i%3==2){str+='<br>';}
  }
  popup.document.body.innerHTML=
   '<div style="border:3px outset ActiveBorder;height:'+hei+'px;overflow:auto;text-align:left;width:'+wid+'px">'
  +'<div style="color:CaptionText;font:caption;height:15px;padding:2px;width:100%;'
  +'filter:progid:DXImageTransform.Microsoft.Gradient(endColorstr=\'#ffffff\',startColorstr=\'ActiveCaption\','
  +'gradientType=\'1\');">アイコン見本</div>'+str+'<select name="surfaceS" id="surfaceS"'
  +'onchange="document.all(\'surface\'+this.selectedIndex).click()">'+surface.innerHTML+'</select>'
  +'</div>';
  popup.show(20,20,wid,hei,top.south.document.body);
  popup.document.body.document.all('surfaceS').focus();
  return;
}
_HTML_
  print<<"_HTML_";
//-->
</script>
<form name="north" id="north" method="post" action="index.cgi" target="south" onsubmit="setTimeout(autoreset,20)">
<table style="width:770px" summary="主要項目">
<col style="width:110px">
<col style="width:75px">
<col style="width:160px">
<col style="width:75px">
<col style="width:100px">
<col style="width:85px">
<col style="width:40px">
<col style="width:120px">
<col>
<tr>
<td rowspan="5" style="text-align:center">
<h1>$CF{'pgtit'}</h1>
<img name="Preview" id="Preview" alt="Preview" src="$CF{'icondir'}$CK{'icon'}" $CF{'imgatt'}
 onclick="surfaceSample()"><br>
<label accesskey="z" for="surface" title="hyoZyo\n表情アイコンを選択します（使えれば）"
><span class="ak">Z</span>yo</label><select name="surface" id="surface"
 onchange="iconPreview(this.options[this.selectedIndex].value)" tabindex="50">
_HTML_
  if($CK{'icon'}=~/^((?:[^\/#]*\/)*)((?:[^\/#.]*\.)*?[^\/#.]+)(\.[^\/#.]*)?#(\d+)$/o){
    print qq(<option value="$1$2$3">-</option>\n);
    for(0..$4){print qq(<option value="$1$2$_$3">$_</option>\n);}
  }else{
    print qq(<option value="$CK{'icon'}">-</option>\n);
  }
  print<<"_HTML_";
</select><be>
<div style="margin:0.3em 0;text-align:center" title="reloadQ\n上フレームをリロードします"
>[<a href="$CF{'index'}?north" accesskey="q" tabindex="52"
>再読込(<span class="ak">Q</span>)</a>]
</td>
<th><label accesskey="n" for="name" title="Name\n参加者名、発言者名などで使う名前です"
>名前(<span class="ak">N</span>)</label>:</th>
<td><input type="text" name="name" id="name" maxlength="20" size="20"
 style="ime-mode:active;width:100px" value="$CK{'name'}" tabindex="11"></td>
<th><label accesskey="c" for="color" title="name Color\n参加者名、発言者名などで使う名前の色です"
>名前色(<span class="ak">C</span>)</label>:</th>
<td>@{[&iptcol('color','tabindex="21"')]}</td>
<th><label accesskey="g" for="line" title="log Gyosu\n表示するログの行数です\n最高$CF{'max'}行"
>ログ行数(<span class="ak">G</span>)</label>:</th>
<td><input type="text" name="line" id="line" maxlength="4" size="4"
 style="ime-mode:disabled;width:32px" value="$CK{'line'}行" tabindex="31"></td>
<td style="text-align:center"><input type="submit" accesskey="s" class="submit"
 title="Submit\n現在の内容で発言します" value="OK" tabindex="41"></td>
<td></td>
</tr>

<tr>
<th><label accesskey="i" for="icon" title="Icon\n使用するアイコンを選択します"
>アイコン(<span class="ak">I</span>)</label>:</th>
<td>@{[&iptico($CK{'icon'},'tabindex="12"')]}</td>
<th><label accesskey="c" for="bcolo" title="body Color\n発言した本文の色です"
>文章色(<span class="ak">C</span>)</label>:</th>
<td>@{[&iptcol('bcolo','tabindex="22"')]}</td>
<th><label accesskey="r" for="reload" title="Reload\n何秒ごとに自動的にリロードするか、です"
>更新間隔(<span class="ak">R</span>)</label>:</th>
<td><input type="text" name="reload" id="reload" maxlength="4" size="4"
 style="ime-mode:disabled;width:32px" value="$CK{'reload'}秒" tabindex="32"></td>
<td style="text-align:center"><input type="reset" class="reset"
 title="reset\n内容を初期化します" value="キャンセル" tabindex="42"></td>
</tr>

<tr>
<th><label accesskey="b" for="body" title="Body\n発言する本文の内容です"
>内容(<span class="ak">B</span>)</label>:</th>
<td colspan="5"><input type="text" name="body" id="body" maxlength="300" size="100"
 style="ime-mode:active;width:460px" tabindex="1"></td>
<td><label accesskey="k" for="cook" title="cooKie\nチェックを入れると現在の設定をCookieに保存します"
><input type="checkbox" name="cook" id="cook"
 class="check" tabindex="51" checked="checked">クッキ保存(<span class="ak">K</span>)</label></td>
</tr>

<tr>
<th><label accesskey="y" for="id" title="identitY name\nCGI内部で使用する、管理用の名前を選択します
この名前が実際に表に出ることはありません\nこの登録名が同じだと同一人物だとみなされます"
>登録名(<span class="ak">Y</span>)</label>:</th>
<td><input type="text" name="id" id="id" maxlength="20" size="20"
 style="ime-mode:active;width:150px" value="$CK{'id'}" tabindex="101"></td>
<th><label accesskey="l" for="email" title="e-maiL\nメールアドレスです"
>E-mai<span class="ak">l</span></label>:</th>
<td colspan="3"><input type="text" name="email" id="email" maxlength="200" size="40"
 style="ime-mode:inactive;width:200px" value="$CK{'email'}" tabindex="111"></td>
<th style="text-align:center">[ <a href="$CF{'sitehome'}" target="_top"
title="$CF{'sitename'}へ帰ります\n退室メッセージは出ないので帰りの挨拶を忘れずに"
>$CF{'sitename'}へ帰る</a> ]</th>
</tr>

<tr>
<th><label accesskey="m" for="cmd" title="coMmand\nコマンド"
>Co<span class="ak">m</span>mand</label>:</th>
<td><input type="text" name="cmd" id="cmd" maxlength="200" style="ime-mode:inactive;width:150px"
 value="$CK{'cmd'}" tabindex="102"></td>
<th><label accesskey="o" for="home" title="hOme\nサイトのURLです"
>H<span class="ak">o</span>me</label>:</th>
<td colspan="3"><input type="text" name="home" id="home" maxlength="200" size="40"
 style="ime-mode:inactive;width:200px" value="$CK{'home'}" tabindex="112"></td>
<th style="text-align:center">- <a href="http://www.airemix.com/" title="Airemixへいってみる"
>Marldia $CF{'version'}</a> -</th>
</tr>
</table>
</form>
</body>
</html>
_HTML_
  exit;
}


#-------------------------------------------------
# South
#
sub south{
  my@log=();
  my%MB;

  #表情アイコン
  if(($IN{'icon'}=~/^((?:[^\/#]*\/)*(?:[^\/#.]*\.)*?[^\/#.]+)(?:\.[^\/#.]*)?#\d+$/o)
   &&($IN{'surface'}=~/^$1\d*(?:\.[^\/#.]*)?$/o)){
    $IN{'icon'}=$IN{'surface'};
  }

  #クッキー書き込み
  if($IN{'cook'}){
    my$cook=&hashstr(\%IN,qw(id name color bcolo line reload icon email home cmd));
    #0-9A-Za-z\-\.\_
    $cook=~s{(\W)}{'%'.unpack('H2',$1)}ego;
    my$gmt=&datef(($^T+20000000),'gmt');
    print"Set-Cookie: Marldia=$cook; expires=$gmt\n";
  }

  #参加者・ランキング・書き込み処理
  sysopen(LOG,$CF{'log'},O_CREAT|O_RDWR)||die"Can't write log.";
  flock(LOG,LOCK_EX);
  #参加者読み込み
  while(<LOG>){
    /\S/o||last;
    /\bid=\t([^\t]+);\t(?:[^\t]*=\t[^\t]*;\t)*$/o||next;
    $MB{$1}=$_;
  }
  @log=grep{m/^Mar1=\t[^\t]*;\t(?:[^\t]*=\t[^\t]*;\t)*$/o}<LOG>;
  
  #自分のデータを追加
  if($IN{'name'}&&$ENV{'CONTENT_LENGTH'}){
    #能動的リロード
    delete$MB{"$IN{'ra'}"};
    $MB{"$IN{'id'}"}=&hashstr(\%IN,qw(id name color reload ra))."time=\t$^T;\texpire=\t$^T;\t\n";
  }elsif($IN{'name'}){
    #普通にリロード
    delete$MB{"$IN{'ra'}"};
    $MB{"$IN{'id'}"}=~m/\texpire=\t(\d+);\t/;
    $MB{"$IN{'id'}"}=&hashstr(\%IN,qw(id name color reload ra))."time=\t$^T;\texpire=\t$1;\t\n";
  }else{
    #ろむ
    $MB{"$IN{'ra'}"}="id=\t$IN{'ra'};\t".&hashstr(\%IN,qw(reload ra))."time=\t$^T;\t\n";
  }
  
  #参加者処理
  my@mb=();
  for(keys%MB){
    my%DT=($MB{"$_"}=~m/([^\t]*)=\t([^\t]*);\t/go);
    ($DT{'reload'}<20)&&($DT{'reload'}=20);
    (($DT{'time'}+($DT{'reload'}*6))<$^T)&&(delete$MB{$_},next);#TimeOver
    (exists$DT{'expire'})||(next);#ROM
    $DT{'expire'}=$^T-$DT{'expire'};
    push(@mb,qq[<a style="color:$DT{'color'}" title="$DT{'expire'}秒">$DT{'name'}</a>☆]);
  }

  if(length$IN{'body'}){
    #ランキング加点
    my%RK;
    sysopen(RANK,$CF{'rank'},O_CREAT|O_RDWR)||die"Can't write rank.";
    flock(RANK,LOCK_EX);
    while(<RANK>){
      /\bid=\t([^\t]+);\t(?:[^\t]*=\t[^\t]*;\t)*$/o||next;
      $RK{$1}=$_;
    }
    if($RK{"$IN{'id'}"}=~s/\texp=\t([^\t]*);\t/\texp=\t@{[$IN{'exp'}=$1+1]};\t/o){
      unless($RK{"$IN{'id'}"}=~s/\tname=\t([^\t]*);\t/\tname=\t$IN{'name'};\t/o){
        $RK{"$IN{'id'}"}=&hashstr(\%IN,qw(id name exp))."\n";
      }
    }else{
      $RK{"$IN{'id'}"}="id=\t$IN{'id'};\tname=\t$IN{'name'};\texp=\t1;\t\n";
      $IN{'exp'}=1;
    }
    truncate(RANK,0);
    seek(RANK,0,0);
    print RANK values%RK;
    close RANK;
    #発言処理
    my$data="Mar1=\t;\t".&hashstr(\%IN,qw(id name color bcolo body icon home email exp ua ra))."time=\t$^T;\t\n";
    splice(@log,$CF{'max'}-1);
    unshift(@log,$data);
  }elsif($IN{'del'}){
    #記事削除
    for(@log){
      (/\texp=\t$IN{'del'};\t/o&&/\tid=\t$IN{'id'};\t/o)||next;
      s/^(Mar1=\t)([^\t]*)(;\t)/$1del$3/o;
      last;
    }
  }
  truncate(LOG,0);
  seek(LOG,0,0);
  print LOG values%MB,"\n",@log;
  close(LOG);
  
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
    &header(qq(<meta http-equiv="refresh" content="$IN{'reload'};url=index.cgi?$query">\n));
  }else{
    &header;
  }
  my$member;
  if(@mb){
    $member="@mb";
  }else{
    my@wabi=(qw(かんこどり みてるだけ？ (-_☆)ｷﾗｰﾝ),"@{[('|_･)ﾁﾗ☆')x$audience]}");
    $member=$wabi[int(rand($#wabi+1))];
  }
  my$time=sprintf('%02d:%02d:%02d',(localtime$^T)[2,1,0]);
  print<<"_HTML_";
<table class="meminfo" summary="参加者情報など"><tr>
<td class="reload">[ <a href="index.cgi?$query">$time</a> ]</td>
<td class="member">[合計:$visitor人 参加者:$entrant人 観客:$audience人] [ $member ]</td>
<td class="respan">(<span>$IN{'reload'}秒間隔</span>)</td>
</tr></table>
_HTML_
  
  #ログ表示
  @log=splice(@log,0,$IN{'line'});
  for(@log){
    /^Mar1=\tdel;\t/o&&(next);
    my%DT=($_=~m/([^\t]*)=\t([^\t]*);\t/go);
    $DT{'date'}=&date($DT{'time'});
    
    #名前・メールアドレス・名前色
    if($DT{'email'}&&$DT{'color'}){
      $DT{'name'}=qq[<a href="mailto:$DT{'email'}" title="$DT{'email'}" style="color:$DT{'color'}">$DT{'name'}</a>];
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
    srand($DT{'exp'});
    $DT{'level'}=1+int(rand(sqrt$DT{'exp'}*2));
    
    my$del='';
    if(($IN{'id'})&&($DT{'id'}eq$IN{'id'})){
      $del=qq([<a href="$CF{'index'}?del=$DT{'exp'}&amp;$query">削除</a>]);
    }
    print<<"_HTML_";
<table cellspacing="0" class="article" summary="article">
<tr>
<th class="articon" rowspan="2"><img src="$CF{'icondir'}$DT{'icon'}" alt="$DT{'icon'}" $CF{'imgatt'}></th>
<th class="artname" nowrap>$DT{'name'}&nbsp;$DT{'home'}</th>
<td class="artbody" style="color:$DT{'bcolo'};">$DT{'body'}</td>
</tr>
<tr>
<td class="artdel">$del</td>
<td class="artinfo"><span class="artlev">Exp.$DT{'exp'}/Lv.$DT{'level'}</span>
<span class="artdate">$DT{'date'}</span></td>
</tr>
</table>
_HTML_
  }
  &footer;
  exit;
}


#-------------------------------------------------
# 管理
#
sub manage{
  unless($IN{'manage'}){
    die"「何もしない＠管理」";
  }
  #引数処理
  my@arg=grep{s/\\(\\)|\\(")|"/$1$2/go;s/\\"/"/go;$_;}($IN{'manage'}=~
  /([^"\\\ ]*(?:\\[^\ ][^"\\\ ]*)*(?:"[^"\\]*(?:\\.[^"\\]*)*(?:"[^"\\\ ]*(?:\\[^\ ][^"\\\ ]*)*)?)*\\?)/go);

=item 管理コマンド

$CF{'manpas'}='manage';なら、
#manage ...
で...というコマンドが発動

◇rank (del|cat|conv) [id ...]
 ランキングを表示
・del
 引数として指定されたIDの情報を削除
・cat
 第一引数のIDに、それ以降のIDを統合する
・conv
 1.5以前のランキングデータを1.6形式に変換する

◇mem
 参加者情報を表示

=cut

  #分岐
  if('rank'eq$arg[0]){
    #発言ランキング
    unless($arg[1]){
    }elsif('del'eq$arg[1]){
      #ランキングから削除
      sysopen(RANK,$CF{'rank'},O_CREAT|O_RDWR)||die"Can't write rank.";
      flock(RANK,LOCK_EX);
      my%RK=map{m/\bid=\t([^\t]+);\t/o;($1,$_)}(<RANK>);
      delete$RK{$arg[2]};
      truncate(RANK,0);
      seek(RANK,0,0);
      print RANK values%RK;
      close RANK;
    }elsif('cat'eq$arg[1]){
      #IDおよび経験地の統合
      sysopen(RANK,$CF{'rank'},O_CREAT|O_RDWR)||die"Can't write rank.";
      flock(RANK,LOCK_EX);
      my%RK=map{m/\bid=\t([^\t]+);\t/o;($1,$_)}(<RANK>);
      for(3..$#arg){
        my$exp=($RK{$arg[$_]}=~/\texp=\t([^\t]*);\t/o)?$1:next;
        $RK{$arg[2]}=~s/\texp=\t([^\t]*);\t/\texp=\t@{[$1+$exp]};\t/o;
        delete$RK{$arg[$_]};
      }
      truncate(RANK,0);
      seek(RANK,0,0);
      print RANK values%RK;
      close RANK;
    }elsif('conv'eq$arg[1]){
      sysopen(RANK,$CF{'rank'},O_CREAT|O_RDWR)||die"Can't write rank.";
      flock(RANK,LOCK_EX);
      my%RK=map{m/(.*)/o}(<RANK>);
      my$rank='';
      for(keys%RK){
        ('-f'ne$arg[2])&&($_=~/^id=/)&&(die"すでに変換済み？('rank conv -f'とすると強制的に変換します)");
        $RK{$_}=~s/\tpoint=\t/\texp=\t/;
        $rank.="id=\t$_;\t$RK{$_}\n";
      }
      truncate(RANK,0);
      seek(RANK,0,0);
      print RANK $rank;
      close RANK;
    }
    
    #ランキング表示
    &header;
    print<<'_HTML_';
<table summary="Ranking">
<caption>発言ランキング</caption>
_HTML_
    sysopen(RANK,$CF{'rank'},O_CREAT|O_RDONLY)||die"Can't read rank.";
    flock(RANK,LOCK_SH);
    print map{"<tr><td>$_</td></tr>"}grep{(m/(.*)/o)}<RANK>;#注意：IDも表示される
    close RANK;
    print"</table>";
    &footer;
    exit;
  }elsif('mem'eq$arg[0]){
    #見物人一覧
    &header;
    print<<"_HTML_";
<table summary="roms">
<caption>見物人一覧</caption>
_HTML_
    #参加者読み込み
    sysopen(LOG,$CF{'log'},O_CREAT|O_RDONLY)||die"Can't read log.";
    flock(LOG,LOCK_SH);
    while(<LOG>){
      /\S/o||last;
      /\bid=\t([^\t]+);\t(?:[^\t]*=\t[^\t]*;\t)*$/o||next;
      print"<tr><td>$_</td></tr>";
    }
    close LOG;
    print"</table>";
    &footer;
    exit;
  }elsif(''eq$arg[0]){
    #
  }elsif(''eq$arg[0]){
    #
  }elsif(''eq$arg[0]){
    #
  }else{
    #無効なコマンド
    die"\'$arg[0]\'はコマンドとしてとして認識されていません";
  }
  exit;
}



#------------------------------------------------------------------------------#
# Sub Routins
#
# main直下のサブルーチン群の補助

#-------------------------------------------------
# Form内容取得
sub getform{
  my$i;my%DT;
  unless($ENV{'REQUEST_METHOD'}){
  }elsif('HEAD'eq$ENV{'REQUEST_METHOD'}){ #forWWWD
#MethodがHEADならばLastModifedを出力して、
#最後の投稿時刻を知らせる
    my$last=&datef((stat("$CF{'log'}0.cgi"))[9],'last');
    print"Last-Modified: $last\n";
    print"Content-Type: text/plain\n\n";
    exit;
  }elsif('POST'eq$ENV{'REQUEST_METHOD'}){
    read(STDIN,$i,$ENV{'CONTENT_LENGTH'});
  }elsif('GET'eq$ENV{'REQUEST_METHOD'}){
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
      if('body'eq$i){
        $CF{'manpas'}&&($j=~/^[#＃]\s*$CF{'manpas'}\s+(.*)/o)&&($DT{'manage'}=$1,last);
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
      $j=~s/"/&#34;/go;
      $j=~s/&(#?\w+;)?/($1)?"&$1":'&#38;'/ego;
      $j=~s/'/&#39;/go;
      $j=~s/\x0D\x0A/<br>/go;$j=~s/\x0D/<br>/go;$j=~s/\x0A/<br>/go;
      $j=~s/(<br>)+$//o;
      $DT{$i}=$j;
    }
  }

  
  if((!%DT)||('frame'eq$DT{'mode'})){
    #フレーム
    $IN{'mode'}='frame';
  }elsif($DT{'manage'}){
    #管理コマンド
    $IN{'mode'}='manage';
    $IN{'manage'}=$DT{'manage'};
  }elsif($DT{'name'}){
    &getck;
    #http URL の正規表現
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
    #ftp URL の正規表現
    my$ftp_URL_regex =
   q{\bftp://(?:(?:[-_.!~*'()a-zA-Z0-9;&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*}.
   q{(?::(?:[-_.!~*'()a-zA-Z0-9;&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*)?@)?(?}.
   q{:(?:[a-zA-Z0-9](?:[-a-zA-Z0-9]*[a-zA-Z0-9])?\.)*[a-zA-Z](?:[-a-zA-}.
   q{Z0-9]*[a-zA-Z0-9])?\.?|[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)(?::[0-9]*)?}.
   q{(?:/(?:[-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*(?:/(?}.
   q{:[-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*)*(?:;type=[}.
   q{AIDaid])?)?(?:\?(?:[-_.!~*'()a-zA-Z0-9;/?:@&=+$,]|%[0-9A-Fa-f][0-9}.
   q{A-Fa-f])*)?(?:#(?:[-_.!~*'()a-zA-Z0-9;/?:@&=+$,]|%[0-9A-Fa-f][0-9A}.
   q{-Fa-f])*)?};
    #メールアドレスの正規表現改
    #"aaa@localhost"などはWWW上で「メールアドレス」として使うとは思えないので
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
   .q{^\x80-\xff])*\]))+};
    
    if(defined$DT{'body'}){
      #外部入力の汚染除去
      $DT{'body'}=~s{($http_URL_regex|$ftp_URL_regex|($mail_regex))}
      {<a href="@{[''ne$2?'mailto:':'']}$1" target="_blank">$1</a>}go;
      #自動リンクと誤解によるAタグ入力を補正する
      $DT{'body'}=~s{href=(&#3\d;)<a href="([^"]*\1&?)" target="_blank">\2</a>}{href=$1$2}go;
      $DT{'body'}=~s{(<a href=")([^"]*)&#60;/a&(" target="_blank">\2)&#60;/a&</a>#62;}{$1$2$3</a>&#60;/a&#62;}go;
      $IN{'body'}=($DT{'body'}=~/(.+)/o)?"$1":'';
      $IN{'cook'}=($DT{'cook'}=~/(.)/o)?'on':'0';
    }
    if(defined$DT{'del'}){
      (($DT{'del'}=~/(\d+)/o)&&(int$1))&&($IN{'del'}=int$1);
    }
    $IN{'name'}=($DT{'name'}=~/(.{1,100})/o)?"$1":'';
    $IN{'id'}=($DT{'id'}=~/(.{1,100})/o)?"$1":($CK{'id'}?$CK{'id'}:$IN{'name'});
    $IN{'color'}=($DT{'color'}=~/([\#\w\(\)\,]{1,20})/o)?"$1":'';
    $IN{'bcolo'}=($DT{'bcolo'}=~/([\#\w\(\)\,]{1,20})/o)?"$1":'';
    $DT{'email'}=($DT{'email'}=~/(.{1,200})/o)?"$1":'';
    $IN{'email'}=($DT{'email'}=~/($mail_regex)/o)?"$1":'';
    $DT{'home'}=($DT{'home'}=~/(.{1,200})/o)?"$1":'';
    $IN{'home'}=($DT{'home'}=~/($http_URL_regex)/o)?"$1":'';
    $IN{'icon'}=($DT{'icon'}=~/([\w\:\.\~\-\%\/\#]+)/o)?"$1":'';
    ($DT{'surface'}=~/([\w\.\~\-\%\/]+)/o)&&($IN{'surface'}="$1");
    $IN{'cmd'}=($DT{'cmd'}=~/(.+)/o)?"$1":undef;
    $IN{'line'}=(($DT{'line'}=~/(\d+)/o)&&(int$1))?int$1:$CF{'defline'};
    $IN{'reload'}=($DT{'reload'}=~/(\d+)/o)?int$1:$CF{'defreload'};
  }elsif((defined$DT{'north'})||('north'eq$DT{'mode'})){
    #北
    $IN{'mode'}='north';
    $IN{'line'}=$CF{'defline'};
    $IN{'reload'}=$CF{'defreload'};
  }elsif(defined$DT{'south'}){
    #南
    $IN{'mode'}='south';
    $IN{'line'}=$CF{'romline'};
    $IN{'reload'}=$CF{'romreload'};
  }
  $IN{'ra'}=($ENV{'REMOTE_ADDR'}=~/([\d\:\.]{2,56})/o)?"$1":'';
  $IN{'hua'}=($ENV{'HTTP_USER_AGENT'}=~/([^\t]+)/)?"$1":'';
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
    open(STDOUT,"| $CF{'gzip'} -c");
    print"<!-- gzip enable -->\n";
  }else{print"\n<!-- gzip disable -->\n";}
=cut
  print<<"_HTML_";

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" "http://www.w3.org/TR/REC-html40/loose.dtd">
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
<link rel="start" href="$CF{'sitehome'}">
<link rel="index" href="$CF{'index'}">
<link rel="help" href="$CF{'help'}">
<link rev="made" href="mailto:naruse\@airemix.com">
<title>$CF{'title'}</title>
</head>
<body>
_HTML_
}


#-------------------------------------------------
# フッター出力
#
sub footer{
  print<<"_HTML_";
<div class="AiremixCopy">- <a href="http://www.airemix.com/" target="_top" title="Airemix - Marldia -">Airemix Marldia</a><var>$CF{'version'}</var> -</div>
</body>
</html>
_HTML_
  exit;
}


#-------------------------------------------------
# ハッシュから「N=\tV;\t文字列」を取得する
#
sub hashstr{
  my$hash=shift@_;
  my$str='';
  for(@_){
    $str.="$_=\t$hash->{$_};\t";
  }
  return$str;
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
    %CK=($j=~/(\w+)=\t((?:$ascii|$twoBytes|$threeBytes)*);\t/go);
    last;
  }
  return%CK;
}


#-------------------------------------------------
# フォーマットされた日付取得を返す
sub datef{
=item 引数
$ time形式の時刻
;
$ 出力形式(gmt|last)
=cut
  unless($_[1]){
  }elsif($_[1]eq'gmt'){
   #Cookie用
    return sprintf("%s, %02d-%s-%d %s GMT",(split(/\s+/o,gmtime($_[0])))[0,2,1,4,3]);
  }elsif($_[1]eq'last'){
   #LastModified用
    return sprintf("%s, %02d %s %s %s GMT",(split(/\s+/o,gmtime($_[0])))[0,2,1,4,3]);
  }
  return&date;
}


#-------------------------------------------------
# 投稿日時表示用にフォーマットされた日付取得を返す
sub date{
=item 引数
$ time形式時刻
=cut
  my($sec,$min,$hour,$mday,$mon,$year,$wday)=localtime($_[0]);
  #sprintfの説明は、Perlの解説を見てください^^;;
  return sprintf("%4d年%02d月%02d日(%s) %02d時%02d分" #"1970年01月01日(木) 09時00分"の例
  ,$year+1900,$mon+1,$mday,('日','月','火','水','木','金','土')[$wday],$hour,$min);
#  return sprintf("%1d:%01d:%2d %4d/%02d/%02d(%s)" #"9:0: 0 1970/01/01(Thu)"の例
#  ,$hour,$min,$sec,$year+1900,$mon+1,$mday,('Sun','Mon','Tue','Wed','Thu','Fri','Sat')[$wday]);
}


#-------------------------------------------------
# アイコンリスト
#
sub iptico{
=item 引数
$ デフォルト指定にしたいアイコンファイル名を入れた書き換え可能な変数
;
$ SELECTタグに追加したい属性
$ 拡張コマンド
=cut
  my$opt='';
  ($_[1])&&($opt=" $_[1]");

=item 複数アイコンリスト
$CF{'icls'}の最初の一文字が' '（半角空白）だった場合複数リストモードになります
具体的な例を出すと、
・単一とみなされる例
'icon.txt'
'icon1.txt icon2.txt' #"icon1.txt icon2"というテキストファイルだとみなします
'"icon.txt" "exicon.txt"'
・複数とみなされる例
' "icon.txt" "exicon.txt"'
' "icon.txt" exicon.txt'
' icon.txt exicon.txt'
=cut

  if($CK{'iconlist'}&&('reset'ne$_[2])){
    #キャッシュである$CK{'iconlist'}を返す
    return$CK{'iconlist'};
  }
  
  
  #アイコンリスト読み込み
  my$list;
  if($CK{'cmd'}=~/\biconlist=nolist(;|$)/o){
   #`icon=nolist`でアイコンリストを読み込まない
  }elsif($CF{'icls'}=~/^ /o){
    #複数アイコンリスト読み込み
    for($CF{'icls'}=~/("(?:\\["\\]|\\\d{1,3}|.)*?"|\S+)/go){
      ($_)||(next);
      (sysopen(RD,"$_",O_RDONLY))||(die"Can't open multi-iconlist($_).");
      eval"flock(RD,LOCK_SH);";
      $list.=join('',<RD>);
      close(RD);
    }
  }else{
    #単一アイコンリスト読み込み
    (sysopen(RD,"$CF{'icls'}",O_RDONLY))||(die"Can't open single-iconlist.");
    eval"flock(RD,LOCK_SH);";
    $list=join('',<RD>);
    close(RD);
  }

  #選択アイコンの決定＋SELECTタグの中身
  if($CF{'exicon'}&&($CK{'cmd'}=~/\bicon=([^;]*)/o)&&$IC{$1}){
    #パスワード型
    $_[0]=$IC{$1};
    $list.=qq(<option value="$_[0]" selected>専用アイコン</option>\n);
  }elsif($CF{'exicfi'}&&($CK{'cmd'}=~/\b$CF{'exicfi'}=([^;]*)/o)){
    #ファイル指定型
    $_[0]=$1;
    $list.=qq(<option value="$_[0]" selected>ファイル指定</option>\n);
  }elsif($_[0]and$list=~s/(value="$_[0]")/$1 selected="selected"/io){
  }elsif($list=~s/value=(["'])(.+?)\1/value=$1$2$1 selected="selected"/io){
    $_[0]=$2;
  }
  
  $CK{'iconlist'}=<<"_HTML_";
<select name="icon" id="icon" onchange="iconChange(this.options[this.selectedIndex].value)"$opt>
$list</select>
_HTML_
  return$CK{'iconlist'};
}


#-------------------------------------------------
# カラーリスト読み込み
#
sub iptcol{

=item 引数

$_[0]: 'color'
$_[1]: 'tabindex=12'

=cut

  my$id='color';
  my$opt='';
  ($_[0])&&($id=$_[0]);
  ($_[1])&&($opt=" $_[1]");
  if('input'eq$CF{'colway'}){
    return<<"_HTML_";
<input type="text" name="$id" id="$id" class="blur" maxlength="20" style="ime-mode:disabled; width:90px;"
 onFocus="this.className='focus'" onBlur="this.className='blur'" value="$CK{$id}"$opt>
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
    if($CK{$id}&&$list=~s/(value=(["'])$CK{$id}\2)/$1 selected="selected"/io){
    }elsif($list=~s/value=(["'])(.+?)\1/value="$2" selected="selected"/io){
      $CK{$id}=$2;
    }
    return<<"_HTML_";
<select name="$id" id="$id"$opt>
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
Copyright &copy;2001 <a href="http://www.airemix.com/" title="Airemix">Airemix</a>. All rights reserved.</p>
</body>
</html>
_HTML_
  exit;
}

#-------------------------------------------------
# 初期設定
BEGIN{
  #Revision Number
  $CF{'correv'}=qq$Revision: 1.7 $;
  $CF{'version'}=($CF{'correv'}=~/(\d[\w\.]+)/o)?"v$1":'unknown';#"Revision: 1.4"->"v1.4"
  #エラーが出たらエラー画面を表示するように
  if($0 eq __FILE__){
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
+#  http://www.airemix.com/  #+
_HTML_
    exit;
    };
  }
}
1;
__END__
