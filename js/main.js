// Set colors and grades for circle markers
var colors = chroma.scale('RdBu').mode('lch').colors(5);
var grades = [-80, -60, -40, -20, 0, 20, 40, 60, 80];

// Function to set size of circle markers
function getRadius(attribute) {
    var attribute = Math.abs(attribute);
    return (attribute >= 0 && attribute < 20) ? 8 :
           (attribute >= 20 && attribute < 40) ? 10 :
           (attribute >= 40 && attribute < 60) ? 12:
           (attribute >= 60 && attribute < 80) ? 14 :
           16;  // attribute >= 80
}

// Function to set color of circle markers
function getColor(attribute) {
    return (attribute < 0) ? colors[1] : colors[colors.length - 2];
}

// Create legend
var legend_snowpack_changes = '<b class="legend-title">Change in April Snowpack (%), 1955-2020</b><br><br>' +
    '<div class="container">' +
        '<div class="row align-items-center mb-1"><div class="col-3 text-center d-flex justify-content-center"><i class="fa-border-prop-radius" style="background: ' + getColor(grades[8]) + '; opacity: 1; width: ' + getRadius(grades[8]) * 2 + 'px; height: ' + getRadius(grades[8]) * 2 + 'px; border-radius: 50%;"></i></div><div class="col-4 text-right label-left"><p>' + grades[8] + '</p></div><div class="col-2 text-center"><p>or</p></div><div class="col-3 text-left label-right"><p>higher</p></div></div>' +
        '<div class="row align-items-center mb-1"><div class="col-3 text-center d-flex justify-content-center"><i class="fa-border-prop-radius" style="background: ' + getColor(grades[8]) + '; opacity: 1; width: ' + getRadius(grades[7]) * 2 + 'px; height: ' + getRadius(grades[7]) * 2 + 'px; border-radius: 50%;"></i></div><div class="col-4 text-right label-left"><p>' + grades[7] + '</p></div><div class="col-2 text-center"><p>to</p></div><div class="col-3 text-right label-right-number"><p>' + grades[8] + '</p></div><div class="col-2"></div></div>' +
        '<div class="row align-items-center mb-1"><div class="col-3 text-center d-flex justify-content-center"><i class="fa-border-prop-radius" style="background: ' + getColor(grades[8]) + '; opacity: 1; width: ' + getRadius(grades[6]) * 2 + 'px; height: ' + getRadius(grades[6]) * 2 + 'px; border-radius: 50%;"></i></div><div class="col-4 text-right label-left"><p>' + grades[6] + '</p></div><div class="col-2 text-center"><p>to</p></div><div class="col-3 text-right label-right-number"><p>' + grades[7] + '</p></div><div class="col-2"></div></div>' +
        '<div class="row align-items-center mb-1"><div class="col-3 text-center d-flex justify-content-center"><i class="fa-border-prop-radius" style="background: ' + getColor(grades[8]) + '; opacity: 1; width: ' + getRadius(grades[5]) * 2 + 'px; height: ' + getRadius(grades[5]) * 2 + 'px; border-radius: 50%;"></i></div><div class="col-4 text-right label-left"><p>' + grades[5] + '</p></div><div class="col-2 text-center"><p>to</p></div><div class="col-3 text-right label-right-number"><p>' + grades[6] + '</p></div><div class="col-2"></div></div>' +
        '<div class="row align-items-center mb-1"><div class="col-3 text-center d-flex justify-content-center"><i class="fa-border-prop-radius" style="background: ' + getColor(grades[8]) + '; opacity: 1; width: ' + getRadius(grades[4]) * 2 + 'px; height: ' + getRadius(grades[4]) * 2 + 'px; border-radius: 50%;"></i></div><div class="col-4 text-right label-left"><p>' + grades[4] + '</p></div><div class="col-2 text-center"><p>to</p></div><div class="col-3 text-right label-right-number"><p>' + grades[5] + '</p></div><div class="col-2"></div></div>' +
        '<div class="row align-items-center mb-1"><div class="col-3 text-center d-flex justify-content-center"><i class="fa-border-prop-radius" style="background: ' + getColor(grades[0]) + '; opacity: 1; width: ' + getRadius(grades[4]) * 2 + 'px; height: ' + getRadius(grades[4]) * 2 + 'px; border-radius: 50%;"></i></div><div class="col-4 text-right label-left"><p>' + grades[4] + '</p></div><div class="col-2 text-center"><p>to</p></div><div class="col-3 text-right label-right-number"><p>' + grades[3] + '</p></div><div class="col-2"></div></div>' +
        '<div class="row align-items-center mb-1"><div class="col-3 text-center d-flex justify-content-center"><i class="fa-border-prop-radius" style="background: ' + getColor(grades[0]) + '; opacity: 1; width: ' + getRadius(grades[3]) * 2 + 'px; height: ' + getRadius(grades[3]) * 2 + 'px; border-radius: 50%;"></i></div><div class="col-4 text-right label-left"><p>' + grades[3] + '</p></div><div class="col-2 text-center"><p>to</p></div><div class="col-3 text-right label-right-number"><p>' + grades[2] + '</p></div><div class="col-2"></div></div>' +
        '<div class="row align-items-center mb-1"><div class="col-3 text-center d-flex justify-content-center"><i class="fa-border-prop-radius" style="background: ' + getColor(grades[0]) + '; opacity: 1; width: ' + getRadius(grades[2]) * 2 + 'px; height: ' + getRadius(grades[2]) * 2 + 'px; border-radius: 50%;"></i></div><div class="col-4 text-right label-left"><p>' + grades[2] + '</p></div><div class="col-2 text-center"><p>to</p></div><div class="col-3 text-right label-right-number"><p>' + grades[1] + '</p></div><div class="col-2"></div></div>' +
        '<div class="row align-items-center mb-1"><div class="col-3 text-center d-flex justify-content-center"><i class="fa-border-prop-radius" style="background: ' + getColor(grades[0]) + '; opacity: 1; width: ' + getRadius(grades[1]) * 2 + 'px; height: ' + getRadius(grades[1]) * 2 + 'px; border-radius: 50%;"></i></div><div class="col-4 text-right label-left"><p>' + grades[1] + '</p></div><div class="col-2 text-center"><p>to</p></div><div class="col-3 text-right label-right-number"><p>' + grades[0] + '</p></div><div class="col-2"></div></div>' +
        '<div class="row align-items-center mb-1"><div class="col-3 text-center d-flex justify-content-center"><i class="fa-border-prop-radius" style="background: ' + getColor(grades[0]) + '; opacity: 1; width: ' + getRadius(grades[0]) * 2 + 'px; height: ' + getRadius(grades[0]) * 2 + 'px; border-radius: 50%;"></i></div><div class="col-4 text-right label-left"><p>' + grades[0] + '</p></div><div class="col-2 text-center"><p>or</p></div><div class="col-3 text-left label-right"><p>lower</p></div></div>' +
    '</div>' +
    '<br>' +
    '<small class="reference">Data: <a href="https://www.epa.gov/climate-indicators/climate-change-indicators-snowpack" target="_blank">Environmental Protection Agency</a></small>';

