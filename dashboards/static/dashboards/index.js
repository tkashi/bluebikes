$(function() {
    
    const DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    const MARGIN = {top: 20, right: 20, bottom: 70, left: 50};

    const countByDay = (countOfDays, countOfDate) => {
        day = new Date(countOfDate.start_date).getDay();
        countOfDays[day] += countOfDate.count;
        return countOfDays;
    }

    $.ajax('../apis/trips/summary', {
        data: {
            group_by: 'start_date',
            aggregate: 'count'
        }
    }).done(resp => {
        data = resp.reduce(countByDay, [0, 0, 0, 0, 0, 0, 0]);

        
        const width = $('main').width() - MARGIN.left - MARGIN.right;
        const height = 400 - MARGIN.top - MARGIN.bottom;

        const svg = d3.select("#myChart")
            .attr("width", width + MARGIN.left + MARGIN.right)
            .attr("height", height + MARGIN.top + MARGIN.bottom)
            .append("g")
            .attr("transform", "translate(" + MARGIN.left + "," + MARGIN.top + ")");
        
        const x = d3.scale.ordinal().rangeRoundBands([0, width], .05);
        const y = d3.scale.linear().range([height, 0]);

        x.domain(DAYS);
        y.domain([0, d3.max(data)]);

        const xAxis = d3.svg.axis().scale(x).orient("bottom");
        const yAxis = d3.svg.axis().scale(y).orient("left").ticks(10);

        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis)
            .selectAll("text")
            .style("text-anchor", "end")
            .attr("dx", "-.8em")
            .attr("transform", "rotate(-45)" );

        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)
            .append("text")
            .attr("y", -10)
            .style("text-anchor", "end")
            .text("# of trips");

        svg.selectAll("bar")
            .data(data)
            .enter().append("rect")
            .style("fill", "#2f9bf5")
            .attr("x", (d, idx) => { return x(DAYS[idx]); })
            .attr("width", x.rangeBand())
            .attr("y", d => { return y(d); })
            .attr("height", d => { return height - y(d); });
    });
});