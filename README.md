
# Real-Time Pharmaceutical Manufacturing Equipment Monitoring & IoT Analytics

> A local-first IoT analytics proof-of-concept for monitoring manufacturing equipment using simulated sensor data, Python-based anomaly detection, and Power BI.

---

## Overview

This project demonstrates an end-to-end **IoT equipment monitoring and analytics pipeline** for a pharmaceutical manufacturing environment.

The system simulates sensor readings from multiple manufacturing assets, processes the incoming data using Python-based monitoring logic, calculates equipment health scores, detects abnormal operating conditions, and presents actionable insights through a **Power BI operations dashboard**.

The project is designed as a learning and portfolio proof-of-concept for applying IoT analytics concepts to manufacturing operations and is structured to support future migration to **Microsoft Fabric Real-Time Intelligence**.

---

## Business Problem

Manufacturing facilities continuously generate equipment data such as:

- Temperature
- Pressure
- Humidity
- Vibration
- Motor current
- RPM

Manually monitoring these parameters makes it difficult to identify gradual equipment degradation before it becomes a major operational issue.

This project addresses the problem by creating an analytics pipeline that can:

- Monitor equipment health
- Identify abnormal sensor readings
- Detect warning and critical conditions
- Calculate an interpretable equipment health score
- Identify the sensor parameters responsible for an alert
- Visualize equipment trends and anomalies through Power BI

The ultimate objective is to support **condition-based monitoring and proactive maintenance decisions**.

---

## Project Objectives

The project aims to demonstrate how an IoT-enabled manufacturing analytics system can:

1. Generate realistic time-series sensor data.
2. Model correlated equipment behavior rather than purely random values.
3. Simulate progressive equipment degradation.
4. Apply machine-specific operating thresholds.
5. Classify sensor conditions as `NORMAL`, `WARNING`, or `CRITICAL`.
6. Calculate an explainable equipment health score.
7. Generate actionable alert reasons.
8. Visualize equipment health and sensor trends in Power BI.
9. Provide a scalable architecture for future real-time streaming integration.

---

# System Architecture

## Current Local Architecture

```text
┌───────────────────────┐
│  Simulated IoT        │
│  Sensors              │
│                       │
│  Temperature          │
│  Pressure             │
│  Humidity             │
│  Vibration            │
│  Motor Current        │
│  RPM                  │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ Python Sensor         │
│ Simulator             │
│                       │
│ • Correlated signals  │
│ • Natural variation   │
│ • Degradation trends  │
│ • Anomaly scenarios   │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ Raw Sensor Data       │
│ CSV Storage           │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ Python Data Processor │
│                       │
│ • Data validation     │
│ • Threshold analysis  │
│ • Sensor status       │
│ • Health scoring      │
│ • Alert generation    │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ Processed Dataset     │
│ powerbi_sensor_data   │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ Power BI Desktop      │
│                       │
│ • KPIs                │
│ • Equipment health    │
│ • Sensor trends       │
│ • Alerts              │
│ • Conditional format  │
└───────────────────────┘
````

---

## Future Real-Time Architecture

The local prototype is designed to evolve into a production-oriented streaming architecture:

```text
┌─────────────────────┐
│ Physical IoT        │
│ Sensors             │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ IoT Gateway / MQTT  │
└─────────┬───────────┘
          │
          ▼
