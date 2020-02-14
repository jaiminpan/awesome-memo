
# QuickCmd

## Basic
```

```

## Topics

```sh

bin/pulsar-admin namespaces get-backlog-quotas test-tenant/standalone/test-ns


bin/pulsar-admin namespaces set-backlog-quota test-tenant/standalone/test-ns --limit 1k --policy producer_exception
```

## Producer & Consumer

```sh
### comsumer subscriptions
bin/pulsar-admin  --admin-url http://10.0.xx.xx:8080/  topics subscriptions  topic_name

### comsumer unsubscribe
bin/pulsar-admin  --admin-url http://10.0.xx.xx:8080/  topics unsubscribe  -s my_comsumer_name  topic_name

```


## Lession & learn

Q: Found Log
```
 pulsar write failed
org.apache.pulsar.client.api.PulsarClientException$TimeoutException: Could not send message to broker within given timeout
```
after Restart
```
Found Exception: Cannot create producer on topic with backlog quota exceeded
```
A: Delete Unused consumer which block the message dead.