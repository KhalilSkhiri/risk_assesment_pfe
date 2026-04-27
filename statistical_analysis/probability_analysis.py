"""
Probability Analysis Module for Climate Risk Assessment

This module provides probabilistic tools for assessing climate risk
and emission scenarios with confidence intervals.
"""

import math
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class RiskLevel(Enum):
    """Emission risk categories."""
    LOW = "LOW"           # < 25th percentile
    MEDIUM = "MEDIUM"     # 25th - 75th percentile
    HIGH = "HIGH"         # > 75th percentile
    CRITICAL = "CRITICAL" # > 90th percentile


@dataclass
class ConfidenceInterval:
    """Confidence interval for predictions."""
    lower_bound: float
    point_estimate: float
    upper_bound: float
    confidence_level: float  # 0.95 for 95% CI
    
    def contains(self, value: float) -> bool:
        """Check if value is within confidence interval."""
        return self.lower_bound <= value <= self.upper_bound
    
    def width(self) -> float:
        """Return width of confidence interval."""
        return self.upper_bound - self.lower_bound


class ProbabilityAnalyzer:
    """
    Analyze emission data probabilistically.
    
    Provides tools for:
    - Statistical distribution analysis
    - Confidence intervals for predictions
    - Risk categorization based on historical volatility
    """
    
    def __init__(self, data: List[float]):
        """
        Initialize analyzer with emission data.
        
        Args:
            data: List of historical emission values (tCO2e)
        """
        self.data = data
        self.mean = self._calculate_mean()
        self.std_dev = self._calculate_std_dev()
        self.variance = self.std_dev ** 2
    
    def _calculate_mean(self) -> float:
        """Calculate mean of data."""
        return sum(self.data) / len(self.data) if self.data else 0
    
    def _calculate_std_dev(self) -> float:
        """Calculate standard deviation of data."""
        if len(self.data) < 2:
            return 0
        
        variance = sum((x - self.mean) ** 2 for x in self.data) / (len(self.data) - 1)
        return math.sqrt(variance)
    
    def get_statistics(self) -> Dict[str, float]:
        """Get descriptive statistics."""
        if not self.data:
            return {}
        
        sorted_data = sorted(self.data)
        n = len(sorted_data)
        
        return {
            "mean": self.mean,
            "median": sorted_data[n // 2],
            "std_dev": self.std_dev,
            "variance": self.variance,
            "min": min(self.data),
            "max": max(self.data),
            "range": max(self.data) - min(self.data),
            "coefficient_of_variation": self.std_dev / self.mean if self.mean != 0 else 0
        }
    
    def percentile(self, p: float) -> float:
        """
        Calculate percentile value.
        
        Args:
            p: Percentile (0-100)
        
        Returns:
            Value at given percentile
        """
        if not self.data or p < 0 or p > 100:
            raise ValueError("Invalid percentile value")
        
        sorted_data = sorted(self.data)
        index = (p / 100) * (len(sorted_data) - 1)
        
        lower_index = int(index)
        upper_index = min(lower_index + 1, len(sorted_data) - 1)
        
        if lower_index == upper_index:
            return sorted_data[lower_index]
        
        # Linear interpolation
        fraction = index - lower_index
        return (sorted_data[lower_index] * (1 - fraction) + 
                sorted_data[upper_index] * fraction)
    
    def confidence_interval(self, 
                          point_estimate: float, 
                          confidence_level: float = 0.95) -> ConfidenceInterval:
        """
        Calculate confidence interval for a point estimate.
        
        Args:
            point_estimate: The estimated value (e.g., predicted emissions)
            confidence_level: Confidence level (0.95 for 95% CI)
        
        Returns:
            ConfidenceInterval object with bounds
        """
        if self.std_dev == 0:
            return ConfidenceInterval(point_estimate, point_estimate, 
                                     point_estimate, confidence_level)
        
        # Use z-score (normal approximation)
        z_score = self._get_z_score(confidence_level)
        margin_of_error = z_score * self.std_dev
        
        return ConfidenceInterval(
            lower_bound=point_estimate - margin_of_error,
            point_estimate=point_estimate,
            upper_bound=point_estimate + margin_of_error,
            confidence_level=confidence_level
        )
    
    def categorize_risk(self, value: float) -> RiskLevel:
        """
        Categorize emission value as risk level.
        
        Args:
            value: Emission value to categorize
        
        Returns:
            RiskLevel enum indicating risk category
        """
        p25 = self.percentile(25)
        p75 = self.percentile(75)
        p90 = self.percentile(90)
        
        if value > p90:
            return RiskLevel.CRITICAL
        elif value > p75:
            return RiskLevel.HIGH
        elif value >= p25:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    def probability_above_threshold(self, threshold: float) -> float:
        """
        Estimate probability that emissions exceed threshold.
        
        Uses normal distribution approximation.
        
        Args:
            threshold: Emission threshold in tCO2e
        
        Returns:
            Probability (0-1) that emissions exceed threshold
        """
        if self.std_dev == 0:
            return 1.0 if self.mean > threshold else 0.0
        
        z_score = (threshold - self.mean) / self.std_dev
        return 1 - self._normal_cdf(z_score)
    
    def probability_in_range(self, lower: float, upper: float) -> float:
        """
        Estimate probability that emissions fall within range.
        
        Args:
            lower: Lower bound of range
            upper: Upper bound of range
        
        Returns:
            Probability (0-1) that emissions fall in range
        """
        if self.std_dev == 0:
            if lower <= self.mean <= upper:
                return 1.0
            else:
                return 0.0
        
        z_lower = (lower - self.mean) / self.std_dev
        z_upper = (upper - self.mean) / self.std_dev
        
        return self._normal_cdf(z_upper) - self._normal_cdf(z_lower)
    
    @staticmethod
    def _get_z_score(confidence_level: float) -> float:
        """Get z-score for given confidence level."""
        scores = {
            0.90: 1.645,
            0.95: 1.96,
            0.99: 2.576
        }
        return scores.get(confidence_level, 1.96)
    
    @staticmethod
    def _normal_cdf(z: float) -> float:
        """Approximate cumulative distribution function for standard normal."""
        return (1 + math.erf(z / math.sqrt(2))) / 2
