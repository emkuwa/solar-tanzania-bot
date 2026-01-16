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
    raise Exception("Hakuna model ya Gemini inayopatikana kwa API key yako.")

# =============================
# FETCH SOLAR COMPANIES
# =============================
def fetch_solar_companies():
    prompt = """
Generate a list of 25 real Solar Energy companies operating in Tanzania.
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
    return json.loads(text)

# =============================
# SAVE COMPANIES JSON
# =============================
def generate_companies_json(companies):
    path = os.path.join(DIST_FOLDER, "companies.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(companies, f, indent=2, ensure_ascii=False)
    print("📦 companies.json created")

# =============================
# HTML + UI ASSETS
# =============================
def generate_assets():
    css = """
body {
  margin: 0;
  font-family: Arial, sans-serif;
  background: #f9fafb;
}
header {
  background: linear-gradient(90deg,#16a34a,#22c55e);
  color: white;
  padding: 20px;
  text-align: center;
}
.search {
  width: 95%;
  max-width: 600px;
  padding: 12px;
  margin: 20px auto;
  display: block;
  border-radius: 8px;
  border: 1px solid #ccc;
}
#companies {
  display: grid;
  grid-template-columns: repeat(auto-fit,minmax(250px,1fr));
  gap: 15px;
  padding: 20px;
}
.card {
  background: white;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}
.card h3 {
  margin-top: 0;
  color: #16a34a;
}
"""

    js = """
let allCompanies = [];

fetch("companies.json")
  .then(r => r.json())
  .then(data => {
    allCompanies = data;
    renderCompanies(data);
  })
  .catch(() => {
    document.getElementById("error").innerText = "Failed to load companies.json";
  });

function renderCompanies(list){
  const container = document.getElementById("companies");
  container.innerHTML = "";
  list.forEach(c => {
    const div = document.createElement("div");
    div.className = "card";
    div.innerHTML = `
      <h3>${c.name}</h3>
      <p><b>Location:</b> ${c.location}</p>
      <p>${c.description}</p>
      <p><b>Services:</b> ${c.services}</p>
      <p><b>Phone:</b> ${c.phone}</p>
    `;
    container.appendChild(div);
  });
}

function searchCompanies(){
  const q = document.getElementById("search").value.toLowerCase();
  const filtered = allCompanies.filter(c =>
    c.name.toLowerCase().includes(q) ||
    c.location.toLowerCase().includes(q) ||
    c.services.toLowerCase().includes(q)
  );
  renderCompanies(filtered);
}
"""

    save(f"{DIST_FOLDER}/assets/style.css", css)
    save(f"{DIST_FOLDER}/assets/script.js", js)

# =============================
# INDEX.HTML
# =============================
def generate_index():
    html = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Solar Tanzania Directory</title>
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header>
  <h1>☀ Solar Tanzania</h1>
  <p>Find Trusted Solar Companies in Tanzania</p>
</header>

<input id="search" class="search" placeholder="Search company or city..." onkeyup="searchCompanies()">

<p id="error" style="color:red;text-align:center;"></p>

<div id="companies"></div>

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

    print("📦 Creating companies.json...")
    generate_companies_json(companies)

    print("🎨 Creating UI assets...")
    generate_assets()

    print("📄 Creating index.html...")
    generate_index()

    print("🏁 Solar Tanzania site generated successfully!")

if __name__ == "__main__":
    main()
