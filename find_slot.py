__author__ = 'se416237'
import utils
import sys

user = 'Hans'
location = utils.rand_location()
print utils.get_adr(location)

conn = utils.cass_connect()
parkings = conn.execute('SELECT * FROM parkings')
parkings = map(lambda x: (x, utils.get_distance(location, (x.lat, x.lon))), parkings)
parkings = sorted(parkings, key=lambda x: x[1])

find_slots = conn.prepare("SELECT * FROM slots WHERE parking_id=? AND user='' LIMIT 1")
take_slot = conn.prepare("INSERT INTO slots (parking_id, slot_no, user) VALUES (?, ?, ?)")
save_slot = conn.prepare("INSERT INTO users (username, parking, slot_no) VALUES (?, ?, ?)")

my_slot = None
for p in parkings:
    free_slots = conn.execute(find_slots.bind([str(p[0].id)]))
    if len(free_slots) > 0:
        my_slot = free_slots[0]
        print p[0].name, p[1], "km \t", p[0].address, '  slot=', my_slot.slot_no

if my_slot is None:
    print('No free slots')
    exit()

conn.execute(take_slot.bind([my_slot.parking_id, int(my_slot.slot_no), user]))
conn.execute("INSERT INTO users (username, parking, slot_no) VALUES ('%s', '%s', %s)" % (user, my_slot.parking_id, my_slot.slot_no))

