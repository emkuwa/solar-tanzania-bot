import os
import json
import google.generativeai as genai

# -----------------------------
# CONFIG
# -----------------------------
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
DIST_FOLDER = "dist"

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY haijawekwa kwenye GitHub Secrets")

genai.configure(api_key=GEMINI_API_KEY)

# -----------------------------
# UTILITY FUNCTIONS
# -----------------------------
def ensure_dist_folder():
    if not os.path.exists(DIST_FOLDER):
        os.makedirs(DIST_FOLDER)

def save_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# -----------------------------
# MODEL DISCOVERY
# -----------------------------
def get_working_model():
    """
    Hii inatafuta model halisi inayopatikana kwenye account yako
    na inayounga mkono generateContent.
    """
    print("🔍 Searching for available Gemini models...")
    models = genai.list_models()

    for m in models:
        if "generateContent" in m.supported_generation_methods:
            print(f"✅ Using model: {m.name}")
            return m.name

    raise Exception("❌ Hakuna model yoyote inayounga mkono generateContent kwenye API key yako.")

# -----------------------------
# AI PART
# -----------------------------
def fetch_solar_companies():
    prompt = """
    Nipe orodha ya makampuni 6 ya Solar Energy Tanzania.
    Jibu lazima liwe JSON pekee, bila maelezo mengine, kwa muundo huu:

    [
      {
        "name": "Company Name",
        "description": "Short description",
        "location": "City or Region",
        "website": "https://example.com"
      }
    ]
    """

    model_name = get_working_model()
    model = genai.GenerativeModel(model_name)

    response = model.generate_content(prompt)

    text = response.text.strip()
    text = text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        print("❌ Gemini amerudisha JSON isiyo sahihi:")
        print(text)
        raise

# -----------------------------
# HTML GENERATION
# -----------------------------
def generate_index_html(companies):
    list_items = ""
    for i, company in enumerate(companies):
        filename = f"company_{i+1}.html"
        list_items += f"""
        <li>
            <a href="{filename}">
                <strong>{company["name"]}</strong> – {company["location"]}
            </a>
        </li>
        """

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Solar Companies in Tanzania</title>
</head>
<body>
<h1>Solar Companies in Tanzania</h1>
<ul>
{list_items}
</ul>
</body>
</html>
"""
    save_file(os.path.join(DIST_FOLDER, "index.html"), html)

def generate_company_pages(companies):
    for i, company in enumerate(companies):
        filename = f"company_{i+1}.html"

        html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{company["name"]}</title>
</head>
<body>
<h1>{company["name"]}</h1>
<p><b>Location:</b> {company["location"]}</p>
<p><b>Description:</b> {company["description"]}</p>
<p><b>Website:</b> <a href="{company["website"]}" target="_blank">{company["website"]}</a></p>
<p><a href="index.html">Back</a></p>
</body>
</html>
"""
        save_file(os.path.join(DIST_FOLDER, filename), html)

# -----------------------------
# MAIN
# -----------------------------
def main():
    print("📁 Creating dist folder...")
    ensure_dist_folder()

    print("🤖 Fetching companies from Gemini...")
    companies = fetch_solar_companies()

    print("📝 Generating HTML...")
    generate_index_html(companies)
    generate_company_pages(companies)

    print("✅ Done! Website generated successfully.")

if __name__ == "__main__":
    main()
