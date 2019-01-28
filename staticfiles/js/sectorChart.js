var sectorData;
var tickerData;
var graphOptions;
var sectorChart;
var tickerChart;

var sectorctx = document.getElementById("sector-chart");
var tickerctx = document.getElementById("ticker-chart");

// Utility Functions
function getSectors(quotes){
    var sectors = {}
    for (var d in quotes){
    	if (quotes[d]['sector'] in sectors){
    		sectors[quotes[d]['sector']] += 1
    	}
        else{
        	sectors[quotes[d]['sector']] = 1
        }
    }
    return sectors
}

function drawGraphs(quotes, stocks){
    // Chart settings
    sectorObject = getSectors(quotes);
    tickerObject = stocks;
    var bootstrapColors = [
	            '#17a2b8',
	            '#ffc107',
	            '#28a745',
	            '#dc3545',
	            '#007bff',
	            '#ffffff',
	            '#868e96',
	            '#'
        	]

    sectorData =  {
        labels: Object.keys(sectorObject),
        datasets: [{
            data: Object.values(sectorObject),
            backgroundColor: bootstrapColors
        }],
    };

    tickerData =  {
        labels: Object.keys(tickerObject),
        datasets: [{
            data: Object.values(tickerObject),
            backgroundColor: bootstrapColors
        }],
    };

    graphOptions = {
   		maintainAspectRatio: false,
   		legend: {
            display: true,
            labels: {
                  fontColor: 'white'
                }
        }  		 	
    }

    sectorChart = new Chart(sectorctx, {
        type: 'doughnut',
        data: sectorData,
        options: graphOptions
    });
    tickerChart = new Chart(tickerctx, {
        type: 'doughnut',
        data: tickerData,
        options: graphOptions
    });
    $('#loading-gif').hide();
}

// Charts
$(document).ready(function(){
    sectorctx.height = ($(window).height())*0.25;
    tickerctx.height = ($(window).height())*0.25;
    drawGraphs(quotes, stocks);
})
