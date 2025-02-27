// add hovered class to selected list item
let list = document.querySelectorAll("#accordionSidebar li");

function activeLink() {
  list.forEach((item) => {
    item.classList.remove("hover1");
  });
  this.classList.add("hover1");
}
 
list.forEach((item) => item.addEventListener("mouseover", activeLink));

// Menu Toggle
let toggle = document.querySelector(".toggle");
let navigation_p = document.querySelector(".na_perso");
let main_p = document.querySelector(".main_p");

toggle.onclick = function () {
  navigation_p.classList.toggle("active");
  main_p.classList.toggle("active");
};