┌────────────────────────────┐
│ Microsoft Fabric           │
│ Eventstream                │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│ Fabric Eventhouse / KQL    │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│ Power BI                   │
│ Real-Time / DirectQuery    │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│ Operational Monitoring     │
│ & Alerts                   │
└────────────────────────────┘
```

> Microsoft Fabric integration is documented as a future architecture. The current implementation does **not** require Microsoft Fabric access.

---

# Simulated Manufacturing Environment

The simulator models **8 manufacturing assets** across **4 production/utility locations**.

| ID    | Equipment            | Location          |
| ----- | -------------------- | ----------------- |
| M-001 | Mixing Unit Alpha    | Production Line A |
| M-002 | Mixing Unit Beta     | Production Line A |
| M-003 | Transfer Pump 1      | Utilities Area    |
| M-004 | Air Compressor A     | Utilities Area    |
| M-005 | Main Conveyor        | Production Line B |
| M-006 | Vial Filling Machine | Production Line B |
| M-007 | Blister Packaging 1  | Packaging Area    |
| M-008 | Blister Packaging 2  | Packaging Area    |

Each machine has its own simulated baseline operating characteristics.

---

# Sensor Parameters

The simulator generates six sensor measurements for each machine:

| Sensor        | Unit | Purpose                              |
| ------------- | ---- | ------------------------------------ |
| Temperature   | °C   | Detect thermal degradation           |
| Pressure      | bar  | Monitor process/pneumatic conditions |
| Humidity      | %    | Monitor environmental conditions     |
| Vibration     | mm/s | Detect mechanical degradation        |
| Motor Current | A    | Identify motor loading/overload      |
| RPM           | RPM  | Detect speed reduction under load    |

The simulator does not generate completely independent random values.

Instead, it introduces **correlated behavior** through a synthetic machine load factor.

For example:

```text
Higher Machine Load
       │
       ├──► Higher Motor Current
       │
       ├──► Higher Temperature
       │
       └──► Higher Vibration
```

This creates more realistic relationships between sensor measurements.

---

# Anomaly Simulation

The simulator supports progressive degradation scenarios rather than instantaneous failures.

One of the primary demonstration scenarios is:

### Combined Degradation — M-006

The simulated vial filling machine gradually develops multiple abnormal conditions.

Typical progression:

```text
Normal
  │
  ▼
Temperature increases
  │
  ▼
Vibration increases
  │
  ▼
Motor current increases
  │
  ▼
RPM decreases
  │
  ▼
Critical equipment condition
```

The degradation is intentionally gradual so that the Power BI dashboard can visualize the transition from:

```text
NORMAL → WARNING → CRITICAL
```

---

# Data Processing Pipeline

The Python processor performs several stages of data preparation.

### 1. Data Validation

* Timestamp validation
* Duplicate removal
* Numeric conversion
* Missing-value handling
* Negative-value protection

### 2. Sensor Status Classification

Each sensor is classified as:

```text
NORMAL
WARNING
CRITICAL
```

Thresholds can be defined using:

* Generic baseline-relative rules
* Machine-specific absolute thresholds

This allows different types of equipment to have different monitoring requirements.

### 3. Overall Machine Status

The individual sensor statuses are combined into an overall equipment condition:

```text
Any CRITICAL sensor
        ↓
     CRITICAL

Otherwise, any WARNING sensor
        ↓
      WARNING

Otherwise
        ↓
      NORMAL
```

### 4. Equipment Health Score

An interpretable 0–100 health score is calculated.

Current scoring logic:

```text
Starting score = 100

CRITICAL sensor = -20
WARNING sensor  = -10
```

The result is constrained between:

```text
0 ≤ Health Score ≤ 100
```

### 5. Alert Generation

When abnormal conditions are detected, the processor generates:

* Alert flag
* Overall status
* Health score
* Alert reason

Example:

```text
temperature (CRITICAL)
|
vibration (CRITICAL)
|
motor (CRITICAL)
```

This makes the alerts explainable rather than simply labeling a machine as "failed."

---

# Power BI Dashboard

The processed dataset is consumed by **Power BI Desktop**.

The dashboard is organized into three operational views.

## 1. Operations Overview

Answers:

> **"What is happening across the manufacturing environment?"**

Includes:

* Machines monitored
* Current average health
* Critical machines
* Warning machines
* Machine health matrix
* Temperature trends
* Vibration trends
* Machine selection filters

---

## 2. Equipment Health

Answers:

> **"Which equipment is deteriorating?"**

Includes:

* Equipment health comparison
* Equipment health trends
* Temperature trends
* Vibration trends
* Motor current trends
* Machine-level filtering

This view makes progressive degradation of M-006 visible.

---

## 3. Alerts & Diagnostics

Answers:

> **"What went wrong and why?"**

Includes:

* Critical readings
* Warning readings
* Alert causes
* Affected equipment
* Alert timestamps
* Sensor-level alert reasons

Example:

```text
M-006
    ↓
