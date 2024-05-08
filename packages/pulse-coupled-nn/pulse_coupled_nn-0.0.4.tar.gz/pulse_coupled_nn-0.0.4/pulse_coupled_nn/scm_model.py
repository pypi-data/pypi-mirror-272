import numpy as np
from .general_model import PCNNModel


class SCM(PCNNModel):
    """
    Spiking Cortical Model
    - membrane potential simplified PCNN classifier
    - given by:
        1) U_ij[n] = f*U_ij[n-1]  + S_ij * SumOf{W_kl * Y_kl} + S_ij
        2) Y_ij[n] = 1 if U_ij[n] > Theta_ij[n] else 0
        3) Theta_ij[n] = g*Theta_ij[n-1] + v_theta*Y_ij[n-1]

    """
    def __init__(self, shape, kernel_type, kernel_size):
        super(SCM, self).__init__(shape)
        '''
        '''
        # alpha_theta = 0.2
        # alpha_f = 0.2
        # self.f = np.exp(-alpha_f)
        # self.g = np.exp(-alpha_theta)
        self.v_theta = 500.

        self.Theta = np.zeros(shape)
        # self.W = np.array([[0.5, 1, 0.5], [0.5, 1, 0.5], [0.5, 1, 0.5]])
        self.W = self.choose_kernel(kernel_type, kernel_size)

    def iterate(self, S):
        """
        1) U_ij[n] = f*U_ij[n-1]  + S_ij * SumOf{W_kl * Y_kl} + S_ij
        3) Theta_ij[n] = g*Theta_ij[n-1] + v_theta*Y_ij[n-1]
        2) Y_ij[n] = 1 if U_ij[n] > Theta_ij[n] else 0
        """
        self.U = self.f * self.U + S * self.convolve(self.Y, self.W) + S
        self.Theta = self.g*self.Theta + self.v_theta*self.Y
        self.Y = np.where(self.U > self.Theta, 1, 0)

        return self.Y


