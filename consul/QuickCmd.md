# QuickCmd

### Office Guide
https://www.consul.io/api/agent/service.html

### Other Guide

## Agent
```
# list
curl http://localhost:8500/v1/agent/members

# check health
curl  http://localhost:8500/v1/agent/checks

# config
curl http://localhost:8500/v1/kv/commons/test/config?raw

```

## all Service
```
curl -s localhost:8500/v1/catalog/service/web

```


## agent Service
```
# register
curl -XPUT http://localhost:8500/v1/agent/service/register -d \
'{
  "ID": "myinst_id",
  "Name": "service_name",
  "Tags": [
    "primary",
    "v1"
  ],
  "Address": "127.0.0.1",
  "Port": 80,
  "EnableTagOverride": false,
  "Check": {
    "DeregisterCriticalServiceAfter": "12h",
    "HTTP": "http://localhost:5000/health",
    "Interval": "10s"
  }
}'

# delete
curl -s -XPUT localhost:8500/v1/agent/service/deregister/${SERVICE_ID}

# set check passing：
curl -s localhost:8500/v1/agent/check/pass/${SERVICE_ID}

# list critical service
curl -s localhost:8500/v1/health/state/critical | python -m json.tool

# maintenance
curl -s -XPUT "localhost:8500/v1/agent/service/maintenance/${SERVICE_ID}?enable=true&reason=deploy"

# maintenance resume
curl -s -XPUT "localhost:8500/v1/agent/service/maintenance/${SERVICE_ID}?enable=false"

```
