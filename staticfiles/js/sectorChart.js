var sectorData;
var sectorOptions;
var sectorChart;

var sectorctx = document.getElementById("sector-chart");

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

function drawSectors(quotes){
    // Chart settings
    sectorObject = getSectors(quotes);

    sectorData =  {
        labels: Object.keys(sectorObject),
        datasets: [{
            data: Object.values(sectorObject),
        }],
    };

    sectorChart = new Chart(sectorctx, {
        type: 'doughnut',
        data: sectorData,
        options: Chart.defaults.doughnut
    });
    $('#loading-gif').hide();
}

// Charts
$(document).ready(function(){
    sectorctx.height = ($(window).height())*0.15;
    drawSectors(quotes);
})
