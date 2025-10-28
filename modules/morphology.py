"""
Morphological Operations Module - FIXED
"""

import streamlit as st
import cv2
import numpy as np

def render_morphology():
    """Render Morphology UI"""
    st.markdown("### ⚙️ Settings")
    
    operation = st.selectbox("Operation", 
                            ['Erosion', 'Dilation', 'Opening', 'Closing', 'Gradient'], 
                            key="morph_operation")
    
    col1, col2 = st.columns(2)
    with col1:
        kernel_size = st.slider("Kernel Size", 3, 15, 5, 2, key="morph_kernel")
    with col2:
        iterations = st.slider("Iterations", 1, 5, 1, key="morph_iterations")
    
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    
    if st.button("🔬 Apply", type="primary", use_container_width=True, key="apply_morph"):
        with st.spinner(f"Applying {operation}..."):
            try:
                st.session_state.history.append(st.session_state.processed_image.copy())
                
                if operation == 'Erosion':
                    result = cv2.erode(st.session_state.processed_image, kernel, iterations=iterations)
                elif operation == 'Dilation':
                    result = cv2.dilate(st.session_state.processed_image, kernel, iterations=iterations)
                elif operation == 'Opening':
                    result = cv2.morphologyEx(st.session_state.processed_image, cv2.MORPH_OPEN, kernel, iterations=iterations)
                elif operation == 'Closing':
                    result = cv2.morphologyEx(st.session_state.processed_image, cv2.MORPH_CLOSE, kernel, iterations=iterations)
                else:  # Gradient
                    result = cv2.morphologyEx(st.session_state.processed_image, cv2.MORPH_GRADIENT, kernel)
                
                st.session_state.processed_image = result
                st.success(f"✅ {operation} applied!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
