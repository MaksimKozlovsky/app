def convert_to_text(json_data: dict) -> str:
    user_html = ""
    for field, value in json_data.items():
        user_html += f"{field.capitalize()}: {value}\n"

    return user_html
