import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)

# config
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT"))


@server.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if not auth:
        return 'Missing credentials in auth', 401

    # check db for username and password
    cur = mysql.connection.cursor()
    sql = f"SELECT email, password FROM user WHERE email='{auth.username}'"
    result = cur.execute(sql)

    if result > 0:
        user_row = cur.fetchone()
        email, password = user_row[0], user_row[1]

        if auth.username != email or auth.password != password:
            return "Invalid credentials", 401
        else:
            return create_jwt(auth.username, os.environ.get('JWT_SECRET_KEY'), True)
    else:
        return 'User not found', 404


@server.route('/validate', methods=['POST'])
def validate():
    encoded_jwt = request.headers['Authorization']
    if not encoded_jwt:
        return 'Missing credentials in validate', 401

    encoded_jwt = encoded_jwt.split(" ")[1]
    try:
        decoded = jwt.decode(encoded_jwt, os.environ.get('JWT_SECRET_KEY'), algorithms=['HS256'])
        return decoded, 200
    except Exception as err:
        return f'Not authorized - {err}', 403


def create_jwt(username, secret, is_admin):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "admin": is_admin,
        },
        secret,
        algorithm="HS256",
    )


if __name__ == '__main__':
    server.run(host="0.0.0.0", port=5000, debug=True)
