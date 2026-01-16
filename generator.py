import os
import json
import google.generativeai as genai

# -----------------------------
# CONFIG
# -----------------------------
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
DIST_FOLDER = "dist"
WHATSAPP_NUMBER = "255716002790"  # 0716002790 bila 0, tumetumia format ya kimataifa

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
    Inatafuta model halisi inayopatikana kwenye API key yako
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
    """
    Roboti inatafuta makampuni YOTE ya solar Tanzania
    na kurudisha data katika JSON.
    """
    prompt = """
    Wewe ni mtafiti wa kitaalamu wa soko la nishati ya jua Tanzania.

    Tafuta na orodhesha makampuni yote ya Solar Energy yanayofanya kazi Tanzania kwa sasa.
    Usirudishe idadi ndogo, rudisha makampuni mengi iwezekanavyo.

    Kwa kila kampuni toa taarifa hizi kwa JSON:

    [
      {
        "name": "Jina kamili la kampuni",
        "description": "Maelezo ya kitaalamu kwa Kiswahili kuhusu kampuni na huduma zake",
        "location": "Mkoa au mji",
        "services": "Huduma kuu wanazotoa (mfano: installation, solar panels, batteries, maintenance, consulting)",
        "website": "Website au N/A kama haipo"
      }
    ]

    Sheria:
    - Rudisha JSON pekee bila maelezo mengine.
    - Maelezo yawe kwa Kiswahili.
    - Tumia makampuni halisi au yanayofanana sana na ya kweli Tanzania.
    - Kama website haijulikani, weka "N/A".
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
<title>Solar Tanzania | Orodha ya Makampuni ya Solar</title>
<style>
body {{
    font-family: Arial, sans-serif;
    margin: 40px;
}}
h1 {{
    color: #2c7a2c;
}}
li {{
    margin: 8px 0;
}}
</style>
</head>
<body>

<h1>☀ Solar Companies in Tanzania</h1>
<p>
Directory ya kitaifa ya makampuni ya nishati ya jua Tanzania.
Chagua kampuni kupata maelezo kamili na kuomba huduma moja kwa moja.
</p>

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
        whatsapp_link = f"https://wa.me/{WHATSAPP_NUMBER}?text=Nahitaji%20huduma%20ya%20solar%20kupitia%20Solar%20Tanzania."

        html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{company["name"]} | Solar Tanzania</title>
<style>
body {{
    font-family: Arial, sans-serif;
    margin: 40px;
    line-height: 1.6;
}}
.box {{
    max-width: 800px;
    margin: auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
}}
h1 {{
    color: #2c7a2c;
}}
.button {{
    display: inline-block;
    padding: 12px 20px;
    background: #2c7a2c;
    color: white;
    text-decoration: none;
    border-radius: 5px;
    margin-top: 15px;
}}
.button:hover {{
    background: #256a25;
}}
</style>
</head>
<body>

<div class="box">
<h1>{company["name"]}</h1>

<p><strong>📍 Location:</strong> {company["location"]}</p>
<p><strong>🛠 Services:</strong> {company.get("services", "Solar installation and solar energy solutions")}</p>

<p><strong>📝 Description:</strong><br>
{company["description"]}
</p>

<p><strong>🌐 Website:</strong>
<a href="{company["website"]}" target="_blank">{company["website"]}</a>
</p>

<a class="button" href="{whatsapp_link}">
📞 Omba Huduma ya Sola Kupitia WhatsApp
</a>

<p style="margin-top:20px;">
<a href="index.html">← Rudi kwenye orodha ya makampuni</a>
</p>
</div>

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

    print("🤖 Fetching solar companies from Gemini...")
    companies = fetch_solar_companies()

    print(f"📊 Found {len(companies)} companies. Generating mini-sites...")

    print("📝 Generating index.html...")
    generate_index_html(companies)

    print("🏗 Generating company mini-sites...")
    generate_company_pages(companies)

    print("✅ Solar Tanzania website generated successfully!")

if __name__ == "__main__":
    main()

