/*========================================================*/
// Marldia.js
// encoding="euc-jp"
/* $Id: Marldia.js,v 1.3 2005-03-11 18:47:23 naruse Exp $ */
var ckCookie;
var imgPreview;
var lbSurface;
var lbIcon;
var tbOption;
var bodyContainer;
var bodySwitch;
var nameColor;
var bodyColor;
var eForm;
var chatHistory = new Array;
var currentHistoryIndex = 0;
var maxHistory = 100;
var popup;
var isLoaded=null;

/*========================================================*/
// Init
function init(){
	if(document.all){
		ckCookie=document.all('cook');
		imgPreview=document.all('preview');
		lbSurface=document.all('surface');
		lbIcon=document.all('icon');
		tbOption =document.all('opt');
		bodyContainer=document.all('bodyContainer');
		bodySwitch=document.all('bodySwitch');
		nameColor = document.all('color');
		bodyColor = document.all('bcolo');
		eForm = document.all('north');
	}else if(document.getElementById){
		ckCookie=document.getElementById('cook');
		imgPreview=document.getElementById('preview');
		lbSurface=document.getElementById('surface');
		lbIcon=document.getElementById('icon');
		tbOption =document.getElementById('opt');
		bodyContainer=document.getElementById('bodyContainer');
		bodySwitch=document.getElementById('bodySwitch');
		nameColor = document.getElementById('color');
		bodyColor = document.getElementById('bcolo');
		eForm = document.getElementById('north');
	}else return false;
	isLoaded=true;
	autoreset();
	changeOption();
	nameColor.style.color = nameColor.value;
	bodyColor.style.color = bodyColor.value;
	return true;
}


/*========================================================*/
// Auto Reset
function autoreset(){
	if(!isLoaded)return false;
	if(ckCookie)ckCookie.checked=document.cookie?false:true;
	if(eForm&&eForm['identity']&&eForm['name']){
		if(!eForm['identity'].value&&eForm['name'].value){
			eForm['identity'].value = eForm['name'].value;
		}
	}
	var newBody = bodyContainer.firstChild;
	if(newBody){
		if(maxHistory>0&&newBody.value){
			while(chatHistory.length>0&&!chatHistory[chatHistory.length-1])
				chatHistory.pop();
			chatHistory.push(newBody.value);
			if(chatHistory.length>=maxHistory)
				chatHistory.splice(0,1+chatHistory.length-maxHistory);
			currentHistoryIndex = chatHistory.length;
			chatHistory[currentHistoryIndex] = '';
		}
		newBody.value='';
		newBody.focus();
	}else if(newBody = document.all('body')){
		newBody.value='';
		newBody.focus();
	}
}


/*========================================================*/
// アイコンプレビュー
function iconPreview(arg){
	if(!isLoaded)return false;
	imgPreview.src=arg;
	imgPreview.title=arg;
}


/*========================================================*/
// Change Option
function changeOption(){
	if(!isLoaded)return false;
	
	myIcon.value=null;
	myIcon.isAbsolute=false;
	if(!tbOption||!tbOption.value){
		lbIcon.disabled=false;
	}else if(iconSetting&1&&tbOption.value.match(/(^|;)absoluteIcon=([^;]*)/)){
		//絶対指定アイコン
		myIcon.value=RegExp.$2;
		myIcon.isAbsolute=true;
		lbIcon.disabled=true;
	}else if(iconSetting&2&&tbOption.value.match(/(^|;)relativeIcon=([^;:.]*(\.[^;:.]+)*)/)){
		//相対指定アイコン
		myIcon.value=RegExp.$2;
		lbIcon.disabled=true;
	}else{
		lbIcon.disabled=false;
	}
	if(!myIcon.value)myIcon.value=lbIcon.value;
	
	if(myIcon.isAbsolute){
		imgPreview.src=myIcon.value;
		imgPreview.title='+'+myIcon.value;
	}else{
		imgPreview.src=iconDirectory+myIcon.value;
		imgPreview.title=iconDirectory+'+'+myIcon.value;
	}
	
	lbSurface.selectedIndex=0;
	resetSurface();
	return true;
}


/*========================================================*/
// 現在指定しているアイコンを取得
function getSelectingIcon(){
	if(!isLoaded)return false;
	if(!tbOption||!tbOption.value){
	}else if(iconSetting&1&&tbOption.value.match(/(^|;)absoluteIcon=([^;]*)/)){
		//絶対指定アイコン
		return RegExp.$2
	}else if(iconSetting&2&&tbOption.value.match(/(^|;)relativeIcon=([^;:.]*(\.[^;:.]+)*)/)){
		//相対指定アイコン
		return RegExp.$2
	}
	return lbIcon.value
}


