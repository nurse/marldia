/* Marldia JavaScriptLibrary */
/* $Id: script.js,v 1.1 2001-10-21 12:27:17 naruse Exp $ */
function reset(){
  self.document.north.cook.checked=false;
  self.document.north.mes.value="";
  self.document.north.mes.select();
  self.document.north.mes.focus();
}
function IconPreview(arg){
  document.images["Preview"].src=arg;
}
//‰Šúİ’è
reset();
