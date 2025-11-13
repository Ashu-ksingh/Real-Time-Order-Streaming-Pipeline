# ⚡ Real-Time Order Streaming Data Pipeline

This project demonstrates a complete **real-time data engineering pipeline** using  
**Apache Kafka**, **Spark Structured Streaming**, and **PostgreSQL**.  

It simulates a continuous stream of **e-commerce order events**, processes them with Spark in near real-time, and writes aggregated results to PostgreSQL for analytics.

---

## 🏗️ Architecture

Python Producer
↓
Kafka Topic ("orders")
↓
Spark Structured Streaming
↓
PostgreSQL (realtime_customer_sales)

yaml
Copy code

---

## 🧰 Tech Stack

- **Python** (Kafka producer + orchestration)
- **Apache Kafka** (message broker)
- **Spark Structured Streaming** (real-time transformations)
- **PostgreSQL** (data storage)
- **Docker Compose** (Kafka + Zookeeper)
- **SQLAlchemy / psycopg2** for DB operations

---

## 📂 Project Structure

real_time_order_streaming/
│
├── scripts/
│ ├── producer.py # Kafka producer generating order events
│ ├── spark_consumer.py # Spark consumer processing Kafka stream
│ ├── main.py # Full pipeline orchestrator
│
├── config/
│ ├── db_config.py # PostgreSQL credentials
│ ├── kafka_config.py # Kafka topic + broker settings
│
├── data/
│ └── products.json # (optional) static enrichment file
│
├── docker-compose.yml # Kafka + Zookeeper setup
├── requirements.txt
└── README.md

yaml
Copy code

---

## 🧰 Setup Instructions and output 

```bash
## 1️⃣ Install Dependencies
pip install -r requirements.txt

## 2️⃣ Start Kafka Environment (Docker)
docker-compose up -d

## 3️⃣ Verify Kafka and Zookeeper Containers
docker ps

## 4️⃣ Start Kafka Producer (streaming events)
python scripts/producer.py

## 5️⃣ Start Spark Structured Streaming Consumer
python scripts/spark_consumer.py

## 6️⃣ (Optional) Run Entire Pipeline
python scripts/main.py

## 7️⃣ Check Data in PostgreSQL
SELECT * FROM realtime_customer_sales;

## 🗃️ PostgreSQL Output Table
Table: realtime_customer_sales


Column	Type	Description
window_start	timestamp	Start time of streaming window
window_end	timestamp	End time of streaming window
customer_id	int	Customer identifier
total_sales	double	Total amount spent in window
order_count	int	Number of orders placed

## 📊 Sample Output
window_start	window_end	customer_id	total_sales	order_count
2025-11-12 22:36:00	2025-11-12 22:37:00	101	2400	3
2025-11-12 22:36:30	2025-11-12 22:37:30	104	1200	1
