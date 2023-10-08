from flask import Flask, request
app = Flask(__name__)
from flask import jsonify
from CleanBooks import *
from DatabaseWriter import *
from JsonWriter import *

@app.route("/", methods=['GET'])
def query_engine():

        return "Use /db or /dict to query the datamart"

@app.route("/db", methods=['GET'])
def query_engine_db():
    return(jsonify(get_words_db(process_query_params(), "datamart.db", "datamart", "word")))

@app.route("/dict", methods=['GET'])
def query_engine_dict():
    return(jsonify(get_words_dict(process_query_params(), "datamart.json")))

def get_info():
    list_files = get_files("Datalake/Metadata")
    list_of_dicts = []
    for file in list_files:
        list_of_dicts.append(json_to_dict(f"Datalake/Metadata/{file}"))
    return list_of_dicts

def get_words_db(word_list, database, table_name, primary_key_table):
    database_name = database[:-3]    
    conn, c = DatabaseWriter().connect_to_db()
    list_info = get_info()  
    c.execute(f"PRAGMA table_info({table_name})")
    dict_words = {}
    columns = c.fetchall()
    column_names = [column[1] for column in columns if column[1] != primary_key_table]
    retrieve_database_info(word_list, primary_key_table, database_name, c, list_info, dict_words, column_names)
    conn.close()
    
    return dict_words

def get_words_dict(word_list, json_file):
    dict_json = json_to_dict(json_file)
    list_info = get_info()
    dct = {key: dict_json[key] for key in word_list if key in dict_json}
    if not dct:
        return {}
    else:
        return retrieve_dict_info(dct, list_info)
    
def retrieve_dict_info(dict_filtered, list_info):
    dict_words = {}
    for word in dict_filtered.items():
        word_data = []
        for dict_info in list_info:
            if str(dict_info['id']) in word[1].keys():
                dict_doc = {}
                dict_doc['id'] = dict_info['id']
                dict_doc['title'] = dict_info['title']
                dict_doc['count'] = word[1][str(dict_info['id'])]
                word_data.append(dict_doc)
        dict_words[word[0]] = word_data
    return dict_words

def retrieve_database_info(word_list, primary_key_table, database_name, c, list_info, dict_words, column_names):
    for word in word_list:
        word_data = []
        for column in column_names:
            c.execute(f"SELECT {column} FROM {database_name} WHERE {primary_key_table} = ?", (word,))
            result = c.fetchall()
            if result and result[0][0] != 0:
                dict_doc = {}
                for dict_info in list_info:
                    if int(dict_info['id']) == int(column[1:]):
                        dict_doc['id'] = int(column[1:])
                        dict_doc['title'] = dict_info['title']
                        dict_doc['count'] = result[0][0]
                        word_data.append(dict_doc)
                    
        if word_data:
            dict_words[word] = word_data
            word_data = []

def process_query_params():
    search = request.args.get('search')
    search = search.lower()
    search = search.replace(",", "")
    list_of_words = search.split(" ")
    list_of_words = list(set(list_of_words))
    return list_of_words