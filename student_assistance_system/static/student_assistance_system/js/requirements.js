function showHideDiv(elemId) {
    var div = document.getElementById(elemId)
    div.style.display = div.style.display == "block" ? "none" : "block";
}
function showHideInlineElement(elemId, buttonClicked) {
    var div = document.getElementById(elemId)
    var buttonElement = document.getElementById(buttonClicked)
    console.log(buttonClicked)
    console.log(buttonElement)
    div.style.display = div.style.display == "inline" ? "none" : "inline";
    console.log(buttonElement.style.display)
    buttonElement.style.display = buttonElement.style.display == "inline-flex" ? "none" : "inline-flex";
    console.log(buttonElement)
}


