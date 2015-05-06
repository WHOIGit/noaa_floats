// using functions from floats.js
var map = create_map('map');
var featureOverlay = create_overlay(map);

// a DragBox interaction used to select features by drawing boxes
/*
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
    var feature = new ol.Feature({
      geometry: dragBox.getGeometry(),
    });
    featureOverlay.addFeature(feature);
    create_csv_link();
});
*/

// allow the user to draw a polygon feature
var dragPolygon = new ol.interaction.Draw({
    condition: ol.events.condition.shiftKeyOnly,
    type: 'Polygon'
});
map.addInteraction(dragPolygon);
dragPolygon.on('drawstart', function(e) {
    featureOverlay.getFeatures().clear();
});
dragPolygon.on('drawend', function(e) {
    var feature = e.feature;
    featureOverlay.addFeature(feature.clone());
    var format = new ol.format.WKT({
	defaultDataProjection: 'ESPG:3857'
    });
    feature.getGeometry().transform('EPSG:3857', 'EPSG:4326');
    var params = {
	low_pressure: Number($('#low_pressure').val()),
	high_pressure: Number($('#high_pressure').val()),
	geometry: format.writeFeature(feature)
    };
    var paramString = $.param(params);
    $.getJSON('/query_geom_floats.json?' + paramString, function(r) {
	$.each(r, function(ix, float_id) {
	    console.log('drawing track '+float_id);
	    draw_track(float_id, featureOverlay);
	});
    });
});

function create_csv_link() {
    var extent = dragBox.getGeometry().getExtent();
    latLonExtent = ol.proj.transformExtent(extent, 'EPSG:3857', 'EPSG:4326');
    var low_pressure = Number($('#low_pressure').val());
    var high_pressure = Number($('#high_pressure').val());
    var params = {
	left: latLonExtent[0],
	bottom: latLonExtent[1],
	right: latLonExtent[2],
	top: latLonExtent[3],
	low_pressure: low_pressure,
	high_pressure: high_pressure
    };
    console.log(latLonExtent + ' ' + low_pressure + ' ' + high_pressure);
    var paramString = $.param(params);
    var csv_url = '/query.csv?' + paramString
    $('#download').empty().html('<a href="'+csv_url+'">Download CSV</a>');
    // now, for yucks, draw the tracks
    $.getJSON('/query_floats.json?' + paramString, function(r) {
	$.each(r, function(ix, float_id) {
	    console.log('drawing track '+float_id);
	    draw_track(float_id, featureOverlay);
	});
    });
}

// validate pressure inputs
$('#low_pressure').on('change paste', function() {
    if(isNaN($('#low_pressure').val())) {
	$('#low_pressure').val('0');
    }
    create_csv_link();
});
$('#high_pressure').on('change paste', function() {
    if(isNaN($('#high_pressure').val())) {
	$('#high_pressure').val('9999');
    }
    create_csv_link();
});
