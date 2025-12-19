def format_currency_table(valutes: dict, date: str = None) -> str:
    title = f"Курсы валют {'на ' + date if date else 'на сегодня'}:\n\n"
    lines = [title]
    for char_code, info in valutes.items():
        lines.append(f"<b>{char_code}</b>: {info['Value']:.4f} ₽")
    return "\n".join(lines)


def format_conversion(amount, from_curr, to_curr, rate, result) -> str:
    return f"{amount} {from_curr} = {result:.2f} {to_curr} (курс: {rate:.4f})"
