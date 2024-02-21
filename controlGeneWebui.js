/* pour forcer le chargement de DOMContentLoaded avant de faire quoique ce soit */

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
/*
  At all watchog function called, frequency set by setInterval()
  the 6+3 values possibly changed by the gui :
  3 for power : low high target
  3 for flow : low high target
  3 boutons : generator, gaz, plasma
  are tested to be consistent a string is constructed with the consistent ones and is
  sent to the backend in python. If no error 9*2 values are sent.

  In return from the python backend the values of all registers in received.
  The gui is refreshed accordingly
*/
const elements = [];
const elementsNew = [];
let parametresToSend = "";
let newValues = 0;

function refresh () { // called when the button is clicked
    newValues = 1; /* to tell watchdogFunctionJS to send the new values */
}

function isStringAnInteger(str) {
  return !isNaN(str) && Number.isInteger(parseFloat(str));
}

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
    
    function treatAnswer(answer) {
    }     // FIN     function treatAnswer() {
    // *************************************************************************

    function prepareParam(){
	// For the 6 values corresponding to flow and power, check if low <= consigne <= high
	// if ok return a string setting value format "registerAdd registerValue ..."
	// else return an empty string
	// if there is an incompatibility ALL NEW VALUES ARE DISREGARDED not only the wrong ones
	param = "";
	for(let i=0;i<elements.length;i++) {
	    if (elements[i]==elementsNew[i])
		continue;
	    // from here the element is GUI modifiable
	    val = elementsNew[i].value;
	    if (val == "") { // the filed on the gui is empty
		val = elements[i].innerHTML;
	    }
	    if (!isStringAnInteger(val)) {
		alert(val+" is not a number");
		elementsNew[i].value = "";
		return "";
	    }
	    param += " " + ou[i] + " " + val;
	    // P->puissance D->debit L->limite C->consigne
	    if (ou[i] == 0x96)
		PLB = parseInt(val);
	    else if (ou[i] == 0x97)
		PLH = parseInt(val);
	    else if (ou[i] == 0xA0)
		DLB = parseInt(val);
	    else if (ou[i] == 0xA1)
		DLH = parseInt(val);
	    else if (ou[i] == 0xB2)
		PC = parseInt(val);
	    else if (ou[i] == 0xB3)
		DC = parseInt(val);
	}

	console.log("PLB",PLB," PLH",PLH," PC",PC);
	console.log("DLB",DLB," DLH",DLH," DC",DC);
	// verification des bornes
	let wrong=0;
	if (PLB>PLH) {
	    wrong += 1;
	    alert("Limits of power not compatible");
	}
	if (DLB>DLH) {
	    wrong += 10;
	    alert("Limits of flow not compatible");
	}
	if ((PC<PLB) || (PC>PLH)) {
	    wrong += 100;
	    alert("Power target out of bonds");
	}
	if ((DC<DLB) || (DC>DLH)) {
	    wrong += 1000;
	    alert("flow target out of bonds");
	}
	if (wrong==0)
	    return param;
	// here an error was found
	for(let i=0;i<elements.length;i++) {
	    if (elements[i]==elementsNew[i])
		continue;
	    elementsNew[i].value = "";
	}
	return "";
    }    // FIN    function prepareParam(){
    // ******************************************************************
    
    function watchdogFunctionJS(e) {
	/* blink !*/
	if (eltTemoin.style.visibility == "visible") 
	    eltTemoin.style.visibility = "hidden"
	else
	    eltTemoin.style.visibility = "visible"
	/*   PREPARE THE PARAMETERS TO SEND TO PYTHON  */
	let param = "";
	if (newValues) {
	    newValues = 0;
	    param = prepareParam();
	}
	// console.log("MyFunctionJS says: param for webui.call=",param)
	webui.call('myFunction',param).then((response)=> {
	    /*  PROCCESSING THE RETURN OF THE PYTHON FUNCTION */
	    // console.log("watchdogFunctionJS L 124 I receveid ",response)
	    alert("response "+response)
	    responseSplitted = response.split(" ");
	    for (let i=0;i<responseSplitted.length;i+=2) {
		let add = Number(responseSplitted[i]);
		let val = responseSplitted[i+1];
		if (!lesIndex.has(add))
		    alert("oops JS recevied "+add+" an unknown register address")
		let k = lesIndex.get(add);
		// console.log("watchdogFunctionJS L 133 add=",add," val=",val," k=",k)
		if (elements[k].classList.contains("labelOutput")){
		    elements[k].innerHTML = val;
		}
		else if (elements[k].classList.contains("inputCell")) {
		    elements[k].classList;/*.value = responseSplitted[i+1];*/
		}
		else if ((elements[k].classList.contains("boutonLed")) ||
			 (elements[k].classList.contains("led"))){
		    elements[k].classList.remove("on")
		    elements[k].classList.remove("off")
		    //  la couleur grise de defaut 
		    if (val==0) {
			elements[k].classList.add("off");
		    }
		    else if (val==0x7f7f) {
			elements[k].classList.add("on");
		    }
		}
		else
		    alert("Internal impossible error");
	    }
	});
    } // FIN     function watchdogFunctionJS(e) 

    /* pll.addEventListener("change", my_function);*/
    // pll.addEventListener("click", my_function);
    newValues = 0;
    //setTimeout(watchdogFunctionJS,500); // un seul appel
    setInterval(watchdogFunctionJS,500*2); // appel recurent
});
