#### 单机
version: '3.8'
services:
  quickstart:
    image: starrocks/allin1-ubuntu:3.5.9
    container_name: quickstart
    restart: unless-stopped
    ports:
      - "9030:9030"
      - "8030:8030"
      - "8040:8040"
