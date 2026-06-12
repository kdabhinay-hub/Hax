   import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("8969746545:AAEAwkcZqxvOxfwMBI2IIF2CVz-9a0_w7gg")
CHAT_ID = os.getenv("8360668581")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Store photos with links
photos_db = {}
photo_counter = 0

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command"""
    await update.message.reply_text(
        "🎉 Welcome to Photo Share Bot!\n\n"
        "📸 Send me a photo and I'll create a shareable link\n"
        "/help - Get help\n"
        "/list - View all photos"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command"""
    await update.message.reply_text(
        "📖 How to use:\n\n"
        "1️⃣ Send any photo\n"
        "2️⃣ Bot will generate a unique link\n"
        "3️⃣ Share the link with anyone\n"
        "4️⃣ Anyone can view the photo from the link\n\n"
        "Commands:\n"
        "/start - Start bot\n"
        "/list - View all photos\n"
        "/delete <photo_id> - Delete a photo"
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle photo uploads"""
    global photo_counter
    
    photo = update.message.photo[-1]  # Get highest resolution
    file_id = photo.file_id
    
    photo_counter += 1
    photo_id = f"photo_{photo_counter}"
    
    # Store photo info
    photos_db[photo_id] = {
        "file_id": file_id,
        "user_id": update.effective_user.id,
        "username": update.effective_user.username or "Anonymous"
    }
    
    # Generate link
    link = f"https://t.me/share/url?url=photo_{photo_counter}"
    
    # Send confirmation
    await update.message.reply_text(
        f"✅ Photo uploaded successfully!\n\n"
        f"📎 Photo ID: `{photo_id}`\n"
        f"🔗 Share Link:\n`{link}`\n\n"
        f"Anyone can access this photo using the link!"
    )
    
    logger.info(f"Photo uploaded: {photo_id} by {update.effective_user.username}")

async def list_photos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all uploaded photos"""
    if not photos_db:
        await update.message.reply_text("📷 No photos uploaded yet!")
        return
    
    message = "📸 Your Photos:\n\n"
    for photo_id, info in photos_db.items():
        message += f"• {photo_id} - by @{info['username']}\n"
    
    await update.message.reply_text(message)

async def delete_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete a photo"""
    if not context.args:
        await update.message.reply_text("Usage: /delete <photo_id>")
        return
    
    photo_id = context.args[0]
    
    if photo_id in photos_db:
        del photos_db[photo_id]
        await update.message.reply_text(f"🗑️ Photo {photo_id} deleted!")
    else:
        await update.message.reply_text("❌ Photo not found!")

def main():
    """Start the bot"""
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN not found in .env file!")
        return
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("list", list_photos))
    app.add_handler(CommandHandler("delete", delete_photo))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    logger.info("🤖 Bot started successfully!")
    app.run_polling()

if __name__ == "__main__":
    main()
