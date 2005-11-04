#!/usr/local/bin/perl

#------------------------------------------------------------------------------#
# 'Marldia' Chat System
# - Main Script -
#
# $Revision: 1.34 $
# "This file is written in euc-jp, CRLF." ��
# Scripted by NARUSE,Yui.
#------------------------------------------------------------------------------#
# $cvsid = q$Id: core.cgi,v 1.34 2005-11-04 14:48:10 naruse Exp $;
require 5.005;
use strict;
use vars qw(%CF %IN %CK %IC);
#use Data::Dumper;


#-------------------------------------------------
# MAIN SWITCH
#
sub main{
    &getParams;
    $IN{'name'}&&index(" $CF{'denyname'} "," $IN{'name'} ") > -1&& exit;
    $ENV{'REMOT_ADDR'}&&index(" $CF{'deny_ra'} "," $IN{'REMOT_ADDR'} ") > -1&& exit;
    $ENV{'REMOT_HOST'}&&index(" $CF{'deny_rh'} "," $ENV{'REMOT_HOST'} ") > -1&& exit;
    $ENV{'HTTP_USER_AGENT'}&&index(" $CF{'deny_ua'} "," $ENV{'HTTP_USER_AGENT'} ") > -1&& exit;
    
    &getCookie;
    $CK{'name'}&&index(" $CF{'denyname'} "," $CK{'name'} ") > -1&& exit;

    $CF{'supass'} = [$CF{'admipass'}]unless$CF{'supass'};
    if('jump'eq$IN{'mode'}){
	&locate($IN{'jump'});
    }elsif('xml'eq$IN{'type'}){
	&xmlView();
    }elsif('mobile'eq$IN{'type'} || $IN{'hua'} =~ /(?:^Mozilla\/[1-3].0|DoCoMo|^KDDI|^J-PHONE|^ASTEL)/o){
	my %default = (
		       line => 20
		      );
	for(keys %default){
	    $IN{$_} = $default{$_} unless exists $IN{$_};
	}
	'south'eq$IN{'mode'} ? &mobileView : &mobileEntrance;
    }else{
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
    }
    exit;
}


#------------------------------------------------------------------------------#
# MARD ROUTINS
#
# mainľ���Υ��֥롼����


#-------------------------------------------------
# Mobile Entrance
#
sub mobileEntrance{
    print <<"_HTML_";
Status: 200 OK
Content-type: text/html; charset=euc-jp

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<HTML lang="ja-JP">
<HEAD>
<META http-equiv="Content-type" content="text/html; charset=euc-jp">
<META http-equiv="Content-Style-Type" content="text/css">
<TITLE>$CF{'title'}</TITLE>
</HEAD>
<BODY>
<FORM name="north" method="get" action="$CF{'index'}">
<INPUT name="mode" type="hidden" value="south">
<INPUT name="type" type="hidden" value="mobile">
̾: <INPUT type="text" name="name" value="$IN{'name'}">
̾��: <INPUT type="text" name="color" value="$IN{'color'}" istyle="3">
��: <INPUT type="text" name="line" value="$IN{'line'}" istyle="4">
��������: <INPUT type="text" name="icon" value="$IN{'icon'}" istyle="3">
ʸ��: <INPUT type="text" name="bcolo" value="$IN{'bcolo'}" istyle="3">
Identity: <INPUT type="text" name="id" value="$IN{'id'}">
E-mail: <INPUT type="text" name="email" value="$IN{'email'}" istyle="3">
Option: <INPUT type="text" name="opt" value="$IN{'opt'}" istyle="3">
Home: <INPUT type="text" name="home" value="$IN{'home'}" istyle="3">
<INPUT type="submit" value="OK" accesskey="1">
</FORM>
-<A href="http://www.airemix.com/" title="Airemix�ؤ��äƤߤ�">Marldia v$CF{'version'}</A>-
</BODY>
</HTML>
_HTML_
}


#-------------------------------------------------
# Mobile View
#
sub mobileView{
    #---------------------------------------
    #View�ζ��̽���
    my ($logfile,$chatlog,$members) = &commonRoutineForView();
    
    #-----------------------------
    #���üԾ���
    my@singers=map{qq($_->{'name'})}sort{$a->{'blank'}<=>$b->{'blank'}}$members->getSingersInfo;
    my$intMembers=scalar keys%{$members};
    $members->dispose;
    my$intSingers=@singers;
    my$intAudiences=$intMembers-$intSingers;
    my$strMembers = @singers ? "@singers" : 'Read Only';
    
    #-----------------------------
    #������
    my$query=$IN{'id'} ?
	join(';',map{my$val=$IN{$_};$val=~s{(\W)}{'%'.unpack('H2',$1)}ego;"$_=$val"}
	     grep{defined$IN{$_}}($IN{'quit'}?qw(line reload):qw(name id line reload color))):'south';
    
    #---------------------------------------
    #�ǡ���ɽ��
    
    #-----------------------------
    #�إå�����
    print<<"_HTML_";
Status: 200 OK
Content-type: text/html; charset=euc-jp

<HTML lang="ja-JP">
<HEAD>
<META http-equiv="Content-type" content="text/html; charset=euc-jp">
<TITLE>$CF{'title'}</TITLE>
</HEAD>
<BODY><font size=2>
<FORM name="north" method="post" action="$CF{'index'}">
<INPUT type="hidden" name="name"  value="$IN{'name'}">
<INPUT type="hidden" name="color" value="$IN{'color'}">
<INPUT type="hidden" name="bcolo" value="$IN{'bcolo'}">
<INPUT type="hidden" name="icon"  value="$IN{'icon'}">
<INPUT type="hidden" name="id"    value="$IN{'id'}">
<INPUT type="hidden" name="email" value="$IN{'email'}">
<INPUT type="hidden" name="opt"   value="$IN{'opt'}">
<INPUT type="hidden" name="home"  value="$IN{'home'}">
����:<INPUT type="text" name="body" value="" size="4" accesskey="2">
<INPUT type="submit" value="OK" size="2" accesskey="1">
��:<INPUT type="text" name="line" value="$IN{'line'}" size="1" istyle="4">
<INPUT name="mode" type="checkbox" value="entrance">
</FORM>
_HTML_
    
    #-----------------------------
    #���ü�ɽ��
    print<<"_HTML_";
<pre>��:$intMembers [ $strMembers ]
_HTML_
    my$i=0;
    #-----------------------------
    #��ɽ��
    for(@{$chatlog}){
	my%DT=%{$_};
	'del'eq$DT{'Mar1'}&&next;
	++$i>$IN{'line'}&&last;
	
	#����
	my$date=sprintf("%s",(split(/\s+/o,localtime$DT{'time'}))[3]);;
	#̾�����᡼�륢�ɥ쥹��̾����
	#����
	print<<"_HTML_";
<FONT color="$DT{'color'}">$DT{'name'}</FONT> &gt; <FONT color="$DT{'bcolo'}">$DT{'body'}</FONT> $date
_HTML_
    }
    $chatlog->dispose;
    $logfile->dispose;
    print<<"_HTML_";
Airemix Marldia
</PRE>
</BODY>
</HTML>
_HTML_
    exit;
}


