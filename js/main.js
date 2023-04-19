var colorsWatershed = chroma.scale('Oranges').mode('lab').colors(5);

function setColorWatershed(delta_arag) {
    var id = 0;
    if (delta_arag <= -0.2587) { id = 4; }
    else if (-0.2587 < delta_arag && delta_arag <= -0.2329) { id = 3; }
    else if (-0.2329 < delta_arag && delta_arag <= -0.2228) { id = 2; }
    else if (-0.2228 < delta_arag && delta_arag <= -0.2081) { id = 1; }
    else  { id = 0; }  // -0.2081 < delta_arag && delta_arag <= -0.1851
    return colorsWatershed[id];
}

function styleWatershed(feature) {
    return {
        fillColor: setColorWatershed(feature.properties.delta_mean_arag_t1t2.toFixed(4)),
        fillOpacity: 0.6,
        weight: 1,
        opacity: 1,
        color: '#000000',
        dashArray: '2, 2',
        dashOffset: '2'
    };
}

var colorsVuln = chroma.scale('Oranges').mode('lab').colors(4);

function setColorVuln(vuln) {
    var id = 0;
    if (vuln === 4) { id = 3; }  // High (H/L)
    else if (vuln === 3) { id = 2; }  // Medium (H/H)
    else if (vuln === 2) { id = 1; }  // Medium (L/L)
    else  { id = 0; }  // Low (L/H)
    return colorsVuln[id];
}

function styleVuln(feature) {
    return {
        fillColor: setColorVuln(feature.properties.cluster),
        fillOpacity: 0.6,
        weight: 1,
        opacity: 1,
        color: '#000000',
        dashArray: '2, 2',
        dashOffset: '2'
    };
}

var colorsSnowpack = chroma.scale('Oranges').mode('lab').colors(4);

function setColorSnowpack(trend) {
    var id = 0;
    if (trend === 4) { id = 3; }  // High (H/L)
    else if (trend === 3) { id = 2; }  // Medium (H/H)
    else if (trend === 2) { id = 1; }  // Medium (L/L)
    else  { id = 0; }  // Low (L/H)
    return colorsSnowpack[id];
}

function styleSnowpack(feature) {
    return {
        fillColor: setColorSnowpack(feature.properties["Trend (%)"]),
        fillOpacity: 0.6,
        weight: 1,
        opacity: 1,
        color: '#000000',
        dashArray: '2, 2',
        dashOffset: '2'
    };
}

function highlightFeatureWatershed(e) {
    var layer = e.target;
    layer.setStyle({
        weight: 2,
        opacity: 0.8,
        color: '#ffffff',
        fillOpacity: 0.95,
        dashArray: '1',
        dashOffset: '0'
    });
    $(layer).attr("id", "selected-watershed");
    layer.bringToFront();

    var arag_t1 = layer.feature.properties.mean_arag_t1;
    var arag_t2 = layer.feature.properties.mean_arag_t2;

    // Select the update class, and update the content with the input value.
    $(".updateWatershed").html('<h2>' + layer.feature.properties.NAME + '</h2>' + '<h2>&Delta;<sub>&Omega;<sub>ar</sub></sub> = ' + (layer.feature.properties.delta_mean_arag_t1t2).toFixed(4) + '</h2>');
    $(".infoWatershed").show();
    return arag_t1, arag_t2;
}

function resetHighlightWatershed(e) {
    layers.watersheds_pnw.layer.resetStyle(e.target);
    $(layers.watersheds_pnw.layer).attr("id", "");
    $(".infoWatershed").hide();
}

function onEachFeatureWatershed(feature, layer) {
    layer.on({
        mouseover: highlightFeatureWatershed,
        mouseout: resetHighlightWatershed
    });
}

