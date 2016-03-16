Python
-----------

Install in manaul
---------
### Install Python
  wget https://www.python.org/ftp/python/2.7.8/Python-2.7.8.tgz

  ```sh
    tar xf Python-2.7.7.tgz
    cd Python-2.7.7
    ./configure --prefix=/usr/local
    make && make install
    ls /usr/local/bin/python2.7
  ```
### Install setuptools + pip

  1. setuptools

    ```
      > wget https://bootstrap.pypa.io/ez_setup.py -O - | python
    ```
    For more to reference: https://pypi.python.org/pypi/setuptools
  2. pip
  
    Download from https://pypi.python.org/pypi/pip#download  
    ```
      # tar -xzvf pip-x.x.x.tar.gz
      # cd pip-x.x.x
      # python setup.py install
    ```
    For more to reference: https://pypi.python.org/pypi/pip
  3. After Installed

    ```
      # With pip installed you can now do things like this:
      pip install [packagename]
      pip install --upgrade [packagename]
      pip uninstall [packagename]
    ```
