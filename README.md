# PDFmerger
- Merges PDFs togheter and also converts jpg to pdf

![image](https://github.com/user-attachments/assets/f8a1b36c-6469-496f-97c3-df87c73f6365)

- First, click on 'Select PDFs' and select multiple pdfs you would like to merge
- Next, click 'Merge PDFs' and create a name for the new file
- thats it

# Future improvements
- add encryption (password) support
- add better GUI functionality

# When downloading for local machine

## Create Virtual Environment
```python3 -m venv myenv```

## Activate virtual environment
```source myenv/bin/activate```

## Download packages in virtual environment
```pip3 install PyPDF pillow pyinstaller```

## Create Executable (if you choose to)
```pyinstaller --onefile -w PDFmergerApp.py ```
used pyinstaller to make it executable
