"""
Image Upscaler Module - FIXED
"""

import streamlit as st
import cv2
import numpy as np

def upscale_image(image, scale_factor, method='Bicubic', sharpen=True):
    """Upscale image"""
    interpolation_map = {
        'Nearest Neighbor': cv2.INTER_NEAREST,
        'Bilinear': cv2.INTER_LINEAR,
        'Bicubic': cv2.INTER_CUBIC,
        'Lanczos': cv2.INTER_LANCZOS4
    }
    
    interpolation = interpolation_map.get(method, cv2.INTER_CUBIC)
    height, width = image.shape[:2]
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    
    upscaled = cv2.resize(image, (new_width, new_height), interpolation=interpolation)
    
    if sharpen:
        kernel = np.array([[-1,-1,-1], [-1, 9,-1], [-1,-1,-1]])
        upscaled = cv2.filter2D(upscaled, -1, kernel)
        upscaled = np.clip(upscaled, 0, 255).astype(np.uint8)
    
    return upscaled

def render_upscaler():
    """Render Upscaler UI"""
    st.markdown("### ⚙️ Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        scale_factor = st.selectbox("Scale Factor", [1.5, 2.0, 3.0, 4.0], index=1, key="scale_factor")
    
    with col2:
        method = st.selectbox("Method", ['Nearest Neighbor', 'Bilinear', 'Bicubic', 'Lanczos'], index=2, key="upscale_method")
    
    sharpen = st.checkbox("Apply Post-Sharpening", value=True, key="sharpen_check")
    
    if st.button("🔍 Upscale Image", type="primary", use_container_width=True, key="apply_upscale"):
        with st.spinner(f"Upscaling to {scale_factor}×..."):
            try:
                st.session_state.history.append(st.session_state.processed_image.copy())
                upscaled = upscale_image(st.session_state.processed_image, scale_factor, method, sharpen)
                st.session_state.processed_image = upscaled
                st.success(f"✅ Image upscaled to {upscaled.shape[1]} × {upscaled.shape[0]}!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
