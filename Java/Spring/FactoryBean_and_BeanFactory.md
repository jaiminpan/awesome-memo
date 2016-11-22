# FactoryBean 和 BeanFactory 的区别

## BeanFacotry
**BeanFacotry是一个接口**，定义了 IOC 容器的最基本形式，并不是 IOC 容器的具体实现。
使用它来创建各种类型的Bean，最主要的方法就是getBean(String beanName)。
该方法从容器中返回特定名称的Bean，只不过其中有一种Bean是FacotryBean。如果这个Bean是一个FactoryBean,则把它生成的Bean返回，
否者直接返回Bean.

Spring 给出了很多种实现，如 DefaultListableBeanFactory、 XmlBeanFactory、 ApplicationContext 等，都是附加了某种功能的实现。

## FactoryBean
**FactoryBean是一种Bean**， 要想成为FacotryBean，必须实现FactoryBean 这个接口。
FactoryBean定义了三个接口方法：
* Object getObject(): 返回由FactoryBean创建的Bean的实例，如果isSingleton()方法返回true, 是单例的实例，该实例将放入Spring的缓冲池中
* boolean isSingleton(): 确定由FactoryBean创建的Bean的作用域scope是singleton还是prototype；
* getObjectType(): 返回FactoryBean创建的Bean的类型。


## 重要的事情再说一遍  
FactoryBean 是一直特殊的bean，它实际上也是一个工厂，我们在通过getBean(FactoryBeanName) 得到的Bean，是FacotryBean创建的Bean,
即它通过getObject()创建的Bean。

我们要想得到FactoryBean本身，必须通过&FactoryBeanName得到，即在BeanFactory中通过getBean(&FactoryBeanName)来得到 FactoryBean

在spring 中是通过 BeanFactoryUtils.isFactoryDereference() 来判断一个Bean是否是FactoryBean.
spring 内部实现中应该是在通过BeanFacotry 的getBean(String beanName) 来得到Bean时，如果这个Bean是一个FactoryBean,则把它生成的Bean返回，
否者直接返回Bean.


## 例子
```java
package com.test.factorybean;  
public class Car {
	private int maxSpeed;
	private String brand;
	private double price;
	public int getMaxSpeed() {
		return maxSpeed;
	}  
	public void setMaxSpeed(int maxSpeed) {
		this.maxSpeed = maxSpeed;  
	}  
	public String getBrand() {
		return brand ;  
	}  
	public void setBrand(String brand) {
		this.brand = brand;
	}  
	public double getPrice() {
		return price;
	}
	public void setPrice(double price) {
		this.price = price;  
	}
}
```
```java
package com.test.factorybean;
import org.springframework.beans.factory.FactoryBean;
public class CarFactoryBean implements FactoryBean<Car> {
	private tring carInfo;
	public Car getObject() throws Exception {
		Car car = new Car();
		String[] infos = carInfo.split(",");
		car.setBrand(infos[0]);
		car.setMaxSpeed(Integer.valueOf(infos[1]));
		car.setPrice(Double.valueOf(infos[2]));
		return car;
	}
	public Class<Car> getObjectType() {
		return Car.class;
	}
	public boolean isSingleton() {
		return false;
	}

	// 接受逗号分割符设置属性信息  
	public void setCarInfo(String carInfo) {
		carInfo = carInfo;
	}
	public String getCarInfo() {
		return carInfo;
	}
}
```
有了这个CarFactoryBean后，就可以在配置文件中使用下面这种自定义的配置方式配置Car Bean了：
```xml
<bean id="car" class="com.baobaotao.factorybean.CarFactoryBean" P:carInfo="法拉利,400,2000000"/>
```
当调用getBean("car") 时，Spring 通过反射机制发现`CarFactoryBean`实现了`FactoryBean`的接口，这时 Spring 容器就调用接口方法 `CarFactoryBean#getObject()` 方法返回。

如果希望获取 CarFactoryBean 的实例，则需要在使用 getBean(beanName) 方法时在 beanName 前显示的加上 "&" 前缀：如 getBean("&car");
