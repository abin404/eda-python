def check_if_element_is_available(e):
    if e:
        return e.text.strip()
    else:
        return None