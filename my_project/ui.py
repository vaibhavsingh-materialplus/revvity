import gradio as gr
from PIL import Image
import numpy as np
from main import main
# Dummy function to generate images
def generate_images():
    # Create a list of images (for demonstration purposes)
    images = []
    
    for i in range(4):  # Generate 4 images
        # Create an image with random colors
        img_array = np.random.rand(100, 100, 3) * 255
        img = Image.fromarray(img_array.astype('uint8'))
        images.append(img)
    
    return images

# Gradio interface function
def display_images(text):
    images = generate_images()
    main(text)
    return images

# Create a Gradio interface
interface = gr.Interface(
    fn=display_images, 
    inputs=gr.File(label="Upload PDF File",file_count="single", type="filepath"), 
    outputs=gr.Gallery(label="Images"),  # Use Gallery to display multiple images
    live=True
)

# Launch the interface
if __name__ == "__main__":
    interface.launch()
