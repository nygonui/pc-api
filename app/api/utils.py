from datetime import datetime

import pytz


def get_current_date() -> tuple[str, str]:
    """
    Retrieves the current date and datetime, adjusted to the America/Sao_Paulo timezone.

    Returns:
        tuple[str, str]: A tuple containing two strings:
            - The current date formatted as 'YYYY-MM-DD'.
            - The current datetime formatted as 'YYYY-MM-DDTHH:MM:SS.fZ'
              in the America/Sao_Paulo timezone (note: 'Z' is appended literally
              and does not indicate UTC time).
    """
    return (
        datetime.now(pytz.timezone("America/Sao_Paulo")).strftime("%Y-%m-%d"),
        datetime.now(pytz.timezone("America/Sao_Paulo")).strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        ),
    )
