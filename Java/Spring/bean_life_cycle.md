# Spring Bean的生命周期管理

## 图示
![image](https://github.com/jaiminpan/misc-image/blob/master/memo/spring_life_cycle.png?raw=true)  

## BeanNameAware 接口
*让Bean对Name有知觉*
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
