#!/usr/local/bin/perl

#------------------------------------------------------------------------------#
# 'Marldia' Chat System
# - Main Script -
#
# $Revision: 1.7 $
# "This file is written in euc-jp, CRLF." ��
# Scripted by NARUSE Yui.
#------------------------------------------------------------------------------#
# $cvsid = q$Id: core.cgi,v 1.7 2002-05-04 18:10:30 naruse Exp $;
require 5.004;
#use lib './lib';
use Fcntl qw(:DEFAULT :flock);
use strict;
use vars qw(%CF %IN %CK %IC);
$|=1;

#-------------------------------------------------
# MAIN SWITCH
#
sub main{
  &getform;
  (" $IN{'name'} "=~m/ $CF{'denyname'} /o)&&(&locate($CF{'sitehome'}));
#  (" $ENV{'REMOT_ADDR'} "=~m/ $CF{'denyra'} /o)&&(&locate($CF{'sitehome'}));
#  (" $ENV{'REMOT_HOST'} "=~m/ $CF{'denyrh'} /o)&&(&locate($CF{'sitehome'}));
  
  if('south'eq$IN{'mode'}){
  }elsif('frame'eq$IN{'mode'}){
    &frame;
  }elsif('north'eq$IN{'mode'}){
    &north;
  }elsif('manage'eq$IN{'mode'}){
    &manage;
  }
  &south;
  exit;
}


#------------------------------------------------------------------------------#
# MARD ROUTINS
#
# mainľ���Υ��֥롼����

#-------------------------------------------------
# Frame
#
sub frame{
  print<<"_HTML_";
Content-type: text/html; charset=euc-jp
Content-Language: ja

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN""http://www.w3.org/TR/html4/frameset.dtd">
<html lang="ja">
<head>
<meta http-equiv="Content-type" content="text/html; charset=euc-jp">
<meta http-equiv="Content-Script-Type" content="text/javascript">
<meta http-equiv="Content-Style-Type" content="text/css">
<link rel="start" href="$CF{'sitehome'}">
<link rel="index" href="$CF{'index'}">
<link rel="help" href="$CF{'help'}">
<title>$CF{'title'}</title>
</head>
<frameset rows="120,*">
  <frame frameborder="0" name="north" src="index.cgi?north">
  <frame frameborder="0" name="south" src="index.cgi?south">
  <noframes>
  <pre>
  ���Υڡ�����Microsoft Internet Explorer 6.0 �����˺���Ƥ��ޤ�
  MSIE5.01��Netscape6��Mozilla0.9�ʾ�Ǥ⤽�������˸��뤳�Ȥ������Ȼפ��ޤ�
  Netscape4.x�Ǥ�ɽ���ΰ�����������ǽ��������ޤ�
  �ơ��֥��ե졼����б����Ƥ��ʤ��֥饦���Ǥϡ�ɽ��������ʬ������Ƥ��ޤ����ᡢ
  �¼�Ū�˱������뤳�Ȥ��Ǥ��ޤ���
  Mozilla4�ʾ�ߴ��Υ֥饦���Ǥޤ���Ƥ�������
  </pre>
  </noframes>
</frameset>
_HTML_
  exit;
}


