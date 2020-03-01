
// Initialise chart objects
const portfolioChart = new dc.LineChart('#portfolio-chart');
const volumeChart = new dc.BarChart('#monthly-volume-chart');

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
const dailyGainGroup = gainDays.group().reduceSum(d => Math.abs(d.gain));
const volumeByDayGroup = gainDays.group().reduceSum(d => d.volume);
const indexAvgByDayGroup = gainDays.group().reduce(
    (p, v) => {
        ++p.days;
        p.total += (v.open + v.close) / 2;
        p.avg = Math.round(p.total / p.days);
        return p;
    },
    (p, v) => {
        --p.days;
        p.total -= (v.open + v.close) / 2;
        p.avg = p.days ? Math.round(p.total / p.days) : 0;
        return p;
    },
    () => ({days: 0, total: 0, avg: 0})
)

function drawGraph(){
	//#### Stacked Area Chart

    //Specify an area chart by using a line chart with `.renderArea(true)`.
    // <br>API: [Stack Mixin](https://dc-js.github.io/dc.js/docs/html/StackMixin.html),
    // [Line Chart](https://dc-js.github.io/dc.js/docs/html/LineChart.html)
    portfolioChart /* dc.lineChart('#monthly-move-chart', 'chartGroup') */
        .renderArea(true)
        .width(1100)
        .height(500)
        .transitionDuration(1000)
        .margins({top: 30, right: 50, bottom: 25, left: 40})
        .dimension(gainDays)
        .mouseZoomable(true)
    // Specify a "range chart" to link its brush extent with the zoom of the current "focus chart".
        .rangeChart(volumeChart)
        .x(d3.scaleTime().domain([new Date(2018, 0, 1), new Date(2020, 2, 29)]))
        .round(d3.timeMonth.round)
        .xUnits(d3.timeMonths)
        .elasticY(true)
        .renderHorizontalGridLines(true)
    //##### Legend

        // Position the legend relative to the chart origin and specify items' height and separation.
        .legend(new dc.Legend().x(800).y(10).itemHeight(13).gap(5))
        .brushOn(false)
        // Add the base layer of the stack with group. The second parameter specifies a series name for use in the
        // legend.
        // The `.valueAccessor` will be used for the base layer
        .group(indexAvgByDayGroup, 'Monthly Portfolio Average')
        .valueAccessor(d => d.value.avg)
        // Stack additional layers with `.stack`. The first paramenter is a new group.
        // The second parameter is the series name. The third is a value accessor.
        .stack(dailyGainGroup, 'Daily Portfolio Gain', d => d.value)
        // Title can be called by any stack layer.
        .title(d => {
            let value = d.value.avg ? d.value.avg : d.value;
            if (isNaN(value)) {
                value = 0;
            }
            return `${dateFormat(d.key)}\n${numberFormat(value)}`;
        });

    //#### Range Chart

    // Since this bar chart is specified as "range chart" for the area chart, its brush extent
    // will always match the zoom of the area chart.
    volumeChart.width(1100) /* dc.barChart('#monthly-volume-chart', 'chartGroup'); */
        .height(40)
        .margins({top: 0, right: 50, bottom: 20, left: 40})
        .dimension(gainDays)
        .group(volumeByDayGroup)
        .centerBar(true)
        .gap(1)
        .x(d3.scaleTime().domain([new Date(2018, 0, 1), new Date(2020, 2, 29)]))
        .round(d3.timeMonth.round)
        .alwaysUseRounding(true)
        .xUnits(d3.timeMonths);

    // Render the charts
    dc.renderAll();
}

$(document).ready(function(){
	drawGraph();
})