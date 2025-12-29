from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_scam_url():
    payload = {
        "type": "url",
        "data": "https://sbi-verify-account.xyz"
    }

    response = client.post("/analyze", json=payload)
    data = response.json()

    assert response.status_code == 200
    assert data["verdict"] in ["SCAM", "SUSPICIOUS"]
    assert data["final_score"] >= 40
    assert "ai_explanation" in data


def test_legit_url():
    payload = {
        "type": "url",
        "data": "https://www.onlinesbi.sbi"
    }

    response = client.post("/analyze", json=payload)
    data = response.json()

    assert response.status_code == 200
    assert data["verdict"] == "SAFE"
    assert data["final_score"] < 40


def test_scam_html():
    html = """
    <html>
      <body>
        <h2>Account will be blocked</h2>
        <form>
          <input type="password" placeholder="Enter OTP">
        </form>
      </body>
    </html>
    """

    payload = {
        "type": "html",
        "data": html
    }

    response = client.post("/analyze", json=payload)
    data = response.json()

    assert response.status_code == 200
    assert data["verdict"] in ["SCAM", "SUSPICIOUS"]
    assert data["final_score"] >= 40
    assert len(data["reasons"]) > 0


def test_legit_html():
    html = """
    <html>
      <body>
        <h2>Welcome to Our Bank</h2>
        <p>This page provides information about our services.</p>
      </body>
    </html>
    """

    payload = {
        "type": "html",
        "data": html
    }

    response = client.post("/analyze", json=payload)
    data = response.json()

    assert response.status_code == 200
    assert data["verdict"] == "SAFE"
    assert data["final_score"] < 40

