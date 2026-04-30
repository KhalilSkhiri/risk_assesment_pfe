"""
Linear Regression Module for Emissions Prediction

This module provides tools for building linear regression models
to predict future carbon emissions based on historical data.

Enhanced with:
- Comprehensive diagnostic statistics
- Confidence intervals and prediction bands
- Handling of pathological cases (NaN, constant variance)
- Statistical tests for model assumptions
"""

import math
import numpy as np
from typing import List, Tuple, Dict, Optional, NamedTuple
from dataclasses import dataclass
from scipy import stats as scipy_stats


class ConfidenceInterval(NamedTuple):
    """Confidence interval representation."""
    lower_bound: float
    upper_bound: float
    
    def width(self) -> float:
        """Width of the confidence interval."""
        return self.upper_bound - self.lower_bound
    
    def __repr__(self) -> str:
        return f"CI({self.lower_bound:.2f}, {self.upper_bound:.2f})"


class RegressionDiagnostics(NamedTuple):
    """Comprehensive diagnostic statistics for regression model."""
    r_squared: float
    r_squared_adj: float
    f_statistic: float
    p_value_f: float
    residual_std_error: float
    num_observations: int
    num_parameters: int
    
    # Test results
    shapiro_statistic: float
    shapiro_p_value: float
    
    durbin_watson: float
    
    def __repr__(self) -> str:
        return f"""
Diagnostic Summary:
  R² = {self.r_squared:.4f}, R²_adj = {self.r_squared_adj:.4f}
  F-test: F = {self.f_statistic:.4f}, p-value = {self.p_value_f:.4e}
  Residual Std. Error: {self.residual_std_error:.4f} (on {self.num_observations - self.num_parameters} df)
  Normality (Shapiro-Wilk): p-value = {self.shapiro_p_value:.4e}
  Autocorrelation (Durbin-Watson): {self.durbin_watson:.4f}
"""


@dataclass
class RegressionModel:
    """
    Linear regression model for emissions prediction.
    
    Implements OLS regression with full diagnostic capabilities.
    See FONDEMENTS_MATHEMATIQUES_COMPLETS.md for theoretical foundations.
    """
    
    slope: float
    intercept: float
    r_squared: float
    r_squared_adj: float
    std_error: float
    n: int  # number of observations
    x_data: List[float]
    y_data: List[float]
    residuals: List[float]
    diagnostics: Optional[RegressionDiagnostics] = None
    
    def predict(self, x: float) -> float:
        """Predict y value for given x."""
        return self.slope * x + self.intercept
    
    def predict_batch(self, x_values: List[float]) -> List[float]:
        """Predict multiple values at once."""
        return [self.predict(x) for x in x_values]
    
    def predict_with_interval(self, x: float, confidence_level: float = 0.95) -> ConfidenceInterval:
        """
        Predict y value with confidence interval.
        
        Args:
            x: Input value
            confidence_level: Confidence level (e.g., 0.95 for 95%)
        
        Returns:
            ConfidenceInterval with prediction bounds
        """
        y_pred = self.predict(x)
        
        # Critical value from t-distribution
        alpha = 1 - confidence_level
        t_crit = scipy_stats.t.ppf(1 - alpha/2, self.n - 2)
        
        # Compute variance of prediction
        x_mean = np.mean(self.x_data)
        x_var = np.sum([(x_i - x_mean)**2 for x_i in self.x_data])
        
        if x_var == 0:
            return ConfidenceInterval(y_pred, y_pred)
        
        var_pred = self.std_error**2 * (1 + 1/self.n + (x - x_mean)**2 / x_var)
        margin = t_crit * np.sqrt(var_pred)
        
        return ConfidenceInterval(y_pred - margin, y_pred + margin)
    
    def __repr__(self) -> str:
        status = ""
        if math.isnan(self.r_squared):
            status = " [WARNING: NaN in R²]"
        return (
            f"RegressionModel(y = {self.slope:.4f}x + {self.intercept:.4f}, "
            f"R² = {self.r_squared:.4f}){status}"
        )


