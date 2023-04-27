import math

import gremlin
from gremlin.user_plugin import *


pa_x = PhysicalInputVariable(
        "Physical Rudder Axis",
        "Physical Rudder axis input",
        [gremlin.common.InputType.JoystickAxis]
)

va_lb = VirtualInputVariable(
        "vJoy Left Break Axis",
        "Virtual Left Break axis output",
        [gremlin.common.InputType.JoystickAxis]
)
va_rb = VirtualInputVariable(
        "vJoy Right Break Axis",
        "Virtual Right Break axis output",
        [gremlin.common.InputType.JoystickAxis]
)
mode = ModeVariable("Mode", "Mode in which to use these settings")
# need switck
# inner_dz = FloatVariable(
#         "Inner Deadzone",
#         "Size of the inner deadzone",
#         0.0,
#         0.0,
#         1.0
# )

# Decorators for the two physical axes
dec_x = pa_x.create_decorator(mode.value)

# Storage for the last known axis values
x_value = 0.0

def update_vjoy(vjoy):
        # Full brake applied to both axis when no rudder is applied.
        # 

        vjoy[va_lb.vjoy_id].axis(va_lb.input_id).value = x_value
        vjoy[va_rb.vjoy_id].axis(va_rb.input_id).value = x_value


@dec_x.axis(pa_x.input_id)
def axis1(event, vjoy):
    global x_value
    x_value = event.value
    update_vjoy(vjoy)
