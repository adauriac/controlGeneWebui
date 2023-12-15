/* pour forcer le chargement de DOMContentLoaded avant de faire quoique ce soit */

document.addEventListener("DOMContentLoaded", () => {
    console.log("hi 2")
    let elt = document.getElementById("plasma3")
    console.log(elt)
    console.log(elt.style)
    elt.style.background = "red"

    elt = document.getElementById("powerMeasure")
    console.log(elt.innerHTML)
    elt.innerHTML = "Set fromjs"

    function my_function(e) {
	webui.call('my_function', e);
    }

    const pll = document.getElementById("powerLowLimit");
    pll.addEventListener("change", my_function);
    pll.addEventListener("click", my_function);
});
