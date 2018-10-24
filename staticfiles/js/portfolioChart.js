var graphData;
var portfolioOptions;
var mixedChart;

var portfolioctx = document.getElementById("portfolio-chart");

// Utility Functions
function getGain(data){
    var dayGains = []
    data.forEach(function(d){
        dayGains.push(Number(d.gain))
    })
    console.log(dayGains)
    return dayGains
}

function getGainPct(data){
    var dayGains = []
    data.forEach(function(d){
        dayGains.push(Number(d.pct_gain))
    })
    console.log(dayGains)
    return dayGains
}

function getBenchmark(data){
    var benchmarks = []
    data.forEach(function(d){
        benchmarks.push(Number(d.benchmark_gain))
    })
    console.log(benchmarks)
    return benchmarks
}

function getDailyLabels(data){
    var days = []
    data.forEach(function(d){
        var day_date = new Date(d.date)
        days.push(day_date.toDateString());
    })
    console.log(days)
    return days
}

function drawGraph(portfolio, metric){
    // Chart settings

    graphData =  {
        labels: getDailyLabels(portfolio),
        datasets: [{
            label: "Gain ($)",
            backgroundColor: 'rgb(45, 134, 51, 0.2)',
            borderColor: 'rgb(45, 134, 51)',
            data: metric(portfolio),
            type: 'line',
            yAxisID: 'gain'
        },
        {
            label: "Benchmark",
            data: getBenchmark(portfolio),
            yAxisID: 'benchmark'
        }],
    };

    portfolioOptions = {
        maintainAspectRatio: false,
        elements: {
            line: {
                tension: 0, // disables bezier curves
            },
            point: {
                radius: 1,
            },
        },
        scales: {
            xAxes: [{
                type: 'time',
                time: {
                    displayFormats: {
                        quarter: 'MMM YYYY'
                    }
                },
                display: true
            }],
            yAxes: [{
                id: 'gain'
            },
            {
                id: 'benchmark',
                position: 'right',
                display: false,
            }]
        },
        legend: {
            display: true,
        }
    }

    mixedChart = new Chart(portfolioctx, {
        type: 'bar',
        data: graphData,
        options: portfolioOptions
    });
    $('#loading-gif').hide();
}

// Charts
$(document).ready(function(){
    portfolioctx.height = ($(window).height())*0.55;
    console.log(typeof portfolio)
    drawGraph(portfolio, getGain);
    $('#pct_view').click(function(){
         if(mixedChart){
            mixedChart.destroy();
        }
        drawGraph(portfolio, getGainPct)
    })
    $('#dollar_view').click(function(){
         if(mixedChart){
            mixedChart.destroy();
        }
        drawGraph(portfolio, getGain)
    })
})
