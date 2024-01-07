import cv2

def size_2x(image):
    return cv2.resize(image, (0,0), fx=1.6, fy=1.6)

# image segmenting didn't help improve ocr accuracy
import cv2
import numpy as np

def preprocess_image(image):
    # TODO: add preprocessing for images captured with phone
    # Read image in grayscale
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply binary thresholding
    _, thresh = cv2.threshold(grayscale, 150, 255, cv2.THRESH_BINARY_INV)
    return thresh

def detect_lines(thresh_img):
    # Use Hough Line Transform to detect lines only horizontally
    lines = cv2.HoughLinesP(thresh_img, 1, np.pi / 180, threshold=100, minLineLength=200, maxLineGap=10)
    return lines

def segment_image(image, lines):
    # Sort lines by vertical position
    lines = sorted(lines, key=lambda x: x[0][1])
    
    segments = []
    start_y = 0
    for line in lines:
        x1, y1, x2, y2 = line[0]
        # Segment the image
        # check if the line is horizontal
        if abs(y1 - y2) < 10:
            segment = image[start_y:y1, :]
            segments.append(segment)
            start_y = y2  # Update the starting y-coordinate for the next segment
    
    # Add the last segment of the image
    segments.append(image[start_y:, :])
    
    return segments

def sample_usage():
    # Sample usage
    image_path = 'receipt_images/receipt1.jpg'
    preprocessed_img = preprocess_image(image_path)
    # show image
    # cv2.imshow('image', preprocessed_img)
    # cv2.waitKey(0)
    detected_lines = detect_lines(preprocessed_img)
    # # show lines
    # for line in detected_lines:
    #     x1, y1, x2, y2 = line[0]
    #     if abs(y1 - y2) < 10:
    #         cv2.line(preprocessed_img, (x1, y1), (x2, y2), (255, 0, 0), 3)
    # cv2.imshow('image', preprocessed_img)
    # cv2.waitKey(0)
    image = cv2.imread(image_path)
    segments = segment_image(image, detected_lines)
    # show image
    for i, segment in enumerate(segments):
        cv2.imshow('image', segment)
        cv2.waitKey(0)
