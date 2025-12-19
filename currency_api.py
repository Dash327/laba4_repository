import requests
import json
from typing import Dict, Optional
from .config import CBR_CURRENT_URL, CBR_ARCHIVE_URL
from utils.exceptions import APIError


class CurrencyAPI:
    def get_current_rates(self) -> Dict:
        try:
            res = requests.get(CBR_CURRENT_URL, timeout=10)
            res.raise_for_status()
            return res.json()
        except requests.RequestException as e:
            raise APIError(f"Не удалось получить курсы: {e}")
        except json.JSONDecodeError as e:
            raise APIError(f"Ошибка парсинга ответа: {e}")

    def get_historical_rates(self, date_str: str) -> Dict:
        try:
            d, m, y = date_str.split(".")
            url = CBR_ARCHIVE_URL.format(year=y, month=m, day=d)
            res = requests.get(url, timeout=10)
            if res.status_code == 404:
                raise APIError("Данные за эту дату отсутствуют")
            res.raise_for_status()
            return res.json()
        except ValueError:
            raise APIError("Неверный формат даты")
        except requests.RequestException as e:
            raise APIError(f"Ошибка API: {e}")

    def get_rate(self, currency: str, date: Optional[str] = None) -> float:
        data = self.get_historical_rates(date) if date else self.get_current_rates()
        valute = data.get("Valute", {})
        if currency not in valute:
            raise APIError(f"Валюта {currency} не найдена")
        return valute[currency]["Value"]
