
// Initialise chart objects
const portfolioChart = new dc.CompositeChart('#portfolio-chart');
const volumeChart = new dc.BarChart('#daily-volume-chart');
const stockPie = new dc.PieChart('#ticker-chart');
const heldBar = new dc.RowChart('#held-chart');

// Convert portfolio dates for d3
const dateFormatSpecifier = '%Q';
const dateFormat = d3.timeFormat(dateFormatSpecifier);
const dateFormatParser = d3.timeParse(dateFormatSpecifier);
const numberFormat = d3.format('.2f');

portfolio.forEach(d => {
    d.dd = dateFormatParser(d.date);
    d.month = d3.timeMonth(d.dd); // pre-calculate month for better performance
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
        p.value -= v.value
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
        p.value -= v.value
		p.gain -= v.gain
		p.gain_percentage = (p.gain/p.invested)*100
		p.bench_gain -= v.bench_gain
		p.bench_gain_percentage = (p.bench_gain/p.invested)*100
		return p
	},
	// Init
	function(){
		return {bench_gain: 0, bench_gain_percentage: 0, gain: 0, invested: 0, gain_percentage: 0, count: 0, value: 0};
	}
);
const volumeByDayGroup = gainDays.group().reduceSum(d => d.volume);
const dailyBenchGainGroup = gainDays.group().reduceSum(d => d.bench_gain);
const tickerHeldGroup = stockDimension.group();
const tickerValueGroup = stockDimension.group().reduce(
    // add
    function (p, v){
        ++p.count;
        if(v.date > p.date){
            p.date = v.date
            p.value = v.value
            p.invested = v.invested
        }
        console.log(p)
        return p
    },
    // remove
    function (p, v){
        --p.count;
        if(v.date < p.date){
            p.date = v.date
            p.value = v.value
            p.invested = v.invested
        }
        console.log(p)
        return p
    },
    // Init
    function(){
        return {count: 0, value: 0, invested: 0, date: 0};
    }
);

const colorScale = d3.scaleOrdinal(chartColors)

function drawGraphs(gainGroup, benchGroup, gainValueAccessor, benchValueAccessor){
	//#### Stacked Area Chart
	// Width/Heights
	var portfolioWidth = $('#portfolio-chart').width();
	var portfolioHeight = $('#portfolio-chart').height();
	var volumeHeight = $('#daily-volume-chart').height();
    var piesHeight = $('#ticker-chart').height();
    var piesWidth = $('#ticker-chart').width();
    var heldWidth = $('#held-chart').width();

    // Composite chart with benchmark and gain value Accessors define percentage or dollar value
    portfolioChart
        .width(portfolioWidth)
        .height(portfolioHeight)
        .transitionDuration(2000)
        .margins({top: 50, right: 20, bottom: 25, left: 40})
        .dimension(gainDays)
        .mouseZoomable(false)
    // Specify a "range chart" to link its brush extent with the zoom of the current "focus chart".
        .rangeChart(volumeChart)
        .elasticY(true)
        .x(d3.scaleTime().domain(d3.extent(portfolio, d => d.dd)))
        .round(d3.timeDay.round)
        .xUnits(d3.timeDays)
        .renderHorizontalGridLines(true)
    // ##### Legend
        // Position the legend relative to the chart origin and specify items' height and separation.
        .legend(new dc.Legend().x(50).y(10).itemHeight(13).gap(5))
        .brushOn(false)
        .shareTitle(true)
        .title(d => {
                let value = gainValueAccessor(d);
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
            })
        .compose([
            new dc.LineChart(portfolioChart)
                    .renderArea(true)
                    .dimension(gainDays)
                    .colors(portfolioColor)
                    .group(gainGroup, 'Daily Portfolio Gain')
                    .valueAccessor(d => gainValueAccessor(d)),
            new dc.LineChart(portfolioChart)
                    .renderArea(true)
                    .dimension(gainDays)
                    .colors(benchmarkColor)
                    .group(benchGroup, 'Daily Benchmark Gain')
                    .valueAccessor(d => benchValueAccessor(d))
            ])

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
        .ordinalColors([volumeColor])
        .x(d3.scaleTime().domain(d3.extent(portfolio, d => d.dd)))
        .round(d3.timeDay.round)
        .alwaysUseRounding(true)
        .title(d => {
        	return `Volume: ${numberFormat(d.value)}`
        })
        .xUnits(d3.timeMonths);

    // A pie chart showing current value of each ticker in portfolio
    stockPie.width(piesHeight*0.9)
        .height(piesHeight*0.9)
        .slicesCap(100)
        .innerRadius(piesHeight*0.2)
        .dimension(stockDimension)
        .group(tickerValueGroup)
        .valueAccessor(d => d.value.value)
        .colors(colorScale)
        .on('pretransition', function(chart) {
            chart.selectAll('text.pie-slice').text(function(d) {
                return d.data.key + ' ' + dc.utils.printSingleValue((d.endAngle - d.startAngle) / (2*Math.PI) * 100) + '%';
            })
        });

    // A row chart showing odays tciker held for
    heldBar.width(heldWidth*0.98)
        .height(piesHeight*0.9)
        .dimension(stockDimension)
        .group(tickerHeldGroup)
        .elasticX(true)
        .gap(10)
        .title(d => {
            return `Days Held: ${numberFormat(d.value)}`
        })
        .ordinalColors(chartColors)

    // Render the charts
    dc.renderAll();
}

$(document).ready(function(){
	$('#pct_view').click(function(){
		drawGraphs(dailyGainPctGroup, dailyGainPctGroup, function(x){return x.value.gain_percentage}, function(x){return x.value.bench_gain_percentage});
		$('.portfolio_filters').removeClass('active');
		$(this).addClass('active')
        $('#ticker-chart').addClass('pct')
	})
	$('#dollar_view').click(function(){
		drawGraphs(dailyGainGroup, dailyBenchGainGroup, function(x){return x.value}, function(x){return x.value});
		$('.portfolio_filters').removeClass('active');
		$(this).addClass('active')
        $('#ticker-chart').removeClass('pct')
	})
	drawGraphs(dailyGainPctGroup, dailyGainPctGroup, function(x){return x.value.gain_percentage}, function(x){return x.value.bench_gain_percentage});
    $('#openMenu').click(function(){
        setTimeout(function(){
            drawGraphs(dailyGainPctGroup, dailyGainPctGroup, function(x){return x.value.gain_percentage}, function(x){return x.value.bench_gain_percentage});
        }, 25);
    })
    $('#closeMenu').click(function(){
        setTimeout(function(){
            drawGraphs(dailyGainPctGroup, dailyGainPctGroup, function(x){return x.value.gain_percentage}, function(x){return x.value.bench_gain_percentage});
        }, 25);
    })
})