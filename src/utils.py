def phone_format(n):
    """Nicely format a number in US phone form"""
    n = str(n)
    return format(int(n[:-1]), ",").replace(",", "-") + n[-1]


def title_format(x):
    spaces = x.replace("_", " ")
    return spaces.title()
