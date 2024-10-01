
import fitz  # PyMuPDF
import time
import threading
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog

class PDFSlideshowApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Slideshow")
        
        # Set initial window size
        self.root.geometry("800x600")
        self.label = tk.Label(root)
        self.label.pack(fill=tk.BOTH, expand=True)

        self.pdf_document = None
        self.current_page = 0
        self.total_pages = 0
        self.is_playing = False
        self.delay = 8  # Seconds between slides

        # Buttons
        open_button = tk.Button(root, text="Open PDF", command=self.open_pdf)
        open_button.pack(side=tk.LEFT)
        
        start_button = tk.Button(root, text="Start Slideshow", command=self.start_slideshow)
        start_button.pack(side=tk.LEFT)
        
        stop_button = tk.Button(root, text="Stop Slideshow", command=self.stop_slideshow)
        stop_button.pack(side=tk.LEFT)

    def open_pdf(self):
        # Open a file dialog to choose a PDF
        pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if pdf_path:
            self.pdf_document = fitz.open(pdf_path)
            self.total_pages = len(self.pdf_document)
            self.current_page = 0
            self.show_page(self.current_page)

    def show_page(self, page_num):
        if self.pdf_document is not None:
            page = self.pdf_document.load_page(page_num)
            pix = page.get_pixmap()

            # Get screen size
            screen_width = self.root.winfo_width()
            screen_height = self.root.winfo_height()

            # Get original PDF size
            img_width = pix.width
            img_height = pix.height

            # Check if resizing is needed based on screen size, maintain aspect ratio
            if img_width > screen_width or img_height > screen_height:
                ratio = min(screen_width / img_width, screen_height / img_height)
                img_width = int(img_width * ratio)
                img_height = int(img_height * ratio)

            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img = img.resize((img_width, img_height), Image.LANCZOS)  # Maintain aspect ratio
            img_tk = ImageTk.PhotoImage(img)
            
            self.label.config(image=img_tk)
            self.label.image = img_tk  # Prevent garbage collection

    def start_slideshow(self):
        if not self.is_playing and self.pdf_document is not None:
            self.is_playing = True
            threading.Thread(target=self.slideshow).start()

    def slideshow(self):
        while self.is_playing and self.pdf_document is not None:
            self.show_page(self.current_page)
            self.current_page = (self.current_page + 1) % self.total_pages
            time.sleep(self.delay)

    def stop_slideshow(self):
        self.is_playing = False

# Create the root window and start the app
root = tk.Tk()
app = PDFSlideshowApp(root)
root.mainloop()
