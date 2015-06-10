import utils
import json

conn = utils.cass_connect()
rows = conn.execute("SELECT * FROM slots")
for row in rows:
    print(json.dumps(row))