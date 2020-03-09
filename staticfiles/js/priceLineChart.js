function drawChart(data, trendLine){
    // 1. Access the data
    const dateParser = d3.timeParse('%Q')
    const xAccessor = d => dateParser(d.date)
    const yAccessor = d => d.close

    // 2. Create Dimensions
    var container = $('#share-price-box')
    let dimensions = {
        width: window.innerWidth *0.75,
        height: window.innerHeight *0.45,
        margin: {
            top: 15,
            right: 15,
            bottom: 40,
            left: 60,
        }
    }
    dimensions.boundedWidth = dimensions.width
        - dimensions.margin.left
        - dimensions.margin.right
    dimensions.boundedHeight = dimensions.height
        - dimensions.margin.top
        - dimensions.margin.bottom

    // 3. Draw Canvas
    const wrapper = d3.select('#share-price-box')
        .append('svg')
        .attr('width', dimensions.width)
        .attr('height', dimensions.height)

    const bounds = wrapper.append("g")
        .style("transform", `translate(${
            dimensions.margin.left
        }px, ${
            dimensions.margin.top
        }px)`)

    // 4. Create Scales
    const yScale = d3.scaleLinear()
        .domain(d3.extent(data, yAccessor))
        .range([dimensions.boundedHeight, 0])
        .nice()

    const xScale = d3.scaleTime()
        .domain(d3.extent(data, xAccessor))
        .range([0, dimensions.boundedWidth])
    // Draw trades here if true
    // 5. Draw Data

    const areaGenerator = d3.area()
        .x(d => xScale(xAccessor(d)))
        .y0(dimensions.boundedHeight)
        .y1(d => yScale(yAccessor(d)))

    const lineGenerator = d3.line()
        .x(d => xScale(xAccessor(d)))
        .y(d => yScale(yAccessor(d)))

    const area = bounds.append('path')
        .attr('d', areaGenerator(data))
        .attr('fill', 'rgba(83,221,108,0.3)')
        .attr('stroke-width', 2)

    const line = bounds.append('path')
        .attr('d', lineGenerator(data))
        .attr('fill', trendLine)
        .attr('stroke', '#53dd6c')
        .attr('stroke-width', 1)

    // 6. Draw Peripherals
    const yAxisGenerator = d3.axisLeft()
        .scale(yScale)

    const yAxis = bounds.append("g")
        .call(yAxisGenerator)
    function makeYGridlines(){
        return d3.axisLeft(yScale)
            .ticks(8)
    }
    const yGridlines = bounds.append('g')
        .attr('class', 'grid')
        .call(makeYGridlines()
                .tickSize(-dimensions.width)
                .tickFormat('')
            )
    const xAxisGenerator = d3.axisBottom()
        .scale(xScale)

    const xAxis = bounds.append("g")
        .call(xAxisGenerator)
          .style("transform", `translateY(${
            dimensions.boundedHeight
          }px)`)

    // 7. Set up interactions 
}

$(document).ready(function(){
    drawChart(price_data, 'none');

    // $('#show_trend').click(function(){
    //     drawChart(price_data, 'true')
    // })
})