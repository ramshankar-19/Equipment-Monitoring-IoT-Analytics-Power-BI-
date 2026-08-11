# Equipment-Monitoring-IoT-Analytics-Power-BI-

# Real-Time Pharmaceutical Manufacturing Equipment Monitoring

## Overview
This project is a realistic proof-of-concept IoT monitoring system for a pharmaceutical manufacturing environment. It simulates equipment sensors across multiple production lines and processes the data to feed a Power BI Desktop dashboard.

## Business Problem
Monitoring the health and status of critical pharmaceutical manufacturing equipment (e.g., mixers, conveyors, filling machines) is essential to prevent downtime, ensure quality, and avoid catastrophic failures.

## Project Objective
To build a scalable and explainable IoT analytics pipeline that processes real-time/simulated sensor data and provides clear, actionable insights via an operational dashboard.

## Important Disclaimer
**This is an independent proof-of-concept using simulated IoT sensor data. It does not use proprietary, confidential, or production data from Dr. Reddy's Laboratories or any other company.** All machine profiles and sensor values are purely generated for demonstration purposes.

## Architecture

**Current Local Implementation:**
Simulated Sensors → Python → MQTT (Optional) / Local Storage (CSV) → Power BI Desktop

**Future Architecture (Fabric Integration):**
IoT Sensors → MQTT/IoT Gateway → Microsoft Fabric Eventstream → Eventhouse/KQL → Power BI → Activator

## Technologies
- **Python**: Sensor simulation and data processing (`pandas`, `numpy`)
- **MQTT**: `paho-mqtt` (Optional local transport)
- **Power BI Desktop**: Dashboarding, DAX, Power Query
- *(Future)*: Microsoft Fabric Eventstream, Eventhouse, KQL, Activator

## How to Run (Coming Soon)
*(Instructions will be added as the simulator is built)*

## How to Connect to Power BI (Coming Soon)
*(Instructions will be added for loading the dataset into Power BI)*
