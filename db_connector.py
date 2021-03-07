"""
Date: 2019. 10. 10
Programmer: MH
Description: code for DB schema connector
"""

import pymysql.cursors

conn = None

def connect_to_db():
    try:
        conn = pymysql.connect(host='203.253.23.46', user='root', password='root', db='bokas',
                                    charset='utf8', autocommit=True, cursorclass=pymysql.cursors.DictCursor)
        return True
    except Exception as e:
        return False


def disconnect_from_db():
    conn.close()

if __name__ == '__main__':
    print(connect_to_db())