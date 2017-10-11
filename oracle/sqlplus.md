
# Oracle Client

## Connect to Oracle using clinet

#### Install
```
oracle-instantclient12.2-basic-12.2.0.1.0-1.x86_64.rpm
oracle-instantclient12.2-sqlplus-12.2.0.1.0-1.x86_64.rpm
oracle-instantclient12.2-devel-12.2.0.1.0-1.x86_64.rpm
oracle-instantclient12.2-odbc-12.2.0.1.0-1.x86_64.rpm
```
It will install into `/usr/lib/oracle/12.2/client64`

#### Env
```
export ORACLE_HOME=/usr/lib/oracle/12.2/client64
export LD_LIBRARY_PATH=/usr/lib/oracle/12.2/client64/lib:$LD_LIBRARY_PATH
```

#### Prepare tnsnames.ora
Prepare tnsnames.ora. If the tnsnames.ora location is `/usr/lib/oracle/12.2/client64/network/admin/tnsnames.ora`  
```
export TNS_ADMIN=/usr/lib/oracle/12.2/client64/network/admin
```

** tnsnames.ora Sample **
```
ORA12 =  
 (DESCRIPTION =   
   (ADDRESS_LIST =  
     (ADDRESS = (PROTOCOL = TCP)(HOST = 127.0.0.1)(PORT = 1521))  
   )  
   (CONNECT_DATA =  
      (sid = orcl)
      (SERVER = DEDICATED)
   )
 )  
```

#### Connecting
Use following command to Connect oracle

```
$ORACLE_HOME/bin/sqlplus 'user/password@ORA12'
```


### Reference
http://www.xenialab.it/meo/web/white/oracle/HT_IC_RH.htm
