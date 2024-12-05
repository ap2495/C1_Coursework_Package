import pytest
import numpy as np
import re
from dual_autodiff.dual import Dual

# Implement a test function for every method in dual

def test_init():
    test_number = Dual(5.0, 7.0)
    assert test_number.real == 5.0
    assert test_number.dual == 7.0

def test_add():
    test_number1 = Dual(5.0, 7.0)
    test_number2 = Dual(3.0, 2.0)
    test_sum = test_number1 + test_number2
    assert test_sum.real == 8.0
    assert test_sum.dual == 9.0

def test_sub():
    test_number1 = Dual(5.0, 7.0)
    test_number2 = Dual(3.0, 2.0)
    test_diff = test_number1 - test_number2
    assert test_diff.real == 2.0
    assert test_diff.dual == 5.0

def test_mul():
    test_number1 = Dual(5.0, 7.0)
    test_number2 = Dual(3.0, 2.0)
    test_prod = test_number1 * test_number2
    expected_real = 5.0 * 3.0
    expected_dual = 5.0 * 2.0 + 7.0 * 3.0
    assert test_prod.real == expected_real
    assert test_prod.dual == expected_dual

# From now on I will change the 7.0 to a 1.0, so that the dual number would reflect the derivative
def test_pow():
    test_number = Dual(5.0, 1.0)
    power = test_number ** 3
    expected_real = 5.0 ** 3
    expected_dual = 3 * 5.0 ** (3 - 1) * 1.0
    assert power.real == expected_real
    assert power.dual == expected_dual

def test_sin():
    test_number = Dual(5.0, 1.0)
    sin_test = test_number.sin()
    expected_real = np.sin(5.0)
    expected_dual = np.cos(5.0) * 1.0
    assert sin_test.real == pytest.approx(expected_real, rel=1e-6)
    assert sin_test.dual == pytest.approx(expected_dual, rel=1e-6)


def test_cos():
    test_number = Dual(5.0, 1.0)
    cos_test = test_number.cos()
    expected_real = np.cos(5.0)
    expected_dual = -np.sin(5.0) * 1.0
    assert cos_test.real == pytest.approx(expected_real, rel=1e-6)
    assert cos_test.dual == pytest.approx(expected_dual, rel=1e-6)

def test_tan():
    # Test normal case
    test_number = Dual(5.0, 1.0)
    tan_test = test_number.tan()
    expected_real = np.tan(5.0)
    expected_dual = (1 / np.cos(5.0)) ** 2 * 1.0
    assert tan_test.real == pytest.approx(expected_real, rel=1e-6)
    assert tan_test.dual == pytest.approx(expected_dual, rel=1e-6)

    # Test exception for exactly pi/2 + n*pi
    invalid_number_test = Dual(np.pi / 2, 1.0)
    with pytest.raises(ValueError, match=re.escape("Real value cannot be within 1e-10 of pi/2 + n*pi. Tan and 1/cos(real) are both undefined at these points.")):
        invalid_number_test.tan()

    # Test warning for value close to pi/2 + n*pi
    # I used ChatGPT to figure this out
    almost_invalid = Dual(np.pi / 2 + 1e-8, 1.0)
    with pytest.warns(RuntimeWarning, match=re.escape("The proximity of the real value is less than 1e-6 to pi/2 + n*pi. Beware of potential numerical instability.")):
        tan_almost = almost_invalid.tan()
        # Check the output even when warning is raised
        expected_real = np.tan(almost_invalid.real)
        expected_dual = (1 / np.cos(almost_invalid.real)) ** 2 * 1.0
        assert tan_almost.real == pytest.approx(expected_real, rel=1e-6)
        assert tan_almost.dual == pytest.approx(expected_dual, rel=1e-6)

def test_log():
    test_number = Dual(5.0, 1.0)
    log_test = test_number.log()
    expected_real = np.log(5.0)
    expected_dual = 1 / 5.0 * 1.0
    assert log_test.real == pytest.approx(expected_real, rel=1e-6)
    assert log_test.dual == pytest.approx(expected_dual, rel=1e-6)

    invalid_number1 = Dual(0.0, 1.0)
    with pytest.raises(ValueError) as excinfo:
        invalid_number1.log()
    assert "Log cannot take in 0 or less than 0 for the real value. Real value must be greater than zero." in str(excinfo)

    invalid_number2 = Dual(-5.0, 1.0)
    with pytest.raises(ValueError) as excinfo2:
        invalid_number2.log()
    assert "Log cannot take in 0 or less than 0 for the real value. Real value must be greater than zero." in str(excinfo2)

    # Test exception when 0 < self.real < tolerance_exception (1e-10)
    small_number = Dual(1e-11, 1.0)
    with pytest.raises(ValueError, match=re.escape("Real value is less than 1e-10. Log is undefined at zero, beware of potential overflow.")):
        small_number.log()

    # Test warning when tolerance_exception < self.real < tolerance_warning (1e-10 to 1e-6)
    almost_zero = Dual(1e-7, 1.0)
    with pytest.warns(RuntimeWarning, match=re.escape("Log is undefined for x <= 0. The proximity of the real value to 0 is within 1e-6. Beware of potential numerical instability.")):
        log_almost_zero = almost_zero.log()
        # Check the output even when warning is raised
        expected_real = np.log(1e-7)
        expected_dual = 1 / 1e-7 * 1.0
        assert log_almost_zero.real == pytest.approx(expected_real, rel=1e-6)
        assert log_almost_zero.dual == pytest.approx(expected_dual, rel=1e-6)

    

def test_exp():
    test_number = Dual(5.0, 1.0)
    exp_test = test_number.exp()
    expected_real = np.exp(5.0)
    expected_dual = np.exp(5.0) * 1.0

    assert exp_test.real == expected_real
    assert exp_test.dual == expected_dual
