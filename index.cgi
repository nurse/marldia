#!/usr/local/bin/perl

#------------------------------------------------------------------------------#
# 'Marldia' Chat System
# - Marldia Core File -
#
# $Revision: 1.6 $
# "This file is written in euc-jp, CRLF." 空
# Scripted by NARUSE Yui.
#------------------------------------------------------------------------------#
# $cvsid = q$Id: index.cgi,v 1.6 2002-04-20 16:34:50 naruse Exp $;
require 5.004;
use Fcntl qw(:DEFAULT :flock);
use strict;
use vars qw(%CF %IN %CK %IC);

#YOUR SITE NAME
$CF{'sitename'}='Airemix';
#YOUR SITE TOP
$CF{'sitehome'} = '/';
#titleタグでのチャットタイトル
$CF{'title'}=': Marldia :';
#ページ上のチャットタイトル
$CF{'pgtit'}=': Marldia :';


#管理モードへ移行する際のパスワード
$CF{'manpas'}='manage';
#最大ログ行数
$CF{'max'}=200;
#アクセス禁止な名前
$CF{'denyname'}='管理人';
#使用を許可するタグ（半角スペース区切り）
$CF{'tags'} = 'DEL EM SMALL STRONG RUBY RB RB RT RP';
#色の選択方法(select input)
$CF{'colway'}='input';
#アイコンのIMGタグに追加する属性
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

#EX Iconスイッチ '1'or'0'
$CF{'exicon'}='0';
#ファイル名指定アイコン
$CF{'exicfi'}='iconfile';

#EX Icon
$IC{'hae'}='mae.png'; #苗
$IC{'hie'}='mie.png'; #贄
$IC{'hue'}='mue.png'; #鵺
$IC{'hee'}='mee.png'; #姐
$IC{'hoe'}='moe.png'; #乃絵

#-------------------------------------------------
# 実行 or 読み込み？

if($0 eq __FILE__){
  #直接実行だったら動き出す
  require './core.cgi';
  &main;
}

#-------------------------------------------------
# 初期設定
BEGIN{
  # Revision Number
  $CF{'idxrev'}=qq$Revision: 1.6 $;
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
