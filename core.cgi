#!/usr/local/bin/perl

#------------------------------------------------------------------------------#
# 'Marldia' Chat System
# - Main Script -
#
# $Revision: 1.13 $
# "This file is written in euc-jp, CRLF." ��
# Scripted by NARUSE Yui.
#------------------------------------------------------------------------------#
# $cvsid = q$Id: core.cgi,v 1.13 2002-12-17 06:10:05 naruse Exp $;
require 5.005;
use strict;
use vars qw(%CF %IN %CK %IC);
#$|=1;
#$ENV{'HTTP_ACCEPT_ENCODING'}='';
#use IO::File;
use Data::Dumper;

#-------------------------------------------------
# MAIN SWITCH
#
sub main{
	&getParams;
#	$IN{'name'}&&" $IN{'name'} "=~m/ $CF{'denyname'} /o&&&locate($CF{'sitehome'});
#	(" $ENV{'REMOT_ADDR'} "=~m/ $CF{'denyra'} /o)&&(&locate($CF{'sitehome'}));
#	(" $ENV{'REMOT_HOST'} "=~m/ $CF{'denyrh'} /o)&&(&locate($CF{'sitehome'}));
	
#%IN=(mode=>'south',line=>20,reload=>123);
	if('south'eq$IN{'mode'}){
	}elsif('frame'eq$IN{'mode'}){
		&modeFrame;
	}elsif('north'eq$IN{'mode'}){
		&modeNorth;
	}elsif('admicmd'eq$IN{'mode'}){
		&modeAdmicmd;
	}elsif('usercmd'eq$IN{'mode'}){
		&modeUsercmd;
	}elsif('icct'eq$IN{'mode'}){
		require($CF{'icct'}||'iconctlg.cgi');
		&iconctlg;
	}
	&modeSouth;
	exit;
}


#------------------------------------------------------------------------------#
# MARD ROUTINS
#
# mainľ���Υ��֥롼����

#-------------------------------------------------
# Frame
#
sub modeFrame{
	print<<"_HTML_";
Status: 200 OK
Content-type: text/html; charset=euc-jp
Content-Language: ja
Connection: keep-alive

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
	���Υڡ�����Microsoft Internet Explorer 6.0 �����˺���Ƥ��ޤ�
	MSIE5.01��Netscape6��Mozilla0.9�ʾ�Ǥ⤽�������˸��뤳�Ȥ������Ȼפ��ޤ�
	Netscape4.x�Ǥ�ɽ���ΰ�����������ǽ��������ޤ�
	�ơ��֥��ե졼����б����Ƥ��ʤ��֥饦���Ǥϡ�ɽ��������ʬ������Ƥ��ޤ����ᡢ
	�¼�Ū�˱������뤳�Ȥ��Ǥ��ޤ���
	Mozilla4�ʾ�ߴ��Υ֥饦���Ǥޤ���Ƥ�������
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
sub modeNorth{
	&getCookie;
	(%CK)||(%CK=%IN);
	&header;
	&iptico($CK{'icon'},'tabindex="12"');
	print<<'_HTML_';
<SCRIPT type="text/javascript" defer>
<!--
//--------------------------------------
// �����
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
		cook.checked=document.cookie?false:true;
	}
	if(body){
		body.value="";
		body.focus();
	}
}

//--------------------------------------
// ��������ץ�ӥ塼
function iconPreview(arg){
	if(!preview&&!arg){return;}
	preview.src=icondir+arg;
	preview.alt=arg;
}

//--------------------------------------
// ����������Ѥ�����
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
// ɽ�𥢥�������
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
	+'gradientType=\'1\');">����������<\/div>'+str+'<SELECT name="surfaceS" id="surfaceS"'
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
<TABLE cellspacing="0" style="width:770px" summary="ȯ���ե�����">
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
<LABEL accesskey="z" for="surface" title="hyoZyo\nɽ�𥢥���������򤷤ޤ��ʻȤ���С�"
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
<DIV style="margin:0.3em 0;text-align:center" title="reloadQ\n��ե졼������ɤ��ޤ�"
>[<A href="$CF{'index'}?north" accesskey="q" tabindex="52">���ɹ�(<SPAN class="ak">Q</SPAN>)</A>]
<INPUT name="south" type="hidden" value="">
</DIV>
</TD>
<TH><LABEL accesskey="n" for="name" title="Name\n���ü�̾��ȯ����̾�ʤɤǻȤ�̾���Ǥ�"
>̾��(<SPAN class="ak">N</SPAN>)</LABEL>:</TH>
<TD><INPUT type="text" class="text" name="name" id="name" maxlength="20" size="20"
 style="ime-mode:active;width:100px" value="$CK{'name'}" tabindex="11"></TD>
<TH><LABEL accesskey="c" for="color" title="name Color\n���ü�̾��ȯ����̾�ʤɤǻȤ�̾���ο��Ǥ�"
>̾����(<SPAN class="ak">C</SPAN>)</LABEL>:</TH>
<TD>@{[&iptcol('color','tabindex="21"')]}</TD>
<TH><LABEL accesskey="g" for="line" title="log Gyosu\nɽ��������ιԿ��Ǥ�\n�ǹ�$CF{'max'}��"
>�Կ�(<SPAN class="ak">G</SPAN>)</LABEL>:</TH>
<TD><INPUT type="text" class="text" name="line" id="line" maxlength="4" size="4"
 style="ime-mode:disabled;width:32px" value="$CK{'line'}��" tabindex="31"></TD>
<TD style="text-align:center"><INPUT type="submit" accesskey="s" class="submit"
 title="Submit\n���ߤ����Ƥ�ȯ�����ޤ�" value="OK" tabindex="41"></TD>
<TD></TD>
</TR>

<TR>
<TH><LABEL accesskey="i" for="icon" title="Icon\n���Ѥ��륢����������򤷤ޤ�"
><A href="index.cgi?icct" target="south">��������</A>(<SPAN class="ak">I</SPAN>)</LABEL></TH>
<TD>@{[&iptico($CK{'icon'},'tabindex="12"')]}</TD>
<TH><LABEL accesskey="c" for="bcolo" title="body Color\nȯ��������ʸ�ο��Ǥ�"
>ʸ�Ͽ�(<SPAN class="ak">C</SPAN>)</LABEL>:</TH>
<TD>@{[&iptcol('bcolo','tabindex="22"')]}</TD>
<TH><LABEL accesskey="r" for="reload" title="Reload\n���ä��Ȥ˼�ưŪ�˥���ɤ��뤫���Ǥ�"
>�ֳ�(<SPAN class="ak">R</SPAN>)</LABEL>:</TH>
<TD><INPUT type="text" class="text" name="reload" id="reload" maxlength="4" size="4"
 style="ime-mode:disabled;width:32px" value="$CK{'reload'}��" tabindex="32"></TD>
<TD style="text-align:center"><INPUT type="reset" class="reset"
 title="reset\n���Ƥ��������ޤ�" value="����󥻥�" tabindex="42"></TD>
</TR>

<TR>
<TH><LABEL accesskey="b" for="body" title="Body\nȯ��������ʸ�����ƤǤ�\n\$rank��ȯ����󥭥󥰡�\$member�ǻ��ü԰����򸫤�ޤ�"
>����(<SPAN class="ak">B</SPAN>)</LABEL>:</TH>
<TD colspan="5"><INPUT type="text" class="text" name="body" id="body" maxlength="300" size="100"
 style="ime-mode:active;width:450px" tabindex="1"></TD>
