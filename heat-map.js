// durham: [35.99, -78.8986]
// manhattan: [40.7831, -73.9712]
var mymap = L.map('mapid').setView([40.7831, -73.9712], 13);

L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    subdomains: ['a','b','c']
}).addTo(mymap);

var heatMap = {
    heat: null,
    points: [],
    
    initHeatLayer: function() {
        console.log("Initializing heat layer: " + this.points);
        this.heat = L.heatLayer([], {radius: 30, blur: 15, maxZoom: 20}).addTo(mymap);
    },
    
    updateHeatLayer: function(points) {
        this.points = points;
        for (var i = 0; i < this.points.length; i++) {
            this.heat.setLatLngs(this.points);
        }
    }
}

function updateView(heatMap) {
    var upperLeftLat = mymap.getBounds().getNorth();
    var upperLeftLong = mymap.getBounds().getWest();
    var lowerRightLat = mymap.getBounds().getSouth();
    var lowerRightLong = mymap.getBounds().getEast();

    $.ajax({
        type: "GET",
        url: "http://localhost:8888/getdata",
        // TODO: it might be cleaner to pass an array of points: [[x1,y1],[x2,y2]]
        data: {
            lat1: upperLeftLat,
            long1: upperLeftLong,
            lat2: lowerRightLat,
            long2: lowerRightLong},
        success: function(response){
            heatMap.updateHeatLayer(response.data);
        },
        error: function(err){}
    });
}

$(document).ready(function(){
    console.log("this is called");
    heatMap.initHeatLayer();
    updateView(heatMap);
    mymap.on('moveend', function(){updateView(heatMap);});
});





