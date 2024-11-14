# Nextcloud

A safe home for all your data

## Install On CentOS

### Prepare
```
yum -y install epel-release
```

#### nginx
```
yum -y install nginx
```

#### php、 php-fpm

```sh
# add PHP7 repository
rpm -Uvh https://mirror.webtatic.com/yum/el7/webtatic-release.rpm

yum -y install php70w-mbstring php70w-gd php70w-mcrypt php70w-mysql 

# check php
php --version

# Other Nextcloud needed
yum -y install php70w-cliphp70w-pear php70w-xml  php70w-pdo php70w-json php70w-pecl-apcu php70w-pecl-apcu-devel

yum install php70w-fpm
```

[More Reference for installing php](https://github.com/jaiminpan/awesome-memo/blob/master/php/install.md)

#### php-fpm config
```
vi /etc/php-fpm.d/www.conf

## user = nginx   (change)
## group = nginx  (change)

# Uncomment Following
## env[HOSTNAME] = $HOSTNAME
## env[PATH] = /usr/local/bin:/usr/bin:/bin
## env[TMP] = /tmp
## env[TMPDIR] = /tmp
## env[TEMP] = /tmp
```

```
cd /var/lib/php
chown nginx:nginx -R /var/lib/php/*
```

#### Postgres
[More Reference for installing Postgres](https://github.com/jaiminpan/awesome-memo/blob/master/PostgreSQL/install.md)

### Install Nextcloud

#### For SSL certification
```
mkdir -p /etc/nginx/cert/

openssl req -new -x509 -days 365 -nodes -out /etc/nginx/cert/nextcloud.crt -keyout /etc/nginx/cert/nextcloud.key

chmod 700 /etc/nginx/cert
chmod 600 /etc/nginx/cert/*
```
#### Nextcloud
Download Nextcloud 

https://github.com/nextcloud/server/releases  
OR  
https://nextcloud.com/install/#instructions-server 
OR  
wget https://download.nextcloud.com/server/releases/nextcloud-12.0.4.zip

Sample as nextcloud-12.0.4.zip
```
unzip nextcloud-12.0.4.zip
mv nextcloud /data/

cd /data/
mkdir -p nextcloud/data
chown nginx:nginx -R nextcloud
```

Config nginx for Nextcloud
```
upstream php-handler {
    server 127.0.0.1:9000;
    #server unix:/var/run/php5-fpm.sock;
}

# enforce https
server {
    listen 80;
    server_name cloud.example.com;
    return 307 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name cloud.example.com;

    ssl_certificate /etc/nginx/cert/nextcloud.crt;
    ssl_certificate_key /etc/nginx/cert/nextcloud.key;

    # Add headers to serve security related headers
    # Before enabling Strict-Transport-Security headers please read into this
    # topic first.
    # add_header Strict-Transport-Security "max-age=15768000;
    # includeSubDomains; preload;";
    #
    # WARNING: Only add the preload option once you read about
    # the consequences in https://hstspreload.org/. This option
    # will add the domain to a hardcoded list that is shipped
    # in all major browsers and getting removed from this list
    # could take several months.
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header X-Robots-Tag none;
    add_header X-Download-Options noopen;
    add_header X-Permitted-Cross-Domain-Policies none;

    # Path to the root of your installation
    root /var/www/nextcloud/;

    location = /robots.txt {
        allow all;
        log_not_found off;
        access_log off;
    }

    # The following 2 rules are only needed for the user_webfinger app.
    # Uncomment it if you're planning to use this app.
    #rewrite ^/.well-known/host-meta /public.php?service=host-meta last;
    #rewrite ^/.well-known/host-meta.json /public.php?service=host-meta-json
    # last;

    location = /.well-known/carddav {
      return 301 $scheme://$host/remote.php/dav;
    }
    location = /.well-known/caldav {
      return 301 $scheme://$host/remote.php/dav;
    }

    # set max upload size
    client_max_body_size 512M;
    fastcgi_buffers 64 4K;

    # Enable gzip but do not remove ETag headers
    gzip on;
    gzip_vary on;
    gzip_comp_level 4;
    gzip_min_length 256;
    gzip_proxied expired no-cache no-store private no_last_modified no_etag auth;
    gzip_types application/atom+xml application/javascript application/json application/ld+json application/manifest+json application/rss+xml application/vnd.geo+json application/vnd.ms-fontobject application/x-font-ttf application/x-web-app-manifest+json application/xhtml+xml application/xml font/opentype image/bmp image/svg+xml image/x-icon text/cache-manifest text/css text/plain text/vcard text/vnd.rim.location.xloc text/vtt text/x-component text/x-cross-domain-policy;

    # Uncomment if your server is build with the ngx_pagespeed module
    # This module is currently not supported.
    #pagespeed off;

    location / {
        rewrite ^ /index.php$uri;
    }

    location ~ ^/(?:build|tests|config|lib|3rdparty|templates|data)/ {
        deny all;
    }
    location ~ ^/(?:\.|autotest|occ|issue|indie|db_|console) {
        deny all;
    }

    location ~ ^/(?:index|remote|public|cron|core/ajax/update|status|ocs/v[12]|updater/.+|ocs-provider/.+)\.php(?:$|/) {
        fastcgi_split_path_info ^(.+\.php)(/.*)$;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param PATH_INFO $fastcgi_path_info;
        fastcgi_param HTTPS on;
        #Avoid sending the security headers twice
        fastcgi_param modHeadersAvailable true;
        fastcgi_param front_controller_active true;
        fastcgi_pass php-handler;
        fastcgi_intercept_errors on;
        fastcgi_request_buffering off;
    }

    location ~ ^/(?:updater|ocs-provider)(?:$|/) {
        try_files $uri/ =404;
        index index.php;
    }

    # Adding the cache control header for js and css files
    # Make sure it is BELOW the PHP block
    location ~ \.(?:css|js|woff|svg|gif)$ {
        try_files $uri /index.php$uri$is_args$args;
        add_header Cache-Control "public, max-age=15778463";
        # Add headers to serve security related headers (It is intended to
        # have those duplicated to the ones above)
        # Before enabling Strict-Transport-Security headers please read into
        # this topic first.
        # add_header Strict-Transport-Security "max-age=15768000; includeSubDomains; preload;";
        #
        # WARNING: Only add the preload option once you read about
        # the consequences in https://hstspreload.org/. This option
        # will add the domain to a hardcoded list that is shipped
        # in all major browsers and getting removed from this list
        # could take several months.
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header X-Robots-Tag none;
        add_header X-Download-Options noopen;
        add_header X-Permitted-Cross-Domain-Policies none;
        # Optional: Don't log access to assets
        access_log off;
    }

    location ~ \.(?:png|html|ttf|ico|jpg|jpeg)$ {
        try_files $uri /index.php$uri$is_args$args;
        # Optional: Don't log access to other assets
        access_log off;
    }
}
```

Reference https://docs.nextcloud.com/server/12/admin_manual/installation/nginx.html

#### Start Visit
http://[your server ip address]/




