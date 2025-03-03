import findspark
from pyspark.sql import SparkSession


findspark.init()

spark = SparkSession.builder \
    .appName("MeteoAnalysis") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://localhost:9000") \
    .config("spark.hadoop.fs.s3a.access.key", "minio") \
    .config("spark.hadoop.fs.s3a.secret.key", "password") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .getOrCreate()

df = spark.read.json("s3a://meteo/meteo_20250303_025724.json")

df.show()
