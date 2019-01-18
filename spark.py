from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import udf
import os
import sys

if __name__ == '__main__':
    spark = SparkSession.builder.appName("airMon").getOrCreate()

    # TODO: Change to get multiple csv data
    data2017 = spark\
        .read\
        .format("csv")\
        .options(header="true", inferSchema="true")\
        .load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/Beijing_2017_HourlyPM25_created20170803.csv"))

    def get_AQI_level(value):
        """calculate AQI

        :param value:
        :return: string
        """
        if 50 >= value >= 0:
            return "Good"
        elif 100 >= value >= 51:
            return "Moderate"
        elif 150 >= value >= 101:
            return "Unhealthy for Sensitive Groups"
        elif 200 >= value >= 151:
            return "Unhealthy"
        elif 300 >= value >= 201:
            return "Very Unhealthy"
        elif 500 >= value >= 301:
            return "Hazardous"
        elif value > 500:
            return "Extremely High Level"
        else:
            return None

    # Write an UDF for withColumn
    get_AQI_udf = udf(get_AQI_level, StringType())

    group2017 = data2017\
        .select("Year", "Month", "Day", "Hour", "Value", "QC Name")\
        .withColumn("AQI_Level", get_AQI_udf(data2017['Value']))\
        .groupBy("AQI_LEVEL")\
        .count()

    result2017 = group2017\
        .select("AQI_LEVEL", "count")\
        .withColumn("percent", group2017['count'] / data2017.count() * 100)\
        .selectExpr("AQI_LEVEL as aqi_level", "count", "percent")

    result2017\
        .write\
        .format("org.elasticsearch.spark.sql")\
        .option("es.nodes", "127.0.0.1:9200")\
        .mode("overwrite")\
        .save("weather2017/pm")

    spark.stop()