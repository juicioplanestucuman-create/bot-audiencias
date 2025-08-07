import os
import json
from telegram.ext import Application, MessageHandler, ContextTypes, CommandHandler, filters
from telegram import Update
from utils.drive import guardar_pdf_en_drive
from utils.sheet import registrar_datos_en_sheet
from utils.calendar import crear_evento_desde_sheet
from utils.pdf_parser import extraer_datos_pdf

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"]  # sin /webhook al final

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot activo. Enviame un PDF.")

async def manejar_documento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    archivo = update.message.document
    if archivo.mime_type == "application/pdf":
        archivo_file = await archivo.get_file()
        archivo_pdf = await archivo_file.download_to_drive()
        datos_extraidos = extraer_datos_pdf(archivo_pdf)
        ruta_en_drive = guardar_pdf_en_drive(archivo_pdf, archivo.file_name)
        registrar_datos_en_sheet(datos_extraidos, archivo.file_name, ruta_en_drive)
        # crear_evento_desde_sheet(datos_extraidos)  # solo si lo necesitás
        await update.message.reply_text("PDF recibido y procesado.")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.MimeType("application/pdf"), manejar_documento))

    print("Bot iniciado con webhook...")

    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        webhook_url=WEBHOOK_URL + "/webhook",
    )

if __name__ == "__main__":
    main()

