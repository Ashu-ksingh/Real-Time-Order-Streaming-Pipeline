# main.py — Orchestrator for Real-Time Streaming Pipeline
import os
import subprocess
import time
import sys

# ✅ Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.kafka_config import KAFKA_CONFIG

def run_pipeline():
    print("\n🚀 Starting Real-Time Order Streaming Pipeline...\n")
    print(f"🔹 Kafka Broker: {KAFKA_CONFIG['bootstrap_servers']}")
    print(f"🔹 Kafka Topic: {KAFKA_CONFIG['topic']}\n")

    # ✅ Step 1: Start the Kafka Producer
    print("📦 Launching Kafka Producer (sending live order events)...\n")
    producer_process = subprocess.Popen(
        ["python", "scripts/producer.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    # Give the producer some time to generate messages before starting Spark
    time.sleep(10)

    # ✅ Step 2: Start Spark Structured Streaming Consumer
    print("\n⚡ Launching Spark Structured Streaming Consumer...\n")
    consumer_process = subprocess.Popen(
        ["python", "scripts/spark_consumer.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    print("\n✅ Pipeline is now running:")
    print("   • Producer → generating live orders")
    print("   • Consumer → processing stream and writing to PostgreSQL\n")
    print("💡 Press Ctrl + C to stop both processes.\n")

    try:
        producer_process.wait()
        consumer_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping both processes...")
        producer_process.terminate()
        consumer_process.terminate()


if __name__ == "__main__":
    run_pipeline()
