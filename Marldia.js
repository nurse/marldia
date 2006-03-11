/******************************************************************************
 * 
 * Marldia.js
 * 
 * -*- coding: utf-8 -*-
 * $Id: Marldia.js,v 1.5 2006-03-11 09:33:00 naruse Exp $
 * 
 ******************************************************************************/

/* ****************************************************** */
// definitions
var imgPreview;
var bodyContainer;
var bodySwitch;
var eForm;
var commentHistory;
var maxHistory = 100;
var isInitialized;

/*========================================================*/
// Initialize
function init(){
    if(!Array || !(new Array).push){
	return false;
    }if(document.all){
	imgPreview = document.all('preview');
	bodyContainer=document.all('bodyContainer');
	bodySwitch=document.all('bodySwitch');
	eForm = document.all('north');
    }else if(document.getElementById){
	imgPreview=document.getElementById('preview');
	bodyContainer=document.getElementById('bodyContainer');
	bodySwitch=document.getElementById('bodySwitch');
	eForm = document.getElementById('north');
    }else return false;
    if(!eForm) return false;
    isInitialized=true;
    getCookie();
    if(eForm['cook']){
	eForm['cook'].parentNode.style.display = 'none';
    }
    changeOption();
    commentHistory = new CommentHistory();
    return true;
}


/*========================================================*/
// アイコンプレビュー
function iconPreview(arg){
    if(!isInitialized)return false;
    imgPreview.src=arg;
    imgPreview.title=arg;
}


/*========================================================*/
// Change Option
function changeOption(){
    if(!isInitialized)return false;
    
    myIcon.value=null;
    myIcon.isAbsolute=false;
    myIcon.surface = eForm['surface'].value;
    myIcon.surfaceIndex = eForm['surface'].selectedIndex;
    if(!eForm['opt']||!eForm['opt'].value){
	eForm['icon'].disabled=false;
    }else if(iconSetting&1&&eForm['opt'].value.match(/(^|;)absoluteIcon=([^;]*)/)){
	//絶対指定アイコン
	myIcon.value=RegExp.$2;
	myIcon.isAbsolute=true;
	eForm['icon'].disabled=true;
    }else if(iconSetting&2&&eForm['opt'].value.match(/(^|;)relativeIcon=([^;:.]*(\.[^;:.]+)*)/)){
	//相対指定アイコン
	myIcon.value=RegExp.$2;
	eForm['icon'].disabled=true;
    }else{
	eForm['icon'].disabled=false;
    }
    if(!myIcon.value)myIcon.value=eForm['icon'].value;
	
    if(myIcon.isAbsolute){
	imgPreview.src=myIcon.value;
	imgPreview.title='+'+myIcon.value;
    }else{
	imgPreview.src=iconDirectory+myIcon.value;
	imgPreview.title=iconDirectory+'+'+myIcon.value;
    }
    resetSurface();
    if(myIcon.surfaceIndex >= 0 && basepath(myIcon.surface) != basepath(myIcon.value) &&
       eForm['surface'] && eForm['surface'].options.length > myIcon.surfaceIndex)
	changeSurface(myIcon.surfaceIndex);
    else
	changeSurface(0);
    return true;
}


/*========================================================*/
// Base Path
function basepath(fullpath){
    var temp = fullpath.match(/^([^\/]*\/)*[^\/]*$/);
    return temp && temp[0] ? temp[0] : null;
}


/*========================================================*/
// 現在指定しているアイコンを取得
function getSelectingIcon(){
    if(!isInitialized)return false;
    if(!eForm['opt']||!eForm['opt'].value){
    }else if(iconSetting&1&&eForm['opt'].value.match(/(^|;)absoluteIcon=([^;]*)/)){
	//絶対指定アイコン
	return RegExp.$2
    }else if(iconSetting&2&&eForm['opt'].value.match(/(^|;)relativeIcon=([^;:.]*(\.[^;:.]+)*)/)){
	//相対指定アイコン
	return RegExp.$2
    }
    return eForm['icon'].value
}


