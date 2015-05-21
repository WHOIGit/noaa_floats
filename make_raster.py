import mapnik
m = mapnik.Map(2400,2400)
m.srs = "+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +units=m +k=1.0 +nadgrids=@null +no_defs +over"
m.background = mapnik.Color('rgba(0,0,0,0)')
s = mapnik.Style()
r = mapnik.Rule()
line_symbolizer = mapnik.LineSymbolizer(mapnik.Color('rgb(50%,50%,50%)'),1)
r.symbols.append(line_symbolizer)
s.rules.append(r)
m.append_style('My Style',s)
ds = mapnik.PostGIS(
    host='localhost',
    dbname='floats',
    user='floats',
    password='floats',
    table='floats',
    geometry_field='track'
)
layer = mapnik.Layer('world')
layer.srs = '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'
layer.datasource = ds
layer.styles.append('My Style')
m.layers.append(layer)
# worldExtent is in the map srs which is mercator
worldExtent = mapnik.Box2d(-20037508.34,-20037508.34,20037508.34,20037508.34)
m.zoom_to_box(worldExtent)
OUTF='static/world.png'
mapnik.render_to_file(m,OUTF,'png')
print "rendered image to '%s'" % OUTF

