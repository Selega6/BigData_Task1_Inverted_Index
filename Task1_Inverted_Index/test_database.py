from Controller import Controller
from InvertedIndex import inverted_index_from_files_with_count
import pytest

@pytest.mark.benchmark(group='clean_books')
def test_clean_books(benchmark):
    def clean_books():
        path_to_clean = "Datalake/books"
        Controller.get_clean_books(path_to_clean)
    
    benchmark(clean_books)

@pytest.mark.benchmark(group='build_index')
def test_inverted_index(benchmark):
    def build_index():
        path_to_index_content = "Datalake/content"
        inverted_index_from_files_with_count(path_to_index_content)

    benchmark(build_index)

@pytest.mark.benchmark(group='db_management')
def test_database_management(benchmark):
    def database_management():
        try:
            Controller().start_sqlite_datamart()
        except Exception as e:
            print(f"Error during database insertion: {str(e)}")

    benchmark(database_management)

if __name__ == '__main__':
    pytest.main()
