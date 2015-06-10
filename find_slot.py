__author__ = 'se416237'
import utils
import sys

user = 'Hans'
location = utils.rand_location()
print(utils.get_adr(location))

conn = utils.cass_connect()
parkings = conn.execute('SELECT * FROM parkings')
parkings = map(lambda x: (x, utils.get_distance(location, (x.lat, x.lon))), parkings)
parkings = sorted(parkings, key=lambda x: x[1])

find_slots = conn.prepare("SELECT * FROM slots WHERE parking_id=? AND user='' LIMIT 1")

my_slot = None
for p in parkings:
    free_slots = conn.execute(find_slots.bind([str(p[0].id)]))
    if len(free_slots)>0:
        my_slot = free_slots[0]
        print(p[0].name, p[1], "km \t", p[0].address, '  slot=', my_slot.slot_no)

if my_slot is None:
    print('No free slots')
    exit()

