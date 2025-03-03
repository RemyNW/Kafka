from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, FloatType, TimestampType
from pyspark.sql.functions import col, to_timestamp


# Create a SparkSession
spark = SparkSession.builder \
    .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
    .getOrCreate()

# Get the SparkContext from the SparkSession
sc = spark.sparkContext
# Set the MinIO access key, secret key, endpoint, and other configurations
sc._jsc.hadoopConfiguration().set("fs.s3a.access.key", "minio")
sc._jsc.hadoopConfiguration().set("fs.s3a.secret.key", "password")
sc._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "http://localhost:9000")
sc._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true")
sc._jsc.hadoopConfiguration().set("fs.s3a.connection.ssl.enabled", "false")
sc._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
sc._jsc.hadoopConfiguration().set("fs.s3a.connection.ssl.enabled", "false")
# Read a JSON file from an MinIO bucket using the access key, secret key,
# and endpoint configured above
df = spark.read.option("header", "true") \
    .json("s3a://meteo/meteo_20250303_104928.json")
# show data
df.show()


# Définition du schéma
schema = StructType([
    StructField("datetime", StringType(), True),
    StructField("temperature", FloatType(), True)
])

# Lire les fichiers JSON avec le schéma défini
df = spark.read.schema(schema).json("s3a://meteo/*.json")
df.printSchema()
df.show(20, truncate=False)
df = df.withColumn("datetime", to_timestamp(col("datetime"), "yyyy-MM-dd'T'HH:mm:ss'Z'"))
try:
    print("Tentative d'écriture dans le bucket meteo-parquet...")
    df.write.mode("overwrite").parquet("s3a://meteo-parquet/")
    print("Données écrites avec succès dans le bucket meteo-parquet")
except Exception as e:
    print(f"Erreur lors de l'écriture des données : {e}")

df.printSchema()
df.show()
