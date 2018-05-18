# Environment


#### Custom Env
```java
// configname = "application-uat.properties";
private Environment customEnv(String configname) throws Exception {
	Resource resource = new ClassPathResource(configname);
	Properties props = PropertiesLoaderUtils.loadProperties(resource);
		
	StandardEnvironment stdenv = new StandardEnvironment();
	stdenv.getPropertySources().addLast(new PropertiesPropertySource(configname, props));
	return stdenv;
}
```
