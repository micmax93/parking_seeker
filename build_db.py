__author__ = 'se416237'
from cassandra.cluster import Cluster

cluster = Cluster(['micmax93.me'])
conn = cluster.connect()
conn.execute('DROP KEYSPACE IF EXISTS GPS')
conn.execute("CREATE KEYSPACE IF NOT EXISTS GPS WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }")
conn.execute('USE GPS')

conn.execute('CREATE TABLE IF NOT EXISTS parkings (id varchar,name varchar,address varchar,lat float,lon float,capacity int,PRIMARY KEY (id))')
conn.execute('CREATE TABLE IF NOT EXISTS users (username varchar,parking varchar,slot_no int,PRIMARY KEY (username))')
conn.execute('CREATE TABLE IF NOT EXISTS slots (parking_id varchar,slot_no int,user varchar,PRIMARY KEY ( parking_id, slot_no))')
conn.execute('create index IF NOT EXISTS slot_user on slots(user)')
conn.execute('CREATE INDEX IF NOT EXISTS users_parkings on users(parking)')
conn.execute('CREATE INDEX IF NOT EXISTS users_slots on users(slot_no)')