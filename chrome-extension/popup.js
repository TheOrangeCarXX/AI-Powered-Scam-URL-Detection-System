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

  // ✅ UX FIX: Explain baseline score for SAFE sites
  if (data.verdict === "SAFE" && data.final_score <= 30) {
    scoreEl.textContent = "Low risk (baseline checks)";
    explanationEl.textContent =
      "This website passed scam detection. A small baseline score is applied due to structural safety checks, not scam behavior.";
  } else {
    scoreEl.textContent = `${data.final_score}/100`;
    explanationEl.textContent = data.ai_explanation;
  }

  scanBtn.style.display = "none";

  document.body.className = "";
  if (data.verdict === "SAFE") document.body.classList.add("safe-bg");
  else if (data.verdict === "SUSPICIOUS") document.body.classList.add("suspicious-bg");
  else document.body.classList.add("scam-bg");
}

/* ---------- AUTO DISPLAY (URL-AWARE) ---------- */
document.addEventListener("DOMContentLoaded", () => {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const currentUrl = tabs[0].url;

    chrome.storage.local.get(currentUrl, (res) => {
      if (res[currentUrl]) {
        displayResult(res[currentUrl]);
      } else {
        loading.textContent = "Scanning page…";
        loading.classList.remove("hidden");
      }
    });
  });
});

/* ---------- MANUAL SCAN (OPTIONAL) ---------- */
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
      .then((data) => {
        chrome.storage.local.set({ [tabs[0].url]: data });
        displayResult(data);
      })
      .catch(() => {
        loading.textContent = "❌ Backend not running";
      });
  });
});
