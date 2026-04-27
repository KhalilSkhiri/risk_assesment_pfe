"""
Examples and Usage Demonstrations

Practical examples showing how to use the statistical analysis module
for carbon footprint prediction and risk assessment.
"""

from statistical_analysis.regression_model import LinearRegression
from statistical_analysis.probability_analysis import ProbabilityAnalyzer, RiskLevel
from statistical_analysis.utils import (
    calculate_moving_average, 
    calculate_yoy_change,
    detect_outliers,
    summarize_emissions
)


def example_1_simple_regression():
    """
    Example 1: Simple linear regression on 4-year emission history.
    
    Scenario: Company with growing emissions over 2020-2023
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: Linear Regression - Simple Case")
    print("="*70)
    
    # Historical data
    years = [2020, 2021, 2022, 2023]
    emissions = [5000, 5500, 6100, 6800]  # tCO2e
    
    # Fit regression model
    regressor = LinearRegression()
    model = regressor.fit(years, emissions)
    
    # Display model
    print(f"\nData: {list(zip(years, emissions))}")
    print(f"\nModel: {model}")
    print(f"R-squared: {model.r_squared:.4f}")
    
    # Predictions
    print(f"\nPredictions for future years:")
    future = regressor.predict_future(3)
    for year, pred in future:
        print(f"  {year}: {pred:,.0f} tCO2e")
    
    # Statistics
    stats = regressor.get_statistics()
    print(f"\nTrend: {stats['trend_direction']} ({stats['slope']:.2f} tCO2e/year)")


def example_2_probability_risk_assessment():
    """
    Example 2: Risk assessment using probability analysis.
    
    Scenario: Analyzing volatility in emissions to assess climate risk
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: Probability Analysis - Risk Assessment")
    print("="*70)
    
    # Historical emissions (more volatile)
    historical = [4200, 4800, 4500, 5200, 5800, 5100, 5900]
    
    # Create analyzer
    analyzer = ProbabilityAnalyzer(historical)
    
    # Descriptive statistics
    stats = analyzer.get_statistics()
    print(f"\nHistorical data: {historical}")
    print(f"\nStatistics:")
    print(f"  Mean: {stats['mean']:.0f} tCO2e")
    print(f"  Std Dev: {stats['std_dev']:.0f} tCO2e")
    print(f"  Range: [{stats['min']:.0f}, {stats['max']:.0f}]")
    print(f"  Coefficient of Variation: {stats['coefficient_of_variation']:.2%}")
    
    # Percentiles
    print(f"\nPercentiles:")
    for p in [25, 50, 75, 90]:
        val = analyzer.percentile(p)
        print(f"  P{p}: {val:.0f} tCO2e")
    
    # Risk categorization
    test_values = [4000, 5000, 5800]
    print(f"\nRisk Categorization:")
    for value in test_values:
        risk = analyzer.categorize_risk(value)
        print(f"  {value} tCO2e → {risk.value}")
    
    # Confidence interval
    predicted = 5800
    ci = analyzer.confidence_interval(predicted, confidence_level=0.95)
    print(f"\n95% Confidence Interval for {predicted} tCO2e:")
    print(f"  [{ci.lower_bound:.0f}, {ci.upper_bound:.0f}]")
    print(f"  Width: {ci.width():.0f} tCO2e")
    
    # Probabilities
    print(f"\nProbabilities:")
    prob_above = analyzer.probability_above_threshold(6000)
    print(f"  P(emissions > 6000 tCO2e) = {prob_above:.2%}")
    
    prob_range = analyzer.probability_in_range(5000, 6000)
    print(f"  P(5000 < emissions < 6000 tCO2e) = {prob_range:.2%}")


