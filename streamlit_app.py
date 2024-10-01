import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
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

        # Autorefresh after the specified delay
        st_autorefresh = st.experimental_autorefresh(interval=delay * 1000, key="autorefresh")

        # Simulate autoplay by using Streamlit's session state to keep track of the current slide
        if 'current_slide' not in st.session_state:
            st.session_state.current_slide = 0

        # Display the current slide
        st.image(slides[st.session_state.current_slide], use_column_width=True)

        # Update the slide index and loop back to the start if necessary
        st.session_state.current_slide = (st.session_state.current_slide + 1) % len(slides)

    else:
        st.error("No valid pages found in the uploaded PDF.")
else:
    st.info("Please upload a PDF file to start the slideshow.")
