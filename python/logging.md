# Logging

Refference:  
https://docs.python.org/2/howto/logging.html  
https://docs.python.org/2/howto/logging-cookbook.html  
https://docs.python.org/2/library/logging.html  

#### Example
```
FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT)
d = {'clientip': '192.168.0.1', 'user': 'fbloggs'}
logger = logging.getLogger('tcpserver')
logger.warning('Protocol problem: %s', 'connection reset', extra=d)
```
