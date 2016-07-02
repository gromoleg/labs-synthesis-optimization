# coding: utf-8
import constants
import labs.lab4.constants as lab_constants
from labs.helpers import classes


class GradientMethod(classes.Method):
    name = 'Gradient'

    def __init__(self):
        self.params = [{'var_name': 'function',
                        'name': "f(x,y)",
                        'type': 'function',
                        'default': lab_constants.function},

                       {'var_name': 'm',
                        'default': lab_constants.m},

                       {'var_name': 'function_grad_0',
                        'type': 'function',
                        'default': lab_constants.function_grad_0},

                       {'var_name': 'function_grad_1',
                        'type': 'function',
                        'default': lab_constants.function_grad_1},

                       {'var_name': 'accuracy',
                        'type': 'tuple',
                        'default': lab_constants.accuracy[self.name]}]
        super(GradientMethod, self).__init__(GradientSolution)


class GradientSolution(classes.SolutionThread):
    def __init__(self, *args, **kwargs):
        super(GradientSolution, self).__init__(*args, **kwargs)

    def run(self):
        x = prev_x = [0.5, 1]
        sln = lambda: {'x': str(x), "f(x)": str(self.function(x))}
        k = 0
        f_x = prev_f_x = self.function(x)
        grad = [self.function_grad_0(x), self.function_grad_1(x)]
        tk = (grad[0] ** 2 + grad[1] ** 2) / (2 * self.function(grad))
        end_1 = lambda: (((x[0] - prev_x[0]) ** 2 + (x[1] - prev_x[1]) ** 2) ** 0.5 < self.accuracy[1]) and \
                        abs(f_x - prev_f_x) < self.accuracy[1]
        end_2 = lambda: (grad[0] ** 2 + grad[1] ** 2) ** 0.5 < self.accuracy[0]
        end_3 = lambda: k >= self.m
        self.return_step_solution(sln())
        if end_2() or end_3():
            return self.return_final_solution(sln())
        while True:
            x = [prev_x[0] - tk * grad[0], prev_x[1] - tk * grad[1]]
            k += 1
            f_x = self.function(x)
            grad = [self.function_grad_0(x), self.function_grad_1(x)]
            tk = (grad[0] ** 2 + grad[1] ** 2) / (2 * self.function(grad))
            self.return_step_solution(sln())
            if end_1() or end_2() or end_3():
                break
            if self.exiting:
                return self.return_error_solution()
            prev_x, prev_f_x = x, f_x
        self.return_step_solution(sln())
        return self.return_final_solution(sln())
