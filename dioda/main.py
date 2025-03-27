import RPi.GPIO as GPIO
import time

# Ustawienie numeracji GPIO
GPIO.setmode(GPIO.BCM)

# Wybór pinu do sterowania diodą
LED_PIN = 18
GPIO.setup(LED_PIN, GPIO.OUT)

try:
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH) 
        time.sleep(0.1)                  
        GPIO.output(LED_PIN, GPIO.LOW)  
        time.sleep(0.1)                 
except KeyboardInterrupt:
    print("\nZatrzymano miganie diody")
    GPIO.cleanup()  # Reset ustawień GPIO
