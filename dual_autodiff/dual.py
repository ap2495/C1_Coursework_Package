
import numpy as np
import warnings

class Dual:
    
    def __init__(self, real, dual):

        self.real = real
        self.dual = dual

    def __add__(self, other):

        return Dual(self.real + other.real, self.dual + other.dual)
    
    def __sub__(self, other):

        return Dual(self.real - other.real, self.dual - other.dual)
    
    def __mul__(self, other):

        return Dual(self.real * other.real, self.real * other.dual + self.dual * other.real)
    
    def __pow__(self, exponent):

        return Dual(self.real ** exponent, exponent * self.real ** (exponent - 1) * self.dual)
    
    def sin(self):

        return Dual( np.sin(self.real), np.cos(self.real) * self.dual )
    
    def cos(self):

        return Dual( np.cos(self.real), - np.sin(self.real) * self.dual )
    
    def tan(self):
        tolerance_exception = 1e-10
        tolerance_warning = 1e-6  
        n = round((self.real - np.pi / 2) / np.pi)
        pi_over_2_plus_n_pi = np.pi / 2 + n * np.pi
        delta = abs(self.real - pi_over_2_plus_n_pi)
        if delta < tolerance_exception:
            raise ValueError("Real value cannot be within 1e-10 of pi/2 + n*pi. Tan and 1/cos(real) are both undefined at these points.")
        elif delta < tolerance_warning:
            warnings.warn(
                "The proximity of the real value is less than 1e-6 to pi/2 + n*pi. Beware of potential numerical instability.",
                RuntimeWarning
            )
        
        return Dual( np.tan(self.real), (1/np.cos(self.real))**2  * self.dual)
    
    def log(self):
        tolerance_exception = 1e-10
        tolerance_warning = 1e-6
        if (self.real) > tolerance_exception and (self.real < tolerance_warning):
            warnings.warn(
                "Log is undefined for x <= 0. The proximity of the real value to 0 is within 1e-6. Beware of potential numerical instability.",
                RuntimeWarning
            )
        elif 0.0 < self.real <= tolerance_exception:
            raise ValueError("Real value is less than 1e-10. Log is undefined at zero, beware of potential overflow.")
        elif self.real <= 0:
            raise ValueError('Log cannot take in 0 or less than 0 for the real value. Real value must be greater than zero.')
        
        return Dual( np.log(self.real), 1/self.real * self.dual )
        
        
    
    def exp(self):

        return Dual( np.exp(self.real), np.exp(self.real) * self.dual )
    
    #def __truediv__(self, other):
        #return Dual(self.real / other.real, self.dual / other.dual)
    
    



