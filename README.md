# RAW Image Processor

This repository contains a Python script for processing RAW image files into TIFF images. It provides functionality to read RAW file parameters, process individual RAW files or directories containing multiple RAW files, and save the results as TIFF images.

## Features

- Reads image parameters (width, height, data type, header size) from RAW file headers
- Processes both single RAW files and entire directories
- Converts RAW files to TIFF format
- Optional image display functionality
- Supports both 8-bit and 16-bit pixel formats
- Flexible output path configuration

## Requirements

- Python 3.6+
- NumPy
- Pillow (PIL)
- Matplotlib

## Installation

1. Clone this repository:
```bash
git clone https://github.com/jpalachniak/RAW_TO_TIFF.git
```

2. Install required dependencies:
```bash
pip install numpy pillow matplotlib
```

## Usage

### Basic Usage
To process a single RAW file or all RAW files in a directory, set the path variable to the file or directory path and run the script.

Example:
```python
path = r'C:\Path\To\RAW_Files'
target_path = None
process_path(path, save_tiff=True, display_images=False, tiff_path=target_path)

```

### Advanced Usage

You can customize the processing with various parameters:

```python
process_path(
    path='path/to/your/files',
    save_tiff=True,              # Save output as TIFF
    display_images=False,        # Display images during processing
    width=-1,                    # Custom width (or -1 to read from header)
    height=-1,                   # Custom height (or -1 to read from header)
    pixel_type=-1,              # Pixel type: 8 or 16 bits (or -1 to read from header)
    header_size=-1,             # Header size in bytes (or -1 to read from header)
    tiff_path='output/path'     # Custom output path for TIFF files
)
```

### File Format Specification

The RAW files are expected to have a header containing the following parameters in uint16 format:
1. Image width
2. Image height
3. Pixel data type (8 or 16 bits)
4. Reserved
5. Header size in bytes

## Functions

### `read_raw_parameters(file_path)`
Reads image parameters from the RAW file header.

### `process_raw_file(file_path, ...)`
Processes a single RAW file with options for custom parameters and TIFF conversion.

### `display_image(image_data)`
Displays an image with proper scaling and normalization.

### `process_path(path, ...)`
Main function for processing either single files or directories of RAW files.

## Error Handling

The tool includes basic error handling for:
- Invalid file paths
- Incorrect image dimensions
- Header reading issues
- File access errors

## Example

```python
# Basic usage - process all RAW files in a directory
path = r'C:\Path\To\Your\RAW\Files'
process_path(path, save_tiff=True, display_images=False)

# Advanced usage - specify custom parameters
process_path(
    path,
    save_tiff=True,
    display_images=False,
    width=2976,
    height=2480,
    pixel_type=16,
    header_size=2048
)
```

## License

See the [LICENSE](LICENSE.md) file for license rights and limitations (MIT).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
