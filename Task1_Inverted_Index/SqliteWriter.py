class SqlWriter:

    def insert_columns_of(self, columns_db, index):
        column_names = self.get_columns_names(columns_db, index)
        sql_columns = self.prepare_columns_for_create_table(column_names)
        return list(self.add_columns_to_table(sql_columns))

    def add_columns_to_table(self, column_names):
            columns_insert = []
            for column_name in column_names:
                columns_insert.append(f"ALTER TABLE datamart ADD COLUMN {column_name}")

            return columns_insert

    def insert_data_into_table(self, columns_db, data):
            columns = columns_db
            output = []

            rows_to_insert = []
            for key, values in data.items():
                row = {"word": key}

                for column in columns[1:]:
                    column = column[1:]
                    row[column] = values.get(column, 0)

                rows_to_insert.append(row)

            for row in rows_to_insert:
                output.append([f"INSERT OR REPLACE INTO datamart ({', '.join(columns)}) VALUES ({', '.join(['?'] * len(columns))})", tuple(row.values())])
            return output

    def get_columns_names(self, columns_db, index):
            column_names = set()
            for _, ids in index.items():
                for id in ids:
                    column_names.add("_" + id)
            column_names -= set(columns_db)
            return list(column_names)

    def prepare_columns_for_create_table(self, columns_names):
            columns = set()
            for column_name in columns_names:
                columns.add(f"{column_name} INTEGER DEFAULT 0")
            return list(columns)
        