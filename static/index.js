// using functions from floats.js
var map = create_map('map');
var featureOverlay = create_overlay(map);

// a DragBox interaction used to select features by drawing boxes
var dragBox = new ol.interaction.DragBox({
    condition: ol.events.condition.shiftKeyOnly,
    style: new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: [255, 0, 0, 1]
        })
    })
});

map.addInteraction(dragBox);

dragBox.on('boxstart', function(e) {
    featureOverlay.getFeatures().clear();
    $('#download').empty();
});
dragBox.on('boxend', function(e) {
    var extent = dragBox.getGeometry().getExtent();
    latLonExtent = ol.proj.transformExtent(extent, 'EPSG:3857', 'EPSG:4326');
    console.log(latLonExtent);
    var feature = new ol.Feature({
      geometry: dragBox.getGeometry(),
      name: 'a drag box'
    });
    featureOverlay.addFeature(feature);
    var params = {
	left: latLonExtent[0],
	bottom: latLonExtent[1],
	right: latLonExtent[2],
	top: latLonExtent[3]
    };//FIXME add pressure
    var paramString = $.param(params)
    var csv_url = '/query.csv?' + paramString
    $('#download').empty().html('<a href="'+csv_url+'">Download CSV</a>');
});
