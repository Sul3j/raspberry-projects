import os  # Moduł do wykonywania poleceń systemowych
import glob  # Moduł do wyszukiwania plików w systemie
import time  # Moduł do obsługi opóźnień w pętli

def setup_1wire():
    # Funkcja ładująca moduły jądra wymagane do obsługi czujnika DS18B20.
    os.system('modprobe w1-gpio')  # Włącza obsługę magistrali 1-Wire
    os.system('modprobe w1-therm')  # Włącza obsługę czujników temperatury 1-Wire

def get_device_file():
    # Funkcja zwraca ścieżkę do pliku z danymi czujnika temperatury.
    base_dir = '/sys/bus/w1/devices/'  # Ścieżka do katalogu urządzeń 1-Wire
    device_folder = glob.glob(base_dir + '28*')[0]  # Wyszukuje folder czujnika (identyfikator zaczyna się od "28")
    return device_folder + '/w1_slave'  # Zwraca pełną ścieżkę do pliku z danymi czujnika

def read_temp_raw(device_file):
    # Funkcja odczytuje surowe dane z pliku czujnika temperatury.
    with open(device_file, 'r') as f:  # Otwiera plik w trybie odczytu
        return f.readlines()  # Zwraca zawartość pliku jako listę wierszy

def read_temp(device_file):
    # Funkcja przetwarza dane z pliku i zwraca temperaturę w stopniach Celsjusza.
    lines = read_temp_raw(device_file)  # Odczytuje dane z pliku
    
    while lines[0].strip()[-3:] != 'YES':  # Sprawdza, czy dane są poprawne (czy czujnik poprawnie odczytał temperaturę)
        time.sleep(0.2)  # Czeka 0.2 sekundy i ponawia odczyt
        lines = read_temp_raw(device_file)
    
    equals_pos = lines[1].find('t=')  # Szuka wiersza zawierającego temperaturę
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]  # Pobiera wartość temperatury jako tekst
        temp_c = float(temp_string) / 1000.0  # Konwertuje wartość na stopnie Celsjusza
        return temp_c  # Zwraca temperaturę jako liczbę zmiennoprzecinkową

def main():
    """
    Funkcja główna programu: inicjalizuje czujnik i odczytuje temperaturę w pętli.
    """
    setup_1wire()  # Inicjalizacja magistrali 1-Wire
    device_file = get_device_file()  # Pobranie ścieżki do pliku czujnika
    
    while True:  # Pętla nieskończona do ciągłego odczytu temperatury
        temperature = read_temp(device_file)  # Odczyt temperatury
        print(f'Temperatura: {temperature:.2f}°C')  # Wyświetlenie temperatury w konsoli
        time.sleep(1)  # Odczekanie 1 sekundy przed kolejnym pomiarem

if __name__ == "__main__":
    main()  # Uruchomienie funkcji głównej, jeśli skrypt został uruchomiony bezpośrednio
