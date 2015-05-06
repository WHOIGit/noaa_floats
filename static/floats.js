function create_map(target) {
    var mqLayer = new ol.layer.Tile({
	source: new ol.source.MapQuest({layer:'sat'})
    });
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

function create_overlay(map) {
    var featureOverlay = new ol.FeatureOverlay({
	style: new ol.style.Style({
	    fill: new ol.style.Fill({
		color: 'rgba(255, 255, 255, 0.2)'
	    }),
	    stroke: new ol.style.Stroke({
		color: '#ffcc33',
		width: 2
	    }),
	    image: new ol.style.Circle({
		radius: 7,
		fill: new ol.style.Fill({
		    color: '#ffcc33'
		})
	    })
	})
    });
    featureOverlay.setMap(map);
    return featureOverlay;
}

function draw_track(float_id, featureOverlay) {
    // now get a track and draw it
    $.getJSON('/track/'+float_id, function(r) {
	var format = new ol.format.WKT({
	    defaultDataProjection: 'ESPG:4326'
	});
	var geom = format.readGeometry(r.track);
	var xf = ol.proj.getTransform('EPSG:4326', 'EPSG:3857');
	geom.applyTransform(xf);
	var feature = new ol.Feature({
	    geometry: geom,
	    name: ''+float_id
	});
	featureOverlay.addFeature(feature);
    });
}
