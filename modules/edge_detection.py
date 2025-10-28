"""
Edge Detection Module - FIXED
"""

import streamlit as st
import cv2
import numpy as np

def render_edge_detection():
    """Render Edge Detection UI"""
    st.markdown("### ⚙️ Settings")
    
    method = st.selectbox("Edge Detection Method", ['Canny', 'Sobel', 'Laplacian'], index=0, key="edge_method")
    
    st.markdown("---")
    
    if method == 'Canny':
        col1, col2 = st.columns(2)
        with col1:
            low_threshold = st.slider("Low Threshold", 0, 200, 50, key="canny_low")
        with col2:
            high_threshold = st.slider("High Threshold", 0, 300, 150, key="canny_high")
        
        if st.button("🔲 Detect Edges", type="primary", use_container_width=True, key="apply_canny"):
            with st.spinner("Detecting edges with Canny..."):
                try:
                    st.session_state.history.append(st.session_state.processed_image.copy())
                    gray = cv2.cvtColor(st.session_state.processed_image, cv2.COLOR_BGR2GRAY)
                    edges = cv2.Canny(gray, low_threshold, high_threshold)
                    result = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
                    st.session_state.processed_image = result
                    st.success("✅ Canny edge detection applied!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    elif method == 'Sobel':
        ksize = st.select_slider("Kernel Size", options=[1, 3, 5, 7], value=3, key="sobel_ksize")
        
        if st.button("🔲 Detect Edges", type="primary", use_container_width=True, key="apply_sobel"):
            with st.spinner("Detecting edges with Sobel..."):
                try:
                    st.session_state.history.append(st.session_state.processed_image.copy())
                    gray = cv2.cvtColor(st.session_state.processed_image, cv2.COLOR_BGR2GRAY)
                    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
                    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)
                    magnitude = np.sqrt(sobelx**2 + sobely**2)
                    magnitude = np.uint8(magnitude * 255 / magnitude.max())
                    result = cv2.cvtColor(magnitude, cv2.COLOR_GRAY2BGR)
                    st.session_state.processed_image = result
                    st.success("✅ Sobel edge detection applied!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    else:  # Laplacian
        ksize = st.select_slider("Kernel Size", options=[1, 3, 5, 7], value=3, key="laplacian_ksize")
        
        if st.button("🔲 Detect Edges", type="primary", use_container_width=True, key="apply_laplacian"):
            with st.spinner("Detecting edges with Laplacian..."):
                try:
                    st.session_state.history.append(st.session_state.processed_image.copy())
                    gray = cv2.cvtColor(st.session_state.processed_image, cv2.COLOR_BGR2GRAY)
                    laplacian = cv2.Laplacian(gray, cv2.CV_64F, ksize=ksize)
                    laplacian = np.uint8(np.absolute(laplacian))
                    result = cv2.cvtColor(laplacian, cv2.COLOR_GRAY2BGR)
                    st.session_state.processed_image = result
                    st.success("✅ Laplacian edge detection applied!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
