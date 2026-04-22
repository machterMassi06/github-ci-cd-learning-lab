from pyspark.sql import SparkSession


def get_spark_session():
    """
    Create Spark session for MiniFinkBroker tests and pipeline.
    """
    return SparkSession.builder \
        .master("local[*]") \
        .appName("MiniFinkBroker") \
        .getOrCreate()