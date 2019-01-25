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

## Service
```
# register
curl  --request PUT  --data @test.json http://localhost:8500/v1/agent/service/register

vi test.json
{
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
}

# delete
curl  --request PUT  http://localhost:8500/v1/agent/service/deregister/myinst_id

# set check passing：
curl http://localhost:8500/v1/agent/check/pass/myinst_id

```
