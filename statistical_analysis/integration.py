"""
Integration Guide: Using Statistical Analysis with Calculator

This module shows how to integrate the statistical analysis module
with the existing carbon footprint calculator.
"""

# Note: This is a guide file - adapt to your actual calculator structure


class IntegrationExample:
    """
    Example of integrating statistical analysis with the main calculator.
    
    The statistical module can be used to:
    1. Analyze historical company emissions
    2. Predict future emissions based on trends
    3. Assess climate risk for investment decisions
    """
    
    @staticmethod
    def analyze_company_emissions(company_emissions_history):
        """
        Analyze a company's historical emissions and generate forecast.
        
        Args:
            company_emissions_history: List of (year, total_emissions) tuples
        
        Returns:
            Dictionary with analysis results
        """
        from statistical_analysis.regression_model import LinearRegression
        from statistical_analysis.probability_analysis import ProbabilityAnalyzer
        
        years = [item[0] for item in company_emissions_history]
        emissions = [item[1] for item in company_emissions_history]
        
        # Regression analysis
        regressor = LinearRegression()
        model = regressor.fit(years, emissions)
        
        # Probability analysis
        analyzer = ProbabilityAnalyzer(emissions)
        stats = analyzer.get_statistics()
        
        # Generate forecast
        forecast = regressor.predict_future(3)
        
        # Risk assessment
        avg_future = sum(pred[1] for pred in forecast) / len(forecast)
        risk_level = analyzer.categorize_risk(avg_future)
        
        return {
            "trend": model.slope,
            "forecast": forecast,
            "risk_level": risk_level.value,
            "volatility": stats["coefficient_of_variation"],
            "model_quality": model.r_squared
        }
    
    @staticmethod
    def generate_investment_report(company_data):
        """
        Generate an investment assessment report.
        
        Args:
            company_data: Dictionary with company information
        
        Returns:
            Investment assessment report
        """
        from statistical_analysis.regression_model import LinearRegression
        from statistical_analysis.probability_analysis import ProbabilityAnalyzer
        
        emissions_history = company_data.get("emissions_history", [])
        
        if len(emissions_history) < 2:
            return {"status": "INSUFFICIENT_DATA"}
        
        # Extract years and emissions
        years, emissions = zip(*emissions_history)
        
        # Analysis
        regressor = LinearRegression()
        regressor.fit(years, emissions)
        
        analyzer = ProbabilityAnalyzer(list(emissions))
        
        # Generate report
        forecast = regressor.predict_future(1)
        
        report = {
            "company": company_data.get("name"),
            "analysis_period": f"{min(years)}-{max(years)}",
            "current_emissions": emissions[-1],
            "trend": "increasing" if regressor.model.slope > 0 else "decreasing",
            "annual_change": f"{regressor.model.slope:.2f} tCO2e/year",
            "predicted_next_year": forecast[0][1],
            "risk_level": analyzer.categorize_risk(forecast[0][1]).value,
            "volatility": analyzer.get_statistics()["coefficient_of_variation"],
            "r_squared": regressor.model.r_squared,
        }
        
        # Investment recommendation
        if regressor.model.slope < 0:
            report["recommendation"] = "FAVORABLE"
            report["reason"] = "Emissions are decreasing"
        elif regressor.model.slope > 0 and analyzer.categorize_risk(forecast[0][1]).value == "HIGH":
            report["recommendation"] = "UNFAVORABLE"
            report["reason"] = "Emissions increasing with high risk"
        else:
            report["recommendation"] = "CONDITIONAL"
            report["reason"] = "Monitor emissions trend"
        
        return report


# Example usage
if __name__ == "__main__":
    # Example 1: Analyze company emissions
    print("EXAMPLE: Company Emissions Analysis")
    print("-" * 50)
    
    company_history = [
        (2020, 5000),
        (2021, 5500),
        (2022, 6100),
        (2023, 6800),
    ]
    
    result = IntegrationExample.analyze_company_emissions(company_history)
    
    print(f"Trend: {result['trend']:.2f} tCO2e/year")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Forecast (next 3 years):")
    for year, pred in result['forecast']:
        print(f"  {year}: {pred:,.0f} tCO2e")
    
    # Example 2: Generate investment report
    print("\n\nEXAMPLE: Investment Report")
    print("-" * 50)
    
    company_data = {
        "name": "GreenTech Solutions",
        "emissions_history": [
            (2021, 3000),
            (2022, 3100),
            (2023, 3050),
        ]
    }
    
    report = IntegrationExample.generate_investment_report(company_data)
    
    for key, value in report.items():
        print(f"{key}: {value}")
