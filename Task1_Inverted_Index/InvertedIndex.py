import string
from collections import defaultdict
from CleanBooks import *
import numpy as np
import os

def normalize_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = ' '.join(text.split())
    return text

def inverted_index_from_files_with_count(books_directory):
    inverted_index = defaultdict(lambda: defaultdict(int))

    for filename in os.listdir(books_directory):
        if filename.endswith(".txt"):
            doc_id = os.path.splitext(filename)[0]
            file_path = os.path.join(books_directory, filename)

            with open(file_path, 'r', encoding='utf-8') as file:
                document = file.read()
                normalized_document = normalize_text(document)
                words = normalized_document.split()
                
                for word in words:
                    inverted_index[word][doc_id] += 1
    
    return inverted_index

