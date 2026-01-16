import os
import json

DIST = "dist"

def ensure_dist():
    os.makedirs(DIST, exist_ok=True)
    os.makedirs(f"{DIST}/assets", exist_ok=True)

def save(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def generate_companies_json():
    companies = [
        {
            "name": "Offgrid Africa",
            "location": "Dar es Salaam",
            "services": "Solar installation, lithium batteries",
            "description": "Leading off-grid solar provider in Tanzania.",
            "phone": "+255716002790"
        },
        {
            "name": "Zanzibar Green Power",
            "location": "Zanzibar",
            "services": "Solar hotels, resorts, backup systems",
            "description": "Premium solar solutions for tourism sector.",
            "phone": "+255712000111"
        }
    ]
    save(f"{DIST}/companies.json", json.dumps(companies, indent=2))

def generate_assets():
    css = """
body{font-family:sans-serif;background:#f9fafb;margin:0}
header{background:#16a34a;color:white;padding:15px;text-align:center}
.card{background:white;padding:15px;margin:10px;border-radius:8px}
"""
    js = """
fetch("companies.json")
.then(r=>r.json())
.then(data=>{
  const box=document.getElementById("companies");
  data.forEach(c=>{
    const div=document.createElement("div");
    div.className="card";
    div.innerHTML=`
      <h3>${c.name}</h3>
      <p><b>${c.location}</b></p>
      <p>${c.services}</p>
      <p>${c.description}</p>
      <p>${c.phone}</p>
    `;
    box.appendChild(div);
  });
})
.catch(e=>{
  document.getElementById("error").innerText="Failed to load companies.json";
});
"""
    save(f"{DIST}/assets/style.css", css)
    save(f"{DIST}/assets/script.js", js)

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
<h2>☀ Solar Tanzania</h2>
<p>Find Trusted Solar Companies in Tanzania</p>
</header>

<p id="error" style="color:red;text-align:center;"></p>

<div id="companies"></div>

<script src="assets/script.js"></script>
</body>
</html>
"""
    save(f"{DIST}/index.html", html)

def main():
    ensure_dist()
    generate_companies_json()
    generate_assets()
    generate_index()
    print("✅ Static Solar Tanzania site generated")

def generate_companies_json(companies):
    path = os.path.join(DIST_FOLDER, "companies.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(companies, f, indent=2, ensure_ascii=False)
    print("📦 companies.json created")


if __name__ == "__main__":
    main()
