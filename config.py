"""
VisionLab Pro - Configuration
"""

import cv2

# Application Info
APP_NAME = "VisionLab Pro"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Comprehensive Image Processing Dashboard"

# Page Configuration
PAGE_TITLE = "VisionLab Pro | Image Enhancement Studio"
PAGE_ICON = "🎨"
LAYOUT = "wide"

# File Upload Settings
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'webp']
MAX_FILE_SIZE = 200 * 1024 * 1024

# Module Categories
MODULES = {
    "🧪 Testing": [
        "Test Simple"
    ],
    "Basic Enhancement": [
        "Auto Enhancer",
        "Image Upscaler",
        "Low-Light Enhancer",
        "Image Denoiser"
    ],
    "Color & Artistic": [
        "Color Enhancement",
        "Filter Gallery",
        "Background Removal"
    ],
    "Advanced Processing": [
        "Edge Detection",
        "Morphological Operations",
        "Image Segmentation"
    ],
    "Analysis & Transform": [
        "Frequency Domain",
        "Histogram Analyzer",
        "Image Compression"
    ],
    "Utilities": [
        "Batch Processing"
    ]
}

# Interpolation Methods
INTERPOLATION_METHODS = {
    'Nearest Neighbor': cv2.INTER_NEAREST,
    'Bilinear': cv2.INTER_LINEAR,
    'Bicubic': cv2.INTER_CUBIC,
    'Lanczos': cv2.INTER_LANCZOS4
}
