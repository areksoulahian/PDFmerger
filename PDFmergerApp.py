import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PyPDF2 import PdfMerger

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger")
        self.root.geometry("300x150")

        self.label = tk.Label(root, text="Select PDF files to merge:")
        self.label.pack(pady=10)

        self.select_button = tk.Button(root, text="Select PDFs", command=self.select_files)
        self.select_button.pack(pady=5)

        self.merge_button = tk.Button(root, text="Merge PDFs", command=self.merge_pdfs, state=tk.DISABLED)
        self.merge_button.pack(pady=5)

        self.files = []

    def select_files(self):
        self.files = filedialog.askopenfilenames(
            filetypes=[("PDF files", "*.pdf")],
            title="Select PDF files"
        )
        if self.files:
            self.merge_button.config(state=tk.NORMAL)
            messagebox.showinfo("Files Selected", f"{len(self.files)} files selected")

    def merge_pdfs(self):
        if not self.files:
            messagebox.showwarning("No Files", "Please select PDF files to merge.")
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
            for pdf in self.files:
                merger.append(pdf)
            merger.write(output_file)
            merger.close()
            messagebox.showinfo("Success", f"PDFs merged successfully into {output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()
