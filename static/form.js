var i = 1;
var j = 1;
function addtxxt() {
		var element = document.getElementById('block-1');
		var texts = document.createElement('TEXTAREA');

		texts.setAttribute('cols','80px');
		texts.setAttribute('rows','20'); 
		texts.setAttribute('placeholder','Your text');
		texts.setAttribute('name','textarea' + i);

		i++;

		var br = document.createElement('br');


		element.appendChild(br);
		element.appendChild(texts);

}
function removestuff(){
	var elemen = document.getElementById('block-1');
	if (elemen.childNodes.length >= 2){
	elemen.removeChild(elemen.lastChild);
	elemen.removeChild(elemen.lastChild);
	working = 0;
}
}
function loadimmg(){
	var element = document.getElementById('block-1');
	var ld = document.createElement('INPUT');

	ld.setAttribute('type','file');
	ld.setAttribute('name','imgload' + i);
	ld.setAttribute('accept','image/jpeg,image/png,image/gif');

	var br = document.createElement('br');


    i++;

	element.appendChild(br);
	element.appendChild(ld);
}