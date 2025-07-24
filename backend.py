"Module handling database operations."

import sqlite3

creation_query = '''
    CREATE TABLE IF NOT EXISTS models(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_type VARCHAR(16) NOT NULL,
        manufacturer VARCHAR(16) NOT NULL,
        make VARCHAR(16),
        description VARCHAR(64) NOT NULL,
        year VARCHAR(4),
        scale VARCHAR(8) NOT NULL,
        condition VARCHAR(8) NOT NULL,
        quantity INTEGER NOT NULL,
        location VARCHAR(32) NOT NULL,
        estimate DOUBLE NOT NULL
    )
'''

# Initial database creation/connection.

database_file = 'test.db'

def create_database_connection():

    "Connection function needed before any changes or querying can be made."

    try:

        connection = sqlite3.connect(database_file)
        return connection
    except sqlite3.Error as error:
        print(f"Error connecting to database: {error}")
        return None


def create_table(creation_query):

    "Create database table if needed."

    try:
        connection = create_database_connection()
        cursor = connection.cursor()
        cursor.execute(creation_query)
        connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print(f"Error creating models table: {error}")


def execute_query(query, params=None):

    "Function to execute query on database, Bulk of calls to backend."

    try:
        connection = create_database_connection()
        cursor = connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()
        results = cursor.fetchall()
        cursor.close()
        #print(results)
        return results
    except sqlite3.Error as error:
        print(f"Error executing query: {error}")
        return None

def add_model(model_id, model_type, manufacturer, make, description, year, scale, condition, quantity, location, estimate):

    attribute_string = f"model_type, manufacturer, make, description, year, scale, condition, quantity, location, estimate"
    insertion_string = f"'{model_type}', '{manufacturer}', '{make}','{description}', '{year}', '{scale}', '{condition}', {quantity}, '{location}', {estimate}"

    if make == 'None' and year == 'None':
        
        attribute_string = f"model_type, manufacturer, description, scale, condition, quantity, location, estimate"
        insertion_string = f"'{model_type}', '{manufacturer}', '{description}', '{scale}', '{condition}', {quantity}, '{location}', {estimate}"

    elif make == 'None':
        
        attribute_string = f"model_type, manufacturer, description, year, scale, condition, quantity, location, estimate"
        insertion_string = f"'{model_type}', '{manufacturer}', '{description}', '{year}', '{scale}', '{condition}', {quantity}, '{location}', {estimate}"

    elif year == 'None':
        
        attribute_string = f"model_type, manufacturer, make, description, scale, condition, quantity, location, estimate"
        insertion_string = f"'{model_type}', '{manufacturer}', '{make}', '{description}', '{scale}', '{condition}', {quantity}, '{location}', {estimate}"      
    
    if model_id != '':
        
        attribute_string = 'id, ' + attribute_string
        insertion_string = f"{model_id}, " + insertion_string

    query = f"INSERT INTO models ({attribute_string}) VALUES ({insertion_string})"

    print(query)

    try:
        execute_query(query)
        return True
    except sqlite3.Error as error:
        print(f"Error inserting model: {error}")

# These need to be changed to reflect updated database schema.

def update_model(
    model_id,
    model_type=None,
    manufacturer=None,
    make=None,
    description=None,
    year=None,
    scale=None,
    condition=None,
    quantity=None,
    location=None,
    estimated_value=None
    ):

    "Function to update attributes of model."

    attr=["id", "model_type", "manufacturer", "make", "description", "year", "scale", "condition", "quantity", "location", "estimate"]
    attr_value=[model_id, model_type, manufacturer, make, description, year, scale, condition, quantity, location, estimated_value]
 
    print(model_id)

    query_values = []
    query_attr = []

    for i in range(len(attr)):
        if attr_value[i] != '':
            if attr[i] == 'year' or attr_value[i] == 'quantity':
                query_attr.append(attr[i])
                query_values.append(int(attr_value[i]))
            elif attr[i] == 'value':
                query_attr.append(attr[i])
                query_values.append(float(attr_value[i]))
            else:
                query_attr.append(attr[i])
                query_values.append(f"'{attr_value[i]}'")

    q = ", ".join([f"{a} = {b}" for a, b in zip(query_attr, query_values)])

    query=f"UPDATE models SET {q} WHERE id is {model_id}"

    print(query)

    try:
        return execute_query(query)
    except sqlite3.Error as error:
        print(f"Error deleting model: {error}")
        return None


def delete_model(model_id):

    "Function to delete model with given ID."
    
    query = f"DELETE FROM models WHERE id is {model_id}"

    try:
        execute_query(query)
        return True
    except sqlite3.Error as error:
        print(f"Error deleting model: {error}")
