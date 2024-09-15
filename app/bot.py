from app import app, bot
from flask import request, abort
from telebot.types import Update

@app.route('/', methods=['GET', 'POST'])
def receive_updates():
    if request.method == 'GET':
        return 'OK', 200  # Return 'OK' for GET requests (e.g., health checks)
    elif request.method == 'POST':
        if request.headers.get('content-type') == 'application/json':
            json_string = request.get_data(as_text=True)
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return '', 200  # Always return a response for POST requests
        else:
            abort(403)


# Set webhook with retries
def set_webhook_with_retry(url, max_retries=5, backoff_factor=2):
    for attempt in range(max_retries):
        try:
            bot.set_webhook(url=url, drop_pending_updates=False)
            break
        except apihelper.ApiTelegramException as e:
            if e.error_code == 429:
                retry_after = e.result_json['parameters']['retry_after']
                time.sleep(retry_after)
            else:
                time.sleep(backoff_factor ** attempt)
        else:
            print("Max retries reached. Exiting.")
            exit(1)
