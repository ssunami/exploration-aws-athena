##
from pyspark.sql import SparkSession
from pyspark.sql.functions import col,countDistinct, concat_ws
from pyspark import SparkContext
import sys
from pyspark.sql import functions as F
##
if len(sys.argv) != 4:
    print("Usage: METCS777-term-paper-code-sample-1-Team19.py <csv_file_path> <output_dir_1> <output_dir_2>",file=sys.stderr)
    exit(-1)
##
sc = SparkContext.getOrCreate()
spark = SparkSession.builder.appName("TaxiData").getOrCreate()
# df_raw = spark.read.csv('A5/taxi-data-sorted-small.csv.bz2')
df_raw = spark.read.csv(sys.argv[1])
##
df_float = df_raw.withColumn("_c4", col("_c4").cast("float")) \
    .withColumn("_c5", col("_c5").cast("float")) \
    .withColumn("_c11", col("_c11").cast("float")) \
    .withColumn("_c12", col("_c12").cast("float")) \
    .withColumn("_c16", col("_c16").cast("float"))
df_filtered = df_float.filter(
    (col("_c4").isNotNull()) & (col("_c4") != 0) &
    (col("_c5").isNotNull()) & (col("_c5") != 0) &
    (col("_c11").isNotNull()) & (col("_c11") != 0) &
    (col("_c12").isNotNull()) & (col("_c12") != 0) &
    (col("_c16").isNotNull()) & (col("_c16") != 0)
)
# print(df_filtered.count())
##
df = df_filtered
##
# task 1: find the top 10 
df_task_1 = df.select(col("_c0").alias("medallion"), col("_c1").alias("driver_id"))
driver_counts = df_task_1.groupBy("medallion").agg(countDistinct("driver_id").alias("driver_count"))
# Order by the unique driver count in descending order and take the top 10
top_medallions = driver_counts.orderBy(col("driver_count").desc()).limit(10)
# Show the results
# top_medallions.show()
top_medallions_str = top_medallions.select(concat_ws(", ", "medallion", "driver_count").alias("combined"))
top_medallions_str.coalesce(1).write.format("text").option("header", "false").save(sys.argv[2])
##
df_task_2 = df.select(col("_c4").alias("trip_time_in_secs"))
# Create the 4 categories of 'duration' based on 'trip_time_in_secs'
duration_categories_df = df_task_2.withColumn(
    'duration',
    F.when(F.col('trip_time_in_secs') < 600, 'Less than 10 mins')
     .when((F.col('trip_time_in_secs') >= 600) & (F.col('trip_time_in_secs') < 1200), '10 to 20 mins')
     .when((F.col('trip_time_in_secs') >= 1200) & (F.col('trip_time_in_secs') < 1800), '20 to 30 mins')
     .otherwise('More than 30 mins')
)

# Group by the 'duration', count the number of trips
trip_counts_by_duration_df = duration_categories_df.groupBy('duration').count().orderBy('duration')

# Show the results
# trip_counts_by_duration_df.show()
trip_counts_by_duration_df_str = trip_counts_by_duration_df.select(concat_ws(", ", "duration", "count").alias("combined"))
trip_counts_by_duration_df_str.coalesce(1).write.format("text").option("header", "false").save(sys.argv[3])
##
sc.stop()
##

