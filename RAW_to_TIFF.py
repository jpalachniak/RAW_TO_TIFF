import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt


def read_raw_parameters(file_path):
    """
    Reads RAW image parameters from the first 5 values in the file.

    :param file_path: Path to the RAW file.
    :return: Tuple containing (width, height, data_type, header_size).
    """
    with open(file_path, 'rb') as file:
        # Assumes that parameters are stored in uint16 format.
        parameters = np.fromfile(file, dtype=np.uint16, count=5)

    width = parameters[0]
    height = parameters[1]
    data_type = np.uint16 if parameters[2] == 16 else np.uint8
    header_size = parameters[4]

    return width, height, data_type, header_size


def process_raw_file(file_path, width=-1, height=-1, pixel_type=-1, header_size=-1, save_tiff=True, tiff_path=None):
    """
    Processes a RAW file into an image, reading parameters from the file if set to -1,
    and optionally saves it as a TIFF.

    :param file_path: Path to the RAW file.
    :param width: Image width or -1.
    :param height: Image height or -1.
    :param pixel_type: Pixel data type (16 or 8) or -1.
    :param header_size: Header size in bytes or -1.
    :param save_tiff: Whether to save the result as a TIFF file.
    :param tiff_path: Path to save the TIFF file.
    """
    # If any parameter is set to -1, read parameters from the file
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
        print(f"Error: {e}. Check the provided dimensions and header size.")
        return

    if save_tiff:
        # Ensure that the TIFF save path is valid and includes an extension
        if tiff_path is None:
            tiff_path = os.path.splitext(file_path)[0] + '.tiff'
        elif os.path.isdir(tiff_path):  # If tiff_path is a folder, add the file name
            tiff_path = os.path.join(tiff_path, os.path.basename(os.path.splitext(file_path)[0] + '.tiff'))

        # Now tiff_path should be a valid file path containing the file name and .tiff extension
        Image.fromarray(image_data).save(tiff_path)
        print(f"TIFF file saved: {tiff_path}")
    else:
        # Display the image
        Image.fromarray(image_data).show()


def display_image(image_data):
    # Scale data to 8-bit range
    min_val, max_val = np.min(image_data), np.max(image_data)
    scaled_data = (image_data - min_val) / (max_val - min_val)  # Normalize to range [0, 1]
    display_data = (scaled_data * 255).astype(np.uint8)  # Scale to range [0, 255]
    plt.imshow(display_data, cmap='gray')
    plt.title('Scaled RAW Image')
    plt.show()


def process_path(path, save_tiff=True, display_images=False, width=-1, height=-1, pixel_type=-1, header_size=-1,
                 tiff_path=None):
    """
    Processes a file or all RAW files in a folder into TIFF images and optionally displays them.
    """
    if os.path.isdir(path):
        # Process all RAW files in the folder
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
        # Process a single RAW file
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
        print(f"The provided path {path} is neither a folder nor a file.")


"""
Path can be a path to a folder or
a specific RAW file, e.g., C:\Files\Engineering\Projections\python_test_05_0007.raw
or C:\Files\Engineering\Projections.
If it is a folder path, all images will be processed.
Target_path - location to save TIFFs. If "None", they will be saved in the RAW folder. 
"""

path = r'C:\Files\Engineering\Projections'
target_path = None
process_path(path,
             save_tiff=True,
             display_images=False,
             tiff_path=target_path)
"""
save_tiff = True - saves RAW files as TIFF,
display_images = True - displays each single image on the screen.
If values are not read correctly, use:
"""
# process_path(path, save_tiff=True,
#              display_images=False,
#              width=2976,
#              height=2480,
#              pixel_type=16,
#              header_size=2048)
