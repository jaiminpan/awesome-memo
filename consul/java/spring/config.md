Spring Cloud Consul 配置

### 核心参数
| 配置项                      | 默认值    |
| :-------------------------- | --------- |
| spring.cloud.consul.enabled | true      |
| spring.cloud.consul.host    | localhost |
| spring.cloud.consul.port    | 8500      |


	

### 服务发现参数
| 配置项                                                       | 默认值                   |
| ------------------------------------------------------------ | ------------------------ |
| spring.cloud.consul.discovery.acl-token                      |                          |
| spring.cloud.consul.discovery.catalog-services-watch-delay   | 10                       |
| spring.cloud.consul.discovery.catalog-services-watch-timeout | 2                        |
| spring.cloud.consul.discovery.datacenters                    |                          |
| spring.cloud.consul.discovery.default-query-tag              |                          |
| spring.cloud.consul.discovery.default-zone-metadata-name     | zone                     |
| spring.cloud.consul.discovery.deregister                     | true                     |
| spring.cloud.consul.discovery.enabled                        | true                     |
| spring.cloud.consul.discovery.fail-fast                      | true                     |
| spring.cloud.consul.discovery.health-check-critical-timeout  |                          |
| spring.cloud.consul.discovery.health-check-interval          | 10s                      |
| spring.cloud.consul.discovery.health-check-path              | /actuator/health         |
| spring.cloud.consul.discovery.health-check-timeout           |                          |
| spring.cloud.consul.discovery.health-check-tls-skip-verify   |                          |
| spring.cloud.consul.discovery.health-check-url               |                          |
| spring.cloud.consul.discovery.heartbeat.enabled              | false                    |
| spring.cloud.consul.discovery.heartbeat.interval-ratio       |                          |
| spring.cloud.consul.discovery.heartbeat.ttl-unit             | s                        |
| spring.cloud.consul.discovery.heartbeat.ttl-value            | 30                       |
| spring.cloud.consul.discovery.hostname                       |                          |
| spring.cloud.consul.discovery.instance-group                 |                          |
| spring.cloud.consul.discovery.instance-id                    | 默认为服务名+环境+端口号 |
| spring.cloud.consul.discovery.instance-zone                  |                          |
| spring.cloud.consul.discovery.ip-address                     |                          |
| spring.cloud.consul.discovery.lifecycle.enabled              | true                     |
| spring.cloud.consul.discovery.management-port                |                          |
| spring.cloud.consul.discovery.management-suffix              | management               |
| spring.cloud.consul.discovery.management-tags                |                          |
| spring.cloud.consul.discovery.port                           |                          |
| spring.cloud.consul.discovery.prefer-agent-address           | false                    |
| spring.cloud.consul.discovery.prefer-ip-address              | false                    |
| spring.cloud.consul.discovery.query-passing                  | false                    |
| spring.cloud.consul.discovery.register                       | true                     |
| spring.cloud.consul.discovery.register-health-check          | true                     |
| spring.cloud.consul.discovery.scheme                         | http                     |
| spring.cloud.consul.discovery.server-list-query-tags         |                          |
| spring.cloud.consul.discovery.service-name                   |                          |
| spring.cloud.consul.discovery.tags                           |                          |



### 配置服务参数
| 配置项                                       | 默认值                             |      |
| -------------------------------------------- | ---------------------------------- | ---- |
| spring.cloud.consul.config.enabled           | true                               |      |
| spring.cloud.consul.config.prefix            | config                             |      |
| spring.cloud.consul.config.default-context   | application                        |      |
| spring.cloud.consul.config.profile-separator | ,                                  |      |
| spring.cloud.consul.config.data-key          | data                               |      |
| spring.cloud.consul.config.format            | KEY_VALUE, PROPERTIES, YAML, FILES |      |
| spring.cloud.consul.config.name              | ${spring.application.name}         |      |
| spring.cloud.consul.config.acl-token         |                                    |      |
| spring.cloud.consul.config.fail-fast         | false                              |      |
| spring.cloud.consul.config.watch.enabled     | true                               |      |
| spring.cloud.consul.config.watch.wait-time   | 55                                 |      |
| spring.cloud.consul.config.watch.delay       | 1000                               |      |


