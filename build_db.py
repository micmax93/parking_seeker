__author__ = 'se416237'
from cassandra.cluster import Cluster

cluster = Cluster(['micmax93.me'])
conn = cluster.connect()
conn.execute("CREATE KEYSPACE IF NOT EXISTS GPS WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 4 }")
conn.execute('USE GPS')

conn.execute('CREATE TABLE IF NOT EXISTS parkings (id varchar,name varchar,address varchar,lat float,lon float,capacity int,PRIMARY KEY (id))')
conn.execute('CREATE TABLE IF NOT EXISTS users (username varchar,parking varchar,slot_no int,PRIMARY KEY (username))')
conn.execute('CREATE TABLE IF NOT EXISTS slots (parking_id varchar,slot_no int,user varchar,PRIMARY KEY ( parking_id, slot_no))')
conn.execute('create index IF NOT EXISTS slot_user on slots(user)')


print(conn.execute("select * from users"))
print(conn.execute("select * from parkings"))

# conn.execute("INSERT INTO users (username) VALUES ('Adolfik');")
# conn.execute("INSERT INTO parkings (id, name, address, lat, lon, capacity) VALUES ('007','parking1','dluga 5',52.45,16.85,69);")
# conn.execute("INSERT INTO slots (parking_id, slot_no, user) VALUES ('007',21,'Adolfik');")
import json

print(json.dumps(conn.execute("select * from slots"), indent=2))