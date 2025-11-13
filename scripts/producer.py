import json
import time
import random
from kafka import KafkaProducer
from datetime import datetime
import sys, os

# Add parent path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.kafka_config import KAFKA_CONFIG

KAFKA_TOPIC = KAFKA_CONFIG["topic"]
KAFKA_BROKER = KAFKA_CONFIG["bootstrap_servers"]


# Sample data for simulation
customers = [101, 102, 103, 104, 105]
products = [
    {"product_id": "P001", "name": "Headphones", "price": 600},
    {"product_id": "P002", "name": "Keyboard", "price": 900},
    {"product_id": "P003", "name": "Mouse", "price": 400},
    {"product_id": "P004", "name": "Monitor", "price": 800},
    {"product_id": "P005", "name": "Speaker", "price": 700},
]

def create_order():
    """Generate a random order event"""
    product = random.choice(products)
    order = {
        "order_id": random.randint(1000, 9999),
        "customer_id": random.choice(customers),
        "product_id": product["product_id"],
        "product_name": product["name"],
        "quantity": random.randint(1, 5),
        "price": product["price"],
        "total_amount": product["price"] * random.randint(1, 5),
        "order_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return order


def produce_messages():
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER],
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

    print(f"🚀 Sending messages to Kafka topic '{KAFKA_TOPIC}'...")
    for _ in range(20):  # send 20 messages then stop
        order_event = create_order()
        producer.send(KAFKA_TOPIC, value=order_event)
        print(f"📦 Sent: {order_event}")
        time.sleep(2)


if __name__ == "__main__":
    try:
        produce_messages()
    except KeyboardInterrupt:
        print("\n🛑 Stopped producing messages.")
