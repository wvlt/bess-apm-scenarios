#!/usr/bin/env python3
"""
Demo script for BESS APM Platform Investment Analysis
Runs a quick scenario to demonstrate the simulation capabilities
"""

import sys
import os
import logging

# Add the current directory to Python path
sys.path.append(os.path.dirname(__file__))

from models.bess_models import (
    BESSAsset, MarketConditions, APMPlatformSpec, 
    SimulationParameters, BatteryChemistry
)
from simulation.monte_carlo_engine import BESSPerformanceSimulator
from examples.sample_scenarios import get_scenario, list_scenarios

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_demo_scenario():
    """Run a demonstration of the BESS APM analysis"""
    
    print("🔋 BESS APM Platform Investment Analysis - Demo")
    print("=" * 60)
    
    # Show available scenarios
    print("\nAvailable Scenarios:")
    scenarios = list_scenarios()
    for i, scenario in enumerate(scenarios, 1):
        print(f"{i}. {scenario['name']}: {scenario['description']}")
    
    # Use the NSW utility scenario for demo
    scenario_name = "nsw_utility_advanced"
    scenario = get_scenario(scenario_name)
    
    print(f"\n🎯 Running Demo Scenario: {scenario_name}")
    print(f"Description: {scenario['description']}")
    
    # Extract components
    asset = scenario["asset"]
    market = scenario["market"]
    apm = scenario["apm"]
    params = scenario["simulation"]
    
    # Reduce simulation size for demo
    demo_params = SimulationParameters(
        simulation_years=10,
        num_simulations=100,  # Reduced for demo speed
        discount_rate=params.discount_rate,
        inflation_rate=params.inflation_rate
    )
    
    print(f"\n📊 Asset Details:")
    print(f"  • Capacity: {asset.capacity_mwh} MWh")
    print(f"  • Power: {asset.power_rating_mw} MW")
    print(f"  • Chemistry: {asset.chemistry.value}")
    print(f"  • Initial Cost: ${asset.initial_cost_aud/1_000_000:.1f}M")
    
    print(f"\n💰 Market Conditions:")
    print(f"  • Average Spot Price: ${market.spot_price_avg_aud_mwh}/MWh")
    print(f"  • Price Volatility: {market.price_volatility*100:.0f}%")
    print(f"  • FCAS Price: ${market.fcas_price_avg_aud_mw_hr}/MW/hr")
    print(f"  • Capacity Factor: {market.capacity_factor*100:.0f}%")
    
    print(f"\n🖥️ APM Platform:")
    print(f"  • Name: {apm.name}")
    print(f"  • Annual Cost: ${apm.annual_cost_aud:,}")
    print(f"  • Implementation Cost: ${apm.implementation_cost_aud:,}")
    print(f"  • Predictive Maintenance Improvement: {apm.predictive_maintenance_improvement*100:.0f}%")
    print(f"  • Dispatch Optimization: {apm.dispatch_optimization_improvement*100:.0f}%")
    print(f"  • Degradation Reduction: {apm.degradation_reduction*100:.0f}%")
    
    print(f"\n🎲 Running Monte Carlo Simulation...")
    print(f"  • Simulations: {demo_params.num_simulations}")
    print(f"  • Years: {demo_params.simulation_years}")
    print(f"  • Discount Rate: {demo_params.discount_rate*100:.1f}%")
    
    # Create simulator and run
    simulator = BESSPerformanceSimulator(asset, market, apm, demo_params)
    
    try:
        results_df = simulator.run_monte_carlo()
        
        if results_df.empty:
            print("❌ Simulation failed - no results generated")
            return
        
        # Calculate key metrics
        avg_npv_diff = results_df['npv_difference'].mean()
        positive_roi_prob = (results_df['npv_difference'] > 0).mean() * 100
        avg_payback = results_df['payback_period'].mean()
        avg_irr = results_df['irr_apm'].mean() * 100
        
        # Risk metrics
        var_5 = results_df['npv_difference'].quantile(0.05)
        var_95 = results_df['npv_difference'].quantile(0.95)
        
        print(f"\n✅ Simulation Complete! Results:")
        print("=" * 40)
        
        print(f"\n💰 Financial Metrics:")
        print(f"  • Average NPV Improvement: ${avg_npv_diff/1_000_000:.1f}M")
        print(f"  • ROI vs Asset Value: {(avg_npv_diff/asset.initial_cost_aud)*100:.1f}%")
        print(f"  • Probability of Positive ROI: {positive_roi_prob:.1f}%")
        print(f"  • Average Payback Period: {avg_payback:.1f} years")
        print(f"  • Average IRR: {avg_irr:.1f}%")
        
        print(f"\n⚠️ Risk Assessment:")
        print(f"  • 5th Percentile (VaR): ${var_5/1_000_000:.1f}M")
        print(f"  • 95th Percentile: ${var_95/1_000_000:.1f}M")
        print(f"  • Range: ${(var_95-var_5)/1_000_000:.1f}M")
        
        # Performance improvements
        revenue_improvement = (results_df['total_revenue_apm'].mean() - 
                             results_df['total_revenue_base'].mean()) / results_df['total_revenue_base'].mean() * 100
        
        cost_improvement = (results_df['total_cost_base'].mean() - 
                          results_df['total_cost_apm'].mean()) / results_df['total_cost_base'].mean() * 100
        
        print(f"\n⚡ Performance Improvements:")
        print(f"  • Revenue Increase: {revenue_improvement:.1f}%")
        print(f"  • Net Cost Reduction: {cost_improvement:.1f}%")
        print(f"  • Final State of Health: {results_df['final_soh_apm'].mean()*100:.1f}%")
        print(f"  • Average Availability: {results_df['avg_availability_apm'].mean()*100:.1f}%")
        
        # Investment recommendation
        print(f"\n🎯 Investment Recommendation:")
        if positive_roi_prob >= 70 and avg_npv_diff > apm.implementation_cost_aud * 0.5:
            recommendation = "🟢 STRONG BUY - High probability of significant returns"
        elif positive_roi_prob >= 50 and avg_npv_diff > 0:
            recommendation = "🟡 CONDITIONAL BUY - Moderate returns, assess risk tolerance"
        else:
            recommendation = "🔴 AVOID - High risk of negative returns"
        
        print(f"  {recommendation}")
        
        print(f"\n📊 For detailed analysis and interactive exploration:")
        print(f"  Run: streamlit run app.py")
        print(f"  Or: ./run.sh")
        
    except Exception as e:
        logger.error(f"Simulation failed: {e}")
        print(f"❌ Demo failed: {e}")
        print("Please check the installation and try again.")

if __name__ == "__main__":
    run_demo_scenario()