#-------------------------------------------------
# XML View
#
sub xmlView{
    #-----------------------------
    #�����
    $IN{'line'} = 50 unless $IN{'line'};
    $IN{'lastModified'} = 50 unless $IN{'lastModified'};
    my $version = $IN{'version'} eq '0.2' ? '0.2' : '0.1';
    
    #-----------------------------
    #������
    my$query='south;type=xml;';
    if($IN{'id'}){
	$query='type=xml;'.join(';',map{my$val=$IN{$_};$val=~s{(\W)}{'%'.unpack('H2',$1)}ego;"$_=$val"}
		    grep{defined$IN{$_}}qw(name id line reload color));
	if($IN{'quit'}){
	    $query.=';quit=on';
	    $IN{'reload'} = 0;
	}
    }
    
    #---------------------------------------
    #View�ζ��̽���
    my ($logfile,$chatlog,$members) = &commonRoutineForView();
    
    #-----------------------------
    #���üԾ���
    my $intMembers = scalar keys%{$members};
    
    #---------------------------------------
    #�ǡ���ɽ��
    my $updated = &datef((stat("$CF{'rank'}"))[9],'dateTime');
    my $rootElement = vercmp($version, '>=', '0.2') ? 'feed' : 'document';
    my $doctype = $IN{'doctype'} && vercmp($version, '>=', '0.2') ?
	'<!DOCTYPE feed PUBLIC "-//Airemix//DTD ChatXML 0.2//EN"'
	. ' "http://airemix.org/TR/ChatXML/DTD/ChatXML-0.2.dtd">' . "\n" : '';
    my $xmlns = vercmp($version, '>=', '0.2') ? ' xmlns="http://airemix.org/2005/ChatXML"' : '';
    
    #-----------------------------
    #�إå�����
    print<<"_EOM_";
Status: 200 OK
Content-type: application/xml; charset=euc-jp

<?xml version="1.0" encoding="euc-jp"?>
$doctype<$rootElement version="$version"$xmlns>
  <updated>$updated</updated>
  <system>
    <uri>http://airemix.com/Marldia/$CF{'version'}</uri>
    <name>Marldia</name>
    <version>$CF{'version'}</version>
  </system>
  <site>
    <name>$CF{'sitename'}</name>
    <link rel="alternative" type="text/html" href="$CF{'sitehome'}" />
  </site>
  <entry>
    <title>$CF{'title'}</title>
    <link rel="alternative" type="text/html" href="$CF{'uri'}" />
    <members count="$intMembers">
_EOM_
    for(sort{$a->{'blank'}<=>$b->{'blank'}}$members->getSingersInfo){
	my $member = $_;
	my %person;
	$person{'updated'} = &datef($member->{'lastModified'},'dateTime');
	for(qw/id name color/){
	    $person{$_} = to_cdata($member->{$_}) if exists$member->{$_} && length($member->{$_});
	}
	print "      <member>\n";
        for(qw/updated id color name/){
	    print "        <$_>$person{$_}</$_>\n";
        }
	print "      </member>\n";
    }
    print<<"_EOM_";
    </members>
    <log>
_EOM_
    #-----------------------------
    #��ɽ��
    my$i=0;
    my $isAdmin = 0;
    if($IN{'_opt'}{'su'}&&$CF{'supass'}){
	for(@{$CF{'supass'}}){
	    $IN{'_opt'}{'su'}eq$_ or next;
	    $isAdmin = 1;
	    last;
    	}
    }
    for(@{$chatlog}){
	my%DT=%{$_};
	$DT{'time'} < $IN{'lastModified'} and last;
	!$isAdmin&&'del'eq$DT{'Mar1'}&&next;
	++$i>$IN{'line'}&&last;
	
	my %article;
	my %author;
	
	my $article_id = $DT{'id'};
	$article_id =~ s{(\W)}{'-'.unpack('H2',$1)}ego;
	$article_id = $DT{'exp'}. '_' .$article_id;
	$DT{'level'}=&getLevel($DT{'exp'});
	
	for(qw/id name color email home exp level/){
	    $author{$_} = sprintf('<%s>%s</%s>', $_, to_cdata($DT{$_}), $_)
		if exists$DT{$_} && length($DT{$_});
	}

	#��������
	my %icon = &getIconTag(\%DT);
	$author{'icon'} =
	    sprintf('<icon dir="%s" file="%s" src="%s" width="48" height="48" />',
		    @icon{'dir','file','uri'}) if $icon{'uri'};
	
	#����ܥ���
	if('del'eq$DT{'Mar1'}){
	    $article{'delete'} = qq(<delete />);
	}elsif($IN{'id'}&&$DT{'id'}eq$IN{'id'}){
	    $article{'delete'} = qq(<delete href="$CF{'index'}?del=$DT{'exp'}&#59;$query" />);
	}elsif($isAdmin){
	    $article{'delete'} = qq(<delete href="$CF{'index'}?del=$article_id&#59;$query" />);
	}
	
	$article{'updated'} = '<updated>'.&datef($DT{'time'},'dateTime').'</updated>';
	$article{'body'} = to_cdata($DT{'body'});
	$article{'body'} =~ s/<A class="autolink"[^>]*>([^<]+)<\/A>/$1/go;
	$article{'body'} =~ s/<BR>/\n/go;
	$article{'body'} = '<body>'.$article{'body'}.'</body>';
	
	#����
	print "      <article>\n";
	if(vercmp($version, '>=', '0.2')){
	    $article{'id'} = '<id>'.$article_id.'</id>';
	    $article{'color'} = '<color>'.to_cdata($DT{'bcolo'}).'</color>' if $DT{'bcolo'};
	    delete$author{'home'};
	    $author{'uri'} = sprintf('<%s>%s</%s>', 'uri', to_cdata($DT{'home'}), 'uri') if $DT{'home'};
	    
	    for(qw/updated id body color/){
		print "        $article{$_}\n" if $article{$_};;
	    }
	    print "        <author>\n";
	    for(qw/id color email exp icon level name uri/){
		print "          $author{$_}\n" if $author{$_};
	    }
	    print "        </author>\n";
	}else{
	    $article{'bcolo'} = '<bcolo>'.to_cdata($DT{'bcolo'}).'</bcolo>' if $DT{'bcolo'};
	    for(keys %article){
		print "        $article{$_}\n";
	    }
	    for(keys %author){
		print "        $author{$_}\n";
	    }
	}
	print "      </article>\n"
    }
    $members->dispose;
    $chatlog->dispose;
    $logfile->dispose;
    print<<"_EOM_";
    </log>
  </entry>
</$rootElement>
_EOM_
    exit;
}


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
<FRAME frameborder="0" name="south" src="$CF{'index'}?south">
<NOFRAMES>
<BODY>
<H1>Marldia</H1>
<P><A href="$CF{'index'}?mode=mobile">For Mobile</A></P>
<P><A href="http://airemix.com/">Airemix Marldia</A></P>
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
    (%CK)||(%CK=%IN);
    &header;
    &iptico($CK{'icon'},'tabindex="12"');
    print<<"_HTML_";
