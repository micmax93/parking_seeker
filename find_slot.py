from cassandra import ConsistencyLevel
import random

__author__ = 'se416237'
import utils


class Obj(object):
    pass

conn = utils.cass_connect()
q_find_slots = conn.prepare("SELECT * FROM slots WHERE parking_id=? AND user='' LIMIT 10")
q_take_slot = conn.prepare("INSERT INTO slots (parking_id, slot_no, user) VALUES (?, ?, ?)")
q_save_slot = conn.prepare("INSERT INTO users (username, parking, slot_no) VALUES (?, ?, ?)")
q_find_dup = conn.prepare("SELECT username FROM users WHERE parking=? AND slot_no=? LIMIT 2 ALLOW FILTERING")
q_check_slot = conn.prepare("SELECT user FROM slots WHERE parking_id=? AND slot_no=?")
q_safe_take_slot = conn.prepare("UPDATE slots SET user=? WHERE parking_id=? AND slot_no=? IF user=''")
q_find_slots.consistency_level = ConsistencyLevel.QUORUM
q_take_slot.consistency_level = ConsistencyLevel.QUORUM
q_save_slot.consistency_level = ConsistencyLevel.QUORUM
q_find_dup.consistency_level = ConsistencyLevel.QUORUM
q_check_slot.consistency_level = ConsistencyLevel.QUORUM
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
            my_slot = free_slots[random.randint(0, len(free_slots)-1)]
            return p, my_slot
    return None, None


def take_slot(user, slot, safe=False):
    conn.execute(q_save_slot.bind((user, slot.parking_id, slot.slot_no)))
    if not safe:
        conn.execute(q_take_slot.bind([slot.parking_id, int(slot.slot_no), user]))
    else:
        conn.execute(q_safe_take_slot.bind([user, slot.parking_id, int(slot.slot_no)]))
   # conn.execute(q_save_slot.bind((user, slot.parking_id, slot.slot_no)))


def validate_slot(user, slot):
    dups = conn.execute(q_find_dup.bind([slot.parking_id, slot.slot_no]))
    if len(dups) == 1 and dups[0].username == user:
        return True
    # raw_input('to slow!...')
    u = conn.execute(q_check_slot.bind([slot.parking_id, slot.slot_no]))[0].user
    return u == user


def run(user, location):
    parkings = list_parkings(location)
    safe = False
    while True:
        p, slot = find_slot(parkings)
        if slot is None:
            return None, None
        # raw_input('should I?')
        take_slot(user, slot, safe=safe)
        if validate_slot(user, slot):
            return p, slot
        safe = True

if __name__ == "__main__":
    import sys
    user = sys.argv[1]
    location = utils.rand_location()
    print(utils.get_adr(location))
    p, slot = run(user, location)
    if p is None:
        print("No free slots!")
    else:
        print(p.name, p.distance, "km\t", p.address, " \tslot=", slot.slot_no)
