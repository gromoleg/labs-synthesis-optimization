import constants
import logging
import labs.lab2.constants as lab_constants
from labs.helpers import classes


class QuadraticInterpolationMethod(classes.Method):
    name = 'Quadratic interpolation'

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
        super(QuadraticInterpolationMethod, self).__init__(QuadraticInterpolationSolution)


class QuadraticInterpolationSolution(classes.SolutionThread):
    def __init__(self, *args, **kwargs):
        super(QuadraticInterpolationSolution, self).__init__(*args, **kwargs)
        self.sln = lambda: {'x': self.sigma, "f'(x)": self.derivative(self.sigma)}

    def run(self):
        self.x1 = self.x
        return self.run_from_step2()

    def run_from_step2(self):
        self.steps2_3_4_5()
        return self.run_from_step6()

    def run_from_step6(self):
        self.step6()
        if self.get_denominator() == 0.0:
            self.x1 = self.xmin
            return self.run_from_step2()
        else:
            self.step7()
        return self.step8()

    def steps2_3_4_5(self):
        x1, step = self.x1, self.step
        self.x2 = x1 + step
        self.x3 = x1 + 2 * step if self.function(x1) > self.function(self.x2) else x1 - step

    def step6(self):
        self.xmin, self.fmin = self.min_x_func()

    def step7(self):
        self.sigma = self.get_sigma()

    def step8(self):
        if abs((self.fmin - self.function(self.sigma)) / self.function(self.sigma)) < self.accuracy and \
                        abs((self.xmin - self.sigma) / self.sigma) < self.accuracy:
            self.return_step_solution(self.sln())
            if self.exiting:
                return self.return_error_solution()
            self.return_final_solution(self.sln())
        else:
            self.return_step_solution(self.sln())
            if self.exiting:
                return self.return_error_solution()
            x1, x3 = tuple(sorted((self.x1, self.x3)))
            if x1 <= self.sigma <= x3:
                if self.derivative(x1) < self.derivative(x3):
                    self.x1 = x1
                    self.x2 = x1 + self.step
                    self.x3 = x1 - self.step
                else:
                    self.x1 = x3
                    self.x2 = x3 + self.step
                    self.x3 = x3 - self.step
                self.run_from_step6()
            else:
                self.x1 = self.sigma
                self.run_from_step2()

    def get_sigma(self):
        a, b, g = self.x1, self.x2, self.x3
        f_a, f_b, f_g = self.function(a), self.function(b), self.function(g)
        return 0.5 * ((b ** 2 - g ** 2) * f_a + (g ** 2 - a ** 2) * f_b + (a ** 2 - b ** 2) * f_g) / (
            (b - g) * f_a + (g - a) * f_b + (a - b) * f_g)

    def get_denominator(self):
        a, b, g = self.x1, self.x2, self.x3
        f_a, f_b, f_g = self.function(a), self.function(b), self.function(g)
        return (b - g) * f_a + (g - a) * f_b + (a - b) * f_g

    def min_x_func(self):
        params = (self.x1, self.x2, self.x3)
        func_values = tuple(self.function(param) for param in params)
        min_func_value = min(func_values)
        min_x = params[func_values.index(min_func_value)]
        return min_x, min_func_value
