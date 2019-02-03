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

var Options = {
   	maintainAspectRatio: false,
   	legend: {
        display: true,
        position: 'right',
        labels: {
            fontColor: 'white'
        }
    }  		 	
}

function createGraph(data, ctx, options, type){
	var bootstrapColors = [
	    '#17a2b8',
	    '#ffc107',
	    '#28a745',
	    '#dc3545',
	    '#007bff',
	    '#ffffff',
	    '#868e96',
        ]
    var graphData = {
        labels: Object.keys(data),
        datasets: [{
            data: Object.values(data),
            backgroundColor: bootstrapColors
        }],
    };

    var graph = new Chart(ctx, {
        type: type,
        data: graphData,
        options: options
    });

}

// Charts
$(document).ready(function(){
    createGraph(stocks, tickerctx, Options, 'doughnut');
    createGraph(getSectors(quotes), sectorctx, Options, 'doughnut');
})
