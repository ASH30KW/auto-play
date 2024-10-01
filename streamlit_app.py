import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import time
import io

# Set the title of the Streamlit app
st.title("Autoplay PDF Slideshow")

# Add file uploader to allow PDF upload
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

# Check if a file has been uploaded
if uploaded_file is not None:
    # Load the PDF file
    pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    # Extract pages as images
    slides = []
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)  # Get page
        pix = page.get_pixmap()  # Render page to an image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)  # Convert to PIL image
        slides.append(img)

    # Ensure the PDF has slides
    if slides:
        # Set a delay in seconds between images (adjust as needed)
        delay = 2

        # Simulate autoplay by using Streamlit's session state to keep track of the current slide
        if 'current_slide' not in st.session_state:
            st.session_state.current_slide = 0
            st.session_state.start_time = time.time()

        # Check if enough time has passed to switch slides
        if time.time() - st.session_state.start_time > delay:
            st.session_state.current_slide = (st.session_state.current_slide + 1) % len(slides)
            st.session_state.start_time = time.time()  # Reset the start time for the next slide

        # Display the current slide
        st.image(slides[st.session_state.current_slide], use_column_width=True)

        # Rerun the app after a short period to continue the slideshow
        st.experimental_rerun()
    else:
        st.error("No valid pages found in the uploaded PDF.")
else:
    st.info("Please upload a PDF file to start the slideshow.")
