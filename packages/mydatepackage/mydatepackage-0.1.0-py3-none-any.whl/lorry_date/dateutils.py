from datetime import datetime

def get_current_date():
    """Return the current date as a string."""
    return datetime.now().strftime("%Y-%m-%d")

def add_days_to_date(date_str, days):
    """Add days to a given date."""
    date_format = "%Y-%m-%d"
    date = datetime.strptime(date_str, date_format)
    new_date = date + timedelta(days=days)
    return new_date.strftime(date_format)