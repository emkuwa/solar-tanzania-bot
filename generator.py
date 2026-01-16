import google.generativeai as genai
import os
import shutil
import random
import time

# 1. SETUP - Inasoma Key kutoka GitHub Secrets
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Futa folder la 'dist' kama lipo na litengeneze upya ili kufuta sample za zamani
if os.path.exists('dist'):
    shutil.rmtree('dist')
os.makedirs('dist')

colors = ["#f4b400", "#2e7d32", "#1565c0", "#c62828", "#6a1b9a", "#ef6c00"]

# 2. AI RESEARCH - Gemini inatafuta makampuni halisi
def pata_makampuni_halisi():
    print("🔍 Gemini inatafuta makampuni halisi ya solar Tanzania...")
    prompt = """Orodhesha makampuni 10 makubwa na halisi ya nishati ya jua (solar) yanayofanya kazi Tanzania.
    Nipe majibu katika mfumo huu pekee: Jina la Kampuni | Mkoa | Huduma kuu.
    Mfano: Rex Energy | Dar es Salaam | Solar Power Plants"""
    
    try:
        response = model.generate_content(prompt)
        mistari = response.text.strip().split('\n')
        data = []
        for mstari in mistari:
            if '|' in mstari:
                pande = mstari.split('|')
                data.append({
                    "name": pande[0].strip(),
                    "location": pande[1].strip(),
                    "specialty": pande[2].strip()
                })
        return data
    except Exception as e:
        print(f"Hitilafu: {e}")
        return []

def get_html_template(title, location, body, color):
    return f"""
<!DOCTYPE html>
<html lang="sw">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Huduma za Solar Tanzania</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: auto; padding: 20px; background-color: #f4f7f6; }}
        .header {{ background: {color}; color: white; padding: 40px 20px; text-align: center; border-radius: 10px; }}
        .content {{ background: white; padding: 30px; margin-top: -20px; border-radius: 10px; shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .back-link {{ display: inline-block; margin-bottom: 20px; color: {color}; text-decoration: none; font-weight: bold; }}
    </style>
</head>
<body>
    <a href="index.html" class="back-link">← Rudi Kwenye Orodha</a>
    <div class="header">
        <h1>{title}</h1>
        <p>Eneo: {location}</p>
    </div>
    <div class="content">{body}</div>
</body>
</html>
"""

# 3. MAIN PROCESS
makampuni = pata_makampuni_halisi()
links_for_home = []

for co in makampuni:
    name = co['name']
    # Tengeneza jina la file lisilo na nafasi
    file_name = name.lower().replace(' ', '_').replace('.', '').replace('/', '_') + ".html"
    links_for_home.append({"name": name, "location": co['location'], "url": file_name})
    
    print(f"✍️ Inatengeneza ukurasa wa: {name}...")
    prompt_maudhui = f"Andika makala ndefu ya maneno 250 kuhusu kampuni ya {name} iliyopo {co['location']}. Elezea huduma zao za {co['specialty']} na umuhimu wao kwa wateja wa Tanzania. Tumia Kiswahili sanifu."
    
    try:
        content_ai = model.generate_content(prompt_maudhui).text.replace('\n', '<py><br>')
        rangi = random.choice(colors)
        
        with open(f"dist/{file_name}", "w", encoding="utf-8") as f:
            f.write(get_html_template(name, co['location'], content_ai, rangi))
        time.sleep(2) # Kuzuia overload ya API
    except:
        continue

# 4. TENGENEZA HOME PAGE (INDEX.HTML)
cards = "".join([f'<div style="background:white; padding:20px; border-radius:8px; margin:10px; box-shadow:0 2px 4px rgba(0,0,0,0.1);"><a href="{i["url"]}" style="text-decoration:none; color:#2c3e50;"><h3>{i["name"]}</h3><p>📍 {i["location"]}</p></a></div>' for i in links_for_home])

# Hifadhi hii sehemu ya mwisho kabisa ya generator.py
index_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Solar Tanzania</title>
    <style>
        body {{ font-family: sans-serif; text-align: center; padding: 50px; background: #f4f4f4; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; max-width: 1000px; margin: auto; }}
        .card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); text-decoration: none; color: #333; }}
    </style>
</head>
<body>
    <h1>Orodha ya Makampuni ya Solar Tanzania</h1>
    <div class="grid">
"""

for link in links_for_home:
    index_content += f'<a href="{link["url"]}" class="card"><h3>{link["name"]}</h3><p>📍 {link["location"]}</p></a>'

index_content += "</div></body></html>"

with open("dist/index.html", "w", encoding="utf-8") as f:
    f.write(index_content)

print("✅ Kazi imekamilika! Website mpya imetengenezwa.")
