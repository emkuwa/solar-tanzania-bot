import os
import json
import google.generativeai as genai

# =============================
# CONFIG
# =============================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
DIST = "dist"

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY haijawekwa kwenye GitHub Secrets")

genai.configure(api_key=GEMINI_API_KEY)


# =============================
# UTILS
# =============================
def ensure_dist():
    os.makedirs(DIST, exist_ok=True)
    os.makedirs(f"{DIST}/assets", exist_ok=True)

def save(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# =============================
# MODEL
# =============================
def get_model():
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            print("Using:", m.name)
            return genai.GenerativeModel(m.name)
    raise Exception("Hakuna model ya Gemini")


# =============================
# FETCH COMPANIES
# =============================
def fetch_solar_companies():
    prompt = """
Generate a JSON list of 30 real solar companies in Tanzania.
Include installers, suppliers, shops, distributors.
Return only JSON:

[
  {
    "name": "",
    "location": "",
    "services": "",
    "description": "",
    "phone": ""
  }
]
"""
    model = get_model()
    res = model.generate_content(prompt)
    text = res.text.replace("```json","").replace("```","").strip()
    return json.loads(text)


# =============================
# ASSETS
# =============================
def generate_assets():
    css = """
body{
  margin:0;
  font-family:system-ui, sans-serif;
  background:#f8fafc;
}
header{
  padding:16px;
  background:#0f172a;
  color:white;
}
.hero{
  padding:20px;
}
.search{
  width:100%;
  padding:12px;
  border-radius:10px;
  border:1px solid #ccc;
  margin-bottom:15px;
}
.grid{
  display:grid;
  grid-template-columns:1fr;
  gap:15px;
}
.card{
  background:white;
  padding:15px;
  border-radius:12px;
  box-shadow:0 4px 10px rgba(0,0,0,.08);
}
.card h3{margin:0;color:#0f172a}
.btn{
  display:inline-block;
  background:#22c55e;
  color:white;
  padding:8px 12px;
  border-radius:6px;
  text-decoration:none;
  font-size:14px;
}
"""

    js = """
fetch("companies.json")
.then(r=>r.json())
.then(data=>{
  window.companies=data;
  render(data);
});

function render(list){
  let grid=document.getElementById("grid");
  grid.innerHTML="";
  list.forEach(c=>{
    grid.innerHTML+=`
    <div class="card">
      <h3>${c.name}</h3>
      <p>${c.location}</p>
      <p>${c.services}</p>
      <p>${c.description}</p>
      <a class="btn" href="https://wa.me/255${c.phone.replace(/^0/,'')}">WhatsApp</a>
    </div>`;
  });
}

function filter(){
  let q=document.getElementById("search").value.toLowerCase();
  render(companies.filter(c=>
    c.name.toLowerCase().includes(q) ||
    c.location.toLowerCase().includes(q) ||
    c.services.toLowerCase().includes(q)
  ));
}
"""
    save(f"{DIST}/assets/style.css", css)
    save(f"{DIST}/assets/script.js", js)


# =============================
# INDEX
# =============================
def generate_index():
    html = """<!DOCTYPE html>
<html>
<head>
<title>Solar Tanzania</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header>
  <h2>☀ Solar Tanzania</h2>
</header>

<div class="hero">
  <h3>Find Solar Companies, Shops & Suppliers</h3>
  <input id="search" class="search" placeholder="Search..." onkeyup="filter()">
  <div id="grid" class="grid"></div>
</div>

<script src="assets/script.js"></script>
</body>
</html>
"""
    save(f"{DIST}/index.html", html)


# =============================
# MAIN
# =============================
def main():
    print("📁 Preparing dist...")
    ensure_dist()

    print("🤖 Fetching companies...")
    companies = fetch_solar_companies()

    print("💾 Saving companies.json")
    save(f"{DIST}/companies.json", json.dumps(companies, indent=2))

    print("🎨 Creating UI assets...")
    generate_assets()

    print("📄 Creating index.html...")
    generate_index()

    print("✅ DONE: Mobile-first Solar Tanzania Directory generated!")

if __name__ == "__main__":
    main()
