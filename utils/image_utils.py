"""
Image Utilities - FIXED (no deprecation warnings)
"""

import cv2
import numpy as np
from PIL import Image
import streamlit as st
from io import BytesIO

def load_image(uploaded_file):
    """Load image from uploaded file"""
    try:
        image = Image.open(uploaded_file)
        image_np = np.array(image)
        
        if len(image_np.shape) == 3 and image_np.shape[2] == 3:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        
        return image_np
    except Exception as e:
        st.error(f"Error loading image: {str(e)}")
        return None

def save_image(image, format='PNG'):
    """Convert image to downloadable bytes"""
    try:
        if len(image.shape) == 3 and image.shape[2] == 3:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            image_rgb = image
        
        pil_image = Image.fromarray(image_rgb.astype('uint8'))
        
        buf = BytesIO()
        pil_image.save(buf, format=format)
        byte_im = buf.getvalue()
        
        return byte_im
    except Exception as e:
        st.error(f"Error saving image: {str(e)}")
        return None

def display_image(image, caption="", use_container_width=True):
    """Display image in Streamlit (FIXED - no deprecation warning)"""
    try:
        if len(image.shape) == 3 and image.shape[2] == 3:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            image_rgb = image
        
        # Changed from use_column_width to use_container_width
        st.image(image_rgb, caption=caption, use_container_width=use_container_width)
    except Exception as e:
        st.error(f"Error displaying image: {str(e)}")

def get_image_info(image):
    """Get image information"""
    info = {
        'height': image.shape[0],
        'width': image.shape[1],
        'channels': image.shape[2] if len(image.shape) == 3 else 1,
        'dtype': str(image.dtype),
        'size_mb': image.nbytes / (1024 * 1024)
    }
    return info
