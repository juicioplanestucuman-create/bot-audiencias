import os
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters

from utils.drive import guardar_pdf_en_drive
from utils.sheet import registrar_datos_en_sheet
from utils.calendar import crear_evento_desde_sheet
from utils.pdf_parser import extraer_datos_pdf

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"]  # Ej: https://bot1-xxxx.a.run.app/webhook

# Crear instancia de la app de Telegram
application = Application.builder().token(TELEGRAM_TOKEN).build()

# --- Handlers ---
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
        crear_evento_desde_sheet(datos_extraidos)

# Registrar handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.Document.PDF, manejar_documento))

# --- Servidor Web para Cloud Run ---
if __name__ == "__main__":
    import asyncio
    from aiohttp import web

    async def webhook_handler(request):
        data = await request.json()
        update = Update.de_json(data, application.bot)
        await application.process_update(update)
        return web.Response(text="OK")

    async def on_startup(app):
        await application.bot.set_webhook(WEBHOOK_URL)

    app = web.Application()
    app.router.add_post("/webhook", webhook_handler)
    app.on_startup.append(on_startup)

    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, port=port)
