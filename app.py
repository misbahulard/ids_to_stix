from __future__ import print_function

import pyspark.sql.functions as f

import spark_utils
from idstostix import prototypes
from idstostix.rdd_utils import df_from_rdd
from idstostix.stix_utils import to_observable, to_indicator, to_identity

if __name__ == "__main__":
    spark = spark_utils.get_spark_session()

    spark.sparkContext.setLogLevel("ERROR")

    snort_df = spark.read.json("data/part-00000-143f4dec-d31d-4449-9510-4086bd77fa69-c000.json")
    # snort_df.printSchema()

    snort_df_group = snort_df.groupBy("src_ip", "src_port", "dest_ip", "dest_port", "protocol") \
        .agg(f.min("ts").alias("first_observed"),
             f.max("ts").alias("last_observed"),
             f.count(f.lit(1)).alias("number_observed")).cache()

    # snort_df_group.printSchema()

    rdd_observable = snort_df_group.rdd.map(lambda r: to_observable(r))
    df_observable = df_from_rdd(rdd_observable, prototypes.observable_prototype, spark)
    df_observable.show(truncate=False, vertical=True)

    rdd_indicator = rdd_observable.map(lambda r: to_indicator(r))
    df_indicator = df_from_rdd(rdd_indicator, prototypes.indicator_prototype, spark)
    df_indicator.show(truncate=False, vertical=True)

    rdd_identity = rdd_observable.map(lambda r: to_identity(r))
    df_identity = df_from_rdd(rdd_identity, prototypes.identity_prototype, spark)
    df_identity.show(truncate=False, vertical=True)

    # write data
    # df.write.format("json").mode("overwrite").save('data/observable.txt')

    spark.stop()
