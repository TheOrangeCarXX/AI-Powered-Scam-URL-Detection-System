chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete" && tab.url?.startsWith("http")) {

    fetch("http://127.0.0.1:8000/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        type: "url",
        data: tab.url
      })
    })
    .then(res => res.json())
    .then(data => {
      // Store last scan result for popup
      chrome.storage.local.set({
        lastScanResult: data
      });
    })
    .catch(err => {
      console.error("Auto-scan failed:", err);
    });
  }
});
