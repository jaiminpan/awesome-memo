# Server


## pom.xml

```
    <properties>
        <spring-cloud.version>Finchley.RELEASE</spring-cloud.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-consul-discovery</artifactId>
        </dependency>
    </dependencies>

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

## Code
Add @EnableDiscoveryClient
```
@EnableDiscoveryClient
@SpringBootApplication
public class XXXApplication {
	public static void main(String[] args) {
		SpringApplication.run(XXXApplication.class, args);
	}
}

```

## application.properties
```
management.server.servlet.context-path=actuator
management.endpoint.health.show-details=always
#management.health.redis.enabled=false

spring.cloud.consul.enabled=true
spring.cloud.consul.host=10.81.xx.xxx
spring.cloud.consul.port=8500
spring.cloud.consul.discovery.enabled=true
#spring.cloud.consul.discovery.register=true
spring.cloud.consul.discovery.service-name=${spring.application.name}
spring.cloud.consul.discovery.instance-id=${spring.application.name}-${spring.cloud.client.ip-address}-${server.port}
spring.cloud.consul.discovery.prefer-ip-address=true
#spring.cloud.consul.discovery.hostname=${spring.cloud.client.ip-address}
#spring.cloud.consul.discovery.port=${server.port}
spring.cloud.consul.discovery.healthCheckPath=${server.servlet.context-path}/${management.server.servlet.context-path}/health
spring.cloud.consul.discovery.healthCheckInterval=15s
#spring.cloud.consul.discovery.tags=urlprefix-/${spring.cloud.consul.discovery.service-name}
#spring.cloud.consul.discovery.deregister=true

```

