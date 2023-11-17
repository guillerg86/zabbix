## Template Elastic Cluster By HTTP Lite

This template checks Health of Status using curl

```
curl -k -s https://user:password@SERVER:PORT/_cluster/health
```

This command will return something like


```
{
  "cluster_name": "elasticsearch",
  "status": "yellow",
  "timed_out": false,
  "number_of_nodes": 1,
  "number_of_data_nodes": 1,
  "active_primary_shards": 323,
  "active_shards": 323,
  "relocating_shards": 0,
  "initializing_shards": 0,
  "unassigned_shards": 254,
  "delayed_unassigned_shards": 0,
  "number_of_pending_tasks": 0,
  "number_of_in_flight_fetch": 0,
  "task_max_waiting_in_queue_millis": 0,
  "active_shards_percent_as_number": 55.97920277296361
}
```

### Macros

|MACRO|EXAMPLE|DESCRIPTION|
|-|-|
|{$ELASTIC_HOST}|siem.mydomain.com|Hostname, FQDN or IP of your server|
|{$ELASTIC_PORT}|9200|Port of ElasticSearch server|
|{$ELASTIC_PROTO}|https|Protocol (http, https) of Elastic server|