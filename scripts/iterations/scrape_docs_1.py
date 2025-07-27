import requests 
from bs4 import BeautifulSoup
import os

# Make sure the data directory exists 
os.makedirs("data", exist_ok=True)

# This is the public sitemap provided by Databricks
SITEMAP_URL = "https://docs.databricks.com/sitemap.xml"


def fetch_sitemap_links(sitemap_url):
    print("Fetchhing sitemap...")
    res = requests.get(sitemap_url)
    soup = BeautifulSoup(res.content, "xml")
    urls = [loc.text for loc in soup.find_all("loc")]
    # Filter only real doc pages (not APIs or root)
    return [url for url in urls if "/en/" not in url and url.endswith(".html")]


def fetch_text_from_url(url):
    print(f"Fetching {url}")
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f" Failed with status code {response.status_code}")
            return None
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator="\n")
        return text.strip() 
    except Exception as e:
        print(f" Exception white fetching : {e}")
        return None
    
# Grab the first 10 pages for now
doc_urls = fetch_sitemap_links(SITEMAP_URL)[:10]
    
# Loop through all URLs and save text to a file

for i, url in enumerate(doc_urls):
    text = fetch_text_from_url(url)
    if text:
        filename = f"data/page_{i+1}.txt"
        with open(filename,"w",encoding="utf-8") as f:
            f.write(text)
        print(f"Saved: data/{filename}.txt")
    else:
        print(f"Skipping {filename}: No Valid Content")

