
from pyproj import transform
from pyproj import Proj


# Rijksdriehoeks stelsel.
RD = ("+proj=sterea +lat_0=52.15616055555555 +lon_0=5.38763888888889 "
      "+k=0.999908 +x_0=155000 +y_0=463000 +ellps=bessel "
      "+towgs84=565.237,50.0087,465.658,-0.406857,0.350733,-1.87035,4.0812 "
      "+units=m +no_defs")
rd_projection = Proj(RD)

WGS84 = ('+proj=latlong +datum=WGS84')
wgs84_projection = Proj(WGS84)


def rd_to_wgs84(x, y):
    """Return WGS84 coordinates from RD coordinates."""
    return transform(rd_projection, wgs84_projection, x, y)
