from DB.DB import register


def registration(name, lastname, phone, mail, username, password):
    if (len(name) > 3) & (len(lastname) > 3) & (len(mail) > 3) & \
            (len(phone) > 3) & (len(username) > 1) & (len(password) > 1):
        return register(name, lastname, phone, mail, username, password)
    else:
        return "FAILED - empty field/short passwords"
