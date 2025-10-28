"""
Color Enhancement Module - FIXED
"""

import streamlit as st
import cv2
import numpy as np

def adjust_hsv(image, hue_shift=0, saturation_scale=1.0, value_scale=1.0):
    """Adjust HSV values"""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 0] = (hsv[:, :, 0] + hue_shift) % 180
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * saturation_scale, 0, 255)
    hsv[:, :, 2] = np.clip(hsv[:, :, 2] * value_scale, 0, 255)
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

def auto_white_balance(image):
    """Auto white balance"""
    result = image.astype(np.float32)
    avg_b, avg_g, avg_r = np.mean(result[:, :, 0]), np.mean(result[:, :, 1]), np.mean(result[:, :, 2])
    gray = (avg_b + avg_g + avg_r) / 3
    
    result[:, :, 0] = np.clip(result[:, :, 0] * (gray / avg_b), 0, 255)
    result[:, :, 1] = np.clip(result[:, :, 1] * (gray / avg_g), 0, 255)
    result[:, :, 2] = np.clip(result[:, :, 2] * (gray / avg_r), 0, 255)
    
    return result.astype(np.uint8)

def render_color_enhancement():
    """Render Color Enhancement UI"""
    st.markdown("### ⚙️ Settings")
    
    tab1, tab2 = st.tabs(["🎨 HSV Adjustment", "⚡ Quick Tools"])
    
    with tab1:
        hue_shift = st.slider("Hue Shift", -180, 180, 0, key="color_hue")
        saturation = st.slider("Saturation", 0, 200, 100, key="color_sat")
        value = st.slider("Brightness", 0, 200, 100, key="color_val")
        
        if st.button("🎨 Apply HSV", type="primary", use_container_width=True, key="apply_hsv"):
            with st.spinner("Applying HSV adjustments..."):
                try:
                    st.session_state.history.append(st.session_state.processed_image.copy())
                    result = adjust_hsv(st.session_state.processed_image, hue_shift, saturation/100.0, value/100.0)
                    st.session_state.processed_image = result
                    st.success("✅ HSV adjustments applied!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔘 Auto White Balance", use_container_width=True, key="apply_wb"):
                with st.spinner("Applying white balance..."):
                    try:
                        st.session_state.history.append(st.session_state.processed_image.copy())
                        result = auto_white_balance(st.session_state.processed_image)
                        st.session_state.processed_image = result
                        st.success("✅ White balance applied!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        with col2:
            if st.button("📊 Histogram Eq", use_container_width=True, key="apply_histeq"):
                with st.spinner("Equalizing histogram..."):
                    try:
                        st.session_state.history.append(st.session_state.processed_image.copy())
                        yuv = cv2.cvtColor(st.session_state.processed_image, cv2.COLOR_BGR2YUV)
                        yuv[:, :, 0] = cv2.equalizeHist(yuv[:, :, 0])
                        result = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
                        st.session_state.processed_image = result
                        st.success("✅ Histogram equalized!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
