"""
Sample BESS APM Investment Scenarios
Realistic examples based on Australian market conditions
"""

from models.bess_models import (
    BESSAsset, MarketConditions, APMPlatformSpec, 
    SimulationParameters, BatteryChemistry
)

# Sample BESS Assets
SAMPLE_ASSETS = {
    "utility_scale_lfp": BESSAsset(
        name="Utility Scale LFP BESS",
        capacity_mwh=100.0,
        power_rating_mw=50.0,
        chemistry=BatteryChemistry.LFP,
        commissioning_date="2024-01-01",
        initial_cost_aud=80_000_000,  # $800/kWh
        round_trip_efficiency=0.85,
        degradation_rate_annual=0.02,
        cycle_life_design=8000,
        calendar_life_years=15
    ),
    
    "commercial_nmc": BESSAsset(
        name="Commercial NMC BESS",
        capacity_mwh=20.0,
        power_rating_mw=10.0,
        chemistry=BatteryChemistry.NMC,
        commissioning_date="2024-01-01",
        initial_cost_aud=18_000_000,  # $900/kWh
        round_trip_efficiency=0.88,
        degradation_rate_annual=0.025,
        cycle_life_design=6000,
        calendar_life_years=12
    ),
    
    "grid_scale_lfp": BESSAsset(
        name="Grid Scale LFP BESS",
        capacity_mwh=500.0,
        power_rating_mw=200.0,
        chemistry=BatteryChemistry.LFP,
        commissioning_date="2024-01-01",
        initial_cost_aud=350_000_000,  # $700/kWh (economies of scale)
        round_trip_efficiency=0.87,
        degradation_rate_annual=0.018,
        cycle_life_design=10000,
        calendar_life_years=20
    ),
    
    "frequency_response_lto": BESSAsset(
        name="Fast Response LTO BESS",
        capacity_mwh=10.0,
        power_rating_mw=20.0,  # High power density
        chemistry=BatteryChemistry.LTO,
        commissioning_date="2024-01-01",
        initial_cost_aud=15_000_000,  # $1500/kWh (premium for LTO)
        round_trip_efficiency=0.92,
        degradation_rate_annual=0.01,
        cycle_life_design=20000,
        calendar_life_years=25
    )
}

# Market Scenarios
MARKET_SCENARIOS = {
    "high_volatility_nsw": MarketConditions(
        spot_price_avg_aud_mwh=95.0,
        price_volatility=0.45,
        fcas_price_avg_aud_mw_hr=15.0,
        capacity_factor=0.40,
        dispatch_efficiency=0.75,  # Challenging market
        missed_dispatch_penalty_rate=0.08
    ),
    
    "stable_vic": MarketConditions(
        spot_price_avg_aud_mwh=75.0,
        price_volatility=0.25,
        fcas_price_avg_aud_mw_hr=10.0,
        capacity_factor=0.35,
        dispatch_efficiency=0.85,
        missed_dispatch_penalty_rate=0.03
    ),
    
    "renewable_heavy_sa": MarketConditions(
        spot_price_avg_aud_mwh=110.0,
        price_volatility=0.55,
        fcas_price_avg_aud_mw_hr=20.0,
        capacity_factor=0.45,
        dispatch_efficiency=0.70,  # High variability
        missed_dispatch_penalty_rate=0.10
    ),
    
    "coal_transition_qld": MarketConditions(
        spot_price_avg_aud_mwh=85.0,
        price_volatility=0.35,
        fcas_price_avg_aud_mw_hr=12.0,
        capacity_factor=0.30,
        dispatch_efficiency=0.80,
        missed_dispatch_penalty_rate=0.05
    )
}

# APM Platform Specifications
APM_PLATFORMS = {
    "basic_monitoring": APMPlatformSpec(
        name="Basic Monitoring Platform",
        annual_cost_aud=150_000,
        implementation_cost_aud=400_000,
        predictive_maintenance_improvement=0.08,
        dispatch_optimization_improvement=0.05,
        degradation_reduction=0.03,
        efficiency_improvement=0.01,
        fire_risk_reduction=0.15,
        thermal_runaway_prevention=0.20,
        maintenance_cost_reduction=0.12,
        operator_efficiency_gain=0.10
    ),
    
    "advanced_analytics": APMPlatformSpec(
        name="Advanced Analytics Platform",
        annual_cost_aud=400_000,
        implementation_cost_aud=1_000_000,
        predictive_maintenance_improvement=0.15,
        dispatch_optimization_improvement=0.12,
        degradation_reduction=0.08,
        efficiency_improvement=0.03,
        fire_risk_reduction=0.25,
        thermal_runaway_prevention=0.30,
        maintenance_cost_reduction=0.20,
        operator_efficiency_gain=0.15
    ),
    
    "ai_powered_enterprise": APMPlatformSpec(
        name="AI-Powered Enterprise Platform",
        annual_cost_aud=750_000,
        implementation_cost_aud=2_000_000,
        predictive_maintenance_improvement=0.25,
        dispatch_optimization_improvement=0.18,
        degradation_reduction=0.12,
        efficiency_improvement=0.05,
        fire_risk_reduction=0.35,
        thermal_runaway_prevention=0.40,
        maintenance_cost_reduction=0.30,
        operator_efficiency_gain=0.25
    ),
    
    "vendor_specific_premium": APMPlatformSpec(
        name="Vendor-Specific Premium Solution",
        annual_cost_aud=600_000,
        implementation_cost_aud=1_500_000,
        predictive_maintenance_improvement=0.22,
        dispatch_optimization_improvement=0.16,
        degradation_reduction=0.10,
        efficiency_improvement=0.04,
        fire_risk_reduction=0.30,
        thermal_runaway_prevention=0.35,
        maintenance_cost_reduction=0.25,
        operator_efficiency_gain=0.20
    )
}

