import numpy as np
from .general_model import PCNNModel

class SLM(PCNNModel):
    """
    Sigmoidal-Linking Model
    - membrane potential simplified PCNN classifier
    - given by:
        1) F_ij[n] = S_ij[n]
        2) L_ij[n] = 1 if SumOf{Y_kl} > 0 else 0
        3) U_ij[n] = F_ij[n] + beta * L_ij[n]
        4) Theta_ij[n] = Theta_ij[n-1] - gamma + v_theta*Y_ij[n-1]
        5) Y_ij[n] = 1 if U_ij[n] > Theta_ij[n] else 0

    """
    def __init__(self, shape, kernel_type, kernel_size):
        super(SLM, self).__init__(shape)
        '''
        '''
        self.v_theta = 150.

        self.Theta = np.ones(shape) * self.v_theta
        self.W = self.choose_kernel(kernel_type, kernel_size)

    def iterate(self, S):
        """
        1) F_ij[n] = S_ij[n]
        2) L_ij[n] = 1 if SumOf{Y_kl[n-1]} > 0 else 0
        3) U_ij[n] = F_ij[n] + beta * L_ij[n]
        4) Theta_ij[n] = Theta_ij[n-1] - gamma + v_theta*Y_ij[n-1]
        5) Y_ij[n] = 1 if U_ij[n] > Theta_ij[n] else 0
        """
        self.F = S
        to_sum_y = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
        self.L = np.where(self.convolve(self.Y, to_sum_y) > 0, 1, 0)
        self.U = self.F + self.beta*self.L
        self.Theta = self.Theta + self.gamma + self.v_theta*self.Y
        self.Y = np.where(self.U > self.Theta, 1, 0)

        return self.Y


