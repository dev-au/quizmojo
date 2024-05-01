def error_docs(*errors):
    error_information = ''
    for arg in errors:
        error_information += f'<a href="./errors#{arg.__name__}" target="_blank">{arg.__name__}</a>, '

    def decorator(func):
        func.__doc__ = f"""Exceptions:\n    {error_information}"""

    return decorator
