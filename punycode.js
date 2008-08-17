/* $Id$ */
/*　
 * = Punycode for JavaScript
 * 
 * == Abstract
 * 
 * read RFC.
 * http://www.ietf.org/rfc/rfc3492.txt
 * 
 * == Usage
 * 
 * --- Punycode.encode( text )
 * 
 *     encode text to punycode.
 * 
 *      Punycode.encode("\u004D\u0061\u006A\u0069\u3067\u004B\u006F\u0069\u3059\u308B\u0035\u79D2\u524D");
 *      // => 'MajiKoi5-783gue6qz075azm5e'
 * 
 * --- Punycode.decode( punycode )
 * 
 *     decode punycode to text.
 * 
 *      Punycode.encode('MajiKoi5-783gue6qz075azm5e');
 *      // => "\u004D\u0061\u006A\u0069\u3067\u004B\u006F\u0069\u3059\u308B\u0035\u79D2\u524D"
 * 
 * --- Punycode.test( punycode )
 * 
 *     test this software.
 * 
 * Copyright (c)2005 Airemix. All rights reserved.
 * 
 * This software is licensed under BSDL.
 * 
 */
function Punycode()
{
    var MAXINT = 0x7fffffff;
    var BASE = 36;
    var TMIN = 1;
    var TMAX = 26;
    var SKEW = 38;
    var DAMP = 700;
    var INITIAL_BIAS = 72;
    var INITIAL_N = 0x80;
    var DELIMITER = 0x2D;
  
    /* basic(cp) tests whether cp is a basic code point: */
    function basic(cp){
	return cp < 0x80;
	// ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@*_+-./
    }
  
    function decode_digit(cp){
	return  cp < 58 ? cp - 22 :  cp < 91 ? cp - 65 : cp < 123 ? cp - 97 :  BASE;
    }
  
    function encode_digit(d){
	return d < 26 ? d + 97 : d + 22;
    }
  
    /*** Bias adaptation function ***/
    function adapt(delta, numpoints, firsttime){
	var k;
	delta = firsttime ? parseInt(delta / DAMP) : delta >> 1;
	delta += parseInt(delta / numpoints);
	for (k = 0;  delta > ((BASE - TMIN) * TMAX) >> 1;  k += BASE) {
	    delta = parseInt(delta / (BASE - TMIN));
	}
	return parseInt(k + (BASE - TMIN + 1) * delta / (delta + SKEW));
    }
  
    /*** Main encode function ***/
    function encode(input){
	if(typeof(input)=='string'){
	    var str = input;
	    input = new Array;
	    for(var i=0; i< str.length; i++)
		input.push(str.charCodeAt(i));
	}
	var output = _encode( input );
	for (var j = 0;  j < output.length;  ++j) {
	    var c = output[j];
	    if(c >= 0 && c <= 127); else break;
	    output[j] = String.fromCharCode(c);
	}
	return output.join('');
    }
    Punycode.encode = encode;
  
    function _encode( input ){
	var output = new Array;
	var n = INITIAL_N;
	var delta = 0;
	var bias = INITIAL_BIAS;
	var input_length = input.length;
	
	var temp = [];
	for(var j = 0;  j < input_length;  ++j){
	    if (basic(input[j])) output.push(input[j]);
	    else temp.push(input[j]);
	}
	var sorted = temp.sort(function(a,b){return a==b ? 0 : a>b ? 1 : -1});
	temp = [];
	for(var j = 0;  j < sorted.length;  ++j){
	    if(temp[temp.length-1] != sorted[j]) temp.push(sorted[j]);
	}
	sorted = temp;
	var bcp = output.length;
	var handled = bcp;
	if (bcp > 0) output.push(DELIMITER);
	
	while (handled < input_length) {
	    var m = MAXINT;
	    while(sorted[0] >= n && sorted[0] < m) m = sorted.shift();
	    if (m - n > (MAXINT - delta) / (handled + 1)) throw 'overflow';
	    delta += (m - n) * (handled + 1);
	    n = m;
	    for (j = 0;  j < input.length;  ++j) {
		if (input[j] < n && ++delta == 0) throw 'overflow';
		if (input[j] == n) {
		    var q = delta;
		    for (var k = BASE;  ;  k += BASE) {
			var t = k <= bias ? TMIN : k >= bias + TMAX ? TMAX : k - bias;
			if (q < t) break;
			output.push(encode_digit(t + (q - t) % (BASE - t)));
			q = parseInt((q - t) / (BASE - t));
		    }
		    output.push(encode_digit(q));
		    bias = adapt(delta, handled + 1, handled == bcp);
		    delta = 0;
		    ++handled;
		}
	    }
	    ++delta, ++n;
	}
	return output;
    }
  
    /*** Main decode function ***/
    function decode(input)
    {
	if(typeof(input)=='string'){
	    var str = input;
	    input = new Array;
	    for(var i=0; i< str.length; i++)
		input.push(str.charCodeAt(i));
	}
	var output = _decode( input );
	for (var j = 0;  j < output.length;  ++j)
	    output[j] = String.fromCharCode(output[j]);
	return output.join('');
    }
    Punycode.decode = decode;
  
    function _decode( input )
    {
	var j;
	var output = new Array;
	var n = INITIAL_N;
	var bias = INITIAL_BIAS;
	var bcp = 0;
	
	for (j = input.length;  j >= 0;  --j)
	    if (input[j] == DELIMITER){ bcp = j; break; }
	for (j = 0;  j < bcp;  ++j) {
	    if (!basic(input[j])) throw 'bad_input';
	    output.push( input[j] );
	}
	var i = 0;
	var inp = bcp > 0 ? bcp + 1 : 0;
	while( inp < input.length ){
	    var oldi = i;
	    for (var w = 1, k = BASE;  ;  k += BASE) {
		if (inp >= input.length) throw 'bad_input';
		var digit = decode_digit(input[inp++]);
		if (digit >= BASE) throw 'bad_input';
		if (digit > (MAXINT - i) / w) throw 'overflow';
		i += digit * w;
		var t = k <= bias ? TMIN : k >= bias + TMAX ? TMAX : k - bias;
		if (digit < t) break;
		if (w > MAXINT / (BASE - t)) throw 'overflow';
		w *= (BASE - t);
	    }
	    bias = adapt(i - oldi, output.length + 1, oldi == 0);
	    oldi = parseInt(i / (output.length + 1));
	    if (oldi > MAXINT - n) throw 'overflow';
	    n += oldi;
	    i %= (output.length + 1);
	    output.splice(i++,0,n);
	}
	return output;
    }
}
new Punycode;


