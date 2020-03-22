
// Initialise chart objects
const portfolioChart = new dc.LineChart('#portfolio-chart');
const volumeChart = new dc.BarChart('#daily-volume-chart');
const stockPie = new dc.PieChart('#ticker-chart')

// Convert portfolio dates fro d3
const dateFormatSpecifier = '%Q';
const dateFormat = d3.timeFormat(dateFormatSpecifier);
const dateFormatParser = d3.timeParse(dateFormatSpecifier);
const numberFormat = d3.format('.2f');

portfolio.forEach(d => {
    d.dd = dateFormatParser(d.date);
    d.month = d3.timeMonth(d.dd); // pre-calculate month for better performance
    // d.close = +d.close; // coerce to number
    // d.open = +d.open;
});

// Create crossfilter object from portfolio data
const ndx = crossfilter(portfolio);
const all = ndx.groupAll();
// Create dimension and groups for charting
const gainDays = ndx.dimension(d => d.dd);
const stockDimension = ndx.dimension(d => d.ticker)
const dailyGainGroup = gainDays.group().reduceSum(d => d.gain);
const dailyGainPctGroup = gainDays.group().reduce(
	// add
	function (p, v){
		++p.count;
		p.invested += v.invested
		p.gain += v.gain
		p.gain_percentage = (p.gain/p.invested)*100
		p.bench_gain += v.bench_gain
		p.bench_gain_percentage = (p.bench_gain/p.invested)*100
		return p
	},
	// remove
	function (p, v){
		--p.count;
		p.invested -= v.invested
		p.gain -= v.gain
		p.gain_percentage = (p.gain/p.invested)*100
		p.bench_gain -= v.bench_gain
		p.bench_gain_percentage = (p.bench_gain/p.invested)*100
		return p
	},
	// Init
	function(){
		return {bench_gain: 0, bench_gain_percentage: 0, gain: 0, invested: 0, gain_percentage: 0, count: 0};
	}
);
const volumeByDayGroup = gainDays.group().reduceSum(d => d.volume);
const dailyBenchGainGroup = gainDays.group().reduceSum(d => d.bench_gain);
const tickerValueGroup = stockDimension.group().reduceSum(d => d.value)

function drawGraphs(gainGroup, benchGroup, valueAccessor, benchValueAccessor){
	//#### Stacked Area Chart
	// Width/Heights
	var portfolioWidth = $('#portfolio-chart').width();
	var portfolioHeight = $('#portfolio-chart').height();
	var volumeHeight = $('#daily-volume-chart').height();

    //Specify an area chart by using a line chart with `.renderArea(true)`.
    // <br>API: [Stack Mixin](https://dc-js.github.io/dc.js/docs/html/StackMixin.html),
    // [Line Chart](https://dc-js.github.io/dc.js/docs/html/LineChart.html)
    portfolioChart /* dc.lineChart('#monthly-move-chart', 'chartGroup') */
        .renderArea(true)
        .width(portfolioWidth)
        .height(portfolioHeight)
        .transitionDuration(2000)
        .margins({top: 50, right: 20, bottom: 25, left: 40})
        .dimension(gainDays)
        .mouseZoomable(false)
    // Specify a "range chart" to link its brush extent with the zoom of the current "focus chart".
        .rangeChart(volumeChart)
        .x(d3.scaleTime().domain([d3.min(portfolio, d => d.dd), d3.max(portfolio, d => d.dd)]))
        .round(d3.timeDay.round)
        .xUnits(d3.timeDays)
        .elasticY(true)
        .renderHorizontalGridLines(true)
    //##### Legend

        // Position the legend relative to the chart origin and specify items' height and separation.
        .legend(new dc.Legend().x(800).y(10).itemHeight(13).gap(5))
        .brushOn(false)
        .ordinalColors(['#4472CA', '#53dd6c'])
        // Add the base layer of the stack with group. The second parameter specifies a series name for use in the
        // legend.
        // The `.valueAccessor` will be used for the base layer
        .group(benchGroup, 'Daily Benchmark Gain')
        .valueAccessor(d => benchValueAccessor(d))
        // Stack additional layers with `.stack`. The first paramenter is a new group.
        // The second parameter is the series name. The third is a value accessor.
        .stack(gainGroup, 'Daily Portfolio Gain', d => valueAccessor(d))
        // Title can be called by any stack layer.
        .title(d => {
            let value = valueAccessor(d);
            let bench_value = benchValueAccessor(d);
            if (isNaN(value)) {
                return `${d.key.toISOString().slice(0,10)}\nBenchmark: $ ${numberFormat(bench_value)}`;
            }
            else if(bench_value == value){
            	return `${d.key.toISOString().slice(0,10)}\nGain: $ ${numberFormat(value)}`;
            }
            else{
            	return `${d.key.toISOString().slice(0,10)}\nGain: ${numberFormat(value)} %\nBenchmark: ${numberFormat(bench_value)} %`;
            }
        });

    //#### Range Chart

    // Since this bar chart is specified as "range chart" for the area chart, its brush extent
    // will always match the zoom of the area chart.
    volumeChart.width(portfolioWidth) /* dc.barChart('#monthly-volume-chart', 'chartGroup'); */
        .height(volumeHeight)
        .margins({top: 0, right: 20, bottom: 20, left: 40})
        .dimension(gainDays)
        .group(volumeByDayGroup)
        .centerBar(true)
        .gap(1)
        .ordinalColors(['#FFED65'])
        .x(d3.scaleTime().domain(d3.extent(portfolio, d => d.dd)))
        .round(d3.timeDay.round)
        .alwaysUseRounding(true)
        .title(d => {
        	return `Volume: ${numberFormat(d.value)}`
        })
        .xUnits(d3.timeMonths);

    // A pie chart showing overall value of each ticker in portfolio
    stockPie.width(350)
        .height(160)
        .slicesCap(4)
        .innerRadius(20)
        .dimension(stockDimension)
        .group(tickerValueGroup)
        .on('pretransition', function(chart) {
            chart.selectAll('text.pie-slice').text(function(d) {
                return d.data.key + ' ' + dc.utils.printSingleValue((d.endAngle - d.startAngle) / (2*Math.PI) * 100) + '%';
            })
        });

    // Render the charts
    dc.renderAll();
}

$(document).ready(function(){
	$('#pct_view').click(function(){
		drawGraphs(dailyGainPctGroup, dailyGainPctGroup, function(x){return x.value.gain_percentage}, function(x){return x.value.bench_gain_percentage});
		$('.portfolio_filters').removeClass('active');
		$(this).addClass('active')
	})
	$('#dollar_view').click(function(){
		drawGraphs(dailyGainGroup, dailyBenchGainGroup, function(x){return x.value}, function(x){return x.value});
		$('.portfolio_filters').removeClass('active');
		$(this).addClass('active')
	})
	drawGraphs(dailyGainPctGroup, dailyGainPctGroup, function(x){return x.value.gain_percentage}, function(x){return x.value.bench_gain_percentage});
    $('#openMenu').click(function(){
        setTimeout(function(){
            drawGraphs(dailyGainPctGroup, dailyGainPctGroup, function(x){return x.value.gain_percentage}, function(x){return x.value.bench_gain_percentage});
        }, 100);
    })
    $('#closeMenu').click(function(){
        setTimeout(function(){
            drawGraphs(dailyGainPctGroup, dailyGainPctGroup, function(x){return x.value.gain_percentage}, function(x){return x.value.bench_gain_percentage});
        }, 100);
    })
})