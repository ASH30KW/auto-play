import streamlit as st
import fitz  # PyMuPDF
import time
from PIL import Image

# Set the title of the Streamlit app
st.title("Autoplay PDF Slideshow")

# Define the PDF file path
pdf_path = 'slides.pdf'

# Open the PDF file
pdf_document = fitz.open(pdf_path)

# Extract pages as images
slides = []
for page_num in range(len(pdf_document)):
    page = pdf_document.load_page(page_num)  # Get page
    pix = page.get_pixmap()  # Render page to an image
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)  # Convert to PIL image
    slides.append(img)

# Ensure the PDF has slides
if not slides:
    st.error("No valid PDF slides found!")
else:
    # Set a delay in seconds between images (adjust as needed)
    delay = 2

    # Simulate autoplay by using Streamlit's session state to keep track of the current slide
    if 'current_slide' not in st.session_state:
        st.session_state.current_slide = 0

    # Display the current slide
    st.image(slides[st.session_state.current_slide], use_column_width=True)

    # Move to the next slide after a delay
    time.sleep(delay)

    # Update the slide index and loop back to the start if necessary
    st.session_state.current_slide = (st.session_state.current_slide + 1) % len(slides)

    # Rerun the app to create the autoplay effect
    st.experimental_rerun()
