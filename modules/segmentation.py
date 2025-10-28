"""
Image Segmentation Module - FIXED
"""

import streamlit as st
import cv2
import numpy as np

def render_segmentation():
    """Render Segmentation UI"""
    st.markdown("### ⚙️ Settings")
    
    method = st.selectbox("Segmentation Method", 
                         ['Global Threshold', 'Otsu Threshold', 'Adaptive Threshold'], 
                         key="seg_method")
    
    if method == 'Global Threshold':
        threshold = st.slider("Threshold Value", 0, 255, 127, key="seg_global_thresh")
        
        if st.button("🎯 Segment", type="primary", use_container_width=True, key="apply_global_thresh"):
            with st.spinner("Segmenting..."):
                try:
                    st.session_state.history.append(st.session_state.processed_image.copy())
                    gray = cv2.cvtColor(st.session_state.processed_image, cv2.COLOR_BGR2GRAY)
                    _, thresh = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
                    result = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
                    st.session_state.processed_image = result
                    st.success("✅ Global threshold applied!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    elif method == 'Otsu Threshold':
        if st.button("🎯 Segment", type="primary", use_container_width=True, key="apply_otsu"):
            with st.spinner("Segmenting with Otsu..."):
                try:
                    st.session_state.history.append(st.session_state.processed_image.copy())
                    gray = cv2.cvtColor(st.session_state.processed_image, cv2.COLOR_BGR2GRAY)
                    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                    result = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
                    st.session_state.processed_image = result
                    st.success("✅ Otsu threshold applied!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    else:  # Adaptive Threshold
        block_size = st.slider("Block Size", 3, 51, 11, 2, key="seg_block_size")
        C = st.slider("Constant C", -10, 10, 2, key="seg_c")
        
        if st.button("🎯 Segment", type="primary", use_container_width=True, key="apply_adaptive"):
            with st.spinner("Segmenting with adaptive threshold..."):
                try:
                    st.session_state.history.append(st.session_state.processed_image.copy())
                    gray = cv2.cvtColor(st.session_state.processed_image, cv2.COLOR_BGR2GRAY)
                    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                                   cv2.THRESH_BINARY, block_size, C)
                    result = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
                    st.session_state.processed_image = result
                    st.success("✅ Adaptive threshold applied!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
