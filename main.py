from telegram.ext import Updater, MessageHandler, Filters
from utils.drive import guardar_pdf_en_drive
from utils.sheet import registrar_datos_en_sheet
from utils.calendar import crear_evento_desde_sheet
from utils.pdf_parser import extraer_datos_pdf

import os

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]

def manejar_documento(update, context):
    archivo = update.message.document
    if archivo.mime_type == "application/pdf":
        archivo_pdf = archivo.get_file().download()
        datos_extraidos = extraer_datos_pdf(archivo_pdf)
        ruta_en_drive = guardar_pdf_en_drive(archivo_pdf, archivo.file_name)
        registrar_datos_en_sheet(datos_extraidos, archivo.file_name, ruta_en_drive)

def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    handler = MessageHandler(Filters.document.mime_type("application/pdf"), manejar_documento)
    dispatcher.add_handler(handler)

    print("Bot iniciado. Esperando PDFs...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
