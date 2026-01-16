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
# FIND WORKING MODEL
# =============================
def get_working_model():
    print("🔍 Searching Gemini models...")
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            print("✅ Using model:", m.name)
            return m.name
    raise Exception("Hakuna model ya Gemini inayopatikana.")

# =============================
# FETCH SOLAR COMPANIES
# =============================
def fetch_solar_companies():
    prompt = """
Generate a list of 30 real Solar companies in Tanzania.
Include installers, suppliers, solar shops, battery dealers.
Return ONLY valid JSON.

Format:
[
  {
    "name": "",
    "location": "",
    "services": "",
    "description": "",
    "website": "",
    "phone": ""
  }
]
"""
    model = genai.GenerativeModel(get_working_model())
    response = model.generate_content(prompt)
    text = response.text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)

# =============================
# SAVE JSON
# =============================
def save_companies_json(companies):
    path = f"{DIST_FOLDER}/companies.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(companies, f, ensure_ascii=False, indent=2)

# =============================
# ASSETS
# =============================
def generate_assets():
    css = """
body{
  margin:0;
  font-family:system-ui;
  background:#f9fafb;
}
header{
  background:#15803d;
  color:white;
  padding:15px;
  text-align:center;
}
.search{
  width:100%;
  padding:12px;
  border:1px solid #ddd;
  border-radius:8px;
  margin:15px 0;
}
.grid{
  display:grid;
  grid-template-columns:repeat(auto-fit,minmax(260px,1fr));
  gap:15px;
}
.card{
  background:white;
  border-radius:10px;
  padding:15px;
  box-shadow:0 2px 8px rgba(0,0,0,.08);
}
.card h3{color:#15803d}
"""
    js = """
async function loadCompanies() {
  const res = await fetch("companies.json");
  const companies = await res.json();
  const container = document.getElementById("companies");
  container.innerHTML = "";
  companies.forEach((c, i) => {
    const card = document.createElement("div
