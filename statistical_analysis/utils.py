"""
Utility functions for statistical analysis.

Provides common helper functions for data validation,
normalization, and processing.
"""

from typing import List, Tuple, Dict, Union


def validate_data(data: List[Union[int, float]]) -> bool:
    """
    Validate emission data for statistical analysis.
    
    Args:
        data: List of emission values
    
    Returns:
        True if data is valid, raises ValueError otherwise
    
    Raises:
        ValueError: If data is empty, contains None, or has negative values
    """
    if not data:
        raise ValueError("Data cannot be empty")
    
    if any(x is None for x in data):
        raise ValueError("Data contains None values")
    
    if any(x < 0 for x in data):
        raise ValueError("Emission values cannot be negative")
    
    return True


def normalize_years(years: List[Union[int, float]]) -> List[float]:
    """
    Normalize year values for regression analysis.
    
    Converts years to relative indices (0, 1, 2, ...)
    for numerical stability in regression.
    
    Args:
        years: List of years or time periods
    
    Returns:
        List of normalized indices
    """
    if not years:
        return []
    
    min_year = min(years)
    return [year - min_year for year in years]


def calculate_moving_average(data: List[float], window_size: int) -> List[float]:
    """
    Calculate moving average of emission data.
    
    Args:
        data: List of emission values
        window_size: Size of moving window
    
    Returns:
        List of moving averages (shorter than original if window_size > 1)
    """
    if window_size < 1:
        raise ValueError("Window size must be >= 1")
    
    if window_size > len(data):
        raise ValueError("Window size cannot exceed data length")
    
    moving_avg = []
    for i in range(len(data) - window_size + 1):
        window = data[i:i + window_size]
        avg = sum(window) / window_size
        moving_avg.append(avg)
    
    return moving_avg


def calculate_yoy_change(data: List[float]) -> List[float]:
    """
    Calculate year-over-year percentage change.
    
    Args:
        data: List of emission values (chronological order)
    
    Returns:
        List of YoY percentage changes (one element shorter than input)
    """
    if len(data) < 2:
        raise ValueError("Need at least 2 data points for YoY calculation")
    
    changes = []
    for i in range(1, len(data)):
        if data[i-1] == 0:
            change = 0  # Handle division by zero
        else:
            change = ((data[i] - data[i-1]) / data[i-1]) * 100
        changes.append(change)
    
    return changes


def format_confidence_interval(ci_lower: float, ci_upper: float, 
                              precision: int = 2) -> str:
    """
    Format confidence interval for display.
    
    Args:
        ci_lower: Lower bound of interval
        ci_upper: Upper bound of interval
        precision: Decimal places for rounding
    
    Returns:
        Formatted string representation
    """
    return f"[{ci_lower:.{precision}f}, {ci_upper:.{precision}f}]"


def summarize_emissions(data: List[float]) -> Dict[str, float]:
    """
    Create summary statistics for emissions data.
    
    Args:
        data: List of emission values
    
    Returns:
        Dictionary with summary statistics
    """
    if not data:
        return {}
    
    sorted_data = sorted(data)
    n = len(sorted_data)
    
    return {
        "count": n,
        "min": min(data),
        "max": max(data),
        "mean": sum(data) / n,
        "median": sorted_data[n // 2],
        "total": sum(data)
    }


def detect_outliers(data: List[float], threshold: float = 2.0) -> Tuple[List[int], List[float]]:
    """
    Detect outliers using z-score method.
    
    Args:
        data: List of emission values
        threshold: Z-score threshold (default 2.0 = 95% confidence)
    
    Returns:
        Tuple of (indices of outliers, outlier values)
    """
    import math
    
    if len(data) < 2:
        return [], []
    
    mean = sum(data) / len(data)
    variance = sum((x - mean) ** 2 for x in data) / (len(data) - 1)
    std_dev = math.sqrt(variance)
    
    if std_dev == 0:
        return [], []
    
    outliers_idx = []
    outliers_val = []
    
    for i, x in enumerate(data):
        z_score = abs((x - mean) / std_dev)
        if z_score > threshold:
            outliers_idx.append(i)
            outliers_val.append(x)
    
    return outliers_idx, outliers_val
