#!/usr/local/bin/perl

#------------------------------------------------------------------------------#
# 'Marldia' Chat System
# - Marldia Core File -
#
# $Revision: 1.19 $
# "This file is written in euc-jp, CRLF." ��
# Scripted by NARUSE,Yui.
#------------------------------------------------------------------------------#
# $cvsid = q$Id: index.cgi,v 1.19 2005-05-28 17:25:12 naruse Exp $;
require 5.005;
#use strict;
#use vars qw(%CF %IN %CK %IC);

#YOUR SITE NAME
$CF{'sitename'}='Airemix';
#YOUR SITE TOP
$CF{'sitehome'} = '/';
#title�����ǤΥ���åȥ����ȥ�
$CF{'title'}=': Marldia :';
#�ڡ�����Υ���åȥ����ȥ�
$CF{'pgtit'}=': Marldia :';


#�����⡼�ɤذܹԤ���ݤΥѥ����
$CF{'admipass'}='opensesame';
#�����⡼�ɤ��ɲåѥ����
$CF{'supass'} = [$CF{'admipass'}]unless$CF{'supass'};
#push(@{$CF{'supass'}},'hogehoge');
#������Կ�
$CF{'max'}=200;
#���������ػߤ�̾��
$CF{'denyname'}='������';
#���Ѥ���Ĥ��륿����Ⱦ�ѥ��ڡ������ڤ��
$CF{'tags'}='ACRONYM CODE DEL DFN EM Q SMALL STRONG RUBY RB RB RT RP';
#����������ˡ(select input)
$CF{'colway'}='select';
#���������IMG�������ɲä���°��
$CF{'imgatt'}=' width="48" height="48"';

$CF{'romline'}=20;
$CF{'romreload'}=120;
$CF{'defline'}=20;
$CF{'defreload'}=20;

$CF{'index'} = 'index.cgi'; #MARLDIA MAIN CGI
$CF{'marldiajs'} = 'Marldia.js'; #MARLDIA JAVA SCRIPT
$CF{'style'} = 'style.css'; #CascadeStyleSheet
$CF{'log'}  = 'log.cgi'; #LOG PATH
$CF{'rank'} = 'rank.cgi'; #LOG PATH
$CF{'iconDir'} = '/icon/half/'; #ICON DIRECTORY PATH
$CF{'iconList'} = 'icon.txt'; #ICON LIST PATH

$CF{'iconCtlg'} = 'iconctlg.cgi'; #ICON CATALOG PATH
#$CF{'samp'} = 'icon.html'; #ICON SAMPLE PATH
$ENV{'TZ'}  = 'JST-9'; #TimeZone
$CF{'gzip'} = 'gzip'; #GZIP PATH

#���л��ꥢ������ (0 �Ȥ�ʤ� 1 �Ȥ�)
$CF{'absoluteIcon'}='1';
#���л��ꥢ������ (0 �Ȥ�ʤ� 1 �Ȥ�)
$CF{'relativeIcon'}='1';
#���ѥ�������ǽ (ON 1 OFF 0)
$CF{'exicon'}='0';
#���ѥ����������
#$IC{'PASSWORD'}='FILENAME'; #NAME
#$IC{'hae'}='mae.png'; #��
#$IC{'hie'}='mie.png'; #��
#$IC{'hue'}='mue.png'; #�
#$IC{'hee'}='mee.png'; #��
#$IC{'hoe'}='moe.png'; #ǵ��
#�㡧���ޥ�ɤ�"icon=hoe"��������ǵ���������Ѥ�'moe.png'���Ȥ��ޤ�
#�����Ϥ���Ȥ��ϡ�$IC{'hoe'}='moe.png'; #ǵ���פΤ褦�ˡ��ǽ�Ρ�#�פ���Τ�˺�줺��

#-----------------------------
# ���ꥹ��
$CF{'colorList'}=<<'_CONFIG_';
<OPTION value="#343434" style="color:#343434">����</OPTION>
<OPTION value="#8C8C8C" style="color:#8C8C8C">������</OPTION>
<OPTION value="#FBDADE" style="color:#FBDADE">������</OPTION>
<OPTION value="#D53E62" style="color:#D53E62">���鯿�</OPTION>
<OPTION value="#FF7F8F" style="color:#FF7F8F">�����꿧</OPTION>
<OPTION value="#AD3140" style="color:#AD3140">���û鿧</OPTION>
<OPTION value="#9E2236" style="color:#9E2236">������</OPTION>
<OPTION value="#905D54" style="color:#905D54">����Ʀ��</OPTION>
<OPTION value="#EF454A" style="color:#EF454A">���뿧</OPTION>
<OPTION value="#F1BB93" style="color:#F1BB93">��ȩ��</OPTION>
<OPTION value="#564539" style="color:#564539">�����㿧</OPTION>
<OPTION value="#6B3E08" style="color:#6B3E08">���쿧</OPTION>
<OPTION value="#AA7A40" style="color:#AA7A40">�����ῧ</OPTION>
<OPTION value="#F8A900" style="color:#F8A900">�����ῧ</OPTION>
<OPTION value="#EDAE00" style="color:#EDAE00">��ݵ�⿧</OPTION>
<OPTION value="#C8A65D" style="color:#C8A65D">�����ҿ�</OPTION>
<OPTION value="#C2BD3D" style="color:#C2BD3D">��󴿧</OPTION>
<OPTION value="#AAB300" style="color:#AAB300">������</OPTION>
<OPTION value="#97A61E" style="color:#97A61E">��˨����</OPTION>
<OPTION value="#6DA895" style="color:#6DA895">���ļ���</OPTION>
<OPTION value="#89BDDE" style="color:#89BDDE">������</OPTION>
<OPTION value="#007BC3" style="color:#007BC3">��Ϫ��</OPTION>
<OPTION value="#00519A" style="color:#00519A">��������</OPTION>
<OPTION value="#384D98" style="color:#384D98">�����Ŀ�</OPTION>
<OPTION value="#4347A2" style="color:#4347A2">���˹���</OPTION>
<OPTION value="#A294C8" style="color:#A294C8">��ƣ��</OPTION>
<OPTION value="#714C99" style="color:#714C99">������</OPTION>
<OPTION value="#744B98" style="color:#744B98">���Գ���</OPTION>
<OPTION value="#C573B2" style="color:#C573B2">���Գ���</OPTION>
<OPTION value="#EAE0D5" style="color:#EAE0D5">���ῧ</OPTION>
<OPTION value="#DED2BF" style="color:#DED2BF">���ݲ翧</OPTION>
_CONFIG_

#-------------------------------------------------
# �¹� or �ɤ߹��ߡ�

if($CF{'program'}eq __FILE__){
	#ľ�ܼ¹Ԥ��ä���ư���Ф�
	require './core.cgi';
	&main;
}

#-------------------------------------------------
# �������
BEGIN{
    #���顼���Ф��饨�顼���̤�ɽ������褦��
    # Marldia Error Screen 1.2.2
    unless($CF{'program'}){
	$CF{'encoding'}='euc-jp';
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
    # Revision Number
    $CF{'idxrev'}=qq$Revision: 1.19 $;
}
1;
__END__
