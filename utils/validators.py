import re
from datetime import datetime
from .exceptions import ValidationError


class InputValidator:
    @staticmethod
    def is_valid_date(date_str: str) -> bool:
        """Проверка даты ДД.ММ.ГГГГ и корректности календаря"""
        if not re.fullmatch(r"\d{2}\.\d{2}\.\d{4}", date_str):
            return False
        try:
            day, month, year = map(int, date_str.split("."))
            datetime(year, month, day)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_currency_code(code: str) -> bool:
        return bool(re.fullmatch(r"[A-Z]{3}", code))

    @staticmethod
    def validate_conversion_input(text: str):
        match = re.fullmatch(
            r"(\d+(?:\.\d+)?)\s+([A-Z]{3})\s+to\s+([A-Z]{3})",
            text.strip(),
            re.IGNORECASE,
        )
        if not match:
            raise ValidationError("Формат: '100 USD to RUB'")
        amount = float(match.group(1))
        from_curr = match.group(2).upper()
        to_curr = match.group(3).upper()
        return amount, from_curr, to_curr