<TD><LABEL accesskey="k" for="cook" title="cooKie\n�����å��������ȸ��ߤ������Cookie����¸���ޤ�"
><INPUT type="checkbox" name="cook" id="cook" class="check" tabindex="51" checked="checked"
>���å���¸(<SPAN class="ak">K</SPAN>)</LABEL></TD>
</TR>

<TR>
<TH><LABEL accesskey="y" for="id" title="identitY name\nCGI�����ǻ��Ѥ��롢�����Ѥ�̾�������򤷤ޤ�
����̾�����ºݤ�ɽ�˽Ф뤳�ȤϤ���ޤ���\n������Ͽ̾��Ʊ������Ʊ���ʪ���Ȥߤʤ���ޤ�"
>Identit<SPAN class="ak">y</SPAN></LABEL>:</TH>
<TD><INPUT type="text" class="text" name="id" id="id" maxlength="20" size="20"
 style="ime-mode:active;width:150px" value="$CK{'id'}" tabindex="101"></TD>
<TH><LABEL accesskey="l" for="email" title="e-maiL\n�᡼�륢�ɥ쥹�Ǥ�"
>E-mai<SPAN class="ak">l</SPAN></LABEL>:</TH>
<TD colspan="3"><INPUT type="text" class="text" name="email" id="email" maxlength="200" size="40"
 style="ime-mode:inactive;width:200px" value="$CK{'email'}" tabindex="111"></TD>
<TH style="text-align:center">[ <A href="$CF{'sitehome'}" target="_top"
title="$CF{'sitename'}�ص���ޤ�\n�༼��å������ϽФʤ��Τǵ���ΰ�����˺�줺��"
>$CF{'sitename'}�ص���</A> ]</TH>
</TR>

<TR>
<TH><LABEL accesskey="p" for="opt" title="oPtion\n���ץ����"
>O<SPAN class="ak">p</SPAN>tion</LABEL>:</TH>
<TD><INPUT type="text" class="text" name="opt" id="opt" maxlength="200" style="ime-mode:inactive;width:150px"
 value="$CK{'opt'}" tabindex="102"></TD>
<TH><LABEL accesskey="o" for="home" title="hOme\n�����Ȥ�URL�Ǥ�"
>H<SPAN class="ak">o</SPAN>me</LABEL>:</TH>
<TD colspan="3"><INPUT type="text" class="text" name="home" id="home" maxlength="200" size="40"
 style="ime-mode:inactive;width:200px" value="$CK{'home'}" tabindex="112"></TD>
