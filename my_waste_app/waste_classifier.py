import cv2
import numpy as np

def calculate_texture_features(image):
    """Calculate texture features using gray-level co-occurrence matrix"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    texture_features = np.std(gray)
    return texture_features

def classify_waste(image):
    """
    Enhanced waste classification using color and texture features
    with improved organic waste detection
    """
    # Convert to HSV color space for better color analysis
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Calculate average color in HSV
    avg_color = np.mean(hsv, axis=(0,1))
    hue, saturation, value = avg_color

    # Calculate texture features
    texture = calculate_texture_features(image)

    # Enhanced classification rules with focus on organic waste
    is_organic = (
        (15 <= hue <= 70 and saturation > 30) or    # Yellow-brown-green range
        (texture > 30 and value < 220) or           # Rough texture typical of organic waste
        (saturation > 40 and value < 180)           # Rich colors of organic materials
    )

    is_synthetic = (
        (value > 220 and saturation < 30) or        # Very bright, low saturation
        (190 <= hue <= 270)                         # Blue-purple range
    )

    is_chemical = (
        value < 50 or                               # Very dark materials
        (saturation < 20 and value < 150)           # Gray, dull materials
    )

    # Classify based on the strongest indicator
    if is_organic:
        # Organic materials like banana peels, food waste
        return 'biodegradable', 0.90
    elif is_synthetic:
        # Plastics, metals, glass
        return 'non-biodegradable', 0.85
    elif is_chemical:
        # Chemical or hazardous waste
        return 'chemical', 0.80
    else:
        # If uncertain, analyze texture for final decision
        return ('biodegradable' if texture > 25 else 'non-biodegradable', 0.70)