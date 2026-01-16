import google.generativeai as genai
import os
import shutil

# SETUP
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Tengeneza folder la dist
if os.path.exists('dist'):
    shutil.rmtree('dist')
os.makedirs('dist')

# 1. AI Research - Pata list ya makampuni halisi
prompt = "Orodhesha majina 8 ya makampuni halisi ya solar Tanzania na mikoa yalipo. Format: Jina | Mkoa"
response = model.generate_content(prompt)
lines = response.text.strip().split('\n')

html_cards = ""
for line in lines:
    if '|' in line:
        name, loc = line.split('|')
        name, loc = name.strip(), loc.strip()
        file_name = f"{name.replace(' ', '_').lower()}.html"
        
        # Tengeneza Card ya ukurasa wa mwanzo
        html_cards += f'''
        <a href="{file_name}" style="background:white; padding:20px; border-radius:15px; text-decoration:none; color:#333; box-shadow:0 4px 6px rgba(0,0,0,0.1);">
            <h3 style="margin:0; color:#2e7d32;">{name}</h3>
            <p style="margin:5px 0 0; color:#666;">📍 {loc}</p>
        </a>'''
        
        # Tengeneza ukurasa wa kila kampuni
        with open(f"dist/{file_name}", "w") as f:
            f.write(f"<html><body style='font-family:sans-serif; padding:40px;'><h1>{name}</h1><p>Hii ni kampuni ya solar inayopatikana {loc}.</p><a href='index.html'>Rudi Nyumbani</a></body></html>")

# 2. Tengeneza Index.html
index_html = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Solar Tanzania</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family:sans-serif; background:#f4f7f6; margin:0; padding:40px; text-align:center;">
    <h1 style="color:#2c3e50;">Orodha ya Makampuni ya Solar Tanzania</h1>
    <p>Pata wataalamu wa nishati ya jua karibu nawe</p>
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(250px, 1fr)); gap:20px; max-width:1000px; margin:40px auto;">
        {html_cards}
    </div>
</body>
</html>
'''
with open("dist/index.html", "w") as f:
    f.write(index_html)
