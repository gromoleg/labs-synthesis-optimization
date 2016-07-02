accuracy = {'Gradient': (0.1, 0.15),
            'Newton': (0.1, 0.15)}
m = 10

function = '2 * (x[0] ** 2) + x[0] * x[1] + x[1] ** 2'
function_grad_0 = '4 * x[0] + x[1]'
function_grad_1 = 'x[0] + 2 * x[1]'
tuple_grad_0 = (4, 1)
tuple_grad_1 = (1, 2)
