from __future__ import print_function

import spark_utils
from idstostix import prototypes
from idstostix.rdd_utils import df_from_rdd
from idstostix.stix_utils import to_indicator

if __name__ == '__main__':
    spark = spark_utils.get_spark_session()
    indicator_df = spark.read.json("data/observable.txt")
    indicator_rdd = indicator_df.collect()

    rdd = []
    for r in indicator_rdd:
        rdd.append(to_indicator(r))

    df = df_from_rdd(rdd, prototypes.indicator_prototype, spark)
    df.printSchema()
    df.show(truncate=False, vertical=True)
    df.coalesce(1).write.format("json").mode("overwrite").save('data/indicator.txt')

    spark.stop()
