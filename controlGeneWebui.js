/* pour forcer le chargement de DOMContentLoaded avant de faire quoique ce soit */

document.addEventListener("DOMContentLoaded", () => {
    console.log("hi 2")
    let elt = document.getElementById("plasma3")
    console.log(elt)
    console.log(elt.style)
    elt.style.background = "red"
    let eltPowerLowLimit = document.getElementById("powerLowLimit")

    function my_functionJS(e) {
	let valPowerLowLimit = eltPowerLowLimit.value
	alert("je vais faire un webui.call avec "+valPowerLowLimit);
	webui.call('my_function2', valPowerLowLimit).then((response)=> {
	    console.log(response);
	    eltPowerLowLimit.value = response
	});
    }

    const pll = document.getElementById("powerLowLimit");
    /* pll.addEventListener("change", my_function);*/
    /* pll.addEventListener("click", my_function);*/
    setInterval(my_functionJS,5000);
});
