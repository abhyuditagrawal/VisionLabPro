"""
Background Removal Module
Remove background from images with multiple methods
"""

import streamlit as st
import cv2
import numpy as np

def remove_background_grabcut(image, iterations=5):
    """Remove background using GrabCut algorithm"""
    # Create mask
    mask = np.zeros(image.shape[:2], np.uint8)
    
    # Define rectangle around the subject (center 80% of image)
    height, width = image.shape[:2]
    margin_h = int(height * 0.1)
    margin_w = int(width * 0.1)
    rect = (margin_w, margin_h, width - 2*margin_w, height - 2*margin_h)
    
    # Initialize background and foreground models
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    
    # Apply GrabCut
    cv2.grabCut(image, mask, rect, bgd_model, fgd_model, iterations, cv2.GC_INIT_WITH_RECT)
    
    # Create binary mask
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    
    # Apply mask to image
    result = image * mask2[:, :, np.newaxis]
    
    return result, mask2

def remove_background_threshold(image, threshold=240):
    """Remove white/light backgrounds using simple thresholding"""
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Create mask (invert so dark areas are kept)
    _, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)
    
    # Apply morphological operations to clean up
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # Apply mask
    result = image.copy()
    result[mask == 0] = [0, 0, 0]  # Set background to black
    
    return result, (mask / 255).astype(np.uint8)

def remove_background_color_range(image, lower_color, upper_color):
    """Remove background based on color range"""
    # Convert to HSV for better color detection
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Create mask
    mask = cv2.inRange(hsv, lower_color, upper_color)
    
    # Invert mask (we want to keep the subject, remove background)
    mask = cv2.bitwise_not(mask)
    
    # Apply morphological operations
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # Apply mask
    result = image.copy()
    result[mask == 0] = [0, 0, 0]
    
    return result, (mask / 255).astype(np.uint8)

def add_transparent_background(image, mask):
    """Add alpha channel for transparency"""
    # Convert to RGBA
    b, g, r = cv2.split(image)
    alpha = mask * 255
    result = cv2.merge([b, g, r, alpha.astype(np.uint8)])
    return result

def replace_background(image, mask, new_bg_color):
    """Replace background with custom color"""
    result = image.copy()
    result[mask == 0] = new_bg_color
    return result

