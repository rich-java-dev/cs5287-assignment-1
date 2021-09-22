import argparse
from kafka import KafkaConsumer, TopicPartition  # kafka client publisher
import json  # used as serializer context

#
#  Consumer - subscribes to stock price data and persists into couchdb
#

parser = argparse.ArgumentParser(
    description='Register as consumer to kafka server, recieve and persist stock price data into couchdb')

parser.add_argument('--topic', '-topic', '--t', '-t', nargs='+', default='FCEL',
                    type=str, help='a specific topic (ticker) to look up on ')

parser.add_argument('--server', '-server', default='129.114.26.60:9092',
                    help='the kafka server/node to register as publisher with')

parser.add_argument('--couchdb', '-couchdb', '--datastore', '-datastore',  default='127.0.0.1:5987',
                    help='the kafka server/node to register as publisher with')


args = parser.parse_args()

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
for msg in consumer:
    print(type(msg))
    print(msg)
