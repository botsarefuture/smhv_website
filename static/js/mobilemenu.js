function toggleMobileMenu() {
    var menu = document.getElementById("mobile-menu");
    var menu1 = document.getElementById("menu1");
    var toggle = document.querySelector(".menu-toggle");
    if (menu.style.display === "block" || menu.style.display === "") {
        menu.style.display = "none";
        menu1.style.display = "block";
        toggle.classList.remove("menu-opened");
    } else {
        menu.style.display = "block";
        menu1.style.display = "none";
        toggle.classList.add("menu-opened");
    }
}