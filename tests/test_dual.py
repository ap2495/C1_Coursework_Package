import pytest
import numpy as np
import re
from dual_autodiff.dual import Dual

# Test initialization of Dual numbers
def test_init():
    # Test creating a Dual number with real and dual parts
    test_number = Dual(5.0, 7.0)
    assert test_number.real == 5.0
    assert test_number.dual == 7.0

# Test addition of Dual numbers
def test_add():
    test_number1 = Dual(5.0, 7.0)
    test_number2 = Dual(3.0, 2.0)
    test_sum = test_number1 + test_number2
    assert test_sum.real == 8.0
    assert test_sum.dual == 9.0

# Test subtraction of Dual numbers
def test_sub():
    test_number1 = Dual(5.0, 7.0)
    test_number2 = Dual(3.0, 2.0)
    test_diff = test_number1 - test_number2
    assert test_diff.real == 2.0
    assert test_diff.dual == 5.0

# Test multiplication of Dual numbers
def test_mul():
    test_number1 = Dual(5.0, 7.0)
    test_number2 = Dual(3.0, 2.0)
    test_prod = test_number1 * test_number2
    expected_real = 5.0 * 3.0
    expected_dual = 5.0 * 2.0 + 7.0 * 3.0
    assert test_prod.real == expected_real
    assert test_prod.dual == expected_dual

# Test exponentiation of Dual numbers
def test_pow():
    test_number = Dual(5.0, 1.0)  # Set dual to 1.0 for derivative representation
    power = test_number ** 3
    expected_real = 5.0 ** 3
    expected_dual = 3 * 5.0 ** (3 - 1) * 1.0
    assert power.real == expected_real
    assert power.dual == expected_dual

# Test sine function with Dual numbers
def test_sin():
    test_number = Dual(5.0, 1.0)
    sin_test = test_number.sin()
    expected_real = np.sin(5.0)
    expected_dual = np.cos(5.0) * 1.0
    assert sin_test.real == pytest.approx(expected_real, rel=1e-6)
    assert sin_test.dual == pytest.approx(expected_dual, rel=1e-6)

# Test cosine function with Dual numbers
def test_cos():
    test_number = Dual(5.0, 1.0)
    cos_test = test_number.cos()
    expected_real = np.cos(5.0)
    expected_dual = -np.sin(5.0) * 1.0
    assert cos_test.real == pytest.approx(expected_real, rel=1e-6)
    assert cos_test.dual == pytest.approx(expected_dual, rel=1e-6)

# Test tangent function with Dual numbers
def test_tan():
    test_number = Dual(5.0, 1.0)  # Normal case
    tan_test = test_number.tan()
    expected_real = np.tan(5.0)
    expected_dual = (1 / np.cos(5.0)) ** 2 * 1.0
    assert tan_test.real == pytest.approx(expected_real, rel=1e-6)
    assert tan_test.dual == pytest.approx(expected_dual, rel=1e-6)

    # Test exception for undefined values of tan
    invalid_number_test = Dual(np.pi / 2, 1.0)
    with pytest.raises(ValueError, match=re.escape("Real value cannot be within 1e-10 of pi/2 + n*pi. Tan and 1/cos(real) are both undefined at these points.")):
        invalid_number_test.tan()

    # Test warning for values close to undefined tan points
    almost_invalid = Dual(np.pi / 2 + 1e-8, 1.0)
    with pytest.warns(RuntimeWarning, match=re.escape("The proximity of the real value is less than 1e-6 to pi/2 + n*pi. Beware of potential numerical instability.")):
        tan_almost = almost_invalid.tan()
        expected_real = np.tan(almost_invalid.real)
        expected_dual = (1 / np.cos(almost_invalid.real)) ** 2 * 1.0
        assert tan_almost.real == pytest.approx(expected_real, rel=1e-6)
        assert tan_almost.dual == pytest.approx(expected_dual, rel=1e-6)

# Test natural logarithm with Dual numbers
def test_log():
    test_number = Dual(5.0, 1.0)
    log_test = test_number.log()
    expected_real = np.log(5.0)
    expected_dual = 1 / 5.0 * 1.0
    assert log_test.real == pytest.approx(expected_real, rel=1e-6)
    assert log_test.dual == pytest.approx(expected_dual, rel=1e-6)

    # Test exception for log of non-positive real values
    invalid_number1 = Dual(0.0, 1.0)
    with pytest.raises(ValueError) as excinfo:
        invalid_number1.log()
    assert "Log cannot take in 0 or less than 0 for the real value. Real value must be greater than zero." in str(excinfo)

    invalid_number2 = Dual(-5.0, 1.0)
    with pytest.raises(ValueError) as excinfo2:
        invalid_number2.log()
    assert "Log cannot take in 0 or less than 0 for the real value. Real value must be greater than zero." in str(excinfo2)

    # Test exception for very small real values
    small_number = Dual(1e-11, 1.0)
    with pytest.raises(ValueError, match=re.escape("Real value is less than 1e-10. Log is undefined at zero, beware of potential overflow.")):
        small_number.log()

    # Test warning for real values near zero
    almost_zero = Dual(1e-7, 1.0)
    with pytest.warns(RuntimeWarning, match=re.escape("Log is undefined for x <= 0. The proximity of the real value to 0 is within 1e-6. Beware of potential numerical instability.")):
        log_almost_zero = almost_zero.log()
        expected_real = np.log(1e-7)
        expected_dual = 1 / 1e-7 * 1.0
        assert log_almost_zero.real == pytest.approx(expected_real, rel=1e-6)
        assert log_almost_zero.dual == pytest.approx(expected_dual, rel=1e-6)

