import argparse
import time
import datetime
import csv
import os
import sys
import numpy as np

# Adjust the path so we can run directly from anywhere
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulator.config import (
    RAW_DATA_FILE, DEFAULT_SEED, DEFAULT_DEMO_HOURS, 
    DEFAULT_DEMO_INTERVAL_SEC, DEFAULT_LIVE_INTERVAL_SEC,
    STATUS_NORMAL, ANOMALY_NONE
)
from simulator.machine_profiles import MACHINES
from simulator.anomaly_generator import AnomalyGenerator
from mqtt.mqtt_publisher import MqttPublisher

def setup_csv():
    """Ensure the CSV file has headers if it doesn't exist or is empty."""
    file_exists = os.path.isfile(RAW_DATA_FILE)
    if not file_exists or os.path.getsize(RAW_DATA_FILE) == 0:
        with open(RAW_DATA_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp", "machine_id", "machine_name", "equipment_type", "location",
                "temperature_c", "pressure_bar", "humidity_pct", "vibration_mm_s",
                "motor_current_a", "rpm", "operating_status", "anomaly_type"
            ])

def generate_machine_reading(machine_id, elapsed_minutes, anomaly_gen):
    """Generate a single reading for a machine with realistic correlations and noise."""
    profile = MACHINES[machine_id]
    
    # 1. Base variation (simulate load changes and minor natural fluctuations)
    # Slow drift using sine wave based on time (period = ~60 mins)
    load_factor = 1.0 + 0.1 * np.sin(elapsed_minutes * (2 * np.pi / 60.0)) + np.random.normal(0, 0.05)
    
    # Base state calculations with correlations to load_factor
    temp = profile["baseline_temp_c"] + (load_factor - 1.0) * 5.0 + np.random.normal(0, 0.5)
    pressure = profile["baseline_pressure_bar"] * (1.0 + (load_factor - 1.0)*0.1) + np.random.normal(0, 0.1)
    humidity = profile["baseline_humidity_pct"] + np.random.normal(0, 2.0)
    vibration = profile["baseline_vibration_mm_s"] * (1.0 + (load_factor - 1.0)*0.2) + np.random.normal(0, 0.1)
    current = profile["baseline_current_a"] * load_factor + np.random.normal(0, 0.2)
    rpm = profile["baseline_rpm"] * (1.0 + (load_factor - 1.0)*0.05) + np.random.normal(0, 5)
    
    # Prevent negative values just in case
    state = {
        "temperature_c": max(0, temp),
        "pressure_bar": max(0, pressure),
        "humidity_pct": max(0, humidity),
        "vibration_mm_s": max(0, vibration),
        "motor_current_a": max(0, current),
        "rpm": max(0, rpm)
    }
    
    # 2. Apply anomalies
    state, anomaly_type = anomaly_gen.apply_anomaly(machine_id, state, elapsed_minutes)
    
    # 3. Round to reasonable decimal places
    state["temperature_c"] = round(state["temperature_c"], 2)
    state["pressure_bar"] = round(state["pressure_bar"], 2)
    state["humidity_pct"] = round(state["humidity_pct"], 2)
    state["vibration_mm_s"] = round(state["vibration_mm_s"], 3)
    state["motor_current_a"] = round(state["motor_current_a"], 2)
    state["rpm"] = round(state["rpm"])
    
    return state, anomaly_type

