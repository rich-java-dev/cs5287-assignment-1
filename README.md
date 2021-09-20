
#  cscs5287-assignment-1
## MessageQueue/DataStore Pipeline using Kafka/CouchDB
### Richard White, Rupak Mohanty

## Intro

The purpose of this assignment was to become familiar with the provisioning and configuration of cloud resources, and to build a distributed work-flow.
There are 4 independent hosts in this system.

- 2 host/producers deployed on local/laptop/virtual box
	- configured with DHCP server and subnetted to separate interfaces/IPs
- 2 hosts deployed on cloud (Chameleon) which will server as a multi-node kafka/event stream platform.
- 1 of the 2 cloud hosts will also act as a database end-point to store data provided by producers.

## Technologies
- OS - Ubuntu 20.04 
	- apt/dpkg package mgmt w/ ubunutu repositories
- python as the front-end/client language
- java runtime required for kafka
- apache kafka
- couchdb

## Cloud Provisioning
- create 2 new instances, based on of Ubuntu 20.04 image.
- create/assign RSA key pair
- add proper security group to instances (default + shared kafka/couchdb config)
- assign floating IPs to both instances
- ssh will be used (ex: "ssh -i /path/to/key cc@<floating.public.ip>")
- configuring ufw (Ubuntu's uncomplicated firewall)
	 - sudo ufw <status|enable|disable>
	 - sudo ufw allow from {trusted ips}

## Kafka installation/set-up

prerequisites:
install java and configure env variable to use IPv4
- sudo apt install default-jre -y
-  export KAFKA_OPTS="-Djava.net.preferIPv4Stack=True"

download/untar:
- wget https://dlcdn.apache.org/kafka/2.8.0/kafka_2.13-2.8.0.tgz
- tar -xvf kafka_2.13-2.8.0.tgz
- cd kafka_2.13-2.8.0

configuring kafka:
- nano config/server.properties

starting zookeeper (1 host) from kafka root dir
 - bin/zookeeper-server-start.sh config/zookeeper.properties &

starting kafka cluster (both cloud hosts) from kafka root dir
 - bin/kafka-server-start.sh config/server.properties &

checking running nodes:
- bin/zookeeper-shell.sh localhost:2181 ls /brokers/ids
- bin/zookeeper-shell.sh localhost:2181 get /brokers/ids/0
- bin/zookeeper-shell.sh localhost:2181 get /brokers/ids/1
