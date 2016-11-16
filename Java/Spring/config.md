# Spring Config

## Standalone Application use spring
```java
public static void main(String[] args) throws Exception {

	final AbstractApplicationContext context =
			new ClassPathXmlApplicationContext("classpath:META-INF/spring/integration/stateless-retry-advice-context.xml");

	context.registerShutdownHook();

	LOGGER.info("\n========================================================="
			  + "\n    Demo will terminate in 60 seconds.                    "
			  + "\n=========================================================" );

	Thread.sleep(60000);
	context.close();
}
 
```

```java
public static void main(String[] args) throws Exception {

	final AbstractApplicationContext context =
			new ClassPathXmlApplicationContext("classpath:META-INF/spring/integration/circuit-breaker-advice-context.xml");

	context.registerShutdownHook();

  PagerDutyBridgeService service = (PagerDutyBridgeService) context.getBean("pagerDutyBridgeService");
	LOGGER.info("\n========================================================="
			  + "\n    Demo will terminate in 2 minutes.                     "
			  + "\n=========================================================" );

	Thread.sleep(120000);
	context.close();
}
```


## Web Application use spring

```xml
# web.xml

<web-app>
	<context-param>
		<param-name>contextConfigLocation</param-name>
		<param-value>/WEB-INF/applicationContext.xml</param-value>
		<!-- 
		<param-value>
			classpath*:config/spring/appcontext-*.xml
			classpath*:config/spring/common/appcontext-*.xml
		</param-value>
		-->
	</context-param>
	<listener>
		<listener-class>
			org.springframework.web.context.ContextLoaderListener
		</listener-class>
	</listener>
	<servlet>
	<servlet-name>sampleServlet</servlet-name>
	<servlet-class>
		org.springframework.web.servlet.DispatcherServlet
	</servlet-class>
	</servlet>

...
</web-app>
```


## spring xml
```
<beans>
	<bean id="course" class="demo.Course">
		<property name="module" ref="module"/>
  	</bean>
	
	<bean id="module" class="demo.Module">
		<property name="assignment" ref="assignment"/>
  	</bean>
	
	<bean id="assignment" class="demo.Assignment" />
</beans>
```

#### Reference

* http://www.programcreek.com/java-api-examples/index.php?api=org.springframework.context.support.AbstractApplicationContext  
* https://www.ibm.com/developerworks/cn/webservices/ws-springjava/  
