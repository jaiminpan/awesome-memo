# Profile

#### Profile in springboot


#### Profile in spring tomcat

In `Spring-applicationContext.xml`
```
	<beans profile="dev">
		<context:property-placeholder
				ignore-unresolvable="true"
				location="classpath:property/dev/jdbc.properties,
			classpath:property/dev/redis.properties"/>
	</beans>
	<beans profile="test">
		<context:property-placeholder
				ignore-unresolvable="true"
				location="classpath:property/test/jdbc.properties,
			classpath:property/test/redis.properties"/>
	</beans>
```

In `web.xml`
```
  <context-param>
    <param-name>spring.profiles.default</param-name>
    <param-value>dev</param-value>
  </context-param>
  <init-param>
      <param-name>profileEnable</param-name>
      <param-value>true</param-value>
  </init-param>
```
