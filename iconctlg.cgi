#------------------------------------------------------------------------------#
# 'iconCatalog' iconCatalog for MireilleIconList0.x
# - Mireille/Marldia Icon Catalog Module -
#
$CF{'iconCatalog'}=qq$Revision$;
# "This file is written in utf-8, CRLF." 空
# Scripted by NARUSE Yui.
#------------------------------------------------------------------------------#
# $rcsid = q$Id$;
require 5.005;
#use strict;
#use vars qw(%CF %IN %CK);

=head1 NAME

iconCatalog - Show Icon Catalog with MireilleIconList0.x

=head1 SYNOPSIS

適当に設定して設置してリンクを張ればよい

C< E<lt>A href="iconctlg.cgi"E<gt>アイコン一覧E<lt>/AE<gt> >
iconctlg.cgiが適切に設定されていれば、アイコン一覧が表示されるハズ。

=head1 DESCRIPTION

Mireilleの管理CGI内のアイコン見本生成部分を切り出したもので、
Mireilleからインポートしても使えるし、単独でも使えます。

旧来のicon.htmlは全てのアイコンを一画面に表示するため、
大量のアイコンを登録した状態では暴力的な存在となっていましたが、
ページ分割機能を搭載したため、そんなこともなくなりました。

=head1 CODES

=cut

&main;

sub main{
	if($CF{'program'}eq __FILE__){
		#直接実行のとき
		$CF{'iconList'}='icon.txt';
		$CF{'iconDir'}=	'/icon/full/';
		$CF{'name'}=	'Airemix';
		$CF{'home'}=	'http://www.airemix.com/';
		$CF{'index'}=	'index.cgi';
		$CF{'pgtitle'}=	'Airemix Icon Catalog System';
		$CF{'style'}=	'style.css';
		$CF{'menu'}='';

#-----------------------------
# Page Header
$CF{'pghead'}=<<"_CONFIG_";
<DIV class="center"><TABLE align="center" border="0" cellspacing="0" class="head" summary="PageHeader" width="90%"><TR>
<TH width="100%"><H1 class="head" align="left">$CF{'pgtitle'}</H1></TH>
<TD nowrap>■■■■■■■</TD>
</TR></TABLE></DIV>
_CONFIG_

#-----------------------------
# Page Footer
$CF{'pgfoot'}=<<"_CONFIG_";
<DIV class="center"><TABLE align="center" border="0" cellspacing="0" class="head" summary="PageFooter" width="90%"><TR>
<TD nowrap>■■■■■■■</TD>
<TH width="100%"><H1 class="head" align="right"><A href="$CF{'index'}">BACK to INDEX</A></H1></TH>
</TR></TABLE></DIV>
_CONFIG_

		$CF{'bodyHead'}='';
		$CF{'bodyFoot'}='';
		$CF{'iched'}='';
		$CF{'icfot'}='';
		&getParam;
		if(!$IN{'mode'}){
		}elsif('convert'eq$IN{'mode'}){
			my$iconlist;
			#単一アイコンリスト読み込み
			open(RD,'<'.$CF{'iconList'})||die"Can't open single-iconlist($CF{'iconList'})[$?:$!]";
			eval{flock(RD,1)};
			read(RD,$iconlist,-s$CF{'iconList'});
			close(RD);
			print scalar&generateEalis3qw(&parseMir0x($iconlist));
			exit;
		}
		&iconctlg;
	}else{
		#プログラムごとの揺らぎを調整
		$CF{'menu'}||='';
		$CF{'bodyHead'}||='';
		$CF{'bodyFoot'}||='';
		$CF{'iconList'}||=$CF{'icls'}||'';
		$CF{'iconDir'}||=$CF{'icon'}||$CF{'icondir'}||'';
		defined$IN{'page'}||($IN{'page'}=1);
	}
}


