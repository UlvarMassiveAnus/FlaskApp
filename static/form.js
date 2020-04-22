function addtxxt() {
		var element = document.getElementById('block-1');
		var texts = document.createElement('TEXTAREA');

		texts.setAttribute('cols','80');
		texts.setAttribute('rows','20'); 
		texts.setAttribute('placeholder','Your text');

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
	var ld = document.createElement('div');

	var br = document.createElement('br');


	ld.innerHTML = '<input type="file" name="img" id = "cnfr" accept="image/jpeg,image/png,image/gif">';

	element.appendChild(br);
	element.appendChild(ld);
}