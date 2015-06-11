from cassandra import ConsistencyLevel

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
take_slot = conn.prepare("INSERT INTO slots (parking_id, slot_no, user) VALUES (?, ?, ?)")
save_slot = conn.prepare("INSERT INTO users (username, parking, slot_no) VALUES (?, ?, ?)")
#save_slot.consistency_level = ConsistencyLevel.QUORUM

my_slot = None
for p in parkings:
    free_slots = conn.execute(find_slots.bind([str(p[0].id)]))
    if len(free_slots) > 0:
        my_slot = free_slots[0]
        print(p[0].name, p[1], "km \t", p[0].address, '  slot=', my_slot.slot_no)
        break

if my_slot is None:
    print('No free slots')
    exit()
conn.execute(take_slot.bind([my_slot.parking_id, int(my_slot.slot_no), user]))

conn.execute(save_slot.bind((user, my_slot.parking_id, my_slot.slot_no)))
# conn.execute("INSERT INTO users (username, parking, slot_no) VALUES ('%s', '%s', %s)" % (user, my_slot.parking_id, my_slot.slot_no))

slotsDup = conn.prepare("SELECT username FROM users WHERE parking=? AND slot_no=? ALLOW FILTERING")

count = conn.execute(slotsDup.bind([my_slot.parking_id, my_slot.slot_no]))
print (count)
if len(count)>1:
    print("chcem nowe miejsce")
    for p in parkings:
        free_slots2 = conn.execute(find_slots.bind([str(p[0].id)]))
        if len(free_slots2) > 0:
            my_slot2 = free_slots2[0]
            print(p[0].name, p[1], "km \t", p[0].address, '  slot=', my_slot2.slot_no)
            break

    take_slot2 = conn.prepare("INSERT INTO slots (parking_id, slot_no, user) VALUES (?, ?, ?) IF NOT EXISTS")  # albo:  conn.prepare("UPDATE slots SET user=? where parking_id=? AND slot_no=? IF slot_no='' ") ?
    # przy 2giej wersji:  conn.execute(take_slot.bind(( user, my_slot.parking_id, my_slot.slot_no)))   # tylko to jebie coœ o incie ''
    take_slot2.consistency_level=ConsistencyLevel.QUORUM
    rs = conn.execute(take_slot2.bind([my_slot2.parking_id, int(my_slot2.slot_no), user]))
    # ELF: Jest chunia, bo potrzebujemy 3 replik, zeby to polecenie odpalic! :D obawiam sie tego not exists
    conn.execute(save_slot.bind((user, my_slot2.parking_id, my_slot2.slot_no)))