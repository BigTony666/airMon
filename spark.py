from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import udf
import os


def acquire_data(raw_files, spark):

    _read_file = lambda raw_file: spark \
        .read \
        .format("csv") \
        .options(header="true", inferSchema="true") \
        .load(os.path.join(rootPath, "data/{fileName}".format(fileName=raw_file)))

    return [('-'.join(raw_file.lower().split('_', maxsplit=2)[:2]), _read_file(raw_file)) for raw_file in raw_files]


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


def cook_data(raw_datas):

    def _cook_data(_raw_data):
        _group_data = _raw_data \
            .select("Year", "Month", "Day", "Hour", "Value", "QC Name") \
            .withColumn("AQI_Level", get_AQI_udf(_raw_data['Value'])) \
            .groupBy("AQI_LEVEL") \
            .count()

        return _group_data \
            .select("AQI_LEVEL", "count") \
            .withColumn("percent", _group_data['count'] / _raw_data.count() * 100) \
            .selectExpr("AQI_LEVEL as aqi_level", "count", "percent")

    return [(_raw_data[0], _cook_data(_raw_data[1])) for _raw_data in raw_datas]


def write_data(cooked_datas):
    for cooked_data in cooked_datas:

        cooked_data[1] \
            .write \
            .format("org.elasticsearch.spark.sql") \
            .option("es.nodes", "127.0.0.1:9200") \
            .mode("overwrite") \
            .save("weather_{0}/pm".format(cooked_data[0]))


if __name__ == '__main__':
    spark = SparkSession.builder.appName("airMon").getOrCreate()

    rootPath = os.path.dirname(os.path.abspath(__file__))

    files = os.listdir(os.path.join(rootPath, "data"))

    write_data(cook_data(acquire_data(files, spark)))

    spark.stop()
