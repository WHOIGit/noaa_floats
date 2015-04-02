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

// The features are not added to a regular vector layer/source,
// but to a feature overlay which holds a collection of features.
// This collection is passed to the modify and also the draw
// interaction, so that both can add or modify features.
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

dragBox.on('boxend', function(e) {
    var extent = dragBox.getGeometry().getExtent();
    latLonExtent = ol.proj.transformExtent(extent, 'EPSG:3857', 'EPSG:4326');
    console.log(latLonExtent); // FIXME draw bounding box
    var feature = new ol.Feature({
      geometry: dragBox.getGeometry(),
      name: 'a drag box'
    });
    featureOverlay.addFeature(feature);
});
