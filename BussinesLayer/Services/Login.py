from DB.DB import login


def log_in(username, password):
    try:
        val = login(username, password)
        if len(val) > 0:
            for x in val:
                if username == x[0] and password == x[1]:
                    return "Successfully Login"
                    found = 1
                else:
                    pass
            if found == 0:
                return 'No user Found'
        else:
            return 'No user Found'
    except:
        return 'No user Found'
