#!/usr/local/bin/perl

#------------------------------------------------------------------------------#
# 'Marldia' Chat System
# - Main Script -
#
# $Revision: 1.3 $
# "This file is written in euc-jp, CRLF." ��
# Scripted by NARUSE Yui.
#------------------------------------------------------------------------------#
# $cvsid = q$Id: index.cgi,v 1.3 2001-12-30 06:39:13 naruse Exp $;
#use 5.004;
#use lib './lib';
use Fcntl qw(:DEFAULT :flock);
use strict;
use vars qw(%CF %IN %CK %IC);

$CF{'name'} = 'Airemix'; #YOUR SITE NAME
$CF{'home'} = '/'; #YOUR SITE TOP
$CF{'title'}= ': Marldia :'; #CHAT TITLE
$CF{'icsz'}=' width="48" height="48"'; #ICON SIZE
$CF{'gzip'} = '/usr/bin/gzip'; #GZIP PATH

#������Կ�
$CF{'max'}='50';
#���������ػߤ�̾��
$CF{'denyname'}='������';
#���Ѥ���Ĥ��륿����Ⱦ�ѥ��ڡ������ڤ��
$CF{'tags'} = 'DEL EM SMALL STRONG RUBY RB RB RT RP';
#����������ˡ(select input)
$CF{'colway'}='input';

$CF{'romline'}=10;
$CF{'romreload'}=0;
$CF{'defline'}=20;
$CF{'defreload'}=20;

$ENV{'TZ'}  = 'JST-9'; #TimeZone
$CF{'index'}= 'index.cgi'; #MIREILLE MAIN CGI
$CF{'style'} = 'style.css'; #CascadeStyleSheet
$CF{'help'} = 'help.html'; #HELP FILE
$CF{'log'}  = 'log.pl'; #LOG PATH
$CF{'mem'}  = 'mem.pl'; #MEMLIST PATH
$CF{'rank'} = 'rank.pl'; #LOG PATH
$CF{'icon'} = '/icon/half/'; #ICON PATH
$CF{'icls'} = 'icon.txt'; #ICON LIST PATH
$CF{'samp'} = 'icon.html'; #ICON SAMPLE PATH

$CF{'cmic'}='0';#CustomIconSwitch '1'or'0'

#CustomIcon
$IC{'hae'}='mae.png'; #��
$IC{'hie'}='mie.png'; #��
$IC{'hue'}='mue.png'; #�
$IC{'hee'}='mee.png'; #��
$IC{'hoe'}='moe.png'; #ǵ��

#-------------------------------------------------
# �¹� or �ɤ߹��ߡ�

if($0 eq __FILE__){
  #ľ�ܼ¹Ԥ��ä���ư���Ф�
  require './core.cgi';
}

#-------------------------------------------------
# �������
BEGIN{
  # Revision Number
  $CF{'Index'}=qq$Revision: 1.3 $;
  (getlogin)||(umask(0)); #'nobody'�ä�''����͡�
  # Mireille Error Screen 1.2
  if($0 eq __FILE__){
    $SIG{'__DIE__'}=sub{
      print<<"_HTML_";
Content-Language: ja
Content-type: text/plain; charset=euc-jp

<pre>
       :: Mireille ::
   * Error Screen 1.2 (o__)o// *

_HTML_
      ($_[0])&&(print"ERROR: $_[0]");
      print"\n";
      for(qw(Index Style Core Exte)){
        ($CF{"$_"})&&(print qq($_: $CF{"$_"}\n));
      }
      print"\n";
      for(qw(log icon icls style)){
        ($CF{"$_"})&&(print qq($_: $CF{"$_"}\n));
      }
      print"\ngetlogin : ",getlogin,<<"_HTML_";

PerlVer  : $]
PerlPath : $^X
BaseTime : $^T
OS Name  : $^O
FileName : $0

 = = ENV = =
_HTML_
      for(qw(CONTENT_LENGTH QUERY_STRING REQUEST_METHOD SERVER_NAME HTTP_HOST SCRIPT_NAME OS SERVER_SOFTWARE PROCESSOR_IDENTIFIER)){
        ($ENV{"$_"})&&(print qq($_:\t$ENV{"$_"}\n));
      }
      print<<"_HTML_";

+#       Airemix Mireille       #+
+#  http://airemix.site.ne.jp/  #+
_HTML_
      exit;
    };
  }
}

1;
__END__
