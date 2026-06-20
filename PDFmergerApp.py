import tkinter as tk
<<<<<<< HEAD
from tkinter import filedialog
from tkinter import messagebox
from PyPDF2 import PdfMerger
from PIL import Image


class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger")
        self.root.geometry("300x150")

        self.label = tk.Label(root, text="Select PDF or JPG files to merge:")
        self.label.pack(pady=10)

        self.select_button = tk.Button(root, text="Select Files", command=self.select_files)
        self.select_button.pack(pady=5)

        self.merge_button = tk.Button(root, text="Merge Files", command=self.merge_files, state=tk.DISABLED)
        self.merge_button.pack(pady=5)

=======
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger, PdfReader
from pdf2image import convert_from_path
from fpdf import FPDF
from PIL import Image

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Tool")
        self.root.geometry("350x200")

        # Title Label
        self.label = tk.Label(root, text="Select PDF or JPG files:")
        self.label.pack(pady=10)

        # Select Files Button
        self.select_button = tk.Button(root, text="Select Files", command=self.select_files)
        self.select_button.pack(pady=5)

        # Merge Files Button
        self.merge_button = tk.Button(root, text="Merge Files", command=self.merge_files, state=tk.DISABLED)
        self.merge_button.pack(pady=5)

        # Convert to HTML Button
        self.html_button = tk.Button(root, text="Convert to HTML", command=self.convert_to_html, state=tk.DISABLED)
        self.html_button.pack(pady=5)


>>>>>>> 1e3ed83 (Initial project state)
        self.files = []

    def select_files(self):
        self.files = filedialog.askopenfilenames(
<<<<<<< HEAD
            filetypes=[("PDF files", "*.pdf"), ("JPG files", "*.jpg")],
=======
            filetypes=[("PDF files", "*.pdf"), 
                       ("JPG files", "*.jpg"), 
                       ("Jpeg files", "*.jpeg"), 
                       ("Png files", "*.png"), 
                       ("BMP files", "*.bmp"), 
                       ("Tiff files", "*.tiff")],
>>>>>>> 1e3ed83 (Initial project state)
            title="Select PDF or JPG files"
        )
        if self.files:
            self.merge_button.config(state=tk.NORMAL)
<<<<<<< HEAD
=======
            self.html_button.config(state=tk.NORMAL)
>>>>>>> 1e3ed83 (Initial project state)
            messagebox.showinfo("Files Selected", f"{len(self.files)} files selected")

    def merge_files(self):
        if not self.files:
            messagebox.showwarning("No Files", "Please select PDF or JPG files to merge.")
            return

        output_file = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save Merged PDF As"
        )
        
        if not output_file:
            return
        
        merger = PdfMerger()
        try:
            for file in self.files:
<<<<<<< HEAD
                if file.lower().endswith(".jpg"):
=======
                if file.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".gif")):

>>>>>>> 1e3ed83 (Initial project state)
                    # Convert JPG to PDF
                    image = Image.open(file)
                    pdf_path = file + ".pdf"
                    image.convert("RGB").save(pdf_path)
                    merger.append(pdf_path)
                else:
                    merger.append(file)
            
            merger.write(output_file)
            merger.close()
            messagebox.showinfo("Success", f"Files merged successfully into {output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

<<<<<<< HEAD
=======
    def convert_to_html(self):
        if not self.files:
            messagebox.showwarning("No Files", "Please select a PDF file to convert to HTML.")
            return

        output_dir = filedialog.askdirectory(title="Select Directory to Save HTML")
        
        if not output_dir:
            return
        
        try:
            for file in self.files:
                if file.lower().endswith(".pdf"):
                    pages = convert_from_path(file)
                    for i, page in enumerate(pages):
                        page_path = f"{output_dir}/page_{i + 1}.jpg"
                        page.save(page_path, "JPEG")
                        
                    # Create a simple HTML file
                    with open(f"{output_dir}/output.html", "w") as html_file:
                        html_file.write("<html><body>\n")
                        for i in range(len(pages)):
                            html_file.write(f'<img src="page_{i + 1}.jpg"><br>\n')
                        html_file.write("</body></html>")
            
            messagebox.showinfo("Success", "PDF converted to HTML successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

>>>>>>> 1e3ed83 (Initial project state)
if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()
