import math

import gremlin
from gremlin.user_plugin import *

pa_r = PhysicalInputVariable(
        "Physical Rudder Axis",
        "Physical Rudder axis input",
        [gremlin.common.InputType.JoystickAxis]
)
flip_rudder = BoolVariable(
        "Flip Physical Rudder Axis",
        "Default right down is positive",
        False
)
pa_b = PhysicalInputVariable(
        "Physical Brake Axis",
        "Physical Brake axis input",
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

# Decorators for the two physical axes
dec_r = pa_r.create_decorator(mode.value)
dec_b = pa_b.create_decorator(mode.value)

flip_rudder_mod = -1 if flip_rudder.value else 1

# Storage for the last known axis values
r_value = 0.0
b_value = 0.0

def update_vjoy(vjoy):
        # Full brake applied to both axis when no rudder is applied.
        lb_value = 1.0 - 2.0 * (b_value * (1.0 - r_value * flip_rudder_mod))
        rb_value = 1.0 - 2.0 * (b_value * (1.0 + r_value * flip_rudder_mod))

        vjoy[va_rb.vjoy_id].axis(va_rb.input_id).value = lb_value
        vjoy[va_lb.vjoy_id].axis(va_lb.input_id).value = rb_value

@dec_r.axis(pa_r.input_id)
def axis1(event, vjoy):
    global r_value
    r_value = event.value
    update_vjoy(vjoy)

@dec_b.axis(pa_b.input_id)
def axis2(event, vjoy):
    global b_value
    b_value = event.value
    update_vjoy(vjoy)