#-------------------------------------------------
# アイコン見本
#
sub iconctlg{

=head2 iconctlg

アイコン見本の生成を行いHTMLとしてCGI経由で出力する

=over 4

=cut

	my@others=();
	my%CR;
	my@icon=();

	#アイコンリスト読み込み
	my$iconlist='';
	if($CF{'iconList'}=~/^ /o){
		#複数アイコンリスト読み込み
		for($CF{'iconList'}=~/("[^"\\]*(?:\\.[^"\\]*)*"|\S+)/go){
			$_||next;
			my$tmp;
			open(RD,'<'.$_)||die"Can't open multi-iconlist($_)[$?:$!]";
			eval{flock(RD,1)};
			read(RD,$tmp,-s$_);
			close(RD);
			$iconlist.=$tmp;
		}
	}else{
		#単一アイコンリスト読み込み
		open(RD,'<'.$CF{'iconList'})||die"Can't open single-iconlist($CF{'iconList'})[$?:$!]";
		eval{flock(RD,1)};
		read(RD,$iconlist,-s$CF{'iconList'});
		close(RD);
	}
	
	my@pages=$iconlist=~/<!--\s*(%PAGE-BREAK(?:\s+.*?)?)\s*-->/go;
	my$pages=@pages+1;
	
	#$IN{'page'}が上に超えると全頁を一括表示する
	$IN{'page'}>$pages&&($IN{'page'}=0);
	
	my$page=1; #今何ページ目？
	my$j=0; #今何桁目？
	my$cols=6; #6桁で改行
	my$table=''; #optgroup一つをこれに一時的に格納する
	for(&parseMir0x($iconlist)){
		my%DT=%{$_};
		#コマンド分岐
		if('TAG'eq$DT{'cmd'}){
			$IN{'page'} > 0 && $page != $IN{'page'} && next;
			#$IN{'page'}==0か$page==$IN{'page'}の時のみこれより下を実行
			if($IN{'page'} >= 0 && 'OPTION'eq$DT{'swt'}){
				if(!$j){
					#others
					push(@others,qq(<TD><IMG src="$CF{'iconDir'}$DT{'value'}" onclick="changeIcon(this.title)")
						 .qq( alt="" title="$CF{'iconDir'} + $DT{'value'}")
						 .qq( style="cursor:hand;"><BR>$DT{'label'}</TD>\n));
				}else{
					$table.=qq(<TD><IMG src="$CF{'iconDir'}$DT{'value'}" onclick="changeIcon(this.title)")
						.qq( alt="" title="$CF{'iconDir'} + $DT{'value'}")
						.qq( style="cursor:hand;"><BR>$DT{'label'}</TD>\n);
					if($j<$cols){
						#グループ内1-5桁
						$j++;
					}else{
						#グループ内6桁目：改行
						$table.="</TR>\n<TR>\n";
						$j=1;
					}
				}
			}elsif('OPTGROUP'eq$DT{'swt'}){
				if($IN{'page'} >= 0){
				$table=<<"_HTML_";
<TABLE cellspacing="0" class="icon" summary="$DT{'label'}">
<CAPTION><a name="$DT{'label'}">$DT{'label'}</a></CAPTION>
<COL span="$cols" width="110">
<TR>
_HTML_
				}else{
					push(@icon,qq(<li><a href="index.cgi?icct;page=$page#$DT{'label'}">$DT{'label'}</a></li>\n));
				}
				$j=1;
			}elsif('/OPTGROUP'eq$DT{'swt'}){
				if($IN{'page'} >= 0){
					for(keys%CR){
						if($CR{$_}{'LINK'}){
						}elsif($CR{$_}{'NAME'}&&$CR{$_}{'URL'}){
							$CR{$_}{'LINK'}=qq(<A href="$CR{$_}{'URL'}" title=")
								.(('VENDOR'eq$_)?'製作者':'一次著作権者').qq(">$CR{$_}{'NAME'}</A>);
						}elsif($CR{$_}{'NAME'}){
							$CR{$_}{'LINK'}=$CR{$_}{'NAME'};
						}elsif($CR{$_}{'URL'}){
							$CR{$_}{'LINK'}=qq(<A href="$CR{$_}{'URL'}" title=")
								.(('VENDOR'eq$_)?'製作者':'一次著作権者').qq(">$CR{$_}{'URL'}</A>);
						}
					}
				
					my$copy='';
					if($CR{'VENDOR'}{'LINK'}&&$CR{'COPY1'}{'LINK'}){
						$copy="&#169;$CR{'COPY1'}{'LINK'} &gt;&gt; by$CR{'VENDOR'}{'LINK'}";
					}elsif($CR{'VENDOR'}{'LINK'}){
						$copy="by$CR{'VENDOR'}{'LINK'}";
					}elsif($CR{'COPY1'}{'LINK'}){
						$copy="&#169;$CR{'COPY1'}{'LINK'}";
					}
					$table.=($j>1?"</TR>\n<TR>\n":'').<<"_HTML_";
<TH colspan="$cols" class="foot">$copy</TH>
</TR>
</TABLE>

_HTML_
					push(@icon,$table);
				}
				$j=0;
			}
		}elsif('PAGE-BREAK'eq$DT{'cmd'}){
			#改ページ処理を。
			$page++==$IN{'page'}&& last;
		}elsif('COPY'eq$DT{'cmd'}){
			if('BEGIN'eq$DT{'swt'}){
				undef$CR{$DT{'type'}};
			}elsif('END'eq$DT{'swt'}){
				undef$CR{$DT{'type'}};
			}elsif('SET'eq$DT{'swt'}){
				$CR{$DT{'type'}}{$DT{'key'}}=$DT{'value'};
			}
		}
		#next;
	}

=item 最後のoptgroupが閉じられていない場合

きちんと閉じておく。

=cut

	if($j){
		my$copy='';
		if($CR{'VENDOR'}{'LINK'}&&$CR{'COPY1'}{'LINK'}){
			$copy="&#169;$CR{'COPY1'}{'LINK'} &gt;&gt; by$CR{'VENDOR'}{'LINK'}";
		}elsif($CR{'VENDOR'}{'LINK'}){
			$copy="by$CR{'VENDOR'}{'LINK'}";
		}elsif($CR{'COPY1'}{'LINK'}){
			$copy="&#169;$CR{'COPY1'}{'LINK'}";
		}
		$table.=($j>1?"</TR>\n<TR>\n":'').<<"_HTML_";
<TH colspan="$cols" class="foot">$copy</TH>
</TR>
</TABLE>

_HTML_
		push(@icon,$table);
	}

=item 分類：その他、の処理

OPTGROUPの子要素でないOPTIONは全て、分類：その他(Others)とする

=cut

	if($#others>-1){
		my$j=0;
		$table=<<"_HTML_";
<TABLE cellspacing="0" class="icon" summary="Others">
<CAPTION>その他</CAPTION>
<COL span="$cols" width="110">
<TR>
@{[map{if(++$j>6){$j=0;"</TR><TR>$_"}else{$_}}@others]}
</TR>
</TABLE>

_HTML_
		push(@icon,$table);
	}
	undef$table;
	if($IN{'page'} < 0){
		@icon = map{$$_[1]}sort{$$a[0]cmp$$b[0]}map{/>([^<]+)<\/a>/;[$1,$_]}@icon;
		unshift(@icon, qq!<ul style="line-height:1.5em">!);
		push(@icon, qq!</ul>!);
	}
	
	#-----------------------------
	# HTML出力

=item HTML出力

HTML-META-Last-Modifiedも出力しておく
WWWCでチェックしような人がいないとは限らないので

=cut

	my$encoding='utf-8';
	my$status=sprintf(qq(<META http-equiv="Last-Modified" content="%s, %02d %s %s %s GMT">\n)
	,(split(/\s+/o,gmtime((stat$CF{'iconList'})[9])))[0,2,1,4,3]);
	my$pgslct=$pages-1?&pgslct($pages,'icct'):'';
	my$html=<<"_HTML_";
Content-Language: ja-JP
Content-type: text/html; charset=$encoding

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<!--DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"-->
<HTML lang="ja-JP">
<HEAD>
<META http-equiv="Content-type" content="text/html; charset=$encoding">
<META http-equiv="Content-Script-Type" content="text/javascript">
<META http-equiv="Content-Style-Type" content="text/css">
<LINK rel="stylesheet" type="text/css" href="$CF{'style'}" media="screen" title="DefaultStyle">
<LINK rel="start" href="$CF{'home'}">
<LINK rel="index" href="index.cgi">
<TITLE>: Icon Catalog :</TITLE>
<SCRIPT type="text/javascript">
<!--
function changeIcon(title){
  var array = title.split(' ');
  var value = array[ array.length-1 ];
  var iconSelector = parent.north.document.getElementById('icon');
  if(!iconSelector)return false;
  var options = iconSelector.options;
  var length = options.length
  for( var i = 0; i < length; i++){
    if(options[i].value == value){
      iconSelector.selectedIndex = i;
      iconSelector.onchange();
      break;
    }
  }
  return false;
}
//-->
</SCRIPT>
</HEAD>
<BODY style="margin-top:1em">
$CF{'bodyHead'}
$CF{'pghead'}
$CF{'menu'}
<H2 class="mode">アイコンカタログ</H2>
$CF{'iched'}
$pgslct
@icon
$pgslct
$CF{'icfot'}
$CF{'menu'}
$CF{'pgfoot'}
<DIV class="AiremixCopy">- <A href="http://www.airemix.com/" target="_blank"
 title=": Airemix :">Airemix iconCatalog</A>
<VAR title="times:@{[times]}">$CF{'iconCatalog'}</VAR> -</DIV>
$CF{'bodyFoot'}
</BODY>
</HTML>
_HTML_
    print $html;
    exit;

=back

=cut

}



#-------------------------------------------------
# ページ選択TABLE
#
sub pgslct{

=head2 pgslct

PageSelect

=over 4

=item Description

this is based on Mireille::pgslct 1.2.3.4
これを呼び出すとMireille::pgslctは上書きされることに注意すること

=item 引数

$ ページ数
;
$ モードの保持(rvs,del,icct)

=cut

	my$pages=shift();
	my$mode=$_[0]?"$_[0];page=":'page=';
	my@key=map{qq( accesskey="$_")}('0','!','&#34;','#','$','%','&#38;','&#39;','(',')');#1-9ページのAccessKey

	#配列へ
	my@page=map{$_==$IN{'page'}?qq(<STRONG class="pgsl">$_</STRONG>)
	:qq(<A href="index.cgi?$mode$_").($key[$_]?$key[$_]:'').">$_</A>\n"}(1..$pages);
	unshift(@page,qq(<A href="index.cgi?$mode-1">グループリスト</A>\n));

	#いざ出力
	return<<"_HTML_";
<TABLE align="center" cellspacing="0" class="pgsl" summary="PageSelect" border="1">
<COL style="width:3.5em">
<COL>
<COL style="width:3.5em">
<TR>
<TD>@{[$IN{'page'}<2?'[最先]'
:qq(<A accesskey="," href="index.cgi?$mode@{[$IN{'page'}-1]}">&#60; 前の</A>)]}</TD>
<TD>[ @page ]</TD>
<TD>@{[!($IN{'page'}*($IN{'page'}-$pages))?'[最後]'
:qq(<A accesskey="." href="index.cgi?$mode@{[$IN{'page'}+1]}">次の &#62;</A>)]}</TD>
</TR>
</TABLE>
_HTML_
	#最先（いささき）と最後（いさはて）なのさ（謎

=back

=cut

}


#-------------------------------------------------
# 引数を取得して汚染除去
#
sub getParam{
	my$modifiedFile=$CF{'iconList'};
	my@param=();
	
	#引数取得
	unless($ENV{'REQUEST_METHOD'}){
		@param=@ARGV;
	}elsif('HEAD'eq$ENV{'REQUEST_METHOD'}){ #forWWWD
		#MethodがHEADならばLastModifedを出力して、
		#最後の更新時刻を知らせる
		print 'Last-Modified: '
		.sprintf("%s, %02d %s %s %s GMT",(split(/\s+/o,gmtime((stat$modifiedFile)[9])))[0,2,1,4,3])
		."\nContent-Type: text/plain\n\n";
		exit;
	}else{
		my$i='';
		if('POST'eq$ENV{'REQUEST_METHOD'}){
			read(STDIN,$i,$ENV{'CONTENT_LENGTH'});
		}elsif('GET'eq$ENV{'REQUEST_METHOD'}){
			$i=$ENV{'QUERY_STRING'};
		}
		
		if(length$i>262114){ # 262114:引数サイズの上限(byte)
			die"いくらなんでも量が多すぎます\n$i";
		}elsif(length$i>0){
			@param=split(/[&;]/o,$i); #入力を展開してハッシュに
		}
	}
	
	# EUC-JP文字
	my$eucchar=qr((?:
		[\x09\x0A\x0D\x20-\x7E]			# 1バイト EUC-JP文字改
		|(?:[\x8E\xA1-\xFE][\xA1-\xFE])	# 2バイト EUC-JP文字
		|(?:\x8F[\xA1-\xFE]{2})			# 3バイト EUC-JP文字
	))x;
	
	my%DT;
	while(@param){
		my($i,$j)=split('=',shift(@param),2);
		defined$j||($DT{$i}='',next);
		$i=($i=~/(\w+)/o)?"$1":'';
		study$j;
		$j=~tr/+/\ /;
		$j=~s/%([\dA-Fa-f]{2})/pack('H2',$1)/ego;
		$j=($j=~/($eucchar*)/o)?"$1":'';
		#メインフレームの改行は\x85らしいけど、対応する必要ないよね？
		$j=~s/\x0D\x0A/\n/go;$j=~tr/\r/\n/;
		$DT{$i}=$j;
	}
	%IN=%{&filteringParams(\%DT)}
}
sub filteringParams{
	my%OLD=%{shift()};
	my%NEW;
	$NEW{'page'}=($OLD{'page'}&&(int$OLD{'page'})=~/-1|(\d+)/o)?$1:1;
	$NEW{'mode'}=$1 if($OLD{'mode'}&&$OLD{'mode'}=~/(\w*)/o);
	return\%NEW
}

#------------------------------------------------------------------------------#
# List Parsers and Generators
#

#-------------------------------------------------
# Mireille0.x Parser and Generator
#

=head2 Mireille0.x形式アイコンリストの解析と生成

Mireille0.x形式は主にMireilleやMarldiaで用いられるアイコンリスト形式で、
少ない処理でHTMLに書き出すために、もとからHTMLの断片として作られたリスト形式である。
HTML断片という性格から幅広い拡張性を持つが、ともすれば煩雑になりやすい。
そのため、正規表現が実装されていない言語でこのリスト形式を扱うのは難しいと思われる。

=over 4

=cut

sub parseMir0x{
	my$iconlist=shift;
	my@events;
	while($iconlist=~/(.+)/go){
		$_=$1;
		if(/<!--\s*%(\S+)\s+(.*)-->/o){
			#何かしらのコマンド
			my$command=$1;
			my$param=$2;$param=~s/\s+$//o;
			if('PAGE-BREAK'eq$command){
				#改ページ処理
				push(@events,{cmd=>'PAGE-BREAK'});
			}elsif($command=~/([A-Z]+)(_[A-Z]+)*/o){
				#著作権表示機構

=item MireilleIconListCommand

 イベント：アイコンリストの命令を発見した
 現在存在する命令の形式は以下のよう
cmd:    : 'COPY'
swt:  $1: 'BEGIN','END','SET'
type: $2: 'VENDOR','COPY1'
key:  $3: 'NAME','URL','LINK'
value:$4: 命令の引数

=cut

				my@cmds=split('_',$command);
				if('SET'eq$cmds[0]||'VENDOR'eq$cmds[0]||'COPY1'eq$cmds[0]){
					'SET'eq$cmds[0]&& shift@cmds;
					push(@events,{cmd=>'COPY',swt=>'SET',type=>$cmds[0],key=>$cmds[1],value=>$param});
				}elsif('BEGIN'eq$cmds[0]){
					push(@events,{cmd=>'COPY',swt=>'BEGIN',type=>$cmds[1]});
					push(@events,{cmd=>'COPY',swt=>'SET',type=>$cmds[1],key=>'NAME',value=>$param})if$param;
				}elsif('END'eq$cmds[0]){
					push(@events,{cmd=>'COPY',swt=>'END',type=>$cmds[1]});
				}
			}
			next
		}
		
		if(/^\s*<OPTION ([^>]*)\bvalue=(["'])(.+?)\2([^>]*)>([^<]*)(<\/OPTION>)?/io){

=item OPTION要素

 /^\s*<OPTION (.*)value=(["'])(.+?)\2([^>]*)>([^<]*)(<\/OPTION>)?/io
 <TD><IMG $1src="$CF{'iconDir'}$3" alt="$5"$4><BR>$5</TD>\n
 イベント：一つのアイコンを発見
cmd: TAG
swt: OPTION
label: $3: OPTION要素の内容 または label属性の値
value: $5: value属性の値

=cut

			push(@events,{cmd=>'TAG',swt=>'OPTION',value=>$3,label=>$5});
		}elsif(/^<OPTGROUP ([^>]*)\blabel=(["'])(.+?)\2(.*)>/io){

=item OPTGOUP要素始

 ^<OPTGROUP (.*)label=(["'])(.+?)\2(.*)>$
 <TABLE $1summary="$2"$3>
 イベント：OPTGROUP内に入った
cmd: TAG
swt: OPTGROUP
label: $3: label属性の値

=cut

			push(@events,{cmd=>'TAG',swt=>'OPTGROUP',label=>$3});
		}elsif(/<\/OPTGROUP>/io){#</OPTGROUP>

=item OPTGOUP要素終

 /OPTGROUP/io
 イベント：OPTGROUP外に出た
cmd: TAG
swt: /OPTGROUP

=cut

			push(@events,{cmd=>'TAG',swt=>'/OPTGROUP'});
		}
		next;
	}

=back

=cut

	return@events;
}
sub generateMir0x{
	my@list;
	for(@_){
		my%DT=%{$_};
		if(!$DT{'cmd'}||'TAG'eq$DT{'cmd'}){
			if('OPTION'eq$DT{'swt'}){
				push(@list,qq(<OPTION value="$DT{'value'}">$DT{'label'}</OPTION>));
			}elsif('OPTGROUP'eq$DT{'swt'}){
				push(@list,qq(<OPTGROUP label="$DT{'label'}">));
			}elsif('/OPTGROUP'eq$DT{'swt'}){
				push(@list,qq(</OPTGROUP>));
			}
		}elsif('PAGE-BREAK'eq$DT{'cmd'}){
			push(@list,qq(<!-- %PAGE-BREAK -->));
		}elsif('COPY'eq$DT{'cmd'}){
			if('BEGIN'eq$DT{'swt'}){
				push(@list,qq(<!-- %BEGIN_$DT{'type'} $DT{'value'} -->));
			}elsif('END'eq$DT{'swt'}){
				push(@list,qq(<!-- %SET_$DT{'type'}_$DT{'key'} $DT{'value'} -->));
			}elsif('SET'eq$DT{'swt'}){
				push(@list,qq(<!-- %END_$DT{'type'} -->));
			}
		}
		#next;
	}
	return wantarray?@list:join("\n",map{m/^<OPTION/?"\t$_":$_}@list);
}

#-------------------------------------------------
# ealis3qw[] Parser and Generator
#

=head2 ealis3qw[]形式アイコンリストの解析と生成

ealis3で用いられるqw[]形式アイコンリストの解析と生成を行う。
URLに用いることができない文字である`*'と空白を効果的に用いたリスト形式。
単純な分手で書くときに楽。
Perlのクォート風演算子qwに依存しているが、他の言語でもsplit(/\s+/)すればOKかも。

=cut

sub parseEalis3qw{
	my@icons=$#_?@_:shift=~/(\S+)\s+(\S[^\x0a\x0d]*)/go;
	my@events;
	my$isGroup=0;
	for(0..($#icons-1)/2){
		my$value=$icons[$_*2];
		my$label=$icons[$_*2+1];
		if('**'eq$value){
			$isGroup&& push(@events,{cmd=>'TAG',swt=>'/OPTGROUP'});
			if($value){
				push(@events,{cmd=>'TAG',swt=>'OPTGROUP',label=>$label});
				$isGroup=1;
			}else{
				$isGroup=0;
			}
		}else{
			push(@events,{cmd=>'TAG',swt=>'OPTION',label=>,$label,value=>$value});
		}
		next;
	}
	
	$isGroup&& push(@events,{cmd=>'TAG',swt=>'/OPTGROUP'});
	return@events;
}
sub generateEalis3qw{
	my@list;
	my$max=1;
	my$isGroup=-1;
	for(@_){
		my%DT=%{$_};
		if(!$DT{'cmd'}||'TAG'eq$DT{'cmd'}){
			if('OPTION'eq$DT{'swt'}){
				$max=length$DT{'value'}if$max<length$DT{'value'};
				if(!$isGroup){push(@list,'**','');$isGroup=1;}#無名グループ
				push(@list,$DT{'value'},$DT{'label'});
			}elsif('OPTGROUP'eq$DT{'swt'}){
				push(@list,'**',$DT{'label'});
				$isGroup=1;#グループ内
			}elsif('/OPTGROUP'eq$DT{'swt'}){
				$isGroup=0;#グループはでたけれど
			}
#		}elsif('PAGE-BREAK'eq$DT{'cmd'}){
#			
#		}elsif('COPY'eq$DT{'cmd'}){
#			if('BEGIN'eq$DT{'swt'}){
#				
#			}elsif('END'eq$DT{'swt'}){
#				
#			}elsif('SET'eq$DT{'swt'}){
#				
#			}
		}
		#next;
	}
	return wantarray?@list:join('',
	map{sprintf("\t%-${max}s\t%s\n",$list[$_*2],$list[$_*2+1])}(0..($#list-1)/2));
}


#------------------------------------------------------------------------------#
# jcode.pl: Perl library for Japanese character code conversion
# Copyright (c) 1992-2000 Kazumasa Utashiro <utashiro@iij.ad.jp>
# http://www.srekcah.org/jcode/
sub euc2sjis{
	my$s=$_[0];
	$s=~s<([\xa1-\xfe]{2}|\x8e[\xa1-\xdf]|\x8f[\xa1-\xfe]{2})>
	[
		my($c1,$c2)=unpack('CC',$1);
		if($c1==0x8e){#SS2
			substr($1,1,1);
		}elsif($c1==0x8f){#SS3
			"\x81\xac";
		}elsif($c1 % 2){
			pack('CC',($c1>>1)+($c1<0xdf?0x31:0x71),$c2-0x60-($c2<0xe0));
		}else{
			pack('CC',($c1>>1)+($c1<0xdf?0x30:0x70),$c2-2);
		}
	]ego;
	return$s;
}



#-------------------------------------------------
# 初期設定
#
BEGIN{
	# Mireille Error Screen 1.4
	unless(%CF){
		$CF{'program'}=__FILE__;
		$SIG{'__DIE__'}=sub{
			if($_[0]=~/^(?=.*?flock)(?=.*?unimplemented)/){return}
			print"Content-Language: ja-JP\nContent-type: text/plain; charset=utf-8\n"
			."\n\n<PRE>\t:: Mireille ::\n   * Error Screen 1.4 (o__)o// *\n\n";
			print"ERROR: $_[0]\n"if@_;
			print join('',map{"$_\t: $CF{$_}\n"}grep{$CF{"$_"}}qw(Icon))
			."\n".join('',map{"$_\t: $CF{$_}\n"}grep{$CF{"$_"}}qw(icon icls style));
			print"\ngetlogin\t: ".getlogin;
			print"\n".join('',map{"$$_[0]\t: $$_[1]\n"}
			([PerlVer=>$]],[PerlPath=>$^X],[BaseTime=>$^T],[OSName=>$^O],[FileName=>$0],[__FILE__=>__FILE__]))
			."\n\t= = = ENV = = =\n".join('',map{sprintf"%-20.20s : %s\n",$_,$ENV{$_}}grep{$ENV{"$_"}}
			qw(CONTENT_LENGTH QUERY_STRING REQUEST_METHOD
			SERVER_NAME HTTP_HOST SCRIPT_NAME OS SERVER_SOFTWARE PROCESSOR_IDENTIFIER))
			."\n+#      Airemix Mireille     #+\n+#  http://www.airemix.com/  #+";
			exit;
		};
	}
	# Revision Number
	$CF{'iconCatalog'}=qq$Revision$;
	$CF{'Exte'}.=qq(icon:\t$CF{'iconCatalog'}\n);
}

1;
__END__

=head1 BUGS

確認しているバグがあったらとっくに直しています

=head1 RESTRICTIONS

存在しません
万が一あったとすればそれはバグです

=head1 NOTES

=over 4


=item Comments

これのコメントは使い方の説明やメソッドの説明、と言うよりも、
改造する際の指針のためにつけられています。
もしあなたの環境がB<UNIX>でB<Perl>が入っているのなら、
S<pod2text iconctlg.cgi>
また、B<Windows>でB<Perl>とB<Jcode.pm>が入っているのなら、
S<perl -e"use Jcode;print Jcode::convert(scalar`pod2text iconctlg.cgi`,'sjis','euc')">
もしくは、B<Perl>とB<nkf32.exe>が入っているのなら、
S<pod2text iconctlg.cgi|nkf32 -sE>
などとすればWindowsでも文字化けすることなくPODドキュメントを読め、
このCGIの内部構造が丸わかりっ☆のハズ（ｗ

=item Commands of MireilleIconlist

I<%PAGE-BREAK>命令は実験的な実装です。
正式版までに確実に、何か別の命令に取って代わられると思われます

もともとI<PAGE-BREAK>は、
CSSのI<page-break-after>を意識してつけたのですが、
これでは当然改ページとして入力することになります
しかし、ページごとに異なるページ名をつけようと思うと、
そのページ名を指定するためのキーワードとして、
I<PAGE-BREAK>を使うのは違和感があります。
むしろI<PAGE-START>とかではないか、と。
そのような理由でI<PAGE-BREAK>命令は実験的なものとしています。

もっといい命令名が思いついたらそちらに変える予定です。

=back

=head1 COPYRIGHT

当分はB<Mireille>の一部として配布し、B<MireilleLicense>に順ずるものとします。
将来的に修正BSDライセンスやGPLのような、
より一般的なライセンスを導入することを検討しています。

B<ealis3qw>形式は神乃さんによるB<ealis>で用いられる形式です
http://kano.feena.jp/erial/

=head1 AVAILABILITY

B<Airemix> http://www.airemix.com/

=head1 SEE ALSO

B<Mireille>のヘルプも見てください

=head1 AUTHOR

NARUSE Yui naruse@airemix.com

=cut
