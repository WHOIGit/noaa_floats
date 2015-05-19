// using functions from floats.js
var map = create_map('map');

// create layer for tracks
var tracksLayer = create_overlay(map, '#ffcc33');

// create layer for selections
var selectionLayer = create_overlay(map, '#ff0000');

// allow the user to draw a polygon feature
var dragPolygon = new ol.interaction.Draw({
    condition: ol.events.condition.shiftKeyOnly,
    type: 'Polygon'
});
map.addInteraction(dragPolygon);
dragPolygon.on('drawstart', function(e) {
    selectionLayer.getFeatures().clear();
});
dragPolygon.on('drawend', function(e) {
    tracksLayer.getFeatures().clear();
    // draw a copy of the feature on the map
    var feature = e.feature;
    selectionLayer.addFeature(feature.clone());
    // now convert it to lat/lon
    feature.getGeometry().transform('EPSG:3857', 'EPSG:4326');
    // now generate a WKT representation of it
    var format = new ol.format.WKT({
	defaultDataProjection: 'ESPG:3857'
    });
    var wkt = format.writeFeature(feature);
    // add pressure parameters to geometry parameter
    var params = {
	low_pressure: getLowPressure(),
	high_pressure: getHighPressure(),
	start_date: formatDateParam(getStartDate()),
	end_date: formatDateParam(getEndDate()),
	geometry: format.writeFeature(feature)
    };
    var paramString = $.param(params);
    // query for floats
    $.getJSON('/query_geom_floats.json?' + paramString, function(r) {
	$.each(r, function(ix, float_id) { // for each float
	    // draw its track
	    console.log('drawing track '+float_id);
	    draw_track(float_id, tracksLayer);
	});
    });
    // generate a CSV URL for this query
    var csv_url = '/query_geom.csv?' + paramString;
    // and populate the link interface
    $('#download').empty().html('<a href="'+csv_url+'">Download CSV</a>');
});

function getLowPressure() {
    return $('#pressureSlider').rangeSlider("values").min;
}
function getHighPressure() {
    return $('#pressureSlider').rangeSlider("values").max;
}
function getStartDate() {
    return $('#dateSlider').dateRangeSlider("values").min;
}
function getEndDate() {
    return $('#dateSlider').dateRangeSlider("values").max;
}
function formatDateParam(dp) {
    return dp.toISOString().substring(0,10);
}

// show all float tracks
$('#all').on('click', function() {
    $.getJSON('/all_floats.json', function(r) {
	$.each(r, function(ix, float_id) {
	    console.log('drawing track '+float_id);
	    draw_track(float_id, tracksLayer);
	});
    });
});

// pressure slider
$('#pressureSlider').rangeSlider({
    bounds: {
	min: 0,
	max: 9999
    },
    defaultValues: {
	min: 1000,
	max: 9999
    }
});
$('#dateSlider').dateRangeSlider({
    bounds: {
	min: new Date(1972,8,28),
	max: new Date()
    },
    defaultValues: {
	min: new Date(1980,0,1),
	max: new Date(2015,0,1)
    }
});
