def dt(d: dict) -> tuple:
    """Converts a dictionary to a tuple of tuples (key, value)."""
    return tuple((key, value) for key, value in d.items())

def td(t: tuple) -> dict:
    """Converts a tuple of tuples (key, value) to a dictionary."""
    return {key: value for key, value in t}