# Simulation Configurations
SIMULATION_CONFIGS = {
    "quick_assessment": SimulationParameters(
        simulation_years=10,
        num_simulations=500,
        confidence_intervals=[0.1, 0.25, 0.5, 0.75, 0.9],
        discount_rate=0.08,
        inflation_rate=0.025,
        unplanned_downtime_base=0.05,
        maintenance_cost_base_percent=0.03,
        major_failure_probability=0.01,
        major_failure_cost_multiplier=0.1
    ),
    
    "detailed_analysis": SimulationParameters(
        simulation_years=15,
        num_simulations=2000,
        confidence_intervals=[0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95],
        discount_rate=0.08,
        inflation_rate=0.025,
        unplanned_downtime_base=0.05,
        maintenance_cost_base_percent=0.03,
        major_failure_probability=0.015,
        major_failure_cost_multiplier=0.12
    ),
    
    "conservative_planning": SimulationParameters(
        simulation_years=20,
        num_simulations=1000,
        confidence_intervals=[0.05, 0.25, 0.5, 0.75, 0.95],
        discount_rate=0.10,  # Higher discount rate
        inflation_rate=0.03,
        unplanned_downtime_base=0.08,  # More conservative
        maintenance_cost_base_percent=0.04,
        major_failure_probability=0.02,
        major_failure_cost_multiplier=0.15
    ),
    
    "aggressive_growth": SimulationParameters(
        simulation_years=15,
        num_simulations=1500,
        confidence_intervals=[0.05, 0.25, 0.5, 0.75, 0.95],
        discount_rate=0.06,  # Lower discount rate
        inflation_rate=0.02,
        unplanned_downtime_base=0.03,  # Optimistic
        maintenance_cost_base_percent=0.025,
        major_failure_probability=0.008,
        major_failure_cost_multiplier=0.08
    )
}

# Predefined Scenario Combinations
COMPLETE_SCENARIOS = {
    "nsw_utility_advanced": {
        "asset": SAMPLE_ASSETS["utility_scale_lfp"],
        "market": MARKET_SCENARIOS["high_volatility_nsw"],
        "apm": APM_PLATFORMS["advanced_analytics"],
        "simulation": SIMULATION_CONFIGS["detailed_analysis"],
        "description": "100 MWh utility scale BESS in NSW with advanced APM platform"
    },
    
    "vic_commercial_basic": {
        "asset": SAMPLE_ASSETS["commercial_nmc"],
        "market": MARKET_SCENARIOS["stable_vic"],
        "apm": APM_PLATFORMS["basic_monitoring"],
        "simulation": SIMULATION_CONFIGS["quick_assessment"],
        "description": "20 MWh commercial BESS in Victoria with basic monitoring"
    },
    
    "sa_grid_scale_enterprise": {
        "asset": SAMPLE_ASSETS["grid_scale_lfp"],
        "market": MARKET_SCENARIOS["renewable_heavy_sa"],
        "apm": APM_PLATFORMS["ai_powered_enterprise"],
        "simulation": SIMULATION_CONFIGS["detailed_analysis"],
        "description": "500 MWh grid-scale BESS in SA with AI-powered enterprise APM"
    },
    
    "qld_frequency_premium": {
        "asset": SAMPLE_ASSETS["frequency_response_lto"],
        "market": MARKET_SCENARIOS["coal_transition_qld"],
        "apm": APM_PLATFORMS["vendor_specific_premium"],
        "simulation": SIMULATION_CONFIGS["conservative_planning"],
        "description": "10 MWh fast-response LTO BESS in Queensland with premium APM"
    }
}

def get_scenario(scenario_name: str) -> dict:
    """Get a complete predefined scenario"""
    if scenario_name not in COMPLETE_SCENARIOS:
        raise ValueError(f"Scenario '{scenario_name}' not found. Available: {list(COMPLETE_SCENARIOS.keys())}")
    
    return COMPLETE_SCENARIOS[scenario_name]

def list_scenarios() -> list:
    """List all available predefined scenarios"""
    return [
        {
            "name": name,
            "description": scenario["description"],
            "asset_capacity": scenario["asset"].capacity_mwh,
            "asset_cost": scenario["asset"].initial_cost_aud / 1_000_000,  # Convert to millions
            "apm_annual_cost": scenario["apm"].annual_cost_aud,
            "market_price": scenario["market"].spot_price_avg_aud_mwh
        }
        for name, scenario in COMPLETE_SCENARIOS.items()
    ]

if __name__ == "__main__":
    # Demo: Print all available scenarios
    print("Available BESS APM Investment Scenarios:")
    print("=" * 50)
    
    for scenario_info in list_scenarios():
        print(f"\n{scenario_info['name'].upper()}")
        print(f"Description: {scenario_info['description']}")
        print(f"Asset Capacity: {scenario_info['asset_capacity']} MWh")
        print(f"Asset Cost: ${scenario_info['asset_cost']:.1f}M")
        print(f"APM Annual Cost: ${scenario_info['apm_annual_cost']:,}")
        print(f"Market Price: ${scenario_info['market_price']}/MWh")
