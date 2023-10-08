from Controller import *

if __name__ == '__main__':
    Controller().start_sqlite_datamart()
    Controller().start_json_datamart()
    Controller.activate_query()