function highlightFeatureVuln(e) {
    var layer = e.target;
    layer.setStyle({
        weight: 2,
        opacity: 0.8,
        color: '#ffffff',
        fillOpacity: 0.95,
        dashArray: '1',
        dashOffset: '0'
    });
    layer.bringToFront();
    // Select the update class, and update the content with the input value.
    $(".update").html('<h2><b>' + layer.feature.properties.name + '</b></h2><p>Exposure: ' + layer.feature.properties.exposure + ' </p>' + '<p>Sensitivity: ' + layer.feature.properties.sensitivty + ' </p>' + '<p>Adaptive Capacity: ' + layer.feature.properties.adptvcapac + '</p>');
    $(".info").show();
}

function resetHighlightFeatureVuln(e) {
    layers.vulnerability_watersheds.layer.resetStyle(e.target);
    $(".info").hide();
}

function onEachFeatureVuln(feature, layer) {
    layer.on({
        mouseover: highlightFeatureVuln,
        mouseout: resetHighlightFeatureVuln
    });
}

var legend_stakeholders = '<i class="fa-solid fa-person-skiing" style="background: #ffffff; opacity: 0.5;"></i><p>Stakeholders</p>';
var legend_vulnerability_watersheds = 'Vulnerability to OA*<br />' +
    '<i style="background: ' + colorsVuln[3] + '; opacity: 0.5;"></i><p>High (H/L)</p>' +
    '<i style="background: ' + colorsVuln[2] + '; opacity: 0.5"></i><p>Medium (H/H)</p>' +
    '<i style="background: ' + colorsVuln[1] + '; opacity: 0.5"></i><p>Medium (L/L)</p>' +
    '<i style="background: ' + colorsVuln[0] + '; opacity: 0.5"></i><p>Low (L/H)</p>' +
    '<b class="disclaimer">*Vulnerability estimated by High/Low exposure & sensitivity and High/Low adaptive capacity</b><br />' +
    '<div class="info">\n' + '<div class="update"><h2>Coastal watersheds of the Pacific Northwest, clustered by differential vulnerability of shellfisheries to ocean acidification</h2></div>\n' + '</div>';
var legend_watersheds_pnw = '<b>Rate of change in 30-year mean aragonite saturation state, 1995-2025 vs. 2020-2050 (&Delta;<sub>&Omega;<sub>ar</sub></sub>)</b><br><br>' +
    '<i style="background: ' + colorsWatershed[4] + '; opacity: 0.5;"></i><p><= -0.2587</p>' +
    '<i style="background: ' + colorsWatershed[3] + '; opacity: 0.5;"></i><p><= -0.2329</p>' +
    '<i style="background: ' + colorsWatershed[2] + '; opacity: 0.5"></i><p><= -0.2228</p>' +
    '<i style="background: ' + colorsWatershed[1] + '; opacity: 0.5"></i><p><= -0.2081</p>' +
    '<i style="background: ' + colorsWatershed[0] + '; opacity: 0.5"></i><p><= -0.1851</p>' +
    '<br><b class="disclaimer">Worsening ocean acidification is projected as a long-term decline in aragonite saturation state</b>' +
    '<div class="infoWatershed"><div class="updateWatershed"></div></div>';

