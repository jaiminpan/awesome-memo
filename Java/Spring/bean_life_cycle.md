# Spring Bean的生命周期管理

## 图示
![image](https://github.com/jaiminpan/misc-image/blob/master/memo/spring_life_cycle.png?raw=true)  

## BeanNameAware 接口
**让Bean对Name有知觉**

Spring Bean存活于容器之中，一般情况下spring bean对context的情况并不了解，
如果希望某个bean知道自己在context中的代号：bean name，通过实现BeanNameAware接口即可。

实现：，接口中就一个方法setBeanName()
```java
public class LogginBean implements BeanNameAware {
  private String beanName = null;
  public void setBeanName(String beanName) {
    this.beanName = beanName;
  }
}
```
beanName就是一个bean在容器中的id，如下，则beanName对应为logging
```xml
<bean id="logging" class="xxx.xxx.LogginBean"></bean>
```
运行时的源码位置: invokeAwareMethods in [AbstractAutowireCapableBeanFactory.java][code_AbstractAutowireCapableBeanFactory]

## BeanFactoryAware 接口
**让Bean对Factory有知觉**

让Bean获取配置他们的BeanFactory的引用。
使用上与BeanNameAware接口无异，只不过BeanFactoryAware注入的是个工厂，BeanNameAware注入的是个Bean的名字。
让bean获取配置自己的工厂之后，当然可以在Bean中使用这个工厂的getBean()方法，
但是，实际上非常不推荐这样做，因为结果是进一步加大Bean与Spring的耦合，而且，能通过DI注入进来的尽量通过DI来注入。

当然，除了查找bean，BeanFactory可以提供大量其他的功能，例如
* destroySingletons: 销毁singleton模式的Bean
* preInstantiateSingletons(): 立即实例化所有的Bean实例

#### 其它
preInstantiateSingletons方法本身的目的是让Spring立即处理工厂中所有Bean的定义，并且将这些Bean全部实例化。
因为Spring默认实例化Bean的情况下，采用的是lazy机制，换言之，如果不通过getBean()方法（BeanFactory或者ApplicationContext的方法）获取Bean的话，那么为了节省内存将不实例话Bean，只有在Bean被调用的时候才实例化他们。

运行时的源码位置: invokeAwareMethods in [AbstractAutowireCapableBeanFactory.java][code_AbstractAutowireCapableBeanFactory]


## BeanPostProcessor接口
BeanPostProcessor接口则可以提供全局的、定制多个bean的初始化过程。(对应其它xxxAware接口的作用是定制单个bean的初始化过程)

BeanPostProcessor接口有两个方法
* postProcessBeforeInitialization:在bean的属性值设置之前执行
* postProcessAfterInitialization:在bean的属性值设置之后执行


## InitializingBean接口
如果希望在bean的属性值被设置之后还想做点工作，则可以考虑让这个bean实现InitializingBean接口。
InitializingBean接口中，唯一的afterPropertiesSet()接口可以实现所需要的工作。

注意，如果同时在配置文件指定init-method，调用顺序如下


调用顺序
* postProcessBeforeInitialization()
* _**afterPropertiesSet()**_
* _**[init-method]**_
* postProcessAfterInitialization()

例子：
```xml
<bean id="example" class="xxx.xxx.Example" init-method="initMethod"></bean>
```
```
public class Example implements ApplicationContextAware, InitializingBean {
    private ApplicationContext context;

    @Autowired
    private Map<String, IBusinessProcessor> processorMap;

    @Override
    public void setApplicationContext(ApplicationContext applicationContext) throws BeansException {
      this.context = applicationContext;
    }

    @Override
    public void afterPropertiesSet() throws Exception {
         //在该函数执行之前，这个bean的所有属性的值就都设置好了，包括processMap。
         //do something with processMap
    }
}
```
运行时的源码位置：invokeInitMethods in [AbstractAutowireCapableBeanFactory.java][code_AbstractAutowireCapableBeanFactory]



## 整个例子

```java
@Component  
public class DemoBean implements BeanFactoryAware, BeanNameAware,  
                                  InitializingBean, DisposableBean {  
    @PostConstruct  
    public void postConstruct() {  
       System.out.println("DemoBean: postConstruct-method");  
    }
    public void init() {  
       System.out.println("DemoBean: init-method");  
    }  
    public void destroy() throws Exception {  
       System.out.println("DemoBean: destroy-method!");  
    }  
    public void afterPropertiesSet() throws Exception {  
       System.out.println("DemoBean: after properties set!");  
    }  
    public void setBeanName(String name) {  
       System.out.println("DemoBean: beanName aware, [name=" + name + "]");  
    }  
    public void setBeanFactory(BeanFactory beanFactory) throws BeansException {  
       System.out.println("DemoBean: beanFactory aware");  
    }  
}

@Component  
public class DemoBeanPostProcessor implements BeanPostProcessor {  
    public Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException {  
       System.out.println("DemoBeanPostProcessor: post process before initialization, [beanName=" + beanName + ", bean=" + bean + "]");  
       return bean;  
    }  
    public Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException {  
       System.out.println("DemoBeanPostProcessor: post process after initialization, [beanName=" + beanName + ", bean=" + bean + "]");  
       return bean;  
    }  
}  
```
输出
```
DemoBean: beanName aware, [name=demoBean]
DemoBean: beanFactory aware
DemoBean: postConstruct
DemoBeanPostProcessor: post process before initialization, [beanName=demoBean, bean=com.shansun.multidemo.spring.lifecycle.DemoBean@1deeb40]
DemoBean: after properties set!
## if configurate init-method
## DemoBean: init-method
DemoBeanPostProcessor: post process after initialization, [beanName=demoBean, bean=com.shansun.multidemo.spring.lifecycle.DemoBean@1deeb40]

```
相应的源码位置: initializeBean in [AbstractAutowireCapableBeanFactory.java][code_AbstractAutowireCapableBeanFactory]



[code_AbstractAutowireCapableBeanFactory]: https://github.com/spring-projects/spring-framework/blob/master/spring-beans/src/main/java/org/springframework/beans/factory/support/AbstractAutowireCapableBeanFactory.java

