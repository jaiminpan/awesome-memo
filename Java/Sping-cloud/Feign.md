# Feign

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
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-openfeign</artifactId>
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
```
+import org.springframework.cloud.openfeign.EnableFeignClients;

+@EnableFeignClients
@EnableDiscoveryClient
@SpringBootApplication
public class XXXApplication {
	public static void main(String[] args) {
		SpringApplication.run(XXXApplication.class, args);
	}
}

```

```
package xxxx.feign;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.stereotype.Component;
import org.springframework.web.bind.annotation.*;

@FeignClient(value = "ServiceName", path = "/ContextPath")
public interface XXClient {

       @PostMapping(value = "/send/{id}")
       public String send(@PathVariable("id") String id;
}

public class ProcListenerStart {
+       @Autowired
+       private XXXClient client;
+ ....
}
```

