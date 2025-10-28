"""
Histogram Analyzer Module - FIXED
"""

import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt

def render_histogram():
    """Render Histogram Analyzer UI"""
    st.markdown("### 📈 Histogram Analysis")
    
    if st.button("📊 Show Histogram", type="primary", use_container_width=True, key="show_histogram"):
        try:
            image = st.session_state.processed_image
            colors = ('b', 'g', 'r')
            fig, ax = plt.subplots(figsize=(10, 4))
            
            if len(image.shape) == 3:
                for i, color in enumerate(colors):
                    hist = cv2.calcHist([image], [i], None, [256], [0, 256])
                    ax.plot(hist, color=color)
                ax.set_title('Color Histogram (B, G, R)')
            else:
                hist = cv2.calcHist([image], [0], None, [256], [0, 256])
                ax.plot(hist, color='black')
                ax.set_title('Grayscale Histogram')
            
            ax.set_xlabel('Pixel Value')
            ax.set_ylabel('Frequency')
            ax.set_xlim([0, 256])
            
            st.pyplot(fig)
            plt.close()
            st.success("✅ Histogram generated!")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    st.markdown("---")
    
    if st.button("⚖️ Equalize Histogram", use_container_width=True, key="equalize_hist"):
        with st.spinner("Equalizing histogram..."):
            try:
                st.session_state.history.append(st.session_state.processed_image.copy())
                
                if len(st.session_state.processed_image.shape) == 3:
                    yuv = cv2.cvtColor(st.session_state.processed_image, cv2.COLOR_BGR2YUV)
                    yuv[:, :, 0] = cv2.equalizeHist(yuv[:, :, 0])
                    result = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
                else:
                    result = cv2.equalizeHist(st.session_state.processed_image)
                
                st.session_state.processed_image = result
                st.success("✅ Histogram equalized!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
