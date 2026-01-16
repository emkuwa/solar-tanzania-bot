import google.generativeai as genai
import csv
import os
import random

# 1. Weka API Key yako hapa
genai.configure(api_key="AIzaSyB-YzYRnQCHJ0-mLne1wqZuvIPIVDHWhBw")
model = genai.GenerativeModel('gemini-1.5-flash')

if not os.path.exists('dist'):
    os.makedirs('dist')

links_for_home = []
colors = ["#f4b400", "#2e7d32", "#1565c0", "#c62828", "#6a1b9a", "#ef6c00"]

def generate_unique_page(name, location, specialty):
    prompt = f"Andika maelezo ya kitaalamu ya kampuni ya solar inayoitwa {name} iliyopo {location}. Wanahusika na {specialty}. Tumia Kiswahili."
    try:
        response = model.generate_content(prompt)
        return response.text
    except:
        return f"Karibu kwa huduma bora za Solar kutoka {name}."

def get_html_template(title, location_text, body, color):
    # MABADILIKO: Jina la fomu limekuwa "contact" kwa zote, lakini kuna input ya "kampuni"
    return f"""
<!DOCTYPE html>
<html lang="sw">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Solar Tanzania</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; line-height: 1.6; color: #333; max-width: 900px; margin: auto; padding: 20px; }}
        .header {{ background: {color}; color: white; padding: 40px 20px; text-align: center; border-radius: 15px; margin-bottom: 30px; }}
        .content {{ background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
        .form-box {{ background: #fdfdfd; padding: 30px; border: 2px dashed {color}; border-radius: 15px; margin-top: 40px; }}
        .btn {{ background: {color}; color: white; padding: 15px; border: none; width: 100%; border-radius: 8px; font-weight: bold; cursor: pointer; }}
    </style>
</head>
<body>
    <a href="/" style="text-decoration: none; color: {color}; font-weight: bold;">← Rudi Nyumbani</a>
    <div class="header">
        <h1>{title}</h1>
        <p>Suluhisho la Nishati ya Jua - {location_text}</p>
    </div>
    <div class="content">{body}</div>
    <div class="form-box">
        <h3>Pata Makadirio ya Bei (Quotation) Bure</h3>
        <form name="contact" method="POST" data-netlify="true" action="/asante.html">
            <input type="hidden" name="form-name" value="contact" />
            <input type="hidden" name="kampuni_inayotafutwa" value="{title}" />
            <p>
                <label>Jina lako: <input type="text" name="name" required style="width:100%; padding:10px; margin:10px 0; border:1px solid #ddd;" /></label>
            </p>
            <p>
                <label>Namba ya simu: <input type="tel" name="phone" required style="width:100%; padding:10px; margin:10px 0; border:1px solid #ddd;" /></label>
            </p>
            <button type="submit" class="btn">Nitumie Bei Sasa</button>
        </form>
    </div>
</body>
</html>
"""

# 2. TENGENEZA KURASA ZA KILA KAMPUNI
with open('solar_data.csv', mode='r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    for row in reader:
        name = row.get(next((k for k in row if 'company' in k.lower()), None))
        if name:
            safe_name = name.lower().replace(' ', '_').strip()
            links_for_home.append({"name": name, "url": f"{safe_name}.html"})
            color = random.choice(colors)
            print(f"Inatengeneza ukurasa wa: {name}...")
            content = generate_unique_page(name, row.get('location', ''), row.get('specialty', ''))
            with open(f"dist/{safe_name}.html", 'w', encoding='utf-8') as f:
                f.write(get_html_template(name, row.get('location', ''), content, color))

# 3. TENGENEZA HOME PAGE (index.html)
cards_html = "".join([f'<a class="card" href="{i["url"]}"><h3>{i["name"]}</h3><p>Angalia Maelezo &rarr;</p></a>' for i in links_for_home])
home_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Solar Tanzania Directory</title>
    <style>
        body {{ font-family: sans-serif; text-align: center; padding: 50px; background: #f5f5f5; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; max-width: 1000px; margin: auto; }}
        .card {{ background: white; padding: 25px; border-radius: 12px; text-decoration: none; color: #333; box-shadow: 0 4px 6px rgba(0,0,0,0.1); display: block; }}
        .card:hover {{ background: #f4b400; color: white; }}
    </style>
</head>
<body>
    <h1>Pata Huduma za Solar Tanzania</h1>
    <div class="grid">{cards_html}</div>
</body>
</html>
"""
with open("dist/index.html", "w", encoding='utf-8') as f:
    f.write(home_html)

# 4. TENGENEZA SUCCESS PAGE (asante.html)
asante_html = """
<!DOCTYPE html>
<html lang="sw">
<head><meta charset="UTF-8"><title>Asante</title><style>body { text-align: center; padding: 100px; font-family: sans-serif; }</style></head>
<body>
    <h1>✅ Asante Sana!</h1>
    <p>Tumepokea taarifa zako. Utapigiwa simu na mtaalamu wa solar hivi punde.</p>
    <a href="/">Rudi Mwanzo</a>
</body>
</html>
"""
with open("dist/asante.html", "w", encoding='utf-8') as f:
    f.write(asante_html)

print("\n✅ Kazi Imekamilika! Endesha tena na upload folder la dist.")