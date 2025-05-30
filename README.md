
# PDF-Renamer-IA  
A Python application with a graphical interface (Tkinter), developed to automatically extract metadata from PDF files using AI and OCR, and rename them based on the extracted information. The program leverages LangChain with Groq API and processes PDFs using threads for better performance.

# 📌 Features  

✅ Intuitive graphical interface (Tkinter)  

✅ Automatic metadata extraction using PDFminer and OCR (Tesseract)  

✅ Integration with Groq AI via LangChain for metadata identification  

✅ Background processing using threads for better performance  

✅ Automatic renaming of PDF files based on extracted metadata  

✅ Log file generation for all actions performed  

# ⚙️ How it works  

1. Select a folder containing PDF files.  

2. The program extracts the text from the first page using PDFminer or OCR if necessary.  

3. The extracted text is sent to the Groq AI via LangChain to identify metadata such as author, title, and ISBN.  

4. Files are automatically renamed based on the extracted metadata.  

5. All actions and errors are logged and displayed in the interface.  

# 🛠️ Technologies Used  

1. Python  

2. Tkinter  

3. PDFminer  

4. Tesseract OCR (via pytesseract)  

5. pdf2image  

6. LangChain  

7. Groq API  

8. OS  

9. Threading  

# 🚀 How to use  

1. Configure your Groq API Key in the `api_key` variable.  

2. Install dependencies:  
```bash  
pip install pdfminer.six pytesseract pdf2image langchain_groq  
```  

3. Make sure you have Tesseract installed and configured on your system.  

4. Run the script.  

5. Select the folder with PDF files and click on "Renomear Arquivos PDF".  

6. Monitor the process and logs via the application interface.  

# 📝 Notes  

- The program handles errors such as missing metadata or API token limits gracefully.  
- The renamed files avoid invalid filesystem characters by sanitizing the names.  
- Ensure that Groq API limits are sufficient for batch processing.  
