import constants
import logging
import labs.lab3.constants as lab_constants
from labs.helpers import classes


class DeformedPolyhedronMethod(classes.Method):
    name = 'Deformed polyhedron'

    def __init__(self):
        self.params = [{'var_name': 'x0',
                        'type': 'tuple',
                        'default': lab_constants.x0_deformed_polyhedron},

                       {'var_name': 'x1',
                        'type': 'tuple',
                        'default': lab_constants.x1_deformed_polyhedron},

                       {'var_name': 'x2',
                        'type': 'tuple',
                        'default': lab_constants.x2_deformed_polyhedron},

                       {'var_name': 'function',
                        'name': "f(x,y)",
                        'type': 'function',
                        'default': lab_constants.function},

                       {'var_name': 'alpha',
                        'default': lab_constants.alpha_deformed_polyhedron},

                       {'var_name': 'beta',
                        'default': lab_constants.beta_deformed_polyhedron},

                       {'var_name': 'gamma',
                        'default': lab_constants.gamma_deformed_polyhedron},

                       {'var_name': 'accuracy',
                        'default': lab_constants.accuracy[self.name]}]
        super(DeformedPolyhedronMethod, self).__init__(DeformedPolyhedronSolution)


class DeformedPolyhedronSolution(classes.SolutionThread):
    def __init__(self, *args, **kwargs):
        super(DeformedPolyhedronSolution, self).__init__(*args, **kwargs)

    def run(self):
        sln = lambda: {'x': str(x4), 'f(x)': self.function(x4)}
        x0, x1, x2 = self.x0, self.x1, self.x2
        f_x0, f_x1, f_x2 = self.function(x0), self.function(x1), self.function(x2)
        if f_x0 <= f_x1 and f_x0 <= f_x2:
            x4 = x0
        elif f_x1 <= f_x0 and f_x1 <= f_x2:
            x4 = x1
        else:
            x4 = x2
        f_x4 = self.function(x4)
        if max((f_x0, f_x1, f_x2)) == f_x2:
            if min((f_x0, f_x1)) == f_x1:
                x5 = x0
            else:
                x5 = x1
        elif max((f_x0, f_x1, f_x2)) == f_x1:
            if min((f_x0, f_x1, f_x2)) == f_x0:
                x5 = x2
            else:
                x5 = x0
        elif f_x1 <= f_x2:
            x5 = x2
        else:
            x5 = x1
        f_x5 = self.function(x5)
        if f_x0 >= f_x1 and f_x0 >= f_x2:
            x6 = x0
        elif f_x1 >= f_x0 and f_x1 >= f_x2:
            x6 = x1
        else:
            x6 = x2
        f_x6 = self.function(x6)
        x7 = [0.5 * (x5[0] + x4[0]), 0.5 * (x5[1] + x4[1])]
        f_x7 = self.function(x7)
        end_1 = lambda: (((f_x4 - f_x7) ** 2 + (f_x5 - f_x7) ** 2 + (f_x6 - f_x7) ** 2) / 3) ** 0.5 < self.accuracy
        self.return_step_solution(sln())
        if end_1():
            self.return_final_solution(sln())
        if self.exiting:
            self.return_error_solution()
        while True:
            x8 = [x7[0] + self.alpha * (x7[0] - x6[0]), x7[1] + self.alpha * (x7[1] - x6[1])]
            logging.warning(x4)
            logging.warning(x8)
            f_x8 = self.function(x8)
            x9 = [x7[0] + self.gamma * (x8[0] - x7[0]), x7[1] + self.gamma * (x8[1] - x7[1])]
            f_x9 = self.function(x9)
            x10 = [x7[0] + self.beta * (x6[0] - x7[0]), x7[1] + self.beta * (x6[1] - x7[1])]
            f_x10 = self.function(x10)
            if f_x8 > f_x6:
                x0 = [x4[0] + 0.5 * (x4[0] - x4[0]), x4[1] + 0.5 * (x4[1] - x4[1])]
            else:
                x0 = x4
            f_x0 = self.function(x0)
            if f_x8 > f_x6:
                x1 = [x4[0] + 0.5 * (x5[0] - x4[0]), x4[1] + 0.5 * (x5[1] - x4[1])]
            else:
                x1 = x5
            f_x1 = self.function(x1)
            if f_x8 > f_x6:
                x2 = [x4[0] + 0.5 * (x6[0] - x4[0]), x4[1] + 0.5 * (x6[1] - x4[1])]
            elif f_x8 <= f_x4:
                if f_x9 < f_x4:
                    x2 = x9
                else:
                    x2 = x8
            else:
                if f_x8 < f_x5:
                    x2 = x8
                else:
                    x2 = x10
            f_x2 = self.function(x2)
            if f_x0 <= f_x1 and f_x0 <= f_x2:
                x4 = x0
            elif f_x1 <= f_x0 and f_x1 <= f_x2:
                x4 = x1
            else:
                x4 = x2
            f_x4 = self.function(x4)
            if max((f_x0, f_x1, f_x2)) == f_x2:
                if min((f_x0, f_x1)) == f_x1:
                    x5 = x0
                else:
                    x5 = x1
            elif max((f_x0, f_x1, f_x2)) == f_x1:
                if min((f_x0, f_x1, f_x2)) == f_x0:
                    x5 = x2
                else:
                    x5 = x0
            elif f_x1 <= f_x2:
                x5 = x2
            else:
                x5 = x1
            f_x5 = self.function(x5)
            if f_x0 >= f_x1 and f_x0 >= f_x2:
                x6 = x0
            elif f_x1 >= f_x0 and f_x1 >= f_x2:
                x6 = x1
            else:
                x6 = x2
            f_x6 = self.function(x6)
            x7 = [0.5 * (x5[0] + x4[0]), 0.5 * (x5[1] + x4[1])]
            f_x7 = self.function(x7)

            self.return_step_solution(sln())
            if end_1():
                break
            if self.exiting:
                self.return_error_solution()
        self.return_final_solution(sln())
