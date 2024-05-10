Image Processing Package (text_seg)
Overview

The Image Processing Package (text_seg) is a Python package designed to provide functionalities for image preprocessing and segmentation tasks.
Installation

You can install text_seg using pip:
pip install text_seg

Python Script Usage

from text_seg import main

if __name__ == "__main__":
    # Path to the image
    image_path = "/path/to/image.png"
    
    # Run the main function with appropriate arguments
    main.main(["-p", "-i", image_path])

Dependencies

    opencv-python>=4.0
    tensorflow==2.14.0

License

This project is licensed under the MIT License - see the LICENSE file for details.
Author

    Beijuka Bruno
    Email: beijukab@gmail.com
