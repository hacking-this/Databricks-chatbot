import requests
from bs4 import BeautifulSoup
import os

os.makedirs("data", exist_ok=True)

# Curated list of real, working doc pages with content
DOC_URLS = {
    "delta_lake": "https://docs.databricks.com/en/delta/index.html",
    "spark_sql": "https://docs.databricks.com/en/sql/language-manual/index.html",
    "clusters": "https://docs.databricks.com/en/clusters/index.html",
    "dataframes": "https://docs.databricks.com/en/data/dataframes.html",
}

def fetch_text_from_url(url):
    print(f"🔄 Fetching {url}")
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        res = requests.get(url)
        if res.status_code != 200:
            print(f"❌ Failed with status {res.status_code}")
            return None
        soup = BeautifulSoup(res.text, "html.parser")

        # Remove scripts/styles
        for tag in soup(["script", "style"]):
            tag.decompose()
        
        # FInd all known code block patterns
        code_blocks = []

        # 1. Standard <pre> or <code>
        for tag in soup.find_all(["pre","code"]):
            code_blocks.append(tag.get_text())
        
        # 2. Divs with code-like classes
        for class_name in ["highlight", "language-python", "language-sql","codehilite"]:
            for tag in soup.find_all("div", class_=class_name):
                code_blocks.append(tag.get_text())

        # Combine code snippets
        code_text = "\n\n".join(code_blocks) 


        # Get all readable text
        body_text = soup.get_text(separator="\n")
        combined = f"{body_text.strip()}\n\n --- CODE SNIPPETS ---\n\n{code_text.strip()}"
        return combined
    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")
        return None
    

for name, url in DOC_URLS.items():
    text = fetch_text_from_url(url)
    if text:
        print(f"\n📝 Sample content from {name}:\n{text[:500]}\n")  # <== ADD THIS LINE
        filename = f"data/{name}.txt"
        print(f"💾 Saving content to {filename}")

        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"✅ Saved: {filename}")
        except Exception as e:
            print(f"❌ Error saving {filename}: {e}")
    else:
        print(f"❌ Skipping {name}: No valid content")
