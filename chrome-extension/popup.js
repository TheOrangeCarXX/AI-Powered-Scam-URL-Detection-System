const scanBtn = document.getElementById("scanBtn");
const loading = document.getElementById("loading");
const resultDiv = document.getElementById("result");
const verdictEl = document.getElementById("verdict");
const scoreEl = document.getElementById("score");
const explanationEl = document.getElementById("explanation");

/* ---------- Helper to render result ---------- */
function displayResult(data) {
  loading.classList.add("hidden");
  resultDiv.classList.remove("hidden");

  verdictEl.textContent = data.verdict;
  scoreEl.textContent = `${data.final_score}/100`;
  explanationEl.textContent = data.ai_explanation;

  verdictEl.className = "";
  if (data.verdict === "SAFE") verdictEl.classList.add("safe");
  else if (data.verdict === "SUSPICIOUS") verdictEl.classList.add("suspicious");
  else verdictEl.classList.add("scam");
}

/* ---------- AUTO-SCAN RESULT (from background.js) ---------- */
document.addEventListener("DOMContentLoaded", () => {
  chrome.storage.local.get("lastScanResult", (res) => {
    if (res.lastScanResult) {
      displayResult(res.lastScanResult);
    }
  });
});

/* ---------- MANUAL SCAN (backup) ---------- */
scanBtn.addEventListener("click", () => {
  resultDiv.classList.add("hidden");
  loading.classList.remove("hidden");
  loading.textContent = "Scanning...";

  chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
    const url = tabs[0].url;

    try {
      const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ type: "url", data: url })
      });

      if (!response.ok) {
        loading.textContent = `❌ Backend error (${response.status})`;
        return;
      }

      let data;
      try {
        data = await response.json();
      } catch {
        loading.textContent = "❌ Invalid backend response";
        return;
      }

      displayResult(data);

    } catch (err) {
      loading.textContent = "❌ Backend not running";
      console.error(err);
    }
  });
});
