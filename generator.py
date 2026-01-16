import google.generativeai as genai
import os
import random
import time

# 1. SETUP API KEY (Inasoma kutoka GitHub Secrets)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

if not os.path.exists('dist'):
    os.makedirs('dist')

colors = ["#f4b400", "#2e7d32", "#1565c0", "#c62828", "#6a1b9a", "#ef6c00"]

# 2. AI RESEARCH: Gemini inatafuta makampuni yenyewe
def ai_research_companies():
    print("🔍 Gemini inafanya utafiti wa makampuni ya solar Tanzania...")
    prompt = """Nipe orodha ya makampuni 10 ya solar yanayofanya kazi Tanzania. 
    Kwa kila kampuni nipe: Jina, Mkoa ilipo, na huduma moja wanayotoa. 
    Format: Jina | Mkoa | Huduma. Usiweke maneno mengine."""
    
    try:
        response = model.generate_content(prompt)
        raw_data = response.text.strip().split('\n')
        companies = []
        for line in raw_data:
            if '|' in line:
                parts = line.split('|')
                companies.append({
                    "name": parts[0].strip(),
                    "location": parts[1].strip(),
                    "specialty": parts[2].strip()
                })
        return companies
    except Exception as e:
        print(f"Hitilafu ya AI: {e}")
        return []

# ... (Hapa weka zile function za get_html_template na generate_ai_content nilizokupa awali)

# 3. RUN THE BOT
makampuni = ai_research_companies()
links_for_home = []

for co in makampuni:
    name = co['name']
    safe_name = name.lower().replace(' ', '_').replace('.', '').strip()
    links_for_home.append({"name": name, "url": f"{safe_name}.html"})
    
    # Gemini inaandika maelezo marefu
    prompt_maelezo = f"Andika makala ya maneno 200 kwa Kiswahili kuhusu kampuni ya solar inayoitwa {name} iliyopo {co['location']}. Elezea umuhimu wao katika nishati mbadala."
    content = model.generate_content(prompt_maelezo).text
    
    # Tengeneza HTML file
    color = random.choice(colors)
    # (Hapa script itatumia template yako kutengeneza file la HTML kwenye /dist)
    with open(f"dist/{safe_name}.html", 'w', encoding='utf-8') as f:
        # Fupi kwa ajili ya mfano, tumia template yako kamili hapa
        f.write(f"<html><body style='font-family:sans-serif;'><h1>{name}</h1><p>{content}</p></body></html>")

# ... (Tengeneza index.html kama kawaida)
