# Environment


## Custom Env
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

## Without Spring Env
```java
public static void initialization(String path) throws IOException {

	Properties properties = new Properties()

	try (InputStream resourceAsStream = getPropertyStream(path); //
			InputStreamReader inputstreamreader = new InputStreamReader(resourceAsStream, charset);) {
		properties.load(inputstreamreader);
	}

	properties.forEach((k, v) -> {
		LOGGER.info(k + "=" + v);
	});
}
```
