import utils
import json

conn = utils.cass_connect()
# rows = conn.execute("DROP table slots") or []
rows = conn.execute("SELECT * FROM slots WHERE user=''")
for row in rows:
    print(json.dumps(row))