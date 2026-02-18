// Get all visible text from the webpage
function getPageText() {
    return document.body.innerText;
}

// Send text to backend
async function analyzeText(text) {
    try {
        const response = await fetch("http://127.0.0.1:5000/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();
        showAlert(data.status, data.score);
    } catch (error) {
        console.error("Error connecting to RiskWatch backend:", error);
    }
}

// Show banner on page
function showAlert(status, score) {
    const banner = document.createElement("div");
    banner.style.position = "fixed";
    banner.style.top = "0";
    banner.style.left = "0";
    banner.style.width = "100%";
    banner.style.padding = "10px";
    banner.style.textAlign = "center";
    banner.style.fontSize = "16px";
    banner.style.fontWeight = "bold";
    banner.style.zIndex = "9999";

    if (status === "CRITICAL") {
        banner.style.backgroundColor = "red";
        banner.style.color = "white";
        banner.innerText = "⚠️ RiskWatch Alert: CRITICAL Content Detected | Score: " + score;
    } else {
        banner.style.backgroundColor = "green";
        banner.style.color = "white";
        banner.innerText = "✅ RiskWatch: Page Safe | Score: " + score;
    }

    document.body.prepend(banner);
}

// Run after page loads
window.addEventListener("load", () => {
    const pageText = getPageText();
    analyzeText(pageText);
});
