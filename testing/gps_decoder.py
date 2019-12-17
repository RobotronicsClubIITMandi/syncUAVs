import math
from math import radians, cos, sin, asin, sqrt


class NotGPGGAError(Exception):
    pass


class FixNotAcquiredError(Exception):
    pass


def decodeGPGGA(line):
    line = line.decode("ascii", errors="replace").strip()
    parts = line[1:].split(",")
    if parts[0] != "GPGGA":
        raise NotGPGGAError
    try:
        raw_lat = float(parts[2])
        raw_lon = float(parts[4])
    except ValueError:
        raise FixNotAcquiredError
    lat = math.modf(raw_lat / 100.0)[1] + math.modf(raw_lat / 100.0)[0] * (10.0 / 6.0)
    lon = math.modf(raw_lon / 100.0)[1] + math.modf(raw_lon / 100.0)[0] * (10.0 / 6.0)
    alt = float(parts[9])
    return lat, lon, alt


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r * 100.0  # return in meters
