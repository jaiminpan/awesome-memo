# Client

## Base
Base on 
```
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.0.5.RELEASE</version>
        <relativePath/> <!-- lookup parent from repository -->
    </parent>
```

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
spring.cloud.consul.enabled=true
spring.cloud.consul.host=10.81.xx.xxx
spring.cloud.consul.port=8500
spring.cloud.consul.discovery.enabled=false
```

## Code Sample
```
package xxx;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cloud.client.discovery.DiscoveryClient;
import org.springframework.cloud.client.loadbalancer.LoadBalancerClient;
import org.springframework.stereotype.Service;

@Service
public class ServiceDiscovery {
    @Autowired
    private LoadBalancerClient loadBalancer;

    @Autowired
    private DiscoveryClient discoveryClient;

    /**
     * 从所有服务中选择一个服务（轮询）
     */
    public Object discover(String serviceid) {
        return loadBalancer.choose(serviceid).getUri().toString();
    }

    /**
     * 获取所有服务
     */
    public Object services(String serviceid) {
        return discoveryClient.getInstances(serviceid);
    }
}

```


