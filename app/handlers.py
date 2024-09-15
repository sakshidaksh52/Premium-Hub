import time
import uuid
from telebot import types, apihelper
from app.db import users_collection, file_storage_collection
from app import bot

# Utility functions for MongoDB interaction
def save_user(chat_id):
    users_collection.update_one(
        {'chat_id': chat_id},
        {'$set': {'chat_id': chat_id}},
        upsert=True
    )

def save_file_storage(unique_id, file_info):
    file_storage_collection.update_one(
        {'unique_id': unique_id},
        {'$set': {'file_id': file_info[0], 'file_type': file_info[1]}},
        upsert=True
    )

def load_file_storage(unique_id):
    return file_storage_collection.find_one({'unique_id': unique_id})

# Handle /start command
@bot.message_handler(commands=['start'])
def handle_start(message):
    save_user(message.chat.id)
    args = message.text.split()
    if len(args) > 1:
        unique_id = args[1]
        send_file_by_id(message, unique_id)
    else:
        send_welcome_message(message)

def send_welcome_message(message):
    user_name = message.from_user.first_name or message.from_user.username
    greeting_text = f"Hello, *{user_name}*! 😉\n\nWelcome to the bot."
    bot.send_message(message.chat.id, greeting_text, parse_mode="Markdown")

# Send file by ID
def send_file_by_id(message, unique_id):
    file_info = load_file_storage(unique_id)
    if file_info:
        send_file(message.chat.id, file_info['file_id'], file_info['file_type'])
    else:
        bot.send_message(message.chat.id, "File not found.")

def send_file(chat_id, file_id, file_type):
    if file_type == 'photo':
        bot.send_photo(chat_id, file_id)
    elif file_type == 'video':
        bot.send_video(chat_id, file_id)
    elif file_type == 'document':
        bot.send_document(chat_id, file_id)
    elif file_type == 'audio':
        bot.send_audio(chat_id, file_id)
    elif file_type == 'voice':
        bot.send_voice(chat_id, file_id)
    else:
        bot.send_message(chat_id, "Unsupported file type")
