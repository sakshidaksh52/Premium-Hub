import os
from flask import Flask
from telebot import TeleBot

app = Flask(__name__)

TOKEN = os.getenv('TOKEN')
bot = TeleBot(TOKEN)

# Other configurations like MongoDB can be initialized here if needed
