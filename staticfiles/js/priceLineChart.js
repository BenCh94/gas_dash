function drawChart(data, trendLine, update, drawTrades){
    if(update){
        d3.select("svg").remove();
    }
    // 1. Access the data
    const xAccessor = d => d.date
    const yAccessor = d => d.close
    const bisectDate = d3.bisector(function(d) { return d.date; }).left
    const formatDate = d3.timeFormat("%m/%d/%y")
    const formatValue = d3.format(',')

    // 2. Create Dimensions
    var container = $('#share-price-box')
    let dimensions = {
        width: container.width()*0.99,
        height: container.height(),
        margin: {
            top: 40,
            right: 65,
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

    // Draw trades here if true
    const tradeColorsBuy = ["#f7fcf5","#f6fcf4","#f6fcf4","#f5fbf3","#f5fbf2","#f4fbf2","#f4fbf1","#f3faf0","#f2faf0","#f2faef","#f1faee","#f1faee","#f0f9ed","#f0f9ec","#eff9ec","#eef9eb","#eef8ea","#edf8ea","#ecf8e9","#ecf8e8","#ebf7e7","#ebf7e7","#eaf7e6","#e9f7e5","#e9f6e4","#e8f6e4","#e7f6e3","#e7f6e2","#e6f5e1","#e5f5e1","#e4f5e0","#e4f4df","#e3f4de","#e2f4dd","#e1f4dc","#e1f3dc","#e0f3db","#dff3da","#def2d9","#ddf2d8","#ddf2d7","#dcf1d6","#dbf1d5","#daf1d4","#d9f0d3","#d8f0d2","#d7efd1","#d6efd0","#d5efcf","#d4eece","#d4eece","#d3eecd","#d2edcb","#d1edca","#d0ecc9","#cfecc8","#ceecc7","#cdebc6","#ccebc5","#cbeac4","#caeac3","#c9eac2","#c8e9c1","#c6e9c0","#c5e8bf","#c4e8be","#c3e7bd","#c2e7bc","#c1e6bb","#c0e6b9","#bfe6b8","#bee5b7","#bde5b6","#bbe4b5","#bae4b4","#b9e3b3","#b8e3b2","#b7e2b0","#b6e2af","#b5e1ae","#b3e1ad","#b2e0ac","#b1e0ab","#b0dfaa","#aedfa8","#addea7","#acdea6","#abdda5","#aadca4","#a8dca3","#a7dba2","#a6dba0","#a5da9f","#a3da9e","#a2d99d","#a1d99c","#9fd89b","#9ed799","#9dd798","#9bd697","#9ad696","#99d595","#97d494","#96d492","#95d391","#93d390","#92d28f","#91d18e","#8fd18d","#8ed08c","#8ccf8a","#8bcf89","#8ace88","#88cd87","#87cd86","#85cc85","#84cb84","#82cb83","#81ca82","#80c981","#7ec980","#7dc87f","#7bc77e","#7ac77c","#78c67b","#77c57a","#75c479","#74c478","#72c378","#71c277","#6fc276","#6ec175","#6cc074","#6bbf73","#69bf72","#68be71","#66bd70","#65bc6f","#63bc6e","#62bb6e","#60ba6d","#5eb96c","#5db86b","#5bb86a","#5ab769","#58b668","#57b568","#56b467","#54b466","#53b365","#51b264","#50b164","#4eb063","#4daf62","#4caf61","#4aae61","#49ad60","#48ac5f","#46ab5e","#45aa5d","#44a95d","#42a85c","#41a75b","#40a75a","#3fa65a","#3ea559","#3ca458","#3ba357","#3aa257","#39a156","#38a055","#379f54","#369e54","#359d53","#349c52","#339b51","#329a50","#319950","#30984f","#2f974e","#2e964d","#2d954d","#2b944c","#2a934b","#29924a","#28914a","#279049","#268f48","#258f47","#248e47","#238d46","#228c45","#218b44","#208a43","#1f8943","#1e8842","#1d8741","#1c8640","#1b8540","#1a843f","#19833e","#18823d","#17813d","#16803c","#157f3b","#147e3a","#137d3a","#127c39","#117b38","#107a37","#107937","#0f7836","#0e7735","#0d7634","#0c7534","#0b7433","#0b7332","#0a7232","#097131","#087030","#086f2f","#076e2f","#066c2e","#066b2d","#056a2d","#05692c","#04682b","#04672b","#04662a","#03642a","#036329","#026228","#026128","#026027","#025e27","#015d26","#015c25","#015b25","#015a24","#015824","#015723","#005623","#005522","#005321","#005221","#005120","#005020","#004e1f","#004d1f","#004c1e","#004a1e","#00491d","#00481d","#00471c","#00451c","#00441b"];
    const tradeColorsSell = ["#fff5f0","#fff4ef","#fff4ee","#fff3ed","#fff2ec","#fff2eb","#fff1ea","#fff0e9","#fff0e8","#ffefe7","#ffeee6","#ffeee6","#ffede5","#ffece4","#ffece3","#ffebe2","#feeae1","#fee9e0","#fee9de","#fee8dd","#fee7dc","#fee6db","#fee6da","#fee5d9","#fee4d8","#fee3d7","#fee2d6","#fee2d5","#fee1d4","#fee0d2","#fedfd1","#feded0","#feddcf","#fedccd","#fedbcc","#fedacb","#fed9ca","#fed8c8","#fed7c7","#fdd6c6","#fdd5c4","#fdd4c3","#fdd3c1","#fdd2c0","#fdd1bf","#fdd0bd","#fdcfbc","#fdceba","#fdcdb9","#fdccb7","#fdcbb6","#fdc9b4","#fdc8b3","#fdc7b2","#fdc6b0","#fdc5af","#fdc4ad","#fdc2ac","#fdc1aa","#fdc0a8","#fcbfa7","#fcbea5","#fcbca4","#fcbba2","#fcbaa1","#fcb99f","#fcb89e","#fcb69c","#fcb59b","#fcb499","#fcb398","#fcb196","#fcb095","#fcaf94","#fcae92","#fcac91","#fcab8f","#fcaa8e","#fca98c","#fca78b","#fca689","#fca588","#fca486","#fca285","#fca183","#fca082","#fc9e81","#fc9d7f","#fc9c7e","#fc9b7c","#fc997b","#fc987a","#fc9778","#fc9677","#fc9475","#fc9374","#fc9273","#fc9071","#fc8f70","#fc8e6f","#fc8d6d","#fc8b6c","#fc8a6b","#fc8969","#fc8868","#fc8667","#fc8565","#fc8464","#fb8263","#fb8162","#fb8060","#fb7f5f","#fb7d5e","#fb7c5d","#fb7b5b","#fb795a","#fb7859","#fb7758","#fb7657","#fb7455","#fa7354","#fa7253","#fa7052","#fa6f51","#fa6e50","#fa6c4e","#f96b4d","#f96a4c","#f9684b","#f9674a","#f96549","#f86448","#f86347","#f86146","#f86045","#f75e44","#f75d43","#f75c42","#f65a41","#f65940","#f6573f","#f5563e","#f5553d","#f4533c","#f4523b","#f4503a","#f34f39","#f34e38","#f24c37","#f24b37","#f14936","#f14835","#f04734","#ef4533","#ef4433","#ee4332","#ed4131","#ed4030","#ec3f2f","#eb3d2f","#eb3c2e","#ea3b2d","#e93a2d","#e8382c","#e7372b","#e6362b","#e6352a","#e5342a","#e43229","#e33128","#e23028","#e12f27","#e02e27","#df2d26","#de2c26","#dd2b25","#dc2a25","#db2924","#da2824","#d92723","#d72623","#d62522","#d52422","#d42321","#d32221","#d22121","#d12020","#d01f20","#ce1f1f","#cd1e1f","#cc1d1f","#cb1d1e","#ca1c1e","#c91b1e","#c71b1d","#c61a1d","#c5191d","#c4191c","#c3181c","#c2181c","#c0171b","#bf171b","#be161b","#bd161a","#bb151a","#ba151a","#b91419","#b81419","#b61419","#b51319","#b41318","#b21218","#b11218","#b01218","#ae1117","#ad1117","#ac1117","#aa1017","#a91016","#a71016","#a60f16","#a40f16","#a30e15","#a10e15","#a00e15","#9e0d15","#9c0d14","#9b0c14","#990c14","#970c14","#960b13","#940b13","#920a13","#900a13","#8f0a12","#8d0912","#8b0912","#890812","#870811","#860711","#840711","#820711","#800610","#7e0610","#7c0510","#7a0510","#78040f","#76040f","#75030f","#73030f","#71020e","#6f020e","#6d010e","#6b010e","#69000d","#67000d"];
    // tradeDraw function
    function tradeLine(trade, index){
        if(trade.type == 'b'){
            tradeColor = tradeColorsBuy[index];
        }
        else{
            tradeColor = tradeColorsSell[index];
        }
        const tradePrice = bounds.append("line")
            .attr("x1", xScale(d3.min(data, d => d.date)))
            .attr("x2", xScale(d3.max(data, d => d.date)))
            .attr("y1", yScale(trade.price))
            .attr("y2", yScale(trade.price))
            .attr("stroke", tradeColor)
            .attr("stroke-dasharray", "2px 4px")
    }

    if(drawTrades){
        trades.forEach(tradeLine);
    }

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

    // Draw label on mouseover
    const focus = bounds.append('g')
        .attr('class', 'focus')
        .style('display', 'none')

    focus.append("circle")
            .attr("r", 5);

    focus.append("rect")
        .attr("class", "tooltip")
        .attr("width", 100)
        .attr("height", 50)
        .attr("x", -30)
        .attr("y", 22)
        .attr("rx", 4)
        .attr("ry", 4);

    focus.append("text")
        .attr("class", "tooltip-date")
        .attr('fill', 'white')
        .attr("x", -18)
        .attr("y", 40);

    focus.append("text")
        .attr('fill', 'white')
        .attr("x", -18)
        .attr("y", 60)
        .text("Close: ");

    focus.append("text")
        .attr("class", "tooltip-close")
        .attr('fill', 'white')
        .attr("x", 27)
        .attr("y", 60);

    bounds.append('rect')
        .attr('class', 'overlay')
        .attr('width', dimensions.width)
        .attr('height', dimensions.height)
        .on("mouseover", function() { focus.style("display", null); })
        .on("mouseout", function() { focus.style("display", "none"); })
        .on("mousemove", mousemove);

    function mousemove() {
        var x0 = xScale.invert(d3.mouse(this)[0]),
            i = bisectDate(data, x0, 1),
            d0 = data[i - 1],
            d1 = data[i],
            d = x0 - d0.date > d1.date - x0 ? d1 : d0;
        focus.attr("transform", "translate(" + xScale(d.date) + "," + yScale(d.close) + ")");
        focus.select(".tooltip-date").text(formatDate(d.date));
        focus.select(".tooltip-close").text(formatValue(d.close));
    }
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

function monthDiff(d1, d2) {
    var months;
    months = (d2.getFullYear() - d1.getFullYear()) * 12;
    months -= d1.getMonth() + 1;
    months += d2.getMonth();
    return months <= 0 ? 0 : months;
}

$(document).ready(function(){
    current_data = parseDate(price_data);
    console.log(current_data);
    trend = 'none'
    drawTrades = false
    drawChart(current_data, trend, false, drawTrades);

    $('#show_trend').click(function(){
        if($(this).hasClass('active')){
            trend = 'none';
            $(this).removeClass('active')
        }
        else{
            trend = 'true';
            $(this).addClass('active')
        }
        drawChart(current_data, trend, true, drawTrades)
    })
    $('#show_trades').click(function(){
        if($(this).hasClass('active')){
            drawTrades = false;
            $(this).removeClass('active')
        }
        else{
            drawTrades = true;
            $(this).addClass('active')
        }
        drawChart(current_data, trend, true, drawTrades)
    })
    $('#reset_chart').click(function(){
        $('#show_trend').removeClass('active')
        trend = 'none';
        $('#show_trades').removeClass('active');
        drawTrades = false;
        drawChart(current_data, trend, true, drawTrades);
    })


    $('.priceChart').click(function(){
        months = $(this).attr('id');
        $('.priceChart').removeClass('active');
        $('#timeIn').removeClass('active');
        $(this).addClass('active');
        current_data = filterData(price_data, parseInt(months))
        drawChart(current_data, trend, true, drawTrades)
    })
    $('#timeIn').click(function(){
        firstTrade = new Date(trades[0].date)
        months = monthDiff(firstTrade, new Date());
        $('.priceChart').removeClass('active');
        $(this).addClass('active');
        current_data = filterData(price_data, parseInt(months))
        drawChart(current_data, trend, true, drawTrades)
    })
    $('#openMenu').click(function(){
        setTimeout(function(){
            drawChart(current_data, trend, true, drawTrades);
        }, 50);
    })
    $('#closeMenu').click(function(){
        setTimeout(function(){
            drawChart(current_data, trend, true, drawTrades);
        }, 50);
    })

    $('#chart_settings').click(function(){
        $('.chart_setting').toggleClass('visible');
    })
})
