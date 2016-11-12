function showHideDiv(elemId) {
    var div = document.getElementById(elemId)
    if (div.style.display !== 'none') {
        div.style.display = 'none';
    } else {
        div.style.display = 'block';
    }
}
