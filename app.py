from __future__ import print_function

import pyspark.sql.functions as f

import spark_utils
from idstostix import prototypes
from idstostix.rdd_utils import df_from_rdd
from idstostix.stix_utils import to_observable

if __name__ == "__main__":
    spark = spark_utils.get_spark_session()

    spark.sparkContext.setLogLevel("ERROR")

    snort_df = spark.read.json("data/snort.txt")
    snort_df.printSchema()

    snort_df_group = snort_df.groupBy("src_ip", "src_port", "dest_ip", "dst_port", "protocol") \
        .agg(f.min("timestamp").alias("first_observed"),
             f.max("timestamp").alias("last_observed"),
             f.count(f.lit(1)).alias("number_observed"))

    snort_rdd = snort_df_group.collect()

    # menggunakan cara native tapi lebih cepat
    rdd = []
    for r in snort_rdd:
        rdd.append(to_observable(r))

    # rdd = snort_ds_group.rdd.map(lambda r: to_observable(r))
    df = df_from_rdd(rdd, prototypes.observable_prototype, spark)
    df.show(truncate=False, vertical=True)

    # write data
    df.coalesce(1).write.format("json").mode("overwrite").save('data/observable.txt')

    spark.stop()
