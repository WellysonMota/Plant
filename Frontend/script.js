document.getElementById("refreshBtn").addEventListener("click", fetchSensorData);

const tempCard = document.getElementById("tempCard").querySelector("span");
const humidityCard = document.getElementById("humidityCard").querySelector("span");
const soilCard = document.getElementById("soilCard").querySelector("span");

const ctx = document.getElementById('sensorChart').getContext('2d');
let chart;

function renderChart(dataPoints) {
    const labels = dataPoints.map(d => new Date(d.timestamp).toLocaleTimeString());
    const tempData = dataPoints.map(d => d.temperature);
    const humidityData = dataPoints.map(d => d.humidity);
    const soilData = dataPoints.map(d => d.soil_moisture);

    if (chart) chart.destroy();

    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Temperatura (°C)',
                    data: tempData,
                    borderColor: 'rgb(255, 99, 132)',
                    fill: false
                },
                {
                    label: 'Umidade do Ar (%)',
                    data: humidityData,
                    borderColor: 'rgb(54, 162, 235)',
                    fill: false
                },
                {
                    label: 'Umidade do Solo (%)',
                    data: soilData,
                    borderColor: 'rgb(75, 192, 192)',
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'top' },
                title: { display: true, text: 'Histórico de Leituras' }
            }
        }
    });
}

async function fetchSensorData() {
    try {
        const response = await fetch("/api/sensors/latest");
        const latest = await response.json();
        
        humidityCard.textContent = latest.humidity.toFixed(1) + " %";
        tempCard.textContent = latest.temperature.toFixed(1) + " °C";        
        soilCard.textContent = latest.soil_moisture.toFixed(1) + " %";

        const historyRes = await fetch("/api/sensors/history");
        const history = await historyRes.json();

        renderChart(history);
    } catch (error) {
        alert("Erro ao buscar dados: " + error.message);
    }


}

async function getRelayStatus() {
    const res = await fetch('/api/relay/status');
    const data = await res.json();
    document.getElementById("relayStatus").textContent = data.status ? "Sim" : "Não";
}

async function toggleRelay(state) {
    const url = state ? "/api/relay/activate" : "/api/relay/deactivate";
    await fetch(url, { method: "POST" });
    getRelayStatus();
}

getRelayStatus(); // chama ao carregar a página


// Carregar dados ao abrir a página
fetchSensorData();
setInterval(fetchSensorData, 30000); // 60.000 ms = 1 minuto

