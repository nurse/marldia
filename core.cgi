#!/usr/local/bin/perl

#------------------------------------------------------------------------------#
# 'Marldia' Chat System
# - Main Script -
#
# $Revision: 1.21 $
# "This file is written in euc-jp, CRLF." 空
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
# main直下のサブルーチン群

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
このページはMicrosoft Internet Explorer 6.0 向けに作られています
MSIE5.01やNetscape6、Mozilla0.9以上でもそこそこに見ることが出来ると思います
Netscape4.xでは表示の一部が崩れる可能性があります
テーブルやフレームに対応していないブラウザでは、表示の大部分が崩れてしまうため、
実質的に閲覧することができません
Mozilla4以上互換のブラウザでまた来てください
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
<TABLE cellspacing="0" style="width:770px" summary="発言フォーム">
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
<LABEL accesskey="z" for="surface" title="sUrface&#10;表情アイコンを選択します（使えれば）"
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
<DIV style="margin:0.3em 0;text-align:center" title="reloadQ&#10;上フレームをリロードします"
>[<A href="$CF{'index'}?north" accesskey="q" tabindex="52">再読込(<SPAN class="ak">Q</SPAN>)</A>]
<INPUT name="south" type="hidden" value="">
<INPUT name="previousBody" type="hidden" value="">
</DIV>
</TD>
<TH><LABEL accesskey="n" for="name" title="Name&#10;参加者名、発言者名などで使う名前です"
>名前(<SPAN class="ak">N</SPAN>)</LABEL>:</TH>
<TD><INPUT type="text" class="text" name="name" id="name" maxlength="20" size="20"
style="ime-mode:active;width:80px" value="$CK{'name'}" tabindex="11">
<LABEL accesskey="k" for="cook" title="cooKie&#10;チェックを入れると現在の設定をCookieに保存します"
><INPUT type="checkbox" name="cook" id="cook" class="check" tabindex="12" checked
>Coo<SPAN class="ak">k</SPAN>ie</LABEL></TD>
<TH><LABEL accesskey="c" for="color" title="name Color&#10;参加者名、発言者名などで使う名前の色です"
>名前色(<SPAN class="ak">C</SPAN>)</LABEL>:</TH>
<TD>@{[&iptcol('color','tabindex="21"')]}</TD>
<TH><LABEL accesskey="g" for="line" title="log Gyosu&#10;表示するログの行数です&#10;最高$CF{'max'}行"
>行数(<SPAN class="ak">G</SPAN>)</LABEL>:</TH>
<TD><INPUT type="text" class="text" name="line" id="line" maxlength="4" size="4"
style="ime-mode:disabled;width:32px" value="$CK{'line'}行" tabindex="31"></TD>
<TD style="text-align:center"><INPUT type="submit" accesskey="s" class="submit"
title="Submit&#10;現在の内容で発言します" value="OK" tabindex="41"></TD>
<TD></TD>
</TR>

<TR>
<TH><LABEL accesskey="i" for="icon" title="Icon&#10;使用するアイコンを選択します"
><A href="$CF{'index'}?icct" target="south">アイコン</A>(<SPAN class="ak">I</SPAN>)</LABEL></TH>
<TD>@{[&iptico($CK{'icon'},'tabindex="13"')]}</TD>
<TH><LABEL accesskey="c" for="bcolo" title="body Color&#10;発言した本文の色です"
>文章色(<SPAN class="ak">C</SPAN>)</LABEL>:</TH>
<TD>@{[&iptcol('bcolo','tabindex="22"')]}</TD>
<TH><LABEL accesskey="r" for="reload" title="Reload&#10;何秒ごとに自動的にリロードするか、です"
>間隔(<SPAN class="ak">R</SPAN>)</LABEL>:</TH>
<TD><INPUT type="text" class="text" name="reload" id="reload" maxlength="4" size="4"
style="ime-mode:disabled;width:32px" value="$CK{'reload'}秒" tabindex="32"></TD>
<TD style="text-align:center"><INPUT type="reset" class="reset"
title="reset&#10;内容を初期化します" value="キャンセル" tabindex="42"></TD>
</TR>

