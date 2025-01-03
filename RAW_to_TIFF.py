import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt


def read_raw_parameters(file_path):
    """
    Wczytuje parametry obrazu RAW z pierwszych 5 wartości w pliku.

    :param file_path: Ścieżka do pliku RAW.
    :return: Tuple zawierający (szerokość, wysokość, data_type, header_size).
    """
    with open(file_path, 'rb') as file:
        # Zakładamy, że parametry są zapisane w formacie uint16.
        parameters = np.fromfile(file, dtype=np.uint16, count=5)

    width = parameters[0]
    height = parameters[1]
    data_type = np.uint16 if parameters[2] == 16 else np.uint8
    header_size = parameters[4]

    return width, height, data_type, header_size


def process_raw_file(file_path, width=-1, height=-1, pixel_type=-1, header_size=-1, save_tiff=True, tiff_path=None):
    """
    Przetwarza plik RAW na obraz, wczytując parametry z pliku, jeśli są ustawione na -1,
    i opcjonalnie zapisuje jako TIFF.

    :param file_path: Ścieżka do pliku RAW.
    :param width: Szerokość obrazu lub -1.
    :param height: Wysokość obrazu lub -1.
    :param pixel_type: Typ danych piksela (16 lub 8) lub -1.
    :param header_size: Rozmiar nagłówka w bajtach lub -1.
    :param save_tiff: Czy zapisać wynik jako plik TIFF.
    :param tiff_path: Ścieżka do zapisu pliku TIFF.
    """
    # Jeśli którykolwiek z parametrów jest ustawiony na -1, wczytaj parametry z pliku
    if width == -1 or height == -1 or pixel_type == -1 or header_size == -1:
        width, height, data_type, header_size = read_raw_parameters(file_path)
    else:
        data_type = np.uint16 if pixel_type == 16 else np.uint8

    image_dims = (height, width)

    with open(file_path, 'rb') as file:
        file.seek(header_size)
        raw_data = np.fromfile(file, dtype=data_type)

    try:
        image_data = raw_data.reshape(image_dims)
    except ValueError as e:
        print(f"Błąd: {e}. Sprawdź podane wymiary i rozmiar nagłówka.")
        return

    if save_tiff:
        # Upewnij się, że ścieżka do zapisu TIFF jest poprawna i zawiera rozszerzenie
        if tiff_path is None:
            tiff_path = os.path.splitext(file_path)[0] + '.tiff'
        elif os.path.isdir(tiff_path):  # Jeśli tiff_path jest folderem, dodaj nazwę pliku
            tiff_path = os.path.join(tiff_path, os.path.basename(os.path.splitext(file_path)[0] + '.tiff'))

        # Teraz tiff_path powinna być prawidłową ścieżką do pliku, zawierać nazwę pliku i rozszerzenie .tiff
        Image.fromarray(image_data).save(tiff_path)
        print(f"Zapisano plik TIFF: {tiff_path}")
    else:
        # Wyświetl obraz
        Image.fromarray(image_data).show()


def display_image(image_data):
    # Skalowanie danych do 8-bitowego zakresu
    min_val, max_val = np.min(image_data), np.max(image_data)
    scaled_data = (image_data - min_val) / (max_val - min_val)  # Normalizacja do zakresu [0, 1]
    display_data = (scaled_data * 255).astype(np.uint8)  # Przeskalowanie do zakresu [0, 255]
    plt.imshow(display_data, cmap='gray')
    plt.title('Obraz RAW przeskalowany')
    plt.show()


def process_path(path, save_tiff=True, display_images=False, width=-1, height=-1, pixel_type=-1, header_size=-1,
                 tiff_path=None):
    """
    Przetwarza plik lub wszystkie pliki RAW w folderze na obrazy TIFF i opcjonalnie wyświetla je.
    """
    if os.path.isdir(path):
        # Przetwarzanie wszystkich plików RAW w folderze
        for filename in os.listdir(path):
            if filename.lower().endswith('.raw'):
                file_path = os.path.join(path, filename)
                output_tiff_path = tiff_path if tiff_path else os.path.join(path,
                                                                            os.path.splitext(filename)[0] + '.tiff')
                process_raw_file(file_path, width, height, pixel_type, header_size, save_tiff=save_tiff,
                                 tiff_path=output_tiff_path)
                if display_images:
                    width, height, data_type, header_size = read_raw_parameters(file_path)
                    image_dims = (height, width)
                    with open(file_path, 'rb') as file:
                        file.seek(header_size)
                        raw_data = np.fromfile(file, dtype=data_type).reshape(image_dims)
                    display_image(raw_data)

    elif os.path.isfile(path):
        # Przetwarzanie pojedynczego pliku RAW
        output_tiff_path = tiff_path if tiff_path else os.path.splitext(path)[0] + '.tiff'
        process_raw_file(path, width, height, pixel_type, header_size, save_tiff=save_tiff, tiff_path=output_tiff_path)
        if display_images:
            width, height, data_type, header_size = read_raw_parameters(path)
            image_dims = (height, width)
            with open(path, 'rb') as file:
                file.seek(header_size)
                raw_data = np.fromfile(file, dtype=data_type).reshape(image_dims)
            display_image(raw_data)
    else:
        print(f"Podana ścieżka {path} nie jest ani folderem, ani plikiem.")


"""
Path to może  być ścieżka do folderu lub do
konkretnego pliku RAW np. C:\Pliki\Praca Inżynierska\Projections\python_test_05_0007.raw
albo C:\Pliki\Praca Inżynierska\Projections
jeśli to ścieżka do folderu, to przetworzy wszystkie zdjęcia.
Target_path - miejsce zapisu TIFFów, jeśli "None" to zapisze w folderze z RAWami. 
"""

path = r'C:\Pliki\Praca Inżynierska\Projections'
target_path = None
process_path(path,
             save_tiff=True,
             display_images=False,
             tiff_path=target_path)
"""
save_tiff = True - zapisuje pliki RAW jako TIFF,
display_images=True - pokazuje każde pojedyczne zdjęcie na ekranie.
Jeśli wartości źle się wczytają, można tak:
"""
# process_path(path, save_tiff=True,
#              display_images=False,
#              width=2976,
#              height=2480,
#              pixel_type=16,
#              header_size=2048)
