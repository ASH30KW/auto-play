import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import time

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
        delay = 2  # Delay in seconds

        # Initialize session state for the current slide index if not set
        if 'current_slide' not in st.session_state:
            st.session_state.current_slide = 0

        # Display the current slide
        st.image(slides[st.session_state.current_slide], use_column_width=True)

        # Create a button to manually go to the next slide if desired
        if st.button("Next Slide"):
            st.session_state.current_slide = (st.session_state.current_slide + 1) % len(slides)
        
        # Auto-advance the slide after the delay
        time.sleep(delay)
        st.session_state.current_slide = (st.session_state.current_slide + 1) % len(slides)
        
        # Trigger rerun using st.experimental_set_query_params to update URL and force rerun
        st.experimental_set_query_params(current_slide=st.session_state.current_slide)
    else:
        st.error("No valid pages found in the uploaded PDF.")
else:
    st.info("Please upload a PDF file to start the slideshow.")
