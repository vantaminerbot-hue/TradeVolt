import os
import threading
from flask import Flask, send_from_directory
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TELEGRAM_TOKEN = os.getenv("8648926628:AAF3LxPjGNxGor-NVQriwDsbWaOYvMTjLHw")
WALLET_ADDRESS = "0xc19Bc37eb1e3757F99ac3b70f30e7A10a74e122b"
PRICE = 5
BOT_USERNAME = "Trade_Volt_Bot"  # YOUR CORRECT BOT

web = Flask(__name__)

@web.route('/')
def home():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'index.html')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(f"💰 Pay {PRICE} USDT", callback_data='pay')],
        [InlineKeyboardButton("✅ I Have Paid - Activate", url=f"https://t.me/{BOT_USERNAME}")]
    ]
    await update.message.reply_text(
        f"🚀 TradeVolt - Rent Binance Auto-Trading Bot\n\nPrice: {PRICE} USDT = 14 Days\nWallet: {WALLET_ADDRESS}\nNetwork: BEP20\n\nClick Pay to see wallet, then click I Have Paid after payment.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'pay':
        keyboard = [
            [InlineKeyboardButton("✅ I Have Paid - Activate", url=f"https://t.me/{BOT_USERNAME}")]
        ]
        await query.edit_message_text(
            f"Send {PRICE} USDT to:\n\n{WALLET_ADDRESS}\n\nNetwork: BEP20\n\nAfter paying, click below to activate.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

def run_bot():
    if not TELEGRAM_TOKEN:
        print("No TELEGRAM_TOKEN set - bot thread skipped")
        return
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    print("TradeVolt LIVE")
    app.run_polling()

threading.Thread(target=run_bot, daemon=True).start()

if __name__ == '__main__':
    web.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))