var hideLabel = function(label){ label.labelObject.style.opacity = 0;};
var showLabel = function(label){ label.labelObject.style.opacity = 1;};
var labelEngine = new labelgun.default(hideLabel, showLabel);

var labels = [];

// define color scale for point data markers
var colors = chroma.scale(['#A5BF15', '#C9F5F6']).mode('lch').colors(6);
// set color of markers based on .marker-color-#
for (i = 0; i < 6; i++) {
    $('head').append($("<style> .marker-color-" + (i + 1).toString() + " { color: " + colors[i] + "; font-size: 16px; text-shadow: 1px 1px 1px #000000; opacity: 0.5;} </style>"));
}
var colors2 = ['#2c7bb6', '#abd9e9', '#ffffbf', '#fdae61', '#d7191c'];
for (i = 0; i < 5; i++) {
    $('head').append($("<style> .marker-color2-" + (i + 1).toString() + " { color: " + colors2[i] + "; font-size: 16px; opacity: 0.5; text-shadow: 1px 1px 1px #000000;} </style>"));
}

function onEachFeature(feature, layer) {
    layer.bindTooltip(feature.properties.name, {sticky: true, className: "feature-tooltip"});
}

shellfish_network = null;

// Layer, Scene, and Story Map Management
var layers = {
    estuaries: {
        layer: L.geoJson.ajax('assets/estuaries.geojson', {
            color: 'gray',
            weight: 0,
            opacity: 0,
            fillOpacity: 0.001,
            onEachFeature: function (feature, layer) {
                layer.bindTooltip(feature.properties.nca_name, {sticky: true, className: "feature-tooltip"});
            }
        })
    },
    stakeholders: {
        layer: L.geoJson.ajax('assets/stakeholders.geojson', {
            pointToLayer: function (feature, latlng) {
                var id = 0;
                var ico = "users";
                if (feature.properties.type === "HATCHERY") { id = 0; ico = "fas fa-database"; }
                else if (feature.properties.type === "GROWER") { id = 1; ico = "fab fa-pagelines"; }
                else if (feature.properties.type === "TRIBE") { id = 2; ico = "fas fa-leaf"; }
                else if (feature.properties.type === "PROCESSOR") { id = 3; ico = "fas fa-industry"; }
                else if (feature.properties.type === "DISTRIBUTOR") { id = 4; ico = "fas fa-shipping-fast"; }
                else { id = 5; ico = "fas fa-exchange-alt"} // "RETAILER"
                return L.marker(latlng, {icon: L.divIcon({className: ico + " " + 'marker-color-1'})});
            },
            onEachFeature: function (feature, layer) {
                layer.bindTooltip(feature.properties.name, {sticky: true, className: "feature-tooltip"});
            }
        })
    },
    stakeholders2: {
        layer: L.geoJson.ajax('assets/stakeholders.geojson', {
            pointToLayer: function (feature, latlng) {
                return L.marker(latlng, {icon: L.divIcon({className: "fas fa-ban stakeholders-warning"})});
            }
        })
    },
    hatchery: {
        layer: L.geoJson.ajax('assets/hatchery.geojson', {
            pointToLayer: function (feature, latlng) {
                return L.marker(latlng, {icon: L.divIcon({
                    className: "fas fa-database fa-5x hatchery"})});
                },
            onEachFeature: function (feature, layer) {
                layer.bindTooltip(feature.properties.name, {sticky: true, className: "feature-tooltip"});
            }
        })
    },
    hatchery2: {
        layer: L.geoJson.ajax('assets/hatchery.geojson', {
            color: 'black',
            weight: 2,
            opacity: 0.3,
            pointToLayer: function (feature, latlng) {
                return L.marker(latlng, {icon: L.divIcon({
                    className: "fas fa-database fa-2x hatchery"})});  // changed from 5x to 2x size
            },
            onEachFeature: function (feature, layer) {
                layer.bindTooltip(feature.properties.name, {sticky: true, className: "feature-tooltip"});
            }
        })
    },
    hatchery3: {
        layer: L.geoJson.ajax('assets/hatchery.geojson', {
            color: 'black',
            weight: 2,
            opacity: 0.3,
            pointToLayer: function (feature, latlng) {
                return L.marker(latlng, {icon: L.divIcon({
                    className: "fas fa-exclamation-triangle fa-2x blinking hatchery-warning"})});
            },
            onEachFeature: function (feature, layer) {
                layer.bindTooltip(feature.properties.name, {sticky: true, className: "feature-tooltip"});
            }
        })
    },
    funded_projects: {
        layer: L.geoJson.ajax('assets/funded_projects.geojson', {
            style: function (feature, layer) {
                return {
                    weight: 10,
                    opacity: 0.5
                };
            },
            pointToLayer: function (feature, latlng) {
                var id = 0;
                if (feature.properties.funding_agency === "National Oceanic and Atmospheric Administration") { id = 0; }
                else if (feature.properties.funding_agency === "National Science Foundation") { id = 1; }
                else if (feature.properties.funding_agency === "Environmental Protection Agency") { id = 2; }
                else if (feature.properties.funding_agency === "Oregon State General Fund") { id = 3; }
                else { id = 4; } // "Bonneville Power Adminstration"
                return L.marker(latlng, {icon: L.divIcon({className: "fas fa-flask projects" + " " + 'marker-color2-' + (id + 1).toString() })});
            },
            onEachFeature: function (feature, layer) {
                layer.bindTooltip(feature.properties.asset, {sticky: true, className: "feature-tooltip"});
            }
        })
    },
    shellfish: {
        layer: L.tileLayer('https://api.mapbox.com/styles/v1/katzbr/cjshza9xf1db51fqgpriounjs/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1Ijoia2F0emJyIiwiYSI6ImNqOHhmMnBucDIwZm4ycW8ya2d5cHF0cmsifQ.8rcjz0DyWs_ncWfOZ0VwKA')
    }
};

