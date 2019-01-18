<div align="center">
  <strong>airMon<strong>
</div>

An air quality monitor using Spark, Elasticsearch, Kibana, Azkaban.

## Spark

[Spark](https://spark.apache.org/) is a unified analytics engine for large-scale data processing. We
use Spark to analyze raw data.

Make sure the project environment involves **pyspark** and **py4j**.
 
## Elasticsearch

[Elasticsearch](https://www.elastic.co/products/elasticsearch) is a distributed, RESTful search and analytics engine capable of solving a growing number of use cases.

Download the Elasticsearch and run locally, the default standalone endpoint is `localhost:9200`.

## Kibana

[Kibana](https://www.elastic.co/products/kibana) is a visualization tool that helps us to visualize the ElasticSearch data.

Download the Kibana and run locally, the default standalone endpoint is `localhost:5601`.

## Azkaban

[Azkaban](https://azkaban.github.io/) is a batch workflow job scheduler created at LinkedIn to run Hadoop jobs.

Instead of submitting spark work by ourselves in shell, we can choose to use Azkaban to schedule the work in a more efficient way.

Download the Azkaban and run locally, the default standalone endpoint is `localhost:8081`

## How to run

You can use `spark-submit` to submit the work in shell.
```bash
$ <Spark root>/bin/spark-submit --master local[2] --jars <project root>/library/elasticsearch-spark-20_2.11-6.5.4.jar <project root>/spark.py
```

Or you can upload the work and run it on Azkaban, before that you should make sure the Azkaban is running in the local machine.

