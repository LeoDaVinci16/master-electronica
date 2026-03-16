# Control del PWM pin2
# https://docs.micropython.org/en/latest/esp32/tutorial/pwm.html

from time import sleep
from machine import Pin, PWM

DUTY_MAX = 2**16 - 1   # 16bits -> 65535

d = 0
delta_d = 32

# Crea el objeto class machine.PWM(Pin(2) [, freq=30] [, duty=d] )
p = PWM(Pin(2), 30, duty_u16=d)
print(p)

while True:
    p.duty_u16(d)
#    print(d)

    sleep(1/1000)

    d += delta_d
    if d >= DUTY_MAX:
        print(d)
        d = DUTY_MAX
        delta_d = -delta_d
    elif d <= 0:
        print(d)
        d = 0
        delta_d = -delta_d