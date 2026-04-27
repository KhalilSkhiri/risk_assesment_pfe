"""
Linear Regression Module for Emissions Prediction

This module provides tools for building linear regression models
to predict future carbon emissions based on historical data.
"""

import math
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass


@dataclass
class RegressionModel:
    """Linear regression model for emissions prediction."""
    
    slope: float
    intercept: float
    r_squared: float
    std_error: float
    
    def predict(self, x: float) -> float:
        """Predict y value for given x."""
        return self.slope * x + self.intercept
    
    def predict_batch(self, x_values: List[float]) -> List[float]:
        """Predict multiple values at once."""
        return [self.predict(x) for x in x_values]
    
    def __repr__(self) -> str:
        return (
            f"RegressionModel(y = {self.slope:.4f}x + {self.intercept:.4f}, "
            f"R² = {self.r_squared:.4f})"
        )


class LinearRegression:
    """
    Simple Linear Regression Calculator
    
    Implements ordinary least squares (OLS) method to fit a linear model
    y = mx + b to historical emissions data.
    """
    
    def __init__(self):
        self.model: Optional[RegressionModel] = None
        self.x_data: List[float] = []
        self.y_data: List[float] = []
    
    def fit(self, x_years: List[float], y_emissions: List[float]) -> RegressionModel:
        """
        Fit linear regression model to data.
        
        Args:
            x_years: Years or time periods (independent variable)
            y_emissions: Emission values in tCO2e (dependent variable)
        
        Returns:
            RegressionModel: Fitted model with parameters
        
        Raises:
            ValueError: If data sets have different lengths or are empty
        """
        if len(x_years) != len(y_emissions):
            raise ValueError("x and y must have the same length")
        
        if len(x_years) < 2:
            raise ValueError("At least 2 data points required for linear regression")
        
        self.x_data = x_years
        self.y_data = y_emissions
        
        n = len(x_years)
        
        # Calculate means
        x_mean = sum(x_years) / n
        y_mean = sum(y_emissions) / n
        
        # Calculate slope and intercept
        numerator = sum((x_years[i] - x_mean) * (y_emissions[i] - y_mean) 
                       for i in range(n))
        denominator = sum((x_years[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            raise ValueError("Cannot fit model: x values are constant")
        
        slope = numerator / denominator
        intercept = y_mean - slope * x_mean
        
        # Calculate R-squared
        ss_res = sum((y_emissions[i] - (slope * x_years[i] + intercept)) ** 2 
                     for i in range(n))
        ss_tot = sum((y_emissions[i] - y_mean) ** 2 for i in range(n))
        
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        # Calculate standard error
        if n > 2:
            std_error = math.sqrt(ss_res / (n - 2))
        else:
            std_error = 0.0
        
        self.model = RegressionModel(
            slope=slope,
            intercept=intercept,
            r_squared=r_squared,
            std_error=std_error
        )
        
        return self.model
    
    def predict(self, year: float) -> float:
        """Predict emissions for a given year."""
        if self.model is None:
            raise RuntimeError("Model not fitted yet. Call fit() first.")
        return self.model.predict(year)
    
    def predict_future(self, num_years: int) -> List[Tuple[float, float]]:
        """
        Predict emissions for future years.
        
        Args:
            num_years: Number of years to predict into the future
        
        Returns:
            List of (year, predicted_emissions) tuples
        """
        if not self.x_data:
            raise RuntimeError("No training data available")
        
        last_year = max(self.x_data)
        predictions = []
        
        for i in range(1, num_years + 1):
            future_year = last_year + i
            prediction = self.predict(future_year)
            predictions.append((future_year, prediction))
        
        return predictions
    
    def get_statistics(self) -> Dict[str, float]:
        """Return regression statistics."""
        if self.model is None:
            raise RuntimeError("Model not fitted yet")
        
        return {
            "slope": self.model.slope,
            "intercept": self.model.intercept,
            "r_squared": self.model.r_squared,
            "std_error": self.model.std_error,
            "trend_direction": "increasing" if self.model.slope > 0 else "decreasing"
        }
