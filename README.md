<h1 align="center">
  <img src="https://img.icons8.com/color/96/000000/air-quality.png">
  <br>
  <strong>airMon<strong>
</h1>

<div align="center">
  <p>An air quality monitor using Spark, Elasticsearch, Kibana, Azkaban.</p>
</div>

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

## Sample

<img width="969" alt="air-quality-monitor" src="https://user-images.githubusercontent.com/29159357/51418460-99507a80-1b51-11e9-9c73-82492423ae14.png">

## How to run

You can use `spark-submit` to submit the work in shell.
```bash
$ <Spark root>/bin/spark-submit --master local[2] --jars <project root>/library/elasticsearch-spark-20_2.11-6.5.4.jar <project root>/spark.py
```

Or you can upload the work and run it on Azkaban, before that you should make sure the Azkaban is running in the local machine.

 
 <a href="https://icons8.com/icon/13263/air-quality" style="display:none;">Air Quality icon by Icons8</a>