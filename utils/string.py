def str_to_int(value, default):
    try:
        value = int(value)
    except ValueError:
        return default
    return value