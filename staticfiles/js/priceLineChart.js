function drawChart(data, trendLine, update){
    if(update){
        d3.select("svg").remove();
    }
    // 1. Access the data
    const xAccessor = d => d.date
    const yAccessor = d => d.close

    // 2. Create Dimensions
    var container = $('#share-price-box')
    let dimensions = {
        width: container.width()*0.99,
        height: container.height(),
        margin: {
            top: 15,
            right: 5,
            bottom: 40,
            left: 40,
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

function filterData(data, months){
    var startDate = new Date().setMonth(new Date().getMonth() - months)
    var data = data.filter(function(d){
        return d.date > startDate
    })
    return data
}

function parseDate(data){
    var dateParser = d3.timeParse('%Q')
    data.forEach(function(d){
        d.date = dateParser(d.date)
    })
    return data
}

$(document).ready(function(){
    current_data = parseDate(price_data);
    trend = 'none'
    drawChart(current_data, trend, false);

    $('#show_trend').click(function(){
        if($(this).hasClass('active')){
            trend = 'none';
            $(this).removeClass('active')
        }
        else{
            trend = 'true';
            $(this).addClass('active')
        }
        drawChart(current_data, trend, true)
    })


    $('.priceChart').click(function(){
        months = $(this).attr('id');
        $('.priceChart').removeClass('active');
        $(this).addClass('active');
        current_data = filterData(price_data, parseInt(months))
        drawChart(current_data, trend, true)
    })
    $('#openMenu').click(function(){
        setTimeout(function(){
            drawChart(current_data, trend, true);
        }, 50);
    })
    $('#closeMenu').click(function(){
        setTimeout(function(){
            drawChart(current_data, trend, true);
        }, 50);
    })

    $('#chart_settings').click(function(){
        $('.chart_setting').toggleClass('visible');
    })
})
