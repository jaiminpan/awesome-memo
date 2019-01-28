# Hystrix

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
+        <dependency>
+            <groupId>org.springframework.cloud</groupId>
+            <artifactId>spring-cloud-starter-netflix-hystrix</artifactId>
+        </dependency>
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

## application.properties
```
# default is false
+feign.hystrix.enabled=true
```

## Code
```
+
+import org.springframework.stereotype.Component;
+
+@Component
+public class XXXHystrix implements XXClient {


```

```
package xxxx.feign;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.stereotype.Component;
import org.springframework.web.bind.annotation.*;

-@FeignClient(value = "ServiceName", path = "/ContextPath")
+@FeignClient(value = "ServiceName", path = "/ContextPath", fallback = XXXHystrix.class)
public interface XXClient {
.....
}

public class ProcListenerStart {
+       @Autowired
+       private XXXClient client;
+ ....

}
```

