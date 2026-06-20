import os
import tempfile
import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from pdf2image import convert_from_path
from PIL import Image, ImageTk

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".gif")

class PDFToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Tool")
        self.root.geometry("820x450")

        self.files = []
        self.rotations = {}
        self.preview_photo = None

        self.label = tk.Label(root, text="Add PDF or image files, then preview and adjust the merge order:")
        self.label.pack(pady=10)

        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=6)

        list_frame = tk.Frame(main_frame)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.file_listbox = tk.Listbox(list_frame, height=12, exportselection=False)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.file_listbox.bind("<<ListboxSelect>>", self.on_file_select)

        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox.config(yscrollcommand=scrollbar.set)

        self.status_label = tk.Label(root, text="No files added", anchor="w")
        self.status_label.pack(fill=tk.X, padx=12)

        preview_frame = tk.Frame(main_frame, width=260)
        preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(14, 0))
        preview_frame.pack_propagate(False)

        self.preview_label = tk.Label(preview_frame, text="Preview", relief=tk.SUNKEN, bg="white")
        self.preview_label.pack(fill=tk.BOTH, expand=True)

        self.details_label = tk.Label(preview_frame, text="No file selected", anchor="w", justify=tk.LEFT)
        self.details_label.pack(fill=tk.X, pady=(6, 0))

        controls_frame = tk.Frame(root)
        controls_frame.pack(fill=tk.X, padx=12, pady=10)
        for column in range(8):
            controls_frame.columnconfigure(column, weight=1, uniform="controls")

        self.select_button = tk.Button(controls_frame, text="Add Files", command=self.select_files)
        self.select_button.grid(row=0, column=0, padx=4, pady=3, sticky="ew")

        self.clear_button = tk.Button(controls_frame, text="Clear", command=self.clear_files, state=tk.DISABLED)
        self.clear_button.grid(row=0, column=1, padx=4, pady=3, sticky="ew")

        self.up_button = tk.Button(controls_frame, text="Move Up", command=lambda: self.move_selected(-1), state=tk.DISABLED)
        self.up_button.grid(row=0, column=2, padx=4, pady=3, sticky="ew")

        self.down_button = tk.Button(controls_frame, text="Move Down", command=lambda: self.move_selected(1), state=tk.DISABLED)
        self.down_button.grid(row=0, column=3, padx=4, pady=3, sticky="ew")

        self.rotate_left_button = tk.Button(controls_frame, text="Rotate Left", command=lambda: self.rotate_selected(-90), state=tk.DISABLED)
        self.rotate_left_button.grid(row=0, column=4, padx=4, pady=3, sticky="ew")

        self.rotate_right_button = tk.Button(controls_frame, text="Rotate Right", command=lambda: self.rotate_selected(90), state=tk.DISABLED)
        self.rotate_right_button.grid(row=0, column=5, padx=4, pady=3, sticky="ew")

        self.merge_button = tk.Button(controls_frame, text="Merge Files", command=self.merge_files, state=tk.DISABLED)
        self.merge_button.grid(row=0, column=6, padx=4, pady=3, sticky="ew")

        self.html_button = tk.Button(controls_frame, text="Convert to HTML", command=self.convert_to_html, state=tk.DISABLED)
        self.html_button.grid(row=0, column=7, padx=4, pady=3, sticky="ew")

    def select_files(self):
        selected_files = filedialog.askopenfilenames(
            filetypes=[("PDF files", "*.pdf"), 
                       ("JPG files", "*.jpg"), 
                       ("Jpeg files", "*.jpeg"), 
                       ("Png files", "*.png"), 
                       ("BMP files", "*.bmp"), 
                       ("Tiff files", "*.tiff")],
            title="Add PDF or image files"
        )
        if selected_files:
            added_count = self.add_files(selected_files)
            if added_count == 0:
                self.update_status("Selected files are already in the list.")
                return

            self.refresh_file_list()
            self.set_file_action_buttons_state(tk.NORMAL)
            new_index = len(self.files) - added_count
            self.file_listbox.selection_clear(0, tk.END)
            self.file_listbox.selection_set(new_index)
            self.file_listbox.activate(new_index)
            self.show_preview(new_index)
            self.update_status(f"{added_count} files added. {len(self.files)} total files selected.")

    def add_files(self, selected_files):
        added_count = 0
        for file in selected_files:
            if file in self.files:
                continue

            self.files.append(file)
            self.rotations[file] = 0
            added_count += 1

        return added_count

    def clear_files(self):
        self.files = []
        self.rotations = {}
        self.preview_photo = None
        self.file_listbox.delete(0, tk.END)
        self.preview_label.config(image="", text="Preview")
        self.details_label.config(text="No file selected")
        self.update_status("No files added")
        self.set_file_action_buttons_state(tk.DISABLED)

    def refresh_file_list(self):
        self.file_listbox.delete(0, tk.END)
        for index, file in enumerate(self.files, start=1):
            rotation = self.rotations.get(file, 0)
            rotation_text = f" ({rotation} deg)" if rotation else ""
            self.file_listbox.insert(tk.END, f"{index}. {os.path.basename(file)}{rotation_text}")

    def update_status(self, message):
        self.status_label.config(text=message)

    def get_selected_index(self):
        selection = self.file_listbox.curselection()
        if not selection:
            return None
        return selection[0]

    def on_file_select(self, event=None):
        selected_index = self.get_selected_index()
        if selected_index is not None:
            self.show_preview(selected_index)

    def move_selected(self, direction):
        selected_index = self.get_selected_index()
        if selected_index is None:
            return

        new_index = selected_index + direction
        if new_index < 0 or new_index >= len(self.files):
            return

        self.files[selected_index], self.files[new_index] = self.files[new_index], self.files[selected_index]
        self.refresh_file_list()
        self.file_listbox.selection_set(new_index)
        self.file_listbox.activate(new_index)
        self.show_preview(new_index)

    def rotate_selected(self, degrees):
        selected_index = self.get_selected_index()
        if selected_index is None:
            return

        file = self.files[selected_index]
        self.rotations[file] = (self.rotations.get(file, 0) + degrees) % 360
        self.refresh_file_list()
        self.file_listbox.selection_set(selected_index)
        self.file_listbox.activate(selected_index)
        self.show_preview(selected_index)

    def set_file_action_buttons_state(self, state):
        self.clear_button.config(state=state)
        self.up_button.config(state=state)
        self.down_button.config(state=state)
        self.rotate_left_button.config(state=state)
        self.rotate_right_button.config(state=state)
        self.merge_button.config(state=state)
        self.html_button.config(state=state)

    def show_preview(self, index):
        file = self.files[index]
        rotation = self.rotations.get(file, 0)

        try:
            image = self.create_preview_image(file, rotation)
            image.thumbnail((240, 280))
            self.preview_photo = ImageTk.PhotoImage(image)
            self.preview_label.config(image=self.preview_photo, text="")
            self.details_label.config(text=f"{os.path.basename(file)}\nRotation: {rotation} deg")
        except Exception as e:
            self.preview_photo = None
            self.preview_label.config(image="", text="Preview unavailable")
            self.details_label.config(text=f"{os.path.basename(file)}\n{e}")

    def create_preview_image(self, file, rotation):
        if file.lower().endswith(IMAGE_EXTENSIONS):
            image = Image.open(file)
        elif file.lower().endswith(".pdf"):
            pages = convert_from_path(file, first_page=1, last_page=1, size=(500, None))
            if not pages:
                raise ValueError("PDF has no pages")
            image = pages[0]
        else:
            raise ValueError("Unsupported file type")

        if rotation:
            image = image.rotate(-rotation, expand=True)
        return image

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
            with tempfile.TemporaryDirectory() as temp_dir:
                for file in self.files:
                    rotation = self.rotations.get(file, 0)
                    if file.lower().endswith(IMAGE_EXTENSIONS):
                        pdf_path = self.image_to_temp_pdf(file, rotation, temp_dir)
                        merger.append(pdf_path)
                    elif rotation:
                        pdf_path = self.rotated_pdf_to_temp_pdf(file, rotation, temp_dir)
                        merger.append(pdf_path)
                    else:
                        merger.append(file)

                merger.write(output_file)
            merger.close()
            messagebox.showinfo("Success", f"Files merged successfully into {output_file}")
        except Exception as e:
            merger.close()
            messagebox.showerror("Error", f"An error occurred: {e}")

    def image_to_temp_pdf(self, file, rotation, temp_dir):
        image = Image.open(file)
        if rotation:
            image = image.rotate(-rotation, expand=True)

        pdf_path = os.path.join(temp_dir, f"{os.path.basename(file)}.pdf")
        image.convert("RGB").save(pdf_path)
        return pdf_path

    def rotated_pdf_to_temp_pdf(self, file, rotation, temp_dir):
        reader = PdfReader(file)
        writer = PdfWriter()

        for page in reader.pages:
            page.rotate(rotation)
            writer.add_page(page)

        pdf_path = os.path.join(temp_dir, f"{os.path.basename(file)}.rotated.pdf")
        with open(pdf_path, "wb") as output:
            writer.write(output)
        return pdf_path

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

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFToolApp(root)
    root.mainloop()
