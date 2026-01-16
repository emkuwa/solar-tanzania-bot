import os
import json
import google.generativeai as genai

# -----------------------------
# CONFIG
# -----------------------------
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
DIST_FOLDER = "dist"
ASSETS_FOLDER = os.path.join(DIST_FOLDER, "assets")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing")

genai.configure(api_key=GEMINI_API_KEY)


# -----------------------------
# UTILS
# -----------------------------
def ensure_folders():
    os.makedirs(DIST_FOLDER, exist_ok=True)
    os.makedirs(ASSETS_FOLDER, exist_ok=True)


def save(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# -----------------------------
# FIND WORKING MODEL
# -----------------------------
def get_working_model():
    models = genai.list_models()
    for m in models:
        if "generateContent" in m.supported_generation_methods:
            print(f"Using model: {m.name}")
            return m.name
    raise Exception("No working Gemini model found.")


# -----------------------------
# AI FETCH
# -----------------------------
def fetch_companies():
    prompt = """
    Give me 40 real solar companies in Tanzania.
    Output ONLY valid JSON.

    Structure:
    [
      {
        "name": "",
        "location": "",
        "services": "",
        "description": "",
        "website": ""
      }
    ]
    """

    model_name = get_working_model()
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)

    text = response.text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)


# -----------------------------
# GENERATE INDEX CARDS
# -----------------------------
def generate_cards(companies):
    cards = ""
    for i, c in enumerate(companies):
        cards += f"""
<div class="card"
     data-name="{c['name']}"
     data-location="{c['location']}"
     data-services="{c['services']}">
  <h3>{c['name']}</h3>
  <p>📍 {c['location']}</p>
  <p>⚡ {c['services']}</p>
  <a href="company_{i+1}.html">View Profile →</a>
</div>
"""
    return cards


# -----------------------------
# COMPANY MINI SITES
# -----------------------------
def generate_company_pages(companies):
    for i, c in enumerate(companies):
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{c['name']} – Solar Tanzania</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>

<div class="card">
  <h1>{c['name']}</h1>
  <p>📍 {c['location']}</p>
  <p>⚡ {c['services']}</p>
  <p>{c['description']}</p>
  <p>🌐 <a href="{c['website']}" target="_blank">{c['website']}</a></p>

  <a class="whatsapp-btn"
     href="https://wa.me/255716002790?text=Hello,%20I%20found%20your%20company%20on%20Solar%20Tanzania">
     Contact via WhatsApp
  </a>

  <p><a href="index.html">← Back to directory</a></p>
</div>

</body>
</html>
"""
        save(os.path.join(DIST_FOLDER, f"company_{i+1}.html"), html)


# -----------------------------
# MAIN
# -----------------------------
def main():
    ensure_folders()
    print("Fetching solar companies from AI...")
    companies = fetch_companies()

    print("Generating index.html cards...")
    with open(os.path.join(DIST_FOLDER, "index.html"), "r", encoding="utf-8") as f:
        homepage = f.read()

    cards_html = generate_cards(companies)
    homepage = homepage.replace("<!-- SAMPLE CARD (Generator will replace these dynamically later) -->", cards_html)

    save(os.path.join(DIST_FOLDER, "index.html"), homepage)

    print("Generating mini sites...")
    generate_company_pages(companies)

    print("DONE: Solar Tanzania directory built successfully!")


if __name__ == "__main__":
    main()
