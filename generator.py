import os
import json
import google.generativeai as genai

# =============================
# CONFIG
# =============================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
DIST_FOLDER = "dist"

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY haijawekwa kwenye GitHub Secrets")

genai.configure(api_key=GEMINI_API_KEY)

# =============================
# UTILS
# =============================
def ensure_dist():
    os.makedirs(DIST_FOLDER, exist_ok=True)
    os.makedirs(f"{DIST_FOLDER}/assets", exist_ok=True)

def save(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def save_companies_json(companies):
    path = os.path.join(DIST_FOLDER, "companies.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(companies, f, ensure_ascii=False, indent=2)
    print(f"💾 companies.json saved at {path}")

# =============================
# FIND WORKING MODEL
# =============================
def get_working_model():
    print("🔍 Searching Gemini models...")
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            print("✅ Using model:", m.name)
            return m.name
    raise Exception("Hakuna model ya Gemini inayopatikana kwa API key yako.")

# =============================
# FETCH SOLAR COMPANIES
# =============================
def fetch_solar_companies():
    prompt = """
Generate a list of 30 real Solar Energy companies operating in Tanzania.
Include big brands and small local suppliers who may not have websites.
Respond ONLY in JSON format like this:

[
  {
    "name": "Company Name",
    "location": "City or Region",
    "services": "Solar installation, panels, batteries, inverters",
    "description": "Short professional description",
    "website": "https://example.com or N/A",
    "phone": "07XXXXXXXX"
  }
]
"""

    model_name = get_working_model()
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)

    text = response.text.strip().replace("```json", "").replace("```", "")
    companies = json.loads(text)
    return companies

# =============================
# HTML + UI ASSETS
# =============================
def generate_assets():
    css = """
:root{
  --green:#16a34a;
  --blue:#2563eb;
  --bg:#f9fafb;
  --dark:#1f2937;
}
*{box-sizing:border-box;}
body{
  font-family:Arial,sans-serif;
  background:var(--bg);
  margin:0;
  color:var(--dark);
}
header{
  background:white;
  padding:15px;
  border-bottom:3px solid var(--green);
  display:flex;
  justify-content:space-between;
  align-items:center;
}
header h1{color:var(--green);margin:0;font-size:20px;}
.container{padding:15px;max-width:1100px;margin:auto;}
.search{
  padding:12px;
  width:100%;
  border:1px solid #ddd;
  border-radius:6px;
  margin-bottom:15px;
}
.grid{
  display:grid;
  grid-template-columns:repeat(auto-fit,minmax(260px,1fr));
  gap:15px;
}
.card{
  background:white;
  padding:15px;
  border-radius:10px;
  box-shadow:0 4px 10px rgba(0,0,0,.08);
}
.card h3{color:var(--blue);margin-top:0;}
.card p{font-size:14px;}
.whatsapp{
  display:inline-block;
  background:#25D366;
  color:white;
  padding:10px 14px;
  border-radius:6px;
  text-decoration:none;
  font-weight:bold;
}
.ad{
  background:#e5e7eb;
  text-align:center;
  padding:20px;
  margin:20px 0;
  border-radius:8px;
  font-weight:bold;
}
.footer{
  text-align:center;
  padding:20px;
  font-size:13px;
  color:#555;
}
"""

    js = """
let companiesData = [];

fetch("companies.json")
  .then(res => res.json())
  .then(data => {
    companiesData = data;
    renderCompanies(data);
  });

function renderCompanies(data){
  const grid = document.getElementById("grid");
  grid.innerHTML = "";
  data.forEach((c, i) => {
    grid.innerHTML += `
    <div class="card">
      <h3>${c.name}</h3>
      <p><b>Location:</b> ${c.location}</p>
      <p>${c.description}</p>
      <a href="company_${i+1}.html">View Profile →</a>
    </div>`;
  });
}

function filterCards(){
  let q = document.getElementById("search").value.toLowerCase();
  let filtered = companiesData.filter(c =>
    (c.name + c.location + c.services + c.description).toLowerCase().includes(q)
  );
  renderCompanies(filtered);
}
"""

    save(f"{DIST_FOLDER}/assets/style.css", css)
    save(f"{DIST_FOLDER}/assets/script.js", js)

# =============================
# INDEX PAGE
# =============================
def generate_index():
    html = f"""
<!DOCTYPE html>
<html>
<head>
  <title>Solar Tanzania Directory</title>
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header>
  <h1>☀ Solar Tanzania</h1>
  <span>Clean Energy Directory</span>
</header>

<div class="container">
  <input id="search" class="search" placeholder="Search company, city, service..." onkeyup="filterCards()">

  <div class="ad">ADVERTISEMENT SPACE</div>

  <div id="grid" class="grid"></div>

  <div class="ad">ADVERTISEMENT SPACE</div>
</div>

<div class="footer">
© 2026 Solar Tanzania – Powered by AI
</div>

<script src="assets/script.js"></script>
</body>
</html>
"""
    save(f"{DIST_FOLDER}/index.html", html)

# =============================
# COMPANY PAGES
# =============================
def generate_company_pages(companies):
    for i,c in enumerate(companies):
        html = f"""
<!DOCTYPE html>
<html>
<head>
<title>{c['name']} | Solar Tanzania</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header>
  <h1>{c['name']}</h1>
</header>
<div class="container">
<p><b>Location:</b> {c['location']}</p>
<p><b>Services:</b> {c['services']}</p>
<p>{c['description']}</p>
<p><b>Website:</b> {c['website']}</p>
<p><b>Phone:</b> {c['phone']}</p>

<a class="whatsapp" href="https://wa.me/255716002790?text=Hello,%20I%20need%20solar%20services">Chat on WhatsApp</a>
<br><br>
<a href="index.html">← Back to Directory</a>
</div>
</body>
</html>
"""
        save(f"{DIST_FOLDER}/company_{i+1}.html", html)

# =============================
# MAIN
# =============================
def main():
    print("📁 Preparing dist...")
    ensure_dist()

    print("🤖 Fetching companies...")
    companies = fetch_solar_companies()

    print("💾 Saving companies.json...")
    save_companies_json(companies)

    print("🎨 Creating UI assets...")
    generate_assets()

    print("📄 Creating index...")
    generate_index()

    print("🏢 Creating company pages...")
    generate_company_pages(companies)

    print("✅ Solar Tanzania Directory Generated!")

if __name__=="__main__":
    main()