var legend_ski_areas = '<i class="fa-solid fa-person-skiing" style="color: #000000; background: #ffffff; opacity: 1;"></i><b class="legend-title">: Ski Areas</b><br><hr>';

// Icon options
var iconOptions_skiing = {
    iconUrl: 'img/skiing_transparent.png',
    iconSize: [10, 10]
}
// Creating a custom icon
var customIcon_skiing = L.icon(iconOptions_skiing);

// Creating Marker Options
var markerOptions_skiing = {
    clickable: false,
    draggable: false,
    icon: customIcon_skiing,
    opacity: 0.5
}

var legend_study_areas = '<i class="fa-solid fa-mountain" style="color: #000000; background: #ffffff; opacity: 1;"></i><b class="legend-title">: Study Areas</b><br><hr>';

// Icon options
var iconOptions_mountain = {
    iconUrl: 'img/mountain_transparent.png',
    iconSize: [50, 50]
}
// Creating a custom icon
var customIcon_mountain = L.icon(iconOptions_mountain);

// Creating Marker Options
var markerOptions_mountain = {
    clickable: false,
    draggable: false,
    icon: customIcon_mountain,
    opacity: 1
}


var layers = {
    basemap_light: {
        layer: L.tileLayer('https://api.mapbox.com/styles/v1/katzbr/clgo7dq31002001rh2y4lfrlj/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1Ijoia2F0emJyIiwiYSI6ImNqOHhmMnBucDIwZm4ycW8ya2d5cHF0cmsifQ.8rcjz0DyWs_ncWfOZ0VwKA', {
            attribution: 'Created by <a href="https://github.com/ochoacas/">Cassidy Ochoa</a> & <a href="https://github.com/briangkatz/">Brian G. Katz</a> | <a href="assets/license.txt">Mapbox</a>',
            detectRetina: true
        })
    },
    basemap_light2: {
        layer: L.tileLayer('https://api.mapbox.com/styles/v1/katzbr/clgo7dq31002001rh2y4lfrlj/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1Ijoia2F0emJyIiwiYSI6ImNqOHhmMnBucDIwZm4ycW8ya2d5cHF0cmsifQ.8rcjz0DyWs_ncWfOZ0VwKA', {
            attribution: 'Created by <a href="https://github.com/ochoacas/">Cassidy Ochoa</a> & <a href="https://github.com/briangkatz/">Brian G. Katz</a> | <a href="assets/license.txt">Mapbox</a>',
            detectRetina: true
        })
    },
    snowpack_changes: {
        layer: L.geoJson.ajax('assets/snowpack_changes_1955-2022.geojson', {
            pointToLayer: function (feature, latlng) {
                return L.circleMarker(latlng, {
                    radius: getRadius(feature.properties["Trend (%)"]),
                    fillColor: getColor(feature.properties["Trend (%)"]),
                    stroke: false,
                    fillOpacity: 0.67
                })
            },
            onEachFeature: function (feature, layer) {
                layer.bindTooltip((feature.properties["Trend (%)"].toFixed(0) <= 0 ? "" : "+") + feature.properties["Trend (%)"].toFixed(0).toString() + '%', {sticky: true, className: "feature-tooltip"});
            }
        }),
        legend: legend_snowpack_changes
    },
    ski_areas: {  // source: https://www.nohrsc.noaa.gov/gisdatasets/
        layer: L.geoJson.ajax('assets/ski_areas_all.geojson', {  // change to ski_resorts.geojson
            pointToLayer: function (feature, latlng) {
                return L.marker([latlng.lat, latlng.lng], markerOptions_skiing);
            },
            onEachFeature: function (feature, layer) {
                layer.bindTooltip(feature.properties.NAME, {sticky: true, className: "feature-tooltip"});
            }
        }),
        legend: legend_ski_areas
    },
    study_areas: {  // source: https://www.nohrsc.noaa.gov/gisdatasets/ -- SELECTED OUT BACHELOR & ASPEN
        layer: L.geoJson.ajax('assets/study_areas.geojson', {
            pointToLayer: function (feature, latlng) {
                return L.marker([latlng.lat, latlng.lng], markerOptions_mountain);
            },
            onEachFeature: function (feature, layer) {
                layer.bindTooltip(feature.properties.NAME, {sticky: true, className: "feature-tooltip"});
            }
        }),
        legend: legend_study_areas
    },
};

