#!/usr/local/bin/perl

#------------------------------------------------------------------------------#
# 'Marldia' Chat System
# - Main Script -
#
# $Revision: 1.1 $
# "This file is written in euc-jp, CRLF." 空
# Scripted by NARUSE Yui.
#------------------------------------------------------------------------------#
# $cvsid = q$Id: index.cgi,v 1.1 2001-10-21 12:27:17 naruse Exp $;
#use 5.004;
#use lib './lib';
use Fcntl qw(:DEFAULT :flock);
use strict;
use vars qw(%CF %IN %CK %IC);

$CF{'name'} = 'Airemix'; #YOUR SITE NAME
$CF{'home'} = '/'; #YOUR SITE TOP
$CF{'title'}= ': Marldia :'; #CHAT TITLE

#最大ログ行数
$CF{'max'}='50';
#アクセス禁止な名前
$CF{'denyname'}='管理人';

$ENV{'TZ'}  = 'JST-9'; #TimeZone
$CF{'index'}= 'index.cgi'; #MIREILLE MAIN CGI
$CF{'style'} = 'style.css'; #CascadeStyleSheet
$CF{'help'} = 'help.html'; #HELP FILE
$CF{'log'}  = 'log.pl'; #LOG PATH
$CF{'mem'}  = 'mem.pl'; #MEMLIST PATH
$CF{'rank'} = 'rank.pl'; #LOG PATH
$CF{'icon'} = '/icon/half/'; #ICON PATH
$CF{'icli'} = 'icon.txt'; #ICON LIST PATH
$CF{'samp'} = 'icon.html'; #ICON SAMPLE PATH
$CF{'gzip'} = '/usr/bin/gzip'; #GZIP PATH

$CF{'icsz'}=q{ width='50' height='50'}; #ICON SIZE

$CF{'cmic'}='0';#CustomIconSwitch '1'or'0'

#CustomIcon
$IC{'hae'}='mae.png'; #苗
$IC{'hie'}='mie.png'; #贄
$IC{'hue'}='mue.png'; #鵺
$IC{'hee'}='mee.png'; #姐
$IC{'hoe'}='moe.png'; #乃絵

require 'core.cgi';

#-------------------------------------------------
# 初期設定
BEGIN{
  # Revision Number
  $CF{'idxrev'}=qq$Revision: 1.1 $;
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
Style : $CF{'styrev'}
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
