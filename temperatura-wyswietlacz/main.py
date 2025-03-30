# python3 -m venv venv
# source venv/bin/activate
# pip install RPLCD
# python3 main.py
# deactivate

# VVS - GND / uziemienie
# VDD - 5V / zasilanie 5V
# VO - GND / kontrast
# RS - GPIO 26 / rejest wyboru danych
# RW - GND / odczyt/zapis
# E - GPIO 19 / enable - aktywacja
# D4 - GPIO 13 / dane (4-bit)
# D5 - GPIO 6 / dane (4-bit)
# D6 - GPIO 5 / dane (4-bit)
# D7 - GPIO 11 / dane (4-bit)
# A - 5V rezystor 220Ω / podświetlenie (+5V)
# K - GND / podświetlenie (-)

import os
import glob
import time
from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO

# Konfiguracja wyświetlacza LCD
lcd = CharLCD(
    pin_rs=26, pin_rw=None, pin_e=19,
    pins_data=[13, 6, 5, 11],
    numbering_mode=GPIO.BCM,
    cols=16, rows=2
)

def setup_1wire():
    # Ładuje moduły jądra do obsługi czujnika DS18B20.
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

def get_device_file():
    # Zwraca ścieżkę do pliku czujnika temperatury.
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]  # Znajduje czujnik DS18B20
    return device_folder + '/w1_slave'

def read_temp_raw(device_file):
    # Odczytuje surowe dane z pliku czujnika.
    with open(device_file, 'r') as f:
        return f.readlines()

def read_temp(device_file):
    # Przetwarza dane i zwraca temperaturę w °C.
    lines = read_temp_raw(device_file)
    
    while lines[0].strip()[-3:] != 'YES':  # Czeka na poprawny odczyt
        time.sleep(0.2)
        lines = read_temp_raw(device_file)
    
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

def main():
    # Odczytuje temperaturę i wyświetla na LCD.
    setup_1wire()
    device_file = get_device_file()
    
    while True:
        temperature = read_temp(device_file)
        print(f'Temperatura: {temperature:.2f}°C')  # Wydruk do terminala
        
        lcd.clear()  # Czyści ekran LCD
        lcd.write_string(f'Temp: {temperature:.2f} C')  # Wyświetla temperaturę
        
        time.sleep(1)  # Aktualizacja co 1 sek.

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        lcd.clear()
        lcd.write_string("Program zakonczony")
        GPIO.cleanup()
