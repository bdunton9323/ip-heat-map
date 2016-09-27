
// TODO: this has to be the URL of my server as seen externally
var BASE_API_URL = "http://192.168.1.8:8888";

// Other points of interest
// durham: [35.99, -78.8986]
// manhattan: [40.7831, -73.9712]
var mymap = L.map('mapid').setView([47.0207, 8.6530], 10);

L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v9/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiYmFkOTMyMyIsImEiOiJjaXRrc2cwazkwMDAyMm9wbmdmcjllOXcwIn0.X4q84qTqXZ7HKlpSiCWjVg', {
    attribution: '&copy; <a href="https://www.mapbox.com/map-feedback/">Mapbox</a> © <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> <strong><a href="https://www.mapbox.com/map-feedback/" target="_blank">Improve this map</a></strong>'
}).addTo(mymap);

var heatMap = {
    heat: null,
    points: [],
    opts: {radius: 30, blur: 30, maxZoom: 15},
    
    // Sets whether the IPv4 or IPv6 data should be displayed
    dataSource: "v6",
    
    initHeatLayer: function() {
        this.heat = L.heatLayer([], this.opts).addTo(mymap);
    },

    updateHeatLayer: function(points, zoom) {
        this.points = points;
        this.heat.setLatLngs(this.points);
    }
}

function updateView(heatMap) {
    var upperLeftLat = mymap.getBounds().getNorth();
    var upperLeftLong = mymap.getBounds().getWest();
    var lowerRightLat = mymap.getBounds().getSouth();
    var lowerRightLong = mymap.getBounds().getEast();
    var zoom = mymap.getZoom();
    
    $.ajax({
        type: "GET",
        url: BASE_API_URL + "/getdata" + heatMap.dataSource,

        data: {
            lat1: upperLeftLat,
            long1: upperLeftLong,
            lat2: lowerRightLat,
            long2: lowerRightLong,
            zoom: zoom},
        success: function(response){
            if (response.data) {
                heatMap.updateHeatLayer(response.data, zoom);
            }
        },
        error: function(err){
            console.log("Failed to call /getdata. " + 
                    err.status + ": " + err.statusText);}
    });
}

$(document).ready(function(){
    heatMap.initHeatLayer();
    updateView(heatMap);
    mymap.on('moveend', function(){updateView(heatMap);});

    document.getElementById('dataselector').checked = true;
    document.getElementById('dataselector').onclick = function() {
        if (this.checked) {
            console.log("Using IPv6 data set");
            heatMap.dataSource = "v6";
        } else {
            console.log("Using IPv4 data set");
            heatMap.dataSource = "v4";
        }
        updateView(heatMap);
    };
});