CRITICAL
    ↓
Temperature + Vibration + Motor Current
```

---

# Dataset

A 24-hour demonstration run was generated at approximately 10-second intervals for 8 machines.

### Current dataset

```text
Total records:       69,128
Machines:                 8
Locations:                4
Time period:          24 hours
Sensor parameters:        6
```

The processed dataset contains:

```text
69,128 records
24 columns
```

Key analytical fields include:

```text
timestamp
machine_id
machine_name
equipment_type
location

temperature_c
pressure_bar
humidity_pct
vibration_mm_s
motor_current_a
rpm

temperature_c_status
pressure_bar_status
humidity_pct_status
vibration_mm_s_status
motor_current_a_status
rpm_status

overall_machine_status
health_score
alert_flag
alert_reason
```

---

# Validation Results

The processing pipeline was tested using `pytest`.

Current test results:

```text
5 passed
0 failed
```

Tests cover:

* Normal sensor status evaluation
* Warning threshold evaluation
* Critical threshold evaluation
* Downward threshold logic for RPM
* Health score calculation

The final dataset also successfully validated:

```text
Total raw records:        69,128
Total processed records:  69,128
Duplicates removed:            0
Unique machines:               8
Unique locations:              4
```

---

# Project Structure

```text
PowerBI_IOT/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/
│   │   └── sensor_data.csv
│   │
│   └── processed/
│       └── powerbi_sensor_data.csv
│
├── src/
│   │
│   ├── simulator/
│   │   ├── config.py
│   │   ├── machine_profiles.py
│   │   ├── anomaly_generator.py
│   │   └── sensor_simulator.py
│   │
│   ├── mqtt/
│   │   └── mqtt_publisher.py
│   │
│   └── processing/
│       └── data_processor.py
│
├── powerbi/
│   ├── data_model.md
│   ├── dax_measures.md
│   └── powerbi_setup.md
│
├── docs/
│   ├── architecture.md
│   ├── business_case.md
│   ├── future_fabric_integration.md
│   └── learning_guide.md
│
├── scripts/
│   ├── generate_demo_data.py
│   └── run_demo.bat
│
└── tests/
    ├── test_processing.py
    └── test_simulator.py
```

---

# Installation

## Requirements

* Python 3.11+
* Power BI Desktop
* Windows
* Optional: MQTT broker such as Mosquitto

Install Python dependencies:

```bash
python -m pip install pandas numpy paho-mqtt pytest
```

---

# Running the Project

## Generate Historical Demo Data

From the project root:

```bash
python src/simulator/sensor_simulator.py --mode demo --hours 24 --scenario combined_degradation --machine M-006
```

This generates simulated sensor data in:

```text
data/raw/sensor_data.csv
```

---

## Process the Sensor Data

Run:

```bash
python src/processing/data_processor.py
```

The processed dataset will be written to:

```text
data/processed/powerbi_sensor_data.csv
```

The processor also prints a validation summary containing:

* Record count
* Machine count
* Location count
* Overall status distribution
* Alerts by machine

---

## Run Tests

Run:

```bash
python -m pytest tests -v
```

Expected result:

```text
5 passed
```

---

# Connecting to Power BI

Open **Power BI Desktop**.

Select:

```text
Home → Get Data → Text/CSV
```

Load:

```text
data/processed/powerbi_sensor_data.csv
```

The Power BI report uses the processed dataset as its analytical source.

The dashboard contains DAX measures for:

* Total machines
* Average health
* Critical machines
* Warning machines
* Active alerts
* Critical readings
* Warning readings
* Latest equipment health

Refer to:

```text
powerbi/powerbi_setup.md
```

for the detailed Power BI configuration.

---

# Real-Time / Streaming Extension

The current implementation uses local CSV storage so that the project can be developed without requiring a Microsoft Fabric subscription.

The architecture is intentionally designed so that the processing and visualization concepts can later be migrated to a streaming environment.

### Current

```text
Python
  ↓
