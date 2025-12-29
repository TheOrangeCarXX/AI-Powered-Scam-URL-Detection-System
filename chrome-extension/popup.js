const scanBtn = document.getElementById("scanBtn");
const loading = document.getElementById("loading");
const resultDiv = document.getElementById("result");
const verdictEl = document.getElementById("verdict");
const scoreEl = document.getElementById("score");
const explanationEl = document.getElementById("explanation");

scanBtn.addEventListener("click", async () => {
  // Show loading, hide result
  loading.classList.remove("hidden");
  resultDiv.classList.add("hidden");

  chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
    const url = tabs[0].url;

    try {
      const response = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          type: "url",
          data: url
        })
      });

      const data = await response.json();

      // Hide loading, show result
      loading.classList.add("hidden");
      resultDiv.classList.remove("hidden");

      // Verdict text
      verdictEl.textContent = data.verdict;

      // Final risk score
      scoreEl.textContent = `${data.final_score}/100`;

      // Gemini explanation
      explanationEl.textContent = data.ai_explanation;

      // Reset classes
      verdictEl.className = "";

      // Apply color class
      if (data.verdict === "SAFE") verdictEl.classList.add("safe");
      if (data.verdict === "SUSPICIOUS") verdictEl.classList.add("suspicious");
      if (data.verdict === "SCAM") verdictEl.classList.add("scam");

    } catch (err) {
      loading.textContent = "❌ Backend not running";
      console.error(err);
    }
  });
});
