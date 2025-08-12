const form = document.getElementById("form");
const symbolInput = document.getElementById("symbol");
const errorMsg = document.getElementById("error");
const ctx = document.getElementById("chart");
let chart;

form.addEventListener("submit", async function(e) {
    e.preventDefault();
    const symbol = symbolInput.value.trim().toUpperCase();
    if (!symbol) {
        errorMsg.textContent = "Please enter a symbol.";
        return;
    }
    errorMsg.textContent = "";

    try {
        const res = await fetch(`/api/price?symbol=${symbol}`);
        const data = await res.json();
        if (data.error) {
            errorMsg.textContent = data.error;
            return;
        }

        const dates = data.series.map(item => item.date);
        const closes = data.series.map(item => item.close);

        if (chart) chart.destroy();
        chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{ label: symbol, data: closes, borderColor: 'blue', fill: false }]
            }
        });
    } catch (err) {
        errorMsg.textContent = "Error fetching data.";
    }
});
