# Power BI Dashboard Setup Guide

Follow these steps to connect Power BI Desktop to the simulated pharmaceutical manufacturing dataset.

## 1. Load the Dataset
1. Open **Power BI Desktop**.
2. Click **Get Data** > **Text/CSV**.
3. Navigate to `Desktop/PowerBI_IOT/data/processed/` and select `powerbi_sensor_data.csv`.
4. Click **Load** (or **Transform Data** if you wish to inspect the columns).

## 2. Set Data Types (Important)
Once loaded, go to the **Data View** (table icon on the left) and ensure these columns are correctly typed:
- `timestamp`: Date/Time
- `machine_id`, `machine_name`, `equipment_type`, `location`: Text
- `temperature_c`, `pressure_bar`, `humidity_pct`, `vibration_mm_s`, `motor_current_a`: Decimal Number
- `rpm`, `health_score`, `alert_flag`: Whole Number

## 3. Implement DAX Measures
1. Right-click the `FactSensorReadings` table in the Data pane and select **New Measure**.
2. Copy and paste each measure from [dax_measures.md](file:///C:/Users/battu/Desktop/PowerBI_IOT/powerbi/dax_measures.md). 
3. *Tip: Format the `Avg Health Score` as a whole number.*

## 4. Build the Report Pages
We recommend building a 3-page interactive report.

### Page 1: Plant Operations Overview
- **Visuals**: 
  - 4 KPI Cards along the top: Total Machines, Normal, Warning, Critical.
  - Line Chart: Average Temperature over `timestamp` (hierarchy removed).
  - Donut Chart: Count of `machine_id` by `overall_machine_status`.
- **Slicers**: 
  - `location` (Dropdown)

### Page 2: Equipment Health
- **Slicers**: 
  - `machine_name` (Single Select)
- **Visuals**:
  - Gauge Chart or KPI Card: `Avg Health Score Current` (Max 100).
  - Multi-row Card: Current values for Temperature, Pressure, Vibration, etc.
  - Line Chart (The most important visual): Show `timestamp` on X-axis, and `Avg Temp (5 Min Rolling)` on Y-axis.

### Page 3: Anomaly & Alerts
- **Visuals**:
  - Table: Filtered to show only rows where `alert_flag = 1`. 
  - Columns to include: `timestamp`, `machine_name`, `location`, `overall_machine_status`, `alert_reason`.
  - Conditional Formatting: Apply background colors to `overall_machine_status` (Red = CRITICAL, Yellow = WARNING).

## 5. Refreshing Data
If you run the Python simulator again (in DEMO or LIVE mode) and process the new data via `python data_processor.py`, simply click **Refresh** on the Power BI ribbon to instantly update the dashboard with the new time-series data.
