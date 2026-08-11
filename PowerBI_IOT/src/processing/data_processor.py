import os
import sys
import pandas as pd
import numpy as np
import datetime

# Adjust the path so we can import from simulator
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from simulator.config import (
    RAW_DATA_FILE,
    PROCESSED_DATA_DIR,
    STATUS_NORMAL,
    STATUS_WARNING,
    STATUS_CRITICAL,
)
from simulator.machine_profiles import MACHINES


PROCESSED_DATA_FILE = PROCESSED_DATA_DIR / "powerbi_sensor_data.csv"


# ============================================================
# GENERIC FALLBACK THRESHOLDS
# ============================================================
#
# These are simulated monitoring rules expressed relative to
# each machine's baseline.
#
# Individual machine profiles can override these thresholds
# where percentage-based thresholds are not appropriate.
#
# These are NOT real pharmaceutical equipment specifications.
# ============================================================

THRESHOLDS = {
    "temperature_c": {
        "warning": 1.10,
        "critical": 1.15,
        "direction": "up",
        "type": "multiplier",
    },

    "pressure_bar": {
        "warning": 1.15,
        "critical": 1.25,
        "direction": "up",
        "type": "multiplier",
    },

    "humidity_pct": {
        "warning": 1.20,
        "critical": 1.30,
        "direction": "up",
        "type": "multiplier",
    },

    "vibration_mm_s": {
        "warning": 1.50,
        "critical": 3.00,
        "direction": "up",
        "type": "multiplier",
    },

    "motor_current_a": {
        "warning": 1.20,
        "critical": 1.50,
        "direction": "up",
        "type": "multiplier",
    },

    "rpm": {
        "warning": 0.90,
        "critical": 0.85,
        "direction": "down",
        "type": "multiplier",
    },
}


# ============================================================
# STATUS EVALUATION
# ============================================================

def evaluate_status(val, baseline, thresholds):
    """
    Evaluate a sensor value against its monitoring thresholds.

    Two threshold modes are supported:

    1. multiplier:
       Thresholds are calculated relative to the machine baseline.

    2. absolute:
       Thresholds are fixed sensor values defined in the
       individual machine profile.
    """

    if pd.isna(val):
        return STATUS_NORMAL

    direction = thresholds.get("direction", "up")
    threshold_type = thresholds.get("type", "multiplier")

    # --------------------------------------------------------
    # Absolute threshold mode
    # --------------------------------------------------------
    if threshold_type == "absolute":
        warning_threshold = thresholds["warning"]
        critical_threshold = thresholds["critical"]

    # --------------------------------------------------------
    # Baseline multiplier mode
    # --------------------------------------------------------
    else:
        if baseline == 0:
            return STATUS_NORMAL

        warning_threshold = baseline * thresholds["warning"]
        critical_threshold = baseline * thresholds["critical"]

    # --------------------------------------------------------
    # Increasing sensor value indicates degradation
    # --------------------------------------------------------
    if direction == "up":

        if val >= critical_threshold:
            return STATUS_CRITICAL

        elif val >= warning_threshold:
            return STATUS_WARNING

    # --------------------------------------------------------
    # Decreasing sensor value indicates degradation
    # --------------------------------------------------------
    elif direction == "down":

        if val <= critical_threshold:
            return STATUS_CRITICAL

        elif val <= warning_threshold:
            return STATUS_WARNING

    return STATUS_NORMAL


# ============================================================
# MAIN PROCESSING FUNCTION
# ============================================================

