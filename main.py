import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WALLET_ADDRESS = "0xc19Bc37eb1e3757F99ac3b70f30e7A10a74e122b"
PRICE = 5

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(f"💰 Pay {PRICE} USDT", callback_data='pay')],
        [InlineKeyboardButton("✅ I Have Paid", callback_data='paid')]
    ]
    await update.message.reply_text(
        f"⚡ *TradeVolt* ⚡\n\nRent Binance Auto-Trading Bot\n\nPrice: *{PRICE} USDT = 14 Days*\n\nWallet:\n`{WALLET_ADDRESS}`\n\nNetwork: *BEP20 (BSC)*\nAsset: *USDT*\n\nSend {PRICE} USDT then click I Have Paid.",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'pay':
        await query.edit_message_text(
            f"Send *{PRICE} USDT* to this address:\n\n`{WALLET_ADDRESS}`\n\nNetwork: BEP20\n\nAfter sending, click I Have Paid.",
            parse_mode='Markdown'
        )
    
    if query.data == 'paid':
        await query.edit_message_text(
            f"✅ Thanks! Send your TX hash/screenshot to @TradeVoltBot to activate.\n\nWallet: `{WALLET_ADDRESS}`",
            parse_mode='Markdown'
        )

app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
print("TradeVolt LIVE - Trust Wallet Mode...")
app.run_polling()