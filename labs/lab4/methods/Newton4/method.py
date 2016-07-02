# coding: utf-8
import constants
import labs.lab4.constants as lab_constants
from labs.helpers import classes
import copy


class NewtonMethod4(classes.Method):
    name = 'Newton'

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

                       {'var_name': 'tuple_grad_0',
                        'type': 'tuple',
                        'default': lab_constants.tuple_grad_0},

                       {'var_name': 'tuple_grad_1',
                        'type': 'tuple',
                        'default': lab_constants.tuple_grad_1},

                       {'var_name': 'accuracy',
                        'type': 'tuple',
                        'default': lab_constants.accuracy[self.name]}]
        super(NewtonMethod4, self).__init__(NewtonSolution)


class NewtonSolution(classes.SolutionThread):
    def __init__(self, *args, **kwargs):
        super(NewtonSolution, self).__init__(*args, **kwargs)

    def run(self):
        x = prev_x = [0.5, 1]
        sln = lambda: {'x': str(x), "f(x)": str(self.function(x))}
        k = 0
        f_x = prev_f_x = self.function(x)
        grad = [self.function_grad_0(x), self.function_grad_1(x)]
        end_1 = lambda: (((x[0] - prev_x[0]) ** 2 + (x[1] - prev_x[1]) ** 2) ** 0.5 < self.accuracy[1]) and \
                        abs(f_x - prev_f_x) < self.accuracy[1]
        end_2 = lambda: (grad[0] ** 2 + grad[1] ** 2) ** 0.5 < self.accuracy[0]
        end_3 = lambda: k >= self.m
        grad_inverse = minverse([list(self.tuple_grad_0), list(self.tuple_grad_1)])
        l = grad_inverse[0][0] > 0
        m = (grad_inverse[0][0] * grad_inverse[1][1] - grad_inverse[1][0] * grad_inverse[0][1]) > 0
        if l and m:
            dk = mmultiply(grad_inverse, [grad])
        else:
            dk = grad
        dk = [-_ for _ in dk]
        if l and m:
            tk = 1
        else:
            tk = (grad[0] ** 2 + grad[1] ** 2) / (2 * self.function(grad))
        self.return_step_solution(sln())
        while True:
            k += 1
            x = [x[0] + tk * dk[0], x[1] + tk * dk[1]]
            f_x = self.function(x)
            grad = [self.function_grad_0(x), self.function_grad_1(x)]
            grad_inverse = minverse([list(self.tuple_grad_0), list(self.tuple_grad_1)])
            l = grad_inverse[0][0] > 0
            m = (grad_inverse[0][0] * grad_inverse[1][1] - grad_inverse[1][0] * grad_inverse[0][1]) > 0
            if l and m:
                dk = mmultiply(grad_inverse, [grad])
            else:
                dk = grad
            dk = [-_ for _ in dk]
            if l and m:
                tk = 1
            else:
                tk = (grad[0] ** 2 + grad[1] ** 2) / (2 * self.function(grad))
            self.return_step_solution(sln())
            if end_1() or end_2() or end_3():
                break
            if self.exiting:
                return self.return_error_solution()
            prev_x, prev_f_x = x, f_x
        return self.return_final_solution(sln())


def minverse(matrix):
    # 2x2 only
    matrix = copy.copy(matrix)
    matrix[0][0], matrix[1][1] = matrix[1][1], matrix[0][0]
    det = matrix[0][0] * matrix[1][1] - matrix[1][0] * matrix[0][1]
    for x in range(len(matrix)):
        for y in range(len(matrix[0])):
            matrix[x][y] /= det
    matrix[1][0], matrix[0][1] = -matrix[1][0], -matrix[0][1]
    return matrix


def mmultiply(m1, m2):
    # m1 is 2x2     1   2   x   1
    # m2 is 1x2     2   3       2
    m3 = [m1[0][0] * m2[0][0] + m1[0][1] * m2[0][1], m1[1][0] * m2[0][0] + m1[1][1] * m2[0][1]]
    return m3
