async function drawBars() {

  // 1. Access data
  const dataset = days

  const metricAccessor = d => d.days
  const yAccessor = d => d.stock

  // 2. Create chart dimensions
  const width = $('#held-chart').width();
  const height = $('#held-chart').height();
  let dimensions = {
    width: width,
    height: height,
    margin: {
      top: 5,
      right: 20,
      bottom: 30,
      left: 50,
    },
  }
  dimensions.boundedWidth = dimensions.width
    - dimensions.margin.left
    - dimensions.margin.right
  dimensions.boundedHeight = dimensions.height
    - dimensions.margin.top
    - dimensions.margin.bottom

  // 3. Draw canvas

  const wrapper = d3.select("#held-chart")
    .append("svg")
      .attr("width", dimensions.width)
      .attr("height", dimensions.height)

  const bounds = wrapper.append("g")
      .style("transform", `translate(${
        dimensions.margin.left
      }px, ${
        dimensions.margin.top
      }px)`)

  // 4. Create scales

  const xScale = d3.scaleLinear()
    .domain(d3.extent(dataset, metricAccessor))
    .range([0, dimensions.boundedWidth])
    .nice()

  const yScale = d3.scaleBand()
    .domain(dataset.map(yAccessor))
    .range([0, dimensions.boundedHeight])
    .padding(0.3)
  // 5. Draw data
  const xAxisGenerator = d3.axisBottom()
    .scale(xScale)

  const xAxis = bounds.append("g")
    .call(xAxisGenerator)
    .style("transform", `translateY(${dimensions.boundedHeight}px)`)

  const yAxisGenerator = d3.axisLeft()
    .scale(yScale)

  const yAxis = bounds.append("g")
    .call(yAxisGenerator)  


  // Render the bars
  bounds.selectAll('bar')
    .data(dataset)
    .enter()
    .append('rect')
    .attr('y', d => yScale(yAccessor(d)))
    .attr('width', d => dimensions.boundedWidth - xScale(metricAccessor(d)))
    .attr('height', yScale.bandwidth())
    .attr("fill", d3.scaleOrdinal(chartColors))
    .append('text').text(d => yAccessor(d));
}
drawBars()
