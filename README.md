# SensorDataToInfluxDB

## Overview
SensorDataToInfluxDB is a Google Cloud Function designed to handle incoming sensor data via HTTP requests and persist it to an InfluxDB instance. The function is responsible for data validation, parsing, and writing time-series data points, making it suitable for IoT devices.

Below is a high-level overview of the architecture in which the code in this repository operates:

## Components
- GitHub Repository: Hosts the codebase, including the Cloud Function and CI/CD configurations.
- Google Cloud Build (CI/CD): Automates the build and deployment process, triggered by changes pushed to the GitHub repository.
- Cloud Functions (Powered by Cloud Run): A serverless function that serves as the entry point for incoming sensor data.
- Cloud Run Service: Underlying service that powers the Cloud Function, effectively serving as its runtime.
- InfluxDB: Cloud-based InfluxDB instance hosted on AWS, used for storing time series sensor data.

## Workflow
1. Code Push: Any git push to the GitHub repository initiates the Cloud Build CI/CD pipeline.
2. Function Deployment: Cloud Build automatically deploys the Cloud Function, which in turn updates or controls the underlying Cloud Run service.
3. Data Ingestion: The function validates, processes, and forwards the incoming sensor data to the InfluxDB instance for persistent storage.

![Architecture](./images/architecture.png)
