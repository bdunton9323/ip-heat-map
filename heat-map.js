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
    opts: {radius: 30, blur: 30, maxZoom: 15},
    
    initHeatLayer: function() {
        this.heat = L.heatLayer([], this.opts).addTo(mymap);
    },

    updateHeatLayer: function(points, zoom) {
        this.points = points;
        this.heat.setLatLngs(this.points);
        if (zoom < 10) {
            console.log("setting options");
            //this.opts.blur = 100;
            this.heat.setOptions(this.opts)
        }
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
        url: "http://192.168.1.8:8888/getdata",

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
});





