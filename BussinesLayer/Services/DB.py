import sqlite3
from BussinesLayer.Services.Logger import info, error


def connect():
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    return cursor, conn


def add_new_video(username, video_id, path_video):
    try:
        cursor, conn = connect()
        cursor.execute(""" INSERT INTO members_video_insights 
                            (
                            userName,
                            video_id,
                            path_json_info
                            )
    
                        VALUES 
                        (?,?,?)
                        """, (username, video_id, path_video))
        conn.commit()
        cursor.close()
        conn.close()
        info("Success add new video - " + username + ", video_id - " + video_id)
        return 'success'
    except Exception as e:
        print(e)


def login():
    cursor, conn = connect()
    cursor.execute("SELECT username,password FROM Members")
    res = cursor.fetchall()
    return res


def register(txt_firstname_v, txt_lastname_v, txt_phone_v, txt_emailid_v, txt_username_v, txt_password_v):
    try:
        cursor, conn = connect()
        cursor.execute("""
                               CREATE TABLE IF NOT EXISTS Members 
                                (
                                fname TEXT, 
                                lname TEXT, 
                                Phone TEXT, 
                                email TEXT,
                                username TEXT NOT NULL, 
                                password TEXT NOT NULL,
                                PRIMARY KEY(username,password)
                                )""")
        cursor.execute("SELECT username FROM Members")
        val = cursor.fetchall()
        found = 0
        if len(val) > 0:
            for x in val:
                if txt_username_v == x[0]:
                    found = 1
        if found == 0:
            cursor.execute(""" INSERT INTO Members 
                    (fname,
                    lname,
                    Phone,
                    email,
                    username, 
                    password)
    
                VALUES 
                (?,?,?,?,?,?)
                """, (txt_firstname_v, txt_lastname_v, txt_phone_v, txt_emailid_v, txt_username_v, txt_password_v))

            conn.commit()
            cursor.close()
            conn.close()
            info("Successfully Registration - " + txt_username_v)
            return "Successfully Registration"
        else:
            info("Failed Registration: duplicate username - " + txt_username_v)
            return "username has exist"
    except Exception as e:
        print(e)
        error(" " + e)
        return "Cannot add to Database"