<TR>
<TH><LABEL accesskey="b" for="body" title="Body&#10;発言する本文の内容です&#10;\$rankで発言ランキング、\$memberで参加者一覧を見れます">内容(<SPAN class="ak">B</SPAN>)</LABEL>:</TH>
<TD colspan="5"><INPUT type="text" class="text" name="body" id="body" maxlength="300" size="100"
style="ime-mode:active;width:450px" tabindex="1"></TD>
<TD style="text-align:center"><INPUT type="checkbox" name="quit" id="quit" class="check" tabindex="51"
><LABEL accesskey="Q" for="quit" title="Quit&#10;チェックを入れると参加者から名前を消します。"
>退室モード(<SPAN class="ak">Q</SPAN>)</LABEL></TD>
</TR>

<TR>
<TH><LABEL accesskey="y" for="id" title="identitY name&#10;CGI内部で使用する、管理用の名前を選択します
この名前が実際に表に出ることはありません\nこの登録名が同じだと同一人物だとみなされます"
>Identit<SPAN class="ak">y</SPAN></LABEL>:</TH>
<TD><INPUT type="text" class="text" name="id" id="id" maxlength="20" size="20"
style="ime-mode:active;width:150px" value="$CK{'id'}" tabindex="101"></TD>
<TH><LABEL accesskey="l" for="email" title="e-maiL&#10;メールアドレスです"
>E-mai<SPAN class="ak">l</SPAN></LABEL>:</TH>
<TD colspan="3"><INPUT type="text" class="text" name="email" id="email" maxlength="200" size="40"
style="ime-mode:inactive;width:200px" value="$CK{'email'}" tabindex="111"></TD>
<TH style="text-align:center">[ <A href="$CF{'sitehome'}" target="_top"
title="$CF{'sitename'}へ帰ります&#10;退室メッセージは出ないので帰りの挨拶を忘れずに"
>$CF{'sitename'}へ帰る</A> ]</TH>
</TR>

<TR>
<TH><LABEL accesskey="p" for="opt" title="oPtion&#10;オプション"
>O<SPAN class="ak">p</SPAN>tion</LABEL>:</TH>
<TD><INPUT type="text" class="text" name="opt" id="opt" maxlength="200" style="ime-mode:inactive;width:150px"
value="$CK{'opt'}" tabindex="102" onchange="changeOption()"></TD>
<TH><LABEL accesskey="o" for="home" title="hOme&#10;サイトのURLです"
>H<SPAN class="ak">o</SPAN>me</LABEL>:</TH>
<TD colspan="3"><INPUT type="text" class="text" name="home" id="home" maxlength="200" size="40"
style="ime-mode:inactive;width:200px" value="$CK{'home'}" tabindex="112"></TD>
<TH style="letter-cpacing:-1px;text-align:center">-<A href="http://www.airemix.com/" title="Airemixへいってみる"
target="_top">Marldia $CF{'version'}</A>-</TH>
</TR>
</TABLE>
</FORM>