def render_background_removal():
    """Render Background Removal UI"""
    st.markdown("### 🎯 Background Removal")
    
    method = st.selectbox(
        "Removal Method",
        ['GrabCut (Auto)', 'Threshold (White BG)', 'Color Range', 'AI-Powered (rembg)'],
        key="bg_method"
    )
    
    st.markdown("---")
    
    if method == 'GrabCut (Auto)':
        st.info("🤖 GrabCut automatically detects the subject in the center of the image")
        
        iterations = st.slider("Iterations", 1, 10, 5, key="grabcut_iter",
                               help="More iterations = better accuracy but slower")
        
        if st.button("🎯 Remove Background", type="primary", use_container_width=True, key="apply_grabcut"):
            with st.spinner("Removing background with GrabCut..."):
                try:
                    st.session_state.history.append(st.session_state.processed_image.copy())
                    result, mask = remove_background_grabcut(st.session_state.processed_image, iterations)
                    st.session_state.processed_image = result
                    st.session_state['current_mask'] = mask
                    st.success("✅ Background removed!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    elif method == 'Threshold (White BG)':
        st.info("📄 Best for images with white or light-colored backgrounds")
        
        threshold = st.slider("Threshold", 100, 255, 240, key="threshold_val",
                             help="Higher = removes lighter backgrounds")
        
        if st.button("🎯 Remove Background", type="primary", use_container_width=True, key="apply_threshold"):
            with st.spinner("Removing background..."):
                try:
                    st.session_state.history.append(st.session_state.processed_image.copy())
                    result, mask = remove_background_threshold(st.session_state.processed_image, threshold)
                    st.session_state.processed_image = result
                    st.session_state['current_mask'] = mask
                    st.success("✅ Background removed!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    elif method == 'Color Range':
        st.info("🎨 Remove specific color ranges (e.g., green screen)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Lower Bound (HSV)**")
            lower_h = st.slider("Hue Min", 0, 180, 40, key="lower_h")
            lower_s = st.slider("Sat Min", 0, 255, 40, key="lower_s")
            lower_v = st.slider("Val Min", 0, 255, 40, key="lower_v")
        
        with col2:
            st.markdown("**Upper Bound (HSV)**")
            upper_h = st.slider("Hue Max", 0, 180, 80, key="upper_h")
            upper_s = st.slider("Sat Max", 0, 255, 255, key="upper_s")
            upper_v = st.slider("Val Max", 0, 255, 255, key="upper_v")
        
        lower = np.array([lower_h, lower_s, lower_v])
        upper = np.array([upper_h, upper_s, upper_v])
        
        if st.button("🎯 Remove Background", type="primary", use_container_width=True, key="apply_color_range"):
            with st.spinner("Removing background..."):
                try:
                    st.session_state.history.append(st.session_state.processed_image.copy())
                    result, mask = remove_background_color_range(st.session_state.processed_image, lower, upper)
                    st.session_state.processed_image = result
                    st.session_state['current_mask'] = mask
                    st.success("✅ Background removed!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    else:  # AI-Powered (rembg)
        st.info("🤖 AI-powered background removal using deep learning")
        st.warning("⚠️ Requires 'rembg' library: pip install rembg")
        
        if st.button("🎯 Remove Background", type="primary", use_container_width=True, key="apply_rembg"):
            with st.spinner("Removing background with AI..."):
                try:
                    from rembg import remove
                    from PIL import Image
                    
                    st.session_state.history.append(st.session_state.processed_image.copy())
                    
                    # Convert to PIL
                    img_rgb = cv2.cvtColor(st.session_state.processed_image, cv2.COLOR_BGR2RGB)
                    pil_img = Image.fromarray(img_rgb)
                    
                    # Remove background
                    output = remove(pil_img)
                    
                    # Convert back to OpenCV
                    result = np.array(output)
                    
                    # If output has alpha channel, convert to BGR by replacing transparent with black
                    if result.shape[2] == 4:
                        mask = result[:, :, 3]
                        bgr = cv2.cvtColor(result[:, :, :3], cv2.COLOR_RGB2BGR)
                        bgr[mask == 0] = [0, 0, 0]
                        result = bgr
                    else:
                        result = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
                    
                    st.session_state.processed_image = result
                    st.success("✅ Background removed with AI!")
                    st.rerun()
                except ImportError:
                    st.error("❌ Please install rembg: pip install rembg")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    # Background replacement options
    if 'current_mask' in st.session_state:
        st.markdown("---")
        st.markdown("### 🎨 Background Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("⬛ Black BG", use_container_width=True, key="bg_black"):
                mask = st.session_state['current_mask']
                result = replace_background(st.session_state.processed_image, mask, [0, 0, 0])
                st.session_state.processed_image = result
                st.rerun()
        
        with col2:
            if st.button("⬜ White BG", use_container_width=True, key="bg_white"):
                mask = st.session_state['current_mask']
                result = replace_background(st.session_state.processed_image, mask, [255, 255, 255])
                st.session_state.processed_image = result
                st.rerun()
        
        with col3:
            if st.button("🔵 Blue BG", use_container_width=True, key="bg_blue"):
                mask = st.session_state['current_mask']
                result = replace_background(st.session_state.processed_image, mask, [255, 0, 0])  # BGR format
                st.session_state.processed_image = result
                st.rerun()
        
        # Custom color picker
        st.markdown("#### Custom Background Color")
        color = st.color_picker("Pick a color", "#00FF00", key="custom_bg_color")
        
        if st.button("Apply Custom Color", use_container_width=True, key="apply_custom_bg"):
            # Convert hex to BGR
            hex_color = color.lstrip('#')
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            bgr = (rgb[2], rgb[1], rgb[0])  # Convert to BGR
            
            mask = st.session_state['current_mask']
            result = replace_background(st.session_state.processed_image, mask, bgr)
            st.session_state.processed_image = result
            st.rerun()
