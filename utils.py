__author__ = 'se416237'
from cassandra.cluster import Cluster
from geopy.geocoders import Nominatim
from geopy.distance import vincenty


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