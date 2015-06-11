from cassandra import ConsistencyLevel

__author__ = 'se416237'
import utils
import sys


class Obj(object):
    pass

user = 'Hans'
location = utils.rand_location()
print(utils.get_adr(location))

conn = utils.cass_connect()
q_find_slots = conn.prepare("SELECT * FROM slots WHERE parking_id=? AND user='' LIMIT 1")
q_take_slot = conn.prepare("INSERT INTO slots (parking_id, slot_no, user) VALUES (?, ?, ?)")
q_save_slot = conn.prepare("INSERT INTO users (username, parking, slot_no) VALUES (?, ?, ?)")
q_find_dup = conn.prepare("SELECT username FROM users WHERE parking=? AND slot_no=? LIMIT 2 ALLOW FILTERING")
q_check_slot = conn.prepare("SELECT user FROM slots WHERE parking_id=? AND slot_no=?")
q_safe_take_slot = conn.prepare("UPDATE slots SET user=? WHERE parking_id=? AND slot_no=? IF user=''")
q_safe_take_slot.consistency_level = ConsistencyLevel.QUORUM


def list_parkings(my_location):
    parkings = conn.execute('SELECT * FROM parkings')
    for i in range(len(parkings)):
        p = Obj()
        p.__dict__ = dict(parkings[i]._asdict().items())
        p.distance = utils.get_distance(my_location, (parkings[i].lat, parkings[i].lon))
        parkings[i] = p
    return sorted(parkings, key=lambda x: x.distance)


def find_slot(parkings):
    for p in parkings:
        free_slots = conn.execute(q_find_slots.bind([p.id]))
        if len(free_slots) > 0:
            my_slot = free_slots[0]
            return p, my_slot
    return None, None


def take_slot(slot, safe=False):
    if not safe:
        conn.execute(q_take_slot.bind([slot.parking_id, int(slot.slot_no), user]))
    else:
        conn.execute(q_safe_take_slot.bind([user, slot.parking_id, int(slot.slot_no)]))
    conn.execute(q_save_slot.bind((user, slot.parking_id, slot.slot_no)))


parkings = list_parkings(location)
p, slot = find_slot(parkings)
if slot is None:
    print("No empty slots!")
    exit()
else:
    print(p.name, p.distance, p.address, slot.slot_no)
take_slot(slot, safe=True)