#!/usr/local/bin/perl

#------------------------------------------------------------------------------#
# 'Marldia' Chat System
# - Marldia Core File -
#
# $Revision: 1.5 $
# "This file is written in euc-jp, CRLF." ��
# Scripted by NARUSE Yui.
#------------------------------------------------------------------------------#
# $cvsid = q$Id: index.cgi,v 1.5 2002-03-21 02:52:43 naruse Exp $;
require 5.004;
use Fcntl qw(:DEFAULT :flock);
use strict;
use vars qw(%CF %IN %CK %IC);

#YOUR SITE NAME
$CF{'sitename'}='Airemix';
#YOUR SITE TOP
$CF{'sitehome'} = '/';
#title�����ǤΥ���åȥ����ȥ�
$CF{'title'}=': Marldia :';
#�ڡ�����Υ���åȥ����ȥ�
$CF{'pgtit'}=': Marldia :';

#������Կ�
$CF{'max'}=200;
#���������ػߤ�̾��
$CF{'denyname'}='������';
#���Ѥ���Ĥ��륿����Ⱦ�ѥ��ڡ������ڤ��
$CF{'tags'} = 'DEL EM SMALL STRONG RUBY RB RB RT RP';
#����������ˡ(select input)
$CF{'colway'}='input';
#���������IMG�������ɲä���°��
$CF{'imgatt'}=' width="48" height="48"';

$CF{'romline'}=20;
$CF{'romreload'}=120;
$CF{'defline'}=20;
$CF{'defreload'}=20;

$CF{'index'}= 'index.cgi'; #MIREILLE MAIN CGI
$CF{'style'} = 'style.css'; #CascadeStyleSheet
#$CF{'help'} = 'help.html'; #HELP FILE
$CF{'log'}  = 'log.pl'; #LOG PATH
$CF{'rank'} = 'rank.pl'; #LOG PATH
$CF{'icondir'} = '/icon/half/'; #ICON DIRECTORY PATH
$CF{'icls'} = 'icon.txt'; #ICON LIST PATH
#$CF{'samp'} = 'icon.html'; #ICON SAMPLE PATH
$ENV{'TZ'}  = 'JST-9'; #TimeZone
$CF{'gzip'} = 'gzip'; #GZIP PATH

#EX Icon�����å� '1'or'0'
$CF{'exicon'}='0';
#�ե�����̾���ꥢ������
$CF{'exicfi'}='iconfile';

#EX Icon
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
  $CF{'Index'}=qq$Revision: 1.5 $;
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
