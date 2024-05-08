import numpy as np
from .general_model import PCNNModel

class FLM(PCNNModel):
    """
    Feature Linking Model:
    - given by:
        1) U_ij[n] = f * U_ij[n-1] + (SumOf{M_kl*Y_kl[n-1] + S_ij} )*(1 + beta * SumOf{W_kl*Y_kl[n-1]} - d)
        2) Theta_ij[n] = g * Theta_ij[n-1] - Vtheta * Y_ij[n-1]
        3) Y_ij[n] = 1 if U_ij[n] > Theta_ij[n] else 0
    """

    def __init__(self, shape, kernel_type, kernel_size):
        super(FLM, self).__init__(shape)
        '''
        '''
        self.v_theta = 500
        self.Theta = np.ones(shape) * self.v_theta

        self.M = self.choose_kernel(kernel_type, kernel_size)
        self.W = self.choose_kernel(kernel_type, kernel_size)

    def iterate(self, S):
        """
        1) U_ij[n] = f * U_ij[n-1] + (SumOf{M_kl*Y_kl[n-1] + S_ij} )*(1 + beta * SumOf{W_kl*Y_kl[n-1]} - d)
        2) Theta_ij[n] = g * Theta_ij[n-1] - Vtheta * Y_ij[n-1]
        3) Y_ij[n] = 1 if U_ij[n] > Theta_ij[n] else 0
        """
        d = 1
        self.U = self.F * self.U + (self.convolve(self.Y, self.M) + S) * (1 + self.beta*self.convolve(self.Y, self.W) - d)
        self.Theta = self.g * self.Theta + self.v_theta * self.Y
        self.Y = np.where(self.U > self.Theta, 1, 0)

        return self.Y


