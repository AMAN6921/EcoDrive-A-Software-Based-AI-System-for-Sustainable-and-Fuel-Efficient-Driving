"""
Analytics and Visualization Module
Generate insights and visualizations from traffic data
"""

import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime


class TrafficAnalytics:
    """Analyze and visualize traffic optimization data"""
    
    def __init__(self, history_file: str = 'optimization_history.json'):
        """Load optimization history"""
        self.history_file = history_file
        self.data = None
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load history from JSON file"""
        if not Path(self.history_file).exists():
            print(f"⚠️  No history file found: {self.history_file}")
            return
        
        with open(self.history_file, 'r') as f:
            self.data = json.load(f)
        
        if 'history' in self.data and self.data['history']:
            self.df = pd.DataFrame(self.data['history'])
            self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
            print(f"✅ Loaded {len(self.df)} records")
        else:
            print("⚠️  No history data available")
    
    def plot_vehicle_distribution(self, save_path: str = 'results/vehicle_distribution.png'):
        """Plot vehicle count distribution"""
        if self.df is None or self.df.empty:
            print("No data to plot")
            return
        
        plt.figure(figsize=(10, 6))
        plt.hist(self.df['vehicle_count'], bins=20, color='skyblue', edgecolor='black')
        plt.xlabel('Vehicle Count')
        plt.ylabel('Frequency')
        plt.title('Vehicle Count Distribution')
        plt.grid(True, alpha=0.3)
        
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Saved: {save_path}")
    
    def plot_green_time_optimization(self, save_path: str = 'results/green_time_optimization.png'):
        """Plot green time vs vehicle count"""
        if self.df is None or self.df.empty:
            print("No data to plot")
            return
        
        plt.figure(figsize=(12, 6))
        plt.scatter(self.df['vehicle_count'], self.df['green_duration'], 
                   alpha=0.6, c=self.df['density_score'], cmap='RdYlGn_r', s=50)
        plt.colorbar(label='Density Score')
        plt.xlabel('Vehicle Count')
        plt.ylabel('Green Light Duration (seconds)')
        plt.title('Adaptive Signal Timing: Green Duration vs Traffic Density')
        plt.grid(True, alpha=0.3)
        
        # Add trend line
        z = np.polyfit(self.df['vehicle_count'], self.df['green_duration'], 2)
        p = np.poly1d(z)
        x_trend = np.linspace(self.df['vehicle_count'].min(), 
                             self.df['vehicle_count'].max(), 100)
        plt.plot(x_trend, p(x_trend), "r--", alpha=0.8, linewidth=2, label='Trend')
        plt.legend()
        
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Saved: {save_path}")
    
    def plot_time_series(self, save_path: str = 'results/time_series.png'):
        """Plot time series of vehicle counts and green times"""
        if self.df is None or self.df.empty:
            print("No data to plot")
            return
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)
        
        # Vehicle count over time
        ax1.plot(self.df['timestamp'], self.df['vehicle_count'], 
                color='blue', linewidth=1.5, marker='o', markersize=3)
        ax1.set_ylabel('Vehicle Count', fontsize=12)
        ax1.set_title('Traffic Flow Over Time', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.fill_between(self.df['timestamp'], self.df['vehicle_count'], 
                         alpha=0.3, color='blue')
        
        # Green duration over time
        ax2.plot(self.df['timestamp'], self.df['green_duration'], 
                color='green', linewidth=1.5, marker='s', markersize=3)
        ax2.set_xlabel('Time', fontsize=12)
        ax2.set_ylabel('Green Duration (s)', fontsize=12)
        ax2.set_title('Optimized Signal Timing', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.fill_between(self.df['timestamp'], self.df['green_duration'], 
                         alpha=0.3, color='green')
        
        plt.tight_layout()
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Saved: {save_path}")
    
    def plot_density_heatmap(self, save_path: str = 'results/density_heatmap.png'):
        """Plot density score heatmap"""
        if self.df is None or self.df.empty:
            print("No data to plot")
            return
        
        # Create bins for vehicle count and green duration
        self.df['vehicle_bin'] = pd.cut(self.df['vehicle_count'], bins=10)
        self.df['green_bin'] = pd.cut(self.df['green_duration'], bins=10)
        
        # Create pivot table
        pivot = self.df.pivot_table(
            values='density_score',
            index='vehicle_bin',
            columns='green_bin',
            aggfunc='mean'
        )
        
        plt.figure(figsize=(12, 8))
        sns.heatmap(pivot, annot=True, fmt='.2f', cmap='RdYlGn_r', 
                   cbar_kws={'label': 'Density Score'})
        plt.xlabel('Green Duration (seconds)')
        plt.ylabel('Vehicle Count')
        plt.title('Traffic Density Heatmap')
        plt.tight_layout()
        
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Saved: {save_path}")
    
    def generate_report(self, output_path: str = 'results/report.txt'):
        """Generate text report with statistics"""
        if self.df is None or self.df.empty:
            print("No data for report")
            return
        
        report = []
        report.append("="*60)
        report.append("TRAFFIC OPTIMIZATION ANALYTICS REPORT")
        report.append("="*60)
        report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total Records: {len(self.df)}")
        
        report.append("\n" + "-"*60)
        report.append("VEHICLE STATISTICS")
        report.append("-"*60)
        report.append(f"Average Vehicles: {self.df['vehicle_count'].mean():.1f}")
        report.append(f"Max Vehicles: {self.df['vehicle_count'].max()}")
        report.append(f"Min Vehicles: {self.df['vehicle_count'].min()}")
        report.append(f"Std Deviation: {self.df['vehicle_count'].std():.2f}")
        
        report.append("\n" + "-"*60)
        report.append("SIGNAL TIMING OPTIMIZATION")
        report.append("-"*60)
        report.append(f"Average Green Time: {self.df['green_duration'].mean():.1f}s")
        report.append(f"Max Green Time: {self.df['green_duration'].max():.0f}s")
        report.append(f"Min Green Time: {self.df['green_duration'].min():.0f}s")
        report.append(f"Std Deviation: {self.df['green_duration'].std():.2f}s")
        
        report.append("\n" + "-"*60)
        report.append("DENSITY ANALYSIS")
        report.append("-"*60)
        report.append(f"Average Density Score: {self.df['density_score'].mean():.3f}")
        report.append(f"High Density Events (>0.7): {(self.df['density_score'] > 0.7).sum()}")
        report.append(f"Low Density Events (<0.3): {(self.df['density_score'] < 0.3).sum()}")
        
        # Correlation
        corr = self.df['vehicle_count'].corr(self.df['green_duration'])
        report.append("\n" + "-"*60)
        report.append("OPTIMIZATION EFFECTIVENESS")
        report.append("-"*60)
        report.append(f"Correlation (Vehicles vs Green Time): {corr:.3f}")
        report.append("(Higher correlation indicates better adaptive response)")
        
        report.append("\n" + "="*60)
        
        report_text = "\n".join(report)
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(report_text)
        
        print(report_text)
        print(f"\n✅ Report saved: {output_path}")
    
    def generate_all_visualizations(self):
        """Generate all visualizations and report"""
        print("\n📊 Generating analytics...")
        
        self.plot_vehicle_distribution()
        self.plot_green_time_optimization()
        self.plot_time_series()
        self.plot_density_heatmap()
        self.generate_report()
        
        print("\n✅ All visualizations generated in 'results/' directory")


if __name__ == "__main__":
    analytics = TrafficAnalytics()
    analytics.generate_all_visualizations()
