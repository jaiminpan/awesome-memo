# 内网打通

公网节点
```
version: '3.8'

services:
  easytier-node-a:
    image: easytier/easytier:latest
    container_name: easytier-a
    network_mode: host
    
    cap_add:
      - NET_ADMIN
    restart: always
    # 这里的 command 对应容器内执行的 easytier 命令参数
    volumes:
      - /dev/net/tun:/dev/net/tun
      - /etc/machine-id:/etc/machine-id:ro
      - /data/appdatas/tier/config:/config
    command: >
      -c /config/config.toml
```

#### config.toml
```
instance_name = "easytier"
instance_id = "fbd1061e-2194-4ccf-949b-aa16ab89d318"
dhcp = true
listeners = [
    "tcp://0.0.0.0:11010",
    "udp://0.0.0.0:11010",
    "wg://0.0.0.0:11010",
]
ipv4 = "10.14.14.1"  # 你的虚拟IP（可选）

[network_identity]
network_name = "easytier-net"
network_secret = "w0VYFACSrRvo09bzvkdQ"

[flags]

[[peer]]
uri = "tcp://13.13.13.13:11010"

```

### 内网节点
```
version: '3.8'

services:
  easytier-node-b:
    image: easytier/easytier:latest
    container_name: easytier-b
    network_mode: host
    cap_add:
      - NET_ADMIN
    restart: always
    # 将 <节点A的IP> 替换为节点 A 实际的公网 IP 或局域网 IP
    volumes:
      - /dev/net/tun:/dev/net/tun
      - /etc/machine-id:/etc/machine-id:ro
      - /data/appdatas/tier/config:/config
    command: >
      -c /config/config.toml
```

#### config.toml
```
instance_name = "easytier"
instance_id = "24faf01a-f6f4-4bf1-bb22-1337cd2fd9e9"
ipv4 = "10.14.14.2"  # 你的虚拟IP（可选）
[network_identity]
network_name = "easytier-net"
network_secret = "w0VYFACSrRvo09bzvkdQ"

[flags]

[[peer]]
uri = "tcp://13.13.13.13:11010"
```

