# Zipkin

## Base
Base on
```
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.1.2.RELEASE</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>
```

## pom.xml

```
    <properties>
        <spring-cloud.version>Greenwich.SR2</spring-cloud.version>
    </properties>

    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-zipkin</artifactId>
    </dependency>
    <!-- for kafka support -->
    <dependency>
        <groupId>org.springframework.kafka</groupId>
        <artifactId>spring-kafka</artifactId>
    </dependency>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-dependencies</artifactId>
                <version>${spring-cloud.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>
```

## Property
```
#设置采样比例为1.0。默认是0.1
spring.sleuth.enabled=true
spring.sleuth.sampler.probability=1.0
spring.sleuth.hystrix.strategy.enabled=true

#Zipkin服务器
spring.zipkin.enabled=true
#spring.zipkin.sender.type=web # default value
spring.zipkin.base-url=http://zipkin:9411

<!-- for kafka support -->
#spring.zipkin.sender.type=kafka
#spring.zipkin.kafka.topic=zipkin

#spring.kafka.bootstrap-servers=10.10.99.211:9092,10.10.21.68:9092,10.10.87.0:9092
#spring.kafka.producer.batch-size=1000
#spring.kafka.producer.key-serializer=org.apache.kafka.common.serialization.StringSerializer
#spring.kafka.producer.value-serializer=org.apache.kafka.common.serialization.StringSerializer
```

# Zipkin Server

## OpenZipkin

https://github.com/openzipkin/zipkin

Download zipkin-server-2.12.9-exec.jar

cat startup.sh
```
#!/bin/bash

export KAFKA_BOOTSTRAP_SERVERS=xx.xx.xx.xx:9092,xx.xx.xx.yy:9092
#export KAFKA_GROUP_ID=zipkin
export KAFKA_TOPIC=zipkin
export KAFKA_STREAMS=2

export STORAGE_TYPE=elasticsearch
export ES_INDEX=zipkin
export ES_HOSTS=127.0.0.1:9200

nohup java -jar zipkin-server-2.12.9-exec.jar >> /data/applogs/zipkin/zipkin.log 2>&1  &
```



