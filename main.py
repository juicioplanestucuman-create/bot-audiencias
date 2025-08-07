import os
from telegram.ext import Application, MessageHandler, ContextTypes, CommandHandler, filters
from telegram import Update
from utils.drive import guardar_pdf_en_drive
from utils.sheet import registrar_datos_en_sheet
from utils.calendar import crear_evento_desde_sheet
from utils.pdf_parser import extraer_datos_pdf

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"]  # Ej: https://bot-cloud-abc123.a.run.app/webhook

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot activo. Enviame un PDF.")

async def manejar_documento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    archivo = update.message.document
    if archivo.mime_type == "application/pdf":
        archivo_file = await archivo.get_file()
        archivo_pdf = await archivo_file.download_to_drive()
        datos_extraidos = extraer_datos_pdf(archivo_pdf)
        ruta_en_drive = guardar_pdf_en_drive(archivo_pdf, archivo.file_name)

