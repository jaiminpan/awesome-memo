# Using System Variables

Reference: 
* https://docs.oracle.com/javase/tutorial/essential/environment/sysprop.html
* https://docs.oracle.com/javase/8/docs/api/java/lang/System.html

## In Code

#### System.getenv()
```
public static Map<String,String> getenv()
```
> https://docs.oracle.com/javase/8/docs/api/java/lang/System.html#getenv--  
> Returns an unmodifiable string map view of the **current system environment**.   

#### System.getProperties()
```
public static Properties getProperties()
```
> https://docs.oracle.com/javase/8/docs/api/java/lang/System.html#getProperties--  
> Determines the **current system properties**.  


## In Spring
* https://docs.spring.io/autorepo/docs/spring-framework/4.2.x/javadoc-api/org/springframework/core/env/StandardEnvironment.html

#### System.getenv()
* `{systemEnvironment['ENV_VARIABLE_NAME']}`

You can supply app.environment varialble as,
* environment varilable: export ENV_VARIABLE_NAME=DEV

#### System.getProperties()
* `#{systemProperties['yourkey']}`
* `#{systemProperties.yourkey}`

sample
```
<bean id="yourBean" class="com.company.YourBean">
    <property name="environment" value="#{systemProperties['app.environment'] }"/>
    <!-- other properties goes here....-->
</bean>
```

You can supply app.environment varialble as,
* commandline param:  java -Dapp.environment=DEV ....
 
