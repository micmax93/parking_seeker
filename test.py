import utils
import json

conn = utils.cass_connect()
# rows = conn.execute("DROP table slots") or []
rows = conn.execute("SELECT * FROM users")
for row in rows:
    print(json.dumps(row))