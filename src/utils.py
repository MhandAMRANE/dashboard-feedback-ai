import hashlib
from datetime import datetime


def clean_text(text):
    if text is None:
        return ""
    return str(text).strip()


def generate_text_hash(text):
    cleaned = clean_text(text)
    return hashlib.sha256(cleaned.encode("utf-8")).hexdigest()


def normalize_date(date_value):
    if not date_value:
        return None

    try:
        parsed = datetime.strptime(str(date_value), "%Y-%m-%d")
        return parsed.strftime("%Y-%m-%d")
    except ValueError:
        return None