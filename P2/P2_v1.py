from machine import Pin, ADC, PWM
from time import sleep


###------------------- DEFINITION -----------------------------

ADC_PIN = 34

adc34 = ADC(Pin(ADC_PIN))

adc34.atten(ADC.ATTN_11DB)

adc34.width(ADC.WIDTH_12BIT)

freq = 50

SAMPLES = 11

led_red = Pin(5, Pin.OUT)
pwm_red = PWM(led_red, freq)


led_blue = Pin(4, Pin.OUT)
pwm_blue = PWM(led_blue, freq)

led_green = Pin(2, Pin.OUT)
pwm_green = PWM(led_green, freq)

#led_yellow = Pin(17, Pin.OUT)
#pwm_yellow = PWM(led_yellow, freq)

# Create txt:
file_name = f"mesures_P2_v1.csv"
f = open(file_name, "w")
f.write("duty_cycle,bits\n")


def mediana_lectures_bits(adc, n=11):
    valors = []
    for _ in range(n):
        valors.append(adc.read())   # lectura 0–4095[web:26][web:29]
        sleep(0.005)
    valors.sort()
    return valors[n // 2]


def perc_a_volts(duty_cycle):
    return duty_cycle * 1024 / 100  

def bits_a_volts(bits):
    return bits * 10 / 4095

### ------------------ DUTY CYCLE (main program) ----------------------------

duty_cycle = 0 # en percentatge

#while duty_cycle < 100:
for duty_cycle in range(0, 100, 1):
    d = perc_a_volts(duty_cycle)
    pwm_red.duty(int(d))
    voltage_bits = mediana_lectures_bits(adc34)
    voltage_volts = bits_a_volts(voltage_bits)
    
    
    
    # escriure línia CSV
    linea = "{},{:.3f}, {}, {}\n".format(
        duty_cycle, d, voltage_bits, voltage_volts
    )

    f.write(linea)
    
    print(linea)
    
    sleep(0.01)
    
    duty_cycle = duty_cycle+10
    
print("experiment end")
f.close()
duty_cycle = 0
d = duty_cycle*1024/100
pwm_red.duty(int(d))
pwm_blue.duty(int(d))
pwm_green.duty(int(d))

print("file saved as:", file_name)






