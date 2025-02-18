async function searchUser() {
    const username = document.getElementById("username").value.trim();
    const resultsDiv = document.getElementById("results");
    const defaultMessage = document.getElementById("default-message");


    if (!username) {
        alert("Please enter a username.");
        return;
    }
    // Hide the default message
    defaultMessage.style.display = "none";
    try {
        const response = await fetch(`http://127.0.0.1:5000/search?username=${username}`);
        const data = await response.json();

        resultsDiv.innerHTML = ""; // Clear previous results

        if (data.error) {
            resultsDiv.innerHTML = `<p class="error">Error: Data Unavailable</p>`;
        } else {
            resultsDiv.innerHTML = `
                <h2>Player: ${data.username}</h2>
                <h3>Overall Stats</h3>
                ${generateStatsHTML(data.overall)}

                <h3>Solos Stats</h3>
                ${generateStatsHTML(data.solos)}

                <h3>Quads Stats</h3>
                ${generateStatsHTML(data.quads)}
            `;
        }
    } catch (error) {
        resultsDiv.innerHTML = `<p class="error">Failed to fetch data</p>`;
    }
}

function generateStatsHTML(stats) {
    return `
        <p><strong>Wins:</strong> ${stats.wins}</p>
        <p><strong>Win Rate:</strong> ${stats.winRate.toFixed(2)}%</p>
        <p><strong>Matches Played:</strong> ${stats.matches}</p>
        <p><strong>Total Kills:</strong> ${stats.kills}</p>
        <p><strong>K/D Ratio:</strong> ${stats.kd.toFixed(2)}</p>
        <p><strong>Deaths:</strong> ${stats.deaths}</p>
        <p><strong>Kills per Match:</strong> ${stats.killsPerMatch.toFixed(2)}</p>
        <p><strong>Minutes Played:</strong> ${stats.minutesPlayed}</p>
        <p><strong>Score:</strong> ${stats.score}</p>
        <p><strong>Score per Match:</strong> ${stats.scorePerMatch.toFixed(2)}</p>
        <p><strong>Score per Minute:</strong> ${stats.scorePerMin.toFixed(2)}</p>
    `;
}


// Function to add color syntax highlighting to JSON output
function syntaxHighlight(json) {
    json = json.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^"\\])*"(\s*:)?|\b(true|false|null)\b|\b-?\d+(?:\.\d*)?(?:[eE][+-]?\d+)?\b)/g, function(match) {
        let cls = "number";
        if (/^"/.test(match)) {
            if (/:$/.test(match)) {
                cls = "key";
            } else {
                cls = "string";
            }
        } else if (/true|false/.test(match)) {
            cls = "boolean";
        } else if (/null/.test(match)) {
            cls = "null";
        }
        return `<span class="${cls}">${match}</span>`;
    });
}

