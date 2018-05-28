# SpringBoot Application Property Files

[Application Property Files](https://docs.spring.io/spring-boot/docs/current-SNAPSHOT/reference/htmlsingle/#boot-features-external-config-application-property-files)


SpringApplication loads properties from application.properties files in the following locations and adds them to the Spring Environment:
* A /config subdirectory of the current directory
* The current directory
* A classpath /config package
* The classpath root
The list is ordered by precedence (properties defined in locations higher in the list override those defined in lower locations).

Summary is 
* `file:./config/`
* `file:./`
* `classpath:/config/`
* `classpath:/`

### Use --spring.config.location 
```
$ java -jar myproject.jar --spring.config.location=classpath:/default.properties,classpath:/override.properties
```
