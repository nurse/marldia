#!/usr/local/bin/perl

#------------------------------------------------------------------------------#
# 'Marldia' Chat System
# - Main Script -
#
# $Revision: 1.11 $
# "This file is written in euc-jp, CRLF." 空
# Scripted by NARUSE Yui.
#------------------------------------------------------------------------------#
# $cvsid = q$Id: core.cgi,v 1.11 2002-10-22 08:29:15 naruse Exp $;
require 5.004;
use strict;
use vars qw(%CF %IN %CK %IC);
$|=1;

#-------------------------------------------------
# MAIN SWITCH
#
sub main{
	&getParam;
	(" $IN{'name'} "=~m/ $CF{'denyname'} /o)&&(&locate($CF{'sitehome'}));
#	(" $ENV{'REMOT_ADDR'} "=~m/ $CF{'denyra'} /o)&&(&locate($CF{'sitehome'}));
#	(" $ENV{'REMOT_HOST'} "=~m/ $CF{'denyrh'} /o)&&(&locate($CF{'sitehome'}));
	
	if('south'eq$IN{'mode'}){
	}elsif('frame'eq$IN{'mode'}){
		&frame;
	}elsif('north'eq$IN{'mode'}){
		&north;
	}elsif('admicmd'eq$IN{'mode'}){
		&admicmd;
	}elsif('usercmd'eq$IN{'mode'}){
		&usercmd;
	}elsif('icct'eq$IN{'mode'}){
		require($CF{'icct'}?$CF{'icct'}:'iconctlg.cgi');
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

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd">
<HTML lang="ja-JP">
<HEAD>
<META http-equiv="Content-type" content="text/html; charset=euc-jp">
<META http-equiv="Content-Script-Type" content="text/javascript">
<META http-equiv="Content-Style-Type" content="text/css">
<META http-equiv="MSThemeCompatible" content="yes">
<LINK rel="start" href="$CF{'sitehome'}">
<LINK rel="index" href="$CF{'index'}">
<LINK rel="help" href="$CF{'help'}">
<TITLE>$CF{'title'}</TITLE>
</HEAD>
<FRAMESET rows="120,*">
	<FRAME frameborder="0" name="north" src="$CF{'index'}?north">
	<FRAME frameborder="0" name="south" src="$CF{'index'}?south">
	<NOFRAMES>
	<BODY>
	<PRE>
	このページはMicrosoft Internet Explorer 6.0 向けに作られています
	MSIE5.01やNetscape6、Mozilla0.9以上でもそこそこに見ることが出来ると思います
	Netscape4.xでは表示の一部が崩れる可能性があります
	テーブルやフレームに対応していないブラウザでは、表示の大部分が崩れてしまうため、
	実質的に閲覧することができません
	Mozilla4以上互換のブラウザでまた来てください
	</PRE>
	</BODY>
	</NOFRAMES>
</FRAMESET>
</HTML>
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
<SCRIPT type="text/javascript" defer>
<!--
//--------------------------------------
// 初期化
window.onload=autoreset;
var cook,body,preview,surface,popup;
_HTML_
	print"var icondir='$CF{'iconDir'}';",<<'_HTML_';

function autoreset(){
	if(document.all){
		cook=document.all('cook');
		body=document.all('body');
		preview=document.all('preview');
		surface=document.all('surface');
	}else if(document.getElementById){
		cook=document.getElementById('cook');
		body=document.getElementById('body');
		preview=document.getElementById('preview');
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
	preview.src=icondir+arg;
	preview.alt=arg;
}

//--------------------------------------
// アイコンを変えたら
function iconChange(arg){
	if(!surface&&!arg){return;}
	iconPreview(arg);
	if(!arg.match(/^(([^\/#]*\/)*[^\/#.]+)(\.[^\/#]*)#(\d+)(-\d+)?$/)){
		surface.length=1;
		surface.options[0].text='-';
		surface.options[0].value=arg;
		return;
	}
	var url=RegExp.$1;
	var ext=RegExp.$3;
	var str=RegExp.$5?parseInt(RegExp.$4):0;
	var end=RegExp.$5?-parseInt(RegExp.$5):parseInt(RegExp.$4);
	surface.length=end-str+2;
	surface.options[0].text='-';
	surface.options[0].value=url+ext;
	if(RegExp.$5)url=url.replace(/([1-9]\d*)$/,'');
	for(i=str;i<=end;i++){
		surface.options[i-str+1].text=i;
		surface.options[i-str+1].value=url+i+ext;
	}
}


//--------------------------------------
// 表情アイコン見本
function surfaceSample(e){
	if(document.all){
		e.returnValue=false;
	}else if(document.getElementById){
		e.preventDefault();
	}else{return false;}
	e.cancelBubble=true;
	if(!window.createPopup){return false;}
	event.cancelBubble=true;
	if(popup&&popup.isOpen){
		popup.hide();
		iconPreview(surface.value);
		body.focus();
		return false;
	}
	popup=window.createPopup();
	var wid=200;
	var hei=250;
	var str=
		'<BUTTON type="button" id="surface0" style="margin:0;padding:0;width:50px;border:0"'
		+' onclick="top.north.document.all(\'surface\').selectedIndex=0;document.all(\'surfaceS\').selectedIndex=0'
		+';top.north.document.images[\'preview\'].src=\''+icondir+surface.options[0].value+'\'"'
		+';top.north.document.images[\'preview\'].alt=\''+surface.options[0].value+'\'">'
		+'<IMG src="'+icondir+surface.options[0].value+'" alt="-"><\/button>';

	for(i=1;i<surface.length;i++){
		str+=
		'<BUTTON type="button" id="surface'+i+'" style="margin:0;padding:0;width:50px;border:0"'
		+' onclick="top.north.document.all(\'surface\').selectedIndex='+i+';document.all(\'surfaceS\').selectedIndex='+i
		+';top.north.document.images[\'preview\'].src=\''+icondir+surface.options[i].value+'\'"'
		+';top.north.document.images[\'preview\'].alt=\''+surface.options[i].value+'\'">'
		+'<IMG src="'+icondir+surface.options[i].value+'" alt="'+(i-1)+'"><\/button>';
		if(i%3==2){str+='<BR>';}
	}
	popup.document.body.innerHTML=
	 '<DIV style="border:3px double ActiveBorder;height:'+hei+'px;overflow:auto;text-align:left;width:'+wid+'px">'
	+'<DIV style="color:CaptionText;font:caption;height:15px;padding:2px;width:100%;'
	+'filter:progid:DXImageTransform.Microsoft.Gradient(startColorstr=\'#66aaff\',endColorstr=\'#ffffff\','
	+'gradientType=\'1\');">アイコン見本<\/div>'+str+'<SELECT name="surfaceS" id="surfaceS"'
	+' onchange="document.all(\'surface\'+this.selectedIndex).click()"'
	+' onkeypress="event.keyCode&#62;57&&top.north.document.images[\'preview\'].click()"'
	+' style="ime-mode:disabled">'+surface.innerHTML+'<\/select>'
	+'<INPUT type="button" value="Close" onclick="top.north.document.images[\'preview\'].click()"><\/div>';
	popup.show(20,20,wid,hei,top.south.document.body);
	popup.document.body.document.all('surfaceS').focus();
	return;
}
_HTML_
	print<<"_HTML_";
//-->
</SCRIPT>
<FORM name="north" id="north" method="post" action="$CF{'index'}" target="south"
 onsubmit="setTimeout(autoreset,20)" onreset="setTimeout(autoreset,20)">
<TABLE cellspacing="0" style="width:770px" summary="発言フォーム">
<COL style="width:130px">
<COL style="width: 60px">
<COL style="width:160px">
<COL style="width: 70px">
<COL style="width:130px">
<COL style="width: 55px">
<COL style="width: 45px">
<COL style="width:120px">

<TR>
<TD rowspan="5" style="text-align:center">
<H1 contentEditable="true">$CF{'pgtit'}</H1>
<BUTTON accesskey="x" type="button" style="height:55px;border:none;padding:0;margin:0;"
 onclick="surfaceSample(event)" onkeypress="surfaceSample(event)"><IMG name="preview" id="preview"
 alt="$CK{'icon'}" src="$CF{'iconDir'}$CK{'icon'}" $CF{'imgatt'} style="margin:0"></BUTTON><BR>
<LABEL accesskey="z" for="surface" title="hyoZyo\n表情アイコンを選択します（使えれば）"
><SPAN class="ak">Z</SPAN>yo</LABEL><SELECT name="surface" id="surface"
 onchange="iconPreview(this.options[this.selectedIndex].value)" tabindex="50">
_HTML_
	if($CK{'icon'}=~/^((?:[^\/#]*\/)*)((?:[^\/#.]*\.)*?[^\/#.]+)(\.[^\/#.]*)?#(\d+)$/o){
		print qq(<OPTION value="$1$2$3">-</OPTION>\n);
		for(0..$4){print qq(<OPTION value="$1$2$_$3">$_</OPTION>\n);}
	}else{
		print qq(<OPTION value="$CK{'icon'}">-</OPTION>\n);
	}
	print<<"_HTML_";
</SELECT><BR>
<DIV style="margin:0.3em 0;text-align:center" title="reloadQ\n上フレームをリロードします"
>[<A href="$CF{'index'}?north" accesskey="q" tabindex="52">再読込(<SPAN class="ak">Q</SPAN>)</A>]
</TD>
<TH><LABEL accesskey="n" for="name" title="Name\n参加者名、発言者名などで使う名前です"
>名前(<SPAN class="ak">N</SPAN>)</LABEL>:</TH>
<TD><INPUT type="text" name="name" id="name" maxlength="20" size="20"
 style="ime-mode:active;width:100px" value="$CK{'name'}" tabindex="11"></TD>
<TH><LABEL accesskey="c" for="color" title="name Color\n参加者名、発言者名などで使う名前の色です"
>名前色(<SPAN class="ak">C</SPAN>)</LABEL>:</TH>
<TD>@{[&iptcol('color','tabindex="21"')]}</TD>
<TH><LABEL accesskey="g" for="line" title="log Gyosu\n表示するログの行数です\n最高$CF{'max'}行"
>行数(<SPAN class="ak">G</SPAN>)</LABEL>:</TH>
<TD><INPUT type="text" name="line" id="line" maxlength="4" size="4"
 style="ime-mode:disabled;width:32px" value="$CK{'line'}行" tabindex="31"></TD>
<TD style="text-align:center"><INPUT type="submit" accesskey="s" class="submit"
 title="Submit\n現在の内容で発言します" value="OK" tabindex="41"></TD>
<TD></TD>
</TR>

<TR>
<TH><LABEL accesskey="i" for="icon" title="Icon\n使用するアイコンを選択します"
><A href="index.cgi?icct" target="south">アイコン</A>(<SPAN class="ak">I</SPAN>)</LABEL></TH>
<TD>@{[&iptico($CK{'icon'},'tabindex="12"')]}</TD>
<TH><LABEL accesskey="c" for="bcolo" title="body Color\n発言した本文の色です"
>文章色(<SPAN class="ak">C</SPAN>)</LABEL>:</TH>
<TD>@{[&iptcol('bcolo','tabindex="22"')]}</TD>
<TH><LABEL accesskey="r" for="reload" title="Reload\n何秒ごとに自動的にリロードするか、です"
>間隔(<SPAN class="ak">R</SPAN>)</LABEL>:</TH>
<TD><INPUT type="text" name="reload" id="reload" maxlength="4" size="4"
 style="ime-mode:disabled;width:32px" value="$CK{'reload'}秒" tabindex="32"></TD>
<TD style="text-align:center"><INPUT type="reset" class="reset"
 title="reset\n内容を初期化します" value="キャンセル" tabindex="42"></TD>
</TR>

<TR>
<TH><LABEL accesskey="b" for="body" title="Body\n発言する本文の内容です"
>内容(<SPAN class="ak">B</SPAN>)</LABEL>:</TH>
<TD colspan="5"><INPUT type="text" name="body" id="body" maxlength="300" size="100"
 style="ime-mode:active;width:450px" tabindex="1"></TD>
<TD><LABEL accesskey="k" for="cook" title="cooKie\nチェックを入れると現在の設定をCookieに保存します"
><INPUT type="checkbox" name="cook" id="cook" class="check" tabindex="51" checked="checked"
>クッキ保存(<SPAN class="ak">K</SPAN>)</LABEL></TD>
</TR>

<TR>
<TH><LABEL accesskey="y" for="id" title="identitY name\nCGI内部で使用する、管理用の名前を選択します
この名前が実際に表に出ることはありません\nこの登録名が同じだと同一人物だとみなされます"
>Identit<SPAN class="ak">y</SPAN></LABEL>:</TH>
<TD><INPUT type="text" name="id" id="id" maxlength="20" size="20"
 style="ime-mode:active;width:150px" value="$CK{'id'}" tabindex="101"></TD>
<TH><LABEL accesskey="l" for="email" title="e-maiL\nメールアドレスです"
>E-mai<SPAN class="ak">l</SPAN></LABEL>:</TH>
<TD colspan="3"><INPUT type="text" name="email" id="email" maxlength="200" size="40"
 style="ime-mode:inactive;width:200px" value="$CK{'email'}" tabindex="111"></TD>
<TH style="text-align:center">[ <A href="$CF{'sitehome'}" target="_top"
title="$CF{'sitename'}へ帰ります\n退室メッセージは出ないので帰りの挨拶を忘れずに"
>$CF{'sitename'}へ帰る</A> ]</TH>
</TR>

<TR>
<TH><LABEL accesskey="p" for="opt" title="oPtion\nオプション"
>O<SPAN class="ak">p</SPAN>tion</LABEL>:</TH>
<TD><INPUT type="text" name="opt" id="opt" maxlength="200" style="ime-mode:inactive;width:150px"
 value="$CK{'opt'}" tabindex="102"></TD>
<TH><LABEL accesskey="o" for="home" title="hOme\nサイトのURLです"
>H<SPAN class="ak">o</SPAN>me</LABEL>:</TH>
<TD colspan="3"><INPUT type="text" name="home" id="home" maxlength="200" size="40"
 style="ime-mode:inactive;width:200px" value="$CK{'home'}" tabindex="112"></TD>
<TH style="letter-cpacing:-1px;text-align:center">-<A href="http://www.airemix.com/" title="Airemixへいってみる"
>Marldia $CF{'version'}</A>-</TH>
</TR>
</TABLE>
</FORM>
</BODY>
</HTML>
_HTML_
	exit;
}


#-------------------------------------------------
# South
#
sub south{
	
	#---------------------------------------
	#引数の前処理
	
	#-----------------------------
	#コマンドとその調整
	my%EX;
	for(split(/;/o,$IN{'cmd'})){
		my($i,$j)=split('=',$_,2);
		$i||next;
		defined$j||($j=1);
		$EX{$i}=$j;
	}
	
	#-----------------------------
	#表情アイコン
	$IN{'icon'}=~/^(([^\/#]*\/)*[^\/#.]+)(\.[^\/#]*)#(\d+)(-\d+)?$/o
	&&$IN{'surface'}=~/^$1\d*(?:\.[^\/#.]*)?$/o
	&&($IN{'icon'}=$IN{'surface'});
	
	
	#-----------------------------
	#本文の処理
	#form->data変換
	if($CF{'tags'}&& 'ALLALL'eq$CF{'tags'}){
		#ALLALLは全面OK。但し強調は無効。URI自動リンクも無効。
		#自前でリンクを張ったり、強調してあるものを、二重にリンク・強調してしまいますから
	}else{
		#本文のみタグを使ってもいい設定にもできる
		my$attrdel=0;#属性を消す/消さない(1/0)
		my$str=$IN{'body'};
		study$str;
		$str=~s/&(#?\w+;)?/$1?"&$1":'&#38;'/ego;
		$str=~tr/"'<>/\01-\04/;
		
		#タグ処理
		if($CF{'tags'}&&!$EX{'notag'}){
			my$tags=$CF{'tags'};
			my%tagCom=map{m/(!\w+)(?:\(([^()]+)\))?/o;$1," $2 "||''}($tags=~/!\w+(?:\([^()]+\))?/go);
			if($tagCom{'!SELECTABLE'}){
				$tags.=' '.join(' ',grep{$tagCom{'!SELECTABLE'}=~/ $_ /o}grep{m/\w+/}split(/\s+/,$EX{'usetag'}));
			}elsif(defined$tagCom{'!SELECTABLE'}){
				$tags='\w+';
			}
			
			my$tag_regex_='[^\01-\04]*(?:\01[^\01]*\01[^\01-\04]*|\02[^\02]*\02[^\01-\04]*)*(?:\04|(?=\03)|$(?!\n))';
			my$comment_tag_regex='\03!(?:--[^-]*-(?:[^-]+-)*?-(?:[^\04-]*(?:-[^\04-]+)*?)??)*(?:\04|$(?!\n)|--.*$)';
			my$text_regex = '[^\03]*';
			my$result='';
			#もし BRタグや Aタグなど特定のタグだけは削除したくない場合には， 
			#$tag_tmp = $2; の後に，次のようにして $tag_tmp を $result に加えるようにすればできます． 
			#$result .= $tag_tmp if $tag_tmp =~ /^<\/?(BR|A)(?![\dA-Za-z])/i;
			my$remain=join('|',grep{m/^(?:\\w\+|\w+)$/o}split(/\s+/o,$tags));
			#逆に FONTタグや IMGタグなど特定のタグだけ削除したい場合には， 
			#$tag_tmp = $2; の後に，次のようにして $tag_tmp を $result に加えるようにすればできます． 
			#$result .= $tag_tmp if $tag_tmp !~ /^<\/?(FONT|IMG)(?![\dA-Za-z])/i;
			my$pos=length$str;
			while($str=~/\G($text_regex)($comment_tag_regex|\03$tag_regex_)?/gso){
				$pos=pos$str;
				length$1||length$2||last;
				$result.=$1;
				my$tag_tmp=$2;
				if($tag_tmp=~s/^\03((\/?(?:$remain))(?![\dA-Za-z]).*)\04/<$1>/io){
					$tag_tmp=~tr/\01\02/"'/;
					$result.=$attrdel?"<$2>":$tag_tmp;
				}else{
					$result.=$tag_tmp;
				}
				if($tag_tmp=~/^\03(XMP|PLAINTEXT|SCRIPT)(?![\dA-Za-z])/i){
					$str=~/(.*?)(?:\03\/$1(?![\dA-Za-z])$tag_regex_|$)/gsi;
					(my$tag_tmp=$1)=~tr/\01\02/"'/;
					$result.=$tag_tmp;
				}
			}
			$str=$result.substr($str,$pos);
		}else{
			#許可タグ無しorCommand:notag
		}
		
		#語句強調
		if($CF{'strong'}&&!$EX{'nostrong'}){
			my%ST=map{(my$str=$_)=~tr/"'<>/\01-\04/;$str}($CF{'strong'}=~/(\S+)\s+(\S+)/go);
			if($CF{'strong'}=~/^ /o){
				#拡張語句強調
				for(keys%ST){
					if($_=~/^\/(.+)\/$/o){
						my$regexp=$1;
						($ST{$_}=~s/^\/(.+)\/$/$1/o)?($str=~s[$regexp][$ST{$_}]gm)
						:($str=~s[$regexp][<STRONG  clAss="$ST{$_}"  >$1</STRONG>]gm);
					}elsif($ST{$_}=~s/^\/(.+)\/$/$1/o){
						$str=~s[^(\Q$_\E.*)$][$ST{$_}]gm;
					}else{
						$str=~s[^(\Q$_\E.*)$][<STRONG  clAss="$ST{$_}"  >$1</STRONG>]gm;
					}
				}
			}else{
				#基本語句強調
				for(keys%ST){$str=~s[^(\Q$_\E.*)$][<STRONG  clAss="$ST{$_}"  >$1</STRONG>]gm;}
			}
		}
		
		#URI自動リンク
		if($CF{'noautolink'}||!$EX{'noautolink'}){
			#[-_.!~*'()a-zA-Z0-9;:&=+$,]	->[!$&-.\w:;=~]
			#[-_.!~*'()a-zA-Z0-9:@&=+$,]	->[!$&-.\w:=@~]
			#[-_.!~*'()a-zA-Z0-9;/?:@&=+$,]	->[!$&-/\w:;=?@~]
			#[-_.!~*'()a-zA-Z0-9;&=+$,]		->[!$&-.\w;=~]
			#http URL の正規表現
			my$http_URL_regex =
		q{\b(?:https?|shttp)://(?:(?:[!$&-.\w:;=~]|%[\dA-Fa-f}.
		q{][\dA-Fa-f])*@)?(?:(?:[a-zA-Z\d](?:[-a-zA-Z\d]*[a-zA-Z\d])?\.)}.
		q{*[a-zA-Z](?:[-a-zA-Z\d]*[a-zA-Z\d])?\.?|\d+\.\d+\.\d+\.}.
		q{\d+)(?::\d*)?(?:/(?:[!$&-.\w:=@~]|%[\dA-Fa-f]}.
		q{[\dA-Fa-f])*(?:;(?:[!$&-.\w:=@~]|%[\dA-Fa-f][\dA-}.
		q{Fa-f])*)*(?:/(?:[!$&-.\w:=@~]|%[\dA-Fa-f][\dA-Fa-f}.
		q{])*(?:;(?:[!$&-.\w:=@~]|%[\dA-Fa-f][\dA-Fa-f])*)*)}.
		q{*)?(?:\?(?:[!$&-/\w:;=?@~]|%[\dA-Fa-f][\dA-Fa-f])}.
		q{*)?(?:#(?:[!$&-/\w:;=?@~]|%[\dA-Fa-f][\dA-Fa-f])*}.
		q{)?};
			#ftp URL の正規表現
			my$ftp_URL_regex =
		q{\bftp://(?:(?:[!$&-.\w;=~]|%[\dA-Fa-f][\dA-Fa-f])*}.
		q{(?::(?:[!$&-.\w;=~]|%[\dA-Fa-f][\dA-Fa-f])*)?@)?(?}.
		q{:(?:[a-zA-Z\d](?:[-a-zA-Z\d]*[a-zA-Z\d])?\.)*[a-zA-Z](?:[-a-zA-}.
		q{Z\d]*[a-zA-Z\d])?\.?|\d+\.\d+\.\d+\.\d+)(?::\d*)?}.
		q{(?:/(?:[!$&-.\w:=@~]|%[\dA-Fa-f][\dA-Fa-f])*(?:/(?}.
		q{:[!$&-.\w:=@~]|%[\dA-Fa-f][\dA-Fa-f])*)*(?:;type=[}.
		q{AIDaid])?)?(?:\?(?:[!$&-/\w:;=?@~]|%[\dA-Fa-f][\d}.
		q{A-Fa-f])*)?(?:#(?:[!$&-/\w:;=?@~]|%[\dA-Fa-f][\dA}.
		q{-Fa-f])*)?};
			#メールアドレスの正規表現改
			#"aaa@localhost"などを掲示板で「メールアドレス」として使うとは思えないので。
			my$mail_regex=
		q{(?:[^(\040)<>@,;:".\\\\\[\]\00-\037\x80-\xff]+(?![^(\040)<>@,;:".\\\\}
		.q{\[\]\00-\037\x80-\xff])|"[^\\\\\x80-\xff\n\015"]*(?:\\\\[^\x80-\xff][}
		.q{^\\\\\x80-\xff\n\015"]*)*")(?:\.(?:[^(\040)<>@,;:".\\\\\[\]\00-\037\x}
		.q{80-\xff]+(?![^(\040)<>@,;:".\\\\\[\]\00-\037\x80-\xff])|"[^\\\\\x80-}
		.q{\xff\n\015"]*(?:\\\\[^\x80-\xff][^\\\\\x80-\xff\n\015"]*)*"))*@(?:[^(}
		.q{\040)<>@,;:".\\\\\[\]\00-\037\x80-\xff]+(?![^(\040)<>@,;:".\\\\\[\]\0}
		.q{00-\037\x80-\xff])|\[(?:[^\\\\\x80-\xff\n\015\[\]]|\\\\[^\x80-\xff])*}
		.q{\])(?:\.(?:[^(\040)<>@,;:".\\\\\[\]\00-\037\x80-\xff]+(?![^(\040)<>@,}
		.q{;:".\\\\\[\]\00-\037\x80-\xff])|\[(?:[^\\\\\x80-\xff\n\015\[\]]|\\\\[}
		.q{^\x80-\xff])*\]))+};
		
			$str=~s{(?<!["'])($http_URL_regex|$ftp_URL_regex|($mail_regex))(?!["'])}
			{<A class="autolink" href="@{[$2?'mailto:':'']}$1" target="_blank">$1<\x2fA>}go;
		}else{
			#Command:nolink
		}
		
		#記事番号リンク「>>No.12-6」
		if($CF{'noartno'}||!$EX{'noartno'}){
			$str=~s{(\04\04No\.(\d+)(\-\d+)?)}{<A class="autolink" href="index.cgi?read=$2#art$2$3">$1</A>}go;
		}
		
		$str=~s/\01/&#34;/go;
		$str=~s/\02/&#39;/go;
		$str=~s/\03/&#60;/go;
		$str=~s/\04/&#62;/go;
		$IN{'body'}=$str;
	}
	$IN{'body'}=~s/\t/&nbsp;&nbsp;&nbsp;&nbsp;/go;
	$IN{'body'}=~s/\n+$//o;
	$IN{'body'}=~s/\n/<BR>/go;
	
	
	#-----------------------------
	#クッキー書き込み
	if($IN{'cook'}){
		my$cook=join('',map{"$_=\t$IN{$_};\t"}qw(id name color bcolo line reload icon email home opt));
		#0-9A-Za-z\-\.\_
		$cook=~s{(\W)}{'%'.unpack('H2',$1)}ego;
		my$gmt=&datef(($^T+20000000),'cookie');
		print"Set-Cookie: Marldia=$cook; expires=$gmt\n";
	}

	#---------------------------------------
	#参加者・ランキング・書き込み処理
	my@log=&Log::getArray;
	my%MB;
	for(&Mem::getArray){
		/\S/o||last;
		/\bid=\t([^\t]+);\t(?:[^\t]*=\t[^\t]*;\t)*$/o||next;
		$MB{$1}=$_;
	}

	#-----------------------------
	#自分のデータを追加
	$IN{'time'}=$^T;
	if($IN{'name'}&&$ENV{'CONTENT_LENGTH'}){
		#能動的リロード
		delete$MB{"$IN{'ra'}"};
		$IN{'expires'}=$^T;
		$MB{"$IN{'id'}"}=&enData(map{$_,$IN{$_}}qw(id name color reload ra time expires));
	}elsif($IN{'name'}){
		#普通にリロード
		delete$MB{"$IN{'ra'}"};
		$MB{"$IN{'id'}"}=~/\bexpires=\t(\d+);\t/o;
		$IN{'expires'}=$1;
		$IN{'reload'}&&($^T-$IN{'expires'}>300)&&($IN{'reload'}<280?($IN{'reload'}+=20):($IN{'reload'}=300));
		$MB{"$IN{'id'}"}=&enData(map{$_,$IN{$_}}qw(id name color reload ra time expires));
	}else{
		#ろむ
		$MB{"$IN{'ra'}"}=&enData(id=>$IN{'ra'},(map{$_,$IN{$_}}qw(reload ra time)));
		$IN{'reload'}+=20;
	}

	#-----------------------------
	#参加者処理
	my@mb=();
	for(keys%MB){
		my%DT=&deData($MB{"$_"});
		my$limit=$DT{'time'}+(abs($DT{'reload'}-40)<20?$DT{'reload'}*6:360);
		$limit<$^T&&(delete$MB{$_},next);#TimeOver
		exists$DT{'expires'}||next;#ROM
		$DT{'expires'}=$^T-$DT{'expires'};
		push(@mb,qq[<A style="color:$DT{'color'}" title="$DT{'expires'}秒">$DT{'name'}</A>☆]);
	}

	#-----------------------------
	#書き込み
	if(length$IN{'body'}){
		#-----------------------------
		#ランキング加点
		my%RK=&Rank::getHash;
		if($RK{"$IN{'id'}"}=~s/\texp=\t([^\t]*);\t/\texp=\t@{[$IN{'exp'}=$1+1]};\t/o){
			unless($RK{"$IN{'id'}"}=~s/\tname=\t([^\t]*);\t/\tname=\t$IN{'name'};\t/o){
				$RK{"$IN{'id'}"}=join('',map{"$_=\t$IN{$_};\t"}qw(id name exp))."\n";
			}
		}else{
			$RK{"$IN{'id'}"}="id=\t$IN{'id'};\tname=\t$IN{'name'};\texp=\t1;\t\n";
			$IN{'exp'}=1;
		}
		&Rank::clear(values%RK);
		&Rank::finish;
		#-----------------------------
		#発言処理
		my$data="Mar1=\t;\t"
		.join('',map{"$_=\t$IN{$_};\t"}qw(id name color bcolo body icon home email exp hua ra))."time=\t$^T;\t\n";
		splice(@log,$CF{'max'}-1);
		unshift(@log,$data);
	}elsif($IN{'del'}){
		#-----------------------------
		#発言削除
		for(@log){
			(/\texp=\t$IN{'del'};\t/o&&/\tid=\t$IN{'id'};\t/o)||next;
			s/^(Mar1=\t)([^\t]*)(;\t)/$1del$3/o;
			last;
		}
	}
	{
		#ログ書き
		my@mem=values%MB;
		&Log::clear(\@mem,\@log);
		&Log::finish;
	}

	#-----------------------------
	#ヘッダ出力
	my$query='south';
	if($IN{'id'}){
		$query=join('&amp;',map{my$val=$IN{$_};$val=~s{(\W)}{'%'.unpack('H2',$1)}ego;"$_=$val"}
		grep{$IN{$_}}qw(name id line reload color));
	}
	if($IN{'reload'}){
		&header(qq(<META http-equiv="refresh" content="$IN{'reload'};url=$CF{'index'}?$query">\n));
	}else{
		&header;
	}
	#-----------------------------
	#参加者表示
	my$member;
	my$visitor=scalar(keys%MB);
	my$entrant=$#mb+1;
	my$audience=$visitor-$entrant;
	if(@mb){
		$member="@mb";
	}else{
		my@wabi=(qw(かんこどり みてるだけ？ (-_☆)ｷﾗｰﾝ),"@{[('|_･)ﾁﾗ☆')x$audience]}");
		$member=$wabi[int(rand@wabi)];
	}
	print<<"_HTML_";
<TABLE class="meminfo" summary="参加者情報など"><TR>
<TD class="reload">[ <A href="$CF{'index'}?$query">@{[sprintf('%02d:%02d:%02d',(localtime$^T)[2,1,0])]}</A> ]</TD>
<TD class="member">[合計:$visitor人 参加者:$entrant人 観客:$audience人] [ $member ]</TD>
<TD class="respan">(<SPAN>$IN{'reload'}秒間隔</SPAN>)</TD>
</TR></TABLE>
_HTML_
	#-----------------------------
	#ログ表示
	@log=splice(@log,0,$IN{'line'});
	for(@log){
		/^Mar1=\tdel;\t/o&&(next);
		my%DT=&deData($_);
		
		#日付
		my$date=&date($DT{'time'});
		#名前・メールアドレス・名前色
		my$name=$DT{'email'}&&$DT{'color'}?
		qq[<A href="mailto:$DT{'email'}" title="$DT{'email'}" style="color:$DT{'color'}">$DT{'name'}</A>]
		:$DT{'email'}?qq[<A href="mailto:$DT{'email'}" title="$DT{'email'}">$DT{'name'}</A>]
		:$DT{'color'}?qq[<A style="color:$DT{'color'}">$DT{'name'}</A>]
		:$DT{'name'};
		#ホーム
		my$home=$DT{'home'}?qq[<A href="$DT{'home'}" target="_blank" title="$DT{'home'}">≫</A>]:'≫';
		#レベル計算-てきとー
		srand($DT{'exp'});
		$DT{'level'}=1+int(rand(sqrt$DT{'exp'}*2));
		#削除ボタン
		my$del=$IN{'id'}&&$DT{'id'}eq$IN{'id'}?qq([<A href="$CF{'index'}?del=$DT{'exp'}&amp;$query">削除</A>])
		:'&nbsp;';
		#出力
		print<<"_HTML_";
<TABLE cellspacing="0" class="article" summary="article">
<TR>
<TH class="articon" rowspan="2"><IMG src="$CF{'iconDir'}$DT{'icon'}" alt="$DT{'icon'}" $CF{'imgatt'}></TH>
<TH class="artname" nowrap>$name&nbsp;$home</TH>
<TD class="artbody" style="color:$DT{'bcolo'};">$DT{'body'}</TD>
</TR>
<TR>
<TD class="artdel">$del</TD>
<TD class="artinfo"><SPAN class="artlev">Exp.$DT{'exp'}/Lv.$DT{'level'}</SPAN>
<SPAN class="artdate">$date</SPAN></TD>
</TR>
</TABLE>
_HTML_
	}
	&footer;
	exit;
}


#-------------------------------------------------
# 利用者コマンド
#
sub usercmd{
	unless($IN{'usercmd'}){
		die"「何もしない＠管理」";
	}
	#引数処理
	my@arg=grep{s/\\(\\)|\\(")|"/$1$2/go;$_;}($IN{'usercmd'}=~
	/(?!\s)[^"\\\s]*(?:\\[^\s][^"\\\s]*)*(?:"[^"\\]*(?:\\.[^"\\]*)*(?:"[^"\\\s]*(?:\\[^\s][^"\\\s]*)*)?)*\\?/go);
=item 利用コマンド

◇rank
 ランキングを表示

◇mem
 参加者情報を表示

◇del <exp>
 発言削除

=cut

	#分岐
	if('rank'eq$arg[0]){
		#発言ランキング表示
		&header;
		print<<'_HTML_';
<TABLE summary="Ranking" width="300">
<CAPTION>発言ランキング</CAPTION>
_HTML_
		print map{"<TR><TD>$_->[0]</TD><TD>$_->[1]</TD></TR>"}
		map{[/\tname=\t([^\t]*);\t/o,/\texp=\t([^\t]*);\t/o]}&Rank::getOnlyArray;
		print"</TABLE>";
		&footer;
		exit;
	}elsif('mem'eq$arg[0]){
		#見物人一覧
		&header;
		print<<"_HTML_";
<TABLE summary="members" width="300">
<CAPTION>参加者一覧</CAPTION>
_HTML_
		#参加者読み込み
		for(&Mem::getOnlyArray){
			/\S/o||last;
			/\bname=\t([^\t]+);\t/o||next;
			print"<TR><TD>$1</TD></TR>";
		}
		print"</TABLE>";
		&footer;
		exit;
	}elsif(''eq$arg[0]){
		#
	}elsif(''eq$arg[0]){
		#
	}
	#無効なコマンド
	die"\'$arg[0]\'はコマンドとしてとして認識されていません";
	exit;
}


#-------------------------------------------------
# 管理コマンド
#
sub admicmd{
	unless($IN{'admicmd'}){
		die"「何もしない＠管理」";
	}
	#引数処理
	my@arg=grep{s/\\(\\)|\\(")|"/$1$2/go;$_;}($IN{'admicmd'}=~
	/(?!\s)[^"\\\s]*(?:\\[^\s][^"\\\s]*)*(?:"[^"\\]*(?:\\.[^"\\]*)*(?:"[^"\\\s]*(?:\\[^\s][^"\\\s]*)*)?)*\\?/go);

=item 管理コマンド

$CF{'admipass'}='admicmd';なら、
#admicmd ...
で...というコマンドが発動

◇rank (del|cat|conv) <id ...>
 ランキングを表示
・del
 引数として指定されたIDの情報を削除
・cat
 第一引数のIDに、それ以降のIDを統合する
・conv
 1.5以前のランキングデータを1.6形式に変換する

◇mem
 参加者情報を表示

◇del <id> <exp>
 発言削除

=cut

	#分岐
	if('rank'eq$arg[0]){
		#発言ランキング
		unless($arg[1]){
		}elsif('del'eq$arg[1]){
			#ランキングから削除
			my%RK=&Rank::getHash;
			delete$RK{$arg[2]};
			&Rank::clear(values%RK);
			&Rank::finish;
		}elsif('cat'eq$arg[1]){
			#IDおよび経験地の統合
			my%RK=&Rank::getHash;
			for(3..$#arg){
				my$exp=($RK{$arg[$_]}=~/\texp=\t([^\t]*);\t/o)?$1:next;
				$RK{$arg[2]}=~s/\texp=\t([^\t]*);\t/\texp=\t@{[$1+$exp]};\t/o;
				delete$RK{$arg[$_]};
			}
			&Rank::clear(values%RK);
			&Rank::finish;
		}elsif('conv'eq$arg[1]){
			my%RK=&Rank::getArray;
			for(keys%RK){
				('-f'ne$arg[2])&&($_=~/^id=/)&&(die"すでに変換済み？('rank conv -f'とすると強制的に変換します)");
				$RK{$_}=~s/\tpoint=\t/\texp=\t/;
				$RK{$_}="id=\t$_;\t$RK{$_}\n";
			}
			&Rank::clear(values%RK);
			&Rank::finish;
		}
		
		#ランキング表示
		&header;
		print<<'_HTML_';
<TABLE summary="Ranking" width="300">
<CAPTION>発言ランキング</CAPTION>
_HTML_
		print map{"<TR><TD>$_</TD></TR>"}&Rank::getOnlyArray;#注意：IDも表示される
		print"</TABLE>";
		&footer;
		exit;
	}elsif('mem'eq$arg[0]){
		#見物人一覧
		&header;
		print<<"_HTML_";
<TABLE summary="現在の参加者の一覧を表示します" width="300">
<CAPTION>参加者一覧</CAPTION>
_HTML_
		#参加者読み込み
		print map{"<TR><TD>$_</TD></TR>"}map{m/\bid=\t([^\t]+);\t(?:[^\t]*=\t[^\t]*;\t)*$/o}&Mem::getOnlyArray;
		print"</TABLE>";
		&footer;
		exit;
	}elsif('del'eq$arg[0]){
		#発言削除
		
		my@log=&Log::getArray;
		for(@log){
			(/\texp=\t$arg[2];\t/o&&/\tid=\t$arg[1];\t/o)||next;
			s/^(Mar1=\t)([^\t]*)(;\t)/$1del$3/o;
			last;
		}
		&Log::clear(undef,\@log);
		&Log::finish;
		&header;
		print"<P>削除しましたょ</P>";
		&footer;
	}elsif(''eq$arg[0]){
		#
	}elsif(''eq$arg[0]){
		#
	}
	#無効なコマンド
	die"\'$arg[0]\'はコマンドとしてとして認識されていません";
	exit;
}


#-------------------------------------------------
# Locationで転送
#
sub locate{
	my$i;
	if($_[0]=~/^http:/){
		$i=$_[0];
	}elsif($_[0]=~/\?/){
		$i=sprintf('http://%s%s/',$ENV{'SERVER_NAME'},
		substr($ENV{'SCRIPT_NAME'},0,rindex($ENV{'SCRIPT_NAME'},'/')));
		$i.=sprintf('%s?%s',$_[0]);
	}elsif('/'eq$_[0]){
		$i='http://'.$ENV{'SERVER_NAME'}.'/';
	}elsif($_[0]){
		$i=sprintf('http://%s%s/',$ENV{'SERVER_NAME'},
		substr($ENV{'SCRIPT_NAME'},0,rindex($ENV{'SCRIPT_NAME'},'/')));
		$i.=$_[0];
	}
	print<<"_HTML_";
Status: 303 See Other
Content-type: text/html; charset=euc-jp
Content-Language: ja-JP
Pragma: no-cache
Cache-Control: no-cache
Location: $i

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN"> 
<HTML>
<HEAD>
<META http-equiv="Refresh" content="0;URL=$i">
<TITLE>303 See Ohter</TITLE>
</HEAD>
<BODY>
<H1>: Marldia :</H1>
<P>And, please go <A href="$i">here</A>.</P>
<P>Location: $i</P>
<P>Marldia <VAR>$CF{'correv'}</VAR>.<BR>
Copyright &#169;2001,2002 <A href="http://www.airemix.com/" target="_blank" title="Airemix">Airemix</A>. All rights reserved.</P>
</BODY>
</HTML>
_HTML_
	exit;
}



#------------------------------------------------------------------------------#
# Sub Routins
#
# main直下のサブルーチン群の補助

#-------------------------------------------------
# Form内容取得
#
sub getParam{
	my$param;
	my@param;
	#引数取得
	unless($ENV{'REQUEST_METHOD'}){
		@param=@ARGV;
	}elsif('HEAD'eq$ENV{'REQUEST_METHOD'}){ #forWWWD
#MethodがHEADならばLastModifedを出力して、
#最後の投稿時刻を知らせる
		my$last=&datef((stat("$CF{'log'}0.cgi"))[9],'rfc1123');
		print"Status: 200 OK\nLast-Modified: $last\n"
		."Content-Type: text/plain\n\nLast-Modified: $last";
		exit;
	}elsif('POST'eq$ENV{'REQUEST_METHOD'}){
		read(STDIN,$param,$ENV{'CONTENT_LENGTH'});
	}elsif('GET'eq$ENV{'REQUEST_METHOD'}){
		$param=$ENV{'QUERY_STRING'};
	}
	
	# EUC-JP文字
	my$eucchar=qr((?:
		[\x09\x0A\x0D\x20-\x7E]			# 1バイト EUC-JP文字改
		|(?:[\x8E\xA1-\xFE][\xA1-\xFE])	# 2バイト EUC-JP文字
		|(?:\x8F[\xA1-\xFE]{2})			# 3バイト EUC-JP文字
	))x;
	
	#引数をハッシュに
	if(length$param>262114){ # 262114:引数サイズの上限(byte)
		#サイズ制限
		&showHeader;
		print"いくらなんでも量が多すぎます\n$param";
		&footer;
		exit;
	}elsif(length$param>0){
		#入力を展開
		@param=split(/[&;]/o,$param);
	}
	undef$param;

	#入力を展開してハッシュに入れる
	my%DT;
	while(@param){
		my($i,$j)=split('=',shift(@param),2);
		defined$j||($DT{$i}='',next);
		$i=($i=~/(\w+)/o)?$1:'';
		study$j;
		$j=~tr/+/\ /;
		$j=~s/%([\dA-Fa-f]{2})/pack('H2',$1)/ego;
		$j=($j=~/($eucchar*)/o)?$1:'';
		#メインフレームの改行は\x85らしいけど、対応する必要ないよね？
		$j=~s/\x0D\x0A/\n/go;$j=~tr/\r/\n/;
		if('body'ne$i){
			#本文以外は全面タグ禁止
			$j=~s/\t/&nbsp;&nbsp;&nbsp;&nbsp;/go;
			$j=~s/&(#?\w+;)?/$1?"&$1":'&#38;'/ego;
			$j=~s/"/&#34;/go;
			$j=~s/'/&#39;/go;
			$j=~s/</&#60;/go;
			$j=~s/>/&#62;/go;
			$j=~s/\n/<BR>/go;
			$j=~s/(<BR>)+$//o;
		}#本文は後でまとめて
		$DT{$i}=$j;
	}
	
	#引数の汚染除去
	$IN{'ra'}=($ENV{'REMOTE_ADDR'}&&$ENV{'REMOTE_ADDR'}=~/([\d\:\.]{2,56})/o)?"$1":'';
	$IN{'hua'}=($ENV{'HTTP_USER_AGENT'}&&$ENV{'HTTP_USER_AGENT'}=~/($eucchar+)/o)?"$1":'';
	$IN{'hua'}=~tr/\x09\x0A\x0D/\x20\x20\x20/;
	
	#コマンド系
	if($IN{'body'}){
		if($CF{'admipass'}&&($IN{'body'}=~/^#$CF{'admipass'}\s+(.*)/o){
			$DT{'admicmd'}=$1;
		}elsif($IN{'body'}=~/^\$(\w.*)/o){
			$DT{'usercmd'}=$1;
		}
	}
	
	if(!%DT||'frame'eq$DT{'mode'}){
		#フレーム
		$IN{'mode'}='frame';
	}elsif($DT{'admicmd'}&&!$DT{'nocmd'}){
		#管理コマンド
		$IN{'mode'}='admicmd';
		$IN{'admicmd'}=$DT{'admicmd'};
	}elsif($DT{'usercmd'}&&!$DT{'nocmd'}){
		#利用コマンド
		$IN{'mode'}='usercmd';
		$IN{'usercmd'}=$DT{'usercmd'};
	}elsif(defined$DT{'icct'}){
		#アイコンカタログ
		$IN{'mode'}='icct';
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
			$IN{'body'}=$DT{'body'};
			$IN{'cook'}=($DT{'cook'}=~/(.)/o)?'on':'0';
		}
		if(defined$DT{'del'}){
			$IN{'del'}=$1 if$DT{'del'}=~/([1-9]\d*)/o;
		}
		$IN{'name'}=($DT{'name'}=~/(.{1,100})/o)?$1:'';
		$IN{'id'}=($DT{'id'}=~/(.{1,100})/o)?$1:($CK{'id'}||$IN{'name'});
		$IN{'color'}=($DT{'color'}=~/([\#\w\(\)\,]{1,20})/o)?$1:'';
		$IN{'bcolo'}=($DT{'bcolo'}=~/([\#\w\(\)\,]{1,20})/o)?$1:'';
		$DT{'email'}=($DT{'email'}=~/(.{1,200})/o)?$1:'';
		$IN{'email'}=($DT{'email'}=~/($mail_regex)/o)?$1:'';
		$DT{'home'}=($DT{'home'}=~/(.{1,200})/o)?$1:'';
		$IN{'home'}=($DT{'home'}=~/($http_URL_regex)/o)?$1:'';
		$IN{'icon'}=($DT{'icon'}=~/([\w\:\.\~\-\%\/\#]+)/o)?$1:'';
		$IN{'surface'}=$1 if$DT{'surface'}=~/([\w\.\~\-\%\/]+)/o;
		$IN{'opt'}=$1 if$DT{'opt'}=~/(.+)/o;
		$IN{'line'}=(int($DT{'line'})=~/([1-9]\d*)/o)?$1:$CF{'defline'};
		$IN{'reload'}=(int($DT{'reload'})=~/(\d+)/o)?$1:$CF{'defreload'};
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
	return%IN;
}


#-------------------------------------------------
# Header with G-ZIP etc.
#
sub header{
	print<<'_HTML_';
Content-type: text/html; charset=euc-jp
Content-Language: ja-JP
Pragma: no-cache
Cache-Control: no-cache
_HTML_
	#GZIP Switch
	if($CF{'gzip'}&&$ENV{'HTTP_ACCEPT_ENCODING'}&&(index($ENV{'HTTP_ACCEPT_ENCODING'},'gzip')>-1)){
		print"Content-encoding: gzip\n\n";
		if(!open(STDOUT,"|$CF{'gzip'} -cfq9")){
			#GZIP失敗時のエラーメッセージ
			binmode STDOUT;
			print unpack("u",#GZIP圧縮-uuencodeされたエラーメッセージ
			q|M'XL(``3U_#P""UV134O#0!"&[X'\AR45HBUM$&]I(TBIXD&4>O-20KJTD>;#|.
			q|M[=96Q1\3F;0'*WCQHUJD%*W%0/'@R8OB2>RA$$$\FDU$U+GL[KS/O#/,9@Q,|.
			q|M552FU$[BK9J^K0A9RZ38I$FZ8V,!:=%+$2AN4*E,C4H::6655#%5<$U+;MK"|.
			q|M/,]E;(*#`T4ARVA%)96BK@;7,!M'.4(L@M8U@K&)9E-S:-HJ%&8L24)QGN.Y|.
			q|M7#Z_FI<1RJJF2%&MBM'2QO(:4FDP`,$IK:0SZOST^--IA1*T>R=7$_"Z_<X#|.
			q|MW,(1#`#@#H!A_?N+#Z?%<TXS)/W+(4R8!J_0!`\Z,`XT1S>+N,&<!R\P"L%1|.
			q|M[^GZ#7R>F\HN[HFE7=T6]Q513#,:AM]UWY[_NH__>KMG;L<=N,_@,1?P77#?|.
			q|M@\S0Z;ICQL"A<\"X7XW`OVGW'L$+9PAM>"X1BQ:ZH!-LZ(V?K8812T0`^SM9|.
			q|6DNKU>DJ-N)1F&5($?`$-3&-TWP$`````|);
			exit;
		}
		#GZIP圧縮転送をかけられるときはかける
		$ENV{'HTTP_USER_AGENT'}&&(index($ENV{'HTTP_USER_AGENT'},'MSIE')>-1)&&(print ' 'x 2048); #IEのバグ対策
		print"<!-- gzip enable -->";
	}else{
		print"\n<!-- gzip disable -->";
	}
	print<<"_HTML_";

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<!--DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"-->
<HTML lang="ja-JP">
<HEAD>
<META http-equiv="Content-type" content="text/html; charset=euc-jp">
<META http-equiv="Content-Script-Type" content="text/javascript">
<META http-equiv="Content-Style-Type" content="text/css">
_HTML_

print"$_[0]"if$_[0];

	print<<"_HTML_";
<LINK rel="stylesheet" type="text/css" href="$CF{'style'}" media="screen,print" title="DefaultStyle">
<LINK rel="start" href="$CF{'sitehome'}">
<LINK rel="index" href="$CF{'index'}">
<LINK rel="help" href="$CF{'help'}">
<TITLE>$CF{'title'}</TITLE>
</HEAD>
<BODY>
_HTML_
}


#-------------------------------------------------
# フッター出力
#
sub footer{
	print<<"_HTML_";
<DIV class="AiremixCopy">- <A href="http://www.airemix.com/" target="_top" title="Airemix - Marldia -">Airemix Marldia</A><VAR title="times:@{[times]}">$CF{'version'}</VAR> -</DIV>
</BODY>
</HTML>
_HTML_
	exit;
}


#-------------------------------------------------
# Cookieを取得する
#
sub getck{
	$ENV{'HTTP_COOKIE'}||return undef;
	# EUC-JP文字
	my$eucchar=qr((?:
		[\x0A\x0D\x20-\x7E]			# 1バイト EUC-JP文字改-\x09
		|(?:[\x8E\xA1-\xFE][\xA1-\xFE])	# 2バイト EUC-JP文字
		|(?:\x8F[\xA1-\xFE]{2})			# 3バイト EUC-JP文字
	))x;
	for(split('; ',$ENV{'HTTP_COOKIE'})){
		my($i,$j)=split('=',$_,2);
		'Marldia'eq$i||next;
		$j=~s/%([0-9A-Fa-f]{2})/pack('H2',$1)/ego;
		%CK=($j=~/(\w+)=\t($eucchar*);\t/go);
		last;
	}
	return%CK;
}


#-------------------------------------------------
# フォーマットされた日付取得を返す
#
sub datef{
=item 引数
$ time形式の時刻
;
$ 出力形式(cookie|last)
=cut
	my$time=shift();
	my$type=shift();
	unless($type){
	}elsif('cookie'eq$type){
	# Netscape風Cookie用
		return sprintf("%s, %02d-%s-%d %s GMT",(split(/\s+/o,gmtime$time))[0,2,1,4,3]);
	}elsif('rfc1123'eq$type){
	# RFC1123 主としてLastModified用
		return sprintf("%s, %02d %s %d %s GMT",(split(/\s+/o,gmtime$time))[0,2,1,4,3]);
	}elsif('dateTime'eq$type){
	# ISO 8601 dateTime (CCYY-MM-DDThh:mm:ss+09:00)
		$CF{'timezone'}||&cfgTimeZone($ENV{'TZ'});
		my($sec,$min,$hour,$day,$mon,$year,$wday)=gmtime($time+$CF{'timeOffset'});
		return sprintf("%04d-%02d-%02dT%02d:%02d:%02d+09:00",$year+1900,$mon+1,$day,$hour,$min,$sec,$CF{'timezone'});
	}
	return&date($time);
}


#-------------------------------------------------
# タイムゾーンの取得
sub cfgTimeZone{
=pod
タイムゾーンを環境変数TZから取得して、%CFに設定する
他の関数はこの$CF{'timezone'},$CF{'timeOffset'}を使って、
gmtime()から確実に希望の地域の時刻を算出できる
=item 引数
$ $ENV{'TZ'}
=cut
	my$envtz=shift();
	if($CF{'timezone'}&&$CF{'TZ'}eq$envtz){
		#note. $CF{'timezone'}= EastPlus TimeZone <-> ENV-TZ= EastMinus TimeZone
	}elsif(!$envtz||'Z'eq$envtz||'UTC'eq$envtz||'GMT'eq$envtz){
		$CF{'timezone'}='Z';$CF{'timeOffset'}=0;
	}elsif($envtz=~/([a-zA-Z]*)-(\d+)(:\d+)?/o){
		$CF{'timezone'}=sprintf("+%02d:%02d",$2?$2:0,$3?$3:0);
		$CF{'timeOffset'}=($2?$2*3600:0)+($3?$3*60:0);
	}elsif($envtz=~/([a-zA-Z]*)+?(\d+)(:\d+)?/o){
		$CF{'timezone'}=sprintf("-%02d:%02d",$2?$2:0,$3?$3:0);
		$CF{'timeOffset'}=-($2?$2*3600:0)-($3?$3*60:0);
	}else{
		$CF{'timezone'}='Z';$CF{'timeOffset'}=0;
	}
	$CF{'TZ'}=$envtz;
	return$CF{'timeOffset'};
}


#-------------------------------------------------
# 投稿日時表示用にフォーマットされた日付取得を返す
#
sub date{
=item 引数
$ time形式時刻
=cut
	my($sec,$min,$hour,$mday,$mon,$year,$wday)=localtime($_[0]);
	#sprintfの説明は、Perlの解説を見てください^^;;
	return sprintf("%4d年%02d月%02d日(%s) %02d時%02d分" #"1970年01月01日(木) 09時00分"の例
	,$year+1900,$mon+1,$mday,('日','月','火','水','木','金','土')[$wday],$hour,$min);
#	return sprintf("%1d:%01d:%2d %4d/%02d/%02d(%s)" #"9:0: 0 1970/01/01(Thu)"の例
#	,$hour,$min,$sec,$year+1900,$mon+1,$mday,('Sun','Mon','Tue','Wed','Thu','Fri','Sat')[$wday]);
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

=item 複数アイコンリスト
$CF{'iconList'}の最初の一文字が' '（半角空白）だった場合複数リストモードになります
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

	if($CK{'cacheIconList'}&&('reset'ne$_[2])){
		#キャッシュである$CK{'cacheIconList'}を返す
		return$CK{'cacheIconList'};
	}
	my$opt=$_[1]?" $_[1]":'';
	
	#アイコンリスト読み込み
	my$list;
	if($CK{'opt'}=~/\biconlist=nolist(;|$)/o){
	 #`icon=nolist`でアイコンリストを読み込まない
	}elsif($CF{'iconList'}=~/^ /o){
		#複数アイコンリスト読み込み
		for($CF{'iconList'}=~/("(?:\\["\\]|\\\d{1,3}|.)*?"|\S+)/go){
			($_)||(next);
			open(LIST,"<$_")||die"Can't read multi-iconlist($_)[$!]";
			eval{flock(LIST,1)};
			$list.=join('',<LIST>);
			close(LIST);
		}
	}else{
		#単一アイコンリスト読み込み
		open(LIST,"<$CF{'iconList'}")||(die"Can't open single-iconlist($CF{'iconList'})[$!]");
		eval{flock(LIST,1)};
		$list=join('',<LIST>);
		close(LIST);
	}

	#選択アイコンの決定＋SELECTタグの中身
	if($CF{'exicon'}&&($CK{'opt'}=~/\bicon=([^;]*)/o)&&$IC{$1}){
		#パスワード型
		$_[0]=$IC{$1};
		$list.=qq(<OPTION value="$_[0]" selected>専用アイコン</OPTION>\n);
	}elsif($CF{'exicfi'}&&($CK{'opt'}=~/\b$CF{'exicfi'}=([^;]*)/o)){
		#ファイル指定型
		$_[0]=$1;
		$list.=qq(<OPTION value="$_[0]" selected>ファイル指定</OPTION>\n);
	}elsif($_[0]and$list=~s/(value="$_[0]")/$1 selected="selected"/i){
	}elsif($list=~s/value=(["'])(.+?)\1/value=$1$2$1 selected="selected"/io){
		$_[0]=$2;
	}
	
	$CK{'cacheIconList'}=<<"_HTML_";
<SELECT name="icon" id="icon" onchange="iconChange(this.value)"$opt>
$list</SELECT>
_HTML_
	return$CK{'cacheIconList'};
}


#-------------------------------------------------
# カラーリスト読み込み
#
sub iptcol{

=item 引数

$_[0]: 'color'
$_[1]: 'tabindex=12'

=cut

	my$id=$_[0]?$_[0]:'color';
	my$opt=$_[1]?" $_[1]":'';
	if('input'eq$CF{'colway'}){
		return<<"_HTML_";
<INPUT type="text" name="$id" id="$id" class="blur" maxlength="20" style="ime-mode:disabled; width:90px;"
 onFocus="this.className='focus'" onBlur="this.className='blur'" value="$CK{$id}"$opt>
_HTML_
	}else{
		my$list=$CF{'colorList'};
		if($CK{$id}&&$list=~s/(value=(["'])$CK{$id}\2)/$1 selected="selected"/i){
		}elsif($list=~s/value=(["'])(.+?)\1/value="$2" selected="selected"/io){
			$CK{$id}=$2;
		}
		return<<"_HTML_";
<SELECT name="$id" id="$id"$opt>
$list</SELECT>
_HTML_
	}
}



#-------------------------------------------------
# ログ形式（に｜から）データを変換
#
sub enData{
	my$tmp;
	while(my($key,$val)=splice@_,0,2){$tmp.="$key=\t$val;\t";}
	return $tmp;
}
sub deData{
	return $_[0]=~/([^\t]*)=\t([^\t]*);\t/go;
}


#------------------------------------------------------------------------------#
# ChatLog Class
#
package Log;
{
	my$fh;
	my$path=$::CF{'log'};
	my@log;
	my@mem;
	#リストを返す
	sub getArray{
		my@tmp=&MFile::getArray($fh,$path);
		while(my$line=shift@tmp){$line=~/\S/o||last;push(@mem,$line);}
		@log=grep{m/^Mar1=\t[^\t]*;\t(?:[^\t]*=\t[^\t]*;\t)*$/o}@tmp;
		return@log
	}
	#読み込み専用で開いてリストを返す
	sub getOnlyArray{
		my@tmp=&MFile::getOnlyArray($fh,$path);
		while(shift@tmp){/\S/o||last;push(@mem,$_);}
		@log=grep{m/^Mar1=\t[^\t]*;\t(?:[^\t]*=\t[^\t]*;\t)*$/o}@tmp;
		return@log
	}
	#参加者リストを返す
	sub getMemArray{@mem||&getArray;return@mem;}
	#読み込み専用で開いて参加者リストを返す
	sub getOnlyMemArray{@mem||&getOnlyArray;return@mem;	}
	#クリアして引数を書き込む
	sub clear{
		@mem=@{$_[0]}if$_[0];
		@log=@{$_[1]}if$_[1];
		&MFile::clear($fh,@mem,"\n",@log);
	}
	#close
	sub finish{return&MFile::finish($fh);undef$fh;undef@mem;undef@log;}
}
#------------------------------------------------------------------------------#
# MEMBER CLASS
#
package Mem;
{
	#リストを返す
	sub getArray{return&Log::getMemArray;}
	#読み込み専用で開いてリストを返す
	sub getOnlyArray{return&Log::getOnlyMemArray;}
	#ハッシュを返す
	sub getHash{return map{m/\bid=\t([^\t]+);\t/o;($1,$_)}&getArray;}
	#読み込み専用で開いてハッシュを返す
	sub getOnlyHash{my@tmp=map{m/\bid=\t([^\t]+);\t/o;($1,$_)}&getOnlyArray;&finish;return@tmp;}
	#close
	sub finish{return&Log::finish;}
}
#------------------------------------------------------------------------------#
# RANKING CLASS
#
package Rank;
{
	my$fh;
	my$path=$::CF{'rank'};
	#リストを返す
	sub getArray{return&MFile::getArray($fh,$path);}
	#読み込み専用で開いてリストを返す
	sub getOnlyArray{return&MFile::getOnlyArray($fh,$path);}
	#ハッシュを返す
	sub getHash{return map{m/\bid=\t([^\t]+);\t/o;($1,$_)}&getArray;}
	#読み込み専用で開いてハッシュを返す
	sub getOnlyHash{my@tmp=map{m/\bid=\t([^\t]+);\t/o;($1,$_)}&getOnlyArray;&finish;return@tmp;}
	#クリアして引数を書き込む
	sub clear{&MFile::clear($fh,map{m/(\bid=\t[^\t]+;\t(?:[^\t]*=\t[^\t]*;\t)*)/o;"$1\n"}@_);}
	#close
	sub finish{return&MFile::finish($fh);undef$fh;}
}
#------------------------------------------------------------------------------#
# Marldia File manager
#
package MFile;
{
	#open
	sub start{
	#0=fh; 1=path; 2=1(r)/3(rw)
		my($fh,$path,$type)=@_;
		unless(-e$path){
			my$old=$path;
			$old=~s/\.cgi$/\.pl/o;
			-e$old&&rename($old,$path);
		}
		if($fh){
		}elsif(1==$type){
			local*FH;open(FH,"<$path")||die"Can't read rank($path)[$!]";$fh=*FH;
			eval{flock($fh,1)};
		}elsif(3==$type){
			local*FH;open(FH,"+>>$path")||die"Can't rw rank($path)[$!]";$fh=*FH;
			eval{flock($fh,2)};
		}
		seek($fh,0,0);
		$_[0]=$fh;
	}
	#リストを返す
	sub getArray{
	#0=fh; 1=path
		$_[0]||&start($_[0],$_[1],3);
		my$fh=$_[0];
		return map{m/(.*)/o}(<$fh>);
	}
	#読み込み専用で開いてリストを返す
	sub getOnlyArray{
	#0=fh; 1=path
		$_[0]||&start($_[0],$_[1],1);
		my$fh=$_[0];
		my@tmp=map{m/(.*)/o}(<$fh>);
		&finish($_[0]);
		return@tmp;
	}
	#クリアして引数を書き込む
	sub clear{
		my$fh=shift();
		$fh||die"clearの前にはstartが必要";
		truncate($fh,0);
		seek($fh,0,0);
		print$fh map{m/(.*)/o?"$1\n":"\n"}@_;
	}
	#close
	sub finish{$_[0]||return;close$_[0];undef$_[0];}
}
package main;
#-------------------------------------------------
# 初期設定
#
BEGIN{
	#エラーが出たらエラー画面を表示するように
	unless(%CF){
		$CF{'program'}=__FILE__;
		$SIG{'__DIE__'}=sub{
		print<<"_HTML_";
Content-Language: ja
Content-type: text/plain; charset=euc-jp

<PRE>
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

+#       Airemix Marldia     #+
+#  http://www.airemix.com/  #+
_HTML_
		exit;
		};
	}
	#Revision Number
	$CF{'correv'}=qq$Revision: 1.11 $;
	$CF{'version'}=($CF{'correv'}=~/(\d[\w\.]+)/o)?"v$1":'unknown';#"Revision: 1.4"->"v1.4"
}
1;
__END__
