i = 1;
j = 1;

function addtxxt() {
		var element = document.getElementById('block-1');

		var texts = document.createElement('TEXTAREA');
		var br = document.createElement('br');
		var br2 = document.createElement('br');

		var rght  = document.createElement('input');
		var wrn1 = document.createElement('input');
		var wrn2 = document.createElement('input');
		var wrn3 = document.createElement('input');


		texts.setAttribute('cols','88');
		texts.setAttribute('rows','5'); 
		texts.setAttribute('placeholder','Текст вопроса');
		texts.setAttribute('name','qst'+i);

		wrn1.setAttribute('type','text');
		wrn2.setAttribute('type','text');
		wrn3.setAttribute('type','text');

		wrn1.setAttribute('class','mr-1');
		wrn2.setAttribute('class','mr-1');
		wrn3.setAttribute('class','mr-1');

		wrn1.setAttribute('name','wrn'+j+'-'+i);
		j++;
		wrn2.setAttribute('name','wrn'+j+'-'+i);
		j++;
		wrn3.setAttribute('name','wrn'+j+'-'+i);
		j++;

		rght.setAttribute('type','text');
		rght.setAttribute('value','Правильный ответ');
		rght.setAttribute('class','rght');
		rght.setAttribute('name','rgh'+j+'-'+i);
		
		element.appendChild(texts);
		element.appendChild(br);
		element.appendChild(wrn1);
		element.appendChild(wrn2);
		element.appendChild(wrn3);
		element.appendChild(rght);
		element.appendChild(br2);
		i++;
		j = 1;
}
function removestuff(){
	var elemen = document.getElementById('block-1');
	if (elemen.childNodes.length >= 7){
	elemen.removeChild(elemen.lastChild);
	elemen.removeChild(elemen.lastChild);
	elemen.removeChild(elemen.lastChild);
	elemen.removeChild(elemen.lastChild);
	elemen.removeChild(elemen.lastChild);
	elemen.removeChild(elemen.lastChild); 
	elemen.removeChild(elemen.lastChild);
	
}
}