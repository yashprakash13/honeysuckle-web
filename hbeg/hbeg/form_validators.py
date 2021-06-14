import re

def check_password_size(val):
    """to check size of password
    """
    if len(val) < 6:
        return False
    return True

def check_nickname_size(val):
    """to check size of nickname
    """
    if len(val) < 6:
        return False
    return True

def check_any_name_characters(val):
    """only valid alphanumeric characters + space + underscores
    """
    if not re.match(r'^[A-Za-z0-9_ ]+$', val):
        return False
    return True





