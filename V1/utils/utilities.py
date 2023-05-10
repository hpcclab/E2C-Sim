import sys
# Initializes schemas utilizing given docstring
# createSchema(Cursor, Connection, [str])
def createSchema(cur, conn, schemas):
    if type(schemas) is not list: schemas = [schemas]

    for schema in schemas: cur.execute(schema)
    conn.commit()

# Fetches data from .csv and converts to list of tuples
# [(str)] fromCSV(str)
def fromCSV(file_path):
    data = []

    with open(file_path, 'r') as file:
        next(file)
        lines = file.readlines()

        for line in lines:
            line = line.replace('\n', '')
            line_parsed = line.split(',')
            data.append(tuple(line_parsed))

    return data

# Takes tuples and inserts them into a table
# insertData(Cursor, Connection, [(str)], str)
def insertData(cur, conn, data, table):
    if type(data) is not list: data = [data]

    attributes = fetchAttributes(cur, table)

    # Need a string of '?'s for each attribute
    q_string = '('
    for _ in attributes: q_string = q_string + '?, '
    q_string = q_string[:-2] + ')'

    # ***
    # print(f'(utilities.py) *** {table} ***')
    # print(f'(utilities.py) attributes: {attributes}')
    # print(f'(utilities.py) q_string: {q_string}')
    # print(f'(utilities.py) data: {data}')

    # Ignores repetitive data
    # if table == "eet" and len(data) > 4: #i dont know why empty tuples are being entered only into the eet table but none else ??
    #     data.pop(8)                     #this is only a temporary solution for exactly 4 task types until i can dynamically remove empty tuples
    #     data.pop(6)
    #     data.pop(4)
    #     data.pop(2)
    #     data.pop(0)
    try:
        cur.executemany(
            f'INSERT OR IGNORE INTO {table} ' \
            f'{attributes} ' \
            f'VALUES {q_string};', data
        )
    except:
        print(table)
        print(data)
        print(attributes)
        print(q_string)
        sys.exit()
    conn.commit()

# Returns tuple of attributes from given table
# (str) fetchAttributes(Cursor, str)
def fetchAttributes(cur, table):
    cur.execute(f'PRAGMA table_info({table});')
    raw_info = cur.fetchall()

    attributes = ()
    for tuple in raw_info: attributes = attributes + (tuple[1],)

    return attributes

# printTable(Cursor, str)
def printTable(cur, table):
    cur.execute(f'SELECT * FROM {table} LIMIT 10;')
    print(cur.fetchall())
    print('...')

# deleteTables(Cursor, Connection, [str])
def deleteTables(cur, conn, tables):
    if type(tables) is not list: tables = [tables]

    # ***
    # print(f'(utilities.py) tables: {tables}')

    for table in tables:
        cur.execute(f'DROP TABLE IF EXISTS {table};')
        conn.commit()