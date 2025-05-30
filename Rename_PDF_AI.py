import os
import tkinter as tk
from dotenv import load_dotenv
from tkinter import filedialog, messagebox, ttk
from threading import Thread
from pdfminer.high_level import extract_text
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from pdf2image import convert_from_path
import pytesseract

load_dotenv()

api_key = os.getenv('GROQ_API_KEY')
chat = ChatGroq(model='llama-3.3-70b-versatile')


parar_execucao = False
def answer_ia(texto):
    prompt = (
        "A seguir está a primeira página de um documento PDF. Tente identificar:\n"
        "- Se for um livro: autor, título da obra, ISBN.\n"
        "- Se for um jornal ou revista: título da publicação e data.\n"
        "Retorne no seguinte formato: Tipo - Título - Data ou ISBN.\n"
        "Se não encontrar algum dado, use 'Desconhecido'.\n\n"
        f"{texto}"
    )
    messages = [("user", prompt)]
    message_system = "Você é um bibliotecário especialista em identificar metadados de documentos PDF."
    template = ChatPromptTemplate.from_messages([("system", message_system)] + messages)
    chain = template | chat
    return chain.invoke({}).content.strip()

def extract_first_page_text(file_path):
    #PDFminer
    try:
        text = extract_text(file_path, page_numbers=[0])
        if text and len(text.strip()) > 0:
            log(f"Texto extraído com pdfminer de {file_path}", "info")
            return text.strip()
    except Exception as e:
        log(f"Erro no extract_text: {e}", "error")
    
    #OCR
    try:
        log(f"Tentando OCR para {file_path}", "info")
        images = convert_from_path(file_path, first_page=1, last_page=1)
        if images:
            ocr_text = pytesseract.image_to_string(images[0], lang='por')  # Ajuste 'lang' conforme necessário
            if ocr_text and len(ocr_text.strip()) > 0:
                log(f"Texto extraído com OCR de {file_path}", "info")
                return ocr_text.strip()
    except Exception as e:
        log(f"Erro no OCR de {file_path}: {e}", "error")

    log(f"Não foi possível extrair texto de {file_path}", "error")
    return ""


def rename_pdf_with_ia(file_path):
    global parar_execucao
    text = extract_first_page_text(file_path)
    if not text:
        log(f"Sem texto extraído de {file_path}. Pulando renomeação.", "error")
        return file_path
    try:
        novo_nome_base = answer_ia(text)
        novo_nome = novo_nome_base.replace('/', '-').replace('\\', '-').replace(':', '-') + ".pdf"
        pasta = os.path.dirname(file_path)
        novo_caminho = os.path.join(pasta, novo_nome)
        if not os.path.exists(novo_caminho):
            os.rename(file_path, novo_caminho)
            log(f"Arquivo renomeado: {file_path} -> {novo_nome}", "renomeado")
            return novo_caminho
        else:
            log(f"Arquivo {novo_nome} já existe. Pulando renomeação.", "info")
    except Exception as e:
        log(f"Erro ao renomear {file_path}: {e}", "error")
        if "token" in str(e).lower() or "context length" in str(e).lower():
            log("Erro crítico de tokens. Parando execução.", "error")
            messagebox.showerror("Erro crítico", "Erro de tokens insuficientes ou excesso de contexto. A execução será interrompida.")
            parar_execucao = True
    return file_path


def rename_pdf():
    folder_path = folder_entry.get()
    if not folder_path or not os.path.isdir(folder_path):
        messagebox.showerror("Erro", "Por favor, selecione uma pasta válida.")
        return
    result_text.delete(1.0, tk.END)
    Thread(target=process_rename_pdfs, args=(folder_path,), daemon=True).start()

def process_rename_pdfs(folder_path):
    global parar_execucao
    for root, _, files in os.walk(folder_path):
        for filename in files:
            if parar_execucao:
                log("Execução interrompida devido a erro crítico.", "error")
                return
            if filename.lower().endswith(".pdf"):
                file_path = os.path.join(root, filename)
                rename_pdf_with_ia(file_path)

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_path)

def log(message, tag):
    result_text.insert(tk.END, f"{message}\n", tag)
    result_text.see(tk.END)
    with open("scan_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"{message}\n")

root = tk.Tk()
root.title("Renomeador de PDFs com IA e OCR")
root.geometry("700x400")

folder_label = tk.Label(root, text="Selecione a pasta para renomear PDFs:")
folder_label.pack(pady=10)

folder_entry = tk.Entry(root, width=60)
folder_entry.pack(pady=5)

folder_button = tk.Button(root, text="Procurar", command=select_folder)
folder_button.pack(pady=5)

rename_button = tk.Button(root, text="Renomear Arquivos PDF", command=rename_pdf)
rename_button.pack(pady=10)

result_text = tk.Text(root, wrap=tk.WORD, height=15)
result_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

result_text.tag_config("error", foreground="red")
result_text.tag_config("renomeado", foreground="purple")
result_text.tag_config("info", foreground="blue")

scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=result_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
result_text.config(yscrollcommand=scrollbar.set)

root.mainloop()
