# Project Overview
This project demonstrates how to build a real-time data engineering pipeline for a Smart City use case using Apache Kafka, Apache Spark, AWS services, and BI tools. The goal is to handle streaming data (vehicle, GPS, camera, weather, emergency) in real time, process it, store it efficiently, and make it available for analytics and visualization.

# System Architecture
![System Architecture](System%20Architecture.png)

# Data Sources
Multiple real-time data sources feed into the system:
-	Vehicle Information
-	GPS Information
-	Camera Information
-	Weather Information
-	Emergency Information

These diverse streams mimic a smart city environment where different sensors continuously generate events.

# Data Ingestion (Kafka + Zookeeper + Docker)
-	Apache Kafka is the primary ingestion layer for real-time streaming data.
-	Zookeeper manages Kafka brokers and cluster coordination.
-	Docker containerizes services for scalability and deployment.

Kafka ensures high throughput, fault-tolerant streaming ingestion from smart city data sources.

# Stream Processing (Apache Spark)
-	Apache Spark Streaming consumes the Kafka topics.
-	Spark runs in a master-worker cluster mode, distributing computation.
-	It processes and cleanses the raw data, performing ETL in motion before sending results to storage.

# Storage & Data Lake (AWS S3 + Glue + Data Catalog)
-	Raw Data is first stored in Amazon S3 Raw Storage.
-	AWS Glue Crawlers scan and create metadata for raw and processed data.
-	Transformed Data (after Spark/Glue processing) is stored in S3 Transformed Storage.
-	AWS Glue ETL Jobs are used for further transformation and schema enforcement.
-	AWS Data Catalog serves as the metadata repository.

# Querying & Warehousing (Athena + Redshift)
-	Amazon Athena enables SQL-based querying of S3 data directly.
-	Amazon Redshift acts as the data warehouse for structured, large-scale analytics.
-	IAM ensures secure authentication and access control across AWS services.

# Visualization & Reporting (Power BI, Tableau, Looker Studio)
Processed and curated data from Redshift is consumed by BI tools like:
-	Power BI
-	Tableau
-	Google Looker Studio

These tools provide dashboards, KPIs, and real-time insights for decision-making in the smart city ecosystem.

# Key Skills Learned 
-	Data Ingestion: Kafka, Zookeeper, Docker
-	Stream Processing: Spark Structured Streaming
-	Cloud Storage: Amazon S3 (Raw + Transformed layers)
-	ETL & Metadata: AWS Glue, Data Catalog
-	Query Engines: Athena, Redshift
-	Visualization: Power BI, Tableau, Looker Studio
-	Security: IAM roles and policies
