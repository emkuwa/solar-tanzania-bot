let currentLang = localStorage.getItem("lang") || "en";

function setLanguage(lang) {
  currentLang = lang;
  localStorage.setItem("lang", lang);

  document.querySelectorAll("[data-en]").forEach(el => {
    el.innerText = el.getAttribute("data-" + lang);
  });
}

function filterCards() {
  const search = document.getElementById("search").value.toLowerCase();

  document.querySelectorAll(".card").forEach(card => {
    const name = card.dataset.name.toLowerCase();
    const location = card.dataset.location.toLowerCase();
    const services = card.dataset.services.toLowerCase();

    const match =
      name.includes(search) ||
      location.includes(search) ||
      services.includes(search);

    card.style.display = match ? "block" : "none";
  });
}

document.addEventListener("DOMContentLoaded", () => {
  setLanguage(currentLang);

  document.getElementById("search").addEventListener("input", filterCards);
});
