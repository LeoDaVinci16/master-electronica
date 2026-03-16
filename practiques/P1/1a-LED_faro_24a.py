# LED parpadeando
# 2024 febrero Francisco Casellas

from machine import Pin
from time import sleep_ms

pin_02 = Pin(2, Pin.OUT)   # GPIO2
n=0

while True:
   pin_02.on()
   print(n)
   n=n+1
   sleep_ms(500)
   pin_02.off()
   sleep_ms(200)