# Test exponential function with Dual numbers
def test_exp():
    test_number = Dual(5.0, 1.0)
    exp_test = test_number.exp()
    expected_real = np.exp(5.0)
    expected_dual = np.exp(5.0) * 1.0
    assert exp_test.real == expected_real
    assert exp_test.dual == expected_dual

# Test initialization of Dual numbers with arrays
def test_init_array():
    test_number = Dual(np.array([1.0, 2.0]), np.array([3.0, 4.0]))
    assert np.all(test_number.real == np.array([1.0, 2.0]))
    assert np.all(test_number.dual == np.array([3.0, 4.0]))

# Test addition of Dual arrays
def test_add_array():
    test_number1 = Dual(np.array([1.0, 2.0]), np.array([3.0, 4.0]))
    test_number2 = Dual(np.array([5.0, 6.0]), np.array([7.0, 8.0]))
    test_sum = test_number1 + test_number2
    assert np.all(test_sum.real == np.array([6.0, 8.0]))
    assert np.all(test_sum.dual == np.array([10.0, 12.0]))

# Test subtraction of Dual arrays
def test_sub_array():
    test_number1 = Dual(np.array([5.0, 6.0]), np.array([7.0, 8.0]))
    test_number2 = Dual(np.array([3.0, 2.0]), np.array([1.0, 2.0]))
    test_diff = test_number1 - test_number2
    assert np.all(test_diff.real == np.array([2.0, 4.0]))
    assert np.all(test_diff.dual == np.array([6.0, 6.0]))

# Test multiplication of Dual arrays
def test_mul_array():
    test_number1 = Dual(np.array([5.0, 2.0]), np.array([3.0, 1.0]))
    test_number2 = Dual(np.array([4.0, 3.0]), np.array([2.0, 2.0]))
    test_prod = test_number1 * test_number2
    expected_real = np.array([5.0 * 4.0, 2.0 * 3.0])
    expected_dual = np.array([5.0 * 2.0 + 3.0 * 4.0, 2.0 * 2.0 + 1.0 * 3.0])
    assert np.all(test_prod.real == expected_real)
    assert np.all(test_prod.dual == expected_dual)

# Test exponentiation of Dual arrays
def test_pow_array():
    test_number = Dual(np.array([2.0, 3.0]), np.array([1.0, 1.0]))
    power = test_number ** 2
    expected_real = np.array([4.0, 9.0])
    expected_dual = np.array([2 * 2.0 * 1.0, 2 * 3.0 * 1.0])
    assert np.all(power.real == expected_real)
    assert np.all(power.dual == expected_dual)

# Test sine function with Dual arrays
def test_sin_array():
    test_number = Dual(np.array([0.0, np.pi / 4]), np.array([1.0, 1.0]))
    sin_test = test_number.sin()
    expected_real = np.sin(np.array([0.0, np.pi / 4]))
    expected_dual = np.cos(np.array([0.0, np.pi / 4]))
    assert sin_test.real == pytest.approx(expected_real, rel=1e-6)
    assert sin_test.dual == pytest.approx(expected_dual, rel=1e-6)

# Test cosine function with Dual arrays
def test_cos_array():
    test_number = Dual(np.array([0.0, np.pi / 4]), np.array([1.0, 1.0]))
    cos_test = test_number.cos()
    expected_real = np.cos(np.array([0.0, np.pi / 4]))
    expected_dual = -np.sin(np.array([0.0, np.pi / 4]))
    assert cos_test.real == pytest.approx(expected_real, rel=1e-6)
    assert cos_test.dual == pytest.approx(expected_dual, rel=1e-6)

# Test tangent function with Dual arrays
def test_tan_array():
    test_number = Dual(np.array([0.0, np.pi / 4]), np.array([1.0, 1.0]))
    tan_test = test_number.tan()
    expected_real = np.tan(np.array([0.0, np.pi / 4]))
    expected_dual = (1 / np.cos(np.array([0.0, np.pi / 4]))) ** 2
    assert tan_test.real == pytest.approx(expected_real, rel=1e-6)
    assert tan_test.dual == pytest.approx(expected_dual, rel=1e-6)

# Test natural logarithm with Dual arrays
def test_log_array():
    test_number = Dual(np.array([2.0, 3.0]), np.array([1.0, 1.0]))
    log_test = test_number.log()
    expected_real = np.log(np.array([2.0, 3.0]))
    expected_dual = 1 / np.array([2.0, 3.0])
    assert log_test.real == pytest.approx(expected_real, rel=1e-6)
    assert log_test.dual == pytest.approx(expected_dual, rel=1e-6)

# Test exponential function with Dual arrays
def test_exp_array():
    test_number = Dual(np.array([2.0, 3.0]), np.array([1.0, 1.0]))
    exp_test = test_number.exp()
    expected_real = np.exp(np.array([2.0, 3.0]))
    expected_dual = np.exp(np.array([2.0, 3.0]))
    assert exp_test.real == pytest.approx(expected_real, rel=1e-6)
    assert exp_test.dual == pytest.approx(expected_dual, rel=1e-6)

# Test exception for mismatched shapes in array inputs
def test_shape_mismatch_exception():
    real = np.array([1.0, 2.0, 3.0])
    dual = np.array([4.0, 5.0])  # Mismatched shape
    with pytest.raises(ValueError, match="Shape mismatch"):
        Dual(real, dual)
