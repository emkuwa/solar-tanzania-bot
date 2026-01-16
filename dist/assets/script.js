const companies = [
  {
    name: "Offgrid Africa",
    location: "Dar es Salaam",
    services: "Solar kits, lithium batteries, installations"
  },
  {
    name: "Zanzibar Green Power",
    location: "Zanzibar",
    services: "Hotels, backup systems, tourism solar"
  },
  {
    name: "Mwanza Sun Solutions",
    location: "Mwanza",
    services: "Water pumps, agri-solar systems"
  }
];

function renderCompanies() {
  const container = document.getElementById("companies");
  container.innerHTML = "";

  companies.forEach(c => {
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <h3>${c.name}</h3>
      <p>📍 ${c.location}</p>
      <p>⚡ ${c.services}</p>
    `;
    container.appendChild(card);
  });
}

renderCompanies();

function calculate() {
  const watts = document.getElementById("watts").value;
  const hours = document.getElementById("hours").value;
  if (!watts || !hours) {
    document.getElementById("result").innerText = "Please fill all fields.";
    return;
  }
  const cost = watts * hours * 5;
  document.getElementById("result").innerText = 
    "Estimated basic system cost: Tsh " + cost.toLocaleString();
}
