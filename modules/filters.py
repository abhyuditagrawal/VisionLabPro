"""
Filter Gallery Module
"""

import streamlit as st
import cv2
import numpy as np

def render_filters():
    """Render Filter Gallery UI"""
    st.markdown("### 🎨 Filter Gallery")
    
    tab1, tab2 = st.tabs(["🎭 Artistic", "✨ Effects"])
    
    with tab1:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✏️ Sketch", use_container_width=True):
                with st.spinner("Creating sketch..."):
                    st.session_state.history.append(st.session_state.processed_image.copy())
                    gray = cv2.cvtColor(st.session_state.processed_image, cv2.COLOR_BGR2GRAY)
                    inv_gray = 255 - gray
                    blur = cv2.GaussianBlur(inv_gray, (21, 21), 0)
                    sketch = cv2.divide(gray, 255 - blur, scale=256)
                    result = cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)
                    st.session_state.processed_image = result
                    st.success("✅ Applied!")
                    st.rerun()
        
        with col2:
            if st.button("📜 Sepia", use_container_width=True):
                with st.spinner("Applying sepia..."):
                    st.session_state.history.append(st.session_state.processed_image.copy())
                    kernel = np.array([[0.272, 0.534, 0.131],
                                     [0.349, 0.686, 0.168],
                                     [0.393, 0.769, 0.189]])
                    result = cv2.transform(st.session_state.processed_image, kernel)
                    st.session_state.processed_image = np.clip(result, 0, 255).astype(np.uint8)
                    st.success("✅ Applied!")
                    st.rerun()
        
        with col3:
            if st.button("🎨 Emboss", use_container_width=True):
                with st.spinner("Applying emboss..."):
                    st.session_state.history.append(st.session_state.processed_image.copy())
                    kernel = np.array([[-2, -1, 0], [-1, 1, 1], [0, 1, 2]])
                    result = cv2.filter2D(st.session_state.processed_image, -1, kernel) + 128
                    st.session_state.processed_image = np.clip(result, 0, 255).astype(np.uint8)
                    st.success("✅ Applied!")
                    st.rerun()
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔲 Negative", use_container_width=True):
                with st.spinner("Inverting..."):
                    st.session_state.history.append(st.session_state.processed_image.copy())
                    result = 255 - st.session_state.processed_image
                    st.session_state.processed_image = result
                    st.success("✅ Applied!")
                    st.rerun()
            
            kernel_size = st.slider("Blur Strength", 3, 31, 5, 2)
            if st.button("🌊 Blur", use_container_width=True):
                with st.spinner("Blurring..."):
                    st.session_state.history.append(st.session_state.processed_image.copy())
                    result = cv2.GaussianBlur(st.session_state.processed_image, (kernel_size, kernel_size), 0)
                    st.session_state.processed_image = result
                    st.success("✅ Applied!")
                    st.rerun()
        
        with col2:
            if st.button("⚡ Sharpen", use_container_width=True):
                with st.spinner("Sharpening..."):
                    st.session_state.history.append(st.session_state.processed_image.copy())
                    kernel = np.array([[-1,-1,-1], [-1, 9,-1], [-1,-1,-1]])
                    result = cv2.filter2D(st.session_state.processed_image, -1, kernel)
                    st.session_state.processed_image = np.clip(result, 0, 255).astype(np.uint8)
                    st.success("✅ Applied!")
                    st.rerun()
