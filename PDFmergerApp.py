import tkinter as tk
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

        self.files = []

    def select_files(self):
        self.files = filedialog.askopenfilenames(
            filetypes=[("PDF files", "*.pdf"), ("JPG files", "*.jpg")],
            title="Select PDF or JPG files"
        )
        if self.files:
            self.merge_button.config(state=tk.NORMAL)
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
                if file.lower().endswith(".jpg"):
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

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()
