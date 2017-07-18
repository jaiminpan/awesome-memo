# install package

#### Sample

Install `RPostgreSQL` package in default foler.
```
[root@localhost]# R

> install.packages("RPostgreSQL")
```

Install `RPostgreSQL` in to `/lib64/R/library/` folder
```
[root@localhost]# R

> install.packages("RPostgreSQL", "/lib64/R/library/")
```

## trouble shoot

if file missing for include or library. Please use 
```
# sample as pgsql
ln -s /usr/pgsql/include /usr/local/include/pgsql
# and 
ln -s /usr/pgsql/lib /usr/local/lib/pgsql

```
