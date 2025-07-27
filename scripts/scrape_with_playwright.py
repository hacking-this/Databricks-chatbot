from playwright.sync_api import sync_playwright
import os

DOC_URLS = {
    "workspace": "https://docs.databricks.com/workspace/index.html",
    "clusters": "https://docs.databricks.com/clusters/index.html",
    "sql": "https://docs.databricks.com/sql/index.html",
    "delta": "https://docs.databricks.com/delta/index.html",
    "sql_create_table": "https://docs.databricks.com/en/sql/language-manual/sql-ref-syntax-ddl-create-table.html",
    "delta_merge": "https://docs.databricks.com/en/delta/delta-update.html",
    "autoloader_example": "https://docs.databricks.com/en/ingestion/auto-loader/example.html",
    "delta_optimize": "https://docs.databricks.com/en/delta/optimize.html",
    "notebooks_code": "https://docs.databricks.com/en/notebooks/notebooks-code.html",
}

os.makedirs("data", exist_ok=True)

from bs4 import BeautifulSoup

def fetch_with_browser(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, timeout=90000)
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(3000)

            # Get the raw HTML
            html = page.content()
            soup = BeautifulSoup(html, "html.parser")

            # Extract main visible text
            text = soup.get_text(separator="\n")

            # Extract <pre> and <code> blocks (this is key)
            code_blocks = []
            for tag in soup.find_all(["pre", "code"]):
                snippet = tag.get_text().strip()
                if len(snippet.split()) > 2:  # ignore short tags like "<="
                    code_blocks.append(snippet)

            combined = f"{text.strip()}\n\n--- CODE SNIPPETS ---\n\n" + "\n\n".join(code_blocks)
            return combined

        except Exception as e:
            print(f"❌ Failed to load {url}: {e}")
            return None
        finally:
            browser.close()


for name, url in DOC_URLS.items():
    print(f"🔍 Fetching: {url}")
    try:
        content = fetch_with_browser(url)
        with open(f"data/{name}.txt", "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Saved: data/{name}.txt")
    except Exception as e:
        print(f"❌ Failed: {e}")
