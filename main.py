import os
import logging
from dotenv import load_dotenv
from bot.bot import CurrencyBot


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Загрузка токена
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("Переменная TELEGRAM_BOT_TOKEN не задана в token.env")

if __name__ == "__main__":
    print("Запуск бота...")
    bot = CurrencyBot(TOKEN)
    bot.run()
