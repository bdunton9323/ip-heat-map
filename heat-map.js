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
        this.heat = L.heatLayer([], {radius: 30, blur: 15, maxZoom: 20}).addTo(mymap);
    },
    
    updateHeatLayer: function(points) {
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
        
        // TODO: this has to be the URL of my server as seen externally
        url: "http://localhost:8888/getdata",

        data: {
            lat1: upperLeftLat,
            long1: upperLeftLong,
            lat2: lowerRightLat,
            long2: lowerRightLong,
            zoom: zoom},
        success: function(response){
            if (response.data) {
                heatMap.updateHeatLayer(response.data);
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
});





