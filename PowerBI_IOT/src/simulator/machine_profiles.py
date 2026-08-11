# machine_profiles.py

# Define baselines for realistic pharmaceutical manufacturing equipment
# Values represent normal operating conditions.
# Ranges are expressed as [min, max] or normal mean. 
# We'll use these to generate random variations and correlated behaviors.

MACHINES = {
    "M-001": {
        "machine_id": "M-001",
        "machine_name": "Mixing Unit Alpha",
        "equipment_type": "Mixing Unit",
        "location": "Production Line A",
        "baseline_temp_c": 70.0,
        "baseline_pressure_bar": 3.8,
        "baseline_humidity_pct": 45.0,
        "baseline_vibration_mm_s": 1.5,
        "baseline_current_a": 8.0,
        "baseline_rpm": 1200,
    },
    "M-002": {
        "machine_id": "M-002",
        "machine_name": "Mixing Unit Beta",
        "equipment_type": "Mixing Unit",
        "location": "Production Line A",
        "baseline_temp_c": 72.0,
        "baseline_pressure_bar": 4.0,
        "baseline_humidity_pct": 45.0,
        "baseline_vibration_mm_s": 1.7,
        "baseline_current_a": 8.5,
        "baseline_rpm": 1250,
    },
    "M-003": {
        "machine_id": "M-003",
        "machine_name": "Transfer Pump 1",
        "equipment_type": "Pump",
        "location": "Utilities Area",
        "baseline_temp_c": 55.0,
        "baseline_pressure_bar": 5.0,
        "baseline_humidity_pct": 50.0,
        "baseline_vibration_mm_s": 2.5,
        "baseline_current_a": 6.0,
        "baseline_rpm": 2800,
    },
    "M-004": {
        "machine_id": "M-004",
        "machine_name": "Air Compressor A",
        "equipment_type": "Compressor",
        "location": "Utilities Area",
        "baseline_temp_c": 85.0,
        "baseline_pressure_bar": 8.0,
        "baseline_humidity_pct": 30.0,
        "baseline_vibration_mm_s": 3.0,
        "baseline_current_a": 15.0,
        "baseline_rpm": 3500,
    },
    "M-005": {
        "machine_id": "M-005",
        "machine_name": "Main Conveyor",
        "equipment_type": "Conveyor",
        "location": "Production Line B",

        "baseline_temp_c": 40.0,
        "baseline_pressure_bar": 1.0,
        "baseline_humidity_pct": 55.0,
        "baseline_vibration_mm_s": 1.0,
        "baseline_current_a": 4.0,
        "baseline_rpm": 300,

        # Simulated monitoring thresholds for this project.
        # These are NOT real pharmaceutical equipment specifications.
        "thresholds": {
            "pressure_bar": {
                "warning": 1.45,
                "critical": 1.60,
                "direction": "up"
            },
            "motor_current_a": {
                "warning": 5.75,
                "critical": 6.50,
                "direction": "up"
            }
        },
    },
    "M-006": {
        "machine_id": "M-006",
        "machine_name": "Vial Filling Machine",
        "equipment_type": "Filling Machine",
        "location": "Production Line B",
        "baseline_temp_c": 60.0,
        "baseline_pressure_bar": 2.5,
        "baseline_humidity_pct": 40.0,
        "baseline_vibration_mm_s": 1.2,
        "baseline_current_a": 7.5,
        "baseline_rpm": 900,
    },
    "M-007": {
        "machine_id": "M-007",
        "machine_name": "Blister Packaging 1",
        "equipment_type": "Packaging Machine",
        "location": "Packaging Area",
        "baseline_temp_c": 65.0,
        "baseline_pressure_bar": 6.0, # pneumatic 
        "baseline_humidity_pct": 35.0,
        "baseline_vibration_mm_s": 2.0,
        "baseline_current_a": 10.0,
        "baseline_rpm": 600,
    },
    "M-008": {
        "machine_id": "M-008",
        "machine_name": "Blister Packaging 2",
        "equipment_type": "Packaging Machine",
        "location": "Packaging Area",
        "baseline_temp_c": 64.0,
        "baseline_pressure_bar": 6.0,
        "baseline_humidity_pct": 35.0,
        "baseline_vibration_mm_s": 2.2,
        "baseline_current_a": 10.2,
        "baseline_rpm": 600,
    }
}
