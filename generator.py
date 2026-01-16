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
            "services": "Solar installation, batteries, inverters",
            "description": "Reliable solar energy provider in Zanzibar.",
            "website": "N/A",
            "phone": "0712345678"
        },
        {
            "name": "Dar Solar Tech",
            "location": "Dar es Salaam",
            "services": "Panels, installation, maintenance",
            "description": "Affordable solar systems for homes and businesses.",
            "website": "N/A",
            "phone": "0755555555"
        }
    ]

    path = os.path.join(DIST_FOLDER, "companies.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(companies, f, indent=2, ensure_ascii=False)

    print("✅ companies.json created successfully")

def generate_assets():
    css = """
body{font-family:Arial;background:#f5f5f5;margin:0}
header{background:#16a34a;color:white;padding:20px;text-align:center}
#companies{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:15px;padding:20px}
.card{background:white;padding:15px;border-radius:6px;box-shadow:0 2px 4px rgba(0,0,0,.1)}
"""
    js = """
fetch("companies.json")
.then(r=>r.json())
.then(data=>{
  const c=document.getElementById("companies");
  data.forEach(x=>{
    const d=document.createElement("div");
    d.className="card";
    d.innerHTML=`<h3>${x.name}</h3><p>${x.location}</p><p>${x.description}</p><p>${x.phone}</p>`;
    c.appendChild(d);
  })
})
.catch(()=>document.getElementById("error").innerText="Failed to load companies.json");
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

<p id="error" style="color:red;text-align:center"></p>
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
    print("🚀 Static site generated")

if __name__ == "__main__":
    main()
