# function = "-1.0 + 6 * x + 3 * (x ** 2) + x ** 6"
function = "2.0 * (x ** 2) + exp(-x)"

# derivative = "6.0 + 6 * x + 6 * (x ** 5)"
derivative = "4.0 * x - exp(-x)"

# second_derivative = "6.0 + 30 * (x**4)"
second_derivative = "4.0 + exp(-x)"

# x = -1
dx = 0.1
x = 0

p_types = ('float', 'function')
default_p_type = 'float'
p_aliases = {'func': 'function'}

about_information = """Developed by Oleg Gromyak.<br>
Feel free to contact me via <a href='mailto:oagromyak+labs@gmail.com'>oagromyak@gmail.com</a>
<br><a href='https://github.com/gromoleg/labs-synthesis-optimization'>Source</a>"""

queue_steps_max_size = 50