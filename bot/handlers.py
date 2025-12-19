import logging
from api.currency_api import CurrencyAPI
from utils.validators import InputValidator
from utils.exceptions import ValidationError, APIError
from utils.formatters import format_currency_table, format_conversion
from user_repository import UserRepository
from bot.keaboards import Keyboards

logger = logging.getLogger(__name__)


class MessageHandlers:
    def __init__(self, bot):
        self.bot = bot
        self.api = CurrencyAPI()
        self.validator = InputValidator()
        self.user_repo = UserRepository()

    def handle_start(self, message):
        try:
            self.user_repo.create_user_if_not_exists(
                user_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
            )
            self.bot.send_message(
                message.chat.id,
                "Бот курсов валют запущен!\n\n"
                "Команды:\n"
                "/rate — актуальные курсы\n"
                "/archive — курсы за дату\n"
                "/convert — конвертер (пишите: 100 USD to RUB)\n"
                "/help — помощь",
                Keyboards.start_kb(),
            )
        except Exception as e:
            logger.error(f"Start error: {e}")
            self.bot.reply_to(message, "Ошибка при старте. Попробуйте позже.")

    def handle_rate(self, message):
        try:
            data = self.api.get_current_rates()
            text = format_currency_table(data["Valute"])
            self.bot.send_message(message.chat.id, text, parse_mode="HTML")
        except APIError as e:
            self.bot.reply_to(message, f" {e}")

    def handle_archive(self, message):
        self.bot.send_message(message.chat.id, "Введите дату (ДД.ММ.ГГГГ):")
        self.bot.register_next_step_handler(message, self._process_date)

    def _process_date(self, message):
        date = message.text.strip()
        if not self.validator.is_valid_date(date):
            self.bot.reply_to(message, "Неверный формат. Пример: 15.12.2023")
            return
        try:
            data = self.api.get_historical_rates(date)
            text = format_currency_table(data["Valute"], date)
            self.bot.send_message(message.chat.id, text, parse_mode="HTML")
        except APIError as e:
            self.bot.reply_to(message, f"{e}")

    def handle_convert_text(self, message):
        try:
            amount, from_curr, to_curr = self.validator.validate_conversion_input(
                message.text
            )
            # Получаем курсы
            rate_from = self.api.get_rate(from_curr)
            rate_to = self.api.get_rate(to_curr)
            # Переводим в рубли → в целевую валюту
            rub = amount * rate_from
            result = rub / rate_to
            text = format_conversion(
                amount, from_curr, to_curr, rate_from / rate_to, result
            )
            self.bot.reply_to(message, f"{text}")
        except (ValidationError, APIError) as e:
            self.bot.reply_to(message, f"{e}")
        except Exception as e:
            logger.error(f"Convert error: {e}")
            self.bot.reply_to(message, "Не удалось выполнить конвертацию.")
