from app import app
from app.bot import set_webhook_with_retry
import os

CALLURL = os.getenv('WEBHOOK_URL')

if __name__ == '__main__':
    set_webhook_with_retry(CALLURL)
    app.run(host='0.0.0.0', port=5000, debug=True)
