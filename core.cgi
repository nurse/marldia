#!/usr/local/bin/perl

#------------------------------------------------------------------------------#
# 'Marldia' Chat System
# - Main Script -
#
# $Revision: 1.21 $
# "This file is written in euc-jp, CRLF." ��
# Scripted by NARUSE,Yui.
#------------------------------------------------------------------------------#
# $cvsid = q$Id: core.cgi,v 1.21 2004-11-22 20:55:35 naruse Exp $;
require 5.005;
use strict;
use vars qw(%CF %IN %CK %IC);
#use Data::Dumper;


#-------------------------------------------------
# MAIN SWITCH
#
sub main{
    &getParams;
    #	$IN{'name'}&&index(" $IN{'name'} "," $CF{'denyname'} ")&&&locate($CF{'sitehome'});
    #	$ENV{'REMOT_ADDR'}&&index(" $IN{'REMOT_ADDR'} "," $CF{'denyra'} ")&&(&locate($CF{'sitehome'}));
    #	$ENV{'REMOT_HOST'}&&index(" $ENV{'REMOT_HOST'} "," $CF{'denyrh'} ")&&(&locate($CF{'sitehome'}));

    if('south'eq$IN{'mode'}){
    }elsif('frame'eq$IN{'mode'}){
	&modeFrame;
    }elsif('north'eq$IN{'mode'}){
	&modeNorth;
    }elsif('icct'eq$IN{'mode'}){
	require($CF{'icct'}||'iconctlg.cgi');
	&iconctlg;
    }

    if('admicmd'eq$IN{'mode'}){
	&modeAdmicmd;
    }elsif('usercmd'eq$IN{'mode'}){
	&modeUsercmd;
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
Content-Language: ja
Content-type: text/html; charset=euc-jp

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd">
<HTML lang="ja-JP">
<HEAD>
<META http-equiv="Content-type" content="text/html; charset=euc-jp">
<META http-equiv="Content-Script-Type" content="text/javascript">
<META http-equiv="Content-Style-Type" content="text/css">
<LINK rel="start" href="$CF{'sitehome'}">
<LINK rel="index" href="$CF{'index'}">
<TITLE>$CF{'title'}</TITLE>
</HEAD>
<FRAMESET rows="120,*">
<FRAME frameborder="0" name="north" src="$CF{'index'}?north">
<FRAME frameborder="0" name="south" src="$CF{'program'}?south">
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
    open(JS,$CF{'ProgramDirectory'}.'Marldia.js');
    print qq(<SCRIPT type="text/javascript" defer>\n<!--\n);
    print<JS>;
    print"//-->\n</SCRIPT>";
    close(JS);
    print<<"_HTML_";
<FORM name="north" id="north" method="post" action="$CF{'program'}" target="south"
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
<TD rowspan="5" style="text-align:center;white-space:nowrap" nowrap>
<H1 contentEditable="true">$CF{'pgtit'}</H1>
<BUTTON accesskey="x" type="button" id="surfaceButton" onclick="surfaceSample(event);return false"
onkeypress="surfaceSample(event);return false"><IMG name="preview" id="preview" alt="" title="$CK{'icon'}"
src="$CF{'iconDir'}$CK{'icon'}" $CF{'imgatt'} style="margin:0"></BUTTON><BR>
<LABEL accesskey="z" for="surface" title="sUrface&#10;ɽ�𥢥���������򤷤ޤ��ʻȤ���С�"
>S<SPAN class="ak">u</SPAN>rface</LABEL><SELECT name="surface" id="surface" tabindex="50"
onfocus="if(myIcon.value!=getSelectingIcon())changeOption()" onchange="changeSurface(this.selectedIndex)">
_HTML_
    if($CK{'icon'}=~/^((?:[^\/#]*\/)*)((?:[^\/#.]*\.)*?[^\/#.]+)(\.[^\/#.]*)?#(\d+)$/o){
	print qq(<OPTION value="$1$2$3">-</OPTION>\n);
	for(0..$4){print qq(<OPTION value="$1$2$_$3">$_</OPTION>\n);}
    }else{
	print qq(<OPTION value="$CK{'icon'}">-</OPTION>\n);
    }
    print<<"_HTML_";
</SELECT><BR>
<DIV style="margin:0.3em 0;text-align:center" title="reloadQ&#10;��ե졼������ɤ��ޤ�"
>[<A href="$CF{'index'}?north" accesskey="q" tabindex="52">���ɹ�(<SPAN class="ak">Q</SPAN>)</A>]
<INPUT name="south" type="hidden" value="">
<INPUT name="previousBody" type="hidden" value="">
</DIV>
</TD>
<TH><LABEL accesskey="n" for="name" title="Name&#10;���ü�̾��ȯ����̾�ʤɤǻȤ�̾���Ǥ�"
>̾��(<SPAN class="ak">N</SPAN>)</LABEL>:</TH>
<TD><INPUT type="text" class="text" name="name" id="name" maxlength="20" size="20"
style="ime-mode:active;width:80px" value="$CK{'name'}" tabindex="11">
<LABEL accesskey="k" for="cook" title="cooKie&#10;�����å��������ȸ��ߤ������Cookie����¸���ޤ�"
><INPUT type="checkbox" name="cook" id="cook" class="check" tabindex="12" checked
>Coo<SPAN class="ak">k</SPAN>ie</LABEL></TD>
<TH><LABEL accesskey="c" for="color" title="name Color&#10;���ü�̾��ȯ����̾�ʤɤǻȤ�̾���ο��Ǥ�"
>̾����(<SPAN class="ak">C</SPAN>)</LABEL>:</TH>
<TD>@{[&iptcol('color','tabindex="21"')]}</TD>
<TH><LABEL accesskey="g" for="line" title="log Gyosu&#10;ɽ��������ιԿ��Ǥ�&#10;�ǹ�$CF{'max'}��"
>�Կ�(<SPAN class="ak">G</SPAN>)</LABEL>:</TH>
<TD><INPUT type="text" class="text" name="line" id="line" maxlength="4" size="4"
style="ime-mode:disabled;width:32px" value="$CK{'line'}��" tabindex="31"></TD>
<TD style="text-align:center"><INPUT type="submit" accesskey="s" class="submit"
title="Submit&#10;���ߤ����Ƥ�ȯ�����ޤ�" value="OK" tabindex="41"></TD>
<TD></TD>
</TR>

<TR>
<TH><LABEL accesskey="i" for="icon" title="Icon&#10;���Ѥ��륢����������򤷤ޤ�"
><A href="$CF{'index'}?icct" target="south">��������</A>(<SPAN class="ak">I</SPAN>)</LABEL></TH>
<TD>@{[&iptico($CK{'icon'},'tabindex="13"')]}</TD>
<TH><LABEL accesskey="c" for="bcolo" title="body Color&#10;ȯ��������ʸ�ο��Ǥ�"
>ʸ�Ͽ�(<SPAN class="ak">C</SPAN>)</LABEL>:</TH>
<TD>@{[&iptcol('bcolo','tabindex="22"')]}</TD>
<TH><LABEL accesskey="r" for="reload" title="Reload&#10;���ä��Ȥ˼�ưŪ�˥���ɤ��뤫���Ǥ�"
>�ֳ�(<SPAN class="ak">R</SPAN>)</LABEL>:</TH>
<TD><INPUT type="text" class="text" name="reload" id="reload" maxlength="4" size="4"
style="ime-mode:disabled;width:32px" value="$CK{'reload'}��" tabindex="32"></TD>
<TD style="text-align:center"><INPUT type="reset" class="reset"
title="reset&#10;���Ƥ��������ޤ�" value="����󥻥�" tabindex="42"></TD>
</TR>

<TR>
<TH><LABEL accesskey="b" for="body" title="Body&#10;ȯ��������ʸ�����ƤǤ�&#10;\$rank��ȯ����󥭥󥰡�\$member�ǻ��ü԰����򸫤�ޤ�">����(<SPAN class="ak">B</SPAN>)</LABEL>:</TH>
<TD colspan="5"><INPUT type="text" class="text" name="body" id="body" maxlength="300" size="100"
style="ime-mode:active;width:450px" tabindex="1"></TD>
<TD style="text-align:center"><INPUT type="checkbox" name="quit" id="quit" class="check" tabindex="51"
><LABEL accesskey="Q" for="quit" title="Quit&#10;�����å��������Ȼ��üԤ���̾����ä��ޤ���"
>�༼�⡼��(<SPAN class="ak">Q</SPAN>)</LABEL></TD>
</TR>

<TR>
<TH><LABEL accesskey="y" for="id" title="identitY name&#10;CGI�����ǻ��Ѥ��롢�����Ѥ�̾�������򤷤ޤ�
����̾�����ºݤ�ɽ�˽Ф뤳�ȤϤ���ޤ���\n������Ͽ̾��Ʊ������Ʊ���ʪ���Ȥߤʤ���ޤ�"
>Identit<SPAN class="ak">y</SPAN></LABEL>:</TH>
<TD><INPUT type="text" class="text" name="id" id="id" maxlength="20" size="20"
style="ime-mode:active;width:150px" value="$CK{'id'}" tabindex="101"></TD>
<TH><LABEL accesskey="l" for="email" title="e-maiL&#10;�᡼�륢�ɥ쥹�Ǥ�"
>E-mai<SPAN class="ak">l</SPAN></LABEL>:</TH>
<TD colspan="3"><INPUT type="text" class="text" name="email" id="email" maxlength="200" size="40"
style="ime-mode:inactive;width:200px" value="$CK{'email'}" tabindex="111"></TD>
<TH style="text-align:center">[ <A href="$CF{'sitehome'}" target="_top"
title="$CF{'sitename'}�ص���ޤ�&#10;�༼��å������ϽФʤ��Τǵ���ΰ�����˺�줺��"
>$CF{'sitename'}�ص���</A> ]</TH>
</TR>

<TR>
<TH><LABEL accesskey="p" for="opt" title="oPtion&#10;���ץ����"
>O<SPAN class="ak">p</SPAN>tion</LABEL>:</TH>
<TD><INPUT type="text" class="text" name="opt" id="opt" maxlength="200" style="ime-mode:inactive;width:150px"
value="$CK{'opt'}" tabindex="102" onchange="changeOption()"></TD>
<TH><LABEL accesskey="o" for="home" title="hOme&#10;�����Ȥ�URL�Ǥ�"
>H<SPAN class="ak">o</SPAN>me</LABEL>:</TH>
<TD colspan="3"><INPUT type="text" class="text" name="home" id="home" maxlength="200" size="40"
style="ime-mode:inactive;width:200px" value="$CK{'home'}" tabindex="112"></TD>
<TH style="letter-cpacing:-1px;text-align:center">-<A href="http://www.airemix.com/" title="Airemix�ؤ��äƤߤ�"
target="_top">Marldia $CF{'version'}</A>-</TH>
</TR>
</TABLE>
</FORM>

<SCRIPT type="text/javascript" defer>
<!--
/*========================================================*/
// �����
var iconDirectory='$CF{'iconDir'}';
var iconSetting=@{[$CF{'absoluteIcon'}?1:0]}+@{[$CF{'relativeIcon'}?1:0]}*2;
var myIcon=new Object({value:'$CK{'icon'}',isAbsolute:0});
window.onload=init;
//-->
</SCRIPT>

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
    #View�ζ��̽���
    my ($chatlog,$members) = &commonRoutineForView();
    
    #-----------------------------
    #������
    my$query='south';
    my $mobileQuery ='south;';
    if($IN{'id'}){
	$query=join(';',map{my$val=$IN{$_};$val=~s{(\W)}{'%'.unpack('H2',$1)}ego;"$_=$val"}
		    grep{defined$IN{$_}}qw(name id line reload color));
	if($IN{'quit'}){
	    $query.=';quit=on';
	    $IN{'reload'} = 0;
	}
    }
    
    #-----------------------------
    #���������ѥ�����
    my $mobileQuery ='south;' .
    	join(';',map{my$val=$IN{$_};$val=~s/&#64;/\@/;$val=~s{(\W)}{'%'.unpack('H2',$1)}ego;"$_=$val"}
	     grep{defined$IN{$_}}qw(line name color bcolo icon id email opt home))
	if $IN{'icon'};
    
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
    my $additionalHeader = <<"_HTML_";
<SCRIPT type="text/javascript">
<!--
function reload(){
  self.location = '$CF{'index'}?$query';
}
setTimeout(reload, $IN{'reload'}000);
//-->
</SCRIPT>
<NOSCRIPT>
<META http-equiv="refresh" content="$IN{'reload'};url='$CF{'index'}?$query'">
</NOSCRIPT>
_HTML_
    
    &header($IN{'reload'}?$additionalHeader:'');
    
    #-----------------------------
    #���ü�ɽ��
    my $reload = $IN{'reload'} ? sprintf('%s�ôֳ�',$IN{'reload'}) : 'No Reload';
    $reload = sprintf( '<A href="%s?%s">%s</A>', $CF{'mobile'}, $mobileQuery, $reload) if $mobileQuery;
    print<<"_HTML_";
<TABLE class="meminfo" summary="���üԾ���ʤ�"><TR>
<TD class="reload">[ <A href="$CF{'index'}?$query">@{[sprintf('%02d:%02d:%02d',(localtime$^T)[2,1,0])]}</A> ]</TD>
<TD class="member">[���:$intMembers�� ���ü�:$intSingers�� �ѵ�:$intAudiences��] [ $strMembers ]</TD>
<TD class="respan">($reload)</TD>
</TR></TABLE>
_HTML_
    
    #-----------------------------
    #��ɽ��
    my$i=0;
    for(@{$chatlog}){
	my%DT=%{$_};
	'del'eq$DT{'Mar1'}&&next;
	++$i>$IN{'line'}&&last;

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
	$DT{'_Icon'}=&getIconTag(\%DT)||'&nbsp;';
	#��٥����
	$DT{'level'}=&getLevel($DT{'exp'});
	#����ܥ���
	my$del=$IN{'id'}&&$DT{'id'}eq$IN{'id'}?qq([<A href="$CF{'index'}?del=$DT{'exp'}&#59;$query">���</A>])
	    :'&nbsp;';
	#����
	print<<"_HTML_";
<TABLE cellspacing="0" class="article" summary="article">
<TR>
<TH class="articon" rowspan="2">$DT{'_Icon'}</TH>
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
# ��٥�׻�
#
sub getLevel{
    #��٥�׻�-�ޤȤ�
    my$lev=0;
    my$sum=0;
    while($sum<$_[0]){
	$lev++;
	$sum+=int(exp(($lev-1)/15)*100);
    }
    return $lev;
    #��٥�׻�-�Ƥ��ȡ�
    srand($_[0]);
    return 1+int(rand(sqrt$_[0]*2));
}


#-------------------------------------------------
# ���Ѽԥ��ޥ��
#
sub modeUsercmd{
    unless($IN{'opt'}){
	die"�ֲ��⤷�ʤ���������";
    }
    #��������
    my@arg=grep{s/\\(\\)|\\(")|"/$1$2/go;$_;}($IN{'opt'}=~
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
<COL span="4">
<TH scope="col">�����</TH>
<TH scope="col">�ʤޤ�</TH>
<TH scope="col">���������</TH>
<TH scope="col">���礦����</TH>
<TH scope="col">�ϤĤȤ����礦</TH>
_HTML_
	my $i = 0;
	for(sort{$b->{'exp'}<=>$a->{'exp'}}values%{Rank->getOnlyHash}){
	    $i++;
	    print<<"_HTML_";
<TR>
<TD style="color:$_->{'color'}">$i</TD>
<TD style="color:$_->{'color'}">$_->{'name'}</TD>
<TD style="color:$_->{'bcolo'}">$_->{'exp'}</TD>
<TD style="color:$_->{'bcolo'}">@{[$_->{'lastContact'}?&datef($_->{'lastContact'},'dateTime'):'<HR>']}</TD>
<TD style="color:$_->{'bcolo'}">@{[$_->{'firstContact'}?&datef($_->{'firstContact'},'dateTime'):'<HR>']}</TD>
</TR>
_HTML_
	}
	print"</TABLE>\n";
	&showFooter;
	exit;
    }elsif('member'eq$arg[0]){
	#��ʪ�Ͱ���
	&header;
	print<<'_HTML_';
<TABLE class="table" summary="���üԤΰ���">
<CAPTION>���󤫤��� �������ʤ桼�����⡼�ɡ�</CAPTION>
<COL span="3">
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
    unless($IN{'opt'}){
	die"�ֲ��⤷�ʤ���������";
    }
    #��������
    my@arg=grep{s/\\(\\)|\\(")|"/$1$2/go;length$_;}
    ($IN{'opt'}=~
     /(?!\s)[^"\\\s]*(?:\\[^\s][^"\\\s]*)*(?:"[^"\\]*(?:\\.[^"\\]*)*(?:"[^"\\\s]*(?:\\[^\s][^"\\\s]*)*)?)*\\?/go);
    
=item �������ޥ��

$CF{'admipass'}='admicmd';�ʤ顢
#admicmd ...
��...�Ȥ������ޥ�ɤ�ȯư

��rank (del|merge|conv) <id ...>
��󥭥󥰤�ɽ��
��del
�����Ȥ��ƻ��ꤵ�줿ID�ξ������
��merge
��������ID�ˡ�����ʹߤ�ID�����礹��
��conv
1.5�����Υ�󥭥󥰥ǡ�����1.6�������Ѵ�����

��mem
���üԾ����ɽ��

��del <id> [<exp>]
ȯ�����

=cut

    #ʬ��
    if(!$arg[0]){
    }elsif('rank'eq$arg[0]){
	#ȯ����󥭥�
	my$rank=Rank->getInstance;
	unless($arg[1]){
	}elsif('del'eq$arg[1]){
	    #��󥭥󥰤�����
	    $rank->delete($arg[2]);
	}elsif('merge'eq$arg[1]){
	    #ID����ӷи��Ϥ�����
	    exists$rank->{$arg[2]}&&exists$rank->{$arg[2]}->{'exp'}||die"����ʿͤ��ʤ�";
	    for(3..$#arg){
		(!$rank->{$arg[$_]}||!$rank->{$arg[$_]}->{'exp'})&&next;
		$rank->{$arg[2]}->{'exp'}+=$rank->{$arg[$_]}->{'exp'};
		$rank->delete($arg[$_]);
	    }
	}

	#��󥭥�ɽ��
	&header;
	print<<'_HTML_';
<TABLE class="table" summary="ȯ����󥭥�">
<CAPTION>Ķ��ȯ����󥭥�</CAPTION>
<COL span="7">
<TH scope="col">RANK</TH>
<TH scope="col">NAME</TH>
<TH scope="col">ID</TH>
<TH scope="col">EXP</TH>
<TH scope="col">LAST CONTACT</TH>
<TH scope="col">FIRST CONTACT</TH>
<TH scope="col">REMOTE_ADDR</TH>
<TH scope="col">HTTP_USER_AGENT</TH>
_HTML_
	my %rank = %{$rank->getOnlyHash()};
	my $i = 0;
	for(map{{id=>$_,%{$rank{$_}}}}sort{$rank{$b}->{'exp'}<=>$rank{$a}->{'exp'}}keys%rank){
	    $i++;
	    print<<"_HTML_";
<TR>
<TD style="color:$_->{'color'}">$i</TD>
<TD style="color:$_->{'color'}">$_->{'name'}</TD>
<TD style="color:$_->{'bcolo'}">$_->{'id'}</TD>
<TD style="color:$_->{'bcolo'}">$_->{'exp'}</TD>
<TD style="color:$_->{'bcolo'}">@{[$_->{'lastContact'}?&datef($_->{'lastContact'},'dateTime'):'<HR>']}</TD>
<TD style="color:$_->{'bcolo'}">@{[$_->{'firstContact'}?&datef($_->{'firstContact'},'dateTime'):'<HR>']}</TD>
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
<COL span="6">
<TH scope="col">NAME</TH>
<TH scope="col">ID</TH>
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
<TD style="color:$_->{'bcolo'}">@{[$_->{'id'} or '']}</TD>
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
	my @result = Chatlog->delete({id=>$arg[1],exp=>$arg[2]});
	&header;
	if(@result){
	    print"<P>������ޤ�����</P>";
	}else{
	    print"<P>�ʤˤ������ʤ��ä���</P>";
	}
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
Content-Language: ja-JP
Pragma: no-cache
Cache-Control: no-cache
Location: $i
Content-type: text/html; charset=euc-jp

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
    unless($ENV{'REQUEST_METHOD'}){
    }elsif('HEAD'eq$ENV{'REQUEST_METHOD'}){ #forWWWD
	#Method��HEAD�ʤ��LastModifed����Ϥ��ơ�
	#�Ǹ����ƻ�����Τ餻��
	my$last=&datef((stat("$CF{'rank'}"))[9],'rfc1123');
	print"Status: 200 OK\nLast-Modified: $last\n"
	    ."Content-Type: text/plain\n\nLast-Modified: $last";
	exit;
    }
    my$input=Input->getInstance;
    %IN=%{$input->filtering};
}


#-------------------------------------------------
# Header with G-ZIP etc.
#
sub header{
    print<<'_HTML_';
Status: 200 OK
Pragma: no-cache
Cache-Control: no-cache
Content-Language: ja-JP
Content-type: text/html; charset=euc-jp
_HTML_
    #GZIP Switch
    my$status='';
    $status.=join ''
	,map{qq(<META http-equiv="Set-Cookie" content="$_">\n)}split("\n",$CF{'-setCookie'})if$CF{'-setCookie'};
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
	print ' 'x 2048if$ENV{'HTTP_USER_AGENT'}&&index($ENV{'HTTP_USER_AGENT'},'MSIE')+1; #IE�ΥХ��к�
	$status='<!-- gzip enable -->';
    }else{
	print"\n";
	$status='<!-- gzip disable -->';
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
<LINK rel="stylesheet" type="text/css" href="$CF{'style'}">
<LINK rel="start" href="$CF{'sitehome'}">
<LINK rel="index" href="$CF{'index'}">
<TITLE>$CF{'title'}</TITLE>
$status
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
    $cook=~s{(\W)}{'%'.unpack('H2',$1)}ego;
    my$expires=$^T+33554432; #33554432=2<<24; #33554432�Ȥ����������ä˰�̣�Ϥʤ������ʤߤ˰�ǯ�Ⱦ���
    $CF{'-setCookie'}="Marldia=$cook; expires=".&datef($expires,'cookie');
    $CF{'set_cookie_by_meta_tags'}=1if index($ENV{'SERVER_NAME'},'tok2.com')>-1&&!defined$CF{'set_cookie_by_meta_tags'};
    if($CF{'set_cookie_by_meta_tags'}){
	#tok2�к�
    }else{
	print map{qq(Set-Cookie: $_\n)}split("\n",$CF{'-setCookie'});
	undef($CF{'-setCookie'});
    }
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
    defined$_[0]||return undef;
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
#������������
sub commonRoutineForView{
    #-----------------------------
    #���ޥ�ɤ��ɤ߹���
    my%EX;
    for(split(';',$IN{'opt'})){
	my($i,$j)=split('=',$_,2);
	$i||next;
	$i=~/(\S+(?:\s+\S+)*)/o||next;
	$i=$1;
	$j=defined$j&&$j=~/(\S+(?:\s+\S+)*)/o?$1:'';
	$EX{$i}=$j;
    }
    
    #���ѥ�������ǽ��index.cgi�����ꤹ�롣
    #index.cgi�ǻ��ꤷ����������ѥ���ɤ˹��פ���С�
    $IN{'icon'}=$IC{$EX{'icon'}}if$CF{'exicon'}&&$IC{$EX{'icon'}};
    
    #���л��ꥢ������
    $IN{'icon'}=''if$CF{'absoluteIcon'}&&$EX{'absoluteIcon'};
    #���л��ꥢ������
    $IN{'icon'}=''if$CF{'relativeIcon'}&&$EX{'relativeIcon'};
    #ɽ�𥢥�����
    $IN{'icon'}=$IN{'surface'}if!$IN{'icon'}&&$IN{'surface'};
    
    $IN{'body'}=$IN{'body'}?Filter->filteringBody($IN{'body'},%EX):'';
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
	#��󥭥󥰲���
	$IN{'exp'}=Rank->plusExp(\%IN);
	#ȯ������
	$chatlog->add(\%IN);
    }elsif($IN{'del'}){
	#ȯ�����
	$chatlog->delete({id=>$IN{'id'},exp=>$IN{'del'}});
    }
    return($chatlog,$members);
}


#-------------------------------------------------
# ���������Ѥ�IMG����
#
sub getIconTag{
=item ����

$ ������������ä��ϥå���ؤΥ�ե����
;
$ �ɤΤ褦�ʷ����֤���������

=item �֤�������
��-!keyword!-�פΤ褦�ʷ����Ǥ�
����Ū�ˤϰʲ��ΤȤ���
:-!src!-
dir+file
:-!dir!-
dir\
:-!file!-
file

=cut

    my$data=shift;
    my$text=shift||qq(<IMG src="-!src!-" alt="" title="-!dir!-+-!file!-" $CF{'imgatt'}>);
    my%DT=(dir=>$CF{'iconDir'},file=>$data->{'icon'});
    if($CF{'absoluteIcon'}&&$data->{'opt'}=~/(?:^|;)absoluteIcon=([^#]*)/o){
	#���л��ꥢ������
	$DT{'dir'}='';
	$DT{'file'}||=$1;
    }elsif($CF{'relativeIcon'}&&$data->{'opt'}=~/(?:^|;)relativeIcon=([^;:.]*(?:\.[^;:.]+)*)/o){
	#���л��ꥢ������
	$DT{'file'}||=$1;
    }
    if($DT{'file'}){
	$DT{'src'}=$DT{'dir'}.$DT{'file'};
	$text=~s/(-!(\w+)!-)/defined$DT{$2}?$DT{$2}:$1/ego;
    }else{
	$text=undef;
    }
    return$text;
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

    my$opt=$_[1]?" $_[1]":'';
    if($CF{'-CacheIconList'}&&('reset'ne$_[2])){
	#����å���Ǥ���$CF{'-CacheIconList'}���֤�
	return$CF{'-CacheIconList'};
    }

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
    my$isEconomy=$CK{'opt'}=~/(?:^|;)iconlist=economy(?:\s*;|$)/o;
    my$isAbsolute=0;
    my$isDisabled='';
    unless(@_){
    }elsif($CF{'exicon'}&&($CK{'opt'}=~/(?:^|;)icon=([^;]*)/o)&&$IC{$1}){
	#�ѥ���ɷ�
	$_[0]=$IC{$1};
	if($isEconomy){
	    $iconlist=qq(<OPTION value="$_[0]" selected>���ѥ�������</OPTION>\n);
	}else{
	    $iconlist.=qq(<OPTION value="$_[0]" selected>���ѥ�������</OPTION>\n);
	}
    }elsif($CF{'absoluteIcon'}&&$CK{'opt'}=~/(?:^|;)absoluteIcon=([^;]*)/o){
	#���л��ꥢ������
	$_[0]=$1;
	$isAbsolute=1;
	$isDisabled=1;
	$iconlist=qq(<OPTION value="$_[0]" selected>���л���</OPTION>\n)if$isEconomy;
    }elsif($CF{'relativeIcon'}&&$CK{'opt'}=~/(?:^|;)relativeIcon=([^;:.]*(\.[^;:.]+)*)/o){
	#���л��ꥢ������
	$_[0]=$1;
	$iconlist=qq(<OPTION value="$1" selected>���л���</OPTION>\n)if$isEconomy;
	$isDisabled=1;
    }elsif($_[0]and$iconlist=~s/^(.*value=(["'])$_[0]\2)(.*)$/$1 selected$3/imo){
	$iconlist="$1 selected$3"if$isEconomy;
    }elsif($iconlist=~s/value=(["'])(.+?)\1/value=$1$2$1 selected/io){
	$_[0]=$2;
    }
    $_[0]=$CF{'icondir'}.$_[0]unless$isAbsolute;
    $isDisabled&&=' disabled';
    $CF{'-CacheIconList'}=<<"_HTML_";
<SELECT name="icon" id="icon" onchange="document.images['preview'].src=iconDirectory+this.value;document.images['preview'].title=this.value;"$opt$isDisabled>
$iconlist</SELECT>
_HTML_
    return$CF{'-CacheIconList'};
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
<H2 class="heading2">- ���顼��ȯ�����ޤ��� -</H2>
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
# Input Class
#
{package Input;
    my$singleton;
    #---------------------------------------
    # Class Methods
    sub Input::new{#private
	$singleton&&die '�����Singleton�ʤΤ�new�򾡼�˸ƤФʤ��ǡ�getInstance��Ȥ�����';
	my$class=ref($_[0])||$_[0];shift;

	my$params;
	my@params;
	#��������
	unless($ENV{'REQUEST_METHOD'}){@params=@ARGV}
	elsif('HEAD'eq$ENV{'REQUEST_METHOD'}){return}
	elsif('POST'eq$ENV{'REQUEST_METHOD'}){read(STDIN,$params,$ENV{'CONTENT_LENGTH'})}
	elsif('GET'eq$ENV{'REQUEST_METHOD'}){$params=$ENV{'QUERY_STRING'}}
	# EUC-JPʸ��
	my$eucchar=qr((?:[\x09\x0A\x0D\x20-\x7E]|[\x8E\xA1-\xFE][\xA1-\xFE]|\x8F[\xA1-\xFE]{2}))x;

	#������ϥå����
	if(!$params){
	}elsif(length$params>262114){ # 262114:�����������ξ��(byte)
	    #����������
	    &showHeader;print"������ʤ�Ǥ��̤�¿�����ޤ�\n$params";&showFooter;exit;
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
	    $j=$j=~/($eucchar*)/o?$1:'';
	    #�ᥤ��ե졼��β��Ԥ�\x85�餷�����ɡ��б�����ɬ�פʤ���͡�
	    $j=~s/\x0D\x0A/\n/go;$j=~tr/\r/\n/;
	    if('body'ne$i){
		#��ʸ�ʳ������̥����ػ�
		$j=~s/\t/&nbsp;&nbsp;/go;
		$j=~s/&(#?\w+;)?/$1?"&$1":'&#38;'/ego;
		$j=~s/"/&#34;/go;
		$j=~s/'/&#39;/go;
		$j=~s/</&#60;/go;
		$j=~s/>/&#62;/go;
		$j=~s/\n+$//o;
		$j=~s/\n/<BR>/go;
	    }#��ʸ�ϸ�ǤޤȤ��
	    $DT{$i}=$j;
	}

	$singleton=bless\%DT,$class;
    }

    sub Input::getInstance{$singleton||Input->new}
    sub Input::filtering{
	my$self=ref($_[0])?$_[0]:getInstance();shift;
	my$tmp=Filter->filtering($singleton);
	$singleton=bless$tmp,ref$self;
    }

    #	sub Logfile::DESTROY{shift->dispose}
}


#------------------------------------------------------------------------------#
# Filter Class
#
{package Filter;
    # EUC-JPʸ��
    my$eucchar=qr((?:[\x09\x0A\x0D\x20-\x7E]|[\x8E\xA1-\xFE][\xA1-\xFE]|\x8F[\xA1-\xFE]{2}))x;
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
    sub Filter::filtering{
	shift;
	my%DT=%{shift()};
	my%IN;
	#���ޥ�ɷ�
	if($DT{'body'}){
	    if($::CF{'admipass'}&&$DT{'body'}=~/^#$::CF{'admipass'}\s+(.*)/o){
		$IN{'mode'}='admicmd';
		$IN{'opt'}=$1;
	    }elsif($DT{'body'}=~/^\$(\w.*)/o){
		$IN{'mode'}='usercmd';
		$IN{'opt'}=$1;
	    }
	    $IN{'mode'}&&return\%IN;
	}

	if(!%DT||($DT{'mode'}&&'frame'eq$DT{'mode'})){
	    #�ե졼��
	    $IN{'mode'}='frame';
	}elsif(defined$DT{'icct'}){
	    #�������󥫥���
	    $IN{'page'}=($DT{'page'}&&$DT{'page'}=~/([1-9]\d*)/o)?$1:1;
	    $IN{'mode'}='icct';
	}elsif($DT{'name'}){
	    &::getCookie;

	    if(defined$DT{'body'}){
		$IN{'body'}=$DT{'body'}||'';
		$IN{'cook'}=$DT{'cook'}?1:0;
	    }
	    if(defined$DT{'del'}){
		$IN{'del'}=$1 if$DT{'del'}=~/([1-9]\d*)/o;
	    }
	    $IN{'name'}=($DT{'name'}=~/(.{1,100})/o)?$1:'';
	    $IN{'id'}=($DT{'id'}=~/(.{1,100})/o)?$1:($::CK{'id'}||$IN{'name'});
	    $IN{'color'}=($DT{'color'}=~/([\#\w\(\)\,]{1,20})/o)?$1:'';
	    $IN{'bcolo'}=($DT{'bcolo'}=~/([\#\w\(\)\,]{1,20})/o)?$1:'';
	    $DT{'email'}=($DT{'email'}=~/(.{1,200})/o)?$1:'';
	    $IN{'email'}=($DT{'email'}=~/($mail_regex)/o)?$1:'';
	    $IN{'email'}=~s/\@/&#64;/o;
	    $DT{'home'}=($DT{'home'}=~/(.{1,200})/o)?$1:'';
	    $IN{'home'}=($DT{'home'}=~/($http_URL_regex)/o)?$1:'';
	    $IN{'icon'}=($DT{'icon'}=~/([\w\:\.\~\-\%\/\#]+)/o)?$1:'';
	    $IN{'surface'}=$1 if$DT{'surface'}=~/(.+)/o;
	    $IN{'quit'}=$DT{'quit'}?1:0;
	    $IN{'opt'}=$1 if$DT{'opt'}=~/(.+)/o;
	    $IN{'line'}=($DT{'line'}=~/([1-9]\d*)/o)?$1:$::CF{'defline'};
	    $IN{'reload'}=($DT{'reload'}=~/([1-9]\d+|0)/o)?$1:$::CF{'defreload'};
	    $IN{'mode'}='south';
	}elsif((defined$DT{'north'})||('north'eq$DT{'mode'})){
	    #��
	    $IN{'mode'}='north';
	    $IN{'line'}=$::CF{'defline'};
	    $IN{'reload'}=$::CF{'defreload'};
	}elsif(defined$DT{'south'}){
	    #��
	    $IN{'mode'}='south';
	    $IN{'line'}=$::CF{'romline'};
	    $IN{'reload'}=$::CF{'romreload'};
	}
	$IN{'ra'}=($ENV{'REMOTE_ADDR'}&&$ENV{'REMOTE_ADDR'}=~/([\d\:\.]{2,56})/o)?"$1":'';
	$IN{'hua'}=($ENV{'HTTP_USER_AGENT'}&&$ENV{'HTTP_USER_AGENT'}=~/($eucchar+)/o)?"$1":'';
	$IN{'hua'}=~tr/\x09\x0A\x0D/\x20\x20\x20/;
	if(exists$DT{'change'}){
	    #ChangeChat
	    $IN{'mode'}='change';
	}
	return\%IN;
    }
    sub Filter::filteringBody{
	my$pkg=shift;
	my$str=shift;
	my%EX=@_;
	#-----------------------------
	#��ʸ�ν���
	#form->data�Ѵ�
	unless(defined$str&&length$str){
	    $str='';
	}elsif($::CF{'tags'}&&'ALLALL'eq$::CF{'tags'}){
	    #ALLALL������OK��â����Ĵ��̵����URI��ư��󥯤�̵����
	    #�����ǥ�󥯤�ĥ�ä��ꡢ��Ĵ���Ƥ����Τ���Ť˥�󥯡���Ĵ���Ƥ��ޤ��ޤ�����
	}else{
	    #��ʸ�Τߥ�����ȤäƤ⤤������ˤ�Ǥ���
	    my$attrdel=0;#°����ä�/�ä��ʤ�(1/0)
	    study$str;
	    $str=~tr/"'<>/\01-\04/;
	    $str=~s/&(#?\w+;)/\05$1/go;

	    #��������
	    if($::CF{'tags'}&&!$EX{'notag'}){
		my$tag_regex_='[^\01-\04]*(?:\01[^\01]*\01[^\01-\04]*|\02[^\02]*\02[^\01-\04]*)*(?:\04|(?=\03)|$(?!\n))';
		my$comment_tag_regex='\03!(?:--[^-]*-(?:[^-]+-)*?-(?:[^\04-]*(?:-[^\04-]+)*?)??)*(?:\04|$(?!\n)|--.*$)';
		my$text_regex='[^\03]*';

		my$tags=$::CF{'tags'};
		my%tagCom=map{/(!\w+)(?:\(([^()]+)\))?/o;$1," $2 "||''}($tags=~/!\w+(?:\([^()]+\))?/go);
		if($tagCom{'!SELECTABLE'}){
		    $tags.=' '.join(' ',grep{$tagCom{'!SELECTABLE'}=~/ $_ /o}grep{/\w+/}split(/\s+/,$EX{'usetag'}));
		}elsif(defined$tagCom{'!SELECTABLE'}){
		    $tags='\w+';
		}

		my$result='';
		#�⤷ BR������ A�����ʤ�����Υ��������Ϻ���������ʤ����ˤϡ� 
		#$tag_tmp = $2; �θ�ˡ����Τ褦�ˤ��� $tag_tmp �� $result �˲ä���褦�ˤ���ФǤ��ޤ��� 
		#$result .= $tag_tmp if $tag_tmp =~ /^<\/?(BR|A)(?![\dA-Za-z])/io;
		my$remain=join('|',grep{/^(?:\\w\+|\w+)$/o}split(/\s+/o,$tags));
		#�դ� FONT������ IMG�����ʤ�����Υ�������������������ˤϡ� 
		#$tag_tmp = $2; �θ�ˡ����Τ褦�ˤ��� $tag_tmp �� $result �˲ä���褦�ˤ���ФǤ��ޤ��� 
		#$result .= $tag_tmp if $tag_tmp !~ /^<\/?(FONT|IMG)(?![\dA-Za-z])/io;
		my$pos=length$str;
		while($str=~/\G($text_regex)($comment_tag_regex|\03$tag_regex_)?/gso){
		    $pos=pos$str;
		    ''eq$1&&!$2&&last;
		    $result.=$1;
		    my$tag_tmp=$2;
		    if($tag_tmp=~s/^\03((\/?(?:$remain))(?![\dA-Za-z]).*)\04/<$1>/io){
			$tag_tmp=~tr/\01\02/"'/;
			$result.=$attrdel?"<$2>":$tag_tmp;
		    }else{
			$result.=$tag_tmp;
		    }
		    if($tag_tmp=~/^<(XMP|PLAINTEXT|SCRIPT)(?![\dA-Za-z])/io){
			$str=~/(.*?)(?:<\/$1(?![\dA-Za-z])$tag_regex_|$)/gsi;
			(my$tag_tmp=$1)=~tr/\01-\04/"'<>/;
			$result.=$tag_tmp;
		    }
		}
		$str=$result.substr($str,$pos);
	    }else{
		#���ĥ���̵��orCommand:notag
	    }

	    #URI��ư���
	    if($::CF{'noautolink'}||!$EX{'noautolink'}){
		#�²�ư��
		my$href_regex=qr{($http_URL_regex|$ftp_URL_regex|($mail_regex))};
		my@isMail=('<A class="autolink" href="mailto:','<A class="autolink" href="');
		$str=~s{((?:\G|>)[^<]*?)$href_regex}{$1$isMail[!$3]$2" target="_blank">$2</A>}go;
		if($str=~/<(?:XMP|PLAINTEXT|SCRIPT)(?![0-9A-Za-z])/io){
		    #XMP/PLAINTEXT/SCRIPT����������Ȥ�
		    $str=~s{(<(XMP|PLAINTEXT|SCRIPT)(?![0-9A-Za-z]).*?(?:<\/$2\s*>|$))}
		    {(my$element=$1)=~s/<A class="autolink"[^>]+>(.*?)<\/A>/$1/gos;$element}egios;
		}
	    }else{
		#Command:nolink
	    }

	    $str=~s/&/&#38;/go;
	    $str=~s/\01/&#34;/go;
	    $str=~s/\02/&#39;/go;
	    $str=~s/\03/&#60;/go;
	    $str=~s/\04/&#62;/go;
	    $str=~tr/\05/&/;
	}
	$str=~s/\t/&nbsp;&nbsp;/go;
	$str=~s/\n/<BR>/go;
	return$str;
    }
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
	$singleton&&die '�����Singleton�ʤΤ�new�򾡼�˸ƤФʤ��ǡ�getInstance��Ȥ�����';
	my$class=ref($_[0])||$_[0];shift;
	local*LOGFILE;
	if(-e$path){
	    open(LOGFILE,'+<'.$path)||die"Can't read Logfile($path)[$?:$!]";
	    #+>>�Ȥ����seek($fh,0,0)��ư���Ƥ���ʤ��Τ���ա�
	    $fh=*LOGFILE{IO};
	    eval{flock($fh,2)};
	    #member���ɲ�
	    while(<$fh>){/\S/o?push(@members,$_):last}
	    #chatlog���ɲ�
	    while(<$fh>){/\S/o&&push(@chatlog,$_)}
	}else{
	    open(LOGFILE,'>>'.$path)||die"Can't create Logfile($path)[$?:$!]";
	    $fh=*LOGFILE{IO};
	    eval{flock($fh,2)};
	    @members=();
	    @chatlog=();
	}

	$singleton=bless[\@chatlog,\@members],$class;
    }

    sub Logfile::getInstance{$singleton||Logfile->new}
    sub Logfile::getChatlog	{$singleton||Logfile->new;return@chatlog}
    sub Logfile::getMembers	{$singleton||Logfile->new;return@members}

    sub Logfile::setChatlog	{@chatlog=(@_[1..$#_])if$#_}
    sub Logfile::setMembers	{@members=(@_[1..$#_])if$#_}

    sub Logfile::DESTROY{shift->dispose}

    #dispose -- �ѹ��Ѥߥǡ�����ե��������¸
    sub Logfile::dispose{
	(@members&&@chatlog)||return;
	my$self=shift;
	truncate($path,0);#$fh�������
	seek($fh,0,0);
	print $fh map{$_."\n"}map{/(.*)/o}@members,'',@chatlog,'';
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
	$singleton&&die '�����Singleton�ʤΤ�new�򾡼�˸ƤФʤ��ǡ�getInstance��Ȥ�����';
	my$class=ref($_[0])||$_[0];shift;
	$logfile=Logfile->getInstance;
	my$self=[
		 map{{/([^\t]+)=\t([^\t]*);\t/go}}
		 grep{/^Mar1=\t[^\t]*;\t(?:[^\t]*=\t[^\t]*;\t)*$/o}$logfile->getChatlog
		];

	$singleton=bless$self,$class;
    }
    sub Chatlog::getInstance{$singleton||Chatlog->new;}

    #�����ɲ�
    sub Chatlog::add{
	my$self=ref($_[0])?$_[0]:getInstance();shift;
	my%DT=%{shift()};
	%DT=map{$_=>$DT{$_}}grep{$DT{$_}}qw(Mar1 id name color bcolo body icon home email exp hua ra time opt);
	splice(@{$self},$::CF{'max'}-1);
	unshift(@{$self},\%DT);
    }

    #������
    sub Chatlog::delete{
	my$self=ref($_[0])?$_[0]:getInstance();shift;
	my%DT=%{shift()};
	my @result = ();
	if($DT{'exp'}){
	    for(@{$self}){
		$_->{'id'} eq$DT{'id'} ||next;
		$_->{'exp'}eq$DT{'exp'}||next;
		$_->{'Mar1'}='del';
		push @result, $DT{'id'}, $DT{'exp'};
		last;
	    }
	}else{
	    for(@{$self}){
		$_->{'id'}eq$DT{'id'}||next;
		$_->{'Mar1'}='del';
		push @result, $DT{'id'} unless @result;
		push @result, $DT{'exp'};
	    }
	}
	return @result;
    }
    sub Chatlog::dispose{
	$logfile||return;
	my$self=ref($_[0])?$_[0]:getInstance();shift;
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
	$singleton&&die '�����Singleton�ʤΤ�new�򾡼�˸ƤФʤ��ǡ�getInstance��Ȥ�����';
	my$class=ref($_[0])||$_[0];shift;
	$logfile=Logfile->getInstance;
	my$self={
	    map{$_->[0]=>{$_->[1]=~/([^\t]+)=\t([^\t]*);\t/go}}
	    map{/^id=\t([^\t]+);\t((?:[^\t]+=\t[^\t]*;\t)+)/o;[$1,$2]}
	    grep{/^id=\t[^\t]+;\t(?:[^\t]+=\t[^\t]*;\t)+/o}$logfile->getMembers
	};
	$singleton=bless$self,$class;
    }
    sub Members::getInstance{$singleton||Members->new;}

    sub Members::dispose{
	$logfile||return;
	my$self=ref($_[0])?$_[0]:getInstance();shift;
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
	my$self=ref($_[0])?$_[0]:getInstance();shift;
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
	my$self=ref($_[0])?$_[0]:getInstance();shift;
	my%DT=%{shift()};
	if($DT{'quit'}){
	    #�༼�⡼��
	    delete$singleton->{$DT{'id'}}if$DT{'id'};
	    $singleton->{"$DT{'ra'}"}={id=>$DT{'ra'},(map{$_=>$DT{$_}}qw(reload ra time hua))};
	}elsif($DT{'name'}){
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

	    %members=map{$_->[1]=>{($_->[0]=~/([^\t]+)=\t([^\t]*);\t/go)}}
	    map{[/^(id=\t([^\t]+);\t(?:[^\t]+=\t[^\t]*;\t)+)/o]}
	    grep{/^id=\t[^\t]+;\t(?:[^\t]+=\t[^\t]*;\t)+/o}@tmp;

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
	$singleton&&die '�����Singleton�ʤΤ�new�򾡼�˸ƤФʤ��ǡ�getInstance��Ȥ�����';
	my$class=ref($_[0])||$_[0];shift;
	my%rank=();
	local*RANK;
	if(-e$path){
	    open(RANK,'+<'.$path)||die"Can't open Ranking($path)[$?:$!]";
	    $fh=*RANK{IO};
	    eval{flock($fh,2)};
	    seek($fh,0,0);
	    %rank=map{$_->[0]=>{($_->[1]=~/([^\t]+)=\t([^\t]*);\t/go)}}
	    map{[/^id=\t([^\t]+);\t((?:[^\t]+=\t[^\t]*;\t)+)/o]}
	    grep{/^id=\t[^\t]+;\t(?:[^\t]+=\t[^\t]*;\t)+/o}<$fh>;
	}else{
	    open(RANK,'>>'.$path)||die"Can't create Ranking($path)[$?:$!]";
	    $fh=*RANK{IO};
	    eval{flock($fh,2)};
	}
	$singleton=bless \%rank,$class;
    }
    sub Rank::getInstance{$singleton||Rank->new;}

    sub Rank::dispose{
	my$self=ref($_[0])?$_[0]:getInstance();shift;
	truncate($path,0);#$fh�������
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
	my$self=ref($_[0])?$_[0]:getInstance();shift;
	my%DT=%{shift()};
	
	if(!$self->{"$DT{'id'}"}||!$self->{"$DT{'id'}"}->{'exp'}){
	    $self->{"$DT{'id'}"}={name=>$DT{'name'},exp=>1};
	}else{
	    $self->{"$DT{'id'}"}{'exp'}++;
	    $self->{"$DT{'id'}"}{'name'}=$DT{'name'};
	}
	$self->{"$DT{'id'}"}{'lastContact'}=$^T;
	$self->{"$DT{'id'}"}{'firstContact'}||=$^T;
	$self->{"$DT{'id'}"}{'hua'}=$DT{'hua'};
	$self->{"$DT{'id'}"}{'ra'}=$DT{'ra'};
	$self->{"$DT{'id'}"}{'color'}=$DT{'color'};
	$self->{"$DT{'id'}"}{'bcolo'}=$DT{'bcolo'};
	return$self->{"$DT{'id'}"}->{'exp'};
    }
    #������
    sub Rank::delete{
	my$self=ref($_[0])?$_[0]:getInstance();shift;
	my $id = shift();
	
	delete $self->{$id};
    }
    sub Rank::getOnlyHash{
	my%rank;
	if($singleton){
	    %rank=%{$singleton};
	}else{
	    open(RANK,'<'.$::CF{'rank'});
	    eval{flock(RANK,1)};
	    seek(RANK,0,0);
	    %rank=map{$_->[0]=>{($_->[1]=~/([^\t]+)=\t([^\t]*);\t/go)}}
	    map{[/^id=\t([^\t]+);\t((?:[^\t]+=\t[^\t]*;\t)+)/o]}
	    grep{/^id=\t[^\t]+;\t(?:[^\t]+=\t[^\t]*;\t)+/o}<RANK>;
	    close(RANK);
	}
	return\%rank;
    }

    sub Rank::DESTROY{shift->dispose;}
}


package main;
#-------------------------------------------------
# �������
#
BEGIN{
    #���顼���Ф��饨�顼���̤�ɽ������褦��
    # Marldia Error Screen 1.2.2
    unless($CF{'program'}){
	$CF{'program'}=__FILE__;
	$SIG{'__DIE__'}=$ENV{'REQUEST_METHOD'}?sub{
	    index($_[0],'flock')+1 and index($_[0],'unimplemented')+1 and return;
	    print "Status: 200 OK\nContent-Language: ja-JP\nContent-type: text/html; charset=$CF{'encoding'}\n\n"
		. "<HTML>\n<HEAD>\n"
		.qq(<META http-equiv="Content-type" content="text/html; charset=$CF{'encoding'}">\n)
		. "<TITLE> Marldia Error Screen 1.2.2</TITLE>\n"
		. "</HEAD>\n<BODY>\n\n<PRE>\t::  Marldia ::\n   * Error Screen 1.2.2 (o__)o// *\n\n";
	    print "ERROR: $_[0]\n"if@_;
	    printf"%-20.20s : %s\n",$_,$CF{$_} for grep{$CF{$_}}qw(Index Style Core Exte);
	    print "\n";
	    printf"%-20.20s : %s\n",$_,$CF{$_} for grep{$CF{$_}}qw(index log icon icls style);
	    print "\n";
	    printf"%-20.20s : %s\n",$$_[0],$$_[1]
		for([PerlVer=>$]],[PerlPath=>$^X],[BaseTime=>$^T],[OSName=>$^O],[FileName=>$0],[__FILE__=>__FILE__]);
	    print "\n = = = ENVIRONMENTAL VARIABLE = = =\n";
	    printf"%-20.20s : %s\n",$_,$ENV{$_} for grep{$ENV{$_}}
qw(CONTENT_LENGTH QUERY_STRING REQUEST_METHOD SERVER_NAME HTTP_HOST SCRIPT_NAME OS SERVER_SOFTWARE);
	    print "\n+#      Airemix  Marldia     #+\n+#  http://www.airemix.com/  #+\n</PRE>\n</BODY>\n</HTML>\n";
	    exit;
	}:sub{
	    index($_[0],'flock')+1 and index($_[0],'unimplemented')+1 and return;
	    print@_?"ERROR: $_[0]":'ERROR';
	    exit;
	};
    }
    __FILE__ =~ /^(.*[\\\/:])/o;
    $CF{'ProgramDirectory'} = $1;
    $CF{'program'} = substr($ENV{'SCRIPT_NAME'}, rindex('/'.$ENV{'SCRIPT_NAME'},'/'));

    #Revision Number
    $CF{'correv'}=qq$Revision: 1.21 $;
    $CF{'version'}=($CF{'correv'}=~/(\d[\w\.]+)/o)?"v$1":'unknown';#"Revision: 1.4"->"v1.4"
}
1;
__END__
