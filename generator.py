import google.generativeai as genai
import os
import shutil

# 1. SETUP
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# Safisha folder la dist
if os.path.exists('dist'):
    shutil.rmtree('dist')
os.makedirs('dist')

# 2. AI RESEARCH
print("🔍 Gemini inatafuta makampuni ya solar Tanzania...")
prompt = "Orodhesha majina 6 ya makampuni makubwa ya solar Tanzania na mikoa yalipo. Format: Jina | Mkoa"

try:
    response = model.generate_content(prompt)
    lines = response.text.strip().split('\n')
    
    html_cards = ""
    for line in lines:
        if '|' in line:
            name, loc = line.split('|')
            name, loc = name.strip(), loc.strip()
            
            # Tengeneza jina la file kwa usalama
            clean_name = name.lower().replace(' ', '_').replace('.', '')
            file_name = clean_name + ".html"
            
            # Ongeza card kwenye index
            html_cards += f'<a href="{file_name}" style="background:white; padding:20px; border-radius:15px; text-decoration:none; color:#333; box-shadow:0 4px 6px rgba(0,0,0,0.1); display:block; margin-bottom:15px;">'
            html_cards += f'<h3 style="margin:0; color:#2e7d32;">{name}</h3>'
            html_cards += f'<p style="margin:5px 0 0; color:#666;">📍 {loc}</p></a>'
            
            # Tengeneza ukurasa wa kampuni (Njia salama bila f-string tata)
            page_content = "<html><body style='font-family:sans-serif; padding:40px;'>"
            page_content += "<h1>" + name + "</h1>"
            page_content += "<p>Hii ni kampuni ya solar inayopatikana " + loc + ".</p>"
            page_content += "<a href='index.html'>Rudi Nyumbani</a></body></html>"
            
            with open("dist/" + file_name, "w", encoding="utf-8") as f:
                f.write(page_content)

    # 3. Tengeneza Index.html
    index_start = """
    <!DOCTYPE html>
    <html lang="sw">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Solar Tanzania</title>
    </head>
    <body style="font-family:sans-serif; background:#f4f7f6; margin:0; padding:40px; text-align:center;">
        <h1 style="color:#2c3e50;">Orodha ya Makampuni ya Solar Tanzania</h1>
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(250px, 1fr)); gap:20px; max-width:1000px; margin:40px auto;">
    """
    index_end = "</div></body></html>"
    
    full_index = index_start + html_cards + index_end
    
    with open("dist/index.html", "w", encoding="utf-8") as f:
        f.write(full_index)
    
    print("✅ Kazi imekamilika! Website imetengenezwa.")

except Exception as e:
    print("❌ Hitilafu imetokea: " + str(e))
