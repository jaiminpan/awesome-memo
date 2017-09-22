# Monitor


## KafkaOffsetMonitor
[github](https://github.com/quantifind/KafkaOffsetMonitor)

### Running
Download then run
```sh
java -cp KafkaOffsetMonitor-assembly-0.2.1.jar \
     com.quantifind.kafka.offsetapp.OffsetGetterWeb \
     --zk zk-server1,zk-server2 \
     --port 8080 \
     --refresh 10.seconds \
     --retain 7.days
```

### Problem
It's slow to visit the index.html because it use google cdn.
Fix it by
1. `jar xvf KafkaOffsetMonitor-assembly-0.2.1.jar` to directory `package`
2. modify `package/offsetapp/index.html`

Origin
```xml
<script src="//ajax.googleapis.com/ajax/libs/angularjs/1.2.9/angular.js"></script>
	<script src="//ajax.googleapis.com/ajax/libs/angularjs/1.2.9/angular-route.js"></script>
	<script src="//ajax.googleapis.com/ajax/libs/angularjs/1.2.9/angular-resource.js"></script>
```
Fixed
```xml
<script src="//cdn.bootcss.com/angular.js/1.2.9/angular.min.js"></script>
	<script src="//cdn.bootcss.com/angular.js/1.2.9/angular-route.min.js"></script>
	<script src="//cdn.bootcss.com/angular.js/1.2.9/angular-resource.min.js"></script>
```

3. `jar cvf myKafkaOffsetMonitor.jar -C package/ .`