/*========================================================*/
// 表情アイコンのリセット
function resetSurface(){
	if(!myIcon.value.match(/^(([^\/#]*\/)*[^\/#.]+)(\.[^\/#]*)#(\d+)(-\d+)?$/)){
		lbSurface.length=1;
		lbSurface.options[0].text='-';
		lbSurface.options[0].value=myIcon.value;
		return;
	}
	var url=RegExp.$1;
	var ext=RegExp.$3;
	var str=RegExp.$5?parseInt(RegExp.$4):0;
	var end=RegExp.$5?-parseInt(RegExp.$5):parseInt(RegExp.$4);
	lbSurface.length=end-str+2;
	lbSurface.options[0].text='-';
	lbSurface.options[0].value=url+ext;
	if(RegExp.$5)url=url.replace(/([1-9]\d*)$/,'');
	for(i=str;i<=end;i++){
		lbSurface.options[i-str+1].text=i;
		lbSurface.options[i-str+1].value=url+i+ext;
	}
}


/*========================================================*/
// 表情アイコンを変更
function changeSurface(index){
	if(!isLoaded)return false;
	
	if(myIcon.value!=getSelectingIcon())return changeOption();
	if(lbSurface.selectedIndex!=index)lbSurface.selectedIndex=index;
	var value=lbSurface.value;
	
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
	if(!isLoaded)return false;
	if(myIcon.value!=getSelectingIcon())changeOption();
	if(document.all){
		e.returnValue=false;
	}else if(document.getElementById){
		e.preventDefault();
	}else return false;
	e.cancelBubble=true;
	if(!top.south)return false;
	if(!window.createPopup)return false;
	event.cancelBubble=true;
	if(popup&&popup.isOpen){
		popup.hide();
		var newBody = bodyContainer.firstChild;
		newBody.focus();
		return false;
	}
	popup=window.createPopup();
	var intWidth =200;
	var intHeight=250;
	
	var fragment=popup.document.createDocumentFragment();
	for(i=0;i<lbSurface.length;i++){
		var elButton=popup.document.createElement('BUTTON');
		elButton.id='surface'+i.toString();
		elButton.style.margin='0';
		elButton.style.padding='0';
		elButton.style.width='50px';
		elButton.style.border='0';
		elButton.title=i.toString();
		elButton.onclick=function(){changeSurface(this.title)};
		var elImg=popup.document.createElement('IMG');
		elImg.src=myIcon.isAbsolute?lbSurface.options[i].value:iconDirectory+lbSurface.options[i].value;
		elImg.title=i?(i-1).toString():'-';
		elButton.appendChild(elImg);
		fragment.appendChild(elButton);
	}
	
	var div1=popup.document.createElement('DIV');
	div1.style.border='3px double ActiveBorder';
	div1.style.height=intHeight.toString()+'px';
	div1.style.overflow='auto';
	div1.style.textAlign='left';
	div1.style.width=intWidth.toString()+'px';
	popup.document.body.appendChild(div1);
	
	var p1=popup.document.createElement('P');
	p1.appendChild(popup.document.createTextNode('アイコン見本'));
	p1.style.color	='CaptionText';
	p1.style.font	='caption';
	p1.style.height	='15px';
	p1.style.padding='2px';
	p1.style.width	='100%';
	p1.style.filter	="progid:DXImageTransform.Microsoft.Gradient("
		+"startColorstr='#66aaff',endColorstr='#ffffff',gradientType='1')";
	div1.appendChild(p1);
	
	var divSurfaceList=popup.document.createElement('DIV');
	divSurfaceList.id='surfaceList';
	divSurfaceList.appendChild(fragment);
	div1.appendChild(divSurfaceList);
	
	var p2=popup.document.createElement('P');
	div1.appendChild(p2);
	
	var bt1=popup.document.createElement('INPUT');
	bt1.type='button';
	bt1.value='Close';
	bt1.onclick=function(){imgPreview.click()};
	p2.appendChild(bt1);
	
	popup.show(20,20,intWidth,intHeight,top.south.document.body);
	return true;
}


/*========================================================*/
// Switch Body Form Type
function switchBodyFormType(e){
	bodyContainer.removeChild(bodyContainer.firstChild);
	var newBody;
	if(bodySwitch.value=='↓'){
		bodySwitch.value='←'
		newBody = document.createElement('TEXTAREA');
		newBody.setAttribute('rows','0');
	}else{
		bodySwitch.value='↓'
		newBody = document.createElement('INPUT');
		newBody.type="text";
		newBody.setAttribute('maxlength','300');
		newBody.setAttribute('size','100');
		newBody.onkeydown = getChatHistoryByKey;
		newBody.onmousewheel = getChatHistoryByMouseWheel;
	}
	newBody.setAttribute('id','body');
	newBody.setAttribute('name','body');
	newBody.setAttribute('tabindex','1');
	newBody.style.imeMode = 'active';
	newBody.style.width = '400px';
	newBody.className="text";
	bodyContainer.insertBefore(newBody,bodyContainer.firstChild);
	return false;
}

/*========================================================*/
// Get Chat History By Key
function getChatHistoryByKey(e){
	var keyCode;
	if(document.all){
		e = event;
		keyCode = e.keyCode;
	}else if(document.getElementById){
		keyCode = e.which;
	}else return true;
	if(e.altKey||e.ctrlKey||e.shiftKey||e.modifiers){
		return true;
	}else if(keyCode==38||keyCode==40){
		getChatHistory(keyCode-39);
		return false;
	}
	return true;
}


/*========================================================*/
// Get Chat History By Mouse Wheel
function getChatHistoryByMouseWheel(e){
	var keyCode;
	if(document.all){
		e = event;
	}else if(document.getElementById){
	}else return true;
	
	if(!e.wheelDelta)return true;
	
	getChatHistory( e.wheelDelta >= 120 ? -1 : 1);
	return;
}


/*========================================================*/
// Get Chat History
function getChatHistory(count){
	if(!chatHistory.length)return true;
	var newBody = bodyContainer.firstChild;
	if(!newBody)return true;
	status = 'currentHistoryIndex:' + currentHistoryIndex + ' ';
	status += 'chatHistory.length:' + chatHistory.length + ' ';
	if(newBody.value||newBody.value=="")
		chatHistory[currentHistoryIndex] = newBody.value;
	currentHistoryIndex += count;
	if(currentHistoryIndex < 0){
		currentHistoryIndex = 0;
	}else if(currentHistoryIndex >= chatHistory.length){
		currentHistoryIndex = chatHistory.length-1;
	}
	newBody.value = chatHistory[currentHistoryIndex];
	return;
}
