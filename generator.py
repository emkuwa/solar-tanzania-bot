import os
import json
import requests
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
# AI PART
# -----------------------------
def fetch_solar_companies():
    """
    Tunaiambia Gemini itoe data katika JSON safi
    ili iwe rahisi kusoma na Python.
    """
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

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    # Gemini wakati mwingine hurudisha ```json ... ```
    text = response.text.strip()
    text = text.replace("```json", "").replace("```", "").strip()

    try:
        companies = json.loads(text)
        return companies
    except json.JSONDecodeError as e:
        print("Failed to parse Gemini JSON response:")
        print(text)
        raise e


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
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
        }}
        h1 {{
            color: #2c7a2c;
        }}
        ul {{
            list-style: none;
            padding: 0;
        }}
        li {{
            margin: 10px 0;
        }}
        a {{
            text-decoration: none;
            color: #1a4fa3;
        }}
    </style>
</head>
<body>
    <h1>Solar Companies in Tanzania</h1>
    <p>List of solar energy companies generated automatically using AI.</p>
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
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
        }}
        h1 {{
            color: #2c7a2c;
        }}
        a {{
            color: #1a4fa3;
        }}
    </style>
</head>
<body>
    <h1>{company["name"]}</h1>
    <p><strong>Location:</strong> {company["location"]}</p>
    <p><strong>Description:</strong> {company["description"]}</p>
    <p><strong>Website:</strong>
        <a href="{company["website"]}" target="_blank">
            {company["website"]}
        </a>
    </p>

    <p><a href="index.html">← Back to Home</a></p>
</body>
</html>
"""
        save_file(os.path.join(DIST_FOLDER, filename), html)


# -----------------------------
# MAIN FLOW
# -----------------------------
def main():
    print("Creating dist folder...")
    ensure_dist_folder()

    print("Fetching solar companies from Gemini...")
    companies = fetch_solar_companies()

    print("Generating index.html...")
    generate_index_html(companies)

    print("Generating company pages...")
    generate_company_pages(companies)

    print("Website generation completed successfully!")


if __name__ == "__main__":
    main()
