const scanBtn = document.getElementById("scanBtn");
const loading = document.getElementById("loading");
const resultDiv = document.getElementById("result");
const verdictEl = document.getElementById("verdict");
const scoreEl = document.getElementById("score");
const explanationEl = document.getElementById("explanation");

/* ---------- Render Result ---------- */
function displayResult(data) {
  loading.classList.add("hidden");
  resultDiv.classList.remove("hidden");

  verdictEl.textContent = data.verdict;
  scoreEl.textContent = `${data.final_score}/100`;
  explanationEl.textContent = data.ai_explanation;

  // Hide scan button once auto-scan is shown
  scanBtn.style.display = "none";

  // Reset body color
  document.body.className = "";

  if (data.verdict === "SAFE") document.body.classList.add("safe-bg");
  else if (data.verdict === "SUSPICIOUS") document.body.classList.add("suspicious-bg");
  else document.body.classList.add("scam-bg");
}

/* ---------- AUTO-SCAN DISPLAY ---------- */
document.addEventListener("DOMContentLoaded", () => {
  chrome.storage.local.get("lastScanResult", (res) => {
    if (res.lastScanResult) {
      displayResult(res.lastScanResult);
    } else {
      loading.textContent = "Click scan to analyze page";
      loading.classList.remove("hidden");
    }
  });
});

/* ---------- MANUAL SCAN (optional refresh) ---------- */
scanBtn.addEventListener("click", () => {
  loading.classList.remove("hidden");
  loading.textContent = "Scanning...";
  resultDiv.classList.add("hidden");

  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    fetch("http://127.0.0.1:8000/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        type: "url",
        data: tabs[0].url
      })
    })
      .then((res) => res.json())
      .then((data) => displayResult(data))
      .catch(() => {
        loading.textContent = "❌ Backend not running";
      });
  });
});