var layers = {
    satellite: {
        layer: L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1Ijoia2F0emJyIiwiYSI6ImNqOHhmMnBucDIwZm4ycW8ya2d5cHF0cmsifQ.8rcjz0DyWs_ncWfOZ0VwKA', {
            id: 'mapbox.satellite'
        })
    },
    watersheds_pnw: {
        layer: L.geoJson.ajax("assets/watersheds_pnw.geojson", {
            style: styleWatershed,
            onEachFeature: onEachFeatureWatershed
        }),
        legend: legend_watersheds_pnw
    },
    stakeholders: {
        layer: L.geoJson.ajax('assets/stakeholders.geojson', {
            pointToLayer: function (feature, latlng) {
                var id = 0;
                var ico = "fa-solid fa-person-skiing";
//                if (feature.properties.type === "HATCHERY") { id = 0; ico = "fa-solid fa-person-skiing"; }
//                else if (feature.properties.type === "GROWER") { id = 1; ico = "fa-solid fa-person-skiing"; }
//                else if (feature.properties.type === "TRIBE") { id = 2; ico = "fa-solid fa-person-skiing"; }
//                else if (feature.properties.type === "PROCESSOR") { id = 3; ico = "fa-solid fa-person-skiing"; }
//                else if (feature.properties.type === "DISTRIBUTOR") { id = 4; ico = "fa-solid fa-person-skiing"; }
//                else { id = 5; ico = "fa-solid fa-person-skiing"} // "RETAILER"
                return L.marker(latlng, {icon: L.divIcon({className: ico + " " + 'marker-color-1'})});
            },
            onEachFeature: function (feature, layer) {
                layer.bindTooltip(feature.properties.name, {sticky: true, className: "feature-tooltip"});
            }
        }),
        legend: legend_stakeholders
    },
    vulnerability_watersheds: {
        layer: L.geoJson.ajax("assets/vulnerability_watersheds.geojson", {
            style: styleVuln,
            onEachFeature: onEachFeatureVuln
        }),
        legend: legend_vulnerability_watersheds
    },
    snowpack_changes: {
        layer: L.geoJson.ajax('assets/snowpack_changes_1955-2022.geojson', {
            pointToLayer: function (feature, latlng) {
                return L.circleMarker(latlng, {
                    radius: 40,
                    fillColor: "#2c8b19",
                    stroke: false,
                    fillOpacity: 0.25
                })
            },
            onEachFeature: function (feature, layer) {
                layer.bindTooltip(feature.properties["Trend (%)"].toFixed(2).toString(), {sticky: true, className: "feature-tooltip"});
            }
        }),
        legend: legend_stakeholders
    }
};

var scenes = {
    title: {lat: 44.75, lng: -123.75, zoom: 7, name: 'Title'},
    intro: {lat: 44.75, lng: -123.75, zoom: 7, name: 'Intro', layers: [layers.snowpack_changes, layers.satellite]},
    exposure: {lat: 44.75, lng: -123.75, zoom: 7, name: 'Exposure', layers: [layers.watersheds_pnw, layers.satellite]},
    sensitivity: {lat: 44.75, lng: -123.75, zoom: 7, name: 'Sensitivity', layers: [layers.stakeholders, layers.satellite]},
    adaptive_capacity: {lat: 44.75, lng: -123.75, zoom: 7, name: 'Adaptive Capacity', layers: [layers.satellite]},
    combined: {lat: 44.75, lng: -123.75, zoom: 7, name: 'Combined', layers: [layers.vulnerability_watersheds, layers.satellite]},
    end: {lat: 44.75, lng: -123.75, zoom: 7, name: 'End'}
};

$('#storymap').storymap({
    scenes: scenes,
    baselayer: layers.satellite,
    navbar: true,
    legend: true,
    credits: "",
    loader: true,
    scalebar: true,
    flyto: true,
    navwidget: true,
    createMap: function () {
        // Create a map in the "map" div, set the view to a given place and zoom
        var map = L.map($(".storymap-map")[0], {
            zoomControl: false,
            scrollWheelZoom: false,
            fadeAnimation: true,
            zoomAnimation: true
        }).setView([44.75, -123.75], 7);

        return map;
    }
});

// Create Leaflet map object, set map center and zoom level
var side_by_side_map = L.map('side-by-side-map', {
    minZoom: 5,
    maxZoom: 6,
    zoomControl: true,
    scrollWheelZoom: false
}).setView([42, -124], 5);

L.control.scale({
    position: "bottomleft",
    metric: false
}).addTo(side_by_side_map);

var t1 = L.tileLayer('assets/avg_arag_1995-2025/{z}/{x}/{y}.png', {
  minZoom: 5,
  maxZoom: 6,
  tms: false,
  attribution: 'OA Model: <a href="https://www.biogeosciences.net/10/193/2013/bg-10-193-2013.html" target="_blank" style="color:#000000;text-decoration:none;">Hauri et al., 2013</a>'
}).addTo(side_by_side_map);

