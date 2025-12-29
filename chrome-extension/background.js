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
      if (!response.ok) return null;
      return response.json();
    })
    .then((data) => {
      if (!data) return;

      // ✅ STORE RESULT PER URL (CRITICAL FIX)
      chrome.storage.local.set({
        [tab.url]: data
      });

      console.log("✅ Auto-scan stored for:", tab.url);
    })
    .catch((err) => {
      console.error("❌ Auto-scan failed:", err);
    });
});