CSV
  ↓
Power BI
```

### Future

```text
IoT Sensors
  ↓
MQTT / IoT Gateway
  ↓
Microsoft Fabric Eventstream
  ↓
Eventhouse / KQL
  ↓
Power BI
```

Potential future capabilities include:

* Near-real-time sensor monitoring
* Streaming anomaly detection
* Automatic dashboard refresh
* Rolling time windows
* Real-time operational alerts
* Fabric Activator-based actions
* Historical equipment analytics

---

# Key Engineering & Analytics Concepts Demonstrated

This project demonstrates practical experience with:

### Manufacturing Analytics

* Condition monitoring
* Equipment health
* Preventive / predictive maintenance concepts
* Sensor thresholding
* Operational alerting

### Data Engineering

* Time-series data generation
* Data validation
* Data cleaning
* Data transformation
* Local data pipelines

### Analytics

* Rule-based anomaly detection
* Health scoring
* Correlated sensor behavior
* Time-series analysis
* Operational KPIs

### Power BI

* Power Query
* DAX measures
* KPI cards
* Matrix visualizations
* Line charts
* Slicers
* Conditional formatting
* Operational dashboards

### IoT Architecture

* Sensor data simulation
* MQTT concepts
* Streaming architecture
* Event-driven data pipelines
* Future Microsoft Fabric integration

---

# Business Value

The project demonstrates how raw machine telemetry can be converted into operational insights:

```text
Raw Sensor Data
       ↓
Cleaned Data
       ↓
Sensor-Level Conditions
       ↓
Equipment Health
       ↓
Alerts
       ↓
Operational Decision
```

For a manufacturing organization, such a system could help operations and maintenance teams:

* Identify deteriorating equipment earlier
* Prioritize maintenance activities
* Reduce unexpected downtime
* Understand the root sensor contributing to an alert
* Monitor equipment across multiple production areas
* Move from reactive to condition-based monitoring

---

# Disclaimer

This project is an **independent educational and portfolio proof-of-concept**.

It uses entirely **synthetic/simulated sensor data** and fictional equipment profiles.

It does **not** use:

* proprietary data
* Confidential manufacturing information
* Production equipment specifications
* Real plant sensor data
* Confidential operational thresholds

Any pharmaceutical manufacturing terminology is used solely to create a realistic demonstration environment.

All monitoring thresholds are **simulated values created for this project** and should not be interpreted as actual pharmaceutical manufacturing safety or operating limits.

---

# Future Improvements

Potential extensions include:

* Continuous sensor streaming
* Rolling 24-hour data windows
* Automated data refresh
* MQTT-based streaming ingestion
* Microsoft Fabric Eventstream integration
* Fabric Eventhouse/KQL analytics
* Real-time Power BI monitoring
* Advanced anomaly detection using ML
* Predictive maintenance models
* Remaining Useful Life (RUL) prediction
* Automated maintenance recommendations

---

## Author

**B. Hari Rama Shankar**
Mechanical Engineering | IIT Madras

This project combines **manufacturing engineering, IoT concepts, Python data processing, and Power BI analytics** to demonstrate an end-to-end equipment monitoring workflow.

````


And for your FMCG applications, the most important part of this README is the **Business Problem → Processing → Equipment Health → Operational Decision** story. That makes it look like a manufacturing analytics project rather than simply a Power BI practice project.
