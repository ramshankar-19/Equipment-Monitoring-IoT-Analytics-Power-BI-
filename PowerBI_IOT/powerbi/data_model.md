# Power BI Data Model

For this proof-of-concept, we are using a simplified star-schema (or single-table) architecture suitable for the generated dataset. 

## Primary Fact Table
**`FactSensorReadings`** (Loaded from `data/processed/powerbi_sensor_data.csv`)

| Column | Data Type | Description |
|---|---|---|
| `timestamp` | Date/Time | The exact time of the reading. |
| `machine_id` | Text | Unique identifier for the equipment (e.g. M-001). |
| `machine_name` | Text | Human-readable name. |
| `equipment_type` | Text | Category of equipment (Mixer, Pump, etc.). |
| `location` | Text | Physical location in the plant. |
| `temperature_c` | Decimal Number | Actual temperature reading. |
| `temperature_c_status` | Text | Calculated status (NORMAL, WARNING, CRITICAL). |
| `vibration_mm_s` | Decimal Number | Actual vibration reading. |
| `vibration_mm_s_status`| Text | Calculated status. |
| `motor_current_a` | Decimal Number | Actual current reading. |
| `motor_current_a_status`| Text | Calculated status. |
| `overall_machine_status`| Text | Worst-case status of the machine at that timestamp. |
| `health_score` | Whole Number | 0-100 score based on penalty deductions. |
| `alert_flag` | Whole Number | 1 if WARNING/CRITICAL, 0 if NORMAL. |
| `alert_reason` | Text | Explanation of which sensors triggered the alert. |

## Dimension Tables (Optional for V1)
Because the `powerbi_sensor_data.csv` is fully denormalized (containing `machine_name`, `location`, `equipment_type`), you do not strictly *need* dimension tables for this V1. 

However, for a true Star Schema, you can extract the following in Power Query:
1. **`DimMachine`**: `machine_id`, `machine_name`, `equipment_type`, `location`
2. **`DimDate` / `DimTime`**: Auto-generated Date table based on `timestamp` for time-intelligence DAX.

*Note: For the best performance with Microsoft Fabric Eventhouse in the future, retaining a wide, denormalized table structure is actually often preferred for KQL/DirectLake performance.*
