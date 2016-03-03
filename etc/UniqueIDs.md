Sharding & IDs
---------------

http://instagram-engineering.tumblr.com/post/10853187575/sharding-ids-at-instagram


#### Each of our IDs consists of:

* 41 bits for time in milliseconds (gives us 41 years of IDs with a custom epoch)
* 13 bits that represent the logical shard ID (max shards id: 2^13 = 8192)
* 10 bits that represent an auto-incrementing sequence, modulus 1024 (2^10 = 1024). This means we can generate 1024 IDs, per shard, per millisecond

#### Example:

1. time id:  
  1387263000 = September 9th, 2011, at 5:00pm  
  milliseconds since the beginning of our epoch (defined January 1st, 2011)  
  `id = 1387263000 << (64-41)`

2. shard id:  
  user ID: 31341, logical shards: 2000, 31341 % 2000 -> 1341  
  `id |= 1341 << (64-41-13)`  

3. seq id:  
  generated 5000 IDs for this table already; next value is 5001  
  `id |= (5001 % 1024)`

### Here’s the PL/PGSQL that accomplishes all this (for an example schema insta5):
```plpgsql
CREATE SCHEMA insta5;
CREATE SEQUENCE table_id_seq;

CREATE OR REPLACE FUNCTION insta5.next_id(OUT result bigint) AS $$
DECLARE
    our_epoch bigint := 1314220021721;
    seq_id bigint;
    now_millis bigint;
    shard_id int := 5;
BEGIN
    SELECT nextval('insta5.table_id_seq') % 1024 INTO seq_id;

    SELECT FLOOR(EXTRACT(EPOCH FROM clock_timestamp()) * 1000) INTO now_millis;
    result := (now_millis - our_epoch) << 23;
    result := result | (shard_id << 10);
    result := result | (seq_id);
END;
$$ LANGUAGE PLPGSQL;

CREATE TABLE insta5.our_table (
    "id" bigint NOT NULL DEFAULT insta5.next_id(),
    ...rest of table schema...
)
```
