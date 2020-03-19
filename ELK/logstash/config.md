
## Logstash

vi logstash.yml
```
input {
  file {
    path => "/var/log/test.log"
    start_position => "beginning"
    codec => multiline {             # 使用codec/multiline插件
      pattern => "^%{TIMESTAMP_ISO8601}"    # 指定匹配的表达式
      negate => true                 # 是否匹配到
      what => "previous"             # 可选previous或next, previous是合并到匹配的上一行末尾
      max_lines => 1000              # 最大允许的行
      max_bytes => "10MiB"           # 允许的大小
      auto_flush_interval => 30      # 如果在规定时候内没有新的日志事件就不等待后面的日志事件
    }
    
  }
}
```

### test config
```
input {
  stdin {}
}

filter {
  grok {
    match => { "message" => "%{TIMESTAMP_ISO8601:logtime} %{USERNAME:appname},%{USERNAME:traceid},%{USERNAME:spanid} %{LOGLEVEL:loglevel} %{USERNAME:thread} %{JAVACLASS:logclass} - %{JAVALOGMESSAGE:message}" }
  }
  geoip {
    source => "clientip"
  }
}

output {
  stdout {
    codec => rubydebug
  }
}
```

### practice filebeat config

For log Pattern `[%d{yyyy-MM-dd HH:mm:ss.SSS}][${spring.application.name:-},%X{X-B3-TraceId:-},%X{X-B3-SpanId:-}] %level %thread %logger{32}:%line - %msg%n`

```
input {
  beats {
    port => 5044
  }
}

filter {
  grok {
    match => { "message" => "\[%{TIMESTAMP_ISO8601:logtime}\]\[%{USERNAME:appname}?,%{USERNAME:traceid}?,%{USERNAME:spanid}?\] %{LOGLEVEL:loglevel} (?<thread>[0-9a-zA-Z.+-_$#@]+) (?<logclass>[0-9a-zA-Z.]+:[0-9]+) - %{JAVALOGMESSAGE:message}" }
  }
  geoip {
    source => "clientip"
  }
}

output {
  elasticsearch {
    hosts => ["http://127.0.0.1:9200"]
    index => "log-main-%{+YYYY.MM.dd}"
    # index in weekly
    # index => "applog-main-%{+xxxx.ww}"
    #user => "elastic"
    #password => "changeme"
  }
}

```


## filebeat

cat filebeat.yml
```
# for log multiline meld to pervious
multiline.pattern: ^\[[0-9]{4}-[0-9]{2}-[0-9]{2}
multiline.negate: true
multiline.match: after
multiline.timeout: 30s

output.logstash.hosts: ["10.10.xx.xx:5044"]

logging.to_files: true
logging.files:
  path: /data/applogs/filebeat
  name: filebeat
  keepfiles: 7
  permissions: 0644
```
