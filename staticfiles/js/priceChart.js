var graphData;
var priceOptions;
var mixedChart;

var pricectx = document.getElementById("share-price-chart");

// Utility Functions

function getChartData(range, trades){
    $('#loading-gif').show();
    $.get("https://api.iextrading.com/1.0/stock/"+ ticker +"/chart/"+range, 
    function(iexdata, status){
        drawGraph(iexdata, trades);
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
    return max_val*4
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

function getTrades(trades, show){
    var annotations = [];
    for (var i = trades.length - 1; i >= 0; i--) {
        annotations.push({
                type: 'line',
                mode: 'horizontal',
                scaleID: 'price',
                value: trades[i]['price'],
                borderColor: 'rgb(75, 192, 192)',
                borderWidth: 1,
                label: {
                  enabled: true,
                  position: 'center',
                  content: trades[i]['type'] + trades[i]['amount'] + ', ' + trades[i]['date']
                },
                onMouseover: function(e){
                    var element = this;
                    element.options.label.enabled = true;
                    element.chartInstance.update();
                }
              })         
    }
    if (show){
        return annotations
    }
    else{
        return [];
    }
}

function drawGraph(iexdata, showTrades){
    // Chart settings

    graphData =  {
        labels: getDailyLabels(iexdata),
        datasets: [{
            label: "Share Price",
            backgroundColor: 'rgb(45, 134, 51, 0.2)',
            borderColor: 'rgb(45, 134, 51)',
            data: getClosePrices(iexdata),
            type: 'line',
            yAxisID: 'price',
            xAxisID: 'daily'
        },
        {
            label: "Volume",
            data: getVolumes(iexdata),
            yAxisID: 'volume',
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
                id: 'quarters',
                type: 'time',
                time: {
                    displayFormats: {
                        quarter: 'MMM YYYY'
                    }
                },
                ticks: {
                    fontColor: 'white'
                },
                display: true
            },
            {
                id: 'daily',
                time: {
                    unit: 'day',
                },
                display: false,
            }],
            yAxes: [{
                id: 'price',
                ticks: {
                    fontColor: 'white'
                }
            },
            {
                id: 'volume',
                position: 'right',
                display: false,
                ticks: {
                    max: getMaxVolume(iexdata)
                }
            }]
        },
        legend: {
            display: false,
        },
        annotation: {
            annotations: getTrades(trades, showTrades)
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
    // pricectx.height = ($(window).height())*0.45;
    getChartData("6m", false);

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
        $('#graph_timelines').show()
    })
    $('#show_trades').click(function(){
        var time = $('.priceChart.active').attr('id')
        if(mixedChart){
            mixedChart.destroy();
        }
        if($(this).hasClass('active')){
            getChartData(time, false);
            $(this).removeClass('active');
        }
        else{
            getChartData(time, true);
            $(this).addClass('active');
        }
    })
    $('#timeIn').click(function(){
        $('.priceChart').removeClass('active');
        $('#timeIn').addClass('active');
        drawGraph("5y");
        $('#time_btns').hide()
        $('#graph_timelines').show()
    })
})
