# Filter

ES中filter的用法有两种，一种是filted query，如下
1.
```json
{
  "query":{
    "filtered":{
      "query":{
        "term":{"title":"kitchen3"}
      },
      "filter":{
        "term":{"price":1000}
      }
    }
  }
}
```
这种方式已经deprecated了，可以通过boolQuery实现。
2.
```json
{
  "query": {
    "bool": {
      "must": {
        "term": {
          "term":{"title":"kitchen3"}
        }
      },
      "filter": {
        "term": {
          "price":1000
        }
      }
    }
  }
}
```

另一种是直接放在根目录：
3.
```json
{
  "query":{
    "term":{"title":"kitchen3"}
  },
  "filter":{
    "term":{"price":1000}
  }
}
```

### 区别
根目录中的filter(**3**)在query后执行。在filter query先执行filter(**2**)，不计算score，再执行query。
如果还要在搜索结果中执行aggregation操作，filter query(**2**)聚合的是filter和query之后的结果，而filter(**3**)聚合的是query的结果。


https://stackoverflow.com/questions/28958882/elasticsearch-filtered-query-vs-filter

