"""
Unit Tests for Statistical Analysis Module

Tests for regression model, probability analysis, and utility functions.
Run with: python -m pytest tests/test_statistical_analysis.py
"""

import pytest
import math
from statistical_analysis.regression_model import LinearRegression, RegressionModel
from statistical_analysis.probability_analysis import ProbabilityAnalyzer, RiskLevel, ConfidenceInterval
from statistical_analysis.utils import (
    validate_data,
    normalize_years,
    calculate_moving_average,
    calculate_yoy_change,
    detect_outliers,
    summarize_emissions
)


class TestLinearRegression:
    """Tests for LinearRegression class."""
    
    def test_simple_fit(self):
        """Test basic regression fit."""
        regressor = LinearRegression()
        x = [1, 2, 3, 4]
        y = [2, 4, 6, 8]
        
        model = regressor.fit(x, y)
        
        assert model.slope == pytest.approx(2.0)
        assert model.intercept == pytest.approx(0.0)
        assert model.r_squared == pytest.approx(1.0)
    
    def test_prediction(self):
        """Test prediction on fitted model."""
        regressor = LinearRegression()
        x = [1, 2, 3, 4]
        y = [2, 4, 6, 8]
        
        regressor.fit(x, y)
        pred = regressor.predict(5)
        
        assert pred == pytest.approx(10.0)
    
    def test_batch_prediction(self):
        """Test batch predictions."""
        regressor = LinearRegression()
        x = [1, 2, 3]
        y = [1, 2, 3]
        
        model = regressor.fit(x, y)
        preds = model.predict_batch([4, 5, 6])
        
        assert len(preds) == 3
        assert preds[0] == pytest.approx(4.0)
        assert preds[2] == pytest.approx(6.0)
    
    def test_future_predictions(self):
        """Test predicting future years."""
        regressor = LinearRegression()
        x = [2020, 2021, 2022, 2023]
        y = [100, 110, 120, 130]
        
        regressor.fit(x, y)
        future = regressor.predict_future(2)
        
        assert len(future) == 2
        assert future[0][0] == 2024
        assert future[1][0] == 2025
    
    def test_insufficient_data(self):
        """Test error on insufficient data."""
        regressor = LinearRegression()
        
        with pytest.raises(ValueError):
            regressor.fit([1], [1])
    
    def test_mismatched_lengths(self):
        """Test error on mismatched data lengths."""
        regressor = LinearRegression()
        
        with pytest.raises(ValueError):
            regressor.fit([1, 2, 3], [1, 2])
    
    def test_constant_x_values(self):
        """Test error on constant x values."""
        regressor = LinearRegression()
        
        with pytest.raises(ValueError):
            regressor.fit([1, 1, 1], [2, 3, 4])
    
    def test_predict_before_fit(self):
        """Test error when predicting before fit."""
        regressor = LinearRegression()
        
        with pytest.raises(RuntimeError):
            regressor.predict(5)
    
    def test_statistics(self):
        """Test regression statistics."""
        regressor = LinearRegression()
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]
        
        regressor.fit(x, y)
        stats = regressor.get_statistics()
        
        assert "slope" in stats
        assert "r_squared" in stats
        assert "trend_direction" in stats
        assert stats["trend_direction"] == "increasing"


