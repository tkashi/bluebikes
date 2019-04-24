(function() {
    
    const DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    const MARGIN = {top: 20, right: 20, bottom: 70, left: 50};

    const countByDay = (countOfDays, countOfDate) => {
        day = new Date(countOfDate.start_date).getDay();
        countOfDays[day] += countOfDate.count;
        return countOfDays;
    }


    const showTripSummary = $root => {
        $root.append('<svg id="myChart"></svg>')

        $.ajax('../apis/trips/summary', {
            data: {
                group_by: 'start_date',
                aggregate: 'count'
            }
        }).done(resp => {
            data = resp.reduce(countByDay, [0, 0, 0, 0, 0, 0, 0]);

                    
            const width = $root.width() - MARGIN.left - MARGIN.right;
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
    };

    function projectPoint(x, y) {
        const point = map.latLngToLayerPoint(new L.LatLng(y, x));
        this.stream.point(point.x, point.y);
      }

    const showStationsMap = $root => {
        const INITIAL_ZOOM_LEVEL = 13

        const $map = $('<p id="map"></p>')
        $map.width($root.width())
        $root.append($map);
        
        const map = new L.Map($map[0], {center: [42.36, -71.05], zoom: INITIAL_ZOOM_LEVEL}).addLayer(new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'));
        L.svg().addTo(map);	
        
        const svg = d3.select('#map').select('svg');
        const g = svg.append('g').attr('class', 'leaflet-zoom-hide');

        $.ajax('../apis/stations', {
            data: {
                limit: 300,
                fields: 'lat,lon,station_id,capacity'
            }
        }).done(resp => {

            const results = resp['results'];
            results.forEach(function(d){
                d.LatLngObj = new L.LatLng(d.lat, d.lon);
            });

            const circles = g.selectAll("circle")
                .data(results)
                .enter()
                .append("circle").attr({
                    "stroke": "black",
                    "stroke-width": 1,
                    "opacity": .7,
                    "fill": "red"
                }); 
            
            function update() {
                circles.attr('transform', d => {
                    const point = map.latLngToLayerPoint(d.LatLngObj)
                    return `translate(${point.x}, ${point.y})`
                });
                zoom = map.getZoom();
                circles.attr('r', d => {
                    return d.capacity / 20 * 3 * (zoom / INITIAL_ZOOM_LEVEL) ** 2
                });
            } 
    
            map.on('moveend', update);
     
            update();
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