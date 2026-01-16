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
            "services": "Solar pumps, home solar systems",
            "description": "Solar energy for agriculture and households.",
            "phone": "0766666666"
        }
    ]

    path = os.path.join(DIST_FOLDER, "companies.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(companies, f, indent=2, ensure_ascii=False)

    print("✅ companies.json created inside dist/")

def generate_assets():
    css = """
body{font-family:Arial;margin:0;background:#f5f5f5}
header{background:#16a34a;color:white;padding:20px;text-align:center}
#list{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:15px;padding:20px}
.card{background:white;padding:15px;border-radius:6px;box-shadow:0 2px 4px rgba(0,0,0,.1)}
.whatsapp{background:#25D366;color:white;padding:6px 10px;border-radius:4px;text-decoration:none}
"""
    js = """
fetch("companies.json")
.then(r=>r.json())
.then(data=>{
  window.companies=data;
  render(data);
})
.catch(()=>{
  document.getElementById("list").innerHTML="Failed to load companies.json";
});

function render(data){
  let html="";
  data.forEach(c=>{
    html+=`
    <div class="card">
      <h3>${c.name}</h3>
      <p><b>${c.location}</b></p>
      <p>${c.description}</p>
      <a class="whatsapp" href="https://wa.me/255${c.phone.replace(/^0/,'')}">WhatsApp</a>
    </div>`;
  });
  document.getElementById("list").innerHTML=html;
}

function search(){
  let q=document.getElementById("search").value.toLowerCase();
  let f=window.companies.filter(c=>JSON.stringify(c).toLowerCase().includes(q));
  render(f);
}
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

<input id="search" placeholder="Search..." onkeyup="search()" style="width:90%;margin:10px;padding:10px">

<div id="list">Loading...</div>

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
    print("🚀 Solar Tanzania static site generated")

if __name__ == "__main__":
    main()
