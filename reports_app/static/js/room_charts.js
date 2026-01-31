document.addEventListener('DOMContentLoaded', function() {
    const roomId = document.getElementById('room_id').value;
    loadRoomStats(roomId);
});

async function loadRoomStats(roomId) {
    try {
        const response = await fetch(`/reports/room_stats/${roomId}`);
        const data = await response.json();

        const categories = data.map(item => item.question); 
        const values = data.map(item => item.succesfull);   

        renderChart(categories, values);

    } catch (error) {
        console.error("Помилка завантаження статистики:", error);
    }
}

function renderChart(categories, values) {
    const options = {
        series: [{
            name: 'Успішність',
            data: values
        }],
        chart: {
            type: 'bar',
            height: 350,
            width: "100%",
            background: 'transparent',
            toolbar: { show: false }
        },
        plotOptions: {
            bar: {
                borderRadius: 4,
                columnWidth: '45%',
                distributed: true,
            }
        },
        colors: ['#FF4560', '#FEB019', '#00E396', '#008FFB', '#775DD0'],
        
        dataLabels: {
            enabled: true,
            formatter: function (val) {
                return val + "%";
            },
            style: {
                colors: ['#fff'],
                fontSize: '12px'
            }
        },
        xaxis: {
            categories: categories,
            labels: {
                style: {
                    colors: '#a1a1a1',
                    fontSize: '14px'
                }
            },
            axisBorder: { show: false },
            axisTicks: { show: false }
        },
        yaxis: {
            max: 100, 
            labels: {
                style: { colors: '#a1a1a1' }
            }
        },
        grid: {
            borderColor: '#333',
            yaxis: { lines: { show: true } }
        },
        legend: { show: false }, 
        tooltip: {
            theme: 'dark',
            y: {
                formatter: function (val) {
                    return val + "% правильних";
                }
            }
        },
        noData: {
            text: "Дані відсутні",
            style: { color: '#a1a1a1', fontSize: '16px' }
        }
    };

    const chart = new ApexCharts(document.querySelector("#questionsChart"), options);
    chart.render();
}