<SCRIPT type="text/javascript">
<!--
/*========================================================*/
// �����
MARLDIA_CORE_ID = '\$Id: core.cgi,v 1.34 2005-11-04 14:48:10 naruse Exp $';
var isInitialized;
var iconDirectory = '$CF{'iconDir'}';
var iconSetting = @{[ !!$CF{'absoluteIcon'} * 1 + !!$CF{'relativeIcon'} * 2 ]};
var myIcon = { 'value': '$CK{'icon'}', 'isAbsolute': 0 };
function init(){}

/*========================================================*/
// OnSubmit
function onSubmitHandler(e){
    if(document.forms && document.forms[0]){
	var form = document.forms[0];
	if(form['identity'] && form['name'] &&
	   !form['identity'].value && form['name'].value){
	    form['identity'].value = form['name'].value;
	}
	if(isInitialized){
	    if(commentHistory && form['body'].value && maxHistory > 0){
		commentHistory.last();
		commentHistory.set( form['body'].value );
		commentHistory.push('');
	    }
	    setCookie();
	}
	form.submit();
	if(form['cook'] && form['cook'].checked) form['cook'].checked = false;
	if(form['body'] && form['body'].value){
	    form['body'].value = '';
	    form['body'].focus();
	}
	if(!e){
	}else if(document.all){ 
	    e.returnValue = false;
	}else if(document.getElementById){
	    e.preventDefault();
	}else return false;
	if(e) e.cancelBubble=true;
	return false;
    }else{
	return true;
    }
}
//-->
</SCRIPT>
<![if gte IE 5.5000]>
<SCRIPT type="text/javascript" src="./punycode.js"></SCRIPT>
<SCRIPT type="text/javascript" src="./$CF{'marldiajs'}"></SCRIPT>
<![endif]>

<SCRIPT type="text/javascript" defer>
<!--
window.onload = init;
//-->
</SCRIPT>

