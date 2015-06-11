import utils
import json

conn = utils.cass_connect()
# rows = conn.execute("INSERT INTO users(username, parking, slot_no) VALUES ('fredy', 'dc7c97f0-1027-11e5-9839-c92f508c7e4f', 3)") or []
# rows = conn.execute("INSERT INTO slots(user, parking_id, slot_no) VALUES ('fredy', 'dc7c97f0-1027-11e5-9839-c92f508c7e4f', 3)") or []
rows = conn.execute("SELECT * FROM slots")
for row in rows:
    print(json.dumps(row))