def example_3_combined_analysis():
    """
    Example 3: Combined regression + probability analysis.
    
    Scenario: Predict future emissions and assess confidence/risk
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: Combined Analysis - Regression + Probability")
    print("="*70)
    
    # Historical data (6 years)
    years = [2018, 2019, 2020, 2021, 2022, 2023]
    emissions = [3200, 3400, 3500, 3800, 4100, 4400]
    
    # Step 1: Fit regression
    regressor = LinearRegression()
    model = regressor.fit(years, emissions)
    
    print(f"Regression Model: {model}")
    print(f"Annual increase: {model.slope:.2f} tCO2e/year")
    
    # Step 2: Predict future year
    future_year = 2024
    predicted = regressor.predict(future_year)
    print(f"\nPredicted emissions for {future_year}: {predicted:.0f} tCO2e")
    
    # Step 3: Assess risk with probability analyzer
    analyzer = ProbabilityAnalyzer(emissions)
    
    # Confidence interval
    ci = analyzer.confidence_interval(predicted, confidence_level=0.95)
    print(f"95% Confidence Interval: [{ci.lower_bound:.0f}, {ci.upper_bound:.0f}]")
    
    # Risk level
    risk = analyzer.categorize_risk(predicted)
    print(f"Risk Level: {risk.value}")
    
    # Probability of exceeding trend
    prob = analyzer.probability_above_threshold(predicted + 500)
    print(f"Probability of exceeding {predicted + 500:.0f} tCO2e: {prob:.2%}")


def example_4_utility_functions():
    """
    Example 4: Using utility functions for data analysis.
    
    Scenario: Preprocessing and analyzing raw emission data
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: Utility Functions - Data Analysis Tools")
    print("="*70)
    
    # Raw data with some volatility
    years = [2019, 2020, 2021, 2022, 2023]
    emissions = [4200, 4100, 4800, 4300, 5200]
    
    print(f"Original data: {emissions}")
    
    # Moving average (smooth the data)
    ma_3 = calculate_moving_average(emissions, window_size=3)
    print(f"\n3-year moving average: {[f'{x:.0f}' for x in ma_3]}")
    
    # Year-over-year change
    yoy = calculate_yoy_change(emissions)
    print(f"\nYear-over-year change (%):")
    for i, change in enumerate(yoy):
        print(f"  {years[i]} → {years[i+1]}: {change:+.1f}%")
    
    # Summary statistics
    summary = summarize_emissions(emissions)
    print(f"\nEmissions Summary:")
    print(f"  Count: {summary['count']}")
    print(f"  Total: {summary['total']:.0f} tCO2e")
    print(f"  Average: {summary['mean']:.0f} tCO2e")
    print(f"  Median: {summary['median']:.0f} tCO2e")
    
    # Outlier detection
    outlier_idx, outlier_vals = detect_outliers(emissions, threshold=1.5)
    if outlier_idx:
        print(f"\nOutliers detected (z > 1.5):")
        for idx, val in zip(outlier_idx, outlier_vals):
            print(f"  Year {years[idx]}: {val} tCO2e")
    else:
        print(f"\nNo outliers detected")


def example_5_investment_decision():
    """
    Example 5: Use case for investment decision support.
    
    Scenario: Bank evaluating whether to finance a company
    """
    print("\n" + "="*70)
    print("EXAMPLE 5: Investment Decision Support")
    print("="*70)
    
    company_name = "GreenTech Solutions"
    
    # Historical emissions (3 years)
    years = [2021, 2022, 2023]
    emissions = [3000, 3100, 3050]
    
    # Analyze trajectory
    regressor = LinearRegression()
    model = regressor.fit(years, emissions)
    
    # Analyze volatility
    analyzer = ProbabilityAnalyzer(emissions)
    
    # Get statistics
    stats = analyzer.get_statistics()
    
    print(f"\nCompany: {company_name}")
    print(f"Historical Emissions (2021-2023): {emissions}")
    
    print(f"\nEmissions Trend Analysis:")
    print(f"  Slope: {model.slope:.2f} tCO2e/year ({'+' if model.slope > 0 else ''}{(model.slope/3050)*100:.1f}% annual change)")
    print(f"  R²: {model.r_squared:.4f} (model fit quality)")
    
    print(f"\nVolatility Analysis:")
    print(f"  Mean: {stats['mean']:.0f} tCO2e")
    print(f"  Std Dev: {stats['std_dev']:.0f} tCO2e")
    print(f"  CV: {stats['coefficient_of_variation']:.2%}")
    
    # Prediction
    pred_2024 = regressor.predict(2024)
    ci = analyzer.confidence_interval(pred_2024, confidence_level=0.95)
    
    print(f"\nForecast for 2024:")
    print(f"  Expected: {pred_2024:.0f} tCO2e")
    print(f"  95% CI: [{ci.lower_bound:.0f}, {ci.upper_bound:.0f}]")
    
    # Risk assessment
    risk = analyzer.categorize_risk(pred_2024)
    print(f"  Risk Level: {risk.value}")
    
    # Investment recommendation
    print(f"\nInvestment Assessment:")
    if model.slope < 0 and risk in [RiskLevel.LOW, RiskLevel.MEDIUM]:
        print(f"  ✓ FAVORABLE: Decreasing emissions with low risk")
    elif model.slope > 0 and risk == RiskLevel.HIGH:
        print(f"  ✗ UNFAVORABLE: Increasing emissions with high risk")
    else:
        print(f"  ⚠ CONDITIONAL: Monitor closely")


if __name__ == "__main__":
    # Run all examples
    example_1_simple_regression()
    example_2_probability_risk_assessment()
    example_3_combined_analysis()
    example_4_utility_functions()
    example_5_investment_decision()
    
    print("\n" + "="*70)
    print("All examples completed!")
    print("="*70)
