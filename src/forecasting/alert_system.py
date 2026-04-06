"""
Milestone 13: Alert System
Create rule-based alerts for high bed occupancy or oxygen demand
"""

import pandas as pd
import numpy as np
from datetime import datetime

class ResourceAlertSystem:
    """Alert system for healthcare resource monitoring."""
    
    def __init__(self):
        self.alerts = []
        self.thresholds = {
            'bed_occupancy_critical': 0.90,  # 90% occupancy
            'bed_occupancy_warning': 0.75,   # 75% occupancy
            'icu_ratio_critical': 0.80,      # 80% ICU usage
            'icu_ratio_warning': 0.60,       # 60% ICU usage
            'oxygen_critical': 100,          # High oxygen demand
            'oxygen_warning': 75             # Moderate oxygen demand
        }
    
    def check_bed_occupancy(self, current_occupancy, capacity):
        """Check bed occupancy levels."""
        occupancy_rate = current_occupancy / capacity
        
        if occupancy_rate >= self.thresholds['bed_occupancy_critical']:
            self.create_alert(
                'CRITICAL',
                'Bed Occupancy',
                f'{occupancy_rate:.1%} occupancy - CRITICAL LEVEL',
                f'{current_occupancy}/{capacity} beds occupied'
            )
        elif occupancy_rate >= self.thresholds['bed_occupancy_warning']:
            self.create_alert(
                'WARNING',
                'Bed Occupancy',
                f'{occupancy_rate:.1%} occupancy - High usage',
                f'{current_occupancy}/{capacity} beds occupied'
            )
        else:
            self.create_alert(
                'NORMAL',
                'Bed Occupancy',
                f'{occupancy_rate:.1%} occupancy - Normal',
                f'{current_occupancy}/{capacity} beds occupied'
            )
    
    def check_icu_capacity(self, icu_patients, total_icu_beds):
        """Check ICU capacity."""
        icu_rate = icu_patients / total_icu_beds
        
        if icu_rate >= self.thresholds['icu_ratio_critical']:
            self.create_alert(
                'CRITICAL',
                'ICU Capacity',
                f'{icu_rate:.1%} ICU usage - CRITICAL',
                f'{icu_patients}/{total_icu_beds} ICU beds occupied'
            )
        elif icu_rate >= self.thresholds['icu_ratio_warning']:
            self.create_alert(
                'WARNING',
                'ICU Capacity',
                f'{icu_rate:.1%} ICU usage - Monitor closely',
                f'{icu_patients}/{total_icu_beds} ICU beds occupied'
            )
    
    def check_oxygen_demand(self, oxygen_usage):
        """Check oxygen demand levels."""
        if oxygen_usage >= self.thresholds['oxygen_critical']:
            self.create_alert(
                'CRITICAL',
                'Oxygen Supply',
                f'Oxygen demand: {oxygen_usage} units - CRITICAL',
                'Immediate supply check required'
            )
        elif oxygen_usage >= self.thresholds['oxygen_warning']:
            self.create_alert(
                'WARNING',
                'Oxygen Supply',
                f'Oxygen demand: {oxygen_usage} units - Elevated',
                'Monitor supply levels'
            )
    
    def create_alert(self, severity, category, message, details):
        """Create and log an alert."""
        alert = {
            'timestamp': datetime.now(),
            'severity': severity,
            'category': category,
            'message': message,
            'details': details
        }
        self.alerts.append(alert)
        
        # Print alert
        icon = '🔴' if severity == 'CRITICAL' else '🟡' if severity == 'WARNING' else '🟢'
        print(f"\n{icon} [{severity}] {category}")
        print(f"   {message}")
        print(f"   {details}")
    
    def get_alerts(self, severity=None):
        """Retrieve alerts, optionally filtered by severity."""
        if severity:
            return [a for a in self.alerts if a['severity'] == severity]
        return self.alerts
    
    def generate_report(self):
        """Generate alert summary report."""
        print(f"\n{'='*60}")
        print("ALERT SYSTEM REPORT")
        print(f"{'='*60}")
        
        critical = len([a for a in self.alerts if a['severity'] == 'CRITICAL'])
        warning = len([a for a in self.alerts if a['severity'] == 'WARNING'])
        normal = len([a for a in self.alerts if a['severity'] == 'NORMAL'])
        
        print(f"\n📊 Alert Summary:")
        print(f"  🔴 Critical: {critical}")
        print(f"  🟡 Warning: {warning}")
        print(f"  🟢 Normal: {normal}")
        print(f"  Total: {len(self.alerts)}")
        
        if critical > 0:
            print(f"\n⚠️  IMMEDIATE ACTION REQUIRED - {critical} critical alerts")
        elif warning > 0:
            print(f"\n⚠️  Monitor closely - {warning} warnings")
        else:
            print(f"\n✅ All systems normal")
        
        return {
            'critical': critical,
            'warning': warning,
            'normal': normal,
            'total': len(self.alerts)
        }
