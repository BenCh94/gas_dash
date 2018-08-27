var graphData;
var priceOptions;
var mixedChart;

var pricectx = document.getElementById("share-price-chart");

// Utility Functions

function getChartData(range){
    $('#loading-gif').show();
    $.get("https://api.iextrading.com/1.0/stock/"+ ticker +"/chart/"+range, 
    function(iexdata, status){
        drawGraph(iexdata);
    })
}

function getClosePrices(data){
    var closePrices = []
    data.forEach(function(d){
        closePrices.push(Number(d.close))
    })
    console.log(closePrices)
    return closePrices
}

function getVolumes(data){
    var volumes = []
    data.forEach(function(d){
        volumes.push(Number(d.volume))
    })
    console.log(volumes)
    return volumes
}

function getMaxVolume(data){
    var vols = []
    data.forEach(function(d){
        vols.push(Number(d.volume))
    })
    var max_val = Math.max.apply(Math, vols)
    console.log(max_val)
    return max_val*10
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

function drawGraph(iexdata){
    // Chart settings

    graphData =  {
        labels: getDailyLabels(iexdata),
        datasets: [{
            label: "Share Price",
            backgroundColor: 'rgb(45, 134, 51, 0.2)',
            borderColor: 'rgb(45, 134, 51)',
            data: getClosePrices(iexdata),
            type: 'line',
            yAxisID: 'price'
        },
        {
            label: "Volume",
            data: getVolumes(iexdata),
            yAxisID: 'volume'
        }],
    };

    priceOptions = {
        maintainAspectRatio: false,
        elements: {
            line: {
                tension: 0, // disables bezier curves
            },
            point: {
                radius: 0,
            },
        },
        scales: {
            xAxes: [{
                time: {
                    unit: 'day'
                    },
                display: false
            }],
            yAxes: [{
                id: 'price'
            },
            {
                id: 'volume',
                position: 'right',
                display: false,
            }]
        },
        legend: {
            display: false,
        }
    }

    mixedChart = new Chart(pricectx, {
        type: 'bar',
        data: graphData,
        options: priceOptions
    });
    $('#loading-gif').hide();
}

// Charts
$(document).ready(function(){
    pricectx.height = ($(window).height())*0.525;
    getChartData("5y");

    $(".priceChart").click(function(e){
        $('.priceChart').removeClass('active');
        $('#timeIn').removeClass('active');
        $(this).addClass('active');
        var time = e.target.id;
        if(mixedChart){
            mixedChart.destroy();
        }
        console.log(time)
        getChartData(time);
    })
    $('#timeIn').click(function(){
        $('.priceChart').removeClass('active');
        $('#timeIn').addClass('active');
        drawGraph("5y");
    })
})
