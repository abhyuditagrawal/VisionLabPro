"""
Frequency Domain Module - FIXED
"""

import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt

def render_frequency():
    """Render Frequency Domain UI"""
    st.markdown("### 📊 Frequency Domain Analysis")
    
    if st.button("🔄 Compute FFT", type="primary", use_container_width=True, key="compute_fft"):
        with st.spinner("Computing FFT..."):
            try:
                gray = cv2.cvtColor(st.session_state.processed_image, cv2.COLOR_BGR2GRAY)
                
                # FFT
                f = np.fft.fft2(gray)
                fshift = np.fft.fftshift(f)
                magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1)
                
                # Display
                fig, ax = plt.subplots(1, 2, figsize=(12, 5))
                ax[0].imshow(gray, cmap='gray')
                ax[0].set_title('Original Image')
                ax[0].axis('off')
                
                ax[1].imshow(magnitude_spectrum, cmap='gray')
                ax[1].set_title('Magnitude Spectrum')
                ax[1].axis('off')
                
                st.pyplot(fig)
                plt.close()
                st.success("✅ FFT computed!")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    st.info("💡 Frequency domain shows the image in terms of its frequency components.")
