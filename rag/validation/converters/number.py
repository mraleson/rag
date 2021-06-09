def number(v, accept=None, reject=None):
    try:
        return int(v)
    except ValueError:
        return float(v)
