# Client

## import data
```sh
# CSV FORMAT
cat qv_stock.csv | clickhouse-client --query="INSERT INTO stock FORMAT CSV";

# CSV FORMAT WITH HEADER
cat qv_stock.csv | clickhouse-client --query="INSERT INTO stock FORMAT CSVWithNames";
```
