# %%
import argparse
import yfinance as yf  # downloading data from yahoo finance api stock data
from kafka import KafkaProducer  # kafka client publisher
import json  # used as serializer context
from time import sleep
import pandas as pd

#
#  PRICER - Produces Stock price data onto a given Kafka server
#
# %%
parser = argparse.ArgumentParser(
    description='Look up historic stock data for a given ticket (topic)')

parser.add_argument('--topic', '-topic', '--t', '-t', default='FCEL',
                    type=str, help='a specific topic (ticker) to look up on ')

parser.add_argument('--start_date', '--start', '-start', '-begin',
                    default='2021-01-01', help='starting date for ticker history range')

parser.add_argument('--end_date', '--end', '-end', '--e', '-e',
                    default='2021-09-01', help='ending date for ticker history range')

parser.add_argument('--server', '-server', default='129.114.26.60:9092',
                    help='the kafka server/node to register as publisher with')

args = parser.parse_args()

# get topic and look up via basic api
topic = args.topic
start_date = args.start_date
end_date = args.end_date
server = args.server

# sanitize input here...

print(f"Producer expecting to publish on topic {topic} from {start_date} to {end_date}")

# %%
# connect producer to kafka server
print(f"attempting to register to kafka server: '{server}' ...")
# acquire the producer
# (you will need to change this to your bootstrap server's IP addr)
producer = KafkaProducer(bootstrap_servers=[server],
                         api_version=(0, 11, 5),
                         acks=1)  # wait for leader to write to log

print("connected.")

# %%
# download stock data
data = yf.download(tickers=topic, start=start_date, end=end_date)

# format the index as an actual column
data['date'] = data.index
data['date'] = data['date'].dt.strftime('%Y-%m-%d') # format date into mm/dd/yyyy format

# serialize data into json
data['json'] = data.apply(lambda x: x.to_json(), axis=1)

# %%
# process the data and publish each 'row' to Kafka server
for row in data.json.iteritems():
    val = row[1]
    print(val)
    producer.send(topic, bytes(val, 'utf-8')) # encode as utf-8 string
    sleep(1)