class LinearRegression:
    """
    Linear Regression Calculator with Full Diagnostics
    
    Implements Ordinary Least Squares (OLS) regression with:
    - Full model diagnostics (R², adjusted R², F-test)
    - Assumption testing (Shapiro-Wilk for normality, Durbin-Watson for autocorrelation)
    - Confidence intervals and prediction bands
    - Handling of pathological cases that produce NaN
    
    Reference: FONDEMENTS_MATHEMATIQUES_COMPLETS.md Section C (Mesure de qualité d'ajustement)
    """
    
    def __init__(self):
        self.model: Optional[RegressionModel] = None
        self.x_data: List[float] = []
        self.y_data: List[float] = []
    
    def _check_assumptions(self, residuals: List[float]) -> Tuple[float, float, float]:
        """
        Check regression assumptions.
        
        Returns:
            Tuple of (shapiro_stat, shapiro_p, durbin_watson)
        """
        # Shapiro-Wilk test for normality
        if len(residuals) >= 3:
            try:
                shapiro_stat, shapiro_p = scipy_stats.shapiro(residuals)
            except:
                shapiro_stat, shapiro_p = np.nan, np.nan
        else:
            shapiro_stat, shapiro_p = np.nan, np.nan
        
        # Durbin-Watson test for autocorrelation
        if len(residuals) >= 2:
            diff = np.sum(np.diff(residuals)**2)
            sum_sq = np.sum(np.array(residuals)**2)
            durbin_watson = diff / sum_sq if sum_sq > 0 else np.nan
        else:
            durbin_watson = np.nan
        
        return shapiro_stat, shapiro_p, durbin_watson
    
    def _compute_diagnostics(self, residuals: List[float], ss_res: float, 
                            ss_tot: float, slope: float) -> RegressionDiagnostics:
        """
        Compute comprehensive model diagnostics.
        
        Args:
            residuals: Model residuals
            ss_res: Sum of squared residuals
            ss_tot: Total sum of squares
            slope: Regression slope
        
        Returns:
            RegressionDiagnostics object with all statistics
        """
        n = len(self.x_data)
        p = 1  # number of predictors (slope only, not intercept)
        
        # R-squared and Adjusted R-squared
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
        r_squared_adj = 1 - (1 - r_squared) * (n - 1) / (n - p - 1)
        
        # Residual standard error
        residual_std_error = math.sqrt(ss_res / (n - 2)) if n > 2 else 0
        
        # F-statistic for overall model significance
        ss_exp = ss_tot - ss_res
        ms_exp = ss_exp / p
        ms_res = ss_res / (n - p - 1) if (n - p - 1) > 0 else 1
        f_statistic = ms_exp / ms_res if ms_res > 0 else 0
        p_value_f = 1 - scipy_stats.f.cdf(f_statistic, p, n - p - 1) if f_statistic > 0 else 1
        
        # Assumption tests
        shapiro_stat, shapiro_p, durbin_watson = self._check_assumptions(residuals)
        
        return RegressionDiagnostics(
            r_squared=r_squared,
            r_squared_adj=r_squared_adj,
            f_statistic=f_statistic,
            p_value_f=p_value_f,
            residual_std_error=residual_std_error,
            num_observations=n,
            num_parameters=p + 1,
            shapiro_statistic=shapiro_stat,
            shapiro_p_value=shapiro_p,
            durbin_watson=durbin_watson
        )
    
    def fit(self, x_years: List[float], y_emissions: List[float]) -> RegressionModel:
        r"""
        Fit linear regression model to data using OLS method.
        
        Mathematical formulation:
        $$\min_{m,b} \sum_{i=1}^{n} (E_i - (m \cdot t_i + b))^2$$
        
        Solution:
        $$\hat{m} = \frac{\sum_{i=1}^{n} (t_i - \bar{t})(E_i - \bar{E})}{\sum_{i=1}^{n} (t_i - \bar{t})^2}$$
        $$\hat{b} = \bar{E} - \hat{m} \cdot \bar{t}$$
        
        Args:
            x_years: Time points (independent variable)
            y_emissions: Emission values in tCO2e (dependent variable)
        
        Returns:
            RegressionModel: Fitted model with full diagnostics
        
        Raises:
            ValueError: If data invalid or assumptions severely violated
        """
        if len(x_years) != len(y_emissions):
            raise ValueError("x and y must have the same length")
        
        if len(x_years) < 2:
            raise ValueError("At least 2 data points required for linear regression")
        
        self.x_data = list(x_years)
        self.y_data = list(y_emissions)
        
        n = len(x_years)
        x_array = np.array(x_years)
        y_array = np.array(y_emissions)
        
        # Calculate means
        x_mean = np.mean(x_array)
        y_mean = np.mean(y_array)
        
        # CASE 1: Check if x values are constant (singular design matrix)
        x_var = np.sum((x_array - x_mean) ** 2)
        if x_var < 1e-10:  # essentially zero
            raise ValueError(
                "Cannot fit model: independent variable (x) is constant. "
                "This makes the design matrix singular (determinant = 0). "
                "Check your input data for lack of variation."
            )
        
        # CASE 2: Check if y values are constant (perfect multicollinearity with intercept)
        y_var = np.sum((y_array - y_mean) ** 2)
        if y_var < 1e-10:  # essentially zero
            print("[WARNING] Dependent variable (y) is constant.")
            print("  This leads to SS_tot ≈ 0, which causes R² = NaN (0/0 indeterminate form)")
            print("  Setting R² = 0 by convention (model explains no variance)")
            r_squared = 0.0
        else:
            r_squared = None  # Will compute normally
        
        # Calculate slope using OLS formula
        numerator = np.sum((x_array - x_mean) * (y_array - y_mean))
        slope = numerator / x_var
        intercept = y_mean - slope * x_mean
        
        # Calculate residuals and sums of squares
        y_pred = slope * x_array + intercept
        residuals = list(y_array - y_pred)
        
        ss_res = np.sum((y_array - y_pred) ** 2)
        ss_tot = np.sum((y_array - y_mean) ** 2)
        
        # CASE 3: Handle R² calculation carefully
        if ss_tot < 1e-10:  # SS_tot ≈ 0
            if r_squared is None:
                r_squared = 0.0  # By convention
            r_squared_adj = 0.0
        else:
            if r_squared is None:
                r_squared = 1 - (ss_res / ss_tot)
            # Adjusted R²: R²_adj = 1 - (1-R²)(n-1)/(n-p-1)
            r_squared_adj = 1 - (1 - r_squared) * (n - 1) / (n - 2)
        
        # Standard error
        if n > 2:
            std_error = math.sqrt(ss_res / (n - 2))
        else:
            std_error = 0.0
        
        # Compute full diagnostics
        diagnostics = self._compute_diagnostics(residuals, ss_res, ss_tot, slope)
        
        self.model = RegressionModel(
            slope=slope,
            intercept=intercept,
            r_squared=r_squared,
            r_squared_adj=r_squared_adj,
            std_error=std_error,
            n=n,
            x_data=self.x_data,
            y_data=self.y_data,
            residuals=residuals,
            diagnostics=diagnostics
        )
        
        return self.model
    
    def predict(self, year: float) -> float:
        """Predict emissions for a given year."""
        if self.model is None:
            raise RuntimeError("Model not fitted yet. Call fit() first.")
        return self.model.predict(year)
    
    def predict_future(self, num_years: int, confidence_level: float = 0.95) -> List[Tuple[float, float, ConfidenceInterval]]:
        """
        Predict emissions for future years with confidence intervals.
        
        Args:
            num_years: Number of years to predict
            confidence_level: Confidence level for prediction intervals
        
        Returns:
            List of (year, prediction, confidence_interval) tuples
        """
        if not self.x_data:
            raise RuntimeError("No training data available")
        
        last_year = max(self.x_data)
        predictions = []
        
        for i in range(1, num_years + 1):
            future_year = last_year + i
            prediction = self.predict(future_year)
            ci = self.model.predict_with_interval(future_year, confidence_level)
            predictions.append((future_year, prediction, ci))
        
        return predictions
    
    def get_statistics(self) -> Dict[str, float]:
        """Return comprehensive regression statistics."""
        if self.model is None:
            raise RuntimeError("Model not fitted yet")
        
        return {
            "slope": self.model.slope,
            "intercept": self.model.intercept,
            "r_squared": self.model.r_squared,
            "r_squared_adj": self.model.r_squared_adj,
            "std_error": self.model.std_error,
            "n_observations": self.model.n,
            "trend_direction": "increasing" if self.model.slope > 0 else "decreasing",
            "slope_magnitude": abs(self.model.slope)
        }
    
    def get_diagnostics(self) -> RegressionDiagnostics:
        """Get full model diagnostics."""
        if self.model is None or self.model.diagnostics is None:
            raise RuntimeError("Model not fitted yet")
        return self.model.diagnostics
    
    def get_residuals(self) -> List[float]:
        """Get model residuals."""
        if self.model is None:
            raise RuntimeError("Model not fitted yet")
        return self.model.residuals
    
    def get_fitted_values(self) -> List[float]:
        """Get fitted values from the model."""
        if self.model is None:
            raise RuntimeError("Model not fitted yet")
        return [self.model.predict(x) for x in self.model.x_data]
    
    def r_squared_interpretation(self) -> str:
        """Provide interpretation of R² value."""
        if self.model is None:
            return "Model not fitted"
        
        r2 = self.model.r_squared
        
        if math.isnan(r2):
            return "R² = NaN: This occurs when SS_tot = 0, meaning all y-values are identical."
        
        if r2 >= 0.95:
            return f"R² = {r2:.4f}: Excellent fit. Model explains {r2*100:.1f}% of variance."
        elif r2 >= 0.80:
            return f"R² = {r2:.4f}: Good fit. Model explains {r2*100:.1f}% of variance."
        elif r2 >= 0.50:
            return f"R² = {r2:.4f}: Moderate fit. Model explains {r2*100:.1f}% of variance."
        elif r2 >= 0.0:
            return f"R² = {r2:.4f}: Weak fit. Model explains {r2*100:.1f}% of variance."
        else:
            return f"R² = {r2:.4f}: Model performs worse than a horizontal line."
