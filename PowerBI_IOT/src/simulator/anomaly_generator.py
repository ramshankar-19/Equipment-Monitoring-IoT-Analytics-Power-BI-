import numpy as np

class AnomalyGenerator:
    def __init__(self, scenario_name, target_machine_id):
        self.scenario = scenario_name
        self.target_machine_id = target_machine_id
        
    def apply_anomaly(self, machine_id, current_state, elapsed_minutes):
        """
        Applies anomaly effects to the current_state if the machine matches the target.
        Returns the modified state and the anomaly type tag.
        """
        if self.scenario == "NONE" or machine_id != self.target_machine_id:
            return current_state, "NONE"
            
        anomaly_type = self.scenario
        
        # Calculate a severity multiplier based on time (gradual degradation)
        # Reaches max severity after ~120 minutes (2 hours)
        severity = min(elapsed_minutes / 120.0, 1.0)
        
        if self.scenario == "vibration_failure":
            # Vibration gradually increases, becomes critical
            current_state["vibration_mm_s"] += (severity * 5.0) 
            # Slight secondary effect on temperature
            current_state["temperature_c"] += (severity * 5.0)
            
        elif self.scenario == "high_temperature":
            # Temperature gradually increases
            current_state["temperature_c"] += (severity * 15.0)
            
        elif self.scenario == "motor_overload":
            # Current increases significantly, RPM drops slightly
            current_state["motor_current_a"] += (severity * 6.0)
            current_state["rpm"] -= (severity * 100)
            # Temperature rises due to overload
            current_state["temperature_c"] += (severity * 10.0)
            
        elif self.scenario == "high_pressure":
            # Pressure rises beyond critical
            current_state["pressure_bar"] += (severity * 2.0)
            
        elif self.scenario == "combined_degradation":
            # Temperature + vibration + motor current gradually increase together
            current_state["temperature_c"] += (severity * 12.0)
            current_state["vibration_mm_s"] += (severity * 4.0)
            current_state["motor_current_a"] += (severity * 5.0)
            current_state["rpm"] -= (severity * 50)
            
        return current_state, anomaly_type