class TestProbabilityAnalyzer:
    """Tests for ProbabilityAnalyzer class."""
    
    def test_mean_calculation(self):
        """Test mean calculation."""
        data = [100, 200, 300]
        analyzer = ProbabilityAnalyzer(data)
        
        assert analyzer.mean == pytest.approx(200.0)
    
    def test_std_dev_calculation(self):
        """Test standard deviation calculation."""
        data = [1, 2, 3, 4, 5]
        analyzer = ProbabilityAnalyzer(data)
        
        expected_std = math.sqrt(2.5)
        assert analyzer.std_dev == pytest.approx(expected_std)
    
    def test_statistics(self):
        """Test statistics dictionary."""
        data = [100, 200, 300, 400, 500]
        analyzer = ProbabilityAnalyzer(data)
        
        stats = analyzer.get_statistics()
        
        assert "mean" in stats
        assert "median" in stats
        assert "std_dev" in stats
        assert "variance" in stats
        assert stats["mean"] == 300
        assert stats["median"] == 300
    
    def test_percentile(self):
        """Test percentile calculation."""
        data = [10, 20, 30, 40, 50]
        analyzer = ProbabilityAnalyzer(data)
        
        assert analyzer.percentile(0) == 10
        assert analyzer.percentile(50) == 30
        assert analyzer.percentile(100) == 50
    
    def test_confidence_interval(self):
        """Test confidence interval calculation."""
        data = [100, 100, 100, 100, 100]  # No variance
        analyzer = ProbabilityAnalyzer(data)
        
        ci = analyzer.confidence_interval(100, confidence_level=0.95)
        
        assert ci.point_estimate == 100
        assert ci.lower_bound == 100
        assert ci.upper_bound == 100
    
    def test_risk_categorization(self):
        """Test risk level categorization."""
        data = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
        analyzer = ProbabilityAnalyzer(data)
        
        # Low risk (< 25th percentile)
        assert analyzer.categorize_risk(150) == RiskLevel.LOW
        
        # Medium risk (25-75 percentile)
        assert analyzer.categorize_risk(550) == RiskLevel.MEDIUM
        
        # High risk (> 75 percentile)
        assert analyzer.categorize_risk(850) == RiskLevel.HIGH
    
    def test_probability_above_threshold(self):
        """Test probability above threshold."""
        data = [100, 100, 100, 100, 100]  # All same value
        analyzer = ProbabilityAnalyzer(data)
        
        prob = analyzer.probability_above_threshold(100)
        assert prob == pytest.approx(0.5, abs=0.1)  # ~50% at mean
        
        prob = analyzer.probability_above_threshold(50)
        assert prob > 0.9  # Almost certainly above 50
    
    def test_probability_in_range(self):
        """Test probability within range."""
        data = [100, 100, 100, 100, 100]
        analyzer = ProbabilityAnalyzer(data)
        
        prob = analyzer.probability_in_range(50, 150)
        assert prob > 0.95  # Very likely to be in this range


class TestUtilityFunctions:
    """Tests for utility functions."""
    
    def test_validate_data(self):
        """Test data validation."""
        # Valid data
        assert validate_data([1, 2, 3]) == True
        
        # Empty data
        with pytest.raises(ValueError):
            validate_data([])
        
        # None values
        with pytest.raises(ValueError):
            validate_data([1, None, 3])
        
        # Negative values
        with pytest.raises(ValueError):
            validate_data([1, -2, 3])
    
    def test_normalize_years(self):
        """Test year normalization."""
        years = [2020, 2021, 2022, 2023]
        normalized = normalize_years(years)
        
        assert normalized == [0, 1, 2, 3]
    
    def test_moving_average(self):
        """Test moving average calculation."""
        data = [1, 2, 3, 4, 5]
        ma = calculate_moving_average(data, window_size=3)
        
        assert len(ma) == 3
        assert ma[0] == 2.0  # (1+2+3)/3
        assert ma[2] == 4.0  # (3+4+5)/3
    
    def test_yoy_change(self):
        """Test year-over-year change."""
        data = [100, 150, 120, 180]
        changes = calculate_yoy_change(data)
        
        assert len(changes) == 3
        assert changes[0] == 50.0  # (150-100)/100 * 100
        assert changes[1] == -20.0  # (120-150)/150 * 100
    
    def test_detect_outliers(self):
        """Test outlier detection."""
        data = [100, 100, 100, 100, 500]  # 500 is outlier
        outlier_idx, outlier_vals = detect_outliers(data, threshold=2.0)
        
        assert len(outlier_idx) > 0
        assert 500 in outlier_vals
    
    def test_summarize_emissions(self):
        """Test emissions summary."""
        data = [100, 200, 300]
        summary = summarize_emissions(data)
        
        assert summary["count"] == 3
        assert summary["min"] == 100
        assert summary["max"] == 300
        assert summary["mean"] == 200
        assert summary["total"] == 600


class TestConfidenceInterval:
    """Tests for ConfidenceInterval dataclass."""
    
    def test_contains(self):
        """Test if value is within interval."""
        ci = ConfidenceInterval(100, 150, 200, 0.95)
        
        assert ci.contains(150) == True
        assert ci.contains(100) == True
        assert ci.contains(200) == True
        assert ci.contains(50) == False
        assert ci.contains(250) == False
    
    def test_width(self):
        """Test interval width."""
        ci = ConfidenceInterval(100, 150, 200, 0.95)
        
        assert ci.width() == 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
