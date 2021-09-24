
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
	 
- transferring files via scp - we will use this to deploy the python scripts to run:
> scp -i {key_file} [user@source:][source_file] [user@destination:][dest_file]

> $ scp -i /c/users/rwhite/.ssh/t6-rw1 /c/vanderbilt/CS5287/cs5287-assignment-1/src/h3/Consumer.py cc@129.114.26.60:Consumer.py

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

## CouchDB configuration/set-up

> sudo apt update && sudo apt install -y curl apt-transport-https gnupg

> curl https://couchdb.apache.org/repo/keys.asc | gpg --dearmor | sudo tee /usr/share/keyrings/couchdb-archive-keyring.gpg >/dev/null 2>&1

> source /etc/os-release

> echo  "deb [signed-by=/usr/share/keyrings/couchdb-archive-keyring.gpg] https://apache.jfrog.io/artifactory/couchdb-deb/ _${_VERSION_CODENAME_}_ main" | sudo tee etc/apt/sources.list.d/couchdb.list >/dev/null

> sudo apt update  

> sudo apt install -y couchdb

### test Couchdb:

> curl http://127.0.0.1:5984/

expected response:

> {"couchdb":"Welcome","version":"3.1.1","git_sha":"ce596c65d","uuid":"46d26c41cd949d16e4c3f10ca5b85fb8","features":["access-ready","partitioned","pluggable-storage-engines","reshard","scheduler"],"vendor":{"name":"The Apache Software Foundation"}}

### install python couchdb package
> pip install couchdb


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

Run Producer(s) on multiple hosts
 > python3 src/h1/Producer.py --topic APPL --start_date 2021-01-01 --end_date 2021-09-24 &

> python3 src/h1/Producer.py --topic MSFT --start_date 2021-01-01 --end_date 2021-09-24 &


## Consumers

The Consumer app is founder under src/h3/Consumer.py

This app behaves as a Kafka Consumer and interfaces with the CouchDB server.

Install Python
> sudo apt install python
> sudo apt install pip

Install python dependencies via pip
> pip install -r src/requirements.txt

Review Producer options

> python3 h3/Consumer.py --help
> optional arguments:
  -h, --help            show this help message and exit
  --topic TOPIC [TOPIC ...], -topic TOPIC [TOPIC ...], --t TOPIC [TOPIC ...], -t TOPIC [TOPIC ...]
                        a specific topic (ticker) to register as consumer with
  --server SERVER, -server SERVER
                        the kafka server/node to register as consumer with
  --couchdb COUCHDB, -couchdb COUCHDB, --datastore COUCHDB, -datastore COUCHDB
                        the couchdb server to post against

Run multiple Consumers on h3 host
> python3 Consumer.py --topic MSFT &

> python3 Consumer.py --topic APPL &