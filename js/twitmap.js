
function initmap() {
    var mymap = L.map('mapid').setView([52.6, 4], 11);

    L.tileLayer("http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {maxzoom: 18}).addTo(mymap)
}

initmap()
