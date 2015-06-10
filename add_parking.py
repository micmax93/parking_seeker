__author__ = 'se416237'

import utils
import sys, uuid

p_id = str(uuid.uuid1())
name = sys.argv[1]
capacity = int(sys.argv[2])

if len(sys.argv) >= 4:
    address = sys.argv[3]
else:
    address = utils.get_adr(utils.rand_location())
gps = utils.get_gps(address)

conn = utils.cass_connect()

insert_parking = conn.prepare('INSERT INTO parkings (id, name, address, lat, lon, capacity) VALUES (?, ?, ?, ?, ?, ?)')
conn.execute(insert_parking.bind([p_id, name, address, gps.latitude, gps.longitude, capacity]))

insert_slot = conn.prepare('INSERT INTO slots (parking_id, slot_no,user) VALUES (?, ?,"")')
for x in range(0,capacity):
    conn.execute(insert_slot.bind([p_id, x]))