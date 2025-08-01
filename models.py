from flask_login import UserMixin
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app

# Dummy db object for init_app
class db:
    @staticmethod
    def init_app(app):
        pass


from flask import current_app
import MySQLdb

class User(UserMixin):
    def __init__(self, id, username, password_hash, role):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.role = role

    @staticmethod
    def get_by_id(user_id):
        conn = MySQLdb.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            passwd=current_app.config['MYSQL_PASSWORD'],
            db=current_app.config['MYSQL_DB']
        )
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password_hash, role FROM users WHERE id = %s", (user_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return User(*row)
        return None

    @staticmethod
    def authenticate(username, password):
        conn = MySQLdb.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            passwd=current_app.config['MYSQL_PASSWORD'],
            db=current_app.config['MYSQL_DB']
        )
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password_hash, role FROM users WHERE username = %s", (username,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row and row[2] == password:
            return User(*row)
        return None


class Notification:
    @staticmethod
    def get_all():
        conn = MySQLdb.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            passwd=current_app.config['MYSQL_PASSWORD'],
            db=current_app.config['MYSQL_DB']
        )
        cursor = conn.cursor()
        cursor.execute("SELECT message FROM notifications ORDER BY created_at DESC")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [row[0] for row in rows]


class ExamResult:
    @staticmethod
    def get_by_user(user_id):
        conn = MySQLdb.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            passwd=current_app.config['MYSQL_PASSWORD'],
            db=current_app.config['MYSQL_DB']
        )
        cursor = conn.cursor()
        cursor.execute("SELECT subject, marks, grade, exam_date FROM exam_results WHERE user_id = %s", (user_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [f"{row[0]}: {row[1]} marks, Grade {row[2]}, Date {row[3]}" for row in rows]


class Timetable:
    @staticmethod
    def get_by_user(user_id):
        conn = MySQLdb.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            passwd=current_app.config['MYSQL_PASSWORD'],
            db=current_app.config['MYSQL_DB']
        )
        cursor = conn.cursor()
        cursor.execute("SELECT day_of_week, subject, start_time, end_time FROM timetable WHERE user_id = %s", (user_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [f"{row[0]}: {row[1]} ({row[2]} - {row[3]})" for row in rows]
