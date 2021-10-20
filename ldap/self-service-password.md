# self-service-password

[github](https://github.com/ltb-project/self-service-password)
[Document](https://ltb-project.org/documentation/self-service-password)


### Download
wget https://github.com/ltb-project/self-service-password/archive/v1.3.tar.gz

### pre-instal
php and etc


###

vim /PATH-TO/self-service-password/conf/config.inc.php
```sh
$ldap_url = "ldap://172.xx.xx.xx:389";
$ldap_starttls = false;
$ldap_binddn = "cn=admin,dc=xxxx,dc=com";
$ldap_bindpw = "****";
$ldap_base = "dc=xxxx,dc=com";
$ldap_login_attribute = "uid";
$ldap_fullname_attribute = "cn";
$ldap_filter = "(&(objectClass=person)($ldap_login_attribute={login}))";
$mail_from = "msg_data@xxxx.com";
$mail_from_name = "Self Service Password";
$mail_signature = "";

$notify_on_change = true;
 https://github.com/PHPMailer/PHPMailer)
$mail_sendmailpath = '/usr/sbin/sendmail';
$mail_protocol = 'smtp';
$mail_smtp_debug = 0;
$mail_debug_format = 'html';
$mail_smtp_host = 'localhost';
$mail_smtp_auth = true;
$mail_smtp_user = 'msg_data@xxxxx.com';
$mail_smtp_pass = 'xxxxx';
$mail_smtp_port = 25;

keyphrase = "secret";
```

### nginx.conf

[nginx/self-service-password/1.3](https://ltb-project.org/documentation/self-service-password/1.3/config_nginx)

```sh
server {
    listen 80;

    root /var/www/html;
    index index.php index.html index.htm;

    # Make site accessible from http://localhost/
    server_name _;

    # Disable sendfile as per https://docs.vagrantup.com/v2/synced-folders/virtualbox.html
    sendfile off;

    gzip on;
    gzip_comp_level 6;
    gzip_min_length 1000;
    gzip_types text/plain text/css application/json application/x-javascript text/xml application/xml application/xml+rss text/javascript application/javascript text/x-js;
    gzip_vary on;
    gzip_proxied any;
    gzip_disable "MSIE [1-6]\.(?!.*SV1)";

    # Add stdout logging
    error_log /dev/stdout warn;
    access_log /dev/stdout main;

    # pass the PHP scripts to FastCGI server listening on socket
    location ~ \.php {
        fastcgi_pass unix:/var/run/php-fpm.socket;
        fastcgi_split_path_info       ^(.+\.php)(/.+)$;
        fastcgi_param PATH_INFO       $fastcgi_path_info;
        fastcgi_param PATH_TRANSLATED $document_root$fastcgi_path_info;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_index index.php;
        try_files $fastcgi_script_name =404;
        fastcgi_read_timeout 600;
        include fastcgi_params;
    }

    error_page 404 /404.html;
    location = /404.html {
        root /usr/share/nginx/html;
        internal;
    }

    # deny access to . files, for security
    location ~ /\. {
        log_not_found off; 
        deny all;
    }

    location ~ /scripts {
        log_not_found off; 
        deny all;
    }
}
```



