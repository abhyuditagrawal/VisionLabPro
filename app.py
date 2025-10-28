"""
VisionLab Pro - Main Application (SESSION STATE FIXED)
"""

import streamlit as st
import cv2
import numpy as np
from config import *
from utils.image_utils import load_image, save_image, get_image_info
from utils.metrics import calculate_all_metrics, get_quality_label

# Page config
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout=LAYOUT)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF4B4B;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'original_image' not in st.session_state:
    st.session_state.original_image = None
if 'processed_image' not in st.session_state:
    st.session_state.processed_image = None
if 'history' not in st.session_state:
    st.session_state.history = []
if 'current_module' not in st.session_state:
    st.session_state.current_module = "Auto Enhancer"
if 'current_file_id' not in st.session_state:
    st.session_state.current_file_id = None

# Header
st.markdown(f'<div class="main-header">🎨 {APP_NAME}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-header">{APP_DESCRIPTION}</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📤 Upload Image")
    uploaded_file = st.file_uploader("Choose an image", type=ALLOWED_EXTENSIONS, key="file_uploader")
    
    # Only load image if it's a NEW upload
    if uploaded_file is not None:
        file_id = f"{uploaded_file.name}_{uploaded_file.size}"
        
        # Check if this is a new file
        if st.session_state.current_file_id != file_id:
            image = load_image(uploaded_file)
            if image is not None:
                st.session_state.original_image = image
                st.session_state.processed_image = image.copy()
                st.session_state.history = []
                st.session_state.current_file_id = file_id
                st.success("✅ Image loaded!")
        
        # Show info if image exists
        if st.session_state.original_image is not None:
            info = get_image_info(st.session_state.original_image)
            with st.expander("📊 Image Info"):
                st.write(f"**Dimensions:** {info['width']} × {info['height']}")
                st.write(f"**Channels:** {info['channels']}")
                st.write(f"**Size:** {info['size_mb']:.2f} MB")
    
    st.markdown("---")
    st.header("🛠️ Modules")
    
    for category, modules in MODULES.items():
        st.subheader(category)
        for module in modules:
            if st.button(module, key=f"btn_{module}", use_container_width=True):
                st.session_state.current_module = module
                st.rerun()
    
    st.markdown("---")
    st.header("⚡ Quick Actions")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Reset", use_container_width=True):
            if st.session_state.original_image is not None:
                st.session_state.processed_image = st.session_state.original_image.copy()
                st.rerun()
    
    with col2:
        if st.button("↩️ Undo", use_container_width=True):
            if len(st.session_state.history) > 0:
                st.session_state.processed_image = st.session_state.history.pop()
                st.rerun()
    
    if st.session_state.processed_image is not None:
        st.markdown("---")
        st.header("💾 Download")
        
        col1, col2 = st.columns(2)
        
        with col1:
            png_data = save_image(st.session_state.processed_image, 'PNG')
            if png_data:
                st.download_button("PNG", png_data, "output.png", "image/png", use_container_width=True)
        
        with col2:
            jpg_data = save_image(st.session_state.processed_image, 'JPEG')
            if jpg_data:
                st.download_button("JPEG", jpg_data, "output.jpg", "image/jpeg", use_container_width=True)

# Main content
if st.session_state.original_image is None:
    st.info("👈 Upload an image to get started!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📸 Basic")
        st.write("• Auto Enhancer")
        st.write("• Upscaler")
        st.write("• Low-Light")
        st.write("• Denoiser")
    
    with col2:
        st.markdown("#### 🎨 Advanced")
        st.write("• Color Enhancement")
        st.write("• Filters")
        st.write("• Edge Detection")
        st.write("• Morphology")
    
    with col3:
        st.markdown("#### 📊 Analysis")
        st.write("• Segmentation")
        st.write("• Frequency")
        st.write("• Histogram")
        st.write("• Compression")

else:
    current_module = st.session_state.current_module
    st.header(f"🔧 {current_module}")
    
    # Display images
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original")
        if len(st.session_state.original_image.shape) == 3:
            original_display = cv2.cvtColor(st.session_state.original_image, cv2.COLOR_BGR2RGB)
        else:
            original_display = st.session_state.original_image
        st.image(original_display, use_container_width=True)
    
    with col2:
        st.subheader("Processed")
        if len(st.session_state.processed_image.shape) == 3:
            processed_display = cv2.cvtColor(st.session_state.processed_image, cv2.COLOR_BGR2RGB)
        else:
            processed_display = st.session_state.processed_image
        st.image(processed_display, use_container_width=True)
    
    st.markdown("---")
    
    # Module routing
    if current_module == "Test Simple":
        from modules.test_simple import render_test_simple
        render_test_simple()
    
    elif current_module == "Auto Enhancer":
        from modules.auto_enhancer import render_auto_enhancer
        render_auto_enhancer()
    
    elif current_module == "Image Upscaler":
        from modules.upscaler import render_upscaler
        render_upscaler()
    
    elif current_module == "Background Removal":
        from modules.background_removal import render_background_removal
        render_background_removal()
    
    elif current_module == "Low-Light Enhancer":
        from modules.low_light import render_low_light
        render_low_light()
    
    elif current_module == "Image Denoiser":
        from modules.denoiser import render_denoiser
        render_denoiser()
    
    elif current_module == "Color Enhancement":
        from modules.color_enhancement import render_color_enhancement
        render_color_enhancement()
    
    elif current_module == "Filter Gallery":
        from modules.filters import render_filters
        render_filters()
    
    elif current_module == "Edge Detection":
        from modules.edge_detection import render_edge_detection
        render_edge_detection()
    
    elif current_module == "Morphological Operations":
        from modules.morphology import render_morphology
        render_morphology()
    
    elif current_module == "Image Segmentation":
        from modules.segmentation import render_segmentation
        render_segmentation()
    
    elif current_module == "Frequency Domain":
        from modules.frequency import render_frequency
        render_frequency()
    
    elif current_module == "Histogram Analyzer":
        from modules.histogram import render_histogram
        render_histogram()
    
    elif current_module == "Image Compression":
        from modules.compression import render_compression
        render_compression()
    
    elif current_module == "Batch Processing":
        from modules.batch_processing import render_batch_processing
        render_batch_processing()
    
    # Quality metrics
    st.markdown("---")
    st.subheader("📊 Quality Metrics")
    
    try:
        metrics = calculate_all_metrics(st.session_state.original_image, st.session_state.processed_image)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            psnr_val = metrics.get('PSNR')
            if psnr_val:
                if psnr_val == float('inf'):
                    st.metric("PSNR", "∞ dB", "Identical")
                else:
                    label = get_quality_label('PSNR', psnr_val)
                    st.metric("PSNR", f"{psnr_val:.2f} dB", label)
        
        with col2:
            ssim_val = metrics.get('SSIM')
            if ssim_val:
                label = get_quality_label('SSIM', ssim_val)
                st.metric("SSIM", f"{ssim_val:.4f}", label)
        
        with col3:
            mse_val = metrics.get('MSE')
            if mse_val is not None:
                st.metric("MSE", f"{mse_val:.2f}")
    except Exception as e:
        st.info("Processing image...")

# Footer
st.markdown("---")
st.markdown(f"<div style='text-align: center; color: #666;'>{APP_NAME} v{APP_VERSION} | Built with Streamlit & OpenCV</div>", unsafe_allow_html=True)
