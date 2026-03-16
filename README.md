# **Smart City Real-Time Data Engineering Pipeline (Flow Explanation)**

## Project Overview
This project demonstrates how to build a real-time data engineering pipeline for a Smart City use case using Apache Kafka, Apache Spark, AWS services, and BI tools. The goal is to handle streaming data (vehicle, GPS, camera, weather, emergency) in real time, process it, store it efficiently, and make it available for analytics and visualization.

## System Architecture
![System Architecture](System%20Architecture.png)

## **1\. Data Generation Layer (IoT / Simulation Layer)**

**Component:** main.py  
**Role:** Simulates smart city sensor data.

**What happens here**

This component **generates synthetic city events** that mimic real-world systems such as:

- 🚗 Vehicle telemetry
- 📍 GPS location data
- 📷 Traffic camera events
- 🌧 Weather information
- 🚨 Emergency alerts

**Example event**

```
Vehicle Event
{  
vehicle_id: "V123",  
speed: 65,  
latitude: 40.712,  
longitude: -74.006,  
timestamp: 2026-03-15  
}
```

**Why it exists**

- Real smart cities have **thousands of IoT sensors**, but since we don't have them, the Python script **simulates streaming data**.

**Output**

- The simulated data is **sent to Kafka topics**.

    - Vehicle data → Kafka topic: vehicle_data  
    - GPS data → Kafka topic: gps_data  
    - Traffic camera → Kafka topic: traffic_data  
    - Weather data → Kafka topic: weather_data  
    - Emergency data → Kafka topic: emergency_data

## **2\. Event Streaming Layer**

**Apache Kafka**

- **Role:** Real-time event streaming platform.

**What Kafka does**

- Kafka acts like a **high-speed messaging backbone**.
- Producer → Kafka → Consumers

**In this project**

- Producer = main.py
- Consumers = Spark Streaming

**Why Kafka is used**

- Because smart city data is:

  - Continuous
  - High volume
  - Real-time
  - Multiple systems need it

Kafka allows:

- buffering  
- scalability  
- decoupling systems  
- fault tolerance

**Example Flow**
```
Vehicle Event  
     ↓  
Kafka Topic (vehicle_data)  
     ↓  
Spark Streaming Consumer
```
## **3\. Coordination Layer**

**ZooKeeper**

- **Role:** Kafka cluster manager.

- ZooKeeper manages:

  - broker coordination
  - leader election
  - metadata management

**Example**

If Kafka has multiple brokers:

- Broker1  
- Broker2  
- Broker3

ZooKeeper decides:

- Leader Broker  
- Replica Brokers

**Why it's used**

- Kafka needs **distributed coordination**.

- _(Note: Modern Kafka uses KRaft instead of ZooKeeper.)_

## **4\. Distributed Processing Layer**

**Apache Spark Structured Streaming**

**Component:** spark-city.py

- This is the **core processing engine of the pipeline**.

**Spark reads Kafka streams**
```
Spark Streaming  
↓  
Reads Kafka Topics  
↓  
Processes streaming data
```
Spark subscribes to topics:

- vehicle_data  
- gps_data  
- traffic_data  
- weather_data  
- emergency_data

**What Spark does with the data**

- Reads JSON messages from Kafka  
- Applies schemas  
- Converts to structured dataframes  
- Performs transformations  
- Writes results to storage

**Spark Cluster Architecture**

Docker setup simulates a distributed Spark cluster.
```
     Spark Master  
          │  
┌─────────┼─────────┐  
│         │         │  
Worker1 Worker2 Worker3
```
**Why Spark workers exist**

Workers process partitions of the stream in parallel.

Example:
```
Vehicle stream  
↓  
Partition1 → Worker1  
Partition2 → Worker2  
Partition3 → Worker3
```
This makes the pipeline **scalable**.

## **5\. Data Lake Storage Layer**

**Amazon S3**

- Spark writes processed data to **S3**.

**Storage zones used**

From the architecture diagram:
```
Raw Storage (Bronze Layer)  
           ↓  
Transformed Storage (Silver Layer)
```
**Example output files**

- s3://smartcity/raw/vehicle_data/  
- s3://smartcity/raw/gps_data/  
- s3://smartcity/raw/weather_data/

Files are stored as:
- Parquet format

**Why Parquet**

Parquet is:

- columnar  
- compressed  
- fast for analytics  
- optimized for big data

## **6\. Metadata Management Layer**

**AWS Glue**

- Glue performs **data cataloging**.

**What Glue does**

- Crawls S3 data  
- Detects schemas  
- Registers tables in **Glue Data Catalog**

Example:
```
S3 path:  
s3://smartcity/vehicle_data/  
<br/>Glue table:  
vehicle_data_table
```
Now other services can query the data.

## **7\. Query Layer**

**Amazon Athena**

- Athena allows SQL queries directly on S3.

Example query:
```
SELECT vehicle_id, avg(speed)  
FROM vehicle_data  
GROUP BY vehicle_id
```
**Why Athena**

- No database server required.
- Athena = **serverless SQL for S3**

## **8\. Data Warehouse Layer**

**Amazon Redshift**

- Redshift acts as the **analytics warehouse**.
- Data can move from: S3 → Redshift

Why?

Because Redshift provides:

- faster BI queries
- complex joins
- dimensional models
- aggregated reporting

## **9\. Visualization Layer**

BI tools connect to Athena or Redshift.

**Tools shown in architecture**

- Power BI
- Tableau
- Looker Studio

**Example dashboards**

Smart city analytics dashboards might show:

 -traffic congestion heatmaps  
- accident hotspots  
- vehicle movement patterns  
- emergency response times  
- weather impact on traffic

**Full Pipeline Flow (Simplified)**
```
IoT Simulation  
(main.py)  
  │  
  ▼  
Kafka Producers  
  │  
  ▼  
Kafka Topics  
(vehicle/gps/weather/etc)  
  │  
  ▼  
Spark Structured Streaming  
(spark-city.py)  
  │  
  ▼  
S3 Data Lake (Parquet)  
  │  
  ▼  
AWS Glue Catalog  
  │  
  ▼  
Athena / Redshift  
  │  
  ▼  
BI Dashboards  
(PowerBI / Tableau / Looker)
```
**Why This Architecture Is Important**

This project demonstrates **modern data engineering architecture**.

**Key engineering concepts used**

- Event-driven architecture  
- Streaming pipelines  
- Distributed processing  
- Cloud data lakes  
- Schema enforcement  
- Data cataloging  
- Serverless querying  
- Analytics warehouse
