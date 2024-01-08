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
    # Use Hough Line Transform to detect lines that are mostly horizontal
    lines = cv2.HoughLinesP(thresh_img, 1, np.pi / 180, threshold=100, minLineLength=thresh_img.shape[1] - 100, maxLineGap=20)

    # Filter out non-horizontal lines and lines at the same position
    horizontal_lines = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if abs(y2 - y1) < 10:  # Adjust for horizontal threshold
            # Check if the line is at the same position as already detected lines
            same_position = False
            for h_line in horizontal_lines:
                hx1, hy1, hx2, hy2 = h_line[0]
                if abs(y1 - hy1) < 10 and abs(y2 - hy2) < 10:  # Adjust for position threshold
                    same_position = True
                    break
            if not same_position:
                horizontal_lines.append(line)

    return horizontal_lines

def segment_image(image, lines):
    # Sort lines by vertical position
    lines = sorted(lines, key=lambda x: x[0][1])
    
    segments = []
    start_y = 0
    for line in lines:
        x1, y1, x2, y2 = line[0]
        # Add the segment of the image above the current line
        segments.append(image[start_y:y1, :])
        start_y = y2
    
    # Add the last segment of the image
    segments.append(image[start_y:, :])
    
    return segments

def sample_usage():
    # Sample usage
    image_path = 'receipts/31-3170553.pdf0.jpg'
    image = cv2.imread(image_path)
    preprocessed_img = preprocess_image(image)
    # show image
    # cv2.imshow('image', preprocessed_img)
    # cv2.waitKey(0)
    detected_lines = detect_lines(preprocessed_img)
    # show lines
    for line in detected_lines:
        x1, y1, x2, y2 = line[0]
        if abs(y1 - y2) < 10:
            cv2.line(preprocessed_img, (x1, y1), (x2, y2), (255, 0, 0), 3)
    cv2.imshow('image', preprocessed_img)
    cv2.waitKey(0)
    segments = segment_image(image, detected_lines)
    # show image
    for i, segment in enumerate(segments):
        cv2.imshow('image', segment)
        cv2.waitKey(0)

if __name__ == '__main__':
    sample_usage()