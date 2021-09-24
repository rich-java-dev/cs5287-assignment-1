# %%
import argparse
import json
from kafka import KafkaConsumer, TopicPartition  # kafka client publisher
from couchdb import Server

#
#  Consumer - subscribes to stock price data and persists data into couchdb
#
# %%
parser = argparse.ArgumentParser(
    description='Register as consumer to kafka server, recieve and persist stock price data into couchdb')

parser.add_argument('--topic', '-topic', '--t', '-t', default='FCEL',
                    type=str, help='a specific topic (ticker) to register as consumer with')

parser.add_argument('--server', '-server', default='129.114.26.60:9092',
                    help='the kafka server/node to register as consumer with')

parser.add_argument('--couchdb', '-couchdb', '--datastore', '-datastore',  default='http://admin:admin@127.0.0.1:5984/',
                    help='the couchdb server to post against')

args = parser.parse_args()

# %%
# get topic and look up via basic api
topic = args.topic
server = args.server
couchdb = args.couchdb

# sanitize input here...

# %%
# from kafka import KafkaConsum,er  # kafka client subscriber
# server = '129.114.26.60:9092'
print(f"attempting to connect to kafka server: '{server}' ...")
consumer = KafkaConsumer(topic, bootstrap_servers=server)
print("connected.")

# %%
# connect to couchdb /create database under topic
couch_server = Server(couchdb)
db_name = topic.lower()
try:
    db = couch_server.create(db_name)
except Exception:
    print("Database already exists")
    db = couch_server[db_name]


# %%
# subscribe to, and store all data into couchdb
for msg in consumer:
    # get bytes object from event
    raw_data = msg.value
    raw_str = raw_data.decode('utf8')  # decode bytes into str
    json_data = json.dumps(raw_str)  # dump str into json
    data = json.loads(raw_str)  # load up dictionary 'data' from raw str

    print(data)
    doc_id, doc_rev = db.save(data)

# %%
# print all documents by querying them from couchdb
# in the given database after publishing them.
for doc_id in db:
    print("fetching data from db:")
    doc = db[doc_id]
    print(doc)