// Set story scene titles, locations, zoom levels, and layers
var scenes = {
    title: {lat: 42.5, lng: -100, zoom: 5, name: 'Title'},
    intro: {lat: 42.5, lng: -100, zoom: 5, name: 'Intro', layers: [layers.snowpack_changes, layers.basemap_light]},
    skiing: {lat: 42.5, lng: -100, zoom: 5, name: 'Ski Areas', layers: [layers.ski_areas, layers.snowpack_changes, layers.basemap_light]},
    sites: {lat: 42.5, lng: -100, zoom: 5, name: 'Study Areas', layers: [layers.study_areas, layers.ski_areas, layers.snowpack_changes, layers.basemap_light]},
    counties: {lat: 42.5, lng: -100, zoom: 5, name: 'Counties', layers: [layers.basemap_light]},
    bachelor: {lat: 43.99528, lng: -121.68028, zoom: 13, name: 'Bachelor', layers: [layers.basemap_light]},
    aspen: {lat: 39.17611, lng: -106.82861, zoom: 13, name: 'Aspen', layers: [layers.basemap_light]},
    forecast: {lat: 42.5, lng: -100, zoom: 5, name: 'Forecast', layers: [layers.basemap_light]},
    comparison: {lat: 42.5, lng: -100, zoom: 5, name: 'Comparison', layers: [layers.basemap_light]},
    end: {lat: 42.5, lng: -100, zoom: 5, name: 'End'}
};

// Initalize the story map with options for the main map container
$('#storymap').storymap({
    scenes: scenes,
    baselayer: layers.basemap_light,
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
            zoomControl: true,
            scrollWheelZoom: false,
            fadeAnimation: true,
            zoomAnimation: true,
        }).setView([39.4997222185, -113.5024305610014], 4);

        return map;
    }
});

// Leaflet Time Dimension
var startDate = new Date('2100-01-01');

// Set bounds for time series map
var southWest = L.latLng(28.99874999922195, -125.00069444477808);  // these values were obtained from the metadata: https://geoserver.hydroshare.org/geoserver/HS-96cba44cd74843639f855d7c9e22024b/wms?request=GetCapabilities
var northEast = L.latLng(50.00069443777805, -101.99791667422191);
var bounds = L.latLngBounds(southWest, northEast);

var time_series_map = L.map('time-series-map', {
    minZoom: 4,
    maxZoom: 10,
    maxBounds: bounds,
    fullscreenControl: true,
    zoomControl: true,
    timeDimensionControl: true,
    timeDimensionControlOptions: {
//        autoPlay: true,  // starts the animation automatically
        loopButton: true,
        timeSteps: 1,
        position: 'bottomleft',
        playerOptions: {
            buffer: 0,
            transitionTime: 250,
            loop: true,
            startOver: true
        }
    },
    timeDimension: true,
    timeDimensionOptions: {
        period: "P1MT0H",  // monthly frequency
        timeInterval: startDate.toISOString() + "/P11MT0H"  // monthly frequency
    }
}).setView([39.4997222185, -113.5024305610014], 4);;

layers.basemap_light2.layer.addTo(time_series_map);  // have to add a separate copy of base map layer to side panel map

var sweLayer = L.tileLayer('assets/swe/{d}{h}/{z}/{x}/{y}.png', {
    attribution: 'Lute, A. C., J. Abatzoglou, T. Link (2022). SnowClim: Future Snow Data, <a href="https://doi.org/10.4211/hs.96cba44cd74843639f855d7c9e22024b">HydroShare</a>',
    tms: false,
    bounds: bounds,
    minZoom: 4,
    maxZoom: 10,
    opacity: 0.65
});
var sweTimeLayer = L.timeDimension.layer.tileLayer.custom(sweLayer, {})
    .addTo(time_series_map);