var t2 = L.tileLayer('assets/avg_arag_2020-2050/{z}/{x}/{y}.png', {
  minZoom: 5,
  maxZoom: 6,
  tms: false,
  attribution: 'OA Model: <a href="https://www.biogeosciences.net/10/193/2013/bg-10-193-2013.html" target="_blank" style="color:#000000;text-decoration:none;">Hauri et al., 2013</a>'
}).addTo(side_by_side_map);

L.control.sideBySide(t1, t2).addTo(side_by_side_map);

layers.satellite.layer.addTo(side_by_side_map);

function setColorArag(mean_arag) {
    var id = 0;
    if (1.2511 <= mean_arag && mean_arag < 1.8936) { id = 4; }
    else if (1.8936 <= mean_arag && mean_arag < 2.1332) { id = 3; }
    else if (2.1332 <= mean_arag && mean_arag < 2.2867) { id = 2; }
    else if (2.2867 <= mean_arag && mean_arag < 2.4780) { id = 1; }
    else  { id = 0; }  // 2.4780 <= mean_arag && mean_arag < 2.9231
    return colorsWatershed[id];
}

var legend = L.control({position: 'bottomright'});
legend.onAdd = function (side_by_side_map) {

var div = L.DomUtil.create('div', 'info legend-custom');
div.innerHTML += '<b>OA climate change (30-year mean &Omega;<sub>ar</sub>), 1995-2025 (left) vs. 2020-2050 (right)</b><br>' +
    '<i style="background: ' + colorsWatershed[4] + '; opacity: 0.5;"></i><p>1.25 <= &Omega; < 1.89</p>' +
    '<i style="background: ' + colorsWatershed[3] + '; opacity: 0.5;"></i><p>1.89 <= &Omega; < 2.13</p>' +
    '<i style="background: ' + colorsWatershed[2] + '; opacity: 0.5"></i><p>2.13 <= &Omega; < 2.29</p>' +
    '<i style="background: ' + colorsWatershed[1] + '; opacity: 0.5"></i><p>2.29 <= &Omega; < 2.48</p>' +
    '<i style="background: ' + colorsWatershed[0] + '; opacity: 0.5"></i><p>2.48 <= &Omega; < 2.92</p>' +
    '<small><a href="https://www.biogeosciences.net/10/193/2013/bg-10-193-2013.html" target="_blank">Data: Hauri et al., 2013</a></small>'
return div;
};
legend.addTo(side_by_side_map);

// Set SVG width, height based on viewing window size
function setWidth(window) {
    var width = $(window).width() * 0.215;  // large
    if ($(window).width() < 1920 && $(window).width() > 1024) { width = $(window).width() * 0.3; }  // medium
    else if ($(window).width() <= 1024) { width = $('.storymap-story').width() - 40; }  // small
    else if ($(window).width() <= 768) { width = $('.storymap-story').width() - 40; }  // x-small
    return width;
}
function setHeight(window) {
    var height = $(window).height() * 0.195;  // large
    if ($(window).height() < 1280 && $(window).height() > 857) { height = $(window).height() * 0.225; }  // medium
    else if ($(window).height() <= 857) { height = $(window).height() * 0.33; }  // small
    else if ($(window).height() >= 2000) { height = $(window).height() * 0.225; }  // x-large
    return height;
}

// Species Responses
d3.csv("assets/species.csv").then(d => chart(d))