var scenes = {
    title: {lat: 45, lng: -124, zoom: 7, name: 'Title'},
    whiskey: {lat: 45.408, lng: -123.950140, zoom: 13, name: 'Whiskey Creek', layers: [layers.hatchery, layers.estuaries, layers.shellfish]},
    network: {lat: 45, lng: -124, zoom: 7, name: 'Importance to Network', layers: [layers.hatchery2, layers.stakeholders, layers.shellfish]},
    seed: {lat: 45, lng: -124, zoom: 7, name: 'Oyster Seed Crisis', layers: [layers.hatchery3, layers.stakeholders2, layers.shellfish]},
    adaptation: {lat: 45, lng: -124, zoom: 7, name: 'Adaptive Capacity', layers: [layers.funded_projects, layers.shellfish]},
    success: {lat: 45.408, lng: -123.960140, zoom: 13, name: 'Successful Adaptation', layers: [layers.hatchery, layers.shellfish]},
    end: {lat: 45.408, lng: -123.960140, zoom: 13, name: 'Assessment'}
};


$('#storymap').storymap({
    scenes: scenes,
    baselayer: layers.shellfish,
    navbar: true,
    legend: true,
    credits: "",
    loader: true,
    scalebar: false,
    flyto: true,
    navwidget: true,
    createMap: function () {
        // Create a map in the "map" div, set the default view and zoom level
        var map = L.map($(".storymap-map")[0], {
            zoomControl: false,
            scrollWheelZoom: false,
            fadeAnimation: true,
            zoomAnimation: true
        }).setView([45.408, -123.950140], 13);

        return map;
    }
});

(function (i, s, o, g, r, a, m) {
    i['GoogleAnalyticsObject'] = r;
    i[r] = i[r] || function () {
        (i[r].q = i[r].q || []).push(arguments)
    }, i[r].l = 1 * new Date();
    a = s.createElement(o),
        m = s.getElementsByTagName(o)[0];
    a.async = 1;
    a.src = g;
    m.parentNode.insertBefore(a, m)
})(window, document, 'script', 'https://www.google-analytics.com/analytics.js', 'ga');

ga('create', 'UA-110256930-2', 'auto');
ga('send', 'pageview');
