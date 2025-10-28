"""
Auto Enhancer Module - FIXED
"""

import streamlit as st
import cv2
import numpy as np

def auto_enhance(image, strength=50):
    """Apply automatic enhancement"""
    result = image.copy().astype(np.float32) / 255.0
    
    # Gamma correction
    gamma = 1.0 + (strength / 100.0) * 0.5
    result = np.power(result, 1.0 / gamma)
    result = (result * 255).astype(np.uint8)
    
    # CLAHE
    if len(result.shape) == 3:
        lab = cv2.cvtColor(result, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0 + strength/50, tileGridSize=(8,8))
        l = clahe.apply(l)
        result = cv2.merge([l, a, b])
        result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
    
    # Sharpening
    blur = cv2.GaussianBlur(result, (0, 0), 3)
    sharpening_strength = strength / 100.0
    result = cv2.addWeighted(result, 1.0 + sharpening_strength, blur, -sharpening_strength, 0)
    
    # Denoising
    if strength > 30:
        result = cv2.bilateralFilter(result, 5, 50, 50)
    
    return np.clip(result, 0, 255).astype(np.uint8)

def render_auto_enhancer():
    """Render Auto Enhancer UI"""
    st.markdown("### ⚙️ Settings")
    
    strength = st.slider("Enhancement Strength", 0, 100, 50, key="auto_strength")
    
    if st.button("✨ Apply Enhancement", type="primary", use_container_width=True, key="apply_auto"):
        with st.spinner("Enhancing image..."):
            try:
                st.session_state.history.append(st.session_state.processed_image.copy())
                enhanced = auto_enhance(st.session_state.processed_image, strength)
                st.session_state.processed_image = enhanced
                st.success("✅ Enhancement applied!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
