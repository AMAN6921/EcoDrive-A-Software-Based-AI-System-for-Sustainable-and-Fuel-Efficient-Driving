"""
ML-based Traffic Signal Optimization Module
Dynamically calculates optimal signal timings based on traffic density
"""

import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass
import json
from datetime import datetime


@dataclass
class SignalTiming:
    """Traffic signal timing configuration"""
    green_duration: float  # seconds
    yellow_duration: float = 3.0  # seconds
    red_duration: float = 0.0  # calculated based on other lanes
    
    
class TrafficSignalOptimizer:
    """Optimizes traffic signal timings based on real-time density"""
    
    def __init__(self, 
                 min_green: float = 10.0,
                 max_green: float = 90.0,
                 base_green: float = 30.0):
        """
        Initialize optimizer
        
        Args:
            min_green: Minimum green light duration (seconds)
            max_green: Maximum green light duration (seconds)
            base_green: Base green light duration for medium traffic
        """
        self.min_green = min_green
        self.max_green = max_green
        self.base_green = base_green
        self.history = []
        
    def calculate_optimal_timing(self, 
                                 vehicle_count: int,
                                 density_score: float,
                                 lane_id: str = "main") -> SignalTiming:
        """
        Calculate optimal signal timing based on traffic conditions
        
        Args:
            vehicle_count: Number of vehicles detected
            density_score: Normalized density score (0-1)
            lane_id: Identifier for the lane
            
        Returns:
            SignalTiming object with optimized durations
        """
        # Dynamic green time calculation
        # Formula: base_time + (density_score * adjustment_range)
        adjustment_range = self.max_green - self.base_green
        green_duration = self.base_green + (density_score * adjustment_range)
        
        # Apply bounds
        green_duration = max(self.min_green, min(self.max_green, green_duration))
        
        # Round to nearest 5 seconds for practical implementation
        green_duration = round(green_duration / 5) * 5
        
        timing = SignalTiming(green_duration=green_duration)
        
        # Log decision
        self._log_decision(lane_id, vehicle_count, density_score, timing)
        
        return timing
    
    def calculate_multi_lane_timing(self, 
                                    lane_densities: Dict[str, Tuple[int, float]]) -> Dict[str, SignalTiming]:
        """
        Calculate optimal timings for multiple lanes at an intersection
        
        Args:
            lane_densities: Dict mapping lane_id to (vehicle_count, density_score)
            
        Returns:
            Dict mapping lane_id to SignalTiming
        """
        timings = {}
        total_cycle_time = 0
        
        # Calculate individual timings
        for lane_id, (vehicle_count, density_score) in lane_densities.items():
            timing = self.calculate_optimal_timing(vehicle_count, density_score, lane_id)
            timings[lane_id] = timing
            total_cycle_time += timing.green_duration + timing.yellow_duration
        
        # Set red durations (time when other lanes have green)
        for lane_id in timings:
            own_time = timings[lane_id].green_duration + timings[lane_id].yellow_duration
            timings[lane_id].red_duration = total_cycle_time - own_time
        
        return timings
    
    def estimate_fuel_savings(self, 
                             vehicle_count: int,
                             optimized_green: float,
                             fixed_green: float = 60.0) -> Dict[str, float]:
        """
        Estimate fuel and emission savings from optimization
        
        Args:
            vehicle_count: Number of vehicles
            optimized_green: Optimized green duration
            fixed_green: Traditional fixed green duration
            
        Returns:
            Dict with savings estimates
        """
        # Average idle fuel consumption: 0.6 liters/hour = 0.0001667 L/second
        idle_fuel_rate = 0.0001667  # L/second per vehicle
        
        # Average CO2 emission: 2.3 kg per liter of gasoline
        co2_per_liter = 2.3  # kg
        
        # Calculate wait time reduction
        # Simplified model: vehicles wait on average half the red time
        fixed_wait = (120 - fixed_green) / 2  # Assume 120s cycle
        optimized_wait = (120 - optimized_green) / 2
        wait_reduction = fixed_wait - optimized_wait
        
        # Calculate savings
        fuel_saved = vehicle_count * wait_reduction * idle_fuel_rate  # liters
        co2_saved = fuel_saved * co2_per_liter  # kg
        
        # Calculate percentage improvements
        fuel_reduction_pct = (wait_reduction / fixed_wait) * 100 if fixed_wait > 0 else 0
        
        return {
            'fuel_saved_liters': round(fuel_saved, 3),
            'co2_saved_kg': round(co2_saved, 3),
            'wait_time_reduction_sec': round(wait_reduction, 1),
            'fuel_reduction_percent': round(fuel_reduction_pct, 1)
        }
    
    def _log_decision(self, lane_id: str, vehicle_count: int, 
                     density_score: float, timing: SignalTiming):
        """Log optimization decision for analysis"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'lane_id': lane_id,
            'vehicle_count': vehicle_count,
            'density_score': round(density_score, 3),
            'green_duration': timing.green_duration
        }
        self.history.append(entry)
    
    def get_statistics(self) -> Dict:
        """Get optimization statistics"""
        if not self.history:
            return {}
        
        green_times = [entry['green_duration'] for entry in self.history]
        vehicle_counts = [entry['vehicle_count'] for entry in self.history]
        
        return {
            'total_decisions': len(self.history),
            'avg_green_time': round(np.mean(green_times), 1),
            'min_green_time': min(green_times),
            'max_green_time': max(green_times),
            'avg_vehicle_count': round(np.mean(vehicle_counts), 1)
        }
    
    def save_history(self, filepath: str = 'optimization_history.json'):
        """Save optimization history to file"""
        with open(filepath, 'w') as f:
            json.dump({
                'history': self.history,
                'statistics': self.get_statistics()
            }, f, indent=2)
        print(f"✅ History saved to {filepath}")
