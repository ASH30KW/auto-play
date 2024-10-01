import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
from streamlit_autorefresh import st_autorefresh

# Set the title of the Streamlit app
st.title("Autoplay PDF Slideshow")

# Add file uploader to allow PDF upload
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

# Automatically refresh the app every 2 seconds
autorefresh_interval = 5000  # Time in milliseconds (2000ms = 2 seconds)
st_autorefresh(interval=autorefresh_interval)

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
        # Initialize session state for the current slide index if not set
        if 'current_slide' not in st.session_state:
            st.session_state.current_slide = 0

        # Display the current slide
        st.image(slides[st.session_state.current_slide], use_column_width=True)

        # Auto-advance the slide index every refresh
        st.session_state.current_slide = (st.session_state.current_slide + 1) % len(slides)
    else:
        st.error("No valid pages found in the uploaded PDF.")
else:
    st.info("Please upload a PDF file to start the slideshow.")