def run_demo(hours, interval_sec, scenario, target_machine, enable_mqtt):
    """Generate historical dataset."""
    print(f"Starting DEMO mode generation for {hours} hours at {interval_sec}s intervals.")
    setup_csv()
    anomaly_gen = AnomalyGenerator(scenario, target_machine)
    mqtt_pub = MqttPublisher(enabled=enable_mqtt)
    
    start_time = datetime.datetime.now() - datetime.timedelta(hours=hours)
    end_time = datetime.datetime.now()
    current_time = start_time
    
    total_records = 0
    with open(RAW_DATA_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        
        while current_time <= end_time:
            elapsed_minutes = (current_time - start_time).total_seconds() / 60.0
            
            for m_id, profile in MACHINES.items():
                state, anomaly_type = generate_machine_reading(m_id, elapsed_minutes, anomaly_gen)
                
                record_dict = {
                    "timestamp": current_time.isoformat(),
                    "machine_id": m_id,
                    "machine_name": profile["machine_name"],
                    "equipment_type": profile["equipment_type"],
                    "location": profile["location"],
                    "temperature_c": state["temperature_c"],
                    "pressure_bar": state["pressure_bar"],
                    "humidity_pct": state["humidity_pct"],
                    "vibration_mm_s": state["vibration_mm_s"],
                    "motor_current_a": state["motor_current_a"],
                    "rpm": state["rpm"],
                    "operating_status": STATUS_NORMAL,
                    "anomaly_type": anomaly_type
                }
                
                writer.writerow(list(record_dict.values()))
                mqtt_pub.publish_reading(profile["location"], m_id, record_dict)
                total_records += 1
                
            current_time += datetime.timedelta(seconds=interval_sec)
            
    mqtt_pub.disconnect()
    print(f"Demo generation complete! Created {total_records} records at {RAW_DATA_FILE}")

def run_live(interval_sec, scenario, target_machine, enable_mqtt):
    """Run continuously and append readings."""
    print(f"Starting LIVE mode at {interval_sec}s intervals. Press Ctrl+C to stop.")
    setup_csv()
    anomaly_gen = AnomalyGenerator(scenario, target_machine)
    mqtt_pub = MqttPublisher(enabled=enable_mqtt)
    
    start_time = datetime.datetime.now()
    
    try:
        while True:
            current_time = datetime.datetime.now()
            elapsed_minutes = (current_time - start_time).total_seconds() / 60.0
            
            records = []
            for m_id, profile in MACHINES.items():
                state, anomaly_type = generate_machine_reading(m_id, elapsed_minutes, anomaly_gen)
                record_dict = {
                    "timestamp": current_time.isoformat(),
                    "machine_id": m_id,
                    "machine_name": profile["machine_name"],
                    "equipment_type": profile["equipment_type"],
                    "location": profile["location"],
                    "temperature_c": state["temperature_c"],
                    "pressure_bar": state["pressure_bar"],
                    "humidity_pct": state["humidity_pct"],
                    "vibration_mm_s": state["vibration_mm_s"],
                    "motor_current_a": state["motor_current_a"],
                    "rpm": state["rpm"],
                    "operating_status": STATUS_NORMAL,
                    "anomaly_type": anomaly_type
                }
                records.append(list(record_dict.values()))
                mqtt_pub.publish_reading(profile["location"], m_id, record_dict)
            
            with open(RAW_DATA_FILE, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(records)
                
            print(f"[{current_time.isoformat()}] Generated {len(records)} readings.")
            time.sleep(interval_sec)
            
    except KeyboardInterrupt:
        print("\nLive simulation stopped by user.")
    finally:
        mqtt_pub.disconnect()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pharmaceutical Manufacturing Sensor Simulator")
    parser.add_argument("--mode", choices=["demo", "live"], required=True, help="Run mode (demo for historical batch, live for real-time)")
    parser.add_argument("--hours", type=int, default=DEFAULT_DEMO_HOURS, help="Number of hours to simulate (Demo mode only)")
    parser.add_argument("--interval", type=int, help="Interval in seconds between readings")
    parser.add_argument("--scenario", default=ANOMALY_NONE, help="Anomaly scenario to run (e.g. vibration_failure, high_temperature, combined_degradation)")
    parser.add_argument("--machine", default="M-004", help="Target machine for the anomaly (e.g. M-004)")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help="Random seed for reproducibility")
    parser.add_argument("--mqtt", action="store_true", help="Enable MQTT publishing")
    
    args = parser.parse_args()
    
    np.random.seed(args.seed)
    
    # Set default intervals based on mode
    interval = args.interval
    if interval is None:
        interval = DEFAULT_DEMO_INTERVAL_SEC if args.mode == "demo" else DEFAULT_LIVE_INTERVAL_SEC
        
    if args.mode == "demo":
        run_demo(args.hours, interval, args.scenario, args.machine, args.mqtt)
    else:
        run_live(interval, args.scenario, args.machine, args.mqtt)
