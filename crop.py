import cv2

def crop_image(input_path, output_path, x, y, w, h):
    """
    Crop the image located at input_path and save the cropped image to output_path.

    :param input_path: Path to the input image file.
    :param output_path: Path where the cropped image will be saved.
    :param x: The x-coordinate of the top-left corner of the cropping rectangle.
    :param y: The y-coordinate of the top-left corner of the cropping rectangle.
    :param w: The width of the cropping rectangle.
    :param h: The height of the cropping rectangle.
    """
    try:
        # Read the image using OpenCV
        img = cv2.imread(input_path)

        if img is None:
            raise FileNotFoundError(f"Image file {input_path} not found.")

        # Get image dimensions
        #width, height = img.shape[:2]

        # Ensure cropping coordinates are within image bounds
        #if x < 0 or y < 0 or x + w > width or y + h > height:   
           # raise ValueError("Cropping rectangle exceeds image dimensions.")

        # Crop the image
        cropped_img = img[y:y+h, x:x+w]
        imgray = cv2.cvtColor(cropped_img,cv2.COLOR_BGR2GRAY)
        _,thresh = cv2.threshold(imgray, 250, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

        # Save the cropped image
        if len(contours)<300:
            cv2.imwrite(output_path, cropped_img)
        print(f"Cropped image saved to {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
#crop_image('input.jpg', 'output.jpg', 100, 50, 200, 150)
