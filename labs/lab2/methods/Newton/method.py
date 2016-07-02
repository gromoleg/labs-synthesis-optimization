import constants
import labs.lab2.constants as lab_constants
from labs.helpers import classes
import logging


class NewtonMethod(classes.Method):
    name = 'Newton'

    def __init__(self):
        self.params = [{'var_name': 'x'},

                       {'var_name': 'derivative',
                        'name': "f'(x)",
                        'type': 'func'},

                       {'var_name': 'second_derivative',
                        'name': 'f"(x)',
                        'type': 'func'},

                       {'var_name': 'accuracy',
                        'default': lab_constants.accuracy[self.name]}]
        super(NewtonMethod, self).__init__(NewtonSolution)


class NewtonSolution(classes.SolutionThread):
    def __init__(self, *args, **kwargs):
        super(NewtonSolution, self).__init__(*args, **kwargs)

    def run(self):
        x, derivative, second_derivative, accuracy = self.x, self.derivative, self.second_derivative, self.accuracy
        sln = lambda: {'x': x, "f'(x)": derivative(x)}
        while not (abs(derivative(x)) < accuracy):
            temp_x=x
            x -= derivative(x) / second_derivative(x)
            self.return_step_solution(sln())
            if self.exiting:
                return self.return_error_solution()
        logging.info('%s: result=%s' % (self.name, x))
        print(temp_x)
        self.return_final_solution(sln())
