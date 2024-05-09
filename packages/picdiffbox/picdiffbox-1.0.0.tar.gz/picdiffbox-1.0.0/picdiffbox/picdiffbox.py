import cv2
from skimage.metrics import structural_similarity as ssim
import numpy as np
import os

def compare_images(image1_path, image2_path, output_dir=None):
    # Load the two images
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)

    # Convert images to grayscale
    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Compute the Structural Similarity Index (SSI) between the two images
    (score, diff) = ssim(gray_image1, gray_image2, full=True)
    diff = (diff * 255).astype("uint8")

    # Threshold the difference image, find contours to localize differences
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw bounding boxes around the differences
    for i, contour in enumerate(contours):
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(image1, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # Save the image with differences highlighted
    if output_dir is None:
        output_dir = os.path.dirname(image1_path)
    output_path = os.path.join(output_dir, 'diff_image.png')
    cv2.imwrite(output_path, image1)
    print(f"Differences saved in: {output_path}")
    return output_path

# Example usage
# result_path = compare_images('input1.png', 'input2.png')
# print(f"Differences saved in: {result_path}")
