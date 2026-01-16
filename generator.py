import os
import json

DIST_FOLDER = "dist"

def ensure_dist():
    os.makedirs(DIST_FOLDER, exist_ok=True)
    os.makedirs(f"{DIST_FOLDER}/assets", exist_ok=True)

def save(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def generate_companies_json():
    companies = [
        {
            "name": "Zanzibar Solar Solutions",
            "location": "Zanzibar",
            "services": "Installation, batteries, inverters",
            "description": "Reliable solar energy provider in Zanzibar.",
            "phone": "0712345678"
        },
        {
            "name": "Dar Solar Tech",
            "location": "Dar es Salaam",
            "services": "Panels, installation, maintenance",
            "description": "Affordable solar systems for homes and businesses.",
            "phone": "0755555555"
        },
        {
            "name": "Mwanza Sun Power",
            "location": "Mwanza",
            "services": "Solar water pumps, home systems",
            "description": "Solar solutions for agriculture and homes.",
            "phone": "0766666666"
        }
    ]

    path = os.path.join(DIST_FOLDER, "companies.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(companies, f, indent=2, ensure_ascii=False)

    print("✅ companies.json created")

def generate_assets():
    css = """
body{
  margin:0;
  font-family:Arial,sans-serif;
  background:#f5f5f5;
}
header{
  background:#16a34a;
  color:white;
  padding:20px;
  text-align:center;
}
#companies{
  display:grid;
  grid-template-columns:repeat(auto-fit,minmax(250px,1fr));
  gap:15px;
  padding:20px;
}
.card{
  background:white;
  padding:15px;
  border-radius:8px;
  box-shadow:0 2px 4px rgba(0,0,0,.1);
}
.card h3{
  margin-top:0;
  color:#2563eb;
}
"""
    js = """
fetch("companies.json")
.then(r => r.json())
.then(data => {
  const box = document.getElementById("companies");
  data.forEach(c => {
    const div = document.createElement("div");
    div.className = "card";
    div.innerHTML = `
      <h3>${c.name}</h3>
      <p><b>Location:</b> ${c.location}</p>
      <p><b>Services:</b> ${c.services}</p>
      <p>${c.description}</p>
      <p><b>Phone:</b> ${c.phone}</p>
    `;
    box.appendChild(div);
  });
})
.catch(() => {
  document.getElementById("error").innerText = "Failed to load companies.json";
});
"""
    save(f"{DIST_FOLDER}/assets/style.css", css)
    save(f"{DIST_FOLDER}/assets/script.js", js)

def generate_index():
    html = """
<!DOCTYPE html>
<html>
<head>
<title>Solar Tanzania</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header>
  <h1>☀ Solar Tanzania</h1>
  <p>Find Trusted Solar Companies in Tanzania</p>
</header>

<p id="error" style="color:red;text-align:center;"></p>
<div id="companies"></div>

<script src="assets/script.js"></script>
</body>
</html>
"""
    save(f"{DIST_FOLDER}/index.html", html)

def main():
    ensure_dist()
    generate_companies_json()
    generate_assets()
    generate_index()
    print("🚀 Static Solar Tanzania site generated successfully")

if __name__ == "__main__":
    main()
