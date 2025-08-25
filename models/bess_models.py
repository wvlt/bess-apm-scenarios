"""
BESS Asset Models for APM Platform Impact Analysis
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import numpy as np
from enum import Enum


class BatteryChemistry(Enum):
    LFP = "Lithium Iron Phosphate"
    NMC = "Nickel Manganese Cobalt"
    LTO = "Lithium Titanate"


class OperatingMode(Enum):
    ENERGY_ARBITRAGE = "energy_arbitrage"
    FREQUENCY_RESPONSE = "frequency_response"
    PEAK_SHAVING = "peak_shaving"
    BACKUP_POWER = "backup_power"


@dataclass
class BESSAsset:
    """Represents a Battery Energy Storage System asset"""
    name: str
    capacity_mwh: float  # Total energy capacity
    power_rating_mw: float  # Maximum power output
    chemistry: BatteryChemistry
    commissioning_date: str
    initial_cost_aud: float
    
    # Performance characteristics
    round_trip_efficiency: float = 0.85  # Default 85%
    degradation_rate_annual: float = 0.02  # 2% per year
    cycle_life_design: int = 6000  # Design cycles
    calendar_life_years: int = 15
    
    # Operating parameters
    depth_of_discharge_max: float = 0.9  # Maximum DOD
    c_rate_max: float = 1.0  # Maximum C-rate
    operating_temp_range: tuple = (-10, 45)  # Celsius
    
    # Current state (for simulation)
    current_soh: float = 1.0  # State of Health (0-1)
    current_age_years: float = 0.0
    total_cycles: int = 0
    

@dataclass
class MarketConditions:
    """Market conditions affecting BESS revenue"""
    spot_price_avg_aud_mwh: float = 85.0
    price_volatility: float = 0.3  # Standard deviation
    fcas_price_avg_aud_mw_hr: float = 12.0
    capacity_factor: float = 0.35  # How often the asset is utilized
    
    # AEMO dispatch patterns
    dispatch_efficiency: float = 0.8  # How well we respond to dispatch
    missed_dispatch_penalty_rate: float = 0.05  # 5% revenue penalty


@dataclass
class APMPlatformSpec:
    """APM Platform specifications and capabilities"""
    name: str
    annual_cost_aud: float
    implementation_cost_aud: float
    
    # Performance improvements
    predictive_maintenance_improvement: float = 0.15  # 15% reduction in unplanned downtime
    dispatch_optimization_improvement: float = 0.12  # 12% better dispatch response
    degradation_reduction: float = 0.08  # 8% slower degradation
    efficiency_improvement: float = 0.03  # 3% efficiency gain
    
    # Risk reduction
    fire_risk_reduction: float = 0.25  # 25% reduction in fire risk
    thermal_runaway_prevention: float = 0.30  # 30% better thermal management
    
    # Operational benefits
    maintenance_cost_reduction: float = 0.20  # 20% reduction in maintenance costs
    operator_efficiency_gain: float = 0.15  # 15% operator efficiency improvement


@dataclass
class SimulationParameters:
    """Parameters for Monte Carlo simulation"""
    simulation_years: int = 15
    num_simulations: int = 1000
    confidence_intervals: List[float] = field(default_factory=lambda: [0.05, 0.25, 0.5, 0.75, 0.95])
    
    # Economic parameters
    discount_rate: float = 0.08  # 8% discount rate
    inflation_rate: float = 0.025  # 2.5% inflation
    
    # Risk parameters
    unplanned_downtime_base: float = 0.05  # 5% annual downtime without APM
    maintenance_cost_base_percent: float = 0.03  # 3% of asset value annually
    major_failure_probability: float = 0.01  # 1% chance per year
    major_failure_cost_multiplier: float = 0.1  # 10% of asset value


@dataclass
class FinancialMetrics:
    """Financial performance metrics"""
    annual_revenue_base: float = 0.0
    annual_revenue_with_apm: float = 0.0
    annual_costs_base: float = 0.0
    annual_costs_with_apm: float = 0.0
    
    npv_base: float = 0.0
    npv_with_apm: float = 0.0
    npv_difference: float = 0.0
    
    roi: float = 0.0
    payback_period_years: float = 0.0
    irr: float = 0.0
    
    # Risk metrics
    value_at_risk_5_percent: float = 0.0
    expected_shortfall: float = 0.0
