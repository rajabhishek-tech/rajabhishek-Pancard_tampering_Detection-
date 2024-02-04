from flask import render_template, request
from app import app
import os
from skimage.metrics import structural_similarity
import imutils
import cv2
from PIL import Image

def resize_and_save_image(image, target_path, size=(250, 160)):
    resized_image = image.resize(size)
    resized_image.save(target_path)

def read_image_as_array(image_path):
    return cv2.imread(image_path)

def convert_to_grayscale(image_array):
    return cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)

def calculate_structural_similarity(original_gray, uploaded_gray):
    return structural_similarity(original_gray, uploaded_gray, full=True)

def process_images(file_upload):
    # Paths
    uploads_folder = app.config['UPLOADS_FOLDER']
    existing_images_folder = app.config['EXISTING_IMAGES_FOLDER']

    # Get uploaded image
    uploaded_image = Image.open(file_upload)

    # Resize and save the uploaded image
    resize_and_save_image(uploaded_image, os.path.join(uploads_folder, 'uploaded_image.jpg'))

    # Resize and save the original image
    original_image = Image.open(os.path.join(existing_images_folder, 'original_image.jpg'))
    resize_and_save_image(original_image, os.path.join(existing_images_folder, 'original_image.jpg'))

    # Read uploaded and original images as arrays
    original_image_array = read_image_as_array(os.path.join(existing_images_folder, 'original_image.jpg'))
    uploaded_image_array = read_image_as_array(os.path.join(uploads_folder, 'uploaded_image.jpg'))

    # Convert images into grayscale
    original_gray = convert_to_grayscale(original_image_array)
    uploaded_gray = convert_to_grayscale(uploaded_image_array)

    # Calculate structural similarity
    similarity_score, difference_image = calculate_structural_similarity(original_gray, uploaded_gray)

    return similarity_score, difference_image

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        try:
            # Get uploaded image
            file_upload = request.files['file_upload']

            # Ensure the file is an image
            if not file_upload.content_type.startswith('image'):
                raise ValueError("Uploaded file is not an image.")

            # Process images and calculate similarity score
            similarity_score, difference_image = process_images(file_upload)

            # Save all output images (if required)
            generated_images_folder = app.config['GENERATED_IMAGES_FOLDER']
            cv2.imwrite(os.path.join(generated_images_folder, 'difference_image.jpg'), difference_image)

            return render_template('index.html', similarity_score=f"{round(similarity_score * 100, 2)}% correct")

        except Exception as e:
            # Handle exceptions (e.g., invalid image file, file not found)
            error_message = f"Error: {str(e)}"
            return render_template('index.html', error=error_message)