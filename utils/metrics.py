"""
Quality Metrics - FIXED (handles identical images)
"""

import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import mean_squared_error as mse

def calculate_psnr(original, processed):
    """Calculate PSNR"""
    try:
        # Check if images are identical
        if np.array_equal(original, processed):
            return float('inf')  # Perfect quality
        
        if len(original.shape) == 3:
            original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
            processed_gray = cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY)
        else:
            original_gray = original
            processed_gray = processed
        
        return psnr(original_gray, processed_gray)
    except:
        return None

def calculate_ssim(original, processed):
    """Calculate SSIM"""
    try:
        # Check if images are identical
        if np.array_equal(original, processed):
            return 1.0  # Perfect similarity
        
        if len(original.shape) == 3:
            original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
            processed_gray = cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY)
        else:
            original_gray = original
            processed_gray = processed
        
        return ssim(original_gray, processed_gray)
    except:
        return None

def calculate_mse(original, processed):
    """Calculate MSE"""
    try:
        # Check if images are identical
        if np.array_equal(original, processed):
            return 0.0  # No error
        
        return mse(original, processed)
    except:
        return None

def calculate_all_metrics(original, processed):
    """Calculate all metrics"""
    metrics = {
        'PSNR': calculate_psnr(original, processed),
        'SSIM': calculate_ssim(original, processed),
        'MSE': calculate_mse(original, processed)
    }
    return metrics

def get_quality_label(metric_name, value):
    """Get quality label"""
    if value is None:
        return "N/A"
    
    if value == float('inf'):
        return "Identical"
    
    thresholds = {
        'PSNR': {'excellent': 40, 'good': 30, 'fair': 20},
        'SSIM': {'excellent': 0.95, 'good': 0.85, 'fair': 0.70}
    }
    
    if metric_name not in thresholds:
        return "N/A"
    
    t = thresholds[metric_name]
    
    if value >= t['excellent']:
        return "Excellent"
    elif value >= t['good']:
        return "Good"
    elif value >= t['fair']:
        return "Fair"
    else:
        return "Poor"
