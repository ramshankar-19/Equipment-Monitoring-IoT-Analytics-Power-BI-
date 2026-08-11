# Power BI DAX Measures

These are the required DAX measures for the Plant Operations and Equipment Health dashboard pages.

## Base KPIs

**Total Machines:**
```dax
Total Machines = DISTINCTCOUNT('FactSensorReadings'[machine_id])
```

**Active Machines:**
```dax
Active Machines = CALCULATE(DISTINCTCOUNT('FactSensorReadings'[machine_id]), 'FactSensorReadings'[rpm] > 0)
```

## Machine Status KPIs (Based on the latest reading)

Because the dataset is time-series, we need to find the status of each machine *at the latest timestamp* to show its current state.

**Latest Timestamp (Helper Measure):**
```dax
Latest Timestamp = MAX('FactSensorReadings'[timestamp])
```

**Normal Machines:**
```dax
Normal Machines = 
CALCULATE(
    DISTINCTCOUNT('FactSensorReadings'[machine_id]),
    'FactSensorReadings'[overall_machine_status] = "NORMAL",
    'FactSensorReadings'[timestamp] = [Latest Timestamp]
)
```

**Warning Machines:**
```dax
Warning Machines = 
CALCULATE(
    DISTINCTCOUNT('FactSensorReadings'[machine_id]),
    'FactSensorReadings'[overall_machine_status] = "WARNING",
    'FactSensorReadings'[timestamp] = [Latest Timestamp]
)
```

**Critical Machines:**
```dax
Critical Machines = 
CALCULATE(
    DISTINCTCOUNT('FactSensorReadings'[machine_id]),
    'FactSensorReadings'[overall_machine_status] = "CRITICAL",
    'FactSensorReadings'[timestamp] = [Latest Timestamp]
)
```

## Averages & Aggregations

**Average Health Score (Current):**
```dax
Avg Health Score Current = 
CALCULATE(
    AVERAGE('FactSensorReadings'[health_score]),
    'FactSensorReadings'[timestamp] = [Latest Timestamp]
)
```

**Average Temperature:**
```dax
Avg Temperature = AVERAGE('FactSensorReadings'[temperature_c])
```
*(Repeat pattern for Pressure, Vibration, Motor Current, RPM)*

## Alerts

**Active Alerts Count:**
```dax
Active Alerts = 
CALCULATE(
    SUM('FactSensorReadings'[alert_flag]),
    'FactSensorReadings'[timestamp] = [Latest Timestamp]
)
```

## Rolling Averages (5-Minute)

These are critical for smoothing out the noise in line charts to reveal true degradation trends.

**5-Min Rolling Average Temperature:**
```dax
Avg Temp (5 Min Rolling) = 
AVERAGEX(
    FILTER(
        ALL('FactSensorReadings'),
        'FactSensorReadings'[machine_id] = MAX('FactSensorReadings'[machine_id]) &&
        'FactSensorReadings'[timestamp] > MAX('FactSensorReadings'[timestamp]) - TIME(0, 5, 0) &&
        'FactSensorReadings'[timestamp] <= MAX('FactSensorReadings'[timestamp])
    ),
    'FactSensorReadings'[temperature_c]
)
```
*(Repeat pattern for Vibration and Motor Current)*
