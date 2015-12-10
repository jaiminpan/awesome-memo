Python
-----------

Install in manaul
---------
1. wget https://www.python.org/ftp/python/2.7.8/Python-2.7.8.tgz

  ```sh
  tar xf Python-2.7.7.tgz
  cd Python-2.7.7
  ./configure --prefix=/usr/local
  make && make install
  ls /usr/local/bin/python2.7
  ```
2. setuptools + pip

  ```sh
  # First get the setup script for Setuptools:
  wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
  
  # Then install it for Python 2.7 :
  python2.7 ez_setup.py
  
  # Now install pip using the newly installed setuptools:
  easy_install-2.7 pip
  
  # With pip installed you can now do things like this:
  pip2.7 install [packagename]
  pip2.7 install --upgrade [packagename]
  pip2.7 uninstall [packagename]
  ```
