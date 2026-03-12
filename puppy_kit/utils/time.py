"""Time parsing utilities."""

from datetime import datetime, timedelta
import re


def parse_time_input(s: str) -> datetime:
    """Parse relative (1h, 24h, 7d) or ISO 8601 time strings to datetime.

    Supported formats:
    - "now" → current time
    - "1h", "24h", "7d" → relative time in past
    - "1w" → 1 week ago
    - "30m" → 30 minutes ago
    - "2026-03-10T10:00:00Z" (ISO 8601 with Z)
    - "2026-03-10T10:00:00" (ISO 8601)
    - "2026-03-10" (date only)

    Returns:
        datetime object (naive, in local time)
    """
    now = datetime.now()

    if s == "now":
        return now

    # Match patterns like "1h", "24h", "7d", "1w", "30m"
    match = re.fullmatch(r"(\d+)([hdwm])", s.lower())
    if match:
        value = int(match.group(1))
        unit = match.group(2)
        delta = {
            "h": timedelta(hours=value),
            "d": timedelta(days=value),
            "w": timedelta(weeks=value),
            "m": timedelta(minutes=value),
        }[unit]
        return now - delta

    # Try ISO 8601 formats
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue

    raise ValueError(
        f"Cannot parse time: {s!r}. Use formats like '1h', '24h', '7d', "
        "'1w', '30m', or '2026-03-10T00:00:00Z'"
    )


def parse_time_range(from_str: str, to_str: str = "now") -> tuple[int, int]:
    """Parse time range strings to Unix timestamps.

    Supported formats:
    - "now"
    - "1h" (1 hour ago)
    - "24h" (24 hours ago)
    - "7d" (7 days ago)
    - "2026-02-10T10:00:00" (ISO datetime)

    Returns:
        Tuple of (from_timestamp, to_timestamp)
    """
    now = datetime.now()

    def parse_relative(s: str) -> datetime:
        if s == "now":
            return now

        # Match patterns like "1h", "24h", "7d", "30m"
        match = re.match(r"^(\d+)([hdm])$", s)
        if match:
            value = int(match.group(1))
            unit = match.group(2)

            if unit == "h":
                return now - timedelta(hours=value)
            elif unit == "d":
                return now - timedelta(days=value)
            elif unit == "m":
                return now - timedelta(minutes=value)

        # Try parsing as ISO datetime
        try:
            return datetime.fromisoformat(s)
        except ValueError:
            raise ValueError(f"Invalid time format: {s}")

    from_dt = parse_relative(from_str)
    to_dt = parse_relative(to_str)

    return int(from_dt.timestamp()), int(to_dt.timestamp())