#-------------------------------------------------
# North
#
sub north{
  &getck;
  (%CK)||(%CK=%IN);
  &header;
  &iptico($CK{'icon'},'tabindex="12"');
  print<<'_HTML_';
<script type="text/javascript" defer>
<!--
//--------------------------------------
// �����
window.onload=autoreset;
var cook,body,preview,surface;
_HTML_
  print qq(var icondir='$CF{'icondir'}';\n);
  print<<'_HTML_';
function autoreset(){
  if(document.all){
    cook=document.all('cook');
    body=document.all('body');
    preview=document.all('Preview');
    surface=document.all('surface');
  }else if(document.getElementById){
    cook=document.getElementById('cook');
    body=document.getElementById('body');
    preview=document.getElementById('Preview');
    surface=document.getElementById('surface');
  }else{return}

  if(cook){
    cook.checked=(document.cookie)?false:true;
  }
  if(body){
    body.value="";
    body.focus();
  }
}

//--------------------------------------
// ��������ץ�ӥ塼
function iconPreview(arg){
  if(!preview&&!arg){return;}
  arg=icondir+arg;
  preview.src=arg;
}

//--------------------------------------
// ����������Ѥ�����
function iconChange(arg){
  if(!surface&&!arg){return;}
  iconPreview(arg);
  if(!arg.match(/^(([^\/#]*\/)*([^\/#.]*\.)*[^\/#.]+)(\.[^\/#.]*)#(\d+)$/)){
    surface.length=1;
    surface.options[0].text='-';
    surface.options[0].value=arg;
    return;
  }
  var url=RegExp.$1;
  var ext=RegExp.$4;
  var len=parseInt(RegExp.$5)+1;
  surface.length=len+1;
  surface.options[0].text='-';
  surface.options[0].value=url+ext;
  for(i=0;i<len;i++){
    surface.options[i+1].text=i;
    surface.options[i+1].value=url+i+ext;
  }
}


//--------------------------------------
// ɽ�𥢥�������
function surfaceSample(){
  if(!window.createPopup){return;}
  var popup=window.createPopup();
  var wid=200;
  var hei=250;
  var str=
    '<button type="button" id="surface0" style="margin:0;padding:0;width:50px"'
    +' onclick="top.north.document.all(\'surface\').selectedIndex=0;document.all(\'surfaceS\').selectedIndex=0'
    +';top.north.document.all(\'preview\').src=\''+icondir+surface.options[0].value+'\'">'
    +'<img src="'+icondir+surface.options[0].value+'" alt="-"></button>';

  for(i=1;i<surface.length;i++){
    str+=
    '<button type="button" id="surface'+i+'" style="margin:0;padding:0;width:50px"'
    +' onclick="top.north.document.all(\'surface\').selectedIndex='+i+';document.all(\'surfaceS\').selectedIndex='+i
    +';top.north.document.all(\'preview\').src=\''+icondir+surface.options[i].value+'\'">'
    +'<img src="'+icondir+surface.options[i].value+'" alt="'+(i-1)+'"></button>';
    if(i%3==2){str+='<br>';}
  }
  popup.document.body.innerHTML=
   '<div style="border:3px outset ActiveBorder;height:'+hei+'px;overflow:auto;text-align:left;width:'+wid+'px">'
  +'<div style="color:CaptionText;font:caption;height:15px;padding:2px;width:100%;'
  +'filter:progid:DXImageTransform.Microsoft.Gradient(endColorstr=\'#ffffff\',startColorstr=\'ActiveCaption\','
  +'gradientType=\'1\');">����������</div>'+str+'<select name="surfaceS" id="surfaceS"'
  +'onchange="document.all(\'surface\'+this.selectedIndex).click()">'+surface.innerHTML+'</select>'
  +'</div>';
  popup.show(20,20,wid,hei,top.south.document.body);
  popup.document.body.document.all('surfaceS').focus();
  return;
}
_HTML_
  print<<"_HTML_";
//-->
</script>
<form name="north" id="north" method="post" action="index.cgi" target="south" onsubmit="setTimeout(autoreset,20)">
<table style="width:770px" summary="���׹���">
<col style="width:110px">
<col style="width:75px">
<col style="width:160px">
<col style="width:75px">
<col style="width:100px">
<col style="width:85px">
<col style="width:40px">
<col style="width:120px">
<col>
<tr>
<td rowspan="5" style="text-align:center">
<h1>$CF{'pgtit'}</h1>
<img name="Preview" id="Preview" alt="Preview" src="$CF{'icondir'}$CK{'icon'}" $CF{'imgatt'}
 onclick="surfaceSample()"><br>
<label accesskey="z" for="surface" title="hyoZyo\nɽ�𥢥���������򤷤ޤ��ʻȤ���С�"
><span class="ak">Z</span>yo</label><select name="surface" id="surface"
 onchange="iconPreview(this.options[this.selectedIndex].value)" tabindex="50">
_HTML_
  if($CK{'icon'}=~/^((?:[^\/#]*\/)*)((?:[^\/#.]*\.)*?[^\/#.]+)(\.[^\/#.]*)?#(\d+)$/o){
    print qq(<option value="$1$2$3">-</option>\n);
    for(0..$4){print qq(<option value="$1$2$_$3">$_</option>\n);}
  }else{
    print qq(<option value="$CK{'icon'}">-</option>\n);
  }
  print<<"_HTML_";
</select><be>
<div style="margin:0.3em 0;text-align:center" title="reloadQ\n��ե졼������ɤ��ޤ�"
>[<a href="$CF{'index'}?north" accesskey="q" tabindex="52"
>���ɹ�(<span class="ak">Q</span>)</a>]
</td>
<th><label accesskey="n" for="name" title="Name\n���ü�̾��ȯ����̾�ʤɤǻȤ�̾���Ǥ�"
>̾��(<span class="ak">N</span>)</label>:</th>
<td><input type="text" name="name" id="name" maxlength="20" size="20"
 style="ime-mode:active;width:100px" value="$CK{'name'}" tabindex="11"></td>
<th><label accesskey="c" for="color" title="name Color\n���ü�̾��ȯ����̾�ʤɤǻȤ�̾���ο��Ǥ�"
>̾����(<span class="ak">C</span>)</label>:</th>
<td>@{[&iptcol('color','tabindex="21"')]}</td>
<th><label accesskey="g" for="line" title="log Gyosu\nɽ��������ιԿ��Ǥ�\n�ǹ�$CF{'max'}��"
>���Կ�(<span class="ak">G</span>)</label>:</th>
<td><input type="text" name="line" id="line" maxlength="4" size="4"
 style="ime-mode:disabled;width:32px" value="$CK{'line'}��" tabindex="31"></td>
<td style="text-align:center"><input type="submit" accesskey="s" class="submit"
 title="Submit\n���ߤ����Ƥ�ȯ�����ޤ�" value="OK" tabindex="41"></td>
<td></td>
</tr>

<tr>
<th><label accesskey="i" for="icon" title="Icon\n���Ѥ��륢����������򤷤ޤ�"
>��������(<span class="ak">I</span>)</label>:</th>
<td>@{[&iptico($CK{'icon'},'tabindex="12"')]}</td>
<th><label accesskey="c" for="bcolo" title="body Color\nȯ��������ʸ�ο��Ǥ�"
>ʸ�Ͽ�(<span class="ak">C</span>)</label>:</th>
<td>@{[&iptcol('bcolo','tabindex="22"')]}</td>
<th><label accesskey="r" for="reload" title="Reload\n���ä��Ȥ˼�ưŪ�˥���ɤ��뤫���Ǥ�"
>�����ֳ�(<span class="ak">R</span>)</label>:</th>
<td><input type="text" name="reload" id="reload" maxlength="4" size="4"
 style="ime-mode:disabled;width:32px" value="$CK{'reload'}��" tabindex="32"></td>
<td style="text-align:center"><input type="reset" class="reset"
 title="reset\n���Ƥ��������ޤ�" value="����󥻥�" tabindex="42"></td>
</tr>

<tr>
<th><label accesskey="b" for="body" title="Body\nȯ��������ʸ�����ƤǤ�"
>����(<span class="ak">B</span>)</label>:</th>
<td colspan="5"><input type="text" name="body" id="body" maxlength="300" size="100"
 style="ime-mode:active;width:460px" tabindex="1"></td>
<td><label accesskey="k" for="cook" title="cooKie\n�����å��������ȸ��ߤ������Cookie����¸���ޤ�"
><input type="checkbox" name="cook" id="cook"
 class="check" tabindex="51" checked="checked">���å���¸(<span class="ak">K</span>)</label></td>
</tr>

<tr>
<th><label accesskey="y" for="id" title="identitY name\nCGI�����ǻ��Ѥ��롢�����Ѥ�̾�������򤷤ޤ�
����̾�����ºݤ�ɽ�˽Ф뤳�ȤϤ���ޤ���\n������Ͽ̾��Ʊ������Ʊ���ʪ���Ȥߤʤ���ޤ�"
>��Ͽ̾(<span class="ak">Y</span>)</label>:</th>
<td><input type="text" name="id" id="id" maxlength="20" size="20"
 style="ime-mode:active;width:150px" value="$CK{'id'}" tabindex="101"></td>
<th><label accesskey="l" for="email" title="e-maiL\n�᡼�륢�ɥ쥹�Ǥ�"
>E-mai<span class="ak">l</span></label>:</th>
<td colspan="3"><input type="text" name="email" id="email" maxlength="200" size="40"
 style="ime-mode:inactive;width:200px" value="$CK{'email'}" tabindex="111"></td>
<th style="text-align:center">[ <a href="$CF{'sitehome'}" target="_top"
title="$CF{'sitename'}�ص���ޤ�\n�༼��å������ϽФʤ��Τǵ���ΰ�����˺�줺��"
>$CF{'sitename'}�ص���</a> ]</th>
</tr>

<tr>
<th><label accesskey="m" for="cmd" title="coMmand\n���ޥ��"
>Co<span class="ak">m</span>mand</label>:</th>
<td><input type="text" name="cmd" id="cmd" maxlength="200" style="ime-mode:inactive;width:150px"
 value="$CK{'cmd'}" tabindex="102"></td>
<th><label accesskey="o" for="home" title="hOme\n�����Ȥ�URL�Ǥ�"
>H<span class="ak">o</span>me</label>:</th>
<td colspan="3"><input type="text" name="home" id="home" maxlength="200" size="40"
 style="ime-mode:inactive;width:200px" value="$CK{'home'}" tabindex="112"></td>
<th style="text-align:center">- <a href="http://www.airemix.com/" title="Airemix�ؤ��äƤߤ�"
>Marldia $CF{'version'}</a> -</th>
</tr>
</table>
</form>
</body>
</html>
_HTML_
  exit;
}


#-------------------------------------------------
# South
#
sub south{
  my@log=();
  my%MB;

  #ɽ�𥢥�����
  if(($IN{'icon'}=~/^((?:[^\/#]*\/)*(?:[^\/#.]*\.)*?[^\/#.]+)(?:\.[^\/#.]*)?#\d+$/o)
   &&($IN{'surface'}=~/^$1\d*(?:\.[^\/#.]*)?$/o)){
    $IN{'icon'}=$IN{'surface'};
  }

  #���å����񤭹���
  if($IN{'cook'}){
    my$cook=&hashstr(\%IN,qw(id name color bcolo line reload icon email home cmd));
    #0-9A-Za-z\-\.\_
    $cook=~s{(\W)}{'%'.unpack('H2',$1)}ego;
    my$gmt=&datef(($^T+20000000),'gmt');
    print"Set-Cookie: Marldia=$cook; expires=$gmt\n";
  }

  #���üԡ���󥭥󥰡��񤭹��߽���
  sysopen(LOG,$CF{'log'},O_CREAT|O_RDWR)||die"Can't write log.";
  flock(LOG,LOCK_EX);
  #���ü��ɤ߹���
  while(<LOG>){
    /\S/o||last;
    /\bid=\t([^\t]+);\t(?:[^\t]*=\t[^\t]*;\t)*$/o||next;
    $MB{$1}=$_;
  }
  @log=grep{m/^Mar1=\t[^\t]*;\t(?:[^\t]*=\t[^\t]*;\t)*$/o}<LOG>;
  
  #��ʬ�Υǡ������ɲ�
  if($IN{'name'}&&$ENV{'CONTENT_LENGTH'}){
    #ǽưŪ�����
    delete$MB{"$IN{'ra'}"};
    $MB{"$IN{'id'}"}=&hashstr(\%IN,qw(id name color reload ra))."time=\t$^T;\texpire=\t$^T;\t\n";
  }elsif($IN{'name'}){
    #���̤˥����
    delete$MB{"$IN{'ra'}"};
    $MB{"$IN{'id'}"}=~m/\texpire=\t(\d+);\t/;
    $MB{"$IN{'id'}"}=&hashstr(\%IN,qw(id name color reload ra))."time=\t$^T;\texpire=\t$1;\t\n";
  }else{
    #���
    $MB{"$IN{'ra'}"}="id=\t$IN{'ra'};\t".&hashstr(\%IN,qw(reload ra))."time=\t$^T;\t\n";
  }
  
  #���üԽ���
  my@mb=();
  for(keys%MB){
    my%DT=($MB{"$_"}=~m/([^\t]*)=\t([^\t]*);\t/go);
    ($DT{'reload'}<20)&&($DT{'reload'}=20);
    (($DT{'time'}+($DT{'reload'}*6))<$^T)&&(delete$MB{$_},next);#TimeOver
    (exists$DT{'expire'})||(next);#ROM
    $DT{'expire'}=$^T-$DT{'expire'};
    push(@mb,qq[<a style="color:$DT{'color'}" title="$DT{'expire'}��">$DT{'name'}</a>��]);
  }

  if(length$IN{'body'}){
    #��󥭥󥰲���
    my%RK;
    sysopen(RANK,$CF{'rank'},O_CREAT|O_RDWR)||die"Can't write rank.";
    flock(RANK,LOCK_EX);
    while(<RANK>){
      /\bid=\t([^\t]+);\t(?:[^\t]*=\t[^\t]*;\t)*$/o||next;
      $RK{$1}=$_;
    }
    if($RK{"$IN{'id'}"}=~s/\texp=\t([^\t]*);\t/\texp=\t@{[$IN{'exp'}=$1+1]};\t/o){
      unless($RK{"$IN{'id'}"}=~s/\tname=\t([^\t]*);\t/\tname=\t$IN{'name'};\t/o){
        $RK{"$IN{'id'}"}=&hashstr(\%IN,qw(id name exp))."\n";
      }
    }else{
      $RK{"$IN{'id'}"}="id=\t$IN{'id'};\tname=\t$IN{'name'};\texp=\t1;\t\n";
      $IN{'exp'}=1;
    }
    truncate(RANK,0);
    seek(RANK,0,0);
    print RANK values%RK;
    close RANK;
    #ȯ������
    my$data="Mar1=\t;\t".&hashstr(\%IN,qw(id name color bcolo body icon home email exp ua ra))."time=\t$^T;\t\n";
    splice(@log,$CF{'max'}-1);
    unshift(@log,$data);
  }elsif($IN{'del'}){
    #�������
    for(@log){
      (/\texp=\t$IN{'del'};\t/o&&/\tid=\t$IN{'id'};\t/o)||next;
      s/^(Mar1=\t)([^\t]*)(;\t)/$1del$3/o;
      last;
    }
  }
  truncate(LOG,0);
  seek(LOG,0,0);
  print LOG values%MB,"\n",@log;
  close(LOG);
  
  my$visitor=scalar(keys%MB);
  my$entrant=$#mb+1;
  my$audience=$visitor-$entrant;

  my$query='south';
  if($IN{'id'}){
    my%DT=%IN;
    for(keys%IN){
      $DT{$_}=~s{(\W)}{'%'.unpack('H2',$1)}ego;
      $_="$_=$DT{$_}";
    }
    $query='';
    for(qw(name id line reload color)){
      $query.="$_=$DT{$_}&amp;";
    }
  }
  
  if($IN{'reload'}){
    &header(qq(<meta http-equiv="refresh" content="$IN{'reload'};url=index.cgi?$query">\n));
  }else{
    &header;
  }
  my$member;
  if(@mb){
    $member="@mb";
  }else{
    my@wabi=(qw(���󤳤ɤ� �ߤƤ������ (-_��)���׎���),"@{[('|_��)���ס�')x$audience]}");
    $member=$wabi[int(rand($#wabi+1))];
  }
  my$time=sprintf('%02d:%02d:%02d',(localtime$^T)[2,1,0]);
  print<<"_HTML_";
<table class="meminfo" summary="���üԾ���ʤ�"><tr>
<td class="reload">[ <a href="index.cgi?$query">$time</a> ]</td>
<td class="member">[���:$visitor�� ���ü�:$entrant�� �ѵ�:$audience��] [ $member ]</td>
<td class="respan">(<span>$IN{'reload'}�ôֳ�</span>)</td>
</tr></table>
_HTML_
  
  #��ɽ��
  @log=splice(@log,0,$IN{'line'});
  for(@log){
    /^Mar1=\tdel;\t/o&&(next);
    my%DT=($_=~m/([^\t]*)=\t([^\t]*);\t/go);
    $DT{'date'}=&date($DT{'time'});
    
    #̾�����᡼�륢�ɥ쥹��̾����
    if($DT{'email'}&&$DT{'color'}){
      $DT{'name'}=qq[<a href="mailto:$DT{'email'}" title="$DT{'email'}" style="color:$DT{'color'}">$DT{'name'}</a>];
    }elsif($DT{'email'}){
      $DT{'name'}=qq[<a href="mailto:$DT{'email'}" title="$DT{'email'}">$DT{'name'}</a>];
    }elsif($DT{'color'}){
      $DT{'name'}=qq[<a style="color:$DT{'color'}">$DT{'name'}</a>];
    }
    
    #
    if($DT{'home'}){
      $DT{'home'}=qq[<a href="$DT{'home'}" target="_blank" title="$DT{'home'}">��</a>];
    }else{
      $DT{'home'}="��";
    }
    srand($DT{'exp'});
    $DT{'level'}=1+int(rand(sqrt$DT{'exp'}*2));
    
    my$del='';
    if(($IN{'id'})&&($DT{'id'}eq$IN{'id'})){
      $del=qq([<a href="$CF{'index'}?del=$DT{'exp'}&amp;$query">���</a>]);
    }
    print<<"_HTML_";
<table cellspacing="0" class="article" summary="article">
<tr>
<th class="articon" rowspan="2"><img src="$CF{'icondir'}$DT{'icon'}" alt="$DT{'icon'}" $CF{'imgatt'}></th>
<th class="artname" nowrap>$DT{'name'}&nbsp;$DT{'home'}</th>
<td class="artbody" style="color:$DT{'bcolo'};">$DT{'body'}</td>
</tr>
<tr>
<td class="artdel">$del</td>
<td class="artinfo"><span class="artlev">Exp.$DT{'exp'}/Lv.$DT{'level'}</span>
<span class="artdate">$DT{'date'}</span></td>
</tr>
</table>
_HTML_
  }
  &footer;
  exit;
}


#-------------------------------------------------
# ����
#
sub manage{
  unless($IN{'manage'}){
    die"�ֲ��⤷�ʤ���������";
  }
  #��������
  my@arg=grep{s/\\(\\)|\\(")|"/$1$2/go;s/\\"/"/go;$_;}($IN{'manage'}=~
  /([^"\\\ ]*(?:\\[^\ ][^"\\\ ]*)*(?:"[^"\\]*(?:\\.[^"\\]*)*(?:"[^"\\\ ]*(?:\\[^\ ][^"\\\ ]*)*)?)*\\?)/go);

=item �������ޥ��

$CF{'manpas'}='manage';�ʤ顢
#manage ...
��...�Ȥ������ޥ�ɤ�ȯư

��rank (del|cat|conv) [id ...]
 ��󥭥󥰤�ɽ��
��del
 �����Ȥ��ƻ��ꤵ�줿ID�ξ������
��cat
 ��������ID�ˡ�����ʹߤ�ID�����礹��
��conv
 1.5�����Υ�󥭥󥰥ǡ�����1.6�������Ѵ�����

��mem
 ���üԾ����ɽ��

=cut

  #ʬ��
  if('rank'eq$arg[0]){
    #ȯ����󥭥�
    unless($arg[1]){
    }elsif('del'eq$arg[1]){
      #��󥭥󥰤�����
      sysopen(RANK,$CF{'rank'},O_CREAT|O_RDWR)||die"Can't write rank.";
      flock(RANK,LOCK_EX);
      my%RK=map{m/\bid=\t([^\t]+);\t/o;($1,$_)}(<RANK>);
      delete$RK{$arg[2]};
      truncate(RANK,0);
      seek(RANK,0,0);
      print RANK values%RK;
      close RANK;
    }elsif('cat'eq$arg[1]){
      #ID����ӷи��Ϥ�����
      sysopen(RANK,$CF{'rank'},O_CREAT|O_RDWR)||die"Can't write rank.";
      flock(RANK,LOCK_EX);
      my%RK=map{m/\bid=\t([^\t]+);\t/o;($1,$_)}(<RANK>);
      for(3..$#arg){
        my$exp=($RK{$arg[$_]}=~/\texp=\t([^\t]*);\t/o)?$1:next;
        $RK{$arg[2]}=~s/\texp=\t([^\t]*);\t/\texp=\t@{[$1+$exp]};\t/o;
        delete$RK{$arg[$_]};
      }
      truncate(RANK,0);
      seek(RANK,0,0);
      print RANK values%RK;
      close RANK;
    }elsif('conv'eq$arg[1]){
      sysopen(RANK,$CF{'rank'},O_CREAT|O_RDWR)||die"Can't write rank.";
      flock(RANK,LOCK_EX);
      my%RK=map{m/(.*)/o}(<RANK>);
      my$rank='';
      for(keys%RK){
        ('-f'ne$arg[2])&&($_=~/^id=/)&&(die"���Ǥ��Ѵ��Ѥߡ�('rank conv -f'�Ȥ���ȶ���Ū���Ѵ����ޤ�)");
        $RK{$_}=~s/\tpoint=\t/\texp=\t/;
        $rank.="id=\t$_;\t$RK{$_}\n";
      }
      truncate(RANK,0);
      seek(RANK,0,0);
      print RANK $rank;
      close RANK;
    }
    
    #��󥭥�ɽ��
    &header;
    print<<'_HTML_';
<table summary="Ranking">
<caption>ȯ����󥭥�</caption>
_HTML_
    sysopen(RANK,$CF{'rank'},O_CREAT|O_RDONLY)||die"Can't read rank.";
    flock(RANK,LOCK_SH);
    print map{"<tr><td>$_</td></tr>"}grep{(m/(.*)/o)}<RANK>;#��ա�ID��ɽ�������
    close RANK;
    print"</table>";
    &footer;
    exit;
  }elsif('mem'eq$arg[0]){
    #��ʪ�Ͱ���
    &header;
    print<<"_HTML_";
<table summary="roms">
<caption>��ʪ�Ͱ���</caption>
_HTML_
    #���ü��ɤ߹���
    sysopen(LOG,$CF{'log'},O_CREAT|O_RDONLY)||die"Can't read log.";
    flock(LOG,LOCK_SH);
    while(<LOG>){
      /\S/o||last;
      /\bid=\t([^\t]+);\t(?:[^\t]*=\t[^\t]*;\t)*$/o||next;
      print"<tr><td>$_</td></tr>";
    }
    close LOG;
    print"</table>";
    &footer;
    exit;
  }elsif(''eq$arg[0]){
    #
  }elsif(''eq$arg[0]){
    #
  }elsif(''eq$arg[0]){
    #
  }else{
    #̵���ʥ��ޥ��
    die"\'$arg[0]\'�ϥ��ޥ�ɤȤ��ƤȤ���ǧ������Ƥ��ޤ���";
  }
  exit;
}



#------------------------------------------------------------------------------#
# Sub Routins
#
# mainľ���Υ��֥롼���󷲤����

#-------------------------------------------------
# Form���Ƽ���
sub getform{
  my$i;my%DT;
  unless($ENV{'REQUEST_METHOD'}){
  }elsif('HEAD'eq$ENV{'REQUEST_METHOD'}){ #forWWWD
#Method��HEAD�ʤ��LastModifed����Ϥ��ơ�
#�Ǹ����ƻ�����Τ餻��
    my$last=&datef((stat("$CF{'log'}0.cgi"))[9],'last');
    print"Last-Modified: $last\n";
    print"Content-Type: text/plain\n\n";
    exit;
  }elsif('POST'eq$ENV{'REQUEST_METHOD'}){
    read(STDIN,$i,$ENV{'CONTENT_LENGTH'});
  }elsif('GET'eq$ENV{'REQUEST_METHOD'}){
    $i=$ENV{'QUERY_STRING'};
  }

  if(length$i>262114){
    #����������
    die"������ʤ�Ǥ��̤�¿�����ޤ�\n$i";
    exit;
  }elsif(length$i>0){
    #���Ϥ�Ÿ�����ƥϥå���������
    # EUC-JPʸ��
    my$ascii='[\x09\x0A\x0D\x20-\x7E]'; # 1�Х��� EUC-JPʸ����
    my$twoBytes='(?:[\x8E\xA1-\xFE][\xA1-\xFE])'; # 2�Х��� EUC-JPʸ��
    my$threeBytes='(?:\x8F[\xA1-\xFE][\xA1-\xFE])'; # 3�Х��� EUC-JPʸ��
    for(split(/[&;]/o,$i)){
      my($i,$j)=split('=',$_,2);
      (defined$j)||($DT{$i}='',next);
      study$j;
      $j=~tr/+/\ /;
      $j=~s/%([0-9A-Fa-f]{2})/pack('H2',$1)/ego;
      $j=($j=~/((?:$ascii|$twoBytes|$threeBytes)*)/o)?"$1":'';
      $j=~s/\t/\ \ /go;
      if('body'eq$i){
        $CF{'manpas'}&&($j=~/^[#��]\s*$CF{'manpas'}\s+(.*)/o)&&($DT{'manage'}=$1,last);
        #��ʸ�Τߥ�����ȤäƤ⤤������ˤ�Ǥ���
        $j=~s/</&#60;\t/go;
        $j=~s/>/&#62;\t/go;
        if($CF{'tags'}){
          $j=~s{&#60;\t(/?)(\w+)([^\t]*)&#62;\t}
          {my($a,$b,$c)=($1,$2,$3);($CF{'tags'}=~/\b$2\b/io)?"<$a$b>":"&#60;$a$b$c&#62;"}ego;
        }
        $j=~tr/\t//d;
      }else{
        $j=~s/</&#60;/go;
        $j=~s/>/&#62;/go;
      }
      $j=~s/"/&#34;/go;
      $j=~s/&(#?\w+;)?/($1)?"&$1":'&#38;'/ego;
      $j=~s/'/&#39;/go;
      $j=~s/\x0D\x0A/<br>/go;$j=~s/\x0D/<br>/go;$j=~s/\x0A/<br>/go;
      $j=~s/(<br>)+$//o;
      $DT{$i}=$j;
    }
  }

  
  if((!%DT)||('frame'eq$DT{'mode'})){
    #�ե졼��
    $IN{'mode'}='frame';
  }elsif($DT{'manage'}){
    #�������ޥ��
    $IN{'mode'}='manage';
    $IN{'manage'}=$DT{'manage'};
  }elsif($DT{'name'}){
    &getck;
    #http URL ������ɽ��
    my$http_URL_regex =
   q{\b(?:https?|shttp)://(?:(?:[-_.!~*'()a-zA-Z0-9;:&=+$,]|%[0-9A-Fa-f}.
   q{][0-9A-Fa-f])*@)?(?:(?:[a-zA-Z0-9](?:[-a-zA-Z0-9]*[a-zA-Z0-9])?\.)}.
   q{*[a-zA-Z](?:[-a-zA-Z0-9]*[a-zA-Z0-9])?\.?|[0-9]+\.[0-9]+\.[0-9]+\.}.
   q{[0-9]+)(?::[0-9]*)?(?:/(?:[-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f]}.
   q{[0-9A-Fa-f])*(?:;(?:[-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f][0-9A-}.
   q{Fa-f])*)*(?:/(?:[-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f}.
   q{])*(?:;(?:[-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*)*)}.
   q{*)?(?:\?(?:[-_.!~*'()a-zA-Z0-9;/?:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])}.
   q{*)?(?:#(?:[-_.!~*'()a-zA-Z0-9;/?:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*}.
   q{)?};
    #ftp URL ������ɽ��
    my$ftp_URL_regex =
   q{\bftp://(?:(?:[-_.!~*'()a-zA-Z0-9;&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*}.
   q{(?::(?:[-_.!~*'()a-zA-Z0-9;&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*)?@)?(?}.
   q{:(?:[a-zA-Z0-9](?:[-a-zA-Z0-9]*[a-zA-Z0-9])?\.)*[a-zA-Z](?:[-a-zA-}.
   q{Z0-9]*[a-zA-Z0-9])?\.?|[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)(?::[0-9]*)?}.
   q{(?:/(?:[-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*(?:/(?}.
   q{:[-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*)*(?:;type=[}.
   q{AIDaid])?)?(?:\?(?:[-_.!~*'()a-zA-Z0-9;/?:@&=+$,]|%[0-9A-Fa-f][0-9}.
   q{A-Fa-f])*)?(?:#(?:[-_.!~*'()a-zA-Z0-9;/?:@&=+$,]|%[0-9A-Fa-f][0-9A}.
   q{-Fa-f])*)?};
    #�᡼�륢�ɥ쥹������ɽ����
    #"aaa@localhost"�ʤɤ�WWW��ǡ֥᡼�륢�ɥ쥹�פȤ��ƻȤ��Ȥϻפ��ʤ��Τ�
    my$mail_regex=
   q{(?:[^(\040)<>@,;:".\\\\\[\]\000-\037\x80-\xff]+(?![^(\040)<>@,;:".\\\\}
   .q{\[\]\000-\037\x80-\xff])|"[^\\\\\x80-\xff\n\015"]*(?:\\\\[^\x80-\xff][}
   .q{^\\\\\x80-\xff\n\015"]*)*")(?:\.(?:[^(\040)<>@,;:".\\\\\[\]\000-\037\x}
   .q{80-\xff]+(?![^(\040)<>@,;:".\\\\\[\]\000-\037\x80-\xff])|"[^\\\\\x80-}
   .q{\xff\n\015"]*(?:\\\\[^\x80-\xff][^\\\\\x80-\xff\n\015"]*)*"))*@(?:[^(}
   .q{\040)<>@,;:".\\\\\[\]\000-\037\x80-\xff]+(?![^(\040)<>@,;:".\\\\\[\]\0}
   .q{00-\037\x80-\xff])|\[(?:[^\\\\\x80-\xff\n\015\[\]]|\\\\[^\x80-\xff])*}
   .q{\])(?:\.(?:[^(\040)<>@,;:".\\\\\[\]\000-\037\x80-\xff]+(?![^(\040)<>@,}
   .q{;:".\\\\\[\]\000-\037\x80-\xff])|\[(?:[^\\\\\x80-\xff\n\015\[\]]|\\\\[}
   .q{^\x80-\xff])*\]))+};
    
    if(defined$DT{'body'}){
      #�������Ϥα�������
      $DT{'body'}=~s{($http_URL_regex|$ftp_URL_regex|($mail_regex))}
      {<a href="@{[''ne$2?'mailto:':'']}$1" target="_blank">$1</a>}go;
      #��ư��󥯤ȸ��ˤ��A�������Ϥ���������
      $DT{'body'}=~s{href=(&#3\d;)<a href="([^"]*\1&?)" target="_blank">\2</a>}{href=$1$2}go;
      $DT{'body'}=~s{(<a href=")([^"]*)&#60;/a&(" target="_blank">\2)&#60;/a&</a>#62;}{$1$2$3</a>&#60;/a&#62;}go;
      $IN{'body'}=($DT{'body'}=~/(.+)/o)?"$1":'';
      $IN{'cook'}=($DT{'cook'}=~/(.)/o)?'on':'0';
    }
    if(defined$DT{'del'}){
      (($DT{'del'}=~/(\d+)/o)&&(int$1))&&($IN{'del'}=int$1);
    }
    $IN{'name'}=($DT{'name'}=~/(.{1,100})/o)?"$1":'';
    $IN{'id'}=($DT{'id'}=~/(.{1,100})/o)?"$1":($CK{'id'}?$CK{'id'}:$IN{'name'});
    $IN{'color'}=($DT{'color'}=~/([\#\w\(\)\,]{1,20})/o)?"$1":'';
    $IN{'bcolo'}=($DT{'bcolo'}=~/([\#\w\(\)\,]{1,20})/o)?"$1":'';
    $DT{'email'}=($DT{'email'}=~/(.{1,200})/o)?"$1":'';
    $IN{'email'}=($DT{'email'}=~/($mail_regex)/o)?"$1":'';
    $DT{'home'}=($DT{'home'}=~/(.{1,200})/o)?"$1":'';
    $IN{'home'}=($DT{'home'}=~/($http_URL_regex)/o)?"$1":'';
    $IN{'icon'}=($DT{'icon'}=~/([\w\:\.\~\-\%\/\#]+)/o)?"$1":'';
    ($DT{'surface'}=~/([\w\.\~\-\%\/]+)/o)&&($IN{'surface'}="$1");
    $IN{'cmd'}=($DT{'cmd'}=~/(.+)/o)?"$1":undef;
    $IN{'line'}=(($DT{'line'}=~/(\d+)/o)&&(int$1))?int$1:$CF{'defline'};
    $IN{'reload'}=($DT{'reload'}=~/(\d+)/o)?int$1:$CF{'defreload'};
  }elsif((defined$DT{'north'})||('north'eq$DT{'mode'})){
    #��
    $IN{'mode'}='north';
    $IN{'line'}=$CF{'defline'};
    $IN{'reload'}=$CF{'defreload'};
  }elsif(defined$DT{'south'}){
    #��
    $IN{'mode'}='south';
    $IN{'line'}=$CF{'romline'};
    $IN{'reload'}=$CF{'romreload'};
  }
  $IN{'ra'}=($ENV{'REMOTE_ADDR'}=~/([\d\:\.]{2,56})/o)?"$1":'';
  $IN{'hua'}=($ENV{'HTTP_USER_AGENT'}=~/([^\t]+)/)?"$1":'';
  return%IN;
}


#-------------------------------------------------
# Header with G-ZIP etc.
sub header{
  print<<'_HTML_';
Content-type: text/html; charset=euc-jp
Content-Language: ja
Pragma: no-cache
Cache-Control: no-cache
_HTML_
=gzip
  if((-x$CF{'gzip'})&&($ENV{'HTTP_ACCEPT_ENCODING'}=~/gzip/)){
    print"Content-encoding: gzip\n\n";
    open(STDOUT,"| $CF{'gzip'} -c");
    print"<!-- gzip enable -->\n";
  }else{print"\n<!-- gzip disable -->\n";}
=cut
  print<<"_HTML_";

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" "http://www.w3.org/TR/REC-html40/loose.dtd">
<html lang="ja">
<head>
<meta http-equiv="Content-type" content="text/html; charset=euc-jp">
<meta http-equiv="Content-Script-Type" content="text/javascript">
<meta http-equiv="Content-Style-Type" content="text/css">
_HTML_

($_[0])&&(print"$_[0]");

  #CSS Switch
  CSS:{
    if($ENV{'HTTP_USER_AGENT'}=~m/MSIE 3/o){
      #IE3��NG
      last CSS;
    }elsif($ENV{'HTTP_USER_AGENT'}=~m{Mozilla/4.*compatible}o){
      #Mozilla/4�ߴ����̤�
    }elsif($ENV{'HTTP_USER_AGENT'}=~m{Mozilla/4}o){
      #NetscapeNavogator4�ϥ���
      last CSS;
    }
    #����ʳ��ˤϰ���Ϥ��Ƥ���
    print qq{<link rel="stylesheet" type="text/css" href="$CF{'style'}" media="screen" title="DefaultStyle">\n};
  }
  print<<"_HTML_";
<link rel="start" href="$CF{'sitehome'}">
<link rel="index" href="$CF{'index'}">
<link rel="help" href="$CF{'help'}">
<link rev="made" href="mailto:naruse\@airemix.com">
<title>$CF{'title'}</title>
</head>
<body>
_HTML_
}


#-------------------------------------------------
# �եå�������
#
sub footer{
  print<<"_HTML_";
<div class="AiremixCopy">- <a href="http://www.airemix.com/" target="_top" title="Airemix - Marldia -">Airemix Marldia</a><var>$CF{'version'}</var> -</div>
</body>
</html>
_HTML_
  exit;
}


#-------------------------------------------------
# �ϥå��夫���N=\tV;\tʸ����פ��������
#
sub hashstr{
  my$hash=shift@_;
  my$str='';
  for(@_){
    $str.="$_=\t$hash->{$_};\t";
  }
  return$str;
}

#-------------------------------------------------
# Cookie���������
#
sub getck{
  ($ENV{'HTTP_COOKIE'})||(return undef);
  my$ascii='[\x0A\x0D\x20-\x7E]'; # 1�Х��� EUC-JPʸ����-\x09
  my$twoBytes='(?:[\x8E\xA1-\xFE][\xA1-\xFE])'; # 2�Х��� EUC-JPʸ��
  my$threeBytes='(?:\x8F[\xA1-\xFE][\xA1-\xFE])'; # 3�Х��� EUC-JPʸ��
  my$cook=($ENV{'HTTP_COOKIE'}=~/([^\t]+)/o)?"$1":'';
  for(split('; ',$cook)){
    my($i,$j)=split('=',$_,2);
    ('Marldia'ne$i)&&(next);
    $j=~s/%([0-9A-Fa-f]{2})/pack('H2',$1)/ego;
    %CK=($j=~/(\w+)=\t((?:$ascii|$twoBytes|$threeBytes)*);\t/go);
    last;
  }
  return%CK;
}


#-------------------------------------------------
# �ե����ޥåȤ��줿���ռ������֤�
sub datef{
=item ����
$ time�����λ���
;
$ ���Ϸ���(gmt|last)
=cut
  unless($_[1]){
  }elsif($_[1]eq'gmt'){
   #Cookie��
    return sprintf("%s, %02d-%s-%d %s GMT",(split(/\s+/o,gmtime($_[0])))[0,2,1,4,3]);
  }elsif($_[1]eq'last'){
   #LastModified��
    return sprintf("%s, %02d %s %s %s GMT",(split(/\s+/o,gmtime($_[0])))[0,2,1,4,3]);
  }
  return&date;
}


#-------------------------------------------------
# �������ɽ���Ѥ˥ե����ޥåȤ��줿���ռ������֤�
sub date{
=item ����
$ time��������
=cut
  my($sec,$min,$hour,$mday,$mon,$year,$wday)=localtime($_[0]);
  #sprintf�������ϡ�Perl�β���򸫤Ƥ�������^^;;
  return sprintf("%4dǯ%02d��%02d��(%s) %02d��%02dʬ" #"1970ǯ01��01��(��) 09��00ʬ"����
  ,$year+1900,$mon+1,$mday,('��','��','��','��','��','��','��')[$wday],$hour,$min);
#  return sprintf("%1d:%01d:%2d %4d/%02d/%02d(%s)" #"9:0: 0 1970/01/01(Thu)"����
#  ,$hour,$min,$sec,$year+1900,$mon+1,$mday,('Sun','Mon','Tue','Wed','Thu','Fri','Sat')[$wday]);
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
=cut
  my$opt='';
  ($_[1])&&($opt=" $_[1]");

=item ʣ����������ꥹ��
$CF{'icls'}�κǽ�ΰ�ʸ����' '��Ⱦ�Ѷ���ˤ��ä����ʣ���ꥹ�ȥ⡼�ɤˤʤ�ޤ�
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

  if($CK{'iconlist'}&&('reset'ne$_[2])){
    #����å���Ǥ���$CK{'iconlist'}���֤�
    return$CK{'iconlist'};
  }
  
  
  #��������ꥹ���ɤ߹���
  my$list;
  if($CK{'cmd'}=~/\biconlist=nolist(;|$)/o){
   #`icon=nolist`�ǥ�������ꥹ�Ȥ��ɤ߹��ޤʤ�
  }elsif($CF{'icls'}=~/^ /o){
    #ʣ����������ꥹ���ɤ߹���
    for($CF{'icls'}=~/("(?:\\["\\]|\\\d{1,3}|.)*?"|\S+)/go){
      ($_)||(next);
      (sysopen(RD,"$_",O_RDONLY))||(die"Can't open multi-iconlist($_).");
      eval"flock(RD,LOCK_SH);";
      $list.=join('',<RD>);
      close(RD);
    }
  }else{
    #ñ�쥢������ꥹ���ɤ߹���
    (sysopen(RD,"$CF{'icls'}",O_RDONLY))||(die"Can't open single-iconlist.");
    eval"flock(RD,LOCK_SH);";
    $list=join('',<RD>);
    close(RD);
  }

  #���򥢥�����η����SELECT���������
  if($CF{'exicon'}&&($CK{'cmd'}=~/\bicon=([^;]*)/o)&&$IC{$1}){
    #�ѥ���ɷ�
    $_[0]=$IC{$1};
    $list.=qq(<option value="$_[0]" selected>���ѥ�������</option>\n);
  }elsif($CF{'exicfi'}&&($CK{'cmd'}=~/\b$CF{'exicfi'}=([^;]*)/o)){
    #�ե�������귿
    $_[0]=$1;
    $list.=qq(<option value="$_[0]" selected>�ե��������</option>\n);
  }elsif($_[0]and$list=~s/(value="$_[0]")/$1 selected="selected"/io){
  }elsif($list=~s/value=(["'])(.+?)\1/value=$1$2$1 selected="selected"/io){
    $_[0]=$2;
  }
  
  $CK{'iconlist'}=<<"_HTML_";
<select name="icon" id="icon" onchange="iconChange(this.options[this.selectedIndex].value)"$opt>
$list</select>
_HTML_
  return$CK{'iconlist'};
}


#-------------------------------------------------
# ���顼�ꥹ���ɤ߹���
#
sub iptcol{

=item ����

$_[0]: 'color'
$_[1]: 'tabindex=12'

=cut

  my$id='color';
  my$opt='';
  ($_[0])&&($id=$_[0]);
  ($_[1])&&($opt=" $_[1]");
  if('input'eq$CF{'colway'}){
    return<<"_HTML_";
<input type="text" name="$id" id="$id" class="blur" maxlength="20" style="ime-mode:disabled; width:90px;"
 onFocus="this.className='focus'" onBlur="this.className='blur'" value="$CK{$id}"$opt>
_HTML_
  }else{
    my$list=<<"_HTML_";
<option value="#000000" style="background-color: #000000;">Black</option>
<option value="#2f4f4f" style="background-color: #2f4f4f;">DarkSlateGray</option>
<option value="#696969" style="background-color: #696969;">DimGray</option>
<option value="#808080" style="background-color: #808080;">Gray</option>
<option value="#708090" style="background-color: #708090;">SlateGray</option>
<option value="#778899" style="background-color: #778899;">LightSlateGray</option>
<option value="#8b4513" style="background-color: #8b4513;">SaddleBrown</option>
<option value="#a0522d" style="background-color: #a0522d;">Sienna</option>
<option value="#d2691e" style="background-color: #d2691e;">Chocolate</option>
<option value="#cd5c5c" style="background-color: #cd5c5c;">IndianRed</option>
<option value="#a52a2a" style="background-color: #a52a2a;">Brown</option>
<option value="#8b0000" style="background-color: #8b0000;">DarkRed</option>
<option value="#800000" style="background-color: #800000;">Maroon</option>
<option value="#b22222" style="background-color: #b22222;">FireBrick</option>
<option value="#ff6347" style="background-color: #ff6347;">Tomato</option>
<option value="#ff4500" style="background-color: #ff4500;">OrangeRed</option>
<option value="#dc143c" style="background-color: #dc143c;">Crimson</option>
<option value="#c71585" style="background-color: #c71585;">MediumVioletRed</option>
<option value="#ff1493" style="background-color: #bb1493;">DeepPink</option>
<option value="#8b008b" style="background-color: #8b008b;">DarkMagenta</option>
<option value="#800080" style="background-color: #800080;">Purple</option>
<option value="#9932cc" style="background-color: #9932cc;">DarkOrchid</option>
<option value="#9400d3" style="background-color: #9400d3;">DarkViolet</option>
<option value="#8a2be2" style="background-color: #8a2be2;">BlueViolet</option>
<option value="#6a5acd" style="background-color: #6a5acd;">SlateBlue</option>
<option value="#4b0082" style="background-color: #4b0082;">Indigo</option>
<option value="#00008e" style="background-color: #00008e;">DarkBlue</option>
<option value="#000080" style="background-color: #000080;">Navy</option>
<option value="#191970" style="background-color: #191970;">MidnightBlue</option>
<option value="#483d8b" style="background-color: #483d8b;">DarkSlateBlue</option>
<option value="#0000cd" style="background-color: #0000cd;">MediumBlue</option>
<option value="#4169e1" style="background-color: #4169e1;">RoyalBlue</option>
<option value="#5f9ea0" style="background-color: #5f9ae0;">CadetBlue</option>
<option value="#4682b4" style="background-color: #4682b4;">SteelBlue</option>
<option value="#008080" style="background-color: #008080;">Teal</option>
<option value="#008b8b" style="background-color: #008b8b;">Darkcyan</option>
<option value="#2e8b57" style="background-color: #2e8b57;">SeaGreen</option>
<option value="#228b22" style="background-color: #228b22;">ForestGreen</option>
<option value="#006400" style="background-color: #006400;">DarkGreen</option>
<option value="#556b2f" style="background-color: #556b2f;">DarkOliveGreen</option>
<option value="#6b8e23" style="background-color: #6b8e23;">OliveDrab</option>
<option value="#808000" style="background-color: #808000;">Olive</option>
_HTML_
    if($CK{$id}&&$list=~s/(value=(["'])$CK{$id}\2)/$1 selected="selected"/io){
    }elsif($list=~s/value=(["'])(.+?)\1/value="$2" selected="selected"/io){
      $CK{$id}=$2;
    }
    return<<"_HTML_";
<select name="$id" id="$id"$opt>
$list</select>
_HTML_
  }
}


#-------------------------------------------------
# Location��ž��
sub locate{
  my$i;
  if($_[0]=~/^http:/){
    $i=$_[0];
  }elsif($_[0]=~/\?/){
    $i=sprintf('http://%s%s/',$ENV{'SERVER_NAME'},
    substr($ENV{'SCRIPT_NAME'},0,rindex($ENV{'SCRIPT_NAME'},'/')));
    $i.=sprintf('%s?%s',$_[0]);
  }elsif($_[0]eq'/'){
    $i='http://'.$ENV{'SERVER_NAME'}.'/';
  }elsif($_[0]){
    $i=sprintf('http://%s%s/',$ENV{'SERVER_NAME'},
    substr($ENV{'SCRIPT_NAME'},0,rindex($ENV{'SCRIPT_NAME'},'/')));
    $i.=$_[0];
  }
  print<<"_HTML_";
Location: $i
Content-Type: text/html
Pragma: no-cache
Cache-Control: no-cache

<!DOCTYPE html PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html>
<head>
<meta http-equiv="Refresh" content="0;URL=$i">
<title>301 Moved Permanently</title>
</head>
<body>
<h1>Writing is Complete!</h1>
<p>And, please go <a href="$i">here</A>.</p>
<p>Location: $i</p>
<p>Marldia <span class="red">$CF{'correv'}</span>.<br>
Copyright &copy;2001 <a href="http://www.airemix.com/" title="Airemix">Airemix</a>. All rights reserved.</p>
</body>
</html>
_HTML_
  exit;
}

#-------------------------------------------------
# �������
BEGIN{
  #Revision Number
  $CF{'correv'}=qq$Revision: 1.7 $;
  $CF{'version'}=($CF{'correv'}=~/(\d[\w\.]+)/o)?"v$1":'unknown';#"Revision: 1.4"->"v1.4"
  #���顼���Ф��饨�顼���̤�ɽ������褦��
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
