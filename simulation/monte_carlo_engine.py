"""
Monte Carlo Simulation Engine for BESS APM Platform Impact Analysis
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import asdict
import logging

from models.bess_models import (
    BESSAsset, MarketConditions, APMPlatformSpec, 
    SimulationParameters, FinancialMetrics
)


class BESSPerformanceSimulator:
    """Simulates BESS performance over time with and without APM platform"""
    
    def __init__(self, asset: BESSAsset, market: MarketConditions, 
                 apm: Optional[APMPlatformSpec] = None, 
                 params: SimulationParameters = SimulationParameters()):
        self.asset = asset
        self.market = market
        self.apm = apm
        self.params = params
        self.logger = logging.getLogger(__name__)
        
    def simulate_degradation(self, years: float, with_apm: bool = False) -> float:
        """Simulate battery degradation over time"""
        base_degradation = self.asset.degradation_rate_annual * years
        
        if with_apm and self.apm:
            # APM reduces degradation through better management
            reduction_factor = 1 - self.apm.degradation_reduction
            base_degradation *= reduction_factor
            
        # Add some randomness
        degradation_noise = np.random.normal(0, 0.005)  # 0.5% std dev
        return max(0, min(1, base_degradation + degradation_noise))
    
    def simulate_availability(self, year: int, with_apm: bool = False) -> float:
        """Simulate system availability considering downtime"""
        base_availability = 1 - self.params.unplanned_downtime_base
        
        if with_apm and self.apm:
            # APM improves availability through predictive maintenance
            improvement = self.apm.predictive_maintenance_improvement
            availability = base_availability + (1 - base_availability) * improvement
        else:
            availability = base_availability
            
        # Add random events
        random_downtime = np.random.exponential(0.02)  # Random failures
        availability = max(0.5, availability - random_downtime)
        
        return availability
    
    def simulate_dispatch_performance(self, with_apm: bool = False) -> float:
        """Simulate how well the system responds to AEMO dispatch instructions"""
        base_efficiency = self.market.dispatch_efficiency
        
        if with_apm and self.apm:
            improvement = self.apm.dispatch_optimization_improvement
            dispatch_efficiency = min(0.98, base_efficiency + improvement)
        else:
            dispatch_efficiency = base_efficiency
            
        # Add market volatility impact
        volatility_impact = np.random.normal(0, 0.05)
        return max(0.6, min(0.98, dispatch_efficiency + volatility_impact))
    
    def simulate_annual_revenue(self, year: int, soh: float, availability: float, 
                              dispatch_efficiency: float) -> float:
        """Calculate annual revenue based on system performance"""
        # Base revenue calculation
        energy_revenue = (
            self.asset.capacity_mwh * 
            self.market.spot_price_avg_aud_mwh * 
            365 * 
            self.market.capacity_factor *
            soh *  # Reduced capacity due to degradation
            availability *  # Reduced due to downtime
            dispatch_efficiency  # Reduced due to poor dispatch response
        )
        
        # FCAS revenue (frequency control ancillary services)
        fcas_revenue = (
            self.asset.power_rating_mw *
            self.market.fcas_price_avg_aud_mw_hr *
            24 * 365 * 0.3 *  # 30% of time providing FCAS
            availability
        )
        
        # Add market price volatility
        price_multiplier = np.random.lognormal(0, self.market.price_volatility)
        total_revenue = (energy_revenue + fcas_revenue) * price_multiplier
        
        # Apply dispatch penalties
        penalty = (1 - dispatch_efficiency) * self.market.missed_dispatch_penalty_rate
        total_revenue *= (1 - penalty)
        
        return total_revenue
    
    def simulate_annual_costs(self, year: int, soh: float, with_apm: bool = False) -> float:
        """Calculate annual operational costs"""
        # Base maintenance costs
        base_maintenance = self.asset.initial_cost_aud * self.params.maintenance_cost_base_percent
        
        if with_apm and self.apm:
            # APM reduces maintenance costs
            maintenance_cost = base_maintenance * (1 - self.apm.maintenance_cost_reduction)
            # Add APM platform costs
            apm_cost = self.apm.annual_cost_aud
        else:
            maintenance_cost = base_maintenance
            apm_cost = 0
        
        # Degradation increases maintenance costs
        degradation_multiplier = 1 + (1 - soh) * 0.5  # 50% increase at full degradation
        maintenance_cost *= degradation_multiplier
        
        # Random major failures
        major_failure_cost = 0
        if np.random.random() < self.params.major_failure_probability:
            if with_apm and self.apm:
                # APM reduces failure risk
                failure_reduction = (self.apm.fire_risk_reduction + 
                                   self.apm.thermal_runaway_prevention) / 2
                if np.random.random() > failure_reduction:
                    major_failure_cost = (self.asset.initial_cost_aud * 
                                        self.params.major_failure_cost_multiplier * 0.5)
            else:
                major_failure_cost = (self.asset.initial_cost_aud * 
                                    self.params.major_failure_cost_multiplier)
        
        return maintenance_cost + apm_cost + major_failure_cost
    
    def run_single_simulation(self) -> Tuple[Dict, Dict]:
        """Run a single Monte Carlo simulation"""
        results_base = {"revenues": [], "costs": [], "soh": [], "availability": []}
        results_apm = {"revenues": [], "costs": [], "soh": [], "availability": []}
        
        # Initialize state
        soh_base = 1.0
        soh_apm = 1.0
        
        for year in range(self.params.simulation_years):
            # Simulate degradation
            degradation_base = self.simulate_degradation(1.0, with_apm=False)
            degradation_apm = self.simulate_degradation(1.0, with_apm=True)
            
            soh_base = max(0.5, soh_base - degradation_base)
            soh_apm = max(0.5, soh_apm - degradation_apm)
            
            # Simulate availability
            availability_base = self.simulate_availability(year, with_apm=False)
            availability_apm = self.simulate_availability(year, with_apm=True)
            
            # Simulate dispatch performance
            dispatch_base = self.simulate_dispatch_performance(with_apm=False)
            dispatch_apm = self.simulate_dispatch_performance(with_apm=True)
            
            # Calculate revenues
            revenue_base = self.simulate_annual_revenue(
                year, soh_base, availability_base, dispatch_base
            )
            revenue_apm = self.simulate_annual_revenue(
                year, soh_apm, availability_apm, dispatch_apm
            )
            
            # Calculate costs
            cost_base = self.simulate_annual_costs(year, soh_base, with_apm=False)
            cost_apm = self.simulate_annual_costs(year, soh_apm, with_apm=True)
            
            # Store results
            results_base["revenues"].append(revenue_base)
            results_base["costs"].append(cost_base)
            results_base["soh"].append(soh_base)
            results_base["availability"].append(availability_base)
            
            results_apm["revenues"].append(revenue_apm)
            results_apm["costs"].append(cost_apm)
            results_apm["soh"].append(soh_apm)
            results_apm["availability"].append(availability_apm)
        
        return results_base, results_apm
    
    def calculate_financial_metrics(self, cash_flows: List[float], 
                                  initial_investment: float = 0) -> Dict:
        """Calculate financial metrics from cash flows"""
        cash_flows = np.array(cash_flows)
        years = np.arange(len(cash_flows))
        
        # NPV calculation
        discount_factors = (1 + self.params.discount_rate) ** years
        npv = np.sum(cash_flows / discount_factors) - initial_investment
        
        # Payback period (simple)
        cumulative_cf = np.cumsum(cash_flows)
        payback_idx = np.where(cumulative_cf >= initial_investment)[0]
        payback_period = payback_idx[0] if len(payback_idx) > 0 else len(cash_flows)
        
        # IRR approximation (simplified)
        irr = 0.0
        if npv > 0 and initial_investment > 0:
            irr = (np.sum(cash_flows) / initial_investment) ** (1/len(cash_flows)) - 1
        
        return {
            "npv": npv,
            "payback_period": payback_period,
            "irr": irr,
            "total_cash_flow": np.sum(cash_flows)
        }
    
    def run_monte_carlo(self) -> pd.DataFrame:
        """Run full Monte Carlo simulation"""
        self.logger.info(f"Running {self.params.num_simulations} Monte Carlo simulations")
        
        simulation_results = []
        
        for sim_idx in range(self.params.num_simulations):
            try:
                results_base, results_apm = self.run_single_simulation()
                
                # Calculate cash flows
                cash_flows_base = [r - c for r, c in zip(results_base["revenues"], 
                                                        results_base["costs"])]
                cash_flows_apm = [r - c for r, c in zip(results_apm["revenues"], 
                                                       results_apm["costs"])]
                
                # Calculate financial metrics
                metrics_base = self.calculate_financial_metrics(cash_flows_base)
                apm_investment = self.apm.implementation_cost_aud if self.apm else 0
                metrics_apm = self.calculate_financial_metrics(cash_flows_apm, apm_investment)
                
                # Store simulation result
                simulation_results.append({
                    "simulation_id": sim_idx,
                    "npv_base": metrics_base["npv"],
                    "npv_apm": metrics_apm["npv"],
                    "npv_difference": metrics_apm["npv"] - metrics_base["npv"],
                    "payback_period": metrics_apm["payback_period"],
                    "irr_apm": metrics_apm["irr"],
                    "total_revenue_base": sum(results_base["revenues"]),
                    "total_revenue_apm": sum(results_apm["revenues"]),
                    "total_cost_base": sum(results_base["costs"]),
                    "total_cost_apm": sum(results_apm["costs"]),
                    "final_soh_base": results_base["soh"][-1],
                    "final_soh_apm": results_apm["soh"][-1],
                    "avg_availability_base": np.mean(results_base["availability"]),
                    "avg_availability_apm": np.mean(results_apm["availability"])
                })
                
            except Exception as e:
                self.logger.warning(f"Simulation {sim_idx} failed: {e}")
                continue
        
        return pd.DataFrame(simulation_results)
