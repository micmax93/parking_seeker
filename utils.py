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
        location = geolocator.geocode(address)
    except:
        return None
    return location


def get_distance(beg, end):
    return vincenty(beg, end).km


def rand_location():
    lon = random.randrange(1680, 1694)/100.0
    lat = random.randrange(5238, 5263)/100.0
    return lat, lon
