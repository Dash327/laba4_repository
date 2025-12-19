import telebot
from .handlers import MessageHandlers


class CurrencyBot:
    def __init__(self, token: str):
        self.bot = telebot.TeleBot(token)
        self.handlers = MessageHandlers(self.bot)
        self._register_handlers()

    def _register_handlers(self):
        bot = self.bot
        bot.message_handler(commands=["start"])(self.handlers.handle_start)
        bot.message_handler(commands=["rate"])(self.handlers.handle_rate)
        bot.message_handler(commands=["archive"])(self.handlers.handle_archive)
        bot.message_handler(commands=["help"])(lambda m: self.handlers.handle_start(m))
        # Обработка текста для конвертации
        bot.message_handler(func=lambda m: m.text and " to " in m.text.lower())(
            self.handlers.handle_convert_text
        )

    def run(self):
        self.bot.infinity_polling()
