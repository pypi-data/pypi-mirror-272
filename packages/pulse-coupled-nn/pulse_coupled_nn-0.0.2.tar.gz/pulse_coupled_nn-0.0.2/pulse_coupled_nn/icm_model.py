import numpy as np
from .general_model import PCNNModel


class ICM(PCNNModel):
    """
    Intersecting Cortical Model
    - simplified PCNN classifier
    - beta set to 0 => classifier with only feeding wave
    - given by:
        1) F_ij[n] = f*F_ij[n-1]  + SumOf{M_kl * Y_kl} + S_ij
        2) Y_ij[n] = 1 if F_ij[n] > Theta_ij[n] else 0
        3) Theta_ij[n] = g*Theta_ij[n-1] + v_theta*Y_ij[n-1]


    """
    def __init__(self, shape, kernel_type, kernel_size):
        super(ICM, self).__init__(shape)
        '''
        '''
        # self.f = 0.5
        # self.g = 0.45
        self.v_theta = 150.

        self.Theta = np.ones(shape) * self.v_theta

        self.W = self.choose_kernel(kernel_type, kernel_size)

    def iterate(self, S):
        """
        1) F_ij[n] = f*F_ij[n-1]  + SumOf{M_kl * Y_kl} + S_ij
        2) Y_ij[n] = 1 if F_ij[n] > Theta_ij[n] else 0
        3) Theta_ij[n] = g*Theta_ij[n-1] + c*Y_ij[n-1]
        """

        self.F = self.f * self.F + self.convolve(self.Y, self.W) + S
        self.Theta = self.g * self.Theta + self.v_theta * self.Y
        self.Y = np.where(self.F > self.Theta, 1, 0)

        return self.Y
