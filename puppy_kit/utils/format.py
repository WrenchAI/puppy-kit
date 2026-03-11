"""Output formatting utilities for compact display."""


def truncate(s: str | None, max_len: int = 80) -> str:
    """Truncate string to max_len, adding ellipsis if truncated."""
    if not s:
        return ""
    s = str(s)
    if len(s) > max_len:
        return s[:max_len] + "…"
    return s


def fmt_tags(tags: list[str] | None, max_show: int = 3) -> str:
    """Format tag list, showing first max_show tags + count if more exist."""
    if not tags:
        return ""
    shown = tags[:max_show]
    rest = len(tags) - max_show
    result = ", ".join(shown)
    if rest > 0:
        return f"{result} +{rest} more"
    return result


def json_list_response(
    data: list, hint: str = "Use --verbose for full fields. Use --limit to control result size."
) -> dict:
    """Wrap list data in envelope with metadata and hint."""
    return {"data": data, "count": len(data), "hint": hint}
