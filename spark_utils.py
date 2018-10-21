from pyspark.sql import SparkSession


def get_spark_session():
    session = SparkSession \
        .builder \
        .master("local[6]") \
        .appName("Ids to STIX") \
        .config("spark.ui.enabled", True) \
        .config("spark.sql.warehouse.dir", "file:///C:/temp") \
        .getOrCreate()

    return session
