from datetime import date

def is_future_date(d: date) -> bool:
    """Check if a given date is in the future."""
    return d > date.today()

def normalize_string(text: str) -> str:
    """Trim and convert a string to lowercase."""
    return text.strip().lower()

def keyword_in_title(title: str, keyword: str) -> bool:
    """Check if a keyword exists in a title."""
    return keyword.lower() in title.lower()