<TH style="letter-cpacing:-1px;text-align:center">-<A href="http://www.airemix.com/" title="Airemix�ؤ��äƤߤ�"
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
sub modeSouth{
	
	#---------------------------------------
	#������������
	
	#-----------------------------
	#���ޥ�ɤȤ���Ĵ��
	my%EX;
	if($IN{'cmd'}){
		for(split(/;/o,$IN{'cmd'})){
			my($i,$j)=split('=',$_,2);
			$i||next;
			defined$j||($j=1);
			$EX{$i}=$j;
		}
	}
	
	#-----------------------------
	#ɽ�𥢥�����
	$IN{'icon'}&&$IN{'icon'}=~/^(([^\/#]*\/)*[^\/#.]+)(\.[^\/#]*)#(\d+)(-\d+)?$/o
	&&$IN{'surface'}=~/^$1\d*(?:\.[^\/#.]*)?$/o
	&&($IN{'icon'}=$IN{'surface'});
	
	
	#-----------------------------
	#��ʸ�ν���
	#form->data�Ѵ�
	unless(defined$IN{'body'}&& length$IN{'body'}){
		$IN{'body'}='';
	}elsif($CF{'tags'}&& 'ALLALL'eq$CF{'tags'}){
		#ALLALL������OK��â����Ĵ��̵����URI��ư��󥯤�̵����
		#�����ǥ�󥯤�ĥ�ä��ꡢ��Ĵ���Ƥ����Τ���Ť˥�󥯡���Ĵ���Ƥ��ޤ��ޤ�����
	}else{
		#��ʸ�Τߥ�����ȤäƤ⤤������ˤ�Ǥ���
		my$attrdel=0;#°����ä�/�ä��ʤ�(1/0)
		my$str=$IN{'body'};
		study$str;
		$str=~tr/"'<>/\01-\04/;
		
		#��������
		if($CF{'tags'}&&!$EX{'notag'}){
			my$tag_regex_='[^\01-\04]*(?:\01[^\01]*\01[^\01-\04]*|\02[^\02]*\02[^\01-\04]*)*(?:\04|(?=\03)|$(?!\n))';
			my$comment_tag_regex='\03!(?:--[^-]*-(?:[^-]+-)*?-(?:[^\04-]*(?:-[^\04-]+)*?)??)*(?:\04|$(?!\n)|--.*$)';
			my$text_regex = '[^\03]*';
			
			my$tags=$CF{'tags'};
			my%tagCom=map{m/(!\w+)(?:\(([^()]+)\))?/o;$1," $2 "||''}($tags=~/!\w+(?:\([^()]+\))?/go);
			if($tagCom{'!SELECTABLE'}){
				$tags.=' '.join(' ',grep{$tagCom{'!SELECTABLE'}=~/ $_ /o}grep{m/\w+/}split(/\s+/,$EX{'usetag'}));
			}elsif(defined$tagCom{'!SELECTABLE'}){
				$tags='\w+';
			}
			
			my$result='';
			#�⤷ BR������ A�����ʤ�����Υ��������Ϻ���������ʤ����ˤϡ� 
			#$tag_tmp = $2; �θ�ˡ����Τ褦�ˤ��� $tag_tmp �� $result �˲ä���褦�ˤ���ФǤ��ޤ��� 
			#$result .= $tag_tmp if $tag_tmp =~ /^<\/?(BR|A)(?![\dA-Za-z])/i;
			my$remain=join('|',grep{m/^(?:\\w\+|\w+)$/o}split(/\s+/o,$tags));
			#�դ� FONT������ IMG�����ʤ�����Υ�������������������ˤϡ� 
			#$tag_tmp = $2; �θ�ˡ����Τ褦�ˤ��� $tag_tmp �� $result �˲ä���褦�ˤ���ФǤ��ޤ��� 
			#$result .= $tag_tmp if $tag_tmp !~ /^<\/?(FONT|IMG)(?![\dA-Za-z])/i;
			my$pos=length$str;
			while($str=~/\G($text_regex)($comment_tag_regex|\03$tag_regex_)?/gso){
				$pos=pos$str;
				($1&& length$1)||($2&& length$2)||last;
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
			#���ĥ���̵��orCommand:notag
		}
		
		#��綯Ĵ
		if($CF{'strong'}&&!$EX{'nostrong'}){
			my%ST=map{(my$str=$_)=~tr/"'<>/\01-\04/;$str}($CF{'strong'}=~/(\S+)\s+(\S+)/go);
			if($CF{'strong'}=~/^ /o){
				#��ĥ��綯Ĵ
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
				#���ܸ�綯Ĵ
				for(keys%ST){$str=~s[^(\Q$_\E.*)$][<STRONG  clAss="$ST{$_}"  >$1</STRONG>]gm;}
			}
		}
		
		#URI��ư���
		if($CF{'noautolink'}||!$EX{'noautolink'}){
			#[-_.!~*'()a-zA-Z0-9;:&=+$,]	->[!$&-.\w:;=~]
			#[-_.!~*'()a-zA-Z0-9:@&=+$,]	->[!$&-.\w:=@~]
			#[-_.!~*'()a-zA-Z0-9;/?:@&=+$,]	->[!$&-/\w:;=?@~]
			#[-_.!~*'()a-zA-Z0-9;&=+$,]		->[!$&-.\w;=~]
			#http URL ������ɽ��
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
			#ftp URL ������ɽ��
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
			#�᡼�륢�ɥ쥹������ɽ����
			#"aaa@localhost"�ʤɤ�Ǽ��Ĥǡ֥᡼�륢�ɥ쥹�פȤ��ƻȤ��Ȥϻפ��ʤ��Τǡ�
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
			#�²�ư��
			my$tag_regex_=q{[^"'<>]*(?:"[^"]*"[^"'<>]*|'[^']*'[^"'<>]*)*(?:>|(?=<)|$(?!\n))};
			my$comment_tag_regex='<!(?:--[^-]*-(?:[^-]+-)*?-(?:[^>-]*(?:-[^>-]+)*?)??)*(?:>|$(?!\n)|--.*$)';
			my$tag_regex=qq{$comment_tag_regex|<$tag_regex_};
			my$text_regex=q{[^<]*};
			my$result='';
			my$skip=0;
			my$pos=length$str;
			while($str=~/($text_regex)($tag_regex)?/gso){
				''eq$1&&!$2&& last;
				$pos=pos$str;
				my$text_tmp=$1;
				my$tag_tmp=$2;
				if($skip){
					$result.=$text_tmp.$tag_tmp;
					$skip=0 if$tag_tmp=~/^<\/[aA](?!\w)/;
				}else{
					$text_tmp=~s{($http_URL_regex|$ftp_URL_regex|($mail_regex))}
					{
						my$href=$2?'mailto:':'';
						my$org=$1;
						($href.=$org)=~tr/"/\01/;
						qq{<A class="autolink" href="$href" target="_blank">$org</A>}
					}ego;
					$result.=$text_tmp.$tag_tmp;
					$skip=1 if$tag_tmp=~/^<[aA](?!\w)/;
					if($tag_tmp=~/^<(XMP|PLAINTEXT|SCRIPT)(?!\w)/i){
						$str=~/(.*?(?:<\/$1(?!\w)$tag_regex_|$))/gis;
						$result.=$1;
					}
				}
			}
			$str=$result.substr($str,$pos);
		}else{
			#Command:nolink
		}
		
		#�����ֹ��󥯡�>>No.12-6��
		if($CF{'noartno'}||!$EX{'noartno'}){
			$str=~s{(\04\04No\.(\d+)(-\d+)?)}{<A class="autolink" href="index.cgi?read=$2#art$2$3">$1</A>}go;
		}
		
		$str=~s/&(#?\w+;)?/$1?"&$1":'&#38;'/ego;
		$str=~s/\01/&#34;/go;
		$str=~s/\02/&#39;/go;
		$str=~s/\03/&#60;/go;
		$str=~s/\04/&#62;/go;
		$IN{'body'}=$str;
	}
	$IN{'body'}=~s/\t/&nbsp;&nbsp;&nbsp;&nbsp;/go;
	$IN{'body'}=~s/\n+$//o;
	$IN{'body'}=~s/\n/<BR>/go;
	
	$IN{'isActive'}=$ENV{'CONTENT_LENGTH'}?1:0;
	$IN{'time'}=$^T;
	
	
	#-----------------------------
	#���å����񤭹���
	$IN{'cook'}&&&setCookie;
	
	#---------------------------------------
	#���üԡ���󥭥󥰡��񤭹��߽���
	my$chatlog=Chatlog->getInstance;
	my$members=Members->getInstance;
	
	#-----------------------------
	#��ʬ�Υǡ������ɲ�
	$IN{'reload'}=$members->add(\%IN);
	
	#-----------------------------
	#�񤭹���
	if(length$IN{'body'}){
		#-----------------------------
		#��󥭥󥰲���
		$IN{'exp'}=Rank->plusExp(\%IN);
		#-----------------------------
		#ȯ������
		$chatlog->add(\%IN);
	}elsif($IN{'del'}){
		#-----------------------------
		#ȯ�����
		$chatlog->delete({id=>$IN{'id'},exp=>$IN{'del'}});
	}
	
	
	
	#-----------------------------
	#������
	my$query='south';
	if($IN{'id'}){
		$query=join(';',map{my$val=$IN{$_};$val=~s{(\W)}{'%'.unpack('H2',$1)}ego;"$_=$val"}
		grep{defined$IN{$_}}qw(name id line reload color));
	}
	
	#-----------------------------
	#���üԾ���
	my@singers=map{qq(<A style="color:$_->{'color'}" title="$_->{'blank'}��">$_->{'name'}</A>��)}
	sort{$a->{'blank'}<=>$b->{'blank'}}$members->getSingersInfo;
	my$intMembers=scalar keys%{$members};
	my$intSingers=@singers;
	my$intAudiences=$intMembers-$intSingers;
	my$strMembers;
	if(@singers){
		$strMembers="@singers";
	}else{
		my@wabisabi=(qw(���󤳤ɤ� �ߤƤ������ (-_��)���׎���),"@{[('|_��)���ס�')x$intAudiences]}");
		$strMembers=$wabisabi[int(rand@wabisabi)];
	}
	
	#---------------------------------------
	#�ǡ���ɽ��
	#-----------------------------
	#�إå�����
	&header($IN{'reload'}?
	qq(<META http-equiv="refresh" content="$IN{'reload'};url='$CF{'index'}?$query'">\n):'');
	#-----------------------------
	#���ü�ɽ��
	print<<"_HTML_";
<TABLE class="meminfo" summary="���üԾ���ʤ�"><TR>
<TD class="reload">[ <A href="$CF{'index'}?$query">@{[sprintf('%02d:%02d:%02d',(localtime$^T)[2,1,0])]}</A> ]</TD>
<TD class="member">[���:$intMembers�� ���ü�:$intSingers�� �ѵ�:$intAudiences��] [ $strMembers ]</TD>
<TD class="respan">(<SPAN>$IN{'reload'}�ôֳ�</SPAN>)</TD>
</TR></TABLE>
_HTML_
	my$i=0;
	#-----------------------------
	#��ɽ��
	for(@{$chatlog}){
		my%DT=%{$_};
		'del'eq$DT{'Mar1'}&& next;
		++$i>$IN{'line'}&& last;
		
		#����
		my$date=&date($DT{'time'});
		#̾�����᡼�륢�ɥ쥹��̾����
		my$name=$DT{'email'}&&$DT{'color'}?
		qq(<A href="mailto:$DT{'email'}" title="$DT{'email'}" style="color:$DT{'color'}">$DT{'name'}</A>)
		:$DT{'email'}?qq(<A href="mailto:$DT{'email'}" title="$DT{'email'}">$DT{'name'}</A>)
		:$DT{'color'}?qq(<A style="color:$DT{'color'}">$DT{'name'}</A>)
		:$DT{'name'};
		#�ۡ���
		my$home=$DT{'home'}?qq(<A href="$DT{'home'}" target="_blank" title="$DT{'home'}">��</A>):'��';
		#��٥�׻�-�Ƥ��ȡ�
		srand($DT{'exp'});
		$DT{'level'}=1+int(rand(sqrt$DT{'exp'}*2));
		#����ܥ���
		my$del=$IN{'id'}&&$DT{'id'}eq$IN{'id'}?qq([<A href="$CF{'index'}?del=$DT{'exp'}&#59;$query">���</A>])
		:'&nbsp;';
		#����
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
	&showFooter;
	exit;
}


#-------------------------------------------------
# ���Ѽԥ��ޥ��
#
sub modeUsercmd{
	unless($IN{'cmd'}){
		die"�ֲ��⤷�ʤ���������";
	}
	#��������
	my@arg=grep{s/\\(\\)|\\(")|"/$1$2/go;$_;}($IN{'cmd'}=~
	/(?!\s)[^"\\\s]*(?:\\[^\s][^"\\\s]*)*(?:"[^"\\]*(?:\\.[^"\\]*)*(?:"[^"\\\s]*(?:\\[^\s][^"\\\s]*)*)?)*\\?/go);
=item ���ѥ��ޥ��

��rank
 ��󥭥󥰤�ɽ��

��mem
 ���üԾ����ɽ��

��del <exp>
 ȯ�����

=cut

	#ʬ��
	if('rank'eq$arg[0]){
		#ȯ����󥭥�ɽ��
		&header;
		print<<'_HTML_';
<TABLE class="table" summary="ȯ����󥭥�">
<CAPTION>�ϥĥ����󤭤󤰡ʤ桼�����⡼�ɡ�</CAPTION>
	<TH scope="col">�ʤޤ�</TH>
	<TH scope="col">���������</TH>
	<TH scope="col">�ϤĤȤ����礦</TH>
_HTML_
		for(sort{$b->{'exp'}<=>$a->{'exp'}}values%{Rank->getOnlyHash}){
			print<<"_HTML_";
<TR>
	<TD style="color:$_->{'color'}">$_->{'name'}</TD>
	<TD style="color:$_->{'bcolo'}">$_->{'exp'}</TD>
	<TD style="color:$_->{'bcolo'}">@{[&date($_->{'firstContact'})]}</TD>
</TR>
_HTML_
		}
		print"</TABLE>";
		&showFooter;
		exit;
	}elsif('member'eq$arg[0]){
		#��ʪ�Ͱ���
		&header;
		print<<'_HTML_';
<TABLE class="table" summary="���üԤΰ���">
<CAPTION>���󤫤��� �������ʤ桼�����⡼�ɡ�</CAPTION>
	<TH scope="col">�ʤޤ�</TH>
	<TH scope="col">�֤��</TH>
	<TH scope="col">���Ȥ���</TH>
_HTML_
		for(values%{Members->getOnlyHash}){
			if($_->{'name'}){
				print<<"_HTML_";
<TR>
	<TD style="color:$_->{'color'}">$_->{'name'}</TD>
	<TD style="color:$_->{'bcolo'}">@{[$^T-$_->{'lastModified'}]}</TD>
	<TD style="color:$_->{'bcolo'}">@{[$^T-$_->{'time'}]}</TD>
</TR>
_HTML_
			}else{
				print<<"_HTML_";
<TR>
	<TD>ROM</TD>
	<TD>null</TD>
	<TD>@{[$^T-$_->{'time'}]}</TD>
</TR>
_HTML_
			}
		}
		print"</TABLE>";
		&showFooter;
		exit;
	}elsif(''eq$arg[0]){
		#
	}
	#̵���ʥ��ޥ��
	die"'$arg[0]'�ϥ��ޥ�ɤȤ��ƤȤ���ǧ������Ƥ��ޤ���";
	exit;
}


#-------------------------------------------------
# �������ޥ��
#
sub modeAdmicmd{
	unless($IN{'cmd'}){
		die"�ֲ��⤷�ʤ���������";
	}
	#��������
	my@arg=grep{s/\\(\\)|\\(")|"/$1$2/go;$_;}($IN{'cmd'}=~
	/(?!\s)[^"\\\s]*(?:\\[^\s][^"\\\s]*)*(?:"[^"\\]*(?:\\.[^"\\]*)*(?:"[^"\\\s]*(?:\\[^\s][^"\\\s]*)*)?)*\\?/go);

=item �������ޥ��

$CF{'admipass'}='admicmd';�ʤ顢
#admicmd ...
��...�Ȥ������ޥ�ɤ�ȯư

��rank (del|cat|conv) <id ...>
 ��󥭥󥰤�ɽ��
��del
 �����Ȥ��ƻ��ꤵ�줿ID�ξ������
��cat
 ��������ID�ˡ�����ʹߤ�ID�����礹��
��conv
 1.5�����Υ�󥭥󥰥ǡ�����1.6�������Ѵ�����

��mem
 ���üԾ����ɽ��

��del <id> <exp>
 ȯ�����

=cut

	#ʬ��
	if(!$arg[0]){
	}elsif('rank'eq$arg[0]){
		#ȯ����󥭥�
		unless($arg[1]){
		}elsif('del'eq$arg[1]){
			#��󥭥󥰤�����
			Rank->delete($arg[2]);
		}elsif('cat'eq$arg[1]){
			#ID����ӷи��Ϥ�����
			my$rank=Rank->getInstance;
			$rank->{$arg[2]}->{'exp'}||die"����ʿͤ��ʤ�";
			for(3..$#arg){
				(!$rank->{$arg[$_]}||!$rank->{$arg[$_]}->{'exp'})&& next;
				$rank->{$arg[2]}->{'exp'}+=$rank->{$arg[$_]}->{'exp'};
				$rank->delete($arg[$_]);
			}
		}
		
		#��󥭥�ɽ��
		&header;
		print<<'_HTML_';
<TABLE class="table" summary="ȯ����󥭥�">
<CAPTION>Ķ��ȯ����󥭥�</CAPTION>
	<TH scope="col">NAME</TH>
	<TH scope="col">EXP</TH>
	<TH scope="col">FIRST CONTACT</TH>
	<TH scope="col">REMOTE_ADDR</TH>
	<TH scope="col">HTTP_USER_AGENT</TH>
_HTML_
		for(sort{$b->{'exp'}<=>$a->{'exp'}}values%{Rank->getOnlyHash}){
			print<<"_HTML_";
<TR>
	<TD style="color:$_->{'color'}">$_->{'name'}</TD>
	<TD style="color:$_->{'bcolo'}">$_->{'exp'}</TD>
	<TD style="color:$_->{'bcolo'}">@{[&datef($_->{'firstContact'},'dateTime')]}</TD>
	<TD style="color:$_->{'bcolo'}">$_->{'ra'}</TD>
	<TD style="color:$_->{'bcolo'}">$_->{'hua'}</TD>
</TR>
_HTML_
		}
		print"</TABLE>";
		&showFooter;
		exit;
	}elsif('member'eq$arg[0]){
		#��ʪ�Ͱ���
		&header;
		print<<'_HTML_';
<TABLE class="table" summary="���üԤΰ���">
<CAPTION>Ķ�����ü԰���</CAPTION>
	<TH scope="col">NAME</TH>
	<TH scope="col">BLANK</TH>
	<TH scope="col">OTOSATA</TH>
	<TH scope="col">REMOTE_ADDR</TH>
	<TH scope="col">HTTP_USER_AGENT</TH>
_HTML_
		for(values%{Members->getOnlyHash}){
			if($_->{'name'}){
				print<<"_HTML_";
<TR>
	<TD style="color:$_->{'color'}">$_->{'name'}</TD>
	<TD style="color:$_->{'bcolo'}">@{[$^T-$_->{'lastModified'}]}</TD>
	<TD style="color:$_->{'bcolo'}">@{[$^T-$_->{'time'}]}</TD>
	<TD style="color:$_->{'bcolo'}">$_->{'ra'}</TD>
	<TD style="color:$_->{'bcolo'}">$_->{'hua'}</TD>
</TR>
_HTML_
			}else{
				print<<"_HTML_";
<TR>
	<TD>ROM</TD>
	<TD>null</TD>
	<TD>@{[$^T-$_->{'time'}]}</TD>
	<TD>$_->{'ra'}</TD>
	<TD>$_->{'hua'}</TD>
</TR>
_HTML_
			}
		}
		print"</TABLE>";
		&showFooter;
		exit;
	}elsif('del'eq$arg[0]){
		#ȯ�����
		Chatlog->delete(id=>$arg[1],exp=>$arg[2])||next;
		&header;
		print"<P>������ޤ�����</P>";
		&showFooter;
#	}elsif(''eq$arg[0]){
#		#
	}
	#̵���ʥ��ޥ��
	die"'$arg[0]'�ϥ��ޥ�ɤȤ��ƤȤ���ǧ������Ƥ��ޤ���";
	exit;
}


#-------------------------------------------------
# Location��ž��
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
# mainľ���Υ��֥롼���󷲤����

#-------------------------------------------------
# Form���Ƽ���
#
sub getParams{
	my$params;
	my@params;
	#��������
	unless($ENV{'REQUEST_METHOD'}){
		@params=@ARGV;
	}elsif('HEAD'eq$ENV{'REQUEST_METHOD'}){ #forWWWD
#Method��HEAD�ʤ��LastModifed����Ϥ��ơ�
#�Ǹ����ƻ�����Τ餻��
		my$last=&datef((stat("$CF{'rank'}"))[9],'rfc1123');
		print"Status: 200 OK\nLast-Modified: $last\n"
		."Content-Type: text/plain\n\nLast-Modified: $last";
		exit;
	}elsif('POST'eq$ENV{'REQUEST_METHOD'}){
		read(STDIN,$params,$ENV{'CONTENT_LENGTH'});
	}elsif('GET'eq$ENV{'REQUEST_METHOD'}){
		$params=$ENV{'QUERY_STRING'};
	}
	
	# EUC-JPʸ��
	my$eucchar=qr((?:
		[\x09\x0A\x0D\x20-\x7E]			# 1�Х��� EUC-JPʸ����
		|(?:[\x8E\xA1-\xFE][\xA1-\xFE])	# 2�Х��� EUC-JPʸ��
		|(?:\x8F[\xA1-\xFE]{2})			# 3�Х��� EUC-JPʸ��
	))x;
	
	#������ϥå����
	if(!$params){
	}elsif(length$params>262114){ # 262114:�����������ξ��(byte)
		#����������
		&showHeader;
		print"������ʤ�Ǥ��̤�¿�����ޤ�\n$params";
		&showFooter;
		exit;
	}elsif(length$params>0){
		#���Ϥ�Ÿ��
		@params=split(/[&;]/o,$params);
	}

	#���Ϥ�Ÿ�����ƥϥå���������
	my%DT;
	while(@params){
		my($i,$j)=split('=',shift(@params),2);
		$i=~/([a-z][-.:\w]*)/o||next;$i=$1;
		defined$j||($DT{$i}='')||next;
		study$j;
		$j=~tr/+/\ /;
		$j=~s/%([\dA-Fa-f]{2})/pack('H2',$1)/ego;
		$j=($j=~/($eucchar*)/o)?$1:'';
		$j=~s/\x0D\x0A/\n/go;$j=~tr/\r/\n/;
		if('body'ne$i){
			#��ʸ�ʳ������̥����ػ�
			$j=~s/\t/&nbsp;&nbsp;&nbsp;&nbsp;/go;
			$j=~s/&(#?\w+;)?/$1?"&$1":'&#38;'/ego;
			$j=~s/"/&#34;/go;
			$j=~s/'/&#39;/go;
			$j=~s/</&#60;/go;
			$j=~s/>/&#62;/go;
			$j=~s/\n/<BR>/go;
			$j=~s/(<BR>)+$//o;
		}#��ʸ�ϸ�ǤޤȤ��
		$DT{$i}=$j;
	}
	
	#�����α�������
	$IN{'ra'}=($ENV{'REMOTE_ADDR'}&&$ENV{'REMOTE_ADDR'}=~/([\d\:\.]{2,56})/o)?"$1":'';
	$IN{'hua'}=($ENV{'HTTP_USER_AGENT'}&&$ENV{'HTTP_USER_AGENT'}=~/($eucchar+)/o)?"$1":'';
	$IN{'hua'}=~tr/\x09\x0A\x0D/\x20\x20\x20/;
	
	#���ޥ�ɷ�
	if($DT{'body'}){
		if($CF{'admipass'}&&$DT{'body'}=~/^#$CF{'admipass'}\s+(.*)/o){
			$IN{'mode'}='admicmd';
			$IN{'cmd'}=$1;
		}elsif($DT{'body'}=~/^\$(\w.*)/o){
			$IN{'mode'}='usercmd';
			$IN{'cmd'}=$1;
		}
		$IN{'mode'}&& return;
	}
	
	if(!%DT||($DT{'mode'}&& 'frame'eq$DT{'mode'})){
		#�ե졼��
		$IN{'mode'}='frame';
	}elsif(defined$DT{'icct'}){
		#�������󥫥���
		$IN{'page'}=($DT{'page'}&&$DT{'page'}=~/([1-9]\d*)/o)?$1:1;
		$IN{'mode'}='icct';
	}elsif($DT{'name'}){
		&getCookie;
		#http URL ������ɽ��
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
		#ftp URL ������ɽ��
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
		#�᡼�륢�ɥ쥹������ɽ����
		#"aaa@localhost"�ʤɤ�WWW��ǡ֥᡼�륢�ɥ쥹�פȤ��ƻȤ��Ȥϻפ��ʤ��Τ�
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
			$IN{'body'}=$DT{'body'}||'';
			$IN{'cook'}=$DT{'cook'}?'on':'0';
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
		$IN{'line'}=($DT{'line'}=~/([1-9]\d*)/o)?$1:$CF{'defline'};
		$IN{'reload'}=($DT{'reload'}=~/([1-9]\d+|0)/o)?$1:$CF{'defreload'};
		$IN{'mode'}='south';
	}elsif((defined$DT{'north'})||('north'eq$DT{'mode'})){
		#��
		$IN{'mode'}='north';
		$IN{'line'}=$CF{'defline'};
		$IN{'reload'}=$CF{'defreload'};
	}elsif(defined$DT{'south'}){
		#��
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
Status: 200 OK
Content-type: text/html; charset=euc-jp
Content-Language: ja-JP
Connection: keep-alive
Pragma: no-cache
Cache-Control: no-cache
_HTML_
	#GZIP Switch
	if($CF{'gzip'}&&$ENV{'HTTP_ACCEPT_ENCODING'}&&(index($ENV{'HTTP_ACCEPT_ENCODING'},'gzip')>-1)){
		print"Content-encoding: gzip\n\n";
		if(!open(STDOUT,"|$CF{'gzip'} -cfq9")){
			#GZIP���Ի��Υ��顼��å�����
			binmode STDOUT;
			print unpack("u",#GZIP����-uuencode���줿���顼��å�����
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
		#GZIP����ž���򤫤�����Ȥ��Ϥ�����
		$ENV{'HTTP_USER_AGENT'}&&(index($ENV{'HTTP_USER_AGENT'},'MSIE')>-1)&&(print ' 'x 2048); #IE�ΥХ��к�
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
@{[$_[0]||'']}
<LINK rel="stylesheet" type="text/css" href="$CF{'style'}" media="screen,print" title="DefaultStyle">
<LINK rel="start" href="$CF{'sitehome'}">
<LINK rel="index" href="$CF{'index'}">
<LINK rel="help" href="\$CF{'help'}">
<TITLE>$CF{'title'}</TITLE>
</HEAD>
<BODY>
_HTML_
}


#-------------------------------------------------
# �եå�������
#
sub showFooter{
	print<<"_HTML_";
<DIV class="AiremixCopy">- <A href="http://www.airemix.com/" target="_top" title="Airemix - Marldia -">Airemix Marldia</A><VAR title="times:@{[times]}">$CF{'version'}</VAR> -</DIV>
</BODY>
</HTML>
_HTML_
	exit;
}


#-------------------------------------------------
# Cookie���������
#
sub getCookie{
	$ENV{'HTTP_COOKIE'}||return undef;
	# EUC-JPʸ��
	my$eucchar=qr((?:
		[\x0A\x0D\x20-\x7E]			# 1�Х��� EUC-JPʸ����-\x09
		|(?:[\x8E\xA1-\xFE][\xA1-\xFE])	# 2�Х��� EUC-JPʸ��
		|(?:\x8F[\xA1-\xFE]{2})			# 3�Х��� EUC-JPʸ��
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
# Cookie�����ꤹ��
#
sub setCookie{
	my$cook=join('',map{"$_=\t$IN{$_};\t"}qw(id name color bcolo line reload icon email home opt));
	#0-9A-Za-z\-\.\_
	$cook=~s{(\W)}{'%'.unpack('H2',$1)}ego;
	my$gmt=&datef(($^T+20000000),'cookie');
	print"Set-Cookie: Marldia=$cook; expires=$gmt\n";
}

#-------------------------------------------------
# �������ɽ���Ѥ˥ե����ޥåȤ��줿���ռ������֤�
sub date{
=item ����
$ time��������
=cut
	$CF{'timezone'}||&cfgTimeZone($ENV{'TZ'});
	my($sec,$min,$hour,$day,$mon,$year,$wday)=gmtime($_[0]+$CF{'timeOffset'});
	#sprintf�������ϡ�Perl�β���򸫤Ƥ�������^^;;
	return sprintf("%4dǯ%02d��%02d��(%s) %02d��%02dʬ%s" #"1970ǯ01��01��(��) 09��00ʬ"����
	,$year+1900,$mon+1,$day,('��','��','��','��','��','��','��')[$wday],$hour,$min,$ENV{'TZ'});
#	return sprintf("%1d:%01d:%2d %4d/%02d/%02d(%s)" #"9:0: 0 1970/01/01(Thu)"����
#	,$hour,$min,$sec,$year+1900,$mon+1,$day,('Sun','Mon','Tue','Wed','Thu','Fri','Sat')[$wday]);
}


#-------------------------------------------------
# �ե����ޥåȤ��줿���ռ������֤�
#
sub datef{
=item ����
$ time�����λ���
;
$ ���Ϸ���(cookie|last|dateTime)
=cut
	my$time=shift;
	my$type=shift;
	unless($type){
	}elsif('cookie'eq$type){
	# Netscape��Cookie��
		return sprintf("%s, %02d-%s-%d %s GMT",(split(/\s+/o,gmtime$time))[0,2,1,4,3]);
	}elsif('rfc1123'eq$type){
	# RFC1123 ��Ȥ���LastModified��
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
# �����ॾ����μ���
sub cfgTimeZone{
=pod
�����ॾ�����Ķ��ѿ�TZ����������ơ�%CF�����ꤹ��
¾�δؿ��Ϥ���$CF{'timezone'},$CF{'timeOffset'}��Ȥäơ�
gmtime()����μ¤˴�˾���ϰ�λ���򻻽ФǤ���
=item ����
$ $ENV{'TZ'}
=cut
	my$envtz=shift;
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
# ��������ꥹ��
#
sub iptico{
=item ����
$ �ǥե���Ȼ���ˤ�������������ե�����̾�����줿�񤭴�����ǽ���ѿ�
;
$ SELECT�������ɲä�����°��
$ ��ĥ���ޥ��

=item ʣ����������ꥹ��
$CF{'iconList'}�κǽ�ΰ�ʸ����' '��Ⱦ�Ѷ���ˤ��ä����ʣ���ꥹ�ȥ⡼�ɤˤʤ�ޤ�
����Ū�����Ф��ȡ�
��ñ��Ȥߤʤ������
'icon.txt'
'icon1.txt icon2.txt' #"icon1.txt icon2"�Ȥ����ƥ����ȥե�������Ȥߤʤ��ޤ�
'"icon.txt" "exicon.txt"'
��ʣ���Ȥߤʤ������
' "icon.txt" "exicon.txt"'
' "icon.txt" exicon.txt'
' icon.txt exicon.txt'
=cut

	if($CK{'CacheIconList'}&&('reset'ne$_[2])){
		#����å���Ǥ���$CK{'CacheIconList'}���֤�
		return$CK{'CacheIconList'};
	}
	my$opt=$_[1]?" $_[1]":'';
	
	#��������ꥹ���ɤ߹���
	my$iconlist='';
	if($CK{'opt'}=~/\biconlist=nolist(;|$)/o){
	 #`icon=nolist`�ǥ�������ꥹ�Ȥ��ɤ߹��ޤʤ�
	}elsif($CF{'iconList'}=~/^ /o){
		#ʣ����������ꥹ���ɤ߹���
		for($CF{'iconList'}=~/("[^"\\]*(?:\\.[^"\\]*)*"|\S+)/go){
			$_||next;
			my$tmp;
			open(RD,'<'.$_)||die"Can't open multi-iconlist($_).";
			eval{flock(RD,1)};
			read(RD,$tmp,-s$_);
			close(RD);
			$iconlist.=$tmp;
		}
	}else{
		#ñ�쥢������ꥹ���ɤ߹���
		open(RD,'<'.$CF{'iconList'})||die"Can't open single-iconlist.";
		eval{flock(RD,1)};
		read(RD,$iconlist,-s$CF{'iconList'});
		close(RD);
	}

	#���򥢥�����η����SELECT���������
	if($CF{'exicon'}&&($CK{'opt'}=~/\bicon=([^;]*)/o)&&$IC{$1}){
		#�ѥ���ɷ�
		$_[0]=$IC{$1};
		$iconlist.=qq(<OPTION value="$_[0]" selected>���ѥ�������</OPTION>\n);
	}elsif($CF{'exicfi'}&&($CK{'opt'}=~/\b$CF{'exicfi'}=([^;]*)/o)){
		#�ե�������귿
		$_[0]=$1;
		$iconlist.=qq(<OPTION value="$_[0]" selected>�ե��������</OPTION>\n);
	}elsif($_[0]and$iconlist=~s/(value="$_[0]")/$1 selected="selected"/i){
	}elsif($iconlist=~s/value=(["'])(.+?)\1/value=$1$2$1 selected="selected"/io){
		$_[0]=$2;
	}
	
	$CK{'CacheIconList'}=<<"_HTML_";
<SELECT name="icon" id="icon" onchange="iconChange(this.value)"$opt>
$iconlist</SELECT>
_HTML_
	return$CK{'CacheIconList'};
}


#-------------------------------------------------
# ���顼�ꥹ���ɤ߹���
#
sub iptcol{

=item ����

$_[0]: 'color'
$_[1]: 'tabindex=12'

=cut

	my$id=$_[0]||'color';
	my$opt=$_[1]?" $_[1]":'';
	if('input'eq$CF{'colway'}){
		return<<"_HTML_";
<INPUT type="text" class="text" name="$id" id="$id" class="blur" maxlength="20" style="ime-mode:disabled; width:90px;"
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
# �桼�����������顼
#
sub showUserError{
	my$message=shift();
	&showHeader;
	print<<"_HTML_";
<H2 class="mode">- ���顼��ȯ�����ޤ��� -</H2>
<P>�����ؤ򤫤��ƿ������������ޤ���<BR>
<span class="warning">$message</span>���ᡢ<BR>����ʽ�����³�Ԥ��뤳�Ȥ��Ǥ��ޤ���Ǥ���<BR>
�ʲ���ǰ�Τ��ả���Ϥ��줿�ǡ��������󤷤Ƥ����ޤ�<BR>
���פʾ��󤬤����硢��¸���Ƥ����ơ��ޤ��ε������Ƥ��Ƥ�������</P>
<TABLE border="1" summary="�桼���������ѿ���ɽ�����Ƥ���">
<CAPTION>��������ä�����</CAPTION>
_HTML_
	print map{"<TR><TH>$_</TH><TD><XMP>$IN{$_}</XMP></TD>\n"}keys%IN;
	print '</TABLE>';
	&showgetFooter;
	exit;
}



#------------------------------------------------------------------------------#
# Logfile Class
#
{package Logfile;
	my$fh;
	my$path=$::CF{'log'};
	my@members;
	my@chatlog;
	my$singleton;
	
	#---------------------------------------
	# Class Methods
	sub Logfile::new{#private
		$fh&& die"�����Singleton�ʤΤ�new�򾡼�˸ƤФʤ��ǡ�getInstance��Ȥ�����";
		my$proto=shift;my$class=ref($proto)||$proto;
		local*LOGFILE;
		if(-e$::CF{'log'}){
			open(LOGFILE,'+<'.$path); #+>>�Ȥ����seek($fh,0,0)��ư���Ƥ���ʤ��Τ���ա�
			$fh=*LOGFILE{IO};
			eval{flock($fh,2)};
			seek($fh,0,0);
			#member���ɲ�
			while(<$fh>){/\S/o||last;push(@members,$_);}
			#chatlog���ɲ�
			while(<$fh>){/\S/o||last;push(@chatlog,$_);}
		}else{
			open(LOGFILE,'>'.$::CF{'log'});
			$fh=*LOGFILE{IO};
			eval{flock($fh,2)};
			@members=();
			@chatlog=();
		}
		
		$singleton=bless [\@chatlog,\@members],$class;
	}
	
	sub Logfile::getInstance{$singleton||Logfile->new;}
	sub Logfile::getChatlog	{$singleton||Logfile->new;return @chatlog;}
	sub Logfile::getMembers	{$singleton||Logfile->new;return @members;}
	
	sub Logfile::setChatlog	{my$self=shift;@chatlog=@_;}
	sub Logfile::setMembers	{my$self=shift;@members=@_;}
	
	sub Logfile::DESTROY{my$self=shift;$self->dispose;}
	
	#dispose -- �ѹ��Ѥߥǡ�����ե��������¸
	sub Logfile::dispose{
		(@members&&@chatlog)||return;
		my$self=shift;
		truncate($path,0);
		seek($fh,0,0);
		print $fh join("\n",@members,'',@chatlog,'');
		close($fh);
		undef$fh;undef@members;undef@chatlog;undef$singleton;
	}
}


#------------------------------------------------------------------------------#
# Chatlog Class
#
{package Chatlog;
	my$logfile;
	my$singleton;
	
	#---------------------------------------
	# Class Methods
	sub Chatlog::new{#private
		my$proto=shift;
		my$class=ref($proto)||$proto;
		$logfile=Logfile->getInstance;
		my$chatlog=[
			map{{/([^\t]+)=\t([^\t]*);\t/go}}
			grep{m/^Mar1=\t[^\t]*;\t(?:[^\t]*=\t[^\t]*;\t)*$/o}$logfile->getChatlog
		];
		
		$singleton=bless $chatlog,$class;
	}
	sub Chatlog::getInstance{$singleton||Chatlog->new;}
	
	#�����ɲ�
	sub Chatlog::add{
		my$proto=shift;my$self=ref($proto)?$proto:getInstance();
		my%DT=%{shift()};
		%DT=map{$_=>$DT{$_}}qw(Mar1 id name color bcolo body icon home email exp hua ra time);
		splice(@{$self},$::CF{'max'}-1);
		unshift(@{$self},\%DT);
	}
	
	#������
	sub Chatlog::delete{
		my$proto=shift;my$self=ref($proto)?$proto:getInstance();
		my%DT=%{shift()};
		for(@{$self}){
			$_->{'id'} eq$DT{'id'} ||next;
			$_->{'exp'}eq$DT{'exp'}||next;
			$_->{'Mar1'}='del';
			last;
		}
	}
	sub Chatlog::dispose{
		$logfile||return;
		my$proto=shift;my$self=ref($proto)?$proto:getInstance();
		$logfile->setChatlog(
			map{
				my%DT=%{$_};
				my$tmp="Mar1=\t$DT{Mar1};\t";
				delete$DT{Mar1};
				$tmp.join('',map{"$_=\t$DT{$_};\t"}keys%DT);
			}@{$self}
		);
		undef$logfile;undef$singleton;
	}
	
	sub Chatlog::DESTROY{my$self=shift;$self->dispose;}
}


#------------------------------------------------------------------------------#
# MEMBERS CLASS
#

{package Members;
	my$logfile;
	my$singleton;
	
	#---------------------------------------
	# Class Methods
	sub Members::new{#private
		my$proto=shift;
		my$class=ref($proto)||$proto;
		$logfile=Logfile->getInstance;
		my$members={
			map{$_->[0]=>{$_->[1]=~/([^\t]+)=\t([^\t]*);\t/go}}
			map{m/^id=\t([^\t]+);\t((?:[^\t]+=\t[^\t]*;\t)+)/o;[$1,$2]}
			grep{m/^id=\t[^\t]+;\t(?:[^\t]+=\t[^\t]*;\t)+/o}$logfile->getMembers
		};
		$singleton=bless $members,$class;
	}
	sub Members::getInstance{$singleton||Members->new;}
	
	sub Members::dispose{
		$logfile||return;
		my$proto=shift;my$self=ref($proto)?$proto:getInstance();
		$logfile->setMembers(
			map{
				my%DT=%{$self->{$_}};
				delete$DT{'id'};
				"id=\t$_;\t".join('',map{"$_=\t$DT{$_};\t"}keys%DT);
			}keys%{$self}
		);
		undef$logfile;undef$singleton;
	}
	
	#���üԤ����
	sub Members::getSingersInfo{
		my$proto=shift;my$self=ref($proto)?$proto:getInstance();
		my@singers;
		for(keys%{$self}){
			my$i=$self->{$_};
			my$limit=$i->{'time'}+(abs($i->{'reload'}-40)<20?$i->{'reload'}*6:360);
			$limit<$^T&&(delete$self->{$_},next);#TimeOver
			exists$i->{'name'}||next;#ROM
			$i->{'blank'}=$^T-$i->{'lastModified'};
			push(@singers,$i);
		}
		return@singers;
	}
	
	#�����οͤ��ɲ�
	sub Members::add{
		my$proto=shift;my$self=ref($proto)?$proto:getInstance();
		my%DT=%{shift()};
		if($DT{'name'}){
			delete$singleton->{"$DT{'ra'}"};
			if($DT{'isActive'}){
				#ǽưŪ�����
				$DT{'lastModified'}=$^T;
			}else{
				#���̤˥����
				$DT{'lastModified'}=$singleton->{"$DT{'id'}"}->{'lastModified'};
				if(!$DT{'reload'}||$^T-$DT{'lastModified'}<300){}
				elsif($DT{'reload'}<280){$DT{'reload'}+=20}
				else{$DT{'reload'}=300;}
			}
			$singleton->{"$DT{'id'}"}={map{$_=>$DT{$_}}qw(id name color bcolo exp reload ra time lastModified hua)};
		}else{
			#���
			$singleton->{"$DT{'ra'}"}={id=>$DT{'ra'},(map{$_=>$DT{$_}}qw(reload ra time hua))};
			$DT{'reload'}+=20;
		}
		return$DT{'reload'};
	}
	
	#�ɤ߹������ѥϥå�����֤�
	sub Members::getOnlyHash{
		my%members;
		if($singleton){
			%members=%{$singleton};
		}else{
			open(MEMBER,'<'.$::CF{'log'});
			eval{flock(MEMBER,1)};
			my@tmp;
			while(<MEMBER>){/\S/o?push(@tmp,$_):last}
			close(MEMBER);
			
			%members=map{$_->[0]=>{($_->[1]=~/([^\t]+)=\t([^\t]*);\t/go)}}
			map{[m/^id=\t([^\t]+);\t((?:[^\t]+=\t[^\t]*;\t)+)/o]}
			grep{m/^id=\t[^\t]+;\t(?:[^\t]+=\t[^\t]*;\t)+/o}@tmp;
		
		}
		return\%members;
	}
	
	sub Members::DESTROY{my$self=shift;$self->dispose;}
}


#------------------------------------------------------------------------------#
# RANKING CLASS
#
{package Rank;
	my$fh;
	my$path=$::CF{'rank'};
	my$singleton;
	
	#---------------------------------------
	# Class Methods
	sub Rank::new{#private
		$fh&& die"�����Singleton�ʤΤ�new�򾡼�˸ƤФʤ��ǡ�getInstance��Ȥ�����";
		my$proto=shift;
		my$class=ref($proto)||$proto;
		my%rank=();
		local*RANK;
		if(-e$::CF{'rank'}){
			open(RANK,'+<'.$path)||die"Can't open Ranking($path)[$?:$!]";
			$fh=*RANK{IO};
			eval{flock($fh,2)};
			seek($fh,0,0);
			%rank=map{$_->[0]=>{($_->[1]=~/([^\t]+)=\t([^\t]*);\t/go)}}
			map{[m/^id=\t([^\t]+);\t((?:[^\t]+=\t[^\t]*;\t)+)/o]}
			grep{m/^id=\t[^\t]+;\t(?:[^\t]+=\t[^\t]*;\t)+/o}<$fh>;
		}else{
			open(RANK,'>'.$::CF{'rank'});
			$fh=*RANK{IO};
			eval{flock($fh,2)};
		}
		$singleton=bless \%rank,$class;
	}
	sub Rank::getInstance{$singleton||Rank->new;}
	
	sub Rank::dispose{
		my$proto=shift;my$self=ref($proto)?$proto:getInstance();
		truncate($path,0);
		seek($fh,0,0);
		print $fh (
			join"\n",map{
				my%DT=%{$self->{$_}};
				delete$DT{'id'};
				"id=\t$_;\t".join('',map{"$_=\t$DT{$_};\t"}keys%DT);
			}keys%{$self}
		);
		close($fh);
		undef$fh;undef$singleton;
	}
	
	#�и��ͤ�+1
	sub Rank::plusExp{
		my$proto=shift;my$self=ref($proto)?$proto:getInstance();
		my%DT=%{shift()};
		
		if(!$singleton->{"$DT{'id'}"}||!$singleton->{"$DT{'id'}"}->{'exp'}){
			$singleton->{"$DT{'id'}"}={name=>$DT{'name'},exp=>1};
		}else{
			$singleton->{"$DT{'id'}"}{'exp'}++;
			$singleton->{"$DT{'id'}"}{'name'}=$DT{'name'};
		}
		$singleton->{"$DT{'id'}"}{'firstContact'}||=$^T;
		$singleton->{"$DT{'id'}"}{'hua'}=$DT{'hua'};
		$singleton->{"$DT{'id'}"}{'ra'}=$DT{'ra'};
		$singleton->{"$DT{'id'}"}{'color'}=$DT{'color'};
		$singleton->{"$DT{'id'}"}{'bcolo'}=$DT{'bcolo'};
		return$singleton->{"$DT{'id'}"}->{'exp'};
	}
	sub Rank::getOnlyHash{
		my%rank;
		if($singleton){
			%rank=%{$singleton};
		}else{
			open(RANK,'<'.$::CF{'rank'});
			eval{flock(RANK,1)};
			<RANK>;#test.
			seek(RANK,0,0);
			%rank=map{$_->[0]=>{($_->[1]=~/([^\t]+)=\t([^\t]*);\t/go)}}
			map{[m/^id=\t([^\t]+);\t((?:[^\t]+=\t[^\t]*;\t)+)/o]}
			grep{m/^id=\t[^\t]+;\t(?:[^\t]+=\t[^\t]*;\t)+/o}<RANK>;
			close(RANK);
		}
		return\%rank;
	}
	
	sub Rank::DESTROY{my$self=shift;$self->dispose;}
}


package main;
#-------------------------------------------------
# �������
#
BEGIN{
	#���顼���Ф��饨�顼���̤�ɽ������褦��
	unless(%CF){
		$CF{'program'}=__FILE__;
		$SIG{'__DIE__'}=$ENV{'REQUEST_METHOD'}?sub{
			if($_[0]=~/^(?=.*?flock)(?=.*?unimplemented)/){return}
			print"Status: 200 OK\nContent-Language: ja-JP\nContent-type: text/plain; charset=euc-jp"
			."\n\n<PRE>\t:: Marldia ::\n   * Error Screen 1.4 (o__)o// *\n\n";
			print"ERROR: $_[0]\n"if@_;
			print join('',map{"$_\t: $CF{$_}\n"}grep{$CF{"$_"}}qw(idxrev correv))
			."\n".join('',map{"$_\t: $CF{$_}\n"}grep{$CF{"$_"}}qw(log icon icls style));
			print"\ngetlogin\t: ".getlogin;
			print"\n".join('',map{"$$_[0]\t: $$_[1]\n"}
			([PerlVer=>$]],[PerlPath=>$^X],[BaseTime=>$^T],[OSName=>$^O],[FileName=>$0],[__FILE__=>__FILE__]))
			."\n\t= = = ENV = = =\n".join('',map{sprintf"%-20.20s : %s\n",$_,$ENV{$_}}grep{$ENV{"$_"}}
			qw(CONTENT_LENGTH QUERY_STRING REQUEST_METHOD
			SERVER_NAME HTTP_HOST SCRIPT_NAME OS SERVER_SOFTWARE PROCESSOR_IDENTIFIER))
			."\n+#      Airemix  Marldia     #+\n+#  http://www.airemix.com/  #+";
			exit;
		}:sub{
			if($_[0]=~/^(?=.*?flock)(?=.*?unimplemented)/){return}
			print@_?"ERROR: $_[0]":'ERROR';
			exit;
		};
	}
	#Revision Number
	$CF{'correv'}=qq$Revision: 1.13 $;
	$CF{'version'}=($CF{'correv'}=~/(\d[\w\.]+)/o)?"v$1":'unknown';#"Revision: 1.4"->"v1.4"
}
1;
__END__
