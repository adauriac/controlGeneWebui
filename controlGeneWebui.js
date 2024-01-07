/* pour forcer le chargement de DOMContentLoaded avant de faire quoique ce soit */

function refresh () {
    newValues = 1; /* to tell myFunctionJS to send the new values */
    for(let k=0;k<element.length;k++) {
	if (elements[k].classList.contains("labelOutput")){
	}
	else if (elements[k].classList.contains("inputCell")) {
	    alert(element[k].value);
	}
	else if (elements[k].classList.contains("boutonLed")) {
	}
	else if (elements[k].classList.contains("led")) {
	    console.log("led "+elements[k].style.background)
	}
	else
	    alert("Internal impossible error");
    }
}
/*
   PROPOPSE PAR Hassan DRAGA POUR ATTENDRE Websocket 
document.addEventListener('DOMContentLoaded', function() {

	// DOM is loaded, and `webui` object should be available.
	webui.setEventCallback((e) => {

		if (e == webui.event.CONNECTED) {
			// Connection to the backend is established
			console.log('Connected.');
		} else if (e == webui.event.DISCONNECTED) {
			// Connection to the backend is lost
			console.log('Disconnected.');
		}
	});
});
*/

document.addEventListener("DOMContentLoaded", () => {
    console.log("hi 2");
    const lesIndex = new Map([
	[0x65,0],/* Arret d'urgence         0x65 Led */
	[0x66,1],/* Defaut critique         0x66 Led */
	[0x68,2],/* Debit mesure            0x68 Label */
	[0x6B,3],/* Puissance mesure        0x6B Label */
	[0x6E,4],/* Etat du procede         0x67 Led */
	[0x72,5],/* Tension mesure          0x72 Label */
	[0x7F,6],/* Courant mesure          0x7F Label */
	[0x96,7],/* Limite puissance basse  0x96 Input */
	[0x97,8],/* Limite puissance haute  0x97 Input */
	[0xA0,9],/* Limite debit bas        0xA0 Input */
	[0xA1,10],/* Limite debit haut      0xA1 Input */
	[0xB2,11],/* Consigne puissance     0xB2 Input */
	[0xB3,12],/* Consigne debit         0xB3 Input */
	[0xBB,13],/* Generateur             0xBB Bouton */
	[0xBC,14],/* Gaz                    0xBC Bouton */
	[0xBD,15]]);/* Plasma               0xBD Bouton */
    const ou = [];
    lesIndex.forEach(function(value,key) { ou[value] = key;});
    const elements = [];
    elements[0] = document.getElementById("arrUrg");                 /* Led */
    elements[1] = document.getElementById("defCrit");                /* Led */
    elements[2] = document.getElementById("flowMeas");               /* Label */
    elements[3] = document.getElementById("powerMeas");              /* Label */
    elements[4] = document.getElementById("etatProc");               /* Led */
    elements[5] = document.getElementById("tensionMeas");            /* Label */
    elements[6] = document.getElementById("bridgeCurMeas");          /* Label */
    elements[7] = document.getElementById("limitPuissanceBasse"); /* Input */
    elements[8] = document.getElementById("limitPuissanceHaute"); /* Input */
    elements[9] = document.getElementById("debitBas");            /* Input */
    elements[10] = document.getElementById("debitHaut");          /* Input */
    elements[11] = document.getElementById("consignePuissance");  /* Input */
    elements[12] = document.getElementById("consigneDebit");      /* Input */
    elements[13] = document.getElementById("gene");                  /* Bouton */
    elements[14] = document.getElementById("gaz");                   /* Bouton */
    elements[15] = document.getElementById("plasma");                /* Bouton */
    const elementsNew = [];
    for(let i=0;i<elements.length;i++)
	elementsNew[i] = elements[i];
    elementsNew[7] = document.getElementById("limitPuissanceBasseNew"); /* Input */
    elementsNew[8] = document.getElementById("limitPuissanceHauteNew"); /* Input */
    elementsNew[9] = document.getElementById("debitBasNew");            /* Input */
    elementsNew[10] = document.getElementById("debitHautNew");          /* Input */
    elementsNew[11] = document.getElementById("consignePuissanceNew");  /* Input */
    elementsNew[12] = document.getElementById("consigneDebitNew");      /* Input */
    
    let eltDivBoutonLed = document.getElementById("divBoutonLed");
    let eltDivConsignes = document.getElementById("divConsignes");
    let eltDivValues = document.getElementById("divValues");
    let eltGo = document.getElementById("goBtn");
    let eltTemoin = document.getElementById("temoin");
    
    /* Positionnement des 3 groupes */
    eltDivConsignes.style.left = 240+"px";
    eltDivValues.style.left = 240+"px";
    eltDivValues.style.top = 250+"px";
    eltGo.style.left = 650+"px";
    eltGo.style.top = 105+"px";
    eltTemoin.style.top = 310+"px";
    eltTemoin.style.left = 550+"px";

    function treatAnswer() {
    }     // FIN     function treatAnswer() {
    // *************************************************************************
    
    function myFunctionJS(e) {
	/* blink !*/
	if (eltTemoin.style.visibility == "visible") 
	    eltTemoin.style.visibility = "hidden"
	else
	    eltTemoin.style.visibility = "visible"
	/*   PREPARE THE PARAMETERS TO SEND TO PYTHON  */
	param = "";
	if (newValues) {
	    newValues = 0;
	    for(let i=0;i<elements.length;i++) {
		if (elements[i]==elementsNew[i])
		    continue;
		param += " " + ou[i] + " " + elementsNew[i].value;
	    }
	}
	else
	    param = "205 ?"
	// console.log(param)
	webui.call('myFunction',param).then((response)=> {
	    /*  PROCCESSING THE RETURN OF THE PYTHON FUNCTION */
	    responseSplitted = response.split(" ");
	    for (let i=0;i<responseSplitted.length;i+=2) {
		let add = Number(responseSplitted[i]);
		let val = responseSplitted[i+1];
		if (!lesIndex.has(add))
		    alert("oops JS recevied "+add+" an unknown register address")
		let k = lesIndex.get(add);
		if (elements[k].classList.contains("labelOutput")){
		    elements[k].innerHTML = responseSplitted[i+1];
		}
		else if (elements[k].classList.contains("inputCell")) {
		    continue;/*.value = responseSplitted[i+1];*/
		}
		else if (elements[k].classList.contains("boutonLed")) {
		    console.log(elements[k])
		}
		else if (elements[k].classList.contains("led")) {
		    console.log("led "+elements[k].style.background)
		}
		else
		    alert("Internal impossible error");
	    }
	});
    }

    /* pll.addEventListener("change", my_function);*/
    // pll.addEventListener("click", my_function);
    newValues = 1;
    setInterval(myFunctionJS,500);
});
