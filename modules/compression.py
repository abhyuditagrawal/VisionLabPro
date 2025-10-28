"""
Image Compression Module - FIXED
"""

import streamlit as st
import cv2
import numpy as np

def render_compression():
    """Render Compression UI"""
    st.markdown("### 💾 Image Compression")
    
    quality = st.slider("JPEG Quality", 1, 100, 90, key="compression_quality",
                       help="Higher = better quality, larger file")
    
    if st.button("🗜️ Compress", type="primary", use_container_width=True, key="apply_compression"):
        with st.spinner("Compressing..."):
            try:
                st.session_state.history.append(st.session_state.processed_image.copy())
                
                # Simulate JPEG compression
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
                _, encimg = cv2.imencode('.jpg', st.session_state.processed_image, encode_param)
                result = cv2.imdecode(encimg, 1)
                
                st.session_state.processed_image = result
                
                # Calculate compression ratio
                original_size = st.session_state.original_image.nbytes
                compressed_size = len(encimg)
                ratio = original_size / compressed_size
                
                st.success(f"✅ Compressed! Ratio: {ratio:.2f}:1")
                st.info(f"Original: {original_size/1024:.1f} KB → Compressed: {compressed_size/1024:.1f} KB")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