/*========================================================*/
// 表情アイコンのリセット
function resetSurface(){
    if(!myIcon.value.match(/^(([^\/#]*\/)*[^\/#.]+)(\.[^\/#]*)#(\d+)(-\d+)?$/)){
	eForm['surface'].length=1;
	eForm['surface'].options[0].text='-';
	eForm['surface'].options[0].value=myIcon.value;
	return;
    }
    var url=RegExp.$1;
    var ext=RegExp.$3;
    var str=RegExp.$5?parseInt(RegExp.$4):0;
    var end=RegExp.$5?-parseInt(RegExp.$5):parseInt(RegExp.$4);
    eForm['surface'].length=end-str+2;
    eForm['surface'].options[0].text='-';
    eForm['surface'].options[0].value=url+ext;
    if(RegExp.$5)url=url.replace(/([1-9]\d*)$/,'');
    for(i=str;i<=end;i++){
	eForm['surface'].options[i-str+1].text=i;
	eForm['surface'].options[i-str+1].value=url+i+ext;
    }
}


/*========================================================*/
// 表情アイコンを変更
function changeSurface(index){
    if(!isInitialized)return false;
	
    if(myIcon.value!=getSelectingIcon())return changeOption();
    if(eForm['surface'].selectedIndex!=index)eForm['surface'].selectedIndex=index;
    var value=eForm['surface'].value;
	
    if(myIcon.isAbsolute){
	imgPreview.src=value;
	imgPreview.title='+'+value;
    }else{
	imgPreview.src=iconDirectory+value;
	imgPreview.title=iconDirectory+'+'+value;
    }
    return true;
}


/*========================================================*/
// 表情アイコン見本
function surfaceSample(e){
    if(!isInitialized || !document.getElementById || !top.south || !top.south.document)
	return false;
    if(!e)e = window.event;
    if(!e){
    }else if(document.all){ 
	e.returnValue = false;
    }else if(document.getElementById){
	e.preventDefault();
    }else return false;
    if(e) e.cancelBubble=true;
    
    if(e && e.type == 'click' && !document.all && !e.detail) return false;
    if(e.altKey ^ e.ctrlKey ^ e.shiftKey){
	return showCommandWindow(e);
    }
    
    var myDocument = top.south.document;
    if(myIcon.value!=getSelectingIcon())changeOption();
    
    var surfaceWindow = myDocument.getElementById('surfaceWindow');
    if(surfaceWindow){
	surfaceWindow.parentNode.removeChild(surfaceWindow);
	surfaceWindow = null;
	eForm['body'].focus();
	return false;
    }
    
    surfaceWindow = createDivWindow({
	'id'		: 'surfaceWindow',
	'height'	: '250px',
	'width'		: '250px',
	'top'		: '20px',
	'left'		: '20px',
	'title'		: 'Surface Icon',
	'document'	: myDocument
    				});
    
    var fragment=myDocument.createDocumentFragment();
    for(i=0;i<eForm['surface'].length;i++){
	var elButton = myDocument.createElement('button');
	elButton.id='surface'+i.toString();
	elButton.style.border	= '0';
	elButton.style.margin	= '0';
	elButton.style.padding	= '0';
	elButton.style.width	= '60px';
	elButton.title=i.toString();
	elButton.onclick=function(){changeSurface(this.title)};
	var elImg = myDocument.createElement('img');
	elImg.src=myIcon.isAbsolute?eForm['surface'].options[i].value:iconDirectory+eForm['surface'].options[i].value;
	elImg.title=i?(i-1).toString():'-';
	elButton.appendChild(elImg);
	fragment.appendChild(elButton);
    }
    
    var divSurfaceList = myDocument.createElement('div');
    divSurfaceList.id			= 'surfaceList';
    divSurfaceList.style.borderWidth	= '1px';
    divSurfaceList.style.borderStyle	= 'solid';
    divSurfaceList.style.borderClor	= 'ActiveBorder';
    divSurfaceList.style.margin		= '2px';
    divSurfaceList.appendChild(fragment);
    surfaceWindow.appendChild(divSurfaceList);
    
    myDocument.body.appendChild(surfaceWindow);
    return true;
}


/*========================================================*/
// コマンドウィンドウ
function showCommandWindow(e){
    if(!isInitialized || !document.getElementById || !top.south || !top.south.document)
    	return false;
    if(!e){
    }else if(document.all){ 
	e.returnValue = false;
    }else if(document.getElementById){
	e.preventDefault();
    }else return false;
    if(e) e.cancelBubble=true;
    
    var myDocument = top.north.document;
    var eWindow = myDocument.getElementById('commandWindow');
    if(eWindow){
	eWindow.parentNode.removeChild(eWindow);
	eWindow = null;
	eForm['body'].focus();
	return false;
    }
    
    eWindow = createDivWindow({
	'id'		: 'commandWindow',
	'height'	: '5em',
	'width'		: '300px',
	'top'		: '4em',
	'left'		: '300px',
	'title'		: 'Command Window',
	'document'	: myDocument
    				});
    
    var p1= myDocument.createElement('form');
    p1.style.margin	= '0 2px';
    eWindow.appendChild(p1);
    
    var lbCommand = myDocument.createElement('label');
    lbCommand.htmlFor = 'commandLine';
    lbCommand.title	= "Try `help' for information.";
    lbCommand.appendChild( myDocument.createTextNode('Command:') );
    p1.appendChild(lbCommand);
    
    var eCommandLine = myDocument.createElement('input');
    eCommandLine.id		= 'commandLine';
    eCommandLine.style.width	= '150px';
    eCommandLine.type		= 'text';
    eCommandLine.onkeypress	= function(e){
	var keyCode;
	if(!e)e = window.event;
	if(document.all){
	    keyCode = e.keyCode;
	}else if(document.getElementById){
	    keyCode = e.which;
	}else return true;
	
	switch(keyCode){
	case 13:
	   eCommandSubmit.click();
	   return false;
	case 27:
	   eWindow.close();
	   break;
	}
    };
    lbCommand.appendChild(eCommandLine);
    
    var eCommandSubmit = myDocument.createElement('input');
    eCommandSubmit.id		= 'commandSubmit';
    eCommandSubmit.type		= 'button';
    eCommandSubmit.value	= 'OK';
    eCommandSubmit.onclick = function(){
	var command = eCommandLine.value;
	var temp = '';
	switch(command){
	case '?':
	case 'help':
	case 'usage':
	   alert(
		 "help:		show this help\n" +
		 "status:		show status\n" +
		 "cookie show:	show cookie\n" +
		 "cookie set:		set current information for cookie\n" +
		 "export:		export current information\n" +
		 "import:		import information from string\n" +
		 "version:		show current revision",
		 "quit:			close this window"
		);
	   break;
	case 'status':
	   status = navigator.userAgent;
	   break;
	case 'cookie show':
	case 'show cookie':
	   prompt('document.cookie is :', document.cookie);
	   break;
	case 'cookie set':
	case 'set cookie':
	   setCookie();
	   break;
	case 'export':
	   if(temp = exportInfo()){
	       prompt('Exported Information:', temp);
	   }else{
	       alert("Cookieが未設定です");
	   }
	   break;
	case 'import':
	   if(temp = prompt('Import Information?',document.cookie)) return false;
	   if(importInfo(temp)){
	       alert("インポートされました");
	   }else{
	       alert("正しく情報が入力されていません");
	   }
	   break;
	case 'version':
	   alert(
		 MARLDIA_CORE_ID + "\n"+
		 "$Id: Marldia.js,v 1.5 2006-03-11 09:33:00 naruse Exp $");
	   break;
	case 'exit':
	case 'quit':
	   eWindow.close();
	   break;
	default:
	   alert('Command "' + command + '" is undefined');
	   break;
	}
	eCommandLine.value = '';
	eCommandLine.focus();
    };
    p1.appendChild(eCommandSubmit);
    
    myDocument.body.appendChild(eWindow);
    eCommandLine.focus();
    return false;
}


/*========================================================*/
// Create Div Window
function createDivWindow(option){
    if(option['id'] && option['width'] && option['height'] &&
       (option['top'] || option['bottom']) && (option['left'] || option['right']) &&
       option['document']){
    }else return null;
    var w = option['document'].createElement('div');
    w.id			= option['id'];
    w.style.backgroundColor	= 'Window';
    w.style.borderWidth		= '1px';
    w.style.borderStyle		= 'solid';
    w.style.borderColor		= 'ActiveBorder';
    w.style.color		= 'WindowText';
    w.style.height		= option['height'];
    w.style.width		= option['width'];
    if(option['top']){
	w.style.top		= option['top'];
    }else{
	w.style.bottom		= option['bottom'];
    }
    if(option['left']){
	w.style.left		= option['left'];
    }else{
	w.style.right		= option['right'];
    }
    w.style.position		= document.all ? 'absolute' : 'fixed';
    w.style.overflow		= 'auto';
    w.style.textAlign		= 'left';
    
    if(option['title']){
	var dCaption = option['document'].createElement('div');
	dCaption.style.backgroundColor	= 'ActiveCaption';
	dCaption.style.color		= 'CaptionText';
	dCaption.style.fontFamily	= 'Caption';
	dCaption.style.height		= '1em';
	dCaption.style.margin		= '0 0 0.5em 0';
	dCaption.style.padding		= '2px';
	w.appendChild(dCaption);
	
	dCaption.appendChild( option['document'].createTextNode(option['title']) );
	
	var dTitleR = option['document'].createElement('div');
	dTitleR.style.backgroundColor	= 'InactiveCaption';
	dTitleR.style.color		= 'InactiveCaptionText';
	dTitleR.style.height		= '1em';
	dTitleR.style.margin		= '0';
	dTitleR.style.padding		= '2px';
	dTitleR.style.position		= 'absolute';
	dTitleR.style.right		= '0px';
	dTitleR.style.textAlign		= 'right';
	dTitleR.style.top		= '0px';
	dTitleR.style.width		= '20%';
	dCaption.appendChild(dTitleR);
	
	var sClose = option['document'].createElement('span');
	sClose.style.backgroundColor	= 'InactiveCaption';
	sClose.style.color		= 'InactiveCaptionText';
	sClose.style.borderColor	= 'InactiveCaptionText';
	sClose.style.borderStyle	= 'solid';
	sClose.style.borderWidth	= '1px';
	sClose.style.cursor		= 'default';
	sClose.style.height		= '1em';
	sClose.style.margin		= '0';
	sClose.style.padding		= '0';
	sClose.style.width		= '1em';
	sClose.onmouseover		= function(e){
	    sClose.style.borderColor	= 'CaptionText';
	    sClose.style.color		= 'CaptionText';
	    return true;
	};
	sClose.onmouseout		= function(e){
	    sClose.style.borderColor	= 'InactiveCaptionText';
	    sClose.style.color		= 'InactiveCaptionText';
	    return true;
	};
	sClose.onclick		= function(){
	    w.style.diaplay = 'none';
	    w.parentNode.removeChild(w);
	    return false;
	};
	w.close = sClose.onclick;
	dTitleR.appendChild(sClose);
	sClose.appendChild( option['document'].createTextNode('×') );
    }
    
    return w;
}


/*========================================================*/
// Switch Body Form Type
function switchBodyFormType(e){
    bodyContainer.removeChild(bodyContainer.firstChild);
    if(bodySwitch.value=='↓'){
	bodySwitch.value='←';
	eForm['body'] = document.createElement('TEXTAREA');
	eForm['body'].setAttribute('rows','0');
    }else{
	bodySwitch.value='↓';
	eForm['body'] = document.createElement('INPUT');
	eForm['body'].type="text";
	eForm['body'].setAttribute('maxlength','300');
	eForm['body'].setAttribute('size','100');
	eForm['body'].onkeydown = getChatHistoryByKey;
	eForm['body'].onmousewheel = getChatHistoryByMouseWheel;
    }
    eForm['body'].setAttribute('id','body');
    eForm['body'].setAttribute('name','body');
    eForm['body'].setAttribute('tabindex','1');
    eForm['body'].style.imeMode = 'active';
    eForm['body'].style.width = '400px';
    eForm['body'].className="text";
    bodyContainer.insertBefore(eForm['body'],bodyContainer.firstChild);
    return false;
}


/*========================================================*/
// Comment History
function CommentHistory(){
    this.array = new Array('');
    this.index = 0;
    if(!this.array.push)
	return null;
}
if(CommentHistory.prototype){
    CommentHistory.prototype.index = function(){
	return this.index;
    };
    CommentHistory.prototype.length = function(){
	return this.array.length;
    };
    CommentHistory.prototype.isLast = function(){
	return this.index == this.array.length-1;
    };
    CommentHistory.prototype.before = function(){
	if(this.index<1){
	    this.index = 0;
	    return null;
	}else{
	    this.index--;
	    return this.array[this.index];
	}
    };
    CommentHistory.prototype.next = function(){
	if( this.index > this.array.length-2 ){
	    this.index = this.array.length - 1;
	    return null;
	}else{
	    this.index++;
	    return this.array[this.index];
	}
    };
    CommentHistory.prototype.last = function(){
	this.index = this.array.length - 1;
	return this.array[this.index];
    };
    CommentHistory.prototype.set = function(str){
	if(this.index<1||this.array.length==0){
	    this.index = 0;
	}else if( this.index > this.array.length-2 ){
	    this.index = this.array.length - 1;
	}
	this.array[this.index] = str;
	return;
    };
    CommentHistory.prototype.push = function(str){
	if( this.array.length >= maxHistory  ){
	    this.array.shift();
	    this.before();
	}
	this.array.push(str);
	this.index = this.array.length - 1;
	return this.array[this.index];
    };
}


/*========================================================*/
// Get Chat History By Key
function getChatHistoryByKey(e){
    var keyCode;
    if(!e)e = window.event;
    if(document.all){
	keyCode = e.keyCode;
    }else if(document.getElementById){
	keyCode = e.which;
    }else return true;
    
    if(keyCode==38||keyCode==40){
	if(e.altKey||e.ctrlKey||e.shiftKey||e.modifiers){
	    return false;
	}else{
	    getChatHistory(keyCode-39);
	}
    }else if(keyCode==13){
	if(e.altKey||e.ctrlKey||e.shiftKey||e.modifiers){
	    if(document.all){
		e.returnValue=false;
	    }else if(document.getElementById){
		e.preventDefault();
	    }else return false;
	    eForm['body'].value += "\n";
	    return false;
	}
    }
    return true;
}


/*========================================================*/
// Get Chat History By Mouse Wheel
function getChatHistoryByMouseWheel(e){
    var keyCode;
    if(!e)e = window.event;
    if(commentHistory && (document.all || document.getElementById)){
    }else return true;
	
    if(!e.wheelDelta)return true;
	
    getChatHistory( e.wheelDelta >= 120 ? -1 : 1);
    return;
}


/*========================================================*/
// Get Chat History
function getChatHistory(count){
    if(!commentHistory || !eForm['body']) return true;
    if( commentHistory.isLast() ){
	commentHistory.set(eForm['body'].value)
    }
    var str = count > 0 ? commentHistory.next() : commentHistory.before();
    if( str != null ){
	eForm['body'].value = str;
    }
    return;
}


/*========================================================*/
// Import Cookie
function importInfo(str){
    if(str && str.match); else return false;
    var matched = str.match(/(^|; )Marldia1=([^;]+)/);
    if(matched && matched[2]); else return false;
    var hash = IrDr.load(matched[2]);
    if(typeof(hash) != 'object') return false;
    return hash;
}


/*========================================================*/
// Get Cookie
function getCookie(){
    var hash = importInfo(document.cookie);
    if(hash){
	for(var key in hash){
	    if(eForm[key]){
		eForm[key].value = hash[key];
	    }
	}
    }
    if(eForm['color'] && eForm['color'].value)
	eForm['color'].style.color = eForm['color'].value;
    if(eForm['bcolo'] && eForm['bcolo'].value)
	eForm['bcolo'].style.color = eForm['bcolo'].value;
}


/*========================================================*/
// Export Cookie
function exportInfo(){
    var hash = {
	'name'		: eForm['name'].value,
	'id'		: eForm['id'].value,
	'email'		: eForm['email'].value,
	'home'		: eForm['home'].value,
	'icon'		: eForm['icon'].value,
	'color'		: eForm['color'].value,
	'bcolo'		: eForm['bcolo'].value,
	'line'		: eForm['line'].value,
	'reload'	: eForm['reload'].value,
	'surface'	: eForm['surface'].value,
	'surfaceIndex'	: eForm['surface'].selectedIndex,
	'opt'		: eForm['opt'].value
    };
    var expires = new Date((new Date()).getTime()+2*365*24*60*60*1000);
    var cookiePath = '';
    var cookieDomain = '';
    var cookieSecure = false;
    var cookie = "Marldia1=" + IrDr.save(hash) +
        ((expires) ? "; expires=" + expires.toGMTString() : "") +
        ((cookiePath) ? "; path=" + cookiePath : "") +
        ((cookieDomain) ? "; domain=" + cookieDomain : "") +
        ((cookieSecure) ? "; secure" : "");
    return cookie;
}


/*========================================================*/
// Set Cookie
function setCookie(){
    var cookie = exportInfo();
    if(cookie) document.cookie = cookie;
    return;
}
