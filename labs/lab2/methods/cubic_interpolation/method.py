# coding: utf-8
import constants
import labs.lab2.constants as lab_constants
from labs.helpers import classes


class CubicInterpolationMethod(classes.Method):
    name = 'Cubic interpolation'

    def __init__(self):
        self.params = [{'var_name': 'x'},

                       {'var_name': 'function',
                        'name': "f(x)",
                        'type': 'function'},

                       {'var_name': 'derivative',
                        'name': "f'(x)",
                        'type': 'function'},

                       {'var_name': 'step',
                        'default': constants.dx},

                       {'var_name': 'accuracy',
                        'default': lab_constants.accuracy[self.name]}]
        super(CubicInterpolationMethod, self).__init__(CubicInterpolationSolution)


class CubicInterpolationSolution(classes.SolutionThread):
    def __init__(self, *args, **kwargs):
        super(CubicInterpolationSolution, self).__init__(*args, **kwargs)
        self.sln = lambda: {'x': self.sigma, "f'(x)": self.derivative(self.sigma)}

    def run(self):
        self.x0 = self.x
        if self.derivative(self.x0) < 0:
            self.k = 0
            self.xk_prev = self.x0
            self.xk = self.xk_prev + (2 ** self.k) * self.step
            while self.derivative(self.xk_prev) * self.derivative(self.xk) > 0:
                self.k += 1
                self.xk_prev = self.xk
                self.xk += (2 ** self.k) * self.step
        elif self.derivative(self.x0) > 0:
            self.k = 0
            self.xk_prev = self.x0
            self.xk = self.xk_prev - (2 ** self.k) * self.step
            while self.derivative(self.xk_prev) * self.derivative(self.xk) > 0:
                self.k += 1
                self.xk_prev = self.xk
                self.xk -= (2 ** self.k) * self.step
        self.x1, self.x2 = self.xk_prev, self.xk
        return self.run_from_step5()

    def run_from_step5(self):
        x1, x2 = self.x1, self.x2
        z = 3 * (self.function(x1) - self.function(x2)) / (x2 - x1) + self.derivative(x1) + self.derivative(x2)
        w = (z ** 2 - self.derivative(x1) * self.derivative(x2)) ** 0.5
        if x1 > x2:
            w = -w
        u = (self.derivative(x2) + w - z) / (self.derivative(x2) - self.derivative(x1) + 2 * w)
        if u < 0:
            sigma = x2
        elif 0 <= u <= 1:
            sigma = x2 - u * (x2 - x1)
        else:
            sigma = x1
        # step 6
        while self.function(sigma) > self.function(x1):
            sigma -= 0.5 * (sigma - x1)
        self.sigma = sigma
        # step 7
        if abs(self.derivative(sigma)) <= self.accuracy and abs((sigma - x1) / sigma) <= self.accuracy:
            self.return_step_solution(self.sln())
            self.return_final_solution(self.sln())
        elif self.derivative(sigma) * self.derivative(x1) < 0:
            self.x1 = sigma
            self.x2 = x1
            self.return_step_solution(self.sln())
            if self.exiting:
                return self.return_error_solution()
            return self.run_from_step5()
        elif self.derivative(sigma) * self.derivative(x2) < 0:
            self.x1 = sigma
            self.return_step_solution(self.sln())
            if self.exiting:
                return self.return_error_solution()
            return self.run_from_step5()
        return self.return_error_solution()