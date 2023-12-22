/* pour forcer le chargement de DOMContentLoaded avant de faire quoique ce soit */

document.addEventListener("DOMContentLoaded", () => {
    console.log("hi 2")
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
    
    /* les 6 valeurs aue le gui va envoyer a la carte */
    let consignePuissance = document.getElementById("consignePuissance");
    function my_functionJS(e) {
	if (eltTemoin.style.visibility == "visible") 
	    eltTemoin.style.visibility = "hidden"
	else
	    eltTemoin.style.visibility = "visible" 
	/* alert("je vais faire un webui.call avec "+valPowerLowLimit);*/
	/* prepare the string to send */
	let param = "";
	webui.call('my_function2', valPowerLowLimit).then((response)=> {
	    console.log(response);
	    eltPowerLowLimit.value = response
	});
    }

    const pll = document.getElementById("powerLowLimit");
    /* pll.addEventListener("change", my_function);*/
    /* pll.addEventListener("click", my_function);*/
    setInterval(my_functionJS,1000);
});
