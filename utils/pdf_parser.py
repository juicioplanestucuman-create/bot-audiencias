import fitz  # PyMuPDF
import re

def extraer_datos_pdf(ruta_pdf):
    doc = fitz.open(ruta_pdf)
    texto = ""
    for pagina in doc:
        texto += pagina.get_text()

    expediente = re.search(r'Expediente\s*[:\-]?\s*(\S+)', texto, re.IGNORECASE)
    caratula = re.search(r'Caratul[ao]\s*[:\-]?\s*(.+)', texto, re.IGNORECASE)
    fecha = re.search(r'(\d{1,2}/\d{1,2}/\d{4})', texto)
    hora = re.search(r'(\d{1,2}:\d{2})', texto)
    plazo = re.search(r'en\s+(\d+)\s+d[ií]as', texto, re.IGNORECASE)

    descripcion = " ".join(texto.strip().split())[:250]

    datos = {
        "expediente": expediente.group(1) if expediente else "",
        "caratula": caratula.group(1).strip() if caratula else "",
        "descripcion": descripcion,
        "fecha": fecha.group(1) if fecha else "",
        "hora": hora.group(1) if hora else "",
        "plazo": plazo.group(1) if plazo else "",
    }

    return datos
