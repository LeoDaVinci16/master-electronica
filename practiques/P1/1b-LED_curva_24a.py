# Obtencion de la curva del LED
# 2024 febrero Francisco Casellas

from time import sleep
import machine

# Configuro el ADC
pin34 = machine.Pin(34)                 # Defino el PIN34
adc34 = machine.ADC(pin34)              # ADC en el PIN34
adc34.atten(machine.ADC.ATTN_11DB)      # {0, 2_5, 6, 11} dB de atenuación con Vref = 1,1 V.
                                        # Rango de lectura entre 0.0V y {1.0, 1.34, 2.0. 3,6} V
adc34.width(machine.ADC.WIDTH_12BIT)    # Resolucion de {9, 10, 11, 12} bits

# Configuro el DAC
dac25 = machine.DAC(machine.Pin(25))            # DAC 1 pin GPIO_25
dac25.write(128)                				# Valor del DAC (128 -> 1.65V, sale 1,622V) (255 -> 3.3V y sale 3,164V)
sleep(1)
num= 255

for i in range(0, 255, 50):
    dac25.write(i)
    print(i, adc34.read())
    sleep(1)