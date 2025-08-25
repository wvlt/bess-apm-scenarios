"""
BESS APM Platform Impact Analysis Dashboard
Interactive Monte Carlo Simulation for Investment Decision Making
"""
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import logging
from typing import Dict, List

# Configure logging
logging.basicConfig(level=logging.INFO)

# Import our custom modules
import sys
import os
sys.path.append(os.path.dirname(__file__))

from models.bess_models import (
    BESSAsset, MarketConditions, APMPlatformSpec, 
    SimulationParameters, BatteryChemistry, OperatingMode
)
from simulation.monte_carlo_engine import BESSPerformanceSimulator


def main():
    st.set_page_config(
        page_title="BESS APM Platform ROI Analysis",
        page_icon="🔋",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🔋 BESS APM Platform Investment Analysis")
    st.markdown("""
    **Monte Carlo Simulation for Battery Energy Storage System (BESS) Asset Performance Management Platform ROI**
    
    This tool helps you evaluate the financial impact of investing in an APM platform for your BESS assets.
    Adjust the parameters in the sidebar to see how different scenarios affect your ROI.
    """)
    
    # Sidebar for inputs
    st.sidebar.header("📊 Simulation Parameters")
    
    # BESS Asset Configuration
    st.sidebar.subheader("🔋 BESS Asset Configuration")
    
    asset_name = st.sidebar.text_input("Asset Name", "BESS-Site-01")
    capacity_mwh = st.sidebar.slider("Capacity (MWh)", 10, 500, 100, 10)
    power_rating_mw = st.sidebar.slider("Power Rating (MW)", 5, 200, 50, 5)
    
    chemistry = st.sidebar.selectbox(
        "Battery Chemistry",
        options=[chem.value for chem in BatteryChemistry],
        index=0
    )
    
    initial_cost_aud = st.sidebar.number_input(
        "Initial Asset Cost (AUD Million)", 
        min_value=10.0, 
        max_value=1000.0, 
        value=float(capacity_mwh * 0.8),  # Rough estimate
        step=10.0
    ) * 1_000_000
    
    # Performance parameters
    st.sidebar.subheader("⚡ Performance Parameters")
    round_trip_efficiency = st.sidebar.slider("Round Trip Efficiency", 0.70, 0.95, 0.85, 0.01)
    degradation_rate = st.sidebar.slider("Annual Degradation Rate", 0.01, 0.05, 0.02, 0.001)
    
    # Market Conditions
    st.sidebar.subheader("💰 Market Conditions")
    spot_price_avg = st.sidebar.slider("Average Spot Price (AUD/MWh)", 50, 200, 85, 5)
    price_volatility = st.sidebar.slider("Price Volatility", 0.1, 0.8, 0.3, 0.05)
    fcas_price = st.sidebar.slider("FCAS Price (AUD/MW/hr)", 5, 30, 12, 1)
    capacity_factor = st.sidebar.slider("Capacity Factor", 0.2, 0.8, 0.35, 0.05)
    
    # APM Platform Configuration
    st.sidebar.subheader("🖥️ APM Platform Configuration")
    
    apm_platforms = {
        "Basic APM": {"annual": 200_000, "implementation": 500_000, "benefits": "low"},
        "Advanced APM": {"annual": 500_000, "implementation": 1_200_000, "benefits": "medium"},
        "Enterprise APM": {"annual": 800_000, "implementation": 2_000_000, "benefits": "high"},
        "Custom": {"annual": 0, "implementation": 0, "benefits": "custom"}
    }
    
    selected_platform = st.sidebar.selectbox("APM Platform Type", list(apm_platforms.keys()))
    
    if selected_platform == "Custom":
        apm_annual_cost = st.sidebar.number_input("Annual Cost (AUD)", 0, 2_000_000, 400_000, 50_000)
        apm_implementation_cost = st.sidebar.number_input("Implementation Cost (AUD)", 0, 5_000_000, 1_000_000, 100_000)
        
        # Custom benefits
        st.sidebar.write("**APM Benefits (%)**")
        predictive_maintenance = st.sidebar.slider("Predictive Maintenance Improvement", 0.0, 0.5, 0.15, 0.01)
        dispatch_optimization = st.sidebar.slider("Dispatch Optimization", 0.0, 0.3, 0.12, 0.01)
        degradation_reduction = st.sidebar.slider("Degradation Reduction", 0.0, 0.2, 0.08, 0.01)
        maintenance_cost_reduction = st.sidebar.slider("Maintenance Cost Reduction", 0.0, 0.4, 0.20, 0.01)
    else:
        platform_config = apm_platforms[selected_platform]
        apm_annual_cost = platform_config["annual"]
        apm_implementation_cost = platform_config["implementation"]
        
        # Predefined benefits based on platform tier
        if platform_config["benefits"] == "low":
            predictive_maintenance, dispatch_optimization, degradation_reduction, maintenance_cost_reduction = 0.10, 0.08, 0.05, 0.15
        elif platform_config["benefits"] == "medium":
            predictive_maintenance, dispatch_optimization, degradation_reduction, maintenance_cost_reduction = 0.15, 0.12, 0.08, 0.20
        else:  # high
            predictive_maintenance, dispatch_optimization, degradation_reduction, maintenance_cost_reduction = 0.25, 0.18, 0.12, 0.30
    
    # Simulation Parameters
    st.sidebar.subheader("🎲 Simulation Settings")
    num_simulations = st.sidebar.slider("Number of Simulations", 100, 5000, 1000, 100)
    simulation_years = st.sidebar.slider("Analysis Period (Years)", 5, 25, 15, 1)
    discount_rate = st.sidebar.slider("Discount Rate", 0.05, 0.15, 0.08, 0.005)
    
    # Run simulation button
    if st.sidebar.button("🚀 Run Analysis", type="primary"):
        run_simulation(
            asset_name, capacity_mwh, power_rating_mw, chemistry, initial_cost_aud,
            round_trip_efficiency, degradation_rate, spot_price_avg, price_volatility,
            fcas_price, capacity_factor, apm_annual_cost, apm_implementation_cost,
            predictive_maintenance, dispatch_optimization, degradation_reduction,
            maintenance_cost_reduction, num_simulations, simulation_years, discount_rate
        )


def run_simulation(asset_name, capacity_mwh, power_rating_mw, chemistry, initial_cost_aud,
                  round_trip_efficiency, degradation_rate, spot_price_avg, price_volatility,
                  fcas_price, capacity_factor, apm_annual_cost, apm_implementation_cost,
                  predictive_maintenance, dispatch_optimization, degradation_reduction,
                  maintenance_cost_reduction, num_simulations, simulation_years, discount_rate):
    """Run the Monte Carlo simulation and display results"""
    
    # Create asset, market, and APM objects
    asset = BESSAsset(
        name=asset_name,
        capacity_mwh=capacity_mwh,
        power_rating_mw=power_rating_mw,
        chemistry=BatteryChemistry.LFP,  # Default
        commissioning_date="2024-01-01",
        initial_cost_aud=initial_cost_aud,
        round_trip_efficiency=round_trip_efficiency,
        degradation_rate_annual=degradation_rate
    )
    
    market = MarketConditions(
        spot_price_avg_aud_mwh=spot_price_avg,
        price_volatility=price_volatility,
        fcas_price_avg_aud_mw_hr=fcas_price,
        capacity_factor=capacity_factor
    )
    
    apm = APMPlatformSpec(
        name="Selected APM Platform",
        annual_cost_aud=apm_annual_cost,
        implementation_cost_aud=apm_implementation_cost,
        predictive_maintenance_improvement=predictive_maintenance,
        dispatch_optimization_improvement=dispatch_optimization,
        degradation_reduction=degradation_reduction,
        maintenance_cost_reduction=maintenance_cost_reduction
    )
    
    params = SimulationParameters(
        simulation_years=simulation_years,
        num_simulations=num_simulations,
        discount_rate=discount_rate
    )
    
    # Run simulation
    with st.spinner("Running Monte Carlo simulation... This may take a moment."):
        simulator = BESSPerformanceSimulator(asset, market, apm, params)
        results_df = simulator.run_monte_carlo()
    
    if results_df.empty:
        st.error("Simulation failed to produce results. Please check your parameters.")
        return
    
    # Display results
    display_results(results_df, asset, apm)


def display_results(results_df: pd.DataFrame, asset: BESSAsset, apm: APMPlatformSpec):
    """Display simulation results with charts and metrics"""
    
    st.header("📈 Simulation Results")
    
    # Key Metrics Summary
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_npv_diff = results_df['npv_difference'].mean()
        st.metric(
            "Average NPV Improvement", 
            f"${avg_npv_diff/1_000_000:.1f}M",
            f"{(avg_npv_diff/asset.initial_cost_aud)*100:.1f}% of asset value"
        )
    
    with col2:
        positive_roi_prob = (results_df['npv_difference'] > 0).mean() * 100
        st.metric("Probability of Positive ROI", f"{positive_roi_prob:.1f}%")
    
    with col3:
        avg_payback = results_df['payback_period'].mean()
        st.metric("Average Payback Period", f"{avg_payback:.1f} years")
    
    with col4:
        avg_irr = results_df['irr_apm'].mean() * 100
        st.metric("Average IRR", f"{avg_irr:.1f}%")
    
    # NPV Distribution Chart
    st.subheader("💰 NPV Improvement Distribution")
    
    fig_npv = px.histogram(
        results_df, 
        x='npv_difference',
        nbins=50,
        title="Distribution of NPV Improvement (APM vs No APM)",
        labels={'npv_difference': 'NPV Difference (AUD)', 'count': 'Frequency'}
    )
    fig_npv.add_vline(x=0, line_dash="dash", line_color="red", annotation_text="Break-even")
    fig_npv.add_vline(x=avg_npv_diff, line_dash="dash", line_color="green", annotation_text="Mean")
    st.plotly_chart(fig_npv, use_container_width=True)
    
    # Risk Analysis
    st.subheader("⚠️ Risk Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Value at Risk
        var_5 = np.percentile(results_df['npv_difference'], 5)
        var_25 = np.percentile(results_df['npv_difference'], 25)
        
        st.write("**Value at Risk (VaR)**")
        st.write(f"5th percentile: ${var_5/1_000_000:.1f}M")
        st.write(f"25th percentile: ${var_25/1_000_000:.1f}M")
        
        if var_5 < -apm.implementation_cost_aud:
            st.warning("⚠️ Risk of significant loss detected")
    
    with col2:
        # Confidence intervals
        percentiles = [5, 25, 50, 75, 95]
        confidence_data = []
        
        for p in percentiles:
            value = np.percentile(results_df['npv_difference'], p)
            confidence_data.append({"Percentile": f"{p}th", "NPV Difference (M AUD)": value/1_000_000})
        
        confidence_df = pd.DataFrame(confidence_data)
        st.write("**Confidence Intervals**")
        st.dataframe(confidence_df, use_container_width=True)
    
    # Performance Comparison
    st.subheader("⚡ Performance Comparison")
    
    # Create performance metrics comparison
    performance_metrics = {
        "Metric": ["Total Revenue", "Total Costs", "Final State of Health", "Average Availability"],
        "Without APM": [
            f"${results_df['total_revenue_base'].mean()/1_000_000:.1f}M",
            f"${results_df['total_cost_base'].mean()/1_000_000:.1f}M",
            f"{results_df['final_soh_base'].mean()*100:.1f}%",
            f"{results_df['avg_availability_base'].mean()*100:.1f}%"
        ],
        "With APM": [
            f"${results_df['total_revenue_apm'].mean()/1_000_000:.1f}M",
            f"${results_df['total_cost_apm'].mean()/1_000_000:.1f}M",
            f"{results_df['final_soh_apm'].mean()*100:.1f}%",
            f"{results_df['avg_availability_apm'].mean()*100:.1f}%"
        ]
    }
    
    performance_df = pd.DataFrame(performance_metrics)
    st.dataframe(performance_df, use_container_width=True)
    
    # Sensitivity Analysis Chart
    st.subheader("📊 Revenue vs Cost Analysis")
    
    fig_scatter = px.scatter(
        results_df,
        x='total_revenue_apm',
        y='total_cost_apm',
        color='npv_difference',
        title="Revenue vs Cost Relationship (With APM)",
        labels={
            'total_revenue_apm': 'Total Revenue (AUD)',
            'total_cost_apm': 'Total Costs (AUD)',
            'npv_difference': 'NPV Difference'
        },
        color_continuous_scale='RdYlGn'
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Summary Recommendations
    st.subheader("🎯 Investment Recommendation")
    
    if positive_roi_prob >= 70 and avg_npv_diff > apm.implementation_cost_aud * 0.5:
        recommendation = "🟢 **STRONG BUY**: High probability of positive ROI with significant returns"
        color = "green"
    elif positive_roi_prob >= 50 and avg_npv_diff > 0:
        recommendation = "🟡 **CONDITIONAL BUY**: Moderate returns, consider risk tolerance"
        color = "orange"
    else:
        recommendation = "🔴 **AVOID**: High risk of negative returns"
        color = "red"
    
    st.markdown(f"<div style='padding: 1rem; border-left: 4px solid {color}; background-color: rgba(0,0,0,0.1);'>{recommendation}</div>", unsafe_allow_html=True)
    
    # Key Value Drivers
    st.subheader("🔑 Key Value Drivers")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Revenue Improvements:**")
        revenue_improvement = (results_df['total_revenue_apm'].mean() - results_df['total_revenue_base'].mean()) / results_df['total_revenue_base'].mean() * 100
        st.write(f"• Average revenue increase: {revenue_improvement:.1f}%")
        st.write(f"• Better dispatch response: {apm.dispatch_optimization_improvement*100:.0f}%")
        st.write(f"• Improved availability: {apm.predictive_maintenance_improvement*100:.0f}%")
    
    with col2:
        st.write("**Cost Reductions:**")
        cost_reduction = (results_df['total_cost_base'].mean() - results_df['total_cost_apm'].mean()) / results_df['total_cost_base'].mean() * 100
        st.write(f"• Net cost reduction: {cost_reduction:.1f}%")
        st.write(f"• Maintenance savings: {apm.maintenance_cost_reduction*100:.0f}%")
        st.write(f"• Degradation reduction: {apm.degradation_reduction*100:.0f}%")
    
    # Export results option
    if st.button("📥 Export Results to CSV"):
        csv = results_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"bess_apm_analysis_{asset.name.replace(' ', '_')}.csv",
            mime="text/csv"
        )


if __name__ == "__main__":
    main()
