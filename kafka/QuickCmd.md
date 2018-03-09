
# QuickCmd

## Basic
```
# start kafka
bin/kafka-server-start.sh -daemon config/server.properties

# stop kafka
bin/kafka-server-stop.sh
```

## Topics
```
# List existing topics
bin/kafka-topics.sh --zookeeper localhost:2181 --list

# Describe all topics
bin/kafka-topics.sh --zookeeper localhost:2181 --describe

# Describe a topic
bin/kafka-topics.sh --zookeeper localhost:2181 --describe --topic my_topic

# Create topic
bin/kafka-topics.sh --zookeeper localhost:2181 --create --replication-factor 1 --partitions 1 --topic my_topic

# Delete topic
bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic my_topic

# Increase partition for topic (can not decrease)
bin/kafka-topics.sh --zookeeper localhost:2181 --alter --topic my_topic --partitions 10

# (Deprecated) add retention to 6 hours  (unit:ms)
bin/kafka-topics.sh --zookeeper localhost:2181 --alter --topic my_topic --config retention.ms=21600000

# (Current) add retention to (unit:ms)
bin/kafka-configs.sh --zookeeper localhost:2181 --alter --entity-type topics --entity-name my_topic --add-config retention.ms=21600000
# Note: The default retention time is 24 hours (86400000 millis).

# remove retention
bin/kafka-topics.sh --zookeeper localhost:2181 --alter --topic mytopic --delete-config retention.ms
```

## Producer & Consumer
```
# kafka producer
bin/kafka-console-producer.sh --broker-list localhost:9092 --topic my_topic
bin/kafka-console-producer.sh --broker-list localhost:9092 --topic my_topic < file.log

# (old) kafka consumer
bin/kafka-console-consumer.sh --zookeeper localhost:2181 --topic my_topic --from-beginning
# (new) kafka consumer
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic my_topic --from-beginning

# reassign replica for topic
bin/kafka-reassign-partitions.sh --zookeeper localhost:2181 --reassignment-json-file custom-reassignment.json --execute

# cat custom-reassignment.json
{
   "version": 1,
   "partitions": [
       {
           "topic": "test0",
           "partition": 0,
           "replicas": [1,2]
       },
       {
           "topic": "test0",
           "partition": 1,
           "replicas": [1,2,3]
       },
       {
           "topic": "test0",
           "partition": 2,
           "replicas": [1,2,3]
       }
    ]
}

bin/kafka-reassign-partitions.sh --zookeeper localhost:2181 --reassignment-json-file custom-reassignment.json --verify
```

## Message & Offset
```
# Get number of messages in a topic
bin/kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list localhost:9092 --topic my_topic --time -1 \
 --offsets 1 | awk -F ":" '{sum += $3} END {print sum}'
 
# Get the latest offset still in a topic
bin/kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list localhost:9092 --topic my_topic --time -1

# Get the earliest offset still in a topic
bin/kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list localhost:9092 --topic my_topic --time -2
```

## Kafka Consumer Groups
```
# List the consumer groups known to Kafka
bin/kafka-consumer-groups.sh --zookeeper localhost:2181 --list (old api)
bin/kafka-consumer-groups.sh --new-consumer --bootstrap-server localhost:9092 --list (new api)

bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group test-consumer-group

# View the details of a consumer group
bin/kafka-consumer-groups.sh --zookeeper localhost:2181 --describe --group <group name>

# lookup offset position of consumer group per partition
bin/kafka-consumer-offset-checker.sh --zookeeper localhost:2181 --group {group-id} --topic {topic} 
bin/kafka-run-class.sh kafka.tools.ConsumerOffsetChecker --zookeeper localhost:2181 --group {group-id} --topic my_topic 
```

## kafka-run-class
```
# make down broker
bin/kafka-run-class.sh kafka.admin.ShutdownBroker --zookeeper localhost:2181 --broker 0 --num.retries 3 --retry.interval.ms 60

# delete topic
bin/kafka-run-class.sh kafka.admin.DeleteTopicCommand --zookeeper localhost:2181 --topic my_topic
```

## Config
```
# describe config of topic
bin/kafka-configs.sh --zookeeper localhost:2181 --describe --entity-type topics --entity-name my_topic
```
