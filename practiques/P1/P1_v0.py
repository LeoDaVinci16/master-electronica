from machine import Pin, DAC, ADC
from time import sleep

file_name = "mesures_groc.csv"

# CREAR CSV
f = open(file_name, "w")

# capçalera CSV
f.write("dac_value,dac_voltage,adc34_bits,adc34_voltage,adc35_bits,adc35_voltage\n")

# DAC al pin 25
dac = DAC(Pin(25))

# ADC als pins 34 i 35
adc34 = ADC(Pin(34))
adc35 = ADC(Pin(35))

#adc34.atten(ADC.ATTN_11DB)      # rang aproximat 0–3,3 V[web:14][web:26]
#adc35.atten(ADC.ATTN_11DB)
#adc34.width(ADC.WIDTH_34BIT)    # 0–4095[web:26][web:29]
#adc35.width(ADC.WIDTH_34BIT)

VREF = 3.3
ADC_MAX = 4095

def mediana_lectures_bits(adc, n=11):
    valors = []
    for _ in range(n):
        valors.append(adc.read())   # lectura 0–4095[web:26][web:29]
        sleep(0.005)
    valors.sort()
    return valors[n // 2]

def bits_a_volts(bits):
    return bits * VREF / ADC_MAX   # conversió lineal 0–4095 → 0–3,3 V[web:14][web:29]

valor = 0
pas = 5

# while True:
while valor < 255:
    # Escriu al DAC (0–255 → 0–3,3 V aprox.)
    dac.write(valor)

    # Mediana de 11 lectures en bits
    m34_bits = mediana_lectures_bits(adc34)
    m35_bits = mediana_lectures_bits(adc35)

    # Conversió a volts
    m34_v = bits_a_volts(m34_bits)
    m35_v = bits_a_volts(m35_bits)

    print("DAC25:", valor,
          " ADC34:", m34_bits, "bits", ",", "{:.3f}".format(m34_v), "V",
          " ADC35:", m35_bits, "bits", ",", "{:.3f}".format(m35_v), "V")
    
    # escriure línia CSV
    linea = "{},{:.3f},{},{:.3f},{},{:.3f}\n".format(
        valor, bits_a_volts(valor),
        m34_bits, m34_v,
        m35_bits, m35_v
    )

    f.write(linea)

    sleep(0.001)

    valor += pas
    if valor >= 255 or valor <= 0:
         pas = -pas

valor = 0
dac.write(valor)
print("Ending iteration with: DAC25:", valor,
          " ADC34:", m34_bits, "bits", ",", "{:.3f}".format(m34_v), "V",
          " ADC35:", m35_bits, "bits", ",", "{:.3f}".format(m35_v), "V")
print("Fitxer guardat:", file_name) 