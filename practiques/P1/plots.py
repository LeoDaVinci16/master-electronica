import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("lab_blue.csv")

print(df.head())

plt.plot(df['dac_value'], df['dac_voltage'], label='DAC Voltage')
plt.plot(df['dac_value'], df['adc34_voltage'], label='ADC34 Voltage')
plt.plot(df['dac_value'], df['adc35_voltage'], label='ADC35 Voltage')
plt.xlabel('DAC Value')
plt.ylabel('Voltage')
plt.title('DAC & ADC Measurements')
plt.legend()
plt.grid(True)
plt.show()