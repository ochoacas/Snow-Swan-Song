var ecoregions_legend = '<i style="background: black; opacity: 0.5"></i><p><b>Ecoregions</b></p>';

function setColor(GROWER_CNT) {
    //Tenary operation: condition ? valueIfTrue : valueIfFalse
    // condition ? value1 : value2
    return GROWER_CNT > 60 ? '#a08060' :
        GROWER_CNT > 59 ? '#b89e85' :
            GROWER_CNT > 39 ? '#d0beac' :
                GROWER_CNT > 19 ? '#e8ded5' :
                    '#ffffff';
}

function style(feature) {
    return {
        fillColor: setColor(feature.properties.GROWER_CNT),
        fillOpacity: 0.5,
        weight: 2,
        opacity: 0.8,
        color: '#ffffff',
        dashArray: '4'
    };
}

var ecoregions_choropleth_legend = '<p><b># of Growers</b></p>' +
    '<i style="background: #ffffff; opacity: 0.5"></i><p><b>0</b></p>' +
    '<i style="background: #e8ded5; opacity: 0.5"></i><p><b>1 - 19</b></p>' +
    '<i style="background: #d0beac; opacity: 0.5"></i><p><b>20 - 39</b></p>' +
    '<i style="background: #b89e85; opacity: 0.5"></i><p><b>40 - 59</b></p>' +
    '<i style="background: #a08060; opacity: 0.5"></i><p><b>60+</b></p>';

$('html > head').append($("<style> .marker-icon { color: red; font-size: 15px; text-shadow: 0 0 3px #ffffff;} </style>"));

var colors = chroma.scale('Set2').mode('lch').colors(10);
for (i = 1; i < 11; i++) {
    $('html > head').append($("<style> .marker-icon-" + i.toString() + " { color: " + colors[i] + "; font-size: 15px; text-shadow: 0 0 3px #ffffff;} </style>"));
}


var collaboration_circle_legend = '<i class=""><svg height="16" width="16"> <circle cx="8" cy="8" r="6" stroke="white" stroke-width="1" fill="a0a0c0" fillOpacity="0.4" /> </svg></i><p><b>Research Partners</b></p>';

var layers = {
    ecoregions: {
        layer: L.geoJson.ajax('assets/upwelling_ecoregions.geojson', {
            color: 'black',
            weight: 2,
            opacity: 0.3,
            pointToLayer: function (feature, latlng) {
                // return L.circle(latlng, 1000 * Math.pow(Math.floor((Math.random() * 3) + 1), 2));
                return L.marker(latlng, {icon: L.divIcon({className: 'glyphicon glyphicon-one-fine-smaller-dot glow-effect'})});
            },
            onEachFeature: function (feature, layer) {
                layer.bindTooltip(feature.properties.ECOREGION, {sticky: true, className: "feature-tooltip"});
            }
        }),
        legend: ecoregions_legend
    },
    ecoregions_choropleth: {
        layer: L.geoJson.ajax('assets/upwelling_ecoregions.geojson', {
            style: style,
            onEachFeature: function (feature, layer) {
                layer.bindTooltip(feature.properties.GROWER_CNT, {
                    className: 'feature-label',
                    permanent: false,
                    direction: 'center',
                    sticky: true
                });
            }
        }),
        legend: ecoregions_choropleth_legend
    },
    collaboration_circle: {
        layer: L.geoJson.ajax('assets/collaboration.geojson', {
            style: function (feature) {
                return {
                    fillColor: chroma.random(),
                    fillOpacity: 0.4,
                    stroke: true,
                    weight: 10,
                    opacity: 0.8,
                    color: '#a0a0c0'
                };
            },
            pointToLayer: function (feature, latlng) {
                return L.circleMarker(latlng);
            },
            onEachFeature: function (feature, layer) {
                layer.bindTooltip(feature.properties.name, {sticky: true, className: "feature-tooltip"});
            }
        }),
        legend: collaboration_circle_legend
    },
    shellfish: {
        layer: L.tileLayer('https://api.mapbox.com/styles/v1/katzbr/cjshza9xf1db51fqgpriounjs/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1Ijoia2F0emJyIiwiYSI6ImNqOHhmMnBucDIwZm4ycW8ya2d5cHF0cmsifQ.8rcjz0DyWs_ncWfOZ0VwKA')
    }
};

var scenes = {
    title: {lat: 55, lng: -138, zoom: 4, name: 'Title'},
    importance: {lat: 47.05, lng: -124, zoom: 9, name: 'Societal importance of shellfish', layers: [layers.shellfish]},
    oa: {lat: 46, lng: -155.6, zoom: 5, name: 'Ocean acidification', layers: [layers.shellfish]},
    shellfish: {lat: 45.408, lng: -123.960140, zoom: 13, name: 'Impacts to shellfish', layers: [layers.shellfish]},
    future: {lat: 15, lng: -138, zoom: 2, name: 'Looking ahead', layers: [layers.shellfish]},
    collaboration: {lat: 47, lng: -125, zoom: 4, name: 'Collaboration', layers: [layers.collaboration_circle, layers.shellfish]},
    regional_assessment: {lat: 44.0000000, lng: -123.5000000, zoom: 7, name: 'Assessment'}
};

$('#storymap').storymap({
    scenes: scenes,
    baselayer: layers.shellfish,
    navbar: true,
    legend: false,
    credits: "",
    loader: true,
    scalebar: false,
    navwidget: true,
    createMap: function () {
        var map = L.map($(".storymap-map")[0], {
            zoomControl: false,
            scrollWheelZoom: false
        }).setView([55, -138], 4);

        return map;
    }
});