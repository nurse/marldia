#!/usr/local/bin/perl

#------------------------------------------------------------------------------#
# 'Marldia' Chat System
# - Main Script -
#
# $Revision: 1.2 $
# "This file is written in euc-jp, CRLF." ��
# Scripted by NARUSE,Yui.
#------------------------------------------------------------------------------#
# $cvsid = q$Id: mobile.cgi,v 1.2 2004-11-23 18:30:10 naruse Exp $;
require 5.005;
use strict;
use vars qw(%CF %IN %CK %IC);
#use Data::Dumper;
require'index.cgi';
require'core.cgi';

#-------------------------------------------------
# MAIN SWITCH
#
sub mobileMain{
    &getParams;
    
    my %default = (
		   line => 20
		  );
    for(keys %default){
	$IN{$_} = $default{$_} unless exists $IN{$_};
    }
    'south'eq$IN{'mode'} ? &mobileView : &mobileEntrance;
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
<FORM name="north" method="post" action="$CF{'program'}">
<INPUT name="south" type="hidden">
̾: <INPUT type="text" name="name">
̾��: <INPUT type="text" name="color">
��: <INPUT type="text" name="line" value="20">
��������: <INPUT type="text" name="icon">
ʸ��: <INPUT type="text" name="bcolo">
����: <INPUT type="text" name="body">
Identity: <INPUT type="text" name="id">
E-mail: <INPUT type="text" name="email">
Option: <INPUT type="text" name="opt">
Home: <INPUT type="text" name="home">
<INPUT type="submit" value="OK">
</FORM>
-<A href="http://www.airemix.com/" title="Airemix�ؤ��äƤߤ�">Marldia $CF{'version'}</A>-
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
    my ($chatlog,$members) = &commonRoutineForView();
    
    #-----------------------------
    #���üԾ���
    my@singers=map{qq($_->{'name'})}sort{$a->{'blank'}<=>$b->{'blank'}}$members->getSingersInfo;
    my$intMembers=scalar keys%{$members};
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
<FORM name="north" method="post" action="$CF{'program'}">
<INPUT type="hidden" name="name"  value="$IN{'name'}">
<INPUT type="hidden" name="color" value="$IN{'color'}">
<INPUT type="hidden" name="bcolo" value="$IN{'bcolo'}">
<INPUT type="hidden" name="icon"  value="$IN{'icon'}">
<INPUT type="hidden" name="id"    value="$IN{'id'}">
<INPUT type="hidden" name="email" value="$IN{'email'}">
<INPUT type="hidden" name="opt"   value="$IN{'opt'}">
<INPUT type="hidden" name="home"  value="$IN{'home'}">
<INPUT name="south" type="hidden">
����: <INPUT type="text" name="body" size="5">
��: <INPUT type="text" name="line" value="20" size="2">
<INPUT type="submit" value="OK" size="2">
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
    print<<"_HTML_";
Airemix Marldia
</PRE>
</BODY>
</HTML>
_HTML_
    exit;
}



#------------------------------------------------------------------------------#
# Sub Routins
#
# mainľ���Υ��֥롼���󷲤����



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
	
    #Revision Number
    $CF{'correv'}=qq$Revision: 1.2 $;
    $CF{'version'}=($CF{'correv'}=~/(\d[\w\.]+)/o)?"v$1":'unknown';#"Revision: 1.4"->"v1.4"
}

mobileMain();
1;
__END__
