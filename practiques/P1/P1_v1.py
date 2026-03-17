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

SAMPLES = 11       # lectures per mediana
DELAY = 0.005      # temps entre lectures
LOOP_DELAY = 0.1

DAC_MIN = 0
DAC_MAX = 255

# -----------------------
# INICIALITZACIÓ
# -----------------------

dac = DAC(Pin(DAC_PIN))

adc12 = ADC(Pin(ADC1_PIN))
adc13 = ADC(Pin(ADC2_PIN))

# configuració recomanada ESP32
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
        lectura = adc.read()

        # protecció per lectures incorrectes
        if lectura < 0:
            lectura = 0
        if lectura > ADC_MAX:
            lectura = ADC_MAX

        valors.append(lectura)

        sleep(DELAY)

    valors.sort()

    return valors[n // 2]


def bits_a_volts(bits):

    return bits * VREF / ADC_MAX


def limitar(valor, vmin, vmax):

    if valor < vmin:
        return vmin
    if valor > vmax:
        return vmax

    return valor


# -----------------------
# VARIABLES
# -----------------------

valor = 0
pas = 10

print("Sistema iniciat")
print("DAC pin:", DAC_PIN)
print("ADC pins:", ADC1_PIN, ADC2_PIN)
print("---------------------------")

# -----------------------
# LOOP PRINCIPAL
# -----------------------

while True:

    # assegura rang correcte
    valor = limitar(valor, DAC_MIN, DAC_MAX)

    dac.write(valor)

    # lectures
    m12_bits = mediana_lectures_bits(adc12)
    m13_bits = mediana_lectures_bits(adc13)

    # conversió
    m12_v = bits_a_volts(m12_bits)
    m13_v = bits_a_volts(m13_bits)

    print(
        "DAC:", valor,
        "| ADC34:", m12_bits, "bits", "{:.3f}".format(m12_v), "V",
        "| ADC35:", m13_bits, "bits", "{:.3f}".format(m13_v), "V"
    )

    sleep(LOOP_DELAY)

    # rampa opcional
    valor += pas
    if valor >= DAC_MAX or valor <= DAC_MIN:
        pas = -pas 