<SCRIPT type="text/javascript" defer>
<!--
/*========================================================*/
// 初期化
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
    #Viewの共通処理
    my ($chatlog,$members) = &commonRoutineForView();
    
    #-----------------------------
    #クエリ
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
    #携帯電話用クエリ
    my $mobileQuery ='south;' .
    	join(';',map{my$val=$IN{$_};$val=~s/&#64;/\@/;$val=~s{(\W)}{'%'.unpack('H2',$1)}ego;"$_=$val"}
	     grep{defined$IN{$_}}qw(line name color bcolo icon id email opt home))
	if $IN{'icon'};
    
    #-----------------------------
    #参加者情報
    my@singers=map{qq(<A style="color:$_->{'color'}" title="$_->{'blank'}秒">$_->{'name'}</A>☆)}
    sort{$a->{'blank'}<=>$b->{'blank'}}$members->getSingersInfo;
    my$intMembers=scalar keys%{$members};
    my$intSingers=@singers;
    my$intAudiences=$intMembers-$intSingers;
    my$strMembers;
    if(@singers){
	$strMembers="@singers";
    }else{
	my@wabisabi=(qw(かんこどり みてるだけ？ (-_☆)ｷﾗｰﾝ),"@{[('|_･)ﾁﾗ☆')x$intAudiences]}");
	$strMembers=$wabisabi[int(rand@wabisabi)];
    }

    #---------------------------------------
    #データ表示
    #-----------------------------
    #ヘッダ出力
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
    #参加者表示
    my $reload = $IN{'reload'} ? sprintf('%s秒間隔',$IN{'reload'}) : 'No Reload';
    $reload = sprintf( '<A href="%s?%s">%s</A>', $CF{'mobile'}, $mobileQuery, $reload) if $mobileQuery;
    print<<"_HTML_";
<TABLE class="meminfo" summary="参加者情報など"><TR>
<TD class="reload">[ <A href="$CF{'index'}?$query">@{[sprintf('%02d:%02d:%02d',(localtime$^T)[2,1,0])]}</A> ]</TD>
<TD class="member">[合計:$intMembers人 参加者:$intSingers人 観客:$intAudiences人] [ $strMembers ]</TD>
<TD class="respan">($reload)</TD>
</TR></TABLE>
_HTML_
    
    #-----------------------------
    #ログ表示
    my$i=0;
    for(@{$chatlog}){
	my%DT=%{$_};
	'del'eq$DT{'Mar1'}&&next;
	++$i>$IN{'line'}&&last;

	#日付
	my$date=&date($DT{'time'});
	#名前・メールアドレス・名前色
	my$name=$DT{'email'}&&$DT{'color'}?
qq(<A href="mailto:$DT{'email'}" title="$DT{'email'}" style="color:$DT{'color'}">$DT{'name'}</A>)
	    :$DT{'email'}?qq(<A href="mailto:$DT{'email'}" title="$DT{'email'}">$DT{'name'}</A>)
	    :$DT{'color'}?qq(<A style="color:$DT{'color'}">$DT{'name'}</A>)
	    :$DT{'name'};
	#ホーム
	my$home=$DT{'home'}?qq(<A href="$DT{'home'}" target="_blank" title="$DT{'home'}">≫</A>):'≫';
	$DT{'_Icon'}=&getIconTag(\%DT)||'&nbsp;';
	#レベル取得
	$DT{'level'}=&getLevel($DT{'exp'});
	#削除ボタン
	my$del=$IN{'id'}&&$DT{'id'}eq$IN{'id'}?qq([<A href="$CF{'index'}?del=$DT{'exp'}&#59;$query">削除</A>])
	    :'&nbsp;';
	#出力
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
# レベル計算
#
sub getLevel{
    #レベル計算-まとも
    my$lev=0;
    my$sum=0;
    while($sum<$_[0]){
	$lev++;
	$sum+=int(exp(($lev-1)/15)*100);
    }
    return $lev;
    #レベル計算-てきとー
    srand($_[0]);
    return 1+int(rand(sqrt$_[0]*2));
}


#-------------------------------------------------
# 利用者コマンド
#
sub modeUsercmd{
    unless($IN{'opt'}){
	die"「何もしない＠管理」";
    }
    #引数処理
    my@arg=grep{s/\\(\\)|\\(")|"/$1$2/go;$_;}($IN{'opt'}=~
					      /(?!\s)[^"\\\s]*(?:\\[^\s][^"\\\s]*)*(?:"[^"\\]*(?:\\.[^"\\]*)*(?:"[^"\\\s]*(?:\\[^\s][^"\\\s]*)*)?)*\\?/go);
=item 利用コマンド

◇rank
ランキングを表示

◇mem
参加者情報を表示

◇del <exp>
発言削除

=cut

    #分岐
    if('rank'eq$arg[0]){
	#発言ランキング表示
	&header;
	print<<'_HTML_';
<TABLE class="table" summary="発言ランキング">
<CAPTION>ハツゲンらんきんぐ（ゆーざーもーど）</CAPTION>
<COL span="4">
<TH scope="col">じゅんい</TH>
<TH scope="col">なまえ</TH>
<TH scope="col">けいけんち</TH>
<TH scope="col">しょうそく</TH>
<TH scope="col">はつとうじょう</TH>
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
	#見物人一覧
	&header;
	print<<'_HTML_';
<TABLE class="table" summary="参加者の一覧">
<CAPTION>さんかしゃ いちらん（ゆーざーもーど）</CAPTION>
<COL span="3">
<TH scope="col">なまえ</TH>
<TH scope="col">ぶらんく</TH>
<TH scope="col">おとさた</TH>
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
    #無効なコマンド
    die"'$arg[0]'はコマンドとしてとして認識されていません";
    exit;
}


#-------------------------------------------------
# 管理コマンド
#
sub modeAdmicmd{
    unless($IN{'opt'}){
	die"「何もしない＠管理」";
    }
    #引数処理
    my@arg=grep{s/\\(\\)|\\(")|"/$1$2/go;length$_;}
    ($IN{'opt'}=~
     /(?!\s)[^"\\\s]*(?:\\[^\s][^"\\\s]*)*(?:"[^"\\]*(?:\\.[^"\\]*)*(?:"[^"\\\s]*(?:\\[^\s][^"\\\s]*)*)?)*\\?/go);
    
=item 管理コマンド

$CF{'admipass'}='admicmd';なら、
#admicmd ...
で...というコマンドが発動

◇rank (del|merge|conv) <id ...>
ランキングを表示
・del
引数として指定されたIDの情報を削除
・merge
第一引数のIDに、それ以降のIDを統合する
・conv
1.5以前のランキングデータを1.6形式に変換する

◇mem
参加者情報を表示

◇del <id> [<exp>]
発言削除

=cut

    #分岐
    if(!$arg[0]){
    }elsif('rank'eq$arg[0]){
	#発言ランキング
	my$rank=Rank->getInstance;
	unless($arg[1]){
	}elsif('del'eq$arg[1]){
	    #ランキングから削除
	    $rank->delete($arg[2]);
	}elsif('merge'eq$arg[1]){
	    #IDおよび経験地の統合
	    exists$rank->{$arg[2]}&&exists$rank->{$arg[2]}->{'exp'}||die"そんな人いない";
	    for(3..$#arg){
		(!$rank->{$arg[$_]}||!$rank->{$arg[$_]}->{'exp'})&&next;
		$rank->{$arg[2]}->{'exp'}+=$rank->{$arg[$_]}->{'exp'};
		$rank->delete($arg[$_]);
	    }
	}

	#ランキング表示
	&header;
	print<<'_HTML_';
<TABLE class="table" summary="発言ランキング">
<CAPTION>超！発言ランキング</CAPTION>
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
	#見物人一覧
	&header;
	print<<'_HTML_';
<TABLE class="table" summary="参加者の一覧">
<CAPTION>超！参加者一覧</CAPTION>
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
	#発言削除
	my @result = Chatlog->delete({id=>$arg[1],exp=>$arg[2]});
	&header;
	if(@result){
	    print"<P>削除しましたょ</P>";
	}else{
	    print"<P>なにも削除しなかったょ</P>";
	}
	&showFooter;
	#	}elsif(''eq$arg[0]){
	#		#
    }
    #無効なコマンド
    die"'$arg[0]'はコマンドとしてとして認識されていません";
    exit;
}


#-------------------------------------------------
# Locationで転送
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
# main直下のサブルーチン群の補助

#-------------------------------------------------
# Form内容取得
#
sub getParams{
    unless($ENV{'REQUEST_METHOD'}){
    }elsif('HEAD'eq$ENV{'REQUEST_METHOD'}){ #forWWWD
	#MethodがHEADならばLastModifedを出力して、
	#最後の投稿時刻を知らせる
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
	    #GZIP失敗時のエラーメッセージ
	    binmode STDOUT;
	    print unpack("u",#GZIP圧縮-uuencodeされたエラーメッセージ
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
	#GZIP圧縮転送をかけられるときはかける
	print ' 'x 2048if$ENV{'HTTP_USER_AGENT'}&&index($ENV{'HTTP_USER_AGENT'},'MSIE')+1; #IEのバグ対策
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
# フッター出力
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
# Cookieを取得する
#
sub getCookie{
    $ENV{'HTTP_COOKIE'}||return undef;
    # EUC-JP文字
    my$eucchar=qr((?:
[\x0A\x0D\x20-\x7E]			# 1バイト EUC-JP文字改-\x09
|(?:[\x8E\xA1-\xFE][\xA1-\xFE])	# 2バイト EUC-JP文字
|(?:\x8F[\xA1-\xFE]{2})			# 3バイト EUC-JP文字
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
# Cookieを設定する
#
sub setCookie{
    my$cook=join('',map{"$_=\t$IN{$_};\t"}qw(id name color bcolo line reload icon email home opt));
    $cook=~s{(\W)}{'%'.unpack('H2',$1)}ego;
    my$expires=$^T+33554432; #33554432=2<<24; #33554432という数字に特に意味はない、ちなみに一年と少し
    $CF{'-setCookie'}="Marldia=$cook; expires=".&datef($expires,'cookie');
    $CF{'set_cookie_by_meta_tags'}=1if index($ENV{'SERVER_NAME'},'tok2.com')>-1&&!defined$CF{'set_cookie_by_meta_tags'};
    if($CF{'set_cookie_by_meta_tags'}){
	#tok2対策
    }else{
	print map{qq(Set-Cookie: $_\n)}split("\n",$CF{'-setCookie'});
	undef($CF{'-setCookie'});
    }
}

#-------------------------------------------------
# 投稿日時表示用にフォーマットされた日付取得を返す
sub date{
=item 引数
$ time形式時刻
=cut
    $CF{'timezone'}||&cfgTimeZone($ENV{'TZ'});
    my($sec,$min,$hour,$day,$mon,$year,$wday)=gmtime($_[0]+$CF{'timeOffset'});
    #sprintfの説明は、Perlの解説を見てください^^;;
    return sprintf("%4d年%02d月%02d日(%s) %02d時%02d分%s" #"1970年01月01日(木) 09時00分"の例
		   ,$year+1900,$mon+1,$day,('日','月','火','水','木','金','土')[$wday],$hour,$min,$ENV{'TZ'});
    #	return sprintf("%1d:%01d:%2d %4d/%02d/%02d(%s)" #"9:0: 0 1970/01/01(Thu)"の例
    #	,$hour,$min,$sec,$year+1900,$mon+1,$day,('Sun','Mon','Tue','Wed','Thu','Fri','Sat')[$wday]);
}


#-------------------------------------------------
# フォーマットされた日付取得を返す
#
sub datef{
=item 引数
$ time形式の時刻
;
$ 出力形式(cookie|last|dateTime)
=cut
    defined$_[0]||return undef;
    my$time=shift;
    my$type=shift;
    unless($type){
    }elsif('cookie'eq$type){
	# Netscape風Cookie用
	return sprintf("%s, %02d-%s-%d %s GMT",(split(/\s+/o,gmtime$time))[0,2,1,4,3]);
    }elsif('rfc1123'eq$type){
	# RFC1123 主としてLastModified用
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
# タイムゾーンの取得
sub cfgTimeZone{
=pod
タイムゾーンを環境変数TZから取得して、%CFに設定する
他の関数はこの$CF{'timezone'},$CF{'timeOffset'}を使って、
gmtime()から確実に希望の地域の時刻を算出できる
=item 引数
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
#引数の前処理
sub commonRoutineForView{
    #-----------------------------
    #コマンドの読み込み
    my%EX;
    for(split(';',$IN{'opt'})){
	my($i,$j)=split('=',$_,2);
	$i||next;
	$i=~/(\S+(?:\s+\S+)*)/o||next;
	$i=$1;
	$j=defined$j&&$j=~/(\S+(?:\s+\S+)*)/o?$1:'';
	$EX{$i}=$j;
    }
    
    #専用アイコン機能。index.cgiで設定する。
    #index.cgiで指定したアイコンパスワードに合致すれば。
    $IN{'icon'}=$IC{$EX{'icon'}}if$CF{'exicon'}&&$IC{$EX{'icon'}};
    
    #絶対指定アイコン
    $IN{'icon'}=''if$CF{'absoluteIcon'}&&$EX{'absoluteIcon'};
    #相対指定アイコン
    $IN{'icon'}=''if$CF{'relativeIcon'}&&$EX{'relativeIcon'};
    #表情アイコン
    $IN{'icon'}=$IN{'surface'}if!$IN{'icon'}&&$IN{'surface'};
    
    $IN{'body'}=$IN{'body'}?Filter->filteringBody($IN{'body'},%EX):'';
    $IN{'isActive'}=$ENV{'CONTENT_LENGTH'}?1:0;
    $IN{'time'}=$^T;
    
    #-----------------------------
    #クッキー書き込み
    $IN{'cook'}&&&setCookie;
    
    #---------------------------------------
    #参加者・ランキング・書き込み処理
    my$chatlog=Chatlog->getInstance;
    my$members=Members->getInstance;
    
    #-----------------------------
    #自分のデータを追加
    $IN{'reload'}=$members->add(\%IN);
    
    #-----------------------------
    #書き込み
    if(length$IN{'body'}){
	#ランキング加点
	$IN{'exp'}=Rank->plusExp(\%IN);
	#発言処理
	$chatlog->add(\%IN);
    }elsif($IN{'del'}){
	#発言削除
	$chatlog->delete({id=>$IN{'id'},exp=>$IN{'del'}});
    }
    return($chatlog,$members);
}


#-------------------------------------------------
# アイコン用のIMGタグ
#
sub getIconTag{
=item 引数

$ 記事情報の入ったハッシュへのリファレンス
;
$ どのような形で返すかの設定

=item 返り値設定
「-!keyword!-」のような形式です
具体的には以下のとおり
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
	#絶対指定アイコン
	$DT{'dir'}='';
	$DT{'file'}||=$1;
    }elsif($CF{'relativeIcon'}&&$data->{'opt'}=~/(?:^|;)relativeIcon=([^;:.]*(?:\.[^;:.]+)*)/o){
	#相対指定アイコン
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
# アイコンリスト
#
sub iptico{

=item 引数

$ デフォルト指定にしたいアイコンファイル名を入れた書き換え可能な変数
;
$ SELECTタグに追加したい属性
$ 拡張コマンド

=item 複数アイコンリスト

$CF{'iconList'}の最初の一文字が' '（半角空白）だった場合複数リストモードになります
具体的な例を出すと、
・単一とみなされる例
'icon.txt'
'icon1.txt icon2.txt' #"icon1.txt icon2"というテキストファイルだとみなします
'"icon.txt" "exicon.txt"'
・複数とみなされる例
' "icon.txt" "exicon.txt"'
' "icon.txt" exicon.txt'
' icon.txt exicon.txt'

=cut

    my$opt=$_[1]?" $_[1]":'';
    if($CF{'-CacheIconList'}&&('reset'ne$_[2])){
	#キャッシュである$CF{'-CacheIconList'}を返す
	return$CF{'-CacheIconList'};
    }

    #アイコンリスト読み込み
    my$iconlist='';
    if($CK{'opt'}=~/\biconlist=nolist(;|$)/o){
	#`icon=nolist`でアイコンリストを読み込まない
    }elsif($CF{'iconList'}=~/^ /o){
	#複数アイコンリスト読み込み
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
	#単一アイコンリスト読み込み
	open(RD,'<'.$CF{'iconList'})||die"Can't open single-iconlist.";
	eval{flock(RD,1)};
	read(RD,$iconlist,-s$CF{'iconList'});
	close(RD);
    }

    #選択アイコンの決定＋SELECTタグの中身
    my$isEconomy=$CK{'opt'}=~/(?:^|;)iconlist=economy(?:\s*;|$)/o;
    my$isAbsolute=0;
    my$isDisabled='';
    unless(@_){
    }elsif($CF{'exicon'}&&($CK{'opt'}=~/(?:^|;)icon=([^;]*)/o)&&$IC{$1}){
	#パスワード型
	$_[0]=$IC{$1};
	if($isEconomy){
	    $iconlist=qq(<OPTION value="$_[0]" selected>専用アイコン</OPTION>\n);
	}else{
	    $iconlist.=qq(<OPTION value="$_[0]" selected>専用アイコン</OPTION>\n);
	}
    }elsif($CF{'absoluteIcon'}&&$CK{'opt'}=~/(?:^|;)absoluteIcon=([^;]*)/o){
	#絶対指定アイコン
	$_[0]=$1;
	$isAbsolute=1;
	$isDisabled=1;
	$iconlist=qq(<OPTION value="$_[0]" selected>絶対指定</OPTION>\n)if$isEconomy;
    }elsif($CF{'relativeIcon'}&&$CK{'opt'}=~/(?:^|;)relativeIcon=([^;:.]*(\.[^;:.]+)*)/o){
	#相対指定アイコン
	$_[0]=$1;
	$iconlist=qq(<OPTION value="$1" selected>相対指定</OPTION>\n)if$isEconomy;
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
# カラーリスト読み込み
#
sub iptcol{

=item 引数

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
# ユーザー向けエラー
#
sub showUserError{
    my$message=shift();
    &showHeader;
    print<<"_HTML_";
<H2 class="heading2">- エラーが発生しました -</H2>
<P>ご不便をかけて申し訳ございません<BR>
<span class="warning">$message</span>ため、<BR>正常な処理を続行することができませんでした<BR>
以下に念のため今入力されたデータを羅列しておきます<BR>
重要な情報がある場合、保存しておいて、またの機会に投稿してください</P>
<TABLE border="1" summary="ユーザー入力変数を表示しておく">
<CAPTION>今受け取った引数</CAPTION>
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
	$singleton&&die 'これはSingletonなのでnewを勝手に呼ばないで！getInstanceを使うこと';
	my$class=ref($_[0])||$_[0];shift;

	my$params;
	my@params;
	#引数取得
	unless($ENV{'REQUEST_METHOD'}){@params=@ARGV}
	elsif('HEAD'eq$ENV{'REQUEST_METHOD'}){return}
	elsif('POST'eq$ENV{'REQUEST_METHOD'}){read(STDIN,$params,$ENV{'CONTENT_LENGTH'})}
	elsif('GET'eq$ENV{'REQUEST_METHOD'}){$params=$ENV{'QUERY_STRING'}}
	# EUC-JP文字
	my$eucchar=qr((?:[\x09\x0A\x0D\x20-\x7E]|[\x8E\xA1-\xFE][\xA1-\xFE]|\x8F[\xA1-\xFE]{2}))x;

	#引数をハッシュに
	if(!$params){
	}elsif(length$params>262114){ # 262114:引数サイズの上限(byte)
	    #サイズ制限
	    &showHeader;print"いくらなんでも量が多すぎます\n$params";&showFooter;exit;
	}elsif(length$params>0){
	    #入力を展開
	    @params=split(/[&;]/o,$params);
	}

	#入力を展開してハッシュに入れる
	my%DT;
	while(@params){
	    my($i,$j)=split('=',shift(@params),2);
	    $i=~/([a-z][-.:\w]*)/o||next;$i=$1;
	    defined$j||($DT{$i}='')||next;
	    study$j;
	    $j=~tr/+/\ /;
	    $j=~s/%([\dA-Fa-f]{2})/pack('H2',$1)/ego;
	    $j=$j=~/($eucchar*)/o?$1:'';
	    #メインフレームの改行は\x85らしいけど、対応する必要ないよね？
	    $j=~s/\x0D\x0A/\n/go;$j=~tr/\r/\n/;
	    if('body'ne$i){
		#本文以外は全面タグ禁止
		$j=~s/\t/&nbsp;&nbsp;/go;
		$j=~s/&(#?\w+;)?/$1?"&$1":'&#38;'/ego;
		$j=~s/"/&#34;/go;
		$j=~s/'/&#39;/go;
		$j=~s/</&#60;/go;
		$j=~s/>/&#62;/go;
		$j=~s/\n+$//o;
		$j=~s/\n/<BR>/go;
	    }#本文は後でまとめて
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
    # EUC-JP文字
    my$eucchar=qr((?:[\x09\x0A\x0D\x20-\x7E]|[\x8E\xA1-\xFE][\xA1-\xFE]|\x8F[\xA1-\xFE]{2}))x;
    #[-_.!~*'()a-zA-Z0-9;:&=+$,]	->[!$&-.\w:;=~]
    #[-_.!~*'()a-zA-Z0-9:@&=+$,]	->[!$&-.\w:=@~]
    #[-_.!~*'()a-zA-Z0-9;/?:@&=+$,]	->[!$&-/\w:;=?@~]
    #[-_.!~*'()a-zA-Z0-9;&=+$,]		->[!$&-.\w;=~]
    #http URL の正規表現
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
    #ftp URL の正規表現
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
    #メールアドレスの正規表現改
    #"aaa@localhost"などを掲示板で「メールアドレス」として使うとは思えないので。
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
	#コマンド系
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
	    #フレーム
	    $IN{'mode'}='frame';
	}elsif(defined$DT{'icct'}){
	    #アイコンカタログ
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
	    #北
	    $IN{'mode'}='north';
	    $IN{'line'}=$::CF{'defline'};
	    $IN{'reload'}=$::CF{'defreload'};
	}elsif(defined$DT{'south'}){
	    #南
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
	#本文の処理
	#form->data変換
	unless(defined$str&&length$str){
	    $str='';
	}elsif($::CF{'tags'}&&'ALLALL'eq$::CF{'tags'}){
	    #ALLALLは全面OK。但し強調は無効。URI自動リンクも無効。
	    #自前でリンクを張ったり、強調してあるものを、二重にリンク・強調してしまいますから
	}else{
	    #本文のみタグを使ってもいい設定にもできる
	    my$attrdel=0;#属性を消す/消さない(1/0)
	    study$str;
	    $str=~tr/"'<>/\01-\04/;
	    $str=~s/&(#?\w+;)/\05$1/go;

	    #タグ処理
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
		#もし BRタグや Aタグなど特定のタグだけは削除したくない場合には， 
		#$tag_tmp = $2; の後に，次のようにして $tag_tmp を $result に加えるようにすればできます． 
		#$result .= $tag_tmp if $tag_tmp =~ /^<\/?(BR|A)(?![\dA-Za-z])/io;
		my$remain=join('|',grep{/^(?:\\w\+|\w+)$/o}split(/\s+/o,$tags));
		#逆に FONTタグや IMGタグなど特定のタグだけ削除したい場合には， 
		#$tag_tmp = $2; の後に，次のようにして $tag_tmp を $result に加えるようにすればできます． 
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
		#許可タグ無しorCommand:notag
	    }

	    #URI自動リンク
	    if($::CF{'noautolink'}||!$EX{'noautolink'}){
		#実稼動部
		my$href_regex=qr{($http_URL_regex|$ftp_URL_regex|($mail_regex))};
		my@isMail=('<A class="autolink" href="mailto:','<A class="autolink" href="');
		$str=~s{((?:\G|>)[^<]*?)$href_regex}{$1$isMail[!$3]$2" target="_blank">$2</A>}go;
		if($str=~/<(?:XMP|PLAINTEXT|SCRIPT)(?![0-9A-Za-z])/io){
		    #XMP/PLAINTEXT/SCRIPTタグがあるとき
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
	$singleton&&die 'これはSingletonなのでnewを勝手に呼ばないで！getInstanceを使うこと';
	my$class=ref($_[0])||$_[0];shift;
	local*LOGFILE;
	if(-e$path){
	    open(LOGFILE,'+<'.$path)||die"Can't read Logfile($path)[$?:$!]";
	    #+>>とするとseek($fh,0,0)が動いてくれないので注意！
	    $fh=*LOGFILE{IO};
	    eval{flock($fh,2)};
	    #memberを追加
	    while(<$fh>){/\S/o?push(@members,$_):last}
	    #chatlogを追加
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

    #dispose -- 変更済みデータをファイルに保存
    sub Logfile::dispose{
	(@members&&@chatlog)||return;
	my$self=shift;
	truncate($path,0);#$fhじゃダメ
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
	$singleton&&die 'これはSingletonなのでnewを勝手に呼ばないで！getInstanceを使うこと';
	my$class=ref($_[0])||$_[0];shift;
	$logfile=Logfile->getInstance;
	my$self=[
		 map{{/([^\t]+)=\t([^\t]*);\t/go}}
		 grep{/^Mar1=\t[^\t]*;\t(?:[^\t]*=\t[^\t]*;\t)*$/o}$logfile->getChatlog
		];

	$singleton=bless$self,$class;
    }
    sub Chatlog::getInstance{$singleton||Chatlog->new;}

    #ログを追加
    sub Chatlog::add{
	my$self=ref($_[0])?$_[0]:getInstance();shift;
	my%DT=%{shift()};
	%DT=map{$_=>$DT{$_}}grep{$DT{$_}}qw(Mar1 id name color bcolo body icon home email exp hua ra time opt);
	splice(@{$self},$::CF{'max'}-1);
	unshift(@{$self},\%DT);
    }

    #ログを削除
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
	$singleton&&die 'これはSingletonなのでnewを勝手に呼ばないで！getInstanceを使うこと';
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

    #参加者を取得
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

    #引数の人を追加
    sub Members::add{
	my$self=ref($_[0])?$_[0]:getInstance();shift;
	my%DT=%{shift()};
	if($DT{'quit'}){
	    #退室モード
	    delete$singleton->{$DT{'id'}}if$DT{'id'};
	    $singleton->{"$DT{'ra'}"}={id=>$DT{'ra'},(map{$_=>$DT{$_}}qw(reload ra time hua))};
	}elsif($DT{'name'}){
	    delete$singleton->{"$DT{'ra'}"};
	    if($DT{'isActive'}){
		#能動的リロード
		$DT{'lastModified'}=$^T;
	    }else{
		#普通にリロード
		$DT{'lastModified'}=$singleton->{"$DT{'id'}"}->{'lastModified'};
		if(!$DT{'reload'}||$^T-$DT{'lastModified'}<300){}
		elsif($DT{'reload'}<280){$DT{'reload'}+=20}
		else{$DT{'reload'}=300;}
	    }
	    $singleton->{"$DT{'id'}"}={map{$_=>$DT{$_}}qw(id name color bcolo exp reload ra time lastModified hua)};
	}else{
	    #ろむ
	    $singleton->{"$DT{'ra'}"}={id=>$DT{'ra'},(map{$_=>$DT{$_}}qw(reload ra time hua))};
	    $DT{'reload'}+=20;
	}
	return$DT{'reload'};
    }

    #読み込み専用ハッシュを返す
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
	$singleton&&die 'これはSingletonなのでnewを勝手に呼ばないで！getInstanceを使うこと';
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
	truncate($path,0);#$fhじゃダメ
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

    #経験値を+1
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
    #ログを削除
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
# 初期設定
#
BEGIN{
    #エラーが出たらエラー画面を表示するように
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
