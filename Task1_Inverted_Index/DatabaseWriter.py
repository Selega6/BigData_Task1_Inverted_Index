import sqlite3
from SqliteWriter import *

class DatabaseWriter:
    def __init__(self):
        self.conn = sqlite3.connect("datamart.db")
        self.c = self.conn.cursor()
        self.sql_writer = SqlWriter()

    def connect_to_db(self):
        conn = sqlite3.connect("datamart.db")
        c = conn.cursor()
        return conn, c

    datamart = '''CREATE TABLE IF NOT EXISTS datamart (
                        word TEXT PRIMARY KEY
                    )'''

    def create_table(self):
        try:
            self.c.execute(DatabaseWriter.datamart)
            self.c.execute("PRAGMA schema_version = 1") 
            print("The 'datamart' table has been created.")

        except sqlite3.Error as e:
            print("Error creating the table:", e)


    def delete_table(self, sql):
        self.c.execute(sql)

    def add_columns(self, index_content):
        try:
            self.c.execute("PRAGMA table_info(datamart)")
            columns_to_insert = list(self.sql_writer.insert_columns_of(list(self.extract_columns()), index_content))

            for column in columns_to_insert:
                self.c.execute(f"{column}")

            self.conn.commit()
        except sqlite3.Error as e:
            print("Error adding the columns:", e)

    def insert_data(self, index_content):
        try:
            self.c.execute("PRAGMA table_info(datamart)")
            data_to_insert = list(self.sql_writer.insert_data_into_table(list(self.extract_columns()), index_content))

            for word in data_to_insert:
                self.c.execute(f"{word[0]}", word[1])

            self.conn.commit()
        except sqlite3.Error as e:
            print("Error inserting the data:", e)


    def extract_columns(self):
        self.c.execute("PRAGMA table_info(datamart)")
        existing_columns = [column[1] for column in self.c.fetchall()]
        return existing_columns

