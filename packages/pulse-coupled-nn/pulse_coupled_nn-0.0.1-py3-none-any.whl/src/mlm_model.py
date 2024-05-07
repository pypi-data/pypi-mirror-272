import numpy as np
from .general_model import PCNNModel


class MLM(PCNNModel):
    """
    Multi Linking Model
    - given by:
        1) F_ij[n] = f * F_ij[n-1] + Vf * SumOf{M_kl * Y_kl[n-1]} + S_ij
        2) L_ij[n] = h * L_ij[n-1] + Vl * SumOf{W_kl * Y_kl[n-1]}
        3) U_ij[n] = F_ij[n] *(1 + beta * L_ij[n])
        4) Theta_ij[n] = g * Theta_ij[n-1] - Vtheta * Y_ij[n-1]
        5) Y_ij[n] = 1 if U_ij[n] > Theta_ij[n] else 0

    """
    def __init__(self, shape, kernel_type, kernel_size):
        super(MLM, self).__init__(shape)
        self.internal_iterations = 5
        self.v_theta = 50
        self.Theta = np.ones(shape) * self.v_theta

        self.M = self.choose_kernel(kernel_type, kernel_size)
        self.W = self.choose_kernel(kernel_type, kernel_size)

        # same, but internal
        self.F_I = np.zeros(shape)
        self.L_I = np.zeros(shape)
        self.U_I = np.zeros(shape)
        self.Y_I = np.zeros(shape)
        self.Theta_I = np.ones(shape)


    def iterate(self, S):
        """
        1) F_ij[n] = f * F_ij[n-1] + Vf * SumOf{M_kl * Y_kl[n-1]} + S_ij
        2) L_ij[n] = h * L_ij[n-1] + Vl * SumOf{W_kl * Y_kl[n-1]}
        3) U_ij[n] = F_ij[n] *(1 + beta * L_ij[n])
        4) Theta_ij[n] = g * Theta_ij[n] - Vtheta * Y_ij[n-1]
        5) Y_ij[n] = 1 if U_ij[n] > Theta_ij[n] else 0
        """
        linking_iterations = []
        for _ in range(self.internal_iterations):
            self.F_I = self.f * self.F_I + self.v_f * self.convolve(self.Y_I, self.M) + S
            self.L_I = self.h * self.L + self.v_l * self.convolve(self.Y_I, self.W)
            self.U_I = self.F_I * (1 + self.beta * self.L_I)
            self.Theta_I = self.g * self.Theta_I + self.v_theta * self.Y_I
            self.Y_I = np.where(self.U_I > self.Theta_I, 1, 0)
            linking_iterations.append(self.L_I)

        geometric_mean = np.ones_like(self.L_I)
        for i in range(len(linking_iterations)):
            geometric_mean *= (1 + self.beta*linking_iterations[i])

        self.F = self.f * self.F + self.v_f * self.convolve(self.Y, self.M) + S
        self.U = self.F * geometric_mean
        self.Theta = self.g * self.Theta + self.v_theta * self.Y
        self.Y = np.where(self.U > self.Theta, 1, 0)

        return self.Y


