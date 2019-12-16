import math


class NotGPGGAError(Exception):
    pass


def decodeGPGGA(line):
    line = line.decode("ascii", errors="replace").strip()
    parts = line[1:].split(",")
    if parts[0] != "GPGGA":
        raise NotGPGGAError
    raw_lat = float(parts[2])
    raw_lon = float(parts[4])
    lat = math.modf(raw_lat / 100.0)[1] + math.modf(raw_lat / 100.0)[0] * (10.0 / 6.0)
    lon = math.modf(raw_lon / 100.0)[1] + math.modf(raw_lon / 100.0)[0] * (10.0 / 6.0)
    alt = float(parts[9])
    return lat, lon, alt
