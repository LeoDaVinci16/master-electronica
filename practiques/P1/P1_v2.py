from machine import Pin, DAC, ADC
from time import sleep

# -----------------------
# CONFIGURACIÓ
# -----------------------

DAC_PIN = 25
ADC1_PIN = 34
ADC2_PIN = 35

VREF = 3.3
ADC_MAX = 4095
DAC_MAX = 255

SAMPLES = 11
DELAY = 0.005

FILE_NAME = "lab_orange.csv"

# -----------------------
# INICIALITZACIÓ
# -----------------------

dac = DAC(Pin(DAC_PIN))

adc12 = ADC(Pin(ADC1_PIN))
adc13 = ADC(Pin(ADC2_PIN))

adc12.atten(ADC.ATTN_11DB)
adc13.atten(ADC.ATTN_11DB)

adc12.width(ADC.WIDTH_12BIT)
adc13.width(ADC.WIDTH_12BIT)

# -----------------------
# FUNCIONS
# -----------------------

def mediana_lectures_bits(adc, n=SAMPLES):

    valors = []

    for _ in range(n):
        valors.append(adc.read())
        sleep(DELAY)

    valors.sort()

    return valors[n // 2]


def bits_a_volts(bits):

    return bits * VREF / ADC_MAX


# -----------------------
# CREAR CSV
# -----------------------

f = open(FILE_NAME, "w")

# capçalera CSV
f.write("dac_value,dac_voltage,adc34_bits,adc34_voltage,adc35_bits,adc35_voltage\n")

print("Iniciant rampa...")

# -----------------------
# RAMPA DAC
# -----------------------

for valor in range(0, DAC_MAX + 1):

    dac.write(valor)

    sleep(0.001)  # temps perquè estabilitzi

    m12_bits = mediana_lectures_bits(adc12)
    m13_bits = mediana_lectures_bits(adc13)

    m12_v = bits_a_volts(m12_bits)
    m13_v = bits_a_volts(m13_bits)

    dac_v = valor * VREF / DAC_MAX

    # escriure línia CSV
    linea = "{},{:.3f},{},{:.3f},{},{:.3f}\n".format(
        valor, dac_v,
        m12_bits, m12_v,
        m13_bits, m13_v
    )

    f.write(linea)

    print(linea)

# -----------------------
# FINAL
# -----------------------

f.close()

valor = 0
dac.write(valor)
print("Rampa completada")
print("Fitxer guardat:", FILE_NAME) 