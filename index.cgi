#!/usr/local/bin/perl

#------------------------------------------------------------------------------#
# 'Marldia' Chat System
# - Marldia Core File -
#
# $Revision: 1.11 $
# "This file is written in euc-jp, CRLF." 空
# Scripted by NARUSE Yui.
#------------------------------------------------------------------------------#
# $cvsid = q$Id: index.cgi,v 1.11 2002-10-22 08:29:15 naruse Exp $;
require 5.004;
use strict;
use vars qw(%CF %IN %CK %IC);
use lib '../bbs/';

#YOUR SITE NAME
$CF{'sitename'}='Airemix';
#YOUR SITE TOP
$CF{'sitehome'} = '/';
#titleタグでのチャットタイトル
$CF{'title'}=': Marldia :';
#ページ上のチャットタイトル
$CF{'pgtit'}=': Marldia :';


#管理モードへ移行する際のパスワード
$CF{'admipass'}='manage';
#最大ログ行数
$CF{'max'}=200;
#アクセス禁止な名前
$CF{'denyname'}='管理人';
#使用を許可するタグ（半角スペース区切り）
$CF{'tags'}='ACRONYM CODE DEL DFN EM Q SMALL STRONG RUBY RB RB RT RP';
#色の選択方法(select input)
$CF{'colway'}='select';
#アイコンのIMGタグに追加する属性
$CF{'imgatt'}=' width="48" height="48"';

$CF{'romline'}=20;
$CF{'romreload'}=120;
$CF{'defline'}=20;
$CF{'defreload'}=20;

$CF{'index'}= 'index.cgi'; #MIREILLE MAIN CGI
$CF{'style'} = 'style.css'; #CascadeStyleSheet
#$CF{'help'} = 'help.html'; #HELP FILE
$CF{'log'}  = 'log.cgi'; #LOG PATH
$CF{'rank'} = 'rank.cgi'; #LOG PATH
$CF{'iconDir'} = '/icon/half/'; #ICON DIRECTORY PATH
$CF{'iconList'} = 'icon.txt'; #ICON LIST PATH

$CF{'iconCtlg'} = 'iconctlg.cgi'; #ICON CATALOG PATH
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

#-----------------------------
# 色リスト
$CF{'colorList'}=<<'_CONFIG_';
<OPTION value="#343434" style="color:#343434">■墨</OPTION>
<OPTION value="#FBDADE" style="color:#FBDADE">■桜色</OPTION>
<OPTION value="#D53E62" style="color:#D53E62">■薔薇色</OPTION>
<OPTION value="#FF7F8F" style="color:#FF7F8F">■珊瑚色</OPTION>
<OPTION value="#AD3140" style="color:#AD3140">■臙脂色</OPTION>
<OPTION value="#9E2236" style="color:#9E2236">■茜色</OPTION>
<OPTION value="#905D54" style="color:#905D54">■小豆色</OPTION>
<OPTION value="#EF454A" style="color:#EF454A">■朱色</OPTION>
<OPTION value="#F1BB93" style="color:#F1BB93">■肌色</OPTION>
<OPTION value="#564539" style="color:#564539">■焦茶色</OPTION>
<OPTION value="#6B3E08" style="color:#6B3E08">■褐色</OPTION>
<OPTION value="#AA7A40" style="color:#AA7A40">■琥珀色</OPTION>
<OPTION value="#F8A900" style="color:#F8A900">■山吹色</OPTION>
<OPTION value="#EDAE00" style="color:#EDAE00">■鬱金色</OPTION>
<OPTION value="#C8A65D" style="color:#C8A65D">■芥子色</OPTION>
<OPTION value="#C2BD3D" style="color:#C2BD3D">■鶸色</OPTION>
<OPTION value="#AAB300" style="color:#AAB300">■若草色</OPTION>
<OPTION value="#97A61E" style="color:#97A61E">■萌黄色</OPTION>
<OPTION value="#6DA895" style="color:#6DA895">■青磁色</OPTION>
<OPTION value="#89BDDE" style="color:#89BDDE">■空色</OPTION>
<OPTION value="#007BC3" style="color:#007BC3">■露草色</OPTION>
<OPTION value="#00519A" style="color:#00519A">■瑠璃色</OPTION>
<OPTION value="#384D98" style="color:#384D98">■群青色</OPTION>
<OPTION value="#4347A2" style="color:#4347A2">■桔梗色</OPTION>
<OPTION value="#A294C8" style="color:#A294C8">■藤色</OPTION>
<OPTION value="#714C99" style="color:#714C99">■菫色</OPTION>
<OPTION value="#744B98" style="color:#744B98">■菖蒲色</OPTION>
<OPTION value="#C573B2" style="color:#C573B2">■菖蒲色</OPTION>
<OPTION value="#EAE0D5" style="color:#EAE0D5">■香色</OPTION>
<OPTION value="#DED2BF" style="color:#DED2BF">■象牙色</OPTION>
_CONFIG_

#-------------------------------------------------
# 実行 or 読み込み？

if($CF{'program'}eq __FILE__){
  #直接実行だったら動き出す
  require './core.cgi';
  &main;
}

#-------------------------------------------------
# 初期設定
BEGIN{
  unless(%CF){
    $CF{'program'}=__FILE__;
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
  # Revision Number
  $CF{'idxrev'}=qq$Revision: 1.11 $;
}
1;
__END__
