def convert_to_text(json_data: dict) -> str:
    user_html = ""
    for field, value in json_data.items():
        user_html += f"{field.capitalize()}: {value}\n"

    return user_html


def convert_to_text_ticket(json_data: dict) -> str:
    ticket_html = ""
    for field, value in json_data.items():
        ticket_html += f"{field.capitalize()}: {value}\n"

    return ticket_html


def convert_to_text_date(json_data: dict) -> str:
    date_html = ""
    for field, value in json_data.items():
        date_html += f"{field.capitalize()}: {value}\n"

    return date_html

