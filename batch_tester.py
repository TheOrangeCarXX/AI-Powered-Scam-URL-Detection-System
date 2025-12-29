import requests
import os
import csv
import glob

# Configuration
API_URL = "http://127.0.0.1:8000/analyze"
RESULTS_FILE = "scan_results.csv"

# Paths to your test data (Adjust if your folder names are different)
URLS_FILE = "test-pages/urls.txt"
HTML_DIRS = ["test-pages/fake", "test-pages/legit"]

def scan_item(item_type, data, source_name):
    try:
        payload = {"type": item_type, "data": data}
        response = requests.post(API_URL, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            return {
                "Source": source_name,
                "Type": item_type,
                "Score": result.get("final_score", "N/A"),
                "Verdict": result.get("verdict", "N/A"),
                "AI_Score": result.get("ai_score", "N/A"),
                "Rule_Score": result.get("rule_score", "N/A")
            }
        else:
            print(f"❌ Error scanning {source_name}: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Connection Error for {source_name}: {e}")
        return None

def main():
    results = []
    print(f"🚀 Starting Batch Scan against {API_URL}...\n")

    # 1. TEST URLS from urls.txt
    if os.path.exists(URLS_FILE):
        print(f"📄 Scanning URLs from {URLS_FILE}...")
        with open(URLS_FILE, "r") as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith("[")]
            
        for url in urls:
            print(f"   Testing: {url}...")
            res = scan_item("url", url, url)
            if res: results.append(res)
    else:
        print(f"⚠️ Warning: {URLS_FILE} not found.")

    # 2. TEST HTML FILES from folders
    print(f"\n📂 Scanning HTML files...")
    for folder in HTML_DIRS:
        # Find all .html files in the folder
        files = glob.glob(os.path.join(folder, "*.html"))
        for file_path in files:
            print(f"   Testing: {file_path}...")
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            res = scan_item("html", content, os.path.basename(file_path))
            if res: results.append(res)

    # 3. SAVE RESULTS
    if results:
        keys = results[0].keys()
        with open(RESULTS_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(results)
        
        print(f"\n✅ Done! Results saved to '{RESULTS_FILE}'")
        print("-" * 60)
        print(f"{'Source':<40} | {'Score':<5} | {'Verdict'}")
        print("-" * 60)
        for r in results:
            print(f"{r['Source'][:40]:<40} | {r['Score']:<5} | {r['Verdict']}")
    else:
        print("\n❌ No results found. Is the server running?")

if __name__ == "__main__":
    main()