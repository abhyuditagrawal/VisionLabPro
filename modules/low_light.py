"""
Low-Light Enhancer Module - FIXED
"""

import streamlit as st
import cv2
import numpy as np

def enhance_low_light(image, gamma=2.2, clahe_strength=2.0, denoise_strength=5):
    """Enhance low-light images"""
    result = image.copy().astype(np.float32) / 255.0
    
    # Gamma correction
    result = np.power(result, 1.0 / gamma)
    result = (result * 255).astype(np.uint8)
    
    # CLAHE in HSV
    if len(result.shape) == 3:
        hsv = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        clahe = cv2.createCLAHE(clipLimit=clahe_strength, tileGridSize=(8, 8))
        v = clahe.apply(v)
        hsv = cv2.merge([h, s, v])
        result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    # Denoise
    if denoise_strength > 0:
        result = cv2.bilateralFilter(result, denoise_strength, 75, 75)
    
    return result

def render_low_light():
    """Render Low-Light Enhancer UI"""
    st.markdown("### ⚙️ Settings")
    
    st.markdown("#### 🎚️ Quick Presets")
    col1, col2, col3 = st.columns(3)
    
    preset_clicked = None
    with col1:
        if st.button("💡 Mild", use_container_width=True, key="preset_mild"):
            preset_clicked = 'mild'
    with col2:
        if st.button("🔆 Medium", use_container_width=True, key="preset_medium"):
            preset_clicked = 'medium'
    with col3:
        if st.button("☀️ Strong", use_container_width=True, key="preset_strong"):
            preset_clicked = 'strong'
    
    st.markdown("---")
    
    # Set defaults based on preset
    if preset_clicked == 'mild':
        gamma_val, clahe_val, denoise_val = 1.5, 1.5, 3
    elif preset_clicked == 'medium':
        gamma_val, clahe_val, denoise_val = 2.0, 2.0, 5
    elif preset_clicked == 'strong':
        gamma_val, clahe_val, denoise_val = 2.5, 3.0, 7
    else:
        gamma_val, clahe_val, denoise_val = 2.0, 2.0, 5
    
    gamma = st.slider("Brightness (Gamma)", 1.0, 3.5, gamma_val, 0.1, key="lowlight_gamma")
    clahe_strength = st.slider("Contrast Enhancement", 1.0, 5.0, clahe_val, 0.5, key="lowlight_clahe")
    denoise_strength = st.slider("Denoise Strength", 0, 15, denoise_val, 1, key="lowlight_denoise")
    
    apply_btn = st.button("🌙 Enhance", type="primary", use_container_width=True, key="apply_lowlight")
    
    if apply_btn or preset_clicked:
        with st.spinner("Enhancing low-light image..."):
            try:
                st.session_state.history.append(st.session_state.processed_image.copy())
                enhanced = enhance_low_light(st.session_state.processed_image, gamma, clahe_strength, denoise_strength)
                st.session_state.processed_image = enhanced
                st.success("✅ Low-light enhancement applied!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
