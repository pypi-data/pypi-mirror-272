import pwmio

def pwm(pin, frequency=5000, duty_cycle=0):
    pwm = pwmio.PWMOut(pin, frequency=frequency, duty_cycle=duty_cycle)
    return pwm