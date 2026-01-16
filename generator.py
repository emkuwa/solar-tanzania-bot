import os
import json

DIST = "dist"

def main():
    print("Creating dist folder...")
    os.makedirs(DIST, exist_ok=True)

    companies = [
        {
            "name": "Test Solar One",
            "location": "Dar es Salaam",
            "description": "Sample solar company for testing"
        },
        {
            "name": "Zanzibar Solar Hub",
            "location": "Zanzibar",
            "description": "Another sample company"
        }
    ]

    print("Writing companies.json...")
    with open(os.path.join(DIST, "companies.json"), "w", encoding="utf-8") as f:
        json.dump(companies, f, indent=2, ensure_ascii=False)

    print("Writing index.html...")
    with open(os.path.join(DIST, "index.html"), "w", encoding="utf-8") as f:
        f.write("""
<!DOCTYPE html>
<html>
<head>
  <title>Solar Tanzania Test</title>
</head>
<body>
  <h1>Solar Tanzania Test</h1>
  <pre id="data">Loading...</pre>

  <script>
    fetch("companies.json")
      .then(r => r.json())
      .then(d => {
        document.getElementById("data").textContent = JSON.stringify(d, null, 2);
      })
      .catch(() => {
        document.body.innerHTML = "<h2>FAILED TO LOAD companies.json</h2>";
      });
  </script>
</body>
</html>
""")

    print("DONE. companies.json and index.html created.")

if __name__ == "__main__":
    main()
