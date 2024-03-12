import argparse
import pyzbar
import cv2

def preprocess(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Resize image
    image = cv2.resize(image, None, fx=0.7, fy=0.7, interpolation=cv2.INTER_CUBIC)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate x & y gradient
    gradX = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    gradY = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)

    # Subtract the y-gradient from the x-gradient
    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)

    # Blur the image
    blurred = cv2.blur(gradient, (3, 3))

    # Threshold the image
    _, thresh = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)

    return thresh

def barcode(image):
    # Create a reader
    scanner = zbar.ImageScanner()

    # Configure the reader
    scanner.parse_config('enable')

    # Obtain image data
    width, height = image.shape[::-1]  # OpenCV returns height and width in reverse order
    raw = image.tobytes()

    image_data = zbar.Image(width, height, 'Y800', raw)

    # Scan the image for barcodes
    scanner.scan(image_data)

    # Extract results
    for symbol in image_data:
        # Print barcode format and data
        print('Barcode Format:', symbol.type)
        print('Barcode Data:', symbol.data)

    print('-----------------------------------------------------------------------')

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Barcode Detection and Decoding')
    parser.add_argument('-i', '--image', required=True, help='Path to the input image file')
    args = parser.parse_args()

    # Preprocess the image
    processed_image = preprocess(args.image)

    # Detect and decode barcodes
    barcode(processed_image)

if __name__ == '__main__':
    main()
