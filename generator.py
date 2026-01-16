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

# =============================
# FIND WORKING MODEL (HII IKO HAPA, KABLA YA KUITWA)
# =============================
def get_working_model():
    print("🔍 Searching available Gemini models...")
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            print("✅ Using model:", m.name)
            return m.name
    raise Exception("No compatible Gemini model found for this API key.")

# =============================
# FETCH SOLAR COMPANIES
# =============================
def fetch_solar_companies():
    prompt = """
Generate a list of 40 solar companies operating in Tanzania.
Include large companies and small local installers.

Return STRICT JSON only:

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

    text = response.text.strip()
    text = text.replace("```json", "").replace("```", "")

    return json.loads(text)

# =============================
# UI ASSETS
# =============================
def generate_assets():
    css = """
body{margin:0;font-family:Arial;background:#f5f7fa;}
header{background:#16a34a;color:white;padding:18px;text-align:center;}
.search{padding:12px;width:100%;border:1px solid #ddd;border-radius:6px;}
.container{padding:15px;}
.card{background:white;padding:12px;border-radius:8px;margin-bottom:12px;box-shadow:0 2px 4px rgba(0,0,0,.1);}
.card h3{margin:0;color:#2563eb;}
.whatsapp{background:#25D366;color:white;padding:6px 10px;border-radius:5px;text-decoration:none;}
"""

    js = """
fetch("companies.json")
.then(r=>r.json())
.then(data=>{
  window.companies=data;
  render(data);
})
.catch(()=>document.getElementById("list").innerHTML="Failed to load companies.json");

function render(data){
  let html="";
  data.forEach(c=>{
    html+=`
    <div class="card">
      <h3>${c.name}</h3>
      <p><b>${c.location}</b></p>
      <p>${c.description}</p>
      <a class="whatsapp" href="https://wa.me/255716002790">WhatsApp</a>
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

# =============================
# INDEX
# =============================
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

<div class="container">
  <input id="search" class="search" placeholder="Search company or city" onkeyup="search()">
  <div id="list">Loading companies...</div>
</div>

<script src="assets/script.js"></script>
</body>
</html>
"""
    save(f"{DIST_FOLDER}/index.html", html)

# =============================
# MAIN
# =============================
def main():
    print("📁 Preparing dist...")
    ensure_dist()

    print("🤖 Fetching companies...")
    companies = fetch_solar_companies()

    print("💾 Saving companies.json...")
    save(f"{DIST_FOLDER}/companies.json", json.dumps(companies, indent=2))

    print("🎨 Creating UI...")
    generate_assets()
    generate_index()

    print("✅ Solar Tanzania generated successfully!")

if __name__ == "__main__":
    main()
