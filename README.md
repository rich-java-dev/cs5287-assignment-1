
# cs5287-assignment-1
## MessageQueue/DataStore Pipeline using Kafka/CouchDB
### authors: 
Richard White, Rupak Mohanty

## Intro

The purpose of this assignment was to become familiar with the provisioning and configuration of cloud resources, and to build a distributed work-flow.
There are 4 independent hosts in this system.

- 2 host/producers deployed on local/laptop/virtual box
	- configured with DHCP server and subnetted to separate interfaces/IPs
- 2 hosts deployed on cloud (Chameleon) which will server as a multi-node kafka/event stream platform.
- 1 of the 2 cloud hosts will also act as a database end-point to store data provided by producers.


## Primary Technologies
- Operating System - Ubuntu 20.04 
	- apt/dpkg package mgmt w/ ubunutu repositories
- Development Language - Python as the front-end/client language
	- pip as dependency management software
	- client-side producers that generate data by topic, and publish to kafka 
	- server-side consumers that subscribe to topics, and persist data into couchdb

- java runtime required for kafka nodes/instances
- apache kafka - and event streaming platform (Message Queue) built for dependability in distributed systems context.
- couchdb - a RESTful, Document based (NoSQL) DataStore.

## Cloud Provisioning
- create 2 new instances, based on of Ubuntu 20.04 image.
- create/assign RSA key pair
- add proper security group to instances (default + shared kafka/couchdb config)
- assign floating IPs to both instances
- ssh will be used 
	> ssh -i /path/to/key cc@<floating.public.ip>
- configuring ufw (Ubuntu's uncomplicated firewall)
	 > sudo ufw <status|enable|disable>
	 > sudo ufw allow from \<trusted ip>

## Kafka installation/set-up

prerequisites:
install java and configure kafka env variable to use IPv4
> sudo apt install default-jre -y
>  export KAFKA_OPTS="-Djava.net.preferIPv4Stack=True"

download/untar:
> wget https://dlcdn.apache.org/kafka/2.8.0/kafka_2.13-2.8.0.tgz
> tar -xvf kafka_2.13-2.8.0.tgz
> cd kafka_2.13-2.8.0

configuring kafka:
- nano config/server.properties

starting zookeeper (1 host required, could use additional for active replication) from kafka root dir
 - bin/zookeeper-server-start.sh config/zookeeper.properties &

starting kafka cluster (both cloud hosts) from kafka root dir
 - bin/kafka-server-start.sh config/server.properties &

checking running nodes:
- bin/zookeeper-shell.sh localhost:2181 ls /brokers/ids
- bin/zookeeper-shell.sh localhost:2181 get /brokers/ids/0
- bin/zookeeper-shell.sh localhost:2181 get /brokers/ids/1


## Producers

- We will use yfinance API to look up and publish historical stock price data by ticker (each topic is a different ticker)
- yfinance uses pandas/numpy as the primary data structures for storing queries 

Install Python
> sudo apt install python
> sudo apt install pip

Install python dependencies via pip
> pip install -r src/requirements.txt

Review Producer options
>  python3 h1/Producer.py --help
>>  optional arguments:
  -h, --help            show this help message and exit
  --topic TOPIC [TOPIC ...], -topic TOPIC [TOPIC ...], --t TOPIC [TOPIC ...], -t TOPIC [TOPIC ...]
                        a specific topic (ticker) to look up on
  --start_date START_DATE, --start START_DATE, -start START_DATE, -begin START_DATE
                        starting date for ticker history range
  --end_date END_DATE, --end END_DATE, -end END_DATE, --e END_DATE, -e END_DATE
                        ending date for ticker history range
  --server SERVER, -server SERVER
                        the kafka server/node to register as publisher with

Run Producer
 > python3 src/h1/Producer.py --topic FCEL --start_date 2021-01-01 --end_date 2021-09-21

