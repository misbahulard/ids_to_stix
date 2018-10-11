from pyspark.sql import SparkSession

if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .master("local[*]") \
        .appName("IdsToStix") \
        .config("spark.ui.enabled", True) \
        .config("spark.sql.warehouse.dir", "file:///C:/temp") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")

    snort_ds = spark.read.parquet("observable.parquet")
    snort_ds.printSchema()
    snort_ds.show()

    spark.stop()
