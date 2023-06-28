import cv2
import numpy as np
from sklearn.cluster import KMeans

def find_dominant_color(image_path, num_colors):
    # Load the image with alpha channel
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    # Filter out transparent pixels
    non_transparent_pixels = image[:, :, :3][image[:, :, 3] == 255]

    # Reshape the pixels to a 2D array
    pixels = non_transparent_pixels.reshape(-1, 3)

    # Perform K-means clustering on the pixel values
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)

    # Get the RGB values of the cluster centers
    colors = kmeans.cluster_centers_

    # Get the labels assigned to each pixel
    labels = kmeans.labels_

    # Count the frequency of each label
    label_counts = np.bincount(labels)

    # Find the index of the most frequent label
    dominant_color_index = np.argmax(label_counts)

    # Get the dominant color using its index
    dominant_color = colors[dominant_color_index]

    return dominant_color.astype(int)

# Specify the path to your image and the number of dominant colors to find
image_path = "data/temp/result_single/test.png"
num_colors = 3

# Find the dominant color
dominant_color = find_dominant_color(image_path, num_colors)

# Print the dominant color (RGB values)
print("Dominant Color: ", dominant_color)