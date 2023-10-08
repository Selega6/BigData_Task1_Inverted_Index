from Controller import Controller
import pytest

@pytest.mark.benchmark(group='clean_books2')
def test_clean_books_performance(benchmark):
    def clean_books():
        path_to_clean = "Datalake/books"
        Controller.get_clean_books(path_to_clean)

    benchmark(clean_books)

@pytest.mark.benchmark(group='build_index2')
def test_inverted_index_performance(benchmark):
    def build_inverted_index():
        Controller().get_index_from_books()
    benchmark(build_inverted_index)

@pytest.mark.benchmark(group='json_datamart')
def test_JSON_datamart_performance(benchmark):
    def build_JSON_datamart():
        Controller().start_json_datamart()
    benchmark(build_JSON_datamart)

if __name__ == '__main__':
    pytest.main()
