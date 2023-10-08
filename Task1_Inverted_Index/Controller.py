from InvertedIndex import *
from CleanBooks import *
import subprocess
from DatabaseWriter import *
from JsonWriter import *

class Controller:

    def __init__(self):
        self.databaseWriter = DatabaseWriter()


    def get_clean_books(path):    
        list_books = get_files(path)
        list_books_for_processing, list_books = get_books_to_process(list_books)
        process_books(list_books_for_processing, list_books)

    def inverted_index(path_to_index_content):
        return inverted_index_from_files_with_count(path_to_index_content)
    

    def start_sqlite_datamart(self):
        self.databaseWriter.create_table()
        inverted_index = self.get_index_from_books()
        self.databaseWriter.add_columns(inverted_index)
        self.databaseWriter.insert_data(inverted_index)
    
    def start_json_datamart(self):
        inverted_index = self.get_index_from_books()
        write_json(inverted_index)

    def get_index_from_books(self):
        path_to_clean = "Datalake/books"
        path_to_index_content = "Datalake/content"
        Controller.get_clean_books(path_to_clean)
        inverted_index = Controller.inverted_index(path_to_index_content)
        return inverted_index


    def activate_query():
        command = 'flask --app query_engine run'
        subprocess.run(command, shell=True)

