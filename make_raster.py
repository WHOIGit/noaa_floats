import mapnik
m = mapnik.Map(1200,1200)
m.srs = "+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +units=m +k=1.0 +nadgrids=@null +no_defs"

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


# http://svn.openstreetmap.org/applications/rendering/mapnik/generate_image.py
# shows reprojection, but I don't have it working yet
#longlat = mapnik.Projection('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
#merc = mapnik.Projection('+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over')
#transform = mapnik.ProjTransform(longlat,merc)
#merc_box = transform.forward(mapnik.Box2d(-179,-89,179,89))
#m.zoom_to_box(merc_box)

#worldExtent = mapnik.Box2d(-180.0, -90.0, 180.0, 90.0)
worldExtent = mapnik.Box2d(-20037508.34,-20037508.34,20037508.34,20037508.34)
m.zoom_to_box(worldExtent) # but we need to reproject to mercator
OUTF='static/world.png'
mapnik.render_to_file(m,OUTF,'png')
print "rendered image to '%s'" % OUTF

