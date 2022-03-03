import sqlite3


class DataBase(object):
	"""docstring for ClassName"""
	def __init__(self, database_file):
		"""Подключение и курсор"""
		self.connection = sqlite3.connect(database_file)
		self.cursor = self.connection.cursor()

	def write_to_db(self, user_id, first_name):
		with self.connection:
			return self.cursor.execute("INSERT INTO Users_Info ('user_id', 'first_name', 'status') VALUES (?, ?, ?)", (user_id, first_name, 100))

	def change_status(self, user_id, stc, first_name):
		with self.connection:
			if self.check_user(user_id):
				if self.cursor.execute("SELECT status FROM Users_Info WHERE user_id = {}".format(user_id)).fetchall()[0][0] + stc > 100:
					return self.cursor.execute("UPDATE Users_Info SET status = 100 WHERE user_id = {}".format(user_id))
				elif self.cursor.execute("SELECT status FROM Users_Info WHERE user_id = {}".format(user_id)).fetchall()[0][0] + stc < 1:
					return self.cursor.execute("UPDATE Users_Info SET status = 1 WHERE user_id = {}".format(user_id))
				else:
					return self.cursor.execute("UPDATE Users_Info SET status = status + {} WHERE user_id = {}".format(stc, user_id))
			else:
				self.write_to_db(user_id, first_name)

	def check_user(self, user_id):
		with self.connection:
			return self.cursor.execute("SELECT * FROM Users_Info WHERE user_id = {}".format(user_id)).fetchall()

	def check_status(self, user_id):
		with self.connection:
			return self.cursor.execute("SELECT status FROM Users_Info WHERE user_id = {}".format(user_id)).fetchall()