/*
 * =begin
 * 
 * = JSON Module
 * 
 * --- JSON::save( obj ) #=> String
 *     save object as JSON string.
 * 
 * --- JSON::load( str ) #=> obj
 *     load JSON string.
 * 
 * =end
 * 
 */

function JSON(){
    JSON.save = save;
    function save( obj ){
	var result;
	var temp = [];
	switch(typeof obj){
	case 'undefined':
	    return 'null';
	    break;
	case 'boolean':
	case 'number':
	    return obj.toString();
	    break;
	case 'string':
	    return '"' + obj.replace(/\\/g,'\\\\').replace(/"/g,'\\"') + '"';
	    break;
	case 'object':
	    if( obj == null ){
		return 'null';
	    }else if( obj instanceof(Date) ){
		return '"' + obj.getUTCFullYear() + '-' +
		    obj.getUTCMonth() + '-' +
		    obj.getUTCDay() + 'T' +
		    obj.getUTCHours() + ':' +
		    obj.getUTCMinutes() + ':' +
		    obj.getUTCSeconds() + 'Z"';
	    }else if( obj instanceof(Array) ){
		for( var i = 0; i < obj.length; i++ ){
		    temp.push(save(obj[i]));
		}
		return '[' + temp.join(',') + ']';
	    }else{
		for( i in obj ){
		    temp.push( save(i) + ':' + save(obj[i]) );
		}
		return '{' + temp.join(',') + '}';
	    }
	    break;
	default:
	    throw("#{obj.class} can't save as JSON.");
	    break;
	}
	return null;
    }
    
    JSON.load = load;
    function load( str ){
	var result = null;
	try{
	    result = eval('('+str+')');
	}catch(e){
	}
	return result;
    }
}
new JSON;

// Object Escape method with JavaScript Object Notation and Punycode and URI Escape
IrDr = new Object;
IrDr.encode = function(str){
    if(typeof str != 'string') return null;
    var temp = [];
    var array = [];
    for( var i = 0; i < str.length; i += 100 ){
	temp.push(Punycode.encode(str.substring(i,i+100))
		  .replace(/([\x00-\x20%,;\|\x7F])/g,
			   function($1){
	    var s = $1.charCodeAt().toString(16);
	    return '%'+ (s.length<2?'0':'')+s;
		       }));
    }
    return 'id0--' + temp.join('|');
}

IrDr.decode = function(str){
    if(typeof str != 'string') return null;
    if(str.substring(0,5) != 'id0--') return null;
    
    var temp = str.split('|');
    temp[0] = temp[0].substring(5);
    for( var i = 0; i < temp.length; i++ ){
	temp[i] = Punycode.decode(unescape(temp[i]));
    }
    return temp.join('');
}
IrDr.save = function(obj){
    return IrDr.encode( JSON.save( obj ) );
}
IrDr.load = function(str){
    return JSON.load( IrDr.decode( str ) );
}

if(typeof document == 'undefined'){
    if(typeof print != 'undefined'){
	//Punycode
	var source = unescape("\u004D\u0061\u006A\u0069\u3067\u004B\u006F\u0069\u3059\u308B\u0035\u79D2\u524D");
	var expect = 'MajiKoi5-783gue6qz075azm5e';
	var encoded = Punycode.encode(source);
	print(encoded);
	print('Punycode Encode: ' + (expect==encoded?'succeess':'fail'));
	var decoded = Punycode.decode(expect);
	print('Punycode Decode: ' + (source==decoded?'succeess':'fail'));
	
	//source = '　 !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ' +
	//    '[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~' + "\r\nあいうえおかきくけこ\t亜煕%21";
	
	source = {
	    'string'	: 'hoge"fu\'ga"hoge',
	    'nunmber'	: 128,
	    'date'	: Date.now(),
	    'hash'	: { 'foo' : 'bar', 'fog' : 'baz' },
	    'array'	: [ 1,2,3,'one','two','three']
	};
	print('JSON test');
	encoded = JSON.save(source);
	print(encoded);
	decoded = JSON.load(encoded);
	print(JSON.save(decoded));
	print((encoded==JSON.save(decoded)).toString());
	
	source = encoded;
	encoded = IrDr.encode(source);
	print( encoded + "\n" );
	decoded = IrDr.decode(encoded);
	print( decoded.toString() + "\n" );
	print( (source == decoded).toString() + "\n" );
	
    }
}
