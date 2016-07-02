# coding: utf-8
import constants
import labs.lab3.constants as lab_constants
from labs.helpers import classes


class ConfigurationsMethod(classes.Method):
    name = 'Configurations'

    def __init__(self):
        self.params = [{'var_name': 'x0',
                        'type': 'tuple',
                        'default': lab_constants.x0_configurations},

                       {'var_name': 'function',
                        'name': "f(x,y)",
                        'type': 'function',
                        'default': lab_constants.function},

                       {'var_name': 'delta1',
                        'default': lab_constants.delta_1_configurations},

                       {'var_name': 'delta2',
                        'default': lab_constants.delta_2_configurations},

                       {'var_name': 'lmbda',
                        'name': 'lambda',
                        'default': lab_constants.lambda_configurations},

                       {'var_name': 'alpha',
                        'default': lab_constants.alpha_configurations},

                       {'var_name': 'accuracy',
                        'default': lab_constants.accuracy[self.name]}]
        super(ConfigurationsMethod, self).__init__(ConfigurationsSolution)


class ConfigurationsSolution(classes.SolutionThread):
    def __init__(self, *args, **kwargs):
        super(ConfigurationsSolution, self).__init__(*args, **kwargs)

    def run(self):
        base = self.x0
        sln = lambda: {'x': str(base), 'f(x)': self.function(base)}
        d1, d2 = self.delta1, self.delta2
        yk = base
        f_x = self.function(yk)
        yk_pd1 = yk[0] + d1
        f_yk_pd1 = self.function([yk_pd1, yk[1]])
        bool_1 = f_yk_pd1 < f_x
        yk_md1 = yk[0] - d1
        f_yk_md1 = self.function([yk_md1, yk[1]])
        bool_2 = f_yk_md1 < f_x

        # line 2
        yk_2 = []
        if bool_1:
            yk_2.append(yk_pd1)
        elif bool_2:
            yk_2.append(yk_md1)
        else:
            yk_2.append(yk[0])
        yk_2.append(yk[1])
        f_yk_2 = self.function(yk_2)
        yk_pd2 = yk_2[1] + d2
        f_yk_pd2 = self.function([yk_2[0], yk_pd2])
        bool_2_1 = f_yk_pd2 < f_yk_2
        yk_md2 = yk_2[1] - d2
        f_yk_md2 = self.function([yk_2[0], yk_md2])
        bool_2_2 = f_yk_md2 < f_yk_2

        # line 3
        yk_3 = [yk_2[0]]
        if bool_2_1:
            yk_3.append(yk_pd2)
        elif bool_2_2:
            yk_3.append(yk_md2)
        else:
            yk_3.append(yk_2[1])
        f_yk_3 = self.function(yk_3)
        f_base = self.function(base)
        bool_3 = f_yk_3 < f_base
        end_1 = d1 <= self.accuracy and d2 <= self.accuracy
        if end_1:
            self.return_step_solution(sln())
            return self.return_final_solution(sln())
        while True:
            prev_base = base
            # line 1
            if bool_3:
                base = yk_3
            else:
                if d1 > self.accuracy:
                    d1 = d1 / self.alpha
                if d2 > self.accuracy:
                    d2 = d2 / self.alpha
            yk = [base[0] + self.lmbda * (base[0] - prev_base[0]), base[1] + self.lmbda * (base[1] - prev_base[1])]
            f_x = self.function(yk)
            yk_pd1 = yk[0] + d1
            f_yk_pd1 = self.function([yk_pd1, yk[1]])
            bool_1 = f_yk_pd1 < f_x
            yk_md1 = yk[0] - d1
            f_yk_md1 = self.function([yk_md1, yk[1]])
            bool_2 = f_yk_md1 < f_x

            # line 2
            yk_2 = []
            if bool_1:
                yk_2.append(yk_pd1)
            elif bool_2:
                yk_2.append(yk_md1)
            else:
                yk_2.append(yk[0])
            yk_2.append(yk[1])
            f_yk_2 = self.function(yk_2)
            yk_pd2 = yk_2[1] + d2
            f_yk_pd2 = self.function([yk_2[0], yk_pd2])
            bool_2_1 = f_yk_pd2 < f_yk_2
            yk_md2 = yk_2[1] - d2
            f_yk_md2 = self.function([yk_2[0], yk_md2])
            bool_2_2 = f_yk_md2 < f_yk_2

            # line 3
            yk_3 = [yk_2[0]]
            if bool_2_1:
                yk_3.append(yk_pd2)
            elif bool_2_2:
                yk_3.append(yk_md2)
            else:
                yk_3.append(yk_2[1])
            f_yk_3 = self.function(yk_3)
            f_base = self.function(base)
            bool_3 = f_yk_3 < f_base
            end_1 = d1 <= self.accuracy and d2 <= self.accuracy
            self.return_step_solution(sln())
            if end_1:
                break
            if self.exiting:
                self.return_error_solution()
        return self.return_final_solution(sln())
