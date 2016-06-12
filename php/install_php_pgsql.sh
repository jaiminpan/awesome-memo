# php -i | grep postgres to check if postgres installed

PHP_VER="5.5.29"
 
# Check if extension exists first
php -m | grep pgsql
 
# Update brew and install requirements
brew update
brew install autoconf
 
# Download PHP source and extract
mkdir -p ~/src; cd ~/src
wget -c http://br1.php.net/distributions/php-$PHP_VER.tar.bz2
tar -xjf php-$PHP_VER.tar.bz2
 
# Go to extension dir and phpize
cd php-$PHP_VER/ext/pdo_pgsql/
phpize
 
# Configure for Postgress.app
# Use just "./configure" for brew version
./configure --with-pdo-pgsql="/Library/PostgreSQL/9.3/"
make
sudo make install
 
# Add extension to php.ini
sudo echo "extension=pdo_pgsql.so" >> /etc/php.ini
 
# Go to extension dir and phpize
cd php-$PHP_VER/ext/pgsql/
phpize
 
# Configure for Postgress.app
# Use just "./configure" for brew version
./configure --with-pgsql="/Library/PostgreSQL/9.3/"
make
sudo make install
 
# Add extension to php.ini
sudo echo "extension=pgsql.so" >> /etc/php.ini
 
# Check if extension exists, again
php -m | grep pgsql