def process_data():

    print(f"Reading raw data from {RAW_DATA_FILE}...")

    try:
        df = pd.read_csv(RAW_DATA_FILE)

    except FileNotFoundError:
        print("Raw data file not found. Run simulator first.")
        return

    initial_count = len(df)

    # ========================================================
    # 1. VALIDATION & CLEANING
    # ========================================================

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce"
    )

    # Remove records with invalid timestamps
    df = df.dropna(subset=["timestamp"])

    # Remove exact duplicate records
    df = df.drop_duplicates()

    # Numeric sensor columns
    num_cols = [
        "temperature_c",
        "pressure_bar",
        "humidity_pct",
        "vibration_mm_s",
        "motor_current_a",
        "rpm",
    ]

    # Convert numeric fields safely
    for col in num_cols:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    # Fill missing numeric values
    df[num_cols] = df[num_cols].ffill().bfill()

    # Prevent impossible negative physical measurements
    for col in num_cols:
        df[col] = df[col].apply(
            lambda x: max(0, x)
        )

    clean_count = len(df)

    # ========================================================
    # 2. DERIVE SENSOR STATUSES
    # ========================================================

    print(
        "Calculating thresholds, statuses, and health scores..."
    )

    # Initialize status columns
    for col in num_cols:
        df[f"{col}_status"] = STATUS_NORMAL

    # Initialize business-level fields
    df["overall_machine_status"] = STATUS_NORMAL
    df["health_score"] = 100
    df["alert_flag"] = 0
    df["alert_reason"] = "None"

    # ========================================================
    # 3. APPLY MACHINE-SPECIFIC THRESHOLDS
    # ========================================================

    for m_id in df["machine_id"].unique():

        if m_id not in MACHINES:
            continue

        mask = df["machine_id"] == m_id
        profile = MACHINES[m_id]

        # Optional machine-specific threshold overrides
        machine_thresholds = profile.get(
            "thresholds",
            {}
        )

        for col in num_cols:

            # ------------------------------------------------
            # Find the machine baseline
            # ------------------------------------------------

            if col == "temperature_c":

                baseline = profile.get(
                    "baseline_temp_c",
                    0
                )

            elif col == "motor_current_a":

                baseline = profile.get(
                    "baseline_current_a",
                    0
                )

            else:

                baseline = profile.get(
                    f"baseline_{col}",
                    0
                )

            # ------------------------------------------------
            # Select threshold configuration
            #
            # Machine-specific threshold if available.
            # Otherwise generic fallback.
            # ------------------------------------------------

            threshold_config = machine_thresholds.get(
                col,
                THRESHOLDS[col]
            )

            # ------------------------------------------------
            # Evaluate every reading for this machine
            # ------------------------------------------------

            df.loc[
                mask,
                f"{col}_status"
            ] = df.loc[
                mask,
                col
            ].apply(
                lambda x: evaluate_status(
                    x,
                    baseline,
                    threshold_config
                )
            )

    # ========================================================
    # 4. OVERALL STATUS + HEALTH SCORE
    # ========================================================

    def calc_overall(row):

        statuses = [
            row[f"{col}_status"]
            for col in num_cols
        ]

        criticals = statuses.count(
            STATUS_CRITICAL
        )

        warnings = statuses.count(
            STATUS_WARNING
        )

        # ----------------------------------------------------
        # Health Score
        #
        # Base score = 100
        #
        # Each CRITICAL sensor = -20
        # Each WARNING sensor  = -10
        #
        # Score is constrained between 0 and 100.
        # ----------------------------------------------------

        score = (
            100
            - (criticals * 20)
            - (warnings * 10)
        )

        score = max(
            0,
            min(100, score)
        )

        # ----------------------------------------------------
        # Overall machine status
        # ----------------------------------------------------

        overall = STATUS_NORMAL

        if criticals > 0:

            overall = STATUS_CRITICAL

        elif warnings > 0:

            overall = STATUS_WARNING

        # ----------------------------------------------------
        # Alert flag
        # ----------------------------------------------------

        alert = (
            1
            if overall != STATUS_NORMAL
            else 0
        )

        # ----------------------------------------------------
        # Alert reason
        # ----------------------------------------------------

        reason = "None"

        if alert:

            reasons = []

            for col in num_cols:

                status = row[
                    f"{col}_status"
                ]

                if status in [
                    STATUS_WARNING,
                    STATUS_CRITICAL,
                ]:

                    # Convert:
                    # temperature_c -> temperature
                    # vibration_mm_s -> vibration
                    # motor_current_a -> motor
                    # pressure_bar -> pressure
                    # humidity_pct -> humidity
                    # rpm -> rpm

                    sensor_name = (
                        col.split("_")[0]
                    )

                    reasons.append(
                        f"{sensor_name} ({status})"
                    )

            reason = " | ".join(
                reasons
            )

        return pd.Series([
            overall,
            score,
            alert,
            reason,
        ])

    # Apply calculation
    res = df.apply(
        calc_overall,
        axis=1
    )

    df[
        [
            "overall_machine_status",
            "health_score",
            "alert_flag",
            "alert_reason",
        ]
    ] = res

    # ========================================================
    # 5. PROCESSING METADATA
    # ========================================================

    df["processed_timestamp"] = (
        datetime.datetime.now().isoformat()
    )

    df["data_quality_flag"] = "CLEAN"

    # ========================================================
    # 6. CLEAN RAW SIMULATOR FIELDS
    # ========================================================

    # Rename anomaly_type to make it clear that this is
    # simulator metadata and NOT the detection mechanism.

    if "anomaly_type" in df.columns:

        df = df.rename(
            columns={
                "anomaly_type":
                "simulated_scenario"
            }
        )

    # Remove the simulator's raw operating status because
    # the processor independently calculates machine status.

    if "operating_status" in df.columns:

        df = df.drop(
            columns=["operating_status"]
        )

    # ========================================================
    # 7. SAVE PROCESSED DATA
    # ========================================================

    print(
        f"Saving processed data to {PROCESSED_DATA_FILE}..."
    )

    df.to_csv(
        PROCESSED_DATA_FILE,
        index=False
    )

    # ========================================================
    # 8. SUMMARY VALIDATION REPORT
    # ========================================================

    print("\n" + "=" * 50)
    print("PROCESSING SUMMARY REPORT")
    print("=" * 50)

    print(
        f"Total Raw Records:        {initial_count}"
    )

    print(
        f"Total Processed Records:  {clean_count}"
    )

    print(
        f"Duplicates Removed:       "
        f"{initial_count - clean_count}"
    )

    print(
        f"Unique Machines:          "
        f"{df['machine_id'].nunique()}"
    )

    print(
        f"Unique Locations:         "
        f"{df['location'].nunique()}"
    )

    print(
        f"Min Timestamp:            "
        f"{df['timestamp'].min()}"
    )

    print(
        f"Max Timestamp:            "
        f"{df['timestamp'].max()}"
    )

    print("-" * 50)

    print(
        "Overall Status Distribution:"
    )

    print(
        df["overall_machine_status"].value_counts()
    )

    print("-" * 50)

    print("Alerts by Machine:")

    alerts = df[
        df["alert_flag"] == 1
    ]

    if len(alerts) > 0:

        print(
            alerts["machine_id"]
            .value_counts()
        )

    else:

        print("No alerts detected.")

    print("=" * 50)


# ============================================================
# SCRIPT ENTRY POINT
# ============================================================

if __name__ == "__main__":
    process_data()