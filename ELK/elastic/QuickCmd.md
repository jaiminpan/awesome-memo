# Quick Cmd

### 查看元数据
```sh
curl 10.10.158.23:9200/_cat/indices?v

curl /uni:goods?pretty
curl -H "Content-Type: application/json" -XGET /uni:goods?pretty
```

### 查询索引
```sh

curl -H "Content-Type: application/json" -XPOST /goodsidx_latest/_search -d \
'{
  "query": {
    "match": { "accId": "126262", "name": "大象" }
  }
'}

curl -H "Content-Type: application/json" -XPOST /goodsidx_latest/_search?routing=126262 -d \
'{
  "query": {
    "bool": {
        "must":     { "match": { "uniname": "大象" }},
        "filter":   { "term": { "accId" : "126262"} }
    }
  }
}'

```

### 创建
```sh
# create idx 
curl -H "Content-Type: application/json" -XPUT /goodsidx_latest -d \
'{
  "settings": {
    "index": {
      "number_of_shards": 32,
      "number_of_replicas": 0,
      "routing_partition_size": 1,
      "refresh_interval": -1  // 不落盘，数据准备推荐
    },
    "analysis": {
      "tokenizer": {
        "ngram_tokenizer": {
          "type": "nGram",
          "min_gram": 4,
          "max_gram": 8,
          "token_chars": [
            "letter",
            "digit"
          ]
        }
      },
      "analyzer": {
        "ngram_tokenizer_analyzer": {
          "type": "custom",
          "tokenizer": "ngram_tokenizer",
          "filter": [
            "lowercase"
          ]
        },
        "ik_pinyin_analyzer": {
          "type": "custom",
          "tokenizer": "ik_max_word",
          "filter": "pinyin_filter"
        }
      },
      "filter": {
        "pinyin_filter": {
          "type": "pinyin",
          "keep_first_letter": true,
          "keep_separate_first_letter": false,
          "keep_full_pinyin": true,
          "keep_original": false,
          "limit_first_letter_length": 10,
          "lowercase": true,
          "remove_duplicated_term": true
        }
      }
    }
  }
}'

# create mapping
curl -H "Content-Type: application/json" -XPUT /goodsidx_latest/_mapping/goodstype -d \
'{
    "properties" : {
      "gid" : {
        "type" : "keyword"
      },
      "accid" : {
        "type" : "keyword"
      },
      "classtrace" : {
        "type" : "keyword"
      },
      "platstats" : {
        "type" : "keyword"
      },
      "barcode" : {
        "type" : "keyword",
        "copy_to": "mixcodekey"
      },
      "mixcodekey" : {
        "type" : "text",
        "store": false,
        "analyzer" : "ngram_tokenizer_analyzer",
        "search_analyzer": "standard"
      },
      "name" : {
        "type" : "text",
        "index": false,
        "copy_to": "mixnamekey"
      },
      "skuattr" : {
        "type" : "text",
        "index": false,
        "copy_to": "mixnamekey"
      },
      "mixnamekey": {
        "type": "text",
        "store": false,
        "analyzer" : "ik_pinyin_analyzer"
      }
    }
}'

### alias
curl -H "Content-Type: application/json" -XPOST /_aliases -d \
'{
  "actions": [{
      "add": {
        "index": "uni:goods_202002", // 原有索引
        "alias": "uni:goods" // 服务的别名
      }
  }]
}'

curl -H "Content-Type: application/json" -XPOST /_aliases -d \
'{
  "actions": [{"add": {
    "index": "uni:goods_202002",
    "alias": "uni:goods"
  }}, {"remove": {
    "index": "uni:goods_20200215",
    "alias": "uni:goods"
  }}]
}'

```


### 设置副本和落盘时间间隔
```sh
curl -H "Content-Type: application/json" -XPUT /goodsidx_latest/_settings -d \
'{
  "index" : {
    "number_of_replicas" : 2,
    "refresh_interval": "3s"
  }
}'
```


### Reindex
```sh
curl -H "Content-Type: application/json" -XPOST /_reindex?wait_for_completion=false -d \
'{
  "source": {
    "index": "unigoodsidx",
    "size": 5000
  },
  "dest": {
    "index": "uni:goodsidx"
  },
    "script": {
    "inline": "ctx._routing = ctx._source.accId"
  }
}'

### 查看
curl -H "Content-Type: application/json" -XGET /_tasks/[taskid]

```

### analyze 测试
```sh
curl -H "Content-Type: application/json" -XPOST /goodsidx_latest/_analyze -d \
'{
  "analyzer": "ngram_tokenizer_analyzer",
  "text":"08871特 殊67354xy814"
}'

curl -H "Content-Type: application/json" -XPOST /goodsidx_latest/_analyze -d \
'{
  "analyzer": "ngram_tokenizer_analyzer",
  "text":"08 87 1特 殊67 35 4x y814"
}'
```

### 删除索引
```sh
curl -XDELETE  /goodsidx_latest
```

### 删除doc
```sh
## Routing当创建index的时候如果指定了routing，那么在删除的时候要同时指定文档的id和routing，如果routing不匹配，光是id匹配也不会删除
curl -H "Content-Type: application/json" -XDELETE /goodsidx_latest/[type]/[id]

```
