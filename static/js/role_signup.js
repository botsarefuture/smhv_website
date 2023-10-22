// Lisää klikkitapahtuman kuuntelija jokaiseen roolilaatikkoon
document.querySelectorAll(".role").forEach(function (box) {
  // Kun roolilaatikkoa klikataan, vaihda valintaruutu ja sovella tyylejä
  box.addEventListener("click", function () {
    const checkbox = box.querySelector(".custom-checkbox");
    checkbox.checked = !checkbox.checked;
    box.classList.toggle("selected", checkbox.checked);
  });

  var open = false;

  box.querySelector(".view-more-button").addEventListener("click", toggleText);
  box.querySelector(".role-description").addEventListener("click", toggleText);

  function toggleText() {
    var description = box.querySelector(".role-description");
    var button = box.querySelector(".view-more-button");

    const checkbox = box.querySelector(".custom-checkbox");
    checkbox.checked = !checkbox.checked;
    box.classList.toggle("selected", checkbox.checked);

    if (open === true) {
      description.style.maxHeight = "40px"; // Säädä korkeutta tarpeen mukaan
      description.classList.add("fade");
      open = !open;
      button.innerHTML = "Näytä lisää ⏷";
    } else {
      description.style.maxHeight = "none";
      description.classList.remove("fade");
      open = !open;
      button.innerHTML = "Piilota ⏶";
    }
  }
});
