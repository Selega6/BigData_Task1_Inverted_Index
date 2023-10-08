import os

cut_words = ["and", "no", "the", "or", "i", "they", "is", "are", "you", "me", "he", "she", "it", "we", "us", "them", "a", "an", "of", "to", "in", "on", "for", "with", "at", "from", "by", "as", "but", "if", "so", "what", "when", "where", "how", "why", "that", "this", "these", "those", "my", "your", "his", "her", "its", "our", "their", "mine", "yours", "his", "hers", "ours", "theirs", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "will", "would", "shall", "should", "can", "could", "may", "might", "must", "ought", "need"]
punctuation_marks = [".", ",", ";", ":", '"', "'", "¿", "?", "¡", "!", "(", ")", "[", "]", "{", "}", "/", "\\", "-", "—", "–", "*", "&", "#", "%", "$", "€", "£", "¥", "~", "^", "=", "+", "-", "*", "/", "+"]
def get_files(path):
    files = []
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            files.append(file)
    return files

def read_document(file_name):
    with open(file_name, 'r', encoding= 'utf-8') as f:
        document = f.read()
    return document

def clean_text(content, cut_words, punctuation_marks):
    content = content.lower()
    text_list = content.split()
    for word in text_list:
        if word in cut_words or word in punctuation_marks:
            text_list.remove(word)
    result = ' '.join(text_list)
    return result

def get_books_to_process(list_books):
    list_books_for_processing = []
    list_processed = get_files("Datalake/content")
    for file in list_books:
        list_books_for_processing.append(file[-9:-4] + ".txt")   

    list_books_for_processing = list(set(list_books_for_processing) - set(list_processed))

    for book in list_books:
        if str(book[-9:-4] + '.txt') not in list_books_for_processing:
            list_books.remove(book)
    return list_books_for_processing, list_books

def process_books(list_books_for_processing, list_books):
    if len(list_books_for_processing) != 0:
        for libro in list_books:
            content = read_document("Datalake/books/" + libro)
            content = clean_text(content, cut_words, punctuation_marks)
            id = str(libro[-9:-4])
            with open("Datalake/Content/" + id + ".txt", "w", encoding= "utf-8") as f:
                f.write(content)
    else:
        print("No new files to process")
    return