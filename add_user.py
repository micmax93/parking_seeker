__author__ = 'ple91'

import utils
import sys, uuid

p_id = str(uuid.uuid1())
username = sys.argv[1]

conn = utils.cass_connect()

insert_user = conn.prepare('INSERT INTO users ( username) VALUES (?)')
conn.execute(insert_user.bind([username]))