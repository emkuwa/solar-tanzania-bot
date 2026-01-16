let allCompanies = [];

async function loadCompanies() {
  try {
    const res = await fetch("companies.json");
    allCompanies = await res.json();
    renderCompanies(allCompanies);
  } catch (e) {
    document.getElementById("companies").innerHTML =
      "<p style='color:red'>Failed to load companies.json</p>";
  }
}

function renderCompanies(companies) {
  const container = document.getElementById("companies");
  container.innerHTML = "";

  companies.forEach((c, i) => {
    const card = document.createElement("div");
    card.className = "card";

    card.innerHTML = `
      <h3>${c.name}</h3>
      <p><strong>Location:</strong> ${c.location}</p>
      <p>${c.description}</p>
      <div class="actions">
        <a href="company_${i + 1}.html" class="btn">View Profile</a>
      </div>
    `;

    container.appendChild(card);
  });
}

function filterCompanies() {
  const q = document.getElementById("search").value.toLowerCase();
  const filtered = allCompanies.filter(c =>
    (c.name + c.location + c.services + c.description)
      .toLowerCase()
      .includes(q)
  );
  renderCompanies(filtered);
}

document.addEventListener("DOMContentLoaded", loadCompanies);
