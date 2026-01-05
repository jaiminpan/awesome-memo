在/opt/plane目录新建以下三个文件：

docker-compose.yml

````
services:
  plane-web:
    image: makeplane/plane-frontend:v1.1.0
    environment:
      NEXT_PUBLIC_API_BASE_URL: ${API_URL}
    depends_on:
      - plane-api
    restart: unless-stopped

  plane-api:
    image: makeplane/plane-backend:v1.1.0
    environment:
      DATABASE_URL: ${DATABASE_URL}
      REDIS_URL: ${REDIS_URL}

      # Storage (S3)
      FILE_STORAGE_BACKEND: s3
      AWS_ACCESS_KEY_ID: ${AWS_ACCESS_KEY_ID}
      AWS_SECRET_ACCESS_KEY: ${AWS_SECRET_ACCESS_KEY}
      AWS_S3_BUCKET_NAME: ${AWS_S3_BUCKET_NAME}
      AWS_S3_REGION: ${AWS_S3_REGION}
      AWS_S3_ENDPOINT: ${AWS_S3_ENDPOINT}

      NEXTAUTH_SECRET: ${NEXTAUTH_SECRET}
      NEXTAUTH_URL: ${WEB_URL}
    ports:
      - "8000:8000"
    depends_on:
      - plane-migrator
    restart: unless-stopped

  plane-worker:
    image: makeplane/plane-backend:v1.1.0
    command: ["celery", "-A", "plane.celery_app", "worker", "--loglevel=info"]
    environment:
      DATABASE_URL: ${DATABASE_URL}
      REDIS_URL: ${REDIS_URL}
    depends_on:
      - plane-api
    restart: unless-stopped

  plane-scheduler:
    image: makeplane/plane-backend:v1.1.0
    command: ["celery", "-A", "plane.celery_app", "beat", "--loglevel=info"]
    environment:
      DATABASE_URL: ${DATABASE_URL}
      REDIS_URL: ${REDIS_URL}
    depends_on:
      - plane-api
    restart: unless-stopped

  plane-migrator:
    image: makeplane/plane-backend:v1.1.0
    command: ["python", "manage.py", "migrate"]
    environment:
      DATABASE_URL: ${DATABASE_URL}
    restart: "no"

  plane-db:
    image: postgres:14
    volumes:
      - ./pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: plane
      POSTGRES_PASSWORD: plane123
    networks:
      - plane-network

  plane-redis:
    image: redis:7
    volumes:
      - ./redisdata:/data
    networks:
      - plane-network

networks:
  plane-network:
    driver: bridge

````



````
nginx.conf

# ================================
# Upstreams
# ================================
upstream plane_web      { server 127.0.0.1:3000; }
upstream plane_space    { server 127.0.0.1:3000; }
upstream plane_admin    { server 127.0.0.1:3000; }
upstream plane_live     { server 127.0.0.1:3000; }
upstream plane_api      { server 127.0.0.1:8000; }
upstream plane_minio    { server 127.0.0.1:9000; }


# ================================
# Server
# ================================
server {
    listen 80;
    server_name ${SITE_ADDRESS};

    # 等价 Caddy request_body.max_size
    client_max_body_size ${FILE_SIZE_LIMIT};

    # 公共代理头（直接写在每个 location）
    # 也可放在 server{} 里，但某些 Nginx 版本不继承 upgrade，需要写在 location 中。

    # --------------------------------
    # /spaces/*
    # --------------------------------
    location /spaces/ {
        proxy_pass http://plane_space;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
    }

    # --------------------------------
    # /god-mode/*
    # --------------------------------
    location /god-mode/ {
        proxy_pass http://plane_admin;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
    }

    # --------------------------------
    # /live/*  (WebSocket heavy)
    # --------------------------------
    location /live/ {
        proxy_pass http://plane_live;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
    }

    # --------------------------------
    # /api/*
    # --------------------------------
    location /api/ {
        proxy_pass http://plane_api;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
    }

    # --------------------------------
    # /auth/*
    # --------------------------------
    location /auth/ {
        proxy_pass http://plane_api;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
    }

    # --------------------------------
    # /${BUCKET_NAME}/*
    # --------------------------------
    location /${BUCKET_NAME}/ {
        proxy_pass http://plane_minio;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
    }

    # --------------------------------
    # 默认路由 /* → web:3000
    # --------------------------------
    location / {
        proxy_pass http://plane_web;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
    }
}

# WebSocket upgrade 映射（必须要）
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}

````

cat .env
````
API_URL=http://your-domain.com/api
WEB_URL=http://your-domain.com

# DATABASE_URL: postgres://plane:plane123@plane-db:5432/plane
# REDIS_URL: redis://plane-redis:6379/

DATABASE_URL=postgres://plane:plane123@172.31.32.62:5432/plane
REDIS_URL=redis://172.31.32.62:6379/0

USE_MINIO=0
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx
AWS_S3_BUCKET_NAME=plane
AWS_S3_REGION=ap-east-1
AWS_S3_ENDPOINT=https://s3.amazonaws.com

NEXTAUTH_SECRET=your-random-secret
````
