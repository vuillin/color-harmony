import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
from color_utils import rgb_to_hex

def extract_colors_from_image(image_path, num_colors=5):
    """
    Extracts dominant colors from an image using K-Means clustering.
    Resizes image for performance before processing.
    """
    try:
        img = Image.open(image_path)
        img = img.convert('RGB')
        img = img.resize((150, 150))
        
        img_array = np.array(img)
        pixels = img_array.reshape(-1, 3)

        kmeans = KMeans(n_clusters=num_colors, random_state=42, n_init=10)
        kmeans.fit(pixels)
        
        colors = kmeans.cluster_centers_.astype(int)
        hex_colors = [rgb_to_hex(tuple(color)) for color in colors]
        
        return hex_colors

    except Exception as e:
        print(f"Error processing image: {e}")
        return []