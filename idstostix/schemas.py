import pyspark.sql.types as pst

observable_schema = pst.StructType([
    pst.StructField("created", pst.StringType(), True),
    pst.StructField("first_observed", pst.StringType(), True),
    pst.StructField("id", pst.StringType(), True),
    pst.StructField("last_observed", pst.StringType(), True),
    pst.StructField("modified", pst.StringType(), True),
    pst.StructField("number_observed", pst.LongType(), True),
    pst.StructField("objects", pst.StructType([
        pst.StructField("0", pst.StructType([
            pst.StructField("type", pst.StringType(), True),
            pst.StructField("value", pst.StringType(), True)
        ]), True),
        pst.StructField("1", pst.StructType([
            pst.StructField("type", pst.StringType(), True),
            pst.StructField("value", pst.StringType(), True)
        ]), True),
        pst.StructField("2", pst.StructType([
            pst.StructField("dst_port", pst.LongType(), True),
            pst.StructField("dst_ref", pst.StringType(), True),
            pst.StructField("protocols", pst.ArrayType(pst.StringType(), True), True),
            pst.StructField("src_port", pst.LongType(), True),
            pst.StructField("src_ref", pst.StringType(), True),
            pst.StructField("type", pst.StringType(), True)
        ]), True)
    ]), True),
    pst.StructField("type", pst.StringType(), True)
])
