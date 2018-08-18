var graphData;
var priceOptions;
var myLineChart;

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
        }],
    };

    priceOptions = {
        maintainAspectRatio: false,
        elements: {
            line: {
                tension: 0, // disables bezier curves
            }
        },
        scales: {
            xAxes: [{
                time: {
                    unit: 'day'
                    },
                display: false
                }]
        }
    }

    myLineChart = new Chart(pricectx, {
        type: 'line',
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
        if(myLineChart){
            myLineChart.destroy();
        }
        console.log(time)
        getChartData(time);
    })
    $('#timeIn').click(function(){
        $('.priceChart').removeClass('active');
        $('#timeIn').addClass('active');
        drawGraph("5y");
    })
    $('#timeIn').addClass('active');
})
