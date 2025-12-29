chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status !== "complete") return;
  if (!tab.url || !tab.url.startsWith("http")) return;

  fetch("http://127.0.0.1:8000/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      type: "url",
      data: tab.url
    })
  })
    .then((response) => {
      if (!response.ok) {
        console.error("Auto-scan backend error:", response.status);
        return null;
      }
      return response.json();
    })
    .then((data) => {
      if (!data) return;

      // ✅ SAFETY CHECK
      if (chrome?.storage?.local) {
        chrome.storage.local.set({ lastScanResult: data });
        console.log("✅ Auto-scan stored result for:", tab.url);
      } else {
        console.warn("chrome.storage.local not available yet");
      }
    })
    .catch((err) => {
      console.error("❌ Auto-scan failed:", err);
    });
});
