"""
Image Denoiser Module - FIXED
"""

import streamlit as st
import cv2

def render_denoiser():  # ← Make sure it's render_denoiser (with 'r' at the end)
    """Render Denoiser UI"""
    st.markdown("### ⚙️ Settings")
    
    filter_type = st.selectbox("Denoising Filter", 
                               ['Gaussian Blur', 'Median Filter', 'Bilateral Filter', 'Non-Local Means'], 
                               index=2, key="denoise_filter_type")
    
    st.markdown("---")
    
    if filter_type == 'Gaussian Blur':
        kernel_size = st.slider("Kernel Size", 3, 31, 5, 2, key="gauss_kernel")
        
        if st.button("🧹 Apply Gaussian Blur", type="primary", use_container_width=True, key="apply_gauss"):
            with st.spinner("Applying Gaussian Blur..."):
                try:
                    st.session_state.history.append(st.session_state.processed_image.copy())
                    result = cv2.GaussianBlur(st.session_state.processed_image, (kernel_size, kernel_size), 0)
                    st.session_state.processed_image = result
                    st.success("✅ Gaussian Blur applied!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    elif filter_type == 'Median Filter':
        kernel_size = st.slider("Kernel Size", 3, 21, 5, 2, key="median_kernel")
        
        if st.button("🧹 Apply Median Filter", type="primary", use_container_width=True, key="apply_median"):
            with st.spinner("Applying Median Filter..."):
                try:
                    st.session_state.history.append(st.session_state.processed_image.copy())
                    result = cv2.medianBlur(st.session_state.processed_image, kernel_size)
                    st.session_state.processed_image = result
                    st.success("✅ Median Filter applied!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    elif filter_type == 'Bilateral Filter':
        col1, col2 = st.columns(2)
        with col1:
            d = st.slider("Diameter", 3, 15, 9, key="bilateral_d")
            sigma_color = st.slider("Color Sigma", 10, 200, 75, key="bilateral_color")
        with col2:
            sigma_space = st.slider("Space Sigma", 10, 200, 75, key="bilateral_space")
        
        if st.button("🧹 Apply Bilateral Filter", type="primary", use_container_width=True, key="apply_bilateral"):
            with st.spinner("Applying Bilateral Filter..."):
                try:
                    st.session_state.history.append(st.session_state.processed_image.copy())
                    result = cv2.bilateralFilter(st.session_state.processed_image, d, sigma_color, sigma_space)
                    st.session_state.processed_image = result
                    st.success("✅ Bilateral Filter applied!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    else:  # Non-Local Means
        col1, col2 = st.columns(2)
        with col1:
            h = st.slider("Filter Strength", 3, 20, 10, key="nlm_h")
            template_size = st.slider("Template Window", 3, 11, 7, 2, key="nlm_template")
        with col2:
            search_size = st.slider("Search Window", 11, 31, 21, 2, key="nlm_search")
        
        if st.button("🧹 Apply Non-Local Means", type="primary", use_container_width=True, key="apply_nlm"):
            with st.spinner("Applying Non-Local Means..."):
                try:
                    st.session_state.history.append(st.session_state.processed_image.copy())
                    if len(st.session_state.processed_image.shape) == 3:
                        result = cv2.fastNlMeansDenoisingColored(st.session_state.processed_image, None, h, h, template_size, search_size)
                    else:
                        result = cv2.fastNlMeansDenoising(st.session_state.processed_image, None, h, template_size, search_size)
                    st.session_state.processed_image = result
                    st.success("✅ Non-Local Means applied!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
