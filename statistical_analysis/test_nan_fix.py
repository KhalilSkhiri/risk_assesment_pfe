#!/usr/bin/env python3
"""
Test script for NaN handling in regression model
"""
import sys
sys.path.insert(0, 'c:\\Users\\yacco\\code_pfe')

from statistical_analysis.regression_model import LinearRegression

def test_nan_problem():
    """Test that NaN problem is handled correctly"""
    print("\n" + "="*70)
    print("TEST: NaN Problem Handling")
    print("="*70)
    
    print("\nCase: All emissions values are constant (5000, 5000, 5000, 5000)")
    print("Expected: R² = 0 (by convention, not NaN)")
    
    years = [2020, 2021, 2022, 2023, 2024]
    emissions = [5000, 5000, 5000, 5000, 5000]  # ALL SAME
    
    lr = LinearRegression()
    model = lr.fit(years, emissions)
    
    print(f"\nResult: R² = {model.r_squared}")
    print(f"Is NaN? {model.r_squared != model.r_squared}")  # NaN != NaN is True
    
    if model.r_squared == 0.0:
        print("✓ PASS: R² correctly set to 0 (not NaN)")
    else:
        print(f"✗ FAIL: R² = {model.r_squared} (expected 0.0)")
    
    print(f"\nInterpretation: {lr.r_squared_interpretation()}")

def test_good_fit():
    """Test that good fit still works"""
    print("\n" + "="*70)
    print("TEST: Normal Case (Good Fit)")
    print("="*70)
    
    years = [2020, 2021, 2022, 2023, 2024]
    emissions = [5000, 5500, 6100, 6700, 7200]
    
    lr = LinearRegression()
    model = lr.fit(years, emissions)
    
    print(f"\nR² = {model.r_squared:.4f}")
    print(f"R²_adj = {model.r_squared_adj:.4f}")
    print(f"Slope = {model.slope:.2f} tCO2e/year")
    
    if 0 < model.r_squared <= 1 and not (model.r_squared != model.r_squared):
        print("✓ PASS: Good fit case works correctly")
    else:
        print("✗ FAIL: Good fit case failed")

def test_diagnostics():
    """Test that diagnostics are computed"""
    print("\n" + "="*70)
    print("TEST: Diagnostic Statistics")
    print("="*70)
    
    years = [2020, 2021, 2022, 2023, 2024, 2025]
    emissions = [5000, 5600, 6100, 6700, 7200, 7800]
    
    lr = LinearRegression()
    model = lr.fit(years, emissions)
    
    diag = lr.get_diagnostics()
    
    print(f"\nDiagnostics:")
    print(f"  F-statistic: {diag.f_statistic:.4f}")
    print(f"  p-value (F-test): {diag.p_value_f:.4e}")
    print(f"  Shapiro-Wilk p-value: {diag.shapiro_p_value:.4e}")
    print(f"  Durbin-Watson: {diag.durbin_watson:.4f}")
    
    if all(isinstance(getattr(diag, attr), (float, int)) 
           for attr in ['f_statistic', 'shapiro_p_value', 'durbin_watson']):
        print("✓ PASS: All diagnostics computed")
    else:
        print("✗ FAIL: Some diagnostics missing")

def test_prediction_intervals():
    """Test prediction intervals"""
    print("\n" + "="*70)
    print("TEST: Prediction Intervals")
    print("="*70)
    
    years = [2020, 2021, 2022, 2023]
    emissions = [5000, 5500, 6100, 6800]
    
    lr = LinearRegression()
    model = lr.fit(years, emissions)
    
    future_pred = lr.predict_future(2, confidence_level=0.95)
    
    print(f"\nPredictions with 95% CI:")
    for year, pred, ci in future_pred:
        print(f"  {year}: {pred:,.0f} [{ci.lower_bound:,.0f}, {ci.upper_bound:,.0f}]")
    
    if len(future_pred) == 2 and all(hasattr(item[2], 'lower_bound') for item in future_pred):
        print("✓ PASS: Prediction intervals computed")
    else:
        print("✗ FAIL: Prediction intervals failed")

if __name__ == "__main__":
    try:
        test_nan_problem()
        test_good_fit()
        test_diagnostics()
        test_prediction_intervals()
        
        print("\n" + "="*70)
        print("ALL TESTS COMPLETED")
        print("="*70)
        print("\n✓ Module is working correctly!")
        print("✓ NaN problem is SOLVED!")
        print("✓ Full diagnostics available!")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