<FORM name="north" id="north" method="post" action="$CF{'index'}" target="south"
onsubmit="return onSubmitHandler(event);">
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
<TD style="text-align:center;white-space:nowrap" nowrap>
<H1 contentEditable="true">$CF{'pgtit'}</H1>
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
<TD rowspan="3" style="text-align:center;white-space:nowrap" nowrap>
<BUTTON accesskey="x" type="button" id="surfaceButton" onclick="isInitialized&&surfaceSample(event);return false"
onkeypress="isInitialized&&surfaceSample(event);return false"><IMG name="preview" id="preview" alt="" title="$CK{'icon'}"
src="$CF{'iconDir'}$CK{'icon'}" $CF{'imgatt'} style="margin:0"></BUTTON>
</TD>
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
<TH><LABEL accesskey="b" for="body" title="Body&#10;ȯ��������ʸ�����ƤǤ�&#10;/rank��ȯ����󥭥󥰡�/member�ǻ��ü԰����򸫤�ޤ�">����(<SPAN class="ak">B</SPAN>)</LABEL>:</TH>
<TD colspan="5" id="bodyContainer"><INPUT type="text" class="text" name="body" id="body"
maxlength="300" size="100" style="ime-mode:active;width:400px" tabindex="1">
<INPUT type="button" id="bodySwitch" class="button" value="��" tabindex="2"
onclick="isInitialized&&switchBodyFormType(event);return false;"></TD>
<TD style="text-align:center"><!--INPUT type="checkbox" name="quit" id="quit" class="check" tabindex="51"
><LABEL accesskey="Q" for="quit" title="Quit&#10;�����å��������Ȼ��üԤ���̾����ä��ޤ���"
>�༼�⡼��(<SPAN class="ak">Q</SPAN>)</LABEL--></TD>
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
<TD style="text-align:center;white-space:nowrap" nowrap>
<LABEL accesskey="z" for="surface" title="sUrface&#10;ɽ�𥢥���������򤷤ޤ��ʻȤ���С�"
>S<SPAN class="ak">u</SPAN>rface</LABEL><SELECT name="surface" id="surface" tabindex="50"
onfocus="if(isInitialized&&myIcon&&myIcon.value!=getSelectingIcon())changeOption()" onchange="isInitialized&&changeSurface(this.selectedIndex)">
_HTML_
    if($CK{'icon'}=~/^((?:[^\/#]*\/)*)((?:[^\/#.]*\.)*?[^\/#.]+)(\.[^\/#.]*)?#(\d+)$/o){
	print qq(<OPTION value="$1$2$3">-</OPTION>\n);
	for(0..$4){print qq(<OPTION value="$1$2$_$3">$_</OPTION>\n);}
    }else{
	print qq(<OPTION value="$CK{'icon'}">-</OPTION>\n);
    }
    print<<"_HTML_";
</SELECT><INPUT name="south" type="hidden" value="">
</TD>
<TH><LABEL accesskey="p" for="opt" title="oPtion&#10;���ץ����"
>O<SPAN class="ak">p</SPAN>tion</LABEL>:</TH>
<TD><INPUT type="text" class="text" name="opt" id="opt" style="ime-mode:inactive;width:150px"
value="$CK{'opt'}" tabindex="102" onblur="isInitialized&&changeOption()"></TD>
<TH><LABEL accesskey="o" for="home" title="hOme&#10;�����Ȥ�URL�Ǥ�"
>H<SPAN class="ak">o</SPAN>me</LABEL>:</TH>
<TD colspan="3"><INPUT type="text" class="text" name="home" id="home" maxlength="200" size="40"
style="ime-mode:inactive;width:200px" value="$CK{'home'}" tabindex="112"></TD>
<TH style="letter-cpacing:-1px;text-align:center">-<A href="http://airemix.com/" title="Airemix�ؤ��äƤߤ�"
target="_top">Marldia v$CF{'version'}</A>-</TH>
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
    #View�ζ��̽���
    my ($logfile,$chatlog,$members) = &commonRoutineForView();
    
    #-----------------------------
    #������
    my$query='south';
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
    my $mobileQuery = 'south&amp;type=mobile&amp;' .
    	join('&amp;',map{my$val=$IN{$_};$val=~s/&#64;/\@/;$val=~s{(\W)}{'%'.unpack('H2',$1)}ego;"$_=$val"}
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
    push @singers, qq(<A href="$CF{'index'}?$mobileQuery">����</A>��) if $mobileQuery;
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
    my $additionalHeader = '';
    if($IN{'reload'}){
	$additionalHeader = <<"_HTML_";
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
    }
    $additionalHeader .= qq{<STYLE type="text/css">\n<!--\n} . $IN{'_opt'}{'css'}
    . "\n-->\n</STYLE>\n"if $IN{'_opt'}{'css'};
    &header($additionalHeader);
    
    #-----------------------------
    #���ü�ɽ��
    my $reload = $IN{'reload'} ? sprintf('%s�ôֳ�',$IN{'reload'}) : 'No Reload';
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
    my $isAdmin = 0;
    if($IN{'_opt'}{'su'}&&$CF{'supass'}){
	for(@{$CF{'supass'}}){
	    $IN{'_opt'}{'su'}eq$_ or next;
	    $isAdmin = 1;
	    last;
    	}
    }
    for(@{$chatlog}){
	my%DT=%{$_};
	!$isAdmin&&'del'eq$DT{'Mar1'}&&next;
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
	$DT{'_Icon'}=&getIconTag(\%DT)||'&#160;';
	#��٥����
	$DT{'level'}=&getLevel($DT{'exp'});
	#����ܥ���
	my$del = '&#160;';
	if('del'eq$DT{'Mar1'}){
	    $del = qq([�����]);
	}elsif($IN{'id'}&&$DT{'id'}eq$IN{'id'}){
	    $del = qq([<A href="$CF{'index'}?del=$DT{'exp'}&#59;$query">���</A>]);
	}elsif($isAdmin){
	    my$id = $DT{'id'};
	    $id=~s{(\W)}{'%'.unpack('H2',$1)}ego;
	    $del = qq([<A href="$CF{'index'}?del=$DT{'exp'}_$id&#59;$query">���</A>]);
	}
	#����
	print<<"_HTML_";
<TABLE cellspacing="0" class="article" summary="article">
<TR>
<TH class="articon" rowspan="2">$DT{'_Icon'}</TH>
<TH class="artname" nowrap>$name&#160;$home</TH>
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
    $chatlog->dispose;
    $members->dispose;
    $logfile->dispose;
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
    unless($IN{'body'}){
	die"�ֲ��⤷�ʤ���������";
    }
    #��������
    my@arg=grep{s/\\(\\)|\\(")|"/$1$2/go;$_;}($IN{'body'}=~
					      /(?!\s)[^"\\\s]*(?:\\[^\s][^"\\\s]*)*(?:"[^"\\]*(?:\\.[^"\\]*)*(?:"[^"\\\s]*(?:\\[^\s][^"\\\s]*)*)?)*\\?/go);

=item ���ѥ��ޥ��

��rank
��󥭥󥰤�ɽ��

��mem
���üԾ����ɽ��

��del <exp>
ȯ�����

��edit <exp> [<key>=<value>]..
ȯ���Խ�

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
    }elsif('del'eq$arg[0]){
	#ȯ�����
	my @result = Chatlog->delete({id=>$IN{'id'},exp=>$arg[1]});
	&header;
	if(@result){
	    print"<P>������ޤ�����</P>";
	}else{
	    print"<P>�ʤˤ������ʤ��ä���</P>";
	}
	&showFooter;
    }elsif('edit'eq$arg[0]){
	#ȯ���Խ�
	&header;
	my $data = Chatlog->get({id=>$IN{'id'},exp=>$arg[1]});
	if($data){
	    for(2..$#arg){
		my($key,$value) = split('=',$arg[$_],2);
		index(' name color bcolo body home email opt icon '," $key ") > -1 or next;
		# 'icon' may cause a security hole...
		$data->{$key} = $value;
	    }
	    print"<P>�������ޤ�����</P>";
	}else{
	    print"<P>�ʤˤ⽤�����ʤ��ä���</P>";
	}
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
    unless($IN{'body'}){
	die"�ֲ��⤷�ʤ���������";
    }
    $IN{'_opt'} = parseOption($IN{'opt'});
    my $isAdmin = 0;
    if($IN{'_opt'}{'su'}&&$CF{'supass'}){
	for(@{$CF{'supass'}}){
	    $IN{'_opt'}{'su'}eq$_ or next;
	    $isAdmin = 1;
	    last;
    	}
    }
    die'password is not valid'unless$isAdmin;
    
    #��������
    my@arg=grep{s/\\(\\)|\\(")|"/$1$2/go;length$_;}
    ($IN{'body'}=~
     /(?!\s)[^"\\\s]*(?:\\[^\s][^"\\\s]*)*(?:"[^"\\]*(?:\\.[^"\\]*)*(?:"[^"\\\s]*(?:\\[^\s][^"\\\s]*)*)?)*\\?/go);

=item �������ޥ��

$::CF{'admipass'}='admicmd';�ʤ顢
���ץ�����su=admincmd�Ȼ��ꤷ����ǡ�
#admin ...
��...�Ȥ������ޥ�ɤ�ȯư

��rank (del|merge|conv) <...>
��󥭥󥰤�ɽ��
��del <id>
�����Ȥ��ƻ��ꤵ�줿ID�ξ������
��delByExp <exp>
�����Ȥ��ƻ��ꤵ�줿�и��ͤ�꾯�ʤ��ͤ���
��merge <mainid> [<subid>]..
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
	my $rank = Rank->getInstance;
	my %rank = %{Rank->getOnlyHash()};
	if($arg[1]){
	    if('del'eq$arg[1]){
		#��󥭥󥰤�����
		$rank->delete($arg[2]);
	    }elsif('delByExp'eq$arg[1]){
		#�и��Ϥξ��ʤ��ͤ��󥭥󥰤�����
		for(keys%rank){
		    if($arg[2] > $rank{$_}->{'exp'}){
			$rank->delete($_);
		    }
		}
	    }elsif('merge'eq$arg[1]){
		#ID����ӷи��Ϥ�����
		exists$rank->{$arg[2]}&&exists$rank->{$arg[2]}->{'exp'}||die"����ʿͤ��ʤ�";
		for(3..$#arg){
		    (!$rank->{$arg[$_]}||!$rank->{$arg[$_]}->{'exp'})&&next;
		    $rank->{$arg[2]}->{'exp'}+=$rank->{$arg[$_]}->{'exp'};
		    $rank->delete($arg[$_]);
		}
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
	$rank->dispose;
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
	$i=~s/&#38;/&/go;
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
    my $location = '';
    my $href = $i;
    my $status='Status: 303 See Other';
    $href=~s/%([0-9A-Fa-f]{2})/pack('H2',$1)/ego;
    if($href=~/\w+:\/\/[\x00-\x2E\x30-\x7F]*[^\x00-\x7f]/o){
	$href=~s/&(#?\w+;)?/$1?"&$1":'&#38;'/ego;
	$href=~s/"/&#34;/go;
	$href=~s/'/&#39;/go;
	$href=~s/</&#60;/go;
	$href=~s/>/&#62;/go;
	$status='Status: 200 OK';
    }else{
	$href = $i;
	$location = "Location: $i";
    }
    print<<"_HTML_";
$status
Content-Language: ja-JP
Pragma: no-cache
Cache-Control: no-cache
Content-type: text/html; charset=euc-jp
$location

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN"> 
<HTML>
<HEAD>
<!--META http-equiv="Refresh" content="0;URL=$href"-->
<TITLE>303 See Ohter</TITLE>
</HEAD>
<BODY>
<H1>: Marldia :</H1>
<P>And, please go <A href="$href">here</A>.</P>
<P>Location: $href</P>
<P>Marldia <VAR>$CF{'correv'}</VAR>.<BR>
Copyright &#169;2001,2002 <A href="http://airemix.com/" target="_blank" title="Airemix">Airemix</A>. All rights reserved.</P>
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
<DIV class="AiremixCopy">- <A href="http://airemix.com/" target="_top" title="Airemix - Marldia -">Airemix Marldia</A><VAR title="times:@{[times]}">v$CF{'version'}</VAR> -</DIV>
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
    if($CF{'ckpath'}){
	$CF{'-setCookie'}=sprintf'Marldia=%s; expires=%s'
	    ,$cook,&datef(0,'cookie');
	$CF{'-setCookie'}.="\n";
	$CF{'-setCookie'}.=sprintf'Marldia=%s; expires=%s; %s'
	    ,$cook,&datef($expires,'cookie'),$CF{'ckpath'};
    }else{
	$CF{'-setCookie'}="Marldia=$cook; expires=".&datef($expires,'cookie');
    }
    $CF{'set_cookie_by_meta_tags'}=1if index($ENV{'SERVER_NAME'},'tok2.com')>-1&&!defined$CF{'set_cookie_by_meta_tags'};
    if($CF{'set_cookie_by_meta_tags'}){
	#tok2�к�
    }else{
	print "Set-Cookie: $_\n" for split("\n",$CF{'-setCookie'});
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

=head2 ���դ����

=head3 Arguments

  $ ����

=head3 Return Value

  $jd,$year,$mon,$day,$hour,$min,$sec,$unix

=head3 �б����շ���

RFC1123, ANSI C����, ISO9601 dateTime

=head3 See Also

=over

=item RFC1123���������դ����

  http://www.faireal.net/articles/3/16/

=back

=cut

sub parse_date{
    my$date=shift();
    my($day,$mon,$year,$hour,$min,$sec);
    my$months='(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)';
    my%month=qw(Jan 1 Feb 2 Mar 3 Apr 4 May 5 Jun 6 Jul 7 Aug 8 Sep 9 Oct 10 Nov 11 Dec 12);
    if($date=~/\w+,?\s*(\d+)(?:-|\s+)($months)(?:-|\s+)(\d+) (\d+):(\d+):(\d+)\s*GMT/o){
	# RFC1123 'Thu, 01 Jan 1970 00:00:00 GMT'
	($year,$mon,$day,$hour,$min,$sec)=map{int}($3,$month{$2},$1,$4,$5,$6);
    }elsif($date=~/\w+\s+($months)\s+(\d+)\s+(\d+):(\d+):(\d+)\s+(\d+)/o){
	#gmtime() 'Thu Jan  1 00:00:00 1970'
	($year,$mon,$day,$hour,$min,$sec)=map{int}($6,$month{$1},$2,$3,$4,$5);
    }elsif($date=~/(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:Z|([-+])(\d{2})(?::(\d{2})))?/o){
	# ISO 8601 dateTime (CCYY-MM-DDThh:mm:ss+09:00)
	($year,$mon,$day,$hour,$min,$sec)=map{int}($1,$2,$3,$4,$5,$6);
	'+'eq$7?($hour-=$8,$9 and$min-=$9):($hour+=$8,$9 and$min+=$9)if$7&&$8;
    }else{
	return 0;
    }
    $mon||return 0;
    my($_Y,$_M,$_day)=($year,$mon,$hour/24+$min/1440+$sec/86400);
    if($mon<3){
	$_Y-=1;
	$_M+=12;
    }
    my$jd=int(365.25*($_Y+4716))+int(30.6001*($_M+1))+2-int($_Y/100)+int($_Y/400)+$day+$_day-1524.5;
    my$unix=((int($jd-$_day-2440587.5)*24+$hour)*60+$min)*60+$sec;
    return wantarray ? ($jd,$year,$mon,$day,$hour,$min,$sec,$unix) : $unix;
}


#-------------------------------------------------
#������������
sub commonRoutineForView{
    $IN{'_opt'} = parseOption($IN{'opt'});
    my %EX = %{$IN{'_opt'}};
    #���ѥ�������ǽ��index.cgi�����ꤹ�롣
    #index.cgi�ǻ��ꤷ����������ѥ���ɤ˹��פ���С�
    $IN{'icon'}=$IC{$EX{'icon'}}if$CF{'exicon'}&&$IC{$EX{'icon'}};
    
    #���л��ꥢ������
    $IN{'icon'}=''if$CF{'absoluteIcon'}&&$EX{'absoluteIcon'};
    #���л��ꥢ������
    $IN{'icon'}=''if$CF{'relativeIcon'}&&$EX{'relativeIcon'};
    #ɽ�𥢥�����
    if(!$IN{'surface'}){
    }elsif(!$IN{'icon'}){
	$IN{'icon'}=$IN{'surface'};
    }elsif($IN{'icon'}=~/^((?:[^\/#]*\/)*[^\/#.]*(?:\.[^\/#.]*)*)(\.[^\/#]*)(?:#\d+(?:-\d+)?)?$/o
	   && $IN{'surface'}=~/^$1/){
	$IN{'icon'}=$IN{'surface'};
    }
    
    $IN{'body'}=$IN{'body'}?Filter->filteringBody($IN{'body'},%EX):'';
    $IN{'isActive'}=$ENV{'CONTENT_LENGTH'}?1:0;
    $IN{'time'}=$^T;
    
    #-----------------------------
    #���å����񤭹���
    $IN{'cook'}&&&setCookie;
    
    #---------------------------------------
    #���üԡ���󥭥󥰡��񤭹��߽���
    my$logfile=Logfile->getInstance;
    my$chatlog=Chatlog->getInstance;
    my$members=Members->getInstance;
    
    #-----------------------------
    #��ʬ�Υǡ������ɲ�
    $IN{'reload'}=$members->add(\%IN);
    $members->getSingersInfo;
    
    #-----------------------------
    #�񤭹���
    if(length$IN{'body'}&&$IN{'id'}){
	#��󥭥󥰲���
	if( 'HASH' ne ref($chatlog->[0]) || #Ϣ³����ɻ�
	   $chatlog->[0]->{'id'} ne $IN{'id'} ||
	   $chatlog->[0]->{'body'} ne $IN{'body'} ){
	    my $rank = Rank->getInstance;
	    $IN{'exp'}=$rank->plusExp(\%IN);
	    $rank->dispose;
	    #ȯ������
	    $chatlog->add(\%IN);
	}
    }elsif($IN{'del'}){
	#ȯ�����
	my$id;
	if($IN{'del'}=~s/([1-9]\d*)_(.*)/$1/o){
	    $id = $2;
	}else{
	    $id = $IN{'id'};
	}
	$chatlog->delete({id=>$id,exp=>$IN{'del'}});
    }
    $logfile->close;
    return($logfile,$chatlog,$members);
}


#-------------------------------------------------
# ���ޥ�ɤ��ɤ߹���
#
sub parseOption{
    my $str = shift;
    my %hash;
    my@option=($str=~/\w+(?:=(?:"[^"\\]*(?:\\.[^"\\]*)*"|'[^'\\]*(?:\\.[^'\\]*)*'|[^"';]*))?/go);
    for(@option){
	my($i,$j)=split('=',$_,2);
	$i||next;
	$j=defined$j&&$j=~/^(?:"(.*)"|'(.*)'|(.*))$/o?$1||$2||$3:'';
	$hash{$i}=$j;
    }
    return \%hash;
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
:-!uri!-
absolute uri
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
	if($DT{'src'} =~ /^http:/o){
	    $DT{'uri'} = $DT{'src'};
	}elsif($DT{'src'} =~ /^\//o){
	    $DT{'uri'} = 'http://' . $ENV{'HTTP_HOST'} . $DT{'src'};
	}else{
	    $CF{'uri'} =~ /([^#?]+\/)/o;
	    $DT{'uri'} = $1.$DT{'src'};
	}
	$text=~s/(-!(\w+)!-)/defined$DT{$2}?$DT{$2}:$1/ego;
    }else{
	$text=undef;
    }
    return wantarray ? %DT : $text;
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
    }elsif($_[0]and$_[0]=~/([^#]+)/oand$iconlist=~s/^(.*value=(["'])$1(?:#\d+(?:-\d+)?)?\2)(.*)$/$1 selected$3/imo){
	$iconlist="$1 selected$3"if$isEconomy;
    }elsif($iconlist=~s/value=(["'])(.+?)\1/value=$1$2$1 selected/io){
	$_[0]=$2;
    }
    $_[0]=$CF{'icondir'}.$_[0]unless$isAbsolute;
    $isDisabled&&=' disabled';
    $CF{'-CacheIconList'}=<<"_HTML_";
<SELECT name="icon" id="icon" onchange="document.images['preview'].src=iconDirectory+this.value;document.images['preview'].title=this.value;if(changeOption)changeOption()"$opt$isDisabled>
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
<SELECT name="$id" id="$id"$opt onchange="this.style.color=this.value" onkeydown="this.style.color=this.value">
$list</SELECT>
_HTML_
    }
}


#-------------------------------------------------
# Version Compare
#
sub vercmp{

=item ����

$_[0]: string A
$_[1]: cmp
$_[2]: string B

=cut

    my $a = shift;
    my @a = ref$a eq 'ARRAY' ? @{$a} : split('\.', $a);
    my $cmp = shift;
    my $b = shift;
    my @b = ref$b eq 'ARRAY' ? @{$b} : split('\.', $b);
    my $result = 0;
    for(my$i=0; ; $i++){
	if($i > $#a){
	    if($i > $#b){
		$result = 0;
	    }else{
		$result = -1;
	    }
	    last;
	}elsif($i > $#b){
	    $result = 1;
	    last;
	}elsif($a[$i] <=> $b[$i]){
	    $result = $a[$i] <=> $b[$i];
	    last;
	}
    }
    if('<' eq $cmp){
	$result == -1 ;
    }elsif('<=' eq $cmp){
	$result < 1;
    }elsif('==' eq $cmp){
	$result == 0;
    }elsif('>' eq $cmp){
	$result == 1;
    }elsif('>=' eq $cmp){
	$result > -1;
    }else{
	$result;
    }
}


#-------------------------------------------------

=head2 Escape CDATA

=item ����

$str: string

=cut

sub to_cdata{
    my $str = shift;
    $str =~ s/]]>/]]]]><![CDATA[>/go;
    return '<![CDATA[' . $str . ']]>';
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
	
	#Gabri Duke�к�
	$ENV{'SERVER_PROTOCOL'} eq 'HTTP/1.0'
	    and $params =~ /body=(?!.*&\w+=)[-+*.@\w%&=]*(?:[^-+*.@\w%&=][-+*.@\w%&=]*)*$/o
	    and die 'GabriDuke? :' . $params;

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
	for(@params){
	    my($i,$j)=split('=',$_,2);
	    $i=~/([a-z][-.:\w]*)/o||next;$i=$1;
	    defined$j||($DT{$i}='')||next;
	    study$j;
	    $j=~tr/+/\ /;
	    $j=~s/%([\dA-Fa-f]{2})/pack('H2',$1)/ego;
	    #�ᥤ��ե졼��β��Ԥ�\x85�餷�����ɡ��б�����ɬ�פʤ���͡�
	    $j=~s/\x0D\x0A/\n/go;$j=~tr/\r/\n/;
	    if('body'ne$i&&'opt'ne$i){
		#��ʸ�ʳ������̥����ػ�
		$j=~s/&(#?\w+;)?/$1?"&$1":'&#38;'/ego;
		$j=~s/"/&#34;/go;
		$j=~s/'/&#39;/go;
		$j=~s/</&#60;/go;
		$j=~s/>/&#62;/go;
		$j=~s/\t/&#160;&#160;/go;
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
q{][\dA-Fa-f])*@)?(?:(?:[^\.\:\/]+\.)}.
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
q{:(?:[^\.\:\/]+\.)*[a-zA-Z](?:[-a-zA-}.
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

	# Encoding
	if($DT{'encoding'}){
	    $IN{'encoding'} = $DT{'encoding'};
	    {
		local $SIG{'__DIE__'} = sub{};
		# Encode
		eval q{
			use Encode;
			for(keys%DT){
				$DT{$_} = Encode::encode($::CF{'encoding'},
				    Encode::decode($IN{'encoding'}, $DT{$_}),
				    Encode::FB_HTMLCREF);
			}
		};
		# Jcode
		my $enc = $IN{'encoding'};
		$enc = $enc=~/ISO-2022-JP/i	? 'jis' :
		    $enc=~/Shift_JIS/i		? 'sjis' :
		    $enc=~/EUC(?:-JP)?/i	? 'euc' :
		    $enc=~/UTF-?16/i		? 'ucs2' :
		    $enc=~/UTF-?8/i		? 'utf8' : 'euc';
		eval q{use Jcode;for(keys%DT){$DT{$_} = Jcode->new( $DT{$_}, $enc )->euc}} if $@;
	    }
	    for(keys%DT){
		#�¡��ݡ�����������������������������
		$DT{$_} =~ s/&#8741;/��/go;
		$DT{$_} =~ s/&#65374;/��/go;
		$DT{$_} =~ s/&#65293;/��/go;
		$DT{$_} =~ s/&#65504;/��/go;
		$DT{$_} =~ s/&#65505;/��/go;
		$DT{$_} =~ s/&#65506;/��/go;
		$DT{$_} =~ s/&#65508;/��/go;
		$DT{$_} =~ s/&#8544;/��/go;
		$DT{$_} =~ s/&#8545;/��/go;
		$DT{$_} =~ s/&#8546;/��/go;
		$DT{$_} =~ s/&#8547;/��/go;
		$DT{$_} =~ s/&#8548;/��/go;
		$DT{$_} =~ s/&#8549;/��/go;
		$DT{$_} =~ s/&#8550;/��/go;
		$DT{$_} =~ s/&#8551;/��/go;
		$DT{$_} =~ s/&#8552;/��/go;
		$DT{$_} =~ s/&#8553;/��/go;
		$DT{$_} =~ s/&#8481;/��/go;
		$DT{$_} =~ s/&#12849;/��/go;
	    }
	    if($::CF{'encoding'}=~/euc-?jp/io){
		$DT{$_} =~ s/\x8f\xa2\xf1/��/go;
	    }
	}
	
	#������ʸ���Ͻ���
	for(keys%DT){
	    if($DT{$_}=~/^($eucchar*)$/o){
		$DT{$_} = $1;
	    }else{
		$DT{$_} =~ s{(\W)}{'%'.unpack('H2',$1)}ego;
	    }
	}
	
	#�ü�
	if('mobile'eq$DT{'type'}){
	    $IN{'type'}='mobile';
	}elsif('xml'eq$DT{'type'}){
	    $IN{'type'}='xml';
	    $IN{'_lastModified'} = $DT{'lastModified'};
	    $IN{'lastModified'} = scalar ::parse_date($DT{'lastModified'}) || $DT{'lastModified'};
	}
	
	#���ޥ�ɷ�
	if(!$DT{'body'}or'xml'eq$DT{'type'}){
	    $IN{'version'} = $DT{'version'} && $DT{'version'} =~ /((?:0|[1-9]\d*)(?:\.(?:0|[1-9]\d*))*)/o ? $1 : '0.1';
	    $IN{'doctype'} = $DT{'doctype'} && $DT{'doctype'} ne 'no' ? 'yes' : '';
	}elsif($::CF{'admipass'}&&$DT{'body'}=~/^\/admin\s*(.*)/o){
	    $IN{'mode'}='admicmd';
	    $IN{'body'}=$1;
	    $IN{'opt'}=$1 if$DT{'opt'}=~/(.+)/o;
	    $IN{'mode'}&&return\%IN;
	}elsif($DT{'body'}=~/^\/(\w+(?:\s.*)?)$/o){
	    $IN{'mode'}='usercmd';
	    $IN{'body'}=$1;
	    $IN{'id'}=($DT{'id'}=~/(.{1,100})/o)?$1:($::CK{'id'}||$IN{'name'});
	    $IN{'opt'}=$1 if$DT{'opt'}=~/(.+)/o;
	    $IN{'mode'}&&return\%IN;
	}
	$DT{'body'}=~s/^\/\//\//o if$DT{'body'};
	
	if(!%DT||($DT{'mode'}&&'frame'eq$DT{'mode'})){
	    #�ե졼��
	    $IN{'mode'}='frame';
	}elsif(defined$DT{'jump'} or 'jump'eq$IN{'mode'}){
	    #�������󥫥���
	    $IN{'mode'} = 'jump';
	    $IN{'jump'} = $DT{'jump'};
	}elsif(exists$DT{'icct'} or 'icct'eq$IN{'mode'}){
	    #�������󥫥���
	    $IN{'page'}=($DT{'page'}&&$DT{'page'}=~/([1-9]\d*)/o)?$1:1;
	    $IN{'mode'}='icct';
	}elsif(defined$DT{'id'}&&$DT{'name'}){
	    #ȯ��
	    if(defined$DT{'body'}){
		$IN{'body'}=$DT{'body'}||'';
		$IN{'cook'}=$DT{'cook'}?1:0;
	    }
	    if(defined$DT{'del'}){
		$IN{'del'}=$1 if$DT{'del'}=~/([1-9]\d*(?:_.*)?)/o;
	    }
	    $IN{'name'}=($DT{'name'}=~/(.{1,100})/o)?$1:'';
	    $IN{'id'}=($DT{'id'}=~/(.{1,100})/o)?$1:($::CK{'id'}||$IN{'name'});
	    if($DT{'bcolo'}){
		$IN{'color'}=($DT{'color'}=~/([\#\w\(\)\,]{1,20})/o)?$1:'';
		$IN{'bcolo'}=($DT{'bcolo'}=~/([\#\w\(\)\,]{1,20})/o)?$1:'';
	    }else{
		$IN{'nameColor'}=($DT{'nameColor'}=~/([\#\w\(\)\,]{1,20})/o)?$1:'';
		$IN{'color'}=($DT{'color'}=~/([\#\w\(\)\,]{1,20})/o)?$1:'';
	    }
	    $DT{'email'}=($DT{'email'}=~/(.{1,200})/o)?$1:'';
	    $IN{'email'}=($DT{'email'}=~/($mail_regex)/o)?$1:'';
	    $IN{'email'}=~s/\@/&#64;/o;
	    $DT{'home'} = $DT{'uri'} if $DT{'uri'};
	    $DT{'home'}=($DT{'home'}=~/(.{1,200})/o)?$1:'';
	    $IN{'home'}=($DT{'home'}=~/($http_URL_regex)/o)?$1:'';
	    $IN{'icon'}=($DT{'icon'}=~/([\w\:\.\~\-\%\/\#]+)/o)?$1:'';
	    $IN{'surface'}=$1 if$DT{'surface'}=~/([\w\:\.\~\-\%\/\#]+)/o;
	    $IN{'quit'}=$DT{'quit'}?1:0;
	    $IN{'opt'}=$1 if$DT{'opt'}=~/(.+)/o;
	    $IN{'line'}=($DT{'line'}=~/([1-9]\d*)/o)?$1:$::CF{'defline'};
	    $IN{'reload'}=($DT{'reload'}=~/([1-9]\d+|0)/o)?$1:$::CF{'defreload'};
	    if('entrance' eq $DT{'mode'}){
		$IN{'mode'}='entrance';
	    }else{
		$IN{'mode'}='south';
	    }
	}elsif( defined$DT{'north'} or 'north'eq$DT{'mode'}){
	    #��
	    $IN{'mode'}='north';
	    $IN{'line'}=$::CF{'defline'};
	    $IN{'reload'}=$::CF{'defreload'};
	}elsif( defined$DT{'south'} or 'south'eq$IN{'mode'}){
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
		my $safe = 0;
		my$pos=length$str;
		while($str=~/\G($text_regex)($comment_tag_regex|\03$tag_regex_)?/gso){
		    $safe++>10000 and die 'AutoLink Processing Error($str)';
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
		my $anchorContent = q{" target="_blank" onclick="window.open(this.href);return false;">};
		$str=~s{((?:\G|>)[^<]*?)$href_regex}{$1$isMail[!$3]$2$anchorContent$2</A>}go;
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
	$str=~s/\t/&#160;&#160;/go;
	$str=~s/(\x20{2,})/'&#160;' x length$1/ego;
	$str=~s/^[\n\r]+//go;
	$str=~s/[\n\r]+$//go;
	$str=~s/\n/<BR>/go;
	$str=~s/(&#60;!--.*?--&#62;)/<span style="color:green">$1<\/span>/go;
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
    my$isOpen=0;

    #---------------------------------------
    # Class Methods
    sub Logfile::new{#private
	$singleton&&die '�����Singleton�ʤΤ�new�򾡼�˸ƤФʤ��ǡ�getInstance��Ȥ�����';
	my$class=ref($_[0])||$_[0];shift;
	local*LOGFILE;
	if(-e$path){
	    open(LOGFILE,'+<'.$path)||die"Can't read Logfile($path)[$?:$!]";
	    #+>>�Ȥ����seek($fh,0,0)��ư���Ƥ���ʤ��Τ���ա�
	    eval{flock(LOGFILE,2)};
	    $fh=*LOGFILE{IO};
	    #member���ɲ�
	    while(<$fh>){/\S/o?push(@members,$_):last}
	    #chatlog���ɲ�
	    while(<$fh>){/\S/o&&push(@chatlog,$_)}
	}else{
	    open(LOGFILE,'>>'.$path)||die"Can't create Logfile($path)[$?:$!]";
	    eval{flock(LOGFILE,2)};
	    $fh=*LOGFILE{IO};
	    @members=();
	    @chatlog=();
	}
	$isOpen=1;
	$singleton=bless[\@chatlog,\@members],$class;
    }

    sub Logfile::getInstance{$singleton||Logfile->new}
    sub Logfile::getChatlog	{$singleton||Logfile->new;return@chatlog}
    sub Logfile::getMembers	{$singleton||Logfile->new;return@members}

    sub Logfile::setChatlog	{@chatlog=(@_[1..$#_])if$#_}
    sub Logfile::setMembers	{@members=(@_[1..$#_])if$#_}

    sub Logfile::DESTROY{shift->dispose}

    #close -- �ѹ��Ѥߥǡ�����ե��������¸
    sub Logfile::close{
	$isOpen||return;
	(@members&&@chatlog)||return;
	Chatlog->getInstance->close if Chatlog->hasInstance;
	Members->getInstance->close if Members->hasInstance;
	my$self=shift;
	truncate($path,0);#$fh�������
	seek($fh,0,0);
	print $fh map{$_."\n"}map{/(.*)/o}@members,'',@chatlog,'';
	close($fh);
	$isOpen=0;
    }
    
    sub Logfile::dispose{
	(@members&&@chatlog)||return;
	my$self=ref($_[0])?$_[0]:return;shift;
	$self->close;
	undef$fh;undef@members;undef@chatlog;undef$singleton;
    }
}


#------------------------------------------------------------------------------#
# Chatlog Class
#
{package Chatlog;
    my$logfile;
    my$singleton=undef;
    my$isOpen=0;

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

	$isOpen=1;
	$singleton=bless$self,$class;
    }
    sub Chatlog::getInstance{$singleton||Chatlog->new;}
    sub Chatlog::hasInstance{$singleton}

    #�����ɲ�
    sub Chatlog::add{
	my$self=ref($_[0])?$_[0]:getInstance();shift;
	my%DT=%{shift()};
	%DT=map{$_=>$DT{$_}}grep{$DT{$_}}qw(Mar1 id name color bcolo body icon home email exp hua ra time opt);
	splice(@{$self},$::CF{'max'}-1);
	unshift(@{$self},\%DT);
    }

    #�����ִ�
    sub Chatlog::get{
	my$self=ref($_[0])?$_[0]:getInstance();shift;
	my%DT=%{shift()};
	my @result = ();
	if($DT{'exp'}){
	    for(@{$self}){
		$_->{'id'} eq$DT{'id'} ||next;
		$_->{'exp'}eq$DT{'exp'}||next;
		return $_;
	    }
	}
	return undef;
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
    
    sub Chatlog::close{
	$isOpen||return;
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
	$isOpen=0;
    }
    
    sub Chatlog::dispose{
	$logfile||return;
	my$self=ref($_[0])?$_[0]:getInstance();shift;
	$self->close;
	undef$logfile;undef$singleton;
    }
    
    sub Chatlog::DESTROY{my$self=shift;$self->dispose;}
}


#------------------------------------------------------------------------------#
# MEMBERS CLASS
#

{package Members;
    my$logfile;
    my$singleton=undef;
    my$isOpen=0;

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
	$isOpen=1;
	$singleton=bless$self,$class;
    }
    sub Members::getInstance{$singleton||Members->new;}
    sub Members::hasInstance{$singleton}
    
    sub Members::close{
	$isOpen||return;
	$logfile||return;
	my$self=ref($_[0])?$_[0]:getInstance();shift;
	$logfile->setMembers(
			     map{
				 my%DT=%{$self->{$_}};
				 delete$DT{'id'};
				 "id=\t$_;\t".join('',map{"$_=\t$DT{$_};\t"}keys%DT);
				}keys%{$self}
			    );
	$isOpen=0;
    }
    
    sub Members::dispose{
	$logfile||return;
	my$self=ref($_[0])?$_[0]:getInstance();shift;
	$self->close;
	undef$logfile;undef$singleton;
    }

    #���üԤ����
    sub Members::getSingersInfo{
	my$self=ref($_[0])?$_[0]:getInstance();shift;
	my@singers;
	for(keys%{$self}){
	    my$i=$self->{$_};
	    $i->{'id'} = $_;
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
#	if($DT{'quit'}){
#	    #�༼�⡼��
#	    delete$singleton->{$DT{'id'}}if$DT{'id'};
#	    $singleton->{"$DT{'ra'}"}={id=>$DT{'ra'},(map{$_=>$DT{$_}}qw(reload ra time hua))};
#	}els
	if($DT{'name'}){
	    delete$singleton->{"$DT{'ra'}"};
	    if($DT{'isActive'}||!exists$singleton->{$DT{'id'}}){
		#ǽưŪ�����
		$DT{'lastModified'}=$^T;
	    }else{
		#���̤˥����
		$DT{'lastModified'}=$singleton->{$DT{'id'}}->{'lastModified'};
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
	Logfile->getInstance; #�ǥåɥ�å��ɻ�
	$singleton&&die '�����Singleton�ʤΤ�new�򾡼�˸ƤФʤ��ǡ�getInstance��Ȥ�����';
	my$class=ref($_[0])||$_[0];shift;
	my%rank=();
	local*RANK;
	if(-e$path){
	    open(RANK,'+<'.$path)||die"Can't open Ranking($path)[$?:$!]";
	    eval{flock(RANK,2)};
	    $fh=*RANK{IO};
	    seek($fh,0,0);
	    %rank=map{$_->[0]=>{($_->[1]=~/([^\t]+)=\t([^\t]*);\t/go)}}
	    map{[/^id=\t([^\t]+);\t((?:[^\t]+=\t[^\t]*;\t)+)/o]}
	    grep{/^id=\t[^\t]+;\t(?:[^\t]+=\t[^\t]*;\t)+/o}<$fh>;
	}else{
	    open(RANK,'>>'.$path)||die"Can't create Ranking($path)[$?:$!]";
	    eval{flock(RANK,2)};
	    $fh=*RANK{IO};
	}
	$singleton=bless \%rank,$class;
    }
    sub Rank::getInstance{$singleton||Rank->new;}

    sub Rank::dispose{
	$singleton&&$fh or return;
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
    $CF{'encoding'}='euc-jp'unless$CF{'encoding'};
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
	    print"\nRUID:$< EUID:$> RGID:$( EGID:$)\n";
	    print "\n = = = ENVIRONMENTAL VARIABLE = = =\n";
	    printf"%-20.20s : %s\n",$_,$ENV{$_} for grep{$ENV{$_}}
qw(CONTENT_LENGTH QUERY_STRING REQUEST_METHOD SERVER_NAME HTTP_HOST SCRIPT_NAME OS SERVER_SOFTWARE);
	    print "\n+#      Airemix  Marldia     #+\n+#  http://airemix.com/  #+\n</PRE>\n</BODY>\n</HTML>\n";
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
    $CF{'uri'} = 'http://' . $ENV{'HTTP_HOST'} . $ENV{'SCRIPT_NAME'};
    if($CF{'sitehome'} =~ /^\//o){
	$CF{'sitehome'} = 'http://' . $ENV{'HTTP_HOST'} . $CF{'sitehome'};
    }

    #Revision Number
    $CF{'correv'}=qq$Revision: 1.34 $;
    $CF{'version'}=($CF{'correv'}=~/(\d[\w\.]+)/o)?"$1":'0.0';#"Revision: 1.4"->"1.4"
}
1;
__END__
