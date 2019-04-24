(function() {
    
    const DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    const MARGIN = {top: 20, right: 20, bottom: 70, left: 50};

    const countByDay = (countOfDays, countOfDate) => {
        day = new Date(countOfDate.start_date).getDay();
        countOfDays[day] += countOfDate.count;
        return countOfDays;
    }

    /**
     * Show trip summary. By default, it shows the histogram of the number of trips for each day.
     * 
     * @param {jQuery} $root content elements
     */
    const showTripSummary = $root => {
        $root.append('<svg id="myChart"></svg>')

        // get number of trips for each date
        $.ajax('../apis/trips/summary', {
            data: {
                group_by: 'start_date',
                aggregate: 'count'
            }
        }).done(resp => {
            // summarize by day
            data = resp.reduce(countByDay, [0, 0, 0, 0, 0, 0, 0]);

            const width = $root.width() - MARGIN.left - MARGIN.right;
            const height = 400 - MARGIN.top - MARGIN.bottom;
    
            // show bar chart
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
    
            // xAxis
            svg.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate(0," + height + ")")
                .call(xAxis)
                .selectAll("text")
                .style("text-anchor", "end")
                .attr("dx", "-.8em")
                .attr("transform", "rotate(-45)" );
    
            // yAxis
            svg.append("g")
                .attr("class", "y axis")
                .call(yAxis)
                .append("text")
                .attr("y", -10)
                .style("text-anchor", "end")
                .text("# of trips");
    
            // bars
            svg.selectAll("bar")
                .data(data)
                .enter().append("rect")
                .style("fill", "#2f9bf5")
                .attr("x", (d, idx) => { return x(DAYS[idx]); })
                .attr("width", x.rangeBand())
                .attr("y", d => { return y(d); })
                .attr("height", d => { return height - y(d); });
        });
    };


    /**
     * Show the stations on the map.
     * 
     * @param {jQuery} $root content element
     */
    function showStationsMap($root) {
        const INITIAL_ZOOM_LEVEL = 13

        // add map element to content
        const $map = $('<p id="map"></p>')
        $map.width($root.width())
        $root.append($map);
        
        const map = new L.Map($map[0], {
            center: [42.36, -71.05], 
            zoom: INITIAL_ZOOM_LEVEL
        }).addLayer(new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'));

        // add svg layer
        L.svg().addTo(map);	
        
        const svg = d3.select('#map').select('svg');
        const g = svg.append('g').attr('class', 'leaflet-zoom-hide');

        // get capacity and location information of all stations
        $.ajax('../apis/stations', {
            data: {
                limit: 300,
                fields: 'lat,lon,station_id,capacity'
            }
        }).done(resp => {

            const results = resp['results'];
            
            // add Location data object to original data
            results.forEach(function(d){
                d.LatLngObj = new L.LatLng(d.lat, d.lon);
            });

            // add circles
            const circles = g.selectAll("circle")
                .data(results)
                .enter()
                .append("circle").attr({
                    "stroke": "black",
                    "stroke-width": 1,
                    "opacity": .7,
                    "fill": "red"
                }); 
            
            // update every time the map is reset
            function update() {
                circles.attr('transform', d => {
                    const point = map.latLngToLayerPoint(d.LatLngObj)
                    return `translate(${point.x}, ${point.y})`
                });
                zoom = map.getZoom();
                circles.attr('r', d => {
                    return d.capacity / 20 * 3 * (zoom / INITIAL_ZOOM_LEVEL) ** 2 // change circle size depending on capacity and zoom level
                });
            } 
    
            map.on('moveend', update);
     
            update(); // first update
        });

    };


    $(function() {
        $content = $('#content');
        $mainTitle = $('main').find('h1.h2');
        $sideBar = $('.sidebar');

        function initMain(hash, func) {
            const $as = $sideBar.find('a.nav-link');
            $as.removeClass('active');
            const $a = $as.filter('[href="' + hash + '"]');
            $a.addClass('active');
            const title = $a.text().trim();
            $mainTitle.text(title);
            $content.empty();
            func($content)
        }

        const  hashChangeHandler = e => {
            switch (location.hash) {
                case '':
                case '#summary':
                    initMain('#summary', showTripSummary);
                    break;
                case '#stations':
                    initMain('#stations', showStationsMap);
                    break;
            }
        };

        hashChangeHandler();
        window.addEventListener('hashchange', hashChangeHandler);
    })
})();