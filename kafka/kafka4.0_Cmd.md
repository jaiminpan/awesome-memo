kafka4.0 Cmd

# 查看
./kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group game_detail

# 列出所有 Consumer Groups（User Groups）
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list


```
bin/kafka-consumer-groups.sh \
  --bootstrap-server <BROKER_ADDRESS> \
  --group <CONSUMER_GROUP_ID> \
  --reset-offsets \
  --topic <TOPIC_NAME> \
  --to-earliest | --to-latest | --to-offset <OFFSET> | --shift-by <N> \
  --execute
```

# 重置到最新（跳过未消费消息）
bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --group my-consumer-group \
  --topic my-topic \
  --reset-offsets \
  --to-latest \
  --execute

bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --group game_detail \
  --topic admin_game_detail \
  --reset-offsets \
  --to-latest \
  --execute
 