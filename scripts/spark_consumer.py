import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, sum as Fsum, count
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType

# Add parent path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.db_config import DB_CONFIG
from config.kafka_config import KAFKA_CONFIG

# ✅ PostgreSQL connection
jdbc_url = f"jdbc:postgresql://{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

# ✅ Kafka connection
KAFKA_TOPIC = KAFKA_CONFIG["topic"]
KAFKA_BROKER = KAFKA_CONFIG["bootstrap_servers"]

# ✅ Schema for order data
order_schema = StructType([
    StructField("order_id", IntegerType()),
    StructField("customer_id", IntegerType()),
    StructField("product_id", StringType()),
    StructField("product_name", StringType()),
    StructField("quantity", IntegerType()),
    StructField("price", DoubleType()),
    StructField("total_amount", DoubleType()),
    StructField("order_time", StringType())
])

spark = (
    SparkSession.builder
    .appName("RealTimeOrderConsumer")
    .config(
        "spark.jars.packages",
        "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.postgresql:postgresql:42.7.4"
    )
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

print("🚀 Spark Structured Streaming Consumer started...")

# ✅ Read Stream from Kafka using config
orders_raw_df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", KAFKA_BROKER)
    .option("subscribe", KAFKA_TOPIC)
    .option("startingOffsets", "latest")
    .load()
)
