__author__ = 'se416237'
from cassandra.cluster import Cluster
from geopy.geocoders import Nominatim
from geopy.distance import vincenty
import random


def cass_connect():
    cluster = Cluster(['micmax93.me'])
    conn = cluster.connect()
    conn.execute('USE GPS')
    return conn


def get_gps(address):
    geolocator = Nominatim()
    try:
        location = geolocator.geocode(address, timeout=5)
    except:
        return None
    return location


def get_adr(gps):
    geolocator = Nominatim()
    try:
        location = geolocator.reverse(gps, timeout=5)
    except:
        return None
    return location.address


def get_distance(beg, end):
    return vincenty(beg, end).km


def rand_location():
    lon = random.randrange(16800, 16940)/1000.0
    lat = random.randrange(52380, 52630)/1000.0
    return lat, lon
