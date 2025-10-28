"""
Simple Test Module - To verify processing works
"""

import streamlit as st
import cv2
import numpy as np

def render_test_simple():
    """Render Test Module"""
    st.markdown("### 🧪 Simple Tests")
    
    st.info("These are EXTREME transformations - you WILL see the difference!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔴 Make Red", use_container_width=True, key="test_red"):
            st.session_state.history.append(st.session_state.processed_image.copy())
            # Make entire image red
            result = st.session_state.processed_image.copy()
            result[:, :, 0] = 0  # Blue = 0
            result[:, :, 1] = 0  # Green = 0
            result[:, :, 2] = 255  # Red = 255
            st.session_state.processed_image = result
            st.success("✅ Made RED!")
            st.rerun()
    
    with col2:
        if st.button("⬛ Make Black", use_container_width=True, key="test_black"):
            st.session_state.history.append(st.session_state.processed_image.copy())
            # Make entire image black
            result = np.zeros_like(st.session_state.processed_image)
            st.session_state.processed_image = result
            st.success("✅ Made BLACK!")
            st.rerun()
    
    with col3:
        if st.button("⬜ Make White", use_container_width=True, key="test_white"):
            st.session_state.history.append(st.session_state.processed_image.copy())
            # Make entire image white
            result = np.ones_like(st.session_state.processed_image) * 255
            st.session_state.processed_image = result
            st.success("✅ Made WHITE!")
            st.rerun()
    
    st.markdown("---")
    
    if st.button("🔄 Flip Upside Down", use_container_width=True, key="test_flip"):
        st.session_state.history.append(st.session_state.processed_image.copy())
        result = cv2.flip(st.session_state.processed_image, 0)
        st.session_state.processed_image = result
        st.success("✅ Flipped!")
        st.rerun()
    
    if st.button("🔲 True Negative (Invert)", use_container_width=True, key="test_negative"):
        st.session_state.history.append(st.session_state.processed_image.copy())
        result = 255 - st.session_state.processed_image
        st.session_state.processed_image = result
        st.success("✅ Inverted!")
        st.rerun()
    
    # Show pixel values
    st.markdown("---")
    st.markdown("### 🔍 Pixel Inspector")
    
    orig_pixel = st.session_state.original_image[0, 0]
    proc_pixel = st.session_state.processed_image[0, 0]
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Original Pixel [0,0]:**")
        st.code(f"B:{orig_pixel[0]} G:{orig_pixel[1]} R:{orig_pixel[2]}")
    
    with col2:
        st.write("**Processed Pixel [0,0]:**")
        st.code(f"B:{proc_pixel[0]} G:{proc_pixel[1]} R:{proc_pixel[2]}")
    
    if np.array_equal(st.session_state.original_image, st.session_state.processed_image):
        st.error("⚠️ IMAGES ARE IDENTICAL - Processing not working!")
    else:
        st.success("✅ Images are different - Processing IS working!")
