from DB.db_api import login
from BussinesLayer.Services.Logger import info


def log_in(username, password):
    val = login()
    if len(val) > 0:
        for x in val:
            if username == x[0] and password == x[1]:
                info("Successfully Login - " + username)
                return "Successfully Login"
        info('No user Found - ' + username)
        return 'No user Found'
    else:
        info('No user Found - ' + username)
        return 'No user Found'