function chart(data) {

    var keys = data.columns.slice(1);

    var parseTime = d3.timeParse("%Y%m%d"),
        formatDate = d3.timeFormat("%Y-%m-%d"),
        bisectDate = d3.bisector(d => d.omega_arag).left,
        formatValue = d3.format(",.1f"),
        formatFloat = d3.format(".2f");

    data.forEach(function(d) {
        d.date = parseTime(d.date);
        d.omega_arag = formatFloat(d.omega_arag);
        return d;
    })

    var width = setWidth(window);
    var height = setHeight(window);

    var svg = d3.select("#species-response-chart")
        .attr("width", width)
        .attr("height", height),
        margin = {
            top: 15,
            right: 10,
            bottom: 15,
            left: 40
        },
        width = +svg.attr("width"),
        height = +svg.attr("height") - margin.top - margin.bottom;

    var x = d3.scaleLinear()
        .rangeRound([margin.left, width - margin.right])
        .domain(d3.extent(data, d => formatFloat(d.omega_arag)))
        .range([width - margin.right, margin.left]);

    var y = d3.scaleLinear()
        .rangeRound([height - margin.bottom, margin.top]);

    var z = d3.scaleOrdinal(d3.schemePaired);

    var line = d3.line()
        .curve(d3.curveBasis)
        .x(d => x(formatFloat(d.omega_arag)))
        .y(d => y(formatFloat(d.response)));

    svg.append("g")
        .attr("class","x-axis")
        .attr("transform", "translate(0," + (height - margin.bottom) + ")")
        .call(d3.axisBottom(x).tickFormat(d3.format(".1f")));

    svg.append("text")
      .attr("transform",
            "translate(" + (width/2) + " ," +
                           (height + margin.top + 10) + ")")
      .style("text-anchor", "middle")
      .text("Aragonite saturation state");

    svg.append("g")
        .attr("class", "y-axis")
        .attr("transform", "translate(" + margin.left + ",0)");

    svg.append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", -2)
          .attr("x", 0 - (height / 2))
          .attr("dy", "1em")
          .style("text-anchor", "middle")
          .text("Growth (% change from pre-industrial)");

    var mean_arag = svg.append("g")
        .attr("class", "focusMean")
        .style("display", "block");
    mean_arag.append("line").attr("class", "lineHoverMean")
        .style("stroke", "#999")
        .attr("stroke-width", 3)
        .style("shape-rendering", "crispEdges")
        .style("opacity", 0.5)
        .attr("y1", -height)
        .attr("y2",0);

    var mean_arag2 = svg.append("g")
        .attr("class", "focusMean")
        .style("display", "block");
    mean_arag2.append("line").attr("class", "lineHoverMean")
        .style("stroke", "#999")
        .attr("stroke-width", 3)
        .style("shape-rendering", "crispEdges")
        .style("opacity", 0.5)
        .attr("y1", -height)
        .attr("y2",0);

    var focus = svg.append("g")
        .attr("class", "focus")
        .style("display", "none");
    focus.append("line").attr("class", "lineHover")
        .style("stroke", "#000")
        .attr("stroke-width", 3)
        .style("shape-rendering", "crispEdges")
        .style("opacity", 0.5)
        .attr("y1", -height)
        .attr("y2",0);
    focus.append("text").attr("class", "lineHoverArag")
        .attr("text-anchor", "middle")
        .attr("font-size", 12)
        .attr("font-color", "rgb(255,255,255,1)");

    var overlay = svg.append("rect")
        .attr("class", "overlay")
        .attr("x", margin.left)
        .attr("width", width - margin.right - margin.left)
        .attr("height", height);

    // Hover over a watershed to have the species chart updated by its 30-year mean omega_arag
    $(layers.watersheds_pnw.layer).mouseover(function(feature, layer) {
        feature = feature.originalEvent.layer.feature;
        mean_arag.selectAll(".lineHoverMean")
            .attr("transform", "translate(" + x(feature.properties.mean_arag_t1) + "," + height + ")");
        mean_arag.selectAll(".lineHoverArag")
            .attr("transform",
                "translate(" + x(feature.properties.mean_arag_t1) + "," + (height + margin.bottom) + ")");
        console.log("Aragonite saturation state (30-year mean) T1: " + feature.properties.mean_arag_t1);
        mean_arag2.selectAll(".lineHoverMean")
            .attr("transform", "translate(" + x(feature.properties.mean_arag_t2) + "," + height + ")");
        mean_arag2.selectAll(".lineHoverArag")
            .attr("transform",
                "translate(" + x(feature.properties.mean_arag_t2) + "," + (height + margin.bottom) + ")");
        console.log("Aragonite saturation state (30-year mean) T2: " + feature.properties.mean_arag_t2);
    });

    update(d3.select('#selectbox').property('value'), 0);

    function update(input, speed) {

        var copy = keys.filter(f => f.includes(input))

        var species_all = copy.map(function(id) {
            return {
                id: id,
                values: data.map(d => {return {omega_arag: d.omega_arag, response: +d[id]}})
            };
        });

        y.domain([
            d3.min(species_all, d => d3.min(d.values, c => c.response)),
            d3.max(species_all, d => d3.max(d.values, c => c.response))
        ]).nice();

        svg.selectAll(".y-axis").transition()
            .duration(speed)
            .call(d3.axisLeft(y).tickSize(-width + margin.right + margin.left))

        var species = svg.selectAll(".species_all")
            .data(species_all);

        species.exit().remove();

        species.enter().insert("g", ".focus").append("path")
            .attr("class", "line species_all")
            .style("stroke", d => z(d.id))
            .style("stroke-width", 3)
            .merge(species)
        .transition().duration(speed)
            .attr("d", d => line(d.values))

        tooltip(copy);
    }

    function tooltip(copy) {

        var labels = focus.selectAll(".lineHoverText")
            .data(copy)
        labels.enter().append("text")
            .attr("class", "lineHoverText")
            .style("fill", d => z(d))
            .attr("text-anchor", "middle")
            .attr("font-size", '1vw')
            .attr("dy", (_, i) => 1 + i * 2 + "em")
            .merge(labels);

        var circles = focus.selectAll(".hoverCircle")
            .data(copy)
        circles.enter().append("circle")
            .attr("class", "hoverCircle")
            .style("fill", d => z(d))
            .attr("r", 3)
            .merge(circles);

        // Have an overlay line appear and disappear over the species response curves on mouseover/mouseout
        svg.selectAll(".overlay")
            .on("mouseover", function() { focus.style("display", null); })
            .on("mouseout", function() { focus.style("display", "none"); })
            .on("mousemove", mousemove);

        // Function to display data values (y) respective to mouse hover location (x)
        function mousemove() {

            var x0 = x.invert(d3.mouse(this)[0]),
                i = bisectDate(data, x0, 0.1),
                d0 = data[i - 1],
                d1 = data[i],
                d = x0 - d0.omega_arag > d1.omega_arag - x0 ? d1 : d0;

            focus.select(".lineHover")
                .attr("transform", "translate(" + x(d.omega_arag) + "," + height + ")");
            focus.select(".lineHoverArag")
                .attr("transform",
                    "translate(" + x(d.omega_arag) + "," + (height + margin.bottom) + ")")
                .text(d.omega_arag);
            // Circles move along data values at the mouse hover event location, i.e. y(d[e])
            focus.selectAll(".hoverCircle")
                .attr("cy", e => y(d[e]))
                .attr("cx", x(d.omega_arag));
            focus.selectAll(".lineHoverText")
                .attr("transform",
                    "translate(" + (x(d.omega_arag)) + "," + height / 2.5 + ")")
                // Display data headings and values on overlay line
                .text(e => e.split("_")[1].split('-').join(' ') + ": " + formatValue(d[e]) + "%");

            x(d.omega_arag) > (width - width / 4)
                ? focus.selectAll("text.lineHoverText")
                    .attr("text-anchor", "end")
                    .attr("dx", -7.5)
                : focus.selectAll("text.lineHoverText")
                    .attr("text-anchor", "start")
                    .attr("dx", 7.5)
        }
    }
    var selectbox = d3.select("#selectbox")
        .on("change", function() {
            update(this.value, 500);
        })
};
