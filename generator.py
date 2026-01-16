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
Respond ONLY in JSON format:

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
# CREATE companies.json
# =============================
def generate_companies_json(companies):
    path = os.path.join(DIST_FOLDER, "companies.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(companies, f, indent=2, ensure_ascii=False)
    print("📦 companies.json created inside dist/")

# =============================
# ASSETS
# =============================
def generate_assets():
    css = """
body{
  font-family:Arial,sans-serif;
  margin:0;
  background:#f9fafb;
}
header{
  background:linear-gradient(to right,#16a34a,#22c55e);
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
  box-shadow:0 2px 5px rgba(0,0,0,.1);
}
"""
    js = """
fetch("companies.json")
  .then(res => res.json())
  .then(data => {
    const container = document.getElementById("companies");
    data.forEach(c => {
      const div = document.createElement("div");
      div.className = "card";
      div.innerHTML = `
        <h3>${c.name}</h3>
        <p><b>Location:</b> ${c.location}</p>
        <p>${c.description}</p>
        <p><b>Phone:</b> ${c.phone}</p>
      `;
      container.appendChild(div);
    });
  })
  .catch(() => {
    document.getElementById("error").innerText = "Failed to load companies.json";
  });
"""
    save(f"{DIST_FOLDER}/assets/style.css", css)
    save(f"{DIST_FOLDER}/assets/script.js", js)

# =============================
# INDEX HTML
# =============================
def generate_index():
    html = f"""
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

# =============================
# MAIN
# =============================
def main():
    print("📁 Preparing dist...")
    ensure_dist()

    print("🤖 Fetching companies...")
    companies = fetch_solar_companies()

    print("📦 Writing companies.json...")
    generate_companies_json(companies)

    print("🎨 Generating assets...")
    generate_assets()

    print("📄 Generating index.html...")
    generate_index()

    print("✅ Solar Tanzania static site generated successfully!")

if __name__ == "__main__":
    main()
