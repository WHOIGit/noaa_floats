function create_map(target) {
    // create map based on MapQuest satellite layer
    var mqLayer = new ol.layer.Tile({
	source: new ol.source.MapQuest({layer:'sat'})
    });
    // center of the universe is Woods Hole MA
    var woho = ol.proj.transform([-70.661810, 41.526994], 'EPSG:4326', 'EPSG:3857');
    var aView = new ol.View({
	center: woho,
	zoom: 4
    });
    var map = new ol.Map({
	target: 'map'
    });
    map.addLayer(mqLayer);
    map.setView(aView);
    return map;
}

function create_overlay(map, color) {
    // create an overlay for features
    var overlay = new ol.FeatureOverlay({
	style: new ol.style.Style({
	    fill: new ol.style.Fill({
		color: 'rgba(255, 255, 255, 0.2)'
	    }),
	    stroke: new ol.style.Stroke({
		color: color,
		width: 2
	    })
	})
    });
    overlay.setMap(map);
    return overlay;
}

function random_color() {
    var r = Math.floor(Math.random()*256);
    var g = Math.floor(Math.random()*256);
    var b = Math.floor(Math.random()*256);
    return 'rgb('+r+','+g+','+b+')';
}

function id2color(id) {
    var r = (id % 128) + 127;
    var g = ((id >> 7) % 128) + 127;
    var b = ((id >> 14) % 128) + 127;
    return 'rgb('+r+','+g+','+b+')';
}

function draw_track(float_id, featureOverlay) {
    // get a track and draw it
    $.getJSON('/track/'+float_id, function(r) {
	var format = new ol.format.WKT({
	    defaultDataProjection: 'ESPG:4326'
	});
	var geom = format.readGeometry(r.track);
	geom.transform('EPSG:4326', 'EPSG:3857');
	var feature = new ol.Feature({
	    geometry: geom,
	    name: ''+float_id
	});
	feature.setStyle(new ol.style.Style({
	    stroke: new ol.style.Stroke({
		color: id2color(float_id),
		width: 2
	    })
	}));
	featureOverlay.addFeature(feature);
    });
}
