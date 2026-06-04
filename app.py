import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import os  # Imported to handle local file path checking

# --- Configuration ---
RESIZE_OPTIONS = {
    "2500 x 1308 pixels (Website Hero)": (2500, 1308),
    "1200 x 1200 pixels (Square Post)": (1200, 1200),
    "1200 x 628 pixels (Social Media Banner)": (1200, 628),
    "960 x 1200 pixels (Vertical)": (960, 1200),
    "300 x 600 pixels (Sidebar Ad)": (300, 600),
}

# Define the path to your default image
DEFAULT_IMAGE_PATH = "default_image.jpg"  # Replace with your local file name/path

# --- Streamlit App Layout ---
st.set_page_config(
    page_title="Image Resizer App",
    layout="centered",
    initial_sidebar_state="auto"
)

st.title("📸 Image Resizer")
st.info("This is a beginner Pythonic image resizer developed with vibe coding. More functionalities can be added in this app.")
st.markdown("Upload an image and choose a predefined size to resize it.")

# --- 1. Upload Button ---
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

pil_image = None

# Check if user uploaded a file, otherwise try to load the default image
if uploaded_file is not None:
    pil_image = Image.open(uploaded_file)
    image_caption = "Uploaded Image"
elif os.path.exists(DEFAULT_IMAGE_PATH):
    pil_image = Image.open(DEFAULT_IMAGE_PATH)
    image_caption = "Default Image (No file uploaded)"
else:
    st.info("Please upload an image to get started.")

# --- 2. Processing and Display ---
if pil_image is not None:
    # Convert PIL image to OpenCV format (numpy array)
    opencv_image_rgb = np.array(pil_image)
    opencv_image_bgr = cv2.cvtColor(opencv_image_rgb, cv2.COLOR_RGB2BGR)

    st.subheader("Original Image")
    st.image(pil_image, caption=image_caption, use_column_width=True)
    st.write(f"Original Dimensions: {pil_image.width} x {pil_image.height} pixels")
    st.markdown("---")

    # --- Single Selection for Resizing with Radio Buttons ---
    st.subheader("Resize Options")
    selected_size_label = st.radio(
        "Select desired output size:",
        list(RESIZE_OPTIONS.keys())
    )

    if selected_size_label:
        st.subheader("Resized Image")
        
        # Create a container for results to keep it organized
        results_container = st.container()

        # Process the single selected size
        width, height = RESIZE_OPTIONS[selected_size_label]
        
        with results_container:
            st.write(f"### {selected_size_label}")
            
            # Perform resizing using OpenCV
            try:
                resized_image_bgr = cv2.resize(opencv_image_bgr, (width, height), interpolation=cv2.INTER_AREA)
                
                # Convert back to RGB for Streamlit display
                resized_image_rgb = cv2.cvtColor(resized_image_bgr, cv2.COLOR_BGR2RGB)
                
                st.image(resized_image_rgb, caption=f"Resized to {width} x {height}", use_column_width=True)
                st.write(f"New Dimensions: {width} x {height} pixels")

                # --- 3. Download Feature ---
                is_success, im_buf_arr = cv2.imencode(".png", resized_image_bgr)
                if is_success:
                    byte_im = im_buf_arr.tobytes()
                    st.download_button(
                        label=f"Download {selected_size_label.split('(')[0].strip()}", 
                        data=byte_im,
                        file_name=f"resized_{width}x{height}.png",
                        mime="image/png"
                    )
                else:
                    st.error("Failed to encode image for download.")
                    
            except Exception as e:
                st.error(f"Error resizing image to {width}x{height}: {e}")
        st.markdown("---") 
    else:
        st.info("Please select a resize option to see results.")

st.sidebar.markdown("---")
st.sidebar.info("This app uses OpenCV for efficient image resizing.")
st.sidebar.caption("Developed by AI")
