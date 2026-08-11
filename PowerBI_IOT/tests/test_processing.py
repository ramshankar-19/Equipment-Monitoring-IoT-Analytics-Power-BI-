import pytest
import pandas as pd
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from processing.data_processor import evaluate_status
from simulator.config import STATUS_NORMAL, STATUS_WARNING, STATUS_CRITICAL

def test_evaluate_status_normal():
    # Baseline 100, Warning 1.10, Critical 1.15
    thresholds = {"warning": 1.10, "critical": 1.15, "direction": "up"}
    assert evaluate_status(100, 100, thresholds) == STATUS_NORMAL
    assert evaluate_status(105, 100, thresholds) == STATUS_NORMAL

def test_evaluate_status_warning():
    thresholds = {"warning": 1.10, "critical": 1.15, "direction": "up"}
    assert evaluate_status(110.1, 100, thresholds) == STATUS_WARNING
    assert evaluate_status(114, 100, thresholds) == STATUS_WARNING

def test_evaluate_status_critical():
    thresholds = {"warning": 1.10, "critical": 1.15, "direction": "up"}
    assert evaluate_status(115, 100, thresholds) == STATUS_CRITICAL
    assert evaluate_status(120, 100, thresholds) == STATUS_CRITICAL

def test_evaluate_status_downward():
    # RPM drops
    thresholds = {"warning": 0.90, "critical": 0.85, "direction": "down"}
    assert evaluate_status(1000, 1000, thresholds) == STATUS_NORMAL
    assert evaluate_status(900, 1000, thresholds) == STATUS_WARNING
    assert evaluate_status(850, 1000, thresholds) == STATUS_CRITICAL
    assert evaluate_status(800, 1000, thresholds) == STATUS_CRITICAL

def test_health_score_logic():
    # Mock row evaluation mimicking the calc_overall logic
    def mock_calc_overall(statuses):
        criticals = statuses.count(STATUS_CRITICAL)
        warnings = statuses.count(STATUS_WARNING)
        score = 100 - (criticals * 20) - (warnings * 10)
        return max(0, min(100, score))

    assert mock_calc_overall([STATUS_NORMAL]*6) == 100
    assert mock_calc_overall([STATUS_WARNING, STATUS_NORMAL, STATUS_NORMAL, STATUS_NORMAL, STATUS_NORMAL, STATUS_NORMAL]) == 90
    assert mock_calc_overall([STATUS_CRITICAL, STATUS_NORMAL, STATUS_NORMAL, STATUS_NORMAL, STATUS_NORMAL, STATUS_NORMAL]) == 80
    assert mock_calc_overall([STATUS_WARNING, STATUS_WARNING, STATUS_NORMAL, STATUS_NORMAL, STATUS_NORMAL, STATUS_NORMAL]) == 80
    assert mock_calc_overall([STATUS_CRITICAL, STATUS_CRITICAL, STATUS_CRITICAL, STATUS_CRITICAL, STATUS_CRITICAL, STATUS_CRITICAL]) == 0
