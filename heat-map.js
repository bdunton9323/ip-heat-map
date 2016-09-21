var mymap = L.map('mapid').setView([35.99, -78.8986], 13);

L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    subdomains: ['a','b','c']
}).addTo(mymap);

var testPoints = [[35, -78.8986, 0.2], // lat, long, intensity
    [35.99, -78.8986, 0.2],
    [35.99, -78.8986, 0.2],
    [35.99, -78.8986, 0.2],
    [35.99, -78.8986, 0.2],
    [35.99, -78.8986, 0.2],
    [35.99, -78.8986, 0.2],
    [35.99, -78.8986, 0.2],
    [35.99, -78.8986, 0.2],
    [35.99, -79, 0.5]];

var heat = null;

$(document).ready(function(){initHeatLayer(testPoints);});
//var heat = updateHeatLayer(testPoints);

function initHeatLayer(points) {
    console.log("Initializing heat layer: " + points);
    heat = L.heatLayer(points, {radius: 25}).addTo(mymap);
}

function updateHeatLayer(points) {
    console.log("Updating heat layer: " + points);
    for (var i = 0; i < points.length; i++) {
        heat.addLatLng(points[i]);
    }
}

mymap.on('moveend', function() {
    var upperLeftLat = mymap.getBounds().getWest();
    var upperLeftLong = mymap.getBounds().getNorth();
    var lowerRightLat = mymap.getBounds().getEast();
    var lowerRightLong = mymap.getBounds().getSouth();

    $.ajax({
        type: "GET",
        url: "http://localhost:8888/getdata",
        // TODO: it might be cleaner to pass an array of points: [[x1,y1],[x2,y2]]
        data: {
            lat1: upperLeftLat, 
            long1: upperLeftLong,
            lat2: lowerRightLat,
            long2: lowerRightLong},
        //contentType: 'application/json; charset=utf-8',
        //dataType: "json",
        success: function(response){console.log("got data: " + response); updateHeatLayer(response.data);},
        error: function(err){}
    });
});