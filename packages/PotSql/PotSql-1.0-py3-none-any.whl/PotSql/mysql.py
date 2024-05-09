import pymysql

# query for classical create table:
#   id int AUTO_INCREMENT, name varchar(255), email varchar(255), age int, PRIMARY KEY (id);

# source - (column, element)
# end_output - (bool_output, bool_end_output, table)

class mysql():
    def __init__(self, host, user, password, database, port=3306, debug=(False, None)):
        self.debug = debug
        self.connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()

    def execute(self, query):
        self.cursor.execute(query)

    def fget(self):
        return self.cursor.fetchall()

    def apply(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

    def createTable(self, table, query):
        query = f"CREATE TABLE {table}({query});"
        self.cursor.execute(query)

    def createTableAuto(self, table, **values):
        sp = None
        query = f"CREATE TABLE {table}("
        for e in values.keys():
            if values[e] == 'IDcONSTsTRINGtYPE' and sp != None:
                return 'error'

            elif values[e] == 'IDcONSTsTRINGtYPE' and sp == None:
                query += f"{e} int(255) AUTO_INCREMENT, "
                sp = e

            elif values[e] == 'int' or values[e] == 'integer':
                query += f"{e} int(255), "

            elif values[e] == 'float':
                query += f"{e} float, "

            elif values[e] == 'str' or values[e] == 'string':
                query += f"{e} varchar(255), "

            else:
                return 'error'

        if sp != None:
            query += f"PRIMARY KEY ({sp}));"
        else:
            query = query[:-2] + ");"

        # print(query)
        self.cursor.execute(query)

    def clearTable(self, table):
        self.cursor.execute(f"TRUNCATE {table}")

    def destroyTable(self, table):
        self.cursor.execute(f"DROP TABLE {table};")

    def addRow(self, table, **new_values):
        # INSERT INTO `tl` (`id`, `firstname`, `lastname`, `age`, `lovenum`) VALUES (NULL, 'fre', 'fre', '32', '1.5');

        keys = ", ".join([str(i) for i in new_values.keys()])
        values = ", ".join(["'" + str(i) + "'" for i in new_values.values()])

        self.cursor.execute(f"INSERT INTO {table} ({keys}) VALUES ({values})")

    def destroyRow(self, table, source=("id", 1)):
        self.cursor.execute(f"DELETE FROM {table} WHERE {table}.{source[0]} = '{source[1]}';")

    def screach(self, table, source=("id", 1), column_screach=None):
        self.cursor.execute(f"SELECT * FROM {table} WHERE {source[0]}='{source[1]}';")

        inputp = self.cursor.fetchall()
        if inputp == (): return None
        inputp = inputp[0]

        if column_screach != None and column_screach in inputp:
            return inputp[column_screach]
        else:
            return inputp

    def change(self, table, column, new_value, source=("id", 1)):
        query = f"UPDATE {table} SET {column} = '{new_value}' WHERE {table}.{source[0]} = '{source[1]}'"
        self.cursor.execute(query)

    def feturnTable(self, table, beautiful_view=False):
        self.cursor.execute(f"SELECT * FROM {table}")
        return_data = self.cursor.fetchall()

        if return_data == (): return None

        if len(return_data) > 1:
            if beautiful_view:
                for i in return_data:
                    print(i)
            else:
                return return_data

        elif len(return_data) == 1:
            if beautiful_view:
                print(return_data[0])
            else:
                return return_data[0]

        else:
            return 'error'

    def feturnColumn(self, table, name_column):
        self.cursor.execute(f"SELECT {name_column} FROM {table}")
        return_data = self.cursor.fetchall()
        feturn_data = []

        for i in return_data: feturn_data.append(i[name_column])
        return feturn_data

    def __del__(self):
        if self.debug[0]:
            self.feturnTable(self.debug[1], True)

        self.connection.close()
