# 🔋 BESS APM Platform Investment Analysis Tool

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://wvlt-bess-apm-scenarios-app-main.streamlit.app)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/wvlt/bess-apm-scenarios)
[![Python](https://img.shields.io/badge/Python-3.8+-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## Overview

This application provides a comprehensive Monte Carlo simulation framework for evaluating the financial impact of investing in an Asset Performance Management (APM) platform for Battery Energy Storage System (BESS) assets.

The tool helps answer critical business questions such as:
- What is the ROI of implementing an APM platform?
- How does APM investment impact battery lifecycle and revenue?
- What are the risks and confidence intervals for different scenarios?
- Which APM platform offers the best value proposition?

## Key Features

### 🔋 Comprehensive BESS Modeling
- Multiple battery chemistries (LFP, NMC, LTO)
- Realistic degradation modeling
- Performance optimization scenarios
- Market dispatch simulation

### 💰 Financial Analysis
- Net Present Value (NPV) calculations
- Internal Rate of Return (IRR)
- Payback period analysis
- Risk assessment with Value at Risk (VaR)

### 🎲 Monte Carlo Simulation
- Thousands of scenario iterations
- Stochastic modeling of market conditions
- Risk quantification
- Confidence interval analysis

### 📊 Interactive Dashboard
- Real-time parameter adjustment
- Visual results presentation
- Sensitivity analysis
- Export capabilities

## APM Platform Benefits Modeled

### Predictive Maintenance
- **5-25% reduction** in unplanned downtime
- Early detection of cell degradation
- Optimized maintenance scheduling
- Reduced catastrophic failure risk

### Dispatch Optimization
- **8-18% improvement** in AEMO dispatch response
- Better energy arbitrage opportunities
- Enhanced FCAS revenue capture
- Reduced penalty costs

### Battery Life Extension
- **5-12% reduction** in degradation rate
- Optimized charge/discharge profiles
- Better thermal management
- Cell balancing improvements

### Operational Efficiency
- **15-30% reduction** in maintenance costs
- Improved operator efficiency
- Better data-driven decisions
- Enhanced safety protocols

## Quick Start

### Prerequisites
```bash
Python 3.8+
pip install -r requirements.txt
```

### Installation
```bash
git clone <repository>
cd bess-apm-scenarios
pip install -r requirements.txt
```

### Running the Application
```bash
streamlit run app.py
```

The application will open in your web browser at `http://localhost:8501`

## 🌐 Live Demo

**Try the live application here: [BESS APM Analysis Tool](https://wvlt-bess-apm-scenarios-app-main.streamlit.app)**

## 🚀 Deployment Options

### Streamlit Cloud (Recommended)
1. Fork this repository
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Deploy from your forked repository
5. Set main file as `app.py`

### Docker Deployment
```bash
# Build the Docker image
docker build -t bess-apm-analysis .

# Run the container
docker run -p 8501:8501 bess-apm-analysis
```

### Local Development
```bash
# Clone the repository
git clone https://github.com/wvlt/bess-apm-scenarios.git
cd bess-apm-scenarios

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## Using the Tool

### 1. Configure BESS Asset
- **Capacity**: Energy storage capacity in MWh
- **Power Rating**: Maximum power output in MW
- **Chemistry**: Battery technology type
- **Initial Cost**: Total asset investment
- **Performance**: Efficiency and degradation parameters

### 2. Set Market Conditions
- **Spot Prices**: Average electricity prices (AUD/MWh)
- **Volatility**: Market price fluctuation
- **FCAS Prices**: Frequency control service rates
- **Capacity Factor**: Asset utilization rate

### 3. Select APM Platform
Choose from predefined platforms or create custom configuration:

**Basic APM** ($200K annual, $500K implementation)
- 10% predictive maintenance improvement
- 8% dispatch optimization
- 5% degradation reduction

**Advanced APM** ($500K annual, $1.2M implementation)
- 15% predictive maintenance improvement
- 12% dispatch optimization
- 8% degradation reduction

**Enterprise APM** ($800K annual, $2M implementation)
- 25% predictive maintenance improvement
- 18% dispatch optimization
- 12% degradation reduction

### 4. Run Analysis
- Set simulation parameters (iterations, time horizon)
- Execute Monte Carlo simulation
- Review results and recommendations

## Interpreting Results

### Key Metrics

**NPV Improvement**: Additional value created by APM investment
- Positive values indicate profitable investment
- Compare against implementation costs

**Probability of Positive ROI**: Likelihood of profitable outcome
- >70% suggests strong investment case
- 50-70% indicates moderate confidence
- <50% suggests high risk

**Payback Period**: Time to recover initial investment
- Shorter periods indicate faster returns
- Consider against asset lifetime

**IRR**: Internal rate of return
- Compare against cost of capital
- Higher IRR indicates better investment

### Risk Assessment

**Value at Risk (VaR)**: Potential losses at confidence levels
- 5th percentile: Worst-case scenarios
- Helps understand downside risk

**Distribution Analysis**: Range of potential outcomes
- Wide distributions indicate higher uncertainty
- Skewed distributions show asymmetric risk

## Example Scenarios

### Scenario 1: Large Utility BESS (100 MWh)
- **Asset**: 100 MWh / 50 MW LFP system
- **Cost**: $80M initial investment
- **Market**: $85/MWh average spot price
- **Result**: Advanced APM shows 15% NPV improvement

### Scenario 2: Commercial BESS (20 MWh)
- **Asset**: 20 MWh / 10 MW system
- **Cost**: $16M initial investment
- **Market**: High volatility market
- **Result**: Basic APM sufficient for positive ROI

### Scenario 3: Grid-Scale BESS (500 MWh)
- **Asset**: 500 MWh / 200 MW system
- **Cost**: $400M initial investment
- **Market**: FCAS-heavy revenue model
- **Result**: Enterprise APM justified by scale

## Technical Architecture

### Models (`models/bess_models.py`)
- `BESSAsset`: Battery system specifications
- `MarketConditions`: Economic environment
- `APMPlatformSpec`: Platform capabilities
- `SimulationParameters`: Analysis settings

### Simulation Engine (`simulation/monte_carlo_engine.py`)
- Monte Carlo framework
- Stochastic modeling
- Financial calculations
- Risk assessment

### Dashboard (`app.py`)
- Streamlit interface
- Interactive controls
- Results visualization
- Export functionality

## Validation and Accuracy

The simulation model has been validated against:
- Industry performance data
- Vendor specifications
- Academic research
- Real-world case studies

### Model Assumptions
- Linear degradation with stochastic variation
- Log-normal electricity price distributions
- Independent failure events
- Perfect market liquidity

### Limitations
- Model simplified for rapid analysis
- Some correlations not captured
- Regulatory changes not modeled
- Technology improvements not projected

## Customization

### Adding New APM Platforms
Edit the `apm_platforms` dictionary in `app.py`:

```python
"Custom Platform": {
    "annual": 600_000,
    "implementation": 1_500_000,
    "benefits": {
        "predictive_maintenance": 0.20,
        "dispatch_optimization": 0.15,
        "degradation_reduction": 0.10,
        "maintenance_cost_reduction": 0.25
    }
}
```

### Modifying Market Models
Update the `MarketConditions` class to include:
- Seasonal price variations
- Time-of-use rates
- Network charges
- Carbon pricing

### Advanced Analytics
Extend the simulation to include:
- Machine learning predictions
- Weather correlations
- Grid constraint modeling
- Portfolio optimization

## Support and Development

### Common Issues
1. **Import Errors**: Ensure all packages installed
2. **Slow Performance**: Reduce simulation iterations
3. **Memory Issues**: Use smaller datasets for development

### Contributing
- Follow PEP 8 style guidelines
- Add unit tests for new features
- Update documentation
- Validate against real data

### Roadmap
- [ ] Integration with real SCADA systems
- [ ] Machine learning degradation models
- [ ] Multi-asset portfolio analysis
- [ ] Real-time market data feeds
- [ ] Advanced risk modeling

## Contact

For technical questions or business inquiries regarding this BESS APM analysis tool, please contact the development team.

---

**Disclaimer**: This tool provides estimates based on modeling assumptions. Actual results may vary based on specific asset characteristics, market conditions, and implementation factors. Consult with domain experts for investment decisions.
