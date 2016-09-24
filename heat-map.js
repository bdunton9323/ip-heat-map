// durham: [35.99, -78.8986]
// manhattan: [40.7831, -73.9712]
var mymap = L.map('mapid').setView([40.7831, -73.9712], 13);

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

$(document).ready(function(){
    // TODO: do this a better way than having a function initialize a global 'heat' var
    initHeatLayer();
    updateView()});
mymap.on('moveend', updateView);
//var heat = updateHeatLayer(testPoints);

function initHeatLayer(points) {
    console.log("Initializing heat layer: " + points);
    heat = L.heatLayer([], {radius: 30, blur: 15, maxZoom: 20}).addTo(mymap);
}

function updateHeatLayer(points) {
    console.log("Updating heat layer: " + points);
    for (var i = 0; i < points.length; i++) {
        heat.addLatLng(points[i]);
    }
}

function updateView() {
    var upperLeftLat = mymap.getBounds().getNorth();
    var upperLeftLong = mymap.getBounds().getWest();
    var lowerRightLat = mymap.getBounds().getSouth();
    var lowerRightLong = mymap.getBounds().getEast();
    
    console.log("UL: (" + upperLeftLat + ", " + upperLeftLong + ") LR: (" + lowerRightLat + " " + lowerRightLong + ")");

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
        success: function(response){
            console.log("got data: " + response.data[0]); 
            updateHeatLayer(response.data);
        },
        error: function(err){}
    });
}

