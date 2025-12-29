const scanBtn = document.getElementById("scanBtn");
const loading = document.getElementById("loading");
const resultDiv = document.getElementById("result");
const verdictEl = document.getElementById("verdict");
const scoreEl = document.getElementById("score");
const explanationEl = document.getElementById("explanation");

scanBtn.addEventListener("click", () => {
  // Reset UI
  resultDiv.classList.add("hidden");
  loading.classList.remove("hidden");
  loading.textContent = "Scanning...";

  chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
    const url = tabs[0].url;

    try {
      const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          type: "url",
          data: url
        })
      });

      // ✅ Check HTTP status FIRST
      if (!response.ok) {
        loading.textContent = `❌ Backend error (${response.status})`;
        return;
      }

      // ✅ Safely parse JSON
      let data;
      try {
        data = await response.json();
      } catch (err) {
        loading.textContent = "❌ Invalid response from backend";
        console.error("JSON parse error:", err);
        return;
      }

      // Show result
      loading.classList.add("hidden");
      resultDiv.classList.remove("hidden");

      verdictEl.textContent = data.verdict;
      scoreEl.textContent = `${data.final_score}/100`;
      explanationEl.textContent = data.ai_explanation;

      // Reset verdict color
      verdictEl.className = "";

      if (data.verdict === "SAFE") verdictEl.classList.add("safe");
      else if (data.verdict === "SUSPICIOUS") verdictEl.classList.add("suspicious");
      else if (data.verdict === "SCAM") verdictEl.classList.add("scam");

    } catch (err) {
      loading.textContent = "❌ Backend not running";
      console.error("Fetch error:", err);
    }
  });
});
