import os
import requests
import time

# Backend API endpoint
API_URL = "http://127.0.0.1:8000/analyze"

# Directory containing test HTML files
TEST_DATA_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "test-pages")
)

# Function to run the batch tests
def run_tests():
    print("\n🔍 Starting AI-Powered Security Batch Scan")
    print("=" * 90)
    print(f"{'CATEGORY':<10} | {'FILENAME':<35} | {'VERDICT':<12} | {'SCORE'}")
    print("-" * 90)

    if not os.path.exists(TEST_DATA_DIR):
        print(f"❌ Error: Test directory {TEST_DATA_DIR} not found.")
        return

    test_sets = [
        ("LEGIT", os.path.join(TEST_DATA_DIR, "legit")),
        ("FAKE", os.path.join(TEST_DATA_DIR, "fake")),
    ]

    for category, folder in test_sets:
        if not os.path.exists(folder):
            print(f"❌ Missing folder: {folder}")
            continue

        files = [f for f in os.listdir(folder) if f.endswith(".html")]

        for filename in sorted(files):
            file_path = os.path.join(folder, filename)

            with open(file_path, "r", encoding="utf-8") as f:
                html_content = f.read()

            payload = {
                "type": "html",
                "data": f"http://local-test/{category.lower()}/{filename}",
                "html": html_content
            }

            try:
                response = requests.post(API_URL, json=payload, timeout=10)

                if response.status_code != 200:
                    print(f"{category:<10} | {filename:<35} | ERROR {response.status_code}")
                    continue

                result = response.json()

                verdict = result.get("verdict", "UNKNOWN")
                score = result.get("final_score", 0)

                icon = "✅"
                if category == "FAKE" and verdict == "SAFE":
                    icon = "❌ (MISMATCH)"
                elif category == "LEGIT" and verdict == "SCAM":
                    icon = "⚠️ (FALSE POSITIVE)"

                print(
                    f"{category:<10} | {filename:<35} | "
                    f"{verdict:<12} | {score:>5.1f}/100 {icon}"
                )

            except requests.exceptions.ConnectionError:
                print("❌ Backend not running. Start FastAPI server first.")
                return
            except Exception as e:
                print(f"{category:<10} | {filename:<35} | ERROR: {str(e)}")

            # Prevent rate limiting
            time.sleep(0.4)

    print("-" * 90)
    print("Scan Complete.\n")

if __name__ == "__main__":
    run_tests()
