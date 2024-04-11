const searchInput = document.getElementById("inputsearchlevel");
console.log("AJGJLF LJ FLJFLJ LJF ")
console.log(searchInput)
searchInput.addEventListener("input", function (event) {
    const value = event.target.value.toLowerCase();
    //Create array with classname and then loop it the number of times the elements  :)
    const servName = document.getElementsByClassName("card-title");
    const card = document.getElementsByClassName("card_display");
    for (let i = 0; i < servName.length; i++) {
        if (servName[i].innerHTML.toLowerCase().includes(value)) {
            card[i].style.display = "initial";
        } else {
            card[i].style.display = "none";
        }
    }
});