import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
RAW_DATA_FILE = RAW_DATA_DIR / "sensor_data.csv"

# Ensure directories exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Default Simulation Settings
DEFAULT_SEED = 42
DEFAULT_DEMO_HOURS = 24
DEFAULT_DEMO_INTERVAL_SEC = 10
DEFAULT_LIVE_INTERVAL_SEC = 2

# Status constants (for simulator tagging)
STATUS_NORMAL = "NORMAL"
STATUS_WARNING = "WARNING"
STATUS_CRITICAL = "CRITICAL"

ANOMALY_NONE = "NONE"
